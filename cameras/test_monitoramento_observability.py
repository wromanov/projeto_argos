"""Fakes e testes locais do contrato MON-OBS."""

from datetime import datetime, timezone
import json
import logging
import unittest

from .monitoramento.confirmation import ConfirmationPolicy
from .monitoramento.contracts import ProbeResult, ProbeResultCode
from .monitoramento.fakes import FakeClock
from .monitoramento.observability import (
    LoggingTelemetry,
    NoopTelemetry,
    config_snapshot,
    record_heartbeat,
    record_stage_failure,
)
from .monitoramento.scheduler import DueScheduler
from .monitoramento.schemas import CompletionDisposition, MonitoringConfig, ScheduleCandidate

START = datetime(2026, 9, 1, 12, 0, tzinfo=timezone.utc)


class FakeTelemetry:
    def __init__(self):
        self.events = []
        self.counters = []
        self.gauges = []
        self.observations = []
        self.validator = NoopTelemetry()

    def emit_event(self, name, fields):
        self.validator.emit_event(name, fields)
        self.events.append((name, dict(fields)))

    def increment(self, name, labels=None):
        labels = {} if labels is None else labels
        self.validator.increment(name, labels)
        self.counters.append((name, dict(labels)))

    def gauge(self, name, value, labels=None):
        labels = {} if labels is None else labels
        self.validator.gauge(name, value, labels)
        self.gauges.append((name, value, dict(labels)))

    def observe_seconds(self, name, value, labels=None):
        labels = {} if labels is None else labels
        self.validator.observe_seconds(name, value, labels)
        self.observations.append((name, value, dict(labels)))


class BrokenTelemetry:
    def emit_event(self, *_args, **_kwargs):
        fake_url = "https://" + "user" + ":" + "secret" + "@example.invalid/path"
        raise RuntimeError(f"sink contains {fake_url}")

    increment = emit_event
    gauge = emit_event
    observe_seconds = emit_event


class OwnershipDeniedPort:
    policy = ConfirmationPolicy(2, 2, "v1")

    def load(self, _candidate, _policy):
        raise AssertionError("denied lease must not reach confirmation")

    def store(self, *_args, **_kwargs):
        raise AssertionError("denied lease must not reach persistence")

    def claim(self, _camera_id, _owner_id, _lease_seconds):
        return None

    def release(self, _camera_id, _ownership):
        return True


