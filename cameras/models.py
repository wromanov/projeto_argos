from uuid import uuid4

from django.conf import settings
from django.utils import timezone
from django.utils.text import get_valid_filename
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models
from django.db.models import F, Q
from django.db.models.functions import Coalesce, Lower
from django.db.models import Value

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
    firmware_version = models.CharField(
        max_length=100,
        blank=True,
        default="",
        verbose_name="Versão do firmware",
    )
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
        permissions = (
            ("desativar_camera", "Pode desativar câmera"),
            ("reativar_camera", "Pode reativar câmera"),
            ("alterar_situacao_camera", "Pode alterar situação operacional da câmera"),
            ("registrar_substituicao_camera", "Pode registrar substituição física de câmera"),
            ("view_camera_connection", "Pode consultar conexão técnica da câmera"),
            ("change_camera_connection", "Pode alterar conexão técnica da câmera"),
            ("manage_camera_capability", "Pode administrar capacidade técnica da câmera"),
            ("view_camera_credential", "Pode consultar metadados da credencial da câmera"),
            ("change_camera_credential", "Pode alterar credencial da câmera"),
            ("reveal_camera_credential", "Pode revelar credencial da câmera"),
            ("run_camera_connection_test", "Pode executar teste de conexão da câmera"),
            ("view_camera_diagnostic", "Pode consultar diagnóstico técnico da câmera"),
            ("capture_camera_image", "Pode executar captura direta da câmera"),
            ("manage_camera_target_policy", "Pode administrar política de destino de câmeras"),
            ("manage_monitoring_runtime", "Pode administrar o runtime de monitoramento"),
            ("importar_cameras", "Pode importar câmeras por planilha"),
        )
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


class CameraImportPreview(models.Model):
    """Prévia validada de XLSX, vinculada ao usuário e sem reter o arquivo."""

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    file_sha256 = models.CharField(max_length=64)
    plano = models.JSONField(default=list)
    resumo = models.JSONField(default=dict)
    criado_em = models.DateTimeField(auto_now_add=True)
    expira_em = models.DateTimeField(db_index=True)
    consumido_em = models.DateTimeField(null=True, blank=True)

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
    monitoring_owner_id = models.CharField(max_length=255, null=True, blank=True)
    monitoring_lease_expires_at = models.DateTimeField(null=True, blank=True, db_index=True)
    monitoring_ownership_epoch = models.PositiveBigIntegerField(default=0)
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
            models.CheckConstraint(
                condition=(
                    models.Q(monitoring_owner_id__isnull=True, monitoring_lease_expires_at__isnull=True)
                    | models.Q(monitoring_owner_id__isnull=False, monitoring_lease_expires_at__isnull=False)
                ),
                name="estado_monitoramento_lease_coherent",
            ),
        ]


