"""Entrega privada de variantes derivadas para a galeria E4."""

from dataclasses import dataclass
from enum import StrEnum
from hashlib import sha256
from io import BytesIO
from uuid import UUID

from django.conf import settings
from django.core.files.storage import default_storage
from PIL import Image, ImageOps, UnidentifiedImageError

from cameras.models import CameraImageRecord


# Dimensões de caixa fechadas no servidor. THUMB < FULL; thumbnail() mantém
# proporção, não corta e não amplia imagens menores que a caixa.
VARIANT_BOUNDS = {"THUMB": (320, 224), "FULL": (1600, 1120)}
SUPPORTED_FORMATS = {"JPEG", "PNG", "WEBP"}


class GalleryPreviewState(StrEnum):
    AVAILABLE = "AVAILABLE"
    NOT_FOUND = "NOT_FOUND"
    UNAVAILABLE = "UNAVAILABLE"
    ERROR = "ERROR"


@dataclass(frozen=True, slots=True)
class CameraGalleryPreviewResult:
    state: GalleryPreviewState
    content: bytes | None = None


class CameraGalleryPreviewService:
    """Entrega bytes apenas por câmera, UUID imutável e variante permitida."""

    def __init__(self, *, storage=None):
        self.storage = storage or default_storage

    def deliver(self, camera_id: int, immutable_id, variant: str) -> CameraGalleryPreviewResult:
        if not isinstance(variant, str) or variant not in VARIANT_BOUNDS:
            return CameraGalleryPreviewResult(GalleryPreviewState.ERROR)
        try:
            image_id = immutable_id if isinstance(immutable_id, UUID) else UUID(str(immutable_id))
        except (TypeError, ValueError, AttributeError):
            return CameraGalleryPreviewResult(GalleryPreviewState.NOT_FOUND)

        try:
            record = CameraImageRecord.objects.filter(
                pk=image_id,
                camera_id=camera_id,
                withdrawn_at__isnull=True,
                provenance__in=(
                    CameraImageRecord.Provenance.CAPTURA_CAMERA,
                    CameraImageRecord.Provenance.UPLOAD_MANUAL,
                ),
            ).first()
        except (TypeError, ValueError):
            record = None
        if record is None:
            return CameraGalleryPreviewResult(GalleryPreviewState.NOT_FOUND)

        if (
            record.integrity_status != CameraImageRecord.IntegrityStatus.VALID
            or len(record.sha256) != 64
            or any(char not in "0123456789abcdef" for char in record.sha256)
        ):
            return CameraGalleryPreviewResult(GalleryPreviewState.ERROR)

        try:
            exists = self.storage.exists(record.storage_key)
        except Exception:
            exists = False
        if not exists:
            return CameraGalleryPreviewResult(GalleryPreviewState.UNAVAILABLE)

        max_bytes = getattr(settings, "ARGOS_PREVIEW_MAX_SOURCE_BYTES", 20 * 1024 * 1024)
        max_pixels = getattr(settings, "ARGOS_PREVIEW_MAX_SOURCE_PIXELS", 20_000_000)
        if record.size_bytes is not None and record.size_bytes > max_bytes:
            return CameraGalleryPreviewResult(GalleryPreviewState.ERROR)
        try:
            with self.storage.open(record.storage_key, "rb") as source:
                data = source.read(max_bytes + 1)
            if len(data) > max_bytes:
                return CameraGalleryPreviewResult(GalleryPreviewState.ERROR)
        except Exception:
            return CameraGalleryPreviewResult(GalleryPreviewState.UNAVAILABLE)
        if not data or sha256(data).hexdigest() != record.sha256:
            return CameraGalleryPreviewResult(GalleryPreviewState.ERROR)

        try:
            with Image.open(BytesIO(data)) as source:
                if source.format not in SUPPORTED_FORMATS or getattr(source, "n_frames", 1) != 1:
                    return CameraGalleryPreviewResult(GalleryPreviewState.ERROR)
                if not source.width or not source.height or source.width * source.height > max_pixels:
                    return CameraGalleryPreviewResult(GalleryPreviewState.ERROR)
                source.verify()
            with Image.open(BytesIO(data)) as source:
                source.load()
                transformed = ImageOps.exif_transpose(source).convert("RGB")
                transformed.thumbnail(VARIANT_BOUNDS[variant], Image.Resampling.LANCZOS)
                output = BytesIO()
                # Re-encoding creates a clean JPEG without source metadata.
                transformed.save(output, format="JPEG", quality=85, optimize=True)
            return CameraGalleryPreviewResult(GalleryPreviewState.AVAILABLE, output.getvalue())
        except (OSError, ValueError, SyntaxError, UnidentifiedImageError, Image.DecompressionBombError):
            return CameraGalleryPreviewResult(GalleryPreviewState.ERROR)
        except Exception:
            return CameraGalleryPreviewResult(GalleryPreviewState.ERROR)
