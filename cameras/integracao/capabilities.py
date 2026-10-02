"""Resolução estrita de perfis e elegibilidade de capabilities."""

from urllib.parse import unquote

from django.core.exceptions import PermissionDenied, ValidationError
from django.db import transaction

from cameras.models import CameraCapabilityProfile, EventoAuditoria

COMPATIBILITY_UNVERIFIED = "UNVERIFIED"
COMPATIBILITY_SUPPORTED = "SUPPORTED"


def _require_profile_permission(actor):
    if not getattr(actor, "is_authenticated", False) or not actor.has_perm("cameras.manage_camera_capability"):
        raise PermissionDenied


def validate_profile(profile):
    """Valida campos estruturados contra allowlists fechadas."""
    profile.full_clean()
    if not profile.allowed_schemes:
        raise ValidationError({"allowed_schemes": "O perfil deve permitir ao menos um scheme."})
    if not profile.allowed_ports:
        raise ValidationError({"allowed_ports": "O perfil deve permitir ao menos uma porta."})
    if len(set(profile.allowed_schemes)) != len(profile.allowed_schemes):
        raise ValidationError({"allowed_schemes": "O perfil não pode repetir schemes."})
    if len(set(profile.allowed_ports)) != len(profile.allowed_ports):
        raise ValidationError({"allowed_ports": "O perfil não pode repetir portas."})
    if profile.adapter_key == CameraCapabilityProfile.Adapter.RTSP and not set(profile.allowed_schemes) <= {"rtsp", "rtsps"}:
        raise ValidationError({"allowed_schemes": "Perfil RTSP não pode permitir schemes HTTP."})
    if profile.adapter_key == CameraCapabilityProfile.Adapter.HTTP_SNAPSHOT and not set(profile.allowed_schemes) <= {"http", "https"}:
        raise ValidationError({"allowed_schemes": "Perfil HTTP não pode permitir schemes RTSP."})
    secure_schemes = {"rtsps", "https"}
    if profile.tls_policy == CameraCapabilityProfile.TLSPolicy.REQUIRED and not set(profile.allowed_schemes) <= secure_schemes:
        raise ValidationError({"tls_policy": "TLS requerido precisa de schemes seguros."})
    if profile.tls_policy in {CameraCapabilityProfile.TLSPolicy.NOT_REQUIRED, CameraCapabilityProfile.TLSPolicy.NOT_APPLICABLE} and set(profile.allowed_schemes) & secure_schemes:
        raise ValidationError({"tls_policy": "Policy TLS conflita com os schemes permitidos."})
    if profile.default_path:
        path = profile.default_path
        if not path.startswith("/") or path.startswith("//") or "\\" in path or "?" in path or "#" in path:
            raise ValidationError({"default_path": "Path default deve ser relativo e sem query/fragmento."})
        if any(part == ".." for part in unquote(path).split("/")):
            raise ValidationError({"default_path": "Path default não pode navegar para diretórios anteriores."})
    if profile.credential_required and profile.auth_method == CameraCapabilityProfile.AuthMethod.NONE:
        raise ValidationError({"auth_method": "Credencial obrigatória exige método de autenticação."})
    return profile


@transaction.atomic
def create_capability_profile(*, actor, profile):
    # Perfil é global e não possui camera_id; a permissão de gestão também é global.
    _require_profile_permission(actor)
    validate_profile(profile)
    profile.created_by = actor
    profile.save()
    from cameras.auditoria import registrar_evento

    registrar_evento(
        codigo="camera.capability_profile.created",
        resumo="Perfil de capability criado.",
        categoria=EventoAuditoria.Categoria.SISTEMA,
        usuario=actor,
        entidade=profile,
        alteracoes={"profile_key": {"anterior": None, "atual": profile.profile_key}, "version": {"anterior": None, "atual": profile.version}},
    )
    return profile


@transaction.atomic
def set_capability_profile_active(*, actor, profile_id, active):
    _require_profile_permission(actor)
    if not isinstance(active, bool):
        raise ValidationError({"active": "Estado do perfil deve ser booleano."})
    profile = CameraCapabilityProfile.objects.select_for_update().get(pk=profile_id)
    if profile.active == active:
        return profile
    previous = profile.active
    profile.active = active
    profile.save(update_fields=["active"])
    from cameras.auditoria import registrar_evento

    registrar_evento(
        codigo="camera.capability_profile.activated" if active else "camera.capability_profile.deactivated",
        resumo="Estado do perfil de capability alterado.",
        categoria=EventoAuditoria.Categoria.SISTEMA,
        usuario=actor,
        entidade=profile,
        alteracoes={"active": {"anterior": previous, "atual": active}},
        metadados={"profile_key": profile.profile_key, "version": profile.version},
    )
    return profile


def compatibility_status(camera, profile):
    """Sem evidência CAM-INT-06, cadastro livre não comprova suporte."""
    return COMPATIBILITY_UNVERIFIED


def require_automatic_compatibility(camera, profile):
    status = compatibility_status(camera, profile)
    if status != COMPATIBILITY_SUPPORTED:
        raise ValidationError("Capability sem evidência SUPPORTED não pode executar automaticamente.")
    return status


def require_manual_discovery(*, actor, camera, profile):
    from cameras.authorization import require_camera_permission

    require_camera_permission(actor=actor, permission_codename="run_camera_connection_test", camera_id=camera.pk)
    if profile.profile_key != "RTSP_DISCOVERY_V1" or profile.adapter_key != CameraCapabilityProfile.Adapter.RTSP:
        raise ValidationError("Teste manual de discovery exige o perfil RTSP_DISCOVERY_V1.")
    if not profile.active:
        raise ValidationError("Perfil inativo não pode iniciar novo teste manual.")
    return {"compatibility": COMPATIBILITY_UNVERIFIED, "evidence_stage": profile.probe_evidence_stage}
