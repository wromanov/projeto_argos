from io import StringIO

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from .admin_security import ARGOS_ADMIN_GROUP_NAME, can_manage_user


class SecR01BAdminTests(TestCase):
    def setUp(self):
        call_command("configurar_perfis_argos", stdout=StringIO())
        user_model = get_user_model()
        self.admin_user = user_model.objects.create_user(
            username="admin-operacional",
            password="Senha-forte-123",
            is_staff=True,
        )
        self.admin_group = Group.objects.get(name=ARGOS_ADMIN_GROUP_NAME)
        self.admin_user.groups.add(self.admin_group)
        self.common_user = user_model.objects.create_user(
            username="usuario-comum",
            password="Senha-forte-123",
        )
        self.client.force_login(self.admin_user)

    def user_change_url(self, user):
        return reverse("admin:auth_user_change", args=(user.pk,))

    def password_change_url(self, user):
        return reverse("admin:auth_user_password_change", args=(user.pk,))

    def test_policy_allows_only_unprivileged_targets(self):
        user_model = get_user_model()
        superuser = user_model.objects.create_superuser(
            username="superuser-alvo",
            password="Senha-forte-123",
        )
        staff_user = user_model.objects.create_user(
            username="staff-alvo",
            password="Senha-forte-123",
            is_staff=True,
        )
        direct_permission_user = user_model.objects.create_user(
            username="permissao-direta",
            password="Senha-forte-123",
        )
        direct_permission_user.user_permissions.add(
            Permission.objects.get(codename="view_user")
        )
        future_group_user = user_model.objects.create_user(
            username="grupo-futuro",
            password="Senha-forte-123",
        )
        future_group_user.groups.add(Group.objects.create(name="Auditor ARGOS"))

        self.assertTrue(can_manage_user(self.admin_user, self.common_user))
        self.assertFalse(can_manage_user(self.admin_user, self.admin_user))
        self.assertFalse(can_manage_user(self.admin_user, superuser))
        self.assertFalse(can_manage_user(self.admin_user, staff_user))
        self.assertFalse(
            can_manage_user(self.admin_user, direct_permission_user)
        )
        self.assertFalse(can_manage_user(self.admin_user, future_group_user))

    def test_change_form_hides_privileged_fields_and_future_groups(self):
        response = self.client.get(self.user_change_url(self.common_user))

        self.assertEqual(response.status_code, 200)
        for field_name in ("is_superuser", "is_staff", "user_permissions"):
            self.assertNotContains(response, field_name)
        self.assertContains(response, "is_active")
        self.assertContains(response, "Monitoramento ARGOS")
        self.assertContains(response, "Operador ARGOS")
        self.assertContains(response, "Técnico ARGOS")
        self.assertNotContains(response, "Administrador ARGOS")

    def test_change_post_cannot_elevate_or_assign_direct_permissions(self):
        monitoramento = Group.objects.get(name="Monitoramento ARGOS")
        operador = Group.objects.get(name="Operador ARGOS")
        tecnico = Group.objects.get(name="Técnico ARGOS")
        view_user = Permission.objects.get(codename="view_user")
        future_group = Group.objects.create(name="Auditor ARGOS")

        rejected_response = self.client.post(
            self.user_change_url(self.common_user),
            {
                "username": self.common_user.username,
                "first_name": "Nome",
                "last_name": "Comum",
                "email": "comum@example.test",
                "is_active": "on",
                "groups": [future_group.pk],
            },
        )

        self.assertEqual(rejected_response.status_code, 200)
        self.common_user.refresh_from_db()
        self.assertFalse(self.common_user.groups.exists())

        response = self.client.post(
            self.user_change_url(self.common_user),
            {
                "username": self.common_user.username,
                "first_name": "Nome",
                "last_name": "Comum",
                "email": "comum@example.test",
                "is_active": "on",
                "groups": [monitoramento.pk, operador.pk, tecnico.pk],
                "is_staff": "on",
                "is_superuser": "on",
                "user_permissions": [view_user.pk],
            },
        )

        self.assertEqual(response.status_code, 302)
        self.common_user.refresh_from_db()
        self.assertFalse(self.common_user.is_staff)
        self.assertFalse(self.common_user.is_superuser)
        self.assertFalse(self.common_user.user_permissions.exists())
        self.assertEqual(
            set(self.common_user.groups.values_list("name", flat=True)),
            {"Monitoramento ARGOS", "Operador ARGOS", "Técnico ARGOS"},
        )

    def test_protected_accounts_are_blocked_on_change_and_password_endpoints(self):
        user_model = get_user_model()
        protected_users = [
            user_model.objects.create_superuser(
                username="superuser-protegido",
                password="Senha-forte-123",
            ),
            user_model.objects.create_user(
                username="staff-protegido",
                password="Senha-forte-123",
                is_staff=True,
            ),
            self.admin_user,
        ]

        for target in protected_users:
            self.assertIn(
                self.client.get(self.user_change_url(target)).status_code,
                (302, 403, 404),
            )
            self.assertIn(
                self.client.get(self.password_change_url(target)).status_code,
                (403, 404),
            )

    def test_password_endpoint_allows_common_user(self):
        response = self.client.post(
            self.password_change_url(self.common_user),
            {
                "usable_password": "true",
                "password1": "Nova-senha-forte-123",
                "password2": "Nova-senha-forte-123",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.common_user.refresh_from_db()
        self.assertTrue(self.common_user.check_password("Nova-senha-forte-123"))

    def test_creation_starts_without_elevated_privileges(self):
        response = self.client.post(
            reverse("admin:auth_user_add"),
            {
                "username": "usuario-criado",
                "password1": "Senha-forte-456",
                "password2": "Senha-forte-456",
                "usable_password": "true",
                "is_staff": "on",
                "is_superuser": "on",
            },
        )

        self.assertEqual(response.status_code, 302)
        created = get_user_model().objects.get(username="usuario-criado")
        self.assertFalse(created.is_staff)
        self.assertFalse(created.is_superuser)
        self.assertFalse(created.groups.exists())

    def test_group_admin_is_superuser_only(self):
        self.assertEqual(
            self.client.get(reverse("admin:auth_group_add")).status_code,
            403,
        )

        superuser = get_user_model().objects.create_superuser(
            username="superuser-admin",
            password="Senha-forte-123",
        )
        superuser.groups.add(self.admin_group)
        self.client.force_login(superuser)
        self.assertEqual(
            self.client.get(reverse("admin:auth_group_add")).status_code,
            200,
        )
        response = self.client.get(self.user_change_url(self.common_user))
        self.assertEqual(response.status_code, 200)
        for field_name in ("is_superuser", "is_staff", "user_permissions"):
            self.assertContains(response, field_name)

    def test_command_reconciles_legacy_group_permissions(self):
        monitoramento = Group.objects.get(name="Monitoramento ARGOS")
        operador = Group.objects.get(name="Operador ARGOS")
        monitoramento_before = set(
            monitoramento.permissions.values_list("codename", flat=True)
        )
        operador_before = set(
            operador.permissions.values_list("codename", flat=True)
        )
        legacy_permissions = Permission.objects.filter(
            content_type__app_label="auth",
            codename__in=("add_group", "change_group"),
        )
        self.admin_group.permissions.add(*legacy_permissions)

        call_command("configurar_perfis_argos", stdout=StringIO())

        admin_permissions = set(
            self.admin_group.permissions.values_list("codename", flat=True)
        )
        self.assertFalse({"add_group", "change_group", "delete_group"} & admin_permissions)
        self.assertTrue({"view_user", "add_user", "change_user"} <= admin_permissions)
        self.assertEqual(
            monitoramento_before,
            set(monitoramento.permissions.values_list("codename", flat=True)),
        )
        self.assertEqual(
            operador_before,
            set(operador.permissions.values_list("codename", flat=True)),
        )
