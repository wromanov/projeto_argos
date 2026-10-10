from __future__ import annotations

import asyncio
from dataclasses import dataclass
from datetime import datetime, timezone
import logging
import os
import signal
import time
from typing import Callable, Mapping
from uuid import uuid4

from django.core.exceptions import ImproperlyConfigured
from django.db import close_old_connections, connection
from django.utils.module_loading import import_string

from cameras.integracao.rtsp.gst_adapter import GStreamerRtspAdapter, GStreamerUnavailable
from cameras.integracao.target_policy import TargetPolicy
from cameras.monitoramento.confirmation import ConfirmationPolicy
from cameras.monitoramento.contracts import ProbeResult
from cameras.monitoramento.observability import LoggingTelemetry, MonitoringTelemetry, record_heartbeat
from cameras.monitoramento.repository import DjangoMonitoringRepository
from cameras.monitoramento.scheduler import DueScheduler
from cameras.monitoramento.schemas import Attempt, CompletionDisposition, MonitoringConfig, SchedulerLifecycle
from cameras.monitoramento.clock import SystemClock
from cameras.integracao.diagnostics import run_automatic_camera_diagnostic

logger = logging.getLogger(__name__)


class RuntimeOperationDeadline(RuntimeError):
    """An ORM producer exceeded its budget and remains tracked until it returns."""


class RuntimePreflightError(RuntimeError):
    """Falha operacional sanitizada antes de qualquer admissão."""

    def __init__(self, code: str) -> None:
        if not code.isupper() or not code.replace("_", "").isalnum():
            raise ValueError("preflight error code must be sanitized")
        self.code = code
        super().__init__(code)


@dataclass(frozen=True, slots=True)
class RuntimeDependencies:
    config: MonitoringConfig
    confirmation_policy: ConfirmationPolicy
    target_policy: TargetPolicy
    repository: object
    telemetry: MonitoringTelemetry
    diagnostic: Callable[..., object] = run_automatic_camera_diagnostic
    database_preflight: Callable[[], None] | None = None
    adapter_preflight: Callable[[], None] | None = None
    credential_preflight: Callable[[], None] | None = None
    clock: object | None = None


