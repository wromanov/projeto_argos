from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import QueryDict
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.dateparse import parse_date

from .auditoria import CAMPOS_ATIVIDADE_AUDITAVEIS, CAMPOS_CAMERA_AUDITAVEIS, calcular_alteracoes, registrar_evento, valores_iniciais
from .forms import (
    AlterarSituacaoCameraForm, AtividadeCameraForm, CameraCriacaoForm,
    CameraEdicaoForm, DesativarCameraForm, ReativarCameraForm, SubstituirCameraForm,
)
from .governanca import (
    ErroGovernancaCamera, alterar_situacao_camera, desativar_camera,
    q_camera_completa, q_camera_incompleta, reativar_camera, substituir_camera,
)
from .models import AtividadeCamera, Camera, EventoAuditoria, SubstituicaoCamera
from .validadores import normalizar_texto_cadastral

ORDENACOES_PERMITIDAS = {"nome", "-nome", "status", "-status", "ip", "-ip", "atualizado_em", "-atualizado_em"}


def _valores_get_unicos(request, nome, normalizar=False):
    valores = []
    for bruto in request.GET.getlist(nome):
        valor = bruto.strip()
        if not valor:
            continue
        if normalizar:
            valor = normalizar_texto_cadastral(valor)
        if valor and valor not in valores:
            valores.append(valor)
    return valores


def _primeiro_valor(valores):
    return valores[0] if valores else ""


def _adicionar_filtros_ativos(
    destino,
    nome,
    valores,
    grupo,
    rotulos=None,
    ignorar_caixa=False,
):
    rotulos = rotulos or {}

    for valor in valores:
        filtro = {
            "nome": nome,
            "valor": valor,
            "grupo": grupo,
            "rotulo": rotulos.get(valor, valor),
        }

        if ignorar_caixa:
            filtro["ignorar_caixa"] = True

        destino.append(filtro)


def _query_params(**params):
    query = QueryDict(mutable=True)
    for key, values in params.items():
        if values is None:
            continue
        if not isinstance(values, (list, tuple)):
            values = [values]
        for value in values:
            if value != "":
                query.appendlist(key, str(value))
    return query


