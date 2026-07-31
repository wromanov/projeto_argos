import re

from django.core.exceptions import ValidationError


def normalizar_mac(valor):
    if valor is None or not str(valor).strip():
        return None
    compacto = re.sub(r"[:.\-]", "", str(valor).strip())
    if not re.fullmatch(r"[0-9A-Fa-f]{12}", compacto):
        raise ValidationError("Informe um endereço MAC válido.")
    compacto = compacto.upper()
    return ":".join(compacto[indice:indice + 2] for indice in range(0, 12, 2))


def validar_mac(valor):
    normalizar_mac(valor)