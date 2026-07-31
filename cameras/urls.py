from django.urls import path

from . import views


app_name = "cameras"

urlpatterns = [
    path("", views.lista_cameras, name="lista"),
    path("<int:pk>/", views.detalhe_camera, name="detalhe"),
]
