"""Seleção de imagem exclusiva do painel Quick Detail (ARGOS IMG-07)."""

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from uuid import UUID

from django.core.files.storage import default_storage
from django.db.models import F

from cameras.models import CameraImageRecord
from .read_service import CameraImageReadService, LatestCameraCaptureStatus


class QuickDetailImageState(StrEnum):
    AVAILABLE = "AVAILABLE"
    NO_IMAGE_AVAILABLE = "NO_IMAGE_AVAILABLE"
    UNAVAILABLE = "UNAVAILABLE"
    ERROR = "ERROR"


@dataclass(frozen=True, slots=True)
class QuickDetailImageResult:
    camera_id: int
    state: QuickDetailImageState
    source: str
    capture_state: LatestCameraCaptureStatus
    immutable_id: UUID | None
    recorded_at: datetime | None


class QuickDetailImageReadService:
    """Seleciona primeiro o registro corrente; validação nunca promove fallback."""

    def __init__(self, *, storage_exists=None):
        self.storage_exists = storage_exists or default_storage.exists

    @staticmethod
    def latest_active_record(camera_id: int):
        return CameraImageRecord.objects.filter(
            camera_id=camera_id,
            withdrawn_at__isnull=True,
        ).order_by(F("recorded_at").desc(), F("id").desc()).first()

    def select(self, camera_id: int) -> QuickDetailImageResult:
        capture = CameraImageReadService(storage_exists=self.storage_exists).latest_camera_capture(camera_id)
        record = self.latest_active_record(camera_id)
        if record is None:
            return QuickDetailImageResult(
                camera_id, QuickDetailImageState.NO_IMAGE_AVAILABLE, "NONE",
                capture.status, None, None,
            )

        if (record.integrity_status != CameraImageRecord.IntegrityStatus.VALID
                or len(record.sha256) != 64
                or any(char not in "0123456789abcdef" for char in record.sha256)):
            state = QuickDetailImageState.ERROR
        else:
            try:
                available = self.storage_exists(record.storage_key)
            except Exception:
                available = False
            state = QuickDetailImageState.AVAILABLE if available else QuickDetailImageState.UNAVAILABLE

        return QuickDetailImageResult(
            camera_id, state, record.provenance, capture.status, record.pk, record.recorded_at,
        )
