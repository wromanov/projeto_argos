"""Contratos puros para o monitoramento técnico de câmeras."""

from .contracts import Clock, ProbeAdapter, ProbeRequest, ProbeResult, ProbeResultCode

__all__ = [
    "Clock",
    "ProbeAdapter",
    "ProbeRequest",
    "ProbeResult",
    "ProbeResultCode",
]
