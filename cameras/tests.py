from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import Camera


class ListaCamerasTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_superuser(username="teste-lista", password="senha", email="")
        self.client.force_login(self.user)
        self.online = self.criar_camera(
            1,
            nome="CAM-ALFA",
            patrimonio="PAT-ALFA",
            status="ONLINE",
            situacao_operacional=Camera.SituacaoOperacional.PRODUCAO,
            terminal="TPS1",
            tipo="DOME",
            fabricante="Axis",
            vlan=100,
            farm="FARM-A",
        )
        self.offline = self.criar_camera(
            2,
            nome="CAM-BRAVO",
            patrimonio="PAT-BRAVO",
            status="OFFLINE",
            situacao_operacional=Camera.SituacaoOperacional.DESATIVADA,
            terminal="TPS2",
            tipo="BULLET",
            fabricante="Hikvision",
            vlan=200,
            farm="FARM-B",
        )
        self.nao_verificada = self.criar_camera(
            3,
            nome="CAM-CHARLIE",
            patrimonio="PAT-CHARLIE",
            status=None,
            situacao_operacional=Camera.SituacaoOperacional.PRODUCAO,
            terminal="TPS2",
            tipo="FISHEYE",
            fabricante="Axis",
            vlan=210,
            farm="FARM-B",
        )

    def criar_camera(self, indice, **atributos):
        valores = {
            "nome": f"CAM-{indice:03d}",
            "patrimonio": f"PAT-{indice:03d}",
            "ip": f"10.0.0.{indice}",
            "mascara_subrede": "255.255.255.0",
            "vlan": 100,
            "fabricante": "Axis",
            "modelo": "Modelo padrão",
            "serial": f"SERIAL-{indice:03d}",
            "mac": f"AA:BB:CC:DD:EE:{indice:02X}",
            "tipo": "DOME",
            "situacao_operacional": Camera.SituacaoOperacional.PRODUCAO,
            "terminal": "TPS1",
            "farm": "FARM-A",
        }
        valores.update(atributos)
        return Camera.objects.create(**valores)

    def buscar(self, **parametros):
        return self.client.get("/cameras/", parametros)

    def nomes_da_pagina(self, response):
        return [camera.nome for camera in response.context["cameras"]]

    def test_listagem_sem_filtros_retorna_cameras(self):
        response = self.buscar()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["total_resultados"], 3)

    def test_pesquisa_por_nome(self):
        response = self.buscar(q="BRAVO")
        self.assertEqual(self.nomes_da_pagina(response), ["CAM-BRAVO"])

    def test_pesquisa_parcial_sem_diferenciar_maiusculas(self):
        response = self.buscar(q="cam-al")
        self.assertEqual(self.nomes_da_pagina(response), ["CAM-ALFA"])

    def test_pesquisa_por_patrimonio(self):
        response = self.buscar(q="PAT-CHAR")
        self.assertEqual(self.nomes_da_pagina(response), ["CAM-CHARLIE"])

    def test_filtro_por_status_online(self):
        self.assertEqual(self.nomes_da_pagina(self.buscar(status="ONLINE")), ["CAM-ALFA"])

    def test_filtro_por_status_offline(self):
        self.assertEqual(self.nomes_da_pagina(self.buscar(status="OFFLINE")), ["CAM-BRAVO"])

    def test_filtro_por_status_nao_verificado(self):
        self.assertEqual(self.nomes_da_pagina(self.buscar(status="NAO_VERIFICADO")), ["CAM-CHARLIE"])

    def test_filtro_por_camera_em_producao(self):
        self.assertEqual(self.nomes_da_pagina(self.buscar(situacao_operacional="PRODUCAO")), ["CAM-ALFA", "CAM-CHARLIE"])

    def test_filtro_por_camera_desativada(self):
        self.assertEqual(self.nomes_da_pagina(self.buscar(situacao_operacional="DESATIVADA")), ["CAM-BRAVO"])

    def test_filtro_por_terminal(self):
        self.assertEqual(self.nomes_da_pagina(self.buscar(terminal="TPS2")), ["CAM-BRAVO", "CAM-CHARLIE"])

    def test_filtro_por_tipo(self):
        self.assertEqual(self.nomes_da_pagina(self.buscar(tipo="BULLET")), ["CAM-BRAVO"])

    def test_filtro_por_fabricante(self):
        self.assertEqual(self.nomes_da_pagina(self.buscar(fabricante="Hikvision")), ["CAM-BRAVO"])

    def test_filtro_por_vlan(self):
        self.assertEqual(self.nomes_da_pagina(self.buscar(vlan="210")), ["CAM-CHARLIE"])

    def test_filtro_por_farm(self):
        self.assertEqual(self.nomes_da_pagina(self.buscar(farm="FARM-A")), ["CAM-ALFA"])

    def test_combinacao_de_pesquisa_e_filtros(self):
        response = self.buscar(q="CAM", terminal="TPS2", situacao_operacional="PRODUCAO", fabricante="Axis")
        self.assertEqual(self.nomes_da_pagina(response), ["CAM-CHARLIE"])

    def test_multifiltro_status_combina_valores_com_or(self):
        response = self.buscar(status=["ONLINE", "OFFLINE"])
        self.assertEqual(self.nomes_da_pagina(response), ["CAM-ALFA", "CAM-BRAVO"])

    def test_multifiltro_situacao_combina_valores_com_or(self):
        response = self.buscar(situacao_operacional=["PRODUCAO", "DESATIVADA"])
        self.assertEqual(self.nomes_da_pagina(response), ["CAM-ALFA", "CAM-BRAVO", "CAM-CHARLIE"])

    def test_multifiltro_terminal_combina_valores_com_or(self):
        response = self.buscar(terminal=["TPS1", "TPS2"])
        self.assertEqual(self.nomes_da_pagina(response), ["CAM-ALFA", "CAM-BRAVO", "CAM-CHARLIE"])

    def test_multifiltro_combina_categorias_com_and(self):
        response = self.buscar(situacao_operacional=["PRODUCAO"], terminal=["TPS2"], fabricante=["Axis"])
        self.assertEqual(self.nomes_da_pagina(response), ["CAM-CHARLIE"])

    def test_multifiltro_enum_invalido_preserva_valor_valido(self):
        response = self.buscar(status=["INVALIDO", "ONLINE"])
        self.assertEqual(self.nomes_da_pagina(response), ["CAM-ALFA"])
        self.assertEqual(response.context["status_selecionados"], ["ONLINE"])

    def test_multifiltro_expoe_contexto_plural_e_legado(self):
        response = self.buscar(status=["ONLINE", "OFFLINE"])
        self.assertEqual(response.context["status_selecionados"], ["ONLINE", "OFFLINE"])
        self.assertEqual(response.context["status_selecionado"], "ONLINE")

    def test_filtros_ativos_expoem_um_chip_por_valor(self):
        response = self.buscar(
            q="CAM",
            status=["ONLINE", "OFFLINE"],
            situacao_operacional=["PRODUCAO"],
            tipo=["DOME"],
        )

        self.assertEqual(
            response.context["filtros_ativos"],
            [
                {
                    "nome": "q",
                    "valor": "CAM",
                    "grupo": "Pesquisa",
                    "rotulo": "CAM",
                },
                {
                    "nome": "status",
                    "valor": "ONLINE",
                    "grupo": "Status técnico",
                    "rotulo": "Online",
                },
                {
                    "nome": "status",
                    "valor": "OFFLINE",
                    "grupo": "Status técnico",
                    "rotulo": "Offline",
                },
                {
                    "nome": "situacao_operacional",
                    "valor": "PRODUCAO",
                    "grupo": "Situação operacional",
                    "rotulo": "Produção",
                },
                {
                    "nome": "tipo",
                    "valor": "DOME",
                    "grupo": "Tipo",
                    "rotulo": "Dome",
                },
            ],
        )

    def test_ordenacao_por_nome(self):
        response = self.buscar(ordenacao="-nome")
        self.assertEqual(self.nomes_da_pagina(response), ["CAM-CHARLIE", "CAM-BRAVO", "CAM-ALFA"])

    def test_ordenacao_invalida_usa_padrao(self):
        response = self.buscar(ordenacao="campo_invalido")
        self.assertEqual(response.context["ordenacao"], "nome")
        self.assertEqual(self.nomes_da_pagina(response), ["CAM-ALFA", "CAM-BRAVO", "CAM-CHARLIE"])

    def test_paginacao_com_mais_de_vinte_registros(self):
        for indice in range(4, 25):
            self.criar_camera(indice)
        primeira_pagina = self.buscar()
        segunda_pagina = self.buscar(page="2")
        self.assertEqual(len(primeira_pagina.context["cameras"]), 20)
        self.assertEqual(len(segunda_pagina.context["cameras"]), 4)
        self.assertTrue(segunda_pagina.context["page_obj"].has_previous())
        pagina_com_filtros = self.buscar(q="CAM", terminal="TPS1", ordenacao="-nome")
        self.assertContains(
            pagina_com_filtros,
            "?q=CAM&amp;terminal=TPS1&amp;ordenacao=-nome&amp;page=2",
        )

    def test_pagina_invalida_nao_gera_erro(self):
        response = self.buscar(page="invalida")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["page_obj"].number, 1)

    def test_contador_representa_queryset_filtrado(self):
        response = self.buscar(terminal="TPS2")
        self.assertEqual(response.context["total_resultados"], 2)
        self.assertContains(response, '<strong>2</strong><span>câmeras</span>')

    def test_estado_sem_resultados(self):
        response = self.buscar(q="inexistente")
        self.assertContains(response, "Nenhuma câmera encontrada")
        self.assertTrue(response.context["possui_cameras_cadastradas"])

    def test_estado_sem_cameras_cadastradas(self):
        Camera.objects.all().delete()
        response = self.buscar()
        self.assertContains(response, "Nenhuma câmera cadastrada")
        self.assertFalse(response.context["possui_cameras_cadastradas"])
