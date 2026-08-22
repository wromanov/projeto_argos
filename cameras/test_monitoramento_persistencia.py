"""Integração local SQLite da persistência MON-05C, sem rede ou worker."""

from datetime import datetime, timedelta, timezone
from unittest.mock import patch

from django.db import IntegrityError, connection, transaction
from django.test import TestCase

from cameras.models import Camera, EstadoMonitoramento, EventoAuditoria, TransicaoEstadoMonitoramento
from cameras.monitoramento.confirmation import ConfirmationPolicy, TechnicalState, reduce_confirmation
from cameras.monitoramento.contracts import ProbeResult, ProbeResultCode
from cameras.monitoramento.fakes import FakeClock
from cameras.monitoramento.repository import DjangoMonitoringRepository, is_evidence_stale
from cameras.monitoramento.scheduler import DueScheduler
from cameras.monitoramento.schemas import CompletionDisposition, MonitoringConfig, ScheduleCandidate, SchedulerLifecycle


START = datetime(2026, 1, 1, tzinfo=timezone.utc)
POLICY = ConfirmationPolicy(failures_to_offline=2, successes_to_online=1, version="mon05c-v1")


class GenerationRaceRepository(DjangoMonitoringRepository):
    """Moves the persisted generation after scheduler pre-check and before CAS."""

    def __init__(self, camera_id: int):
        super().__init__()
        self.camera_id = camera_id

    def store(self, candidate, result, memory, decision, next_due_at):
        EstadoMonitoramento.objects.filter(camera_id=self.camera_id).update(
            estado_estavel=TechnicalState.UNKNOWN.value,
            estado_alterado_em=START + timedelta(minutes=30),
            ultima_evidencia_util_em=START + timedelta(minutes=20),
            proximo_vencimento_em=START + timedelta(minutes=40),
            ultima_geracao_configuracao=6,
            sequencia_positiva=0,
            sequencia_negativa=7,
            confirmacao_ultima_observacao_em=START + timedelta(minutes=10),
        )
        return super().store(candidate, result, memory, decision, next_due_at)


