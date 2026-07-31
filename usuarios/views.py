from django.contrib import messages
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.decorators import login_not_required, login_required
from django.contrib.auth.models import Permission
from django.contrib.auth.views import LoginView
from django.db import transaction
from django.db.models import Q
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from .forms import ArgosAuthenticationForm, ArgosPasswordChangeForm, DadosPessoaisForm, PerfilProprioForm
from .models import PerfilUsuario


@method_decorator(login_not_required, name="dispatch")
class ArgosLoginView(LoginView):
    template_name = "usuarios/login.html"
    authentication_form = ArgosAuthenticationForm
    redirect_authenticated_user = True


@require_POST
def logout_argos(request):
    logout(request)
    return redirect("usuarios:login")


@login_required
def perfil(request):
    perfil_usuario, _ = PerfilUsuario.objects.get_or_create(usuario=request.user)
    grupos = request.user.groups.order_by("name")
    if request.user.is_superuser:
        permissoes = Permission.objects.select_related("content_type").order_by("content_type__app_label", "name")
    else:
        permissoes = Permission.objects.filter(Q(user=request.user) | Q(group__user=request.user)).select_related("content_type").distinct().order_by("content_type__app_label", "name")
    return render(request, "usuarios/perfil.html", {"perfil_usuario": perfil_usuario, "grupos": grupos, "permissoes": permissoes})


@login_required
@transaction.atomic
def editar_perfil(request):
    perfil_usuario, _ = PerfilUsuario.objects.get_or_create(usuario=request.user)
    if request.method == "POST":
        dados_form = DadosPessoaisForm(request.POST, instance=request.user)
        perfil_form = PerfilProprioForm(request.POST, instance=perfil_usuario)
        if dados_form.is_valid() and perfil_form.is_valid():
            dados_form.save(); perfil_form.save(); messages.success(request, "Perfil atualizado com sucesso.")
            return redirect("usuarios:perfil")
    else:
        dados_form = DadosPessoaisForm(instance=request.user); perfil_form = PerfilProprioForm(instance=perfil_usuario)
    return render(request, "usuarios/editar_perfil.html", {"dados_form": dados_form, "perfil_form": perfil_form, "perfil_usuario": perfil_usuario})


@login_required
def alterar_senha(request):
    form = ArgosPasswordChangeForm(request.user, request.POST or None)
    if request.method == "POST" and form.is_valid():
        usuario = form.save(); update_session_auth_hash(request, usuario); messages.success(request, "Senha alterada com sucesso.")
        return redirect("usuarios:perfil")
    return render(request, "usuarios/alterar_senha.html", {"form": form})
