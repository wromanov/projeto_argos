from io import StringIO

from django import forms
from django.contrib.staticfiles import finders
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management import call_command
from django.core.paginator import Paginator
from django.http import QueryDict
from django.template import RequestContext
from django.template.loader import render_to_string
from django.templatetags.static import static
from django.urls import reverse
from django.test import RequestFactory, SimpleTestCase, TestCase
from django.utils.html import format_html

from cameras.models import Camera
from core.templatetags.ui_extras import querystring


class BrandComponentTests(SimpleTestCase):
    template_name = "components/brand.html"

    def render_brand(self, **context):
        return render_to_string(self.template_name, context)

    def test_renderizacao_basica_exibe_nome_e_simbolo_institucional(self):
        html = self.render_brand()

        self.assertIn("ARGOS", html)
        self.assertIn("argos-icon.svg", html)
        self.assertIn('class="argos-brand"', html)

    def test_subtitle_e_opcional(self):
        com_subtitle = self.render_brand(subtitle="Central operacional")
        sem_subtitle = self.render_brand()

        self.assertIn("Central operacional", com_subtitle)
        self.assertIn('class="argos-brand__subtitle"', com_subtitle)
        self.assertNotIn("argos-brand__subtitle", sem_subtitle)

    def test_href_torna_marca_um_link(self):
        html = self.render_brand(href="/inicio/")

        self.assertIn('<a class="argos-brand" href="/inicio/">', html)
        self.assertNotIn('<div class="argos-brand">', html)

    def test_sem_href_nao_cria_link_artificial(self):
        html = self.render_brand()

        self.assertIn('<div class="argos-brand">', html)
        self.assertNotIn("<a ", html)

    def test_simbolo_e_decorativo_e_nome_permanece_disponivel(self):
        html = self.render_brand()

        self.assertIn('aria-hidden="true"', html)
        self.assertIn('alt=""', html)
        self.assertIn("ARGOS", html)


