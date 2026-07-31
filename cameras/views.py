from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.dateparse import parse_date
from django.views.decorators.http import require_POST

from .auditoria import (
    CAMPOS_ATIVIDADE_AUDITAVEIS, CAMPOS_CAMERA_AUDITAVEIS,
    calcular_alteracoes, registrar_evento, valores_iniciais,
)
from .forms import AtividadeCameraForm, CameraForm
from .models import AtividadeCamera, Camera, EventoAuditoria

ORDENACOES_PERMITIDAS = {"nome", "-nome", "status", "-status", "ip", "-ip", "atualizado_em", "-atualizado_em"}


@permission_required("cameras.view_camera", raise_exception=True)
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
        queryset = queryset.filter(Q(nome__icontains=q) | Q(patrimonio__icontains=q) | Q(ip__icontains=q) | Q(serial__icontains=q) | Q(mac__icontains=q) | Q(fabricante__icontains=q) | Q(modelo__icontains=q) | Q(terminal__icontains=q) | Q(pavimento__icontains=q) | Q(setor__icontains=q) | Q(ambiente__icontains=q) | Q(farm__icontains=q))
    if status_selecionado == "ONLINE": queryset = queryset.filter(status="ONLINE")
    elif status_selecionado == "OFFLINE": queryset = queryset.filter(status="OFFLINE")
    elif status_selecionado == "NAO_VERIFICADO": queryset = queryset.filter(status__isnull=True)
    if ativo_selecionado == "1": queryset = queryset.filter(ativo=True)
    elif ativo_selecionado == "0": queryset = queryset.filter(ativo=False)
    if terminal_selecionado: queryset = queryset.filter(terminal=terminal_selecionado)
    if tipo_selecionado in Camera.TipoCamera.values: queryset = queryset.filter(tipo=tipo_selecionado)
    if fabricante_selecionado: queryset = queryset.filter(fabricante=fabricante_selecionado)
    try: vlan = int(vlan_selecionada)
    except (TypeError, ValueError): vlan = None
    if vlan is not None and 1 <= vlan <= 4094: queryset = queryset.filter(vlan=vlan)
    if farm_selecionada: queryset = queryset.filter(farm=farm_selecionada)
    if ordenacao not in ORDENACOES_PERMITIDAS: ordenacao = "nome"
    queryset = queryset.order_by(ordenacao, "pk")
    total_resultados = queryset.count()
    paginator = Paginator(queryset, 20); page_obj = paginator.get_page(request.GET.get("page"))
    parametros = request.GET.copy(); parametros.pop("page", None)
    return render(request, "cameras/lista.html", {
        "cameras": page_obj, "page_obj": page_obj, "paginator": paginator, "q": q,
        "status_selecionado": status_selecionado, "ativo_selecionado": ativo_selecionado,
        "terminal_selecionado": terminal_selecionado, "tipo_selecionado": tipo_selecionado,
        "fabricante_selecionado": fabricante_selecionado, "vlan_selecionada": vlan_selecionada,
        "farm_selecionada": farm_selecionada,
        "terminais": Camera.objects.exclude(terminal="").values_list("terminal", flat=True).distinct().order_by("terminal"),
        "tipos_camera": Camera.TipoCamera.choices,
        "fabricantes": Camera.objects.exclude(fabricante="").values_list("fabricante", flat=True).distinct().order_by("fabricante"),
        "vlans": Camera.objects.values_list("vlan", flat=True).distinct().order_by("vlan"),
        "farms": Camera.objects.exclude(farm="").values_list("farm", flat=True).distinct().order_by("farm"),
        "total_resultados": total_resultados, "possui_cameras_cadastradas": Camera.objects.exists(),
        "ordenacao": ordenacao, "query_string": parametros.urlencode(),
    })


@permission_required("cameras.add_camera", raise_exception=True)
def criar_camera(request):
    form = CameraForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        camera = form.save(commit=False)
        if request.user.is_authenticated: camera.criado_por = camera.atualizado_por = request.user
        camera.save()
        registrar_evento(codigo="camera.criada", resumo="Câmera criada", categoria=EventoAuditoria.Categoria.CAMERA, request=request, camera=camera, entidade=camera, alteracoes=valores_iniciais(camera, CAMPOS_CAMERA_AUDITAVEIS))
        messages.success(request, "Câmera cadastrada com sucesso.")
        return redirect("cameras:detalhe", pk=camera.pk)
    return render(request, "cameras/formulario.html", {"form": form, "titulo_pagina": "Nova câmera"})


