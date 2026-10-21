from datetime import date, datetime as PythonDateTime, timezone as datetime_timezone
from hashlib import sha256
import tempfile
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.exceptions import PermissionDenied, ValidationError
from django.core.files.storage import default_storage
from django.test import TestCase, override_settings
from django.utils import timezone

from cameras.imagens.capture_service import request_camera_capture, run_next_capture
from cameras.imagens.gallery_service import CameraGalleryReadService, GalleryState
from cameras.integracao.credentials import CredentialOperationError, ResolvedCameraCredential
from cameras.integracao.rtsp.fake import FakeRtspAdapter
from cameras.integracao.rtsp.gst_adapter import GStreamerRtspAdapter
from cameras.integracao.rtsp.ports import RtspJpegFrame, RtspStage, StageStatus
from cameras.integracao.target_policy import TargetPolicy
from cameras.models import (
    Camera,
    CameraCapabilityEvidence,
    CameraCapabilityProfile,
    CameraCaptureJob,
    CameraConnectionConfig,
    CameraCredential,
    CameraCredentialVersion,
    CameraImageRecord,
    EstadoMonitoramento,
    EventoAuditoria,
)


class _HttpAdapterThatMustNotRun:
    async def capture(self, request, *, credential=None):
        raise AssertionError("RTSP must never fall back to HTTP")


