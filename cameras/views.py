from django.contrib import messages
from django.contrib.auth.decorators import login_not_required, permission_required
from django.core.exceptions import PermissionDenied, ValidationError
from django.core.paginator import Paginator
from django.db import IntegrityError, transaction
from django.db.models import Q
from django.http import HttpResponse, JsonResponse, QueryDict
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.dateparse import parse_date
from uuid import UUID

from .auditoria import CAMPOS_ATIVIDADE_AUDITAVEIS, CAMPOS_CAMERA_AUDITAVEIS, calcular_alteracoes, registrar_evento, valores_iniciais
from .forms import (
    AlterarSituacaoCameraForm, AtividadeCameraForm, CameraCriacaoForm,
    CameraEdicaoForm, DesativarCameraForm, ReativarCameraForm, SubstituirCameraForm,
)
from .integracao.configuration import invalidate_target_config_generation_if_ip_changed
from .authorization import require_camera_permission
from .governanca import (
    ErroGovernancaCamera, alterar_situacao_camera, desativar_camera,
    q_camera_completa, q_camera_incompleta, reativar_camera, substituir_camera,
)
from .models import AtividadeCamera, Camera, CameraImportPreview, EventoAuditoria, SubstituicaoCamera
from .monitoramento.read_service import MonitoringReadService
from .monitoramento.presentation import (
    MONITORING_STATE_LABELS,
    camera_health_presentation_labels,
    monitoring_state_label,
)
from .imagens.upload_service import aceitar_upload_manual
from .imagens.display_service import DisplayImageReadService
from .imagens.preview_service import (
    CameraImagePreviewService, DisplayImagePreviewService, PreviewState,
    QuickDetailImagePreviewService, QuickDetailPreviewState, CONTENT_TYPE, VARIANTS,
)
from .quick_detail import camera_quick_detail
from .validadores import normalizar_texto_cadastral
from .xlsx_import import ImportFileError, build_template, confirm_preview, preview_xlsx, record_failed_confirmation

ORDENACOES_PERMITIDAS = {"nome", "-nome", "status", "-status", "ip", "-ip", "atualizado_em", "-atualizado_em"}


def _duracao_textual(inicio, fim=None):
    """Representação humana derivada; nunca é persistida."""
    if not inicio:
        return "—"
    segundos = max(0, int(((fim or timezone.now()) - inicio).total_seconds()))
    if segundos < 3600:
        return f"{max(1, segundos // 60)} min"
    if segundos < 86400:
        return f"{segundos // 3600} h"
    return f"{segundos // 86400} dia(s)"


def _monitoramento_ui(projecao):
    """Adapta o contrato MON-07B a texto seguro para os templates."""
    efetivo = str(projecao.effective_state)
    stable = str(projecao.stable_state)
    if efetivo == "OUT_OF_SCOPE":
        contexto = "Configuração incompleta" if str(projecao.scope_reason) == "INCOMPLETE_CONFIGURATION" else "Fora do escopo"
    elif projecao.is_stale:
        contexto = f"Dados desatualizados · último estado {monitoring_state_label(stable)}"
    elif projecao.open_outage and efetivo == "OFFLINE":
        contexto = f"Offline há {_duracao_textual(projecao.open_outage.opened_at)}"
    else:
        contexto = ""
    return {"label": monitoring_state_label(efetivo), "effective_state": efetivo,
            "stable_label": monitoring_state_label(stable),
            "has_confirmed_state": stable in {"ONLINE", "OFFLINE"},
            "freshness": str(projecao.freshness), "is_stale": projecao.is_stale, "em_escopo": projecao.em_escopo,
            "contexto": contexto, "evidence_at": projecao.evidence_at, "state_since": projecao.state_since,
            "scope_reason": str(projecao.scope_reason or ""), "open_outage": projecao.open_outage,
            "outage_duration": _duracao_textual(projecao.open_outage.opened_at) if projecao.open_outage else ""}


