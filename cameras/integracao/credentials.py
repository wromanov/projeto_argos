"""Credential lifecycle use cases; secret material stays behind Fernet."""

import json
from dataclasses import dataclass, field

from cryptography.fernet import Fernet, InvalidToken
from django.contrib.auth import authenticate
from django.core.exceptions import PermissionDenied, ValidationError
from django.db import transaction
from django.db.models import Max
from django.utils import timezone

from cameras.authorization import require_camera_permission
from cameras.models import (
    Camera,
    CameraConnectionConfig,
    CameraCredential,
    CameraCredentialVersion,
    EventoAuditoria,
)

from .key_provider import CredentialKeyError, get_environment_key_provider

_PAYLOAD_SCHEMA_VERSION = 1
_USERNAME_MAX_LENGTH = 255
_PASSWORD_MAX_LENGTH = 1024


class CredentialOperationError(Exception):
    """Safe operation failure whose string representation contains only a code."""

    def __init__(self, code):
        self.code = code
        super().__init__(code)


@dataclass(frozen=True)
class ResolvedCameraCredential:
    """Ephemeral credentials for one authorized in-memory connection attempt."""

    username: str = field(repr=False)
    password: str = field(repr=False)

    def __str__(self):
        return "ResolvedCameraCredential(<redacted>)"

    def __reduce_ex__(self, protocol):
        raise TypeError("ResolvedCameraCredential cannot be serialized.")


def _provider(provider):
    return provider if provider is not None else get_environment_key_provider()


def _validate_secret(username, password):
    if not isinstance(username, str) or not isinstance(password, str):
        raise ValidationError("Username e senha devem ser texto.")
    if not username or len(username) > _USERNAME_MAX_LENGTH:
        raise ValidationError("Username de credencial inválido.")
    if not password or len(password) > _PASSWORD_MAX_LENGTH:
        raise ValidationError("Senha de credencial inválida.")


def _encrypt(username, password, *, key_provider):
    _validate_secret(username, password)
    key, key_version = key_provider.active_key()
    payload = json.dumps(
        {"schema_version": _PAYLOAD_SCHEMA_VERSION, "username": username, "password": password},
        ensure_ascii=False,
        separators=(",", ":"),
    ).encode("utf-8")
    return Fernet(key).encrypt(payload).decode("ascii"), key_version


def _decrypt(version, *, key_provider):
    try:
        key = key_provider.key_for_version(version.key_version)
    except CredentialKeyError as exc:
        raise CredentialOperationError(exc.code) from None
    try:
        raw = Fernet(key).decrypt(version.ciphertext.encode("ascii"))
        payload = json.loads(raw.decode("utf-8"))
    except (InvalidToken, UnicodeDecodeError, ValueError, TypeError):
        raise CredentialOperationError("DECRYPT_FAILED") from None
    if (
        not isinstance(payload, dict)
        or set(payload) != {"schema_version", "username", "password"}
        or payload.get("schema_version") != _PAYLOAD_SCHEMA_VERSION
        or not isinstance(payload.get("username"), str)
        or not isinstance(payload.get("password"), str)
    ):
        raise CredentialOperationError("DECRYPT_FAILED")
    try:
        _validate_secret(payload["username"], payload["password"])
    except ValidationError:
        raise CredentialOperationError("DECRYPT_FAILED") from None
    return payload["username"], payload["password"]


_RESOLUTION_CONFIG_FIELDS = (
    "camera_id",
    "config_version",
    "credential_id",
    "profile_id",
    "enabled",
    "rtsp_uri",
    "http_endpoint_override",
    "http_port_override",
    "transport",
)


@transaction.atomic
def resolve_active_credential_for_execution(*, config):
    """Resolve only the configured ACTIVE version for an internal attempt.

    The caller must have selected this persisted configuration after its own
    authorization and target-policy checks. This service enforces integrity
    and credential lifecycle, and never performs human reveal authorization.
    """
    if not isinstance(config, CameraConnectionConfig) or config.pk is None or config._state.adding:
        raise CredentialOperationError("CONFIGURATION_NOT_ALLOWED")

    # Match the lock order used by credential lifecycle operations so rotation
    # and revocation cannot interleave between eligibility checks and decrypt.
    camera = Camera.objects.select_for_update().filter(pk=config.camera_id).first()
    if camera is None:
        raise CredentialOperationError("CONFIGURATION_NOT_ALLOWED")
    persisted_config = (
        CameraConnectionConfig.objects.select_for_update()
        .filter(pk=config.pk, camera_id=camera.pk)
        .first()
    )
    if persisted_config is None or any(
        getattr(persisted_config, name) != getattr(config, name)
        for name in _RESOLUTION_CONFIG_FIELDS
    ):
        raise CredentialOperationError("CONFIGURATION_NOT_ALLOWED")

    if persisted_config.credential_id is None:
        raise CredentialOperationError("CREDENTIAL_NOT_CONFIGURED")
    credential = (
        CameraCredential.objects.select_for_update()
        .filter(pk=persisted_config.credential_id)
        .first()
    )
    if credential is None:
        raise CredentialOperationError("CREDENTIAL_NOT_CONFIGURED")
    if credential.camera_id != persisted_config.camera_id:
        raise CredentialOperationError("CROSS_CAMERA_REFERENCE")
    if credential.state != CameraCredential.State.ACTIVE:
        raise CredentialOperationError("VERSION_NOT_ALLOWED")
    if credential.active_version_id is None:
        raise CredentialOperationError("NO_ACTIVE_VERSION")

    active_version = (
        CameraCredentialVersion.objects.select_for_update()
        .filter(pk=credential.active_version_id)
        .first()
    )
    if active_version is None:
        raise CredentialOperationError("VERSION_NOT_ALLOWED")
    if active_version.credential_id != credential.pk:
        raise CredentialOperationError("CROSS_CAMERA_REFERENCE")
    if active_version.state != CameraCredentialVersion.State.ACTIVE:
        raise CredentialOperationError("VERSION_NOT_ALLOWED")
    active_ids = list(
        credential.versions.filter(state=CameraCredentialVersion.State.ACTIVE)
        .values_list("pk", flat=True)
    )
    if active_ids != [active_version.pk]:
        raise CredentialOperationError("VERSION_NOT_ALLOWED")

    try:
        username, password = _decrypt(
            active_version,
            key_provider=_provider(None),
        )
    except CredentialKeyError as exc:
        raise CredentialOperationError(exc.code) from None
    return ResolvedCameraCredential(username=username, password=password)


