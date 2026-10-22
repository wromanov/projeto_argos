"""Lifecycle bounded de imagens: retenção lógica, rotação e holds auditados."""

from calendar import monthrange
from datetime import datetime
from uuid import uuid4

from django.core.exceptions import PermissionDenied, ValidationError
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db import connection, transaction
from django.utils import timezone

from cameras.authorization import require_camera_permission
from cameras.models import Camera, CameraImageRecord, EventoAuditoria


MAX_ACTIVE_IMAGES = 3
RETENTION_MONTHS = 12
MAX_LIFECYCLE_BATCH = 500
MAX_ROTATION_BATCH = 100
HOLD_PERMISSION = "manage_camera_image_hold"


class ImageLifecycleCapacityError(ValidationError):
    """Não há imagens elegíveis suficientes para respeitar o limite."""


class ImageLifecycleStorageError(Exception):
    """O storage não aceitou os bytes já validados."""


def add_calendar_months(value: datetime, months: int) -> datetime:
    """Move um instante em meses corridos, limitando ao último dia do mês."""
    month_index = value.year * 12 + value.month - 1 + months
    year, zero_based_month = divmod(month_index, 12)
    month = zero_based_month + 1
    day = min(value.day, monthrange(year, month)[1])
    return value.replace(year=year, month=month, day=day)


def _lock_camera(camera_id):
    queryset = Camera.objects.all()
    if connection.features.has_select_for_update:
        queryset = queryset.select_for_update()
    return queryset.get(pk=camera_id)


def _active_records(camera_id):
    return CameraImageRecord.objects.filter(
        camera_id=camera_id, withdrawn_at__isnull=True
    )


def _audit_lifecycle(
    *, code, summary, camera, record, actor=None, origin=None, request=None
):
    from cameras.auditoria import registrar_evento

    registrar_evento(
        codigo=code,
        resumo=summary,
        categoria=EventoAuditoria.Categoria.CAMERA,
        request=request,
        usuario=actor,
        camera=camera,
        entidade=record,
        metadados={
            "image_record_id": str(record.pk),
            "executor": "ARGOS-IMG-LIFECYCLE",
        },
        origem=origin or EventoAuditoria.Origem.COMANDO,
    )


def _withdraw(record, *, reason, actor=None, at):
    record._lifecycle_service_mutation = True
    record.withdraw(reason=reason, by=actor, at=at)


def _expire_due_locked(*, camera, now, limit, actor=None):
    cutoff = add_calendar_months(now, -RETENTION_MONTHS)
    records = list(
        _active_records(camera.pk)
        .filter(recorded_at__lte=cutoff, retention_held_at__isnull=True)
        .order_by("recorded_at", "pk")[:limit]
    )
    for record in records:
        _withdraw(record, reason="RETENTION_12_MONTHS", at=now)
        _audit_lifecycle(
            code="imagem.retencao.expirada",
            summary="Imagem retirada logicamente ao completar 12 meses.",
            camera=camera,
            record=record,
            actor=actor,
            origin=EventoAuditoria.Origem.COMANDO,
        )
    return len(records)


def _rotate_to_limit(*, camera, new_record, actor, now):
    active = _active_records(camera.pk)
    excess = active.count() - MAX_ACTIVE_IMAGES
    if excess <= 0:
        return 0
    if excess > MAX_ROTATION_BATCH:
        raise ImageLifecycleCapacityError(
            "A câmera excede o limite legado e precisa de reconciliação bounded."
        )
    victims = list(
        active.filter(retention_held_at__isnull=True)
        .exclude(pk=new_record.pk)
        .order_by("recorded_at", "pk")[:excess]
    )
    if len(victims) != excess:
        raise ImageLifecycleCapacityError(
            "Não há imagem elegível para rotação sem afetar itens protegidos."
        )
    for record in victims:
        _withdraw(record, reason="ROTATED_BY_CAMERA_LIMIT", actor=actor, at=now)
        _audit_lifecycle(
            code="imagem.lifecycle.rotacionada",
            summary="Imagem retirada logicamente pela capacidade da câmera.",
            camera=camera,
            record=record,
            actor=actor,
            origin=EventoAuditoria.Origem.WEB if actor else EventoAuditoria.Origem.COMANDO,
        )
    return len(victims)


def persist_validated_image(
    *,
    camera,
    provenance,
    data,
    content_type,
    extension,
    width,
    height,
    sha256,
    captured_at=None,
    uploaded_by=None,
    original_filename="",
    captured_by_system="",
    recorded_by_system="",
    actor=None,
    request=None,
    storage=None,
    on_created=None,
):
    """Grava bytes validados e aplica lifecycle/aceite na mesma transação.

    Só o objeto recém-criado é compensado se qualquer gravação relacional,
    rotação, auditoria ou callback falhar. Bytes históricos nunca são apagados.
    """
    storage = storage or default_storage
    storage_name = f"camera-images/{camera.pk}/{uuid4().hex}.{extension}"
    saved_key = None
    try:
        try:
            saved_key = storage.save(storage_name, ContentFile(data))
        except Exception:
            raise ImageLifecycleStorageError from None
        with transaction.atomic():
            locked_camera = _lock_camera(camera.pk)
            accepted_at = timezone.now()
            _expire_due_locked(
                camera=locked_camera, now=accepted_at, limit=MAX_ACTIVE_IMAGES + 1
            )
            record = CameraImageRecord(
                camera=locked_camera,
                provenance=provenance,
                captured_at=captured_at,
                recorded_at=accepted_at,
                storage_key=saved_key,
                content_type=content_type,
                size_bytes=len(data),
                width=width,
                height=height,
                sha256=sha256,
                original_filename=original_filename,
                uploaded_by=uploaded_by,
                captured_by_system=captured_by_system,
                recorded_by_system=recorded_by_system,
            )
            record.save(force_insert=True)
            _rotate_to_limit(
                camera=locked_camera,
                new_record=record,
                actor=actor,
                now=accepted_at,
            )
            if provenance == CameraImageRecord.Provenance.UPLOAD_MANUAL:
                _audit_lifecycle(
                    code="imagem.upload_manual",
                    summary="Imagem enviada manualmente.",
                    camera=locked_camera,
                    record=record,
                    actor=actor,
                    origin=(
                        EventoAuditoria.Origem.WEB
                        if request is not None
                        else EventoAuditoria.Origem.COMANDO
                    ),
                    request=request,
                )
            if on_created is not None:
                on_created(record)
            return record
    except Exception:
        if saved_key is not None:
            try:
                storage.delete(saved_key)
            except Exception:
                pass
        raise


