import os
from django.core.exceptions import ImproperlyConfigured

_TRUE_VALUES = {"1", "true", "yes", "on", "sim"}
_FALSE_VALUES = {"0", "false", "no", "off", "nao", "não"}


def get_env_bool(name: str, default: bool) -> bool:
    value = os.environ.get(name)
    if value is None: return default
    normalized = value.strip().lower()
    if normalized in _TRUE_VALUES: return True
    if normalized in _FALSE_VALUES: return False
    raise ImproperlyConfigured(f"A variável {name} deve conter um valor booleano válido.")


def get_env_int(name: str, default: int, minimum: int | None = None, maximum: int | None = None) -> int:
    raw = os.environ.get(name)
    try: value = default if raw is None else int(raw.strip())
    except (TypeError, ValueError): raise ImproperlyConfigured(f"A variável {name} deve conter um inteiro válido.") from None
    if minimum is not None and value < minimum: raise ImproperlyConfigured(f"A variável {name} está abaixo do mínimo permitido.")
    if maximum is not None and value > maximum: raise ImproperlyConfigured(f"A variável {name} está acima do máximo permitido.")
    return value


def get_env_list(name: str, default: list[str] | None = None) -> list[str]:
    raw = os.environ.get(name)
    if raw is None: return list(default or [])
    return [item.strip() for item in raw.split(",") if item.strip()]


def get_required_env(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value: raise ImproperlyConfigured(f"A variável obrigatória {name} não foi configurada.")
    return value


def get_required_secret(name: str, minimum_length: int = 50) -> str:
    value = get_required_env(name)
    if len(value) < minimum_length or len(set(value)) < 12 or value.startswith("django-insecure-"):
        raise ImproperlyConfigured(f"A variável {name} não atende aos requisitos mínimos de segurança.")
    return value
