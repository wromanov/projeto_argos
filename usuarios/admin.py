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

    def save_model(self, request, obj, form, change):
        anterior = PerfilUsuario.objects.get(pk=obj.pk) if change else None
        super().save_model(request, obj, form, change)
        alteracoes = calcular_alteracoes(anterior, obj, ("telefone", "ramal")) if anterior else {}
        if alteracoes:
            registrar_evento(
                codigo="perfil.atualizado",
                resumo="Perfil atualizado pelo Admin",
                categoria=EventoAuditoria.Categoria.PERFIL,
                request=request,
                usuario=obj.usuario,
                entidade=obj.usuario,
                alteracoes=alteracoes,
                origem=EventoAuditoria.Origem.ADMIN,
            )

    def has_add_permission(self, request): return False
    def has_delete_permission(self, request, obj=None): return False
