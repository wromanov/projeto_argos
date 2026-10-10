"""Harness integrado MON-08C: persistência SQLite descartável em escala."""

from collections import Counter
from datetime import datetime, timedelta, timezone
from time import perf_counter

from django.db import connection
from django.db.models import Count
from django.test import TransactionTestCase

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


ASSET_COUNT = 2300
FAST_ASSET_COUNT = 3
START = datetime(2026, 9, 23, tzinfo=timezone.utc)
POLICY = ConfirmationPolicy(
    failures_to_offline=2,
    successes_to_online=1,
    version="mon08c-1-normal-v1",
)


class Mon08CExecutionStrategyHarnessTests(TransactionTestCase):
    """Exercita scheduler -> reducer -> ORM no banco SQLite real.

    Os métodos ``test_fast_correctness_*`` validam semântica com dataset
    pequeno. Os métodos ``test_scale_mon08c_*`` preservam evidência material
    da integração em 2.300 ativos.

    ``TransactionTestCase`` é intencional: não envolve o teste inteiro em uma
    transação que esconderia os commits das transações curtas do repositório.
    O runner Django cria e descarta o banco de testes automaticamente.
    """

    def _create_cameras(self, asset_count: int = ASSET_COUNT) -> None:
        Camera.objects.bulk_create(
            [
                Camera(
                    nome=f"MON08C-CAM-{index:04d}",
                    fabricante="FAB",
                    modelo="MOD",
                    serial=f"MON08C-SER-{index:04d}",
                    mac=f"02:08:{index // 256:02X}:{index % 256:02X}:00:01",
                    tipo=Camera.TipoCamera.BULLET,
                    terminal="T",
                    pavimento="P",
                    setor="S",
                    ambiente="A",
                    ip=f"10.{index // 255}.{index % 255}.2",
                    mascara_subrede="255.255.255.0",
                    gateway="10.0.0.1",
                    vlan=10,
                    farm="F",
                    retencao_esperada_dias=1,
                    codec="H264",
                )
                for index in range(1, asset_count + 1)
            ],
            batch_size=250,
        )

    class _QueryCounter:
        """Conta todas as queries sem depender do buffer limitado de debug."""

        def __init__(self) -> None:
            self.profile: Counter[str] = Counter()

        def __call__(self, execute, sql, params, many, context):
            normalized = sql.lstrip().upper()
            self.profile[normalized.split(maxsplit=1)[0] if normalized else "EMPTY"] += 1
            return execute(sql, params, many, context)

    def _scheduler(self, repository: DjangoMonitoringRepository, at: datetime) -> DueScheduler:
        return DueScheduler(
            MonitoringConfig(concurrency=20, queue_bound=40),
            FakeClock(at),
            current_generation=repository.current_generation,
            is_eligible=repository.is_eligible,
            confirmation_port=repository,
            confirmation_policy=POLICY,
        )

    def _state_snapshot(self) -> tuple[tuple[object, ...], ...]:
        """Captura somente os valores persistidos necessários às assertions."""

        return tuple(
            EstadoMonitoramento.objects.order_by("camera_id").values_list(
                "camera_id",
                "estado_estavel",
                "sequencia_positiva",
                "sequencia_negativa",
                "confirmacao_ultima_observacao_em",
                "ultima_evidencia_util_em",
                "proximo_vencimento_em",
                "ultima_geracao_configuracao",
                "versao_politica_confirmacao",
                "em_escopo",
            )
        )

    def _legacy_camera_snapshot(self) -> tuple[tuple[object, ...], ...]:
        return tuple(
            Camera.objects.order_by("pk").values_list(
                "pk",
                "status",
                "status_em",
                "ultima_verificacao",
            )
        )

    def _unavailability_snapshot(self) -> tuple[tuple[object, ...], ...]:
        return tuple(
            Indisponibilidade.objects.order_by("camera_id", "pk").values_list(
                "pk",
                "camera_id",
                "opened_at",
                "closed_at",
                "open_origin",
                "close_reason",
                "opening_transition_id",
                "closing_transition_id",
            )
        )

    def _complete_candidates(
        self,
        repository: DjangoMonitoringRepository,
        candidates: tuple[ScheduleCandidate, ...],
        result: ProbeResult,
    ) -> tuple[int, float, int, Counter[str]]:
        """Completa candidatos recarregados usando um scheduler novo."""

        scheduler = self._scheduler(repository, result.observed_at)
        processed = 0
        remaining = {candidate.camera_id: candidate for candidate in candidates}
        query_counter = self._QueryCounter()
        started = perf_counter()
        with connection.execute_wrapper(query_counter):
            while remaining:
                if scheduler.active_count == 0:
                    scheduler.tick(result.observed_at, remaining.values())
                active_attempts = scheduler.active_attempts
                self.assertTrue(
                    active_attempts,
                    "scheduler stopped admitting eligible due assets "
                    f"(processed={processed}, lifecycle={scheduler.lifecycle}, "
                    f"queued={scheduler.queued_count}, active={scheduler.active_count}, "
                    f"operational_error={scheduler._operational_error!r})",
                )
                for attempt in active_attempts:
                    outcome = scheduler.complete(attempt.attempt_id, result, result.observed_at)
                    self.assertEqual(outcome.disposition, CompletionDisposition.ACCEPTED)
                    processed += 1
                    remaining.pop(attempt.camera_id, None)
        duration = perf_counter() - started
        profile = query_counter.profile
        return processed, duration, sum(profile.values()), profile

    def _reload_due_candidates(
        self,
        restart_at: datetime,
        asset_count: int = ASSET_COUNT,
    ) -> tuple[DjangoMonitoringRepository, tuple[ScheduleCandidate, ...], float, int, Counter[str]]:
        """Reconstrói o repository e recarrega candidatos pelo caminho normal."""

        repository = DjangoMonitoringRepository()
        query_counter = self._QueryCounter()
        started = perf_counter()
        with connection.execute_wrapper(query_counter):
            candidates = tuple(repository.list_due(restart_at, asset_count))
        duration = perf_counter() - started
        profile = query_counter.profile
        return repository, candidates, duration, sum(profile.values()), profile

    def _restart_at_from_persisted_due(self, asset_count: int = ASSET_COUNT) -> datetime:
        persisted_due = list(
            EstadoMonitoramento.objects.values_list("proximo_vencimento_em", flat=True)
        )
        self.assertEqual(len(persisted_due), asset_count)
        self.assertTrue(all(value is not None for value in persisted_due))
        return max(value for value in persisted_due) + timedelta(seconds=1)

    def _assert_reloaded_candidates_match_persisted_state(
        self,
        candidates: tuple[ScheduleCandidate, ...],
        asset_count: int = ASSET_COUNT,
    ) -> None:
        persisted_schedule = {
            camera_id: (next_due_at, generation)
            for camera_id, next_due_at, generation in EstadoMonitoramento.objects.values_list(
                "camera_id",
                "proximo_vencimento_em",
                "ultima_geracao_configuracao",
            )
        }
        reloaded_schedule = {
            candidate.camera_id: (candidate.next_due_at, candidate.config_generation)
            for candidate in candidates
        }
        self.assertEqual(len(reloaded_schedule), asset_count)
        self.assertTrue(all(candidate.eligible for candidate in candidates))
        self.assertEqual(reloaded_schedule, persisted_schedule)

    def _complete_round(
        self,
        repository: DjangoMonitoringRepository,
        camera_ids: tuple[int, ...],
        result: ProbeResult,
    ) -> tuple[int, float, int, Counter[str]]:
        """Completa uma rodada pelo scheduler e registra a persistência real."""

        candidates = tuple(
            ScheduleCandidate(camera_id, result.observed_at, config_generation=1)
            for camera_id in camera_ids
        )
        return self._complete_candidates(repository, candidates, result)

    def test_scale_mon08c_initial_persistence_unknown_to_online_2300_assets(self):
        setup_started = perf_counter()
        self._create_cameras()
        camera_rows = list(Camera.objects.order_by("pk").values("pk", "status", "status_em", "ultima_verificacao"))
        setup_duration = perf_counter() - setup_started

        self.assertEqual(len(camera_rows), ASSET_COUNT)
        self.assertEqual(len({row["pk"] for row in camera_rows}), ASSET_COUNT)
        self.assertTrue(all(row["status"] is None for row in camera_rows))
        self.assertTrue(all(row["status_em"] is None for row in camera_rows))
        self.assertTrue(all(row["ultima_verificacao"] is None for row in camera_rows))

        processed, execution_duration, query_count_total, query_profile = self._complete_round(
            DjangoMonitoringRepository(),
            tuple(row["pk"] for row in camera_rows),
            ProbeResult(ProbeResultCode.SUCCESS, START, duration_seconds=0),
        )

        states = list(EstadoMonitoramento.objects.order_by("camera_id"))
        final_camera_rows = list(Camera.objects.order_by("pk").values("pk", "status", "status_em", "ultima_verificacao"))
        final_distribution = Counter(state.estado_estavel for state in states)

        self.assertEqual(processed, ASSET_COUNT)
        self.assertEqual(len(states), ASSET_COUNT)
        self.assertEqual(len({state.camera_id for state in states}), ASSET_COUNT)
        self.assertEqual(final_distribution, Counter({TechnicalState.ONLINE.value: ASSET_COUNT}))
        self.assertFalse(EstadoMonitoramento.objects.filter(estado_estavel="SUSPECT").exists())
        self.assertEqual(TransicaoEstadoMonitoramento.objects.count(), ASSET_COUNT)
        self.assertEqual(Indisponibilidade.objects.filter(closed_at__isnull=True).count(), 0)
        self.assertEqual(EventoAuditoria.objects.count(), 0)
        self.assertEqual(len(final_camera_rows), ASSET_COUNT)
        self.assertTrue(all(row["status"] is None for row in final_camera_rows))
        self.assertTrue(all(row["status_em"] is None for row in final_camera_rows))
        self.assertTrue(all(row["ultima_verificacao"] is None for row in final_camera_rows))

        # Métricas factuais do experimento; impressas pelo runner apenas para
        # registro da execução, sem transformar limites em SLA.
        print(
            "MON08C1_METRICS "
            f"setup_seconds={setup_duration:.6f} "
            f"execution_seconds={execution_duration:.6f} "
            f"average_completion_seconds={execution_duration / processed:.9f} "
            f"query_count_total={query_count_total} "
            f"query_profile={dict(sorted(query_profile.items()))}"
        )

    def test_scale_mon08c_mass_lifecycle_failure_recovery_2300_assets(self):
        """MON-08C-2 + MON-08C-3: falha e recovery no mesmo fluxo de escala."""

        self._create_cameras()
        camera_rows = list(Camera.objects.order_by("pk").values("pk", "status", "status_em", "ultima_verificacao"))
        camera_ids = tuple(row["pk"] for row in camera_rows)
        self.assertEqual(len(camera_ids), ASSET_COUNT)
        self.assertEqual(len(set(camera_ids)), ASSET_COUNT)
        self.assertTrue(all(row["status"] is None for row in camera_rows))
        self.assertTrue(all(row["status_em"] is None for row in camera_rows))
        self.assertTrue(all(row["ultima_verificacao"] is None for row in camera_rows))

        repository = DjangoMonitoringRepository()
        prepared, _, _, _ = self._complete_round(
            repository,
            camera_ids,
            ProbeResult(ProbeResultCode.SUCCESS, START, duration_seconds=0),
        )
        self.assertEqual(prepared, ASSET_COUNT)
        self.assertEqual(
            Counter(EstadoMonitoramento.objects.values_list("estado_estavel", flat=True)),
            Counter({TechnicalState.ONLINE.value: ASSET_COUNT}),
        )
        self.assertEqual(TransicaoEstadoMonitoramento.objects.count(), ASSET_COUNT)
        self.assertEqual(Indisponibilidade.objects.filter(closed_at__isnull=True).count(), 0)

        round_1_processed, round_1_duration, round_1_queries, round_1_profile = self._complete_round(
            repository,
            camera_ids,
            ProbeResult(ProbeResultCode.TIMEOUT, START + timedelta(seconds=1), duration_seconds=0),
        )
        round_1_distribution = Counter(EstadoMonitoramento.objects.values_list("estado_estavel", flat=True))
        new_offline_transitions_after_failure_1 = (
            TransicaoEstadoMonitoramento.objects.count() - ASSET_COUNT
        )
        open_indisponibilidades_after_failure_1 = Indisponibilidade.objects.filter(
            closed_at__isnull=True
        ).count()

        self.assertEqual(round_1_processed, ASSET_COUNT)
        self.assertEqual(round_1_distribution, Counter({TechnicalState.ONLINE.value: ASSET_COUNT}))
        self.assertEqual(new_offline_transitions_after_failure_1, 0)
        self.assertEqual(open_indisponibilidades_after_failure_1, 0)
        self.assertEqual(EstadoMonitoramento.objects.filter(sequencia_negativa=1).count(), ASSET_COUNT)
        self.assertFalse(EstadoMonitoramento.objects.filter(estado_estavel="SUSPECT").exists())

        round_2_processed, round_2_duration, round_2_queries, round_2_profile = self._complete_round(
            repository,
            camera_ids,
            ProbeResult(ProbeResultCode.TIMEOUT, START + timedelta(seconds=2), duration_seconds=0),
        )
        states = list(EstadoMonitoramento.objects.order_by("camera_id"))
        offline_distribution = Counter(state.estado_estavel for state in states)
        offline_transitions = TransicaoEstadoMonitoramento.objects.filter(
            estado_anterior=TechnicalState.ONLINE.value,
            estado_atual=TechnicalState.OFFLINE.value,
        )
        open_intervals = Indisponibilidade.objects.filter(closed_at__isnull=True)
        open_indisponibilidades_after_failure_2 = open_intervals.count()

        self.assertEqual(round_2_processed, ASSET_COUNT)
        self.assertEqual(offline_distribution, Counter({TechnicalState.OFFLINE.value: ASSET_COUNT}))
        self.assertEqual(offline_transitions.count(), ASSET_COUNT)
        self.assertEqual(TransicaoEstadoMonitoramento.objects.count(), ASSET_COUNT * 2)
        self.assertEqual(open_indisponibilidades_after_failure_2, ASSET_COUNT)
        self.assertEqual(
            open_intervals.filter(open_origin=Indisponibilidade.OrigemAbertura.ONLINE_TO_OFFLINE).count(),
            ASSET_COUNT,
        )
        self.assertEqual(
            open_intervals.exclude(
                opening_transition__estado_anterior=TechnicalState.ONLINE.value,
                opening_transition__estado_atual=TechnicalState.OFFLINE.value,
            ).count(),
            0,
        )
        self.assertEqual(
            Indisponibilidade.objects.values("camera_id").filter(closed_at__isnull=True).distinct().count(),
            ASSET_COUNT,
        )
        self.assertTrue(
            all(
                state.sequencia_positiva == 0
                and state.sequencia_negativa == 0
                and state.confirmacao_ultima_observacao_em == START + timedelta(seconds=2)
                and state.ultima_evidencia_util_em == START + timedelta(seconds=2)
                and state.versao_politica_confirmacao == POLICY.version
                for state in states
            )
        )
        self.assertFalse(EstadoMonitoramento.objects.filter(estado_estavel="SUSPECT").exists())

        recovery_processed, recovery_duration, recovery_queries, recovery_profile = self._complete_round(
            repository,
            camera_ids,
            ProbeResult(ProbeResultCode.SUCCESS, START + timedelta(seconds=3), duration_seconds=0),
        )
        recovery_transitions = TransicaoEstadoMonitoramento.objects.filter(
            estado_anterior=TechnicalState.OFFLINE.value,
            estado_atual=TechnicalState.ONLINE.value,
        )
        intervals = Indisponibilidade.objects.select_related(
            "opening_transition", "closing_transition"
        ).order_by("camera_id")
        final_states = list(EstadoMonitoramento.objects.order_by("camera_id"))
        final_distribution = Counter(state.estado_estavel for state in final_states)
        final_camera_rows = list(Camera.objects.order_by("pk").values("status", "status_em", "ultima_verificacao"))
        duplicate_open_intervals = (
            Indisponibilidade.objects.filter(closed_at__isnull=True)
            .values("camera_id")
            .annotate(total=Count("pk"))
            .filter(total__gt=1)
            .count()
        )

        self.assertEqual(recovery_processed, ASSET_COUNT)
        self.assertEqual(final_distribution, Counter({TechnicalState.ONLINE.value: ASSET_COUNT}))
        self.assertEqual(recovery_transitions.count(), ASSET_COUNT)
        self.assertEqual(recovery_transitions.values("camera_id").distinct().count(), ASSET_COUNT)
        self.assertEqual(TransicaoEstadoMonitoramento.objects.count(), ASSET_COUNT * 3)
        self.assertEqual(intervals.count(), ASSET_COUNT)
        self.assertEqual(intervals.filter(closed_at__isnull=True).count(), 0)
        self.assertEqual(intervals.filter(closed_at__isnull=False).count(), ASSET_COUNT)
        self.assertEqual(duplicate_open_intervals, 0)
        self.assertTrue(
            all(
                interval.opened_at == START + timedelta(seconds=2)
                and interval.closed_at == START + timedelta(seconds=3)
                and interval.open_origin == Indisponibilidade.OrigemAbertura.ONLINE_TO_OFFLINE
                and interval.close_reason == Indisponibilidade.MotivoFechamento.RECUPERADA
                and interval.opening_transition.estado_anterior == TechnicalState.ONLINE.value
                and interval.opening_transition.estado_atual == TechnicalState.OFFLINE.value
                and interval.closing_transition is not None
                and interval.closing_transition.estado_anterior == TechnicalState.OFFLINE.value
                and interval.closing_transition.estado_atual == TechnicalState.ONLINE.value
                and interval.closing_transition.ocorrida_em == START + timedelta(seconds=3)
                for interval in intervals
            )
        )
        self.assertTrue(
            all(
                state.sequencia_positiva == 0
                and state.sequencia_negativa == 0
                and state.confirmacao_ultima_observacao_em == START + timedelta(seconds=3)
                and state.ultima_evidencia_util_em == START + timedelta(seconds=3)
                and state.versao_politica_confirmacao == POLICY.version
                for state in final_states
            )
        )
        self.assertFalse(EstadoMonitoramento.objects.filter(estado_estavel="SUSPECT").exists())
        self.assertEqual(EventoAuditoria.objects.count(), 0)
        self.assertTrue(all(row["status"] is None for row in final_camera_rows))
        self.assertTrue(all(row["status_em"] is None for row in final_camera_rows))
        self.assertTrue(all(row["ultima_verificacao"] is None for row in final_camera_rows))

        print(
            "MON08C2_C3_METRICS "
            f"round_1_seconds={round_1_duration:.6f} "
            f"round_1_average_completion_seconds={round_1_duration / round_1_processed:.9f} "
            f"round_1_query_count={round_1_queries} "
            f"round_1_query_profile={dict(sorted(round_1_profile.items()))} "
            f"round_1_new_offline_transitions={new_offline_transitions_after_failure_1} "
            f"round_1_open_indisponibilidades={open_indisponibilidades_after_failure_1} "
            f"round_2_seconds={round_2_duration:.6f} "
            f"round_2_average_completion_seconds={round_2_duration / round_2_processed:.9f} "
            f"round_2_query_count={round_2_queries} "
            f"round_2_query_profile={dict(sorted(round_2_profile.items()))} "
            f"round_2_offline_transitions={offline_transitions.count()} "
            f"round_2_open_indisponibilidades={open_indisponibilidades_after_failure_2} "
            f"recovery_seconds={recovery_duration:.6f} "
            f"recovery_average_completion_seconds={recovery_duration / recovery_processed:.9f} "
            f"recovery_query_count={recovery_queries} "
            f"recovery_query_profile={dict(sorted(recovery_profile.items()))} "
            f"recovery_transitions_created={recovery_transitions.count()} "
            f"indisponibilidades_closed={intervals.filter(closed_at__isnull=False).count()} "
            "sqlite_errors=0"
        )

    def test_fast_correctness_restart_online_reloads_state_without_duplicate_history(self):
        """FAST/CORRECTNESS: restart ONLINE é idempotente com 3 ativos."""

        self.assertEqual(connection.vendor, "sqlite")
        self._create_cameras(FAST_ASSET_COUNT)
        camera_ids = tuple(Camera.objects.order_by("pk").values_list("pk", flat=True))
        self.assertEqual(len(camera_ids), FAST_ASSET_COUNT)
        self.assertEqual(len(set(camera_ids)), FAST_ASSET_COUNT)

        repository = DjangoMonitoringRepository()
        prepared, _, _, _ = self._complete_round(
            repository,
            camera_ids,
            ProbeResult(ProbeResultCode.SUCCESS, START, duration_seconds=0),
        )
        pre_restart_state = self._state_snapshot()
        pre_restart_transition_count = TransicaoEstadoMonitoramento.objects.count()
        pre_restart_indisponibilidade_count = Indisponibilidade.objects.count()
        pre_restart_open_count = Indisponibilidade.objects.filter(closed_at__isnull=True).count()

        self.assertEqual(prepared, FAST_ASSET_COUNT)
        self.assertEqual(
            Counter(row[1] for row in pre_restart_state),
            Counter({TechnicalState.ONLINE.value: FAST_ASSET_COUNT}),
        )
        self.assertEqual(pre_restart_transition_count, FAST_ASSET_COUNT)
        self.assertEqual(pre_restart_indisponibilidade_count, 0)
        self.assertEqual(pre_restart_open_count, 0)
        self.assertFalse(EstadoMonitoramento.objects.filter(estado_estavel="SUSPECT").exists())

        # O objeto anterior não participa do reload nem da continuidade.
        del repository
        restart_at = self._restart_at_from_persisted_due(FAST_ASSET_COUNT)
        reloaded_repository, reloaded_candidates, reload_duration, reload_queries, reload_profile = (
            self._reload_due_candidates(restart_at, FAST_ASSET_COUNT)
        )
        post_reload_state = self._state_snapshot()
        post_reload_transition_count = TransicaoEstadoMonitoramento.objects.count()
        post_reload_indisponibilidade_count = Indisponibilidade.objects.count()
        post_reload_open_count = Indisponibilidade.objects.filter(closed_at__isnull=True).count()

        self.assertEqual(len(reloaded_candidates), FAST_ASSET_COUNT)
        self.assertTrue(all(candidate.is_due(restart_at) for candidate in reloaded_candidates))
        self._assert_reloaded_candidates_match_persisted_state(reloaded_candidates, FAST_ASSET_COUNT)
        self.assertEqual(post_reload_state, pre_restart_state)
        self.assertEqual(post_reload_transition_count, pre_restart_transition_count)
        self.assertEqual(post_reload_indisponibilidade_count, pre_restart_indisponibilidade_count)
        self.assertEqual(post_reload_open_count, pre_restart_open_count)

        # SUCCESS em ONLINE é a evidência legítima de continuidade e não deve
        # recriar UNKNOWN -> ONLINE nem qualquer indisponibilidade.
        processed, operation_duration, post_restart_queries, operation_profile = self._complete_candidates(
            reloaded_repository,
            reloaded_candidates,
            ProbeResult(ProbeResultCode.SUCCESS, restart_at, duration_seconds=0),
        )

        final_state = self._state_snapshot()
        final_transitions = TransicaoEstadoMonitoramento.objects.count()
        final_indisponibilidades = Indisponibilidade.objects.count()
        final_open_count = Indisponibilidade.objects.filter(closed_at__isnull=True).count()

        self.assertEqual(processed, FAST_ASSET_COUNT)
        self.assertEqual(
            Counter(row[1] for row in final_state),
            Counter({TechnicalState.ONLINE.value: FAST_ASSET_COUNT}),
        )
        self.assertEqual(final_transitions, pre_restart_transition_count)
        self.assertEqual(
            TransicaoEstadoMonitoramento.objects.filter(
                estado_anterior=TechnicalState.UNKNOWN.value,
                estado_atual=TechnicalState.ONLINE.value,
            ).count(),
            FAST_ASSET_COUNT,
        )
        self.assertEqual(final_indisponibilidades, pre_restart_indisponibilidade_count)
        self.assertEqual(final_open_count, 0)
        self.assertFalse(EstadoMonitoramento.objects.filter(estado_estavel="SUSPECT").exists())
        self.assertEqual(EventoAuditoria.objects.count(), 0)
        self.assertTrue(
            all(
                row["status"] is None
                and row["status_em"] is None
                and row["ultima_verificacao"] is None
                for row in Camera.objects.values("status", "status_em", "ultima_verificacao")
            )
        )

        print(
            "MON08C4_FAST_ONLINE_RESTART_METRICS "
            f"asset_count={FAST_ASSET_COUNT} "
            f"reload_seconds={reload_duration:.6f} "
            f"reload_query_count={reload_queries} "
            f"reload_query_profile={dict(sorted(reload_profile.items()))} "
            f"post_restart_seconds={operation_duration:.6f} "
            f"post_restart_query_count={post_restart_queries} "
            f"post_restart_query_profile={dict(sorted(operation_profile.items()))} "
            f"pre_transitions={pre_restart_transition_count} "
            f"post_reload_transitions={post_reload_transition_count} "
            f"final_transitions={final_transitions} "
            f"pre_indisponibilidades={pre_restart_indisponibilidade_count} "
            f"post_reload_indisponibilidades={post_reload_indisponibilidade_count} "
            f"final_indisponibilidades={final_indisponibilidades} "
            "restart_only_new_transitions=0 "
            "restart_only_new_indisponibilidades=0 "
            "sqlite_errors=0"
        )

    def test_scale_mon08c_restart_offline_reloads_and_recovers_without_duplicate_history(self):
        """SCALE/MON-08C-4: OFFLINE persistido recupera sem duplicar histórico."""

        self.assertEqual(connection.vendor, "sqlite")
        self._create_cameras()
        camera_ids = tuple(Camera.objects.order_by("pk").values_list("pk", flat=True))
        self.assertEqual(len(camera_ids), ASSET_COUNT)
        self.assertEqual(len(set(camera_ids)), ASSET_COUNT)

        repository = DjangoMonitoringRepository()
        prepared, _, _, _ = self._complete_round(
            repository,
            camera_ids,
            ProbeResult(ProbeResultCode.SUCCESS, START, duration_seconds=0),
        )
        first_failure, _, _, _ = self._complete_round(
            repository,
            camera_ids,
            ProbeResult(ProbeResultCode.TIMEOUT, START + timedelta(seconds=1), duration_seconds=0),
        )
        confirmed_offline, _, _, _ = self._complete_round(
            repository,
            camera_ids,
            ProbeResult(ProbeResultCode.TIMEOUT, START + timedelta(seconds=2), duration_seconds=0),
        )

        pre_restart_state = self._state_snapshot()
        pre_restart_transition_count = TransicaoEstadoMonitoramento.objects.count()
        pre_restart_indisponibilidade_count = Indisponibilidade.objects.count()
        pre_restart_open_count = Indisponibilidade.objects.filter(closed_at__isnull=True).count()

        self.assertEqual(prepared, ASSET_COUNT)
        self.assertEqual(first_failure, ASSET_COUNT)
        self.assertEqual(confirmed_offline, ASSET_COUNT)
        self.assertEqual(
            Counter(row[1] for row in pre_restart_state),
            Counter({TechnicalState.OFFLINE.value: ASSET_COUNT}),
        )
        self.assertEqual(pre_restart_transition_count, ASSET_COUNT * 2)
        self.assertEqual(pre_restart_indisponibilidade_count, ASSET_COUNT)
        self.assertEqual(pre_restart_open_count, ASSET_COUNT)
        self.assertTrue(
            all(
                row[2] == 0
                and row[3] == 0
                and row[4] == START + timedelta(seconds=2)
                and row[5] == START + timedelta(seconds=2)
                and row[7] == 1
                and row[8] == POLICY.version
                and row[9] is True
                for row in pre_restart_state
            )
        )
        self.assertFalse(EstadoMonitoramento.objects.filter(estado_estavel="SUSPECT").exists())

        # Novo repository e novos objetos de scheduler/runtime serão usados após
        # este ponto; o banco de testes permanece o mesmo.
        del repository
        restart_at = self._restart_at_from_persisted_due()
        reloaded_repository, reloaded_candidates, reload_duration, reload_queries, reload_profile = (
            self._reload_due_candidates(restart_at)
        )
        post_reload_state = self._state_snapshot()
        post_reload_transition_count = TransicaoEstadoMonitoramento.objects.count()
        post_reload_indisponibilidade_count = Indisponibilidade.objects.count()
        post_reload_open_count = Indisponibilidade.objects.filter(closed_at__isnull=True).count()

        self.assertEqual(len(reloaded_candidates), ASSET_COUNT)
        self.assertTrue(all(candidate.is_due(restart_at) for candidate in reloaded_candidates))
        self._assert_reloaded_candidates_match_persisted_state(reloaded_candidates)
        self.assertEqual(post_reload_state, pre_restart_state)
        self.assertEqual(post_reload_transition_count, pre_restart_transition_count)
        self.assertEqual(post_reload_indisponibilidade_count, pre_restart_indisponibilidade_count)
        self.assertEqual(post_reload_open_count, pre_restart_open_count)

        recovery_processed, operation_duration, post_restart_queries, operation_profile = self._complete_candidates(
            reloaded_repository,
            reloaded_candidates,
            ProbeResult(ProbeResultCode.SUCCESS, restart_at, duration_seconds=0),
        )

        recovery_transitions = TransicaoEstadoMonitoramento.objects.filter(
            estado_anterior=TechnicalState.OFFLINE.value,
            estado_atual=TechnicalState.ONLINE.value,
        )
        final_state = self._state_snapshot()
        final_indisponibilidades = Indisponibilidade.objects.select_related(
            "opening_transition", "closing_transition"
        ).order_by("camera_id")
        multiple_open = (
            Indisponibilidade.objects.filter(closed_at__isnull=True)
            .values("camera_id")
            .annotate(total=Count("pk"))
            .filter(total__gt=1)
            .count()
        )
        final_open_count = Indisponibilidade.objects.filter(closed_at__isnull=True).count()
        final_transitions = TransicaoEstadoMonitoramento.objects.count()

        self.assertEqual(recovery_processed, ASSET_COUNT)
        self.assertEqual(
            Counter(row[1] for row in final_state),
            Counter({TechnicalState.ONLINE.value: ASSET_COUNT}),
        )
        self.assertEqual(recovery_transitions.count(), ASSET_COUNT)
        self.assertEqual(final_transitions, ASSET_COUNT * 3)
        self.assertEqual(final_indisponibilidades.count(), ASSET_COUNT)
        self.assertEqual(final_open_count, 0)
        self.assertEqual(multiple_open, 0)
        self.assertTrue(
            all(
                interval.opened_at == START + timedelta(seconds=2)
                and interval.closed_at == restart_at
                and interval.open_origin == Indisponibilidade.OrigemAbertura.ONLINE_TO_OFFLINE
                and interval.close_reason == Indisponibilidade.MotivoFechamento.RECUPERADA
                and interval.opening_transition.estado_anterior == TechnicalState.ONLINE.value
                and interval.opening_transition.estado_atual == TechnicalState.OFFLINE.value
                and interval.closing_transition is not None
                and interval.closing_transition.estado_anterior == TechnicalState.OFFLINE.value
                and interval.closing_transition.estado_atual == TechnicalState.ONLINE.value
                and interval.closing_transition.ocorrida_em == restart_at
                for interval in final_indisponibilidades
            )
        )
        self.assertTrue(
            all(
                row[2] == 0
                and row[3] == 0
                and row[4] == restart_at
                and row[5] == restart_at
                and row[7] == 1
                and row[8] == POLICY.version
                and row[9] is True
                for row in final_state
            )
        )
        self.assertFalse(EstadoMonitoramento.objects.filter(estado_estavel="SUSPECT").exists())
        self.assertEqual(EventoAuditoria.objects.count(), 0)
        self.assertTrue(
            all(
                row["status"] is None
                and row["status_em"] is None
                and row["ultima_verificacao"] is None
                for row in Camera.objects.values("status", "status_em", "ultima_verificacao")
            )
        )

        print(
            "MON08C4_OFFLINE_RESTART_METRICS "
            f"reload_seconds={reload_duration:.6f} "
            f"reload_query_count={reload_queries} "
            f"reload_query_profile={dict(sorted(reload_profile.items()))} "
            f"post_restart_seconds={operation_duration:.6f} "
            f"post_restart_query_count={post_restart_queries} "
            f"post_restart_query_profile={dict(sorted(operation_profile.items()))} "
            f"pre_transitions={pre_restart_transition_count} "
            f"post_reload_transitions={post_reload_transition_count} "
            f"final_transitions={final_transitions} "
            f"pre_indisponibilidades={pre_restart_indisponibilidade_count} "
            f"post_reload_indisponibilidades={post_reload_indisponibilidade_count} "
            f"final_indisponibilidades={final_indisponibilidades.count()} "
            "restart_only_new_transitions=0 "
            "restart_only_new_indisponibilidades=0 "
            "sqlite_errors=0"
        )

    def test_scale_mon08c_stale_generation_rejects_2300_old_completions_without_side_effects(self):
        """SCALE/MON-08C-5: completions antigas não atravessam o CAS."""

        old_attempt_generation = 1
        current_generation = old_attempt_generation + 1
        self.assertEqual(connection.vendor, "sqlite")
        self._create_cameras()
        camera_ids = tuple(Camera.objects.order_by("pk").values_list("pk", flat=True))
        self.assertEqual(len(camera_ids), ASSET_COUNT)
        self.assertEqual(len(set(camera_ids)), ASSET_COUNT)

        repository = DjangoMonitoringRepository()
        prepared, _, _, _ = self._complete_round(
            repository,
            camera_ids,
            ProbeResult(ProbeResultCode.SUCCESS, START, duration_seconds=0),
        )
        pending_failure, _, _, _ = self._complete_round(
            repository,
            camera_ids,
            ProbeResult(ProbeResultCode.TIMEOUT, START + timedelta(seconds=1), duration_seconds=0),
        )

        pre_stale_state = self._state_snapshot()
        pre_stale_legacy = self._legacy_camera_snapshot()
        pre_stale_transition_count = TransicaoEstadoMonitoramento.objects.count()
        pre_stale_indisponibilidade_count = Indisponibilidade.objects.count()
        pre_stale_open_indisponibilidade_count = Indisponibilidade.objects.filter(
            closed_at__isnull=True
        ).count()
        pre_stale_audit_count = EventoAuditoria.objects.count()

        self.assertEqual(prepared, ASSET_COUNT)
        self.assertEqual(pending_failure, ASSET_COUNT)
        self.assertEqual(
            Counter(row[1] for row in pre_stale_state),
            Counter({TechnicalState.ONLINE.value: ASSET_COUNT}),
        )
        self.assertTrue(all(row[3] == 1 for row in pre_stale_state))
        self.assertEqual(pre_stale_transition_count, ASSET_COUNT)
        self.assertEqual(pre_stale_indisponibilidade_count, 0)
        self.assertEqual(pre_stale_open_indisponibilidade_count, 0)
        self.assertEqual(pre_stale_audit_count, 0)
        self.assertTrue(all(row[1] is None for row in pre_stale_legacy))
        self.assertTrue(all(row[2] is None for row in pre_stale_legacy))
        self.assertTrue(all(row[3] is None for row in pre_stale_legacy))

        persisted_schedule = tuple(
            EstadoMonitoramento.objects.order_by("camera_id").values_list(
                "camera_id",
                "proximo_vencimento_em",
                "ultima_geracao_configuracao",
            )
        )
        self.assertEqual(len(persisted_schedule), ASSET_COUNT)
        self.assertTrue(all(row[2] == old_attempt_generation for row in persisted_schedule))
        old_attempt_at = self._restart_at_from_persisted_due()
        old_candidates = tuple(
            ScheduleCandidate(camera_id, next_due_at, config_generation=generation)
            for camera_id, next_due_at, generation in persisted_schedule
        )

        old_attempts: list[tuple[DueScheduler, object]] = []
        for offset in range(0, ASSET_COUNT, 20):
            batch = old_candidates[offset : offset + 20]
            old_scheduler = self._scheduler(repository, old_attempt_at)
            report = old_scheduler.tick(old_attempt_at, batch)
            self.assertEqual(report.admitted, len(batch))
            self.assertEqual(report.queued, 0)
            self.assertEqual(report.active, len(batch))
            self.assertTrue(all(attempt.config_generation == old_attempt_generation for attempt in report.attempts))
            old_attempts.extend((old_scheduler, attempt) for attempt in report.attempts)

        self.assertEqual(len(old_attempts), ASSET_COUNT)
        self.assertEqual(
            Counter(attempt.config_generation for _, attempt in old_attempts),
            Counter({old_attempt_generation: ASSET_COUNT}),
        )

        generation_rows_updated = EstadoMonitoramento.objects.filter(
            ultima_geracao_configuracao=old_attempt_generation
        ).update(ultima_geracao_configuracao=current_generation)
        self.assertEqual(generation_rows_updated, ASSET_COUNT)
        self.assertEqual(
            Counter(EstadoMonitoramento.objects.values_list("ultima_geracao_configuracao", flat=True)),
            Counter({current_generation: ASSET_COUNT}),
        )
        self.assertEqual(repository.current_generation(camera_ids[0]), current_generation)
        before_stale_completion_state = self._state_snapshot()
        before_stale_completion_legacy = self._legacy_camera_snapshot()
        before_stale_completion_unavailabilities = self._unavailability_snapshot()

        stale_result = ProbeResult(
            ProbeResultCode.TIMEOUT,
            old_attempt_at + timedelta(seconds=1),
            duration_seconds=0,
        )
        stale_outcomes = []
        stale_query_counter = self._QueryCounter()
        stale_started = perf_counter()
        with connection.execute_wrapper(stale_query_counter):
            for old_scheduler, attempt in old_attempts:
                stale_outcomes.append(
                    old_scheduler.complete(
                        attempt.attempt_id,
                        stale_result,
                        stale_result.observed_at,
                    )
                )
        stale_duration = perf_counter() - stale_started

        post_stale_state = self._state_snapshot()
        post_stale_legacy = self._legacy_camera_snapshot()
        post_stale_unavailabilities = self._unavailability_snapshot()
        post_stale_transition_count = TransicaoEstadoMonitoramento.objects.count()
        post_stale_indisponibilidade_count = Indisponibilidade.objects.count()
        post_stale_open_indisponibilidade_count = Indisponibilidade.objects.filter(
            closed_at__isnull=True
        ).count()
        post_stale_audit_count = EventoAuditoria.objects.count()

        stale_rejected = sum(
            outcome.disposition is CompletionDisposition.CONFIG_CHANGED
            for outcome in stale_outcomes
        )
        stale_with_side_effect = sum(
            before != after
            for before, after in zip(before_stale_completion_state, post_stale_state)
        )
        stale_state_changes = sum(
            before[1] != after[1]
            for before, after in zip(before_stale_completion_state, post_stale_state)
        )
        stale_confirmation_memory_changes = sum(
            (before[2], before[3], before[4], before[8])
            != (after[2], after[3], after[4], after[8])
            for before, after in zip(before_stale_completion_state, post_stale_state)
        )
        stale_generation_overwrites = sum(
            before[7] != after[7]
            for before, after in zip(before_stale_completion_state, post_stale_state)
        )
        stale_next_due_overwrites = sum(
            before[6] != after[6]
            for before, after in zip(before_stale_completion_state, post_stale_state)
        )
        stale_legacy_changes = sum(
            before != after
            for before, after in zip(before_stale_completion_legacy, post_stale_legacy)
        )
        stale_new_transitions = post_stale_transition_count - pre_stale_transition_count
        stale_new_indisponibilidades = post_stale_indisponibilidade_count - pre_stale_indisponibilidade_count
        stale_closed_indisponibilidades = sum(
            before[3] is None and after[3] is not None
            for before, after in zip(
                before_stale_completion_unavailabilities,
                post_stale_unavailabilities,
            )
        )
        stale_functional_audit_events = post_stale_audit_count - pre_stale_audit_count

        self.assertEqual(len(stale_outcomes), ASSET_COUNT)
        self.assertTrue(all(outcome.disposition is CompletionDisposition.CONFIG_CHANGED for outcome in stale_outcomes))
        self.assertEqual(stale_rejected, ASSET_COUNT)
        self.assertEqual(stale_with_side_effect, 0)
        self.assertEqual(stale_state_changes, 0)
        self.assertEqual(stale_confirmation_memory_changes, 0)
        self.assertEqual(stale_generation_overwrites, 0)
        self.assertEqual(stale_next_due_overwrites, 0)
        self.assertEqual(stale_legacy_changes, 0)
        self.assertEqual(stale_new_transitions, 0)
        self.assertEqual(stale_new_indisponibilidades, 0)
        self.assertEqual(stale_closed_indisponibilidades, 0)
        self.assertEqual(post_stale_open_indisponibilidade_count, pre_stale_open_indisponibilidade_count)
        self.assertEqual(post_stale_unavailabilities, before_stale_completion_unavailabilities)
        self.assertEqual(stale_functional_audit_events, 0)
        self.assertEqual(
            Counter(row[1] for row in post_stale_state),
            Counter({TechnicalState.ONLINE.value: ASSET_COUNT}),
        )
        self.assertEqual(
            Counter(row[7] for row in post_stale_state),
            Counter({current_generation: ASSET_COUNT}),
        )
        self.assertFalse(EstadoMonitoramento.objects.filter(estado_estavel="SUSPECT").exists())

        control_camera_id = post_stale_state[0][0]
        control_next_due = post_stale_state[0][6]
        control_at = stale_result.observed_at + timedelta(seconds=1)
        control_scheduler = self._scheduler(repository, control_at)
        control_candidate = ScheduleCandidate(
            control_camera_id,
            control_next_due,
            config_generation=current_generation,
        )
        control_attempt = control_scheduler.tick(control_at, [control_candidate]).attempts[0]
        control_outcome = control_scheduler.complete(
            control_attempt.attempt_id,
            ProbeResult(ProbeResultCode.SUCCESS, control_at, duration_seconds=0),
            control_at,
        )
        controlled_state = EstadoMonitoramento.objects.get(camera_id=control_camera_id)
        self.assertEqual(control_outcome.disposition, CompletionDisposition.ACCEPTED)
        self.assertEqual(controlled_state.ultima_geracao_configuracao, current_generation)
        self.assertEqual(controlled_state.estado_estavel, TechnicalState.ONLINE.value)
        self.assertEqual(controlled_state.sequencia_negativa, 0)
        self.assertEqual(controlled_state.confirmacao_ultima_observacao_em, control_at)
        self.assertGreater(controlled_state.proximo_vencimento_em, control_next_due)

        stale_query_profile = dict(sorted(stale_query_counter.profile.items()))
        print(
            "MON08C5_METRICS "
            f"asset_count={ASSET_COUNT} "
            f"old_attempts={len(old_attempts)} "
            f"old_attempt_generation={old_attempt_generation} "
            f"current_generation={current_generation} "
            f"stale_completions_submitted={len(stale_outcomes)} "
            f"stale_completions_rejected={stale_rejected} "
            f"stale_completions_with_side_effect={stale_with_side_effect} "
            f"stale_state_changes={stale_state_changes} "
            f"stale_confirmation_memory_changes={stale_confirmation_memory_changes} "
            f"stale_generation_overwrites={stale_generation_overwrites} "
            f"stale_next_due_overwrites={stale_next_due_overwrites} "
            f"stale_new_transitions={stale_new_transitions} "
            f"stale_new_indisponibilidades={stale_new_indisponibilidades} "
            f"stale_closed_indisponibilidades={stale_closed_indisponibilidades} "
            f"stale_functional_audit_events={stale_functional_audit_events} "
            f"pre_stale_state_distribution={dict(Counter(row[1] for row in pre_stale_state))} "
            f"post_stale_state_distribution={dict(Counter(row[1] for row in post_stale_state))} "
            f"pre_stale_transition_count={pre_stale_transition_count} "
            f"post_stale_transition_count={post_stale_transition_count} "
            f"pre_stale_indisponibilidade_count={pre_stale_indisponibilidade_count} "
            f"post_stale_indisponibilidade_count={post_stale_indisponibilidade_count} "
            f"stale_duration_seconds={stale_duration:.6f} "
            f"stale_query_count={sum(stale_query_counter.profile.values())} "
            f"stale_query_profile={stale_query_profile} "
            "current_generation_completion_control=PASS "
            "persisted_suspect_count=0 "
            "real_persistence_path=scheduler->generation_validation->repository->Django_ORM->SQLite "
            "real_network_used=NO real_camera_used=NO real_credential_used=NO "
            "legacy_camera_technical_fields_changed=NO functional_audit_pollution=0 "
            "sqlite_errors=0"
        )
