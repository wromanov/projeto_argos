"""Cenários focais da MON-09C: lease persistente e fencing por câmera."""

from datetime import datetime, timedelta, timezone

from django.db import IntegrityError
from django.test import TestCase
from django.utils import timezone as django_timezone

from cameras.models import Camera, EstadoMonitoramento, Indisponibilidade, TransicaoEstadoMonitoramento
from cameras.monitoramento.confirmation import ConfirmationPolicy, TechnicalState
from cameras.monitoramento.contracts import ProbeResult, ProbeResultCode
from cameras.monitoramento.fakes import FakeClock
from cameras.monitoramento.repository import DjangoMonitoringRepository
from cameras.monitoramento.scheduler import DueScheduler
from cameras.monitoramento.schemas import CompletionDisposition, MonitoringConfig, ScheduleCandidate, SchedulerLifecycle


START = datetime(2026, 1, 1, tzinfo=timezone.utc)
POLICY = ConfirmationPolicy(failures_to_offline=2, successes_to_online=1, version="mon09c-v1")


class FailingClaimRepository(DjangoMonitoringRepository):
    def claim(self, camera_id, owner_id, lease_seconds):
        raise IntegrityError("forced claim failure")


class MonitoringOwnershipFencingTests(TestCase):
    def camera(self, suffix: int = 1) -> Camera:
        return Camera.objects.create(
            nome=f"CAM-{suffix}", fabricante="FAB", modelo="MOD", serial=f"SER-{suffix}",
            mac=f"00:11:22:33:44:{suffix:02X}", tipo=Camera.TipoCamera.BULLET,
            terminal="T", pavimento="P", setor="S", ambiente="A", ip=f"10.0.0.{suffix + 1}",
            mascara_subrede="255.255.255.0", gateway="10.0.0.1", vlan=10, farm="F",
            retencao_esperada_dias=1, codec="H264",
        )

    @staticmethod
    def candidate(camera: Camera, at: datetime = START) -> ScheduleCandidate:
        return ScheduleCandidate(camera.pk, at, config_generation=1)

    @staticmethod
    def result(code: ProbeResultCode = ProbeResultCode.SUCCESS, at: datetime = START) -> ProbeResult:
        return ProbeResult(code=code, observed_at=at, duration_seconds=0)

    @staticmethod
    def expire(camera: Camera) -> None:
        EstadoMonitoramento.objects.filter(camera=camera).update(
            monitoring_lease_expires_at=django_timezone.now() - timedelta(seconds=1)
        )

    def scheduler(self, repository: DjangoMonitoringRepository, *, service: str, at: datetime = START) -> DueScheduler:
        return DueScheduler(
            MonitoringConfig(concurrency=1, queue_bound=1, ownership_lease_seconds=30),
            FakeClock(at),
            current_generation=repository.current_generation,
            is_eligible=repository.is_eligible,
            confirmation_port=repository,
            confirmation_policy=POLICY,
            ownership_port=repository,
            service_instance_id=service,
        )

    def test_claim_has_single_winner_and_epoch_is_monotonic_after_expiry(self):
        camera = self.camera()
        repository = DjangoMonitoringRepository()

        owner_a = repository.claim(camera.pk, "worker-a:runtime-a", 30)
        owner_b_denied = repository.claim(camera.pk, "worker-b:runtime-b", 30)
        self.expire(camera)
        owner_b = repository.claim(camera.pk, "worker-b:runtime-b", 30)

        self.assertIsNotNone(owner_a)
        self.assertIsNone(owner_b_denied)
        self.assertIsNotNone(owner_b)
        self.assertGreater(owner_b.epoch, owner_a.epoch)
        state = EstadoMonitoramento.objects.get(camera=camera)
        self.assertEqual(state.monitoring_owner_id, owner_b.owner_id)
        self.assertEqual(state.monitoring_ownership_epoch, owner_b.epoch)

    def test_valid_completion_applies_domain_effect_and_releases_lease_atomically(self):
        camera = self.camera()
        repository = DjangoMonitoringRepository()
        scheduler = self.scheduler(repository, service="worker-a")
        attempt = scheduler.tick(START, [self.candidate(camera)]).attempts[0]

        outcome = scheduler.complete(attempt.attempt_id, self.result(), START, producer_terminated=True)

        state = EstadoMonitoramento.objects.get(camera=camera)
        self.assertEqual(outcome.disposition, CompletionDisposition.ACCEPTED)
        self.assertEqual(state.estado_estavel, TechnicalState.ONLINE.value)
        self.assertIsNone(state.monitoring_owner_id)
        self.assertIsNone(state.monitoring_lease_expires_at)
        self.assertEqual(state.monitoring_ownership_epoch, attempt.ownership.epoch)
        self.assertEqual(TransicaoEstadoMonitoramento.objects.count(), 1)

    def test_expired_lease_without_takeover_accepts_current_owner_completion(self):
        camera = self.camera()
        repository = DjangoMonitoringRepository()
        scheduler = self.scheduler(repository, service="worker-a")
        attempt = scheduler.tick(START, [self.candidate(camera)]).attempts[0]
        self.expire(camera)

        outcome = scheduler.complete(attempt.attempt_id, self.result(), START, producer_terminated=True)

        state = EstadoMonitoramento.objects.get(camera=camera)
        self.assertEqual(outcome.disposition, CompletionDisposition.ACCEPTED)
        self.assertEqual(state.estado_estavel, TechnicalState.ONLINE.value)
        self.assertIsNone(state.monitoring_owner_id)
        self.assertIsNone(state.monitoring_lease_expires_at)
        self.assertEqual(state.monitoring_ownership_epoch, attempt.ownership.epoch)
        self.assertEqual(TransicaoEstadoMonitoramento.objects.count(), 1)

    def test_stale_owner_completion_after_takeover_has_no_domain_side_effect(self):
        camera = self.camera()
        repository = DjangoMonitoringRepository()
        scheduler_a = self.scheduler(repository, service="worker-a")
        attempt_a = scheduler_a.tick(START, [self.candidate(camera)]).attempts[0]
        self.expire(camera)
        owner_b = repository.claim(camera.pk, "worker-b:runtime-b", 30)

        outcome = scheduler_a.complete(attempt_a.attempt_id, self.result(), START, producer_terminated=True)

        state = EstadoMonitoramento.objects.get(camera=camera)
        self.assertEqual(outcome.disposition, CompletionDisposition.OWNERSHIP_LOST)
        self.assertEqual(state.estado_estavel, TechnicalState.UNKNOWN.value)
        self.assertIsNone(state.ultima_evidencia_util_em)
        self.assertIsNone(state.proximo_vencimento_em)
        self.assertEqual(state.monitoring_owner_id, owner_b.owner_id)
        self.assertEqual(state.monitoring_ownership_epoch, owner_b.epoch)
        self.assertEqual((state.sequencia_positiva, state.sequencia_negativa), (0, 0))
        self.assertEqual(TransicaoEstadoMonitoramento.objects.count(), 0)
        self.assertEqual(Indisponibilidade.objects.count(), 0)

    def test_new_owner_completion_after_takeover_is_accepted(self):
        camera = self.camera()
        repository = DjangoMonitoringRepository()
        scheduler_a = self.scheduler(repository, service="worker-a")
        attempt_a = scheduler_a.tick(START, [self.candidate(camera)]).attempts[0]
        self.expire(camera)
        scheduler_b = self.scheduler(repository, service="worker-b")
        attempt_b = scheduler_b.tick(START, [self.candidate(camera)]).attempts[0]

        stale = scheduler_a.complete(attempt_a.attempt_id, self.result(), START, producer_terminated=True)
        accepted = scheduler_b.complete(attempt_b.attempt_id, self.result(), START, producer_terminated=True)

        state = EstadoMonitoramento.objects.get(camera=camera)
        self.assertEqual(stale.disposition, CompletionDisposition.OWNERSHIP_LOST)
        self.assertEqual(accepted.disposition, CompletionDisposition.ACCEPTED)
        self.assertEqual(state.estado_estavel, TechnicalState.ONLINE.value)
        self.assertIsNone(state.monitoring_owner_id)
        self.assertEqual(state.monitoring_ownership_epoch, attempt_b.ownership.epoch)
        self.assertEqual(TransicaoEstadoMonitoramento.objects.count(), 1)

    def test_config_generation_and_fencing_must_both_be_current(self):
        camera = self.camera()
        repository = DjangoMonitoringRepository()
        scheduler = self.scheduler(repository, service="worker-a")
        config_stale = scheduler.tick(START, [self.candidate(camera)]).attempts[0]
        EstadoMonitoramento.objects.filter(camera=camera).update(ultima_geracao_configuracao=2)

        config_outcome = scheduler.complete(config_stale.attempt_id, self.result(), START, producer_terminated=True)
        self.assertEqual(config_outcome.disposition, CompletionDisposition.CONFIG_CHANGED)
        self.assertEqual(TransicaoEstadoMonitoramento.objects.count(), 0)

        EstadoMonitoramento.objects.filter(camera=camera).update(ultima_geracao_configuracao=1)
        scheduler = self.scheduler(repository, service="worker-a")
        ownership_stale = scheduler.tick(START, [self.candidate(camera)]).attempts[0]
        self.expire(camera)
        repository.claim(camera.pk, "worker-b:runtime-b", 30)

        ownership_outcome = scheduler.complete(ownership_stale.attempt_id, self.result(), START, producer_terminated=True)
        self.assertEqual(ownership_outcome.disposition, CompletionDisposition.OWNERSHIP_LOST)
        self.assertEqual(TransicaoEstadoMonitoramento.objects.count(), 0)

        self.expire(camera)
        scheduler = self.scheduler(repository, service="worker-c")
        valid = scheduler.tick(START, [self.candidate(camera)]).attempts[0]
        accepted = scheduler.complete(valid.attempt_id, self.result(), START, producer_terminated=True)
        self.assertEqual(accepted.disposition, CompletionDisposition.ACCEPTED)
        self.assertEqual(TransicaoEstadoMonitoramento.objects.count(), 1)

    def test_crash_expiry_and_takeover_do_not_create_offline_or_outage(self):
        camera = self.camera()
        repository = DjangoMonitoringRepository()
        owner_a = repository.claim(camera.pk, "worker-a:runtime-a", 30)
        self.expire(camera)
        owner_b = repository.claim(camera.pk, "worker-b:runtime-b", 30)

        state = EstadoMonitoramento.objects.get(camera=camera)
        self.assertGreater(owner_b.epoch, owner_a.epoch)
        self.assertEqual(state.estado_estavel, TechnicalState.UNKNOWN.value)
        self.assertIsNone(state.ultima_evidencia_util_em)
        self.assertEqual(TransicaoEstadoMonitoramento.objects.count(), 0)
        self.assertEqual(Indisponibilidade.objects.count(), 0)

    def test_cancelled_old_owner_cannot_release_current_owner_or_create_evidence(self):
        camera = self.camera()
        repository = DjangoMonitoringRepository()
        scheduler = self.scheduler(repository, service="worker-a")
        attempt = scheduler.tick(START, [self.candidate(camera)]).attempts[0]
        self.expire(camera)
        owner_b = repository.claim(camera.pk, "worker-b:runtime-b", 30)

        outcome = scheduler.cancel(attempt.attempt_id, producer_terminated=True)

        state = EstadoMonitoramento.objects.get(camera=camera)
        self.assertEqual(outcome.disposition, CompletionDisposition.CANCELLED)
        self.assertEqual(state.monitoring_owner_id, owner_b.owner_id)
        self.assertEqual(state.monitoring_ownership_epoch, owner_b.epoch)
        self.assertIsNone(state.ultima_evidencia_util_em)
        self.assertEqual(TransicaoEstadoMonitoramento.objects.count(), 0)
        self.assertEqual(Indisponibilidade.objects.count(), 0)

    def test_claim_database_failure_starts_no_attempt(self):
        camera = self.camera()
        repository = FailingClaimRepository()
        scheduler = self.scheduler(repository, service="worker-a")

        report = scheduler.tick(START, [self.candidate(camera)])

        self.assertEqual(report.attempts, ())
        self.assertEqual(scheduler.active_count, 0)
        self.assertEqual(scheduler.lifecycle, SchedulerLifecycle.DEGRADED)
        self.assertFalse(EstadoMonitoramento.objects.filter(camera=camera).exists())

    def test_completion_database_failure_rolls_back_domain_and_lease_commit(self):
        camera = self.camera()
        repository = DjangoMonitoringRepository(
            before_transition=lambda: (_ for _ in ()).throw(IntegrityError("forced completion failure"))
        )
        scheduler = self.scheduler(repository, service="worker-a")
        attempt = scheduler.tick(START, [self.candidate(camera)]).attempts[0]

        outcome = scheduler.complete(attempt.attempt_id, self.result(), START, producer_terminated=True)

        state = EstadoMonitoramento.objects.get(camera=camera)
        self.assertEqual(outcome.disposition, CompletionDisposition.OPERATIONAL_FAILURE)
        self.assertEqual(state.estado_estavel, TechnicalState.UNKNOWN.value)
        self.assertIsNone(state.ultima_evidencia_util_em)
        self.assertEqual(state.monitoring_owner_id, attempt.ownership.owner_id)
        self.assertEqual(scheduler.active_count, 1)
        self.assertEqual(TransicaoEstadoMonitoramento.objects.count(), 0)
        self.assertEqual(Indisponibilidade.objects.count(), 0)
