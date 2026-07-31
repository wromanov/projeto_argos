from django.contrib import messages
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.decorators import login_not_required, login_required
from django.contrib.auth.models import Permission
from django.contrib.auth.views import LoginView
from django.db import transaction
from django.db.models import Q
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.http import require_POST

from cameras.auditoria import CAMPOS_PERFIL_AUDITAVEIS, registrar_evento
from cameras.models import EventoAuditoria
from .forms import ArgosAuthenticationForm, ArgosPasswordChangeForm, DadosPessoaisForm, PerfilProprioForm
from .models import PerfilUsuario


@method_decorator(login_not_required, name="dispatch")
class ArgosLoginView(LoginView):
    template_name = "usuarios/login.html"
    authentication_form = ArgosAuthenticationForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        response = super().form_valid(form)
        registrar_evento(codigo="autenticacao.login_sucesso", resumo="Login realizado com sucesso", categoria=EventoAuditoria.Categoria.AUTENTICACAO, request=self.request, usuario=form.get_user(), entidade=form.get_user())
        return response

    def form_invalid(self, form):
        registrar_evento(codigo="autenticacao.login_falha", resumo="Tentativa de login não autorizada", categoria=EventoAuditoria.Categoria.AUTENTICACAO, request=self.request)
        return super().form_invalid(form)


@require_POST
@never_cache
def logout_argos(request):
    registrar_evento(codigo="autenticacao.logout", resumo="Logout realizado", categoria=EventoAuditoria.Categoria.AUTENTICACAO, request=request, entidade=request.user)
    logout(request)
    return redirect("usuarios:login")


@login_required
@never_cache
def perfil(request):
    perfil_usuario, _ = PerfilUsuario.objects.get_or_create(usuario=request.user)
    grupos = request.user.groups.order_by("name")
    permissoes = Permission.objects.select_related("content_type").order_by("content_type__app_label", "name") if request.user.is_superuser else Permission.objects.filter(Q(user=request.user) | Q(group__user=request.user)).select_related("content_type").distinct().order_by("content_type__app_label", "name")
    return render(request, "usuarios/perfil.html", {"perfil_usuario": perfil_usuario, "grupos": grupos, "permissoes": permissoes})


@login_required
@never_cache
@transaction.atomic
def editar_perfil(request):
    perfil_usuario, _ = PerfilUsuario.objects.get_or_create(usuario=request.user)
    anteriores = {campo: getattr(request.user, campo, None) for campo in ("first_name", "last_name", "email")}
    anteriores.update({campo: getattr(perfil_usuario, campo, None) for campo in ("telefone", "ramal")})
    dados_form = DadosPessoaisForm(request.POST or None, instance=request.user); perfil_form = PerfilProprioForm(request.POST or None, instance=perfil_usuario)
    if request.method == "POST" and dados_form.is_valid() and perfil_form.is_valid():
        usuario = dados_form.save(); perfil_atual = perfil_form.save()
        atuais = {campo: getattr(usuario, campo, None) for campo in ("first_name", "last_name", "email")}
        atuais.update({campo: getattr(perfil_atual, campo, None) for campo in ("telefone", "ramal")})
        alteracoes = {campo: {"anterior": anteriores[campo], "atual": atuais[campo]} for campo in CAMPOS_PERFIL_AUDITAVEIS if anteriores.get(campo) != atuais.get(campo)}
        if alteracoes: registrar_evento(codigo="perfil.atualizado", resumo="Perfil atualizado", categoria=EventoAuditoria.Categoria.PERFIL, request=request, entidade=usuario, alteracoes=alteracoes)
        messages.success(request, "Perfil atualizado com sucesso.")
        return redirect("usuarios:perfil")
    return render(request, "usuarios/editar_perfil.html", {"dados_form": dados_form, "perfil_form": perfil_form, "perfil_usuario": perfil_usuario})


@sensitive_post_parameters("old_password", "new_password1", "new_password2")
@login_required
@never_cache
def alterar_senha(request):
    form = ArgosPasswordChangeForm(request.user, request.POST or None)
    if request.method == "POST" and form.is_valid():
        usuario = form.save(); update_session_auth_hash(request, usuario)
        registrar_evento(codigo="perfil.senha_alterada", resumo="Senha alterada", categoria=EventoAuditoria.Categoria.PERFIL, request=request, entidade=usuario)
        messages.success(request, "Senha alterada com sucesso.")
        return redirect("usuarios:perfil")
    return render(request, "usuarios/alterar_senha.html", {"form": form})