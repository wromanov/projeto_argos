from django.urls import path
from . import views
app_name = "usuarios"
urlpatterns = [path("login/", views.ArgosLoginView.as_view(), name="login"), path("logout/", views.logout_argos, name="logout")]
