"""Settings descartáveis para testes funcionais do QA local."""

import atexit
import shutil
import tempfile
from pathlib import Path
from uuid import uuid4

from config.settings import *  # noqa: F403


TEST_PARENT = Path(__file__).resolve().parents[2] / ".local" / "qa" / "test-runs"
TEST_PARENT.mkdir(parents=True, exist_ok=True)
TEST_ROOT = TEST_PARENT / f"argos_hom01_test_{uuid4().hex}"
TEST_ROOT.mkdir()
tempfile.tempdir = str(TEST_ROOT)
atexit.register(shutil.rmtree, TEST_ROOT, ignore_errors=True)

DATABASES["default"]["NAME"] = str(TEST_ROOT / "database.sqlite3")
DATABASES["default"]["TEST"] = {"NAME": str(TEST_ROOT / "database.test.sqlite3")}
MEDIA_ROOT = TEST_ROOT / "media"
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]
DEBUG = True
VISUAL_QA_ENABLED = True
VISUAL_QA_USERNAME = "qa-visual-hom01"
OPERATIONAL_QA_USERNAME = "qa-operacional-hom01"
