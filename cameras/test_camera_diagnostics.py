"""CAM-INT-05 automatic diagnostics and atomic MON completion tests."""

from datetime import date, datetime, timedelta, timezone

from django.contrib.auth import get_user_model
from django.test import TestCase

from cameras.integracao.diagnostics import (
    ConnectionTestResult,
    DiagnosticSource,
    run_automatic_camera_diagnostic,
)
from cameras.integracao.rtsp.fake import FakeRtspAdapter
from cameras.integracao.rtsp.ports import RtspStage, StageStatus
from cameras.integracao.target_policy import TargetPolicy
from cameras.models import (
    Camera,
    CameraCapabilityEvidence,
    CameraCapabilityProfile,
    CameraConnectionConfig,
    CameraHealthSnapshot,
    EstadoMonitoramento,
)
from cameras.monitoramento.confirmation import ConfirmationPolicy, TechnicalState
from cameras.monitoramento.fakes import FakeClock
from cameras.monitoramento.repository import DjangoMonitoringRepository
from cameras.monitoramento.scheduler import DueScheduler
from cameras.monitoramento.schemas import CompletionDisposition, MonitoringConfig, ScheduleCandidate


NOW = datetime(2026, 10, 10, 12, tzinfo=timezone.utc)
POLICY = TargetPolicy.from_mapping({
    "allowed_cidrs": ["10.42.0.0/24"],
    "ports_by_scheme": {"rtsp": [554]},
    "allowed_paths_by_scheme": {"rtsp": ["/stream-a"]},
})


class CameraDiagnosticTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="diagnostic-reviewer")
        self.camera = Camera.objects.create(
            nome="Camera A", fabricante="Vendor", modelo="Model", serial="SER-A",
            mac="00:11:22:33:44:55", tipo=Camera.TipoCamera.BULLET,
            terminal="T", pavimento="P", setor="S", ambiente="A", ponto_referencia="PR",
            farm="F", codec="H264", ip="10.42.0.10", mascara_subrede="255.255.255.0",
            gateway="10.42.0.1", vlan=10, retencao_esperada_dias=30,
        )
        self.profile = CameraCapabilityProfile.objects.get(profile_key="RTSP_DISCOVERY_V1", version=1)
        CameraCapabilityEvidence.objects.create(
            profile=self.profile, camera=self.camera, vendor="Vendor", model="Model",
            firmware_exact="", status=CameraCapabilityEvidence.Status.SUPPORTED,
            source_type=CameraCapabilityEvidence.SourceType.LAB, source_ref="CAM-INT-05 test fixture",
            evidence_date=date(2026, 10, 10), reviewer=self.user,
        )
        CameraConnectionConfig.objects.create(
            camera=self.camera, profile=self.profile, enabled=True,
            rtsp_uri="rtsp://10.42.0.10:554/stream-a", config_version=1,
        )

    def diagnose(self, adapter=None, generation=1, at=NOW):
        return run_automatic_camera_diagnostic(
            camera_id=self.camera.pk, config_generation=generation, target_policy=POLICY,
            adapter=adapter or FakeRtspAdapter(monotonic=lambda: 1.0, now=lambda: at),
            monotonic=lambda: 1.0, now=lambda: at,
        )

    def test_automatic_d_pass_alone_maps_to_success_and_preserves_a_to_d_evidence(self):
        result = self.diagnose()
        self.assertEqual(result.source, DiagnosticSource.AUTOMATIC)
        self.assertEqual(tuple(item.state for item in result.stages), (StageStatus.PASS,) * 4)
        self.assertEqual(result.probe_result.code.name, "SUCCESS")
        self.assertEqual(result.reached_stage, "D")

    def test_failed_stage_leaves_later_stages_not_run_and_neutral_error_codes(self):
        adapter = FakeRtspAdapter(
            outcomes={RtspStage.RTSP_REACHABILITY: StageStatus.FAIL},
            error_code="AUTH_FAILURE", monotonic=lambda: 1.0, now=lambda: NOW,
        )
        result = self.diagnose(adapter)
        self.assertEqual(tuple(item.state for item in result.stages), (
            StageStatus.PASS, StageStatus.FAIL, StageStatus.NOT_RUN, StageStatus.NOT_RUN,
        ))
        self.assertEqual(result.probe_result.code.name, "AUTH_FAILURE")
        self.assertFalse(result.probe_result.is_success)

    def test_d_fail_never_maps_to_success(self):
        adapter = FakeRtspAdapter(
            outcomes={RtspStage.MEDIA_DELIVERY: StageStatus.FAIL},
            error_code="PROTOCOL_ERROR", monotonic=lambda: 1.0, now=lambda: NOW,
        )
        result = self.diagnose(adapter)
        self.assertEqual(tuple(item.state for item in result.stages), (
            StageStatus.PASS, StageStatus.PASS, StageStatus.PASS, StageStatus.FAIL,
        ))
        self.assertEqual(result.probe_result.code.name, "PROTOCOL_ERROR")
        self.assertFalse(result.probe_result.is_success)

    def test_stale_generation_fails_closed_before_adapter(self):
        EstadoMonitoramento.objects.create(camera=self.camera, ultima_geracao_configuracao=2)
        adapter = FakeRtspAdapter(monotonic=lambda: 1.0, now=lambda: NOW)
        result = self.diagnose(adapter, generation=1)
        self.assertEqual(result.probe_result.code.name, "CONFIG_ERROR")
        self.assertEqual(result.stages[0].state, StageStatus.NOT_RUN)
        self.assertEqual(adapter.calls, 0)

    def test_profile_deactivation_between_probe_and_completion_rejects_snapshot(self):
        diagnostic = self.diagnose()
        self.profile.active = False
        self.profile.save(update_fields=["active"])
        repository = DjangoMonitoringRepository()
        scheduler = DueScheduler(
            MonitoringConfig(concurrency=1, queue_bound=1), FakeClock(NOW),
            current_generation=repository.current_generation, is_eligible=repository.is_eligible,
            confirmation_port=repository, confirmation_policy=ConfirmationPolicy(2, 1, "test-v1"),
            ownership_port=repository, service_instance_id="test-worker",
        )
        attempt = scheduler.tick(NOW, [ScheduleCandidate(self.camera.pk, NOW, 1)]).attempts[0]
        outcome = scheduler.complete(
            attempt.attempt_id, diagnostic.probe_result, NOW, diagnostic=diagnostic, producer_terminated=True,
        )
        self.assertEqual(outcome.disposition, CompletionDisposition.CONFIG_CHANGED)
        self.assertFalse(CameraHealthSnapshot.objects.filter(camera=self.camera).exists())
        self.assertEqual(EstadoMonitoramento.objects.get(camera=self.camera).estado_estavel, TechnicalState.UNKNOWN.value)

    def test_manual_source_cannot_be_persisted_as_automatic_diagnostic(self):
        automatic = self.diagnose()
        manual = ConnectionTestResult(
            automatic.camera_id, automatic.stages, automatic.config_version, automatic.config_generation,
            DiagnosticSource.MANUAL, automatic.correlation_id, automatic.probe_result,
        )
        repository = DjangoMonitoringRepository()
        scheduler = DueScheduler(
            MonitoringConfig(concurrency=1, queue_bound=1), FakeClock(NOW),
            current_generation=repository.current_generation, is_eligible=repository.is_eligible,
            confirmation_port=repository, confirmation_policy=ConfirmationPolicy(2, 1, "test-v1"),
            ownership_port=repository, service_instance_id="test-worker",
        )
        attempt = scheduler.tick(NOW, [ScheduleCandidate(self.camera.pk, NOW, 1)]).attempts[0]
        with self.assertRaises(ValueError):
            scheduler.complete(attempt.attempt_id, manual.probe_result, NOW, diagnostic=manual)
        self.assertFalse(CameraHealthSnapshot.objects.filter(camera=self.camera).exists())

    def test_snapshot_and_online_completion_commit_atomically_with_fencing(self):
        diagnostic = self.diagnose()
        repository = DjangoMonitoringRepository()
        scheduler = DueScheduler(
            MonitoringConfig(concurrency=1, queue_bound=1), FakeClock(NOW),
            current_generation=repository.current_generation, is_eligible=repository.is_eligible,
            confirmation_port=repository, confirmation_policy=ConfirmationPolicy(2, 1, "test-v1"),
            ownership_port=repository, service_instance_id="test-worker",
        )
        attempt = scheduler.tick(NOW, [ScheduleCandidate(self.camera.pk, NOW, 1)]).attempts[0]
        outcome = scheduler.complete(
            attempt.attempt_id, diagnostic.probe_result, NOW, diagnostic=diagnostic, producer_terminated=True,
        )
        self.assertEqual(outcome.disposition, CompletionDisposition.ACCEPTED)
        state = EstadoMonitoramento.objects.get(camera=self.camera)
        snapshot = CameraHealthSnapshot.objects.get(camera=self.camera)
        self.assertEqual(state.estado_estavel, TechnicalState.ONLINE.value)
        self.assertEqual(snapshot.config_generation, 1)
        self.assertEqual(snapshot.correlation_id, diagnostic.correlation_id)
        self.assertEqual(snapshot.stage_d_state, StageStatus.PASS.value)
        self.assertIsNone(state.monitoring_owner_id)

    def test_obsolete_owner_cannot_write_snapshot_or_completion(self):
        diagnostic = self.diagnose()
        repository = DjangoMonitoringRepository()
        candidate = ScheduleCandidate(self.camera.pk, NOW, 1)
        lease = repository.claim(self.camera.pk, "old-worker", 30)
        self.assertIsNotNone(lease)
        state = EstadoMonitoramento.objects.get(camera=self.camera)
        state.monitoring_lease_expires_at = datetime(2000, 1, 1, tzinfo=timezone.utc)
        state.save(update_fields=["monitoring_lease_expires_at"])
        current = repository.claim(self.camera.pk, "new-worker", 30)
        self.assertIsNotNone(current)
        from cameras.monitoramento.confirmation import reduce_confirmation

        memory = repository.load(candidate, ConfirmationPolicy(2, 1, "test-v1"))
        memory, decision = reduce_confirmation(memory, diagnostic.probe_result, ConfirmationPolicy(2, 1, "test-v1"))
        stored = repository.store(
            candidate, diagnostic.probe_result, memory, decision, NOW + timedelta(minutes=5),
            ownership=lease, diagnostic=diagnostic,
        )
        self.assertEqual(stored, CompletionDisposition.OWNERSHIP_LOST)
        self.assertFalse(CameraHealthSnapshot.objects.filter(camera=self.camera).exists())
        self.assertEqual(EstadoMonitoramento.objects.get(camera=self.camera).estado_estavel, TechnicalState.UNKNOWN.value)

    def test_snapshot_rolls_back_when_monitoring_transition_fails(self):
        diagnostic = self.diagnose()

        def fail_transition():
            raise RuntimeError("injected transaction failure")

        repository = DjangoMonitoringRepository(before_transition=fail_transition)
        scheduler = DueScheduler(
            MonitoringConfig(concurrency=1, queue_bound=1), FakeClock(NOW),
            current_generation=repository.current_generation, is_eligible=repository.is_eligible,
            confirmation_port=repository, confirmation_policy=ConfirmationPolicy(2, 1, "test-v1"),
            ownership_port=repository, service_instance_id="test-worker",
        )
        attempt = scheduler.tick(NOW, [ScheduleCandidate(self.camera.pk, NOW, 1)]).attempts[0]
        outcome = scheduler.complete(
            attempt.attempt_id, diagnostic.probe_result, NOW, diagnostic=diagnostic, producer_terminated=True,
        )
        self.assertEqual(outcome.disposition, CompletionDisposition.OPERATIONAL_FAILURE)
        self.assertFalse(CameraHealthSnapshot.objects.filter(camera=self.camera).exists())
        self.assertEqual(EstadoMonitoramento.objects.get(camera=self.camera).estado_estavel, TechnicalState.UNKNOWN.value)

    def test_older_observation_does_not_replace_newer_snapshot(self):
        repository = DjangoMonitoringRepository()
        policy = ConfirmationPolicy(2, 1, "test-v1")
        newer = self.diagnose(at=NOW + timedelta(seconds=10))
        older = self.diagnose(at=NOW)

        def complete(diagnostic, now):
            scheduler = DueScheduler(
                MonitoringConfig(concurrency=1, queue_bound=1), FakeClock(now),
                current_generation=repository.current_generation, is_eligible=repository.is_eligible,
                confirmation_port=repository, confirmation_policy=policy,
                ownership_port=repository, service_instance_id="test-worker",
            )
            attempt = scheduler.tick(now, [ScheduleCandidate(self.camera.pk, now, 1)]).attempts[0]
            return scheduler.complete(attempt.attempt_id, diagnostic.probe_result, now, diagnostic=diagnostic, producer_terminated=True)

        self.assertEqual(complete(newer, NOW + timedelta(seconds=10)).disposition, CompletionDisposition.ACCEPTED)
        self.assertEqual(complete(older, NOW + timedelta(seconds=20)).disposition, CompletionDisposition.ACCEPTED)
        snapshot = CameraHealthSnapshot.objects.get(camera=self.camera)
        self.assertEqual(snapshot.observed_at, newer.observed_at)
        self.assertEqual(snapshot.correlation_id, newer.correlation_id)
