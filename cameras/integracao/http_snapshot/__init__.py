"""HTTP snapshot acquisition boundary."""

from .adapter import (
    HttpSnapshotAdapter,
    SnapshotCaptureError,
    SnapshotImage,
    SnapshotRequest,
)

__all__ = [
    "HttpSnapshotAdapter",
    "SnapshotCaptureError",
    "SnapshotImage",
    "SnapshotRequest",
]
