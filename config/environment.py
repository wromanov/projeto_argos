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


def get_env_optional_int(name: str, default: int | None = None) -> int | None:
    raw = os.environ.get(name)
    if raw is None:
        return default
    try:
        return int(raw.strip())
    except (TypeError, ValueError):
        raise ImproperlyConfigured(f"A variável {name} deve conter um inteiro válido.") from None


def get_env_float(name: str, default: float) -> float:
    raw = os.environ.get(name)
    try:
        return default if raw is None else float(raw.strip())
    except (TypeError, ValueError):
        raise ImproperlyConfigured(f"A variável {name} deve conter um número válido.") from None


def get_monitoring_config_from_environment():
    """Resolve uma única configuração validada para o scheduler local."""

    # Import local evita que os helpers genéricos de ambiente dependam do app
    # durante o bootstrap comum das settings.
    from cameras.monitoramento.schemas import MonitoringConfig

    defaults = MonitoringConfig()
    try:
        return MonitoringConfig(
            concurrency=get_env_int("ARGOS_MONITORING_CONCURRENCY", defaults.concurrency),
            cycle_interval_seconds=get_env_int("ARGOS_MONITORING_CYCLE_INTERVAL_SECONDS", defaults.cycle_interval_seconds),
            probe_timeout_seconds=get_env_float("ARGOS_MONITORING_PROBE_TIMEOUT_SECONDS", defaults.probe_timeout_seconds),
            connect_timeout_seconds=get_env_float("ARGOS_MONITORING_CONNECT_TIMEOUT_SECONDS", defaults.connect_timeout_seconds),
            queue_bound=get_env_optional_int("ARGOS_MONITORING_QUEUE_BOUND"),
            shutdown_timeout_seconds=get_env_int("ARGOS_MONITORING_SHUTDOWN_TIMEOUT_SECONDS", defaults.shutdown_timeout_seconds),
            jitter_ratio=get_env_float("ARGOS_MONITORING_JITTER_RATIO", defaults.jitter_ratio),
            stale_after_seconds=get_env_optional_int("ARGOS_MONITORING_STALE_AFTER_SECONDS"),
            heartbeat_seconds=get_env_int("ARGOS_MONITORING_HEARTBEAT_SECONDS", defaults.heartbeat_seconds),
            ownership_lease_seconds=get_env_optional_int("ARGOS_MONITORING_OWNERSHIP_LEASE_SECONDS"),
        )
    except (TypeError, ValueError) as exc:
        raise ImproperlyConfigured(f"Configuração de monitoramento inválida: {exc}") from None


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
