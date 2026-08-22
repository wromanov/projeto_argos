from datetime import datetime, timedelta, timezone
from unittest.mock import patch

from django.db import IntegrityError
from django.test import TestCase

from cameras.models import (
    Camera,
    EstadoMonitoramento,
    EventoAuditoria,
    Indisponibilidade,
    TransicaoEstadoMonitoramento,
)
from cameras.monitoramento.confirmation import ConfirmationPolicy, TechnicalState
from cameras.monitoramento.contracts import ProbeResult, ProbeResultCode
from cameras.monitoramento.fakes import FakeClock
from cameras.monitoramento.repository import DjangoMonitoringRepository
from cameras.monitoramento.scheduler import DueScheduler
from cameras.monitoramento.schemas import CompletionDisposition, MonitoringConfig, ScheduleCandidate


START = datetime(2026, 1, 1, tzinfo=timezone.utc)
POLICY = ConfirmationPolicy(failures_to_offline=2, successes_to_online=1, version="mon06c-v1")


class MonitoringUnavailabilityIntegrationTests(TestCase):
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

    def result(self, code: ProbeResultCode, at: datetime) -> ProbeResult:
        return ProbeResult(code=code, observed_at=at, duration_seconds=0)

    def candidate(self, camera: Camera, at: datetime) -> ScheduleCandidate:
        return ScheduleCandidate(camera.pk, at, config_generation=1)

    def scheduler(self, repository: DjangoMonitoringRepository, at: datetime = START) -> DueScheduler:
        return DueScheduler(
            MonitoringConfig(concurrency=1, queue_bound=1),
            FakeClock(at),
            current_generation=repository.current_generation,
            is_eligible=repository.is_eligible,
            confirmation_port=repository,
            confirmation_policy=POLICY,
        )

    def complete(
        self,
        camera: Camera,
        code: ProbeResultCode,
        at: datetime,
        repository: DjangoMonitoringRepository | None = None,
    ):
        repository = repository or DjangoMonitoringRepository()
        scheduler = self.scheduler(repository, at)
        attempt = scheduler.tick(at, [self.candidate(camera, at)]).attempts[0]
        return scheduler.complete(attempt.attempt_id, self.result(code, at), at), repository

    def bring_offline(self, camera: Camera, start: datetime = START, repository=None):
        repository = repository or DjangoMonitoringRepository()
        self.complete(camera, ProbeResultCode.TIMEOUT, start, repository)
        return self.complete(camera, ProbeResultCode.TIMEOUT, start + timedelta(seconds=1), repository)

    def test_unknown_to_offline_opens_initial_interval_with_canonical_timestamp(self):
        camera = self.camera()
        self.bring_offline(camera)

        state = EstadoMonitoramento.objects.get(camera=camera)
        transition = TransicaoEstadoMonitoramento.objects.get(camera=camera)
        interval = Indisponibilidade.objects.get(camera=camera)
        self.assertEqual(state.estado_estavel, TechnicalState.OFFLINE.value)
        self.assertEqual((transition.estado_anterior, transition.estado_atual), ("UNKNOWN", "OFFLINE"))
        self.assertEqual(transition.ocorrida_em, START + timedelta(seconds=1))
        self.assertEqual(interval.open_origin, Indisponibilidade.OrigemAbertura.INITIAL_OFFLINE)
        self.assertEqual(interval.opened_at, transition.ocorrida_em)
        self.assertEqual(interval.opening_transition_id, transition.pk)
        self.assertEqual(interval.camera_id, transition.camera_id)

    def test_online_to_offline_opens_online_to_offline_interval(self):
        camera = self.camera()
        repository = DjangoMonitoringRepository()
        self.complete(camera, ProbeResultCode.SUCCESS, START, repository)
        self.complete(camera, ProbeResultCode.TIMEOUT, START + timedelta(seconds=1), repository)
        self.bring_offline(camera, START + timedelta(seconds=2), repository)

        transition = TransicaoEstadoMonitoramento.objects.get(
            camera=camera, estado_anterior="ONLINE", estado_atual="OFFLINE"
        )
        interval = Indisponibilidade.objects.get(camera=camera)
        self.assertEqual(interval.open_origin, Indisponibilidade.OrigemAbertura.ONLINE_TO_OFFLINE)
        self.assertEqual(interval.opened_at, START + timedelta(seconds=2))
        self.assertEqual(interval.opening_transition_id, transition.pk)

    def test_offline_repeated_does_not_restart_or_duplicate_interval(self):
        camera = self.camera()
        repository = DjangoMonitoringRepository()
        self.bring_offline(camera, repository=repository)
        interval = Indisponibilidade.objects.get(camera=camera)
        transition_count = TransicaoEstadoMonitoramento.objects.count()

        outcome, _ = self.complete(camera, ProbeResultCode.TIMEOUT, START + timedelta(seconds=2), repository)

        interval.refresh_from_db()
        self.assertEqual(outcome.disposition, CompletionDisposition.ACCEPTED)
        self.assertEqual(Indisponibilidade.objects.get(camera=camera).pk, interval.pk)
        self.assertEqual(interval.opened_at, START + timedelta(seconds=1))
        self.assertEqual(TransicaoEstadoMonitoramento.objects.count(), transition_count)

    def test_offline_to_online_closes_with_recovery_transition_and_timestamp(self):
        camera = self.camera()
        repository = DjangoMonitoringRepository()
        self.bring_offline(camera, repository=repository)
        recovery_at = START + timedelta(seconds=2)
        self.complete(camera, ProbeResultCode.SUCCESS, recovery_at, repository)

        interval = Indisponibilidade.objects.get(camera=camera)
        transition = TransicaoEstadoMonitoramento.objects.get(
            camera=camera, estado_anterior="OFFLINE", estado_atual="ONLINE"
        )
        self.assertEqual(interval.close_reason, Indisponibilidade.MotivoFechamento.RECUPERADA)
        self.assertEqual(interval.closed_at, recovery_at)
        self.assertEqual(interval.closing_transition_id, transition.pk)
        self.assertEqual(interval.camera_id, transition.camera_id)
        self.assertEqual(interval.closed_at - interval.opened_at, timedelta(seconds=1))

    def test_repeated_online_does_not_create_history(self):
        camera = self.camera()
        repository = DjangoMonitoringRepository()
        self.complete(camera, ProbeResultCode.SUCCESS, START, repository)
        count = TransicaoEstadoMonitoramento.objects.count()
        self.complete(camera, ProbeResultCode.SUCCESS, START + timedelta(seconds=1), repository)
        self.assertEqual(TransicaoEstadoMonitoramento.objects.count(), count)
        self.assertFalse(Indisponibilidade.objects.filter(camera=camera).exists())

    def test_leave_scope_offline_closes_without_closing_transition(self):
        camera = self.camera()
        repository = DjangoMonitoringRepository()
        self.bring_offline(camera, repository=repository)
        occurred_at = START + timedelta(seconds=2)

        repository.leave_scope(camera.pk, occurred_at)

        state = EstadoMonitoramento.objects.get(camera=camera)
        interval = Indisponibilidade.objects.get(camera=camera)
        self.assertFalse(state.em_escopo)
        self.assertEqual(interval.close_reason, Indisponibilidade.MotivoFechamento.SAIU_DO_ESCOPO)
        self.assertEqual(interval.closed_at, occurred_at)
        self.assertIsNone(interval.closing_transition_id)
        self.assertEqual(TransicaoEstadoMonitoramento.objects.count(), 1)

    def test_leave_scope_without_open_interval_only_marks_out_of_scope(self):
        camera = self.camera()
        repository = DjangoMonitoringRepository()
        self.complete(camera, ProbeResultCode.SUCCESS, START, repository)

        repository.leave_scope(camera.pk, START + timedelta(seconds=1))

        state = EstadoMonitoramento.objects.get(camera=camera)
        self.assertFalse(state.em_escopo)
        self.assertFalse(Indisponibilidade.objects.filter(camera=camera).exists())
        self.assertEqual(TransicaoEstadoMonitoramento.objects.count(), 1)

    def test_leave_scope_unknown_without_state_is_valid_and_creates_no_history(self):
        camera = self.camera()
        DjangoMonitoringRepository().leave_scope(camera.pk, START)

        state = EstadoMonitoramento.objects.get(camera=camera)
        self.assertFalse(state.em_escopo)
        self.assertEqual(state.estado_estavel, TechnicalState.UNKNOWN.value)
        self.assertFalse(Indisponibilidade.objects.filter(camera=camera).exists())
        self.assertFalse(TransicaoEstadoMonitoramento.objects.filter(camera=camera).exists())

    def test_leave_scope_is_idempotent_and_keeps_first_close_timestamp(self):
        camera = self.camera()
        repository = DjangoMonitoringRepository()
        self.bring_offline(camera, repository=repository)
        first_at = START + timedelta(seconds=2)
        repository.leave_scope(camera.pk, first_at)
        interval = Indisponibilidade.objects.get(camera=camera)

        repository.leave_scope(camera.pk, START + timedelta(seconds=20))

        interval.refresh_from_db()
        self.assertEqual(interval.closed_at, first_at)
        self.assertEqual(interval.close_reason, Indisponibilidade.MotivoFechamento.SAIU_DO_ESCOPO)
        self.assertEqual(Indisponibilidade.objects.filter(camera=camera).count(), 1)
        self.assertEqual(TransicaoEstadoMonitoramento.objects.filter(camera=camera).count(), 1)

    def test_return_to_scope_does_not_open_and_later_offline_opens_new_interval(self):
        camera = self.camera()
        repository = DjangoMonitoringRepository()
        self.bring_offline(camera, repository=repository)
        repository.leave_scope(camera.pk, START + timedelta(seconds=2))
        previous = Indisponibilidade.objects.get(camera=camera)

        repository.enter_scope(camera.pk, START + timedelta(seconds=3))
        state = EstadoMonitoramento.objects.get(camera=camera)
        self.assertTrue(state.em_escopo)
        self.assertEqual(state.estado_estavel, TechnicalState.UNKNOWN.value)
        self.assertEqual(Indisponibilidade.objects.count(), 1)

        self.bring_offline(camera, START + timedelta(seconds=4), repository)

        intervals = list(Indisponibilidade.objects.filter(camera=camera).order_by("opened_at"))
        self.assertEqual(len(intervals), 2)
        self.assertEqual(intervals[0].pk, previous.pk)
        self.assertIsNotNone(intervals[0].closed_at)
        self.assertEqual(intervals[1].open_origin, Indisponibilidade.OrigemAbertura.INITIAL_OFFLINE)
        self.assertEqual(intervals[1].opened_at, START + timedelta(seconds=5))

    def test_stale_suspect_and_neutral_results_do_not_change_history(self):
        camera = self.camera()
        repository = DjangoMonitoringRepository()
        first, _ = self.complete(camera, ProbeResultCode.TIMEOUT, START, repository)
        state = EstadoMonitoramento.objects.get(camera=camera)
        self.assertEqual(state.estado_estavel, TechnicalState.UNKNOWN.value)
        self.assertEqual(state.sequencia_negativa, 1)
        self.assertFalse(Indisponibilidade.objects.exists())

        self.complete(camera, ProbeResultCode.AUTH_FAILURE, START + timedelta(seconds=1), repository)
        state.refresh_from_db()
        self.assertEqual(state.estado_estavel, TechnicalState.UNKNOWN.value)
        self.assertTrue(first.next_due_at > START)
        self.assertFalse(Indisponibilidade.objects.exists())

    def test_discarded_completion_does_not_open_or_close_history(self):
        camera = self.camera()
        repository = DjangoMonitoringRepository()
        self.bring_offline(camera, repository=repository)
        interval = Indisponibilidade.objects.get(camera=camera)
        scheduler = self.scheduler(repository, START + timedelta(seconds=2))
        attempt = scheduler.tick(
            START + timedelta(seconds=2), [self.candidate(camera, START + timedelta(seconds=2))]
        ).attempts[0]
        EstadoMonitoramento.objects.filter(camera=camera).update(ultima_geracao_configuracao=2)

        outcome = scheduler.complete(
            attempt.attempt_id,
            self.result(ProbeResultCode.SUCCESS, START + timedelta(seconds=2)),
            START + timedelta(seconds=2),
        )

        interval.refresh_from_db()
        self.assertEqual(outcome.disposition, CompletionDisposition.CONFIG_CHANGED)
        self.assertIsNone(interval.closed_at)
        self.assertEqual(TransicaoEstadoMonitoramento.objects.filter(camera=camera).count(), 1)

    def test_restart_reuses_existing_open_interval_without_duplication(self):
        camera = self.camera()
        repository = DjangoMonitoringRepository()
        self.bring_offline(camera, repository=repository)
        original = Indisponibilidade.objects.get(camera=camera)
        fresh_repository = DjangoMonitoringRepository()

        memory = fresh_repository.load(self.candidate(camera, START + timedelta(seconds=2)), POLICY)
        self.assertEqual(memory.state, TechnicalState.OFFLINE)
        self.complete(camera, ProbeResultCode.TIMEOUT, START + timedelta(seconds=2), fresh_repository)

        interval = Indisponibilidade.objects.get(camera=camera)
        self.assertEqual(interval.pk, original.pk)
        self.assertEqual(interval.opened_at, original.opened_at)
        self.assertEqual(Indisponibilidade.objects.filter(camera=camera, closed_at__isnull=True).count(), 1)

    def test_opening_failure_rolls_back_state_memory_evidence_due_transition_and_interval(self):
        camera = self.camera()
        repository = DjangoMonitoringRepository()
        first, _ = self.complete(camera, ProbeResultCode.TIMEOUT, START, repository)
        before = EstadoMonitoramento.objects.get(camera=camera)

        with patch.object(Indisponibilidade.objects, "create", side_effect=IntegrityError("forced opening failure")):
            outcome, _ = self.complete(camera, ProbeResultCode.TIMEOUT, START + timedelta(seconds=1), repository)

        after = EstadoMonitoramento.objects.get(camera=camera)
        self.assertEqual(outcome.disposition, CompletionDisposition.OPERATIONAL_FAILURE)
        self.assertEqual(after.estado_estavel, before.estado_estavel)
        self.assertEqual(after.sequencia_negativa, before.sequencia_negativa)
        self.assertEqual(after.ultima_evidencia_util_em, before.ultima_evidencia_util_em)
        self.assertEqual(after.proximo_vencimento_em, before.proximo_vencimento_em)
        self.assertEqual(TransicaoEstadoMonitoramento.objects.count(), 0)
        self.assertFalse(Indisponibilidade.objects.exists())
        self.assertEqual(first.next_due_at, before.proximo_vencimento_em)

    def test_closing_failure_rolls_back_recovery_state_transition_and_interval(self):
        camera = self.camera()
        repository = DjangoMonitoringRepository()
        self.bring_offline(camera, repository=repository)
        interval = Indisponibilidade.objects.get(camera=camera)

        with patch.object(Indisponibilidade, "save", side_effect=IntegrityError("forced closing failure")):
            outcome, _ = self.complete(camera, ProbeResultCode.SUCCESS, START + timedelta(seconds=2), repository)

        state = EstadoMonitoramento.objects.get(camera=camera)
        interval.refresh_from_db()
        self.assertEqual(outcome.disposition, CompletionDisposition.OPERATIONAL_FAILURE)
        self.assertEqual(state.estado_estavel, TechnicalState.OFFLINE.value)
        self.assertIsNone(interval.closed_at)
        self.assertIsNone(interval.close_reason)
        self.assertIsNone(interval.closing_transition_id)
        self.assertEqual(TransicaoEstadoMonitoramento.objects.count(), 1)

    def test_scope_close_failure_rolls_back_scope_flag_and_interval(self):
        camera = self.camera()
        repository = DjangoMonitoringRepository()
        self.bring_offline(camera, repository=repository)
        interval = Indisponibilidade.objects.get(camera=camera)

        with patch.object(Indisponibilidade, "save", side_effect=IntegrityError("forced scope failure")):
            with self.assertRaises(IntegrityError):
                repository.leave_scope(camera.pk, START + timedelta(seconds=2))

        state = EstadoMonitoramento.objects.get(camera=camera)
        interval.refresh_from_db()
        self.assertTrue(state.em_escopo)
        self.assertIsNone(interval.closed_at)
        self.assertIsNone(interval.close_reason)

    def test_cross_table_camera_mismatch_is_rejected_and_rolled_back(self):
        camera_a = self.camera(1)
        camera_b = self.camera(2)
        foreign_transition = TransicaoEstadoMonitoramento.objects.create(
            camera=camera_b,
            estado_anterior="UNKNOWN",
            estado_atual="ONLINE",
            ocorrida_em=START,
        )
        repository = DjangoMonitoringRepository()

        with patch.object(TransicaoEstadoMonitoramento.objects, "create", return_value=foreign_transition):
            outcome, _ = self.complete(camera_a, ProbeResultCode.SUCCESS, START, repository)

        self.assertEqual(outcome.disposition, CompletionDisposition.OPERATIONAL_FAILURE)
        self.assertFalse(EstadoMonitoramento.objects.filter(camera=camera_a).exists())
        self.assertFalse(Indisponibilidade.objects.filter(camera=camera_a).exists())
        self.assertEqual(TransicaoEstadoMonitoramento.objects.filter(camera=camera_a).count(), 0)
        self.assertEqual(TransicaoEstadoMonitoramento.objects.filter(camera=camera_b).count(), 1)

    def test_leave_scope_requires_explicit_aware_timestamp(self):
        camera = self.camera()
        repository = DjangoMonitoringRepository()

        with self.assertRaises(ValueError):
            repository.leave_scope(camera.pk, datetime(2026, 1, 1))

        self.assertFalse(EstadoMonitoramento.objects.filter(camera=camera).exists())

    def test_audit_and_legacy_camera_fields_remain_isolated(self):
        camera = self.camera()
        repository = DjangoMonitoringRepository()
        self.bring_offline(camera, repository=repository)
        repository.leave_scope(camera.pk, START + timedelta(seconds=2))
        camera.refresh_from_db()

        self.assertEqual(EventoAuditoria.objects.count(), 0)
        self.assertIsNone(camera.status)
        self.assertIsNone(camera.status_em)
        self.assertIsNone(camera.ultima_verificacao)
        self.assertNotIn("duration", {field.name for field in Indisponibilidade._meta.fields})
