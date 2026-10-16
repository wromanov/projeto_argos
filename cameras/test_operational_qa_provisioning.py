from hashlib import sha256
from io import BytesIO
from tempfile import TemporaryDirectory

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.exceptions import ImproperlyConfigured
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from PIL import Image

from cameras.models import (
    AtividadeCamera,
    Camera,
    CameraHealthSnapshot,
    CameraImageRecord,
    EstadoMonitoramento,
    Indisponibilidade,
)
from scripts.localqa.provisioning import (
    OPERATIONAL_QA_PERMISSIONS,
    VISUAL_QA_PERMISSIONS,
    identity_marker,
    provision_operational_qa_user,
    validate_visual_qa_user,
)


def synthetic_image():
    stream = BytesIO()
    Image.new("RGB", (3, 2), "red").save(stream, format="PNG")
    return SimpleUploadedFile("qa-synthetic.png", stream.getvalue(), content_type="image/png")


@override_settings(VISUAL_QA_USERNAME="qa-visual-hom01")
class OperationalQAProvisioningTests(TestCase):
    def setUp(self):
        self.user_model = get_user_model()
        self.visual = self.user_model.objects.create_user(
            username="qa-visual-hom01",
            email=identity_marker("qa-visual-hom01", "visual"),
            password="visual-original-password",
            is_active=True,
        )
        self.visual.user_permissions.set(
            Permission.objects.filter(content_type__app_label="cameras", codename__in=VISUAL_QA_PERMISSIONS)
        )

    def test_create_reexecution_exact_permissions_and_visual_account_preserved(self):
        original_visual_hash = self.visual.password
        visual_permissions = frozenset(self.visual.user_permissions.values_list("codename", flat=True))

        user, created = provision_operational_qa_user("temporary-operational-password-1")
        self.assertTrue(created)
        self.assertEqual(user.username, "qa-operacional-hom01")
        self.assertEqual(frozenset(user.user_permissions.values_list("codename", flat=True)), OPERATIONAL_QA_PERMISSIONS)
        self.assertEqual(len(OPERATIONAL_QA_PERMISSIONS), 7)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.groups.exists())

        user, created_again = provision_operational_qa_user("temporary-operational-password-2")
        self.assertFalse(created_again)
        self.assertEqual(self.user_model.objects.filter(username="qa-operacional-hom01").count(), 1)
        self.assertFalse(user.check_password("temporary-operational-password-1"))
        self.assertTrue(user.check_password("temporary-operational-password-2"))
        self.assertEqual(frozenset(user.user_permissions.values_list("codename", flat=True)), OPERATIONAL_QA_PERMISSIONS)

        validate_visual_qa_user()
        self.visual.refresh_from_db()
        self.assertEqual(self.visual.password, original_visual_hash)
        self.assertEqual(frozenset(self.visual.user_permissions.values_list("codename", flat=True)), visual_permissions)

    def test_unknown_preexisting_username_is_not_modified(self):
        existing = self.user_model.objects.create_user(
            username="qa-operacional-hom01", password="unrelated-user-password"
        )
        original_hash = existing.password

        with self.assertRaises(ImproperlyConfigured):
            provision_operational_qa_user("temporary-operational-password")

        existing.refresh_from_db()
        self.assertEqual(existing.password, original_hash)
        self.assertEqual(existing.email, "")
        self.assertEqual(existing.user_permissions.count(), 0)

    def test_visual_validation_rejects_unknown_user_without_writing(self):
        self.visual.email = "unrecognized@example.invalid"
        self.visual.save(update_fields=("email",))
        original_hash = self.visual.password

        with self.assertRaisesMessage(ImproperlyConfigured, "não tem o marcador reconhecido"):
            validate_visual_qa_user()

        self.visual.refresh_from_db()
        self.assertEqual(self.visual.password, original_hash)
        self.assertEqual(self.visual.email, "unrecognized@example.invalid")