def _historico_indisponibilidade_ui(item):
    origem = {"INITIAL_OFFLINE": "Offline inicial", "ONLINE_TO_OFFLINE": "Online para offline"}
    fechamento = {"RECUPERADA": "Recuperada", "SAIU_DO_ESCOPO": "Saiu do escopo"}
    return {"opened_at": item.opened_at, "closed_at": item.closed_at,
            "open_origin": origem.get(item.open_origin, "—"),
            "close_reason": fechamento.get(item.close_reason, "") if item.close_reason else "",
            "duration": _duracao_textual(item.opened_at, item.closed_at)}


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
    monitoring_service = MonitoringReadService()
    page_cameras = tuple(monitoring_service.camera_queryset(page_obj.object_list))
    displays = DisplayImageReadService().display_images(page_cameras, check_storage=False)
    camera_rows = tuple(
        {"camera": camera, "monitoring": _monitoramento_ui(monitoring_service.project(camera)),
         "display": displays[camera.pk]}
        for camera in page_cameras
    )
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
            "ONLINE": monitoring_state_label("ONLINE"),
            "OFFLINE": monitoring_state_label("OFFLINE"),
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
        "cameras": page_obj, "camera_rows": camera_rows, "page_obj": page_obj, "paginator": paginator, "q": q,
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
            ("ONLINE", monitoring_state_label("ONLINE")),
            ("OFFLINE", monitoring_state_label("OFFLINE")),
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
        "monitoring_state_labels": dict(MONITORING_STATE_LABELS),
        "can_import_cameras": request.user.has_perm("cameras.importar_cameras"),
    })


