"""Cobertura mínima da proteção de PerfilUsuario no Django Admin (SEC-R02B)."""

from io import StringIO

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.core.management import call_command
from django.test import RequestFactory, TestCase
from django.urls import reverse

from cameras.models import EventoAuditoria

from .admin_security import ARGOS_ADMIN_GROUP_NAME
from .models import PerfilUsuario


class SecR02BPerfilUsuarioAdminTests(TestCase):
    password = "Senha-forte-123"

    def setUp(self):
        call_command("configurar_perfis_argos", stdout=StringIO())
        self.user_model = get_user_model()
        self.admin_group = Group.objects.get(name=ARGOS_ADMIN_GROUP_NAME)
        self.actor = self.user_model.objects.create_user(
            username="admin-perfil",
            password=self.password,
            is_staff=True,
        )
        self.actor.groups.add(self.admin_group)
        self.common = self.user_model.objects.create_user(
            username="perfil-comum",
            password=self.password,
        )
        self.client.force_login(self.actor)

    def change_url(self, user):
        return reverse("admin:usuarios_perfilusuario_change", args=(user.perfil.pk,))

    def profile_data(self, **extra):
        data = {
            "telefone": "11999990000",
            "ramal": "1234",
            "cargo": "Analista",
            "setor": "Operações",
            "_save": "Salvar",
        }
        data.update(extra)
        return data

    def test_admin_argos_sees_and_edits_allowed_profile_with_audit(self):
        changelist = self.client.get(reverse("admin:usuarios_perfilusuario_changelist"))
        self.assertContains(changelist, self.change_url(self.common))

        response = self.client.post(self.change_url(self.common), self.profile_data())

        self.assertEqual(response.status_code, 302)
        self.common.perfil.refresh_from_db()
        self.assertEqual(
            (
                self.common.perfil.telefone,
                self.common.perfil.ramal,
                self.common.perfil.cargo,
                self.common.perfil.setor,
            ),
            ("11999990000", "1234", "Analista", "Operações"),
        )
        evento = EventoAuditoria.objects.get(codigo="perfil.atualizado")
        self.assertEqual(evento.usuario_id, self.actor.pk)
        self.assertEqual(evento.entidade_tipo, self.common._meta.label)
        self.assertEqual(evento.entidade_id, str(self.common.pk))
        self.assertEqual(
            set(evento.alteracoes),
            {"telefone", "ramal", "cargo", "setor"},
        )

    def test_protected_profiles_are_hidden_and_direct_requests_do_not_mutate(self):
        other_admin = self.user_model.objects.create_user(
            username="outro-admin-perfil",
            password=self.password,
            is_staff=True,
        )
        other_admin.groups.add(self.admin_group)
        superuser = self.user_model.objects.create_superuser(
            username="superuser-perfil",
            password=self.password,
        )
        future_group_user = self.user_model.objects.create_user(
            username="grupo-futuro-perfil",
            password=self.password,
        )
        future_group_user.groups.add(Group.objects.create(name="Auditor Futuro"))
        protected_users = [self.actor, superuser, other_admin, future_group_user]

        changelist = self.client.get(reverse("admin:usuarios_perfilusuario_changelist"))
        for user in protected_users:
            self.assertNotContains(changelist, self.change_url(user))
            before = (user.perfil.telefone, user.perfil.ramal, user.perfil.cargo, user.perfil.setor)
            self.assertEqual(self.client.get(self.change_url(user)).status_code, 302)
            self.assertEqual(
                self.client.post(self.change_url(user), self.profile_data()).status_code,
                302,
            )
            user.perfil.refresh_from_db()
            self.assertEqual(
                (user.perfil.telefone, user.perfil.ramal, user.perfil.cargo, user.perfil.setor),
                before,
            )

    def test_direct_permission_target_is_fail_closed(self):
        target = self.user_model.objects.create_user(
            username="permissao-direta-perfil",
            password=self.password,
        )
        target.user_permissions.add(
            Permission.objects.get(content_type__app_label="auth", codename="view_user")
        )

        model_admin = admin.site._registry[PerfilUsuario]
        request = RequestFactory().get("/admin/")
        request.user = self.actor
        self.assertTrue(model_admin.has_view_permission(request, self.common.perfil))
        self.assertTrue(model_admin.has_change_permission(request, self.common.perfil))
        self.assertFalse(model_admin.has_view_permission(request, target.perfil))
        self.assertFalse(model_admin.has_change_permission(request, target.perfil))

        self.assertEqual(self.client.get(self.change_url(target)).status_code, 302)
        self.assertEqual(
            self.client.post(self.change_url(target), self.profile_data()).status_code,
            302,
        )

    def test_superuser_retains_profile_access_and_editing(self):
        superuser = self.user_model.objects.create_superuser(
            username="super-admin-perfil",
            password=self.password,
        )
        self.client.force_login(superuser)

        self.assertEqual(
            self.client.get(reverse("admin:usuarios_perfilusuario_changelist")).status_code,
            200,
        )
        self.assertEqual(self.client.get(self.change_url(self.common)).status_code, 200)
        response = self.client.post(
            self.change_url(self.common),
            self.profile_data(cargo="Coordenador"),
        )
        self.assertEqual(response.status_code, 302)
        self.common.perfil.refresh_from_db()
        self.assertEqual(self.common.perfil.cargo, "Coordenador")

    def test_add_and_delete_remain_blocked(self):
        self.assertEqual(
            self.client.get(reverse("admin:usuarios_perfilusuario_add")).status_code,
            403,
        )
        self.assertEqual(
            self.client.post(
                reverse("admin:usuarios_perfilusuario_delete", args=(self.common.perfil.pk,))
            ).status_code,
            403,
        )
