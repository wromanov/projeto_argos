"""Authorized, durable camera capture requests and HTTP worker execution."""

from __future__ import annotations

import os
import re
from hashlib import sha256
from uuid import uuid4

from asgiref.sync import async_to_sync
from django.conf import settings
from django.core.exceptions import PermissionDenied, ValidationError
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db import IntegrityError, transaction
from django.utils import timezone

from cameras.authorization import require_camera_permission
from cameras.integracao.capabilities import COMPATIBILITY_SUPPORTED, compatibility_status
from cameras.integracao.configuration import resolve_connection_config
from cameras.integracao.credentials import CredentialOperationError, resolve_active_credential_for_execution
from cameras.integracao.http_snapshot.adapter import (
    MAX_ATTEMPT_SECONDS,
    SUPPORTED_CONTENT_TYPES,
    HttpSnapshotAdapter,
    SnapshotCaptureError,
    SnapshotRequest,
)
from cameras.integracao.target_policy import TargetDecision, TargetPolicy, TargetPolicyError
from cameras.models import (
    Camera,
    CameraCaptureJob,
    CameraConnectionConfig,
    CameraImageRecord,
    CameraCapabilityProfile,
    EventoAuditoria,
)


_KEY_PATTERN = re.compile(r"\A[A-Za-z0-9._~-]{16,128}\Z")
_CONFIG_FIELDS = (
    "camera_id", "config_version", "credential_id", "profile_id", "enabled",
    "rtsp_uri", "http_endpoint_override", "http_port_override", "transport",
)
_ADAPTER_ERRORS = frozenset(CameraCaptureJob.ERROR_CODES) - {
    "AUTHORIZATION_DENIED", "CREDENTIAL_UNAVAILABLE", "STORAGE_ERROR", "INTERNAL_ERROR",
}


def request_camera_capture(
    *, actor, camera_id, idempotency_key=None, source_preference=None,
    target_policy=None, environment_allowed_ports=None,
):
    """Authorize, validate and durably enqueue one explicit HTTP capture."""
    require_camera_permission(
        actor=actor, permission_codename="capture_camera_image", camera_id=camera_id
    )
    key = uuid4().hex if idempotency_key is None else idempotency_key
    if not isinstance(key, str) or not _KEY_PATTERN.fullmatch(key):
        raise ValidationError("Chave de idempotência inválida.")
    existing = CameraCaptureJob.objects.filter(
        camera_id=camera_id, requestor=actor, idempotency_key=key
    ).first()
    if existing is not None:
        return existing
    if source_preference not in (None, CameraCaptureJob.Source.HTTP_SNAPSHOT):
        raise ValidationError("Fonte de captura não disponível nesta execução.")

    try:
        policy, allowed_ports = _runtime_policy(target_policy, environment_allowed_ports)
        config = _load_http_config(camera_id=camera_id, allowed_ports=allowed_ports)
        _require_supported_camera(config.camera, config.profile)
        _authorized_http_target(policy, config, allowed_ports)
    except (_CaptureFailure, TargetPolicyError, ValidationError):
        raise ValidationError("Câmera não elegível para captura.") from None

    try:
        with transaction.atomic():
            job = CameraCaptureJob.objects.create(
                camera=config.camera,
                requestor=actor,
                idempotency_key=key,
                source=CameraCaptureJob.Source.HTTP_SNAPSHOT,
                profile_key=config.profile.profile_key,
                profile_version=config.profile.version,
                config_version=config.config_version,
            )
            _audit_job(
                job, actor, "imagem.captura.solicitada", "Captura de imagem solicitada.",
                origin=EventoAuditoria.Origem.WEB,
            )
            return job
    except IntegrityError:
        # A concurrent identical request is resolved by the database constraint.
        return CameraCaptureJob.objects.get(
            camera_id=camera_id, requestor=actor, idempotency_key=key
        )