def _audit(*, code, summary, actor, camera, credential, version, outcome="success", request=None):
    from cameras.auditoria import registrar_evento

    registrar_evento(
        codigo=code,
        resumo=summary,
        categoria=EventoAuditoria.Categoria.CAMERA,
        request=request,
        usuario=actor,
        camera=camera,
        entidade=credential,
        metadados={
            "credential_id": credential.pk,
            "credential_version_id": version.pk if version else None,
            "credential_version": version.version if version else None,
            "operation": code,
            "outcome": outcome,
        },
    )


def credential_metadata(*, actor, camera_id, key_provider=None):
    """Return allowlisted non-secret metadata after explicit authorization."""
    require_camera_permission(actor=actor, permission_codename="view_camera_credential", camera_id=camera_id)
    credential = CameraCredential.objects.filter(camera_id=camera_id).select_related("active_version").first()
    if credential is None:
        return {"configured": False}
    active = credential.active_version
    if active is None or active.state != CameraCredentialVersion.State.ACTIVE:
        return {"configured": False}
    return {
        "configured": True,
        "username": _decrypt(active, key_provider=_provider(key_provider))[0],
        "key_version": active.key_version,
        "updated_at": credential.updated_at,
        "version": active.version,
    }


@transaction.atomic
def replace_camera_credential(*, actor, camera_id, username, password, key_provider=None, request=None):
    """Create and activate a new encrypted version, preserving the prior on failure."""
    require_camera_permission(actor=actor, permission_codename="change_camera_credential", camera_id=camera_id)
    camera = Camera.objects.select_for_update().get(pk=camera_id)
    credential, _ = CameraCredential.objects.select_for_update().get_or_create(camera=camera)
    provider = _provider(key_provider)
    try:
        ciphertext, key_version = _encrypt(username, password, key_provider=provider)
        # Verify the just-encrypted payload before any active pointer changes.
        next_number = (credential.versions.aggregate(value=Max("version"))["value"] or 0) + 1
        current = credential.active_version
        candidate = CameraCredentialVersion.objects.create(
            credential=credential,
            version=next_number,
            ciphertext=ciphertext,
            key_version=key_version,
            state=CameraCredentialVersion.State.PENDING,
            created_by=actor,
            rotated_from=current,
        )
        if _decrypt(candidate, key_provider=provider) != (username, password):
            raise CredentialOperationError("DECRYPT_FAILED")
        now = timezone.now()
        if current is not None:
            CameraCredentialVersion.objects.filter(pk=current.pk).update(
                state=CameraCredentialVersion.State.RETIRED,
                retired_at=now,
            )
        candidate.state = CameraCredentialVersion.State.ACTIVE
        candidate.activated_at = now
        candidate.save(update_fields=["state", "activated_at"])
        credential.active_version = candidate
        credential.state = CameraCredential.State.ACTIVE
        credential.updated_by = actor
        credential.save(update_fields=["active_version", "state", "updated_by", "updated_at"])
        _audit(
            code="camera.credential.created" if next_number == 1 else "camera.credential.replaced",
            summary="Credencial de câmera alterada.",
            actor=actor,
            camera=camera,
            credential=credential,
            version=candidate,
            request=request,
        )
        return credential
    except CredentialKeyError as exc:
        raise CredentialOperationError(exc.code) from None


