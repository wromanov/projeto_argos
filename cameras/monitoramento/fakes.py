"""Relógio e adapter sintéticos para testes puros."""

from collections import deque
from datetime import datetime, timedelta, timezone
import math
from numbers import Real
from typing import Iterable

from .contracts import ProbeRequest, ProbeResult, ProbeResultCode


def _finite_non_negative(value: object, field_name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, Real):
        raise TypeError(f"{field_name} must be a real number")
    normalized = float(value)
    if not math.isfinite(normalized):
        raise ValueError(f"{field_name} must be finite")
    if normalized < 0:
        raise ValueError(f"{field_name} must be non-negative")
    return normalized


class FakeClock:
    """Relógio determinístico que avança sem dormir."""

    __slots__ = ("_current_at", "_monotonic_value")

    def __init__(
        self,
        start_at: datetime | None = None,
        monotonic_start: float = 0.0,
    ) -> None:
        if start_at is None:
            start_at = datetime(2000, 1, 1, tzinfo=timezone.utc)
        if not isinstance(start_at, datetime):
            raise TypeError("start_at must be a datetime")
        if start_at.utcoffset() is None:
            raise ValueError("start_at must be timezone-aware")
        self._current_at = start_at.astimezone(timezone.utc)
        self._monotonic_value = _finite_non_negative(monotonic_start, "monotonic_start")

    @property
    def current_at(self) -> datetime:
        return self._current_at

    @property
    def monotonic_value(self) -> float:
        return self._monotonic_value

    def now(self) -> datetime:
        return self._current_at

    def monotonic(self) -> float:
        return self._monotonic_value

    def advance(self, seconds: float) -> None:
        seconds = _finite_non_negative(seconds, "seconds")
        self._current_at += timedelta(seconds=seconds)
        self._monotonic_value += seconds


class FakeProbe:
    """Adapter assíncrono determinístico que nunca toca rede nem ORM."""

    def __init__(
        self,
        outcomes: Iterable[ProbeResultCode],
        clock: FakeClock,
        latency_seconds: float = 0.0,
    ) -> None:
        self._outcomes = deque(outcomes)
        self._clock = clock
        self._latency_seconds = _finite_non_negative(latency_seconds, "latency_seconds")

    async def probe(self, request: ProbeRequest) -> ProbeResult:
        if not self._outcomes:
            raise AssertionError("FakeProbe outcome queue exhausted")
        outcome = self._outcomes.popleft()
        if not isinstance(outcome, ProbeResultCode):
            raise TypeError("FakeProbe outcomes must be ProbeResultCode values")

        started_monotonic = self._clock.monotonic()
        if self._latency_seconds > request.timeout_seconds:
            elapsed = request.timeout_seconds
            result_code = ProbeResultCode.TIMEOUT
        else:
            elapsed = self._latency_seconds
            result_code = outcome

        self._clock.advance(elapsed)
        duration_seconds = self._clock.monotonic() - started_monotonic
        return ProbeResult(
            code=result_code,
            observed_at=self._clock.now(),
            duration_seconds=duration_seconds,
        )
