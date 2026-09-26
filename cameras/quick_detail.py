"""Projeção limitada de metadados para a inspeção contextual de câmera."""

from django.urls import reverse

from .imagens.display_service import DisplayImageReadService, DisplayImageState
from .models import Camera
from .monitoramento.read_service import MonitoringReadService


def camera_quick_detail(camera_id):
    monitoring_service = MonitoringReadService()
    camera = monitoring_service.camera_queryset(Camera.objects.filter(pk=camera_id)).get()
    monitoring = monitoring_service.project(camera)
    display = DisplayImageReadService().display_image(camera.pk)
    location = {field: getattr(camera, field) or None for field in (
        "terminal", "pavimento", "setor", "ambiente", "ponto_referencia"
    )}
    location["breadcrumb"] = " > ".join(filter(None, (
        location["terminal"], location["pavimento"], location["setor"]
    ))) or None
    return {
        "camera": {"id": camera.pk, "nome": camera.nome, "patrimonio": camera.patrimonio,
                   "fabricante": camera.fabricante or None, "modelo": camera.modelo or None,
                   "ip": camera.ip, "tipo": camera.get_tipo_display() if camera.tipo else None},
        "location": location,
        "monitoring": {"state": str(monitoring.effective_state),
                       "stable_state": str(monitoring.stable_state),
                       "freshness": str(monitoring.freshness),
                       "evidence_at": monitoring.evidence_at.isoformat() if monitoring.evidence_at else None,
                       "state_since": monitoring.state_since.isoformat() if monitoring.state_since else None,
                       "scope_reason": str(monitoring.scope_reason) if monitoring.scope_reason else None},
        "image": {"state": str(display.state), "source": str(display.source),
                  "capture_state": str(display.capture_state),
                  "preview_url": reverse("cameras:preview_exibicao", args=[camera.pk, "PANEL"])
                  if display.state == DisplayImageState.AVAILABLE else None},
        "links": {"full_detail_url": reverse("cameras:detalhe", args=[camera.pk])},
    }
