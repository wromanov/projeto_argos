"""Labels de apresentação para estados do monitoramento e diagnóstico."""

from types import MappingProxyType


# OUT_OF_SCOPE é uma projeção de escopo, não um estado técnico persistido.
MONITORING_STATE_LABELS = MappingProxyType({
    "ONLINE": "Online",
    "OFFLINE": "Offline",
    "UNKNOWN": "Desconhecido",
    "OUT_OF_SCOPE": "Não monitorada",
})

# A projeção de saúde é um contrato técnico independente dos estados MON.
# Seus rótulos ficam aqui para que a UI não exponha esses códigos diretamente.
CAMERA_HEALTH_EVIDENCE_LABELS = MappingProxyType({
    "CURRENT": "Atual",
    "UNKNOWN": "Não determinada",
})
CAMERA_HEALTH_FRESHNESS_LABELS = MappingProxyType({
    "FRESH": "Atualizado",
    "STALE": "Desatualizado",
    "UNKNOWN": "Não determinado",
})


def monitoring_state_label(state):
    """Retorna o rótulo visual sem alterar ou normalizar o código técnico."""
    return MONITORING_STATE_LABELS[str(state)]


def camera_health_presentation_labels(evidence_state, freshness):
    """Localiza o resumo A–D sem alterar a projeção técnica."""
    return {
        "evidence_state": CAMERA_HEALTH_EVIDENCE_LABELS[str(evidence_state)],
        "freshness": CAMERA_HEALTH_FRESHNESS_LABELS[str(freshness)],
    }
