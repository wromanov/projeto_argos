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
            "fabricante": "AXIS",
            "modelo": "MODELO DE TESTE",
            "serial": f"SERIAL-{indice:03d}",
            "mac": f"AA:BB:CC:DD:EE:{indice:02X}",
            "tipo": Camera.TipoCamera.DOME,
            "situacao_operacional": Camera.SituacaoOperacional.PRODUCAO,
            "terminal": "TPS1",
            "pavimento": "Terreo",
            "setor": "Seguranca",
            "ambiente": "SALA DE MONITORAMENTO",
            "gateway": "10.10.0.254",
            "farm": "Farm A",
            "retencao_esperada_dias": 30,
            "codec": "H.264",        }
        valores.update(atributos)
        return Camera.objects.create(**valores)

    def test_lista_camera_possui_filtros_e_tabela_acessiveis(self):
        response = self.client.get(reverse("cameras:lista"))
        self.assertNotContains(response, 'aria-label="Navegação estrutural"')
        self.assertContains(response, 'class="page-heading__title"')
        self.assertContains(response, 'class="page-heading__eyebrow"')
        self.assertContains(response, 'class="form-container filter-panel inventory-filters-card"')
        self.assertContains(response, 'class="filter-panel__grid inventory-filter-form"')
        self.assertContains(response, 'class="filter-panel__actions inventory-filter-actions"')
        self.assertContains(response, 'role="search"')
        self.assertContains(response, 'aria-label="Filtros do inventário de câmeras"')
        self.assertContains(response, 'data-filter-multiselect', count=8)
        for parametro in (
            "status",
            "situacao_operacional",
            "completude",
            "terminal",
            "tipo",
            "fabricante",
            "vlan",
            "farm",
        ):
            self.assertContains(response, f'name="{parametro}"')
        self.assertContains(response, "js/filtros.js")
        self.assertContains(response, 'role="region" aria-label="Câmeras encontradas" tabindex="0"')
        self.assertContains(response, "Relação de câmeras encontradas no inventário")
        self.assertContains(response, 'scope="col"')

    def test_multisselecao_mantem_multiplos_valores_marcados(self):
        response = self.client.get(
            reverse("cameras:lista"),
            {"status": ["ONLINE", "OFFLINE"]},
        )

        self.assertContains(response, 'value="ONLINE"')
        self.assertContains(response, 'value="OFFLINE"')
        self.assertContains(response, "2 seleções")

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

    def test_lista_agrupa_informacoes_sem_remover_dados(self):
        response = self.client.get(reverse("cameras:lista"))

        for cabecalho in ("Status", "Câmera", "Localização", "Rede", "Equipamento", "Ações"):
            self.assertContains(response, f'<th scope="col">{cabecalho}</th>')
        self.assertContains(response, '<th class="camera-table__heading--governance" scope="col">Governança</th>')
        for valor in (
            "CAM-FRONTEND",
            "PAT-001",
            "TPS1",
            "SALA DE MONITORAMENTO",
            "10.10.0.1",
            "VLAN:",
            "100",
            "AXIS",
            "MODELO DE TESTE",
            "Dome",
            "Produção",
            "Cadastro completo",
        ):
            self.assertContains(response, valor)

    def test_resumo_aparece_somente_com_filtros_ativos(self):
        sem_filtros = self.client.get(reverse("cameras:lista"), {"page": "1"})
        self.assertNotContains(sem_filtros, 'class="active-filters"')

        filtrada = self.client.get(
            reverse("cameras:lista"),
            {"q": "CAM-FRONTEND"},
        )
        self.assertContains(filtrada, 'class="active-filters"')
        self.assertContains(filtrada, "Filtros ativos")
        self.assertContains(filtrada, "Pesquisa")
        self.assertContains(filtrada, "CAM-FRONTEND")
        self.assertContains(filtrada, "Limpar todos")
        self.assertNotContains(
            filtrada,
            "Consulta filtrada no inventário.",
        )

    def test_chip_remove_um_valor_e_preserva_os_demais(self):
        response = self.client.get(
            reverse("cameras:lista"),
            {
                "status": ["ONLINE", "OFFLINE"],
                "situacao_operacional": "PRODUCAO",
                "page": "2",
            },
        )

        self.assertContains(
            response,
            'href="?status=OFFLINE&amp;situacao_operacional=PRODUCAO"',
        )
        self.assertContains(
            response,
            'href="?status=ONLINE&amp;situacao_operacional=PRODUCAO"',
        )
        self.assertNotContains(
            response,
            'href="?status=OFFLINE&amp;situacao_operacional=PRODUCAO&amp;page=2"',
        )

    def test_estado_vazio_distingue_inventario_sem_cameras(self):
        Camera.objects.all().delete()
        response = self.client.get(reverse("cameras:lista"))

        self.assertContains(response, "Nenhuma câmera cadastrada")
        self.assertContains(response, "Cadastre o primeiro equipamento do inventário.")
        self.assertNotContains(response, "Consulta filtrada no inventário.")

    def test_chip_remove_filtro_textual_normalizado(self):
        response = self.client.get(
            reverse("cameras:lista"),
            {
                "fabricante": "axis",
                "status": "ONLINE",
                "page": "2",
            },
        )

        self.assertContains(
            response,
            'aria-label="Remover filtro Fabricante: AXIS"',
        )
        self.assertContains(
            response,
            'href="?status=ONLINE"',
        )

    def test_multisselecao_stale_mantem_resumo_legivel(self):
        response = self.client.get(
            reverse("cameras:lista"),
            {"terminal": "TPS-LEGADO"},
        )

        html = response.content.decode("utf-8")

        self.assertRegex(
            html,
            r'(?s)<fieldset class="form-field filter-multiselect-field">'
            r'\s*<legend class="form-label">\s*Terminal\s*</legend>'
            r'.*?data-filter-summary-text[^>]*>'
            r'\s*TPS-LEGADO\s*</span>',
        )

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

    def test_eventos_compartilham_contrato_visual_de_filtros_sem_alterar_parametros(self):
        response = self.client.get(
            reverse("eventos:lista"),
            {
                "q": "camera",
                "categoria": [
                    "CAMERA",
                    "SISTEMA",
                ],
                "origem": [
                    "WEB",
                    "ADMIN",
                ],
                "data_inicial": "2026-08-01",
                "data_final": "2026-08-10",
            },
        )

        html = response.content.decode("utf-8")

        self.assertContains(
            response,
            'class="page-heading__eyebrow"',
        )
        self.assertContains(
            response,
            'class="filter-panel event-filter-panel"',
        )
        self.assertContains(
            response,
            'class="filter-panel__grid event-filters"',
        )
        self.assertContains(
            response,
            'class="filter-panel__actions event-filter-actions"',
        )
        self.assertContains(
            response,
            'role="search"',
        )

        for parametro in (
            'name="q"',
            'name="categoria"',
            'name="origem"',
            'name="data_inicial"',
            'name="data_final"',
        ):
            self.assertContains(
                response,
                parametro,
            )

        self.assertEqual(
            html.count('data-filter-multiselect'),
            2,
        )

        self.assertEqual(
            html.count('name="categoria"'),
            len(response.context["categorias"]),
        )
        self.assertEqual(
            html.count('name="origem"'),
            len(response.context["origens"]),
        )

        self.assertRegex(
            html,
            r'(?s)<legend class="form-label">\s*Categoria\s*</legend>'
            r'.*?data-filter-summary-text[^>]*>\s*2 sele\u00e7\u00f5es\s*</span>',
        )
        self.assertRegex(
            html,
            r'(?s)<legend class="form-label">\s*Origem\s*</legend>'
            r'.*?data-filter-summary-text[^>]*>\s*2 sele\u00e7\u00f5es\s*</span>',
        )

        for valor in (
            "CAMERA",
            "SISTEMA",
            "WEB",
            "ADMIN",
        ):
            self.assertRegex(
                html,
                rf'value="{valor}"[^>]*checked',
            )

        self.assertNotRegex(
            html,
            r'<select[^>]+name="(?:categoria|origem)"',
        )

        self.assertContains(
            response,
            'static/js/filtros.js',
        )
    def test_eventos_sem_filtros_nao_exibem_filtros_ativos(self):
        response = self.client.get(
            reverse("eventos:lista"),
        )

        self.assertNotContains(
            response,
            'class="active-filters"',
        )

    def test_eventos_exibem_filtros_ativos_com_remocao_individual(self):
        response = self.client.get(
            reverse("eventos:lista"),
            {
                "categoria": [
                    "CAMERA",
                    "SISTEMA",
                ],
                "origem": ["WEB"],
                "page": "2",
            },
        )

        self.assertContains(
            response,
            'aria-label="Filtros ativos"',
        )
        self.assertContains(
            response,
            "Remover filtro Categoria: Sistema",
        )
        self.assertContains(
            response,
            'href="?categoria=CAMERA&amp;origem=WEB"',
        )
        self.assertContains(
            response,
            'href="/eventos/"',
        )
