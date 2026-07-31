from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import resolve, reverse

from .models import Camera, EventoAuditoria
from .views import detalhe_evento, lista_eventos


class RotasEventosTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="rotas", password="senha")
        self.user.user_permissions.add(Permission.objects.get(codename="consultar_eventos"))
        self.camera = Camera.objects.create(
            nome="CAM-ROTAS", fabricante="Axis", modelo="M",
            ip="10.23.0.1", mascara_subrede="255.255.255.0", vlan=100,
        )
        self.evento = EventoAuditoria.objects.create(
            categoria=EventoAuditoria.Categoria.CAMERA,
            codigo="camera.criada", resumo="Câmera criada", camera=self.camera,
        )

    def test_reverse_lista_eventos_retorna_rota_raiz(self):
        self.assertEqual(reverse("eventos:lista"), "/eventos/")

    def test_reverse_detalhe_evento_retorna_rota_raiz(self):
        self.assertEqual(reverse("eventos:detalhe", kwargs={"pk": self.evento.pk}), f"/eventos/{self.evento.pk}/")

    def test_reverse_eventos_camera_permanece_sob_cameras(self):
        self.assertEqual(reverse("cameras:eventos_camera", kwargs={"pk": self.camera.pk}), f"/cameras/{self.camera.pk}/eventos/")

    def test_resolve_lista_eventos_aponta_para_view_correta(self):
        self.assertIs(resolve("/eventos/").func, lista_eventos)

    def test_resolve_detalhe_evento_aponta_para_view_correta(self):
        self.assertIs(resolve(f"/eventos/{self.evento.pk}/").func, detalhe_evento)

    def test_rota_geral_antiga_retorna_404(self):
        self.assertEqual(self.client.get("/cameras/eventos/").status_code, 404)

    def test_rota_detalhe_antiga_retorna_404(self):
        self.assertEqual(self.client.get(f"/cameras/eventos/{self.evento.pk}/").status_code, 404)

    def test_links_principais_usam_rota_canonica_de_eventos(self):
        self.client.force_login(self.user)
        response = self.client.get("/")
        self.assertContains(response, 'href="/eventos/"')
        self.assertNotContains(response, 'href="/cameras/eventos/"')