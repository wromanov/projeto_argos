from django.contrib.auth.decorators import permission_required
from django.db.models import Count, Q
from django.shortcuts import render

from cameras.governanca import q_camera_completa, q_camera_incompleta
from cameras.models import AtividadeCamera, Camera, SubstituicaoCamera
from cameras.monitoramento.read_service import MonitoringReadService
from cameras.monitoramento.presentation import MONITORING_STATE_LABELS


def inicio(request):
    pode_inventario = request.user.has_perm("cameras.view_camera")
    nome = request.user.get_full_name() or request.user.get_username()
    return render(request, "core/inicio.html", {"nome_exibicao": nome, "quantidade_modulos": 2 if pode_inventario else 0, "pode_inventario": pode_inventario, "pode_eventos": request.user.has_perm("cameras.consultar_eventos")})


@permission_required("cameras.view_camera", raise_exception=True)
def dashboard(request):
    cameras = Camera.objects.all()
    monitoring = MonitoringReadService().aggregate(cameras)
    ips_duplicados = cameras.exclude(ip__isnull=True).order_by().values("ip").annotate(total=Count("pk")).filter(total__gt=1)
    cameras_com_ip_duplicado = sum(item["total"] for item in ips_duplicados)
    contexto = {
        "total_cameras": cameras.count(),
        "cameras_producao": cameras.filter(situacao_operacional=Camera.SituacaoOperacional.PRODUCAO).count(),
        "cameras_estoque": cameras.filter(situacao_operacional=Camera.SituacaoOperacional.ESTOQUE).count(),
        "cameras_desativadas": cameras.filter(situacao_operacional=Camera.SituacaoOperacional.DESATIVADA).count(),
        "cameras_completas": cameras.filter(q_camera_completa()).count(),
        "cameras_incompletas": cameras.filter(q_camera_incompleta()).count(),
        "monitoring": monitoring,
        "monitoring_state_labels": dict(MONITORING_STATE_LABELS),
        "cameras_com_ip_duplicado": cameras_com_ip_duplicado,
        "total_substituicoes": SubstituicaoCamera.objects.count(),
        "total_atividades": AtividadeCamera.objects.count(),
        "atividades_recentes": AtividadeCamera.objects.select_related("camera", "criado_por")[:5],
        "cameras_recentes": cameras.select_related("atualizado_por").order_by("-atualizado_em")[:5],
    }
    return render(request, "core/dashboard.html", contexto)