class CameraHealthSnapshot(models.Model):
    """Última sequência sanitizada de diagnóstico automático A-D."""

    class StageState(models.TextChoices):
        PASS = "PASS", "Pass"
        FAIL = "FAIL", "Fail"
        NOT_RUN = "NOT_RUN", "Not run"

    camera = models.OneToOneField(
        Camera,
        on_delete=models.CASCADE,
        related_name="health_snapshot",
    )
    observed_at = models.DateTimeField()
    config_generation = models.PositiveIntegerField()
    stage_a_state = models.CharField(max_length=7, choices=StageState.choices)
    stage_a_observed_at = models.DateTimeField()
    stage_a_duration_seconds = models.FloatField()
    stage_a_error_code = models.CharField(max_length=64, blank=True, default="")
    stage_b_state = models.CharField(max_length=7, choices=StageState.choices)
    stage_b_observed_at = models.DateTimeField()
    stage_b_duration_seconds = models.FloatField()
    stage_b_error_code = models.CharField(max_length=64, blank=True, default="")
    stage_c_state = models.CharField(max_length=7, choices=StageState.choices)
    stage_c_observed_at = models.DateTimeField()
    stage_c_duration_seconds = models.FloatField()
    stage_c_error_code = models.CharField(max_length=64, blank=True, default="")
    stage_d_state = models.CharField(max_length=7, choices=StageState.choices)
    stage_d_observed_at = models.DateTimeField()
    stage_d_duration_seconds = models.FloatField()
    stage_d_error_code = models.CharField(max_length=64, blank=True, default="")
    reached_stage = models.CharField(max_length=1, blank=True, default="")
    correlation_id = models.UUIDField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [models.Index(fields=["observed_at"], name="cam_health_observed_idx")]
        constraints = [
            models.CheckConstraint(condition=Q(config_generation__gt=0), name="cam_health_generation_positive"),
            *[
                models.CheckConstraint(
                    condition=Q(**{f"stage_{stage}_state__in": ["PASS", "FAIL", "NOT_RUN"]}),
                    name=f"cam_health_stage_{stage}_state_valid",
                )
                for stage in "abcd"
            ],
            *[
                models.CheckConstraint(
                    condition=Q(**{f"stage_{stage}_duration_seconds__gte": 0}),
                    name=f"cam_health_stage_{stage}_duration_nonnegative",
                )
                for stage in "abcd"
            ],
            models.CheckConstraint(
                condition=Q(reached_stage__in=["", "A", "B", "C", "D"]),
                name="cam_health_reached_stage_valid",
            ),
            models.CheckConstraint(
                condition=Q(stage_a_state="PASS") | Q(stage_b_state="NOT_RUN"),
                name="cam_health_stage_b_requires_a",
            ),
            models.CheckConstraint(
                condition=Q(stage_b_state="PASS") | Q(stage_c_state="NOT_RUN"),
                name="cam_health_stage_c_requires_b",
            ),
            models.CheckConstraint(
                condition=Q(stage_c_state="PASS") | Q(stage_d_state="NOT_RUN"),
                name="cam_health_stage_d_requires_c",
            ),
            models.CheckConstraint(
                condition=Q(stage_a_state="PASS", stage_b_state="PASS", stage_c_state="PASS", stage_d_state="PASS")
                | ~Q(stage_d_state="PASS"),
                name="cam_health_d_pass_requires_abc",
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


class Indisponibilidade(models.Model):
    """Intervalo técnico confirmado de indisponibilidade de uma câmera."""

    class OrigemAbertura(models.TextChoices):
        INITIAL_OFFLINE = "INITIAL_OFFLINE", "Offline inicial"
        ONLINE_TO_OFFLINE = "ONLINE_TO_OFFLINE", "Online para offline"

    class MotivoFechamento(models.TextChoices):
        RECUPERADA = "RECUPERADA", "Recuperada"
        SAIU_DO_ESCOPO = "SAIU_DO_ESCOPO", "Saiu do escopo"

    camera = models.ForeignKey(
        Camera,
        on_delete=models.PROTECT,
        related_name="indisponibilidades",
        verbose_name="Câmera",
    )
    opened_at = models.DateTimeField(db_index=True, verbose_name="Aberta em")
    closed_at = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True,
        verbose_name="Encerrada em",
    )
    open_origin = models.CharField(
        max_length=20,
        choices=OrigemAbertura.choices,
        verbose_name="Origem da abertura",
    )
    close_reason = models.CharField(
        max_length=20,
        choices=MotivoFechamento.choices,
        null=True,
        blank=True,
        verbose_name="Motivo do encerramento",
    )
    opening_transition = models.OneToOneField(
        TransicaoEstadoMonitoramento,
        on_delete=models.PROTECT,
        related_name="indisponibilidade_aberta",
        verbose_name="Transição de abertura",
    )
    closing_transition = models.OneToOneField(
        TransicaoEstadoMonitoramento,
        on_delete=models.PROTECT,
        related_name="indisponibilidade_fechada",
        null=True,
        blank=True,
        verbose_name="Transição de encerramento",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criada em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizada em")

    class Meta:
        ordering = ["-opened_at", "-pk"]
        verbose_name = "Indisponibilidade"
        verbose_name_plural = "Indisponibilidades"
        indexes = [
            models.Index(fields=["camera", "-opened_at"], name="indisp_camera_opened_idx"),
        ]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(
                    open_origin__in=[
                        "INITIAL_OFFLINE",
                        "ONLINE_TO_OFFLINE",
                    ]
                ),
                name="indisp_open_origin_valid",
            ),
            models.CheckConstraint(
                condition=models.Q(close_reason__isnull=True)
                | models.Q(
                    close_reason__in=[
                        "RECUPERADA",
                        "SAIU_DO_ESCOPO",
                    ]
                ),
                name="indisp_close_reason_valid",
            ),
            models.CheckConstraint(
                condition=models.Q(closed_at__isnull=True)
                | models.Q(closed_at__gte=F("opened_at")),
                name="indisp_closed_at_after_opened_at",
            ),
            models.CheckConstraint(
                condition=(
                    models.Q(
                        closed_at__isnull=True,
                        close_reason__isnull=True,
                        closing_transition__isnull=True,
                    )
                    | models.Q(closed_at__isnull=False, close_reason__isnull=False)
                ),
                name="indisp_open_closed_coherent",
            ),
            models.CheckConstraint(
                condition=(
                    models.Q(close_reason__isnull=True, closing_transition__isnull=True)
                    | models.Q(
                        close_reason="RECUPERADA",
                        closing_transition__isnull=False,
                    )
                    | models.Q(
                        close_reason="SAIU_DO_ESCOPO",
                        closing_transition__isnull=True,
                    )
                ),
                name="indisp_close_reason_transition_coherent",
            ),
            models.UniqueConstraint(
                fields=["camera"],
                condition=models.Q(closed_at__isnull=True),
                name="indisp_one_open_camera",
            ),
        ]



