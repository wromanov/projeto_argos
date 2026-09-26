"""Leitura canônica da imagem apresentada no Inventário e Quick Detail."""

from dataclasses import dataclass
from enum import StrEnum
from typing import Iterable
from uuid import UUID

from django.core.files.storage import default_storage
from django.db.models import F, Window
from django.db.models.functions import RowNumber

from cameras.models import Camera, CameraImageRecord
from .read_service import CameraImageReadService, LatestCameraCaptureStatus


class DisplayImageSource(StrEnum):
    CAPTURA_CAMERA = "CAPTURA_CAMERA"
    UPLOAD_MANUAL = "UPLOAD_MANUAL"
    NONE = "NONE"


class DisplayImageState(StrEnum):
    AVAILABLE = "AVAILABLE"
    NO_IMAGE_AVAILABLE = "NO_IMAGE_AVAILABLE"
    UNAVAILABLE = "UNAVAILABLE"
    ERROR = "ERROR"


@dataclass(frozen=True, slots=True)
class DisplayImageResult:
    camera_id: int
    source: DisplayImageSource
    state: DisplayImageState
    capture_state: LatestCameraCaptureStatus
    fallback_reason: str
    immutable_id: UUID | None


class DisplayImageReadService:
    def __init__(self, *, storage_exists=None):
        self.storage_exists = storage_exists or default_storage.exists
        self.capture_service = CameraImageReadService(storage_exists=self.storage_exists)

    def display_image(self, camera: Camera | int, *, check_storage=True) -> DisplayImageResult:
        camera_id = camera.pk if isinstance(camera, Camera) else int(camera)
        return self.display_images((camera_id,), check_storage=check_storage)[camera_id]

    @staticmethod
    def latest_manual_records(camera_ids: Iterable[int]):
        return (
            CameraImageRecord.objects.filter(
                camera_id__in=camera_ids,
                provenance=CameraImageRecord.Provenance.UPLOAD_MANUAL,
                withdrawn_at__isnull=True,
            )
            .annotate(_latest_rank=Window(
                expression=RowNumber(), partition_by=[F("camera_id")],
                order_by=[F("recorded_at").desc(), F("id").desc()],
            ))
            .filter(_latest_rank=1)
        )

    def display_images(self, cameras: Iterable[Camera | int], *, check_storage=True) -> dict[int, DisplayImageResult]:
        ids = tuple(dict.fromkeys(c.pk if isinstance(c, Camera) else int(c) for c in cameras))
        captures = self.capture_service.latest_camera_captures(ids, check_storage=check_storage)
        missing = [camera_id for camera_id, capture in captures.items()
                   if capture.status == LatestCameraCaptureStatus.NO_CAPTURE_AVAILABLE]
        manuals = {record.camera_id: record for record in self.latest_manual_records(missing)} if missing else {}
        results = {}
        for camera_id, capture in captures.items():
            if capture.status != LatestCameraCaptureStatus.NO_CAPTURE_AVAILABLE:
                results[camera_id] = DisplayImageResult(
                    camera_id, DisplayImageSource.CAPTURA_CAMERA,
                    DisplayImageState(capture.status.value), capture.status,
                    "CAPTURE_HAS_PRIORITY", capture.metadata.immutable_id,
                )
                continue
            record = manuals.get(camera_id)
            if record is None:
                results[camera_id] = DisplayImageResult(
                    camera_id, DisplayImageSource.NONE, DisplayImageState.NO_IMAGE_AVAILABLE,
                    capture.status, "NO_CAPTURE_NO_MANUAL", None,
                )
                continue
            projected = self.capture_service._project(record, check_storage=check_storage)
            results[camera_id] = DisplayImageResult(
                camera_id, DisplayImageSource.UPLOAD_MANUAL,
                DisplayImageState(projected.status.value), capture.status,
                "NO_CAPTURE_AVAILABLE", record.pk,
            )
        return results