class OperationalQACameraAuthorizationTests(TestCase):
    def setUp(self):
        self.media = TemporaryDirectory()
        self.addCleanup(self.media.cleanup)
        self.settings_override = override_settings(MEDIA_ROOT=self.media.name)
        self.settings_override.enable()
        self.addCleanup(self.settings_override.disable)

        self.production = self._camera("QA produção", Camera.SituacaoOperacional.PRODUCAO)
        self.deactivated = self._camera("QA desativada", Camera.SituacaoOperacional.DESATIVADA)
        user_model = get_user_model()
        self.visual = user_model.objects.create_user(
            username="qa-visual-hom01",
            email=identity_marker("qa-visual-hom01", "visual"),
            password="visual-original-password",
        )
        self.visual.user_permissions.set(
            Permission.objects.filter(content_type__app_label="cameras", codename__in=VISUAL_QA_PERMISSIONS)
        )
        self.operational, _ = provision_operational_qa_user("temporary-operational-password")

    @staticmethod
    def _camera(name, situation):
        return Camera.objects.create(
            nome=name,
            fabricante="FICTÍCIO QA",
            modelo="QA-TESTE",
            situacao_operacional=situation,
        )

    def test_visual_detail_hides_operational_controls_for_both_camera_situations(self):
        self.client.force_login(self.visual)
        for camera in (self.production, self.deactivated):
            with self.subTest(camera=camera.situacao_operacional):
                response = self.client.get(reverse("cameras:detalhe", args=[camera.pk]))
                self.assertEqual(response.status_code, 200)
                self.assertNotContains(response, reverse("cameras:upload_imagem", args=[camera.pk]))
                self.assertNotContains(response, reverse("cameras:criar_atividade", args=[camera.pk]))

    def test_visual_endpoints_enforce_permissions_for_both_camera_situations(self):
        self.client.force_login(self.visual)
        with override_settings(VISUAL_QA_ENABLED=False):
            for camera in (self.production, self.deactivated):
                with self.subTest(camera=camera.situacao_operacional):
                    upload = self.client.post(
                        reverse("cameras:upload_imagem", args=[camera.pk]),
                        {"imagem": synthetic_image()},
                    )
                    activity = self.client.post(
                        reverse("cameras:criar_atividade", args=[camera.pk]),
                        {"tipo": "AVARIA", "titulo": "QA", "descricao": "Fictício", "ocorrida_em": "2026-10-11T10:00"},
                    )
                    self.assertEqual(upload.status_code, 403)
                    self.assertEqual(activity.status_code, 403)
        self.assertEqual(CameraImageRecord.objects.count(), 0)
        self.assertEqual(AtividadeCamera.objects.count(), 0)

    def test_operational_detail_and_post_endpoints_work_for_production_and_deactivated(self):
        self.client.force_login(self.operational)
        monitoring_before = (
            EstadoMonitoramento.objects.count(),
            Indisponibilidade.objects.count(),
            CameraHealthSnapshot.objects.count(),
        )
        for camera in (self.production, self.deactivated):
            with self.subTest(camera=camera.situacao_operacional):
                detail = self.client.get(reverse("cameras:detalhe", args=[camera.pk]))
                self.assertEqual(detail.status_code, 200)
                self.assertContains(detail, reverse("cameras:upload_imagem", args=[camera.pk]))
                self.assertContains(detail, reverse("cameras:criar_atividade", args=[camera.pk]))
                self.assertContains(detail, 'type="file"')
                self.assertContains(detail, "Enviar imagem")

                upload = self.client.post(
                    reverse("cameras:upload_imagem", args=[camera.pk]),
                    {"imagem": synthetic_image()},
                )
                self.assertEqual(upload.status_code, 302)
                self.assertTrue(CameraImageRecord.objects.filter(camera=camera, uploaded_by=self.operational).exists())

                activity = self.client.post(
                    reverse("cameras:criar_atividade", args=[camera.pk]),
                    {"tipo": "AVARIA", "titulo": "Inspeção sintética", "descricao": "Registro de QA fictício", "ocorrida_em": "2026-10-11T10:00", "responsavel": "QA"},
                )
                self.assertEqual(activity.status_code, 302)
                self.assertTrue(AtividadeCamera.objects.filter(camera=camera, titulo="Inspeção sintética").exists())
                camera.refresh_from_db()
                expected_situation = (
                    Camera.SituacaoOperacional.PRODUCAO
                    if camera == self.production
                    else Camera.SituacaoOperacional.DESATIVADA
                )
                self.assertEqual(camera.situacao_operacional, expected_situation)
        self.assertEqual(
            monitoring_before,
            (
                EstadoMonitoramento.objects.count(),
                Indisponibilidade.objects.count(),
                CameraHealthSnapshot.objects.count(),
            ),
        )
