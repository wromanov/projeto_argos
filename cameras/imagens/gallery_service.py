"""Leitura bounded da galeria E4 de imagens de uma câmera."""

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
import logging
from typing import Callable
from uuid import UUID

from django.core.files.storage import default_storage

from cameras.models import CameraImageRecord


MAX_GALLERY_IMAGES = 3
logger = logging.getLogger(__name__)


class GalleryState(StrEnum):
    EMPTY = "EMPTY"
    AVAILABLE = "AVAILABLE"
    OVER_LIMIT = "OVER_LIMIT"


class GalleryImageState(StrEnum):
    AVAILABLE = "AVAILABLE"
    UNAVAILABLE = "UNAVAILABLE"
    ERROR = "ERROR"


@dataclass(frozen=True, slots=True)
class CameraGalleryImage:
    immutable_id: UUID
    provenance: str
    captured_at: datetime | None
    recorded_at: datetime
    state: GalleryImageState


@dataclass(frozen=True, slots=True)
class CameraGalleryResult:
    state: GalleryState
    images: tuple[CameraGalleryImage, ...]


class CameraGalleryReadService:
    """Projeta no máximo três registros ativos, sem expor dados de storage."""

    def __init__(self, *, storage_exists: Callable[[str], bool] | None = None):
        self._storage_exists = storage_exists or default_storage.exists

    def list_active(self, camera_id: int) -> CameraGalleryResult:
        records = list(
            CameraImageRecord.objects.filter(
                camera_id=camera_id,
                withdrawn_at__isnull=True,
                provenance__in=(
                    CameraImageRecord.Provenance.CAPTURA_CAMERA,
                    CameraImageRecord.Provenance.UPLOAD_MANUAL,
                ),
            )
            .only(
                "id", "camera_id", "provenance", "captured_at", "recorded_at",
                "storage_key", "sha256", "integrity_status",
            )
            .order_by("recorded_at", "id")[: MAX_GALLERY_IMAGES + 1]
        )
        if len(records) > MAX_GALLERY_IMAGES:
            logger.warning(
                "Camera image gallery active-record limit exceeded",
                extra={"camera_id": camera_id, "active_image_limit": MAX_GALLERY_IMAGES},
            )
            return CameraGalleryResult(GalleryState.OVER_LIMIT, ())
        if not records:
            return CameraGalleryResult(GalleryState.EMPTY, ())

        images = tuple(self._project(record) for record in records)
        return CameraGalleryResult(GalleryState.AVAILABLE, images)

    def _project(self, record: CameraImageRecord) -> CameraGalleryImage:
        if (
            record.integrity_status != CameraImageRecord.IntegrityStatus.VALID
            or len(record.sha256) != 64
            or any(char not in "0123456789abcdef" for char in record.sha256)
        ):
            state = GalleryImageState.ERROR
        else:
            try:
                exists = self._storage_exists(record.storage_key)
            except Exception:
                exists = False
            state = GalleryImageState.AVAILABLE if exists else GalleryImageState.UNAVAILABLE
        return CameraGalleryImage(
            immutable_id=record.pk,
            provenance=record.provenance,
            captured_at=record.captured_at,
            recorded_at=record.recorded_at,
            state=state,
        )
