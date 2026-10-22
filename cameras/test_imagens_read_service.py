"""Testes focados do contrato canônico IMG-02."""

from datetime import datetime, timedelta, timezone
from uuid import UUID, uuid4

from django.core.exceptions import ValidationError
from django.db import connection
from django.test import TestCase
from django.test.utils import CaptureQueriesContext

from cameras.imagens.lifecycle_service import expire_due_images
from cameras.models import (
    Camera,
    CameraImageRecord,
    EstadoMonitoramento,
    Indisponibilidade,
    TransicaoEstadoMonitoramento,
)
from cameras.imagens.read_service import (
    CameraImageReadService,
    LatestCameraCaptureStatus,
)


NOW = datetime(2026, 9, 24, 12, tzinfo=timezone.utc)


class CameraImageReadServiceTests(TestCase):
    def setUp(self):
        self.available_keys = set()
        self.storage_checks = []
        self.service = CameraImageReadService(storage_exists=self.storage_exists)
        self.camera_number = 0

    def storage_exists(self, key):
        self.storage_checks.append(key)
        return key in self.available_keys

    def camera(self):
        self.camera_number += 1
        n = self.camera_number
        return Camera.objects.create(
            nome=f"IMG-CAM-{n}",
            fabricante="Axis",
            modelo="M1",
            serial=f"IMG-SER-{n}",
            mac=f"00:11:22:33:44:{n:02X}",
            tipo=Camera.TipoCamera.BULLET,
            terminal="T",
            pavimento="P",
            setor="S",
            ambiente="A",
            ip=f"10.0.0.{n + 1}",
            mascara_subrede="255.255.255.0",
            gateway="10.0.0.1",
            vlan=10,
            farm="F",
            retencao_esperada_dias=1,
            codec="H264",
            status=Camera.StatusCamera.ONLINE,
            status_em=NOW - timedelta(days=1),
            ultima_verificacao=NOW - timedelta(days=1),
        )

    def record(
        self,
        camera,
        *,
        captured_at=NOW,
        recorded_at=NOW,
        provenance=CameraImageRecord.Provenance.CAPTURA_CAMERA,
        immutable_id=None,
        storage_key=None,
        **overrides,
    ):
        values = {
            "camera": camera,
            "provenance": provenance,
            "captured_at": captured_at,
            "recorded_at": recorded_at,
            "storage_key": storage_key or f"opaque/{uuid4().hex}",
            "content_type": "image/jpeg",
            "size_bytes": 128,
            "width": 16,
            "height": 9,
            "sha256": "a" * 64,
            "integrity_status": CameraImageRecord.IntegrityStatus.VALID,
            "recorded_by_system": "img02-test",
        }
        if immutable_id is not None:
            values["id"] = immutable_id
        values.update(overrides)
        return CameraImageRecord.objects.create(**values)

    def test_camera_has_one_to_many_image_records_and_only_two_provenances(self):
        camera = self.camera()
        first = self.record(camera, captured_at=NOW - timedelta(minutes=1))
        second = self.record(camera, captured_at=NOW)
        self.assertEqual(camera.image_records.count(), 2)
        self.assertEqual(
            {choice for choice, _label in CameraImageRecord.Provenance.choices},
            {"CAPTURA_CAMERA", "UPLOAD_MANUAL"},
        )
        self.assertEqual(first.camera_id, second.camera_id)

    def test_capture_time_is_required_for_camera_capture_and_forbidden_for_manual_upload(self):
        camera = self.camera()
        capture = CameraImageRecord(
            camera=camera,
            provenance=CameraImageRecord.Provenance.CAPTURA_CAMERA,
            storage_key="opaque/capture",
            content_type="image/jpeg",
            sha256="a" * 64,
            recorded_by_system="img02-test",
        )
        with self.assertRaises(ValidationError):
            capture.full_clean()

        manual = CameraImageRecord(
            camera=camera,
            provenance=CameraImageRecord.Provenance.UPLOAD_MANUAL,
            captured_at=NOW,
            storage_key="opaque/manual",
            content_type="image/jpeg",
            sha256="b" * 64,
            recorded_by_system="img02-test",
        )
        with self.assertRaises(ValidationError):
            manual.full_clean()

        manual.captured_at = None
        manual.full_clean()

    def test_only_authorized_provenance_values_validate(self):
        record = CameraImageRecord(
            camera=self.camera(),
            provenance="INFERRED_FROM_EXIF",
            captured_at=NOW,
            storage_key="opaque/invalid",
            content_type="image/jpeg",
            sha256="a" * 64,
            recorded_by_system="img02-test",
        )
        with self.assertRaises(ValidationError):
            record.full_clean()

    def test_camera_without_capture_returns_no_capture_available(self):
        result = self.service.latest_camera_capture(self.camera())
        self.assertEqual(result.status, LatestCameraCaptureStatus.NO_CAPTURE_AVAILABLE)
        self.assertIsNone(result.metadata)

    def test_latest_capture_prefers_capture_time_before_recorded_time(self):
        camera = self.camera()
        older_capture = self.record(
            camera,
            captured_at=NOW - timedelta(minutes=1),
            recorded_at=NOW + timedelta(minutes=10),
            storage_key="opaque/older",
        )
        later_capture = self.record(
            camera,
            captured_at=NOW,
            recorded_at=NOW,
            storage_key="opaque/later-capture",
        )
        self.available_keys.update({older_capture.storage_key, later_capture.storage_key})

        result = self.service.latest_camera_capture(camera)

        self.assertEqual(result.metadata.immutable_id, later_capture.pk)
        self.assertEqual(result.status, LatestCameraCaptureStatus.AVAILABLE)
        self.assertFalse(hasattr(result.metadata, "storage_key"))

    def test_equal_capture_times_use_recorded_at_as_tiebreaker(self):
        camera = self.camera()
        first = self.record(camera, recorded_at=NOW, storage_key="opaque/recorded-first")
        second = self.record(
            camera,
            recorded_at=NOW + timedelta(seconds=1),
            storage_key="opaque/recorded-second",
        )
        self.available_keys.add(second.storage_key)

        result = self.service.latest_camera_capture(camera)

        self.assertEqual(result.metadata.immutable_id, second.pk)
        self.assertEqual(result.status, LatestCameraCaptureStatus.AVAILABLE)
        self.assertNotEqual(first.pk, second.pk)

    def test_equal_capture_and_recorded_times_use_immutable_id_as_tiebreaker(self):
        camera = self.camera()
        lower = self.record(
            camera,
            immutable_id=UUID(int=1),
            storage_key="opaque/id-lower",
        )
        higher = self.record(
            camera,
            immutable_id=UUID(int=2),
            storage_key="opaque/id-higher",
        )
        self.available_keys.add(higher.storage_key)

        result = self.service.latest_camera_capture(camera)

        self.assertEqual(result.metadata.immutable_id, higher.pk)
        self.assertEqual(result.status, LatestCameraCaptureStatus.AVAILABLE)
        self.assertNotEqual(lower.pk, higher.pk)

    def test_latest_unavailable_does_not_fall_back_to_older_available_capture(self):
        camera = self.camera()
        older = self.record(
            camera,
            captured_at=NOW - timedelta(minutes=1),
            storage_key="opaque/older-available",
        )
        latest = self.record(camera, storage_key="opaque/latest-missing")
        self.available_keys.add(older.storage_key)

        result = self.service.latest_camera_capture(camera)

        self.assertEqual(result.status, LatestCameraCaptureStatus.UNAVAILABLE)
        self.assertEqual(result.metadata.immutable_id, latest.pk)
        self.assertEqual(self.storage_checks, [latest.storage_key])

    def test_latest_invalid_does_not_fall_back_to_older_available_capture(self):
        camera = self.camera()
        older = self.record(
            camera,
            captured_at=NOW - timedelta(minutes=1),
            storage_key="opaque/older-available",
        )
        latest = self.record(
            camera,
            integrity_status=CameraImageRecord.IntegrityStatus.INVALID,
            storage_key="opaque/latest-invalid",
        )
        self.available_keys.add(older.storage_key)

        result = self.service.latest_camera_capture(camera)

        self.assertEqual(result.status, LatestCameraCaptureStatus.ERROR)
        self.assertEqual(result.metadata.immutable_id, latest.pk)
        self.assertEqual(self.storage_checks, [])

    def test_manual_upload_is_not_eligible_for_latest_camera_capture(self):
        camera = self.camera()
        manual = self.record(
            camera,
            provenance=CameraImageRecord.Provenance.UPLOAD_MANUAL,
            captured_at=None,
            original_filename=r"C:\client\camera.jpg",
            storage_key="opaque/manual",
        )
        self.available_keys.add(manual.storage_key)

        result = self.service.latest_camera_capture(camera)

        self.assertEqual(result.status, LatestCameraCaptureStatus.NO_CAPTURE_AVAILABLE)
        self.assertIsNone(result.metadata)
        self.assertEqual(self.storage_checks, [])

    def test_withdrawn_record_is_excluded_from_current_latest_selection(self):
        camera = self.camera()
        previous = self.record(
            camera,
            captured_at=NOW - timedelta(minutes=1),
            storage_key="opaque/previous",
        )
        current = self.record(
            camera,
            recorded_at=NOW - timedelta(days=400),
            storage_key="opaque/current",
        )
        self.available_keys.update({previous.storage_key, current.storage_key})
        self.assertEqual(expire_due_images(camera_id=camera.pk), 1)

        result = self.service.latest_camera_capture(camera)

        self.assertEqual(result.status, LatestCameraCaptureStatus.AVAILABLE)
        self.assertEqual(result.metadata.immutable_id, previous.pk)

    def test_batch_read_uses_one_orm_query_for_multiple_cameras(self):
        first_camera = self.camera()
        second_camera = self.camera()
        first_record = self.record(first_camera, storage_key="opaque/batch-first")
        second_record = self.record(second_camera, storage_key="opaque/batch-second")
        self.available_keys.update({first_record.storage_key, second_record.storage_key})

        with CaptureQueriesContext(connection) as queries:
            results = self.service.latest_camera_captures([first_camera, second_camera])

        self.assertEqual(len(queries), 1)
        self.assertEqual(results[first_camera.pk].metadata.immutable_id, first_record.pk)
        self.assertEqual(results[second_camera.pk].metadata.immutable_id, second_record.pk)

    def test_read_path_has_no_monitoring_side_effects(self):
        camera = self.camera()
        self.record(camera)
        monitoring = EstadoMonitoramento.objects.create(
            camera=camera,
            estado_estavel=EstadoMonitoramento.EstadoEstavel.ONLINE,
            estado_alterado_em=NOW,
            ultima_evidencia_util_em=NOW,
            em_escopo=True,
        )
        before = (
            monitoring.estado_estavel,
            monitoring.estado_alterado_em,
            monitoring.ultima_evidencia_util_em,
            TransicaoEstadoMonitoramento.objects.filter(camera=camera).count(),
            Indisponibilidade.objects.filter(camera=camera).count(),
        )

        self.service.latest_camera_capture(camera)

        monitoring.refresh_from_db()
        after = (
            monitoring.estado_estavel,
            monitoring.estado_alterado_em,
            monitoring.ultima_evidencia_util_em,
            TransicaoEstadoMonitoramento.objects.filter(camera=camera).count(),
            Indisponibilidade.objects.filter(camera=camera).count(),
        )
        self.assertEqual(after, before)
