"""Insere um conjunto idempotente de câmeras totalmente fictícias."""

from pathlib import Path

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.exceptions import ValidationError
from django.db import transaction

from cameras.models import Camera


SEED_MARKER = "[ARGOS LOCAL QA — FICTÍCIO]"
CAMERAS = (
    {
        "patrimonio": "ARGOS-QA-001",
        "nome": "QA — Terminal Aurora — Entrada",
        "fabricante": "DAHUA (FICTÍCIO)",
        "modelo": "IPC-QA-BULLET",
        "tipo": Camera.TipoCamera.BULLET,
        "situacao_operacional": Camera.SituacaoOperacional.PRODUCAO,
        "terminal": "T1",
        "pavimento": "Térreo",
        "setor": "Entrada norte",
        "ambiente": "Área de teste",
        "farm": "ESTACIONAMENTO",
        "ip": "192.0.2.10",
        "mascara_subrede": "255.255.255.0",
        "gateway": "192.0.2.1",
        "vlan": 110,
        "serial": "ARGOS-QA-SERIAL-001",
        "mac": "02:00:00:00:01:01",
        "retencao_esperada_dias": 30,
        "codec": "H.264",
    },
    {
        "patrimonio": "ARGOS-QA-002",
        "nome": "QA — Terminal Aurora — Plataforma",
        "fabricante": "HIKVISION (FICTÍCIO)",
        "modelo": "DS-QA-DOME",
        "tipo": Camera.TipoCamera.DOME,
        "situacao_operacional": Camera.SituacaoOperacional.PRODUCAO,
        "terminal": "T1",
        "pavimento": "1º pavimento",
        "setor": "Plataforma leste",
        "ambiente": "Área de teste",
        "farm": "STVV",
        "ip": "192.0.2.11",
        "mascara_subrede": "255.255.255.0",
        "gateway": "192.0.2.1",
        "vlan": 111,
        "serial": "ARGOS-QA-SERIAL-002",
        "mac": "02:00:00:00:01:02",
        "retencao_esperada_dias": 90,
        "codec": "H.265",
    },
    {
        "patrimonio": "ARGOS-QA-003",
        "nome": "QA — Terminal Brisa — Pátio",
        "fabricante": "AXIS (FICTÍCIO)",
        "modelo": "M-QA-SPEED-DOME",
        "tipo": Camera.TipoCamera.SPEED_DOME,
        "situacao_operacional": Camera.SituacaoOperacional.ESTOQUE,
        "terminal": "T2",
        "pavimento": "",
        "setor": "",
        "ambiente": "Estoque de teste",
        "farm": "",
        "ip": None,
        "mascara_subrede": None,
        "gateway": None,
        "vlan": None,
        "serial": "ARGOS-QA-SERIAL-003",
        "mac": "02:00:00:00:01:03",
        "retencao_esperada_dias": 180,
        "codec": "H.265",
    },
    {
        "patrimonio": "ARGOS-QA-004",
        "nome": "QA — Terminal Brisa — Cadastro incompleto",
        "fabricante": "GENÉRICO (FICTÍCIO)",
        "modelo": "QA-PENDENTE",
        "tipo": Camera.TipoCamera.FISHEYE,
        "situacao_operacional": Camera.SituacaoOperacional.PRODUCAO,
        "terminal": "T2",
        "pavimento": "",
        "setor": "Aguardando cadastro",
        "ambiente": "Área de teste",
        "farm": "",
        "ip": "192.0.2.13",
        "mascara_subrede": "",
        "gateway": "",
        "vlan": None,
        "serial": "ARGOS-QA-SERIAL-004",
        "mac": "02:00:00:00:01:04",
        "retencao_esperada_dias": None,
        "codec": "",
    },
    {
        "patrimonio": "ARGOS-QA-005",
        "nome": "QA — Terminal Aurora — Desativada",
        "fabricante": "FICTÍCIO",
        "modelo": "QA-RETIRADA",
        "tipo": Camera.TipoCamera.BULLET,
        "situacao_operacional": Camera.SituacaoOperacional.DESATIVADA,
        "terminal": "T1",
        "pavimento": "Térreo",
        "setor": "Depósito de teste",
        "ambiente": "Área de teste",
        "farm": "COANA",
        "ip": "192.0.2.14",
        "mascara_subrede": "255.255.255.0",
        "gateway": "192.0.2.1",
        "vlan": 113,
        "serial": "ARGOS-QA-SERIAL-005",
        "mac": "02:00:00:00:01:05",
        "retencao_esperada_dias": 15,
        "codec": "H.264",
    },
)


def _assert_qa_database():
    expected = (settings.BASE_DIR / ".local" / "qa" / "argos_visual_qa.sqlite3").resolve()
    actual = Path(settings.DATABASES["default"]["NAME"]).resolve()
    marker = expected.parent / ".argos-qa-owner.json"
    if not getattr(settings, "QA_LOCAL_ONLY", False) or actual != expected:
        raise ImproperlyConfigured("Seed bloqueado: settings não apontam para o SQLite QA dedicado.")
    if not marker.is_file():
        raise ImproperlyConfigured("Seed bloqueado: marcador de propriedade do QA ausente.")


def seed():
    _assert_qa_database()
    fields = {field.name for field in Camera._meta.fields}
    with transaction.atomic():
        for data in CAMERAS:
            values = {**data, "observacoes": f"{SEED_MARKER} Registro sintético para inspeção local; sem monitoramento real."}
            camera = Camera.objects.filter(patrimonio=data["patrimonio"]).first()
            if camera and not camera.observacoes.startswith(SEED_MARKER):
                raise ImproperlyConfigured(
                    f"Seed bloqueado: patrimônio {data['patrimonio']} pertence a um registro não identificado como QA."
                )
            if camera is not None:
                # Existing QA records may have been edited for review; preserve them.
                continue
            camera = Camera()
            for name, value in values.items():
                if name not in fields:
                    raise ImproperlyConfigured(f"Campo do seed incompatível com o model atual: {name}.")
                setattr(camera, name, value)
            try:
                camera.full_clean()
            except ValidationError as error:
                raise ImproperlyConfigured(
                    f"Dados sintéticos não passaram pelas validações do model ({data['patrimonio']}): {error}"
                ) from error
            camera.save()
    return len(CAMERAS)
