from django.contrib import admin

from .models import AtividadeCamera, Camera


@admin.register(Camera)
class CameraAdmin(admin.ModelAdmin):
    list_display = (
        "nome",
        "patrimonio",
        "status",
        "ativo",
        "terminal",
        "ip",
        "vlan",
        "farm",
        "fabricante",
        "modelo",
        "ultima_verificacao",
        "atualizado_em",
    )
    search_fields = (
        "nome",
        "patrimonio",
        "ip",
        "serial",
        "mac",
        "fabricante",
        "modelo",
        "terminal",
        "setor",
        "ambiente",
    )
    list_filter = (
        "ativo",
        "status",
        "tipo",
        "terminal",
        "fabricante",
        "vlan",
        "farm",
        "origem_cadastro",
    )
    readonly_fields = (
        "criado_por",
        "criado_em",
        "atualizado_por",
        "atualizado_em",
    )
    fieldsets = (
        (
            "Identificação",
            {
                "fields": (
                    "patrimonio",
                    "nome",
                    "fabricante",
                    "modelo",
                    "serial",
                    "mac",
                    "ativo",
                    "tipo",
                ),
            },
        ),
        (
            "Localização",
            {
                "fields": (
                    "terminal",
                    "pavimento",
                    "setor",
                    "ambiente",
                    "descricao_detalhada",
                    "ponto_referencia",
                ),
            },
        ),
        ("Rede", {"fields": ("ip", "mascara_subrede", "gateway", "vlan")}),
        (
            "Gravação",
            {"fields": ("farm", "retencao_esperada_dias", "codec")},
        ),
        (
            "Monitoramento",
            {"fields": ("status", "status_em", "ultima_verificacao")},
        ),
        (
            "Governança",
            {
                "fields": (
                    "criado_por",
                    "criado_em",
                    "atualizado_por",
                    "atualizado_em",
                    "origem_cadastro",
                    "observacoes",
                ),
            },
        ),
    )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.criado_por = request.user
        obj.atualizado_por = request.user
        super().save_model(request, obj, form, change)


@admin.register(AtividadeCamera)
class AtividadeCameraAdmin(admin.ModelAdmin):
    list_display = (
        "camera", "tipo", "titulo", "responsavel", "ocorrida_em", "criado_por", "atualizado_em",
    )
    search_fields = (
        "camera__nome", "camera__patrimonio", "camera__ip", "titulo", "descricao", "responsavel",
    )
    list_filter = ("tipo", "ocorrida_em", "camera__terminal", "responsavel")
    autocomplete_fields = ("camera",)
    readonly_fields = ("criado_por", "criado_em", "atualizado_por", "atualizado_em")
    fieldsets = (
        ("Atividade", {"fields": ("camera", "tipo", "titulo", "descricao", "ocorrida_em", "responsavel")} ),
        ("Governança", {"fields": ("criado_por", "criado_em", "atualizado_por", "atualizado_em")} ),
    )

    def save_model(self, request, obj, form, change):
        if request.user.is_authenticated:
            if not change and obj.criado_por_id is None:
                obj.criado_por = request.user
            obj.atualizado_por = request.user
        super().save_model(request, obj, form, change)
