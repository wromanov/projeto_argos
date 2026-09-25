"""Aceitação de upload manual, sem inferir captura de equipamento."""

from hashlib import sha256
from io import BytesIO
from uuid import uuid4

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db import transaction
from django.utils import timezone

from cameras.models import CameraImageRecord, sanitizar_nome_original


# Restrição operacional reversível. A política de produto permanece pendente.
FORMATS = {"JPEG": ("jpg", "jpeg", "image/jpeg"), "PNG": ("png", "image/png"), "WEBP": ("webp", "image/webp")}
EXTENSION = {"jpg": "JPEG", "jpeg": "JPEG", "png": "PNG", "webp": "WEBP"}


def aceitar_upload_manual(*, camera, usuario, arquivo, request=None):
    if not usuario.is_authenticated or not usuario.has_perm("cameras.add_cameraimagerecord"):
        raise PermissionError("Upload não autorizado.")
    if arquivo is None:
        raise ValidationError("Selecione uma imagem.")

    nome = sanitizar_nome_original(arquivo.name)
    extensao = nome.rsplit(".", 1)[-1].lower() if "." in nome else ""
    if extensao not in EXTENSION:
        raise ValidationError("Extensão de imagem não permitida.")

    limite = getattr(settings, "ARGOS_MANUAL_IMAGE_MAX_BYTES", 10 * 1024 * 1024)
    if limite is not None and arquivo.size > limite:
        raise ValidationError("Imagem excede o limite configurado.")
    if not arquivo.size:
        raise ValidationError("Imagem vazia.")

    data = arquivo.read(limite + 1 if limite is not None else -1)
    if not data:
        raise ValidationError("Imagem vazia.")
    if limite is not None and len(data) > limite:
        raise ValidationError("Imagem excede o limite configurado.")

    try:
        from PIL import Image, UnidentifiedImageError
        with Image.open(BytesIO(data)) as imagem:
            formato = imagem.format
            if formato not in FORMATS or EXTENSION[extensao] != formato:
                raise ValidationError("Nome e conteúdo da imagem não correspondem.")
            if getattr(imagem, "n_frames", 1) != 1:
                raise ValidationError("Imagens animadas não são aceitas.")
            width, height = imagem.size
            max_pixels = getattr(settings, "ARGOS_MANUAL_IMAGE_MAX_PIXELS", 20_000_000)
            if not width or not height or (max_pixels is not None and width * height > max_pixels):
                raise ValidationError("Dimensões de imagem inválidas ou acima do limite configurado.")
            imagem.verify()
        with Image.open(BytesIO(data)) as imagem:
            imagem.load()
            # Regrava pixels em formato raster limpo: remove EXIF, payloads
            # anexados e demais metadados fornecidos pelo cliente.
            output = BytesIO()
            if formato == "JPEG":
                imagem.convert("RGB").save(output, format="JPEG")
            elif formato == "WEBP":
                imagem.convert("RGB").save(output, format="WEBP")
            else:
                imagem.convert("RGB").save(output, format="PNG")
            data = output.getvalue()
            if limite is not None and len(data) > limite:
                raise ValidationError("Imagem processada excede o limite configurado.")
    except ValidationError:
        raise
    except (OSError, ValueError, SyntaxError, UnidentifiedImageError) as exc:
        raise ValidationError("Arquivo de imagem inválido ou corrompido.") from exc

    # A chave deriva exclusivamente de identidade gerada no servidor.
    storage_key = f"camera-images/{camera.pk}/{uuid4().hex}.{FORMATS[formato][0]}"
    saved_key = None
    try:
        saved_key = default_storage.save(storage_key, ContentFile(data))
        with transaction.atomic():
            record = CameraImageRecord(
                camera=camera, provenance=CameraImageRecord.Provenance.UPLOAD_MANUAL,
                captured_at=None, recorded_at=timezone.now(), storage_key=saved_key,
                content_type=FORMATS[formato][-1], size_bytes=len(data),
                width=width, height=height, sha256=sha256(data).hexdigest(),
                original_filename=nome, uploaded_by=usuario,
            )
            record.full_clean()
            record.save()
            if request is not None:
                from cameras.auditoria import registrar_evento
                from cameras.models import EventoAuditoria
                registrar_evento(
                    codigo="imagem.upload_manual", resumo="Imagem enviada manualmente",
                    categoria=EventoAuditoria.Categoria.CAMERA, request=request,
                    camera=camera, entidade=record,
                    metadados={"provenance": record.provenance, "size_bytes": record.size_bytes},
                )
        return record
    except Exception:
        if saved_key is not None:
            try:
                default_storage.delete(saved_key)
            except Exception:
                pass
        raise