@permission_required("cameras.change_camera", raise_exception=True)
def editar_camera(request, pk):
    camera = get_object_or_404(Camera, pk=pk)
    anterior = Camera.objects.get(pk=pk)
    form = CameraForm(request.POST or None, instance=camera)
    if request.method == "POST" and form.is_valid():
        camera = form.save(commit=False)
        alteracoes = calcular_alteracoes(anterior, camera, CAMPOS_CAMERA_AUDITAVEIS)
        if request.user.is_authenticated: camera.atualizado_por = request.user
        camera.save()
        if alteracoes:
            registrar_evento(codigo="camera.atualizada", resumo="Câmera atualizada", categoria=EventoAuditoria.Categoria.CAMERA, request=request, camera=camera, entidade=camera, alteracoes=alteracoes)
        messages.success(request, "Câmera atualizada com sucesso.")
        return redirect("cameras:detalhe", pk=camera.pk)
    return render(request, "cameras/formulario.html", {"form": form, "camera": camera, "titulo_pagina": "Editar câmera"})


@require_POST
@permission_required("cameras.change_camera", raise_exception=True)
def alternar_atividade_camera(request, pk):
    camera = get_object_or_404(Camera, pk=pk); anterior = camera.ativo; camera.ativo = not camera.ativo
    campos = ["ativo", "atualizado_em"]
    if request.user.is_authenticated: camera.atualizado_por = request.user; campos.append("atualizado_por")
    camera.save(update_fields=campos)
    codigo = "camera.ativada" if camera.ativo else "camera.inativada"
    resumo = "Câmera reativada" if camera.ativo else "Câmera inativada"
    registrar_evento(codigo=codigo, resumo=resumo, categoria=EventoAuditoria.Categoria.CAMERA, request=request, camera=camera, entidade=camera, alteracoes={"ativo": {"anterior": anterior, "atual": camera.ativo}})
    messages.success(request, f"{resumo} com sucesso.")
    return redirect("cameras:detalhe", pk=camera.pk)


@permission_required("cameras.view_camera", raise_exception=True)
def detalhe_camera(request, pk):
    camera = get_object_or_404(Camera, pk=pk)
    contexto = {"camera": camera, "atividades": camera.atividades.select_related("criado_por", "atualizado_por")[:10]}
    if request.user.has_perm("cameras.consultar_eventos"):
        contexto["eventos_auditoria"] = camera.eventos_auditoria.select_related("usuario")[:10]
    return render(request, "cameras/detalhe.html", contexto)


@permission_required("cameras.view_atividadecamera", raise_exception=True)
def lista_atividades_camera(request, camera_pk):
    camera = get_object_or_404(Camera, pk=camera_pk); paginator = Paginator(camera.atividades.select_related("criado_por", "atualizado_por"), 20); page_obj = paginator.get_page(request.GET.get("page"))
    return render(request, "cameras/atividades/lista.html", {"camera": camera, "atividades": page_obj, "page_obj": page_obj, "total_atividades": paginator.count})


@permission_required("cameras.add_atividadecamera", raise_exception=True)
def criar_atividade_camera(request, camera_pk):
    camera = get_object_or_404(Camera, pk=camera_pk)
    form = AtividadeCameraForm(request.POST or None, initial=None if request.method == "POST" else {"ocorrida_em": timezone.localtime().replace(second=0, microsecond=0)})
    if request.method == "POST" and form.is_valid():
        atividade = form.save(commit=False); atividade.camera = camera
        if request.user.is_authenticated: atividade.criado_por = atividade.atualizado_por = request.user
        atividade.save()
        registrar_evento(codigo="atividade.criada", resumo="Atividade criada", categoria=EventoAuditoria.Categoria.ATIVIDADE, request=request, camera=camera, entidade=atividade, alteracoes=valores_iniciais(atividade, CAMPOS_ATIVIDADE_AUDITAVEIS))
        messages.success(request, "Atividade registrada com sucesso.")
        return redirect("cameras:detalhe", pk=camera.pk)
    return render(request, "cameras/atividades/formulario.html", {"form": form, "camera": camera, "titulo_pagina": "Registrar atividade", "modo_edicao": False})


