from django.urls import path

from . import views


app_name = "cameras"

urlpatterns = [
    path("", views.lista_cameras, name="lista"),
    path("nova/", views.criar_camera, name="criar"),
    path("substituicoes/", views.lista_substituicoes, name="lista_substituicoes"),
    path("substituicoes/<int:pk>/", views.detalhe_substituicao, name="detalhe_substituicao"),
    path("<int:pk>/editar/", views.editar_camera, name="editar"),
    path("<int:pk>/desativar/", views.desativar_camera_view, name="desativar"),
    path("<int:pk>/reativar/", views.reativar_camera_view, name="reativar"),
    path("<int:pk>/alterar-situacao/", views.alterar_situacao_camera_view, name="alterar_situacao"),
    path("<int:pk>/substituir/", views.substituir_camera_view, name="substituir"),
    path("<int:pk>/eventos/", views.eventos_camera, name="eventos_camera"),
    path("<int:pk>/monitoramento/historico/", views.historico_monitoramento, name="historico_monitoramento"),
    path("<int:pk>/imagens/upload/", views.upload_imagem_camera, name="upload_imagem"),
    path("atividades/<int:pk>/editar/", views.editar_atividade_camera, name="editar_atividade"),
    path("<int:camera_pk>/atividades/nova/", views.criar_atividade_camera, name="criar_atividade"),
    path(
        "<int:camera_pk>/substituicoes/",
        views.lista_substituicoes_camera,
        name="lista_substituicoes_camera",
    ),
    path("<int:camera_pk>/atividades/", views.lista_atividades_camera, name="lista_atividades"),
    path("<int:pk>/", views.detalhe_camera, name="detalhe"),
]
