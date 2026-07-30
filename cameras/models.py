from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Camera(models.Model):
    class TipoCamera(models.TextChoices):
        BULLET = "BULLET", "Bullet"
        DOME = "DOME", "Dome"
        SPEED_DOME = "SPEED_DOME", "Speed Dome"
        FISHEYE = "FISHEYE", "Fisheye"

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

    def __str__(self):
        return self.nome