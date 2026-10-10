"""Scheduler due-based bounded e determinístico do laboratório MON-05B."""

from datetime import datetime, timedelta, timezone
from decimal import Decimal
import asyncio
import hashlib
import heapq
import math
from numbers import Real
from collections import deque
import logging
import re
import time
from typing import Awaitable, Callable, Iterable, TypeVar, cast
from uuid import UUID, uuid4

from .confirmation import ConfirmationPolicy, reduce_confirmation
from .contracts import Clock, ProbeResult
from .observability import MonitoringTelemetry, NoopTelemetry, config_snapshot
from .ports import ConfirmationStatePort, OwnershipClaimPort
from .schemas import (
    Attempt,
    AttemptState,
    CompletionDisposition,
    CompletionOutcome,
    MonitoringConfig,
    OwnershipLease,
    ScheduleCandidate,
    SchedulerLifecycle,
    SchedulerRuntimeStatus,
    TickReport,
)


logger = logging.getLogger(__name__)
_SAFE_OPERATIONAL_ERROR_CODE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,63}$")


def _aware_utc(value: object, field_name: str) -> datetime:
    if not isinstance(value, datetime):
        raise TypeError(f"{field_name} must be a datetime")
    if value.utcoffset() is None:
        raise ValueError(f"{field_name} must be timezone-aware")
    return value.astimezone(timezone.utc)


