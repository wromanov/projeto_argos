"""Vendor-neutral, allowlisted observability for the monitoring subsystem."""

from __future__ import annotations

from datetime import datetime
import json
import logging
import math
from numbers import Real
import re
from typing import Mapping, Protocol

from .confirmation import ConfirmationPolicy
from .schemas import MonitoringConfig

logger = logging.getLogger(__name__)
_SAFE_CODE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,63}$")
_SAFE_VERSION = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,31}$")
_STAGES = frozenset({"A", "B", "C", "D"})
_OUTCOMES = frozenset({"SUCCESS", "TIMEOUT", "CONNECTION_REFUSED", "AUTH_FAILURE", "TLS_ERROR", "PROTOCOL_ERROR", "CONFIG_ERROR", "TARGET_BLOCKED", "CANCELLED", "INCONCLUSIVE"})
_DISPOSITIONS = frozenset({"ACCEPTED", "DUPLICATE", "OLD_ATTEMPT", "CONFIG_CHANGED", "OWNERSHIP_LOST", "ELIGIBILITY_LOST", "CANCELLED", "OPERATIONAL_FAILURE"})
_EVENT_FIELDS = {
    "monitoring.scheduler.started": frozenset({"concurrency", "queue_capacity"}),
    "monitoring.scheduler.lifecycle": frozenset({"state"}),
    "monitoring.config.snapshot": frozenset({
        "concurrency", "cycle_interval_seconds", "probe_timeout_seconds",
        "connect_timeout_seconds", "queue_bound", "shutdown_timeout_seconds",
        "jitter_ratio", "stale_after_seconds", "heartbeat_seconds",
        "ownership_lease_seconds", "db_operation_deadline_seconds", "recovery_max_attempts", "recovery_max_elapsed_seconds", "policy_status", "policy_version",
    }),
    "monitoring.cycle.started": frozenset({"timestamp"}),
    "monitoring.cycle.completed": frozenset({"timestamp", "eligible", "due", "admitted", "deferred", "queued", "active", "duration_seconds"}),
    "monitoring.worker.heartbeat": frozenset({"timestamp", "state", "active", "queued"}),
    "monitoring.probe.completed": frozenset({"outcome", "duration_seconds", "disposition"}),
    "monitoring.health_stage.failed": frozenset({"stage", "outcome"}),
    "monitoring.repository.failed": frozenset({"error_code"}),
    "monitoring.ownership": frozenset({"outcome"}),
    "monitoring.stale_completion.rejected": frozenset(),
}
_COUNTER_METRICS = frozenset({"monitoring.probe.outcomes", "monitoring.health_stage.failures", "monitoring.repository.failures", "monitoring.ownership.outcomes", "monitoring.stale_completion.rejections", "monitoring.attempts.cancelled", "monitoring.attempts.started", "monitoring.attempts.completed"})
_GAUGE_METRICS = frozenset({"monitoring.work.eligible", "monitoring.work.due", "monitoring.work.admitted", "monitoring.work.deferred", "monitoring.queue.depth", "monitoring.attempts.active", "monitoring.worker.heartbeat_age_seconds"})
_OBSERVATION_METRICS = frozenset({"monitoring.cycle.duration_seconds", "monitoring.probe.duration_seconds"})
_METRIC_LABELS = {
    "monitoring.cycle.duration_seconds": frozenset(),
    "monitoring.work.eligible": frozenset(),
    "monitoring.work.due": frozenset(),
    "monitoring.work.admitted": frozenset(),
    "monitoring.work.deferred": frozenset(),
    "monitoring.queue.depth": frozenset(),
    "monitoring.attempts.active": frozenset(),
    "monitoring.attempts.cancelled": frozenset(),
    "monitoring.attempts.started": frozenset(),
    "monitoring.attempts.completed": frozenset(),
    "monitoring.probe.outcomes": frozenset({"outcome", "adapter_version", "profile_version"}),
    "monitoring.probe.duration_seconds": frozenset({"outcome"}),
    "monitoring.health_stage.failures": frozenset({"stage", "outcome"}),
    "monitoring.worker.heartbeat_age_seconds": frozenset(),
    "monitoring.repository.failures": frozenset({"error_code"}),
    "monitoring.ownership.outcomes": frozenset({"outcome"}),
    "monitoring.stale_completion.rejections": frozenset(),
}


def _scalar(value: object, field: str) -> bool | int | float | str:
    if isinstance(value, bool):
        return value
    if isinstance(value, int):
        return value
    if isinstance(value, Real):
        number = float(value)
        if not math.isfinite(number):
            raise ValueError(f"{field} must be finite")
        return number
    if isinstance(value, str):
        if "\r" in value or "\n" in value:
            raise ValueError(f"{field} must not contain line breaks")
        return value
    if isinstance(value, datetime):
        if value.utcoffset() is None:
            raise ValueError(f"{field} must be timezone-aware")
        return value.isoformat()
    raise TypeError(f"{field} must be a JSON scalar")


