from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Camera


class ListaCamerasFrontendTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_superuser(username="frontend-cameras", password="senha-forte", email="")
        self.client.force_login(self.user)
        self.camera = self.criar_camera(1, nome="CAM-FRONTEND", status=Camera.StatusCamera.ONLINE)

    def criar_camera(self, indice, **atributos):
        valores = {
            "nome": f"CAM-{indice:03d}",
            "patrimonio": f"PAT-{indice:03d}",
            "ip": f"10.10.0.{indice}",
            "mascara_subrede": "255.255.255.0",
            "vlan": 100,
            "fabricante": "Axis",
            "modelo": "Modelo de teste",
            "serial": f"SERIAL-{indice:03d}",
            "mac": f"AA:BB:CC:DD:EE:{indice:02X}",
            "tipo": Camera.TipoCamera.DOME,
            "situacao_operacional": Camera.SituacaoOperacional.PRODUCAO,
            "terminal": "TPS1",
            "pavimento": "Terreo",
            "setor": "Seguranca",
            "ambiente": "Sala de monitoramento",
            "gateway": "10.10.0.254",
            "farm": "Farm A",
            "retencao_esperada_dias": 30,
            "codec": "H.264",        }
        valores.update(atributos)
        return Camera.objects.create(**valores)

    def test_lista_camera_possui_filtros_e_tabela_acessiveis(self):
        response = self.client.get(reverse("cameras:lista"))
        self.assertContains(response, 'role="search"')
        self.assertContains(response, 'aria-label="Filtros do inventário de câmeras"')
        self.assertContains(response, 'for="id_situacao_operacional"')
        self.assertContains(response, 'role="region" aria-label="Câmeras encontradas" tabindex="0"')
        self.assertContains(response, "Relação de câmeras encontradas no inventário")
        self.assertContains(response, 'scope="col"')

    def test_lista_camera_exibe_badges_textuais_e_estado_vazio(self):
        incompleta = self.criar_camera(2, nome="CAM-INCOMPLETA", ip="", status=Camera.StatusCamera.OFFLINE)
        response = self.client.get(reverse("cameras:lista"))
        self.assertContains(response, "Produção")
        self.assertContains(response, "Online")
        self.assertContains(response, "Cadastro completo")
        self.assertContains(response, "Cadastro incompleto")
        self.assertContains(response, 'badge badge--producao')
        self.assertContains(response, 'badge badge--online')
        self.assertContains(response, 'badge badge--incompleto')
        vazio = self.client.get(reverse("cameras:lista"), {"q": "sem-correspondencia"})
        self.assertContains(vazio, "Nenhuma câmera encontrada")
        self.assertContains(vazio, "Não há câmeras correspondentes aos filtros informados.")
        self.assertContains(vazio, "Limpar filtros")

    def test_paginacao_camera_preserva_filtros(self):
        for indice in range(2, 22):
            self.criar_camera(indice, nome=f"CAM-PAG-{indice:03d}")
        response = self.client.get(reverse("cameras:lista"), {"q": "CAM", "situacao_operacional": "PRODUCAO", "completude": "COMPLETO"})
        self.assertTemplateUsed(response, "components/paginacao.html")
        self.assertContains(response, "Próxima")
        self.assertContains(response, "q=CAM")
        self.assertContains(response, "situacao_operacional=PRODUCAO")
        self.assertContains(response, "completude=COMPLETO")
        self.assertContains(response, 'aria-current="page"')