def _positive_integer(value: object, field_name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ValueError(f"{field_name} must be a positive integer")
    return value


def _finite_real(value: object, field_name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (Real, Decimal)):
        raise TypeError(f"{field_name} must be a real number")
    normalized = float(value)
    if not math.isfinite(normalized):
        raise ValueError(f"{field_name} must be finite")
    return normalized


def deterministic_jitter_seconds(camera_id: int, schedule_epoch: int, *, interval_seconds: Real, jitter_ratio: Real) -> float:
    """Jitter estável para uma câmera e uma época de agendamento."""

    _positive_integer(camera_id, "camera_id")
    if isinstance(schedule_epoch, bool) or not isinstance(schedule_epoch, int) or schedule_epoch < 0:
        raise ValueError("schedule_epoch must be a non-negative integer")
    interval = _finite_real(interval_seconds, "interval_seconds")
    if interval <= 0:
        raise ValueError("interval_seconds must be positive")
    ratio = _finite_real(jitter_ratio, "jitter_ratio")
    if not 0 <= ratio <= 0.20:
        raise ValueError("jitter_ratio must be between 0 and 0.20")
    digest = hashlib.sha256(f"{schedule_epoch}:{camera_id}".encode("ascii")).digest()
    unit = int.from_bytes(digest[:8], "big") / ((1 << 64) - 1)
    return (2.0 * unit - 1.0) * interval * ratio


def next_due_at(completed_at: datetime, camera_id: int, schedule_epoch: int, config: MonitoringConfig) -> datetime:
    if not isinstance(config, MonitoringConfig):
        raise TypeError("config must be a MonitoringConfig")
    completed = _aware_utc(completed_at, "completed_at")
    jitter = deterministic_jitter_seconds(
        camera_id,
        schedule_epoch,
        interval_seconds=config.cycle_interval_seconds,
        jitter_ratio=config.jitter_ratio,
    )
    return completed + timedelta(seconds=config.cycle_interval_seconds + jitter)


class BoundedDueQueue:
    """Fila limitada e ordenada por ``(next_due_at, camera_id)``."""

    __slots__ = ("_capacity", "_heap", "_items")

    def __init__(self, capacity: int) -> None:
        self._capacity = _positive_integer(capacity, "capacity")
        self._heap: list[tuple[datetime, int, ScheduleCandidate]] = []
        self._items: dict[int, ScheduleCandidate] = {}

    @property
    def capacity(self) -> int:
        return self._capacity

    def __len__(self) -> int:
        return len(self._items)

    def __contains__(self, camera_id: object) -> bool:
        return camera_id in self._items

    def offer(self, candidate: ScheduleCandidate) -> bool:
        if not isinstance(candidate, ScheduleCandidate):
            raise TypeError("candidate must be a ScheduleCandidate")
        if candidate.camera_id in self._items or len(self) >= self._capacity:
            return False
        self._items[candidate.camera_id] = candidate
        heapq.heappush(self._heap, (candidate.next_due_at, candidate.camera_id, candidate))
        return True

    def pop(self) -> ScheduleCandidate:
        while self._heap:
            _, camera_id, candidate = heapq.heappop(self._heap)
            if camera_id in self._items:
                self._items.pop(camera_id, None)
                return candidate
        raise IndexError("pop from empty BoundedDueQueue")

    def discard(self, camera_id: int) -> None:
        """Remove um item queued sem transformar cancelamento em probe."""

        self._items.pop(camera_id, None)

    def snapshot(self) -> tuple[ScheduleCandidate, ...]:
        return tuple(
            candidate
            for _, camera_id, candidate in sorted(self._heap, key=lambda item: (item[0], item[1]))
            if camera_id in self._items
        )


class DueScheduler:
    """Core local: due -> bounded queue -> active attempt -> completion."""

    def __init__(
        self,
        config: MonitoringConfig,
        clock: Clock,
        *,
        current_generation: Callable[[int], int] | None = None,
        is_eligible: Callable[[int], bool] | None = None,
        confirmation_port: ConfirmationStatePort | None = None,
        confirmation_policy: ConfirmationPolicy | None = None,
        ownership_port: OwnershipClaimPort | None = None,
        service_instance_id: str | None = None,
        attempt_id_factory: Callable[[], UUID] = uuid4,
        telemetry: MonitoringTelemetry | None = None,
    ) -> None:
        if not isinstance(config, MonitoringConfig):
            raise TypeError("config must be a MonitoringConfig")
        self._config = config
        self._clock = clock
        self._current_generation = current_generation
        self._is_eligible = is_eligible or (lambda _camera_id: True)
        self._confirmation_port = confirmation_port
        self._confirmation_policy = confirmation_policy
        if ownership_port is not None:
            if confirmation_port is None or ownership_port is not confirmation_port:
                raise ValueError("ownership_port must be the confirmation_port for atomic completion release")
            if not isinstance(service_instance_id, str) or not service_instance_id.strip():
                raise ValueError("service_instance_id is required with ownership_port")
            if len(service_instance_id) > 218:
                raise ValueError("service_instance_id is too long")
            self._owner_id = f"{service_instance_id}:{uuid4()}"
        elif service_instance_id is not None:
            raise ValueError("service_instance_id requires ownership_port")
        else:
            self._owner_id = None
        self._ownership_port = ownership_port
        self._attempt_id_factory = attempt_id_factory
        self._telemetry = telemetry if telemetry is not None else NoopTelemetry()
        self._cycle_started_monotonic: float | None = None
        self._telemetry_failure_reported = False
        self._lifecycle = SchedulerLifecycle.STARTING
        self._queue = BoundedDueQueue(config.queue_bound)
        self._attempts: dict[UUID, Attempt] = {}
        self._active_by_camera: dict[int, UUID] = {}
        self._current_by_camera: dict[int, UUID] = {}
        self._candidate_by_attempt: dict[UUID, ScheduleCandidate] = {}
        self._next_due: dict[int, datetime] = {}
        self._schedule_epoch: dict[int, int] = {}
        self._draining_since: datetime | None = None
        self._operational_error: str | None = None
        self._last_cycle_started_at: datetime | None = None
        self._last_cycle_completed_at: datetime | None = None
        self._cycles_started = 0
        self._cycles_completed = 0
        self._attempts_started = 0
        self._attempts_completed = 0
        self._attempts_cancelled = 0
        self._operational_failures = 0
        self._ownership_acquired = 0
        self._ownership_denied = 0
        self._ownership_lost = 0
        self._stale_owner_completions_rejected = 0

    @property
    def lifecycle(self) -> SchedulerLifecycle:
        return self._lifecycle

    @property
    def active_count(self) -> int:
        return len(self._active_by_camera)

    @property
    def queued_count(self) -> int:
        return len(self._queue)

    @property
    def active_attempts(self) -> tuple[Attempt, ...]:
        return tuple(self._attempts[attempt_id] for attempt_id in self._active_by_camera.values())

    @property
    def queued_attempts(self) -> tuple[Attempt, ...]:
        return tuple(self._attempts[attempt_id] for attempt_id in self._queued_ids())

    @property
    def attempts(self) -> tuple[Attempt, ...]:
        return tuple(self._attempts.values())

    @property
    def next_due(self) -> dict[int, datetime]:
        return dict(self._next_due)

    @property
    def operational_error(self) -> str | None:
        return self._operational_error

    @property
    def runtime_status(self) -> SchedulerRuntimeStatus:
        return SchedulerRuntimeStatus(
            scheduler_state=self._lifecycle,
            in_flight=self.active_count,
            queued=self.queued_count,
            configured_concurrency=self._config.concurrency,
            queue_capacity=self._queue.capacity,
            last_cycle_started_at=self._last_cycle_started_at,
            last_cycle_completed_at=self._last_cycle_completed_at,
            cycles_started=self._cycles_started,
            cycles_completed=self._cycles_completed,
            attempts_started=self._attempts_started,
            attempts_completed=self._attempts_completed,
            attempts_cancelled=self._attempts_cancelled,
            operational_failures=self._operational_failures,
            last_operational_error=self._operational_error,
            ownership_acquired=self._ownership_acquired,
            ownership_denied=self._ownership_denied,
            ownership_lost=self._ownership_lost,
            stale_owner_completions_rejected=self._stale_owner_completions_rejected,
        )

    def start(self) -> SchedulerLifecycle:
        if self._lifecycle is SchedulerLifecycle.STARTING:
            self._lifecycle = SchedulerLifecycle.RUNNING
            logger.info("MONITORING_SCHEDULER_STARTED concurrency=%s queue_capacity=%s", self._config.concurrency, self._queue.capacity)
            self._emit_event("monitoring.scheduler.started", {"concurrency": self._config.concurrency, "queue_capacity": self._queue.capacity})
            self._emit_event("monitoring.config.snapshot", config_snapshot(self._config, self._confirmation_policy))
            self._emit_event("monitoring.scheduler.lifecycle", {"state": self._lifecycle.value})
        elif self._lifecycle is SchedulerLifecycle.DEGRADED:
            self._lifecycle = SchedulerLifecycle.RUNNING
            self._operational_error = None
            self._emit_event("monitoring.scheduler.lifecycle", {"state": self._lifecycle.value})
        elif self._lifecycle is not SchedulerLifecycle.RUNNING:
            raise RuntimeError(f"cannot start scheduler from {self._lifecycle}")
        return self._lifecycle

    def _queued_ids(self) -> tuple[UUID, ...]:
        return tuple(self._current_by_camera[candidate.camera_id] for candidate in self._queue.snapshot())

    def _make_attempt(self, candidate: ScheduleCandidate, now: datetime) -> Attempt:
        attempt_id = self._attempt_id_factory()
        if not isinstance(attempt_id, UUID) or attempt_id in self._attempts:
            raise ValueError("attempt_id_factory must return a fresh UUID")
        attempt = Attempt(attempt_id, candidate.camera_id, candidate.config_generation, now, None, AttemptState.QUEUED)
        self._attempts[attempt_id] = attempt
        self._candidate_by_attempt[attempt_id] = candidate
        self._current_by_camera[candidate.camera_id] = attempt_id
        return attempt

    def _replace_attempt(self, attempt: Attempt, *, state: AttemptState, started_at: datetime | None = None) -> Attempt:
        updated = Attempt(
            attempt.attempt_id,
            attempt.camera_id,
            attempt.config_generation,
            attempt.scheduled_at,
            started_at if started_at is not None else attempt.started_at,
            state,
            attempt.ownership,
        )
        self._attempts[attempt.attempt_id] = updated
        return updated

    def _start_from_queue(self, now: datetime) -> tuple[Attempt, ...]:
        if self._lifecycle in (SchedulerLifecycle.DRAINING, SchedulerLifecycle.STOPPED):
            return ()
        started: list[Attempt] = []
        while self.active_count < self._config.concurrency and len(self._queue):
            candidate = self._queue.pop()
            attempt_id = self._current_by_camera[candidate.camera_id]
            attempt = self._attempts[attempt_id]
            ownership = None
            if self._ownership_port is not None:
                try:
                    ownership = self._ownership_port.claim(
                        candidate.camera_id,
                        self._owner_id,
                        self._config.ownership_lease_seconds,
                    )
                except Exception as exc:
                    self.report_repository_failure(type(exc).__name__)
                    self._discard(attempt, CompletionDisposition.OPERATIONAL_FAILURE, now)
                    break
                if ownership is None:
                    self._ownership_denied += 1
                    self._emit_event("monitoring.ownership", {"outcome": "DENIED"})
                    self._increment("monitoring.ownership.outcomes", {"outcome": "DENIED"})
                    logger.info("MONITORING_OWNERSHIP_DENIED camera_id=%s", candidate.camera_id)
                    self._discard(attempt, CompletionDisposition.OWNERSHIP_LOST, now)
                    continue
            active = Attempt(
                attempt.attempt_id,
                attempt.camera_id,
                attempt.config_generation,
                attempt.scheduled_at,
                now,
                AttemptState.ACTIVE,
                ownership,
            )
            self._attempts[attempt_id] = active
            started.append(active)
            self._active_by_camera[candidate.camera_id] = attempt_id
            self._attempts_started += 1
            self._increment("monitoring.attempts.started")
            if ownership is not None:
                self._ownership_acquired += 1
                self._emit_event("monitoring.ownership", {"outcome": "ACQUIRED"})
                self._increment("monitoring.ownership.outcomes", {"outcome": "ACQUIRED"})
                logger.info("MONITORING_OWNERSHIP_ACQUIRED camera_id=%s ownership_epoch=%s", candidate.camera_id, ownership.epoch)
            logger.info("MONITORING_ATTEMPT_STARTED camera_id=%s", candidate.camera_id)
        return tuple(started)

    def admit(self, candidates: Iterable[ScheduleCandidate], now: datetime | None = None) -> TickReport:
        return self.tick(now, candidates)

    def tick(self, now: datetime | None = None, candidates: Iterable[ScheduleCandidate] = ()) -> TickReport:
        now = _aware_utc(self._clock.now() if now is None else now, "now")
        self._last_cycle_started_at = now
        self._cycle_started_monotonic = time.perf_counter()
        self._cycles_started += 1
        self._emit_event("monitoring.cycle.started", {"timestamp": now})
        self._emit_event("monitoring.scheduler.lifecycle", {"state": self._lifecycle.value})
        logger.info("MONITORING_CYCLE_STARTED")
        if self._lifecycle is SchedulerLifecycle.STARTING:
            self.start()
        if self._lifecycle is SchedulerLifecycle.STOPPED:
            return self._complete_cycle(TickReport(now, 0, 0, 0, 0, self.queued_count, self.active_count, ()))
        if self._lifecycle is SchedulerLifecycle.DRAINING:
            self._finish_shutdown_if_due(now)
            return self._complete_cycle(TickReport(now, 0, 0, 0, 0, self.queued_count, self.active_count, ()))
        if self._lifecycle is SchedulerLifecycle.DEGRADED:
            return self._complete_cycle(TickReport(now, 0, 0, 0, 0, self.queued_count, self.active_count, ()))
        candidate_list = tuple(candidates)
        if not all(isinstance(candidate, ScheduleCandidate) for candidate in candidate_list):
            raise TypeError("candidates must contain ScheduleCandidate values")
        try:
            eligible = tuple(candidate for candidate in candidate_list if candidate.eligible and self._is_eligible(candidate.camera_id))
        except Exception as exc:
            self.report_repository_failure(type(exc).__name__)
            return self._complete_cycle(TickReport(now, 0, 0, 0, 0, self.queued_count, self.active_count, ()))
        due = tuple(
            sorted(
                (
                    candidate
                    for candidate in eligible
                    if candidate.is_due(now)
                    and now >= self._next_due.get(candidate.camera_id, candidate.next_due_at)
                ),
                key=lambda item: (item.next_due_at, item.camera_id),
            )
        )
        started = list(self._start_from_queue(now))
        admitted = 0
        deferred = 0
        for candidate in due:
            if candidate.camera_id in self._current_by_camera:
                continue
            if len(self._queue) >= self._config.queue_bound:
                deferred += 1
                continue
            self._make_attempt(candidate, now)
            self._queue.offer(candidate)
            admitted += 1
        started.extend(self._start_from_queue(now))
        return self._complete_cycle(TickReport(now, len(eligible), len(due), admitted, deferred, self.queued_count, self.active_count, tuple(started)))

    def _complete_cycle(self, report: TickReport) -> TickReport:
        self._last_cycle_completed_at = report.now
        self._cycles_completed += 1
        duration = max(0.0, time.perf_counter() - self._cycle_started_monotonic) if self._cycle_started_monotonic is not None else 0.0
        fields = {
            "timestamp": report.now, "eligible": report.eligible,
            "due": report.due, "admitted": report.admitted,
            "deferred": report.deferred, "queued": report.queued,
            "active": report.active, "duration_seconds": duration,
        }
        self._emit_event("monitoring.cycle.completed", fields)
        self._observe_seconds("monitoring.cycle.duration_seconds", duration)
        self._gauge("monitoring.work.eligible", report.eligible)
        self._gauge("monitoring.work.due", report.due)
        self._gauge("monitoring.work.admitted", report.admitted)
        self._gauge("monitoring.work.deferred", report.deferred)
        self._gauge("monitoring.queue.depth", report.queued)
        self._gauge("monitoring.attempts.active", report.active)
        self._emit_event("monitoring.worker.heartbeat", {"timestamp": report.now, "state": self._lifecycle.value, "active": report.active, "queued": report.queued})
        self._gauge("monitoring.worker.heartbeat_age_seconds", 0)
        logger.info(
            "MONITORING_CYCLE_COMPLETED eligible=%s due=%s admitted=%s deferred=%s queued=%s in_flight=%s",
            report.eligible, report.due, report.admitted, report.deferred, report.queued, report.active,
        )
        return report

    def complete(self, attempt_id: UUID, result: ProbeResult, now: datetime | None = None) -> CompletionOutcome:
        if not isinstance(attempt_id, UUID):
            raise TypeError("attempt_id must be a UUID")
        if not isinstance(result, ProbeResult):
            raise TypeError("result must be a ProbeResult")
        now = _aware_utc(self._clock.now() if now is None else now, "now")
        attempt = self._attempts.get(attempt_id)
        if attempt is None:
            raise KeyError("unknown attempt_id")
        current_id = self._current_by_camera.get(attempt.camera_id)
        if attempt.state in (AttemptState.COMPLETED, AttemptState.CANCELLED):
            if current_id is not None and current_id != attempt_id:
                return CompletionOutcome(attempt, CompletionDisposition.OLD_ATTEMPT)
            return CompletionOutcome(attempt, CompletionDisposition.DUPLICATE)
        if current_id != attempt_id:
            return CompletionOutcome(attempt, CompletionDisposition.OLD_ATTEMPT)
        if attempt.state is not AttemptState.ACTIVE:
            return CompletionOutcome(attempt, CompletionDisposition.CANCELLED)
        self._emit_event("monitoring.probe.completed", {"outcome": result.code.value, "duration_seconds": result.duration_seconds})
        self._increment("monitoring.probe.outcomes", {"outcome": result.code.value})
        self._observe_seconds("monitoring.probe.duration_seconds", result.duration_seconds, {"outcome": result.code.value})
        try:
            current_generation = attempt.config_generation if self._current_generation is None else self._current_generation(attempt.camera_id)
            eligible = self._is_eligible(attempt.camera_id)
        except Exception as exc:
            self.report_repository_failure(type(exc).__name__)
            return self._discard(attempt, CompletionDisposition.OPERATIONAL_FAILURE, now)
        if current_generation != attempt.config_generation:
            return self._discard(attempt, CompletionDisposition.CONFIG_CHANGED, now)
        if not eligible:
            return self._discard(attempt, CompletionDisposition.ELIGIBILITY_LOST, now)
        if result.code.name == "CANCELLED":
            return self._discard(attempt, CompletionDisposition.CANCELLED, now)
        candidate = self._candidate_by_attempt[attempt_id]
        decision = None
        epoch = self._schedule_epoch.get(attempt.camera_id, 0) + 1
        scheduled_next = next_due_at(result.observed_at, attempt.camera_id, epoch, self._config)
        if self._confirmation_port is not None:
            if self._confirmation_policy is None:
                raise ValueError("confirmation_policy is required with confirmation_port")
            try:
                memory = self._confirmation_port.load(candidate, self._confirmation_policy)
                memory, decision = reduce_confirmation(memory, result, self._confirmation_policy)
                if attempt.ownership is None:
                    stored = self._confirmation_port.store(candidate, result, memory, decision, scheduled_next)
                else:
                    stored = self._confirmation_port.store(
                        candidate,
                        result,
                        memory,
                        decision,
                        scheduled_next,
                        ownership=attempt.ownership,
                    )
                if stored is False:
                    return self._discard(attempt, CompletionDisposition.CONFIG_CHANGED, now)
                if stored is CompletionDisposition.CONFIG_CHANGED:
                    return self._discard(attempt, CompletionDisposition.CONFIG_CHANGED, now)
                if stored is CompletionDisposition.OWNERSHIP_LOST:
                    self._ownership_lost += 1
                    self._stale_owner_completions_rejected += 1
                    self._emit_event("monitoring.ownership", {"outcome": "LOST"})
                    self._increment("monitoring.ownership.outcomes", {"outcome": "LOST"})
                    self._emit_event("monitoring.stale_completion.rejected", {})
                    self._increment("monitoring.stale_completion.rejections")
                    logger.info("MONITORING_STALE_OWNER_COMPLETION_REJECTED camera_id=%s ownership_epoch=%s", attempt.camera_id, attempt.ownership.epoch)
                    return self._discard(attempt, CompletionDisposition.OWNERSHIP_LOST, now)
            except Exception as exc:
                self.report_repository_failure(type(exc).__name__)
                return self._discard(attempt, CompletionDisposition.OPERATIONAL_FAILURE, now)
        completed = self._replace_attempt(attempt, state=AttemptState.COMPLETED)
        self._active_by_camera.pop(attempt.camera_id, None)
        self._current_by_camera.pop(attempt.camera_id, None)
        self._schedule_epoch[attempt.camera_id] = epoch
        self._next_due[attempt.camera_id] = scheduled_next
        self._attempts_completed += 1
        self._increment("monitoring.attempts.completed")
        logger.info("MONITORING_ATTEMPT_COMPLETED camera_id=%s disposition=%s", attempt.camera_id, CompletionDisposition.ACCEPTED)
        self._start_from_queue(now)
        self._finish_shutdown_if_due(now)
        return CompletionOutcome(completed, CompletionDisposition.ACCEPTED, scheduled_next, decision)

    def _discard(self, attempt: Attempt, disposition: CompletionDisposition, now: datetime) -> CompletionOutcome:
        cancelled = self._replace_attempt(attempt, state=AttemptState.CANCELLED)
        if attempt.state is AttemptState.QUEUED:
            self._queue.discard(attempt.camera_id)
        self._active_by_camera.pop(attempt.camera_id, None)
        self._current_by_camera.pop(attempt.camera_id, None)
        self._release_ownership(attempt)
        self._attempts_cancelled += 1
        self._increment("monitoring.attempts.cancelled")
        logger.info("MONITORING_ATTEMPT_CANCELLED camera_id=%s disposition=%s", attempt.camera_id, disposition)
        self._start_from_queue(now)
        self._finish_shutdown_if_due(now)
        return CompletionOutcome(cancelled, disposition)

    def cancel(self, attempt_id: UUID) -> CompletionOutcome:
        attempt = self._attempts[attempt_id]
        if attempt.state is AttemptState.CANCELLED:
            return CompletionOutcome(attempt, CompletionDisposition.DUPLICATE)
        cancelled = self._replace_attempt(attempt, state=AttemptState.CANCELLED)
        if attempt.state is AttemptState.QUEUED:
            self._queue.discard(attempt.camera_id)
        self._active_by_camera.pop(attempt.camera_id, None)
        self._current_by_camera.pop(attempt.camera_id, None)
        self._release_ownership(attempt)
        self._attempts_cancelled += 1
        self._increment("monitoring.attempts.cancelled")
        logger.info("MONITORING_ATTEMPT_CANCELLED camera_id=%s disposition=%s", attempt.camera_id, CompletionDisposition.CANCELLED)
        self._start_from_queue(cancelled.started_at or cancelled.scheduled_at)
        return CompletionOutcome(cancelled, CompletionDisposition.CANCELLED)

    def _release_ownership(self, attempt: Attempt) -> None:
        if attempt.ownership is None or self._ownership_port is None:
            return
        try:
            released = self._ownership_port.release(attempt.camera_id, attempt.ownership)
            if not released:
                self._ownership_lost += 1
                self._emit_event("monitoring.ownership", {"outcome": "LOST"})
                self._increment("monitoring.ownership.outcomes", {"outcome": "LOST"})
                logger.info("MONITORING_OWNERSHIP_LOST camera_id=%s ownership_epoch=%s", attempt.camera_id, attempt.ownership.epoch)
        except Exception as exc:
            self.report_repository_failure(type(exc).__name__)

    def request_shutdown(self, now: datetime | None = None) -> SchedulerLifecycle:
        now = _aware_utc(self._clock.now() if now is None else now, "now")
        if self._lifecycle is SchedulerLifecycle.STOPPED:
            return self._lifecycle
        self._lifecycle = SchedulerLifecycle.DRAINING
        self._emit_event("monitoring.scheduler.lifecycle", {"state": self._lifecycle.value})
        self._draining_since = now
        self._finish_shutdown_if_due(now)
        return self._lifecycle

    def _finish_shutdown_if_due(self, now: datetime) -> None:
        if self._lifecycle is not SchedulerLifecycle.DRAINING:
            return
        if not self._active_by_camera:
            for attempt_id in self._queued_ids():
                self.cancel(attempt_id)
            self._mark_stopped()
            return
        if self._draining_since is not None and now >= self._draining_since + timedelta(seconds=self._config.shutdown_timeout_seconds):
            for attempt_id in tuple(self._active_by_camera.values()):
                self.cancel(attempt_id)
            for attempt_id in self._queued_ids():
                self.cancel(attempt_id)
            self._mark_stopped()

    def _mark_stopped(self) -> None:
        if self._lifecycle is not SchedulerLifecycle.STOPPED:
            self._lifecycle = SchedulerLifecycle.STOPPED
            logger.info("MONITORING_SCHEDULER_STOPPED")
            self._emit_event("monitoring.scheduler.lifecycle", {"state": self._lifecycle.value})

    def _telemetry_failed(self) -> None:
        if not self._telemetry_failure_reported:
            self._telemetry_failure_reported = True
            logger.warning("MONITORING_TELEMETRY_FAILURE")

    def _emit_event(self, name: str, fields: dict[str, object]) -> None:
        try:
            self._telemetry.emit_event(name, fields)
        except Exception:
            self._telemetry_failed()

    def _increment(self, name: str, labels: dict[str, str] | None = None) -> None:
        try:
            self._telemetry.increment(name, {} if labels is None else labels)
        except Exception:
            self._telemetry_failed()

    def _gauge(self, name: str, value: Real) -> None:
        try:
            self._telemetry.gauge(name, value)
        except Exception:
            self._telemetry_failed()

    def _observe_seconds(self, name: str, value: Real, labels: dict[str, str] | None = None) -> None:
        try:
            self._telemetry.observe_seconds(name, value, {} if labels is None else labels)
        except Exception:
            self._telemetry_failed()

    def report_repository_failure(self, error_code: str) -> SchedulerLifecycle:
        if not isinstance(error_code, str) or not _SAFE_OPERATIONAL_ERROR_CODE.fullmatch(error_code):
            raise ValueError("error_code must be a short machine-safe code")
        self._operational_error = error_code
        self._operational_failures += 1
        logger.warning("MONITORING_OPERATIONAL_FAILURE error_code=%s", error_code)
        self._emit_event("monitoring.repository.failed", {"error_code": error_code})
        self._increment("monitoring.repository.failures", {"error_code": error_code})
        if self._lifecycle not in (SchedulerLifecycle.STOPPED, SchedulerLifecycle.DRAINING):
            self._lifecycle = SchedulerLifecycle.DEGRADED
            self._emit_event("monitoring.scheduler.lifecycle", {"state": self._lifecycle.value})
        return self._lifecycle

    def restart(self, candidates: Iterable[ScheduleCandidate], now: datetime | None = None) -> TickReport:
        if self._lifecycle is not SchedulerLifecycle.STOPPED:
            raise RuntimeError("restart requires STOPPED scheduler")
        self._queue = BoundedDueQueue(self._config.queue_bound)
        self._attempts.clear()
        self._active_by_camera.clear()
        self._current_by_camera.clear()
        self._candidate_by_attempt.clear()
        self._next_due.clear()
        self._schedule_epoch.clear()
        self._lifecycle = SchedulerLifecycle.STARTING
        self._draining_since = None
        return self.tick(now, candidates)


__all__ = [
    "BoundedDueQueue",
    "DueScheduler",
    "deterministic_jitter_seconds",
    "execute_bounded",
    "next_due_at",
    "run_bounded",
]

T = TypeVar("T")
R = TypeVar("R")


async def execute_bounded(items: Iterable[T], handler: Callable[[T], Awaitable[R]], *, concurrency: int) -> tuple[R, ...]:
    """Executa trabalho já admitido sem criar uma task por candidato."""

    concurrency = _positive_integer(concurrency, "concurrency")
    item_list = tuple(items)
    if not item_list:
        return ()
    if not callable(handler):
        raise TypeError("handler must be callable")
    pending = deque(enumerate(item_list))
    results: list[R | None] = [None] * len(item_list)

    async def runner() -> None:
        while pending:
            index, item = pending.popleft()
            results[index] = await handler(item)

    tasks = [asyncio.create_task(runner()) for _ in range(min(concurrency, len(item_list)))]
    try:
        await asyncio.gather(*tasks)
    except BaseException:
        for task in tasks:
            if not task.done():
                task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)
        raise
    return tuple(cast(R, result) for result in results)


run_bounded = execute_bounded
