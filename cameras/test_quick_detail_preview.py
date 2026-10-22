"""Testes de segurança e stale selection da preview IMG-07."""

from datetime import timedelta
from hashlib import sha256
from io import BytesIO
from tempfile import TemporaryDirectory
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone
from PIL import Image

from cameras.imagens.lifecycle_service import expire_due_images
from cameras.imagens.preview_service import PreviewResult, PreviewState
from cameras.models import Camera, CameraImageRecord


class QuickDetailPreviewTests(TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        override = override_settings(MEDIA_ROOT=self.temp.name)
        override.enable()
        self.addCleanup(override.disable)
        self.camera = Camera.objects.create(nome="Câmera IMG-07")
        self.other_camera = Camera.objects.create(nome="Outra câmera IMG-07")
        self.user = get_user_model().objects.create_user(username="img07-viewer", password="test-pass")

    def allow_view(self):
        self.user.user_permissions.add(Permission.objects.get(codename="view_camera"))
        self.client.force_login(self.user)

    def make_record(self, *, camera=None, recorded_at=None, color="red"):
        camera = camera or self.camera
        buffer = BytesIO()
        Image.new("RGB", (64, 48), color).save(buffer, format="PNG")
        data = buffer.getvalue()
        key = f"img07-synthetic/{camera.pk}/{timezone.now().timestamp()}-{color}.png"
        default_storage.save(key, ContentFile(data))
        return CameraImageRecord.objects.create(
            camera=camera, provenance=CameraImageRecord.Provenance.UPLOAD_MANUAL,
            recorded_at=recorded_at or timezone.now(), storage_key=key, content_type="image/png",
            size_bytes=len(data), width=64, height=48, sha256=sha256(data).hexdigest(),
            integrity_status=CameraImageRecord.IntegrityStatus.VALID,
        )

    def url(self, record, *, camera=None, variant="PANEL"):
        return reverse("cameras:preview_quick_detail", args=[(camera or self.camera).pk, record.pk, variant])

    def test_auth_permission_wrong_camera_variant_and_private_headers(self):
        record = self.make_record()
        self.assertEqual(self.client.get(self.url(record)).status_code, 401)
        self.client.force_login(self.user)
        self.assertEqual(self.client.get(self.url(record)).status_code, 403)
        self.allow_view()
        wrong_camera = self.client.get(self.url(record, camera=self.other_camera))
        self.assertEqual((wrong_camera.status_code, wrong_camera["X-Preview-State"]), (404, "NOT_FOUND"))
        invalid_variant = self.client.get(self.url(record, variant="SOURCE"))
        self.assertEqual((invalid_variant.status_code, invalid_variant["X-Preview-State"]), (400, "INVALID_VARIANT"))
        response = self.client.get(self.url(record))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "image/jpeg")
        self.assertEqual(response["Cache-Control"], "no-store")
        self.assertEqual(response["X-Content-Type-Options"], "nosniff")
        self.assertEqual(response["X-Preview-State"], "AVAILABLE")
        self.assertNotIn("img07-synthetic", response.content.decode("latin-1"))

    def test_withdrawn_or_superseded_identity_is_stale_without_bytes(self):
        self.allow_view()
        record = self.make_record(recorded_at=timezone.now() - timedelta(days=400))
        self.assertEqual(expire_due_images(camera_id=self.camera.pk), 1)
        response = self.client.get(self.url(record))
        self.assertEqual((response.status_code, response["X-Preview-State"], response.content),
                         (409, "STALE_SELECTION", b""))

        old = self.make_record(recorded_at=timezone.now() - timedelta(minutes=1), color="blue")
        self.make_record(recorded_at=timezone.now(), color="green")
        response = self.client.get(self.url(old))
        self.assertEqual((response.status_code, response["X-Preview-State"], response.content),
                         (409, "STALE_SELECTION", b""))

    def test_selection_change_during_image_processing_returns_stale_without_bytes(self):
        self.allow_view()
        selected = self.make_record()
        newer_time = timezone.now() + timedelta(seconds=1)

        def change_selection(record, variant):
            self.make_record(recorded_at=newer_time, color="blue")
            return PreviewResult(PreviewState.AVAILABLE, b"synthetic-preview-bytes")

        with patch("cameras.imagens.preview_service.QuickDetailImagePreviewService._deliver_record", side_effect=change_selection):
            response = self.client.get(self.url(selected))
        self.assertEqual((response.status_code, response["X-Preview-State"], response.content),
                         (409, "STALE_SELECTION", b""))
