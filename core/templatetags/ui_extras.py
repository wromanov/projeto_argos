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



@register.simple_tag(takes_context=True)
def querystring_sem_valor(context, key, value):
    """
    Remove um valor especifico de um parametro GET.

    Preserva os demais valores repetidos e os outros parametros.
    Remove page porque alterar um filtro deve retornar a primeira
    pagina da consulta.
    """
    request = getattr(context, "request", None) or context.get("request")
    if request is None:
        return ""

    query = request.GET.copy()
    valor_removido = str(value)

    restantes = [
        item
        for item in query.getlist(key)
        if item != valor_removido
    ]

    if restantes:
        query.setlist(key, restantes)
    else:
        query.pop(key, None)

    query.pop("page", None)

    return query.urlencode()