class MonitoringPersistenceTests(TestCase):
    def camera(self, suffix: int = 1, **overrides) -> Camera:
        values = {
            "nome": f"CAM-{suffix}", "fabricante": "FAB", "modelo": "MOD",
            "serial": f"SER-{suffix}", "mac": f"00:11:22:33:44:{suffix:02X}",
            "tipo": Camera.TipoCamera.BULLET, "terminal": "T", "pavimento": "P",
            "setor": "S", "ambiente": "A", "ip": f"10.0.0.{suffix % 250 + 1}",
            "mascara_subrede": "255.255.255.0", "gateway": "10.0.0.1", "vlan": 10,
            "farm": "F", "retencao_esperada_dias": 1, "codec": "H264",
        }
        values.update(overrides)
        return Camera.objects.create(**values)

    def candidate(self, camera: Camera, due_at: datetime = START) -> ScheduleCandidate:
        return ScheduleCandidate(camera.pk, due_at, config_generation=1)

    def result(self, code: ProbeResultCode, at: datetime = START) -> ProbeResult:
        return ProbeResult(code=code, observed_at=at, duration_seconds=0)

    def scheduler(self, repository: DjangoMonitoringRepository, at: datetime = START) -> DueScheduler:
        return DueScheduler(
            MonitoringConfig(concurrency=1, queue_bound=1),
            FakeClock(at),
            current_generation=repository.current_generation,
            is_eligible=repository.is_eligible,
            confirmation_port=repository,
            confirmation_policy=POLICY,
        )

    def complete(self, camera: Camera, code: ProbeResultCode, at: datetime = START, repository=None):
        repository = repository or DjangoMonitoringRepository()
        scheduler = self.scheduler(repository, at)
        attempt = scheduler.tick(at, [self.candidate(camera, at)]).attempts[0]
        return scheduler.complete(attempt.attempt_id, self.result(code, at), at), repository

    def test_initial_state_is_lazy_unknown(self):
        camera = self.camera()
        repository = DjangoMonitoringRepository()
        memory = repository.load(self.candidate(camera), POLICY)
        self.assertEqual(memory.state, TechnicalState.UNKNOWN)
        self.assertFalse(EstadoMonitoramento.objects.filter(camera=camera).exists())

    def test_database_accepts_only_the_three_stable_states(self):
        for suffix, value in enumerate(("UNKNOWN", "ONLINE", "OFFLINE"), start=1):
            with self.subTest(value=value):
                state = EstadoMonitoramento.objects.create(
                    camera=self.camera(suffix), estado_estavel=value
                )
                self.assertEqual(state.estado_estavel, value)

    def test_sqlite_migration_contains_stable_state_checks(self):
        with connection.cursor() as cursor:
            state_constraints = connection.introspection.get_constraints(
                cursor, EstadoMonitoramento._meta.db_table
            )
            transition_constraints = connection.introspection.get_constraints(
                cursor, TransicaoEstadoMonitoramento._meta.db_table
            )
        self.assertIn("estado_monitoramento_estado_estavel_valid", state_constraints)
        self.assertIn("transicao_estado_anterior_valid", transition_constraints)
        self.assertIn("transicao_estado_atual_valid", transition_constraints)

    def test_database_rejects_invalid_stable_state_values(self):
        for suffix, value in enumerate(("SUSPECT", "BROKEN"), start=1):
            with self.subTest(value=value):
                with self.assertRaises(IntegrityError):
                    with transaction.atomic():
                        EstadoMonitoramento.objects.create(
                            camera=self.camera(suffix), estado_estavel=value
                        )

    def test_database_rejects_invalid_transition_state_values(self):
        for field_name in ("estado_anterior", "estado_atual"):
            with self.subTest(field_name=field_name):
                values = {
                    "camera": self.camera(10 if field_name == "estado_anterior" else 11),
                    "estado_anterior": TechnicalState.UNKNOWN.value,
                    "estado_atual": TechnicalState.ONLINE.value,
                    "ocorrida_em": START,
                }
                values[field_name] = "SUSPECT"
                with self.assertRaises(IntegrityError):
                    with transaction.atomic():
                        TransicaoEstadoMonitoramento.objects.create(**values)

    def test_online_and_next_due_persist_without_legacy_or_audit_write(self):
        camera = self.camera()
        outcome, _ = self.complete(camera, ProbeResultCode.SUCCESS)
        state = EstadoMonitoramento.objects.get(camera=camera)
        camera.refresh_from_db()
        self.assertEqual(outcome.disposition, CompletionDisposition.ACCEPTED)
        self.assertEqual(state.estado_estavel, TechnicalState.ONLINE)
        self.assertEqual(state.proximo_vencimento_em, outcome.next_due_at)
        self.assertEqual(state.ultima_evidencia_util_em, START)
        self.assertIsNone(camera.status)
        self.assertIsNone(camera.status_em)
        self.assertIsNone(camera.ultima_verificacao)
        self.assertEqual(EventoAuditoria.objects.count(), 0)

    def test_offline_persists_only_after_confirmation(self):
        camera = self.camera()
        repository = DjangoMonitoringRepository()
        first, _ = self.complete(camera, ProbeResultCode.TIMEOUT, repository=repository)
        state = EstadoMonitoramento.objects.get(camera=camera)
        self.assertEqual(state.estado_estavel, TechnicalState.UNKNOWN)
        self.assertEqual(state.sequencia_negativa, 1)
        second, _ = self.complete(camera, ProbeResultCode.TIMEOUT, START + timedelta(seconds=1), repository)
        state.refresh_from_db()
        self.assertEqual(second.decision.current_state, TechnicalState.OFFLINE)
        self.assertEqual(state.estado_estavel, TechnicalState.OFFLINE)
        self.assertEqual(TransicaoEstadoMonitoramento.objects.count(), 1)

    def test_suspect_is_not_a_persisted_state_and_same_state_creates_no_history(self):
        camera = self.camera()
        repository = DjangoMonitoringRepository()
        self.complete(camera, ProbeResultCode.TIMEOUT, repository=repository)
        self.assertNotIn("SUSPECT", EstadoMonitoramento.objects.values_list("estado_estavel", flat=True))
        self.complete(camera, ProbeResultCode.SUCCESS, START + timedelta(seconds=1), repository)
        self.complete(camera, ProbeResultCode.SUCCESS, START + timedelta(seconds=2), repository)
        self.assertEqual(TransicaoEstadoMonitoramento.objects.count(), 1)

    def test_confirmation_memory_watermark_and_due_survive_runtime_rebuild(self):
        camera = self.camera()
        repository = DjangoMonitoringRepository()
        first, _ = self.complete(camera, ProbeResultCode.TIMEOUT, repository=repository)
        fresh_repository = DjangoMonitoringRepository()
        restored = fresh_repository.load(self.candidate(camera), POLICY)
        state = EstadoMonitoramento.objects.get(camera=camera)
        self.assertEqual(restored.negative_streak, 1)
        self.assertEqual(restored.last_observed_at, START)
        self.assertEqual(state.ultima_evidencia_util_em, START)
        self.assertEqual(state.proximo_vencimento_em, first.next_due_at)
        self.assertEqual(tuple(fresh_repository.list_due(first.next_due_at, 10))[0].next_due_at, first.next_due_at)

    def test_stale_is_derived_and_does_not_change_stable_state(self):
        camera = self.camera()
        self.complete(camera, ProbeResultCode.SUCCESS)
        state = EstadoMonitoramento.objects.get(camera=camera)
        self.assertTrue(is_evidence_stale(state.ultima_evidencia_util_em, START + timedelta(minutes=10), timedelta(minutes=5)))
        state.refresh_from_db()
        self.assertEqual(state.estado_estavel, TechnicalState.ONLINE)

    def test_cancelled_and_operational_discard_do_not_advance_evidence(self):
        camera = self.camera()
        repository = DjangoMonitoringRepository()
        scheduler = self.scheduler(repository)
        attempt = scheduler.tick(START, [self.candidate(camera)]).attempts[0]
        cancelled = scheduler.complete(attempt.attempt_id, self.result(ProbeResultCode.CANCELLED), START)
        self.assertEqual(cancelled.disposition, CompletionDisposition.CANCELLED)
        self.assertFalse(EstadoMonitoramento.objects.filter(camera=camera).exists())
        scheduler.report_repository_failure("db_failure")
        self.assertFalse(EstadoMonitoramento.objects.filter(camera=camera).exists())

    def test_config_changed_and_eligibility_lost_do_not_advance_existing_evidence(self):
        camera = self.camera()
        self.complete(camera, ProbeResultCode.SUCCESS)
        repository = DjangoMonitoringRepository()
        original = EstadoMonitoramento.objects.get(camera=camera).ultima_evidencia_util_em
        scheduler = self.scheduler(repository, START + timedelta(seconds=10))
        changed = scheduler.tick(START + timedelta(seconds=10), [self.candidate(camera, START + timedelta(seconds=10))]).attempts[0]
        EstadoMonitoramento.objects.filter(camera=camera).update(ultima_geracao_configuracao=2)
        self.assertEqual(
            scheduler.complete(changed.attempt_id, self.result(ProbeResultCode.SUCCESS, START + timedelta(seconds=10))).disposition,
            CompletionDisposition.CONFIG_CHANGED,
        )
        EstadoMonitoramento.objects.filter(camera=camera).update(ultima_geracao_configuracao=1)
        scheduler = self.scheduler(repository, START + timedelta(seconds=20))
        lost = scheduler.tick(START + timedelta(seconds=20), [self.candidate(camera, START + timedelta(seconds=20))]).attempts[0]
        Camera.objects.filter(pk=camera.pk).update(situacao_operacional=Camera.SituacaoOperacional.ESTOQUE)
        self.assertEqual(
            scheduler.complete(lost.attempt_id, self.result(ProbeResultCode.SUCCESS, START + timedelta(seconds=20))).disposition,
            CompletionDisposition.ELIGIBILITY_LOST,
        )
        self.assertEqual(EstadoMonitoramento.objects.get(camera=camera).ultima_evidencia_util_em, original)

    def test_stale_generation_after_precheck_is_discarded_without_any_commit_effect(self):
        camera = self.camera()
        EstadoMonitoramento.objects.create(
            camera=camera,
            estado_estavel=TechnicalState.UNKNOWN.value,
            ultima_evidencia_util_em=START,
            proximo_vencimento_em=START + timedelta(minutes=1),
            ultima_geracao_configuracao=5,
            versao_politica_confirmacao=POLICY.version,
            confirmacao_ultima_observacao_em=START,
        )
        repository = GenerationRaceRepository(camera.pk)
        scheduler = self.scheduler(repository)
        attempt = scheduler.tick(
            START, [ScheduleCandidate(camera.pk, START, config_generation=5)]
        ).attempts[0]

        outcome = scheduler.complete(
            attempt.attempt_id,
            self.result(ProbeResultCode.SUCCESS, START + timedelta(minutes=2)),
            START + timedelta(minutes=2),
        )

        state = EstadoMonitoramento.objects.get(camera=camera)
        self.assertEqual(outcome.disposition, CompletionDisposition.CONFIG_CHANGED)
        self.assertEqual(scheduler.lifecycle, SchedulerLifecycle.RUNNING)
        self.assertEqual(state.ultima_geracao_configuracao, 6)
        self.assertEqual(state.estado_estavel, TechnicalState.UNKNOWN.value)
        self.assertEqual(state.ultima_evidencia_util_em, START + timedelta(minutes=20))
        self.assertEqual(state.proximo_vencimento_em, START + timedelta(minutes=40))
        self.assertEqual(state.sequencia_negativa, 7)
        self.assertEqual(state.confirmacao_ultima_observacao_em, START + timedelta(minutes=10))
        self.assertEqual(TransicaoEstadoMonitoramento.objects.count(), 0)
        self.assertEqual(EventoAuditoria.objects.count(), 0)

    def test_duplicate_completion_does_not_duplicate_transition(self):
        camera = self.camera()
        repository = DjangoMonitoringRepository()
        scheduler = self.scheduler(repository)
        attempt = scheduler.tick(START, [self.candidate(camera)]).attempts[0]
        scheduler.complete(attempt.attempt_id, self.result(ProbeResultCode.SUCCESS), START)
        duplicate = scheduler.complete(attempt.attempt_id, self.result(ProbeResultCode.SUCCESS), START)
        self.assertEqual(duplicate.disposition, CompletionDisposition.DUPLICATE)
        self.assertEqual(TransicaoEstadoMonitoramento.objects.count(), 1)

    def test_atomic_rollback_when_transition_write_fails(self):
        camera = self.camera()
        repository = DjangoMonitoringRepository(before_transition=lambda: (_ for _ in ()).throw(IntegrityError("forced")))
        outcome, _ = self.complete(camera, ProbeResultCode.SUCCESS, repository=repository)
        self.assertEqual(outcome.disposition, CompletionDisposition.OPERATIONAL_FAILURE)
        self.assertFalse(EstadoMonitoramento.objects.filter(camera=camera).exists())
        self.assertEqual(TransicaoEstadoMonitoramento.objects.count(), 0)

    def test_atomic_rollback_when_state_write_fails(self):
        camera = self.camera()
        with patch.object(EstadoMonitoramento, "save", side_effect=IntegrityError("forced")):
            outcome, _ = self.complete(camera, ProbeResultCode.SUCCESS)
        self.assertEqual(outcome.disposition, CompletionDisposition.OPERATIONAL_FAILURE)
        self.assertFalse(EstadoMonitoramento.objects.filter(camera=camera).exists())
        self.assertEqual(TransicaoEstadoMonitoramento.objects.count(), 0)

    def test_scope_exit_is_not_offline_and_return_resets_to_unknown(self):
        camera = self.camera()
        self.complete(camera, ProbeResultCode.SUCCESS)
        repository = DjangoMonitoringRepository()
        repository.leave_scope(camera.pk, START + timedelta(seconds=1))
        state = EstadoMonitoramento.objects.get(camera=camera)
        self.assertFalse(state.em_escopo)
        self.assertEqual(state.estado_estavel, TechnicalState.ONLINE)
        repository.enter_scope(camera.pk, START + timedelta(seconds=2))
        state.refresh_from_db()
        self.assertTrue(state.em_escopo)
        self.assertEqual(state.estado_estavel, TechnicalState.UNKNOWN)

    def test_local_laboratory_loads_2300_without_history_per_read(self):
        Camera.objects.bulk_create([
            Camera(
                nome=f"CAM-{index}", fabricante="FAB", modelo="MOD", serial=f"SER-{index}",
                mac=f"02:00:{index // 256:02X}:{index % 256:02X}:00:01", tipo=Camera.TipoCamera.BULLET,
                terminal="T", pavimento="P", setor="S", ambiente="A", ip=f"10.{index // 255}.{index % 255}.2",
                mascara_subrede="255.255.255.0", gateway="10.0.0.1", vlan=10, farm="F",
                retencao_esperada_dias=1, codec="H264",
            )
            for index in range(1, 2301)
        ])
        repository = DjangoMonitoringRepository()
        candidates = tuple(repository.list_due(START, 2300))
        self.assertEqual(len(candidates), 2300)
        self.assertEqual(EstadoMonitoramento.objects.count(), 0)
        self.assertEqual(TransicaoEstadoMonitoramento.objects.count(), 0)
