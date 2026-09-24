"""Cenários focais da MON-09D: configuração e diagnóstico operacional."""

from datetime import datetime, timezone
import os
from unittest.mock import patch
from uuid import uuid4

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.test import SimpleTestCase

from cameras.monitoramento.confirmation import ConfirmationMemory, ConfirmationPolicy
from cameras.monitoramento.contracts import ProbeResult, ProbeResultCode
from cameras.monitoramento.fakes import FakeClock
from cameras.monitoramento.scheduler import DueScheduler
from cameras.monitoramento.schemas import (
    CompletionDisposition,
    MonitoringConfig,
    OwnershipLease,
    ScheduleCandidate,
    SchedulerLifecycle,
)
from config.environment import get_monitoring_config_from_environment


START = datetime(2026, 9, 23, tzinfo=timezone.utc)


def candidate(camera_id: int) -> ScheduleCandidate:
    return ScheduleCandidate(camera_id, START)


def success() -> ProbeResult:
    return ProbeResult(ProbeResultCode.SUCCESS, START, 0.0)


class StaleOwnershipPort:
    policy = ConfirmationPolicy(2, 1, "mon09d-v1")

    def claim(self, camera_id: int, _owner_id: str, _lease_seconds: int) -> OwnershipLease | None:
        return OwnershipLease(f"runtime-{camera_id}", 1)

    def release(self, _camera_id: int, _ownership: OwnershipLease) -> bool:
        return False

    def load(self, _candidate: ScheduleCandidate, policy: ConfirmationPolicy) -> ConfirmationMemory:
        return ConfirmationMemory.initial(policy.version)

    def store(self, *_args, **_kwargs) -> CompletionDisposition:
        return CompletionDisposition.OWNERSHIP_LOST


