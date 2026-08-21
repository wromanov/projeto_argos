"""Tipos imutáveis do scheduler local MON-05B."""

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import StrEnum
from numbers import Real
from decimal import Decimal
import math
from uuid import UUID


def _integer_in_range(value: object, field_name: str, minimum: int, maximum: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{field_name} must be an integer")
    if not minimum <= value <= maximum:
        raise ValueError(f"{field_name} must be between {minimum} and {maximum}")
    return value


def _non_negative_integer(value: object, field_name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{field_name} must be an integer")
    if value < 0:
        raise ValueError(f"{field_name} must be non-negative")
    return value


def _finite_real(value: object, field_name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (Real, Decimal)):
        raise TypeError(f"{field_name} must be a real number")
    normalized = float(value)
    if not math.isfinite(normalized):
        raise ValueError(f"{field_name} must be finite")
    return normalized


def _aware_utc(value: object, field_name: str) -> datetime:
    if not isinstance(value, datetime):
        raise TypeError(f"{field_name} must be a datetime")
    if value.utcoffset() is None:
        raise ValueError(f"{field_name} must be timezone-aware")
    return value.astimezone(timezone.utc)


class AttemptState(StrEnum):
    QUEUED = "QUEUED"
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class SchedulerLifecycle(StrEnum):
    STARTING = "STARTING"
    RUNNING = "RUNNING"
    DRAINING = "DRAINING"
    DEGRADED = "DEGRADED"
    STOPPED = "STOPPED"


class CompletionDisposition(StrEnum):
    ACCEPTED = "ACCEPTED"
    DUPLICATE = "DUPLICATE"
    OLD_ATTEMPT = "OLD_ATTEMPT"
    CONFIG_CHANGED = "CONFIG_CHANGED"
    ELIGIBILITY_LOST = "ELIGIBILITY_LOST"
    CANCELLED = "CANCELLED"
    OPERATIONAL_FAILURE = "OPERATIONAL_FAILURE"


@dataclass(frozen=True, slots=True)
class MonitoringConfig:
    concurrency: int = 20
    cycle_interval_seconds: int = 300
    probe_timeout_seconds: float = 5.0
    connect_timeout_seconds: float = 3.0
    queue_bound: int | None = None
    shutdown_timeout_seconds: int = 30
    jitter_ratio: float = 0.10
    stale_after_seconds: int | None = None
    heartbeat_seconds: int = 30

    def __post_init__(self) -> None:
        concurrency = _integer_in_range(self.concurrency, "concurrency", 1, 50)
        cycle_interval = _integer_in_range(self.cycle_interval_seconds, "cycle_interval_seconds", 30, 3600)
        probe_timeout = _finite_real(self.probe_timeout_seconds, "probe_timeout_seconds")
        if not 1 <= probe_timeout <= 30:
            raise ValueError("probe_timeout_seconds must be between 1 and 30")
        connect_timeout = _finite_real(self.connect_timeout_seconds, "connect_timeout_seconds")
        if not 1 <= connect_timeout <= probe_timeout:
            raise ValueError("connect_timeout_seconds must be between 1 and probe_timeout_seconds")
        queue_bound = concurrency * 2 if self.queue_bound is None else _integer_in_range(self.queue_bound, "queue_bound", concurrency, concurrency * 10)
        _integer_in_range(self.shutdown_timeout_seconds, "shutdown_timeout_seconds", 1, 300)
        jitter_ratio = _finite_real(self.jitter_ratio, "jitter_ratio")
        if not 0 <= jitter_ratio <= 0.20:
            raise ValueError("jitter_ratio must be between 0 and 0.20")
        stale_after = cycle_interval * 3 if self.stale_after_seconds is None else _integer_in_range(self.stale_after_seconds, "stale_after_seconds", cycle_interval, 86400)
        _integer_in_range(self.heartbeat_seconds, "heartbeat_seconds", 10, 300)
        object.__setattr__(self, "probe_timeout_seconds", probe_timeout)
        object.__setattr__(self, "connect_timeout_seconds", connect_timeout)
        object.__setattr__(self, "queue_bound", queue_bound)
        object.__setattr__(self, "stale_after_seconds", stale_after)
        object.__setattr__(self, "jitter_ratio", jitter_ratio)


@dataclass(frozen=True, slots=True)
class ScheduleCandidate:
    camera_id: int
    next_due_at: datetime
    config_generation: int = 1
    eligible: bool = True

    def __post_init__(self) -> None:
        if isinstance(self.camera_id, bool) or not isinstance(self.camera_id, int) or self.camera_id <= 0:
            raise ValueError("camera_id must be a positive integer")
        object.__setattr__(self, "next_due_at", _aware_utc(self.next_due_at, "next_due_at"))
        if isinstance(self.config_generation, bool) or not isinstance(self.config_generation, int) or self.config_generation <= 0:
            raise ValueError("config_generation must be a positive integer")
        if not isinstance(self.eligible, bool):
            raise TypeError("eligible must be a bool")

    def is_due(self, now: datetime) -> bool:
        return self.next_due_at <= _aware_utc(now, "now")


@dataclass(frozen=True, slots=True)
class Attempt:
    attempt_id: UUID
    camera_id: int
    config_generation: int
    scheduled_at: datetime
    started_at: datetime | None
    state: AttemptState

    def __post_init__(self) -> None:
        if not isinstance(self.attempt_id, UUID):
            raise TypeError("attempt_id must be a UUID")
        if isinstance(self.camera_id, bool) or not isinstance(self.camera_id, int) or self.camera_id <= 0:
            raise ValueError("camera_id must be a positive integer")
        if isinstance(self.config_generation, bool) or not isinstance(self.config_generation, int) or self.config_generation <= 0:
            raise ValueError("config_generation must be a positive integer")
        object.__setattr__(self, "scheduled_at", _aware_utc(self.scheduled_at, "scheduled_at"))
        if self.started_at is not None:
            object.__setattr__(self, "started_at", _aware_utc(self.started_at, "started_at"))
        if not isinstance(self.state, AttemptState):
            raise TypeError("state must be an AttemptState")


@dataclass(frozen=True, slots=True)
class CompletionOutcome:
    attempt: Attempt
    disposition: CompletionDisposition
    next_due_at: datetime | None = None
    decision: object | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.attempt, Attempt):
            raise TypeError("attempt must be an Attempt")
        if not isinstance(self.disposition, CompletionDisposition):
            raise TypeError("disposition must be a CompletionDisposition")
        if self.next_due_at is not None:
            object.__setattr__(self, "next_due_at", _aware_utc(self.next_due_at, "next_due_at"))


@dataclass(frozen=True, slots=True)
class TickReport:
    now: datetime
    eligible: int
    due: int
    admitted: int
    deferred: int
    queued: int
    active: int
    attempts: tuple[Attempt, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "now", _aware_utc(self.now, "now"))
        for field_name in ("eligible", "due", "admitted", "deferred", "queued", "active"):
            _non_negative_integer(getattr(self, field_name), field_name)
        if not isinstance(self.attempts, tuple):
            raise TypeError("attempts must be a tuple")


__all__ = [
    "Attempt", "AttemptState", "CompletionDisposition", "CompletionOutcome",
    "MonitoringConfig", "ScheduleCandidate", "SchedulerLifecycle", "TickReport",
]
