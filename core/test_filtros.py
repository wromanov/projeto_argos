from pathlib import Path

from django.http import QueryDict
from django.template import RequestContext
from django.template.loader import render_to_string
from django.test import RequestFactory, SimpleTestCase

from core.templatetags.ui_extras import (
    querystring,
    querystring_sem_valor,
)


class GlobalFilterInfrastructureTests(SimpleTestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_querystring_preserva_parametros_repetidos_ao_paginar(self):
        request = self.factory.get(
            "/cameras/",
            {
                "situacao_operacional": [
                    "PRODUCAO",
                    "ESTOQUE",
                ],
                "tipo": ["DOME"],
                "page": "1",
            },
        )

        resultado = QueryDict(
            querystring(
                RequestContext(request),
                page=2,
            )
        )

        self.assertEqual(
            resultado.getlist("situacao_operacional"),
            ["PRODUCAO", "ESTOQUE"],
        )

        self.assertEqual(
            resultado.getlist("tipo"),
            ["DOME"],
        )

        self.assertEqual(
            resultado["page"],
            "2",
        )

    def test_querystring_sem_valor_remove_apenas_valor_solicitado(self):
        request = self.factory.get(
            "/cameras/",
            {
                "situacao_operacional": [
                    "PRODUCAO",
                    "ESTOQUE",
                ],
                "tipo": ["DOME"],
                "page": "3",
            },
        )

        resultado = QueryDict(
            querystring_sem_valor(
                RequestContext(request),
                "situacao_operacional",
                "PRODUCAO",
            )
        )

        self.assertEqual(
            resultado.getlist("situacao_operacional"),
            ["ESTOQUE"],
        )

        self.assertEqual(
            resultado.getlist("tipo"),
            ["DOME"],
        )

        self.assertNotIn(
            "page",
            resultado,
        )

    def test_multisselecao_renderiza_checkboxes_e_estado_selecionado(self):
        html = render_to_string(
            "components/filtro_multisselecao.html",
            {
                "label": "Situacao operacional",
                "name": "situacao_operacional",
                "empty_label": "Todas",
                "opcoes": [
                    ("PRODUCAO", "Producao"),
                    ("ESTOQUE", "Estoque"),
                ],
                "selecionados": [
                    "PRODUCAO",
                    "ESTOQUE",
                ],
            },
        )

        self.assertIn(
            'data-filter-multiselect',
            html,
        )

        self.assertEqual(
            html.count('name="situacao_operacional"'),
            2,
        )

        self.assertEqual(
            html.count("checked"),
            2,
        )

        self.assertIn(
            "2 sele\u00e7\u00f5es",
            html,
        )

    def test_multisselecao_uma_opcao_exibe_rotulo_da_opcao(self):
        html = render_to_string(
            "components/filtro_multisselecao.html",
            {
                "label": "Status tecnico",
                "name": "status",
                "empty_label": "Todos",
                "opcoes": [
                    ("ONLINE", "Online"),
                    ("OFFLINE", "Offline"),
                ],
                "selecionados": ["ONLINE"],
            },
        )

        self.assertIn("Online", html)
        self.assertIn('value="ONLINE"', html)
        self.assertIn("checked", html)

    def test_filtros_ativos_renderizam_remocao_individual_e_limpeza_total(self):
        request = self.factory.get(
            "/cameras/",
            {
                "situacao_operacional": [
                    "PRODUCAO",
                    "ESTOQUE",
                ],
                "tipo": ["DOME"],
            },
        )

        html = render_to_string(
            "components/filtros_ativos.html",
            {
                "filtros_ativos": [
                    {
                        "nome": "situacao_operacional",
                        "valor": "PRODUCAO",
                        "grupo": "Situacao",
                        "rotulo": "Producao",
                    },
                    {
                        "nome": "tipo",
                        "valor": "DOME",
                        "grupo": "Tipo",
                        "rotulo": "Dome",
                    },
                ],
                "clear_url": "/cameras/",
            },
            request=request,
        )

        self.assertIn(
            'aria-label="Filtros ativos"',
            html,
        )

        self.assertIn(
            "Limpar todos",
            html,
        )

        self.assertIn(
            "Remover filtro Situacao: Producao",
            html,
        )

        self.assertIn(
            "situacao_operacional=ESTOQUE",
            html,
        )

        self.assertNotIn(
            "page=",
            html,
        )

    def test_javascript_global_de_filtros_e_progressivo(self):
        javascript = Path(
            "static/js/filtros.js"
        ).read_text(
            encoding="utf-8"
        )

        self.assertIn(
            "[data-filter-multiselect]",
            javascript,
        )

        self.assertIn(
            'input[type="checkbox"]',
            javascript,
        )

        self.assertNotIn(
            "fetch(",
            javascript,
        )
