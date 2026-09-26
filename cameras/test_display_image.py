"""Política DISPLAY_IMAGE e sua entrega privada."""

from datetime import timedelta
from hashlib import sha256
from io import BytesIO
from tempfile import TemporaryDirectory

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

from cameras.imagens.display_service import DisplayImageReadService
from cameras.models import Camera, CameraImageRecord, EstadoMonitoramento


class DisplayImageTests(TestCase):
    def setUp(self):
        temp = TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        override = override_settings(MEDIA_ROOT=temp.name)
        override.enable()
        self.addCleanup(override.disable)
        self.camera = Camera.objects.create(nome="Imagem exibida")
        self.user = get_user_model().objects.create_user(username="display-viewer", password="pass")
        self.url = reverse("cameras:preview_exibicao", args=[self.camera.pk, "THUMB"])

    def record(self, *, provenance="UPLOAD_MANUAL", stored=True, integrity="VALID", camera=None):
        camera = camera or self.camera
        output = BytesIO()
        Image.new("RGB", (120, 80), "blue").save(output, format="PNG")
        data = output.getvalue()
        key = f"private/display-{timezone.now().timestamp()}-{CameraImageRecord.objects.count()}.png"
        if stored:
            default_storage.save(key, ContentFile(data))
        return CameraImageRecord.objects.create(
            camera=camera, provenance=provenance,
            captured_at=timezone.now() if provenance == "CAPTURA_CAMERA" else None,
            storage_key=key, content_type="image/png", size_bytes=len(data),
            sha256=sha256(data).hexdigest(), integrity_status=integrity,
        )

    def authorize(self):
        self.user.user_permissions.add(Permission.objects.get(codename="view_camera"))
        self.client.force_login(self.user)

    def test_priority_and_no_capture_fallback(self):
        manual = self.record()
        service = DisplayImageReadService()
        display = service.display_image(self.camera)
        self.assertEqual((display.source, display.state, display.immutable_id),
                         ("UPLOAD_MANUAL", "AVAILABLE", manual.pk))
        capture = self.record(provenance="CAPTURA_CAMERA")
        display = service.display_image(self.camera)
        self.assertEqual((display.source, display.immutable_id), ("CAPTURA_CAMERA", capture.pk))

    def test_failure_of_capture_never_uses_manual(self):
        self.record()
        capture = self.record(provenance="CAPTURA_CAMERA", stored=False)
        self.assertEqual(DisplayImageReadService().display_image(self.camera).state, "UNAVAILABLE")
        self.assertEqual(DisplayImageReadService().display_image(self.camera).source, "CAPTURA_CAMERA")
        capture.integrity_status = "INVALID"
        capture.save(update_fields=["integrity_status"])
        self.assertEqual(DisplayImageReadService().display_image(self.camera).state, "ERROR")

    def test_latest_manual_failure_never_uses_older(self):
        older = self.record()
        current = self.record(stored=False)
        moment = timezone.now()
        CameraImageRecord.objects.filter(pk=older.pk).update(recorded_at=moment - timedelta(days=1))
        CameraImageRecord.objects.filter(pk=current.pk).update(recorded_at=moment)
        display = DisplayImageReadService().display_image(self.camera)
        self.assertEqual((display.immutable_id, display.state), (current.pk, "UNAVAILABLE"))
        CameraImageRecord.objects.filter(pk=current.pk).update(integrity_status="INVALID")
        self.assertEqual(DisplayImageReadService().display_image(self.camera).state, "ERROR")

    def test_manual_order_uses_recorded_at_then_id(self):
        first = self.record()
        second = self.record()
        moment = timezone.now()
        CameraImageRecord.objects.filter(pk__in=[first.pk, second.pk]).update(recorded_at=moment)
        self.assertEqual(DisplayImageReadService().display_image(self.camera).immutable_id, max(first.pk, second.pk))

    def test_secure_preview_reselects_and_preserves_capture_route(self):
        self.assertEqual(self.client.get(self.url).status_code, 401)
        self.client.force_login(self.user)
        self.assertEqual(self.client.get(self.url).status_code, 403)
        self.authorize()
        self.assertEqual(self.client.get(self.url)["X-Preview-State"], "NO_CAPTURE_AVAILABLE")
        manual = self.record()
        before = EstadoMonitoramento.objects.count()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "image/jpeg")
        self.assertEqual(response["Cache-Control"], "no-store")
        self.assertEqual(response["X-Content-Type-Options"], "nosniff")
        self.assertNotIn(manual.storage_key.encode(), response.content)
        with Image.open(BytesIO(response.content)) as image:
            self.assertEqual((image.format, image.size), ("JPEG", (60, 42)))
        capture_url = reverse("cameras:preview_ultima_captura", args=[self.camera.pk, "THUMB"])
        self.assertEqual(self.client.get(capture_url)["X-Preview-State"], "NO_CAPTURE_AVAILABLE")
        self.assertEqual(EstadoMonitoramento.objects.count(), before)
        self.assertEqual(CameraImageRecord.objects.count(), 1)
        capture = self.record(provenance="CAPTURA_CAMERA", stored=False)
        self.assertEqual(self.client.get(self.url)["X-Preview-State"], "UNAVAILABLE")
        self.assertIsNotNone(capture.pk)

    def test_inventory_batch_and_quick_detail_share_selection(self):
        self.authorize()
        self.record()
        Camera.objects.bulk_create([Camera(nome=f"Empty {n}") for n in range(19)])
        with CaptureQueriesContext(connection) as queries:
            response = self.client.get(reverse("cameras:lista"))
        image_queries = [q for q in queries if "cameras_cameraimagerecord" in q["sql"].lower()]
        self.assertEqual(len(image_queries), 2)
        self.assertContains(response, self.url)
        detail = self.client.get(reverse("cameras:quick_detail", args=[self.camera.pk])).json()["image"]
        self.assertEqual((detail["source"], detail["state"]), ("UPLOAD_MANUAL", "AVAILABLE"))
        self.assertEqual(detail["preview_url"], reverse("cameras:preview_exibicao", args=[self.camera.pk, "PANEL"]))
