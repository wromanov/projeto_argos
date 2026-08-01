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
