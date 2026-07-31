from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models


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

    patrimonio = models.CharField(
        max_length=50,
        unique=True,
        null=True,
        blank=True,
        verbose_name="Patrimônio",
    )
    nome = models.CharField(max_length=150, unique=True)
    fabricante = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    serial = models.CharField(
        max_length=100,
        unique=True,
        null=True,
        blank=True,
        verbose_name="Número de série",
    )
    mac = models.CharField(
        max_length=17,
        null=True,
        blank=True,
        verbose_name="Endereço MAC",
        validators=[
            RegexValidator(
                regex=r"^(?:[0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$",
                message="Informe um endereço MAC no formato AA:BB:CC:DD:EE:FF.",
            ),
        ],
    )
    ativo = models.BooleanField(default=True, verbose_name="Ativa")
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

    ip = models.GenericIPAddressField(protocol="IPv4", unique=True)
    mascara_subrede = models.GenericIPAddressField(
        protocol="IPv4",
        verbose_name="Máscara de sub-rede",
    )
    gateway = models.GenericIPAddressField(protocol="IPv4", null=True, blank=True)
    vlan = models.PositiveSmallIntegerField(
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

    def __str__(self):
        return self.nome