@permission_required("cameras.importar_cameras", raise_exception=True)
def baixar_template_importacao(request):
    response = HttpResponse(
        build_template(),
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response["Content-Disposition"] = 'attachment; filename="argos-template-importacao-cameras-v1.xlsx"'
    return response


@permission_required("cameras.importar_cameras", raise_exception=True)
def importar_cameras(request):
    preview = None
    errors = []
    if request.method == "POST":
        upload = request.FILES.get("arquivo")
        if not upload:
            errors.append("Selecione um arquivo XLSX para validar.")
        else:
            try:
                preview = preview_xlsx(upload, request.user)
            except PermissionError as exc:
                raise PermissionDenied(str(exc)) from exc
            except (ImportFileError, ValueError) as exc:
                errors.append(str(exc))
    return render(request, "cameras/importacao.html", {"preview": preview, "errors": errors})


@permission_required("cameras.importar_cameras", raise_exception=True)
def confirmar_importacao_cameras(request, preview_id):
    if request.method != "POST":
        return HttpResponse(status=405)
    try:
        preview = CameraImportPreview.objects.get(pk=preview_id, usuario=request.user)
    except CameraImportPreview.DoesNotExist as exc:
        raise PermissionDenied("Prévia inexistente ou pertencente a outro usuário.") from exc
    operations = {row.get("operation") for row in preview.plano}
    if "CRIAR" in operations and not request.user.has_perm("cameras.add_camera"):
        raise PermissionDenied
    if "ATUALIZAR" in operations and not request.user.has_perm("cameras.change_camera"):
        raise PermissionDenied
    try:
        result = confirm_preview(preview, request.user, request=request)
    except (TimeoutError, ValueError, IntegrityError) as exc:
        record_failed_confirmation(preview, request.user)
        message = str(exc) if not isinstance(exc, IntegrityError) else "Uma restrição cadastral mudou durante a confirmação; nenhuma linha foi gravada. Valide a planilha novamente."
        messages.error(request, message)
        return redirect("cameras:importar")
    messages.success(request, f"Importação concluída: {result['created']} criadas e {result['updated']} atualizadas.")
    return render(request, "cameras/importacao_resultado.html", {"result": result})


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
@transaction.atomic
def editar_camera(request, pk):
    camera = get_object_or_404(Camera, pk=pk); anterior = Camera.objects.get(pk=pk)
    form = CameraEdicaoForm(request.POST or None, instance=camera)
    for field in form.fields.values():
        field.widget.attrs["form"] = "camera-form"
    if request.method == "POST" and form.is_valid():
        camera = form.save(commit=False); alteracoes = calcular_alteracoes(anterior, camera, CAMPOS_CAMERA_AUDITAVEIS)
        if request.user.is_authenticated: camera.atualizado_por = request.user
        camera.save()
        invalidate_target_config_generation_if_ip_changed(
            camera_id=camera.pk,
            previous_ip=anterior.ip,
            current_ip=camera.ip,
        )
        if alteracoes: registrar_evento(codigo="camera.atualizada", resumo="Câmera atualizada", categoria=EventoAuditoria.Categoria.CAMERA, request=request, camera=camera, entidade=camera, alteracoes=alteracoes)
        messages.success(request, "Câmera atualizada com sucesso.")
        return redirect("cameras:detalhe", pk=camera.pk)
    contexto = {"form": form, "camera": camera, "titulo_pagina": "Editar câmera"}
    if request.user.has_perm("cameras.view_camera_credential"):
        from cameras.integracao.credentials import credential_configuration_status

        contexto["credential_panel_visible"] = True
        contexto["credential_metadata"] = credential_configuration_status(
            actor=request.user,
            camera_id=camera.pk,
        )
    response = render(request, "cameras/formulario.html", contexto)
    response["Cache-Control"] = "no-store, no-cache, must-revalidate, private"
    response["Pragma"] = "no-cache"
    response["Expires"] = "0"
    return response


@permission_required("cameras.view_camera", raise_exception=True)
def detalhe_camera(request, pk):
    service = MonitoringReadService()
    camera = get_object_or_404(service.camera_queryset(Camera.objects.all()), pk=pk)
    monitoring = _monitoramento_ui(service.project(camera))
    include_diagnostic = request.user.has_perm("cameras.view_camera_diagnostic")
    if include_diagnostic:
        require_camera_permission(
            actor=request.user,
            permission_codename="view_camera_diagnostic",
            camera_id=camera.pk,
        )
    camera_health = service.camera_health(camera, include_details=include_diagnostic)
    history = service.history_page(camera.pk, limit=5)
    outage_preview = tuple(_historico_indisponibilidade_ui(item) for item in history.items)
    contexto = {"camera": camera, "monitoring": monitoring, "camera_health": camera_health,
                "camera_health_labels": camera_health_presentation_labels(
                    camera_health.evidence_state, camera_health.freshness
                ),
                "outage_preview": outage_preview,
                "atividades": camera.atividades.select_related("criado_por", "atualizado_por")[:10]}
    if request.user.has_perm("cameras.consultar_eventos"):
        contexto["eventos_auditoria"] = camera.eventos_auditoria.select_related("usuario")[:10]
    if request.user.has_perm("cameras.consultar_substituicoescamera"):
        contexto["substituicoes"] = SubstituicaoCamera.objects.filter(Q(camera_anterior=camera) | Q(camera_substituta=camera)).select_related("camera_anterior", "camera_substituta")[:10]
    return render(request, "cameras/detalhe.html", contexto)


@login_not_required
def quick_detail_camera(request, pk):
    """Metadados privados e limitados; bytes da imagem seguem rota própria."""
    if not request.user.is_authenticated:
        response = JsonResponse({"state": "UNAUTHENTICATED"}, status=401)
    elif not request.user.has_perm("cameras.view_camera"):
        response = JsonResponse({"state": "FORBIDDEN"}, status=403)
    elif request.method != "GET":
        response = JsonResponse({"state": "METHOD_NOT_ALLOWED"}, status=405)
    elif request.GET:
        response = JsonResponse({"state": "INVALID_REQUEST"}, status=400)
    else:
        try:
            payload = camera_quick_detail(pk)
        except Camera.DoesNotExist:
            response = JsonResponse({"state": "NOT_FOUND"}, status=404)
        else:
            response = JsonResponse(payload)
    response["Cache-Control"] = "no-store"
    response["X-Content-Type-Options"] = "nosniff"
    return response


@login_not_required
def preview_ultima_captura(request, pk, variant):
    """Rota fina: somente Camera.pk e variante; autorização antes da busca."""
    return _preview_response(request, pk, variant, CameraImagePreviewService)


def _preview_response(request, pk, variant, service_class):
    """Boundary HTTP comum; a seleção é responsabilidade do serviço recebido."""
    def empty(status, state):
        response = HttpResponse(status=status)
        response["X-Preview-State"] = state
        response["Cache-Control"] = "no-store"
        response["X-Content-Type-Options"] = "nosniff"
        return response

    if not request.user.is_authenticated:
        return empty(401, "UNAUTHENTICATED")
    if not request.user.has_perm("cameras.view_camera"):
        return empty(403, "FORBIDDEN")
    if variant not in VARIANTS or request.GET:
        return empty(400, "INVALID_VARIANT")
    if not Camera.objects.filter(pk=pk).exists():
        return empty(404, "CAMERA_NOT_FOUND")

    result = service_class().deliver(pk, variant)
    if result.state != PreviewState.AVAILABLE:
        status = {PreviewState.NO_CAPTURE_AVAILABLE: 404,
                  PreviewState.UNAVAILABLE: 503, PreviewState.ERROR: 422}[result.state]
        return empty(status, result.state.value)
    response = HttpResponse(result.content, content_type=CONTENT_TYPE)
    response["Content-Disposition"] = 'inline; filename="preview.jpg"'
    response["Cache-Control"] = "no-store"
    response["X-Content-Type-Options"] = "nosniff"
    response["X-Preview-State"] = "AVAILABLE"
    return response


@login_not_required
def preview_exibicao(request, pk, variant):
    """Entrega a seleção atual de DISPLAY_IMAGE com os mesmos limites HTTP."""
    return _preview_response(request, pk, variant, DisplayImagePreviewService)


@login_not_required
def preview_quick_detail(request, pk, immutable_id, variant):
    """Entrega IMG-07 vinculada à câmera, identidade imutável e variante."""
    def empty(status, state):
        response = HttpResponse(status=status)
        response["X-Preview-State"] = state
        response["Cache-Control"] = "no-store"
        response["X-Content-Type-Options"] = "nosniff"
        return response

    if not request.user.is_authenticated:
        return empty(401, "UNAUTHENTICATED")
    if not request.user.has_perm("cameras.view_camera"):
        return empty(403, "FORBIDDEN")
    if request.method != "GET" or variant not in VARIANTS or request.GET:
        return empty(400, "INVALID_VARIANT")
    try:
        selected_id = UUID(immutable_id)
    except (TypeError, ValueError, AttributeError):
        return empty(400, "INVALID_VARIANT")
    if not Camera.objects.filter(pk=pk).exists():
        return empty(404, "NOT_FOUND")

    result = QuickDetailImagePreviewService().deliver(pk, selected_id, variant)
    if result.state != QuickDetailPreviewState.AVAILABLE:
        status, state = {
            QuickDetailPreviewState.NOT_FOUND: (404, "NOT_FOUND"),
            QuickDetailPreviewState.STALE_SELECTION: (409, "STALE_SELECTION"),
            QuickDetailPreviewState.UNAVAILABLE: (503, "UNAVAILABLE"),
            QuickDetailPreviewState.ERROR: (422, "ERROR"),
        }[result.state]
        return empty(status, state)
    response = HttpResponse(result.content, content_type=CONTENT_TYPE)
    response["Content-Disposition"] = 'inline; filename="preview.jpg"'
    response["Cache-Control"] = "no-store"
    response["X-Content-Type-Options"] = "nosniff"
    response["X-Preview-State"] = "AVAILABLE"
    return response


@permission_required("cameras.view_camera", raise_exception=True)
@permission_required("cameras.add_cameraimagerecord", raise_exception=True)
def upload_imagem_camera(request, pk):
    camera = get_object_or_404(Camera, pk=pk)
    if request.method == "POST":
        try:
            aceitar_upload_manual(camera=camera, usuario=request.user,
                                  arquivo=request.FILES.get("imagem"), request=request)
        except ValidationError as exc:
            messages.error(request, " ".join(exc.messages))
        else:
            messages.success(request, "Imagem enviada e registrada como upload manual.")
    return redirect("cameras:detalhe", pk=camera.pk)


@permission_required("cameras.view_camera", raise_exception=True)
def historico_monitoramento(request, pk):
    camera = get_object_or_404(Camera.objects.all(), pk=pk)
    service = MonitoringReadService()
    try:
        requested_page = max(1, int(request.GET.get("page", 1)))
    except (TypeError, ValueError):
        requested_page = 1
    page_size = 20
    first_page = service.history_page(camera.pk, limit=page_size, offset=(requested_page - 1) * page_size)
    paginator = Paginator(range(first_page.total), page_size)
    page_obj = paginator.get_page(requested_page)
    page = first_page if page_obj.number == requested_page else service.history_page(camera.pk, limit=page_size, offset=(page_obj.number - 1) * page_size)
    history_items = tuple(_historico_indisponibilidade_ui(item) for item in page.items)
    return render(request, "cameras/monitoramento/historico.html", {"camera": camera, "history_items": history_items,
        "page_obj": page_obj, "total_indisponibilidades": page.total})


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
