from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied, ValidationError
from django.test import TestCase

from cameras.integracao.capabilities import (
    COMPATIBILITY_UNVERIFIED,
    compatibility_status,
    create_capability_profile,
    set_capability_profile_active,
    require_automatic_compatibility,
    require_manual_discovery,
)
from cameras.models import Camera, CameraCapabilityProfile, EventoAuditoria
from cameras.migrations import __path__ as migrations_path
from importlib import import_module
from django.apps import apps


class CameraCapabilityProfileTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="tech", password="test")
        self.camera = Camera.objects.create(nome="Camera A", fabricante="Livre", modelo="Modelo Livre", ip="192.0.2.10")
        self.profile = CameraCapabilityProfile.objects.get(profile_key="RTSP_DISCOVERY_V1", version=1)

    def test_seed_is_idempotent(self):
        migration = import_module("cameras.migrations.0015_camera_capability_profile_connection_config")
        migration.seed_rtsp_discovery(apps, None)
        migration.seed_rtsp_discovery(apps, None)
        self.assertEqual(CameraCapabilityProfile.objects.filter(profile_key="RTSP_DISCOVERY_V1", version=1).count(), 1)
        self.assertEqual(self.profile.probe_evidence_stage, "B")
        self.assertTrue(self.profile.active)

    def test_seed_does_not_assert_vendor_support(self):
        self.assertEqual(compatibility_status(self.camera, self.profile), COMPATIBILITY_UNVERIFIED)
        with self.assertRaises(ValidationError):
            require_automatic_compatibility(self.camera, self.profile)

    def test_active_profile_version_is_immutable(self):
        self.profile.source_ref = "changed"
        with self.assertRaises(ValidationError):
            self.profile.save()

    def test_profile_creation_requires_manage_permission(self):
        profile = CameraCapabilityProfile(
            profile_key="TEST", version=1, active=False, adapter_key="RTSP",
            allowed_schemes=["rtsp"], allowed_ports=[554], tls_policy="NOT_APPLICABLE",
            auth_method="RTSP_NEGOTIATE", credential_required=False,
            endpoint_policy="TECHNICIAN_OVERRIDE", allowed_override_fields=["path"],
            probe_evidence_stage="B", source_ref="fixture",
        )
        with self.assertRaises(PermissionDenied):
            create_capability_profile(actor=self.user, profile=profile)
        permission = self.user.user_permissions.model.objects.get(codename="manage_camera_capability")
        self.user.user_permissions.add(permission)
        self.user = get_user_model().objects.get(pk=self.user.pk)
        create_capability_profile(actor=self.user, profile=profile)
        self.assertEqual(profile.created_by, self.user)
        self.assertTrue(EventoAuditoria.objects.filter(codigo="camera.capability_profile.created").exists())

    def test_manual_discovery_requires_privilege_and_discovery_profile(self):
        with self.assertRaises(PermissionDenied):
            require_manual_discovery(actor=self.user, camera=self.camera, profile=self.profile)
        permission = self.user.user_permissions.model.objects.get(codename="run_camera_connection_test")
        self.user.user_permissions.add(permission)
        self.user = get_user_model().objects.get(pk=self.user.pk)
        result = require_manual_discovery(actor=self.user, camera=self.camera, profile=self.profile)
        self.assertEqual(result, {"compatibility": "UNVERIFIED", "evidence_stage": "B"})


    def test_profile_deactivation_is_audited_and_blocks_manual_discovery(self):
        permission = self.user.user_permissions.model.objects.get(codename="manage_camera_capability")
        self.user.user_permissions.add(permission)
        self.user = get_user_model().objects.get(pk=self.user.pk)
        profile = set_capability_profile_active(actor=self.user, profile_id=self.profile.pk, active=False)
        self.assertFalse(profile.active)
        self.assertTrue(EventoAuditoria.objects.filter(codigo="camera.capability_profile.deactivated").exists())
        connection_permission = self.user.user_permissions.model.objects.get(codename="run_camera_connection_test")
        self.user.user_permissions.add(connection_permission)
        actor = get_user_model().objects.get(pk=self.user.pk)
        with self.assertRaises(ValidationError):
            require_manual_discovery(actor=actor, camera=self.camera, profile=profile)
