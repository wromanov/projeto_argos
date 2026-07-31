from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.utils import timezone

from .forms import CameraForm
from .models import Camera


ORDENACOES_PERMITIDAS = {
    "nome",
    "-nome",
    "status",
    "-status",
    "ip",
    "-ip",
    "atualizado_em",
    "-atualizado_em",
}


def lista_cameras(request):
    queryset = Camera.objects.all()

    q = request.GET.get("q", "").strip()
    status_selecionado = request.GET.get("status", "")
    ativo_selecionado = request.GET.get("ativo", "")
    terminal_selecionado = request.GET.get("terminal", "")
    tipo_selecionado = request.GET.get("tipo", "")
    fabricante_selecionado = request.GET.get("fabricante", "")
    vlan_selecionada = request.GET.get("vlan", "")
    farm_selecionada = request.GET.get("farm", "")
    ordenacao = request.GET.get("ordenacao", "nome")

    if q:
        queryset = queryset.filter(
            Q(nome__icontains=q)
            | Q(patrimonio__icontains=q)
            | Q(ip__icontains=q)
            | Q(serial__icontains=q)
            | Q(mac__icontains=q)
            | Q(fabricante__icontains=q)
            | Q(modelo__icontains=q)
            | Q(terminal__icontains=q)
            | Q(pavimento__icontains=q)
            | Q(setor__icontains=q)
            | Q(ambiente__icontains=q)
            | Q(farm__icontains=q)
        )

    if status_selecionado == "ONLINE":
        queryset = queryset.filter(status="ONLINE")
    elif status_selecionado == "OFFLINE":
        queryset = queryset.filter(status="OFFLINE")
    elif status_selecionado == "NAO_VERIFICADO":
        queryset = queryset.filter(status__isnull=True)

    if ativo_selecionado == "1":
        queryset = queryset.filter(ativo=True)
    elif ativo_selecionado == "0":
        queryset = queryset.filter(ativo=False)

    if terminal_selecionado:
        queryset = queryset.filter(terminal=terminal_selecionado)

    if tipo_selecionado in Camera.TipoCamera.values:
        queryset = queryset.filter(tipo=tipo_selecionado)

    if fabricante_selecionado:
        queryset = queryset.filter(fabricante=fabricante_selecionado)

    try:
        vlan = int(vlan_selecionada)
    except (TypeError, ValueError):
        vlan = None
    if vlan is not None and 1 <= vlan <= 4094:
        queryset = queryset.filter(vlan=vlan)

    if farm_selecionada:
        queryset = queryset.filter(farm=farm_selecionada)

    if ordenacao not in ORDENACOES_PERMITIDAS:
        ordenacao = "nome"
    queryset = queryset.order_by(ordenacao, "pk")

    total_resultados = queryset.count()
    paginator = Paginator(queryset, 20)
    page_obj = paginator.get_page(request.GET.get("page"))

    parametros_paginacao = request.GET.copy()
    parametros_paginacao.pop("page", None)

    contexto = {
        "cameras": page_obj,
        "page_obj": page_obj,
        "paginator": paginator,
        "q": q,
        "status_selecionado": status_selecionado,
        "ativo_selecionado": ativo_selecionado,
        "terminal_selecionado": terminal_selecionado,
        "tipo_selecionado": tipo_selecionado,
        "fabricante_selecionado": fabricante_selecionado,
        "vlan_selecionada": vlan_selecionada,
        "farm_selecionada": farm_selecionada,
        "terminais": Camera.objects.exclude(terminal="").values_list("terminal", flat=True).distinct().order_by("terminal"),
        "tipos_camera": Camera.TipoCamera.choices,
        "fabricantes": Camera.objects.exclude(fabricante="").values_list("fabricante", flat=True).distinct().order_by("fabricante"),
        "vlans": Camera.objects.values_list("vlan", flat=True).distinct().order_by("vlan"),
        "farms": Camera.objects.exclude(farm="").values_list("farm", flat=True).distinct().order_by("farm"),
        "total_resultados": total_resultados,
        "possui_cameras_cadastradas": Camera.objects.exists(),
        "ordenacao": ordenacao,
        "query_string": parametros_paginacao.urlencode(),
    }

    return render(request, "cameras/lista.html", contexto)


def criar_camera(request):
    if request.method == "POST":
        form = CameraForm(request.POST)
        if form.is_valid():
            camera = form.save(commit=False)
            if request.user.is_authenticated:
                camera.criado_por = request.user
                camera.atualizado_por = request.user
            camera.save()
            messages.success(request, "Câmera cadastrada com sucesso.")
            return redirect("cameras:detalhe", pk=camera.pk)
    else:
        form = CameraForm()

    contexto = {"form": form, "titulo_pagina": "Nova câmera"}
    return render(request, "cameras/formulario.html", contexto)


def editar_camera(request, pk):
    camera = get_object_or_404(Camera, pk=pk)

    if request.method == "POST":
        form = CameraForm(request.POST, instance=camera)
        if form.is_valid():
            camera = form.save(commit=False)
            if request.user.is_authenticated:
                camera.atualizado_por = request.user
            camera.save()
            messages.success(request, "Câmera atualizada com sucesso.")
            return redirect("cameras:detalhe", pk=camera.pk)
    else:
        form = CameraForm(instance=camera)

    contexto = {"form": form, "camera": camera, "titulo_pagina": "Editar câmera"}
    return render(request, "cameras/formulario.html", contexto)


@require_POST
def alternar_atividade_camera(request, pk):
    camera = get_object_or_404(Camera, pk=pk)
    camera.ativo = not camera.ativo

    campos_atualizados = ["ativo", "atualizado_em"]
    if request.user.is_authenticated:
        camera.atualizado_por = request.user
        campos_atualizados.append("atualizado_por")

    camera.save(update_fields=campos_atualizados)

    if camera.ativo:
        messages.success(request, "Câmera reativada com sucesso.")
    else:
        messages.success(request, "Câmera inativada com sucesso.")

    return redirect("cameras:detalhe", pk=camera.pk)


def detalhe_camera(request, pk):
    camera = get_object_or_404(Camera, pk=pk)

    contexto = {
        "camera": camera,
    }

    return render(
        request,
        "cameras/detalhe.html",
        contexto,
    )
