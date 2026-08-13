"""Reducer puro de confirmação de estado técnico.

Este módulo transforma evidência já normalizada em memória canônica e decisão
explicável. Não conhece Django, ORM, relógio, rede, worker ou persistência.
"""

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import StrEnum
import re

from .contracts import ProbeResult, ProbeResultCode


class TechnicalState(StrEnum):
    """Estados técnicos estáveis do monitoramento."""

    UNKNOWN = "UNKNOWN"
    ONLINE = "ONLINE"
    OFFLINE = "OFFLINE"


class TechnicalDecisionAction(StrEnum):
    """Ações de domínio produzidas pelo reducer."""

    NO_CHANGE = "NO_CHANGE"
    CONFIRM_ONLINE = "CONFIRM_ONLINE"
    CONFIRM_OFFLINE = "CONFIRM_OFFLINE"


class ProcessingDisposition(StrEnum):
    """Resultado da validação temporal do probe recebido."""

    ACCEPTED = "ACCEPTED"
    OUT_OF_ORDER = "OUT_OF_ORDER"
    AMBIGUOUS_ORDER = "AMBIGUOUS_ORDER"


class TechnicalDecisionReason(StrEnum):
    """Razões fechadas para explicar o resultado do reducer."""

    POSITIVE_EVIDENCE = "POSITIVE_EVIDENCE"
    NEGATIVE_EVIDENCE = "NEGATIVE_EVIDENCE"
    NEUTRAL_BARRIER = "NEUTRAL_BARRIER"
    CANCELLED_BARRIER = "CANCELLED_BARRIER"
    CONFIRMED_ONLINE = "CONFIRMED_ONLINE"
    CONFIRMED_OFFLINE = "CONFIRMED_OFFLINE"
    OUT_OF_ORDER = "OUT_OF_ORDER"
    AMBIGUOUS_ORDER = "AMBIGUOUS_ORDER"
    STABLE_STATE_REAFFIRMED = "STABLE_STATE_REAFFIRMED"


_SAFE_VERSION = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,63}$")


