from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Q
from django.db.models.functions import Lower

from .validadores import normalizar_mac, normalizar_texto_cadastral, validar_mac


class Camera(models.Model):
    class TipoCamera(models.TextChoices):
        BULLET = "BULLET", "Bullet"
        DOME = "DOME", "Dome"
        SPEED_DOME = "SPEED_DOME", "Speed Dome"
        FISHEYE = "FISHEYE", "Fisheye"

    class StatusCamera(models.TextChoices):
        ONLINE = "ONLINE", "Online"
        OFFLINE = "OFFLINE", "Offline"

    class OrigemCadastro(models.TextChoices):
        MANUAL = "MANUAL", "Manual"
        IMPORTACAO = "IMPORTACAO", "Importação"
        INTEGRACAO = "INTEGRACAO", "Integração"

    class SituacaoOperacional(models.TextChoices):
        PRODUCAO = "PRODUCAO", "Produção"
        ESTOQUE = "ESTOQUE", "Estoque"
        DESATIVADA = "DESATIVADA", "Desativada"

    patrimonio = models.CharField(
        max_length=50,
        unique=True,
        null=True,
        blank=True,
        verbose_name="Patrimônio",
    )
    nome = models.CharField(max_length=150)
    fabricante = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    serial = models.CharField(
        max_length=100,
        unique=True,
        null=True,
        blank=True,
        verbose_name="Número de série",
    )
    mac = models.CharField(max_length=17, null=True, blank=True, default=None, verbose_name="Endereço MAC", validators=[validar_mac])
    situacao_operacional = models.CharField(max_length=20, choices=SituacaoOperacional.choices, default=SituacaoOperacional.PRODUCAO, db_index=True, verbose_name="Situação operacional")
    motivo_desativacao = models.CharField(max_length=500, blank=True, default="", verbose_name="Motivo da última desativação")
    desativada_em = models.DateTimeField(null=True, blank=True, verbose_name="Desativada em")
    desativada_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="cameras_desativadas", verbose_name="Desativada por")
    tipo = models.CharField(
        max_length=20,
        choices=TipoCamera.choices,
        blank=True,
        default="",
        verbose_name="Tipo de câmera",
    )

    terminal = models.CharField(max_length=50, blank=True, default="")
    pavimento = models.CharField(max_length=50, blank=True, default="")
    setor = models.CharField(max_length=100, blank=True, default="")
    ambiente = models.CharField(max_length=100, blank=True, default="")
    descricao_detalhada = models.TextField(
        blank=True,
        default="",
        verbose_name="Descrição detalhada",
    )
    ponto_referencia = models.CharField(
        max_length=200,
        blank=True,
        default="",
        verbose_name="Ponto de referência",
    )

    ip = models.GenericIPAddressField(protocol="IPv4", null=True, blank=True)
    mascara_subrede = models.GenericIPAddressField(protocol="IPv4", null=True, blank=True, verbose_name="Máscara de sub-rede")
    gateway = models.GenericIPAddressField(protocol="IPv4", null=True, blank=True)
    vlan = models.PositiveSmallIntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(4094)],
    )

    farm = models.CharField(max_length=100, blank=True, default="")
    retencao_esperada_dias = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1)],
        verbose_name="Retenção esperada em dias",
    )
    codec = models.CharField(
        max_length=20,
        blank=True,
        default="",
        verbose_name="Codec",
    )

    status = models.CharField(
        max_length=7,
        choices=StatusCamera.choices,
        null=True,
        blank=True,
        verbose_name="Status",
    )
    status_em = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Status desde",
    )
    ultima_verificacao = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Última verificação",
    )

    criado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="cameras_criadas",
        editable=False,
        verbose_name="Criado por",
    )
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    atualizado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="cameras_atualizadas",
        editable=False,
        verbose_name="Atualizado por",
    )
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")
    origem_cadastro = models.CharField(
        max_length=20,
        choices=OrigemCadastro.choices,
        default=OrigemCadastro.MANUAL,
        verbose_name="Origem do cadastro",
    )
    observacoes = models.TextField(
        blank=True,
        default="",
        verbose_name="Observações",
    )

    class Meta:
        ordering = ["nome"]
        verbose_name = "Câmera"
        verbose_name_plural = "Câmeras"
        permissions = (("desativar_camera", "Pode desativar câmera"), ("reativar_camera", "Pode reativar câmera"), ("alterar_situacao_camera", "Pode alterar situação operacional da câmera"), ("registrar_substituicao_camera", "Pode registrar substituição física de câmera"))
        constraints = [
            models.UniqueConstraint(Lower("nome"), condition=~Q(situacao_operacional="DESATIVADA"), name="uniq_camera_nome_ativa_ci"),
            models.UniqueConstraint(Lower("mac"), condition=Q(mac__isnull=False), name="uniq_camera_mac_ci_nao_nulo"),
        ]

    CAMPOS_CAIXA_ALTA = (
        "patrimonio",
        "nome",
        "fabricante",
        "modelo",
        "serial",
        "terminal",
        "pavimento",
        "setor",
        "ambiente",
        "ponto_referencia",
        "farm",
        "codec",
    )

    CAMPOS_PRODUCAO = (
        "nome", "fabricante", "modelo", "serial", "mac", "tipo", "terminal",
        "pavimento", "setor", "ambiente", "ip", "mascara_subrede", "gateway",
        "vlan", "farm", "retencao_esperada_dias", "codec",
    )
    CAMPOS_ESTOQUE = ("nome", "fabricante", "modelo", "serial", "mac", "tipo")
    CAMPOS_DESATIVADA = ("nome",)

    def campos_obrigatorios_situacao(self, situacao=None):
        situacao = situacao or self.situacao_operacional
        return {
            self.SituacaoOperacional.PRODUCAO: self.CAMPOS_PRODUCAO,
            self.SituacaoOperacional.ESTOQUE: self.CAMPOS_ESTOQUE,
            self.SituacaoOperacional.DESATIVADA: self.CAMPOS_DESATIVADA,
        }.get(situacao, ())

    def campos_incompletos(self, situacao=None):
        incompletos = []
        for campo in self.campos_obrigatorios_situacao(situacao):
            valor = getattr(self, campo, None)
            if valor is None or (isinstance(valor, str) and not valor.strip()):
                incompletos.append(campo)
        return incompletos

    def rotulos_campos_incompletos(self, situacao=None):
        return [self._meta.get_field(campo).verbose_name for campo in self.campos_incompletos(situacao)]

    @property
    def cadastro_completo(self):
        return not self.campos_incompletos()

    def save(self, *args, **kwargs):
        update_fields = kwargs.get("update_fields")

        if update_fields is None:
            campos_caixa_alta = self.CAMPOS_CAIXA_ALTA
            normalizar_mac_atual = True
        else:
            update_fields = set(update_fields)

            campos_caixa_alta = tuple(
                campo
                for campo in self.CAMPOS_CAIXA_ALTA
                if campo in update_fields
            )

            normalizar_mac_atual = "mac" in update_fields

        for campo in campos_caixa_alta:
            valor = normalizar_texto_cadastral(
                getattr(self, campo, None)
            )

            if (
                campo in ("patrimonio", "serial")
                and valor == ""
            ):
                valor = None

            setattr(self, campo, valor)

        if normalizar_mac_atual:
            self.mac = normalizar_mac(self.mac)

        return super().save(*args, **kwargs)

    def __str__(self):
        return self.nome


