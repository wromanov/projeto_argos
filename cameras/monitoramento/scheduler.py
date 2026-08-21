"""Scheduler due-based bounded e determinístico do laboratório MON-05B."""

from datetime import datetime, timedelta, timezone
from decimal import Decimal
import asyncio
import hashlib
import heapq
import math
from numbers import Real
from collections import deque
from typing import Awaitable, Callable, Iterable, TypeVar, cast
from uuid import UUID, uuid4

from .confirmation import ConfirmationPolicy, reduce_confirmation
from .contracts import Clock, ProbeResult
from .ports import ConfirmationStatePort
from .schemas import (
    Attempt,
    AttemptState,
    CompletionDisposition,
    CompletionOutcome,
    MonitoringConfig,
    ScheduleCandidate,
    SchedulerLifecycle,
    TickReport,
)


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
        attempt_id_factory: Callable[[], UUID] = uuid4,
    ) -> None:
        if not isinstance(config, MonitoringConfig):
            raise TypeError("config must be a MonitoringConfig")
        self._config = config
        self._clock = clock
        self._current_generation = current_generation
        self._is_eligible = is_eligible or (lambda _camera_id: True)
        self._confirmation_port = confirmation_port
        self._confirmation_policy = confirmation_policy
        self._attempt_id_factory = attempt_id_factory
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

    def start(self) -> SchedulerLifecycle:
        if self._lifecycle is SchedulerLifecycle.STARTING:
            self._lifecycle = SchedulerLifecycle.RUNNING
        elif self._lifecycle is SchedulerLifecycle.DEGRADED:
            self._lifecycle = SchedulerLifecycle.RUNNING
            self._operational_error = None
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
        updated = Attempt(attempt.attempt_id, attempt.camera_id, attempt.config_generation, attempt.scheduled_at, started_at if started_at is not None else attempt.started_at, state)
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
            started.append(self._replace_attempt(attempt, state=AttemptState.ACTIVE, started_at=now))
            self._active_by_camera[candidate.camera_id] = attempt_id
        return tuple(started)

    def admit(self, candidates: Iterable[ScheduleCandidate], now: datetime | None = None) -> TickReport:
        return self.tick(now, candidates)

    def tick(self, now: datetime | None = None, candidates: Iterable[ScheduleCandidate] = ()) -> TickReport:
        now = _aware_utc(self._clock.now() if now is None else now, "now")
        if self._lifecycle is SchedulerLifecycle.STARTING:
            self.start()
        if self._lifecycle is SchedulerLifecycle.STOPPED:
            return TickReport(now, 0, 0, 0, 0, self.queued_count, self.active_count, ())
        if self._lifecycle is SchedulerLifecycle.DRAINING:
            self._finish_shutdown_if_due(now)
            return TickReport(now, 0, 0, 0, 0, self.queued_count, self.active_count, ())
        if self._lifecycle is SchedulerLifecycle.DEGRADED:
            return TickReport(now, 0, 0, 0, 0, self.queued_count, self.active_count, ())
        candidate_list = tuple(candidates)
        if not all(isinstance(candidate, ScheduleCandidate) for candidate in candidate_list):
            raise TypeError("candidates must contain ScheduleCandidate values")
        try:
            eligible = tuple(candidate for candidate in candidate_list if candidate.eligible and self._is_eligible(candidate.camera_id))
        except Exception as exc:
            self.report_repository_failure(type(exc).__name__)
            return TickReport(now, 0, 0, 0, 0, self.queued_count, self.active_count, ())
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
        return TickReport(now, len(eligible), len(due), admitted, deferred, self.queued_count, self.active_count, tuple(started))

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
        try:
            current_generation = attempt.config_generation if self._current_generation is None else self._current_generation(attempt.camera_id)
            eligible = self._is_eligible(attempt.camera_id)
        except Exception as exc:
            self.report_repository_failure(type(exc).__name__)
            return CompletionOutcome(attempt, CompletionDisposition.OPERATIONAL_FAILURE)
        if current_generation != attempt.config_generation:
            return self._discard(attempt, CompletionDisposition.CONFIG_CHANGED, now)
        if not eligible:
            return self._discard(attempt, CompletionDisposition.ELIGIBILITY_LOST, now)
        if result.code.name == "CANCELLED":
            return self._discard(attempt, CompletionDisposition.CANCELLED, now)
        candidate = self._candidate_by_attempt[attempt_id]
        decision = None
        if self._confirmation_port is not None:
            if self._confirmation_policy is None:
                raise ValueError("confirmation_policy is required with confirmation_port")
            memory = self._confirmation_port.load(candidate, self._confirmation_policy)
            memory, decision = reduce_confirmation(memory, result, self._confirmation_policy)
            self._confirmation_port.store(candidate, result, memory, decision)
        completed = self._replace_attempt(attempt, state=AttemptState.COMPLETED)
        self._active_by_camera.pop(attempt.camera_id, None)
        self._current_by_camera.pop(attempt.camera_id, None)
        epoch = self._schedule_epoch.get(attempt.camera_id, 0) + 1
        self._schedule_epoch[attempt.camera_id] = epoch
        scheduled_next = next_due_at(result.observed_at, attempt.camera_id, epoch, self._config)
        self._next_due[attempt.camera_id] = scheduled_next
        self._start_from_queue(now)
        self._finish_shutdown_if_due(now)
        return CompletionOutcome(completed, CompletionDisposition.ACCEPTED, scheduled_next, decision)

    def _discard(self, attempt: Attempt, disposition: CompletionDisposition, now: datetime) -> CompletionOutcome:
        cancelled = self._replace_attempt(attempt, state=AttemptState.CANCELLED)
        if attempt.state is AttemptState.QUEUED:
            self._queue.discard(attempt.camera_id)
        self._active_by_camera.pop(attempt.camera_id, None)
        self._current_by_camera.pop(attempt.camera_id, None)
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
        self._start_from_queue(cancelled.started_at or cancelled.scheduled_at)
        return CompletionOutcome(cancelled, CompletionDisposition.CANCELLED)

    def request_shutdown(self, now: datetime | None = None) -> SchedulerLifecycle:
        now = _aware_utc(self._clock.now() if now is None else now, "now")
        if self._lifecycle is SchedulerLifecycle.STOPPED:
            return self._lifecycle
        self._lifecycle = SchedulerLifecycle.DRAINING
        self._draining_since = now
        self._finish_shutdown_if_due(now)
        return self._lifecycle

    def _finish_shutdown_if_due(self, now: datetime) -> None:
        if self._lifecycle is not SchedulerLifecycle.DRAINING:
            return
        if not self._active_by_camera:
            for attempt_id in self._queued_ids():
                self.cancel(attempt_id)
            self._lifecycle = SchedulerLifecycle.STOPPED
            return
        if self._draining_since is not None and now >= self._draining_since + timedelta(seconds=self._config.shutdown_timeout_seconds):
            for attempt_id in tuple(self._active_by_camera.values()):
                self.cancel(attempt_id)
            for attempt_id in self._queued_ids():
                self.cancel(attempt_id)
            self._lifecycle = SchedulerLifecycle.STOPPED

    def report_repository_failure(self, error_code: str) -> SchedulerLifecycle:
        if not isinstance(error_code, str) or not error_code.strip():
            raise ValueError("error_code must be non-empty")
        self._operational_error = error_code
        if self._lifecycle not in (SchedulerLifecycle.STOPPED, SchedulerLifecycle.DRAINING):
            self._lifecycle = SchedulerLifecycle.DEGRADED
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
