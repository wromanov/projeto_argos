"""Automatic, evidence-bearing camera diagnostics for the future MON worker."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import StrEnum
import math
import os
import re
import time
from typing import Mapping
from uuid import UUID, uuid4

from django.core.exceptions import ValidationError

from cameras.integracao.capabilities import require_automatic_compatibility
from cameras.integracao.configuration import resolve_connection_config
from cameras.integracao.credentials import CredentialOperationError, resolve_active_credential_for_execution
from cameras.integracao.rtsp.gst_adapter import GStreamerRtspAdapter
from cameras.integracao.rtsp.ports import RtspConnectionRequest, RtspDiagnosticResult, RtspStage, StageStatus
from cameras.integracao.target_policy import TargetDecision, TargetPolicy, TargetPolicyError
from cameras.models import CameraConnectionConfig, CameraHealthSnapshot, EstadoMonitoramento
from cameras.monitoramento.contracts import ProbeResult, ProbeResultCode


_SAFE_ERROR_CODE = re.compile(r"^[A-Z][A-Z0-9_]{0,63}$")


class DiagnosticSource(StrEnum):
    MANUAL = "MANUAL"
    AUTOMATIC = "AUTOMATIC"


@dataclass(frozen=True, slots=True)
class HealthStageResult:
    stage: RtspStage
    state: StageStatus
    observed_at: datetime
    duration_seconds: float
    error_code: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.stage, RtspStage) or not isinstance(self.state, StageStatus):
            raise TypeError("stage and state must use diagnostic enums")
        if not isinstance(self.observed_at, datetime) or self.observed_at.utcoffset() is None:
            raise ValueError("stage observed_at must be timezone-aware")
        object.__setattr__(self, "observed_at", self.observed_at.astimezone(timezone.utc))
        if isinstance(self.duration_seconds, bool) or not isinstance(self.duration_seconds, (int, float)):
            raise TypeError("stage duration must be a finite number")
        if not math.isfinite(float(self.duration_seconds)) or self.duration_seconds < 0:
            raise ValueError("stage duration must be finite and non-negative")
        object.__setattr__(self, "duration_seconds", float(self.duration_seconds))
        if self.error_code is not None and (
            self.state is not StageStatus.FAIL or not _SAFE_ERROR_CODE.fullmatch(self.error_code)
        ):
            raise ValueError("stage error_code is invalid")


@dataclass(frozen=True, slots=True)
class ConnectionTestResult:
    camera_id: int
    stages: tuple[HealthStageResult, ...]
    config_version: int
    config_generation: int
    source: DiagnosticSource
    correlation_id: UUID
    probe_result: ProbeResult

    def __post_init__(self) -> None:
        stages = tuple(self.stages)
        if isinstance(self.camera_id, bool) or not isinstance(self.camera_id, int) or self.camera_id <= 0:
            raise ValueError("camera_id must be positive")
        if tuple(item.stage for item in stages) != tuple(RtspStage):
            raise ValueError("diagnostic must contain ordered A/B/C/D stages")
        object.__setattr__(self, "stages", stages)
        for index, item in enumerate(stages[:-1]):
            if item.state is not StageStatus.PASS and any(
                later.state is not StageStatus.NOT_RUN for later in stages[index + 1 :]
            ):
                raise ValueError("a failed or unrun stage requires subsequent stages to be NOT_RUN")
        if stages[3].state is StageStatus.PASS and any(item.state is not StageStatus.PASS for item in stages[:3]):
            raise ValueError("D PASS requires A, B and C PASS")
        for name in ("config_version", "config_generation"):
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
                raise ValueError(f"{name} must be positive")
        if not isinstance(self.source, DiagnosticSource):
            raise TypeError("source must be a DiagnosticSource")
        if not isinstance(self.correlation_id, UUID):
            raise TypeError("correlation_id must be a UUID")
        if not isinstance(self.probe_result, ProbeResult):
            raise TypeError("probe_result must be a ProbeResult")
        if self.probe_result.is_success and any(stage.state is not StageStatus.PASS for stage in stages):
            raise ValueError("SUCCESS requires A, B, C and D PASS")

    @property
    def observed_at(self) -> datetime:
        return self.probe_result.observed_at

    @property
    def reached_stage(self) -> str:
        reached = [stage.stage.value for stage in self.stages if stage.state is not StageStatus.NOT_RUN]
        return reached[-1] if reached else ""

    def snapshot_values(self) -> dict[str, object]:
        if self.source is not DiagnosticSource.AUTOMATIC:
            raise ValueError("only automatic diagnostics can be persisted")
        values: dict[str, object] = {
            "observed_at": self.observed_at,
            "config_generation": self.config_generation,
            "reached_stage": self.reached_stage,
            "correlation_id": self.correlation_id,
        }
        for item in self.stages:
            name = item.stage.value.lower()
            values.update({
                f"stage_{name}_state": item.state.value,
                f"stage_{name}_observed_at": item.observed_at,
                f"stage_{name}_duration_seconds": item.duration_seconds,
                f"stage_{name}_error_code": item.error_code or "",
            })
        return values


def _generation(camera_id: int) -> int:
    state = EstadoMonitoramento.objects.filter(camera_id=camera_id).only("ultima_geracao_configuracao").first()
    return state.ultima_geracao_configuracao if state else 1


def run_automatic_camera_diagnostic(
    *,
    camera_id: int,
    config_generation: int,
    target_policy: TargetPolicy | None = None,
    environ: Mapping[str, str] | None = None,
    adapter=None,
    timeout_seconds: float = 5.0,
    connect_timeout_seconds: float = 3.0,
    monotonic=time.monotonic,
    now=lambda: datetime.now(timezone.utc),
) -> ConnectionTestResult:
    """Run one fail-closed automatic attempt; this function never persists results."""
    if isinstance(camera_id, bool) or not isinstance(camera_id, int) or camera_id <= 0:
        raise ValueError("camera_id must be positive")
    if isinstance(config_generation, bool) or not isinstance(config_generation, int) or config_generation <= 0:
        raise ValueError("config_generation must be positive")
    started = monotonic()
    correlation_id = uuid4()
    config = CameraConnectionConfig.objects.select_related("camera", "profile").filter(camera_id=camera_id).first()
    if config is None:
        return _blocked(camera_id, ProbeResultCode.CONFIG_ERROR, "CONFIG_ERROR", config_generation, 1, correlation_id, now, monotonic, started)
    generation = _generation(camera_id)
    if generation != config_generation:
        return _blocked(camera_id, ProbeResultCode.CONFIG_ERROR, "CONFIG_CHANGED", config_generation, config.config_version, correlation_id, now, monotonic, started)
    if (
        config.camera.situacao_operacional != config.camera.SituacaoOperacional.PRODUCAO
        or not config.camera.cadastro_completo
    ):
        return _blocked(camera_id, ProbeResultCode.CONFIG_ERROR, "NOT_ELIGIBLE", config_generation, config.config_version, correlation_id, now, monotonic, started)
    try:
        source = os.environ if environ is None else environ
        policy = target_policy or TargetPolicy.from_environment(source)
        ports = policy.ports_by_scheme.get("rtsp", ())
        if not ports:
            raise TargetPolicyError()
        resolved = resolve_connection_config(camera_id=camera_id, environment_allowed_ports=ports, automatic=True)
        if resolved["adapter_key"] != "RTSP":
            raise ValidationError("unsupported automatic adapter")
        require_automatic_compatibility(config.camera, config.profile)
        checked = _authorize_target(policy, config, resolved)
        credential = None
        try:
            if config.credential_id is not None:
                credential = resolve_active_credential_for_execution(config=config)
            elif config.profile.credential_required:
                return _blocked(camera_id, ProbeResultCode.CONFIG_ERROR, "CREDENTIAL_UNAVAILABLE", config_generation, config.config_version, correlation_id, now, monotonic, started)
            current = CameraConnectionConfig.objects.select_related("camera", "profile").filter(pk=config.pk).first()
            if current is None or _config_identity(config) != _config_identity(current) or _generation(camera_id) != config_generation:
                return _blocked(camera_id, ProbeResultCode.CONFIG_ERROR, "CONFIG_CHANGED", config_generation, config.config_version, correlation_id, now, monotonic, started)
            if (
                current.camera.situacao_operacional != current.camera.SituacaoOperacional.PRODUCAO
                or not current.camera.cadastro_completo
            ):
                return _blocked(camera_id, ProbeResultCode.CONFIG_ERROR, "NOT_ELIGIBLE", config_generation, current.config_version, correlation_id, now, monotonic, started)
            resolved = resolve_connection_config(camera_id=camera_id, environment_allowed_ports=ports, automatic=True)
            checked = _authorize_target(policy, current, resolved)
            if adapter is None:
                adapter = GStreamerRtspAdapter(monotonic=monotonic, now=now)
            request = RtspConnectionRequest(
                camera_id=camera_id,
                target=checked,
                timeout_seconds=timeout_seconds,
                connect_timeout_seconds=min(connect_timeout_seconds, timeout_seconds),
                transport=current.transport,
                credential=credential,
            )
            try:
                result = adapter.probe(request)
            except Exception:
                # Provider exception text may contain target or credential data.
                return _blocked(camera_id, ProbeResultCode.INCONCLUSIVE, "ADAPTER_FAILURE", config_generation, config.config_version, correlation_id, now, monotonic, started)
        finally:
            credential = None
    except CredentialOperationError:
        return _blocked(camera_id, ProbeResultCode.CONFIG_ERROR, "CREDENTIAL_UNAVAILABLE", config_generation, config.config_version, correlation_id, now, monotonic, started)
    except TargetPolicyError:
        return _blocked(camera_id, ProbeResultCode.TARGET_BLOCKED, "TARGET_BLOCKED", config_generation, config.config_version, correlation_id, now, monotonic, started)
    except ValidationError:
        return _blocked(camera_id, ProbeResultCode.CONFIG_ERROR, "CONFIG_ERROR", config_generation, config.config_version, correlation_id, now, monotonic, started)
    except (TypeError, ValueError, KeyError):
        return _blocked(camera_id, ProbeResultCode.CONFIG_ERROR, "CONFIG_ERROR", config_generation, config.config_version, correlation_id, now, monotonic, started)
    if not isinstance(result, RtspDiagnosticResult):
        return _blocked(camera_id, ProbeResultCode.INCONCLUSIVE, "ADAPTER_FAILURE", config_generation, config.config_version, correlation_id, now, monotonic, started)
    return _connection_result(camera_id, result, config.config_version, config_generation, correlation_id)


def _config_identity(config) -> tuple[object, ...]:
    return (
        config.camera_id, config.profile_id, config.credential_id, config.enabled,
        config.rtsp_uri, config.transport, config.config_version,
        config.camera.ip, config.profile.active, config.profile.adapter_key,
        config.camera.situacao_operacional, config.camera.cadastro_completo,
    )


def _authorize_target(policy, config, resolved):
    profile = config.profile
    if not profile.allowed_ports:
        raise TargetPolicyError()
    default_port = 554 if 554 in profile.allowed_ports else profile.allowed_ports[0] if len(profile.allowed_ports) == 1 else None
    allowed_paths = None if "path" in (profile.allowed_override_fields or ()) else (profile.default_path,)
    checked = policy.validate(
        config.camera.ip, resolved["rtsp_uri"],
        allowed_schemes=tuple(profile.allowed_schemes), allowed_ports=tuple(profile.allowed_ports),
        default_port=default_port, allowed_paths=allowed_paths, farm=getattr(config.camera, "farm", None),
    )
    if checked.decision is not TargetDecision.AUTHORIZED_TARGET or checked.request is None:
        raise TargetPolicyError()
    return checked.request


def _connection_result(camera_id, result, config_version, config_generation, correlation_id):
    observed = result.observed_at
    stages = tuple(
        HealthStageResult(
            stage=item.stage,
            state=item.status,
            observed_at=item.observed_at,
            duration_seconds=item.duration_seconds,
            error_code=item.error_code,
        )
        for item in result.stages
    )
    automatic_success = stages[3].state is StageStatus.PASS
    probe = ProbeResult(
        code=ProbeResultCode.SUCCESS if automatic_success else result.category,
        observed_at=observed,
        duration_seconds=result.duration_seconds,
        error_code=None if automatic_success else result.error_code,
    )
    return ConnectionTestResult(
        camera_id, stages, config_version, config_generation, DiagnosticSource.AUTOMATIC, correlation_id, probe,
    )


def _blocked(camera_id, code, error_code, generation, config_version, correlation_id, now, monotonic, started):
    observed = now()
    if observed.utcoffset() is None:
        observed = observed.replace(tzinfo=timezone.utc)
    observed = observed.astimezone(timezone.utc)
    stages = tuple(
        HealthStageResult(stage, StageStatus.NOT_RUN, observed, 0.0)
        for stage in RtspStage
    )
    probe = ProbeResult(code, observed, max(0.0, monotonic() - started), error_code)
    return ConnectionTestResult(camera_id, stages, max(1, config_version), generation, DiagnosticSource.AUTOMATIC, correlation_id, probe)


__all__ = [
    "ConnectionTestResult", "DiagnosticSource", "HealthStageResult", "run_automatic_camera_diagnostic",
]