class AtividadeCamera(models.Model):
    class TipoAtividade(models.TextChoices):
        AVARIA = "AVARIA", "Avaria identificada"
        RETIRADA = "RETIRADA", "Retirada do local"
        ENVIO_CONSERTO = "ENVIO_CONSERTO", "Enviada para conserto"
        RETORNO_CONSERTO = "RETORNO_CONSERTO", "Retorno do conserto"
        REINSTALACAO = "REINSTALACAO", "Reinstalação"
        MANUTENCAO = "MANUTENCAO", "Manutenção"
        LIMPEZA = "LIMPEZA", "Limpeza"
        REPOSICIONAMENTO = "REPOSICIONAMENTO", "Reposicionamento"
        SUBSTITUICAO = "SUBSTITUICAO", "Substituição"
        INSPECAO = "INSPECAO", "Inspeção"
        OUTRO = "OUTRO", "Outro"

    camera = models.ForeignKey(
        Camera,
        on_delete=models.PROTECT,
        related_name="atividades",
        verbose_name="Câmera",
    )
    tipo = models.CharField(
        max_length=30,
        choices=TipoAtividade.choices,
        default=TipoAtividade.OUTRO,
        verbose_name="Tipo de atividade",
    )
    titulo = models.CharField(max_length=150, verbose_name="Título")
    descricao = models.TextField(verbose_name="Descrição")
    ocorrida_em = models.DateTimeField(
        default=timezone.now,
        verbose_name="Data e hora da atividade",
    )
    responsavel = models.CharField(
        max_length=150,
        blank=True,
        default="",
        verbose_name="Responsável",
    )
    criado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        editable=False,
        related_name="atividades_camera_criadas",
        verbose_name="Criado por",
    )
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    atualizado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        editable=False,
        related_name="atividades_camera_atualizadas",
        verbose_name="Atualizado por",
    )
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    class Meta:
        ordering = ["-ocorrida_em", "-pk"]
        verbose_name = "Atividade da câmera"
        verbose_name_plural = "Atividades das câmeras"

    def __str__(self):
        return f"{self.camera.nome} — {self.get_tipo_display()}"

