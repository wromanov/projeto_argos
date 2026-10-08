from datetime import date
import os
import tempfile
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.exceptions import PermissionDenied, ValidationError
from django.test import TestCase, override_settings

from cameras.imagens.capture_service import request_camera_capture, run_next_capture
from cameras.integracao.http_snapshot.adapter import SnapshotImage
from cameras.integracao.credentials import CredentialOperationError, ResolvedCameraCredential
from cameras.integracao.target_policy import TargetPolicy
from cameras.models import (
    Camera,
    CameraCapabilityEvidence,
    CameraCapabilityProfile,
    CameraCaptureJob,
    CameraCredential,
    CameraCredentialVersion,
    CameraConnectionConfig,
    CameraImageRecord,
    EstadoMonitoramento,
)


class _FakeSnapshotAdapter:
    def __init__(self, event_order=None):
        self.requests = []
        self.event_order = event_order

    async def capture(self, request, *, credential=None):
        if self.event_order is not None:
            self.event_order.append("adapter")
        self.requests.append((request, credential))
        return SnapshotImage(b"validated-image-bytes", "image/png", "PNG", 2, 1)


class CameraCaptureServiceTests(TestCase):
    def setUp(self):
        temporary_media = tempfile.TemporaryDirectory(prefix="argos-capture-test-")
        self.addCleanup(temporary_media.cleanup)
        media_override = override_settings(MEDIA_ROOT=temporary_media.name)
        media_override.enable()
        self.addCleanup(media_override.disable)

        self.actor = get_user_model().objects.create_user(username="capture-tech", password="test")
        permission = Permission.objects.get(content_type__app_label="cameras", codename="capture_camera_image")
        self.actor.user_permissions.add(permission)
        self.camera = Camera.objects.create(
            nome="Capture Camera", fabricante="Vendor", modelo="Model", firmware_version="1.0",
            ip="10.42.0.10", farm="FARM-A",
        )
        self.profile = CameraCapabilityProfile.objects.create(
            profile_key="HTTP_SNAPSHOT_TEST", version=1, active=True,
            adapter_key=CameraCapabilityProfile.Adapter.HTTP_SNAPSHOT,
            allowed_schemes=["https"], allowed_ports=[443],
            tls_policy=CameraCapabilityProfile.TLSPolicy.REQUIRED,
            auth_method=CameraCapabilityProfile.AuthMethod.NONE,
            credential_required=False,
            endpoint_policy=CameraCapabilityProfile.EndpointPolicy.PROFILE_FIXED,
            default_path="/snapshot", allowed_override_fields=[],
            probe_evidence_stage=CameraCapabilityProfile.ProbeStage.D,
            source_ref="test fixture",
        )
        CameraCapabilityEvidence.objects.create(
            profile=self.profile, camera=self.camera, vendor="vendor", model="model",
            firmware_exact="1.0", status=CameraCapabilityEvidence.Status.SUPPORTED,
            source_type=CameraCapabilityEvidence.SourceType.UNIT, source_ref="test evidence",
            evidence_date=date(2026, 1, 1), reviewer=self.actor,
        )
        self.config = CameraConnectionConfig.objects.create(
            camera=self.camera, profile=self.profile, enabled=True,
        )
        self.policy = TargetPolicy.from_mapping({
            "allowed_cidrs": ["10.42.0.0/24"],
            "ports_by_scheme": {"https": [443]},
            "allowed_farms": ["FARM-A"],
        })

    def _request(self, key="capture-key-0001", **kwargs):
        target_policy = kwargs.pop("target_policy", self.policy)
        return request_camera_capture(
            actor=self.actor, camera_id=self.camera.pk, idempotency_key=key,
            target_policy=target_policy, environment_allowed_ports={443}, **kwargs,
        )

    def _configure_path_override_profile(self):
        profile = CameraCapabilityProfile.objects.create(
            profile_key="HTTP_SNAPSHOT_PATH_TEST", version=1, active=True,
            adapter_key=CameraCapabilityProfile.Adapter.HTTP_SNAPSHOT,
            allowed_schemes=["https"], allowed_ports=[443],
            tls_policy=CameraCapabilityProfile.TLSPolicy.REQUIRED,
            auth_method=CameraCapabilityProfile.AuthMethod.NONE,
            credential_required=False,
            endpoint_policy=CameraCapabilityProfile.EndpointPolicy.TECHNICIAN_OVERRIDE,
            default_path="/snapshot", allowed_override_fields=["path"],
            probe_evidence_stage=CameraCapabilityProfile.ProbeStage.D,
            source_ref="test fixture",
        )
        CameraCapabilityEvidence.objects.create(
            profile=profile, camera=self.camera, vendor="vendor", model="model",
            firmware_exact="1.0", status=CameraCapabilityEvidence.Status.SUPPORTED,
            source_type=CameraCapabilityEvidence.SourceType.UNIT,
            source_ref="HTTP_SNAPSHOT_PATH_TEST evidence",
            evidence_date=date(2026, 1, 1), reviewer=self.actor,
        )
        CameraConnectionConfig.objects.filter(pk=self.config.pk).update(profile=profile)
        return profile

    def _configure_authenticated_profile(self, auth_method, profile_key, *, allow_path_override=False):
        profile = CameraCapabilityProfile.objects.create(
            profile_key=profile_key, version=1, active=True,
            adapter_key=CameraCapabilityProfile.Adapter.HTTP_SNAPSHOT,
            allowed_schemes=["https"], allowed_ports=[443],
            tls_policy=CameraCapabilityProfile.TLSPolicy.REQUIRED,
            auth_method=auth_method, credential_required=True,
            endpoint_policy=(
                CameraCapabilityProfile.EndpointPolicy.TECHNICIAN_OVERRIDE
                if allow_path_override
                else CameraCapabilityProfile.EndpointPolicy.PROFILE_FIXED
            ),
            default_path="/snapshot",
            allowed_override_fields=["path"] if allow_path_override else [],
            probe_evidence_stage=CameraCapabilityProfile.ProbeStage.D,
            source_ref="test fixture",
        )
        CameraCapabilityEvidence.objects.create(
            profile=profile, camera=self.camera, vendor="vendor", model="model",
            firmware_exact="1.0", status=CameraCapabilityEvidence.Status.SUPPORTED,
            source_type=CameraCapabilityEvidence.SourceType.UNIT, source_ref=f"{profile_key} evidence",
            evidence_date=date(2026, 1, 1), reviewer=self.actor,
        )
        credential_record = CameraCredential.objects.create(
            camera=self.camera, state=CameraCredential.State.ACTIVE,
        )
        version = CameraCredentialVersion.objects.create(
            credential=credential_record, version=1, ciphertext="not-read-by-test",
            key_version="test", state=CameraCredentialVersion.State.ACTIVE,
            created_by=self.actor,
        )
        credential_record.active_version = version
        credential_record.save(update_fields=["active_version"])
        self.config.profile = profile
        self.config.credential = credential_record
        self.config.save(update_fields=["profile", "credential"])
        return profile

    def test_same_actor_camera_and_key_returns_same_queued_job(self):
        first = self._request()
        second = self._request()

        self.assertEqual(first.pk, second.pk)
        self.assertEqual(CameraCaptureJob.objects.filter(camera=self.camera).count(), 1)
        self.assertEqual(first.status, CameraCaptureJob.Status.QUEUED)

    def test_worker_revalidates_and_persists_capture_without_monitoring_side_effect(self):
        job = self._request()
        adapter = _FakeSnapshotAdapter()
        monitoring_before = list(EstadoMonitoramento.objects.filter(camera=self.camera).values())

        result = run_next_capture(
            target_policy=self.policy, environment_allowed_ports={443}, adapter=adapter,
        )

        self.assertEqual(result.pk, job.pk)
        self.assertEqual(result.status, CameraCaptureJob.Status.SUCCEEDED)
        self.assertEqual(result.image_record.provenance, CameraImageRecord.Provenance.CAPTURA_CAMERA)
        self.assertIsNone(adapter.requests[0][1])
        self.assertEqual(monitoring_before, list(EstadoMonitoramento.objects.filter(camera=self.camera).values()))
        self.assertEqual(len(adapter.requests), 1)

    def test_default_path_is_allowed_when_profile_also_permits_path_override(self):
        self._configure_path_override_profile()
        CameraConnectionConfig.objects.filter(pk=self.config.pk).update(
            http_endpoint_override="/snapshot"
        )
        job = self._request("capture-path-default-01")
        adapter = _FakeSnapshotAdapter()

        result = run_next_capture(
            target_policy=self.policy, environment_allowed_ports={443}, adapter=adapter,
        )

        self.assertEqual(result.pk, job.pk)
        self.assertEqual(result.status, CameraCaptureJob.Status.SUCCEEDED)
        self.assertEqual(adapter.requests[0][0].target.request.path, "/snapshot")

    def test_custom_path_fails_closed_without_independent_policy_allowlist(self):
        self._configure_path_override_profile()
        CameraConnectionConfig.objects.filter(pk=self.config.pk).update(
            http_endpoint_override="/snapshot-alt"
        )

        with self.assertRaises(ValidationError):
            self._request("capture-path-denied-01")

        self.assertFalse(CameraCaptureJob.objects.exists())

    def test_custom_path_requires_and_uses_explicit_policy_allowlist(self):
        self._configure_path_override_profile()
        CameraConnectionConfig.objects.filter(pk=self.config.pk).update(
            http_endpoint_override="/snapshot-alt"
        )
        policy = TargetPolicy.from_mapping({
            "allowed_cidrs": ["10.42.0.0/24"],
            "ports_by_scheme": {"https": [443]},
            "allowed_farms": ["FARM-A"],
            "allowed_paths_by_scheme": {"https": ["/snapshot-alt"]},
        })
        job = self._request("capture-path-allowed-01", target_policy=policy)
        adapter = _FakeSnapshotAdapter()

        result = run_next_capture(
            target_policy=policy, environment_allowed_ports={443}, adapter=adapter,
        )

        self.assertEqual(result.pk, job.pk)
        self.assertEqual(result.status, CameraCaptureJob.Status.SUCCEEDED)
        self.assertEqual(adapter.requests[0][0].target.request.path, "/snapshot-alt")

    def test_worker_uses_environment_http_path_allowlist_and_fails_closed_on_change(self):
        self._configure_path_override_profile()
        CameraConnectionConfig.objects.filter(pk=self.config.pk).update(
            http_endpoint_override="/snapshot-alt"
        )
        environment = {
            "ARGOS_CAMERA_ALLOWED_CIDRS": "10.42.0.0/24",
            "ARGOS_CAMERA_ALLOWED_PORTS": "https:443",
            "ARGOS_CAMERA_ALLOWED_PATHS": "https:/snapshot-alt",
            "ARGOS_CAMERA_ALLOWED_FARMS": "FARM-A",
        }
        with patch.dict("os.environ", environment):
            allowed_job = request_camera_capture(
                actor=self.actor, camera_id=self.camera.pk,
                idempotency_key="capture-env-path-allowed-01",
            )
            allowed_adapter = _FakeSnapshotAdapter()
            allowed_result = run_next_capture(adapter=allowed_adapter)

            self.assertEqual(allowed_result.pk, allowed_job.pk)
            self.assertEqual(allowed_result.status, CameraCaptureJob.Status.SUCCEEDED)
            self.assertEqual(allowed_adapter.requests[0][0].target.request.path, "/snapshot-alt")

            absent_job = request_camera_capture(
                actor=self.actor, camera_id=self.camera.pk,
                idempotency_key="capture-env-path-absent-01",
            )
            os.environ.pop("ARGOS_CAMERA_ALLOWED_PATHS")
            absent_adapter = _FakeSnapshotAdapter()
            with patch("cameras.imagens.capture_service.resolve_active_credential_for_execution") as resolver:
                absent_result = run_next_capture(adapter=absent_adapter)
            resolver.assert_not_called()
            self.assertEqual(absent_result.pk, absent_job.pk)
            self.assertEqual(absent_result.status, CameraCaptureJob.Status.FAILED)
            self.assertEqual(absent_result.error_code, "TARGET_DENIED")
            self.assertEqual(absent_adapter.requests, [])

            os.environ["ARGOS_CAMERA_ALLOWED_PATHS"] = "https:/snapshot-alt"
            revoked_job = request_camera_capture(
                actor=self.actor, camera_id=self.camera.pk,
                idempotency_key="capture-env-path-revoked-01",
            )
            os.environ["ARGOS_CAMERA_ALLOWED_PATHS"] = "https:/snapshot-other"
            revoked_adapter = _FakeSnapshotAdapter()
            with patch("cameras.imagens.capture_service.resolve_active_credential_for_execution") as resolver:
                revoked_result = run_next_capture(adapter=revoked_adapter)
            resolver.assert_not_called()
            self.assertEqual(revoked_result.pk, revoked_job.pk)
            self.assertEqual(revoked_result.status, CameraCaptureJob.Status.FAILED)
            self.assertEqual(revoked_result.error_code, "TARGET_DENIED")
            self.assertEqual(revoked_adapter.requests, [])

            os.environ["ARGOS_CAMERA_ALLOWED_PATHS"] = "https:/snapshot-alt"
            invalid_job = request_camera_capture(
                actor=self.actor, camera_id=self.camera.pk,
                idempotency_key="capture-env-path-invalid-01",
            )
            os.environ["ARGOS_CAMERA_ALLOWED_PATHS"] = "https:relative-path"
            invalid_adapter = _FakeSnapshotAdapter()
            with patch("cameras.imagens.capture_service.resolve_active_credential_for_execution") as resolver:
                invalid_result = run_next_capture(adapter=invalid_adapter)
            resolver.assert_not_called()
            self.assertEqual(invalid_result.pk, invalid_job.pk)
            self.assertEqual(invalid_result.status, CameraCaptureJob.Status.FAILED)
            self.assertEqual(invalid_result.error_code, "CONFIG_INVALID")
            self.assertEqual(invalid_adapter.requests, [])

    def test_custom_path_not_listed_by_policy_is_denied_before_job(self):
        self._configure_path_override_profile()
        CameraConnectionConfig.objects.filter(pk=self.config.pk).update(
            http_endpoint_override="/snapshot-not-allowed"
        )
        policy = TargetPolicy.from_mapping({
            "allowed_cidrs": ["10.42.0.0/24"],
            "ports_by_scheme": {"https": [443]},
            "allowed_farms": ["FARM-A"],
            "allowed_paths_by_scheme": {"https": ["/snapshot-alt"]},
        })

        with self.assertRaises(ValidationError):
            self._request("capture-path-not-listed-01", target_policy=policy)

        self.assertFalse(CameraCaptureJob.objects.exists())

    def test_custom_path_allowlist_revocation_blocks_before_r1_and_adapter(self):
        self._configure_authenticated_profile(
            CameraCapabilityProfile.AuthMethod.BASIC,
            "HTTP_SNAPSHOT_PATH_R1_TEST",
            allow_path_override=True,
        )
        CameraConnectionConfig.objects.filter(pk=self.config.pk).update(
            http_endpoint_override="/snapshot-alt"
        )
        policy = TargetPolicy.from_mapping({
            "allowed_cidrs": ["10.42.0.0/24"],
            "ports_by_scheme": {"https": [443]},
            "allowed_farms": ["FARM-A"],
            "allowed_paths_by_scheme": {"https": ["/snapshot-alt"]},
        })
        job = self._request("capture-path-revoked-01", target_policy=policy)
        adapter = _FakeSnapshotAdapter()

        with patch("cameras.imagens.capture_service.resolve_active_credential_for_execution") as resolver:
            result = run_next_capture(
                target_policy=self.policy, environment_allowed_ports={443}, adapter=adapter,
            )

        resolver.assert_not_called()
        self.assertEqual(result.pk, job.pk)
        self.assertEqual(result.status, CameraCaptureJob.Status.FAILED)
        self.assertEqual(result.error_code, "TARGET_DENIED")
        self.assertEqual(adapter.requests, [])

    def test_denied_target_fails_before_adapter_and_does_not_resolve_credential(self):
        job = self._request()
        adapter = _FakeSnapshotAdapter()
        denied = TargetPolicy.from_mapping({
            "allowed_cidrs": ["10.43.0.0/24"],
            "ports_by_scheme": {"https": [443]},
            "allowed_farms": ["FARM-A"],
        })
        with patch("cameras.imagens.capture_service.resolve_active_credential_for_execution") as resolver:
            result = run_next_capture(
                target_policy=denied, environment_allowed_ports={443}, adapter=adapter,
            )

        resolver.assert_not_called()
        self.assertEqual(result.pk, job.pk)
        self.assertEqual(result.status, CameraCaptureJob.Status.FAILED)
        self.assertEqual(result.error_code, "TARGET_DENIED")
        self.assertEqual(adapter.requests, [])
        self.assertIsNone(result.image_record)

    def test_basic_auth_resolves_only_after_policy_and_passes_secret_only_to_adapter(self):
        self._configure_authenticated_profile(CameraCapabilityProfile.AuthMethod.BASIC, "HTTP_SNAPSHOT_BASIC_TEST")
        job = self._request("capture-basic-key-01")
        event_order = []
        adapter = _FakeSnapshotAdapter(event_order)
        resolved = ResolvedCameraCredential("ephemeral-user", "ephemeral-password")
        from cameras.authorization import require_camera_permission as real_permission

        def permission_check(**kwargs):
            event_order.append("permission")
            return real_permission(**kwargs)

        def resolve(**kwargs):
            event_order.append("resolver")
            return resolved

        with patch("cameras.imagens.capture_service.require_camera_permission", side_effect=permission_check), patch(
            "cameras.imagens.capture_service.resolve_active_credential_for_execution", side_effect=resolve,
        ) as resolver:
            result = run_next_capture(
                target_policy=self.policy, environment_allowed_ports={443}, adapter=adapter,
            )

        resolver.assert_called_once()
        self.assertEqual(result.pk, job.pk)
        self.assertEqual(result.status, CameraCaptureJob.Status.SUCCEEDED)
        self.assertIs(adapter.requests[0][1], resolved)
        self.assertEqual(event_order[-3:], ["permission", "resolver", "adapter"])
        self.assertNotIn("ephemeral-user", str(result.__dict__))
        self.assertNotIn("ephemeral-password", str(result.__dict__))

    def test_digest_auth_resolves_via_r1_and_is_passed_only_to_adapter(self):
        self._configure_authenticated_profile(CameraCapabilityProfile.AuthMethod.DIGEST, "HTTP_SNAPSHOT_DIGEST_TEST")
        job = self._request("capture-digest-key-01")
        adapter = _FakeSnapshotAdapter()
        resolved = ResolvedCameraCredential("digest-user", "digest-password")
        with patch(
            "cameras.imagens.capture_service.resolve_active_credential_for_execution",
            return_value=resolved,
        ) as resolver:
            result = run_next_capture(
                target_policy=self.policy, environment_allowed_ports={443}, adapter=adapter,
            )

        resolver.assert_called_once()
        self.assertEqual(result.pk, job.pk)
        self.assertEqual(result.status, CameraCaptureJob.Status.SUCCEEDED)
        self.assertEqual(adapter.requests[0][0].auth_method, CameraCapabilityProfile.AuthMethod.DIGEST)
        self.assertIs(adapter.requests[0][1], resolved)

    def test_resolver_failure_fails_job_without_adapter_or_image_record(self):
        self._configure_authenticated_profile(CameraCapabilityProfile.AuthMethod.BASIC, "HTTP_SNAPSHOT_R1_FAILURE_TEST")
        job = self._request("capture-r1-failure-01")
        adapter = _FakeSnapshotAdapter()
        with patch(
            "cameras.imagens.capture_service.resolve_active_credential_for_execution",
            side_effect=CredentialOperationError("VERSION_NOT_ALLOWED"),
        ) as resolver:
            result = run_next_capture(
                target_policy=self.policy, environment_allowed_ports={443}, adapter=adapter,
            )

        resolver.assert_called_once()
        self.assertEqual(result.pk, job.pk)
        self.assertEqual(result.status, CameraCaptureJob.Status.FAILED)
        self.assertEqual(result.error_code, "CREDENTIAL_UNAVAILABLE")
        self.assertEqual(adapter.requests, [])
        self.assertIsNone(result.image_record)
        self.assertFalse(CameraImageRecord.objects.filter(camera=self.camera).exists())

    def test_ip_change_after_r1_fails_without_network_or_image(self):
        self._configure_authenticated_profile(CameraCapabilityProfile.AuthMethod.BASIC, "HTTP_SNAPSHOT_IP_CHANGE_TEST")
        job = self._request("capture-ip-change-01")
        adapter = _FakeSnapshotAdapter()
        resolved = ResolvedCameraCredential("ephemeral-user", "ephemeral-password")

        def resolve_then_change_camera_ip(*, config):
            Camera.objects.filter(pk=self.camera.pk).update(ip="10.42.0.11")
            return resolved

        with patch(
            "cameras.imagens.capture_service.resolve_active_credential_for_execution",
            side_effect=resolve_then_change_camera_ip,
        ) as resolver:
            result = run_next_capture(
                target_policy=self.policy, environment_allowed_ports={443}, adapter=adapter,
            )

        resolver.assert_called_once()
        self.assertEqual(result.pk, job.pk)
        self.assertEqual(result.status, CameraCaptureJob.Status.FAILED)
        self.assertEqual(result.error_code, "CONFIG_INVALID")
        self.assertEqual(adapter.requests, [])
        self.assertIsNone(result.image_record)
        self.assertFalse(CameraImageRecord.objects.filter(camera=self.camera).exists())

    def test_permission_denial_precedes_job_creation(self):
        self.actor.user_permissions.clear()

        with self.assertRaises(PermissionDenied):
            self._request()

        self.assertFalse(CameraCaptureJob.objects.exists())

    def test_worker_permission_revocation_precedes_r1_and_http_adapter(self):
        job = self._request()
        self.actor.user_permissions.clear()
        adapter = _FakeSnapshotAdapter()

        with patch("cameras.imagens.capture_service.resolve_active_credential_for_execution") as resolver:
            result = run_next_capture(
                target_policy=self.policy, environment_allowed_ports={443}, adapter=adapter,
            )

        resolver.assert_not_called()
        self.assertEqual(result.pk, job.pk)
        self.assertEqual(result.status, CameraCaptureJob.Status.FAILED)
        self.assertEqual(result.error_code, "AUTHORIZATION_DENIED")
        self.assertEqual(adapter.requests, [])

    def test_rtsp_preference_is_rejected_without_creating_a_capturable_job(self):
        with self.assertRaises(ValidationError):
            self._request(source_preference=CameraCaptureJob.Source.RTSP_FRAME)

        self.assertFalse(CameraCaptureJob.objects.exists())