class MonitoringObservabilityTests(SimpleTestCase):
    def test_environment_binding_produces_validated_config(self):
        environment = {
            "ARGOS_MONITORING_CONCURRENCY": "3",
            "ARGOS_MONITORING_QUEUE_BOUND": "6",
            "ARGOS_MONITORING_CYCLE_INTERVAL_SECONDS": "90",
            "ARGOS_MONITORING_PROBE_TIMEOUT_SECONDS": "8",
            "ARGOS_MONITORING_CONNECT_TIMEOUT_SECONDS": "2",
            "ARGOS_MONITORING_SHUTDOWN_TIMEOUT_SECONDS": "11",
            "ARGOS_MONITORING_JITTER_RATIO": "0.15",
            "ARGOS_MONITORING_STALE_AFTER_SECONDS": "270",
            "ARGOS_MONITORING_HEARTBEAT_SECONDS": "20",
            "ARGOS_MONITORING_OWNERSHIP_LEASE_SECONDS": "9",
        }
        with patch.dict(os.environ, environment, clear=False):
            config = get_monitoring_config_from_environment()

        self.assertEqual((config.concurrency, config.queue_bound, config.cycle_interval_seconds), (3, 6, 90))
        self.assertEqual((config.probe_timeout_seconds, config.connect_timeout_seconds), (8.0, 2.0))
        self.assertEqual(config.ownership_lease_seconds, 9)
        self.assertIsInstance(settings.MONITORING_CONFIG, MonitoringConfig)

    def test_invalid_environment_configuration_fails_fast_with_a_clear_error(self):
        with patch.dict(os.environ, {"ARGOS_MONITORING_CONCURRENCY": "0"}, clear=False):
            with self.assertRaisesMessage(
                ImproperlyConfigured,
                "Configuração de monitoramento inválida: concurrency must be between 1 and 50",
            ):
                get_monitoring_config_from_environment()

    def test_default_lease_is_operationally_derived_but_configuration_remains_independent(self):
        short_shutdown = MonitoringConfig(shutdown_timeout_seconds=1)
        long_shutdown = MonitoringConfig(shutdown_timeout_seconds=300)
        longer_probe = MonitoringConfig(probe_timeout_seconds=8)

        self.assertEqual(short_shutdown.ownership_lease_seconds, long_shutdown.ownership_lease_seconds)
        self.assertEqual(longer_probe.ownership_lease_seconds, 9)
        self.assertEqual(MonitoringConfig(ownership_lease_seconds=1).ownership_lease_seconds, 1)

    def test_runtime_snapshot_exposes_lifecycle_backlog_and_attempt_counters(self):
        scheduler = DueScheduler(MonitoringConfig(concurrency=1, queue_bound=2), FakeClock(START))
        before = scheduler.runtime_status
        self.assertEqual(before.scheduler_state, SchedulerLifecycle.STARTING)
        self.assertEqual((before.in_flight, before.queued), (0, 0))

        report = scheduler.tick(START, [candidate(1), candidate(2), candidate(3)])
        active = report.attempts[0]
        running = scheduler.runtime_status
        self.assertEqual(running.scheduler_state, SchedulerLifecycle.RUNNING)
        self.assertEqual((running.in_flight, running.queued), (1, 1))
        self.assertEqual((running.configured_concurrency, running.queue_capacity), (1, 2))
        self.assertEqual((running.cycles_started, running.cycles_completed, running.attempts_started), (1, 1, 1))
        self.assertEqual(running.last_cycle_started_at, START)
        self.assertEqual(running.last_cycle_completed_at, START)

        scheduler.request_shutdown(START)
        scheduler.complete(active.attempt_id, success(), START)
        stopped = scheduler.runtime_status
        self.assertEqual(stopped.scheduler_state, SchedulerLifecycle.STOPPED)
        self.assertEqual((stopped.attempts_completed, stopped.attempts_cancelled), (1, 1))

    def test_operational_failure_is_diagnostic_and_is_not_a_probe_outcome(self):
        scheduler = DueScheduler(MonitoringConfig(), FakeClock(START))
        with self.assertLogs("cameras.monitoramento.scheduler", level="WARNING") as logs:
            scheduler.report_repository_failure("REPOSITORY_UNAVAILABLE")

        status = scheduler.runtime_status
        self.assertEqual(status.scheduler_state, SchedulerLifecycle.DEGRADED)
        self.assertEqual((status.operational_failures, status.last_operational_error), (1, "REPOSITORY_UNAVAILABLE"))
        self.assertIn("MONITORING_OPERATIONAL_FAILURE error_code=REPOSITORY_UNAVAILABLE", logs.output[0])

    def test_ownership_denial_and_stale_completion_are_visible_without_domain_history(self):
        class DeniedOwnershipPort(StaleOwnershipPort):
            def claim(self, _camera_id: int, _owner_id: str, _lease_seconds: int) -> OwnershipLease | None:
                return None

        # O mesmo adapter é obrigatório para preservar a fronteira atômica.
        denied_port = DeniedOwnershipPort()
        denied = DueScheduler(
            MonitoringConfig(concurrency=1, queue_bound=1),
            FakeClock(START),
            ownership_port=denied_port,
            confirmation_port=denied_port,
            confirmation_policy=denied_port.policy,
            service_instance_id="worker-a",
        )
        denied.tick(START, [candidate(1)])
        self.assertEqual((denied.runtime_status.ownership_denied, denied.runtime_status.in_flight), (1, 0))

        stale_port = StaleOwnershipPort()
        stale = DueScheduler(
            MonitoringConfig(concurrency=1, queue_bound=1),
            FakeClock(START),
            ownership_port=stale_port,
            confirmation_port=stale_port,
            confirmation_policy=stale_port.policy,
            service_instance_id="worker-a",
            attempt_id_factory=uuid4,
        )
        attempt = stale.tick(START, [candidate(2)]).attempts[0]
        outcome = stale.complete(attempt.attempt_id, success(), START)
        status = stale.runtime_status
        self.assertEqual(outcome.disposition, CompletionDisposition.OWNERSHIP_LOST)
        self.assertEqual((status.ownership_acquired, status.stale_owner_completions_rejected), (1, 1))
        self.assertGreaterEqual(status.ownership_lost, 1)