@permission_required("cameras.change_atividadecamera", raise_exception=True)
def editar_atividade_camera(request, pk):
    atividade = get_object_or_404(AtividadeCamera.objects.select_related("camera"), pk=pk)
    anterior = AtividadeCamera.objects.get(pk=pk); camera_original_id = atividade.camera_id; criado_por_original_id = atividade.criado_por_id
    form = AtividadeCameraForm(request.POST or None, instance=atividade)
    if request.method == "POST" and form.is_valid():
        atividade = form.save(commit=False); atividade.camera_id = camera_original_id; atividade.criado_por_id = criado_por_original_id
        alteracoes = calcular_alteracoes(anterior, atividade, CAMPOS_ATIVIDADE_AUDITAVEIS)
        if request.user.is_authenticated: atividade.atualizado_por = request.user
        atividade.save()
        if alteracoes:
            registrar_evento(codigo="atividade.atualizada", resumo="Atividade atualizada", categoria=EventoAuditoria.Categoria.ATIVIDADE, request=request, camera=atividade.camera, entidade=atividade, alteracoes=alteracoes)
        messages.success(request, "Atividade atualizada com sucesso.")
        return redirect("cameras:detalhe", pk=atividade.camera_id)
    return render(request, "cameras/atividades/formulario.html", {"form": form, "atividade": atividade, "camera": atividade.camera, "titulo_pagina": "Editar atividade", "modo_edicao": True})


def _filtrar_eventos(request, queryset):
    q = request.GET.get("q", "").strip(); categoria = request.GET.get("categoria", ""); origem = request.GET.get("origem", "")
    data_inicial = request.GET.get("data_inicial", ""); data_final = request.GET.get("data_final", "")
    periodo_invalido = False
    if q: queryset = queryset.filter(Q(codigo__icontains=q) | Q(resumo__icontains=q) | Q(usuario_username__icontains=q) | Q(usuario_nome__icontains=q) | Q(entidade_descricao__icontains=q) | Q(camera__nome__icontains=q))
    if categoria in EventoAuditoria.Categoria.values: queryset = queryset.filter(categoria=categoria)
    if origem in EventoAuditoria.Origem.values: queryset = queryset.filter(origem=origem)
    inicio = parse_date(data_inicial) if data_inicial else None; fim = parse_date(data_final) if data_final else None
    if (data_inicial and not inicio) or (data_final and not fim) or (inicio and fim and inicio > fim): periodo_invalido = True
    else:
        if inicio: queryset = queryset.filter(ocorrido_em__date__gte=inicio)
        if fim: queryset = queryset.filter(ocorrido_em__date__lte=fim)
    return queryset, {"q": q, "categoria_selecionada": categoria, "origem_selecionada": origem, "data_inicial": data_inicial, "data_final": data_final, "periodo_invalido": periodo_invalido}


@permission_required("cameras.consultar_eventos", raise_exception=True)
def lista_eventos(request):
    queryset, filtros = _filtrar_eventos(request, EventoAuditoria.objects.select_related("camera", "usuario"))
    paginator = Paginator(queryset, 50); page_obj = paginator.get_page(request.GET.get("page")); parametros = request.GET.copy(); parametros.pop("page", None)
    return render(request, "cameras/eventos/lista.html", {**filtros, "eventos": page_obj, "page_obj": page_obj, "paginator": paginator, "total_eventos": paginator.count, "categorias": EventoAuditoria.Categoria.choices, "origens": EventoAuditoria.Origem.choices, "query_string": parametros.urlencode()})


@permission_required("cameras.consultar_eventos", raise_exception=True)
def detalhe_evento(request, pk):
    evento = get_object_or_404(EventoAuditoria.objects.select_related("camera", "usuario"), pk=pk)
    return render(request, "cameras/eventos/detalhe.html", {"evento": evento})


@permission_required("cameras.consultar_eventos", raise_exception=True)
def eventos_camera(request, pk):
    camera = get_object_or_404(Camera, pk=pk); queryset, filtros = _filtrar_eventos(request, camera.eventos_auditoria.select_related("usuario"))
    paginator = Paginator(queryset, 50); page_obj = paginator.get_page(request.GET.get("page")); parametros = request.GET.copy(); parametros.pop("page", None)
    return render(request, "cameras/eventos/camera.html", {**filtros, "camera": camera, "eventos": page_obj, "page_obj": page_obj, "paginator": paginator, "total_eventos": paginator.count, "categorias": EventoAuditoria.Categoria.choices, "origens": EventoAuditoria.Origem.choices, "query_string": parametros.urlencode()})