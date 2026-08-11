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
from django.urls import reverse
from django.test import RequestFactory, SimpleTestCase, TestCase

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

    def test_design_system_e_encontrado_pelo_staticfiles(self):
        self.assertIsNotNone(finders.find("css/design-system.css"))

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
        self.assertContains(response, 'class="page-heading__title"')
        self.assertContains(response, 'class="page-heading__eyebrow"')
        self.assertEqual(response.content.count(b'class="section-heading__eyebrow"'), 4)
        self.assertEqual(response.content.count(b'class="section-heading__title"'), 4)
        self.assertContains(response, 'id="inventario-heading"')
        self.assertContains(response, "Monitoramento técnico")
        self.assertContains(response, "Qualidade cadastral")
        self.assertContains(response, "Produção")
        self.assertContains(response, "Online")
        self.assertContains(response, "Cadastro completo")

    def test_cards_dashboard_usam_filtros_existentes(self):
        self.login_monitoramento()
        response = self.client.get(reverse("core:dashboard"))
        for parametro in (
            "situacao_operacional=PRODUCAO",
            "situacao_operacional=ESTOQUE",
            "situacao_operacional=DESATIVADA",
            "status=ONLINE",
            "status=OFFLINE",
            "status=NAO_VERIFICADO",
            "completude=COMPLETO",
            "completude=INCOMPLETO",
        ):
            self.assertContains(response, parametro)
        self.assertNotContains(response, 'href="/cameras/?ip_duplicado=')

    def test_base_compoe_componentes_globais(self):
        self.login_monitoramento()
        response = self.client.get(reverse("core:inicio"))
        for template_name in (
            "components/cabecalho.html",
            "components/sidebar.html",
            "components/navegacao_principal.html",
            "components/menu_usuario.html",
            "components/mensagens.html",
        ):
            self.assertTemplateUsed(response, template_name)
        self.assertContains(response, 'class="main-navigation"')
        self.assertContains(response, '<form method="post" action="/logout/"', html=False)

    def test_sidebar_preserva_links_condicionais_por_permissao(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("core:inicio"))

        self.assertContains(response, 'class="app-sidebar"')
        self.assertContains(response, 'href="/"')
        self.assertNotContains(response, 'href="/dashboard/"')
        self.assertNotContains(response, 'href="/cameras/"')
        self.assertNotContains(response, 'href="/eventos/"')

    def test_dashboard_diferencia_cards_clicaveis_e_informativos(self):
        self.login_monitoramento()
        response = self.client.get(reverse("core:dashboard"))
        html = response.content.decode()
        self.assertIn('class="metric-card metric-card--link dashboard-metric"', html)
        self.assertIn('<article class="metric-card dashboard-metric"><span>Total de câmeras</span>', html)
        self.assertIn('<article class="metric-card dashboard-metric"><span>Câmeras com IP duplicado</span>', html)
        self.assertNotIn('<a class="metric-card metric-card--link dashboard-metric"><a ', html)
