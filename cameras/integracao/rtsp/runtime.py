"""Trusted per-invocation composition root for manual RTSP diagnostics."""

from __future__ import annotations

import os
import time
from datetime import datetime, timezone
from typing import Mapping

from cameras.integracao.target_policy import TargetPolicy, TargetPolicyError
from cameras.monitoramento.contracts import ProbeResultCode

from .ports import RtspDiagnosticResult, RtspStage, StageResult, StageStatus
from .service import run_camera_connection_test


def run_camera_connection_test_from_environment(
    *,
    actor,
    camera_id,
    environ: Mapping[str, str] | None = None,
    adapter=None,
    timeout_seconds=5.0,
    connect_timeout_seconds=3.0,
    monotonic=time.monotonic,
    now=lambda: datetime.now(timezone.utc),
) -> RtspDiagnosticResult:
    """Build policy from trusted environment and inject it into the service."""
    source = os.environ if environ is None else environ
    try:
        policy = TargetPolicy.from_environment(source)
    except TargetPolicyError:
        return _misconfigured_policy(now)

    rtsp_ports = policy.ports_by_scheme.get("rtsp", ())
    rtsp_paths = policy.allowed_paths_by_scheme.get("rtsp", ())
    if not rtsp_ports or not rtsp_paths:
        return _misconfigured_policy(now)

    return run_camera_connection_test(
        actor=actor,
        camera_id=camera_id,
        target_policy=policy,
        environment_allowed_ports=rtsp_ports,
        adapter=adapter,
        timeout_seconds=timeout_seconds,
        connect_timeout_seconds=connect_timeout_seconds,
        monotonic=monotonic,
        now=now,
    )


def _misconfigured_policy(now) -> RtspDiagnosticResult:
    observed = now()
    if observed.tzinfo is None or observed.utcoffset() is None:
        observed = observed.replace(tzinfo=timezone.utc)
    else:
        observed = observed.astimezone(timezone.utc)
    return RtspDiagnosticResult(
        stages=tuple(StageResult(stage, StageStatus.NOT_RUN, observed_at=observed, duration_seconds=0.0) for stage in RtspStage),
        category=ProbeResultCode.TARGET_BLOCKED,
        observed_at=observed,
        duration_seconds=0.0,
        error_code="MISCONFIGURED_POLICY",
    )
