"""Laboratório sintético local da MON-05B-FIX.

Todos os cenários usam relógio injetado e objetos puros. Não há câmera real,
rede, ORM, migration, worker ou ``sleep`` de sincronização.
"""

import asyncio
from datetime import datetime, timedelta, timezone
import inspect
import unittest
from uuid import UUID

from .monitoramento.confirmation import (
    ConfirmationMemory,
    ConfirmationPolicy,
    TechnicalDecisionAction,
    TechnicalState,
)
from .monitoramento.contracts import ProbeResult, ProbeResultCode
from .monitoramento.fakes import FakeClock
from .monitoramento.schemas import (
    AttemptState,
    CompletionDisposition,
    MonitoringConfig,
    ScheduleCandidate,
    SchedulerLifecycle,
)
from .monitoramento.scheduler import (
    DueScheduler,
    deterministic_jitter_seconds,
    execute_bounded,
    next_due_at,
)


START_AT = datetime(2026, 8, 21, 12, 0, tzinfo=timezone.utc)


def candidate(camera_id: int, due_at: datetime = START_AT, *, generation: int = 1, eligible: bool = True) -> ScheduleCandidate:
    return ScheduleCandidate(camera_id, due_at, config_generation=generation, eligible=eligible)


def result(code: ProbeResultCode, at: datetime) -> ProbeResult:
    return ProbeResult(code=code, observed_at=at, duration_seconds=0.0)


class MemoryConfirmationPort:
    def __init__(self, policy: ConfirmationPolicy) -> None:
        self.policy = policy
        self.memory: dict[int, ConfirmationMemory] = {}
        self.stores = 0

    def load(self, candidate: ScheduleCandidate, policy: ConfirmationPolicy) -> ConfirmationMemory:
        return self.memory.setdefault(candidate.camera_id, ConfirmationMemory.initial(policy.version))

    def store(self, candidate: ScheduleCandidate, _result: ProbeResult, memory: ConfirmationMemory, _decision: object, _next_due_at: datetime) -> None:
        self.stores += 1
        self.memory[candidate.camera_id] = memory


class MonitoringConfigTests(unittest.TestCase):
    def test_defaults_and_bounds(self) -> None:
        config = MonitoringConfig()
        self.assertEqual((config.concurrency, config.queue_bound, config.cycle_interval_seconds), (20, 40, 300))
        for overrides in ({"concurrency": 0}, {"concurrency": 51}, {"queue_bound": 19}, {"shutdown_timeout_seconds": 0}, {"jitter_ratio": .21}):
            with self.subTest(overrides=overrides), self.assertRaises((TypeError, ValueError)):
                MonitoringConfig(**overrides)

    def test_config_and_attempts_are_immutable(self) -> None:
        with self.assertRaises(AttributeError):
            MonitoringConfig().concurrency = 2
        attempt = next(iter(DueScheduler(MonitoringConfig(concurrency=1), FakeClock(start_at=START_AT)).tick(START_AT, [candidate(1)]).attempts))
        with self.assertRaises(AttributeError):
            attempt.state = AttemptState.COMPLETED


