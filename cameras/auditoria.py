import ipaddress
from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import EventoAuditoria

CAMPOS_CAMERA_AUDITAVEIS = (
    "patrimonio", "nome", "fabricante", "modelo", "serial", "mac", "tipo", "ativo",
    "terminal", "pavimento", "setor", "ambiente", "descricao_detalhada",
    "ponto_referencia", "ip", "mascara_subrede", "gateway", "vlan", "farm",
    "retencao_esperada_dias", "codec", "origem_cadastro", "observacoes",
)
CAMPOS_ATIVIDADE_AUDITAVEIS = ("tipo", "titulo", "descricao", "ocorrida_em", "responsavel")
CAMPOS_PERFIL_AUDITAVEIS = ("first_name", "last_name", "email", "telefone", "ramal")
_FRAGMENTOS_SENSIVEIS = (
    "senha", "password", "passwd", "secret", "token", "authorization", "cookie",
    "session", "csrf", "credential", "credencial", "api_key", "access_key", "private_key",
)


def _chave_sensivel(chave):
    chave = str(chave).casefold()
    return any(fragmento in chave for fragmento in _FRAGMENTOS_SENSIVEIS)


def sanitizar_dados(valor):
    if isinstance(valor, dict):
        return {str(chave): "[REDACTED]" if _chave_sensivel(chave) else sanitizar_dados(item) for chave, item in valor.items()}
    if isinstance(valor, (list, tuple)):
        return [sanitizar_dados(item) for item in valor]
    if isinstance(valor, (datetime, date)):
        return valor.isoformat()
    if isinstance(valor, (Decimal, UUID)):
        return str(valor)
    if valor is None or isinstance(valor, (str, int, float, bool)):
        return valor
    return f"<{type(valor).__name__}>"


def obter_ip_requisicao(request):
    if request is None:
        return None
    valor = request.META.get("REMOTE_ADDR")
    try:
        return str(ipaddress.ip_address(valor)) if valor else None
    except ValueError:
        return None


def congelar_usuario(usuario):
    if not usuario or not getattr(usuario, "is_authenticated", False):
        return {"usuario": None, "usuario_username": "", "usuario_nome": "", "usuario_email": ""}
    return {
        "usuario": usuario,
        "usuario_username": usuario.get_username()[:150],
        "usuario_nome": usuario.get_full_name().strip()[:200],
        "usuario_email": (usuario.email or "")[:254],
    }


def descrever_entidade(entidade):
    if entidade is None:
        return {"entidade_tipo": "", "entidade_id": "", "entidade_descricao": ""}
    return {
        "entidade_tipo": entidade._meta.label[:100],
        "entidade_id": str(entidade.pk)[:100],
        "entidade_descricao": str(entidade)[:255],
    }


def calcular_alteracoes(anterior, atual, campos):
    alteracoes = {}
    for campo in campos:
        antes = getattr(anterior, campo, None)
        depois = getattr(atual, campo, None)
        equivalentes_vazios = antes in (None, "") and depois in (None, "")
        if antes != depois and not equivalentes_vazios:
            alteracoes[campo] = {"anterior": sanitizar_dados(antes), "atual": sanitizar_dados(depois)}
    return alteracoes


def valores_iniciais(instancia, campos):
    return {campo: {"anterior": None, "atual": sanitizar_dados(getattr(instancia, campo, None))} for campo in campos}


def registrar_evento(*, codigo, resumo, categoria, request=None, usuario=None, camera=None,
                      entidade=None, alteracoes=None, metadados=None,
                      origem=EventoAuditoria.Origem.WEB, ocorrido_em=None):
    if not codigo or not resumo:
        raise ValidationError("Código e resumo são obrigatórios.")
    if categoria not in EventoAuditoria.Categoria.values:
        raise ValidationError("Categoria de auditoria inválida.")
    if request is not None and usuario is None:
        usuario = request.user
    dados_usuario = congelar_usuario(usuario)
    dados_entidade = descrever_entidade(entidade)
    dados_metadados = dict(metadados or {})
    if request is not None:
        dados_metadados.update({"metodo_http": request.method, "caminho": request.path})
    return EventoAuditoria.objects.create(
        categoria=categoria, codigo=codigo, resumo=resumo, camera=camera,
        alteracoes=sanitizar_dados(alteracoes or {}), metadados=sanitizar_dados(dados_metadados),
        origem=origem, ip_origem=obter_ip_requisicao(request),
        ocorrido_em=ocorrido_em or timezone.now(), **dados_usuario, **dados_entidade,
    )