class MonitoringWorkerRuntime:
    """Orquestra o core MON existente sem executar I/O bloqueante no event loop."""

    def __init__(self, dependencies: RuntimeDependencies, *, worker_id: str | None = None) -> None:
        self.dependencies = dependencies
        self.config = dependencies.config
        self.repository = dependencies.repository
        self.worker_id = worker_id or f"argos-mon-{uuid4()}"
        if not isinstance(self.worker_id, str) or not self.worker_id.startswith("argos-mon-") or len(self.worker_id) > 64:
            raise ValueError("worker_id is invalid")
        clock = dependencies.clock or SystemClock()
        self.scheduler = DueScheduler(
            self.config,
            clock,
            current_generation=self.repository.current_generation,
            is_eligible=self.repository.is_eligible,
            confirmation_port=self.repository,
            confirmation_policy=dependencies.confirmation_policy,
            ownership_port=self.repository,
            service_instance_id=self.worker_id,
            telemetry=dependencies.telemetry,
        )
        self._lock = asyncio.Lock()
        self._stop = asyncio.Event()
        self._attempt_tasks: dict[object, asyncio.Task[None]] = {}
        self._cursor = 0
        self._last_counts = (0, 0)
        self._recovery_started: float | None = None
        self._recovery_attempts = 0
        self._recovery_delay = min(self.config.heartbeat_seconds, self.config.cycle_interval_seconds)
        self.incomplete = False
        self._database_pending: asyncio.Task | None = None
        self._operation_deadline_event = asyncio.Event()
        self._shutdown_started = False

    @staticmethod
    def _database_preflight() -> None:
        try:
            connection.ensure_connection()
        finally:
            close_old_connections()

    @staticmethod
    def _adapter_preflight() -> None:
        adapter = GStreamerRtspAdapter()
        try:
            adapter.loader()
        except GStreamerUnavailable as exc:
            raise RuntimePreflightError("ADAPTER_UNAVAILABLE") from exc

    @staticmethod
    def _credential_preflight() -> None:
        from django.db.models import Q
        from cameras.integracao.key_provider import CredentialKeyError, get_environment_key_provider
        from cameras.models import CameraConnectionConfig

        versions = CameraConnectionConfig.objects.filter(
            enabled=True,
            profile__adapter_key="RTSP",
        ).filter(
            Q(profile__credential_required=True) | Q(credential__isnull=False)
        ).values_list("credential_id", "credential__active_version__key_version").distinct()
        required_versions = tuple(versions)
        if not required_versions:
            return
        try:
            provider = get_environment_key_provider()
            provider.active_key()
            for credential_id, key_version in required_versions:
                if credential_id is None or not key_version:
                    raise RuntimePreflightError("CREDENTIAL_UNAVAILABLE")
                provider.key_for_version(key_version)
        except CredentialKeyError as exc:
            raise RuntimePreflightError("CREDENTIAL_PROVIDER_UNAVAILABLE") from exc

    async def _database_call(self, function, *args, **kwargs):
        if self._database_pending is not None:
            raise RuntimeOperationDeadline("a prior database operation is still running")
        operation = asyncio.create_task(asyncio.to_thread(function, *args, **kwargs))
        done, _ = await asyncio.wait({operation}, timeout=self.config.db_operation_deadline_seconds)
        if not done:
            self._database_pending = operation
            self.incomplete = True
            self._operation_deadline_event.set()
            raise RuntimeOperationDeadline("database operation exceeded its deadline")
        return operation.result()

    async def preflight(self) -> None:
        if not isinstance(self.config, MonitoringConfig):
            raise RuntimePreflightError("CONFIG_INVALID")
        if not isinstance(self.dependencies.target_policy, TargetPolicy):
            raise RuntimePreflightError("TARGET_POLICY_INVALID")
        if not callable(self.dependencies.diagnostic):
            raise RuntimePreflightError("DIAGNOSTIC_UNAVAILABLE")
        checks = (
            (self.dependencies.database_preflight or self._database_preflight, "DATABASE_UNAVAILABLE"),
            (self.dependencies.credential_preflight or self._credential_preflight, "CREDENTIAL_PROVIDER_UNAVAILABLE"),
            (self.dependencies.adapter_preflight or self._adapter_preflight, "ADAPTER_UNAVAILABLE"),
        )
        for check, code in checks:
            try:
                await asyncio.to_thread(check)
            except RuntimePreflightError:
                raise
            except Exception as exc:
                raise RuntimePreflightError(code) from exc

    async def run(self, *, once: bool = False) -> bool:
        await self.preflight()
        async with self._lock:
            await asyncio.to_thread(self.scheduler.start)
        heartbeat = asyncio.create_task(self._heartbeat_loop(), name="monitoring-heartbeat")
        try:
            while not self._stop.is_set():
                if self.scheduler.lifecycle is SchedulerLifecycle.DEGRADED and not self.scheduler.active_count and not self._attempt_tasks:
                    await self._recover()
                if self.incomplete and not self._attempt_tasks:
                    break
                await self._run_cycle()
                if once or self.incomplete:
                    break
                try:
                    await asyncio.wait_for(self._stop.wait(), timeout=self.config.cycle_interval_seconds)
                except TimeoutError:
                    pass
        finally:
            graceful = await self.shutdown()
            self._stop.set()
            await heartbeat
        return graceful

    async def _run_cycle(self) -> None:
        async with self._lock:
            if self.scheduler.lifecycle in (SchedulerLifecycle.DRAINING, SchedulerLifecycle.STOPPED, SchedulerLifecycle.DEGRADED):
                return
            free_queue = self.config.queue_bound - self.scheduler.queued_count
            limit = max(0, min(self.config.queue_bound, free_queue))
            candidates = ()
            if limit:
                try:
                    page = await self._database_call(
                        self.repository.list_due_page,
                        datetime.now(timezone.utc),
                        limit,
                        after_camera_id=self._cursor,
                        exclude_camera_ids=self.scheduler.pending_camera_ids,
                    )
                    candidates = page.candidates
                    self._cursor = page.next_camera_id if page.has_more else 0
                except RuntimeOperationDeadline:
                    return
                except Exception as exc:
                    await asyncio.to_thread(self.scheduler.report_repository_failure, type(exc).__name__)
                    return
            now = datetime.now(timezone.utc)
            try:
                report = await self._database_call(self.scheduler.tick, now, candidates)
            except RuntimeOperationDeadline:
                return
            self._last_counts = report.active, report.queued
            self._launch_pending_attempts(report.attempts)

    def _launch_pending_attempts(self, attempts) -> None:
        for attempt in attempts:
            if attempt.attempt_id not in self._attempt_tasks:
                task = asyncio.create_task(self._execute_attempt(attempt), name=f"monitoring-attempt-{attempt.attempt_id}")
                self._attempt_tasks[attempt.attempt_id] = task
                task.add_done_callback(lambda _done, key=attempt.attempt_id: self._attempt_tasks.pop(key, None))

    async def _execute_attempt(self, attempt: Attempt) -> None:
        try:
            diagnostic = await asyncio.to_thread(
                self.dependencies.diagnostic,
                camera_id=attempt.camera_id,
                config_generation=attempt.config_generation,
                target_policy=self.dependencies.target_policy,
                timeout_seconds=self.config.probe_timeout_seconds,
                connect_timeout_seconds=self.config.connect_timeout_seconds,
            )
            result = diagnostic.probe_result
        except Exception as exc:
            # The diagnostic producer has returned; cancellation is neutral and safe to release.
            async with self._lock:
                try:
                    await self._database_call(self.scheduler.cancel, attempt.attempt_id, producer_terminated=True)
                except RuntimeOperationDeadline:
                    return
                await asyncio.to_thread(self.scheduler.report_repository_failure, type(exc).__name__)
            return
        async with self._lock:
            try:
                outcome = await asyncio.to_thread(
                    self.scheduler.complete,
                    attempt.attempt_id,
                    result,
                    datetime.now(timezone.utc),
                    diagnostic=diagnostic,
                    producer_terminated=True,
                )
                self._launch_pending_attempts(self.scheduler.active_attempts)
                if outcome.disposition is CompletionDisposition.OPERATIONAL_FAILURE:
                    self.incomplete = True
            except KeyError:
                logger.warning("MONITORING_CALLBACK_REJECTED code=UNKNOWN_OR_EVICTED")
            except RuntimeOperationDeadline:
                return
            except Exception as exc:
                await asyncio.to_thread(self.scheduler.report_repository_failure, type(exc).__name__)

    async def _heartbeat_loop(self) -> None:
        while True:
            active, queued = self._last_counts
            record_heartbeat(
                self.dependencies.telemetry,
                at=datetime.now(timezone.utc),
                state=("DRAINING" if self._shutdown_started else "DEGRADED" if self._database_pending is not None else self.scheduler.lifecycle.value),
                active=active,
                queued=queued,
                age_seconds=0,
            )
            try:
                await asyncio.wait_for(self._stop.wait(), timeout=self.config.heartbeat_seconds)
                return
            except TimeoutError:
                continue

    async def _recover(self) -> None:
        if self._recovery_started is None:
            self._recovery_started = time.monotonic()
            self._recovery_attempts = 0
        while not self._stop.is_set():
            elapsed = time.monotonic() - self._recovery_started
            if self._recovery_attempts >= self.config.recovery_max_attempts or elapsed >= self.config.recovery_max_elapsed_seconds:
                self.incomplete = True
                return
            delay = min(self._recovery_delay, self.config.recovery_max_elapsed_seconds - elapsed)
            try:
                await asyncio.wait_for(self._stop.wait(), timeout=max(0, delay))
                return
            except TimeoutError:
                pass
            self._recovery_attempts += 1
            check = asyncio.create_task(asyncio.to_thread(self.dependencies.database_preflight or self._database_preflight))
            done, _ = await asyncio.wait({check}, timeout=min(self.config.db_operation_deadline_seconds, max(0.1, self.config.recovery_max_elapsed_seconds - (time.monotonic() - self._recovery_started))))
            if not done:
                # The operation continues in its thread. Do not retry or admit while it is live.
                self.incomplete = True
                self._operation_deadline_event.set()
                try:
                    await check
                except Exception:
                    pass
                return
            try:
                check.result()
            except Exception:
                self._recovery_delay = min(self.config.cycle_interval_seconds, max(self._recovery_delay, 1) * 2)
                continue
            if self.scheduler.active_count or self._attempt_tasks:
                return
            async with self._lock:
                await asyncio.to_thread(self.scheduler.start)
            self._recovery_started = None
            self._recovery_attempts = 0
            self._recovery_delay = min(self.config.heartbeat_seconds, self.config.cycle_interval_seconds)
            return

    async def shutdown(self) -> bool:
        started = time.monotonic()
        global_deadline = started + self.config.shutdown_timeout_seconds
        drain_deadline = started + self.config.shutdown_timeout_seconds / 2
        self._shutdown_started = True

        # A timed-out ORM call remains a live producer. Wait for its actual return
        # before touching scheduler state or claiming STOPPED.
        if self._database_pending is not None:
            _, pending_db = await asyncio.wait(
                {self._database_pending}, timeout=max(0, drain_deadline - time.monotonic())
            )
            if pending_db and time.monotonic() < global_deadline:
                _, pending_db = await asyncio.wait(
                    pending_db, timeout=max(0, global_deadline - time.monotonic())
                )
            if pending_db:
                self.incomplete = True
                return False
            try:
                self._database_pending.result()
            except Exception:
                pass
            self._database_pending = None

        async with self._lock:
            await asyncio.to_thread(self.scheduler.request_shutdown, datetime.now(timezone.utc))
        pending = {task for task in self._attempt_tasks.values() if not task.done()}
        if pending:
            _, pending = await asyncio.wait(pending, timeout=max(0, drain_deadline - time.monotonic()))
        if pending:
            # Keep the underlying native/thread producer pinned through the global deadline.
            _, pending = await asyncio.wait(pending, timeout=max(0, global_deadline - time.monotonic()))
        if pending:
            self.incomplete = True
        async with self._lock:
            if not pending and self.scheduler.finish_shutdown_if_quiescent():
                pass
            elif self.incomplete:
                self.scheduler.mark_shutdown_incomplete()
        return not self.incomplete and self.scheduler.lifecycle is SchedulerLifecycle.STOPPED


