"""Ports estruturais do monitoramento, sem adapters de produção.

As interfaces permitem que MON-05C conecte persistência e elegibilidade sem
acoplar o scheduler ao ORM. Nenhuma porta aceita segredo, URL arbitrária ou
instância de ``Camera``.
"""

from datetime import datetime
from typing import Iterable, Protocol

from .confirmation import ConfirmationMemory, ConfirmationPolicy, TechnicalDecision
from .contracts import ProbeAdapter, ProbeResult
from .schemas import ScheduleCandidate


class DueCandidatePort(Protocol):
    """Fonte autorizada de candidatos due, limitada ao espaço solicitado."""

    def list_due(self, now: datetime, limit: int) -> Iterable[ScheduleCandidate]:
        ...


class ConfirmationStatePort(Protocol):
    """Porta futura para memória/decisão, sem definir uma implementação ORM."""

    def load(
        self, candidate: ScheduleCandidate, policy: ConfirmationPolicy
    ) -> ConfirmationMemory:
        ...

    def store(
        self,
        candidate: ScheduleCandidate,
        result: ProbeResult,
        memory: ConfirmationMemory,
        decision: TechnicalDecision,
    ) -> None:
        ...


class ConfigGenerationPort(Protocol):
    """Fonte de revalidação da geração no instante da conclusão."""

    def current_generation(self, camera_id: int) -> int:
        ...


class EligibilityPort(Protocol):
    """Fonte de elegibilidade revalidada antes do commit técnico."""

    def is_eligible(self, camera_id: int) -> bool:
        ...


__all__ = [
    "ConfirmationStatePort",
    "ConfigGenerationPort",
    "DueCandidatePort",
    "EligibilityPort",
    "ProbeAdapter",
]