def _validate_event(name: object, fields: object) -> tuple[str, dict[str, bool | int | float | str]]:
    if not isinstance(name, str) or name not in _EVENT_FIELDS:
        raise ValueError("event name is not allowlisted")
    if not isinstance(fields, Mapping):
        raise TypeError("event fields must be a mapping")
    allowed = _EVENT_FIELDS[name]
    if any(not isinstance(key, str) or key not in allowed for key in fields):
        raise ValueError("event field is not allowlisted")
    integer_fields = {"concurrency", "queue_capacity", "cycle_interval_seconds", "queue_bound", "shutdown_timeout_seconds", "stale_after_seconds", "heartbeat_seconds", "ownership_lease_seconds", "recovery_max_attempts", "eligible", "due", "admitted", "deferred", "queued", "active"}
    numeric_fields = {"probe_timeout_seconds", "connect_timeout_seconds", "jitter_ratio", "duration_seconds", "db_operation_deadline_seconds", "recovery_max_elapsed_seconds"}
    clean = {}
    for key, value in fields.items():
        if key == "timestamp":
            if not isinstance(value, datetime) or value.utcoffset() is None:
                raise TypeError("timestamp must be a timezone-aware datetime")
        elif key in integer_fields:
            if isinstance(value, bool) or not isinstance(value, int) or value < 0:
                raise ValueError(f"{key} must be a non-negative integer")
        elif key in numeric_fields:
            if isinstance(value, bool) or not isinstance(value, Real):
                raise TypeError(f"{key} must be a real number")
            if not math.isfinite(float(value)) or float(value) < 0:
                raise ValueError(f"{key} must be finite and non-negative")
        elif not isinstance(value, str):
            raise TypeError(f"{key} must be a string")
        clean[key] = _scalar(value, key)
    if name == "monitoring.config.snapshot":
        if clean.get("policy_status") not in {"CONFIGURED", "UNCONFIGURED"}:
            raise ValueError("policy_status is not allowlisted")
        if "policy_version" in clean and not _SAFE_VERSION.fullmatch(str(clean["policy_version"])):
            raise ValueError("policy_version is not bounded")
    if name == "monitoring.scheduler.lifecycle" and clean.get("state") not in {"STARTING", "RUNNING", "DRAINING", "DEGRADED", "STOPPED"}:
        raise ValueError("state is not allowlisted")
    if name == "monitoring.worker.heartbeat" and clean.get("state") not in {"STARTING", "RUNNING", "DRAINING", "DEGRADED", "STOPPED"}:
        raise ValueError("state is not allowlisted")
    if name == "monitoring.probe.completed":
        if clean.get("outcome") not in _OUTCOMES:
            raise ValueError("outcome is not allowlisted")
        if "disposition" in clean and clean["disposition"] not in _DISPOSITIONS:
            raise ValueError("disposition is not allowlisted")
    if name == "monitoring.health_stage.failed":
        if clean.get("stage") not in _STAGES or clean.get("outcome") not in _OUTCOMES:
            raise ValueError("stage or outcome is not allowlisted")
    if name == "monitoring.ownership" and clean.get("outcome") not in {"ACQUIRED", "DENIED", "LOST"}:
        raise ValueError("ownership outcome is not allowlisted")
    if "error_code" in clean and (not isinstance(clean["error_code"], str) or not _SAFE_CODE.fullmatch(clean["error_code"])):
        raise ValueError("error_code must be a sanitized machine code")
    return name, clean


def _validate_metric(name: object, value: object, labels: object) -> tuple[str, float, dict[str, str]]:
    if not isinstance(name, str) or name not in _METRIC_LABELS:
        raise ValueError("metric name is not allowlisted")
    if isinstance(value, bool) or not isinstance(value, Real):
        raise TypeError("metric value must be a real number")
    number = float(value)
    if not math.isfinite(number) or number < 0:
        raise ValueError("metric value must be finite and non-negative")
    if not isinstance(labels, Mapping):
        raise TypeError("labels must be a mapping")
    allowed = _METRIC_LABELS[name]
    if any(not isinstance(key, str) or key not in allowed for key in labels):
        raise ValueError("metric label is not allowlisted")
    clean: dict[str, str] = {}
    for key, value in labels.items():
        if not isinstance(value, str):
            raise TypeError("metric label values must be strings")
        if key == "stage" and value not in _STAGES:
            raise ValueError("stage label is not allowlisted")
        if key == "outcome" and value not in _OUTCOMES:
            raise ValueError("outcome label is not allowlisted")
        if key == "error_code" and not _SAFE_CODE.fullmatch(value):
            raise ValueError("error_code label must be sanitized")
        if key in {"adapter_version", "profile_version"} and not _SAFE_VERSION.fullmatch(value):
            raise ValueError("version label is not bounded")
        clean[key] = value
    return name, number, clean


class MonitoringTelemetry(Protocol):
    """Telemetry port. Implementations must not own monitoring domain state."""

    def emit_event(self, name: str, fields: Mapping[str, object]) -> None: ...
    def increment(self, name: str, labels: Mapping[str, str] = {}) -> None: ...
    def gauge(self, name: str, value: Real, labels: Mapping[str, str] = {}) -> None: ...
    def observe_seconds(self, name: str, value: Real, labels: Mapping[str, str] = {}) -> None: ...