class CameraRtspCaptureTests(TestCase):
    def setUp(self):
        temporary_media = tempfile.TemporaryDirectory(prefix="argos-rtsp-capture-test-")
        self.addCleanup(temporary_media.cleanup)
        media_override = override_settings(MEDIA_ROOT=temporary_media.name)
        media_override.enable()
        self.addCleanup(media_override.disable)

        self.actor = get_user_model().objects.create_user(username="rtsp-capture-tech", password="test")
        self.actor.user_permissions.add(
            Permission.objects.get(content_type__app_label="cameras", codename="capture_camera_image")
        )
        self.camera = Camera.objects.create(
            nome="RTSP capture camera", fabricante="Vendor", modelo="Model",
            firmware_version="1.0", ip="10.42.0.10", farm="FARM-RTSP",
        )
        self.profile = CameraCapabilityProfile.objects.create(
            profile_key="RTSP_CAPTURE_TEST", version=1, active=True,
            adapter_key=CameraCapabilityProfile.Adapter.RTSP,
            allowed_schemes=["rtsp"], allowed_ports=[554],
            tls_policy=CameraCapabilityProfile.TLSPolicy.NOT_APPLICABLE,
            auth_method=CameraCapabilityProfile.AuthMethod.RTSP_NEGOTIATE,
            credential_required=False,
            endpoint_policy=CameraCapabilityProfile.EndpointPolicy.PROFILE_FIXED,
            default_path="/stream", allowed_override_fields=[],
            probe_evidence_stage=CameraCapabilityProfile.ProbeStage.D,
            source_ref="RTSP capture integration test",
        )
        CameraCapabilityEvidence.objects.create(
            profile=self.profile, camera=self.camera,
            vendor="vendor", model="model", firmware_exact="1.0",
            status=CameraCapabilityEvidence.Status.SUPPORTED,
            source_type=CameraCapabilityEvidence.SourceType.UNIT,
            source_ref="RTSP capture integration test evidence",
            evidence_date=date(2026, 1, 1), reviewer=self.actor,
        )
        self.config = CameraConnectionConfig.objects.create(
            camera=self.camera, profile=self.profile, enabled=True,
        )
        self.policy = TargetPolicy.from_mapping({
            "allowed_cidrs": ["10.42.0.0/24"],
            "ports_by_scheme": {"rtsp": [554]},
            "allowed_paths_by_scheme": {"rtsp": ["/stream"]},
            "allowed_farms": ["FARM-RTSP"],
        })

    def _request(self, key="rtsp-capture-key-0001", **kwargs):
        return request_camera_capture(
            actor=self.actor,
            camera_id=self.camera.pk,
            idempotency_key=key,
            target_policy=kwargs.pop("target_policy", self.policy),
            environment_allowed_ports=kwargs.pop("environment_allowed_ports", {554}),
            **kwargs,
        )

    def _run(self, *, rtsp_adapter=None, http_adapter=None, policy=None, allowed_ports=None):
        return run_next_capture(
            target_policy=policy or self.policy,
            environment_allowed_ports=allowed_ports or {554},
            adapter=http_adapter,
            rtsp_adapter=rtsp_adapter,
        )

    def _attach_credential(self):
        credential = CameraCredential.objects.create(
            camera=self.camera, state=CameraCredential.State.ACTIVE,
        )
        version = CameraCredentialVersion.objects.create(
            credential=credential, version=1, ciphertext="not-read-by-test",
            key_version="test", state=CameraCredentialVersion.State.ACTIVE,
            created_by=self.actor,
        )
        credential.active_version = version
        credential.save(update_fields=["active_version"])
        self.config.credential = credential
        self.config.save(update_fields=["credential"])
        return credential

    def test_no_preference_selects_rtsp_and_fake_persists_into_existing_e4_gallery(self):
        job = self._request()
        adapter = FakeRtspAdapter()
        monitoring_before = list(EstadoMonitoramento.objects.filter(camera=self.camera).values())

        result = self._run(rtsp_adapter=adapter)

        self.assertEqual(job.source, CameraCaptureJob.Source.RTSP_FRAME)
        self.assertEqual(
            result.status,
            CameraCaptureJob.Status.SUCCEEDED,
            f"{result.error_code}; calls={adapter.calls}; uri={adapter.last_uri}",
        )
        record = result.image_record
        self.assertEqual(record.provenance, CameraImageRecord.Provenance.CAPTURA_CAMERA)
        self.assertEqual(record.content_type, "image/jpeg")
        self.assertEqual(record.width, 2)
        self.assertEqual(record.height, 2)
        with default_storage.open(record.storage_key, "rb") as stored:
            stored_bytes = stored.read()
        self.assertEqual(record.sha256, sha256(stored_bytes).hexdigest())
        self.assertIsNotNone(record.captured_at)
        self.assertIsNotNone(record.recorded_at)
        self.assertEqual(adapter.last_uri, "rtsp://10.42.0.10:554/stream")
        self.assertTrue(EventoAuditoria.objects.filter(codigo="imagem.captura.concluida", entidade_id=result.pk).exists())
        gallery = CameraGalleryReadService(storage_exists=lambda key: True).list_active(self.camera.pk)
        self.assertEqual(gallery.state, GalleryState.AVAILABLE)
        self.assertEqual(gallery.images[0].immutable_id, record.pk)
        self.assertEqual(monitoring_before, list(EstadoMonitoramento.objects.filter(camera=self.camera).values()))

    def test_default_worker_real_adapter_and_fake_subclass_fail_before_credentials_and_http(self):
        job = self._request()
        http_adapter = _HttpAdapterThatMustNotRun()
        with patch("cameras.imagens.capture_service.resolve_active_credential_for_execution") as resolver:
            result = self._run(http_adapter=http_adapter)
        resolver.assert_not_called()
        self.assertEqual(result.pk, job.pk)
        self.assertEqual(result.error_code, "CAPABILITY_UNSUPPORTED")

        job = self._request("rtsp-capture-key-0008")
        gstreamer_adapter = object.__new__(GStreamerRtspAdapter)
        with (
            patch("cameras.imagens.capture_service.resolve_active_credential_for_execution") as resolver,
            patch.object(
                GStreamerRtspAdapter,
                "extract_one_jpeg_frame",
                side_effect=AssertionError("real RTSP adapter method must not run"),
            ) as extract,
        ):
            result = self._run(rtsp_adapter=gstreamer_adapter, http_adapter=http_adapter)
        resolver.assert_not_called()
        extract.assert_not_called()
        self.assertEqual(result.pk, job.pk)
        self.assertEqual(result.error_code, "CAPABILITY_UNSUPPORTED")

        class FakeSubclass(FakeRtspAdapter):
            pass

        job = self._request("rtsp-capture-key-0002")
        with patch("cameras.imagens.capture_service.resolve_active_credential_for_execution") as resolver:
            result = self._run(rtsp_adapter=FakeSubclass())
        resolver.assert_not_called()
        self.assertEqual(result.pk, job.pk)
        self.assertEqual(result.error_code, "CAPABILITY_UNSUPPORTED")

    def test_valid_credential_is_resolved_by_r1_and_supplied_only_in_memory(self):
        self._attach_credential()
        job = self._request()
        adapter = FakeRtspAdapter()
        credential = ResolvedCameraCredential("camera-user", "camera-secret")
        with patch(
            "cameras.imagens.capture_service.resolve_active_credential_for_execution",
            return_value=credential,
        ) as resolver:
            result = self._run(rtsp_adapter=adapter)

        resolver.assert_called_once()
        self.assertEqual(result.status, CameraCaptureJob.Status.SUCCEEDED, result.error_code)
        self.assertTrue(adapter.authentication_configured)
        self.assertEqual(result.pk, job.pk)
        self.assertNotIn("camera-secret", str(result))

    def test_inaccessible_credential_stops_before_adapter(self):
        self._attach_credential()
        job = self._request()
        adapter = FakeRtspAdapter()
        with patch(
            "cameras.imagens.capture_service.resolve_active_credential_for_execution",
            side_effect=CredentialOperationError("unavailable"),
        ) as resolver:
            result = self._run(rtsp_adapter=adapter)
        resolver.assert_called_once()
        self.assertEqual(result.pk, job.pk)
        self.assertEqual(result.error_code, "CREDENTIAL_UNAVAILABLE")
        self.assertEqual(adapter.calls, 0)

    def test_config_change_during_r1_resolution_blocks_adapter(self):
        self._attach_credential()
        CameraCapabilityProfile.objects.filter(pk=self.profile.pk).update(
            endpoint_policy=CameraCapabilityProfile.EndpointPolicy.TECHNICIAN_OVERRIDE,
            allowed_override_fields=["path"],
        )
        policy = TargetPolicy.from_mapping({
            "allowed_cidrs": ["10.42.0.0/24"],
            "ports_by_scheme": {"rtsp": [554]},
            "allowed_paths_by_scheme": {"rtsp": ["/stream", "/stream-alt"]},
            "allowed_farms": ["FARM-RTSP"],
        })
        job = self._request("rtsp-capture-key-0006", target_policy=policy)
        adapter = FakeRtspAdapter()
        resolved = ResolvedCameraCredential("camera-user", "camera-secret")

        def change_config(**kwargs):
            CameraConnectionConfig.objects.filter(pk=self.config.pk).update(
                rtsp_uri="rtsp://10.42.0.10:554/stream-alt"
            )
            return resolved

        with patch(
            "cameras.imagens.capture_service.resolve_active_credential_for_execution",
            side_effect=change_config,
        ):
            result = self._run(rtsp_adapter=adapter, policy=policy)

        self.assertEqual(result.pk, job.pk)
        self.assertEqual(result.error_code, "CONFIG_INVALID")
        self.assertEqual(adapter.calls, 0)

    def test_required_missing_or_revoked_credential_blocks_enqueue_and_adapter(self):
        CameraCapabilityProfile.objects.filter(pk=self.profile.pk).update(credential_required=True)
        with self.assertRaises(ValidationError):
            self._request()
        self.assertFalse(CameraCaptureJob.objects.exists())

        CameraCapabilityProfile.objects.filter(pk=self.profile.pk).update(credential_required=False)
        credential = self._attach_credential()
        CameraCredential.objects.filter(pk=credential.pk).update(state=CameraCredential.State.INACTIVE)
        with self.assertRaises(ValidationError):
            self._request("rtsp-capture-key-0003")
        self.assertFalse(CameraCaptureJob.objects.exists())

    def test_rtsp_auth_method_is_closed_before_enqueue(self):
        credential = self._attach_credential()
        CameraCapabilityProfile.objects.filter(pk=self.profile.pk).update(
            auth_method=CameraCapabilityProfile.AuthMethod.NONE,
            credential_required=False,
        )
        with self.assertRaises(ValidationError):
            self._request()
        self.assertFalse(CameraCaptureJob.objects.exists())

        CameraConnectionConfig.objects.filter(pk=self.config.pk).update(credential=None)
        CameraCredential.objects.filter(pk=credential.pk).update(state=CameraCredential.State.INACTIVE)
        CameraCapabilityProfile.objects.filter(pk=self.profile.pk).update(
            auth_method=CameraCapabilityProfile.AuthMethod.BASIC,
        )
        with self.assertRaises(ValidationError):
            self._request("rtsp-capture-key-0007")
        self.assertFalse(CameraCaptureJob.objects.exists())

    def test_rtsp_port_must_be_in_profile_policy_and_environment_intersection(self):
        policy = TargetPolicy.from_mapping({
            "allowed_cidrs": ["10.42.0.0/24"],
            "ports_by_scheme": {"rtsp": [8554]},
            "allowed_paths_by_scheme": {"rtsp": ["/stream"]},
            "allowed_farms": ["FARM-RTSP"],
        })
        with self.assertRaises(ValidationError):
            self._request(target_policy=policy, environment_allowed_ports={8554})
        self.assertFalse(CameraCaptureJob.objects.exists())

    def test_denied_target_and_permission_do_not_create_jobs_or_call_adapter(self):
        denied = TargetPolicy.from_mapping({
            "allowed_cidrs": ["10.43.0.0/24"],
            "ports_by_scheme": {"rtsp": [554]},
            "allowed_paths_by_scheme": {"rtsp": ["/stream"]},
            "allowed_farms": ["FARM-RTSP"],
        })
        with self.assertRaises(ValidationError):
            self._request(target_policy=denied)
        self.actor.user_permissions.clear()
        with self.assertRaises(PermissionDenied):
            self.actor = get_user_model().objects.get(pk=self.actor.pk)
            self._request("rtsp-capture-key-0004")
        self.assertFalse(CameraCaptureJob.objects.exists())

    def test_invalid_jpeg_and_cancellation_during_fake_do_not_persist_image(self):
        job = self._request()
        invalid = RtspJpegFrame(
            b"\xff\xd8not-a-jpeg\xff\xd9", 2, 2, "H264", PythonDateTime.now(datetime_timezone.utc)
        )
        with patch.object(FakeRtspAdapter, "extract_one_jpeg_frame", return_value=invalid):
            result = self._run(rtsp_adapter=FakeRtspAdapter())
        self.assertEqual(result.status, CameraCaptureJob.Status.FAILED)
        self.assertEqual(result.error_code, "IMAGE_INVALID")
        self.assertFalse(CameraImageRecord.objects.filter(camera=self.camera).exists())

        cancelled_job = self._request("rtsp-capture-key-0005")
        adapter = FakeRtspAdapter()
        original = adapter.extract_one_jpeg_frame

        def cancel_during_extract(request):
            CameraCaptureJob.objects.filter(pk=cancelled_job.pk).update(
                status=CameraCaptureJob.Status.CANCELLED,
                error_code="INTERNAL_ERROR",
                finished_at=timezone.now(),
            )
            return original(request)

        with patch.object(adapter, "extract_one_jpeg_frame", side_effect=cancel_during_extract):
            result = self._run(rtsp_adapter=adapter)
        self.assertEqual(result.status, CameraCaptureJob.Status.CANCELLED)
        self.assertIsNone(result.image_record)
        self.assertFalse(CameraImageRecord.objects.filter(camera=self.camera).exists())

    def test_frame_extraction_failure_does_not_call_http(self):
        job = self._request()
        rtsp_adapter = FakeRtspAdapter(
            outcomes={RtspStage.MEDIA_DELIVERY: StageStatus.FAIL},
            error_code="DECODE_FAILED",
        )
        result = self._run(
            rtsp_adapter=rtsp_adapter,
            http_adapter=_HttpAdapterThatMustNotRun(),
        )
        self.assertEqual(result.pk, job.pk)
        self.assertEqual(result.error_code, "IMAGE_INVALID")