def validar_referencia_objeto_storage(value):
    """Rejeita URLs e caminhos absolutos; a chave não é uma autorização de acesso."""
    partes = value.split("/")
    if (
        not value
        or value != value.strip()
        or "://" in value
        or value.startswith(("/", "\\"))
        or "\\" in value
        or any(parte in {".", ".."} for parte in partes)
    ):
        raise ValidationError("Informe uma referência opaca e relativa ao storage.")


def sanitizar_nome_original(value):
    """Mantém apenas o nome-base para exibição/auditoria, nunca caminhos do cliente."""
    candidato = str(value or "").replace("\\", "/").split("/")[-1]
    candidato = "".join(char for char in candidato if ord(char) >= 32 and ord(char) != 127)
    if not candidato:
        return ""
    return get_valid_filename(candidato)[:255]


class CameraImageRecordQuerySet(models.QuerySet):
    def update(self, **kwargs):
        raise ValidationError(
            "Fatos e lifecycle de imagem só podem mudar pelo serviço de lifecycle."
        )

    def bulk_update(self, objs, fields, batch_size=None):
        raise ValidationError(
            "Fatos e lifecycle de imagem só podem mudar pelo serviço de lifecycle."
        )

    def delete(self):
        raise ValidationError("Registros de imagem são históricos; use a retirada lógica.")


