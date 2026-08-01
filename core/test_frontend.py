from django import forms
from django.contrib.staticfiles import finders
from django.core.paginator import Paginator
from django.http import QueryDict
from django.template import RequestContext
from django.template.loader import render_to_string
from django.test import RequestFactory, SimpleTestCase

from core.templatetags.ui_extras import querystring


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
