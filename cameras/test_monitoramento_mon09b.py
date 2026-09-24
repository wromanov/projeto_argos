"""Cenários focais da MON-09B: falhas operacionais e recuperação."""

from datetime import datetime, timedelta, timezone

from django.db import IntegrityError
from django.test import TestCase

from cameras.models import Camera, EstadoMonitoramento, Indisponibilidade, TransicaoEstadoMonitoramento
from cameras.monitoramento.confirmation import (
    ConfirmationMemory,
    ConfirmationPolicy,
    TechnicalDecisionAction,
    TechnicalDecisionReason,
    TechnicalState,
    reduce_confirmation,
)
from cameras.monitoramento.contracts import ProbeResult, ProbeResultCode
from cameras.monitoramento.fakes import FakeClock
from cameras.monitoramento.repository import DjangoMonitoringRepository
from cameras.monitoramento.scheduler import DueScheduler
from cameras.monitoramento.schemas import CompletionDisposition, MonitoringConfig, ScheduleCandidate, SchedulerLifecycle


START = datetime(2026, 1, 1, tzinfo=timezone.utc)
POLICY = ConfirmationPolicy(failures_to_offline=2, successes_to_online=1, version="mon09b-v1")


class MonitoringOperationalFailureTests(TestCase):
    def camera(self, suffix: int = 1) -> Camera:
        return Camera.objects.create(
            nome=f"CAM-{suffix}",
            fabricante="FAB",
            modelo="MOD",
            serial=f"SER-{suffix}",
            mac=f"00:11:22:33:44:{suffix:02X}",
            tipo=Camera.TipoCamera.BULLET,
            terminal="T",
            pavimento="P",
            setor="S",
            ambiente="A",
            ip=f"10.0.0.{suffix + 1}",
            mascara_subrede="255.255.255.0",
            gateway="10.0.0.1",
            vlan=10,
            farm="F",
            retencao_esperada_dias=1,
            codec="H264",
        )

    @staticmethod
    def candidate(camera: Camera, due_at: datetime) -> ScheduleCandidate:
        return ScheduleCandidate(camera.pk, due_at, config_generation=1)

    @staticmethod
    def result(code: ProbeResultCode, observed_at: datetime) -> ProbeResult:
        return ProbeResult(code=code, observed_at=observed_at, duration_seconds=0)

    def scheduler(self, repository: DjangoMonitoringRepository, at: datetime = START) -> DueScheduler:
        return DueScheduler(
            MonitoringConfig(concurrency=1, queue_bound=1),
            FakeClock(at),
            current_generation=repository.current_generation,
            is_eligible=repository.is_eligible,
            confirmation_port=repository,
            confirmation_policy=POLICY,
        )

    def test_timeout_and_connection_failure_follow_the_existing_negative_evidence_contract(self):
        memory = ConfirmationMemory.initial(POLICY.version)
        first, decision = reduce_confirmation(
            memory, self.result(ProbeResultCode.TIMEOUT, START), POLICY
        )
        self.assertEqual(decision.action, TechnicalDecisionAction.NO_CHANGE)
        self.assertEqual(decision.reason, TechnicalDecisionReason.NEGATIVE_EVIDENCE)
        self.assertEqual(first.state, TechnicalState.UNKNOWN)
        self.assertEqual(first.negative_streak, 1)

        second, decision = reduce_confirmation(
            first,
            self.result(ProbeResultCode.CONNECTION_REFUSED, START + timedelta(seconds=1)),
            POLICY,
        )
        self.assertEqual(decision.action, TechnicalDecisionAction.CONFIRM_OFFLINE)
        self.assertEqual(decision.reason, TechnicalDecisionReason.CONFIRMED_OFFLINE)
        self.assertEqual(second.state, TechnicalState.OFFLINE)
        self.assertEqual(second.negative_streak, 0)

    def test_cancelled_completion_does_not_change_persisted_state_or_history(self):
        camera = self.camera()
        EstadoMonitoramento.objects.create(
            camera=camera,
            estado_estavel=TechnicalState.ONLINE.value,
            em_escopo=True,
            versao_politica_confirmacao=POLICY.version,
            sequencia_negativa=1,
            confirmacao_ultima_observacao_em=START,
            ultima_evidencia_util_em=START,
            ultima_geracao_configuracao=1,
        )
        repository = DjangoMonitoringRepository()
        scheduler = self.scheduler(repository, START + timedelta(seconds=1))
        attempt = scheduler.tick(
            START + timedelta(seconds=1),
            [self.candidate(camera, START + timedelta(seconds=1))],
        ).attempts[0]

        outcome = scheduler.complete(
            attempt.attempt_id,
            self.result(ProbeResultCode.CANCELLED, START + timedelta(seconds=1)),
            START + timedelta(seconds=1),
        )

        state = EstadoMonitoramento.objects.get(camera=camera)
        self.assertEqual(outcome.disposition, CompletionDisposition.CANCELLED)
        self.assertEqual(state.estado_estavel, TechnicalState.ONLINE.value)
        self.assertEqual(state.sequencia_negativa, 1)
        self.assertEqual(state.confirmacao_ultima_observacao_em, START)
        self.assertEqual(state.ultima_evidencia_util_em, START)
        self.assertEqual(TransicaoEstadoMonitoramento.objects.count(), 0)
        self.assertEqual(Indisponibilidade.objects.count(), 0)

    def test_database_failure_rolls_back_and_allows_a_new_execution_to_recover(self):
        camera = self.camera()
        repository = DjangoMonitoringRepository()
        initial_scheduler = self.scheduler(repository)
        initial_attempt = initial_scheduler.tick(START, [self.candidate(camera, START)]).attempts[0]
        initial = initial_scheduler.complete(
            initial_attempt.attempt_id,
            self.result(ProbeResultCode.SUCCESS, START),
            START,
        )
        self.assertEqual(initial.disposition, CompletionDisposition.ACCEPTED)

        fail_once = {"enabled": True}

        def fail_transition_once() -> None:
            if fail_once["enabled"]:
                fail_once["enabled"] = False
                raise IntegrityError("forced operational failure")

        failing_repository = DjangoMonitoringRepository(before_transition=fail_transition_once)
        scheduler = self.scheduler(failing_repository, initial.next_due_at)
        first_attempt = scheduler.tick(
            initial.next_due_at,
            [self.candidate(camera, initial.next_due_at)],
        ).attempts[0]
        first_failure = scheduler.complete(
            first_attempt.attempt_id,
            self.result(ProbeResultCode.TIMEOUT, initial.next_due_at),
            initial.next_due_at,
        )
        self.assertEqual(first_failure.disposition, CompletionDisposition.ACCEPTED)

        state = EstadoMonitoramento.objects.get(camera=camera)
        self.assertEqual(state.estado_estavel, TechnicalState.ONLINE.value)
        self.assertEqual(state.sequencia_negativa, 1)

        failed_at = first_failure.next_due_at
        second_attempt = scheduler.tick(
            failed_at,
            [self.candidate(camera, failed_at)],
        ).attempts[0]
        operational_failure = scheduler.complete(
            second_attempt.attempt_id,
            self.result(ProbeResultCode.TIMEOUT, failed_at),
            failed_at,
        )

        state.refresh_from_db()
        self.assertEqual(operational_failure.disposition, CompletionDisposition.OPERATIONAL_FAILURE)
        self.assertEqual(state.estado_estavel, TechnicalState.ONLINE.value)
        self.assertEqual(state.sequencia_negativa, 1)
        self.assertEqual(TransicaoEstadoMonitoramento.objects.count(), 1)
        self.assertEqual(Indisponibilidade.objects.count(), 0)

        self.assertEqual(scheduler.start(), SchedulerLifecycle.RUNNING)
        recovery_at = failed_at + timedelta(seconds=1)
        recovery_attempts = scheduler.tick(
            recovery_at,
            [self.candidate(camera, failed_at)],
        ).attempts
        recovery = scheduler.complete(
            recovery_attempts[0].attempt_id,
            self.result(ProbeResultCode.SUCCESS, recovery_at),
            recovery_at,
        )

        state.refresh_from_db()
        self.assertEqual(recovery.disposition, CompletionDisposition.ACCEPTED)
        self.assertEqual(state.estado_estavel, TechnicalState.ONLINE.value)
        self.assertEqual(state.sequencia_negativa, 0)
        self.assertEqual(TransicaoEstadoMonitoramento.objects.count(), 1)
        self.assertEqual(Indisponibilidade.objects.count(), 0)