@permission_required("cameras.view_camera", raise_exception=True)
def lista_cameras(request):
    queryset = Camera.objects.all()
    q = request.GET.get("q", "").strip()

    status_selecionados = [
        valor for valor in _valores_get_unicos(request, "status")
        if valor in {"ONLINE", "OFFLINE", "NAO_VERIFICADO"}
    ]
    situacoes_selecionadas = [
        valor for valor in _valores_get_unicos(request, "situacao_operacional")
        if valor in Camera.SituacaoOperacional.values
    ]
    completudes_selecionadas = [
        valor for valor in _valores_get_unicos(request, "completude")
        if valor in {"COMPLETO", "INCOMPLETO"}
    ]
    terminais_selecionados = _valores_get_unicos(request, "terminal", normalizar=True)
    tipos_selecionados = [
        valor for valor in _valores_get_unicos(request, "tipo")
        if valor in Camera.TipoCamera.values
    ]
    fabricantes_selecionados = _valores_get_unicos(request, "fabricante", normalizar=True)
    farms_selecionadas = _valores_get_unicos(request, "farm", normalizar=True)

    vlans_selecionadas = []
    for valor in _valores_get_unicos(request, "vlan"):
        try:
            vlan = int(valor)
        except (TypeError, ValueError):
            continue
        if 1 <= vlan <= 4094:
            vlan_texto = str(vlan)
            if vlan_texto not in vlans_selecionadas:
                vlans_selecionadas.append(vlan_texto)

    ordenacao = request.GET.get("ordenacao", "nome")

    if q:
        queryset = queryset.filter(
            Q(nome__icontains=q) | Q(patrimonio__icontains=q) | Q(ip__icontains=q)
            | Q(serial__icontains=q) | Q(mac__icontains=q) | Q(fabricante__icontains=q)
            | Q(modelo__icontains=q) | Q(terminal__icontains=q) | Q(pavimento__icontains=q)
            | Q(setor__icontains=q) | Q(ambiente__icontains=q) | Q(farm__icontains=q)
        )

    if status_selecionados:
        filtro_status = Q()
        status_diretos = [v for v in status_selecionados if v in {"ONLINE", "OFFLINE"}]
        if status_diretos:
            filtro_status |= Q(status__in=status_diretos)
        if "NAO_VERIFICADO" in status_selecionados:
            filtro_status |= Q(status__isnull=True) | Q(status="")
        queryset = queryset.filter(filtro_status)

    if situacoes_selecionadas:
        queryset = queryset.filter(situacao_operacional__in=situacoes_selecionadas)

    if completudes_selecionadas:
        filtro_completude = Q()
        if "COMPLETO" in completudes_selecionadas:
            filtro_completude |= q_camera_completa()
        if "INCOMPLETO" in completudes_selecionadas:
            filtro_completude |= q_camera_incompleta()
        queryset = queryset.filter(filtro_completude)

    if terminais_selecionados:
        queryset = queryset.filter(terminal__in=terminais_selecionados)
    if tipos_selecionados:
        queryset = queryset.filter(tipo__in=tipos_selecionados)
    if fabricantes_selecionados:
        queryset = queryset.filter(fabricante__in=fabricantes_selecionados)
    if vlans_selecionadas:
        queryset = queryset.filter(vlan__in=[int(v) for v in vlans_selecionadas])
    if farms_selecionadas:
        queryset = queryset.filter(farm__in=farms_selecionadas)

    if ordenacao not in ORDENACOES_PERMITIDAS:
        ordenacao = "nome"
    queryset = queryset.order_by(ordenacao, "pk")

    paginator = Paginator(queryset, 20)
    page_obj = paginator.get_page(request.GET.get("page"))
    query_params = _query_params(q=q, status=status_selecionados,
        situacao_operacional=situacoes_selecionadas, completude=completudes_selecionadas,
        terminal=terminais_selecionados, tipo=tipos_selecionados,
        fabricante=fabricantes_selecionados, vlan=vlans_selecionadas,
        farm=farms_selecionadas,
        ordenacao=ordenacao if request.GET.get("ordenacao") in ORDENACOES_PERMITIDAS else None)

    filtros_ativos = []

    if q:
        _adicionar_filtros_ativos(
            filtros_ativos,
            "q",
            [q],
            "Pesquisa",
        )

    _adicionar_filtros_ativos(
        filtros_ativos,
        "status",
        status_selecionados,
        "Status técnico",
        {
            "ONLINE": "Online",
            "OFFLINE": "Offline",
            "NAO_VERIFICADO": "Não verificado",
        },
    )
    _adicionar_filtros_ativos(
        filtros_ativos,
        "situacao_operacional",
        situacoes_selecionadas,
        "Situação operacional",
        {
            str(valor): str(rotulo)
            for valor, rotulo in Camera.SituacaoOperacional.choices
        },
    )
    _adicionar_filtros_ativos(
        filtros_ativos,
        "completude",
        completudes_selecionadas,
        "Completude",
        {
            "COMPLETO": "Completo",
            "INCOMPLETO": "Incompleto",
        },
    )
    _adicionar_filtros_ativos(
        filtros_ativos,
        "terminal",
        terminais_selecionados,
        "Terminal",
        ignorar_caixa=True,
    )
    _adicionar_filtros_ativos(
        filtros_ativos,
        "tipo",
        tipos_selecionados,
        "Tipo",
        {
            str(valor): str(rotulo)
            for valor, rotulo in Camera.TipoCamera.choices
        },
    )
    _adicionar_filtros_ativos(
        filtros_ativos,
        "fabricante",
        fabricantes_selecionados,
        "Fabricante",
        ignorar_caixa=True,
    )
    _adicionar_filtros_ativos(
        filtros_ativos,
        "vlan",
        vlans_selecionadas,
        "VLAN",
    )
    _adicionar_filtros_ativos(
        filtros_ativos,
        "farm",
        farms_selecionadas,
        "Farm",
        ignorar_caixa=True,
    )

    return render(request, "cameras/lista.html", {
        "cameras": page_obj, "page_obj": page_obj, "paginator": paginator, "q": q,
        "status_selecionado": _primeiro_valor(status_selecionados),
        "situacao_selecionada": _primeiro_valor(situacoes_selecionadas),
        "completude_selecionada": _primeiro_valor(completudes_selecionadas),
        "terminal_selecionado": _primeiro_valor(terminais_selecionados),
        "tipo_selecionado": _primeiro_valor(tipos_selecionados),
        "fabricante_selecionado": _primeiro_valor(fabricantes_selecionados),
        "vlan_selecionada": _primeiro_valor(vlans_selecionadas),
        "farm_selecionada": _primeiro_valor(farms_selecionadas),
        "status_selecionados": status_selecionados,
        "situacoes_selecionadas": situacoes_selecionadas,
        "completudes_selecionadas": completudes_selecionadas,
        "terminais_selecionados": terminais_selecionados,
        "tipos_selecionados": tipos_selecionados,
        "fabricantes_selecionados": fabricantes_selecionados,
        "vlans_selecionadas": vlans_selecionadas,
        "farms_selecionadas": farms_selecionadas,
        "filtros_ativos": filtros_ativos,
        "status_filtro_opcoes": [
            ("ONLINE", "Online"),
            ("OFFLINE", "Offline"),
            ("NAO_VERIFICADO", "Não verificado"),
        ],
        "completude_filtro_opcoes": [
            ("COMPLETO", "Completo"),
            ("INCOMPLETO", "Incompleto"),
        ],
        "terminais_filtro_opcoes": [
            (valor, valor)
            for valor in Camera.objects.exclude(terminal="")
            .values_list("terminal", flat=True)
            .distinct()
            .order_by("terminal")
        ],
        "fabricantes_filtro_opcoes": [
            (valor, valor)
            for valor in Camera.objects.exclude(fabricante="")
            .values_list("fabricante", flat=True)
            .distinct()
            .order_by("fabricante")
        ],
        "vlans_filtro_opcoes": [
            (str(valor), str(valor))
            for valor in Camera.objects.exclude(vlan__isnull=True)
            .values_list("vlan", flat=True)
            .distinct()
            .order_by("vlan")
        ],
        "farms_filtro_opcoes": [
            (valor, valor)
            for valor in Camera.objects.exclude(farm="")
            .values_list("farm", flat=True)
            .distinct()
            .order_by("farm")
        ],
        "terminais": Camera.objects.exclude(terminal="").values_list("terminal", flat=True).distinct().order_by("terminal"),
        "tipos_camera": Camera.TipoCamera.choices,
        "situacoes_operacionais": Camera.SituacaoOperacional.choices,
        "fabricantes": Camera.objects.exclude(fabricante="").values_list("fabricante", flat=True).distinct().order_by("fabricante"),
        "vlans": Camera.objects.exclude(vlan__isnull=True).values_list("vlan", flat=True).distinct().order_by("vlan"),
        "farms": Camera.objects.exclude(farm="").values_list("farm", flat=True).distinct().order_by("farm"),
        "total_resultados": paginator.count,
        "possui_cameras_cadastradas": Camera.objects.exists(),
        "ordenacao": ordenacao,
        "query_params": query_params,
    })


