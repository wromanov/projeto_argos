from django.contrib.auth.decorators import permission_required
from django.db.models import Q
from django.shortcuts import render
from cameras.models import AtividadeCamera, Camera


def inicio(request):
    pode_inventario = request.user.has_perm("cameras.view_camera")
    nome = request.user.get_full_name() or request.user.get_username()
    return render(request, "core/inicio.html", {"nome_exibicao": nome, "quantidade_modulos": 2 if pode_inventario else 0, "pode_inventario": pode_inventario})


@permission_required("cameras.view_camera", raise_exception=True)
def dashboard(request):
    cameras = Camera.objects.all()
    contexto = {"total_cameras": cameras.count(), "cameras_ativas": cameras.filter(ativo=True).count(), "cameras_inativas": cameras.filter(ativo=False).count(), "cameras_online": cameras.filter(status=Camera.StatusCamera.ONLINE).count(), "cameras_offline": cameras.filter(status=Camera.StatusCamera.OFFLINE).count(), "cameras_nao_verificadas": cameras.filter(Q(status__isnull=True) | Q(status="")).count(), "total_atividades": AtividadeCamera.objects.count(), "atividades_recentes": AtividadeCamera.objects.select_related("camera", "criado_por")[:5], "cameras_recentes": cameras.select_related("atualizado_por").order_by("-atualizado_em")[:5]}
    return render(request, "core/dashboard.html", contexto)
