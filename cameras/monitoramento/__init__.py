"""Contratos puros para o monitoramento técnico de câmeras."""

from .contracts import Clock, ProbeAdapter, ProbeRequest, ProbeResult, ProbeResultCode
from .confirmation import (
    ConfirmationMemory,
    ConfirmationPolicy,
    ProcessingDisposition,
    TechnicalDecision,
    TechnicalDecisionAction,
    TechnicalDecisionReason,
    TechnicalState,
    reduce_confirmation,
)

__all__ = [
    "Clock",
    "ConfirmationMemory",
    "ConfirmationPolicy",
    "ProcessingDisposition",
    "ProbeAdapter",
    "ProbeRequest",
    "ProbeResult",
    "ProbeResultCode",
    "TechnicalDecision",
    "TechnicalDecisionAction",
    "TechnicalDecisionReason",
    "TechnicalState",
    "reduce_confirmation",
]
