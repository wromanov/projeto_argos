from io import StringIO

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.core.exceptions import ImproperlyConfigured
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from cameras.models import Camera, EventoAuditoria, SubstituicaoCamera
from config.settings import validate_visual_qa_configuration
from core.management.commands.provision_visual_qa import (
    VISUAL_QA_MARKER_DOMAIN,
    VISUAL_QA_PERMISSION_SPECS,
)
from usuarios.models import PerfilUsuario


TEST_QA_USERNAME = "codex_visual_test"
TEST_QA_PASSWORD = "test-only-visual-qa-password"


@override_settings(
    DEBUG=True,
    VISUAL_QA_ENABLED=True,
    VISUAL_QA_USERNAME=TEST_QA_USERNAME,
    VISUAL_QA_PASSWORD=TEST_QA_PASSWORD,
)
class VisualQAMiddlewareTests(TestCase):
    def setUp(self):
        self.command_output = StringIO()
        call_command("provision_visual_qa", stdout=self.command_output)
        self.user = get_user_model().objects.get(username=TEST_QA_USERNAME)
        self.client = Client()
        self.client.force_login(self.user)
        self.host = {"HTTP_HOST": "localhost:8000"}
        self.producao = self.criar_camera(1, Camera.SituacaoOperacional.PRODUCAO)
        self.estoque = self.criar_camera(2, Camera.SituacaoOperacional.ESTOQUE)
        self.desativada = self.criar_camera(3, Camera.SituacaoOperacional.DESATIVADA)

    def criar_camera(self, numero, situacao):
        return Camera.objects.create(
            nome=f"QA-CAMERA-{numero}",
            fabricante="Axis",
            modelo="P3265",
            serial=f"QA-SERIAL-{numero}",
            mac=f"AA:BB:CC:DD:EE:{numero:02X}",
            tipo=Camera.TipoCamera.DOME,
            situacao_operacional=situacao,
            terminal="T1",
            pavimento="1",
            setor="S1",
            ambiente="Sala de QA",
            ip=f"10.20.0.{numero}",
            mascara_subrede="255.255.255.0",
            gateway="10.20.0.254",
            vlan=10,
            farm="FARM-QA",
            retencao_esperada_dias=30,
            codec="H265",
        )

    def get(self, route):
        return self.client.get(route, **self.host)

    def post(self, route, data=None, **extra):
        return self.client.post(route, data or {}, **self.host, **extra)

    def test_safe_gets_cover_visual_qa_pages(self):
        routes = (
            reverse("core:dashboard"),
            reverse("cameras:lista"),
            reverse("cameras:detalhe", args=[self.producao.pk]),
            reverse("cameras:criar"),
            reverse("cameras:editar", args=[self.producao.pk]),
            reverse("cameras:alterar_situacao", args=[self.producao.pk]),
            reverse("cameras:desativar", args=[self.producao.pk]),
            reverse("cameras:reativar", args=[self.desativada.pk]),
            reverse("cameras:substituir", args=[self.producao.pk]),
            reverse("eventos:lista"),
            reverse("cameras:lista_substituicoes"),
            reverse("usuarios:perfil"),
            reverse("usuarios:editar_perfil"),
            reverse("usuarios:alterar_senha"),
        )
        for route in routes:
            with self.subTest(route=route):
                self.assertEqual(self.get(route).status_code, 200)

    def test_profile_get_without_profile_is_200_and_does_not_create_profile(self):
        PerfilUsuario.objects.filter(usuario=self.user).delete()

        response = self.get(reverse("usuarios:perfil"))

        self.assertEqual(response.status_code, 200)
        self.assertFalse(PerfilUsuario.objects.filter(usuario=self.user).exists())

    def test_visual_qa_post_operations_are_blocked_without_view_execution(self):
        camera_before = Camera.objects.values().get(pk=self.producao.pk)
        deactivated_before = Camera.objects.values().get(pk=self.desativada.pk)
        profile_before = PerfilUsuario.objects.values().get(usuario=self.user)
        password_before = self.user.password
        event_count_before = EventoAuditoria.objects.count()
        replacement_count_before = SubstituicaoCamera.objects.count()

        operations = (
            ("camera-edit", reverse("cameras:editar", args=[self.producao.pk]), {"nome": "MUTATED"}),
            ("camera-state", reverse("cameras:alterar_situacao", args=[self.producao.pk]), {"destino": "ESTOQUE", "justificativa": "Tentativa bloqueada."}),
            ("camera-deactivate", reverse("cameras:desativar", args=[self.producao.pk]), {"motivo": "Tentativa bloqueada."}),
            ("camera-reactivate", reverse("cameras:reativar", args=[self.desativada.pk]), {"destino": "PRODUCAO", "justificativa": "Tentativa bloqueada."}),
            ("camera-replace", reverse("cameras:substituir", args=[self.producao.pk]), {"camera_substituta": self.estoque.pk, "motivo": "Tentativa bloqueada."}),
            ("profile-edit", reverse("usuarios:editar_perfil"), {"first_name": "Mutated", "last_name": "User", "email": "mutated@example.com", "telefone": "1", "ramal": "2"}),
            ("password-change", reverse("usuarios:alterar_senha"), {"old_password": TEST_QA_PASSWORD, "new_password1": "other-test-password", "new_password2": "other-test-password"}),
            ("camera-create", reverse("cameras:criar"), {"nome": "MUTATED-CREATE"}),
        )

        for name, route, data in operations:
            with self.subTest(operation=name):
                self.assertEqual(self.post(route, data).status_code, 403)

        self.assertEqual(Camera.objects.values().get(pk=self.producao.pk), camera_before)
        self.assertEqual(Camera.objects.values().get(pk=self.desativada.pk), deactivated_before)
        self.assertEqual(PerfilUsuario.objects.values().get(usuario=self.user), profile_before)
        self.user.refresh_from_db()
        self.assertEqual(self.user.password, password_before)
        self.assertEqual(EventoAuditoria.objects.count(), event_count_before)
        self.assertEqual(SubstituicaoCamera.objects.count(), replacement_count_before)

    def test_logout_post_is_the_only_non_safe_method_exception(self):
        response = self.post(reverse("usuarios:logout"))

        self.assertRedirects(response, reverse("usuarios:login"), fetch_redirect_response=False)
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_logout_delete_is_not_an_exception(self):
        response = self.client.delete(reverse("usuarios:logout"), **self.host)

        self.assertEqual(response.status_code, 403)
        self.assertIn("_auth_user_id", self.client.session)

    def test_login_post_remains_normal_for_anonymous_user(self):
        self.client.logout()

        response = self.client.post(
            reverse("usuarios:login"),
            {"username": TEST_QA_USERNAME, "password": TEST_QA_PASSWORD},
            **self.host,
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn("_auth_user_id", self.client.session)

    def test_loopback_requires_host_and_remote_address(self):
        allowed = (
            ("localhost:8000", "127.0.0.1"),
            ("127.0.0.1:8000", "127.0.0.1"),
            ("[::1]:8000", "::1"),
        )
        for host, remote_addr in allowed:
            with self.subTest(host=host, remote_addr=remote_addr):
                response = self.client.get(
                    reverse("core:dashboard"),
                    HTTP_HOST=host,
                    REMOTE_ADDR=remote_addr,
                )
                self.assertEqual(response.status_code, 200)

    def test_visual_qa_remote_host_is_forbidden_even_from_loopback(self):
        with override_settings(
            ALLOWED_HOSTS=["example.com", "localhost", "127.0.0.1", "::1"]
        ):
            response = self.client.get(
                reverse("core:dashboard"),
                HTTP_HOST="example.com",
                REMOTE_ADDR="127.0.0.1",
            )
        self.assertEqual(response.status_code, 403)

    def test_visual_qa_requires_loopback_remote_address(self):
        for remote_addr in ("192.168.1.10", "10.0.0.8", "172.16.0.2", "203.0.113.10", "", "not-an-ip"):
            with self.subTest(remote_addr=remote_addr):
                response = self.client.get(
                    reverse("core:dashboard"),
                    HTTP_HOST="localhost:8000",
                    REMOTE_ADDR=remote_addr,
                    HTTP_X_FORWARDED_FOR="127.0.0.1",
                    HTTP_X_REAL_IP="127.0.0.1",
                    HTTP_FORWARDED="for=127.0.0.1",
                )
                self.assertEqual(response.status_code, 403)

    def test_visual_qa_bypass_attempt_is_forbidden(self):
        response = self.client.get(
            reverse("core:dashboard"),
            HTTP_HOST="localhost:8000",
            REMOTE_ADDR="203.0.113.10",
        )
        self.assertEqual(response.status_code, 403)

    def test_flag_off_makes_middleware_neutral(self):
        with override_settings(
            VISUAL_QA_ENABLED=False,
            ALLOWED_HOSTS=["example.com", "localhost", "127.0.0.1", "::1"],
        ):
            self.assertEqual(
                self.client.get(
                    reverse("core:dashboard"),
                    HTTP_HOST="example.com",
                    REMOTE_ADDR="203.0.113.10",
                ).status_code,
                200,
            )


class VisualQANormalUserRegressionTests(TestCase):
    def setUp(self):
        call_command("configurar_perfis_argos", stdout=StringIO())
        self.user = get_user_model().objects.create_user(
            username="operador-visual-regression",
            password="test-only-normal-user-password",
        )
        self.user.groups.add(Group.objects.get(name="Operador ARGOS"))
        self.client.force_login(self.user)
        self.camera = Camera.objects.create(
            nome="NORMAL-USER-CAMERA",
            fabricante="Axis",
            modelo="P3265",
            serial="NORMAL-USER-SERIAL",
            mac="AA:BB:CC:DD:EF:01",
            tipo=Camera.TipoCamera.DOME,
            situacao_operacional=Camera.SituacaoOperacional.PRODUCAO,
        )

    def test_normal_user_can_still_execute_authorized_post(self):
        response = self.client.post(
            reverse("cameras:desativar", args=[self.camera.pk]),
            {"motivo": "Motivo operacional válido."},
            HTTP_HOST="localhost:8000",
        )

        self.assertEqual(response.status_code, 302)
        self.camera.refresh_from_db()
        self.assertEqual(self.camera.situacao_operacional, Camera.SituacaoOperacional.DESATIVADA)

    def test_normal_user_is_not_blocked_by_remote_host_rule(self):
        with override_settings(ALLOWED_HOSTS=["example.com", "localhost", "127.0.0.1", "::1"]):
            self.assertNotEqual(
                self.client.get(reverse("cameras:lista"), HTTP_HOST="example.com").status_code,
                403,
            )


class VisualQACommandTests(TestCase):
    def command(self, **settings):
        output = StringIO()
        with override_settings(
            DEBUG=settings.get("DEBUG", True),
            VISUAL_QA_ENABLED=settings.get("VISUAL_QA_ENABLED", True),
            VISUAL_QA_USERNAME=settings.get("VISUAL_QA_USERNAME", TEST_QA_USERNAME),
            VISUAL_QA_PASSWORD=settings.get("VISUAL_QA_PASSWORD", TEST_QA_PASSWORD),
        ):
            call_command("provision_visual_qa", stdout=output)
        return output.getvalue()

    def test_flag_off_is_rejected(self):
        with self.assertRaises(CommandError):
            self.command(VISUAL_QA_ENABLED=False)

    def test_debug_false_is_rejected(self):
        with self.assertRaises(CommandError):
            self.command(DEBUG=False)

    def test_configuration_fails_closed_when_debug_is_false(self):
        with self.assertRaisesMessage(
            ImproperlyConfigured,
            "ARGOS_VISUAL_QA_ENABLED",
        ):
            validate_visual_qa_configuration(False, True)

    def test_username_missing_is_rejected(self):
        with self.assertRaises(CommandError):
            self.command(VISUAL_QA_USERNAME="")

    def test_password_missing_is_rejected(self):
        with self.assertRaises(CommandError):
            self.command(VISUAL_QA_PASSWORD="")

    def test_first_and_second_runs_are_idempotent_and_minimal(self):
        first_output = self.command()
        user = get_user_model().objects.get(username=TEST_QA_USERNAME)
        user.is_staff = True
        user.is_superuser = True
        user.user_permissions.add(Permission.objects.get(codename="delete_camera"))
        user.save(update_fields=["is_staff", "is_superuser"])
        first_password_hash = user.password

        second_output = self.command()
        user.refresh_from_db()

        expected_permissions = {
            "cameras.view_camera",
            "cameras.add_camera",
            "cameras.change_camera",
            "cameras.desativar_camera",
            "cameras.reativar_camera",
            "cameras.alterar_situacao_camera",
            "cameras.registrar_substituicao_camera",
            "cameras.consultar_eventos",
            "cameras.consultar_substituicoescamera",
        }
        self.assertIn(TEST_QA_USERNAME, first_output)
        self.assertIn(TEST_QA_USERNAME, second_output)
        self.assertNotIn(TEST_QA_PASSWORD, first_output + second_output)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertEqual(set(user.get_all_permissions()), expected_permissions)
        self.assertFalse(user.groups.exists())
        self.assertTrue(user.check_password(TEST_QA_PASSWORD))
        self.assertNotEqual(user.password, first_password_hash)
        self.assertTrue(user.email.endswith(f"@{VISUAL_QA_MARKER_DOMAIN}"))

    def test_existing_common_user_collision_is_rejected_without_mutation(self):
        user_model = get_user_model()
        collision = user_model.objects.create_user(
            username=TEST_QA_USERNAME,
            password="test-only-collision-password",
            email="ordinary@example.com",
            is_active=False,
            is_staff=True,
            is_superuser=False,
        )
        group = Group.objects.create(name="Collision group")
        collision.groups.add(group)
        collision.user_permissions.add(Permission.objects.get(codename="delete_camera"))
        before = {
            "password": collision.password,
            "email": collision.email,
            "is_active": collision.is_active,
            "is_staff": collision.is_staff,
            "is_superuser": collision.is_superuser,
            "groups": set(collision.groups.values_list("pk", flat=True)),
            "permissions": set(collision.user_permissions.values_list("pk", flat=True)),
        }

        with self.assertRaises(CommandError):
            self.command()

        collision.refresh_from_db()
        self.assertEqual(collision.password, before["password"])
        self.assertEqual(collision.email, before["email"])
        self.assertEqual(collision.is_active, before["is_active"])
        self.assertEqual(collision.is_staff, before["is_staff"])
        self.assertEqual(collision.is_superuser, before["is_superuser"])
        self.assertEqual(
            set(collision.groups.values_list("pk", flat=True)),
            before["groups"],
        )
        self.assertEqual(
            set(collision.user_permissions.values_list("pk", flat=True)),
            before["permissions"],
        )

    def test_common_user_with_visual_qa_state_but_without_marker_is_rejected_without_mutation(self):
        user_model = get_user_model()
        collision = user_model.objects.create_user(
            username=TEST_QA_USERNAME,
            password="test-only-collision-password",
            email="ordinary@example.com",
            is_active=True,
            is_staff=False,
            is_superuser=False,
        )
        qa_permissions = [
            Permission.objects.get(
                content_type__app_label=app_label,
                content_type__model=model,
                codename=codename,
            )
            for app_label, model, codename in VISUAL_QA_PERMISSION_SPECS
        ]
        collision.user_permissions.set(qa_permissions)
        before = {
            "password": collision.password,
            "email": collision.email,
            "is_active": collision.is_active,
            "is_staff": collision.is_staff,
            "is_superuser": collision.is_superuser,
            "groups": set(collision.groups.values_list("pk", flat=True)),
            "user_permissions": set(
                collision.user_permissions.values_list("pk", flat=True)
            ),
        }

        with self.assertRaises(CommandError):
            self.command()

        collision.refresh_from_db()
        self.assertEqual(collision.password, before["password"])
        self.assertEqual(collision.email, before["email"])
        self.assertEqual(collision.is_active, before["is_active"])
        self.assertEqual(collision.is_staff, before["is_staff"])
        self.assertEqual(collision.is_superuser, before["is_superuser"])
        self.assertEqual(
            set(collision.groups.values_list("pk", flat=True)),
            before["groups"],
        )
        self.assertEqual(
            set(collision.user_permissions.values_list("pk", flat=True)),
            before["user_permissions"],
        )
