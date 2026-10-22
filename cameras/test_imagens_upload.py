from hashlib import sha256
from io import BytesIO
from tempfile import TemporaryDirectory
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, TransactionTestCase, override_settings
from django.db import close_old_connections, connection
from django.urls import reverse
from django.utils import timezone

from PIL import Image

from cameras.imagens.read_service import CameraImageReadService, LatestCameraCaptureStatus
from cameras.imagens.upload_service import aceitar_upload_manual
from cameras.models import Camera, CameraImageRecord, EventoAuditoria


def imagem(nome="foto.png"):
    data = BytesIO()
    Image.new("RGB", (3, 2), "red").save(data, format="PNG")
    return SimpleUploadedFile(nome, data.getvalue(), content_type="image/png")


class ManualImageUploadTests(TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.override = override_settings(MEDIA_ROOT=self.temp.name)
        self.override.enable()
        self.addCleanup(self.override.disable)
        self.camera = Camera.objects.create(nome="Câmera A", fabricante="X", modelo="Y")
        self.other = Camera.objects.create(nome="Câmera B", fabricante="X", modelo="Y")
        self.user = get_user_model().objects.create_user(username="uploader", password="test-pass")
        self.url = reverse("cameras:upload_imagem", args=[self.camera.pk])

    def authorize(self):
        self.user.user_permissions.add(
            Permission.objects.get(codename="add_cameraimagerecord"),
            Permission.objects.get(codename="view_camera"),
        )
        self.client.force_login(self.user)

    def test_requires_authentication_and_explicit_permission(self):
        self.assertEqual(self.client.post(self.url, {"imagem": imagem()}).status_code, 302)
        self.client.force_login(self.user)
        self.assertEqual(self.client.post(self.url, {"imagem": imagem()}).status_code, 403)
        self.assertFalse(CameraImageRecord.objects.exists())

    def test_upload_also_requires_camera_view_permission(self):
        self.user.user_permissions.add(Permission.objects.get(codename="add_cameraimagerecord"))
        self.client.force_login(self.user)
        self.assertEqual(self.client.post(self.url, {"imagem": imagem()}).status_code, 403)
        self.assertFalse(CameraImageRecord.objects.exists())

    def test_valid_upload_records_facts_audit_and_stays_out_of_latest_capture(self):
        self.authorize()
        response = self.client.post(self.url, {"imagem": imagem("../unsafe.png")}, follow=True)
        self.assertEqual(response.status_code, 200)
        record = CameraImageRecord.objects.get()
        self.assertEqual(record.camera, self.camera)
        self.assertEqual(record.provenance, "UPLOAD_MANUAL")
        self.assertEqual(record.uploaded_by, self.user)
        self.assertIsNone(record.captured_at)
        self.assertIsNotNone(record.recorded_at)
        self.assertEqual((record.width, record.height), (3, 2))
        self.assertEqual(record.size_bytes, default_storage.size(record.storage_key))
        self.assertEqual(len(record.sha256), 64)
        with default_storage.open(record.storage_key, "rb") as stored:
            self.assertEqual(record.sha256, sha256(stored.read()).hexdigest())
        self.assertTrue(record.storage_key.startswith(f"camera-images/{self.camera.pk}/"))
        self.assertNotIn("unsafe", record.storage_key)
        self.assertEqual(self.other.image_records.count(), 0)
        self.assertTrue(EventoAuditoria.objects.filter(codigo="imagem.upload_manual", camera=self.camera).exists())
        self.assertEqual(CameraImageReadService().latest_camera_capture(self.camera).status,
                         LatestCameraCaptureStatus.NO_CAPTURE_AVAILABLE)

    def test_empty_invalid_mismatched_and_active_content_rejected(self):
        self.authorize()
        for upload in (
            SimpleUploadedFile("empty.png", b""),
            SimpleUploadedFile("fake.png", b"not an image"),
            imagem("wrong.jpg"),
            SimpleUploadedFile("active.svg", b"<svg><script/></svg>"),
        ):
            with self.subTest(upload=upload.name):
                response = self.client.post(self.url, {"imagem": upload})
                self.assertEqual(response.status_code, 302)
        self.assertFalse(CameraImageRecord.objects.exists())

    def test_database_failure_removes_new_storage_object(self):
        with patch.object(CameraImageRecord, "save", side_effect=RuntimeError("db error")):
            with self.assertRaises(RuntimeError):
                aceitar_upload_manual(camera=self.camera, usuario=self._authorized_user(), arquivo=imagem())
        self.assertEqual(default_storage.listdir("camera-images")[1], [])

    def test_trailing_active_payload_is_not_stored(self):
        self.authorize()
        upload = imagem()
        upload = SimpleUploadedFile("polyglot.png", upload.read() + b"<script>alert(1)</script>")
        self.client.post(self.url, {"imagem": upload})
        record = CameraImageRecord.objects.get()
        with default_storage.open(record.storage_key, "rb") as stored:
            self.assertNotIn(b"<script>", stored.read())

    def test_superuser_can_upload_and_action_is_visible(self):
        admin = get_user_model().objects.create_superuser(username="admin_img", password="test-pass")
        self.client.force_login(admin)
        detail = self.client.get(reverse("cameras:detalhe", args=[self.camera.pk]))
        self.assertContains(detail, self.url)
        self.assertEqual(self.client.post(self.url, {"imagem": imagem()}).status_code, 302)
        self.assertEqual(CameraImageRecord.objects.get().uploaded_by, admin)

    def _authorized_user(self):
        self.user.user_permissions.add(Permission.objects.get(codename="add_cameraimagerecord"))
        return self.user

class ImageLifecycleInvariantTests(TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.override = override_settings(MEDIA_ROOT=self.temp.name)
        self.override.enable()
        self.addCleanup(self.override.disable)
        self.camera = Camera.objects.create(nome="Lifecycle", fabricante="X", modelo="Y")
        self.user = get_user_model().objects.create_user(username="lifecycle")

    def seed(self, *, recorded_at, held=False):
        data = f"legacy-image-{CameraImageRecord.objects.count()}".encode()
        storage_key = default_storage.save(
            f"camera-images/{self.camera.pk}/legacy-{CameraImageRecord.objects.count()}.png",
            ContentFile(data),
        )
        return CameraImageRecord.objects.create(
            camera=self.camera,
            provenance=CameraImageRecord.Provenance.UPLOAD_MANUAL,
            recorded_at=recorded_at,
            storage_key=storage_key,
            content_type="image/png",
            size_bytes=len(data),
            sha256=sha256(data).hexdigest(),
            retention_held_at=recorded_at if held else None,
            retention_held_by=self.user if held else None,
        )

    def persist(self):
        from cameras.imagens.lifecycle_service import persist_validated_image

        return persist_validated_image(
            camera=self.camera,
            provenance=CameraImageRecord.Provenance.UPLOAD_MANUAL,
            data=b"new-bytes",
            content_type="image/png",
            extension="png",
            width=1,
            height=1,
            sha256="b" * 64,
        )

    def test_acceptance_rotates_only_oldest_to_keep_three_active(self):
        from datetime import timedelta
        from django.utils import timezone

        now = timezone.now()
        rows = [self.seed(recorded_at=now - timedelta(days=day)) for day in (3, 2, 1)]
        created = self.persist()
        self.assertEqual(
            list(CameraImageRecord.objects.filter(camera=self.camera, withdrawn_at__isnull=True)
                 .order_by("recorded_at", "pk").values_list("pk", flat=True)),
            [rows[1].pk, rows[2].pk, created.pk],
        )
        rows[0].refresh_from_db()
        self.assertEqual(rows[0].withdrawal_reason, "ROTATED_BY_CAMERA_LIMIT")
        self.assertTrue(all(default_storage.exists(row.storage_key) for row in rows))

    def test_three_held_records_block_acceptance_and_preserve_history(self):
        from datetime import timedelta
        from django.core.exceptions import ValidationError
        from django.utils import timezone
        from cameras.imagens.lifecycle_service import ImageLifecycleCapacityError

        now = timezone.now()
        held = [self.seed(recorded_at=now - timedelta(days=day), held=True) for day in (3, 2, 1)]
        with self.assertRaises(ImageLifecycleCapacityError):
            self.persist()
        self.assertEqual(CameraImageRecord.objects.filter(camera=self.camera, withdrawn_at__isnull=True).count(), 3)
        self.assertEqual([row.refresh_from_db() or row.withdrawn_at for row in held], [None, None, None])
        self.assertTrue(all(default_storage.exists(row.storage_key) for row in held))

    def test_update_and_bulk_update_cannot_bypass_image_facts(self):
        from django.core.exceptions import ValidationError

        row = self.seed(recorded_at=timezone.now())
        with self.assertRaises(ValidationError):
            CameraImageRecord.objects.filter(pk=row.pk).update(sha256="c" * 64)
        row.sha256 = "d" * 64
        with self.assertRaises(ValidationError):
            CameraImageRecord.objects.bulk_update([row], ["sha256"])

    def test_expiration_is_calendar_months_logical_and_hold_aware(self):
        from datetime import timedelta
        from cameras.imagens.lifecycle_service import expire_due_images
        from django.utils import timezone

        now = timezone.now()
        old = self.seed(recorded_at=now - timedelta(days=400))
        held_old = self.seed(recorded_at=now - timedelta(days=400), held=True)
        recent = self.seed(recorded_at=now - timedelta(days=20))
        expired = expire_due_images(batch_size=10, camera_id=self.camera.pk)
        self.assertEqual(expired, 1)
        old.refresh_from_db()
        held_old.refresh_from_db()
        recent.refresh_from_db()
        self.assertEqual(old.withdrawal_reason, "RETENTION_12_MONTHS")
        self.assertIsNone(held_old.withdrawn_at)
        self.assertIsNone(recent.withdrawn_at)
        self.assertTrue(EventoAuditoria.objects.filter(
            codigo="imagem.retencao.expirada", camera=self.camera
        ).exists())

    def test_hold_requires_global_and_camera_scoped_permission(self):
        from django.contrib.auth.models import Permission
        from django.core.exceptions import PermissionDenied
        from cameras.imagens.lifecycle_service import set_image_hold
        from django.utils import timezone

        row = self.seed(recorded_at=timezone.now())
        permission = Permission.objects.get(
            content_type__app_label="cameras", codename="manage_camera_image_hold"
        )
        self.user.user_permissions.add(permission)
        with self.assertRaises(PermissionDenied):
            set_image_hold(actor=self.user, camera_id=self.camera.pk, image_id=row.pk)
        row.refresh_from_db()
        self.assertIsNone(row.retention_held_at)
        self.assertFalse(EventoAuditoria.objects.filter(
            codigo="imagem.hold.ativado", camera=self.camera
        ).exists())

    def test_storage_failure_creates_no_record(self):
        from unittest.mock import patch
        from cameras.imagens.lifecycle_service import ImageLifecycleStorageError

        with patch("cameras.imagens.lifecycle_service.default_storage.save", side_effect=OSError):
            with self.assertRaises(ImageLifecycleStorageError):
                self.persist()
        self.assertFalse(CameraImageRecord.objects.filter(camera=self.camera).exists())

    def test_calendar_month_clamps_leap_day(self):
        from datetime import datetime, timezone as dt_timezone
        from cameras.imagens.lifecycle_service import add_calendar_months

        self.assertEqual(
            add_calendar_months(datetime(2024, 2, 29, 12, tzinfo=dt_timezone.utc), 12),
            datetime(2025, 2, 28, 12, tzinfo=dt_timezone.utc),
        )

    def test_audit_failure_rolls_back_and_compensates_only_new_object(self):
        from unittest.mock import patch
        from django.core.files.base import ContentFile

        old_key = default_storage.save(
            f"camera-images/{self.camera.pk}/historical.png", ContentFile(b"historical")
        )
        prior = CameraImageRecord.objects.create(
            camera=self.camera,
            provenance=CameraImageRecord.Provenance.UPLOAD_MANUAL,
            recorded_at=timezone.now(),
            storage_key=old_key,
            content_type="image/png",
            size_bytes=10,
            sha256="e" * 64,
        )
        with patch("cameras.auditoria.registrar_evento", side_effect=RuntimeError("audit failed")):
            with self.assertRaises(RuntimeError):
                self.persist()
        self.assertEqual(CameraImageRecord.objects.filter(camera=self.camera).count(), 1)
        self.assertTrue(default_storage.exists(old_key))
        self.assertEqual(default_storage.size(old_key), 10)
        self.assertFalse(EventoAuditoria.objects.filter(camera=self.camera).exists())

    def test_hold_release_with_explicit_camera_scope(self):
        from unittest.mock import patch
        from cameras.imagens.lifecycle_service import set_image_hold

        row = self.seed(recorded_at=timezone.now())
        permission = "cameras.manage_camera_image_hold"

        def scoped_has_perm(perm, obj=None):
            return perm == permission and (obj is None or obj.pk == self.camera.pk)

        with patch.object(self.user, "has_perm", side_effect=scoped_has_perm):
            set_image_hold(actor=self.user, camera_id=self.camera.pk, image_id=row.pk)
            row.refresh_from_db()
            self.assertIsNotNone(row.retention_held_at)
            self.assertEqual(row.retention_held_by, self.user)
            set_image_hold(actor=self.user, camera_id=self.camera.pk, image_id=row.pk, held=False)
        row.refresh_from_db()
        self.assertIsNone(row.retention_held_at)
        self.assertIsNone(row.retention_held_by)
        self.assertEqual(EventoAuditoria.objects.filter(
            camera=self.camera, codigo__in=["imagem.hold.ativado", "imagem.hold.liberado"]
        ).count(), 2)

    def test_hold_metadata_requires_actor_and_timestamp_together(self):
        from django.db import IntegrityError, transaction

        row = self.seed(recorded_at=timezone.now())
        table = connection.ops.quote_name(CameraImageRecord._meta.db_table)
        pk = CameraImageRecord._meta.pk.get_db_prep_value(row.pk, connection)
        actor_field = CameraImageRecord._meta.get_field("retention_held_by")
        actor_pk = actor_field.target_field.get_db_prep_value(self.user.pk, connection)
        invalid_updates = (("retention_held_at", timezone.now()), ("retention_held_by_id", actor_pk))
        for column, value in invalid_updates:
            with self.subTest(column=column):
                with self.assertRaises(IntegrityError):
                    with transaction.atomic():
                        with connection.cursor() as cursor:
                            cursor.execute(
                                f"UPDATE {table} SET {connection.ops.quote_name(column)} = %s WHERE id = %s",
                                [value, pk],
                            )

class LifecycleConcurrentAcceptanceTests(TransactionTestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.override = override_settings(MEDIA_ROOT=self.temp.name)
        self.override.enable()
        self.addCleanup(self.override.disable)
        self.camera = Camera.objects.create(nome="Concurrent lifecycle", fabricante="X", modelo="Y")

    def test_same_camera_acceptance_serializes_when_row_locks_are_supported(self):
        if not connection.features.has_select_for_update:
            self.skipTest("O backend não oferece SELECT FOR UPDATE.")

        from concurrent.futures import ThreadPoolExecutor
        from threading import Barrier
        from cameras.imagens.lifecycle_service import persist_validated_image

        camera_id = self.camera.pk
        gate = Barrier(5)

        def accept(_index):
            close_old_connections()
            try:
                gate.wait(timeout=15)
                return persist_validated_image(
                    camera=Camera.objects.get(pk=camera_id),
                    provenance=CameraImageRecord.Provenance.UPLOAD_MANUAL,
                    data=b"concurrent-image",
                    content_type="image/png",
                    extension="png",
                    width=1,
                    height=1,
                    sha256=sha256(b"concurrent-image").hexdigest(),
                )
            finally:
                close_old_connections()

        with ThreadPoolExecutor(max_workers=5) as pool:
            accepted = list(pool.map(accept, range(5)))

        self.assertEqual(len(accepted), 5)
        self.assertEqual(
            CameraImageRecord.objects.filter(camera=self.camera, withdrawn_at__isnull=True).count(),
            3,
        )
        records = CameraImageRecord.objects.filter(camera=self.camera)
        self.assertEqual(records.count(), 5)
        self.assertTrue(all(default_storage.exists(key) for key in records.values_list("storage_key", flat=True)))
