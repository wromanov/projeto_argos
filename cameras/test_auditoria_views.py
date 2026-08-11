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
        self.autenticar()
        response = self.client.get(
            reverse("eventos:lista"),
            {"categoria": "CAMERA"},
        )

        self.assertEqual(
            response.context["total_eventos"],
            1,
        )
        self.assertEqual(
            response.context["categoria_selecionada"],
            "CAMERA",
        )
        self.assertEqual(
            response.context["categorias_selecionadas"],
            ["CAMERA"],
        )

    def test_08_filtro_origem(self):
        self.autenticar()
        response = self.client.get(
            reverse("eventos:lista"),
            {"origem": "ADMIN"},
        )

        self.assertEqual(
            response.context["total_eventos"],
            0,
        )
        self.assertEqual(
            response.context["origem_selecionada"],
            "ADMIN",
        )
        self.assertEqual(
            response.context["origens_selecionadas"],
            ["ADMIN"],
        )

    def test_07_categoria_multivalorada_aplica_or(self):
        EventoAuditoria.objects.create(
            categoria="SISTEMA",
            codigo="sistema.teste",
            resumo="Sistema",
        )

        self.autenticar()

        response = self.client.get(
            reverse("eventos:lista"),
            {
                "categoria": [
                    "CAMERA",
                    "SISTEMA",
                ],
            },
        )

        self.assertEqual(
            response.context["total_eventos"],
            2,
        )

    def test_08_origem_multivalorada_aplica_or(self):
        EventoAuditoria.objects.create(
            categoria="SISTEMA",
            codigo="sistema.admin",
            resumo="Admin",
            origem="ADMIN",
        )

        self.autenticar()

        response = self.client.get(
            reverse("eventos:lista"),
            {
                "origem": [
                    "WEB",
                    "ADMIN",
                ],
            },
        )

        self.assertEqual(
            response.context["total_eventos"],
            2,
        )

    def test_multifiltro_eventos_combina_facetas_com_and(self):
        EventoAuditoria.objects.create(
            categoria="CAMERA",
            codigo="camera.admin",
            resumo="Camera Admin",
            origem="ADMIN",
        )
        EventoAuditoria.objects.create(
            categoria="SISTEMA",
            codigo="sistema.web",
            resumo="Sistema Web",
            origem="WEB",
        )

        self.autenticar()

        response = self.client.get(
            reverse("eventos:lista"),
            {
                "categoria": ["CAMERA"],
                "origem": ["WEB"],
            },
        )

        self.assertEqual(
            response.context["total_eventos"],
            1,
        )
        self.assertEqual(
            [
                evento.codigo
                for evento in response.context["eventos"]
            ],
            ["camera.criada"],
        )

    def test_enum_invalido_preserva_valor_valido_e_contexto_plural(self):
        self.autenticar()

        response = self.client.get(
            reverse("eventos:lista"),
            {
                "categoria": [
                    "INVALIDA",
                    "CAMERA",
                ],
                "origem": [
                    "INVALIDA",
                    "WEB",
                ],
            },
        )

        self.assertEqual(
            response.context["total_eventos"],
            1,
        )
        self.assertEqual(
            response.context["categorias_selecionadas"],
            ["CAMERA"],
        )
        self.assertEqual(
            response.context["origens_selecionadas"],
            ["WEB"],
        )
        self.assertEqual(
            response.context["categoria_selecionada"],
            "CAMERA",
        )
        self.assertEqual(
            response.context["origem_selecionada"],
            "WEB",
        )

    def test_filtros_ativos_refletem_eventos(self):
        self.autenticar()

        response = self.client.get(
            reverse("eventos:lista"),
            {
                "q": "CAM-VIEW",
                "categoria": [
                    "CAMERA",
                    "SISTEMA",
                ],
                "origem": ["WEB"],
                "data_inicial": "2026-08-01",
                "data_final": "2026-08-10",
            },
        )

        filtros = [
            (
                filtro["nome"],
                filtro["valor"],
                filtro["grupo"],
                filtro["rotulo"],
            )
            for filtro in response.context["filtros_ativos"]
        ]

        self.assertIn(
            (
                "q",
                "CAM-VIEW",
                "Pesquisa",
                "CAM-VIEW",
            ),
            filtros,
        )
        self.assertIn(
            (
                "categoria",
                "SISTEMA",
                "Categoria",
                "Sistema",
            ),
            filtros,
        )
        self.assertIn(
            (
                "origem",
                "WEB",
                "Origem",
                "Web",
            ),
            filtros,
        )
        self.assertIn(
            (
                "data_inicial",
                "2026-08-01",
                "De",
                "01/08/2026",
            ),
            filtros,
        )
        self.assertIn(
            (
                "data_final",
                "2026-08-10",
                "At\u00e9",
                "10/08/2026",
            ),
            filtros,
        )

    def test_paginacao_eventos_preserva_parametros_repetidos(self):
        for indice in range(51):
            EventoAuditoria.objects.create(
                categoria="SISTEMA",
                codigo=f"sistema.paginacao.{indice}",
                resumo="Paginacao",
                origem="ADMIN",
            )

        self.autenticar()

        response = self.client.get(
            reverse("eventos:lista"),
            {
                "categoria": [
                    "CAMERA",
                    "SISTEMA",
                ],
                "origem": [
                    "WEB",
                    "ADMIN",
                ],
            },
        )

        self.assertEqual(
            response.context["paginator"].num_pages,
            2,
        )
        self.assertContains(
            response,
            "categoria=CAMERA"
            "&amp;categoria=SISTEMA"
            "&amp;origem=WEB"
            "&amp;origem=ADMIN"
            "&amp;page=2",
        )

    def test_multivalores_duplicados_sao_deduplicados(self):
        self.autenticar()

        response = self.client.get(
            reverse("eventos:lista"),
            {
                "categoria": [
                    "CAMERA",
                    "CAMERA",
                ],
                "origem": [
                    "WEB",
                    "WEB",
                ],
            },
        )

        self.assertEqual(
            response.context["categorias_selecionadas"],
            ["CAMERA"],
        )
        self.assertEqual(
            response.context["origens_selecionadas"],
            ["WEB"],
        )

        filtros_categoria = [
            filtro
            for filtro in response.context["filtros_ativos"]
            if filtro["nome"] == "categoria"
        ]
        filtros_origem = [
            filtro
            for filtro in response.context["filtros_ativos"]
            if filtro["nome"] == "origem"
        ]

        self.assertEqual(
            len(filtros_categoria),
            1,
        )
        self.assertEqual(
            len(filtros_origem),
            1,
        )

    def test_periodo_parcial_aplica_limite_individual(self):
        self.autenticar()

        somente_inicio = self.client.get(
            reverse("eventos:lista"),
            {
                "data_inicial": "2999-01-01",
            },
        )

        self.assertFalse(
            somente_inicio.context["periodo_invalido"],
        )
        self.assertEqual(
            somente_inicio.context["total_eventos"],
            0,
        )

        somente_fim = self.client.get(
            reverse("eventos:lista"),
            {
                "data_final": "2999-01-01",
            },
        )

        self.assertFalse(
            somente_fim.context["periodo_invalido"],
        )
        self.assertEqual(
            somente_fim.context["total_eventos"],
            1,
        )

    def test_historico_camera_aplica_multifiltros_e_isolamento(self):
        EventoAuditoria.objects.create(
            categoria="SISTEMA",
            codigo="sistema.camera.web",
            resumo="Sistema Web",
            camera=self.camera,
            origem="WEB",
        )
        EventoAuditoria.objects.create(
            categoria="CAMERA",
            codigo="camera.admin",
            resumo="Camera Admin",
            camera=self.camera,
            origem="ADMIN",
        )

        outra = Camera.objects.create(
            nome="CAM-GF05D-OUTRA",
            fabricante="Axis",
            modelo="M",
            ip="10.21.0.99",
            mascara_subrede="255.255.255.0",
            vlan=199,
        )

        EventoAuditoria.objects.create(
            categoria="CAMERA",
            codigo="camera.outra.web",
            resumo="Outra Camera Web",
            camera=outra,
            origem="WEB",
        )

        self.autenticar()

        response = self.client.get(
            reverse(
                "cameras:eventos_camera",
                args=[self.camera.pk],
            ),
            {
                "categoria": [
                    "CAMERA",
                    "SISTEMA",
                ],
                "origem": ["WEB"],
            },
        )

        self.assertEqual(
            response.context["total_eventos"],
            2,
        )
        self.assertContains(
            response,
            "camera.criada",
        )
        self.assertContains(
            response,
            "sistema.camera.web",
        )
        self.assertNotContains(
            response,
            "camera.admin",
        )
        self.assertNotContains(
            response,
            "camera.outra.web",
        )

    def test_09_filtro_periodo(self):
        self.autenticar(); hoje = timezone.localdate().isoformat()
        self.assertEqual(self.client.get(reverse("eventos:lista"), {"data_inicial": hoje, "data_final": hoje}).context["total_eventos"], 1)

    def test_10_periodo_invalido(self):
        self.autenticar()
        response = self.client.get(
            reverse("eventos:lista"),
            {
                "data_inicial": "invalida",
                "page": "2",
            },
        )

        self.assertTrue(
            response.context["periodo_invalido"],
        )
        self.assertIn(
            {
                "nome": "data_inicial",
                "valor": "invalida",
                "grupo": "De",
                "rotulo": "invalida",
            },
            response.context["filtros_ativos"],
        )
        self.assertContains(
            response,
            'href="/eventos/"',
        )

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