class NoopTelemetry:
    """Validated sink that intentionally emits nothing."""

    def emit_event(self, name: str, fields: Mapping[str, object]) -> None:
        _validate_event(name, fields)

    def increment(self, name: str, labels: Mapping[str, str] = {}) -> None:
        if name not in _COUNTER_METRICS:
            raise ValueError("metric is not a counter")
        _validate_metric(name, 1, labels)

    def gauge(self, name: str, value: Real, labels: Mapping[str, str] = {}) -> None:
        if name not in _GAUGE_METRICS:
            raise ValueError("metric is not a gauge")
        _validate_metric(name, value, labels)

    def observe_seconds(self, name: str, value: Real, labels: Mapping[str, str] = {}) -> None:
        if name not in _OBSERVATION_METRICS:
            raise ValueError("metric is not a seconds observation")
        _validate_metric(name, value, labels)


class LoggingTelemetry:
    """Structured JSON provider using only Python's standard logging module."""

    def __init__(self, log: logging.Logger | None = None) -> None:
        self._log = log or logger

    def emit_event(self, name: str, fields: Mapping[str, object]) -> None:
        event, clean = _validate_event(name, fields)
        self._log.info(json.dumps({"event": event, **clean}, sort_keys=True, separators=(",", ":"), allow_nan=False))

    def increment(self, name: str, labels: Mapping[str, str] = {}) -> None:
        if name not in _COUNTER_METRICS:
            raise ValueError("metric is not a counter")
        metric, value, clean = _validate_metric(name, 1, labels)
        self._metric(metric, "counter", value, clean)

    def gauge(self, name: str, value: Real, labels: Mapping[str, str] = {}) -> None:
        if name not in _GAUGE_METRICS:
            raise ValueError("metric is not a gauge")
        metric, number, clean = _validate_metric(name, value, labels)
        self._metric(metric, "gauge", number, clean)

    def observe_seconds(self, name: str, value: Real, labels: Mapping[str, str] = {}) -> None:
        if name not in _OBSERVATION_METRICS:
            raise ValueError("metric is not a seconds observation")
        metric, number, clean = _validate_metric(name, value, labels)
        self._metric(metric, "observation", number, clean)

    def _metric(self, name: str, kind: str, value: float, labels: dict[str, str]) -> None:
        self._log.info(json.dumps({"metric": name, "kind": kind, "value": value, "labels": labels}, sort_keys=True, separators=(",", ":"), allow_nan=False))


def record_stage_failure(telemetry: MonitoringTelemetry, stage: str, outcome: str) -> None:
    """Emit a normalized A-D failure at the integration boundary that knows the stage."""
    fields = {"stage": stage, "outcome": outcome}
    _validate_event("monitoring.health_stage.failed", fields)
    labels = {"stage": stage, "outcome": outcome}
    _validate_metric("monitoring.health_stage.failures", 1, labels)
    try:
        telemetry.emit_event("monitoring.health_stage.failed", fields)
        telemetry.increment("monitoring.health_stage.failures", labels)
    except Exception:
        logger.warning("MONITORING_TELEMETRY_FAILURE")


def record_heartbeat(telemetry: MonitoringTelemetry, *, at: datetime, state: str, active: int, queued: int, age_seconds: Real = 0) -> None:
    fields = {"timestamp": at, "state": state, "active": active, "queued": queued}
    _validate_event("monitoring.worker.heartbeat", fields)
    _validate_metric("monitoring.worker.heartbeat_age_seconds", age_seconds, {})
    try:
        telemetry.emit_event("monitoring.worker.heartbeat", fields)
        telemetry.gauge("monitoring.worker.heartbeat_age_seconds", age_seconds)
    except Exception:
        logger.warning("MONITORING_TELEMETRY_FAILURE")


def config_snapshot(
    config: MonitoringConfig, policy: ConfirmationPolicy | None = None
) -> dict[str, object]:
    """Allowlisted non-secret configuration and confirmation-policy metadata."""
    if not isinstance(config, MonitoringConfig):
        raise TypeError("config must be a MonitoringConfig")
    if policy is not None and not isinstance(policy, ConfirmationPolicy):
        raise TypeError("policy must be a ConfirmationPolicy or None")
    snapshot: dict[str, object] = {
        field: getattr(config, field)
        for field in (
            "concurrency", "cycle_interval_seconds", "probe_timeout_seconds",
            "connect_timeout_seconds", "queue_bound", "shutdown_timeout_seconds",
            "jitter_ratio", "stale_after_seconds", "heartbeat_seconds",
            "ownership_lease_seconds", "db_operation_deadline_seconds",
            "recovery_max_attempts", "recovery_max_elapsed_seconds",
        )
    }
    snapshot["policy_status"] = "CONFIGURED" if policy is not None else "UNCONFIGURED"
    if policy is not None:
        snapshot["policy_version"] = policy.version
    return snapshot


__all__ = ["LoggingTelemetry", "MonitoringTelemetry", "NoopTelemetry", "config_snapshot", "record_heartbeat", "record_stage_failure"]