def build_runtime() -> MonitoringWorkerRuntime:
    """Compose production adapters from trusted Django settings/environment."""
    from django.conf import settings
    from cameras.monitoramento.confirmation import ConfirmationPolicy
    from config.environment import get_monitoring_config_from_environment

    try:
        config = get_monitoring_config_from_environment()
        policy_spec = getattr(settings, "MONITORING_CONFIRMATION_POLICY", None)
        if not isinstance(policy_spec, Mapping):
            raise ImproperlyConfigured("confirmation policy is not configured")
        confirmation = ConfirmationPolicy(
            failures_to_offline=policy_spec["failures_to_offline"],
            successes_to_online=policy_spec["successes_to_online"],
            version=policy_spec["version"],
        )
    except Exception as exc:
        raise RuntimePreflightError("CONFIG_INVALID") from exc
    try:
        target_policy = TargetPolicy.from_environment(os.environ)
    except Exception as exc:
        raise RuntimePreflightError("TARGET_POLICY_INVALID") from exc
    repository = DjangoMonitoringRepository()
    telemetry = LoggingTelemetry()
    return MonitoringWorkerRuntime(RuntimeDependencies(config, confirmation, target_policy, repository, telemetry))


__all__ = ["MonitoringWorkerRuntime", "RuntimeDependencies", "RuntimeOperationDeadline", "RuntimePreflightError", "build_runtime"]