class CameraImageRecord(models.Model):
    class Provenance(models.TextChoices):
        CAPTURA_CAMERA = "CAPTURA_CAMERA", "Captura da câmera"
        UPLOAD_MANUAL = "UPLOAD_MANUAL", "Upload manual"

    class IntegrityStatus(models.TextChoices):
        VALID = "VALID", "Íntegro"
        INVALID = "INVALID", "Inválido ou corrompido"

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    camera = models.ForeignKey(
        Camera,
        on_delete=models.PROTECT,
        related_name="image_records",
        db_index=False,
        verbose_name="Câmera",
    )
    provenance = models.CharField(max_length=20, choices=Provenance.choices)
    captured_at = models.DateTimeField(null=True, blank=True, verbose_name="Capturada em")
    recorded_at = models.DateTimeField(default=timezone.now, editable=False, verbose_name="Registrada em")
    storage_key = models.CharField(
        max_length=512,
        validators=[validar_referencia_objeto_storage],
        verbose_name="Referência opaca no storage",
    )
    content_type = models.CharField(
        max_length=127,
        validators=[RegexValidator(r"\Aimage/[A-Za-z0-9][A-Za-z0-9.+-]*\Z", "Informe um content type de imagem registrado.")],
        verbose_name="Content type validado",
    )
    size_bytes = models.PositiveBigIntegerField(null=True, blank=True, verbose_name="Tamanho em bytes")
    width = models.PositiveIntegerField(null=True, blank=True, verbose_name="Largura em pixels")
    height = models.PositiveIntegerField(null=True, blank=True, verbose_name="Altura em pixels")
    sha256 = models.CharField(
        max_length=64,
        validators=[RegexValidator(r"\A[a-f0-9]{64}\Z", "Informe o SHA-256 hexadecimal calculado pelo servidor.")],
        verbose_name="SHA-256",
    )
    integrity_status = models.CharField(
        max_length=10,
        choices=IntegrityStatus.choices,
        default=IntegrityStatus.VALID,
        verbose_name="Integridade",
    )
    original_filename = models.CharField(max_length=255, blank=True, default="", verbose_name="Nome original sanitizado")
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="camera_image_records_uploaded",
        verbose_name="Enviado por",
    )
    captured_by_system = models.CharField(max_length=255, blank=True, default="", verbose_name="Sistema executor da captura")
    recorded_by_system = models.CharField(max_length=255, blank=True, default="", verbose_name="Sistema registrador")
    withdrawn_at = models.DateTimeField(null=True, blank=True, verbose_name="Retirada em")
    withdrawn_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="camera_image_records_withdrawn",
        verbose_name="Retirada por",
    )
    withdrawal_reason = models.CharField(max_length=500, blank=True, default="", verbose_name="Motivo da retirada")
    retention_held_at = models.DateTimeField(null=True, blank=True, verbose_name="Protegida desde")
    retention_held_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="camera_image_records_held",
        verbose_name="Protegida por",
    )

    objects = CameraImageRecordQuerySet.as_manager()

    class Meta:
        verbose_name = "Registro de imagem da câmera"
        verbose_name_plural = "Registros de imagem da câmera"
        permissions = [
            ("manage_camera_image_hold", "Pode proteger ou liberar retenção de imagem por câmera"),
        ]
        constraints = [
            models.CheckConstraint(
                condition=Q(provenance__in=["CAPTURA_CAMERA", "UPLOAD_MANUAL"]),
                name="camimg_provenance_valid",
            ),
            models.CheckConstraint(
                condition=(
                    Q(provenance="CAPTURA_CAMERA", captured_at__isnull=False)
                    | Q(provenance="UPLOAD_MANUAL", captured_at__isnull=True)
                ),
                name="camimg_capture_time_semantics",
            ),
            models.CheckConstraint(
                condition=Q(integrity_status__in=["VALID", "INVALID"]),
                name="camimg_integrity_valid",
            ),
            models.CheckConstraint(
                condition=(
                    Q(withdrawn_at__isnull=True, withdrawal_reason="")
                    | Q(withdrawn_at__isnull=False, withdrawal_reason__gt="")
                ),
                name="camimg_withdrawal_auditable",
            ),
            models.CheckConstraint(
                condition=(
                    Q(retention_held_by__isnull=True, retention_held_at__isnull=True)
                    | Q(retention_held_by__isnull=False, retention_held_at__isnull=False)
                ),
                name="camimg_hold_actor_has_timestamp",
            ),
            models.CheckConstraint(
                condition=(
                    Q(width__isnull=True, height__isnull=True)
                    | Q(width__gt=0, height__gt=0)
                ),
                name="camimg_dimensions_coherent",
            ),
            models.CheckConstraint(
                condition=~Q(storage_key="") & ~Q(sha256=""),
                name="camimg_object_facts_present",
            ),
        ]
        indexes = [
            models.Index(
                fields=["camera", "provenance", "withdrawn_at", "-captured_at", "-recorded_at", "-id"],
                name="camimg_latest_current_idx",
            ),
        ]

    _IMMUTABLE_FACT_FIELDS = (
        "camera_id",
        "provenance",
        "captured_at",
        "recorded_at",
        "storage_key",
        "content_type",
        "size_bytes",
        "width",
        "height",
        "sha256",
        "original_filename",
        "uploaded_by_id",
        "captured_by_system",
        "recorded_by_system",
    )

    def clean(self):
        super().clean()
        errors = {}
        if self.provenance == self.Provenance.CAPTURA_CAMERA:
            if self.captured_at is None:
                errors["captured_at"] = "Capturas da câmera exigem o instante observado pelo fluxo autorizado."
            elif timezone.is_naive(self.captured_at):
                errors["captured_at"] = "captured_at deve ser timezone-aware."
        elif self.provenance == self.Provenance.UPLOAD_MANUAL and self.captured_at is not None:
            errors["captured_at"] = "Upload manual não recebe captured_at presumido."
        if self.recorded_at is not None and timezone.is_naive(self.recorded_at):
            errors["recorded_at"] = "recorded_at deve ser timezone-aware."
        if self.withdrawn_at is not None:
            if timezone.is_naive(self.withdrawn_at):
                errors["withdrawn_at"] = "withdrawn_at deve ser timezone-aware."
            if not self.withdrawal_reason.strip():
                errors["withdrawal_reason"] = "A retirada lógica exige um motivo auditável."
        elif self.withdrawal_reason:
            errors["withdrawal_reason"] = "O motivo só pode ser informado junto à retirada lógica."
        if self.retention_held_at is not None and timezone.is_naive(self.retention_held_at):
            errors["retention_held_at"] = "retention_held_at deve ser timezone-aware."
        if self.retention_held_by_id is not None and self.retention_held_at is None:
            errors["retention_held_at"] = "Um autor de hold exige retention_held_at."
        if self.withdrawn_at is not None and self.retention_held_at is not None:
            errors["retention_held_at"] = "Imagem retirada não pode permanecer protegida."
        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.original_filename = sanitizar_nome_original(self.original_filename)
        if not self._state.adding:
            previous = type(self).objects.filter(pk=self.pk).values(
                *self._IMMUTABLE_FACT_FIELDS,
                "integrity_status",
                "withdrawn_at",
                "withdrawn_by_id",
                "withdrawal_reason",
                "retention_held_at",
                "retention_held_by_id",
            ).first()
            if previous is None:
                raise ValidationError("A identidade de um registro de imagem não pode ser substituída.")
            changed = [
                field for field in self._IMMUTABLE_FACT_FIELDS
                if previous[field] != getattr(self, field)
            ]
            if changed:
                raise ValidationError("Os fatos históricos do registro de imagem são imutáveis.")
            if previous["integrity_status"] == self.IntegrityStatus.INVALID and self.integrity_status != self.IntegrityStatus.INVALID:
                raise ValidationError("A integridade inválida não pode ser revertida no mesmo registro.")
            lifecycle_before = (
                previous["withdrawn_at"], previous["withdrawn_by_id"], previous["withdrawal_reason"]
            )
            lifecycle_after = (self.withdrawn_at, self.withdrawn_by_id, self.withdrawal_reason)
            hold_before = (previous["retention_held_at"], previous["retention_held_by_id"])
            hold_after = (self.retention_held_at, self.retention_held_by_id)
            service_mutation = getattr(self, "_lifecycle_service_mutation", False)
            if lifecycle_before != lifecycle_after and not service_mutation:
                raise ValidationError("Retirada lógica só pode mudar pelo serviço de lifecycle.")
            if previous["withdrawn_at"] is not None and lifecycle_before != lifecycle_after:
                raise ValidationError("A retirada lógica é histórica e não pode ser alterada ou revertida.")
            if hold_before != hold_after and not service_mutation:
                raise ValidationError("Hold só pode mudar pelo serviço de lifecycle.")
            if hold_before[0] is not None and hold_after[0] is not None and hold_before != hold_after:
                raise ValidationError("Um hold ativo não pode ser substituído; libere-o primeiro.")
        self.full_clean()
        result = super().save(*args, **kwargs)
        if hasattr(self, "_lifecycle_service_mutation"):
            del self._lifecycle_service_mutation
        return result

    def withdraw(self, *, reason, by=None, at=None):
        if not getattr(self, "_lifecycle_service_mutation", False):
            raise ValidationError("Retirada lógica só pode mudar pelo serviço de lifecycle.")
        if self._state.adding:
            raise ValidationError("Salve o registro antes de retirá-lo logicamente.")
        if self.withdrawn_at is not None:
            raise ValidationError("O registro já foi retirado logicamente.")
        self.withdrawn_at = at or timezone.now()
        self.withdrawn_by = by
        self.withdrawal_reason = str(reason or "").strip()
        self.save(update_fields=["withdrawn_at", "withdrawn_by", "withdrawal_reason"])

    def delete(self, *args, **kwargs):
        raise ValidationError("Registros de imagem são históricos; use a retirada lógica.")

    def __str__(self):
        return f"{self.provenance} · {self.camera_id} · {self.pk}"

