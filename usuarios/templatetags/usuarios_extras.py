from django import template
register = template.Library()


@register.filter
def nome_exibicao_usuario(usuario):
    nome = usuario.get_full_name().strip()
    return nome or usuario.get_username()


@register.filter
def iniciais_usuario(usuario):
    nome = usuario.get_full_name().strip()
    if nome:
        partes = nome.split()
        return (partes[0][0] + (partes[-1][0] if len(partes) > 1 else "")).upper()
    alfanumerico = "".join(caractere for caractere in usuario.get_username() if caractere.isalnum())
    return alfanumerico[:2].upper() or "US"
