"""Matching declarativo de compatibilidade, sem descoberta de rede real."""

from dataclasses import dataclass

from django.core.exceptions import PermissionDenied, ValidationError

from cameras.models import CameraCapabilityEvidence

UNVERIFIED = CameraCapabilityEvidence.Status.UNVERIFIED
SUPPORTED = CameraCapabilityEvidence.Status.SUPPORTED
UNSUPPORTED = CameraCapabilityEvidence.Status.UNSUPPORTED


@dataclass(frozen=True)
class CompatibilityResolution:
    status: str
    evidence: CameraCapabilityEvidence | None = None
    diagnostics: tuple[str, ...] = ()


def _normalize(value):
    return " ".join((value or "").split()).casefold()


def _resolve_candidates(candidates):
    if not candidates:
        return CompatibilityResolution(UNVERIFIED)
    statuses = {item.status for item in candidates}
    if UNSUPPORTED in statuses:
        chosen = next(item for item in candidates if item.status == UNSUPPORTED)
        return CompatibilityResolution(UNSUPPORTED, chosen)
    if len(statuses) != 1:
        return CompatibilityResolution(UNVERIFIED, diagnostics=("AMBIGUOUS_EVIDENCE",))
    chosen = sorted(candidates, key=lambda item: (item.source_type, item.source_ref, item.pk))[0]
    return CompatibilityResolution(chosen.status, chosen)


def resolve_compatibility(*, camera, profile):
    """Resolve unidade primeiro; exige fabricante, modelo e firmware exatos."""
    if not profile.pk or not camera.pk:
        return CompatibilityResolution(UNVERIFIED)

    vendor = _normalize(camera.fabricante)
    model = _normalize(camera.modelo)
    firmware = _normalize(camera.firmware_version)
    active = CameraCapabilityEvidence.objects.filter(profile=profile, active=True)

    unit_rows = list(active.filter(camera_id=camera.pk).order_by("pk"))
    unit_exact = [
        item for item in unit_rows
        if _normalize(item.vendor) == vendor
        and _normalize(item.model) == model
        and _normalize(item.firmware_exact) == firmware
    ]
    model_exact = list(
        active.filter(camera__isnull=True, vendor=vendor, model=model, firmware_exact=firmware)
        .order_by("pk")
    )

    if unit_exact:
        unit = _resolve_candidates(unit_exact)
        conflict = any(item.status != unit.status for item in model_exact)
        if conflict:
            return CompatibilityResolution(
                unit.status,
                unit.evidence,
                tuple(dict.fromkeys(unit.diagnostics + ("UNIT_EVIDENCE_CONFLICTS_WITH_MODEL_EVIDENCE",))),
            )
        return unit
    model_resolution = _resolve_candidates(model_exact)
    if unit_rows:
        return CompatibilityResolution(
            model_resolution.status,
            model_resolution.evidence,
            tuple(dict.fromkeys(model_resolution.diagnostics + ("STALE_UNIT_EVIDENCE",))),
        )
    return model_resolution


def create_compatibility_evidence(*, actor, evidence):
    """Persist evidence only through the existing camera-capability permission."""
    if not getattr(actor, "is_authenticated", False) or not actor.has_perm("cameras.manage_camera_capability"):
        raise PermissionDenied
    evidence.reviewer = actor
    evidence.full_clean()
    evidence.save()
    return evidence


def set_camera_firmware(*, actor, camera, firmware_version):
    """Update the optional unit firmware value for Technician/Admin actors."""
    if not getattr(actor, "is_authenticated", False) or not actor.has_perm("cameras.manage_camera_capability"):
        raise PermissionDenied
    value = " ".join((firmware_version or "").split())
    if len(value) > 100:
        raise ValidationError({"firmware_version": "Versão excede 100 caracteres."})
    camera.firmware_version = value
    camera.save(update_fields=["firmware_version", "atualizado_em"])
    return camera