class CameraCapabilityProfile(models.Model):
    class Adapter(models.TextChoices):
        RTSP = "RTSP", "RTSP"
        HTTP_SNAPSHOT = "HTTP_SNAPSHOT", "HTTP snapshot"

    class TLSPolicy(models.TextChoices):
        REQUIRED = "REQUIRED", "Required"
        NOT_REQUIRED = "NOT_REQUIRED", "Not required"
        NOT_APPLICABLE = "NOT_APPLICABLE", "Not applicable"

    class AuthMethod(models.TextChoices):
        NONE = "NONE", "None"
        BASIC = "BASIC", "Basic"
        DIGEST = "DIGEST", "Digest"
        RTSP_NEGOTIATE = "RTSP_NEGOTIATE", "RTSP negotiate"

    class EndpointPolicy(models.TextChoices):
        PROFILE_FIXED = "PROFILE_FIXED", "Profile fixed"
        TECHNICIAN_OVERRIDE = "TECHNICIAN_OVERRIDE", "Technician override"

    class ProbeStage(models.TextChoices):
        A = "A", "Network reachability"
        B = "B", "Protocol reachability"
        C = "C", "Media description"
        D = "D", "Media delivery"

    profile_key = models.CharField(max_length=64)
    version = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    active = models.BooleanField(default=False)
    adapter_key = models.CharField(max_length=20, choices=Adapter.choices)
    allowed_schemes = models.JSONField(default=list)
    allowed_ports = models.JSONField(default=list)
    tls_policy = models.CharField(max_length=20, choices=TLSPolicy.choices)
    auth_method = models.CharField(max_length=20, choices=AuthMethod.choices)
    credential_required = models.BooleanField(default=False)
    endpoint_policy = models.CharField(max_length=24, choices=EndpointPolicy.choices)
    default_path = models.CharField(max_length=512, blank=True, default="")
    allowed_override_fields = models.JSONField(default=list)
    probe_evidence_stage = models.CharField(max_length=1, choices=ProbeStage.choices)
    source_ref = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="camera_capability_profiles_created",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["profile_key", "version"], name="uniq_camera_capability_profile_version"),
            models.CheckConstraint(condition=Q(version__gt=0), name="camera_capability_profile_version_positive"),
        ]
        indexes = [models.Index(fields=["active", "adapter_key"], name="cam_cap_active_adapter_idx")]
        ordering = ["profile_key", "-version"]

    def clean(self):
        super().clean()
        if not isinstance(self.allowed_schemes, list) or any(item not in {"rtsp", "rtsps", "http", "https"} for item in self.allowed_schemes):
            raise ValidationError({"allowed_schemes": "Schemes fora da allowlist do catálogo."})
        if not isinstance(self.allowed_ports, list) or any(type(item) is not int or not 1 <= item <= 65535 for item in self.allowed_ports):
            raise ValidationError({"allowed_ports": "Portas devem ser inteiros entre 1 e 65535."})
        if not isinstance(self.allowed_override_fields, list) or any(item not in {"path", "port", "transport"} for item in self.allowed_override_fields):
            raise ValidationError({"allowed_override_fields": "Override fora da allowlist do catálogo."})

    def save(self, *args, **kwargs):
        if self.pk:
            previous = type(self).objects.get(pk=self.pk)
            changed_fields = {
                field.name
                for field in self._meta.concrete_fields
                if field.name not in {"id", "created_at"}
                and getattr(previous, field.attname) != getattr(self, field.attname)
            }
            if previous.active and changed_fields - {"active"}:
                raise ValidationError("Versões ativas de capability são imutáveis; somente a desativação é permitida.")
        return super().save(*args, **kwargs)


