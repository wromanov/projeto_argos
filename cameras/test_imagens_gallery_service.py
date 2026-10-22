"""Testes direcionados dos serviços de listagem e preview da galeria E4."""

from datetime import datetime, timedelta, timezone
from hashlib import sha256
from io import BytesIO
from uuid import UUID, uuid4

from django.db import connection
from django.test import SimpleTestCase, TestCase, override_settings
from PIL import Image

from cameras.imagens.gallery_preview_service import (
    CameraGalleryPreviewResult,
    CameraGalleryPreviewService,
    GalleryPreviewState,
    VARIANT_BOUNDS,
)
from cameras.imagens.gallery_service import (
    CameraGalleryReadService,
    GalleryImageState,
    GalleryState,
)
from cameras.models import Camera, CameraImageRecord


NOW = datetime(2026, 10, 18, 13, 42, tzinfo=timezone.utc)


class MemoryStorage:
    def __init__(self):
        self.objects = {}
        self.exists_checks = []

    def exists(self, key):
        self.exists_checks.append(key)
        return key in self.objects

    def open(self, key, mode="rb"):
        if key not in self.objects:
            raise FileNotFoundError
        return BytesIO(self.objects[key])


class GalleryServicesTests(TestCase):
    def setUp(self):
        self.storage = MemoryStorage()
        self.camera = Camera.objects.create(nome="E4 sintética A")
        self.other_camera = Camera.objects.create(nome="E4 sintética B")
        self.read = CameraGalleryReadService(storage_exists=self.storage.exists)
        self.preview = CameraGalleryPreviewService(storage=self.storage)
        self.counter = 0

    def image_bytes(self, size=(400, 100), color="red", fmt="PNG"):
        buffer = BytesIO()
        Image.new("RGB", size, color).save(buffer, format=fmt)
        return buffer.getvalue()

    def record(
        self,
        *,
        camera=None,
        provenance=CameraImageRecord.Provenance.CAPTURA_CAMERA,
        recorded_at=None,
        captured_at=None,
        immutable_id=None,
        data=None,
        storage_present=True,
        integrity_status=CameraImageRecord.IntegrityStatus.VALID,
        digest=None,
        withdrawn_at=None,
    ):
        self.counter += 1
        camera = camera or self.camera
        data = data if data is not None else self.image_bytes()
        key = f"opaque/{self.counter}"
        if storage_present:
            self.storage.objects[key] = data
        if provenance == CameraImageRecord.Provenance.CAPTURA_CAMERA:
            captured_at = captured_at or NOW
        else:
            captured_at = None
        fields = {
            "camera": camera,
            "provenance": provenance,
            "captured_at": captured_at,
            "recorded_at": recorded_at or NOW,
            "storage_key": key,
            "content_type": "image/png",
            "size_bytes": len(data),
            "width": 400,
            "height": 100,
            "sha256": digest or sha256(data).hexdigest(),
            "integrity_status": integrity_status,
            "withdrawn_at": withdrawn_at,
            "withdrawal_reason": "retirada sintética" if withdrawn_at is not None else "",
        }
        if immutable_id is not None:
            fields["id"] = immutable_id
        return CameraImageRecord.objects.create(**fields)

    def test_empty_one_two_three_and_both_provenances(self):
        self.assertEqual(self.read.list_active(self.camera.pk).state, GalleryState.EMPTY)
        one = self.record()
        result = self.read.list_active(self.camera.pk)
        self.assertEqual((result.state, len(result.images)), (GalleryState.AVAILABLE, 1))
        self.assertEqual(result.images[0].immutable_id, one.pk)

        self.record(provenance=CameraImageRecord.Provenance.UPLOAD_MANUAL)
        two = self.read.list_active(self.camera.pk)
        self.assertEqual((two.state, len(two.images)), (GalleryState.AVAILABLE, 2))
        self.record(provenance=CameraImageRecord.Provenance.CAPTURA_CAMERA)
        result = self.read.list_active(self.camera.pk)
        self.assertEqual((result.state, len(result.images)), (GalleryState.AVAILABLE, 3))
        self.assertEqual(
            {image.provenance for image in result.images},
            {"CAPTURA_CAMERA", "UPLOAD_MANUAL"},
        )
        manual = next(image for image in result.images if image.provenance == "UPLOAD_MANUAL")
        capture = next(image for image in result.images if image.provenance == "CAPTURA_CAMERA")
        self.assertIsNone(manual.captured_at)
        self.assertIsNotNone(manual.recorded_at)
        self.assertIsNotNone(capture.captured_at)

    def test_orders_recorded_at_then_uuid_and_exposes_no_storage_metadata(self):
        when = NOW - timedelta(minutes=1)
        first_id = UUID("00000000-0000-0000-0000-000000000001")
        second_id = UUID("00000000-0000-0000-0000-000000000002")
        later_id = UUID("ffffffff-ffff-ffff-ffff-ffffffffffff")
        self.record(recorded_at=when, immutable_id=second_id)
        self.record(recorded_at=when, immutable_id=first_id)
        self.record(recorded_at=NOW, immutable_id=later_id)

        result = self.read.list_active(self.camera.pk)
        self.assertEqual([image.immutable_id for image in result.images], [first_id, second_id, later_id])
        self.assertFalse(hasattr(result.images[0], "storage_key"))
        self.assertFalse(hasattr(result.images[0], "path"))

    def test_camera_filter_withdrawn_records_and_three_active_plus_withdrawn(self):
        own = self.record()
        self.record(camera=self.other_camera)
        self.record(withdrawn_at=NOW)
        self.record(provenance=CameraImageRecord.Provenance.UPLOAD_MANUAL)
        self.record(provenance=CameraImageRecord.Provenance.CAPTURA_CAMERA)
        result = self.read.list_active(self.camera.pk)
        self.assertEqual(result.state, GalleryState.AVAILABLE)
        self.assertEqual(len(result.images), 3)
        self.assertIn(own.pk, [image.immutable_id for image in result.images])
        self.assertEqual(len(self.storage.exists_checks), 3)

    def test_more_than_three_active_returns_over_limit_without_selecting_or_storage_checks(self):
        for _ in range(4):
            self.record()
        with self.assertLogs("cameras.imagens.gallery_service", level="WARNING") as logged:
            result = self.read.list_active(self.camera.pk)
        self.assertEqual((result.state, result.images), (GalleryState.OVER_LIMIT, ()))
        self.assertEqual(self.storage.exists_checks, [])
        self.assertIn("active-record limit exceeded", logged.output[0])

    def test_integrity_hash_and_storage_failures_are_sanitized_states(self):
        bad_integrity = self.record(integrity_status=CameraImageRecord.IntegrityStatus.INVALID)
        bad_hash = self.record()
        table = connection.ops.quote_name(CameraImageRecord._meta.db_table)
        database_pk = CameraImageRecord._meta.pk.get_db_prep_value(bad_hash.pk, connection)
        with connection.cursor() as cursor:
            cursor.execute(f"UPDATE {table} SET sha256 = %s WHERE id = %s", ["bad", database_pk])
        missing = self.record(storage_present=False)
        result = self.read.list_active(self.camera.pk)
        states = {image.immutable_id: image.state for image in result.images}
        self.assertEqual(states[bad_integrity.pk], GalleryImageState.ERROR)
        self.assertEqual(states[bad_hash.pk], GalleryImageState.ERROR)
        self.assertEqual(states[missing.pk], GalleryImageState.UNAVAILABLE)
        self.assertEqual(self.storage.exists_checks, [missing.storage_key])

    def test_preview_is_camera_and_active_identity_bound_and_variant_closed(self):
        record = self.record()
        wrong_camera = self.preview.deliver(self.other_camera.pk, record.pk, "FULL")
        self.assertEqual(wrong_camera.state, GalleryPreviewState.NOT_FOUND)
        table = connection.ops.quote_name(CameraImageRecord._meta.db_table)
        database_pk = CameraImageRecord._meta.pk.get_db_prep_value(record.pk, connection)
        with connection.cursor() as cursor:
            cursor.execute(
                f"UPDATE {table} SET withdrawn_at = %s, withdrawal_reason = %s WHERE id = %s",
                [NOW, "retirada sintética", database_pk],
            )
        withdrawn = self.preview.deliver(self.camera.pk, record.pk, "FULL")
        self.assertEqual(withdrawn.state, GalleryPreviewState.NOT_FOUND)
        invalid_variant = self.preview.deliver(self.camera.pk, record.pk, "SOURCE")
        self.assertEqual(invalid_variant.state, GalleryPreviewState.ERROR)
        self.assertEqual(self.storage.exists_checks, [])

    def test_preview_missing_identity_storage_and_corrupt_hash(self):
        self.assertEqual(
            self.preview.deliver(self.camera.pk, uuid4(), "THUMB").state,
            GalleryPreviewState.NOT_FOUND,
        )
        missing = self.record(storage_present=False)
        self.assertEqual(
            self.preview.deliver(self.camera.pk, missing.pk, "THUMB").state,
            GalleryPreviewState.UNAVAILABLE,
        )
        tampered = self.record(digest="a" * 64)
        self.assertEqual(
            self.preview.deliver(self.camera.pk, tampered.pk, "THUMB").state,
            GalleryPreviewState.ERROR,
        )

    @override_settings(ARGOS_PREVIEW_MAX_SOURCE_BYTES=20 * 1024 * 1024,
                       ARGOS_PREVIEW_MAX_SOURCE_PIXELS=20_000_000)
    def test_variants_preserve_geometry_do_not_crop_or_enlarge_and_emit_clean_jpeg(self):
        record = self.record(data=self.image_bytes((4000, 1000)))
        thumb = self.preview.deliver(self.camera.pk, record.pk, "THUMB")
        full = self.preview.deliver(self.camera.pk, record.pk, "FULL")
        self.assertEqual((thumb.state, full.state), (GalleryPreviewState.AVAILABLE,) * 2)
        thumb_size = Image.open(BytesIO(thumb.content)).size
        full_image = Image.open(BytesIO(full.content))
        self.assertEqual(thumb_size[0] / thumb_size[1], 4)
        self.assertEqual(full_image.size[0] / full_image.size[1], 4)
        self.assertLessEqual(thumb_size[0], VARIANT_BOUNDS["THUMB"][0])
        self.assertLessEqual(full_image.size[0], VARIANT_BOUNDS["FULL"][0])
        self.assertGreater(full_image.width, thumb_size[0])
        self.assertEqual(full_image.format, "JPEG")
        self.assertFalse(full_image.info.get("exif"))

        small = self.record(data=self.image_bytes((40, 10), color="blue"))
        small_preview = self.preview.deliver(self.camera.pk, small.pk, "FULL")
        small_size = Image.open(BytesIO(small_preview.content)).size
        self.assertEqual(small_size, (40, 10))


class GalleryServiceSurfaceTests(SimpleTestCase):
    def test_authentication_and_http_headers_are_outside_service_contract(self):
        import inspect

        read_params = inspect.signature(CameraGalleryReadService.list_active).parameters
        preview_params = inspect.signature(CameraGalleryPreviewService.deliver).parameters
        self.assertEqual(set(read_params), {"self", "camera_id"})
        self.assertEqual(set(preview_params), {"self", "camera_id", "immutable_id", "variant"})
        self.assertNotIn("request", read_params)
        self.assertNotIn("user", preview_params)
        self.assertFalse(hasattr(CameraGalleryPreviewResult, "headers"))
