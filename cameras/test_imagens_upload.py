from hashlib import sha256
from io import BytesIO
from tempfile import TemporaryDirectory
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.exceptions import ValidationError
from django.core.files.storage import default_storage
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

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