def run_next_capture(*, target_policy=None, environment_allowed_ports=None, adapter=None):
    """Claim and execute one queued job. Returns None when the queue is empty."""
    job_id = _claim_next_job()
    if job_id is None:
        return None
    job = CameraCaptureJob.objects.select_related("camera", "requestor").get(pk=job_id)
    try:
        require_camera_permission(
            actor=job.requestor,
            permission_codename="capture_camera_image",
            camera_id=job.camera_id,
        )
        if job.source != CameraCaptureJob.Source.HTTP_SNAPSHOT:
            raise _CaptureFailure("CAPABILITY_UNSUPPORTED")
        policy, allowed_ports = _runtime_policy(target_policy, environment_allowed_ports)
        config = _load_http_config(camera_id=job.camera_id, allowed_ports=allowed_ports)
        _require_job_config(job, config)
        _require_supported_camera(config.camera, config.profile)
        target = _authorized_http_target(policy, config, allowed_ports)

        credential = None
        if config.profile.auth_method == CameraCapabilityProfile.AuthMethod.NONE:
            if config.profile.credential_required or config.credential_id is not None:
                raise _CaptureFailure("CONFIG_INVALID")
        elif config.profile.auth_method in {
            CameraCapabilityProfile.AuthMethod.BASIC,
            CameraCapabilityProfile.AuthMethod.DIGEST,
        }:
            if target.request is None or target.request.scheme != "https" or config.credential_id is None:
                raise _CaptureFailure("CONFIG_INVALID")
            try:
                require_camera_permission(
                    actor=job.requestor,
                    permission_codename="capture_camera_image",
                    camera_id=job.camera_id,
                )
                credential = resolve_active_credential_for_execution(config=config)
            except PermissionDenied:
                raise
            except CredentialOperationError:
                raise _CaptureFailure("CREDENTIAL_UNAVAILABLE") from None
        else:
            raise _CaptureFailure("CAPABILITY_UNSUPPORTED")

        # Re-read after R1, and revalidate the target before the network port.
        current = _load_http_config(camera_id=job.camera_id, allowed_ports=allowed_ports)
        if _config_changed(config, current):
            raise _CaptureFailure("CONFIG_INVALID")
        target = _authorized_http_target(policy, current, allowed_ports)
        request = SnapshotRequest(
            target=target,
            auth_method=current.profile.auth_method,
            credential_required=current.profile.credential_required,
            allowed_content_types=SUPPORTED_CONTENT_TYPES,
            timeout_seconds=min(
                float(getattr(settings, "ARGOS_CAMERA_CAPTURE_TIMEOUT_SECONDS", MAX_ATTEMPT_SECONDS)),
                MAX_ATTEMPT_SECONDS,
            ),
        )
        snapshot_adapter = adapter or HttpSnapshotAdapter()
        try:
            snapshot = async_to_sync(snapshot_adapter.capture)(request, credential=credential)
        except SnapshotCaptureError as exc:
            if exc.code == "CREDENTIAL_MISSING":
                raise _CaptureFailure("CREDENTIAL_UNAVAILABLE") from None
            code = exc.code if exc.code in _ADAPTER_ERRORS else "INTERNAL_ERROR"
            raise _CaptureFailure(code) from None
        finally:
            credential = None

        observed_at = timezone.now()
        return _persist_success(
            job_id=job_id, camera=current.camera, requestor=job.requestor,
            snapshot=snapshot, captured_at=observed_at,
        )
    except PermissionDenied:
        return _finish_failure(job_id, "AUTHORIZATION_DENIED")
    except _CaptureFailure as exc:
        return _finish_failure(job_id, exc.code)
    except (ValidationError, TargetPolicyError, ValueError, TypeError, KeyError):
        return _finish_failure(job_id, "CONFIG_INVALID")
    except Exception:
        # Do not expose transport, storage, settings, or provider details.
        return _finish_failure(job_id, "INTERNAL_ERROR")


class _CaptureFailure(Exception):
    def __init__(self, code):
        self.code = code
        super().__init__(code)


