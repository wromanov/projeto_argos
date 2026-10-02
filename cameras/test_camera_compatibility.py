from datetime import date

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.exceptions import PermissionDenied
from django.test import TestCase

from cameras.integracao.compatibility import (
    SUPPORTED,
    UNVERIFIED,
    UNSUPPORTED,
    create_compatibility_evidence,
    resolve_compatibility,
    set_camera_firmware,
)
from cameras.models import Camera, CameraCapabilityEvidence, CameraCapabilityProfile


class CameraCompatibilityTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.admin = User.objects.create_user(username="cap-admin", password="test")
        self.operator = User.objects.create_user(username="cap-operator", password="test")
        permission = Permission.objects.get(content_type__app_label="cameras", codename="manage_camera_capability")
        self.admin.user_permissions.add(permission)
        self.admin = User.objects.get(pk=self.admin.pk)
        self.camera = Camera.objects.create(
            nome="Camera compatibility",
            fabricante="Acme",
            modelo="Model X",
            firmware_version="1.0",
        )
        self.profile = CameraCapabilityProfile.objects.get(profile_key="RTSP_DISCOVERY_V1", version=1)

    def evidence(self, *, status, camera=None, firmware="1.0", vendor=" Acme ", model="Model   X", source_type="LAB", source_ref=None):
        evidence = CameraCapabilityEvidence(
            profile=self.profile,
            camera=camera,
            vendor=vendor,
            model=model,
            firmware_exact=firmware,
            status=status,
            source_type=source_type,
            source_ref=source_ref or f"fixture-{CameraCapabilityEvidence.objects.count()}",
            evidence_date=date(2026, 10, 2),
            environment="synthetic fixture",
            limitations="synthetic only",
        )
        return create_compatibility_evidence(actor=self.admin, evidence=evidence)

    def test_missing_or_other_firmware_evidence_is_unverified(self):
        self.assertEqual(resolve_compatibility(camera=self.camera, profile=self.profile).status, UNVERIFIED)
        self.evidence(status=SUPPORTED, firmware="2.0")
        self.assertEqual(resolve_compatibility(camera=self.camera, profile=self.profile).status, UNVERIFIED)

    def test_unit_evidence_precedes_conflicting_model_evidence_and_reports_it(self):
        self.evidence(status=UNSUPPORTED, source_type="DATASHEET", source_ref="model-evidence")
        unit = self.evidence(status=SUPPORTED, camera=self.camera, source_type="UNIT", source_ref="unit-evidence")
        result = resolve_compatibility(camera=self.camera, profile=self.profile)
        self.assertEqual(result.status, SUPPORTED)
        self.assertEqual(result.evidence, unit)
        self.assertIn("UNIT_EVIDENCE_CONFLICTS_WITH_MODEL_EVIDENCE", result.diagnostics)

    def test_unsupported_unit_evidence_blocks_selection(self):
        self.evidence(status=UNSUPPORTED, camera=self.camera, source_type="UNIT")
        self.assertEqual(resolve_compatibility(camera=self.camera, profile=self.profile).status, UNSUPPORTED)

    def test_matching_is_deterministic_and_conflicting_sources_stay_unverified(self):
        self.evidence(status=SUPPORTED, source_ref="source-z")
        first = self.evidence(status=SUPPORTED, source_ref="source-a")
        result = resolve_compatibility(camera=self.camera, profile=self.profile)
        self.assertEqual(result.evidence, first)
        self.assertEqual(resolve_compatibility(camera=self.camera, profile=self.profile), result)

        self.evidence(status=UNVERIFIED, source_ref="source-unverified")
        ambiguous = resolve_compatibility(camera=self.camera, profile=self.profile)
        self.assertEqual(ambiguous.status, UNVERIFIED)
        self.assertIn("AMBIGUOUS_EVIDENCE", ambiguous.diagnostics)

    def test_unverified_and_changed_identity_do_not_reuse_stale_evidence(self):
        self.evidence(status=SUPPORTED, camera=self.camera, source_type="UNIT")
        self.camera.modelo = "Model Y"
        self.camera.save(update_fields=["modelo"])
        result = resolve_compatibility(camera=self.camera, profile=self.profile)
        self.assertEqual(result.status, UNVERIFIED)
        self.assertIn("STALE_UNIT_EVIDENCE", result.diagnostics)

    def test_firmware_edit_uses_existing_technician_admin_permission(self):
        with self.assertRaises(PermissionDenied):
            set_camera_firmware(actor=self.operator, camera=self.camera, firmware_version="2.0")
        updated = set_camera_firmware(actor=self.admin, camera=self.camera, firmware_version=" 2.0 ")
        self.assertEqual(updated.firmware_version, "2.0")

    def test_evidence_creation_requires_capability_permission_and_catalog_is_empty_by_default(self):
        self.assertFalse(CameraCapabilityEvidence.objects.exists())
        evidence = CameraCapabilityEvidence(
            profile=self.profile,
            vendor="Acme",
            model="Model X",
            firmware_exact="1.0",
            status=SUPPORTED,
            source_type="LAB",
            source_ref="fixture",
            evidence_date=date(2026, 10, 2),
            reviewer=self.operator,
        )
        with self.assertRaises(PermissionDenied):
            create_compatibility_evidence(actor=self.operator, evidence=evidence)
        self.assertFalse(CameraCapabilityEvidence.objects.exists())

    def test_repeated_same_active_source_is_rejected_by_database_constraint(self):
        self.evidence(status=SUPPORTED, source_ref="same-source")
        duplicate = CameraCapabilityEvidence(
            profile=self.profile,
            vendor=" ACME ",
            model="model x",
            firmware_exact="1.0",
            status=SUPPORTED,
            source_type="LAB",
            source_ref="same-source",
            evidence_date=date(2026, 10, 2),
            reviewer=self.admin,
        )
        from django.db import IntegrityError, transaction

        with self.assertRaises(IntegrityError), transaction.atomic():
            duplicate.save()