@permission_required("cameras.add_camera", raise_exception=True)
def criar_camera(request):
    form = CameraCriacaoForm(request.POST or None)
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
    camera = get_object_or_404(Camera, pk=pk); anterior = Camera.objects.get(pk=pk)
    form = CameraEdicaoForm(request.POST or None, instance=camera)
    if request.method == "POST" and form.is_valid():
        camera = form.save(commit=False); alteracoes = calcular_alteracoes(anterior, camera, CAMPOS_CAMERA_AUDITAVEIS)
        if request.user.is_authenticated: camera.atualizado_por = request.user
        camera.save()
        if alteracoes: registrar_evento(codigo="camera.atualizada", resumo="Câmera atualizada", categoria=EventoAuditoria.Categoria.CAMERA, request=request, camera=camera, entidade=camera, alteracoes=alteracoes)
        messages.success(request, "Câmera atualizada com sucesso.")
        return redirect("cameras:detalhe", pk=camera.pk)
    return render(request, "cameras/formulario.html", {"form": form, "camera": camera, "titulo_pagina": "Editar câmera"})


@permission_required("cameras.view_camera", raise_exception=True)
def detalhe_camera(request, pk):
    camera = get_object_or_404(Camera, pk=pk)
    contexto = {"camera": camera, "atividades": camera.atividades.select_related("criado_por", "atualizado_por")[:10]}
    if request.user.has_perm("cameras.consultar_eventos"):
        contexto["eventos_auditoria"] = camera.eventos_auditoria.select_related("usuario")[:10]
    if request.user.has_perm("cameras.consultar_substituicoescamera"):
        contexto["substituicoes"] = SubstituicaoCamera.objects.filter(Q(camera_anterior=camera) | Q(camera_substituta=camera)).select_related("camera_anterior", "camera_substituta")[:10]
    return render(request, "cameras/detalhe.html", contexto)