def _validate_threshold(value: object, field_name: str, minimum: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{field_name} must be an integer")
    if value < minimum:
        raise ValueError(f"{field_name} must be at least {minimum}")
    return value


def _validate_version(value: object, field_name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string")
    if not _SAFE_VERSION.fullmatch(value):
        raise ValueError(f"{field_name} must be a short machine-safe value")
    return value


def _utc_datetime(value: object, field_name: str) -> datetime:
    if not isinstance(value, datetime):
        raise TypeError(f"{field_name} must be a datetime")
    if value.utcoffset() is None:
        raise ValueError(f"{field_name} must be timezone-aware")
    return value.astimezone(timezone.utc)


def _validate_streak(value: object, field_name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{field_name} must be an integer")
    if value < 0:
        raise ValueError(f"{field_name} must be non-negative")
    return value


@dataclass(frozen=True, slots=True)
class ConfirmationPolicy:
    """Thresholds obrigatórios e versão da política de confirmação."""

    failures_to_offline: int
    successes_to_online: int
    version: str

    def __post_init__(self) -> None:
        _validate_threshold(self.failures_to_offline, "failures_to_offline", 2)
        _validate_threshold(self.successes_to_online, "successes_to_online", 1)
        _validate_version(self.version, "version")


@dataclass(frozen=True, slots=True)
class ConfirmationMemory:
    """Memória imutável e canônica da confirmação por alvo."""

    state: TechnicalState
    positive_streak: int
    negative_streak: int
    last_observed_at: datetime | None
    policy_version: str

    def __post_init__(self) -> None:
        if not isinstance(self.state, TechnicalState):
            raise TypeError("state must be a TechnicalState")

        positive_streak = _validate_streak(self.positive_streak, "positive_streak")
        negative_streak = _validate_streak(self.negative_streak, "negative_streak")
        if positive_streak > 0 and negative_streak > 0:
            raise ValueError("positive_streak and negative_streak cannot both be active")
        if self.state is TechnicalState.ONLINE and positive_streak > 0:
            raise ValueError("ONLINE memory cannot carry a positive streak")
        if self.state is TechnicalState.OFFLINE and negative_streak > 0:
            raise ValueError("OFFLINE memory cannot carry a negative streak")

        if self.last_observed_at is not None:
            object.__setattr__(
                self,
                "last_observed_at",
                _utc_datetime(self.last_observed_at, "last_observed_at"),
            )
        _validate_version(self.policy_version, "policy_version")

    @classmethod
    def initial(cls, policy_version: str) -> "ConfirmationMemory":
        """Cria uma memória UNKNOWN sem esconder a versão da política."""

        return cls(
            state=TechnicalState.UNKNOWN,
            positive_streak=0,
            negative_streak=0,
            last_observed_at=None,
            policy_version=policy_version,
        )

    @property
    def is_suspect(self) -> bool:
        """Indica pendência direcional sem persistir SUSPECT como estado."""

        return self.positive_streak > 0 or self.negative_streak > 0


@dataclass(frozen=True, slots=True)
class TechnicalDecision:
    """Resultado explicável de uma redução de evidência."""

    action: TechnicalDecisionAction
    disposition: ProcessingDisposition
    previous_state: TechnicalState
    current_state: TechnicalState
    reason: TechnicalDecisionReason
    observed_code: ProbeResultCode
    positive_streak: int
    negative_streak: int
    observed_at: datetime
    policy_version_reset: bool = False

    def __post_init__(self) -> None:
        if not isinstance(self.action, TechnicalDecisionAction):
            raise TypeError("action must be a TechnicalDecisionAction")
        if not isinstance(self.disposition, ProcessingDisposition):
            raise TypeError("disposition must be a ProcessingDisposition")
        if not isinstance(self.previous_state, TechnicalState):
            raise TypeError("previous_state must be a TechnicalState")
        if not isinstance(self.current_state, TechnicalState):
            raise TypeError("current_state must be a TechnicalState")
        if not isinstance(self.reason, TechnicalDecisionReason):
            raise TypeError("reason must be a TechnicalDecisionReason")
        if not isinstance(self.observed_code, ProbeResultCode):
            raise TypeError("observed_code must be a ProbeResultCode")
        positive_streak = _validate_streak(self.positive_streak, "positive_streak")
        negative_streak = _validate_streak(self.negative_streak, "negative_streak")
        if positive_streak > 0 and negative_streak > 0:
            raise ValueError("decision streaks cannot both be active")
        object.__setattr__(
            self,
            "observed_at",
            _utc_datetime(self.observed_at, "observed_at"),
        )
        if not isinstance(self.policy_version_reset, bool):
            raise TypeError("policy_version_reset must be a bool")

    @property
    def is_suspect(self) -> bool:
        """Indica pendência derivada dos streaks devolvidos."""

        return self.positive_streak > 0 or self.negative_streak > 0


_NEGATIVE_CODES = frozenset(
    {
        ProbeResultCode.TIMEOUT,
        ProbeResultCode.CONNECTION_REFUSED,
    }
)
_NEUTRAL_CODES = frozenset(
    {
        ProbeResultCode.AUTH_FAILURE,
        ProbeResultCode.TLS_ERROR,
        ProbeResultCode.PROTOCOL_ERROR,
        ProbeResultCode.CONFIG_ERROR,
        ProbeResultCode.TARGET_BLOCKED,
        ProbeResultCode.INCONCLUSIVE,
    }
)


def _disposition(
    memory: ConfirmationMemory, result: ProbeResult
) -> ProcessingDisposition:
    if memory.last_observed_at is None:
        return ProcessingDisposition.ACCEPTED
    if result.observed_at > memory.last_observed_at:
        return ProcessingDisposition.ACCEPTED
    if result.observed_at < memory.last_observed_at:
        return ProcessingDisposition.OUT_OF_ORDER
    return ProcessingDisposition.AMBIGUOUS_ORDER


def _decision(
    *,
    action: TechnicalDecisionAction,
    disposition: ProcessingDisposition,
    previous_state: TechnicalState,
    current_state: TechnicalState,
    reason: TechnicalDecisionReason,
    result: ProbeResult,
    positive_streak: int,
    negative_streak: int,
    policy_version_reset: bool = False,
) -> TechnicalDecision:
    return TechnicalDecision(
        action=action,
        disposition=disposition,
        previous_state=previous_state,
        current_state=current_state,
        reason=reason,
        observed_code=result.code,
        positive_streak=positive_streak,
        negative_streak=negative_streak,
        observed_at=result.observed_at,
        policy_version_reset=policy_version_reset,
    )


def _barrier_update(
    memory: ConfirmationMemory,
    result: ProbeResult,
    policy: ConfirmationPolicy,
    disposition: ProcessingDisposition,
    reason: TechnicalDecisionReason,
    policy_version_reset: bool,
) -> tuple[ConfirmationMemory, TechnicalDecision]:
    updated = ConfirmationMemory(
        state=memory.state,
        positive_streak=0,
        negative_streak=0,
        last_observed_at=result.observed_at,
        policy_version=policy.version,
    )
    return updated, _decision(
        action=TechnicalDecisionAction.NO_CHANGE,
        disposition=disposition,
        previous_state=memory.state,
        current_state=updated.state,
        reason=reason,
        result=result,
        positive_streak=0,
        negative_streak=0,
        policy_version_reset=policy_version_reset,
    )


def _positive_update(
    memory: ConfirmationMemory,
    result: ProbeResult,
    policy: ConfirmationPolicy,
    disposition: ProcessingDisposition,
    policy_version_reset: bool,
) -> tuple[ConfirmationMemory, TechnicalDecision]:
    positive_streak = memory.positive_streak + 1
    if positive_streak >= policy.successes_to_online:
        updated = ConfirmationMemory(
            state=TechnicalState.ONLINE,
            positive_streak=0,
            negative_streak=0,
            last_observed_at=result.observed_at,
            policy_version=policy.version,
        )
        return updated, _decision(
            action=TechnicalDecisionAction.CONFIRM_ONLINE,
            disposition=disposition,
            previous_state=memory.state,
            current_state=updated.state,
            reason=TechnicalDecisionReason.CONFIRMED_ONLINE,
            result=result,
            positive_streak=0,
            negative_streak=0,
            policy_version_reset=policy_version_reset,
        )

    updated = ConfirmationMemory(
        state=memory.state,
        positive_streak=positive_streak,
        negative_streak=0,
        last_observed_at=result.observed_at,
        policy_version=policy.version,
    )
    return updated, _decision(
        action=TechnicalDecisionAction.NO_CHANGE,
        disposition=disposition,
        previous_state=memory.state,
        current_state=updated.state,
        reason=TechnicalDecisionReason.POSITIVE_EVIDENCE,
        result=result,
        positive_streak=positive_streak,
        negative_streak=0,
        policy_version_reset=policy_version_reset,
    )


def _negative_update(
    memory: ConfirmationMemory,
    result: ProbeResult,
    policy: ConfirmationPolicy,
    disposition: ProcessingDisposition,
    policy_version_reset: bool,
) -> tuple[ConfirmationMemory, TechnicalDecision]:
    negative_streak = memory.negative_streak + 1
    if negative_streak >= policy.failures_to_offline:
        updated = ConfirmationMemory(
            state=TechnicalState.OFFLINE,
            positive_streak=0,
            negative_streak=0,
            last_observed_at=result.observed_at,
            policy_version=policy.version,
        )
        return updated, _decision(
            action=TechnicalDecisionAction.CONFIRM_OFFLINE,
            disposition=disposition,
            previous_state=memory.state,
            current_state=updated.state,
            reason=TechnicalDecisionReason.CONFIRMED_OFFLINE,
            result=result,
            positive_streak=0,
            negative_streak=0,
            policy_version_reset=policy_version_reset,
        )

    updated = ConfirmationMemory(
        state=memory.state,
        positive_streak=0,
        negative_streak=negative_streak,
        last_observed_at=result.observed_at,
        policy_version=policy.version,
    )
    return updated, _decision(
        action=TechnicalDecisionAction.NO_CHANGE,
        disposition=disposition,
        previous_state=memory.state,
        current_state=updated.state,
        reason=TechnicalDecisionReason.NEGATIVE_EVIDENCE,
        result=result,
        positive_streak=0,
        negative_streak=negative_streak,
        policy_version_reset=policy_version_reset,
    )


def reduce_confirmation(
    memory: ConfirmationMemory,
    result: ProbeResult,
    policy: ConfirmationPolicy,
) -> tuple[ConfirmationMemory, TechnicalDecision]:
    """Reduz uma observação em nova memória canônica e decisão técnica."""

    if not isinstance(memory, ConfirmationMemory):
        raise TypeError("memory must be a ConfirmationMemory")
    if not isinstance(result, ProbeResult):
        raise TypeError("result must be a ProbeResult")
    if not isinstance(policy, ConfirmationPolicy):
        raise TypeError("policy must be a ConfirmationPolicy")

    disposition = _disposition(memory, result)
    if disposition is not ProcessingDisposition.ACCEPTED:
        reason = (
            TechnicalDecisionReason.OUT_OF_ORDER
            if disposition is ProcessingDisposition.OUT_OF_ORDER
            else TechnicalDecisionReason.AMBIGUOUS_ORDER
        )
        return memory, _decision(
            action=TechnicalDecisionAction.NO_CHANGE,
            disposition=disposition,
            previous_state=memory.state,
            current_state=memory.state,
            reason=reason,
            result=result,
            positive_streak=memory.positive_streak,
            negative_streak=memory.negative_streak,
        )

    policy_version_reset = memory.policy_version != policy.version
    if policy_version_reset:
        memory = ConfirmationMemory(
            state=memory.state,
            positive_streak=0,
            negative_streak=0,
            last_observed_at=memory.last_observed_at,
            policy_version=policy.version,
        )

    if result.code is ProbeResultCode.CANCELLED:
        return _barrier_update(
            memory,
            result,
            policy,
            disposition,
            TechnicalDecisionReason.CANCELLED_BARRIER,
            policy_version_reset,
        )

    if result.code in _NEUTRAL_CODES:
        return _barrier_update(
            memory,
            result,
            policy,
            disposition,
            TechnicalDecisionReason.NEUTRAL_BARRIER,
            policy_version_reset,
        )

    if result.code is ProbeResultCode.SUCCESS:
        if memory.state is TechnicalState.ONLINE:
            updated = ConfirmationMemory(
                state=TechnicalState.ONLINE,
                positive_streak=0,
                negative_streak=0,
                last_observed_at=result.observed_at,
                policy_version=policy.version,
            )
            return updated, _decision(
                action=TechnicalDecisionAction.NO_CHANGE,
                disposition=disposition,
                previous_state=memory.state,
                current_state=updated.state,
                reason=TechnicalDecisionReason.STABLE_STATE_REAFFIRMED,
                result=result,
                positive_streak=0,
                negative_streak=0,
                policy_version_reset=policy_version_reset,
            )
        return _positive_update(
            memory,
            result,
            policy,
            disposition,
            policy_version_reset,
        )

    if result.code in _NEGATIVE_CODES:
        if memory.state is TechnicalState.OFFLINE:
            updated = ConfirmationMemory(
                state=TechnicalState.OFFLINE,
                positive_streak=0,
                negative_streak=0,
                last_observed_at=result.observed_at,
                policy_version=policy.version,
            )
            return updated, _decision(
                action=TechnicalDecisionAction.NO_CHANGE,
                disposition=disposition,
                previous_state=memory.state,
                current_state=updated.state,
                reason=TechnicalDecisionReason.STABLE_STATE_REAFFIRMED,
                result=result,
                positive_streak=0,
                negative_streak=0,
                policy_version_reset=policy_version_reset,
            )
        return _negative_update(
            memory,
            result,
            policy,
            disposition,
            policy_version_reset,
        )

    raise ValueError(f"unsupported ProbeResultCode: {result.code!r}")


__all__ = [
    "ConfirmationMemory",
    "ConfirmationPolicy",
    "ProcessingDisposition",
    "TechnicalDecision",
    "TechnicalDecisionAction",
    "TechnicalDecisionReason",
    "TechnicalState",
    "reduce_confirmation",
]
