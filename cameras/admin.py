from django.contrib import admin

from .auditoria import CAMPOS_ATIVIDADE_AUDITAVEIS, CAMPOS_CAMERA_AUDITAVEIS, calcular_alteracoes, registrar_evento, valores_iniciais
from .models import AtividadeCamera, Camera, EventoAuditoria, SubstituicaoCamera


@admin.register(Camera)
class CameraAdmin(admin.ModelAdmin):
    list_display = ("nome", "patrimonio", "situacao_operacional", "cadastro_completo_admin", "status", "terminal", "ip", "vlan", "fabricante", "modelo", "atualizado_em")
    search_fields = ("nome", "patrimonio", "ip", "serial", "mac", "fabricante", "modelo", "terminal", "setor", "ambiente")
    list_filter = ("situacao_operacional", "status", "tipo", "terminal", "fabricante", "vlan", "farm", "origem_cadastro")
    readonly_fields = ("situacao_operacional", "motivo_desativacao", "desativada_em", "desativada_por", "criado_por", "criado_em", "atualizado_por", "atualizado_em")
    fieldsets = (
        ("Identificação", {"fields": ("patrimonio", "nome", "fabricante", "modelo", "serial", "mac", "tipo")}),
        ("Situação operacional", {"fields": ("situacao_operacional", "motivo_desativacao", "desativada_em", "desativada_por")}),
        ("Localização", {"fields": ("terminal", "pavimento", "setor", "ambiente", "descricao_detalhada", "ponto_referencia")}),
        ("Rede", {"fields": ("ip", "mascara_subrede", "gateway", "vlan")}),
        ("Gravação", {"fields": ("farm", "retencao_esperada_dias", "codec")}),
        ("Monitoramento", {"fields": ("status", "status_em", "ultima_verificacao")}),
        ("Governança", {"fields": ("criado_por", "criado_em", "atualizado_por", "atualizado_em", "origem_cadastro", "observacoes")}),
    )

    @admin.display(boolean=True, description="Cadastro completo")
    def cadastro_completo_admin(self, obj):
        return obj.cadastro_completo

    def save_model(self, request, obj, form, change):
        anterior = Camera.objects.get(pk=obj.pk) if change else None
        if not change: obj.criado_por = request.user
        obj.atualizado_por = request.user
        super().save_model(request, obj, form, change)
        alteracoes = calcular_alteracoes(anterior, obj, CAMPOS_CAMERA_AUDITAVEIS) if anterior else valores_iniciais(obj, CAMPOS_CAMERA_AUDITAVEIS)
        if alteracoes:
            registrar_evento(codigo="camera.atualizada" if change else "camera.criada", resumo="Câmera atualizada pelo Admin" if change else "Câmera criada pelo Admin", categoria=EventoAuditoria.Categoria.CAMERA, request=request, camera=obj, entidade=obj, alteracoes=alteracoes, origem=EventoAuditoria.Origem.ADMIN)

    def has_delete_permission(self, request, obj=None): return False


@admin.register(AtividadeCamera)
class AtividadeCameraAdmin(admin.ModelAdmin):
    list_display = ("camera", "tipo", "titulo", "responsavel", "ocorrida_em", "criado_por", "atualizado_em")
    search_fields = ("camera__nome", "camera__patrimonio", "camera__ip", "titulo", "descricao", "responsavel")
    list_filter = ("tipo", "ocorrida_em", "camera__terminal", "responsavel")
    autocomplete_fields = ("camera",)
    readonly_fields = ("criado_por", "criado_em", "atualizado_por", "atualizado_em")
    fieldsets = (
        ("Atividade", {"fields": ("camera", "tipo", "titulo", "descricao", "ocorrida_em", "responsavel")}),
        ("Governança", {"fields": ("criado_por", "criado_em", "atualizado_por", "atualizado_em")}),
    )

    def save_model(self, request, obj, form, change):
        anterior = AtividadeCamera.objects.get(pk=obj.pk) if change else None
        if request.user.is_authenticated:
            if not change and obj.criado_por_id is None: obj.criado_por = request.user
            obj.atualizado_por = request.user
        super().save_model(request, obj, form, change)
        alteracoes = calcular_alteracoes(anterior, obj, CAMPOS_ATIVIDADE_AUDITAVEIS) if anterior else valores_iniciais(obj, CAMPOS_ATIVIDADE_AUDITAVEIS)
        if alteracoes:
            registrar_evento(codigo="atividade.atualizada" if change else "atividade.criada", resumo="Atividade atualizada pelo Admin" if change else "Atividade criada pelo Admin", categoria=EventoAuditoria.Categoria.ATIVIDADE, request=request, camera=obj.camera, entidade=obj, alteracoes=alteracoes, origem=EventoAuditoria.Origem.ADMIN)

    def has_delete_permission(self, request, obj=None): return False


@admin.register(EventoAuditoria)
class EventoAuditoriaAdmin(admin.ModelAdmin):
    list_display = ("ocorrido_em", "categoria", "codigo", "resumo", "usuario_username", "camera", "origem")
    search_fields = ("codigo", "resumo", "usuario_username", "usuario_nome", "entidade_descricao", "camera__nome")
    list_filter = ("categoria", "origem", "ocorrido_em")
    date_hierarchy = "ocorrido_em"
    readonly_fields = tuple(field.name for field in EventoAuditoria._meta.fields)
    def has_add_permission(self, request): return False
    def has_change_permission(self, request, obj=None): return request.user.has_perm("cameras.view_eventoauditoria")
    def has_delete_permission(self, request, obj=None): return False


@admin.register(SubstituicaoCamera)
class SubstituicaoCameraAdmin(admin.ModelAdmin):
    list_display = ("ocorrida_em", "camera_anterior", "camera_substituta", "nome_operacional", "registrado_por_username")
    search_fields = ("camera_anterior__nome", "camera_anterior__patrimonio", "camera_anterior__serial", "camera_substituta__nome", "camera_substituta__patrimonio", "camera_substituta__serial", "nome_operacional", "nome_anterior_substituta", "motivo", "registrado_por_username")
    list_filter = ("ocorrida_em",)
    date_hierarchy = "ocorrida_em"
    readonly_fields = tuple(field.name for field in SubstituicaoCamera._meta.fields)
    def has_add_permission(self, request): return False
    def has_change_permission(self, request, obj=None): return False
    def has_delete_permission(self, request, obj=None): return False
