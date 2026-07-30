from django.db import models


class Camera(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    nome = models.CharField(max_length=150)
    ip = models.GenericIPAddressField(unique=True)
    fabricante = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.codigo} - {self.nome}"
