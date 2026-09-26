"""Contrato HTTP e integração da entrega privada de previews."""

from datetime import timedelta
from hashlib import sha256
from io import BytesIO
from tempfile import TemporaryDirectory
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db import connection
from django.test import TestCase, override_settings
from django.test.utils import CaptureQueriesContext
from django.urls import reverse
from django.utils import timezone
from PIL import Image

from cameras.models import Camera, CameraImageRecord, EstadoMonitoramento


class PreviewDeliveryTests(TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        override = override_settings(MEDIA_ROOT=self.temp.name)
        override.enable()
        self.addCleanup(override.disable)
        self.camera = Camera.objects.create(nome="Câmera preview", fabricante="X", modelo="Y")
        self.user = get_user_model().objects.create_user(username="viewer", password="test-pass")
        self.url = self.preview_url("THUMB")

    def preview_url(self, variant, camera=None):
        return reverse("cameras:preview_ultima_captura", args=[(camera or self.camera).pk, variant])

    def allow_view(self):
        self.user.user_permissions.add(Permission.objects.get(codename="view_camera"))
        self.client.force_login(self.user)

    def make_record(self, *, camera=None, provenance="CAPTURA_CAMERA", captured_at=None,
                    integrity="VALID", stored=True, color="red"):
        camera = camera or self.camera
        image = BytesIO()
        Image.new("RGB", (1200, 800), color).save(image, format="PNG")
        data = image.getvalue()
        key = f"test-preview/{camera.pk}/{timezone.now().timestamp()}-{color}.png"
        if stored:
            default_storage.save(key, ContentFile(data))
        return CameraImageRecord.objects.create(
            camera=camera, provenance=provenance,
            captured_at=(captured_at or timezone.now()) if provenance == "CAPTURA_CAMERA" else None,
            storage_key=key, content_type="image/png", size_bytes=len(data),
            width=1200, height=800, sha256=sha256(data).hexdigest(),
            integrity_status=integrity, recorded_by_system="preview-test",
        )

    def test_authentication_permission_camera_and_variant(self):
        self.assertEqual(self.client.get(self.url).status_code, 401)
        self.client.force_login(self.user)
        self.assertEqual(self.client.get(self.url).status_code, 403)
        self.allow_view()
        self.assertEqual(self.client.get(self.preview_url("INVALID")).status_code, 400)
        self.assertEqual(self.client.get(self.url, {"storage_key": "../private_media/key"}).status_code, 400)
        self.assertEqual(self.client.get("/cameras/../private_media/key/").status_code, 404)
        self.assertEqual(self.client.get(reverse("cameras:preview_ultima_captura", args=[99999, "THUMB"])).status_code, 404)
        self.assertEqual(self.client.get(self.url)["X-Preview-State"], "NO_CAPTURE_AVAILABLE")

    def test_available_variants_are_valid_rasters_with_private_headers(self):
        self.allow_view()
        self.make_record()
        for variant, size in (("THUMB", (60, 42)), ("PANEL", (640, 448))):
            with self.subTest(variant=variant):
                response = self.client.get(self.preview_url(variant))
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response["Content-Type"], "image/jpeg")
                self.assertEqual(response["Cache-Control"], "no-store")
                self.assertEqual(response["X-Content-Type-Options"], "nosniff")
                self.assertNotIn(b"test-preview/", response.content)
                with Image.open(BytesIO(response.content)) as image:
                    self.assertEqual(image.size, size)
                    self.assertEqual(image.format, "JPEG")

    def test_superuser_can_receive_preview(self):
        admin = get_user_model().objects.create_superuser(username="qa_admin", password="test-pass")
        self.make_record()
        self.client.force_login(admin)
        self.assertEqual(self.client.get(self.url).status_code, 200)

    def test_manual_upload_is_never_selected(self):
        self.allow_view()
        self.make_record(provenance="UPLOAD_MANUAL")
        response = self.client.get(self.url)
        self.assertEqual((response.status_code, response["X-Preview-State"]), (404, "NO_CAPTURE_AVAILABLE"))

    def test_corrupt_current_object_is_error_and_does_not_change_monitoring(self):
        self.allow_view()
        record = self.make_record()
        monitoring = EstadoMonitoramento.objects.create(camera=self.camera)
        before = (monitoring.estado_estavel, monitoring.estado_alterado_em)
        default_storage.delete(record.storage_key)
        default_storage.save(record.storage_key, ContentFile(b"not an image"))
        response = self.client.get(self.url)
        self.assertEqual((response.status_code, response["X-Preview-State"]), (422, "ERROR"))
        monitoring.refresh_from_db()
        self.assertEqual((monitoring.estado_estavel, monitoring.estado_alterado_em), before)

    def test_unavailable_or_error_latest_never_falls_back(self):
        self.allow_view()
        old = timezone.now() - timedelta(hours=1)
        self.make_record(captured_at=old)
        self.make_record(stored=False)
        response = self.client.get(self.url)
        self.assertEqual((response.status_code, response["X-Preview-State"]), (503, "UNAVAILABLE"))
        latest = CameraImageRecord.objects.order_by("-captured_at").first()
        latest.integrity_status = "INVALID"
        latest.save(update_fields=["integrity_status"])
        response = self.client.get(self.url)
        self.assertEqual((response.status_code, response["X-Preview-State"]), (422, "ERROR"))

    def test_inventory_uses_one_image_query_and_never_opens_storage(self):
        self.allow_view()
        self.make_record()
        Camera.objects.create(nome="Sem captura")
        for number in range(2, 12):
            camera = Camera.objects.create(nome=f"Capture candidate {number}")
            self.make_record(camera=camera)
        with patch.object(default_storage, "open", side_effect=AssertionError("storage opened")), \
             patch.object(default_storage, "exists", side_effect=AssertionError("storage checked")), \
             CaptureQueriesContext(connection) as queries:
            response = self.client.get(reverse("cameras:lista"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, reverse("cameras:preview_exibicao", args=[self.camera.pk, "THUMB"]))
        self.assertContains(response, "Ver detalhes")
        image_queries = [query for query in queries if "cameras_cameraimagerecord" in query["sql"].lower()]
        self.assertEqual(len(image_queries), 2)  # capture batch + missing-camera manual batch
        self.assertEqual(self.client.get(reverse("cameras:lista"), {"q": "Sem captura"}).status_code, 200)
        self.assertEqual(self.client.get(reverse("cameras:lista"), {"page": "2"}).status_code, 200)

    def test_inventory_filter_and_second_page_preserve_detail_action(self):
        self.allow_view()
        Camera.objects.bulk_create([Camera(nome=f"Page camera {n:02d}") for n in range(21)])
        filtered = self.client.get(reverse("cameras:lista"), {"q": "Page camera 03"})
        self.assertContains(filtered, "Page camera 03")
        self.assertNotContains(filtered, "Page camera 04")
        second = self.client.get(reverse("cameras:lista"), {"page": "2"})
        self.assertEqual(second.context["page_obj"].number, 2)
        self.assertContains(second, "Ver detalhes")