def _processar_governanca(request, camera, form, operacao, sucesso, template, **kwargs):
    if request.method == "POST" and form.is_valid():
        try:
            resultado = operacao(camera=camera, usuario=request.user, request=request, **form.cleaned_data)
        except ErroGovernancaCamera as erro:
            form.add_error(None, erro)
        else:
            messages.success(request, sucesso)
            alvo = resultado.camera_substituta if isinstance(resultado, SubstituicaoCamera) else resultado
            return redirect("cameras:detalhe", pk=alvo.pk)
    return render(request, template, {"camera": camera, "form": form, **kwargs})


@permission_required("cameras.desativar_camera", raise_exception=True)
def desativar_camera_view(request, pk):
    camera = get_object_or_404(Camera, pk=pk)
    return _processar_governanca(request, camera, DesativarCameraForm(request.POST or None), desativar_camera, "Câmera desativada com sucesso.", "cameras/governanca/desativar.html")


@permission_required("cameras.reativar_camera", raise_exception=True)
def reativar_camera_view(request, pk):
    camera = get_object_or_404(Camera, pk=pk)
    return _processar_governanca(request, camera, ReativarCameraForm(request.POST or None), reativar_camera, "Câmera reativada com sucesso.", "cameras/governanca/reativar.html")


@permission_required("cameras.alterar_situacao_camera", raise_exception=True)
def alterar_situacao_camera_view(request, pk):
    camera = get_object_or_404(Camera, pk=pk)
    form = AlterarSituacaoCameraForm(request.POST or None, camera=camera)
    return _processar_governanca(request, camera, form, alterar_situacao_camera, "Situação operacional atualizada com sucesso.", "cameras/governanca/alterar_situacao.html")


@permission_required("cameras.registrar_substituicao_camera", raise_exception=True)
def substituir_camera_view(request, pk):
    camera = get_object_or_404(Camera, pk=pk)
    form = SubstituirCameraForm(request.POST or None, camera_anterior=camera)
    if request.method == "POST" and form.is_valid():
        try:
            substituicao = substituir_camera(camera_anterior=camera, usuario=request.user, request=request, **form.cleaned_data)
        except ErroGovernancaCamera as erro:
            form.add_error(None, erro)
        else:
            messages.success(request, "Substituição registrada com sucesso.")
            return redirect("cameras:detalhe", pk=substituicao.camera_substituta_id)
    return render(request, "cameras/governanca/substituir.html", {"camera": camera, "form": form})


@permission_required(
    "cameras.consultar_substituicoescamera",
    raise_exception=True,
)
def lista_substituicoes_camera(request, camera_pk):
    camera = get_object_or_404(Camera, pk=camera_pk)

    queryset = (
        SubstituicaoCamera.objects
        .filter(
            Q(camera_anterior=camera)
            | Q(camera_substituta=camera)
        )
        .select_related(
            "camera_anterior",
            "camera_substituta",
            "registrado_por",
        )
        .order_by("-ocorrida_em", "-pk")
    )

    paginator = Paginator(queryset, 20)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(
        request,
        "cameras/substituicoes/lista_camera.html",
        {
            "camera": camera,
            "substituicoes": page_obj,
            "page_obj": page_obj,
            "total_substituicoes": paginator.count,
        },
    )