def reveal_camera_credential(*, actor, camera_id, current_password, key_provider=None, request=None):
    """Explicit reveal use case. Call only from the dedicated POST/CSRF surface."""
    require_camera_permission(actor=actor, permission_codename="reveal_camera_credential", camera_id=camera_id)
    if not getattr(actor, "is_authenticated", False):
        raise PermissionDenied
    if not isinstance(current_password, str) or not current_password:
        _audit_reveal_failure(actor=actor, camera_id=camera_id, request=request)
        raise CredentialOperationError("REAUTHENTICATION_FAILED")
    authenticated = authenticate(request=request, username=actor.get_username(), password=current_password)
    if authenticated is None or authenticated.pk != actor.pk:
        _audit_reveal_failure(actor=actor, camera_id=camera_id, request=request)
        raise CredentialOperationError("REAUTHENTICATION_FAILED")
    try:
        with transaction.atomic():
            credential = CameraCredential.objects.select_for_update().filter(camera_id=camera_id).select_related("active_version", "camera").first()
            if credential is None or credential.active_version_id is None:
                raise CredentialOperationError("CREDENTIAL_NOT_CONFIGURED")
            active = credential.active_version
            if active.state != CameraCredentialVersion.State.ACTIVE:
                raise CredentialOperationError("CREDENTIAL_NOT_CONFIGURED")
            username, password = _decrypt(active, key_provider=_provider(key_provider))
            _audit(
                code="camera.credential.revealed",
                summary="Credencial de câmera revelada.",
                actor=actor,
                camera=credential.camera,
                credential=credential,
                version=active,
                request=request,
            )
            return {"username": username, "password": password, "version": active.version}
    except CredentialOperationError as exc:
        _audit_reveal_failure(
            actor=actor,
            camera_id=camera_id,
            request=request,
            outcome=exc.code,
            summary="Falha segura ao revelar credencial de câmera.",
        )
        raise


def _audit_reveal_failure(
    *, actor, camera_id, request=None, outcome="REAUTHENTICATION_FAILED",
    summary="Falha de reautenticação ao revelar credencial de câmera.",
):
    camera = Camera.objects.filter(pk=camera_id).first()
    if camera is None:
        return
    credential = CameraCredential.objects.filter(camera=camera).first()
    if credential is not None:
        _audit(
            code="camera.credential.revealed",
            summary=summary,
            actor=actor,
            camera=camera,
            credential=credential,
            version=credential.active_version,
            outcome=outcome,
            request=request,
        )
        return
    from cameras.auditoria import registrar_evento

    registrar_evento(
        codigo="camera.credential.revealed",
        resumo=summary,
        categoria=EventoAuditoria.Categoria.CAMERA,
        request=request,
        usuario=actor,
        camera=camera,
        metadados={"operation": "camera.credential.revealed", "outcome": outcome},
    )


@transaction.atomic
def revoke_camera_credential(*, actor, camera_id, request=None):
    """Revoke the active secret without fallback to an older version."""
    require_camera_permission(actor=actor, permission_codename="change_camera_credential", camera_id=camera_id)
    camera = Camera.objects.select_for_update().get(pk=camera_id)
    credential = CameraCredential.objects.select_for_update().filter(camera=camera).first()
    if credential is None or credential.active_version_id is None:
        raise CredentialOperationError("CREDENTIAL_NOT_CONFIGURED")
    now = timezone.now()
    version = credential.active_version
    version.state = CameraCredentialVersion.State.REVOKED
    version.revoked_at = now
    version.save(update_fields=["state", "revoked_at"])
    credential.active_version = None
    credential.state = CameraCredential.State.INACTIVE
    credential.updated_by = actor
    credential.save(update_fields=["active_version", "state", "updated_by", "updated_at"])
    _audit(
        code="camera.credential.revoked",
        summary="Credencial de câmera revogada.",
        actor=actor,
        camera=camera,
        credential=credential,
        version=version,
        request=request,
    )
    return credential


@transaction.atomic
def rotate_camera_credential_key(*, actor, camera_id, key_provider=None, request=None):
    """Re-encrypt every retained version under the provider's active key."""
    require_camera_permission(actor=actor, permission_codename="change_camera_credential", camera_id=camera_id)
    camera = Camera.objects.select_for_update().get(pk=camera_id)
    credential = CameraCredential.objects.select_for_update().filter(camera=camera).first()
    if credential is None:
        raise CredentialOperationError("CREDENTIAL_NOT_CONFIGURED")
    provider = _provider(key_provider)
    versions = list(credential.versions.select_for_update().order_by("version"))
    if not versions:
        raise CredentialOperationError("CREDENTIAL_NOT_CONFIGURED")
    active = credential.active_version
    if active is not None and (active.state != CameraCredentialVersion.State.ACTIVE or active.credential_id != credential.pk):
        raise CredentialOperationError("CREDENTIAL_NOT_CONFIGURED")
    rewritten = []
    for version in versions:
        username, password = _decrypt(version, key_provider=provider)
        ciphertext, key_version = _encrypt(username, password, key_provider=provider)
        version.ciphertext = ciphertext
        version.key_version = key_version
        version.save(update_fields=["ciphertext", "key_version"])
        rewritten.append(version)
    _audit(
        code="camera.credential.key_rotated",
        summary="Chaves de credencial de câmera atualizadas.",
        actor=actor,
        camera=camera,
        credential=credential,
        version=active,
        request=request,
    )
    return rewritten
