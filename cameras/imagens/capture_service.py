"""Authorized, durable camera capture requests and HTTP worker execution."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from io import BytesIO
import os
import re
from hashlib import sha256
from urllib.parse import urlsplit
from uuid import uuid4

from asgiref.sync import async_to_sync
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied, ValidationError
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db import DEFAULT_DB_ALIAS, IntegrityError, OperationalError, connections, transaction
from django.utils import timezone
from PIL import Image

from cameras.authorization import require_camera_permission
from cameras.integracao.capabilities import COMPATIBILITY_SUPPORTED, compatibility_status
from cameras.integracao.compatibility import UNSUPPORTED as COMPATIBILITY_UNSUPPORTED
from cameras.integracao.compatibility import UNVERIFIED as COMPATIBILITY_UNVERIFIED
from cameras.integracao.configuration import resolve_connection_config
from cameras.integracao.credentials import CredentialOperationError, resolve_active_credential_for_execution
from cameras.integracao.http_snapshot.adapter import (
    MAX_ATTEMPT_SECONDS,
    SUPPORTED_CONTENT_TYPES,
    HttpSnapshotAdapter,
    SnapshotImage,
    SnapshotCaptureError,
    SnapshotRequest,
)
from cameras.integracao.target_policy import TargetDecision, TargetPolicy, TargetPolicyError
from cameras.integracao.rtsp.fake import FakeRtspAdapter
from cameras.integracao.rtsp.ports import RtspConnectionRequest, RtspFrameError, RtspJpegFrame
from cameras.models import (
    Camera,
    CameraCaptureJob,
    CameraConnectionConfig,
    CameraImageRecord,
    CameraCapabilityProfile,
    CameraCredentialVersion,
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
ACTIVE_CAPTURE_STATUSES = (CameraCaptureJob.Status.QUEUED, CameraCaptureJob.Status.RUNNING)


@dataclass(frozen=True)
class CaptureEligibility:
    """Safe factual classification for the authorized Camera Detail projection."""

    state: str
    source_preference: str | None = None

    @property
    def available(self):
        return self.state == "AVAILABLE"


def capture_eligibility(*, actor, camera):
    """Classify only backend facts that are safe to present to a capture-authorized user."""
    require_camera_permission(
        actor=actor,
        permission_codename="capture_camera_image",
        camera_id=camera.pk,
    )

    config = CameraConnectionConfig.objects.select_related("camera", "profile").filter(
        camera_id=camera.pk
    ).first()
    if (
        config is None
        or not config.enabled
        or config.camera.situacao_operacional == Camera.SituacaoOperacional.DESATIVADA
        or not config.profile.active
    ):
        return CaptureEligibility("CONFIGURATION_INCOMPLETE")

    profile = config.profile
    compatibility = compatibility_status(camera, profile)
    if compatibility == COMPATIBILITY_UNSUPPORTED:
        return CaptureEligibility("METHOD_UNSUPPORTED")
    if compatibility == COMPATIBILITY_UNVERIFIED:
        return CaptureEligibility("CAPABILITY_UNVERIFIED")
    if compatibility != COMPATIBILITY_SUPPORTED:
        return CaptureEligibility("UNCLASSIFIED")

    # The active-camera invariant is a conditional unique constraint. Fail closed
    # on engines that cannot enforce it; a UI-only check is not sufficient.
    if not connections[DEFAULT_DB_ALIAS].features.supports_partial_indexes:
        return CaptureEligibility("UNCLASSIFIED")

    try:
        policy, allowed_ports = _runtime_policy(None, None)
        if profile.adapter_key == CameraCapabilityProfile.Adapter.RTSP:
            current = _load_rtsp_config(camera_id=camera.pk, policy=policy, allowed_ports=allowed_ports)
            _authorized_rtsp_target(policy, current, allowed_ports)
            # The P1 GStreamer adapter can follow an RTSP redirect before the
            # application observes its bus message. Until an egress guard is
            # implemented and validated, the web capture action stays disabled.
            return CaptureEligibility("RTSP_NOT_HOMOLOGATED")
        if profile.adapter_key != CameraCapabilityProfile.Adapter.HTTP_SNAPSHOT:
            return CaptureEligibility("METHOD_UNSUPPORTED")
        resolved = _load_http_config(camera_id=camera.pk, allowed_ports=allowed_ports)
        _authorized_http_target(policy, resolved, allowed_ports)
    except (_CaptureFailure, TargetPolicyError, ValidationError, ValueError, TypeError, KeyError):
        # These errors can include security policy and secret-resolution details.
        # No narrower public category is claimed from a generic failure.
        return CaptureEligibility("UNCLASSIFIED")
    return CaptureEligibility("AVAILABLE", CameraCaptureJob.Source.HTTP_SNAPSHOT)


def request_camera_capture(
    *, actor, camera_id, idempotency_key=None, source_preference=None,
    target_policy=None, environment_allowed_ports=None,
):
    """Authorize, validate and durably enqueue one capture from the chosen source."""
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
    if CameraCaptureJob.objects.filter(camera_id=camera_id, status__in=ACTIVE_CAPTURE_STATUSES).exists():
        raise ValidationError("Já existe uma captura em andamento para esta câmera.")
    if source_preference not in (None, CameraCaptureJob.Source.HTTP_SNAPSHOT, CameraCaptureJob.Source.RTSP_FRAME):
        raise ValidationError("Fonte de captura não disponível nesta execução.")

    try:
        policy, allowed_ports = _runtime_policy(target_policy, environment_allowed_ports)
        configured = CameraConnectionConfig.objects.select_related("camera", "profile").filter(
            camera_id=camera_id
        ).first()
        if configured is None:
            raise _CaptureFailure("CONFIG_INVALID")
        expected_source = (
            CameraCaptureJob.Source.RTSP_FRAME
            if configured.profile.adapter_key == CameraCapabilityProfile.Adapter.RTSP
            else CameraCaptureJob.Source.HTTP_SNAPSHOT
            if configured.profile.adapter_key == CameraCapabilityProfile.Adapter.HTTP_SNAPSHOT
            else None
        )
        source = (
            CameraCaptureJob.Source.RTSP_FRAME
            if source_preference is None
            else source_preference
        )
        if expected_source is None or source != expected_source:
            raise _CaptureFailure("CAPABILITY_UNSUPPORTED")
        if source == CameraCaptureJob.Source.RTSP_FRAME:
            config = _load_rtsp_config(camera_id=camera_id, policy=policy, allowed_ports=allowed_ports)
            _require_supported_camera(config.camera, config.profile)
            _authorized_rtsp_target(policy, config, allowed_ports)
        else:
            config = _load_http_config(camera_id=camera_id, allowed_ports=allowed_ports)
            _require_supported_camera(config.camera, config.profile)
            _authorized_http_target(policy, config, allowed_ports)
    except (_CaptureFailure, TargetPolicyError, ValidationError):
        raise ValidationError("Câmera não elegível para captura.") from None

    if not connections[DEFAULT_DB_ALIAS].features.supports_partial_indexes:
        raise ValidationError("Captura não disponível nesta configuração do sistema.")

    try:
        with transaction.atomic():
            job = CameraCaptureJob.objects.create(
                camera=config.camera,
                requestor=actor,
                idempotency_key=key,
                source=source,
                profile_key=config.profile.profile_key,
                profile_version=config.profile.version,
                config_version=config.config_version,
            )
            _audit_job(
                job, actor, "imagem.captura.solicitada", "Captura de imagem solicitada.",
                origin=EventoAuditoria.Origem.WEB,
            )
            return job
    except IntegrityError as exc:
        # The database constraints arbitrate both a repeated idempotency key and
        # distinct simultaneous intents for the same camera.
        return _resolve_capture_creation_conflict(
            camera_id=camera_id, actor=actor, key=key, error=exc
        )
    except OperationalError as exc:
        # SQLite shared-cache connections may report a write-lock race before
        # evaluating the conditional unique index. Fail closed without retrying
        # or issuing a read that could block behind the competing transaction.
        if (
            connections[DEFAULT_DB_ALIAS].vendor != "sqlite"
            or "locked" not in str(exc).casefold()
        ):
            raise
        raise ValidationError("Não foi possível registrar a captura agora.") from None


def _resolve_capture_creation_conflict(*, camera_id, actor, key, error):
    existing = CameraCaptureJob.objects.filter(
        camera_id=camera_id, requestor=actor, idempotency_key=key
    ).first()
    if existing is not None:
        return existing
    if CameraCaptureJob.objects.filter(camera_id=camera_id, status__in=ACTIVE_CAPTURE_STATUSES).exists():
        raise ValidationError("Já existe uma captura em andamento para esta câmera.") from None
    raise error


def camera_capture_available(*, actor, camera):
    """Return whether this actor may enqueue a currently supported capture."""
    try:
        return capture_eligibility(actor=actor, camera=camera).available
    except (PermissionDenied, _CaptureFailure, TargetPolicyError, ValidationError, ValueError, TypeError, KeyError):
        return False


def run_next_capture(*, target_policy=None, environment_allowed_ports=None, adapter=None, rtsp_adapter=None):
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
        if job.source == CameraCaptureJob.Source.RTSP_FRAME:
            return _run_next_rtsp_capture(
                job=job,
                target_policy=target_policy,
                environment_allowed_ports=environment_allowed_ports,
                rtsp_adapter=rtsp_adapter,
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


def _run_next_rtsp_capture(*, job, target_policy, environment_allowed_ports, rtsp_adapter):
    # This is deliberately a test-only seam. Production worker callers do not
    # provide an RTSP extractor until redirect and egress controls are proven.
    if type(rtsp_adapter) is not FakeRtspAdapter:
        raise _CaptureFailure("CAPABILITY_UNSUPPORTED")

    policy, allowed_ports = _runtime_policy(target_policy, environment_allowed_ports)
    config = _load_rtsp_config(camera_id=job.camera_id, policy=policy, allowed_ports=allowed_ports)
    _require_job_config(job, config)
    _require_supported_camera(config.camera, config.profile)
    target = _authorized_rtsp_target(policy, config, allowed_ports)

    credential = None
    if config.profile.auth_method == CameraCapabilityProfile.AuthMethod.NONE:
        if config.profile.credential_required or config.credential_id is not None:
            raise _CaptureFailure("CONFIG_INVALID")
    elif config.profile.auth_method == CameraCapabilityProfile.AuthMethod.RTSP_NEGOTIATE:
        if config.profile.credential_required and config.credential_id is None:
            raise _CaptureFailure("CREDENTIAL_UNAVAILABLE")
        if config.credential_id is not None:
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

    try:
        current = _load_rtsp_config(
            camera_id=job.camera_id, policy=policy, allowed_ports=allowed_ports
        )
        _require_job_config(job, current)
        if _config_changed(config, current):
            raise _CaptureFailure("CONFIG_INVALID")
        _require_supported_camera(current.camera, current.profile)
        target = _authorized_rtsp_target(policy, current, allowed_ports)
        timeout_seconds = min(
            15.0,
            float(getattr(settings, "ARGOS_CAMERA_CAPTURE_TIMEOUT_SECONDS", 15.0)),
        )
        request = RtspConnectionRequest(
            camera_id=current.camera_id,
            target=target.request,
            timeout_seconds=timeout_seconds,
            connect_timeout_seconds=min(3.0, timeout_seconds),
            transport=current.transport,
            credential=credential,
        )
        _require_running_job(job.pk)
        try:
            frame = rtsp_adapter.extract_one_jpeg_frame(request)
        except RtspFrameError as exc:
            raise _CaptureFailure(_RTSP_ERROR_MAP[exc.code]) from None
        snapshot = _validated_rtsp_snapshot(frame)
        _require_running_job(job.pk)
        return _persist_success(
            job_id=job.pk,
            camera=current.camera,
            requestor=job.requestor,
            snapshot=snapshot,
            captured_at=frame.observed_at,
        )
    finally:
        # Resolved secrets live only for this synchronous attempt.
        credential = None


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


def _load_rtsp_config(*, camera_id, policy, allowed_ports):
    config = CameraConnectionConfig.objects.select_related(
        "camera", "profile", "credential", "credential__active_version"
    ).filter(camera_id=camera_id).first()
    if (
        config is None
        or not config.enabled
        or config.camera.situacao_operacional == Camera.SituacaoOperacional.DESATIVADA
    ):
        raise _CaptureFailure("CONFIG_INVALID")
    if (
        config.profile.adapter_key != CameraCapabilityProfile.Adapter.RTSP
        or not config.profile.active
    ):
        raise _CaptureFailure("CAPABILITY_UNSUPPORTED")
    if config.profile.auth_method == CameraCapabilityProfile.AuthMethod.NONE:
        if config.profile.credential_required or config.credential_id is not None:
            raise _CaptureFailure("CONFIG_INVALID")
    elif config.profile.auth_method == CameraCapabilityProfile.AuthMethod.RTSP_NEGOTIATE:
        credential = config.credential
        if config.profile.credential_required and credential is None:
            raise _CaptureFailure("CREDENTIAL_UNAVAILABLE")
        if credential is not None:
            try:
                active_version = credential.active_version
            except ObjectDoesNotExist:
                active_version = None
            if (
                credential.camera_id != config.camera_id
                or credential.state != "ACTIVE"
                or credential.active_version_id is None
                or active_version is None
                or active_version.state != CameraCredentialVersion.State.ACTIVE
            ):
                raise _CaptureFailure("CREDENTIAL_UNAVAILABLE")
    else:
        raise _CaptureFailure("CAPABILITY_UNSUPPORTED")
    policy_ports = frozenset(policy.ports_by_scheme.get("rtsp", ()))
    effective_ports = frozenset(allowed_ports) & policy_ports
    if not effective_ports:
        raise _CaptureFailure("TARGET_DENIED")
    try:
        resolved = resolve_connection_config(
            camera_id=camera_id, environment_allowed_ports=effective_ports, automatic=False
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
        or before.profile.adapter_key != after.profile.adapter_key
        or before.profile.active != after.profile.active
        or before.profile.profile_key != after.profile.profile_key
        or before.profile.version != after.profile.version
        or before.profile.default_path != after.profile.default_path
        or before.profile.endpoint_policy != after.profile.endpoint_policy
        or before.profile.allowed_override_fields != after.profile.allowed_override_fields
        or before.profile.tls_policy != after.profile.tls_policy
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


def _authorized_rtsp_target(policy, config, allowed_ports):
    profile = config.profile
    resolved = resolve_connection_config(
        camera_id=config.camera_id,
        environment_allowed_ports=frozenset(allowed_ports)
        & frozenset(policy.ports_by_scheme.get("rtsp", ())),
        automatic=False,
    )
    uri = resolved["rtsp_uri"]
    if not uri.startswith("rtsp://"):
        raise _CaptureFailure("CONFIG_INVALID")
    allowed_ports_for_target = tuple(
        sorted(frozenset(profile.allowed_ports) & frozenset(allowed_ports)
               & frozenset(policy.ports_by_scheme.get("rtsp", ())))
    )
    if not allowed_ports_for_target:
        raise _CaptureFailure("TARGET_DENIED")
    path = urlsplit(uri).path
    policy_paths = tuple(policy.allowed_paths_by_scheme.get("rtsp", ()))
    if not policy_paths:
        raise _CaptureFailure("TARGET_DENIED")
    allowed_paths = (profile.default_path,) if path == profile.default_path else None
    target = policy.validate(
        config.camera.ip or "",
        uri,
        allowed_schemes=("rtsp",),
        allowed_ports=allowed_ports_for_target,
        default_port=554 if 554 in profile.allowed_ports else (
            profile.allowed_ports[0] if len(profile.allowed_ports) == 1 else None
        ),
        allowed_paths=allowed_paths,
        farm=getattr(config.camera, "farm", None),
    )
    if target.decision is TargetDecision.MISCONFIGURED_POLICY:
        raise _CaptureFailure("TARGET_DENIED")
    if not target.authorized or target.request is None:
        raise _CaptureFailure("TARGET_DENIED")
    return target


_RTSP_ERROR_MAP = {
    "INVALID_REQUEST": "CONFIG_INVALID",
    "TARGET_BLOCKED": "TARGET_DENIED",
    "UNAUTHORIZED_REDIRECT": "TARGET_DENIED",
    "CREDENTIAL_UNAVAILABLE": "CREDENTIAL_UNAVAILABLE",
    "AUTH_FAILURE": "AUTH_FAILURE",
    "CODEC_UNAVAILABLE": "CAPABILITY_UNSUPPORTED",
    "DECODE_FAILED": "IMAGE_INVALID",
    "ENCODE_FAILED": "IMAGE_INVALID",
    "INVALID_SAMPLE": "IMAGE_INVALID",
    "LIMIT_EXCEEDED": "BODY_TOO_LARGE",
    "TIMEOUT": "READ_TIMEOUT",
    "CANCELLED": "INTERNAL_ERROR",
    "TEARDOWN_FAILED": "INTERNAL_ERROR",
    "RUNTIME_ERROR": "INTERNAL_ERROR",
}


def _validated_rtsp_snapshot(frame):
    if not isinstance(frame, RtspJpegFrame):
        raise _CaptureFailure("IMAGE_INVALID")
    data = frame.jpeg_bytes
    if (
        not isinstance(data, bytes)
        or not data
        or len(data) > 5 * 1024 * 1024
        or not data.startswith(b"\xff\xd8")
        or not data.endswith(b"\xff\xd9")
        or type(frame.width) is not int
        or type(frame.height) is not int
        or not 0 < frame.width <= 1920
        or not 0 < frame.height <= 1080
        or frame.width * frame.height > 2_073_600
        or frame.media_type != "image/jpeg"
        or frame.codec not in {"H264", "H265"}
        or not isinstance(frame.observed_at, datetime)
        or frame.observed_at.tzinfo is None
        or frame.observed_at.utcoffset() is None
    ):
        raise _CaptureFailure("IMAGE_INVALID")
    try:
        with Image.open(BytesIO(data)) as image:
            if image.format != "JPEG" or image.size != (frame.width, frame.height):
                raise _CaptureFailure("IMAGE_INVALID")
            image.load()
    except _CaptureFailure:
        raise
    except Exception:
        raise _CaptureFailure("IMAGE_INVALID") from None
    return SnapshotImage(data, "image/jpeg", "JPEG", frame.width, frame.height)


def _require_running_job(job_id):
    if not CameraCaptureJob.objects.filter(
        pk=job_id, status=CameraCaptureJob.Status.RUNNING
    ).exists():
        raise _CaptureFailure("INTERNAL_ERROR")


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