class SchedulerContractTests(unittest.TestCase):
    def make_scheduler(self, *, concurrency: int = 2, queue_bound: int | None = None, generation=None, eligible=None, port=None) -> tuple[DueScheduler, FakeClock]:
        clock = FakeClock(start_at=START_AT)
        config = MonitoringConfig(concurrency=concurrency, queue_bound=queue_bound, shutdown_timeout_seconds=5)
        scheduler = DueScheduler(config, clock, current_generation=generation, is_eligible=eligible, confirmation_port=port, confirmation_policy=port.policy if port else None)
        return scheduler, clock

    def test_due_based_continuous_scheduler_and_individual_next_due(self) -> None:
        scheduler, clock = self.make_scheduler(concurrency=1)
        first = scheduler.tick(START_AT, [candidate(1)]).attempts[0]
        clock.advance(1)
        completed = scheduler.complete(first.attempt_id, result(ProbeResultCode.SUCCESS, clock.now()))
        self.assertEqual(completed.disposition, CompletionDisposition.ACCEPTED)
        self.assertEqual(scheduler.lifecycle, SchedulerLifecycle.RUNNING)
        self.assertGreater(completed.next_due_at, clock.now())
        self.assertEqual(scheduler.tick(START_AT + timedelta(seconds=2), [candidate(1, START_AT)]).admitted, 0)
        # A câmera 2 pode ser admitida sem aguardar a next_due da câmera 1.
        second = scheduler.tick(START_AT + timedelta(seconds=2), [candidate(2, START_AT)]).attempts
        self.assertEqual(len(second), 1)
        self.assertEqual(second[0].camera_id, 2)

    def test_oldest_due_first_and_camera_vacancy_admits_next_candidate(self) -> None:
        scheduler, clock = self.make_scheduler(concurrency=2, queue_bound=3)
        report = scheduler.tick(START_AT, [candidate(3, START_AT), candidate(1, START_AT - timedelta(seconds=3)), candidate(2, START_AT - timedelta(seconds=2))])
        self.assertEqual([attempt.camera_id for attempt in report.attempts], [1, 2])
        self.assertEqual(scheduler.queued_count, 1)
        first = scheduler.active_attempts[0]
        scheduler.complete(first.attempt_id, result(ProbeResultCode.SUCCESS, clock.now()))
        self.assertEqual(scheduler.active_count, 2)
        self.assertIn(3, {attempt.camera_id for attempt in scheduler.active_attempts})

    def test_bounded_active_queue_and_no_storm_for_2300(self) -> None:
        scheduler, _ = self.make_scheduler(concurrency=20, queue_bound=40)
        report = scheduler.tick(START_AT, [candidate(camera_id, START_AT - timedelta(seconds=camera_id % 7)) for camera_id in range(1, 2301)])
        self.assertEqual((report.eligible, report.due, report.admitted, report.deferred), (2300, 2300, 40, 2260))
        self.assertLessEqual(report.active, 20)
        self.assertLessEqual(report.queued, 40)
        self.assertEqual(len({attempt.attempt_id for attempt in scheduler.attempts}), 40)
        self.assertEqual(len({attempt.camera_id for attempt in scheduler.active_attempts}), scheduler.active_count)

    def test_attempt_identity_active_uniqueness_and_duplicate_completion_noop(self) -> None:
        policy = ConfirmationPolicy(2, 1, "v1")
        port = MemoryConfirmationPort(policy)
        scheduler, clock = self.make_scheduler(concurrency=1, port=port)
        first = scheduler.tick(START_AT, [candidate(1)]).attempts[0]
        self.assertIsInstance(first.attempt_id, UUID)
        self.assertEqual(scheduler.active_count, 1)
        self.assertFalse(scheduler.tick(START_AT, [candidate(1)]).attempts)
        accepted = scheduler.complete(first.attempt_id, result(ProbeResultCode.SUCCESS, clock.now()))
        duplicate = scheduler.complete(first.attempt_id, result(ProbeResultCode.SUCCESS, clock.now()))
        self.assertEqual(accepted.decision.action, TechnicalDecisionAction.CONFIRM_ONLINE)
        self.assertEqual(duplicate.disposition, CompletionDisposition.DUPLICATE)
        self.assertEqual(port.stores, 1)

    def test_old_attempt_is_discarded_after_a_new_current_attempt(self) -> None:
        scheduler, clock = self.make_scheduler(concurrency=1)
        old = scheduler.tick(START_AT, [candidate(1)]).attempts[0]
        first = scheduler.complete(old.attempt_id, result(ProbeResultCode.SUCCESS, clock.now()))
        new = scheduler.tick(first.next_due_at, [candidate(1, first.next_due_at)]).attempts[0]
        self.assertEqual(scheduler.complete(old.attempt_id, result(ProbeResultCode.SUCCESS, clock.now())).disposition, CompletionDisposition.OLD_ATTEMPT)
        self.assertEqual(new.state, AttemptState.ACTIVE)

    def test_out_of_order_result_is_handled_by_mon04_without_transition(self) -> None:
        policy = ConfirmationPolicy(2, 1, "v1")
        port = MemoryConfirmationPort(policy)
        scheduler, clock = self.make_scheduler(concurrency=1, port=port)
        first = scheduler.tick(START_AT, [candidate(1)]).attempts[0]
        scheduler.complete(first.attempt_id, result(ProbeResultCode.SUCCESS, clock.now() + timedelta(seconds=2)))
        second_due = scheduler.next_due[1]
        second = scheduler.tick(second_due, [candidate(1, second_due)]).attempts[0]
        outcome = scheduler.complete(second.attempt_id, result(ProbeResultCode.SUCCESS, START_AT))
        self.assertEqual(outcome.disposition, CompletionDisposition.ACCEPTED)
        self.assertEqual(outcome.decision.action, TechnicalDecisionAction.NO_CHANGE)
        self.assertEqual(port.stores, 2)

    def test_generation_changed_and_eligibility_lost_are_discarded_before_confirmation(self) -> None:
        generation = {1: 1, 2: 1}
        eligible = {1: True, 2: True}
        policy = ConfirmationPolicy(2, 1, "v1")
        port = MemoryConfirmationPort(policy)
        scheduler, clock = self.make_scheduler(concurrency=2, generation=generation.__getitem__, eligible=eligible.__getitem__, port=port)
        changed = scheduler.tick(START_AT, [candidate(1), candidate(2)]).attempts
        generation[1] = 2
        eligible[2] = False
        changed_outcome = scheduler.complete(changed[0].attempt_id, result(ProbeResultCode.SUCCESS, clock.now()))
        lost_outcome = scheduler.complete(changed[1].attempt_id, result(ProbeResultCode.SUCCESS, clock.now()))
        self.assertEqual(changed_outcome.disposition, CompletionDisposition.CONFIG_CHANGED)
        self.assertEqual(lost_outcome.disposition, CompletionDisposition.ELIGIBILITY_LOST)
        self.assertEqual(port.stores, 0)
        self.assertEqual(scheduler.lifecycle, SchedulerLifecycle.RUNNING)

    def test_mon04_reducer_is_used_only_after_validation_and_cancel_is_not_failure(self) -> None:
        policy = ConfirmationPolicy(2, 2, "v1")
        port = MemoryConfirmationPort(policy)
        scheduler, clock = self.make_scheduler(concurrency=1, port=port)
        active = scheduler.tick(START_AT, [candidate(1)]).attempts[0]
        accepted = scheduler.complete(active.attempt_id, result(ProbeResultCode.SUCCESS, clock.now()))
        self.assertEqual(accepted.decision.action, TechnicalDecisionAction.NO_CHANGE)
        self.assertEqual(port.memory[1].positive_streak, 1)
        next_attempt = scheduler.tick(accepted.next_due_at, [candidate(1, accepted.next_due_at)]).attempts[0]
        cancelled = scheduler.complete(next_attempt.attempt_id, result(ProbeResultCode.CANCELLED, clock.now()))
        self.assertEqual(cancelled.disposition, CompletionDisposition.CANCELLED)
        self.assertEqual(port.memory[1].positive_streak, 1)

    def test_lifecycle_draining_blocks_admission_and_allows_active_completion(self) -> None:
        scheduler, clock = self.make_scheduler(concurrency=1, queue_bound=1)
        active = scheduler.tick(START_AT, [candidate(1)]).attempts[0]
        self.assertEqual(scheduler.request_shutdown(), SchedulerLifecycle.DRAINING)
        self.assertEqual(scheduler.tick(clock.now(), [candidate(2)]).admitted, 0)
        scheduler.complete(active.attempt_id, result(ProbeResultCode.SUCCESS, clock.now()))
        self.assertEqual(scheduler.lifecycle, SchedulerLifecycle.STOPPED)
        self.assertEqual(scheduler.tick(clock.now(), [candidate(3)]).admitted, 0)

    def test_shutdown_timeout_cancels_active_without_confirmation_failure(self) -> None:
        policy = ConfirmationPolicy(2, 1, "v1")
        port = MemoryConfirmationPort(policy)
        scheduler, clock = self.make_scheduler(concurrency=1, port=port)
        active = scheduler.tick(START_AT, [candidate(1)]).attempts[0]
        scheduler.request_shutdown()
        clock.advance(5)
        scheduler.tick(clock.now())
        self.assertEqual(scheduler.lifecycle, SchedulerLifecycle.STOPPED)
        self.assertEqual(scheduler.attempts[0].state, AttemptState.CANCELLED)
        self.assertEqual(port.stores, 0)

    def test_shutdown_cancels_queued_attempts_without_leaking_queue_state(self) -> None:
        scheduler, _ = self.make_scheduler(concurrency=1, queue_bound=2)
        scheduler.tick(START_AT, [candidate(1), candidate(2)])
        scheduler.request_shutdown()
        self.assertEqual(scheduler.lifecycle, SchedulerLifecycle.DRAINING)
        scheduler.complete(scheduler.active_attempts[0].attempt_id, result(ProbeResultCode.SUCCESS, START_AT))
        self.assertEqual(scheduler.lifecycle, SchedulerLifecycle.STOPPED)
        self.assertEqual(scheduler.queued_count, 0)
        self.assertEqual({attempt.state for attempt in scheduler.attempts}, {AttemptState.COMPLETED, AttemptState.CANCELLED})

    def test_repository_failure_is_degraded_not_probe_failure(self) -> None:
        scheduler, _ = self.make_scheduler()
        self.assertEqual(scheduler.report_repository_failure("REPOSITORY_UNAVAILABLE"), SchedulerLifecycle.DEGRADED)
        self.assertEqual(scheduler.tick(START_AT, [candidate(1)]).admitted, 0)
        self.assertEqual(scheduler.operational_error, "REPOSITORY_UNAVAILABLE")

    def test_restart_rebuilds_due_work_with_bounds(self) -> None:
        scheduler, clock = self.make_scheduler(concurrency=5, queue_bound=10)
        active = scheduler.tick(START_AT, [candidate(1)]).attempts[0]
        scheduler.request_shutdown()
        scheduler.complete(active.attempt_id, result(ProbeResultCode.SUCCESS, clock.now()))
        report = scheduler.restart([candidate(i) for i in range(1, 501)], clock.now())
        self.assertEqual(report.admitted, 10)
        self.assertLessEqual(report.active, 5)
        self.assertLessEqual(report.queued, 10)

    def test_scheduler_source_has_no_operational_dependencies_or_fixed_delay(self) -> None:
        source = inspect.getsource(__import__("cameras.monitoramento.scheduler", fromlist=["DueScheduler"]))
        for forbidden in ("import django", "import socket", "import requests", "sleep(", "FixedDelayScheduler", "finish_cycle"):
            self.assertNotIn(forbidden, source)

    def test_jitter_is_deterministic_and_bounded(self) -> None:
        config = MonitoringConfig()
        value = deterministic_jitter_seconds(7, 3, interval_seconds=config.cycle_interval_seconds, jitter_ratio=config.jitter_ratio)
        self.assertEqual(value, deterministic_jitter_seconds(7, 3, interval_seconds=300, jitter_ratio=.10))
        self.assertLessEqual(abs(value), 30)
        self.assertEqual(next_due_at(START_AT, 7, 3, config).tzinfo, timezone.utc)


class BoundedExecutorLaboratoryTests(unittest.IsolatedAsyncioTestCase):
    async def test_executor_creates_bounded_workers_and_preserves_order(self) -> None:
        calls = 0

        async def handler(item: int) -> int:
            nonlocal calls
            calls += 1
            return item * 2

        results = await execute_bounded(range(100), handler, concurrency=7)
        self.assertEqual(results, tuple(index * 2 for index in range(100)))
        self.assertEqual(calls, 100)


class ScaleLaboratoryTests(unittest.TestCase):
    def test_required_scales(self) -> None:
        for size in (50, 100, 500, 2300):
            with self.subTest(size=size):
                config = MonitoringConfig(concurrency=20, queue_bound=40)
                scheduler = DueScheduler(config, FakeClock(start_at=START_AT))
                report = scheduler.tick(START_AT, [candidate(i) for i in range(1, size + 1)])
                self.assertLessEqual(report.active, config.concurrency)
                self.assertLessEqual(report.queued, config.queue_bound)
                self.assertEqual(len({attempt.camera_id for attempt in scheduler.active_attempts}), report.active)
                self.assertLessEqual(report.admitted, config.concurrency + config.queue_bound)


if __name__ == "__main__":
    unittest.main()
