"""Entrega privada e limitada de previews da captura atual da câmera."""

from dataclasses import dataclass
from enum import StrEnum
from hashlib import sha256
from io import BytesIO

from django.conf import settings
from django.core.files.storage import default_storage
from PIL import Image, ImageOps, UnidentifiedImageError

from cameras.imagens.read_service import CameraImageReadService, LatestCameraCaptureStatus
from cameras.imagens.display_service import DisplayImageReadService, DisplayImageState
from cameras.imagens.quick_detail_service import QuickDetailImageReadService
from cameras.models import CameraImageRecord


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

        return self._deliver_record(record, variant)

    def _deliver_record(self, record: CameraImageRecord, variant: str) -> PreviewResult:

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


class DisplayImagePreviewService(CameraImagePreviewService):
    """Reavalia a seleção no request; nunca confia na projeção do HTML."""

    def deliver(self, camera_id: int, variant: str) -> PreviewResult:
        if variant not in VARIANTS:
            raise ValueError("Variante inválida")
        display = DisplayImageReadService(storage_exists=self.storage.exists).display_image(camera_id)
        if display.state == DisplayImageState.NO_IMAGE_AVAILABLE:
            return PreviewResult(PreviewState.NO_CAPTURE_AVAILABLE)
        if display.state != DisplayImageState.AVAILABLE:
            return PreviewResult(PreviewState(display.state.value))
        record = CameraImageRecord.objects.get(pk=display.immutable_id)
        return self._deliver_record(record, variant)


class QuickDetailPreviewState(StrEnum):
    AVAILABLE = "AVAILABLE"
    NOT_FOUND = "NOT_FOUND"
    STALE_SELECTION = "STALE_SELECTION"
    UNAVAILABLE = "UNAVAILABLE"
    ERROR = "ERROR"


@dataclass(frozen=True, slots=True)
class QuickDetailPreviewResult:
    state: QuickDetailPreviewState
    content: bytes | None = None


class QuickDetailImagePreviewService(CameraImagePreviewService):
    """Entrega a identidade escolhida pelo Quick Detail com double-check stale."""

    def _still_selected(self, camera_id: int, immutable_id) -> bool:
        current = QuickDetailImageReadService.latest_active_record(camera_id)
        return current is not None and current.pk == immutable_id

    def deliver(self, camera_id: int, immutable_id, variant: str) -> QuickDetailPreviewResult:
        if variant not in VARIANTS:
            raise ValueError("Variante inválida")

        record = CameraImageRecord.objects.filter(pk=immutable_id, camera_id=camera_id).first()
        if record is None:
            return QuickDetailPreviewResult(QuickDetailPreviewState.NOT_FOUND)
        if record.withdrawn_at is not None or not self._still_selected(camera_id, immutable_id):
            return QuickDetailPreviewResult(QuickDetailPreviewState.STALE_SELECTION)

        # Seleciona e valida a identidade antes de acessar o storage. A nova
        # consulta após o processamento funciona como ponto de linearização.
        if (record.integrity_status != CameraImageRecord.IntegrityStatus.VALID
                or len(record.sha256) != 64
                or any(char not in "0123456789abcdef" for char in record.sha256)):
            result = PreviewResult(PreviewState.ERROR)
        else:
            try:
                available = self.storage.exists(record.storage_key)
            except Exception:
                available = False
            if not available:
                result = PreviewResult(PreviewState.UNAVAILABLE)
            else:
                result = self._deliver_record(record, variant)

        if not self._still_selected(camera_id, immutable_id):
            return QuickDetailPreviewResult(QuickDetailPreviewState.STALE_SELECTION)
        if result.state == PreviewState.AVAILABLE:
            return QuickDetailPreviewResult(QuickDetailPreviewState.AVAILABLE, result.content)
        return QuickDetailPreviewResult(QuickDetailPreviewState(result.state.value))
