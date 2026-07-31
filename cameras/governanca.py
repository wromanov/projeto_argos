from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Q
from django.utils import timezone

from .auditoria import registrar_evento
from .models import Camera, EventoAuditoria, SubstituicaoCamera


class ErroGovernancaCamera(ValidationError):
    pass


CAMPOS_OPERACIONAIS_TRANSFERIVEIS = (
    "nome", "terminal", "pavimento", "setor", "ambiente", "descricao_detalhada",
    "ponto_referencia", "ip", "mascara_subrede", "gateway", "vlan", "farm",
    "retencao_esperada_dias", "codec",
)


def _q_campos_preenchidos(campos):
    condicao = Q()
    campos_texto = {campo.name for campo in Camera._meta.fields if campo.get_internal_type() in {"CharField", "TextField"}}
    for campo in campos:
        condicao &= Q(**{f"{campo}__isnull": False})
        if campo in campos_texto:
            condicao &= ~Q(**{campo: ""})
            condicao &= ~Q(**{f"{campo}__regex": r"^\s*$"})
    return condicao


def q_camera_completa():
    return (
        Q(situacao_operacional=Camera.SituacaoOperacional.PRODUCAO)
        & _q_campos_preenchidos(Camera.CAMPOS_PRODUCAO)
    ) | (
        Q(situacao_operacional=Camera.SituacaoOperacional.ESTOQUE)
        & _q_campos_preenchidos(Camera.CAMPOS_ESTOQUE)
    ) | (
        Q(situacao_operacional=Camera.SituacaoOperacional.DESATIVADA)
        & _q_campos_preenchidos(Camera.CAMPOS_DESATIVADA)
    )


def q_camera_incompleta():
    return ~q_camera_completa()


def _validar_texto(valor, minimo, maximo, nome):
    valor = (valor or "").strip()
    if not minimo <= len(valor) <= maximo:
        raise ErroGovernancaCamera(f"{nome} deve ter entre {minimo} e {maximo} caracteres.")
    return valor


def validar_completude(camera, situacao):
    faltantes = camera.rotulos_campos_incompletos(situacao)
    if faltantes:
        raise ErroGovernancaCamera(f"Complete os seguintes campos antes de continuar: {', '.join(str(item) for item in faltantes)}.")


@transaction.atomic
def desativar_camera(*, camera, motivo, usuario, request=None):
    camera = Camera.objects.select_for_update().get(pk=camera.pk)
    if camera.situacao_operacional == Camera.SituacaoOperacional.DESATIVADA:
        raise ErroGovernancaCamera("A câmera já está desativada.")
    motivo = _validar_texto(motivo, 10, 500, "O motivo")
    anterior = camera.situacao_operacional
    camera.situacao_operacional = Camera.SituacaoOperacional.DESATIVADA
    camera.motivo_desativacao = motivo
    camera.desativada_em = timezone.now()
    camera.desativada_por = usuario if getattr(usuario, "is_authenticated", False) else None
    camera.atualizado_por = camera.desativada_por
    camera.save(update_fields=["situacao_operacional", "motivo_desativacao", "desativada_em", "desativada_por", "atualizado_por", "atualizado_em"])
    registrar_evento(codigo="camera.desativada", resumo=f'Câmera "{camera}" desativada.', categoria=EventoAuditoria.Categoria.CAMERA, request=request, usuario=usuario, camera=camera, entidade=camera, alteracoes={"situacao_operacional": {"anterior": anterior, "novo": "DESATIVADA"}}, metadados={"motivo": motivo})
    return camera


@transaction.atomic
def reativar_camera(*, camera, destino, justificativa, usuario, request=None):
    camera = Camera.objects.select_for_update().get(pk=camera.pk)
    if camera.situacao_operacional != Camera.SituacaoOperacional.DESATIVADA:
        raise ErroGovernancaCamera("Somente câmeras desativadas podem ser reativadas.")
    if destino not in (Camera.SituacaoOperacional.PRODUCAO, Camera.SituacaoOperacional.ESTOQUE):
        raise ErroGovernancaCamera("Destino operacional inválido.")
    justificativa = _validar_texto(justificativa, 10, 500, "A justificativa")
    validar_completude(camera, destino)
    camera.situacao_operacional = destino
    if getattr(usuario, "is_authenticated", False):
        camera.atualizado_por = usuario
    camera.save(update_fields=["situacao_operacional", "atualizado_por", "atualizado_em"])
    registrar_evento(codigo="camera.reativada", resumo=f'Câmera "{camera}" reativada para {camera.get_situacao_operacional_display()}.', categoria=EventoAuditoria.Categoria.CAMERA, request=request, usuario=usuario, camera=camera, entidade=camera, alteracoes={"situacao_operacional": {"anterior": "DESATIVADA", "novo": destino}}, metadados={"justificativa": justificativa})
    return camera


