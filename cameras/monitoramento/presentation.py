"""Labels de apresentação para estados do monitoramento e diagnóstico."""

from types import MappingProxyType


# OUT_OF_SCOPE é uma projeção de escopo, não um estado técnico persistido.
MONITORING_STATE_LABELS = MappingProxyType({
    "ONLINE": "Online",
    "OFFLINE": "Offline",
    "UNKNOWN": "Desconhecido",
    "OUT_OF_SCOPE": "Não monitorada",
})
