from django.core.validators import MaxValueValidator, MinValueValidator
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

    nome = models.CharField(
        max_length=150,
        unique=True,
    )

    ip = models.GenericIPAddressField(
        protocol="IPv4",
        unique=True,
    )

    mascara_subrede = models.GenericIPAddressField(
        protocol="IPv4",
        verbose_name="Máscara de sub-rede",
    )

    vlan = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(4094),
        ],
    )

    fabricante = models.CharField(
        max_length=100,
    )

    modelo = models.CharField(
        max_length=100,
    )

    tipo = models.CharField(
        max_length=20,
        choices=TipoCamera.choices,
        blank=True,
        default="",
        verbose_name="Tipo de câmera",
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

    def __str__(self):
        return self.nome