def _claim_next_job():
    with transaction.atomic():
        job = CameraCaptureJob.objects.filter(status=CameraCaptureJob.Status.QUEUED).order_by("created_at", "pk").first()
        if job is None:
            return None
        now = timezone.now()
        changed = CameraCaptureJob.objects.filter(pk=job.pk, status=CameraCaptureJob.Status.QUEUED).update(
            status=CameraCaptureJob.Status.RUNNING,
            started_at=now,
        )
        return job.pk if changed == 1 else None


def _runtime_policy(target_policy, environment_allowed_ports):
    if target_policy is None:
        target_policy = TargetPolicy.from_environment(os.environ)
    if not isinstance(target_policy, TargetPolicy):
        raise _CaptureFailure("TARGET_DENIED")
    if environment_allowed_ports is None:
        environment_allowed_ports = {
            port for values in target_policy.ports_by_scheme.values() for port in values
        }
    try:
        allowed_ports = frozenset(environment_allowed_ports)
    except TypeError:
        raise _CaptureFailure("CONFIG_INVALID") from None
    if not allowed_ports or any(type(port) is not int or not 1 <= port <= 65535 for port in allowed_ports):
        raise _CaptureFailure("CONFIG_INVALID")
    return target_policy, allowed_ports


def _load_http_config(*, camera_id, allowed_ports):
    config = CameraConnectionConfig.objects.select_related("camera", "profile", "credential").filter(camera_id=camera_id).first()
    if config is None or not config.enabled or config.camera.situacao_operacional == Camera.SituacaoOperacional.DESATIVADA:
        raise _CaptureFailure("CONFIG_INVALID")
    if config.profile.adapter_key != CameraCapabilityProfile.Adapter.HTTP_SNAPSHOT:
        raise _CaptureFailure("CAPABILITY_UNSUPPORTED")
    try:
        resolved = resolve_connection_config(
            camera_id=camera_id, environment_allowed_ports=allowed_ports, automatic=False
        )
    except ValidationError:
        raise _CaptureFailure("CONFIG_INVALID") from None
    if resolved["compatibility"] != COMPATIBILITY_SUPPORTED:
        raise _CaptureFailure("CAPABILITY_UNSUPPORTED")
    return config


def _require_supported_camera(camera, profile):
    if not profile.active or compatibility_status(camera, profile) != COMPATIBILITY_SUPPORTED:
        raise _CaptureFailure("CAPABILITY_UNSUPPORTED")


def _require_job_config(job, config):
    if (
        config.profile.profile_key != job.profile_key
        or config.profile.version != job.profile_version
        or config.config_version != job.config_version
    ):
        raise _CaptureFailure("CONFIG_INVALID")


def _config_changed(before, after):
    return (
        before.camera.ip != after.camera.ip
        or before.profile.active != after.profile.active
        or before.profile.profile_key != after.profile.profile_key
        or before.profile.version != after.profile.version
        or before.profile.auth_method != after.profile.auth_method
        or before.profile.credential_required != after.profile.credential_required
        or before.profile.allowed_schemes != after.profile.allowed_schemes
        or before.profile.allowed_ports != after.profile.allowed_ports
        or any(getattr(before, field) != getattr(after, field) for field in _CONFIG_FIELDS)
    )


