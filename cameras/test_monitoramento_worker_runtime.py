from __future__ import annotations

import asyncio
from datetime import date, datetime, timezone
from threading import Event
from unittest import IsolatedAsyncioTestCase, TestCase
from unittest.mock import patch
from uuid import uuid4

from django.contrib.auth import get_user_model
from django.test import TransactionTestCase

from cameras.integracao.diagnostics import run_automatic_camera_diagnostic
from cameras.integracao.rtsp.fake import FakeRtspAdapter
from cameras.integracao.rtsp.ports import RtspStage, StageStatus
from cameras.integracao.target_policy import TargetPolicy
from cameras.integracao.diagnostics import ConnectionTestResult, DiagnosticSource, HealthStageResult
from cameras.monitoramento.confirmation import ConfirmationMemory, ConfirmationPolicy
from cameras.monitoramento.contracts import ProbeResult, ProbeResultCode
from cameras.monitoramento.observability import NoopTelemetry
from cameras.monitoramento.runtime import MonitoringWorkerRuntime, RuntimeDependencies, RuntimePreflightError
from cameras.monitoramento.repository import DueCandidatePage, DjangoMonitoringRepository
from cameras.monitoramento.schemas import (
    CompletionDisposition, MonitoringConfig, OwnershipLease, ScheduleCandidate,
)

NOW = datetime(2026, 10, 10, tzinfo=timezone.utc)
POLICY = ConfirmationPolicy(2, 1, "mon-runtime-v1")
TARGET_POLICY = TargetPolicy(
    allowed_cidrs=("10.0.0.0/8",),
    ports_by_scheme={"rtsp": (554,)},
    allowed_paths_by_scheme={"rtsp": ("/stream-a",)},
)


def diagnostic(camera_id: int, config_generation: int, **_kwargs) -> ConnectionTestResult:
    result = ProbeResult(ProbeResultCode.INCONCLUSIVE, NOW, 0.01)
    stages = tuple(HealthStageResult(stage, StageStatus.NOT_RUN, NOW, 0) for stage in RtspStage)
    return ConnectionTestResult(camera_id, stages, 1, config_generation, DiagnosticSource.AUTOMATIC, uuid4(), result)


class MemoryRepository:
    def __init__(self, diagnostic_fn=diagnostic):
        self.items = [ScheduleCandidate(1, NOW)]
        self.stores = 0
        self.claims = 0
        self.releases = 0
        self.diagnostic_fn = diagnostic_fn

    def list_due_page(self, now, limit, *, after_camera_id=0, exclude_camera_ids=()):
        items = tuple(item for item in self.items if item.camera_id > after_camera_id and item.camera_id not in exclude_camera_ids)[:limit]
        return DueCandidatePage(items, items[-1].camera_id if items else after_camera_id, False)

    def list_due(self, now, limit, *, after_camera_id=0, exclude_camera_ids=()):
        return self.list_due_page(now, limit, after_camera_id=after_camera_id, exclude_camera_ids=exclude_camera_ids).candidates

    def current_generation(self, _camera_id):
        return 1

    def is_eligible(self, _camera_id):
        return True

    def claim(self, _camera_id, owner_id, _lease_seconds):
        self.claims += 1
        return OwnershipLease(owner_id, self.claims)

    def release(self, _camera_id, _ownership):
        self.releases += 1
        return True

    def load(self, _candidate, policy):
        return ConfirmationMemory.initial(policy.version)

    def store(self, *_args, **_kwargs):
        self.stores += 1
        return True


class Telemetry(NoopTelemetry):
    def __init__(self):
        self.heartbeats = 0
        self.heartbeat_event = asyncio.Event()
        self.draining_event = asyncio.Event()

    def emit_event(self, name, _fields):
        if _fields.get("state") == "DRAINING":
            self.draining_event.set()
        if name == "monitoring.worker.heartbeat":
            self.heartbeats += 1
            self.heartbeat_event.set()


