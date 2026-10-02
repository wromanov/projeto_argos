from io import StringIO

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser, Group, Permission
from django.core.exceptions import PermissionDenied
from django.core.management import call_command
from django.test import TestCase

from .authorization import require_camera_permission


class CameraAuthorizationTests(TestCase):
    camera_id = 4321
    protected_capabilities = (
        "change_camera_connection",
        "manage_camera_capability",
        "view_camera_credential",
        "change_camera_credential",
        "reveal_camera_credential",
        "run_camera_connection_test",
        "view_camera_diagnostic",
        "capture_camera_image",
    )

    @classmethod
    def setUpTestData(cls):
        call_command("configurar_perfis_argos", stdout=StringIO())
        user_model = get_user_model()
        cls.users = {
            name: user_model.objects.create_user(username=name, password="test-password")
            for name in ("monitor", "operator", "technician", "admin")
        }
        for role, group_name in (
            ("monitor", "Monitoramento ARGOS"),
            ("operator", "Operador ARGOS"),
            ("technician", "Técnico ARGOS"),
            ("admin", "Administrador ARGOS"),
        ):
            cls.users[role].groups.add(Group.objects.get(name=group_name))

    def assert_denied(self, actor, permission_codename):
        with self.assertRaises(PermissionDenied):
            require_camera_permission(
                actor=actor,
                permission_codename=permission_codename,
                camera_id=self.camera_id,
            )

    def test_monitoring_and_operator_cannot_use_technical_capabilities(self):
        for role in ("monitor", "operator"):
            with self.subTest(role=role):
                for codename in self.protected_capabilities:
                    with self.subTest(permission=codename):
                        self.assert_denied(self.users[role], codename)

    def test_operator_can_view_connection_but_not_credential_metadata(self):
        require_camera_permission(
            actor=self.users["operator"],
            permission_codename="view_camera_connection",
            camera_id=self.camera_id,
        )
        self.assert_denied(self.users["operator"], "view_camera_credential")

    def test_technician_and_administrator_can_use_camera_capabilities(self):
        for role in ("technician", "admin"):
            with self.subTest(role=role):
                for codename in self.protected_capabilities:
                    with self.subTest(permission=codename):
                        require_camera_permission(
                            actor=self.users[role],
                            permission_codename=codename,
                            camera_id=self.camera_id,
                        )

    def test_only_administrator_has_global_policy_and_runtime_permissions(self):
        for role in ("monitor", "operator", "technician"):
            for codename in (
                "manage_camera_target_policy",
                "manage_monitoring_runtime",
            ):
                with self.subTest(role=role, permission=codename):
                    self.assert_denied(self.users[role], codename)
        for codename in (
            "manage_camera_target_policy",
            "manage_monitoring_runtime",
        ):
            require_camera_permission(
                actor=self.users["admin"],
                permission_codename=codename,
                camera_id=self.camera_id,
            )

    def test_anonymous_and_authenticated_users_without_roles_are_denied(self):
        unassigned = get_user_model().objects.create_user(
            username="unassigned", password="test-password"
        )
        for actor in (AnonymousUser(), unassigned):
            self.assert_denied(actor, "reveal_camera_credential")

    def test_direct_django_permission_grants_remain_effective(self):
        user = get_user_model().objects.create_user(
            username="direct-permission", password="test-password"
        )
        user.user_permissions.add(
            Permission.objects.get(
                content_type__app_label="cameras",
                codename="run_camera_connection_test",
            )
        )
        require_camera_permission(
            actor=user,
            permission_codename="run_camera_connection_test",
            camera_id=self.camera_id,
        )

    def test_superuser_retains_django_permission_behavior(self):
        superuser = get_user_model().objects.create_superuser(
            username="superuser",
            password="test-password",
        )
        require_camera_permission(
            actor=superuser,
            permission_codename="reveal_camera_credential",
            camera_id=self.camera_id,
        )

    def test_unknown_permission_and_missing_camera_id_fail_closed(self):
        with self.assertRaises(ValueError):
            require_camera_permission(
                actor=self.users["admin"],
                permission_codename="invented_camera_permission",
                camera_id=self.camera_id,
            )
        with self.assertRaises(ValueError):
            require_camera_permission(
                actor=self.users["admin"],
                permission_codename="run_camera_connection_test",
                camera_id=None,
            )