@transaction.atomic
def alterar_situacao_camera(*, camera, destino, justificativa, usuario, request=None):
    camera = Camera.objects.select_for_update().get(pk=camera.pk)
    anterior = camera.situacao_operacional
    if anterior == Camera.SituacaoOperacional.DESATIVADA:
        raise ErroGovernancaCamera("Câmeras desativadas devem ser reativadas.")
    if destino == anterior or {anterior, destino} != {Camera.SituacaoOperacional.PRODUCAO, Camera.SituacaoOperacional.ESTOQUE}:
        raise ErroGovernancaCamera("Transição operacional inválida.")
    justificativa = _validar_texto(justificativa, 10, 500, "A justificativa")
    validar_completude(camera, destino)
    camera.situacao_operacional = destino
    if getattr(usuario, "is_authenticated", False):
        camera.atualizado_por = usuario
    camera.save(update_fields=["situacao_operacional", "atualizado_por", "atualizado_em"])
    codigo = "camera.movida_estoque" if destino == Camera.SituacaoOperacional.ESTOQUE else "camera.colocada_producao"
    resumo = f'Câmera "{camera}" movida para Estoque.' if destino == Camera.SituacaoOperacional.ESTOQUE else f'Câmera "{camera}" colocada em Produção.'
    registrar_evento(codigo=codigo, resumo=resumo, categoria=EventoAuditoria.Categoria.CAMERA, request=request, usuario=usuario, camera=camera, entidade=camera, alteracoes={"situacao_operacional": {"anterior": anterior, "novo": destino}}, metadados={"justificativa": justificativa})
    return camera


@transaction.atomic
def substituir_camera(*, camera_anterior, camera_substituta, motivo, observacoes="", usuario=None, request=None):
    if camera_anterior.pk == camera_substituta.pk:
        raise ErroGovernancaCamera("Selecione uma câmera substituta diferente.")
    ids = sorted((camera_anterior.pk, camera_substituta.pk))
    bloqueadas = {item.pk: item for item in Camera.objects.select_for_update().filter(pk__in=ids).order_by("pk")}
    anterior = bloqueadas[camera_anterior.pk]
    substituta = bloqueadas[camera_substituta.pk]
    if anterior.situacao_operacional != Camera.SituacaoOperacional.PRODUCAO:
        raise ErroGovernancaCamera("A câmera anterior deve estar em Produção.")
    if substituta.situacao_operacional != Camera.SituacaoOperacional.ESTOQUE:
        raise ErroGovernancaCamera("A câmera substituta deve estar em Estoque.")
    validar_completude(substituta, Camera.SituacaoOperacional.ESTOQUE)
    motivo = _validar_texto(motivo, 10, 1000, "O motivo")
    observacoes = (observacoes or "").strip()
    nome_operacional = anterior.nome
    nome_anterior_substituta = substituta.nome
    valores_anteriores = {campo: getattr(substituta, campo) for campo in CAMPOS_OPERACIONAIS_TRANSFERIVEIS}

    anterior.situacao_operacional = Camera.SituacaoOperacional.DESATIVADA
    anterior.motivo_desativacao = motivo
    anterior.desativada_em = timezone.now()
    anterior.desativada_por = usuario if getattr(usuario, "is_authenticated", False) else None
    anterior.atualizado_por = anterior.desativada_por
    anterior.save(update_fields=["situacao_operacional", "motivo_desativacao", "desativada_em", "desativada_por", "atualizado_por", "atualizado_em"])

    for campo in CAMPOS_OPERACIONAIS_TRANSFERIVEIS:
        setattr(substituta, campo, getattr(anterior, campo))
    substituta.situacao_operacional = Camera.SituacaoOperacional.PRODUCAO
    if getattr(usuario, "is_authenticated", False):
        substituta.atualizado_por = usuario
    validar_completude(substituta, Camera.SituacaoOperacional.PRODUCAO)
    substituta.save()

    substituicao = SubstituicaoCamera.objects.create(
        camera_anterior=anterior, camera_substituta=substituta, motivo=motivo,
        observacoes=observacoes, nome_operacional=nome_operacional,
        nome_anterior_substituta=nome_anterior_substituta,
        registrado_por=usuario if getattr(usuario, "is_authenticated", False) else None,
        registrado_por_username=usuario.get_username() if getattr(usuario, "is_authenticated", False) else "",
        registrado_por_nome=usuario.get_full_name().strip() if getattr(usuario, "is_authenticated", False) else "",
    )
    registrar_evento(codigo="camera.substituida", resumo=f'Câmera "{anterior}" substituída fisicamente.', categoria=EventoAuditoria.Categoria.CAMERA, request=request, usuario=usuario, camera=anterior, entidade=substituicao, alteracoes={"situacao_operacional": {"anterior": "PRODUCAO", "novo": "DESATIVADA"}}, metadados={"camera_substituta_id": substituta.pk, "motivo": motivo})
    alteracoes = {"situacao_operacional": {"anterior": "ESTOQUE", "novo": "PRODUCAO"}, "nome": {"anterior": nome_anterior_substituta, "novo": nome_operacional}}
    for campo in CAMPOS_OPERACIONAIS_TRANSFERIVEIS:
        novo = getattr(substituta, campo)
        if valores_anteriores[campo] != novo:
            alteracoes[campo] = {"anterior": valores_anteriores[campo], "novo": novo}
    registrar_evento(codigo="camera.assumiu_posicao", resumo=f'Câmera "{substituta}" assumiu a posição operacional.', categoria=EventoAuditoria.Categoria.CAMERA, request=request, usuario=usuario, camera=substituta, entidade=substituicao, alteracoes=alteracoes, metadados={"camera_anterior_id": anterior.pk, "motivo": motivo})
    return substituicao