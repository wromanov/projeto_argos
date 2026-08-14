"""Regressao adversarial do SEC-007 no Django Admin."""

from io import StringIO

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from .admin_security import ARGOS_ADMIN_GROUP_NAME


class SecR01CAdversarialTests(TestCase):
    password = "Senha-forte-123"

    def setUp(self):
        call_command("configurar_perfis_argos", stdout=StringIO())
        self.user_model = get_user_model()
        self.argos_group = Group.objects.get(name=ARGOS_ADMIN_GROUP_NAME)
        self.monitoramento = Group.objects.get(name="Monitoramento ARGOS")
        self.operador = Group.objects.get(name="Operador ARGOS")
        self.actor = self.user_model.objects.create_user(
            username="admin-argos-a", password=self.password, is_staff=True
        )
        self.actor.groups.add(self.argos_group)
        self.common = self.user_model.objects.create_user(
            username="usuario-comum", password=self.password
        )
        self.permission = Permission.objects.get(
            content_type__app_label="auth", codename="change_user"
        )
        self.client.force_login(self.actor)

    def change_url(self, user):
        return reverse("admin:auth_user_change", args=(user.pk,))

    def password_url(self, user):
        return reverse("admin:auth_user_password_change", args=(user.pk,))

    def valid_change_data(self, user, **extra):
        data = {
            "username": user.username,
            "first_name": "Nome",
            "last_name": "Original",
            "email": "original@example.test",
            "is_active": "on",
            "groups": [],
        }
        data.update(extra)
        return data

    def test_self_promotion_post_does_not_persist_privileges(self):
        future_group = Group.objects.create(name="Auditor ARGOS")
        self.client.post(
            self.change_url(self.actor),
            self.valid_change_data(
                self.actor,
                is_staff="on",
                is_superuser="on",
                user_permissions=[self.permission.pk],
                groups=[self.argos_group.pk, future_group.pk],
            ),
        )
        self.actor.refresh_from_db()
        self.assertFalse(self.actor.is_superuser)
        self.assertTrue(self.actor.is_staff)
        self.assertFalse(self.actor.user_permissions.exists())
        self.assertEqual(list(self.actor.groups.values_list("pk", flat=True)), [self.argos_group.pk])

    def test_tampered_common_user_post_cannot_escalate(self):
        response = self.client.post(
            self.change_url(self.common),
            self.valid_change_data(
                self.common,
                is_staff="on",
                is_superuser="on",
                user_permissions=[self.permission.pk],
                groups=[self.monitoramento.pk],
            ),
        )
        self.assertEqual(response.status_code, 302)
        self.common.refresh_from_db()
        self.assertFalse(self.common.is_staff)
        self.assertFalse(self.common.is_superuser)
        self.assertFalse(self.common.user_permissions.exists())
        self.assertEqual(list(self.common.groups.values_list("name", flat=True)), ["Monitoramento ARGOS"])

    def test_privileged_and_future_groups_cannot_be_assigned(self):
        future_group = Group.objects.create(name="Auditor ARGOS")
        for group in (self.argos_group, future_group):
            response = self.client.post(
                self.change_url(self.common),
                self.valid_change_data(self.common, groups=[group.pk]),
            )
            self.assertEqual(response.status_code, 200)
            self.common.refresh_from_db()
            self.assertFalse(self.common.groups.exists())

    def test_protected_targets_are_hidden_and_direct_urls_do_not_mutate(self):
        direct = self.user_model.objects.create_user(username="direta", password=self.password)
        direct.user_permissions.add(self.permission)
        unknown = self.user_model.objects.create_user(username="desconhecido", password=self.password)
        unknown.groups.add(Group.objects.create(name="Grupo Futuro"))
        protected = [
            self.user_model.objects.create_superuser(username="root", password=self.password),
            self.user_model.objects.create_user(username="staff", password=self.password, is_staff=True),
            self.user_model.objects.create_user(username="admin-argos-b", password=self.password),
            direct,
            unknown,
        ]
        protected[2].groups.add(self.argos_group)
        listing = self.client.get(reverse("admin:auth_user_changelist"))
        for target in protected + [self.actor]:
            self.assertNotContains(listing, self.change_url(target))
            before = (target.username, target.password, target.is_staff, target.is_superuser)
            get_response = self.client.get(self.change_url(target))
            post_response = self.client.post(
                self.change_url(target),
                self.valid_change_data(target, username="mutado-" + str(target.pk)),
            )
            password_response = self.client.post(
                self.password_url(target),
                {"usable_password": "true", "password1": "Outra-senha-123", "password2": "Outra-senha-123"},
            )
            self.assertEqual(get_response.status_code, 302)
            self.assertEqual(post_response.status_code, 302)
            self.assertEqual(password_response.status_code, 403)
            target.refresh_from_db()
            self.assertEqual((target.username, target.password, target.is_staff, target.is_superuser), before)

    def test_group_admin_endpoints_are_closed_without_mutation(self):
        urls = [
            ("get", reverse("admin:auth_group_changelist")),
            ("get", reverse("admin:auth_group_add")),
            ("post", reverse("admin:auth_group_add")),
            ("get", reverse("admin:auth_group_change", args=(self.monitoramento.pk,))),
            ("post", reverse("admin:auth_group_change", args=(self.monitoramento.pk,))),
            ("post", reverse("admin:auth_group_delete", args=(self.monitoramento.pk,))),
        ]
        original = set(self.monitoramento.permissions.values_list("pk", flat=True))
        for method, url in urls:
            response = getattr(self.client, method)(url, {"name": "Grupo Malicioso", "permissions": [self.permission.pk]})
            self.assertEqual(response.status_code, 403)
        self.assertFalse(Group.objects.filter(name="Grupo Malicioso").exists())
        self.monitoramento.refresh_from_db()
        self.assertEqual(set(self.monitoramento.permissions.values_list("pk", flat=True)), original)

    def test_tampered_creation_is_unprivileged_and_legitimate_creation_works(self):
        future_group = Group.objects.create(name="Auditor ARGOS")
        response = self.client.post(
            reverse("admin:auth_user_add"),
            {"username": "criado", "password1": self.password, "password2": self.password,
             "usable_password": "true", "is_staff": "on", "is_superuser": "on",
             "user_permissions": [self.permission.pk], "groups": [self.argos_group.pk, future_group.pk]},
        )
        self.assertEqual(response.status_code, 302)
        created = self.user_model.objects.get(username="criado")
        self.assertFalse(created.is_staff)
        self.assertFalse(created.is_superuser)
        self.assertFalse(created.user_permissions.exists())
        self.assertFalse(created.groups.exists())

    def test_legitimate_edit_assignment_and_password_reset_work(self):
        response = self.client.post(
            self.change_url(self.common),
            self.valid_change_data(
                self.common, username="renomeado", first_name="Novo", last_name="Nome",
                email="novo@example.test", groups=[self.monitoramento.pk, self.operador.pk],
            ),
        )
        self.assertEqual(response.status_code, 302)
        self.common.refresh_from_db()
        self.assertEqual((self.common.username, self.common.first_name, self.common.last_name, self.common.email), ("renomeado", "Novo", "Nome", "novo@example.test"))
        self.assertEqual(set(self.common.groups.values_list("name", flat=True)), {"Monitoramento ARGOS", "Operador ARGOS"})
        response = self.client.post(self.password_url(self.common), {"usable_password": "true", "password1": "Nova-senha-123", "password2": "Nova-senha-123"})
        self.assertEqual(response.status_code, 302)
        self.common.refresh_from_db()
        self.assertTrue(self.common.check_password("Nova-senha-123"))

    def test_superuser_retains_user_and_group_administration(self):
        superuser = self.user_model.objects.create_superuser(username="super-admin", password=self.password)
        self.client.force_login(superuser)
        self.assertEqual(self.client.get(self.change_url(self.common)).status_code, 200)
        self.assertEqual(self.client.get(self.change_url(self.actor)).status_code, 200)
        self.assertEqual(self.client.get(reverse("admin:auth_group_add")).status_code, 200)
        response = self.client.post(reverse("admin:auth_group_add"), {"name": "Grupo Super", "permissions": [self.permission.pk]})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Group.objects.filter(name="Grupo Super", permissions=self.permission).exists())

    def test_non_argos_staff_receives_no_capabilities(self):
        staff = self.user_model.objects.create_user(username="staff-comum", password=self.password, is_staff=True)
        self.client.force_login(staff)
        self.assertEqual(self.client.get(reverse("admin:auth_user_changelist")).status_code, 403)
        self.assertEqual(self.client.get(self.change_url(self.common)).status_code, 403)
        self.assertEqual(self.client.get(reverse("admin:auth_user_add")).status_code, 403)
        self.assertEqual(self.client.get(reverse("admin:auth_group_add")).status_code, 403)

    def test_command_removes_all_legacy_group_permissions_and_is_idempotent(self):
        legacy = Permission.objects.filter(content_type__app_label="auth", codename__in=("add_group", "change_group", "delete_group", "view_group", "view_permission"))
        self.argos_group.permissions.add(*legacy)
        call_command("configurar_perfis_argos", stdout=StringIO())
        first = set(self.argos_group.permissions.values_list("content_type__app_label", "codename"))
        call_command("configurar_perfis_argos", stdout=StringIO())
        second = set(self.argos_group.permissions.values_list("content_type__app_label", "codename"))
        self.assertEqual(first, second)
        self.assertFalse({"add_group", "change_group", "delete_group", "view_group", "view_permission"} & set(self.argos_group.permissions.values_list("codename", flat=True)))
        self.assertTrue({"view_user", "add_user", "change_user"} <= set(self.argos_group.permissions.values_list("codename", flat=True)))

    def test_operational_group_permission_contracts_are_preserved(self):
        expected_monitoramento = {"consultar_eventos", "consultar_substituicoescamera", "view_atividadecamera", "view_camera", "view_eventoauditoria", "view_substituicaocamera"}
        expected_operador = expected_monitoramento | {"add_atividadecamera", "add_camera", "alterar_situacao_camera", "change_atividadecamera", "change_camera", "desativar_camera", "reativar_camera", "registrar_substituicao_camera"}
        self.assertEqual(set(self.monitoramento.permissions.values_list("codename", flat=True)), expected_monitoramento)
        self.assertEqual(set(self.operador.permissions.values_list("codename", flat=True)), expected_operador)
