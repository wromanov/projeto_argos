from io import StringIO
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management import call_command
from django.test import RequestFactory, TestCase
from django.urls import reverse

from .admin import SubstituicaoCameraAdmin
from .forms import CameraEdicaoForm
from .governanca import substituir_camera
from .models import Camera, SubstituicaoCamera


class GovernancaViewsPermissoesTests(TestCase):
    def setUp(self):
        call_command("configurar_perfis_argos",stdout=StringIO()); self.user=get_user_model().objects.create_user("usuario"); self.superuser=get_user_model().objects.create_superuser("admin",email=""); self.camera=self.criar(1,"PRODUCAO"); self.estoque=self.criar(2,"ESTOQUE")
    def criar(self,n,situacao,**extra):
        data=dict(nome=f"CAM-{n}",fabricante="Axis",modelo="P",serial=f"SER-{n}",mac=f"AA:BB:CC:DD:EE:{n:02X}",tipo="DOME",terminal="T1",pavimento="1",setor="S",ambiente="A",ip=f"10.0.0.{n}",mascara_subrede="255.255.255.0",gateway="10.0.0.254",vlan=10,farm="F1",retencao_esperada_dias=30,codec="H265",situacao_operacional=situacao); data.update(extra); return Camera.objects.create(**data)
    def grupo(self,nome): self.user.groups.set([Group.objects.get(name=nome)]); self.client.force_login(self.user)
    def dados(self,c): return {f.name:(getattr(c,f.name) if getattr(c,f.name) is not None else "") for f in CameraEdicaoForm._meta.model._meta.fields if f.name in CameraEdicaoForm.base_fields}
    def test_lista_filtra_por_situacao_operacional(self): self.client.force_login(self.superuser); r=self.client.get(reverse("cameras:lista"),{"situacao_operacional":"ESTOQUE"}); self.assertEqual([c.pk for c in r.context["cameras"]],[self.estoque.pk])
    def test_lista_filtra_por_cadastro_completo(self): self.criar(3,"PRODUCAO",gateway=None); self.client.force_login(self.superuser); r=self.client.get(reverse("cameras:lista"),{"completude":"COMPLETO"}); self.assertIn(self.camera,[*r.context["cameras"]]); self.assertNotContains(r,"CAM-3")
    def test_lista_filtra_por_cadastro_incompleto(self): self.criar(3,"PRODUCAO",gateway=None); self.client.force_login(self.superuser); self.assertEqual(self.client.get(reverse("cameras:lista"),{"completude":"INCOMPLETO"}).context["total_resultados"],1)
    def test_lista_exibe_badges_de_situacao(self): self.client.force_login(self.superuser); r=self.client.get(reverse("cameras:lista")); self.assertContains(r,"Produção"); self.assertContains(r,"Estoque")
    def test_detalhe_exibe_campos_faltantes(self): c=self.criar(3,"PRODUCAO",gateway=None); self.client.force_login(self.superuser); self.assertContains(self.client.get(reverse("cameras:detalhe",args=[c.pk])),"Gateway")
    def test_formulario_de_edicao_nao_expoe_situacao(self): self.assertNotIn("situacao_operacional",CameraEdicaoForm().fields)
    def test_post_adulterado_nao_altera_situacao(self): self.client.force_login(self.superuser); d=self.dados(self.camera); d["situacao_operacional"]="DESATIVADA"; self.client.post(reverse("cameras:editar",args=[self.camera.pk]),d); self.camera.refresh_from_db(); self.assertEqual(self.camera.situacao_operacional,"PRODUCAO")
    def test_desativacao_get_nao_altera_camera(self): self.grupo("Operador ARGOS"); self.client.get(reverse("cameras:desativar",args=[self.camera.pk])); self.camera.refresh_from_db(); self.assertEqual(self.camera.situacao_operacional,"PRODUCAO")
    def test_desativacao_post_valido_altera_camera(self): self.grupo("Operador ARGOS"); self.client.post(reverse("cameras:desativar",args=[self.camera.pk]),{"motivo":"Motivo operacional válido"}); self.camera.refresh_from_db(); self.assertEqual(self.camera.situacao_operacional,"DESATIVADA")
    def test_monitoramento_nao_pode_alterar_situacao(self): self.grupo("Monitoramento ARGOS"); self.assertEqual(self.client.post(reverse("cameras:alterar_situacao",args=[self.camera.pk]),{"destino":"ESTOQUE","justificativa":"Movimento planejado"}).status_code,403)
    def test_operador_pode_alterar_situacao(self): self.grupo("Operador ARGOS"); self.client.post(reverse("cameras:alterar_situacao",args=[self.camera.pk]),{"destino":"ESTOQUE","justificativa":"Movimento planejado"}); self.camera.refresh_from_db(); self.assertEqual(self.camera.situacao_operacional,"ESTOQUE")
    def test_operador_pode_registrar_substituicao(self): self.grupo("Operador ARGOS"); self.client.post(reverse("cameras:substituir",args=[self.camera.pk]),{"camera_substituta":self.estoque.pk,"motivo":"Falha física confirmada","observacoes":""}); self.assertEqual(SubstituicaoCamera.objects.count(),1)
    def test_lista_de_substituicoes_e_somente_leitura(self): self.grupo("Operador ARGOS"); substituir_camera(camera_anterior=self.camera,camera_substituta=self.estoque,motivo="Falha física confirmada",usuario=self.user); r=self.client.get(reverse("cameras:lista_substituicoes")); self.assertEqual(r.status_code,200); self.assertNotContains(r,"Excluir")
    def test_lista_substituicoes_exibe_nome_historico_da_substituta(self):
        self.grupo("Operador ARGOS")
        nome_original = self.estoque.nome

        substituir_camera(
            camera_anterior=self.camera,
            camera_substituta=self.estoque,
            motivo="Falha física confirmada",
            usuario=self.user,
        )

        response = self.client.get(
            reverse("cameras:lista_substituicoes")
        )

        self.assertContains(response, nome_original)

        self.estoque.refresh_from_db()
        self.assertEqual(self.estoque.nome, self.camera.nome)

    def test_lista_substituicoes_busca_nome_historico_da_substituta(self):
        self.grupo("Operador ARGOS")
        nome_original = self.estoque.nome

        substituir_camera(
            camera_anterior=self.camera,
            camera_substituta=self.estoque,
            motivo="Falha física confirmada",
            usuario=self.user,
        )

        response = self.client.get(
            reverse("cameras:lista_substituicoes"),
            {"q": nome_original},
        )

        self.assertEqual(
            response.context["page_obj"].paginator.count,
            1,
        )

    def test_lista_substituicoes_rejeita_data_malformada(self):
        self.grupo("Operador ARGOS")
        substituir_camera(
            camera_anterior=self.camera,
            camera_substituta=self.estoque,
            motivo="Falha fisica confirmada",
            usuario=self.user,
        )

        response = self.client.get(
            reverse("cameras:lista_substituicoes"),
            {"data_inicial": "invalida"},
        )

        self.assertTrue(response.context["periodo_invalido"])
        self.assertEqual(
            response.context["page_obj"].paginator.count,
            1,
        )

    def test_lista_substituicoes_rejeita_periodo_invertido(self):
        self.grupo("Operador ARGOS")
        substituir_camera(
            camera_anterior=self.camera,
            camera_substituta=self.estoque,
            motivo="Falha fisica confirmada",
            usuario=self.user,
        )

        response = self.client.get(
            reverse("cameras:lista_substituicoes"),
            {
                "data_inicial": "2999-01-02",
                "data_final": "2999-01-01",
            },
        )

        self.assertTrue(response.context["periodo_invalido"])
        self.assertEqual(
            response.context["page_obj"].paginator.count,
            1,
        )

    def test_lista_substituicoes_aceita_periodo_parcial(self):
        self.grupo("Operador ARGOS")
        substituir_camera(
            camera_anterior=self.camera,
            camera_substituta=self.estoque,
            motivo="Falha fisica confirmada",
            usuario=self.user,
        )

        somente_inicio = self.client.get(
            reverse("cameras:lista_substituicoes"),
            {"data_inicial": "2999-01-01"},
        )
        somente_fim = self.client.get(
            reverse("cameras:lista_substituicoes"),
            {"data_final": "2999-01-01"},
        )

        self.assertFalse(
            somente_inicio.context["periodo_invalido"],
        )
        self.assertEqual(
            somente_inicio.context["page_obj"].paginator.count,
            0,
        )
        self.assertFalse(
            somente_fim.context["periodo_invalido"],
        )
        self.assertEqual(
            somente_fim.context["page_obj"].paginator.count,
            1,
        )

    def test_lista_substituicoes_exibe_filtros_ativos(self):
        self.grupo("Operador ARGOS")
        substituir_camera(
            camera_anterior=self.camera,
            camera_substituta=self.estoque,
            motivo="Falha fisica confirmada",
            usuario=self.user,
        )

        response = self.client.get(
            reverse("cameras:lista_substituicoes"),
            {
                "q": "Falha",
                "data_inicial": "2020-01-01",
                "data_final": "2999-01-01",
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
            ("q", "Falha", "Pesquisa", "Falha"),
            filtros,
        )
        self.assertIn(
            (
                "data_inicial",
                "2020-01-01",
                "De",
                "01/01/2020",
            ),
            filtros,
        )
        self.assertIn(
            (
                "data_final",
                "2999-01-01",
                "Até",
                "01/01/2999",
            ),
            filtros,
        )

    def test_lista_substituicoes_renderiza_remocao_individual_e_periodo_invalido(self):
        self.grupo("Operador ARGOS")
        substituir_camera(
            camera_anterior=self.camera,
            camera_substituta=self.estoque,
            motivo="Falha fisica confirmada",
            usuario=self.user,
        )

        response = self.client.get(
            reverse("cameras:lista_substituicoes"),
            {
                "q": "CAM",
                "data_inicial": "invalida",
                "page": "2",
            },
        )

        self.assertTrue(response.context["periodo_invalido"])
        self.assertContains(
            response,
            'aria-label="Filtros ativos"',
        )
        self.assertContains(
            response,
            "Remover filtro Pesquisa: CAM",
        )
        self.assertContains(
            response,
            "Remover filtro De: invalida",
        )
        self.assertContains(
            response,
            'href="?q=CAM"',
        )
        self.assertContains(
            response,
            'href="?data_inicial=invalida"',
        )
        self.assertContains(
            response,
            "Limpar todos",
        )
        self.assertContains(
            response,
            'role="alert"',
        )
        self.assertContains(
            response,
            "Informe um período válido.",
        )

    def test_lista_substituicoes_sem_filtros_nao_renderiza_filtros_ativos(self):
        self.grupo("Operador ARGOS")

        response = self.client.get(
            reverse("cameras:lista_substituicoes")
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["filtros_ativos"], [])
        self.assertNotContains(
            response,
            'aria-label="Filtros ativos"',
        )

    def test_lista_substituicoes_data_final_invalida_mantem_contrato(self):
        self.grupo("Operador ARGOS")
        substituir_camera(
            camera_anterior=self.camera,
            camera_substituta=self.estoque,
            motivo="Falha fisica confirmada",
            usuario=self.user,
        )

        response = self.client.get(
            reverse("cameras:lista_substituicoes"),
            {
                "q": "CAM",
                "data_final": "invalida",
                "page": "2",
            },
        )

        self.assertTrue(response.context["periodo_invalido"])
        self.assertEqual(
            response.context["page_obj"].paginator.count,
            1,
        )
        self.assertContains(
            response,
            "Remover filtro Até: invalida",
        )
        self.assertContains(
            response,
            'href="?q=CAM"',
        )

    def test_lista_substituicoes_periodo_valido_nao_exibe_alerta(self):
        self.grupo("Operador ARGOS")
        substituir_camera(
            camera_anterior=self.camera,
            camera_substituta=self.estoque,
            motivo="Falha fisica confirmada",
            usuario=self.user,
        )

        response = self.client.get(
            reverse("cameras:lista_substituicoes"),
            {
                "data_inicial": "2020-01-01",
                "data_final": "2999-01-01",
            },
        )

        self.assertFalse(response.context["periodo_invalido"])
        self.assertNotContains(
            response,
            "Informe um período válido.",
        )

    def test_lista_substituicoes_paginacao_preserva_filtros(self):
        self.grupo("Operador ARGOS")

        for indice in range(51):
            anterior = self.criar(
                3 + indice * 2,
                "PRODUCAO",
            )
            substituta = self.criar(
                4 + indice * 2,
                "ESTOQUE",
            )
            substituir_camera(
                camera_anterior=anterior,
                camera_substituta=substituta,
                motivo="Filtro paginacao",
                usuario=self.user,
            )

        response = self.client.get(
            reverse("cameras:lista_substituicoes"),
            {
                "q": "Filtro paginacao",
                "data_inicial": "2020-01-01",
                "data_final": "2999-01-01",
                "page": "2",
            },
        )

        self.assertEqual(response.context["page_obj"].number, 2)

        html = response.content.decode()
        indice_page = html.index("page=1")
        inicio_href = html.rfind('href="', 0, indice_page) + len('href="')
        fim_href = html.index('"', inicio_href)
        href = html[inicio_href:fim_href].replace("&amp;", "&")

        self.assertIn("q=Filtro+paginacao", href)
        self.assertIn("data_inicial=2020-01-01", href)
        self.assertIn("data_final=2999-01-01", href)
        self.assertIn("page=1", href)
        self.assertEqual(href.count("page="), 1)

    def test_lista_substituicoes_canoniza_q_descarta_desconhecido_e_preserva_datas(self):
        self.grupo("Operador ARGOS")

        for indice in range(51):
            anterior = self.criar(100 + indice * 2, "PRODUCAO")
            substituta = self.criar(101 + indice * 2, "ESTOQUE")
            substituir_camera(
                camera_anterior=anterior,
                camera_substituta=substituta,
                motivo="Filtro canonico",
                usuario=self.user,
            )

        response = self.client.get(
            reverse("cameras:lista_substituicoes"),
            {
                "q": "  Filtro canonico  ",
                "data_inicial": "2999-01-02",
                "data_final": "2999-01-01",
                "foo": "bar",
                "page": ["2", "3"],
            },
        )
        html = response.content.decode("utf-8").replace("&amp;", "&")

        self.assertEqual(response.context["q"], "Filtro canonico")
        self.assertTrue(response.context["periodo_invalido"])
        self.assertIn("data_inicial=2999-01-02", html)
        self.assertIn("data_final=2999-01-01", html)
        self.assertNotIn("foo=bar", html)
        self.assertEqual(html.count("page="), 1)

    def test_historico_local_permanece_sem_interface_de_filtros(self):
        self.grupo("Operador ARGOS")
        substituir_camera(
            camera_anterior=self.camera,
            camera_substituta=self.estoque,
            motivo="Falha fisica confirmada",
            usuario=self.user,
        )

        response = self.client.get(
            reverse(
                "cameras:lista_substituicoes_camera",
                args=[self.camera.pk],
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(
            response,
            'class="replacement-filters"',
        )
        self.assertNotContains(
            response,
            'aria-label="Filtros ativos"',
        )

    def test_historico_local_exibe_apenas_substituicoes_da_camera(self):
        self.grupo("Operador ARGOS")

        relacionada = substituir_camera(
            camera_anterior=self.camera,
            camera_substituta=self.estoque,
            motivo="Substituição relacionada",
            usuario=self.user,
        )

        outra_anterior = self.criar(3, "PRODUCAO")
        outra_substituta = self.criar(4, "ESTOQUE")

        nao_relacionada = substituir_camera(
            camera_anterior=outra_anterior,
            camera_substituta=outra_substituta,
            motivo="Substituição de outra câmera",
            usuario=self.user,
        )

        response = self.client.get(
            reverse(
                "cameras:lista_substituicoes_camera",
                args=[self.camera.pk],
            )
        )

        self.assertEqual(response.status_code, 200)

        self.assertContains(
            response,
            f"<title>Histórico de substituições — {self.camera.nome} — ARGOS</title>",
            html=True,
        )

        self.assertContains(
            response,
            relacionada.motivo,
        )

        self.assertNotContains(
            response,
            nao_relacionada.motivo,
        )

        self.assertEqual(
            response.context["total_substituicoes"],
            1,
        )

    def test_historico_local_identifica_camera_como_substituta(self):
        self.grupo("Operador ARGOS")

        substituir_camera(
            camera_anterior=self.camera,
            camera_substituta=self.estoque,
            motivo="Falha física confirmada",
            usuario=self.user,
        )

        response = self.client.get(
            reverse(
                "cameras:lista_substituicoes_camera",
                args=[self.estoque.pk],
            )
        )

        self.assertContains(
            response,
            'data-replacement-role="substituta"',
            html=False,
        )

        self.assertContains(
            response,
            "Entrou como substituta",
        )

    def test_historico_local_camera_intermediaria_exibe_os_dois_papeis(self):
        self.grupo("Operador ARGOS")

        substituir_camera(
            camera_anterior=self.camera,
            camera_substituta=self.estoque,
            motivo="Primeira substituição",
            usuario=self.user,
        )

        terceira = self.criar(
            3,
            "ESTOQUE",
        )

        substituir_camera(
            camera_anterior=self.estoque,
            camera_substituta=terceira,
            motivo="Segunda substituição",
            usuario=self.user,
        )

        response = self.client.get(
            reverse(
                "cameras:lista_substituicoes_camera",
                args=[self.estoque.pk],
            )
        )

        self.assertContains(
            response,
            'data-replacement-role="substituta"',
            count=1,
            html=False,
        )

        self.assertContains(
            response,
            'data-replacement-role="anterior"',
            count=1,
            html=False,
        )

        self.assertContains(
            response,
            "Entrou como substituta",
        )

        self.assertContains(
            response,
            "Foi substituída",
        )

    def test_detalhe_camera_aponta_para_historico_local(self):
        self.grupo("Operador ARGOS")

        response = self.client.get(
            reverse(
                "cameras:detalhe",
                args=[self.camera.pk],
            )
        )

        url = reverse(
            "cameras:lista_substituicoes_camera",
            args=[self.camera.pk],
        )

        self.assertContains(
            response,
            url,
        )

        self.assertContains(
            response,
            "Ver histórico completo",
        )

        self.assertNotContains(
            response,
            "Ver todas as substituições",
        )

    def test_admin_substituicao_nao_permite_adicionar_editar_ou_excluir(self): a=SubstituicaoCameraAdmin(SubstituicaoCamera,admin.site); req=RequestFactory().get("/"); req.user=self.superuser; self.assertFalse(a.has_add_permission(req)); self.assertFalse(a.has_change_permission(req)); self.assertFalse(a.has_delete_permission(req))
    def test_dashboard_exibe_situacoes_completude_e_ips_duplicados(self): self.criar(3,"ESTOQUE",ip=self.camera.ip); self.client.force_login(self.superuser); r=self.client.get(reverse("core:dashboard")); self.assertContains(r,"Produção"); self.assertContains(r,"Cadastro completo"); self.assertContains(r,"IP duplicado")
    def test_grupos_possuem_matriz_de_governanca_sem_delete(self):
        op=Group.objects.get(name="Operador ARGOS"); cod=set(op.permissions.filter(content_type__app_label="cameras").values_list("codename",flat=True)); self.assertIn("registrar_substituicao_camera",cod); self.assertFalse(any(x.startswith("delete_") for x in cod))
