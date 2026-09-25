"""Entrega privada e limitada de previews da captura atual da câmera."""

from dataclasses import dataclass
from enum import StrEnum
from hashlib import sha256
from io import BytesIO

from django.conf import settings
from django.core.files.storage import default_storage
from PIL import Image, ImageOps, UnidentifiedImageError

from cameras.imagens.read_service import CameraImageReadService, LatestCameraCaptureStatus


class PreviewState(StrEnum):
    AVAILABLE = "AVAILABLE"
    NO_CAPTURE_AVAILABLE = "NO_CAPTURE_AVAILABLE"
    UNAVAILABLE = "UNAVAILABLE"
    ERROR = "ERROR"


# Dimensões fechadas; alterar exige decisão explícita, nunca parâmetros do cliente.
VARIANTS = {"THUMB": (60, 42), "PANEL": (640, 448)}
CONTENT_TYPE = "image/jpeg"


@dataclass(frozen=True, slots=True)
class PreviewResult:
    state: PreviewState
    content: bytes | None = None


class CameraImagePreviewService:
    def __init__(self, *, storage=None):
        self.storage = storage or default_storage

    def deliver(self, camera_id: int, variant: str) -> PreviewResult:
        if variant not in VARIANTS:
            raise ValueError("Variante inválida")

        record = next(iter(CameraImageReadService.latest_records((camera_id,))), None)
        if record is None:
            return PreviewResult(PreviewState.NO_CAPTURE_AVAILABLE)

        # A seleção ocorreu antes desta validação. Nenhuma captura anterior participa.
        projected = CameraImageReadService(storage_exists=self.storage.exists)._project(record)
        if projected.status != LatestCameraCaptureStatus.AVAILABLE:
            return PreviewResult(PreviewState(projected.status.value))

        max_bytes = getattr(settings, "ARGOS_PREVIEW_MAX_SOURCE_BYTES", 20 * 1024 * 1024)
        max_pixels = getattr(settings, "ARGOS_PREVIEW_MAX_SOURCE_PIXELS", 20_000_000)
        if record.size_bytes is not None and record.size_bytes > max_bytes:
            return PreviewResult(PreviewState.ERROR)

        try:
            with self.storage.open(record.storage_key, "rb") as source:
                data = source.read(max_bytes + 1)
            if len(data) > max_bytes:
                return PreviewResult(PreviewState.ERROR)
        except (OSError, IOError):
            return PreviewResult(PreviewState.UNAVAILABLE)
        except Exception:
            return PreviewResult(PreviewState.UNAVAILABLE)

        if not data or sha256(data).hexdigest() != record.sha256:
            return PreviewResult(PreviewState.ERROR)

        try:
            with Image.open(BytesIO(data)) as image:
                if image.format not in {"JPEG", "PNG", "WEBP"} or getattr(image, "n_frames", 1) != 1:
                    return PreviewResult(PreviewState.ERROR)
                if image.width * image.height > max_pixels:
                    return PreviewResult(PreviewState.ERROR)
                image.verify()
            with Image.open(BytesIO(data)) as image:
                image.load()
                transformed = ImageOps.fit(ImageOps.exif_transpose(image).convert("RGB"), VARIANTS[variant], method=Image.Resampling.LANCZOS)
                output = BytesIO()
                transformed.save(output, format="JPEG", quality=82, optimize=True)
                return PreviewResult(PreviewState.AVAILABLE, output.getvalue())
        except (OSError, ValueError, SyntaxError, UnidentifiedImageError, Image.DecompressionBombError):
            return PreviewResult(PreviewState.ERROR)
