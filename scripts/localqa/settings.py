"""Settings de QA visual local; deliberadamente inutilizáveis sem o launcher."""

import os
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured


BASE_DIR = Path(__file__).resolve().parents[2]
if os.environ.get("ARGOS_LOCAL_QA_LAUNCHER") != "1":
    raise ImproperlyConfigured(
        "Este settings exige o launcher local INICIAR_ARGOS_QA.cmd."
    )
if Path(os.environ.get("ARGOS_QA_ROOT", "")).resolve() != BASE_DIR:
    raise ImproperlyConfigured("O QA deve ser iniciado a partir deste checkout.")

from config.settings import *  # noqa: E402,F403,F401

DEBUG = True
SECRET_KEY = os.environ.get(
    "ARGOS_QA_SECRET_KEY", ""
)
if len(SECRET_KEY) < 32:
    raise ImproperlyConfigured("A chave efêmera de QA não foi preparada.")
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]
CSRF_TRUSTED_ORIGINS = ["http://127.0.0.1:8765", "http://localhost:8765"]
VISUAL_QA_ENABLED = True
VISUAL_QA_USERNAME = "qa-visual-hom01"
OPERATIONAL_QA_USERNAME = "qa-operacional-hom01"
OPERATIONAL_QA_PASSWORD = os.environ.get("ARGOS_OPERATIONAL_QA_PASSWORD", "")
if len(OPERATIONAL_QA_PASSWORD) < 24:
    raise ImproperlyConfigured("A senha operacional QA não foi preparada.")

QA_DATABASE_PATH = (BASE_DIR / ".local" / "qa" / "argos_visual_qa.sqlite3").resolve()
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": QA_DATABASE_PATH,
        "OPTIONS": {"timeout": 20},
    }
}
MEDIA_ROOT = BASE_DIR / ".local" / "qa" / "media"
QA_LOCAL_ONLY = True
QA_SYNTHETIC_DATA_ONLY = True
QA_EXTERNAL_INTEGRATIONS_ENABLED = False
QA_MONITORING_WORKER_ENABLED = False
QA_MONITORING_SCHEDULER_ENABLED = False