def make_runtime(repository=None, *, config=None, **kwargs):
    repository = repository or MemoryRepository()
    deps = RuntimeDependencies(
        config=config or MonitoringConfig(concurrency=1, queue_bound=1),
        confirmation_policy=POLICY,
        target_policy=TARGET_POLICY,
        repository=repository,
        telemetry=kwargs.pop("telemetry", Telemetry()),
        diagnostic=kwargs.pop("diagnostic", diagnostic),
        database_preflight=kwargs.pop("database_preflight", lambda: None),
        adapter_preflight=kwargs.pop("adapter_preflight", lambda: None),
        credential_preflight=kwargs.pop("credential_preflight", lambda: None),
    )
    return MonitoringWorkerRuntime(deps), repository, deps.telemetry


class WorkerRuntimeTests(IsolatedAsyncioTestCase):
    async def test_preflight_fails_closed_before_database_or_adapter_checks(self):
        calls = []
        runtime, _repo, _telemetry = make_runtime(
            database_preflight=lambda: calls.append("database"),
            adapter_preflight=lambda: calls.append("adapter"),
        )
        runtime.dependencies = RuntimeDependencies(
            config=runtime.config, confirmation_policy=POLICY, target_policy=object(),
            repository=runtime.repository, telemetry=NoopTelemetry(),
            database_preflight=lambda: calls.append("database"), adapter_preflight=lambda: calls.append("adapter"),
        )
        with self.assertRaises(RuntimePreflightError) as error:
            await runtime.preflight()
        self.assertEqual(error.exception.code, "TARGET_POLICY_INVALID")
        self.assertEqual(calls, [])
        self.assertEqual(runtime.scheduler.active_count, 0)

    async def test_once_runs_runtime_to_core_completion_and_independent_heartbeat(self):
        runtime, repository, telemetry = make_runtime()
        graceful = await runtime.run(once=True)
        self.assertTrue(graceful)
        self.assertEqual(repository.claims, 1)
        self.assertEqual(repository.stores, 1)
        self.assertEqual(repository.releases, 0)  # completion consumes ownership atomically
        self.assertGreaterEqual(telemetry.heartbeats, 1)
        self.assertEqual(runtime.scheduler.active_count, 0)

    async def test_database_deadline_keeps_operation_tracked_until_it_returns(self):
        entered = Event()
        finish = Event()

        class SlowRepository(MemoryRepository):
            def list_due_page(self, now, limit, **kwargs):
                entered.set()
                finish.wait()
                return super().list_due_page(now, limit, **kwargs)

        config = MonitoringConfig(
            concurrency=1, queue_bound=1, probe_timeout_seconds=1, connect_timeout_seconds=1,
            db_operation_deadline_seconds=0.1, shutdown_timeout_seconds=2,
        )
        runtime, repository, _telemetry = make_runtime(SlowRepository(), config=config)
        run = asyncio.create_task(runtime.run(once=True))
        self.assertTrue(await asyncio.to_thread(entered.wait, 3))
        await asyncio.wait_for(runtime._operation_deadline_event.wait(), timeout=2)
        self.assertIsNotNone(runtime._database_pending)
        self.assertEqual(runtime.scheduler.active_count, 0)
        finish.set()
        self.assertFalse(await asyncio.wait_for(run, timeout=5))
        self.assertTrue(runtime.incomplete)
        self.assertEqual(repository.stores, 0)

    async def test_shutdown_drains_active_attempt_without_cancelling_its_thread(self):
        entered = Event()
        finish = Event()

        def blocked_diagnostic(camera_id, config_generation, **_kwargs):
            entered.set()
            finish.wait()
            return diagnostic(camera_id, config_generation)

        runtime, repository, telemetry = make_runtime(diagnostic=blocked_diagnostic)
        run = asyncio.create_task(runtime.run(once=True))
        self.assertTrue(await asyncio.to_thread(entered.wait, 3))
        try:
            await asyncio.wait_for(telemetry.draining_event.wait(), timeout=3)
            self.assertEqual(runtime.scheduler.active_count, 1)
            self.assertEqual(repository.releases, 0)
        finally:
            finish.set()
        self.assertTrue(await asyncio.wait_for(run, timeout=5))
        self.assertEqual(repository.stores, 1)

    async def test_blocking_diagnostic_does_not_block_event_loop_or_heartbeat_task(self):
        entered = Event()
        finish = Event()

        def blocked_diagnostic(camera_id, config_generation, **_kwargs):
            entered.set()
            finish.wait()
            return diagnostic(camera_id, config_generation)

        runtime, repository, telemetry = make_runtime(diagnostic=blocked_diagnostic)
        run = asyncio.create_task(runtime.run(once=True))
        self.assertTrue(await asyncio.to_thread(entered.wait, 3))
        await asyncio.wait_for(telemetry.heartbeat_event.wait(), timeout=1)
        self.assertEqual(runtime.scheduler.active_count, 1)
        finish.set()
        self.assertTrue(await asyncio.wait_for(run, timeout=5))
        self.assertEqual(repository.stores, 1)

    async def test_recovery_is_serial_bounded_and_resets_after_database_returns(self):
        calls = []

        def database_preflight():
            calls.append(len(calls) + 1)
            if len(calls) == 1:
                raise RuntimeError("temporary failure")

        runtime, _repository, _telemetry = make_runtime(database_preflight=database_preflight)
        runtime.scheduler.report_repository_failure("DATABASE_UNAVAILABLE")
        runtime._recovery_delay = 0

        async def skip_delay(awaitable, timeout=None):
            awaitable.close()
            raise TimeoutError

        with patch("cameras.monitoramento.runtime.asyncio.wait_for", new=skip_delay):
            await runtime._recover()

        self.assertEqual(calls, [1, 2])
        self.assertEqual(runtime.scheduler.lifecycle.value, "RUNNING")
        self.assertIsNone(runtime._recovery_started)
        self.assertEqual(runtime._recovery_attempts, 0)
        self.assertFalse(runtime.incomplete)

    async def test_recovery_stops_at_attempt_budget_without_overlapping_checks(self):
        active = 0
        max_active = 0
        calls = 0

        def database_preflight():
            nonlocal active, max_active, calls
            calls += 1
            active += 1
            max_active = max(max_active, active)
            try:
                raise RuntimeError("persistent failure")
            finally:
                active -= 1

        config = MonitoringConfig(recovery_max_attempts=2, recovery_max_elapsed_seconds=900)
        runtime, _repository, _telemetry = make_runtime(config=config, database_preflight=database_preflight)
        runtime.scheduler.report_repository_failure("DATABASE_UNAVAILABLE")
        runtime._recovery_delay = 0

        async def skip_delay(awaitable, timeout=None):
            awaitable.close()
            raise TimeoutError

        with patch("cameras.monitoramento.runtime.asyncio.wait_for", new=skip_delay):
            await runtime._recover()

        self.assertEqual(calls, 2)
        self.assertEqual(max_active, 1)
        self.assertTrue(runtime.incomplete)
        self.assertEqual(runtime.scheduler.lifecycle.value, "DEGRADED")


