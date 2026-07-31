from django.contrib import admin
from .models import PerfilUsuario


@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ("usuario", "cargo", "setor", "telefone", "ramal", "atualizado_em")
    search_fields = ("usuario__username", "usuario__first_name", "usuario__last_name", "usuario__email", "telefone", "ramal", "cargo", "setor")
    list_filter = ("cargo", "setor", "atualizado_em")
    autocomplete_fields = ("usuario",)
    readonly_fields = ("usuario", "criado_em", "atualizado_em")
    fieldsets = (("Usuário", {"fields": ("usuario",)}), ("Dados organizacionais", {"fields": ("telefone", "ramal", "cargo", "setor")}), ("Governança", {"fields": ("criado_em", "atualizado_em")}))

    def has_add_permission(self, request): return False
    def has_delete_permission(self, request, obj=None): return False
