from datetime import timedelta

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Camera, EventoAuditoria


class AuditoriaViewsTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="consulta", password="senha")
        self.permission = Permission.objects.get(codename="consultar_eventos")
        self.view_camera = Permission.objects.get(codename="view_camera")
        self.user.user_permissions.add(self.view_camera)
        self.camera = Camera.objects.create(nome="CAM-VIEW", fabricante="Axis", modelo="M", ip="10.21.0.1", mascara_subrede="255.255.255.0", vlan=100)
        self.evento = EventoAuditoria.objects.create(categoria="CAMERA", codigo="camera.criada", resumo="Câmera criada", camera=self.camera, usuario=self.user, usuario_username="consulta", entidade_descricao="CAM-VIEW", origem="WEB")

    def autenticar(self, permissao=True):
        if permissao: self.user.user_permissions.add(self.permission)
        self.client.force_login(self.user)

    def test_01_anonimo_redirecionado(self):
        self.assertEqual(self.client.get(reverse("eventos:lista")).status_code, 302)

    def test_02_sem_permissao_recebe_403(self):
        self.autenticar(False)
        self.assertEqual(self.client.get(reverse("eventos:lista")).status_code, 403)

    def test_03_com_permissao_recebe_200(self):
        self.autenticar()
        self.assertEqual(self.client.get(reverse("eventos:lista")).status_code, 200)

    def test_04_template_da_lista(self):
        self.autenticar(); response = self.client.get(reverse("eventos:lista"))
        self.assertTemplateUsed(response, "cameras/eventos/lista.html")

    def test_05_exibe_evento(self):
        self.autenticar()
        self.assertContains(self.client.get(reverse("eventos:lista")), "camera.criada")

    def test_06_filtro_textual(self):
        EventoAuditoria.objects.create(categoria="SISTEMA", codigo="outro", resumo="Nada")
        self.autenticar(); response = self.client.get(reverse("eventos:lista"), {"q": "CAM-VIEW"})
        self.assertEqual(response.context["total_eventos"], 1)

    def test_07_filtro_categoria(self):
        self.autenticar(); response = self.client.get(reverse("eventos:lista"), {"categoria": "CAMERA"})
        self.assertEqual(response.context["total_eventos"], 1)

    def test_08_filtro_origem(self):
        self.autenticar(); response = self.client.get(reverse("eventos:lista"), {"origem": "ADMIN"})
        self.assertEqual(response.context["total_eventos"], 0)

    def test_09_filtro_periodo(self):
        self.autenticar(); hoje = timezone.localdate().isoformat()
        self.assertEqual(self.client.get(reverse("eventos:lista"), {"data_inicial": hoje, "data_final": hoje}).context["total_eventos"], 1)

    def test_10_periodo_invalido(self):
        self.autenticar(); response = self.client.get(reverse("eventos:lista"), {"data_inicial": "invalida"})
        self.assertTrue(response.context["periodo_invalido"])

    def test_11_paginacao_de_50(self):
        for indice in range(51):
            EventoAuditoria.objects.create(categoria="SISTEMA", codigo=f"sistema.{indice}", resumo="Teste")
        self.autenticar(); response = self.client.get(reverse("eventos:lista"))
        self.assertEqual(len(response.context["eventos"]), 50)
        self.assertEqual(response.context["paginator"].num_pages, 2)

    def test_12_detalhe_evento(self):
        self.autenticar()
        self.assertEqual(self.client.get(reverse("eventos:detalhe", kwargs={"pk": self.evento.pk})).status_code, 200)

    def test_13_detalhe_sem_acoes_de_mutacao(self):
        self.autenticar(); response = self.client.get(reverse("eventos:detalhe", kwargs={"pk": self.evento.pk}))
        self.assertNotContains(response, "Excluir evento")
        self.assertNotContains(response, "Editar evento")

    def test_14_historico_isola_camera(self):
        outra = Camera.objects.create(nome="CAM-OUTRA", fabricante="Axis", modelo="M", ip="10.21.0.2", mascara_subrede="255.255.255.0", vlan=101)
        EventoAuditoria.objects.create(categoria="CAMERA", codigo="camera.outra", resumo="Outra", camera=outra)
        self.autenticar(); response = self.client.get(reverse("cameras:eventos_camera", args=[self.camera.pk]))
        self.assertContains(response, "camera.criada")
        self.assertNotContains(response, "camera.outra")

    def test_15_detalhe_camera_limita_dez_eventos(self):
        for indice in range(12):
            EventoAuditoria.objects.create(categoria="CAMERA", codigo=f"camera.{indice}", resumo="Teste", camera=self.camera)
        self.autenticar(); response = self.client.get(reverse("cameras:detalhe", args=[self.camera.pk]))
        self.assertEqual(len(response.context["eventos_auditoria"]), 10)

    def test_16_detalhe_camera_oculta_sem_permissao(self):
        self.autenticar(False); response = self.client.get(reverse("cameras:detalhe", args=[self.camera.pk]))
        self.assertNotIn("eventos_auditoria", response.context)
        self.assertNotContains(response, "Eventos de auditoria")