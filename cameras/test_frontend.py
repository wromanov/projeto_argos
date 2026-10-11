import re
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .catalogos import VALOR_PERSONALIZADO
from .forms import CameraEdicaoForm
from .models import Camera, EstadoMonitoramento


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
        self.assertContains(response, 'class="argos-page-title"')
        self.assertContains(response, 'class="argos-eyebrow"')
        self.assertContains(response, 'class="argos-card inventory-filters-card"')
        self.assertContains(response, 'class="argos-filter-bar inventory-filter-form"')
        self.assertContains(response, 'class="argos-inline inventory-filter-actions"')
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
        self.assertContains(response, 'role="region" aria-label="Câmeras encontradas" aria-describedby="inventory-table-hint" tabindex="0"')
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
        self.assertContains(response, "UNKNOWN")
        self.assertContains(response, "NÃO MONITORADA")
        self.assertContains(response, "Cadastro completo")
        self.assertContains(response, "Cadastro incompleto")
        self.assertContains(response, 'badge badge--producao')
        self.assertContains(response, 'badge badge--unknown')
        self.assertContains(response, 'badge badge--out_of_scope')
        self.assertContains(response, 'badge badge--incompleto')
        vazio = self.client.get(reverse("cameras:lista"), {"q": "sem-correspondencia"})
        self.assertContains(vazio, "Nenhuma câmera encontrada")
        self.assertContains(vazio, "Não há câmeras correspondentes aos filtros informados.")
        self.assertContains(vazio, "Limpar filtros")

    def test_lista_agrupa_informacoes_sem_remover_dados(self):
        response = self.client.get(reverse("cameras:lista"))

        for cabecalho in ("Monitoramento", "Câmera", "Localização", "Rede", "Equipamento", "Ações"):
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

    def test_lista_canoniza_filtros_e_descarta_valores_invalidos_e_desconhecidos(self):
        for indice in range(2, 22):
            self.criar_camera(
                indice,
                nome=f"CAM-PAG-{indice:03d}",
                status=Camera.StatusCamera.ONLINE,
            )

        response = self.client.get(
            reverse("cameras:lista"),
            {
                "status": ["INVALIDO", "ONLINE", "ONLINE"],
                "vlan": ["99999", "0100"],
                "ordenacao": "invalida",
                "q": "  CAM  ",
                "foo": "bar",
                "page": ["2", "3"],
            },
        )

        html = response.content.decode("utf-8").replace("&amp;", "&")
        self.assertEqual(response.context["status_selecionados"], ["ONLINE"])
        self.assertEqual(response.context["vlans_selecionadas"], ["100"])
        self.assertEqual(response.context["q"], "CAM")
        self.assertEqual(response.context["ordenacao"], "nome")
        self.assertNotIn("INVALIDO", html)
        self.assertNotIn("vlan=99999", html)
        self.assertNotIn("ordenacao=invalida", html)
        self.assertNotIn("foo=bar", html)
        self.assertIn("q=CAM", html)
        self.assertIn("vlan=100", html)
        links = re.findall(r'href="([^"]+)"', html)
        links_com_page = [link for link in links if "page=" in link]
        self.assertTrue(links_com_page)
        for link in links_com_page:
            self.assertEqual(link.count("status=ONLINE"), 1)
            self.assertEqual(link.count("page="), 1)

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

    def assert_recording_groups(self, response):
        html = response.content.decode("utf-8")

        self.assertEqual(
            html.count('class="camera-form-field-group"'),
            3,
        )

        grupos = (
            ("farm", "farm", "farm_personalizado"),
            (
                "retencao",
                "retencao_esperada_dias",
                "retencao_personalizada_dias",
            ),
            ("codec", "codec", "codec_personalizado"),
        )

        for indice_grupo, (
            grupo,
            campo_principal,
            campo_personalizado,
        ) in enumerate(grupos):
            marcador = (
                '<div class="camera-form-field-group" '
                f'data-recording-group="{grupo}">'
            )
            inicio_grupo = html.index(marcador)
            inicio_principal = html.index(
                f'name="{campo_principal}"',
                inicio_grupo,
            )
            inicio_personalizado = html.index(
                f'id="id_{campo_personalizado}"',
                inicio_grupo,
            )

            self.assertLess(inicio_grupo, inicio_principal)
            self.assertLess(inicio_principal, inicio_personalizado)

            if indice_grupo < len(grupos) - 1:
                proximo_grupo = grupos[indice_grupo + 1][0]
                inicio_proximo_grupo = html.index(
                    '<div class="camera-form-field-group" '
                    f'data-recording-group="{proximo_grupo}">',
                    inicio_grupo + 1,
                )
                self.assertLess(
                    inicio_personalizado,
                    inicio_proximo_grupo,
                )

        for nome in (
            "farm",
            "farm_personalizado",
            "retencao_esperada_dias",
            "retencao_personalizada_dias",
            "codec",
            "codec_personalizado",
        ):
            self.assertContains(response, f'name="{nome}"')

        self.assertContains(response, 'static/js/camera-form.js')
        self.assertContains(response, 'class="field__label"')

    def test_formulario_de_criacao_agrupa_pares_de_gravacao(self):
        response = self.client.get(reverse("cameras:criar"))

        self.assertEqual(response.status_code, 200)
        self.assert_recording_groups(response)

    def test_formulario_de_edicao_exibe_personalizados_legados_no_grupo(self):
        self.camera.farm = "FARM-TPS2-02"
        self.camera.retencao_esperada_dias = 365
        self.camera.codec = "H265"
        self.camera.save(
            update_fields=(
                "farm",
                "retencao_esperada_dias",
                "codec",
            )
        )

        response = self.client.get(
            reverse("cameras:editar", args=[self.camera.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assert_recording_groups(response)
        for container_id in (
            "farm-personalizado-container",
            "retencao-personalizada-container",
            "codec-personalizado-container",
        ):
            self.assertNotRegex(
                response.content.decode("utf-8"),
                rf'id="{container_id}"[^>]*\bhidden\b',
            )

    def test_erro_em_personalizado_mantem_par_visivel_e_aria_associada(self):
        form = CameraEdicaoForm(instance=self.camera)
        dados = {
            nome: form[nome].value() or ""
            for nome in form.fields
        }
        dados.update(
            {
                "farm": VALOR_PERSONALIZADO,
                "farm_personalizado": "",
            }
        )

        response = self.client.post(
            reverse("cameras:editar", args=[self.camera.pk]),
            dados,
        )

        self.assertEqual(response.status_code, 200)
        self.assert_recording_groups(response)
        self.assertContains(
            response,
            'id="farm-personalizado-container" '
            'data-farm-personalizado',
        )
        self.assertNotRegex(
            response.content.decode("utf-8"),
            r'id="farm-personalizado-container" '
            r'[^>]*\bhidden\b',
        )
        self.assertContains(
            response,
            'id="id_farm_personalizado_errors"',
        )
        self.assertContains(
            response,
            'aria-invalid="true"',
        )
        self.assertContains(
            response,
            'aria-errormessage="id_farm_personalizado_errors"',
        )


class CameraDetailFrontendTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_superuser(
            username="frontend-camera-detail", password="senha-forte", email=""
        )
        self.client.force_login(self.user)
        self.camera = Camera.objects.create(
            nome="CAMERA-DETALHE",
            patrimonio="PAT-DETALHE",
            ip="10.20.30.40",
            mascara_subrede="255.255.255.0",
            gateway="10.20.30.1",
            vlan=20,
            fabricante="AXIS",
            modelo="P3265",
            serial="SERIAL-DETALHE",
            mac="AA:BB:CC:DD:EE:FF",
            tipo=Camera.TipoCamera.DOME,
            situacao_operacional=Camera.SituacaoOperacional.PRODUCAO,
            terminal="TPS1",
            ambiente="SALA DE MONITORAMENTO",
            farm="FARM-01",
            retencao_esperada_dias=30,
            codec="H.264",
        )

    def test_camera_detail_fica_fora_do_escopo_ds_24_hom_01(self):
        response = self.client.get(reverse("cameras:detalhe", args=[self.camera.pk]))

        self.assertContains(response, 'class="app-shell"')
        self.assertNotContains(response, "argos-ui-v2-production")
        self.assertNotContains(response, "/static/css/ui-v2/hom-01-2.4.0/")
        self.assertContains(response, "/static/css/ui-v2/camera-detail.css")

    def test_detail_uses_canonical_regions_and_removes_legacy_presentational_classes(self):
        response = self.client.get(reverse("cameras:detalhe", args=[self.camera.pk]))
        self.assertEqual(response.status_code, 200)
        html = response.content.decode("utf-8")

        expected_order = (
            "← Voltar ao inventário",
            "Inventário CFTV / Detalhe da câmera",
            "CAMERA-DETALHE",
            "Estados da câmera",
            "Editar câmera",
            "Situação e completude",
            "Monitoramento técnico",
            "Ações operacionais",
            "Identificação e localização",
            "<dt>Fabricante</dt>",
            "Rede e gravação",
            "Governança cadastral",
            "Histórico",
            "Histórico técnico de indisponibilidades",
            "Histórico de atividades",
            "Histórico de substituições",
            "Eventos de auditoria",
            "Operações complementares",
            "Enviar imagem manualmente",
        )
        content_start = html.index("← Voltar ao inventário")
        positions = [html.index(item, content_start) for item in expected_order]
        self.assertEqual(positions, sorted(positions))
        self.assertContains(response, 'id="camera-detail-title"')
        self.assertContains(response, 'argos-camera-detail__name argos-page-title')
        self.assertContains(response, "argos-back-link")
        self.assertContains(response, "argos-section-surface", count=2)
        self.assertRegex(html, r'<section class="argos-section-surface argos-camera-detail__record-surface" aria-label="Ficha da câmera">')
        self.assertRegex(html, r'<section class="argos-section-surface argos-camera-detail__history-surface" aria-labelledby="camera-detail-history-heading">')
        for region in ("situation", "monitoring", "actions", "identification-location", "network-recording", "governance", "history", "complementary"):
            self.assertIn(f'id="camera-detail-{region}-heading"', html)
        self.assertContains(
            response,
            '<header class="argos-camera-detail__hero" aria-labelledby="camera-detail-title">',
        )
        self.assertContains(response, 'class="argos-data-pair"')
        for legacy_class in (
            "inventory-panel",
            "detail-card",
            "detail-grid",
            "detail-empty-state",
            "camera-governance-panel",
            "activity-card",
        ):
            self.assertNotIn(legacy_class, html)

    def test_detail_reading_order_grouping_and_empty_values(self):
        self.camera.motivo_desativacao = ""
        self.camera.save(update_fields=("motivo_desativacao",))
        response = self.client.get(reverse("cameras:detalhe", args=[self.camera.pk]))
        html = response.content.decode("utf-8")
        hero = html[html.index('aria-labelledby="camera-detail-title"'):]
        positions = [hero.index(marker) for marker in (
            'id="camera-detail-title"',
            'argos-camera-detail__location',
            'aria-label="Estados da câmera"',
            '>Editar câmera</a>',
        )]
        self.assertEqual(positions, sorted(positions))
        for region in ("situation", "monitoring", "actions", "identification-location",
                       "network-recording", "governance", "history", "complementary"):
            self.assertRegex(html, rf'<header class="argos-section-header"><h2 '
                             rf'id="camera-detail-{region}-heading">')
        situation = html[html.index('id="camera-detail-situation-heading"'):]
        self.assertIn('<dl class="argos-data-group argos-camera-detail__pairs">', situation)
        self.assertIn('<div class="argos-data-pair argos-camera-detail__pair--full">'
                      '<dt>Motivo da última desativação</dt>', situation)
        self.assertIn('<span class="argos-state__copy">—</span>', situation)
        activity = html[html.index('id="camera-detail-activities-heading"'):]
        self.assertLess(activity.index('>Registrar atividade</a>'),
                        activity.index('id="camera-detail-activities-all"'))

    def test_detail_preserves_upload_form_contract_and_authorized_edit_action(self):
        response = self.client.get(reverse("cameras:detalhe", args=[self.camera.pk]))
        self.assertContains(response, reverse("cameras:editar", args=[self.camera.pk]))
        self.assertContains(response, reverse("cameras:upload_imagem", args=[self.camera.pk]))
        self.assertContains(
            response,
            '<form class="argos-camera-detail__upload-form" action="'
            f'{reverse("cameras:upload_imagem", args=[self.camera.pk])}'
            '" method="post" enctype="multipart/form-data">',
        )
        self.assertContains(
            response,
            'id="imagem-camera" name="imagem" type="file" '
            'accept="image/jpeg,image/png,image/webp" required',
        )
        self.assertContains(response, 'name="csrfmiddlewaretoken"')
        self.assertContains(response, '<button class="argos-button argos-button--primary" type="submit">Enviar imagem</button>')

    def test_monitoring_badge_remains_legacy_on_inventory_and_ui_v2_on_detail(self):
        detail = self.client.get(reverse("cameras:detalhe", args=[self.camera.pk]))
        self.assertContains(detail, "argos-status-badge--success")

        inventory = self.client.get(reverse("cameras:lista"))
        self.assertRegex(inventory.content.decode("utf-8"), r'class="badge badge--[^\"]+"')

    def test_stale_unknown_context_stacks_below_compact_badges_and_keeps_confirmed_state(self):
        stale_at = timezone.now() - timedelta(days=1)
        self.camera.pavimento = "1º PAVIMENTO"
        self.camera.setor = "SEGURANÇA"
        self.camera.save(update_fields=("pavimento", "setor"))
        EstadoMonitoramento.objects.create(
            camera=self.camera,
            estado_estavel=EstadoMonitoramento.EstadoEstavel.UNKNOWN,
            estado_alterado_em=stale_at,
            ultima_evidencia_util_em=stale_at,
            em_escopo=True,
        )

        response = self.client.get(reverse("cameras:detalhe", args=[self.camera.pk]))
        self.assertEqual(response.status_code, 200)
        html = response.content.decode("utf-8")
        self.assertEqual(html.count("Dados desatualizados"), 1)
        self.assertNotIn("Dados desatualizados · último estado UNKNOWN", html)
        self.assertRegex(html, r'<dt>Último estado confirmado</dt><dd><span>UNKNOWN</span></dd>')

        hero = html[html.index('class="argos-camera-detail__status-cluster"'):html.index("</header>", html.index('class="argos-camera-detail__status-cluster"'))]
        self.assertIn('role="group" aria-label="Estados da câmera"', hero)
        self.assertNotIn("Dados desatualizados", hero)

        monitoring_start = html.index('class="argos-camera-detail__monitoring-status"')
        monitoring = html[monitoring_start:html.index("</dd>", monitoring_start)]
        self.assertLess(
            monitoring.index("UNKNOWN"),
            monitoring.index("Dados desatualizados"),
        )

    def test_out_of_scope_option_a_shows_context_only_in_scope_field(self):
        self.camera.situacao_operacional = Camera.SituacaoOperacional.ESTOQUE
        self.camera.save(update_fields=("situacao_operacional",))

        response = self.client.get(reverse("cameras:detalhe", args=[self.camera.pk]))
        html = response.content.decode("utf-8")
        self.assertEqual(html.count("Fora do escopo"), 1)
        self.assertEqual(html.count("NÃO MONITORADA"), 2)

        hero_start = html.index('class="argos-camera-detail__status-cluster"')
        hero = html[hero_start:html.index("</header>", hero_start)]
        self.assertNotIn("Fora do escopo", hero)
        self.assertNotIn("argos-camera-detail__monitoring-summary", hero)

        state_start = html.index("<dt>Estado atual</dt>")
        scope_start = html.index("<dt>Escopo</dt>", state_start)
        state_row = html[state_start:scope_start]
        scope_row = html[scope_start:html.index("</div>", scope_start)]
        self.assertIn("NÃO MONITORADA", state_row)
        self.assertNotIn("Fora do escopo", state_row)
        self.assertIn("Fora do escopo", scope_row)
        self.assertNotIn('class="argos-camera-detail__status-support"', html)

    def test_incomplete_configuration_context_remains_visible(self):
        self.camera.ip = ""
        self.camera.save(update_fields=("ip",))

        response = self.client.get(reverse("cameras:detalhe", args=[self.camera.pk]))
        html = response.content.decode("utf-8")
        self.assertGreaterEqual(html.count("Configuração incompleta"), 3)
        self.assertIn('class="argos-camera-detail__monitoring-summary"', html)

    def test_monitoring_state_badges_remain_semantic_on_detail(self):
        now = timezone.now()
        self.camera.pavimento = "TÉRREO"
        self.camera.setor = "SETOR DE TESTE"
        self.camera.save(update_fields=("pavimento", "setor"))
        for state, label, badge_class in (
            (EstadoMonitoramento.EstadoEstavel.ONLINE, "ONLINE", "argos-status-badge--success"),
            (EstadoMonitoramento.EstadoEstavel.OFFLINE, "OFFLINE", "argos-status-badge--danger"),
            (EstadoMonitoramento.EstadoEstavel.UNKNOWN, "UNKNOWN", "argos-status-badge--neutral"),
        ):
            with self.subTest(state=state):
                EstadoMonitoramento.objects.update_or_create(
                    camera=self.camera,
                    defaults={
                        "estado_estavel": state,
                        "estado_alterado_em": now,
                        "ultima_evidencia_util_em": now,
                        "em_escopo": True,
                    },
                )
                response = self.client.get(reverse("cameras:detalhe", args=[self.camera.pk]))
                self.assertContains(response, label)
                self.assertContains(response, badge_class)


class GovernancaActionShellFrontendTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_superuser(
            username="frontend-governanca",
            password="senha-forte",
            email="",
        )
        self.client.force_login(self.user)
        self.camera = self.criar_camera(1, "PRODUCAO")
        self.estoque = self.criar_camera(2, "ESTOQUE")
        self.desativada = self.criar_camera(3, "DESATIVADA")

    def criar_camera(self, indice, situacao):
        return Camera.objects.create(
            nome=f"CAM-GOV-{indice}",
            patrimonio=f"PAT-GOV-{indice}",
            ip=f"10.20.0.{indice}",
            mascara_subrede="255.255.255.0",
            vlan=100,
            fabricante="AXIS",
            modelo="MODELO DE TESTE",
            serial=f"SERIAL-GOV-{indice}",
            mac=f"AA:BB:CC:DD:{indice:02X}:01",
            tipo=Camera.TipoCamera.DOME,
            situacao_operacional=situacao,
            terminal="TPS1",
            pavimento="Terreo",
            setor="Seguranca",
            ambiente="SALA DE MONITORAMENTO",
            gateway="10.20.0.254",
            farm="Farm A",
            retencao_esperada_dias=30,
            codec="H.264",
        )

    def casos(self):
        return (
            {
                "nome": "alterar_situacao",
                "url": reverse("cameras:alterar_situacao", args=[self.camera.pk]),
                "titulo": "Alterar situação operacional",
                "descricao": "Atualize o destino operacional sem alterar o monitoramento técnico.",
                "aviso": "A movimentação não altera o status técnico de monitoramento.",
                "label": "Confirmar movimentação",
                "classe": "button button--primary",
                "campos": ("destino", "justificativa"),
            },
            {
                "nome": "desativar",
                "url": reverse("cameras:desativar", args=[self.camera.pk]),
                "titulo": "Desativar câmera",
                "descricao": "Retire a câmera da operação mantendo seu registro histórico.",
                "aviso": "A câmera permanecerá no histórico e não será excluída.",
                "label": "Confirmar desativação",
                "classe": "button button--danger",
                "campos": ("motivo",),
            },
            {
                "nome": "reativar",
                "url": reverse("cameras:reativar", args=[self.desativada.pk]),
                "titulo": "Reativar câmera",
                "descricao": "Escolha o destino operacional para retornar a câmera ao uso.",
                "aviso": "Escolha o destino operacional. A completude será validada antes da reativação.",
                "label": "Confirmar reativação",
                "classe": "button button--primary",
                "campos": ("destino", "justificativa"),
            },
            {
                "nome": "substituir",
                "url": reverse("cameras:substituir", args=[self.camera.pk]),
                "titulo": "Substituir câmera",
                "descricao": "Transfira a operação preservando os dados físicos e o histórico.",
                "aviso": "Os campos operacionais serão transferidos; patrimônio, fabricante, modelo, serial, MAC e tipo da substituta serão preservados. A operação é transacional e o histórico não poderá ser editado ou excluído.",
                "label": "Registrar substituição",
                "classe": "button button--primary",
                "campos": ("camera_substituta", "motivo", "observacoes"),
            },
        )

    def test_quatro_fluxos_renderizam_o_shell_compartilhado_com_seus_contratos(self):
        casos = self.casos()

        for caso in casos:
            with self.subTest(fluxo=caso["nome"]):
                response = self.client.get(caso["url"])
                html = response.content.decode("utf-8")
                url_cancelamento = reverse(
                    "cameras:detalhe",
                    args=[self.desativada.pk if caso["nome"] == "reativar" else self.camera.pk],
                )

                self.assertEqual(response.status_code, 200)
                self.assertTemplateUsed(
                    response,
                    "components/governanca_action_shell.html",
                )
                self.assertContains(
                    response,
                    f'<h1 id="governance-action-title">{caso["titulo"]}</h1>',
                    html=False,
                )
                self.assertContains(response, caso["descricao"])
                self.assertContains(
                    response,
                    f'<div class="governance-notice" role="note">{caso["aviso"]}</div>',
                    html=False,
                )
                self.assertContains(
                    response,
                    f'<button class="{caso["classe"]}" type="submit">{caso["label"]}</button>',
                    html=False,
                )
                self.assertContains(
                    response,
                    'aria-labelledby="governance-action-title"',
                )
                self.assertContains(response, 'role="note"')
                self.assertContains(response, 'method="post"')
                self.assertContains(response, 'name="csrfmiddlewaretoken"')
                self.assertRegex(
                    html,
                    r'<form class="governance-form" method="post" novalidate>',
                )
                self.assertContains(
                    response,
                    f'class="governance-back" href="{url_cancelamento}"',
                    html=False,
                )
                self.assertContains(
                    response,
                    f'class="button button--secondary" href="{url_cancelamento}"',
                    html=False,
                )
                for campo in caso["campos"]:
                    self.assertContains(response, f'name="{campo}"')
                self.assertContains(response, 'class="field__label"')

                for outro in casos:
                    if outro is caso:
                        continue
                    self.assertNotIn(outro["titulo"], html)
                    self.assertNotIn(outro["aviso"], html)
                    self.assertNotIn(outro["label"], html)