@permission_required("cameras.consultar_substituicoescamera", raise_exception=True)
def lista_substituicoes(request):
    queryset = SubstituicaoCamera.objects.select_related("camera_anterior", "camera_substituta", "registrado_por")
    q = request.GET.get("q", "").strip(); data_inicial = request.GET.get("data_inicial", ""); data_final = request.GET.get("data_final", ""); periodo_invalido = False
    if q: queryset = queryset.filter(Q(camera_anterior__nome__icontains=q) | Q(camera_anterior__patrimonio__icontains=q) | Q(camera_anterior__serial__icontains=q) | Q(camera_substituta__nome__icontains=q) | Q(camera_substituta__patrimonio__icontains=q) | Q(camera_substituta__serial__icontains=q) | Q(nome_operacional__icontains=q) | Q(nome_anterior_substituta__icontains=q) | Q(motivo__icontains=q))
    inicio = parse_date(data_inicial) if data_inicial else None; fim = parse_date(data_final) if data_final else None
    if (
        (data_inicial and not inicio)
        or (data_final and not fim)
        or (inicio and fim and inicio > fim)
    ):
        periodo_invalido = True
    else:
        if inicio: queryset = queryset.filter(ocorrida_em__date__gte=inicio)
        if fim: queryset = queryset.filter(ocorrida_em__date__lte=fim)
    filtros_ativos = []

    if q:
        _adicionar_filtros_ativos(
            filtros_ativos,
            "q",
            [q],
            "Pesquisa",
        )

    if data_inicial:
        rotulo_data_inicial = (
            inicio.strftime("%d/%m/%Y")
            if inicio
            else data_inicial
        )
        _adicionar_filtros_ativos(
            filtros_ativos,
            "data_inicial",
            [data_inicial],
            "De",
            {
                data_inicial: rotulo_data_inicial,
            },
        )

    if data_final:
        rotulo_data_final = (
            fim.strftime("%d/%m/%Y")
            if fim
            else data_final
        )
        _adicionar_filtros_ativos(
            filtros_ativos,
            "data_final",
            [data_final],
            "Até",
            {
                data_final: rotulo_data_final,
            },
        )

    paginator = Paginator(queryset, 50); page_obj = paginator.get_page(request.GET.get("page"))
    return render(request, "cameras/substituicoes/lista.html", {"substituicoes": page_obj, "page_obj": page_obj, "q": q, "data_inicial": data_inicial, "data_final": data_final, "periodo_invalido": periodo_invalido, "filtros_ativos": filtros_ativos, "query_params": _query_params(q=q, data_inicial=data_inicial, data_final=data_final)})


@permission_required("cameras.consultar_substituicoescamera", raise_exception=True)
def detalhe_substituicao(request, pk):
    substituicao = get_object_or_404(SubstituicaoCamera.objects.select_related("camera_anterior", "camera_substituta", "registrado_por"), pk=pk)
    return render(request, "cameras/substituicoes/detalhe.html", {"substituicao": substituicao})


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
    atividade = get_object_or_404(AtividadeCamera.objects.select_related("camera"), pk=pk); anterior = AtividadeCamera.objects.get(pk=pk)
    camera_original_id = atividade.camera_id; criado_por_original_id = atividade.criado_por_id
    form = AtividadeCameraForm(request.POST or None, instance=atividade)
    if request.method == "POST" and form.is_valid():
        atividade = form.save(commit=False); atividade.camera_id = camera_original_id; atividade.criado_por_id = criado_por_original_id
        alteracoes = calcular_alteracoes(anterior, atividade, CAMPOS_ATIVIDADE_AUDITAVEIS)
        if request.user.is_authenticated: atividade.atualizado_por = request.user
        atividade.save()
        if alteracoes: registrar_evento(codigo="atividade.atualizada", resumo="Atividade atualizada", categoria=EventoAuditoria.Categoria.ATIVIDADE, request=request, camera=atividade.camera, entidade=atividade, alteracoes=alteracoes)
        messages.success(request, "Atividade atualizada com sucesso.")
        return redirect("cameras:detalhe", pk=atividade.camera_id)
    return render(request, "cameras/atividades/formulario.html", {"form": form, "atividade": atividade, "camera": atividade.camera, "titulo_pagina": "Editar atividade", "modo_edicao": True})


