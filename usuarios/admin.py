from urllib.parse import unquote

from django import forms
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import GroupAdmin as DjangoGroupAdmin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.forms import AdminUserCreationForm, UserChangeForm
from django.contrib.auth.models import Group, Permission
from django.core.exceptions import PermissionDenied
from django.db.models import Exists, OuterRef

from .models import PerfilUsuario
from .admin_security import (
    ARGOS_OPERATIONAL_GROUP_NAMES,
    can_manage_user,
    is_argos_admin,
)


User = get_user_model()


class ArgosUserChangeForm(UserChangeForm):
    """Formulário sem campos capazes de conceder privilégios."""

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "is_active",
            "groups",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["groups"].queryset = Group.objects.filter(
            name__in=ARGOS_OPERATIONAL_GROUP_NAMES
        ).order_by("name")

    def clean_groups(self):
        grupos = self.cleaned_data["groups"]
        if grupos.exclude(name__in=ARGOS_OPERATIONAL_GROUP_NAMES).exists():
            raise forms.ValidationError(
                "Somente perfis operacionais allowlisted podem ser atribuídos."
            )
        return grupos

    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.is_staff = False
        usuario.is_superuser = False
        if commit:
            usuario.save()
            if hasattr(self, "save_m2m"):
                self.save_m2m()
        return usuario


class ArgosUserCreationForm(AdminUserCreationForm):
    """Formulário de criação que nasce sem qualquer privilégio elevado."""

    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.is_staff = False
        usuario.is_superuser = False
        if commit:
            usuario.save()
            if hasattr(self, "save_m2m"):
                self.save_m2m()
        return usuario


class ArgosUserAdmin(DjangoUserAdmin):
    """UserAdmin completo para superusers e restrito para Administrador ARGOS."""

    argos_change_fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Informações pessoais",
            {"fields": ("first_name", "last_name", "email")},
        ),
        ("Permissões operacionais", {"fields": ("is_active", "groups")}),
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        if not is_argos_admin(request.user):
            return queryset.none()

        through_groups = self.model.groups.through
        through_permissions = self.model.user_permissions.through
        groups_protegidos = through_groups.objects.filter(
            user_id=OuterRef("pk")
        ).exclude(group__name__in=ARGOS_OPERATIONAL_GROUP_NAMES)
        permissoes_diretas = through_permissions.objects.filter(
            user_id=OuterRef("pk")
        )
        return (
            queryset.filter(is_superuser=False, is_staff=False)
            .annotate(
                _argos_grupos_protegidos=Exists(groups_protegidos),
                _argos_permissoes_diretas=Exists(permissoes_diretas),
            )
            .filter(
                _argos_grupos_protegidos=False,
                _argos_permissoes_diretas=False,
            )
            .exclude(pk=request.user.pk)
        )

    def get_fieldsets(self, request, obj=None):
        if request.user.is_superuser or not is_argos_admin(request.user):
            return super().get_fieldsets(request, obj)
        if obj is None:
            return self.add_fieldsets
        return self.argos_change_fieldsets

    def get_form(self, request, obj=None, change=False, **kwargs):
        if not request.user.is_superuser and is_argos_admin(request.user):
            kwargs["form"] = (
                ArgosUserCreationForm if obj is None else ArgosUserChangeForm
            )
        return super().get_form(request, obj, change=change, **kwargs)

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        if (
            request is not None
            and not request.user.is_superuser
            and is_argos_admin(request.user)
        ):
            if db_field.name == "groups":
                kwargs["queryset"] = Group.objects.filter(
                    name__in=ARGOS_OPERATIONAL_GROUP_NAMES
                ).order_by("name")
            elif db_field.name == "user_permissions":
                kwargs["queryset"] = Permission.objects.none()
        return super().formfield_for_manytomany(
            db_field,
            request=request,
            **kwargs,
        )

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return super().has_add_permission(request)
        return is_argos_admin(request.user) and super().has_add_permission(request)

    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser:
            return super().has_view_permission(request, obj)
        if not is_argos_admin(request.user):
            return False
        if obj is not None and not can_manage_user(request.user, obj):
            return False
        return super().has_view_permission(request, obj)

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return super().has_change_permission(request, obj)
        if not is_argos_admin(request.user):
            return False
        if obj is not None and not can_manage_user(request.user, obj):
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return super().has_delete_permission(request, obj)
        return False

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser and is_argos_admin(request.user):
            obj.is_staff = False
            obj.is_superuser = False
        super().save_model(request, obj, form, change)

    def save_related(self, request, form, formsets, change):
        if request.user.is_superuser:
            super().save_related(request, form, formsets, change)
            return
        if not is_argos_admin(request.user):
            raise PermissionDenied

        grupos = form.cleaned_data.get("groups")
        if grupos is not None:
            if grupos.exclude(name__in=ARGOS_OPERATIONAL_GROUP_NAMES).exists():
                raise PermissionDenied
            form.instance.groups.set(grupos)

    def user_change_password(self, request, id, form_url=""):
        if not request.user.is_superuser:
            target = self.get_object(request, unquote(id))
            if target is None or not can_manage_user(request.user, target):
                raise PermissionDenied
        return super().user_change_password(request, id, form_url)


class ArgosGroupAdmin(DjangoGroupAdmin):
    """GroupAdmin disponível integralmente apenas para superusers."""

    def has_module_permission(self, request):
        return request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser and super().has_view_permission(request, obj)

    def has_add_permission(self, request):
        return request.user.is_superuser and super().has_add_permission(request)

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser and super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser and super().has_delete_permission(request, obj)


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


for modelo in (User, Group):
    try:
        admin.site.unregister(modelo)
    except admin.sites.NotRegistered:
        pass

admin.site.register(User, ArgosUserAdmin)
admin.site.register(Group, ArgosGroupAdmin)
