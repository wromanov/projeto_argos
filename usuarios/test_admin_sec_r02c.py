"""Regressão adversarial do PerfilUsuarioAdmin (SEC-R02C)."""

from io import StringIO
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from cameras.models import EventoAuditoria

from .admin_security import ARGOS_ADMIN_GROUP_NAME


class SecR02CPerfilUsuarioAdminAdversarialTests(TestCase):
    password = "Senha-forte-123"
    editable_fields = ("telefone", "ramal", "cargo", "setor")

    def setUp(self):
        call_command("configurar_perfis_argos", stdout=StringIO())
        self.user_model = get_user_model()
        self.admin_group = Group.objects.get(name=ARGOS_ADMIN_GROUP_NAME)
        self.monitoramento = Group.objects.get(name="Monitoramento ARGOS")
        self.operador = Group.objects.get(name="Operador ARGOS")
        self.actor = self.create_user("admin-argos", is_staff=True)
        self.actor.groups.add(self.admin_group)
        self.common = self.create_user("comum")
        self.superuser = self.user_model.objects.create_superuser(
            username="superuser", password=self.password
        )
        self.staff = self.create_user("staff", is_staff=True)
        self.other_admin = self.create_user("outro-admin", is_staff=True)
        self.other_admin.groups.add(self.admin_group)
        self.direct_permission = self.create_user("permissao-direta")
        self.direct_permission.user_permissions.add(
            Permission.objects.get(content_type__app_label="auth", codename="view_user")
        )
        self.future_group = self.create_user("grupo-futuro")
        self.future_group.groups.add(Group.objects.create(name="Auditor Futuro"))
        self.monitor_user = self.create_user("monitoramento")
        self.monitor_user.groups.add(self.monitoramento)
        self.operator_user = self.create_user("operador")
        self.operator_user.groups.add(self.operador)
        self.client.force_login(self.actor)

    def create_user(self, username, **kwargs):
        return self.user_model.objects.create_user(
            username=username, password=self.password, **kwargs
        )

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

    def profile_state(self, user):
        user.perfil.refresh_from_db()
        return tuple(getattr(user.perfil, field) for field in self.editable_fields)

    def test_changelist_uses_current_allowlist_and_hides_each_protected_target(self):
        response = self.client.get(reverse("admin:usuarios_perfilusuario_changelist"))
        self.assertEqual(response.status_code, 200)
        for target in (self.common, self.monitor_user, self.operator_user):
            self.assertContains(response, self.change_url(target))
        for target in (
            self.actor, self.superuser, self.staff, self.other_admin,
            self.direct_permission, self.future_group,
        ):
            self.assertNotContains(response, self.change_url(target))

    def test_protected_direct_gets_redirect_without_exposing_profile_data(self):
        for target in (
            self.actor, self.superuser, self.staff, self.other_admin,
            self.direct_permission, self.future_group,
        ):
            response = self.client.get(self.change_url(target))
            self.assertEqual(response.status_code, 302, target.username)

    def test_protected_direct_posts_do_not_mutate_or_audit(self):
        for target in (
            self.actor, self.superuser, self.staff, self.other_admin,
            self.direct_permission, self.future_group,
        ):
            before = self.profile_state(target)
            events_before = EventoAuditoria.objects.filter(codigo="perfil.atualizado").count()
            response = self.client.post(self.change_url(target), self.profile_data())
            self.assertEqual(response.status_code, 302, target.username)
            self.assertEqual(self.profile_state(target), before, target.username)
            self.assertEqual(
                EventoAuditoria.objects.filter(codigo="perfil.atualizado").count(),
                events_before,
                target.username,
            )

    def test_privilege_transitions_are_rechecked_on_next_request(self):
        scenarios = (
            ("staff", lambda user: setattr(user, "is_staff", True)),
            ("permission", lambda user: user.user_permissions.add(Permission.objects.get(content_type__app_label="auth", codename="view_user"))),
            ("future-group", lambda user: user.groups.add(Group.objects.create(name="Grupo Desconhecido"))),
            ("admin-group", lambda user: user.groups.add(self.admin_group)),
        )
        for name, elevate in scenarios:
            with self.subTest(name=name):
                target = self.create_user(f"transicao-{name}")
                self.assertEqual(self.client.get(self.change_url(target)).status_code, 200)
                elevate(target)
                target.save()
                before = self.profile_state(target)
                self.assertEqual(self.client.get(self.change_url(target)).status_code, 302)
                self.assertEqual(
                    self.client.post(self.change_url(target), self.profile_data()).status_code,
                    302,
                )
                self.assertEqual(self.profile_state(target), before)

    def test_allowlisted_targets_accept_get_post_and_persist_all_editable_fields(self):
        for target in (self.monitor_user, self.operator_user):
            with self.subTest(target=target.username):
                self.assertEqual(self.client.get(self.change_url(target)).status_code, 200)
                response = self.client.post(self.change_url(target), self.profile_data())
                self.assertEqual(response.status_code, 302)
                self.assertEqual(self.profile_state(target), ("11999990000", "1234", "Analista", "Operações"))

    def test_adulterated_post_cannot_change_profile_user_or_timestamps(self):
        profile = self.common.perfil
        original_user_id = profile.usuario_id
        created_at = profile.criado_em
        data = self.profile_data(
            usuario=self.operator_user.pk,
            criado_em="2000-01-01 00:00:00",
            atualizado_em="2000-01-01 00:00:00",
        )
        response = self.client.post(self.change_url(self.common), data)
        self.assertEqual(response.status_code, 302)
        profile.refresh_from_db()
        self.assertEqual(profile.usuario_id, original_user_id)
        self.assertEqual(profile.criado_em, created_at)
        self.assertNotEqual(str(profile.atualizado_em)[:10], "2000-01-01")

    def test_audit_identifies_actor_target_and_exact_changes_with_values(self):
        self.common.perfil.telefone = "1100000000"
        self.common.perfil.save()
        response = self.client.post(self.change_url(self.common), self.profile_data())
        self.assertEqual(response.status_code, 302)
        event = EventoAuditoria.objects.get(codigo="perfil.atualizado")
        self.assertEqual(event.usuario_id, self.actor.pk)
        self.assertEqual(event.entidade_tipo, self.common._meta.label)
        self.assertEqual(event.entidade_id, str(self.common.pk))
        self.assertEqual(set(event.alteracoes), set(self.editable_fields))
        self.assertEqual(event.alteracoes["telefone"], {"anterior": "1100000000", "atual": "11999990000"})
        self.assertEqual(event.alteracoes["ramal"], {"anterior": "", "atual": "1234"})

    def test_audit_has_only_changed_field_and_no_empty_event(self):
        self.common.perfil.telefone = "1111111111"
        self.common.perfil.ramal = "1234"
        self.common.perfil.cargo = "Analista"
        self.common.perfil.setor = "Operações"
        self.common.perfil.save()
        response = self.client.post(self.change_url(self.common), self.profile_data(telefone="2222222222"))
        self.assertEqual(response.status_code, 302)
        event = EventoAuditoria.objects.get(codigo="perfil.atualizado")
        self.assertEqual(event.alteracoes, {"telefone": {"anterior": "1111111111", "atual": "2222222222"}})
        events_before = EventoAuditoria.objects.filter(codigo="perfil.atualizado").count()
        response = self.client.post(self.change_url(self.common), self.profile_data(telefone="2222222222"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(EventoAuditoria.objects.filter(codigo="perfil.atualizado").count(), events_before)

    def test_audit_failure_rolls_back_profile_change(self):
        before = self.profile_state(self.common)
        with patch("usuarios.admin.registrar_evento", side_effect=RuntimeError("falha controlada")):
            with self.assertRaisesRegex(RuntimeError, "falha controlada"):
                self.client.post(self.change_url(self.common), self.profile_data())
        self.assertEqual(self.profile_state(self.common), before)
        self.assertFalse(EventoAuditoria.objects.filter(codigo="perfil.atualizado").exists())

    def test_superuser_keeps_full_view_and_edit_capability_but_add_delete_stay_blocked(self):
        self.client.force_login(self.superuser)
        self.assertEqual(self.client.get(reverse("admin:usuarios_perfilusuario_changelist")).status_code, 200)
        for target in (self.common, self.staff, self.other_admin, self.superuser):
            self.assertEqual(self.client.get(self.change_url(target)).status_code, 200)
        self.assertEqual(self.client.post(self.change_url(self.staff), self.profile_data()).status_code, 302)
        self.assertEqual(self.profile_state(self.staff), ("11999990000", "1234", "Analista", "Operações"))
        self.assertEqual(self.client.get(reverse("admin:usuarios_perfilusuario_add")).status_code, 403)
        self.assertEqual(self.client.post(reverse("admin:usuarios_perfilusuario_delete", args=(self.common.perfil.pk,))).status_code, 403)

    def test_non_argos_staff_and_revoked_actor_fail_closed(self):
        self.client.force_login(self.staff)
        self.assertEqual(self.client.get(reverse("admin:usuarios_perfilusuario_changelist")).status_code, 403)
        self.assertEqual(self.client.get(self.change_url(self.common)).status_code, 403)
        self.client.force_login(self.actor)
        self.actor.groups.remove(self.admin_group)
        self.assertEqual(self.client.get(reverse("admin:usuarios_perfilusuario_changelist")).status_code, 403)
        self.assertEqual(self.client.get(self.change_url(self.common)).status_code, 403)