def _filtrar_eventos(request, queryset):
    q = request.GET.get("q", "").strip()

    categorias_selecionadas = [
        valor
        for valor in _valores_get_unicos(request, "categoria")
        if valor in EventoAuditoria.Categoria.values
    ]
    origens_selecionadas = [
        valor
        for valor in _valores_get_unicos(request, "origem")
        if valor in EventoAuditoria.Origem.values
    ]

    data_inicial = request.GET.get("data_inicial", "")
    data_final = request.GET.get("data_final", "")
    periodo_invalido = False

    if q:
        queryset = queryset.filter(
            Q(codigo__icontains=q)
            | Q(resumo__icontains=q)
            | Q(usuario_username__icontains=q)
            | Q(usuario_nome__icontains=q)
            | Q(entidade_descricao__icontains=q)
            | Q(camera__nome__icontains=q)
        )

    if categorias_selecionadas:
        queryset = queryset.filter(
            categoria__in=categorias_selecionadas
        )

    if origens_selecionadas:
        queryset = queryset.filter(
            origem__in=origens_selecionadas
        )

    inicio = parse_date(data_inicial) if data_inicial else None
    fim = parse_date(data_final) if data_final else None

    if (
        (data_inicial and not inicio)
        or (data_final and not fim)
        or (inicio and fim and inicio > fim)
    ):
        periodo_invalido = True
    else:
        if inicio:
            queryset = queryset.filter(
                ocorrido_em__date__gte=inicio
            )
        if fim:
            queryset = queryset.filter(
                ocorrido_em__date__lte=fim
            )

    filtros_ativos = []

    if q:
        _adicionar_filtros_ativos(
            filtros_ativos,
            "q",
            [q],
            "Pesquisa",
        )

    _adicionar_filtros_ativos(
        filtros_ativos,
        "categoria",
        categorias_selecionadas,
        "Categoria",
        dict(EventoAuditoria.Categoria.choices),
    )
    _adicionar_filtros_ativos(
        filtros_ativos,
        "origem",
        origens_selecionadas,
        "Origem",
        dict(EventoAuditoria.Origem.choices),
    )

    if data_inicial:
        rotulo_data_inicial = (
            inicio.strftime("%d/%m/%Y")
            if inicio
            else data_inicial
        )
        _adicionar_filtros_ativos(
            filtros_ativos,
            "data_inicial",
            [data_inicial],
            "De",
            {
                data_inicial: rotulo_data_inicial,
            },
        )

    if data_final:
        rotulo_data_final = (
            fim.strftime("%d/%m/%Y")
            if fim
            else data_final
        )
        _adicionar_filtros_ativos(
            filtros_ativos,
            "data_final",
            [data_final],
            "At\u00e9",
            {
                data_final: rotulo_data_final,
            },
        )

    return queryset, {
        "q": q,
        "categoria_selecionada": _primeiro_valor(
            categorias_selecionadas
        ),
        "origem_selecionada": _primeiro_valor(
            origens_selecionadas
        ),
        "categorias_selecionadas": categorias_selecionadas,
        "origens_selecionadas": origens_selecionadas,
        "data_inicial": data_inicial,
        "data_final": data_final,
        "periodo_invalido": periodo_invalido,
        "filtros_ativos": filtros_ativos,
        "query_params": _query_params(q=q, categoria=categorias_selecionadas, origem=origens_selecionadas, data_inicial=data_inicial, data_final=data_final),
    }

@permission_required("cameras.consultar_eventos", raise_exception=True)
def lista_eventos(request):
    queryset, filtros = _filtrar_eventos(request, EventoAuditoria.objects.select_related("camera", "usuario"))
    paginator = Paginator(queryset, 50); page_obj = paginator.get_page(request.GET.get("page"))
    return render(request, "cameras/eventos/lista.html", {**filtros, "eventos": page_obj, "page_obj": page_obj, "paginator": paginator, "total_eventos": paginator.count, "categorias": EventoAuditoria.Categoria.choices, "origens": EventoAuditoria.Origem.choices})


@permission_required("cameras.consultar_eventos", raise_exception=True)
def detalhe_evento(request, pk):
    return render(request, "cameras/eventos/detalhe.html", {"evento": get_object_or_404(EventoAuditoria.objects.select_related("camera", "usuario"), pk=pk)})


@permission_required("cameras.consultar_eventos", raise_exception=True)
def eventos_camera(request, pk):
    camera = get_object_or_404(Camera, pk=pk); queryset, filtros = _filtrar_eventos(request, camera.eventos_auditoria.select_related("usuario"))
    paginator = Paginator(queryset, 50); page_obj = paginator.get_page(request.GET.get("page"))
    return render(request, "cameras/eventos/camera.html", {**filtros, "camera": camera, "eventos": page_obj, "page_obj": page_obj, "paginator": paginator, "total_eventos": paginator.count, "categorias": EventoAuditoria.Categoria.choices, "origens": EventoAuditoria.Origem.choices})