class CameraCapabilityEvidence(models.Model):
    class Status(models.TextChoices):
        SUPPORTED = "SUPPORTED", "Supported"
        UNSUPPORTED = "UNSUPPORTED", "Unsupported"
        UNVERIFIED = "UNVERIFIED", "Unverified"

    class SourceType(models.TextChoices):
        DATASHEET = "DATASHEET", "Datasheet"
        LAB = "LAB", "Laboratory"
        UNIT = "UNIT", "Unit"

    profile = models.ForeignKey(
        CameraCapabilityProfile,
        on_delete=models.PROTECT,
        related_name="evidence",
    )
    camera = models.ForeignKey(
        Camera,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="capability_evidence",
    )
    vendor = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    firmware_exact = models.CharField(max_length=100, blank=True, default="")
    status = models.CharField(max_length=12, choices=Status.choices)
    source_type = models.CharField(max_length=10, choices=SourceType.choices)
    source_ref = models.CharField(max_length=255)
    evidence_date = models.DateField()
    environment = models.CharField(max_length=255, blank=True, default="")
    limitations = models.TextField(blank=True, default="")
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="camera_capability_evidence_reviewed",
    )
    active = models.BooleanField(default=True)

    class Meta:
        indexes = [
            models.Index(
                fields=["profile", "vendor", "model", "firmware_exact", "status"],
                name="cam_evidence_match_idx",
            ),
            models.Index(fields=["camera", "profile"], name="cam_evidence_camera_idx"),
        ]
        constraints = [
            models.CheckConstraint(
                condition=Q(status__in=("SUPPORTED", "UNSUPPORTED", "UNVERIFIED")),
                name="cam_evidence_status_valid",
            ),
            models.CheckConstraint(
                condition=Q(source_type__in=("DATASHEET", "LAB", "UNIT")),
                name="cam_evidence_source_valid",
            ),
            models.UniqueConstraint(
                "profile",
                "vendor",
                "model",
                "firmware_exact",
                Coalesce("camera_id", Value(0)),
                "source_ref",
                condition=Q(active=True),
                name="uniq_active_cam_cap_evidence",
            ),
        ]

    def clean(self):
        super().clean()
        self.vendor = " ".join((self.vendor or "").split()).casefold()
        self.model = " ".join((self.model or "").split()).casefold()
        self.firmware_exact = " ".join((self.firmware_exact or "").split()).casefold()
        if not self.vendor:
            raise ValidationError({"vendor": "Fabricante é obrigatório."})
        if not self.model:
            raise ValidationError({"model": "Modelo é obrigatório."})
        if not self.source_ref.strip():
            raise ValidationError({"source_ref": "Referência de origem é obrigatória."})

    def save(self, *args, **kwargs):
        self.vendor = " ".join((self.vendor or "").split()).casefold()
        self.model = " ".join((self.model or "").split()).casefold()
        self.firmware_exact = " ".join((self.firmware_exact or "").split()).casefold()
        self.source_ref = (self.source_ref or "").strip()
        return super().save(*args, **kwargs)


