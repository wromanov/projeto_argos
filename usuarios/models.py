from django.conf import settings
from django.db import models


class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="perfil", verbose_name="Usuário")
    telefone = models.CharField(max_length=30, blank=True, default="", verbose_name="Telefone")
    ramal = models.CharField(max_length=20, blank=True, default="", verbose_name="Ramal")
    cargo = models.CharField(max_length=100, blank=True, default="", verbose_name="Cargo")
    setor = models.CharField(max_length=100, blank=True, default="", verbose_name="Setor")
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    class Meta:
        verbose_name = "Perfil de usuário"
        verbose_name_plural = "Perfis de usuários"
        ordering = ["usuario__username"]

    def __str__(self):
        nome = self.usuario.get_full_name().strip()
        return nome or self.usuario.get_username()
