from django.urls import path
from . import views
app_name = "usuarios"
urlpatterns = [path("login/", views.ArgosLoginView.as_view(), name="login"), path("logout/", views.logout_argos, name="logout"), path("perfil/", views.perfil, name="perfil"), path("perfil/editar/", views.editar_perfil, name="editar_perfil"), path("perfil/alterar-senha/", views.alterar_senha, name="alterar_senha")]