class WorkerConfigTests(TestCase):
    def test_v1_defaults_and_cross_budget_validation(self):
        config = MonitoringConfig()
        self.assertEqual(config.db_operation_deadline_seconds, 5)
        self.assertEqual(config.recovery_max_attempts, 5)
        self.assertEqual(config.recovery_max_elapsed_seconds, 900)
        for kwargs in (
            {"db_operation_deadline_seconds": 30, "shutdown_timeout_seconds": 30},
            {"probe_timeout_seconds": 16, "shutdown_timeout_seconds": 30},
            {"recovery_max_elapsed_seconds": 30},
            {"recovery_max_attempts": True},
            {"db_operation_deadline_seconds": float("nan")},
            {"db_operation_deadline_seconds": float("inf")},
            {"recovery_max_elapsed_seconds": float("nan")},
            {"recovery_max_elapsed_seconds": float("inf")},
            {"recovery_max_elapsed_seconds": 3601},
        ):
            with self.subTest(kwargs=kwargs), self.assertRaises((TypeError, ValueError)):
                MonitoringConfig(**kwargs)


class WorkerRuntimeIntegrationTests(TransactionTestCase):
    def test_runtime_composes_due_page_core_automatic_diagnostic_and_atomic_snapshot(self):
        from cameras.models import (
            Camera,
            CameraCapabilityEvidence,
            CameraCapabilityProfile,
            CameraConnectionConfig,
            CameraHealthSnapshot,
            EstadoMonitoramento,
            TransicaoEstadoMonitoramento,
        )
        from cameras.monitoramento.confirmation import TechnicalState

        reviewer = get_user_model().objects.create_user(username="runtime-integration-reviewer")
        camera = Camera.objects.create(
            nome="Runtime Integration Camera", fabricante="Vendor", modelo="Model",
            serial="RUNTIME-1", mac="00:11:22:33:44:66", tipo=Camera.TipoCamera.BULLET,
            terminal="T", pavimento="P", setor="S", ambiente="A", ponto_referencia="PR",
            farm="F", codec="H264", ip="10.0.0.15", mascara_subrede="255.255.255.0",
            gateway="10.0.0.1", vlan=10, retencao_esperada_dias=30,
            situacao_operacional=Camera.SituacaoOperacional.PRODUCAO,
        )
        # TransactionTestCase can run after another test has flushed migration
        # data; ensure the canonical profile exists in either ordering.
        profile, _created = CameraCapabilityProfile.objects.get_or_create(
            profile_key="RTSP_DISCOVERY_V1", version=1,
            defaults={
                "active": True,
                "adapter_key": CameraCapabilityProfile.Adapter.RTSP,
                "allowed_schemes": ["rtsp"],
                "allowed_ports": [554],
                "tls_policy": CameraCapabilityProfile.TLSPolicy.NOT_APPLICABLE,
                "auth_method": CameraCapabilityProfile.AuthMethod.RTSP_NEGOTIATE,
                "credential_required": False,
                "endpoint_policy": CameraCapabilityProfile.EndpointPolicy.TECHNICIAN_OVERRIDE,
                "default_path": "",
                "allowed_override_fields": ["path", "port"],
                "probe_evidence_stage": CameraCapabilityProfile.ProbeStage.B,
                "source_ref": "MON-RUNTIME-V1 SQLite integration fixture",
            },
        )
        CameraCapabilityEvidence.objects.create(
            profile=profile, camera=camera, vendor="Vendor", model="Model", firmware_exact="",
            status=CameraCapabilityEvidence.Status.SUPPORTED,
            source_type=CameraCapabilityEvidence.SourceType.LAB,
            source_ref="MON-RUNTIME-V1 SQLite integration fixture",
            evidence_date=date(2026, 10, 10), reviewer=reviewer,
        )
        CameraConnectionConfig.objects.create(
            camera=camera, profile=profile, enabled=True,
            rtsp_uri="rtsp://10.0.0.15:554/stream-a", config_version=1,
        )

        now = lambda: datetime.now(timezone.utc)
        adapter = FakeRtspAdapter(monotonic=lambda: 1.0, now=now)

        def automatic_diagnostic(**kwargs):
            return run_automatic_camera_diagnostic(
                **kwargs, adapter=adapter, monotonic=lambda: 1.0, now=now,
            )

        dependencies = RuntimeDependencies(
            config=MonitoringConfig(concurrency=1, queue_bound=1),
            confirmation_policy=POLICY,
            target_policy=TARGET_POLICY,
            repository=DjangoMonitoringRepository(),
            telemetry=Telemetry(),
            diagnostic=automatic_diagnostic,
            database_preflight=lambda: None,
            adapter_preflight=lambda: None,
            credential_preflight=lambda: None,
        )
        runtime = MonitoringWorkerRuntime(dependencies)

        self.assertTrue(asyncio.run(runtime.run(once=True)))

        state = EstadoMonitoramento.objects.get(camera=camera)
        snapshot = CameraHealthSnapshot.objects.get(camera=camera)
        self.assertEqual(state.estado_estavel, TechnicalState.ONLINE.value)
        self.assertIsNone(state.monitoring_owner_id)
        self.assertEqual(TransicaoEstadoMonitoramento.objects.count(), 1)
        self.assertEqual(snapshot.config_generation, state.ultima_geracao_configuracao)
        self.assertEqual(snapshot.stage_d_state, StageStatus.PASS.value)
        self.assertEqual(adapter.calls, 1)
