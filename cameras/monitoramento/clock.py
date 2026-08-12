"""Implementação de produção do relógio puro de monitoramento."""

from datetime import datetime, timezone
import time


class SystemClock:
    """Fornece UTC aware e monotônico do processo, sem estado global."""

    def now(self) -> datetime:
        return datetime.now(timezone.utc)

    def monotonic(self) -> float:
        return time.monotonic()
