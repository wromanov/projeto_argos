from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import Client, TestCase
from django.urls import reverse

from .forms import CAMPOS_CAMERA, CameraCriacaoForm, CameraEdicaoForm
from .models import Camera


class CameraFormUiRecoveryTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="camera-form-ui",
            password="test-password",
        )
        permissions = Permission.objects.filter(
            content_type__app_label="cameras",
            codename__in=("add_camera", "change_camera", "view_camera"),
        )
        cls.user.user_permissions.add(*permissions)
        cls.camera = Camera.objects.create(
            nome="CAM-FORM-001",
            fabricante="AXIS",
            modelo="P3265",
            situacao_operacional=Camera.SituacaoOperacional.PRODUCAO,
        )

    def setUp(self):
        self.client.force_login(self.user)

    def test_create_uses_real_form_fields_and_route_scoped_ds_assets(self):
        response = self.client.get(reverse("cameras:criar"))

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context["form"], CameraCriacaoForm)
        self.assertContains(response, 'name="csrfmiddlewaretoken"')
        self.assertContains(response, 'href="/static/css/ui-v2/tokens.css"')
        self.assertContains(response, 'href="/static/css/ui-v2/components.css"')
        self.assertContains(response, 'href="/static/css/ui-v2/patterns.css"')
        self.assertContains(response, 'href="/static/css/ui-v2/camera-form.css"')
        self.assertContains(response, 'name="situacao_operacional"')
        self.assertContains(response, "Cadastrar câmera")

        for field_name in (*CAMPOS_CAMERA, "farm_personalizado", "codec_personalizado", "retencao_personalizada_dias"):
            with self.subTest(field=field_name):
                self.assertContains(response, f'name="{field_name}"')

        self.assertEqual(response.content.count(b'class="argos-card"'), 5)
        self.assertNotContains(response, "Prévia de sucesso")
        self.assertNotContains(response, 'type="file"')

    def test_edit_shows_current_status_without_a_lifecycle_control(self):
        response = self.client.get(reverse("cameras:editar", args=[self.camera.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context["form"], CameraEdicaoForm)
        self.assertContains(response, 'value="CAM-FORM-001"')
        self.assertContains(response, "situação operacional:")
        self.assertContains(response, "Produção")
        self.assertContains(response, "Salvar alterações")
        self.assertNotContains(response, 'name="situacao_operacional"')
        self.assertNotContains(response, 'type="file"')

    def test_invalid_post_preserves_submitted_value_and_accessible_errors(self):
        response = self.client.post(
            reverse("cameras:criar"),
            {
                "nome": "CAM-PENDENTE",
                "farm": "__PERSONALIZADO__",
                "farm_personalizado": "FARM-PENDENTE",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'value="CAM-PENDENTE"')
        self.assertContains(response, "camera-form-errors-title")
        self.assertContains(response, 'role="alert"')
        self.assertContains(response, 'aria-invalid="true"')
        self.assertContains(response, 'aria-errormessage="id_fabricante_errors"')
        self.assertContains(response, 'href="#id_fabricante"')
        self.assertContains(response, 'data-farm-personalizado')

    def test_csrf_protection_remains_active_on_create(self):
        csrf_client = Client(enforce_csrf_checks=True)
        csrf_client.force_login(self.user)

        response = csrf_client.post(reverse("cameras:criar"), {})

        self.assertEqual(response.status_code, 403)

    def test_create_and_edit_permissions_remain_required(self):
        unauthorized = get_user_model().objects.create_user(
            username="camera-form-without-permission",
            password="test-password",
        )
        client = Client()
        client.force_login(unauthorized)

        self.assertEqual(client.get(reverse("cameras:criar")).status_code, 403)
        self.assertEqual(
            client.get(reverse("cameras:editar", args=[self.camera.pk])).status_code,
            403,
        )
