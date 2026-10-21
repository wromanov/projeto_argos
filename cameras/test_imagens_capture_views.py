import uuid
import re
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import Client, TestCase
from django.urls import reverse

from cameras.imagens.capture_service import CaptureEligibility
from cameras.models import Camera, CameraCaptureJob


class CaptureHttpViewsTests(TestCase):
    def setUp(self):
        self.camera = Camera.objects.create(nome="Camera capture HTTP", fabricante="Vendor", modelo="Model")
        self.user = get_user_model().objects.create_user(username="capture-view-user", password="test")
        self.user.user_permissions.add(
            Permission.objects.get(codename="view_camera"),
            Permission.objects.get(codename="capture_camera_image"),
        )
        self.client.force_login(self.user)
        self.status_url = reverse("cameras:capture_status", args=[self.camera.pk, uuid.uuid4()])

    def _job(self, **kwargs):
        values = {
            "camera": self.camera,
            "requestor": self.user,
            "idempotency_key": uuid.uuid4().hex,
            "source": CameraCaptureJob.Source.HTTP_SNAPSHOT,
            "profile_key": "HTTP_SNAPSHOT_TEST",
            "profile_version": 1,
            "config_version": 1,
            "status": CameraCaptureJob.Status.QUEUED,
        }
        values.update(kwargs)
        return CameraCaptureJob.objects.create(**values)

    def _assert_capture_form(self, html):
        action = reverse("cameras:solicitar_captura", args=[self.camera.pk])
        match = re.search(
            rf'<form\b[^>]*\baction="{re.escape(action)}"[^>]*>(.*?)</form>',
            html,
            re.DOTALL,
        )
        self.assertIsNotNone(match, "formulário POST de captura não foi renderizado")
        form = match.group(1)
        self.assertIn('name="csrfmiddlewaretoken"', form)
        self.assertRegex(
            form,
            r'<input\b[^>]*\bname="idempotency_key"[^>]*\bvalue="([a-f0-9]{32})"',
        )
        self.assertIn(
            f'<input type="hidden" name="source_preference" value="{CameraCaptureJob.Source.HTTP_SNAPSHOT}">',
            form,
        )
        self.assertIn("Método configurado: Captura via HTTP.", html)
        self.assertRegex(
            form,
            r'<button\b[^>]*\btype="submit"[^>]*>.*?<span>Capturar imagem</span>.*?</button>',
        )
        return re.search(
            r'<input\b[^>]*\bname="idempotency_key"[^>]*\bvalue="([a-f0-9]{32})"',
            form,
        ).group(1)

    def test_capture_post_requires_csrf_and_passes_only_stable_key(self):
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.user)
        url = reverse("cameras:solicitar_captura", args=[self.camera.pk])
        with self.assertLogs("django.security.csrf", level="WARNING"):
            response = client.post(url, {"idempotency_key": "stable-capture-key-0001"})
        self.assertEqual(response.status_code, 403)

    def test_capture_post_uses_service_and_redirects_to_ssr_job_status(self):
        job = self._job()
        url = reverse("cameras:solicitar_captura", args=[self.camera.pk])
        with patch("cameras.views.request_camera_capture", return_value=job) as request_capture:
            response = self.client.post(url, {
                "idempotency_key": "stable-capture-key-0001",
                "source_preference": CameraCaptureJob.Source.HTTP_SNAPSHOT,
            })
        request_capture.assert_called_once_with(
            actor=self.user,
            camera_id=self.camera.pk,
            idempotency_key="stable-capture-key-0001",
            source_preference=CameraCaptureJob.Source.HTTP_SNAPSHOT,
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn(f"capture_job={job.pk}", response["Location"])

    def test_status_returns_only_safe_state_and_allowlisted_error_code(self):
        job = self._job(
            status=CameraCaptureJob.Status.FAILED,
            error_code="INTERNAL_ERROR",
        )
        url = reverse("cameras:capture_status", args=[self.camera.pk, job.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"state": "FAILED", "terminal": True, "error_code": "INTERNAL_ERROR"})
        self.assertEqual(response["Cache-Control"], "no-store")
        self.assertEqual(response["X-Content-Type-Options"], "nosniff")

    def test_status_masks_non_allowlisted_error_code(self):
        job = self._job(status=CameraCaptureJob.Status.FAILED, error_code="INTERNAL_ERROR")
        CameraCaptureJob.objects.filter(pk=job.pk).update(error_code="URI_WITH_SECRET")
        url = reverse("cameras:capture_status", args=[self.camera.pk, job.pk])
        self.assertEqual(self.client.get(url).json()["error_code"], "")

    def test_status_does_not_disclose_another_requestors_job(self):
        other = get_user_model().objects.create_user(username="other-capture-requestor")
        job = self._job(requestor=other)
        url = reverse("cameras:capture_status", args=[self.camera.pk, job.pk])
        self.assertEqual(self.client.get(url).status_code, 404)

    def test_status_requires_capture_permission(self):
        self.user.user_permissions.remove(Permission.objects.get(codename="capture_camera_image"))
        job = self._job()
        url = reverse("cameras:capture_status", args=[self.camera.pk, job.pk])
        self.assertEqual(self.client.get(url).status_code, 403)

    def test_status_rejects_non_get_with_405(self):
        job = self._job()
        url = reverse("cameras:capture_status", args=[self.camera.pk, job.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.json(), {"state": "METHOD_NOT_ALLOWED"})

    def test_detail_shows_capture_only_when_available_and_keeps_upload_first(self):
        self.user.user_permissions.add(Permission.objects.get(codename="add_cameraimagerecord"))
        with patch("cameras.views.capture_eligibility", return_value=CaptureEligibility("AVAILABLE", CameraCaptureJob.Source.HTTP_SNAPSHOT)):
            response = self.client.get(reverse("cameras:detalhe", args=[self.camera.pk]))
        self.assertEqual(response.status_code, 200)
        html = response.content.decode()
        self.assertIn('id="camera-detail-complementary-heading">Operações complementares', html)
        self.assertIn("Captura direta da câmera", html)
        self.assertLess(html.index('id="imagem-camera"'), html.index("Captura direta da câmera"))
        self._assert_capture_form(html)
        self.assertIn(
            f'<form class="argos-camera-detail__upload-form" action="{reverse("cameras:upload_imagem", args=[self.camera.pk])}" method="post" enctype="multipart/form-data">',
            html,
        )
        self.assertIn('<button class="argos-button argos-button--primary" type="submit">Enviar imagem</button>', html)
        self.assertIn("argos-camera-detail__complementary--capture", html)
        self.assertEqual(response["Cache-Control"], "no-store")

    def test_detail_shows_safe_ineligible_state_without_capture_action(self):
        self.user.user_permissions.add(Permission.objects.get(codename="add_cameraimagerecord"))
        with patch(
            "cameras.views.capture_eligibility",
            return_value=CaptureEligibility("CONFIGURATION_INCOMPLETE"),
        ):
            response = self.client.get(reverse("cameras:detalhe", args=[self.camera.pk]))
        self.assertContains(response, reverse("cameras:upload_imagem", args=[self.camera.pk]))
        self.assertContains(response, "Captura direta da câmera")
        self.assertContains(response, "O perfil de captura desta câmera precisa ser revisado.")
        self.assertNotIn(
            f'action="{reverse("cameras:solicitar_captura", args=[self.camera.pk])}"',
            response.content.decode(),
        )
        self.assertIn("argos-camera-detail__complementary--capture", response.content.decode())
        self.assertIn("Cache-Control", response.headers)

    def test_detail_maps_supported_blocked_states_to_safe_copy_only(self):
        cases = (
            ("METHOD_UNSUPPORTED", "Método de captura não suportado"),
            ("CAPABILITY_UNVERIFIED", "Suporte à captura não confirmado"),
            ("RTSP_NOT_HOMOLOGATED", "Captura RTSP temporariamente indisponível"),
        )
        for state, title in cases:
            with self.subTest(state=state), patch(
                "cameras.views.capture_eligibility", return_value=CaptureEligibility(state)
            ):
                response = self.client.get(reverse("cameras:detalhe", args=[self.camera.pk]))
            html = response.content.decode()
            self.assertIn(title, html)
            self.assertNotIn(
                f'action="{reverse("cameras:solicitar_captura", args=[self.camera.pk])}"', html
            )

    def test_detail_keeps_gallery_when_neither_capture_nor_upload_is_authorized(self):
        self.user.user_permissions.remove(
            Permission.objects.get(codename="capture_camera_image"),
            Permission.objects.get(codename="add_cameraimagerecord"),
        )

        response = self.client.get(reverse("cameras:detalhe", args=[self.camera.pk]))

        self.assertContains(response, "Operações complementares")
        self.assertContains(response, "Ver imagens")
        self.assertNotContains(response, "Enviar imagem manualmente")
        self.assertNotContains(response, "Capturar imagem")
        self.assertNotContains(response, "Captura direta da câmera")
        self.assertNotContains(response, 'id="imagem-camera"')

    def test_detail_capture_only_uses_full_width_surface_without_divider(self):
        self.user.user_permissions.remove(Permission.objects.get(codename="add_cameraimagerecord"))
        with patch("cameras.views.capture_eligibility", return_value=CaptureEligibility("AVAILABLE", CameraCaptureJob.Source.HTTP_SNAPSHOT)):
            response = self.client.get(reverse("cameras:detalhe", args=[self.camera.pk]))

        html = response.content.decode()
        self.assertIn("argos-camera-detail__complementary--surface", html)
        self.assertNotIn("argos-camera-detail__complementary--capture", html)
        self.assertIn("Capturar imagem", html)
        self.assertNotIn('id="imagem-camera"', html)

    def test_detail_without_capture_permission_omits_capture_zone_and_keeps_upload(self):
        self.user.user_permissions.remove(Permission.objects.get(codename="capture_camera_image"))
        self.user.user_permissions.add(Permission.objects.get(codename="add_cameraimagerecord"))

        response = self.client.get(reverse("cameras:detalhe", args=[self.camera.pk]))

        self.assertContains(response, reverse("cameras:upload_imagem", args=[self.camera.pk]))
        self.assertNotContains(response, "Captura direta da câmera")
        self.assertNotIn("argos-camera-detail__complementary--capture", response.content.decode())

    def test_detail_owned_queued_or_running_job_blocks_duplicate_capture(self):
        for status in (CameraCaptureJob.Status.QUEUED, CameraCaptureJob.Status.RUNNING):
            with self.subTest(status=status):
                job = self._job(status=status)
                response = self.client.get(reverse("cameras:detalhe", args=[self.camera.pk]))

                html = response.content.decode()
                self.assertIn(f'data-job-id="{job.pk}"', html)
                self.assertIn(f'data-job-state="{status}"', html)
                self.assertNotRegex(
                    html,
                    rf'<form\b[^>]*\baction="{re.escape(reverse("cameras:solicitar_captura", args=[self.camera.pk]))}"',
                )
                self.assertIn('src="/static/js/camera-capture.js"', html)
                job.delete()

    def test_detail_other_requestors_active_job_shows_generic_feedback_only(self):
        other = get_user_model().objects.create_user(username="other-capture-requestor")
        job = self._job(requestor=other, status=CameraCaptureJob.Status.RUNNING)

        response = self.client.get(reverse("cameras:detalhe", args=[self.camera.pk]))

        html = response.content.decode()
        self.assertContains(response, "Há uma captura em andamento para esta câmera.")
        self.assertNotIn(str(job.pk), html)
        self.assertNotIn(other.username, html)
        self.assertNotIn(
            f'action="{reverse("cameras:solicitar_captura", args=[self.camera.pk])}"', html
        )

    def test_detail_failed_owned_job_allows_a_new_explicit_capture_when_still_eligible(self):
        job = self._job(status=CameraCaptureJob.Status.FAILED, error_code="INTERNAL_ERROR")
        with (
            patch("cameras.views.capture_eligibility", return_value=CaptureEligibility("AVAILABLE", CameraCaptureJob.Source.HTTP_SNAPSHOT)),
            patch("cameras.views.request_camera_capture") as request_capture,
        ):
            response = self.client.get(
                f"{reverse('cameras:detalhe', args=[self.camera.pk])}?capture_job={job.pk}"
            )

        html = response.content.decode()
        self.assertContains(response, "Não foi possível concluir a captura. Tente novamente mais tarde.")
        new_key = self._assert_capture_form(html)
        self.assertNotEqual(new_key, job.idempotency_key)
        request_capture.assert_not_called()
        self.assertNotIn("INTERNAL_ERROR", html)

    def test_detail_failed_job_does_not_offer_retry_when_currently_ineligible(self):
        job = self._job(status=CameraCaptureJob.Status.FAILED, error_code="URI_WITH_SECRET")
        with patch(
            "cameras.views.capture_eligibility",
            return_value=CaptureEligibility("CONFIGURATION_INCOMPLETE"),
        ), patch("cameras.views.request_camera_capture") as request_capture:
            response = self.client.get(
                f"{reverse('cameras:detalhe', args=[self.camera.pk])}?capture_job={job.pk}"
            )

        html = response.content.decode()
        self.assertContains(response, "Não foi possível concluir a captura. Tente novamente mais tarde.")
        self.assertNotRegex(
            html,
            rf'<form\b[^>]*\baction="{re.escape(reverse("cameras:solicitar_captura", args=[self.camera.pk]))}"',
        )
        self.assertNotIn("URI_WITH_SECRET", html)
        request_capture.assert_not_called()

    def test_detail_does_not_disclose_another_requestors_failed_job(self):
        other = get_user_model().objects.create_user(username="other-failed-requestor")
        job = self._job(requestor=other, status=CameraCaptureJob.Status.FAILED, error_code="INTERNAL_ERROR")
        with patch("cameras.views.capture_eligibility", return_value=CaptureEligibility("AVAILABLE", CameraCaptureJob.Source.HTTP_SNAPSHOT)):
            response = self.client.get(
                f"{reverse('cameras:detalhe', args=[self.camera.pk])}?capture_job={job.pk}"
            )

        html = response.content.decode()
        self.assertNotIn(str(job.pk), html)
        self.assertNotIn(other.username, html)
        self.assertNotIn("INTERNAL_ERROR", html)
        self._assert_capture_form(html)

    def test_detail_failed_job_without_capture_permission_keeps_upload_only(self):
        self.user.user_permissions.remove(Permission.objects.get(codename="capture_camera_image"))
        self.user.user_permissions.add(Permission.objects.get(codename="add_cameraimagerecord"))
        job = self._job(status=CameraCaptureJob.Status.FAILED, error_code="INTERNAL_ERROR")

        response = self.client.get(
            f"{reverse('cameras:detalhe', args=[self.camera.pk])}?capture_job={job.pk}"
        )

        html = response.content.decode()
        self.assertContains(response, reverse("cameras:upload_imagem", args=[self.camera.pk]))
        self.assertContains(response, "Enviar imagem")
        self.assertNotContains(response, "Captura direta da câmera")
        self.assertNotRegex(
            html,
            rf'<form\b[^>]*\baction="{re.escape(reverse("cameras:solicitar_captura", args=[self.camera.pk]))}"',
        )
