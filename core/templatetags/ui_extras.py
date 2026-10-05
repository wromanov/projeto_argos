from django import template

register = template.Library()


_UI_V2_EXCLUDED_CAMERA_ROUTES = frozenset(
    {
        "historico_monitoramento",
        "lista_substituicoes",
        "detalhe_substituicao",
        "lista_substituicoes_camera",
        "lista_atividades",
    }
)


@register.simple_tag
def ui_v2_active(request):
    """Indica se a rota atual pertence à superfície visual UI V2."""
    resolver_match = getattr(request, "resolver_match", None)
    if resolver_match is None:
        return False

    return not (
        resolver_match.namespace == "cameras"
        and resolver_match.url_name in _UI_V2_EXCLUDED_CAMERA_ROUTES
    )


@register.simple_tag(takes_context=True)
def querystring(context, **updates):
    """Retorna a query string atual com parâmetros atualizados, sem o '?'."""
    request = getattr(context, "request", None) or context.get("request")
    source = context.get("query_params") if hasattr(context, "get") else None
    query = (source if source is not None else (request.GET if request is not None else {})).copy()
    for key, value in updates.items():
        if value is None:
            query.pop(key, None)
        else:
            query[key] = value
    return query.urlencode()



@register.filter
def rotulo_opcao(valor, opcoes):
    # Exibe o rotulo conhecido e preserva o valor em URLs stale/legadas.
    valor_texto = str(valor)

    for opcao_valor, rotulo in opcoes or ():
        if str(opcao_valor) == valor_texto:
            return rotulo

    return valor


@register.simple_tag(takes_context=True)
def querystring_sem_valor(
    context,
    key,
    value,
    ignorar_caixa=False,
):
    # Remove apenas o valor solicitado, preservando os demais parametros.
    request = getattr(context, "request", None) or context.get("request")
    source = context.get("query_params") if hasattr(context, "get") else None
    if source is not None:
        query = source.copy()
    elif request is not None:
        query = request.GET.copy()
    else:
        return ""

    def comparavel(item):
        item = str(item).strip()
        if ignorar_caixa:
            return item.casefold()
        return item

    valor_removido = comparavel(value)

    restantes = [
        item
        for item in query.getlist(key)
        if comparavel(item) != valor_removido
    ]

    if restantes:
        query.setlist(key, restantes)
    else:
        query.pop(key, None)

    query.pop("page", None)
    return query.urlencode()