class ObservabilityProviderTests(unittest.TestCase):
    def test_noop_accepts_valid_calls_and_rejects_invalid_values_and_labels(self):
        telemetry = NoopTelemetry()
        telemetry.emit_event("monitoring.health_stage.failed", {"stage": "A", "outcome": "TIMEOUT"})
        telemetry.increment("monitoring.probe.outcomes", {"outcome": "SUCCESS"})
        telemetry.gauge("monitoring.queue.depth", 2)
        telemetry.observe_seconds("monitoring.cycle.duration_seconds", 0.25)
        with self.assertRaises(ValueError):
            telemetry.gauge("monitoring.queue.depth", float("nan"))
        with self.assertRaises(ValueError):
            telemetry.increment("monitoring.probe.outcomes", {"camera_id": "1"})

    def test_event_allowlist_rejects_uri_secret_and_uncontracted_fields(self):
        telemetry = NoopTelemetry()
        with self.assertRaises(ValueError):
            fake_code = "https://" + "user" + ":" + "password" + "@host/path"
            telemetry.emit_event("monitoring.repository.failed", {"error_code": fake_code})
        with self.assertRaises(ValueError):
            fake_uri = "rtsp" + "://" + "user" + ":" + "password" + "@host"
            telemetry.emit_event("monitoring.probe.completed", {"outcome": "SUCCESS", "uri": fake_uri})

    def test_config_snapshot_contains_only_typed_operational_values(self):
        snapshot = config_snapshot(MonitoringConfig())
        self.assertIn("concurrency", snapshot)
        self.assertEqual(snapshot["policy_status"], "UNCONFIGURED")
        self.assertNotIn("password", snapshot)
        self.assertNotIn("uri", snapshot)

    def test_config_snapshot_records_only_confirmation_policy_version_and_status(self):
        policy = ConfirmationPolicy(2, 1, "policy-v3")
        snapshot = config_snapshot(MonitoringConfig(), policy)
        self.assertEqual(snapshot["policy_status"], "CONFIGURED")
        self.assertEqual(snapshot["policy_version"], "policy-v3")
        self.assertNotIn("failures_to_offline", snapshot)
        self.assertNotIn("successes_to_online", snapshot)

    def test_logging_provider_emits_deterministic_json(self):
        log = logging.getLogger("argos.monobs.test")
        telemetry = LoggingTelemetry(log)
        with self.assertLogs(log, level="INFO") as captured:
            telemetry.emit_event("monitoring.health_stage.failed", {"stage": "C", "outcome": "TIMEOUT"})
        payload = json.loads(captured.output[0].split(":", 2)[-1])
        self.assertEqual(payload, {"event": "monitoring.health_stage.failed", "outcome": "TIMEOUT", "stage": "C"})

    def test_stage_failure_and_heartbeat_signals(self):
        telemetry = FakeTelemetry()
        record_stage_failure(telemetry, "D", "PROTOCOL_ERROR")
        record_heartbeat(telemetry, at=START, state="RUNNING", active=1, queued=2, age_seconds=0)
        self.assertIn(("monitoring.health_stage.failures", {"stage": "D", "outcome": "PROTOCOL_ERROR"}), telemetry.counters)
        self.assertTrue(any(name == "monitoring.worker.heartbeat" for name, _ in telemetry.events))

    def test_scheduler_emits_cycle_probe_and_queue_signals(self):
        telemetry = FakeTelemetry()
        clock = FakeClock(start_at=START)
        scheduler = DueScheduler(MonitoringConfig(concurrency=1), clock, telemetry=telemetry)
        report = scheduler.tick(START, [ScheduleCandidate(1, START)])
        self.assertEqual(report.admitted, 1)
        attempt = report.attempts[0]
        outcome = scheduler.complete(attempt.attempt_id, ProbeResult(ProbeResultCode.SUCCESS, START, 0.2))
        self.assertEqual(outcome.disposition, CompletionDisposition.ACCEPTED)
        names = [name for name, _ in telemetry.events]
        self.assertIn("monitoring.cycle.started", names)
        self.assertIn("monitoring.cycle.completed", names)
        self.assertIn("monitoring.config.snapshot", names)
        self.assertIn("monitoring.worker.heartbeat", names)
        self.assertTrue(any(name == "monitoring.probe.outcomes" and labels == {"outcome": "SUCCESS"} for name, labels in telemetry.counters))
        self.assertTrue(any(name == "monitoring.probe.duration_seconds" for name, _value, _labels in telemetry.observations))
        self.assertIn(("monitoring.attempts.started", {}), telemetry.counters)
        self.assertIn(("monitoring.attempts.completed", {}), telemetry.counters)
        lifecycle_states = [fields["state"] for name, fields in telemetry.events if name == "monitoring.scheduler.lifecycle"]
        self.assertIn("RUNNING", lifecycle_states)
        scheduler.request_shutdown(START)
        self.assertEqual(scheduler.lifecycle.value, "STOPPED")
        lifecycle_states = [fields["state"] for name, fields in telemetry.events if name == "monitoring.scheduler.lifecycle"]
        self.assertIn("DRAINING", lifecycle_states)
        self.assertIn("STOPPED", lifecycle_states)
        scheduler.complete(attempt.attempt_id, ProbeResult(ProbeResultCode.SUCCESS, START, 0.2))
        self.assertEqual(sum(name == "monitoring.probe.outcomes" for name, _ in telemetry.counters), 1)

    def test_lease_contention_is_signaled_without_domain_failure(self):
        telemetry = FakeTelemetry()
        clock = FakeClock(start_at=START)
        port = OwnershipDeniedPort()
        scheduler = DueScheduler(
            MonitoringConfig(concurrency=1), clock,
            confirmation_port=port, confirmation_policy=port.policy,
            ownership_port=port, service_instance_id="test-worker", telemetry=telemetry,
        )
        report = scheduler.tick(START, [ScheduleCandidate(1, START)])
        self.assertEqual(report.attempts, ())
        self.assertEqual(scheduler.lifecycle.value, "RUNNING")
        self.assertIn(("monitoring.ownership", {"outcome": "DENIED"}), telemetry.events)

    def test_repository_failure_uses_safe_code_and_emits_signal(self):
        telemetry = FakeTelemetry()
        scheduler = DueScheduler(MonitoringConfig(), FakeClock(start_at=START), telemetry=telemetry)
        scheduler.report_repository_failure("DATABASE_UNAVAILABLE")
        self.assertIn(("monitoring.repository.failed", {"error_code": "DATABASE_UNAVAILABLE"}), telemetry.events)
        self.assertIn(("monitoring.repository.failures", {"error_code": "DATABASE_UNAVAILABLE"}), telemetry.counters)
        with self.assertRaises(ValueError):
            fake_code = "https://" + "user" + ":" + "secret" + "@db"
            scheduler.report_repository_failure(fake_code)

    def test_sink_failure_does_not_change_scheduler_domain_result(self):
        clock = FakeClock(start_at=START)
        scheduler = DueScheduler(MonitoringConfig(concurrency=1), clock, telemetry=BrokenTelemetry())
        with self.assertLogs("cameras.monitoramento.scheduler", level="WARNING") as captured:
            report = scheduler.tick(START, [ScheduleCandidate(1, START)])
            attempt = report.attempts[0]
            result = scheduler.complete(attempt.attempt_id, ProbeResult(ProbeResultCode.SUCCESS, START, 0.1))
        self.assertNotIn("secret", "\n".join(captured.output))
        self.assertNotIn("example.invalid", "\n".join(captured.output))
        self.assertEqual(result.disposition, CompletionDisposition.ACCEPTED)
        self.assertEqual(scheduler.lifecycle.value, "RUNNING")
        self.assertEqual(scheduler.runtime_status.attempts_completed, 1)


if __name__ == "__main__":
    unittest.main()