class FrontendSharedComponentsTests(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def render_field(self, field):
        return render_to_string("components/campo_formulario.html", {"field": field})

    def test_campo_formulario_renderiza_help_textual_em_conteiner_compartilhado(self):
        class Formulario(forms.Form):
            nome = forms.CharField(help_text="Informe seu nome.")

        html = self.render_field(Formulario()["nome"])

        self.assertIn('class="field-help"', html)
        self.assertIn('id="id_nome_help"', html)
        self.assertIn("Informe seu nome.", html)
        self.assertIn('aria-describedby="id_nome_help"', html)

    def test_campo_formulario_renderiza_help_estruturado_fora_de_paragrafo(self):
        class Formulario(forms.Form):
            senha = forms.CharField(
                help_text=format_html(
                    "<ul><li>{}</li></ul>",
                    "Use uma senha longa.",
                )
            )

        html = self.render_field(Formulario()["senha"])

        self.assertIn("<ul>", html)
        self.assertIn("<li>Use uma senha longa.</li>", html)
        self.assertIn('id="id_senha_help"', html)
        self.assertIn('aria-describedby="id_senha_help"', html)
        self.assertNotRegex(html, r'<p\b[^>]*class="field-help"')
        self.assertNotRegex(html, r'<p\b[^>]*>\s*<ul>')

    def test_campo_formulario_preserva_escaping_para_help_text_nao_seguro(self):
        class Formulario(forms.Form):
            nome = forms.CharField(help_text='<script>alert("x")</script>')

        html = self.render_field(Formulario()["nome"])

        self.assertIn("&lt;script&gt;alert(&quot;x&quot;)&lt;/script&gt;", html)
        self.assertNotIn("<script>", html)

    def test_campo_formulario_preserva_aria_de_erro_e_help(self):
        class Formulario(forms.Form):
            nome = forms.CharField(help_text="Informe seu nome.")

        formulario = Formulario(data={"nome": ""})
        self.assertFalse(formulario.is_valid())
        html = self.render_field(formulario["nome"])

        self.assertIn('aria-invalid="true"', html)
        self.assertIn('aria-errormessage="id_nome_errors"', html)
        self.assertIn('aria-describedby="id_nome_help id_nome_errors"', html)
        self.assertIn('id="id_nome_errors"', html)

    def test_design_system_e_encontrado_pelo_staticfiles(self):
        self.assertIsNotNone(finders.find("css/design-system.css"))

    def test_design_system_concentra_primitives_de_formulario_compartilhadas(self):
        css = open("static/css/design-system.css", encoding="utf-8").read()

        for seletor in (
            ".form-section",
            ".form-grid",
            ".field__label",
            ".field-help",
            ".field-errors .errorlist",
            ".form-errors-summary h2",
            ".form-actions",
            ".field :is(input, select, textarea)[aria-invalid=\"true\"]",
            ".field :is(input, select, textarea):disabled",
        ):
            self.assertIn(seletor, css)

    def test_querystring_preserva_filtros_e_substitui_pagina(self):
        request = self.factory.get("/cameras/", {"q": "TPS2", "situacao_operacional": "PRODUCAO", "page": "1"})
        original = request.GET.copy()
        resultado = querystring(RequestContext(request), page=2)
        query = QueryDict(resultado)
        self.assertEqual(query["q"], "TPS2")
        self.assertEqual(query["situacao_operacional"], "PRODUCAO")
        self.assertEqual(query["page"], "2")
        self.assertEqual(request.GET, original)

    def test_querystring_remove_parametro_quando_valor_e_none(self):
        request = self.factory.get("/cameras/", {"q": "TPS2", "page": "1"})
        query = QueryDict(querystring(RequestContext(request), page=None))
        self.assertEqual(query["q"], "TPS2")
        self.assertNotIn("page", query)

    def test_partial_paginacao_preserva_filtros_e_possui_navegacao_acessivel(self):
        request = self.factory.get("/cameras/", {"q": "TPS2", "situacao_operacional": "PRODUCAO", "page": "2"})
        page_obj = Paginator(range(30), 10).page(2)
        html = render_to_string("components/paginacao.html", {"page_obj": page_obj}, request=request)
        self.assertIn('aria-label="Paginação"', html)
        self.assertIn('aria-current="page"', html)
        self.assertIn("q=TPS2", html)
        self.assertIn("Anterior", html)
        self.assertIn("Próxima", html)

    def test_partial_estado_vazio_renderiza_texto_e_acao_opcional(self):
        html = render_to_string("components/estado_vazio.html", {"empty_title": "Sem câmeras", "empty_text": "Cadastre um equipamento.", "empty_action_url": "/nova/", "empty_action_label": "Cadastrar"})
        self.assertIn("Sem câmeras", html)
        self.assertIn("Cadastre um equipamento.", html)
        self.assertIn('href="/nova/"', html)
        sem_acao = render_to_string("components/estado_vazio.html", {"empty_title": "Sem dados", "empty_text": "Não há itens."})
        self.assertNotIn('href=""', sem_acao)

    def test_partial_resumo_erros_exibe_alerta_sem_valor_sensivel(self):
        class Formulario(forms.Form):
            senha = forms.CharField(label="Senha", min_length=20)
        form = Formulario({"senha": "segredo-curto"})
        self.assertFalse(form.is_valid())
        html = render_to_string("components/resumo_erros_formulario.html", {"form": form})
        self.assertIn('role="alert"', html)
        self.assertIn("Senha", html)
        self.assertIn("Certifique-se", html)
        self.assertNotIn("segredo-curto", html)

class BaseAndPortalFrontendTests(TestCase):
    def setUp(self):
        call_command("configurar_perfis_argos", stdout=StringIO())
        self.user = get_user_model().objects.create_user(username="frontend", password="senha-forte")

    def login_monitoramento(self):
        self.user.groups.set([Group.objects.get(name="Monitoramento ARGOS")])
        self.client.force_login(self.user)

    def test_base_possui_skip_link_main_mensagens_e_logout_post(self):
        self.login_monitoramento()
        response = self.client.get(reverse("core:inicio"))
        self.assertContains(response, '<title>Início — ARGOS</title>')
        self.assertContains(response, f'href="{static("img/brand/favicon.ico")}"')
        self.assertContains(response, 'href="#conteudo-principal"')
        self.assertContains(response, 'id="conteudo-principal"')
        self.assertContains(response, 'class="app-shell"')
        self.assertContains(response, 'class="app-layout"')
        self.assertContains(response, 'class="app-sidebar"')
        self.assertContains(response, 'class="app-topbar"')
        self.assertNotContains(response, 'class="app-sidebar__user"')
        self.assertContains(response, 'class="user-menu"')
        self.assertContains(response, 'class="page-container app-shell__main"')
        self.assertContains(response, 'aria-live="polite"')
        self.assertContains(response, '<form method="post" action="/logout/"', html=False)
        self.assertContains(response, "csrfmiddlewaretoken")
        self.assertNotContains(response, 'href="/logout/"')

    def test_navegacao_marca_pagina_atual_e_css_movel_nao_oculta_menu(self):
        self.login_monitoramento()
        inicio = self.client.get(reverse("core:inicio"))
        dashboard = self.client.get(reverse("core:dashboard"))
        self.assertEqual(inicio.content.count(b'aria-current="page"'), 1)
        self.assertEqual(dashboard.content.count(b'aria-current="page"'), 1)
        self.assertContains(dashboard, 'aria-label="Navegação principal"')
        css = open("static/css/argos.css", encoding="utf-8").read()
        self.assertNotRegex(css, r"\.main-navigation\s*\{\s*display:\s*none")
        self.assertIn("@media (max-width: 44rem)", css)
        self.assertIn(".main-navigation", css)
        self.assertIn("overflow-x: auto", css)

    def test_ui_v2_hom_01_e_carregado_somente_nas_rotas_autorizadas(self):
        self.login_monitoramento()
        inicio = self.client.get(reverse("core:inicio"))
        dashboard = self.client.get(reverse("core:dashboard"))
        inventario = self.client.get(reverse("cameras:lista"))

        for response in (dashboard, inventario):
            self.assertContains(response, 'class="app-shell argos-ui-v2-production"')
            self.assertContains(response, 'href="/static/css/ui-v2/hom-01-2.4.0/production.css"')
            self.assertContains(response, 'aria-describedby="argos-nav-scroll-hint"')
        for response in (inicio,):
            self.assertContains(response, 'class="app-shell"')
            self.assertNotContains(response, "argos-ui-v2-production")
            self.assertNotContains(response, "/static/css/ui-v2/production.css")
            self.assertNotContains(response, "argos-nav-scroll-hint")
        self.assertContains(dashboard, 'href="/static/css/dashboard-v7.css"')
        self.assertNotContains(inventario, "/static/css/dashboard-v7.css")

    def test_inicio_exibe_cartoes_permitidos_com_links_unicos_e_acessiveis(self):
        self.login_monitoramento()
        response = self.client.get(reverse("core:inicio"))
        for nome, url in (("Inventário", reverse("cameras:lista")), ("Dashboard", reverse("core:dashboard")), ("Eventos", reverse("eventos:lista")), ("Meu Perfil", reverse("usuarios:perfil"))):
            self.assertContains(response, nome)
            self.assertEqual(response.content.count((f'class="module-card" href="{url}"').encode()), 1)
        self.assertContains(response, 'class="module-card"')
        self.assertContains(response, 'aria-hidden="true"')
        self.assertNotContains(response, "Credenciais")
        self.assertNotContains(response, "RTSP")

    def test_dashboard_separa_inventario_monitoramento_e_qualidade(self):
        self.login_monitoramento()
        response = self.client.get(reverse("core:dashboard"))
        self.assertContains(response, 'class="argos-page-title page-heading__title"')
        self.assertContains(response, 'class="argos-eyebrow page-heading__eyebrow"')
        self.assertContains(response, 'id="inventario-heading"')
        self.assertContains(response, 'id="dashboard-monitoring-title"')
        self.assertContains(response, 'id="dashboard-quality-title"')
        self.assertContains(response, "Monitoramento e completude")
        self.assertContains(response, "Total de câmeras")
        self.assertContains(response, "Cadastros completos")
        self.assertContains(response, "Online")
        self.assertContains(response, "Frescor dos dados")
        for label in ("Estado técnico efetivo", "Indisponibilidade detectada", "Fora do escopo técnico", "Estados técnicos das câmeras", "Câmeras exibidas"):
            self.assertContains(response, label)
        self.assertContains(response, "Câmeras com IP duplicado")
        self.assertEqual(response.content.count(b'class="dashboard-v7__surface dashboard-v7__activity-grid"'), 1)
        self.assertEqual(response.content.count(b'class="dashboard-v7__activity-panel"'), 2)
        self.assertNotContains(response, 'class="dashboard-v7__surface dashboard-v7__activity-panel"')

    def test_dashboard_mantem_as_cinco_cameras_recentes(self):
        self.login_monitoramento()
        for index in range(6):
            Camera.objects.create(nome=f"CAM-RECENTE-{index}", fabricante="Axis", modelo="QA")

        response = self.client.get(reverse("core:dashboard"))

        self.assertEqual(response.content.count(b'class="dashboard-v7__recent-item"'), 5)
        self.assertContains(response, "Câmeras atualizadas recentemente")
        self.assertEqual(len(response.context["cameras_recentes"]), 5)

    def test_cards_dashboard_usam_filtros_existentes(self):
        self.login_monitoramento()
        response = self.client.get(reverse("core:dashboard"))
        for parametro in (
            "situacao_operacional=PRODUCAO",
            "situacao_operacional=ESTOQUE",
            "situacao_operacional=DESATIVADA",
            "completude=COMPLETO",
            "completude=INCOMPLETO",
        ):
            self.assertContains(response, parametro)
        self.assertContains(response, "Ver câmeras", count=3)
        for label in ("Monitoramento e completude", "Online", "Offline", "Desconhecido", "Não monitorada"):
            self.assertContains(response, label)
        self.assertNotContains(response, 'href="/cameras/?ip_duplicado=')

    def test_base_compoe_componentes_globais(self):
        self.login_monitoramento()
        response = self.client.get(reverse("core:inicio"))
        for template_name in (
            "components/cabecalho.html",
            "components/sidebar.html",
            "components/brand.html",
            "components/navegacao_principal.html",
            "components/menu_usuario.html",
            "components/mensagens.html",
        ):
            self.assertTemplateUsed(response, template_name)
        self.assertContains(response, 'class="main-navigation"')
        self.assertContains(response, '<form method="post" action="/logout/"', html=False)

    def test_sidebar_consumes_brand_shared_and_preserves_identity(self):
        self.login_monitoramento()
        response = self.client.get(reverse("core:inicio"))

        self.assertContains(response, 'class="argos-brand"')
        self.assertContains(response, 'class="argos-brand__icon"')
        self.assertContains(response, "argos-icon.svg")
        self.assertContains(response, "ARGOS")
        self.assertContains(response, "Central operacional")
        self.assertContains(
            response,
            f'href="{reverse("core:inicio")}"',
        )
        self.assertNotContains(response, 'class="brand"')
        self.assertNotContains(response, 'class="brand__symbol"')

    def test_sidebar_preserva_links_condicionais_por_permissao(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("core:inicio"))

        self.assertContains(response, 'class="app-sidebar"')
        self.assertContains(
            response,
            f'href="{reverse("core:inicio")}"',
        )
        self.assertNotContains(response, 'href="/dashboard/"')
        self.assertNotContains(response, 'href="/cameras/"')
        self.assertNotContains(response, 'href="/eventos/"')

    def test_dashboard_diferencia_cards_clicaveis_e_informativos(self):
        self.login_monitoramento()
        response = self.client.get(reverse("core:dashboard"))
        html = response.content.decode()
        self.assertIn('class="dashboard-v7__inventory-total"', html)
        self.assertIn('<strong>0</strong><span class="dashboard-v7__metric-caption">Câmeras cadastradas</span>', html)
        self.assertIn('href="/cameras/?situacao_operacional=PRODUCAO"', html)
        self.assertIn('href="/cameras/?situacao_operacional=ESTOQUE"', html)
        self.assertIn("<dt>Câmeras com IP duplicado</dt><dd>0</dd>", html)
        self.assertIn("Câmeras exibidas <strong>0</strong>", html)
        self.assertIn("Frescor dos dados", html)
        self.assertIn("0 câmeras com dados desatualizados", html)
        self.assertNotIn('href="/cameras/?ip_duplicado=', html)