class EventoAuditoriaQuerySet(models.QuerySet):
    def update(self, **kwargs):
        raise ValidationError("Eventos de auditoria são imutáveis.")

    def delete(self):
        raise ValidationError("Eventos de auditoria não podem ser excluídos.")


class EventoAuditoria(models.Model):
    class Categoria(models.TextChoices):
        AUTENTICACAO = "AUTENTICACAO", "Autenticação"
        CAMERA = "CAMERA", "Câmera"
        ATIVIDADE = "ATIVIDADE", "Atividade"
        PERFIL = "PERFIL", "Perfil"
        SISTEMA = "SISTEMA", "Sistema"

    class Origem(models.TextChoices):
        WEB = "WEB", "Web"
        ADMIN = "ADMIN", "Admin"
        COMANDO = "COMANDO", "Comando"
        SISTEMA = "SISTEMA", "Sistema"

    categoria = models.CharField(max_length=20, choices=Categoria.choices, db_index=True)
    codigo = models.CharField(max_length=100, db_index=True)
    resumo = models.CharField(max_length=255)
    camera = models.ForeignKey(Camera, on_delete=models.PROTECT, null=True, blank=True, related_name="eventos_auditoria")
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="eventos_auditoria")
    usuario_username = models.CharField(max_length=150, blank=True, default="")
    usuario_nome = models.CharField(max_length=200, blank=True, default="")
    usuario_email = models.EmailField(blank=True, default="")
    entidade_tipo = models.CharField(max_length=100, blank=True, default="")
    entidade_id = models.CharField(max_length=100, blank=True, default="")
    entidade_descricao = models.CharField(max_length=255, blank=True, default="")
    alteracoes = models.JSONField(default=dict, blank=True)
    metadados = models.JSONField(default=dict, blank=True)
    origem = models.CharField(max_length=20, choices=Origem.choices, default=Origem.WEB, db_index=True)
    ip_origem = models.GenericIPAddressField(null=True, blank=True)
    ocorrido_em = models.DateTimeField(default=timezone.now, db_index=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    objects = EventoAuditoriaQuerySet.as_manager()

    class Meta:
        ordering = ["-ocorrido_em", "-pk"]
        verbose_name = "Evento de auditoria"
        verbose_name_plural = "Eventos de auditoria"
        permissions = (("consultar_eventos", "Pode consultar eventos de auditoria"),)
        indexes = [
            models.Index(fields=["categoria", "ocorrido_em"]),
            models.Index(fields=["camera", "ocorrido_em"]),
            models.Index(fields=["usuario", "ocorrido_em"]),
            models.Index(fields=["origem", "ocorrido_em"]),
        ]

    def __str__(self):
        return f"{self.codigo} — {self.resumo}"

    def save(self, *args, **kwargs):
        if self.pk:
            raise ValidationError("Eventos de auditoria são imutáveis.")
        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ValidationError("Eventos de auditoria não podem ser excluídos.")

class SubstituicaoCameraQuerySet(models.QuerySet):
    def update(self, **kwargs):
        raise ValidationError("Substituições de câmera são imutáveis.")

    def delete(self):
        raise ValidationError("Substituições de câmera não podem ser excluídas.")


class SubstituicaoCamera(models.Model):
    camera_anterior = models.ForeignKey(Camera, on_delete=models.PROTECT, related_name="substituicoes_como_anterior", verbose_name="Câmera anterior")
    camera_substituta = models.ForeignKey(Camera, on_delete=models.PROTECT, related_name="substituicoes_como_substituta", verbose_name="Câmera substituta")
    ocorrida_em = models.DateTimeField(default=timezone.now, db_index=True, verbose_name="Data da substituição")
    motivo = models.TextField(max_length=1000, verbose_name="Motivo")
    observacoes = models.TextField(blank=True, default="", verbose_name="Observações")
    nome_operacional = models.CharField(max_length=150, verbose_name="Nome operacional transferido")
    nome_anterior_substituta = models.CharField(max_length=150, verbose_name="Nome anterior da substituta")
    registrado_por = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="substituicoes_camera_registradas", verbose_name="Registrado por")
    registrado_por_username = models.CharField(max_length=150, blank=True, default="", verbose_name="Username registrado")
    registrado_por_nome = models.CharField(max_length=200, blank=True, default="", verbose_name="Nome registrado")
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name="Registrado em")

    objects = SubstituicaoCameraQuerySet.as_manager()

    class Meta:
        verbose_name = "Substituição de câmera"
        verbose_name_plural = "Substituições de câmeras"
        ordering = ["-ocorrida_em", "-pk"]
        permissions = (("consultar_substituicoescamera", "Pode consultar substituições de câmeras"),)
        indexes = [
            models.Index(fields=["camera_anterior", "ocorrida_em"]),
            models.Index(fields=["camera_substituta", "ocorrida_em"]),
        ]

    def __str__(self):
        return f"{self.camera_anterior} → {self.camera_substituta}"

    def save(self, *args, **kwargs):
        if self.pk:
            raise ValidationError("Substituições de câmera são imutáveis.")
        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ValidationError("Substituições de câmera não podem ser excluídas.")


