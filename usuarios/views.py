from django.contrib.auth import logout
from django.contrib.auth.decorators import login_not_required
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST

from .forms import ArgosAuthenticationForm


@method_decorator(login_not_required, name="dispatch")
class ArgosLoginView(LoginView):
    template_name = "usuarios/login.html"
    authentication_form = ArgosAuthenticationForm
    redirect_authenticated_user = True


@require_POST
def logout_argos(request):
    logout(request)
    return redirect("usuarios:login")
