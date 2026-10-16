"""Configuração Django para homologação com PostgreSQL.

Este módulo parte do perfil seguro de produção, mas mantém os caminhos de
dados da homologação isolados em /dados/argos. Segredos são injetados pelo
ambiente do processo e nunca devem ser gravados neste arquivo.
"""

from pathlib import Path

from .environment import get_env_int, get_required_env
from .settings_production import *  # noqa: F403,F401


DATA_ROOT = Path("/dados/argos")
MEDIA_ROOT = DATA_ROOT / "media"
LOG_ROOT = DATA_ROOT / "logs"
STATIC_ROOT = DATA_ROOT / "static"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": get_required_env("ARGOS_DB_NAME"),
        "USER": get_required_env("ARGOS_DB_USER"),
        "PASSWORD": get_required_env("ARGOS_DB_PASSWORD"),
        "HOST": get_required_env("ARGOS_DB_HOST"),
        "PORT": get_env_int("ARGOS_DB_PORT", 5432, minimum=1, maximum=65535),
        "CONN_MAX_AGE": get_env_int("ARGOS_DB_CONN_MAX_AGE", 60, minimum=0),
        "CONN_HEALTH_CHECKS": True,
    }
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{asctime} {levelname} {name}: {message}",
            "style": "{",
        },
    },
    "handlers": {
        "homologation_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": str(LOG_ROOT / "django.log"),
            "maxBytes": 10 * 1024 * 1024,
            "backupCount": 5,
            "encoding": "utf-8",
            "delay": True,
            "formatter": "verbose",
        },
    },
    "root": {"handlers": ["homologation_file"], "level": "INFO"},
}