def expire_due_images(*, batch_size=100, camera_id=None):
    """Retira um lote bounded de imagens vencidas sem apagar seus bytes."""
    if type(batch_size) is not int or not 1 <= batch_size <= MAX_LIFECYCLE_BATCH:
        raise ValueError(f"batch_size deve estar entre 1 e {MAX_LIFECYCLE_BATCH}.")
    candidates = CameraImageRecord.objects.filter(
        withdrawn_at__isnull=True, retention_held_at__isnull=True
    )
    if camera_id is not None:
        candidates = candidates.filter(camera_id=camera_id)
    now = timezone.now()
    cutoff = add_calendar_months(now, -RETENTION_MONTHS)
    camera_ids = list(
        candidates.filter(recorded_at__lte=cutoff)
        .order_by("camera_id")
        .values_list("camera_id", flat=True)
        .distinct()[:batch_size]
    )
    processed = 0
    for current_camera_id in camera_ids:
        if processed >= batch_size:
            break
        with transaction.atomic():
            camera = _lock_camera(current_camera_id)
            processed += _expire_due_locked(
                camera=camera, now=now, limit=batch_size - processed
            )
    return processed


def _require_hold_authority(*, actor, camera):
    require_camera_permission(
        actor=actor, permission_codename=HOLD_PERMISSION, camera_id=camera.pk
    )
    # Django superusers bypass has_perm; no privileged hold authority is approved.
    if getattr(actor, "is_superuser", False):
        raise PermissionDenied
    # ModelBackend has no object grants by default, so this check denies closed
    # until an explicit camera-scope authorization backend/grant exists.
    if not actor.has_perm(f"cameras.{HOLD_PERMISSION}", camera):
        raise PermissionDenied


def _audit_hold_failure(*, actor, camera_id, image_id, held, error):
    """Registra uma recusa/falha sem incluir mensagem ou dados sensíveis."""
    try:
        camera = Camera.objects.filter(pk=camera_id).first()
        from cameras.auditoria import registrar_evento

        registrar_evento(
            codigo=(
                "imagem.hold.negado"
                if isinstance(error, PermissionDenied)
                else "imagem.hold.erro"
            ),
            resumo=(
                "Operação de proteção de imagem negada."
                if isinstance(error, PermissionDenied)
                else "Falha sanitizada ao alterar proteção de imagem."
            ),
            categoria=EventoAuditoria.Categoria.CAMERA,
            usuario=actor if getattr(actor, "is_authenticated", False) else None,
            camera=camera,
            entidade=None,
            metadados={
                "camera_id": str(camera_id),
                "image_record_id": str(image_id),
                "operation": "hold" if held else "release",
                "error_type": type(error).__name__,
                "executor": "ARGOS-IMG-LIFECYCLE",
            },
            origem=EventoAuditoria.Origem.WEB,
        )
    except Exception:
        # A falha de auditoria não deve mascarar o erro original; a operação
        # de negócio já foi revertida pela atomicidade do bloco chamador.
        pass


def set_image_hold(*, actor, camera_id, image_id, held=True):
    try:
        if not getattr(actor, "is_authenticated", False):
            raise PermissionDenied
        with transaction.atomic():
            camera = _lock_camera(camera_id)
            _require_hold_authority(actor=actor, camera=camera)
            record = (
                CameraImageRecord.objects.select_for_update()
                .filter(pk=image_id, camera_id=camera_id)
                .first()
            )
            if record is None:
                raise CameraImageRecord.DoesNotExist
            if record.withdrawn_at is not None:
                raise ValidationError("Uma imagem retirada não pode receber alteração de hold.")
            if held:
                if record.retention_held_at is not None:
                    raise ValidationError("A imagem já está protegida.")
                record.retention_held_at = timezone.now()
                record.retention_held_by = actor
                code = "imagem.hold.ativado"
                summary = "Proteção de retenção ativada para a imagem."
            else:
                if record.retention_held_at is None:
                    raise ValidationError("A imagem não está protegida.")
                record.retention_held_at = None
                record.retention_held_by = None
                code = "imagem.hold.liberado"
                summary = "Proteção de retenção liberada para a imagem."
            record._lifecycle_service_mutation = True
            record.save(update_fields=["retention_held_at", "retention_held_by"])
            _audit_lifecycle(
                code=code,
                summary=summary,
                camera=camera,
                record=record,
                actor=actor,
                origin=EventoAuditoria.Origem.WEB,
            )
            return record
    except Exception as error:
        _audit_hold_failure(
            actor=actor, camera_id=camera_id, image_id=image_id, held=held, error=error
        )
        raise
