"""Read contract canônico de imagens; não executa captura nem altera monitoramento."""

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import Callable, Iterable
from uuid import UUID

from django.core.files.storage import default_storage
from django.db.models import F, Window
from django.db.models.functions import RowNumber

from cameras.models import Camera, CameraImageRecord


class LatestCameraCaptureStatus(StrEnum):
    NO_CAPTURE_AVAILABLE = "NO_CAPTURE_AVAILABLE"
    AVAILABLE = "AVAILABLE"
    UNAVAILABLE = "UNAVAILABLE"
    ERROR = "ERROR"


@dataclass(frozen=True, slots=True)
class CameraImageMetadata:
    immutable_id: UUID
    camera_id: int
    provenance: str
    captured_at: datetime
    recorded_at: datetime
    content_type: str
    size_bytes: int | None
    width: int | None
    height: int | None
    sha256: str
    integrity_status: str
    original_filename: str


@dataclass(frozen=True, slots=True)
class LatestCameraCaptureResult:
    camera_id: int
    status: LatestCameraCaptureStatus
    metadata: CameraImageMetadata | None


class CameraImageReadService:
    """Consulta metadados em lote e só verifica storage após selecionar o latest.

    storage_exists usa Storage.exists (sem abrir bytes). O storage configurado
    é detalhe local/reversível; esta API não retorna URL nem chave.
    """

    def __init__(self, *, storage_exists: Callable[[str], bool] | None = None) -> None:
        self._storage_exists = storage_exists or default_storage.exists

    @staticmethod
    def _camera_id(camera: Camera | int) -> int:
        return camera.pk if isinstance(camera, Camera) else int(camera)

    def latest_camera_capture(self, camera: Camera | int) -> LatestCameraCaptureResult:
        camera_id = self._camera_id(camera)
        return self.latest_camera_captures((camera_id,))[camera_id]

    def latest_camera_captures(
        self, cameras: Iterable[Camera | int]
    ) -> dict[int, LatestCameraCaptureResult]:
        """Retorna latest de várias câmeras usando uma consulta ORM de janela."""
        camera_ids = tuple(dict.fromkeys(self._camera_id(camera) for camera in cameras))
        results = {
            camera_id: LatestCameraCaptureResult(
                camera_id=camera_id,
                status=LatestCameraCaptureStatus.NO_CAPTURE_AVAILABLE,
                metadata=None,
            )
            for camera_id in camera_ids
        }
        if not camera_ids:
            return results

        latest_records = (
            CameraImageRecord.objects.filter(
                camera_id__in=camera_ids,
                provenance=CameraImageRecord.Provenance.CAPTURA_CAMERA,
                withdrawn_at__isnull=True,
            )
            .only(
                "id",
                "camera_id",
                "provenance",
                "captured_at",
                "recorded_at",
                "storage_key",
                "content_type",
                "size_bytes",
                "width",
                "height",
                "sha256",
                "integrity_status",
                "original_filename",
            )
            .annotate(
                _latest_rank=Window(
                    expression=RowNumber(),
                    partition_by=[F("camera_id")],
                    order_by=[
                        F("captured_at").desc(),
                        F("recorded_at").desc(),
                        F("id").desc(),
                    ],
                )
            )
            .filter(_latest_rank=1)
        )

        for record in latest_records:
            results[record.camera_id] = self._project(record)
        return results

    def _project(self, record: CameraImageRecord) -> LatestCameraCaptureResult:
        metadata = CameraImageMetadata(
            immutable_id=record.pk,
            camera_id=record.camera_id,
            provenance=record.provenance,
            captured_at=record.captured_at,
            recorded_at=record.recorded_at,
            content_type=record.content_type,
            size_bytes=record.size_bytes,
            width=record.width,
            height=record.height,
            sha256=record.sha256,
            integrity_status=record.integrity_status,
            original_filename=record.original_filename,
        )
        if (
            record.integrity_status != CameraImageRecord.IntegrityStatus.VALID
            or len(record.sha256) != 64
            or any(char not in "0123456789abcdef" for char in record.sha256)
        ):
            status = LatestCameraCaptureStatus.ERROR
        else:
            try:
                available = self._storage_exists(record.storage_key)
            except Exception:
                # Storage failure is explicit and never changes which record was selected.
                available = False
            status = (
                LatestCameraCaptureStatus.AVAILABLE
                if available
                else LatestCameraCaptureStatus.UNAVAILABLE
            )
        return LatestCameraCaptureResult(
            camera_id=record.camera_id,
            status=status,
            metadata=metadata,
        )
