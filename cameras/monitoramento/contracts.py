"""Contratos pequenos e independentes para probes técnicos.

Este módulo não escolhe destino, não faz preflight de rede e não contém
qualquer integração com Django, ORM ou credenciais.
"""

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import StrEnum
import math
from numbers import Real
import re
from typing import Protocol
from urllib.parse import urlsplit
from ipaddress import IPv4Address


class ProbeResultCode(StrEnum):
    """Categorias técnicas estáveis de uma tentativa de probe."""

    SUCCESS = "SUCCESS"
    TIMEOUT = "TIMEOUT"
    CONNECTION_REFUSED = "CONNECTION_REFUSED"
    AUTH_FAILURE = "AUTH_FAILURE"
    TLS_ERROR = "TLS_ERROR"
    PROTOCOL_ERROR = "PROTOCOL_ERROR"
    CONFIG_ERROR = "CONFIG_ERROR"
    TARGET_BLOCKED = "TARGET_BLOCKED"
    CANCELLED = "CANCELLED"
    INCONCLUSIVE = "INCONCLUSIVE"


class Clock(Protocol):
    """Relógio civil UTC e relógio monotônico injetáveis."""

    def now(self) -> datetime:
        ...

    def monotonic(self) -> float:
        ...


class ProbeAdapter(Protocol):
    """Fronteira estrutural assíncrona de um adapter de probe."""

    async def probe(self, request: "ProbeRequest") -> "ProbeResult":
        ...


def _finite_real(value: object, field_name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, Real):
        raise TypeError(f"{field_name} must be a real number")
    normalized = float(value)
    if not math.isfinite(normalized):
        raise ValueError(f"{field_name} must be finite")
    return normalized


def _utc_datetime(value: object, field_name: str) -> datetime:
    if not isinstance(value, datetime):
        raise TypeError(f"{field_name} must be a datetime")
    if value.utcoffset() is None:
        raise ValueError(f"{field_name} must be timezone-aware")
    return value.astimezone(timezone.utc)


_SAFE_ERROR_CODE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,63}$")


def _safe_error_code(value: object) -> str:
    if not isinstance(value, str):
        raise TypeError("error_code must be a string")
    if not _SAFE_ERROR_CODE.fullmatch(value):
        raise ValueError("error_code must be a short machine-safe code")
    parsed = urlsplit(value)
    if parsed.scheme or parsed.netloc or "://" in value:
        raise ValueError("error_code must not contain a URL")
    return value


def _technical_endpoint(value: object) -> str:
    if not isinstance(value, str):
        raise TypeError("endpoint must be a string or None")
    if "\r" in value or "\n" in value:
        raise ValueError("endpoint must not contain line breaks")
    if value.startswith("//"):
        raise ValueError("endpoint must not be a network-path reference")
    parsed = urlsplit(value)
    if parsed.scheme or parsed.netloc or parsed.username or parsed.password:
        raise ValueError("endpoint must be a relative technical path")
    return value


@dataclass(frozen=True, slots=True)
class ProbeRequest:
    """Destino técnico já resolvido e orçamento de uma tentativa."""

    camera_id: int
    address: IPv4Address
    port: int
    adapter_key: str
    timeout_seconds: float
    endpoint: str | None = None

    def __post_init__(self) -> None:
        if isinstance(self.camera_id, bool) or not isinstance(self.camera_id, int):
            raise TypeError("camera_id must be an integer")
        if self.camera_id <= 0:
            raise ValueError("camera_id must be positive")

        if not isinstance(self.address, IPv4Address):
            raise TypeError("address must be an IPv4Address")

        if isinstance(self.port, bool) or not isinstance(self.port, int):
            raise TypeError("port must be an integer")
        if not 1 <= self.port <= 65535:
            raise ValueError("port must be between 1 and 65535")

        if not isinstance(self.adapter_key, str):
            raise TypeError("adapter_key must be a string")
        if not self.adapter_key.strip():
            raise ValueError("adapter_key must not be empty")

        timeout_seconds = _finite_real(self.timeout_seconds, "timeout_seconds")
        if timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be positive")
        object.__setattr__(self, "timeout_seconds", timeout_seconds)

        if self.endpoint is not None:
            _technical_endpoint(self.endpoint)


@dataclass(frozen=True, slots=True)
class ProbeResult:
    """Evidência imutável e normalizada de uma tentativa."""

    code: ProbeResultCode
    observed_at: datetime
    duration_seconds: float
    error_code: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.code, ProbeResultCode):
            raise TypeError("code must be a ProbeResultCode")

        object.__setattr__(
            self,
            "observed_at",
            _utc_datetime(self.observed_at, "observed_at"),
        )

        duration_seconds = _finite_real(self.duration_seconds, "duration_seconds")
        if duration_seconds < 0:
            raise ValueError("duration_seconds must be non-negative")
        object.__setattr__(self, "duration_seconds", duration_seconds)

        if self.error_code is not None:
            object.__setattr__(self, "error_code", _safe_error_code(self.error_code))
        if self.code is ProbeResultCode.SUCCESS and self.error_code is not None:
            raise ValueError("SUCCESS must not carry error_code")

    @property
    def is_success(self) -> bool:
        return self.code is ProbeResultCode.SUCCESS
