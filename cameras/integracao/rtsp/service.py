"""Manual A→B→C→D diagnostic composition; no monitoring-state writes."""
from datetime import datetime, timezone
import time
from django.core.exceptions import PermissionDenied, ValidationError
from cameras.authorization import require_camera_permission
from cameras.integracao.capabilities import COMPATIBILITY_SUPPORTED, require_manual_discovery
from cameras.integracao.configuration import resolve_connection_config
from cameras.integracao.credentials import CredentialOperationError, resolve_active_credential_for_execution
from cameras.integracao.target_policy import TargetDecision, TargetPolicy
from cameras.models import CameraConnectionConfig
from cameras.monitoramento.contracts import ProbeResultCode
from .gst_adapter import GStreamerRtspAdapter
from .ports import RtspConnectionRequest, RtspDiagnosticResult, RtspStage, StageResult, StageStatus

def run_camera_connection_test(*, actor, camera_id, target_policy, environment_allowed_ports,
                               adapter=None, timeout_seconds=5.0, connect_timeout_seconds=3.0,
                               monotonic=time.monotonic, now=lambda: datetime.now(timezone.utc)):
    """Authorize, validate target, resolve active credential, then call the port."""
    require_camera_permission(actor=actor, permission_codename="run_camera_connection_test", camera_id=camera_id)
    if not isinstance(target_policy, TargetPolicy):
        return _blocked("MISCONFIGURED_POLICY", now)
    config = CameraConnectionConfig.objects.select_related("camera", "profile").filter(camera_id=camera_id).first()
    if config is None:
        return _blocked("CONFIG_ERROR", now)
    try:
        discovery = require_manual_discovery(actor=actor, camera=config.camera, profile=config.profile)
        resolved = resolve_connection_config(camera_id=camera_id, environment_allowed_ports=environment_allowed_ports, automatic=False)
    except (ValidationError, PermissionDenied):
        return _blocked("CONFIG_ERROR", now)
    if resolved["compatibility"] not in {COMPATIBILITY_SUPPORTED, discovery["compatibility"]}:
        return _blocked("UNSUPPORTED_CAPABILITY", now)
    checked, error = _authorize_target(target_policy, config, resolved)
    if error:
        return _blocked(error, now)
    if adapter is None:
        adapter = GStreamerRtspAdapter(monotonic=monotonic, now=now)
    credential = None
    try:
        if config.credential_id is not None:
            credential = resolve_active_credential_for_execution(config=config)
        elif config.profile.credential_required:
            return _blocked("CREDENTIAL_UNAVAILABLE", now)
        # Re-read effective config and re-apply CAM-INT-07 immediately before the port.
        current = CameraConnectionConfig.objects.select_related("camera", "profile").filter(pk=config.pk).first()
        if current is None or _config_changed(config, current):
            return _blocked("CONFIG_ERROR", now)
        current_resolved = resolve_connection_config(camera_id=camera_id, environment_allowed_ports=environment_allowed_ports, automatic=False)
        checked, error = _authorize_target(target_policy, current, current_resolved)
        if error:
            return _blocked(error, now)
        request = RtspConnectionRequest(camera_id, checked, timeout_seconds,
            min(connect_timeout_seconds, timeout_seconds), current.transport, credential)
        return adapter.probe(request)
    except CredentialOperationError:
        return _blocked("CREDENTIAL_UNAVAILABLE", now)
    except (TypeError, ValueError, ValidationError):
        return _blocked("CONFIG_ERROR", now)
    finally:
        credential = None

def _config_changed(before, after):
    fields = ("camera_id", "profile_id", "credential_id", "enabled", "rtsp_uri",
              "http_endpoint_override", "http_port_override", "transport", "config_version")
    return any(getattr(before, field) != getattr(after, field) for field in fields)

def _authorize_target(policy, config, resolved):
    profile = config.profile
    if not profile.allowed_ports:
        return None, "MISCONFIGURED_POLICY"
    default_port = 554 if 554 in profile.allowed_ports else profile.allowed_ports[0] if len(profile.allowed_ports) == 1 else None
    allowed_paths = None if "path" in (profile.allowed_override_fields or ()) else (profile.default_path,)
    checked = policy.validate(config.camera.ip, resolved["rtsp_uri"],
        allowed_schemes=tuple(profile.allowed_schemes), allowed_ports=tuple(profile.allowed_ports),
        default_port=default_port, allowed_paths=allowed_paths, farm=getattr(config.camera, "farm", None))
    if checked.decision is TargetDecision.MISCONFIGURED_POLICY:
        return None, "MISCONFIGURED_POLICY"
    if not checked.authorized or checked.request is None:
        return None, "TARGET_BLOCKED"
    return checked.request, None

def _blocked(error_code, now):
    observed = now()
    if observed.tzinfo is None or observed.utcoffset() is None:
        observed = observed.replace(tzinfo=timezone.utc)
    observed = observed.astimezone(timezone.utc)
    return RtspDiagnosticResult((
        StageResult(RtspStage.NETWORK_REACHABILITY, StageStatus.NOT_RUN, observed_at=observed, duration_seconds=0.0),
        StageResult(RtspStage.RTSP_REACHABILITY, StageStatus.NOT_RUN, observed_at=observed, duration_seconds=0.0),
        StageResult(RtspStage.MEDIA_DESCRIPTION, StageStatus.NOT_RUN, observed_at=observed, duration_seconds=0.0),
        StageResult(RtspStage.MEDIA_DELIVERY, StageStatus.NOT_RUN, observed_at=observed, duration_seconds=0.0)),
        ProbeResultCode.TARGET_BLOCKED if error_code in {"TARGET_BLOCKED", "MISCONFIGURED_POLICY"} else ProbeResultCode.INCONCLUSIVE,
        observed, 0.0, error_code)