class CameraCredential(models.Model):
    class State(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        INACTIVE = "INACTIVE", "Inactive"

    camera = models.OneToOneField(Camera, on_delete=models.CASCADE, related_name="credential")
    active_version = models.ForeignKey(
        "CameraCredentialVersion",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="active_for_credentials",
    )
    state = models.CharField(max_length=12, choices=State.choices, default=State.INACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="camera_credentials_updated",
    )

    def __str__(self):
        return f"Credential for camera {self.camera_id}"


class CameraCredentialVersion(models.Model):
    class State(models.TextChoices):
        PENDING = "PENDING", "Pending"
        ACTIVE = "ACTIVE", "Active"
        RETIRED = "RETIRED", "Retired"
        REVOKED = "REVOKED", "Revoked"

    credential = models.ForeignKey(CameraCredential, on_delete=models.CASCADE, related_name="versions")
    version = models.PositiveIntegerField()
    ciphertext = models.TextField()
    key_version = models.CharField(max_length=32)
    state = models.CharField(max_length=10, choices=State.choices, default=State.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="camera_credential_versions_created",
    )
    activated_at = models.DateTimeField(null=True, blank=True)
    retired_at = models.DateTimeField(null=True, blank=True)
    revoked_at = models.DateTimeField(null=True, blank=True)
    rotated_from = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="rotations",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["credential", "version"], name="uniq_camera_credential_version"),
            models.UniqueConstraint(
                fields=["credential"],
                condition=Q(state="ACTIVE"),
                name="uniq_active_camera_credential_version",
            ),
            models.CheckConstraint(condition=Q(version__gt=0), name="camera_credential_version_positive"),
        ]
        indexes = [models.Index(fields=["credential", "state", "version"], name="cam_cred_state_ver_idx")]

    def __str__(self):
        return f"Credential version {self.version} for {self.credential_id}"