def _authorized_http_target(policy, config, allowed_ports):
    profile = config.profile
    resolved = resolve_connection_config(
        camera_id=config.camera_id, environment_allowed_ports=allowed_ports, automatic=False
    )
    path = resolved["http_endpoint_override"]
    if not path:
        raise _CaptureFailure("CONFIG_INVALID")
    schemes = tuple(profile.allowed_schemes)
    if profile.tls_policy == CameraCapabilityProfile.TLSPolicy.REQUIRED:
        schemes = tuple(scheme for scheme in schemes if scheme == "https")
    if config.credential_id is not None or profile.credential_required:
        schemes = tuple(scheme for scheme in schemes if scheme == "https")
    if not schemes:
        raise _CaptureFailure("CONFIG_INVALID")
    # One deterministic scheme per attempt: no scheme fallback or retry.
    scheme = "https" if "https" in schemes else schemes[0]
    port = resolved["http_port_override"]
    uri = f"{scheme}://{config.camera.ip}:{port}{path}"
    # The declared default path is profile-authorized even when overrides exist.
    # A different effective path still needs a separate TargetPolicy allowlist.
    allowed_paths = (profile.default_path,) if path == profile.default_path else None
    target = policy.validate(
        config.camera.ip or "", uri,
        allowed_schemes=(scheme,),
        allowed_ports=tuple(profile.allowed_ports),
        default_port=port,
        allowed_paths=allowed_paths,
        farm=getattr(config.camera, "farm", None),
    )
    if target.decision is TargetDecision.MISCONFIGURED_POLICY:
        raise _CaptureFailure("TARGET_DENIED")
    if not target.authorized or target.request is None:
        raise _CaptureFailure("TARGET_DENIED")
    return target


def _persist_success(*, job_id, camera, requestor, snapshot, captured_at):
    extension = {"JPEG": "jpg", "PNG": "png", "WEBP": "webp"}.get(snapshot.image_format)
    if extension is None or snapshot.content_type not in SUPPORTED_CONTENT_TYPES:
        return _finish_failure(job_id, "IMAGE_INVALID")
    storage_name = f"camera-images/{camera.pk}/{uuid4().hex}.{extension}"
    saved_key = None
    try:
        try:
            saved_key = default_storage.save(storage_name, ContentFile(snapshot.data))
        except Exception:
            raise _CaptureFailure("STORAGE_ERROR") from None
        with transaction.atomic():
            job = CameraCaptureJob.objects.select_for_update().get(pk=job_id)
            if job.status != CameraCaptureJob.Status.RUNNING:
                raise _CaptureFailure("INTERNAL_ERROR")
            record = CameraImageRecord(
                camera=camera,
                provenance=CameraImageRecord.Provenance.CAPTURA_CAMERA,
                captured_at=captured_at,
                recorded_at=timezone.now(),
                storage_key=saved_key,
                content_type=snapshot.content_type,
                size_bytes=len(snapshot.data),
                width=snapshot.width,
                height=snapshot.height,
                sha256=sha256(snapshot.data).hexdigest(),
                captured_by_system="IMG-CAP",
            )
            record.save()
            job.image_record = record
            job.status = CameraCaptureJob.Status.SUCCEEDED
            job.finished_at = timezone.now()
            job.save(update_fields=["image_record", "status", "finished_at"])
            _audit_job(
                job, requestor, "imagem.captura.concluida", "Captura de imagem concluída.",
                origin=EventoAuditoria.Origem.COMANDO,
            )
            return job
    except Exception:
        if saved_key is not None:
            try:
                default_storage.delete(saved_key)
            except Exception:
                pass
        raise


def _finish_failure(job_id, code):
    safe_code = code if code in CameraCaptureJob.ERROR_CODES else "INTERNAL_ERROR"
    with transaction.atomic():
        job = CameraCaptureJob.objects.select_for_update().filter(pk=job_id).first()
        if job is None or job.status != CameraCaptureJob.Status.RUNNING:
            return job
        job.status = CameraCaptureJob.Status.FAILED
        job.error_code = safe_code
        job.finished_at = timezone.now()
        job.save(update_fields=["status", "error_code", "finished_at"])
        _audit_job(
            job, job.requestor, "imagem.captura.falhou", "Captura de imagem não concluída.",
            error_code=safe_code, origin=EventoAuditoria.Origem.COMANDO,
        )
        return job


def _audit_job(job, actor, code, summary, *, error_code=None, origin):
    metadata = {"source": job.source, "status": job.status}
    if error_code:
        metadata["error_code"] = error_code
    from cameras.auditoria import registrar_evento

    registrar_evento(
        codigo=code,
        resumo=summary,
        categoria=EventoAuditoria.Categoria.CAMERA,
        usuario=actor,
        camera=job.camera,
        entidade=job,
        metadados=metadata,
        origem=origin,
    )
