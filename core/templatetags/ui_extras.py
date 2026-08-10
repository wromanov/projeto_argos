from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def querystring(context, **updates):
    """Retorna a query string atual com parâmetros atualizados, sem o '?'."""
    request = getattr(context, "request", None) or context.get("request")
    query = request.GET.copy() if request is not None else {}
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
    if request is None:
        return ""

    query = request.GET.copy()

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
