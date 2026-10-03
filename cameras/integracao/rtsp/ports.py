"""Typed boundaries for one bounded RTSP attempt and session."""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
from threading import Event
import math
from numbers import Real
from typing import Protocol
import re
from urllib.parse import urlunsplit
from uuid import UUID

from cameras.integracao.credentials import ResolvedCameraCredential
from cameras.integracao.target_policy import AuthorizedTargetRequest
from cameras.monitoramento.contracts import ProbeResultCode

class RtspStage(StrEnum):
    NETWORK_REACHABILITY = "A"
    RTSP_REACHABILITY = "B"
    MEDIA_DESCRIPTION = "C"
    MEDIA_DELIVERY = "D"

class StageStatus(StrEnum):
    PASS = "PASS"
    FAIL = "FAIL"
    NOT_RUN = "NOT_RUN"

_CODE = re.compile(r"^[A-Z][A-Z0-9_]{0,63}$")

@dataclass(frozen=True, slots=True)
class StageResult:
    stage: RtspStage
    status: StageStatus
    error_code: str | None = None
    def __post_init__(self):
        if not isinstance(self.stage, RtspStage) or not isinstance(self.status, StageStatus):
            raise TypeError("stage/status must use RTSP enums")
        if self.error_code is not None and (not _CODE.fullmatch(self.error_code) or self.status is not StageStatus.FAIL):
            raise ValueError("failed stage error code is invalid")

@dataclass(frozen=True, slots=True)
class RtspSession:
    """Opaque session handle; it contains no SDP, frame, URI, or secret."""
    id: UUID
    codec: str
    def __post_init__(self):
        if not isinstance(self.id, UUID): raise TypeError("session id must be a UUID")
        if not isinstance(self.codec, str) or not re.fullmatch(r"[A-Za-z0-9_.+-]{1,32}", self.codec):
            raise ValueError("codec identifier is not safe")

@dataclass(frozen=True, slots=True)
class RtspConnectionRequest:
    camera_id: int
    target: AuthorizedTargetRequest
    timeout_seconds: float
    connect_timeout_seconds: float
    transport: str = "AUTO"
    credential: ResolvedCameraCredential | None = field(default=None, repr=False)
    cancel_event: Event = field(default_factory=Event, repr=False, compare=False)
    def __post_init__(self):
        if isinstance(self.camera_id, bool) or not isinstance(self.camera_id, int) or self.camera_id <= 0:
            raise ValueError("camera_id must be positive")
        if not isinstance(self.target, AuthorizedTargetRequest) or self.target.scheme != "rtsp":
            raise TypeError("target must be an authorized RTSP target")
        for name in ("timeout_seconds", "connect_timeout_seconds"):
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, Real) or not math.isfinite(float(value)) or not 0 < float(value) <= 30:
                raise ValueError(f"{name} must be between 0 and 30 seconds")
            object.__setattr__(self, name, float(value))
        if self.connect_timeout_seconds > self.timeout_seconds:
            raise ValueError("connect timeout exceeds overall timeout")
        if self.transport not in {"AUTO", "TCP", "UDP"}:
            raise ValueError("unsupported RTSP transport")
        if self.credential is not None and not isinstance(self.credential, ResolvedCameraCredential):
            raise TypeError("credential must be the public R1 value object")
        if not isinstance(self.cancel_event, Event):
            raise TypeError("cancel_event must be a threading Event")
        if (not self.target.path.startswith("/") or any(ord(c) < 32 for c in self.target.path)
                or any(marker in self.target.path for marker in ("?", "#", "\\"))
                or any(part == ".." for part in self.target.path.split("/"))):
            raise ValueError("target path is invalid")
    @property
    def uri(self):
        return urlunsplit(("rtsp", f"{self.target.ipv4}:{self.target.port}", self.target.path, "", ""))
    def __reduce_ex__(self, protocol):
        raise TypeError("RTSP request cannot be serialized")

@dataclass(frozen=True, slots=True)
class RtspDiagnosticResult:
    stages: tuple[StageResult, ...]
    category: ProbeResultCode
    observed_at: datetime
    duration_seconds: float
    error_code: str | None = None
    codec: str | None = None
    def __post_init__(self):
        stages = tuple(self.stages)
        if tuple(s.stage for s in stages) != tuple(RtspStage):
            raise ValueError("diagnostic must contain ordered A/B/C/D stages")
        if not isinstance(self.category, ProbeResultCode): raise TypeError("category must be ProbeResultCode")
        if self.observed_at.tzinfo is None or self.observed_at.utcoffset() is None:
            raise ValueError("observed_at must be timezone-aware")
        object.__setattr__(self, "observed_at", self.observed_at.astimezone(timezone.utc))
        if isinstance(self.duration_seconds, bool) or not isinstance(self.duration_seconds, Real) or not math.isfinite(float(self.duration_seconds)) or self.duration_seconds < 0:
            raise ValueError("duration must be finite and non-negative")
        object.__setattr__(self, "duration_seconds", float(self.duration_seconds))
        if self.error_code is not None and not _CODE.fullmatch(self.error_code): raise ValueError("error code is not safe")
        if self.codec is not None and not re.fullmatch(r"[A-Za-z0-9_.+-]{1,32}", self.codec): raise ValueError("codec identifier is not safe")
        if self.category is ProbeResultCode.SUCCESS and any(s.status is not StageStatus.PASS for s in stages):
            raise ValueError("SUCCESS requires A, B, C and D")
    @property
    def is_success(self): return self.category is ProbeResultCode.SUCCESS

class RtspAdapter(Protocol):
    def probe(self, request: RtspConnectionRequest) -> RtspDiagnosticResult: ...
    def describe(self, request: RtspConnectionRequest) -> RtspSession: ...
    def receive_one_frame(self, session: RtspSession) -> bool: ...
    def cancel(self, target: RtspConnectionRequest | RtspSession) -> None: ...

def make_result(statuses, category, started, *, error_code=None, codec=None, monotonic, now):
    stages = tuple(StageResult(stage, status, error_code if status is StageStatus.FAIL else None)
                   for stage, status in zip(RtspStage, statuses, strict=True))
    return RtspDiagnosticResult(stages, category, now().astimezone(timezone.utc),
                                max(0.0, monotonic() - started), error_code, codec)