class CameraConnectionConfig(models.Model):
    class Transport(models.TextChoices):
        AUTO = "AUTO", "Automatic"
        TCP = "TCP", "TCP"
        UDP = "UDP", "UDP"

    camera = models.OneToOneField(Camera, on_delete=models.CASCADE, related_name="connection_config")
    profile = models.ForeignKey(CameraCapabilityProfile, on_delete=models.PROTECT, related_name="camera_configs")
    credential = models.ForeignKey(
        CameraCredential,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="connection_configs",
    )
    enabled = models.BooleanField(default=False)
    rtsp_uri = models.CharField(max_length=1024, blank=True, default="")
    http_endpoint_override = models.CharField(max_length=512, blank=True, default="")
    http_port_override = models.PositiveIntegerField(null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(65535)])
    transport = models.CharField(max_length=8, choices=Transport.choices, default=Transport.AUTO)
    config_version = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="camera_connection_configs_updated")

    class Meta:
        constraints = [models.CheckConstraint(condition=Q(config_version__gt=0), name="camera_connection_config_version_positive")]
        indexes = [models.Index(fields=["enabled", "profile"], name="cam_conn_enabled_profile_idx")]


class CameraCaptureJob(models.Model):
    """Durable request and worker state for an explicit camera image capture."""

    class Source(models.TextChoices):
        HTTP_SNAPSHOT = "HTTP_SNAPSHOT", "HTTP snapshot"
        RTSP_FRAME = "RTSP_FRAME", "RTSP frame"

    class Status(models.TextChoices):
        QUEUED = "QUEUED", "Queued"
        RUNNING = "RUNNING", "Running"
        SUCCEEDED = "SUCCEEDED", "Succeeded"
        FAILED = "FAILED", "Failed"
        CANCELLED = "CANCELLED", "Cancelled"

    ERROR_CODES = (
        "AUTHORIZATION_DENIED", "CONFIG_INVALID", "CAPABILITY_UNSUPPORTED",
        "TARGET_DENIED", "CREDENTIAL_UNAVAILABLE", "CONNECT_TIMEOUT",
        "READ_TIMEOUT", "TLS_ERROR", "CONNECT_ERROR", "HTTP_TRANSPORT_ERROR",
        "AUTH_FAILURE", "HTTP_STATUS_ERROR", "CONTENT_TYPE_INVALID",
        "BODY_TOO_LARGE", "IMAGE_INVALID", "STORAGE_ERROR", "LIFECYCLE_BLOCKED", "INTERNAL_ERROR",
    )

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    camera = models.ForeignKey(Camera, on_delete=models.PROTECT, related_name="capture_jobs")
    requestor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="camera_capture_jobs")
    idempotency_key = models.CharField(max_length=128)
    source = models.CharField(max_length=20, choices=Source.choices)
    profile_key = models.CharField(max_length=64)
    profile_version = models.PositiveIntegerField()
    config_version = models.PositiveIntegerField()
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.QUEUED)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    error_code = models.CharField(max_length=32, blank=True, default="")
    image_record = models.OneToOneField(
        CameraImageRecord, on_delete=models.PROTECT, null=True, blank=True,
        related_name="capture_job",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["camera", "requestor", "idempotency_key"], name="cam_capture_idempotency_uniq"),
            models.UniqueConstraint(
                fields=["camera"],
                condition=Q(status__in=["QUEUED", "RUNNING"]),
                name="cam_capture_active_camera_uniq",
            ),
            models.CheckConstraint(condition=Q(source__in=["HTTP_SNAPSHOT", "RTSP_FRAME"]), name="cam_capture_source_valid"),
            models.CheckConstraint(condition=Q(status__in=["QUEUED", "RUNNING", "SUCCEEDED", "FAILED", "CANCELLED"]), name="cam_capture_status_valid"),
            models.CheckConstraint(condition=Q(profile_version__gt=0), name="cam_capture_profile_version_positive"),
            models.CheckConstraint(condition=Q(config_version__gt=0), name="cam_capture_config_version_positive"),
            models.CheckConstraint(
                condition=(
                    Q(status="SUCCEEDED", image_record__isnull=False, error_code="")
                    | Q(status__in=["QUEUED", "RUNNING"], image_record__isnull=True, error_code="")
                    | Q(status__in=["FAILED", "CANCELLED"], image_record__isnull=True, error_code__gt="")
                ),
                name="cam_capture_result_coherent",
            ),
        ]
        indexes = [
            models.Index(fields=["status", "created_at"], name="cam_capture_status_created_idx"),
            models.Index(fields=["camera", "created_at"], name="cam_capture_camera_created_idx"),
        ]

    def __str__(self):
        return f"{self.source} · {self.camera_id} · {self.pk} · {self.status}"
