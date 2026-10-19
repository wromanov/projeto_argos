"""Testes HTTP/SSR da galeria E4 no detalhe da câmera."""

from datetime import datetime, timezone as datetime_timezone
from hashlib import sha256
from io import BytesIO
from pathlib import Path
from tempfile import TemporaryDirectory
from uuid import uuid4

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone
from PIL import Image

from cameras.models import Camera, CameraImageRecord


CAPTURED_AT = datetime(2026, 10, 18, 13, 42, tzinfo=datetime_timezone.utc)
RECORDED_AT = datetime(2026, 10, 18, 12, 56, tzinfo=datetime_timezone.utc)


class CameraGalleryHttpTests(TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory(
            prefix=".tmp-gallery-http-",
            dir=Path(__file__).resolve().parent.parent,
        )
        self.addCleanup(self.temp.cleanup)
        override = override_settings(MEDIA_ROOT=self.temp.name)
        override.enable()
        self.addCleanup(override.disable)
        self.camera = Camera.objects.create(nome="Câmera galeria E4")
        self.other_camera = Camera.objects.create(nome="Outra câmera galeria E4")
        self.user = get_user_model().objects.create_user(username="gallery-viewer", password="test")

    def allow_view(self):
        self.user.user_permissions.add(Permission.objects.get(codename="view_camera"))
        self.client.force_login(self.user)

    def record(self, *, camera=None, provenance=CameraImageRecord.Provenance.CAPTURA_CAMERA,
               recorded_at=RECORDED_AT, captured_at=CAPTURED_AT, withdrawn=False, color="red"):
        camera = camera or self.camera
        buffer = BytesIO()
        Image.new("RGB", (96, 48), color).save(buffer, format="PNG")
        data = buffer.getvalue()
        key = f"gallery-http/{camera.pk}/{uuid4()}.png"
        default_storage.save(key, ContentFile(data))
        if provenance == CameraImageRecord.Provenance.UPLOAD_MANUAL:
            captured_at = None
        return CameraImageRecord.objects.create(
            camera=camera,
            provenance=provenance,
            captured_at=captured_at,
            recorded_at=recorded_at,
            storage_key=key,
            content_type="image/png",
            size_bytes=len(data),
            width=96,
            height=48,
            sha256=sha256(data).hexdigest(),
            integrity_status=CameraImageRecord.IntegrityStatus.VALID,
            withdrawn_at=timezone.now() if withdrawn else None,
            withdrawal_reason="retirada sintética" if withdrawn else "",
        )

    def test_gallery_trigger_renders_for_viewer_without_capture_or_upload_permission(self):
        self.allow_view()
        response = self.client.get(reverse("cameras:detalhe", args=[self.camera.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ver imagens")
        self.assertContains(response, "Imagens da câmera")
        self.assertContains(response, "Nenhuma imagem ativa registrada para esta câmera.")
        self.assertEqual(response["Cache-Control"], "no-store")

    def test_gallery_shows_provenance_specific_datetime_and_registration_order(self):
        self.allow_view()
        upload = self.record(
            provenance=CameraImageRecord.Provenance.UPLOAD_MANUAL,
            recorded_at=RECORDED_AT,
            color="blue",
        )
        capture = self.record(recorded_at=CAPTURED_AT, captured_at=CAPTURED_AT, color="green")
        response = self.client.get(reverse("cameras:detalhe", args=[self.camera.pk]))
        html = response.content.decode()
        self.assertEqual(response.status_code, 200)
        self.assertLess(html.index(str(upload.pk)), html.index(str(capture.pk)))
        self.assertContains(response, "Origem: Upload manual")
        self.assertContains(response, f"Registrada em {timezone.localtime(RECORDED_AT):%d/%m/%Y · %H:%M}")
        self.assertContains(response, "Origem: Captura da câmera")
        self.assertContains(response, f"Capturada em {timezone.localtime(CAPTURED_AT):%d/%m/%Y · %H:%M}")
        self.assertNotIn("storage_key", html)

    def test_over_limit_disables_gallery_only_and_preserves_all_active_records(self):
        self.allow_view()
        for color in ("red", "blue", "green", "yellow"):
            self.record(color=color)

        with self.assertLogs("cameras.imagens.gallery_service", level="WARNING") as logged:
            response = self.client.get(reverse("cameras:detalhe", args=[self.camera.pk]))

        self.assertContains(response, "Não foi possível exibir as imagens desta câmera.")
        self.assertContains(response, "Ficha da câmera")
        self.assertNotContains(response, "Ampliar Imagem")
        self.assertEqual(self.camera.image_records.filter(withdrawn_at__isnull=True).count(), 4)
        self.assertIn("active-record limit exceeded", logged.output[0])

    def test_gallery_http_requires_view_permission_and_binds_identity_to_camera(self):
        record = self.record()
        url = reverse("cameras:preview_galeria", args=[self.camera.pk, record.pk, "FULL"])
        unauthenticated = self.client.get(url)
        self.assertEqual((unauthenticated.status_code, unauthenticated["X-Preview-State"]),
                         (401, "UNAUTHENTICATED"))

        self.client.force_login(self.user)
        forbidden = self.client.get(url)
        self.assertEqual((forbidden.status_code, forbidden["X-Preview-State"]), (403, "FORBIDDEN"))

        self.allow_view()
        wrong_camera = self.client.get(
            reverse("cameras:preview_galeria", args=[self.other_camera.pk, record.pk, "FULL"])
        )
        self.assertEqual((wrong_camera.status_code, wrong_camera["X-Preview-State"], wrong_camera.content),
                         (404, "NOT_FOUND", b""))
        image = self.client.get(url)
        self.assertEqual(image.status_code, 200)
        self.assertEqual(image["Content-Type"], "image/jpeg")
        self.assertEqual(image["Cache-Control"], "no-store")
        self.assertEqual(image["X-Content-Type-Options"], "nosniff")

    def test_gallery_http_rejects_inactive_missing_and_invalid_requests(self):
        self.allow_view()
        withdrawn = self.record(withdrawn=True)
        inactive = self.client.get(
            reverse("cameras:preview_galeria", args=[self.camera.pk, withdrawn.pk, "THUMB"])
        )
        missing = self.client.get(
            reverse("cameras:preview_galeria", args=[self.camera.pk, uuid4(), "THUMB"])
        )
        invalid_query = self.client.get(
            reverse("cameras:preview_galeria", args=[self.camera.pk, withdrawn.pk, "THUMB"]),
            {"source": "anything"},
        )
        self.assertEqual((inactive.status_code, inactive["X-Preview-State"]), (404, "NOT_FOUND"))
        self.assertEqual((missing.status_code, missing["X-Preview-State"]), (404, "NOT_FOUND"))
        self.assertEqual((invalid_query.status_code, invalid_query["X-Preview-State"]), (400, "INVALID_REQUEST"))
