"""Valida a posse do SQLite QA e prepara migrations, usuário e seed."""

import json
import os
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
QA_DIR = ROOT / ".local" / "qa"
DATABASE = (QA_DIR / "argos_visual_qa.sqlite3").resolve()
MARKER = QA_DIR / ".argos-qa-owner.json"
OWNER_ID = "argos-local-visual-qa-v1"


def fail(message):
    raise SystemExit(f"Preparação QA interrompida: {message}")


def check_marker():
    if DATABASE.exists() and not MARKER.exists():
        fail("o SQLite dedicado já existe sem marcador de propriedade; nenhum dado foi alterado.")
    if MARKER.exists():
        try:
            record = json.loads(MARKER.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            fail(f"o marcador QA não pôde ser validado ({error}).")
        if record != {"owner": OWNER_ID, "database": str(DATABASE)}:
            fail("o marcador QA identifica outro banco ou formato; nenhum dado foi alterado.")
    else:
        QA_DIR.mkdir(parents=True, exist_ok=True)
        try:
            with MARKER.open("x", encoding="utf-8") as handle:
                json.dump({"owner": OWNER_ID, "database": str(DATABASE)}, handle)
                handle.write("\n")
        except FileExistsError:
            check_marker()


def main():
    if os.environ.get("ARGOS_LOCAL_QA_LAUNCHER") != "1":
        fail("execute pelo launcher INICIAR_ARGOS_QA.cmd.")
    if Path(sys.executable).resolve().parent != (ROOT / ".venv" / "Scripts").resolve():
        fail("o Python ativo não é o ambiente .venv deste projeto.")
    check_marker()

    sys.path.insert(0, str(ROOT))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "scripts.localqa.settings")
    import django

    django.setup()
    from django.conf import settings
    from django.core.management import call_command
    from django.core.exceptions import ImproperlyConfigured
    from scripts.localqa.provisioning import (
        OPERATIONAL_QA_PERMISSIONS,
        preflight_operational_qa_user,
        provision_operational_qa_user,
        validate_visual_qa_user,
    )

    if Path(settings.DATABASES["default"]["NAME"]).resolve() != DATABASE:
        raise ImproperlyConfigured("Preparação bloqueada: banco efetivo difere do caminho exclusivo QA.")
    if (
        not settings.DEBUG
        or not settings.QA_LOCAL_ONLY
        or settings.QA_EXTERNAL_INTEGRATIONS_ENABLED
        or settings.QA_MONITORING_WORKER_ENABLED
        or settings.QA_MONITORING_SCHEDULER_ENABLED
    ):
        raise ImproperlyConfigured("Preparação bloqueada: configuração não é exclusivamente QA local.")
    call_command("check", verbosity=0)
    call_command("migrate", interactive=False, verbosity=1)
    visual_user = validate_visual_qa_user()
    preflight_operational_qa_user(settings.OPERATIONAL_QA_USERNAME)

    from scripts.localqa.seed_qa import seed

    count = seed()
    operational_user, created = provision_operational_qa_user(
        settings.OPERATIONAL_QA_PASSWORD, settings.OPERATIONAL_QA_USERNAME
    )
    print(f"Banco QA verificado; seed sintético idempotente: {count} câmeras.")
    print(f"Conta visual preservada e verificada: {visual_user.get_username()}.")
    status = "criada" if created else "reconciliada; senha rotacionada"
    print(f"Conta operacional QA {status}: {operational_user.get_username()}.")
    print(f"Permissões operacionais exatas: {len(OPERATIONAL_QA_PERMISSIONS)}; sem privilégios administrativos.")


if __name__ == "__main__":
    main()
