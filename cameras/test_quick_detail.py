"""Contrato de leitura do CameraQuickDetailPanel."""

from datetime import timedelta
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.db import connection
from django.test import TestCase
from django.test.utils import CaptureQueriesContext
from django.urls import reverse
from django.utils import timezone

from cameras.models import Camera, CameraImageRecord, EstadoMonitoramento
from cameras.monitoramento.read_service import MonitoringReadService


class QuickDetailTests(TestCase):
    def setUp(self):
        self.camera = Camera.objects.create(
            nome="Entrada", patrimonio="CAM-001", fabricante="Marca", modelo="Modelo",
            terminal="Terminal 1", pavimento="", setor="Portaria", ip="192.168.1.10",
        )
        self.user = get_user_model().objects.create_user(username="quick-viewer", password="test-pass")
        self.url = reverse("cameras:quick_detail", args=[self.camera.pk])

    def allow_view(self):
        self.user.user_permissions.add(Permission.objects.get(codename="view_camera"))
        self.client.force_login(self.user)

    def test_auth_and_missing_camera(self):
        self.assertEqual(self.client.get(self.url).status_code, 401)
        self.client.force_login(self.user)
        self.assertEqual(self.client.get(self.url).status_code, 403)
        self.allow_view()
        self.assertEqual(self.client.get(reverse("cameras:quick_detail", args=[999999])).status_code, 404)
        self.assertEqual(self.client.get(self.url, {"storage_key": "../private"}).status_code, 400)

    def test_fields_location_monitoring_and_no_blob_read(self):
        self.allow_view()
        before_monitoring = EstadoMonitoramento.objects.count()
        with patch("cameras.imagens.read_service.default_storage.open", side_effect=AssertionError("blob opened")):
            with CaptureQueriesContext(connection) as queries:
                response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertLessEqual(len(queries), 7)
        data = response.json()
        self.assertEqual(data["camera"]["nome"], self.camera.nome)
        self.assertEqual(data["location"]["breadcrumb"], f"{self.camera.terminal} > {self.camera.setor}")
        self.assertIsNone(data["location"]["pavimento"])
        self.assertEqual(data["monitoring"]["state"], "OUT_OF_SCOPE")
        self.assertEqual(data["monitoring"]["state"], str(MonitoringReadService().current(self.camera.pk).effective_state))
        self.assertEqual(EstadoMonitoramento.objects.count(), before_monitoring)
        self.assertEqual(data["image"], {"state": "NO_IMAGE_AVAILABLE", "source": "NONE",
                                         "capture_state": "NO_CAPTURE_AVAILABLE", "preview_url": None})
        self.assertEqual(data["links"]["full_detail_url"], reverse("cameras:detalhe", args=[self.camera.pk]))
        self.assertNotIn("storage_key", response.content.decode())
        self.assertEqual(response["Cache-Control"], "no-store")

    def test_display_image_semantic_states(self):
        self.allow_view()
        now = timezone.now()
        CameraImageRecord.objects.create(
            camera=self.camera, provenance="UPLOAD_MANUAL", storage_key="private/manual.png",
            content_type="image/png", sha256="a" * 64, integrity_status="VALID",
        )
        image = self.client.get(self.url).json()["image"]
        self.assertEqual((image["state"], image["source"]), ("UNAVAILABLE", "UPLOAD_MANUAL"))
        older = CameraImageRecord.objects.create(
            camera=self.camera, provenance="CAPTURA_CAMERA", captured_at=now - timedelta(days=1),
            storage_key="private/older.png", content_type="image/png", sha256="a" * 64,
            integrity_status="VALID",
        )
        image = self.client.get(self.url).json()["image"]
        self.assertEqual((image["state"], image["source"]), ("UNAVAILABLE", "CAPTURA_CAMERA"))
        with patch("cameras.imagens.read_service.default_storage.exists", return_value=True):
            image = self.client.get(self.url).json()["image"]
        self.assertEqual(image["state"], "AVAILABLE")
        self.assertEqual(image["preview_url"], reverse("cameras:preview_exibicao", args=[self.camera.pk, "PANEL"]))
        latest = CameraImageRecord.objects.create(
            camera=self.camera, provenance="CAPTURA_CAMERA", captured_at=now,
            storage_key="private/latest.png", content_type="image/png", sha256="a" * 64,
            integrity_status="INVALID",
        )
        image = self.client.get(self.url).json()["image"]
        self.assertEqual((image["state"], image["source"], image["preview_url"]),
                         ("ERROR", "CAPTURA_CAMERA", None))
        self.assertNotIn("private/", str(image))
        self.assertIsNotNone(older.pk)
        self.assertIsNotNone(latest.pk)

    def test_inventory_markup_preserves_detail_and_preview(self):
        self.allow_view()
        response = self.client.get(reverse("cameras:lista"))
        self.assertContains(response, "data-quick-detail-trigger")
        self.assertContains(response, "data-quick-detail-dialog")
        self.assertContains(response, "Ver detalhes")
        self.assertContains(response, "Disponibilidade (30 dias)")
        self.assertNotContains(response, "Ponto de referência")
        self.assertContains(response, 'data-quick-detail-value="location.ambiente"')
        self.assertEqual(response.content.decode().count("camera-quick-detail.js"), 1)
        self.assertNotContains(response, "data-quick-detail-edit-link")
        self.assertEqual(self.client.get(reverse("cameras:editar", args=[self.camera.pk])).status_code, 403)
        self.user.user_permissions.add(Permission.objects.get(codename="change_camera"))
        response = self.client.get(reverse("cameras:lista"))
        self.assertContains(response, 'data-quick-detail-edit-link')
        self.assertContains(response, f'data-quick-detail-edit-url="{reverse("cameras:editar", args=[self.camera.pk])}"')
        self.assertEqual(self.client.get(reverse("cameras:editar", args=[self.camera.pk])).status_code, 200)
