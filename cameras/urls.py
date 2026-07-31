from django.urls import path

from . import views


app_name = "cameras"

urlpatterns = [
    path("", views.lista_cameras, name="lista"),
    path("nova/", views.criar_camera, name="criar"),
    path("<int:pk>/editar/", views.editar_camera, name="editar"),
    path("<int:pk>/alternar-atividade/", views.alternar_atividade_camera, name="alternar_atividade"),
    path("atividades/<int:pk>/editar/", views.editar_atividade_camera, name="editar_atividade"),
    path("<int:camera_pk>/atividades/nova/", views.criar_atividade_camera, name="criar_atividade"),
    path("<int:camera_pk>/atividades/", views.lista_atividades_camera, name="lista_atividades"),
    path("<int:pk>/", views.detalhe_camera, name="detalhe"),
]