class EstadoMonitoramento(models.Model):
    """Estado canônico local do monitoramento, isolado dos campos legados de Camera."""

    class EstadoEstavel(models.TextChoices):
        UNKNOWN = "UNKNOWN", "Desconhecido"
        ONLINE = "ONLINE", "Online"
        OFFLINE = "OFFLINE", "Offline"

    camera = models.OneToOneField(
        Camera,
        on_delete=models.CASCADE,
        related_name="estado_monitoramento",
    )
    estado_estavel = models.CharField(
        max_length=7,
        choices=EstadoEstavel.choices,
        default=EstadoEstavel.UNKNOWN,
    )
    estado_alterado_em = models.DateTimeField(null=True, blank=True)
    ultima_evidencia_util_em = models.DateTimeField(null=True, blank=True)
    proximo_vencimento_em = models.DateTimeField(null=True, blank=True, db_index=True)
    ultima_geracao_configuracao = models.PositiveIntegerField(default=1)
    sequencia_positiva = models.PositiveIntegerField(default=0)
    sequencia_negativa = models.PositiveIntegerField(default=0)
    confirmacao_ultima_observacao_em = models.DateTimeField(null=True, blank=True)
    versao_politica_confirmacao = models.CharField(max_length=64, default="initial")
    em_escopo = models.BooleanField(default=True, db_index=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Estado de monitoramento"
        verbose_name_plural = "Estados de monitoramento"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(estado_estavel__in=["UNKNOWN", "ONLINE", "OFFLINE"]),
                name="estado_monitoramento_estado_estavel_valid",
            ),
        ]


class TransicaoEstadoMonitoramento(models.Model):
    """Histórico enxuto: somente mudanças de estado técnico estável."""

    camera = models.ForeignKey(
        Camera,
        on_delete=models.CASCADE,
        related_name="transicoes_monitoramento",
    )
    estado_anterior = models.CharField(max_length=7, choices=EstadoMonitoramento.EstadoEstavel.choices)
    estado_atual = models.CharField(max_length=7, choices=EstadoMonitoramento.EstadoEstavel.choices)
    ocorrida_em = models.DateTimeField(db_index=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["ocorrida_em", "pk"]
        indexes = [models.Index(fields=["camera", "ocorrida_em"])]
        verbose_name = "Transição de estado de monitoramento"
        verbose_name_plural = "Transições de estado de monitoramento"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(estado_anterior__in=["UNKNOWN", "ONLINE", "OFFLINE"]),
                name="transicao_estado_anterior_valid",
            ),
            models.CheckConstraint(
                condition=models.Q(estado_atual__in=["UNKNOWN", "ONLINE", "OFFLINE"]),
                name="transicao_estado_atual_valid",
            ),
        ]
