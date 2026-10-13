import re
from pathlib import Path

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from cameras.models import Camera, SubstituicaoCamera


class SidebarActiveStateTests(TestCase):
    """Exercise the integrated routes, including the Inventory/Governance split."""

    def setUp(self):
        user = get_user_model().objects.create_superuser(
            username="sidebar-qa", password="test-only-password"
        )
        self.client.force_login(user)
        anterior = Camera.objects.create(nome="Anterior", fabricante="Teste", modelo="A")
        substituta = Camera.objects.create(nome="Substituta", fabricante="Teste", modelo="B")
        self.substituicao = SubstituicaoCamera.objects.create(
            camera_anterior=anterior,
            camera_substituta=substituta,
            motivo="Teste de navegação",
            nome_operacional="Câmera de teste",
            nome_anterior_substituta="Substituta anterior",
            registrado_por=user,
        )

    def test_five_routes_have_exactly_the_corresponding_active_link(self):
        for route in (
            "core:inicio", "core:dashboard", "cameras:lista",
            "cameras:lista_substituicoes", "cameras:detalhe_substituicao",
            "eventos:lista",
        ):
            with self.subTest(route=route):
                kwargs = {"args": [self.substituicao.pk]} if route == "cameras:detalhe_substituicao" else {}
                response = self.client.get(reverse(route, **kwargs))
                self.assertEqual(response.status_code, 200)
                navigation = re.search(
                    r'<nav\b[^>]*aria-label="Navegação principal"[^>]*>(.*?)</nav>',
                    response.content.decode(), re.S,
                ).group(1)
                links = re.findall(r"<a\b[^>]*>", navigation)
                self.assertEqual(len(links), 5)
                active = [link for link in links if 'aria-current="page"' in link]
                self.assertEqual(len(active), 1)
                active_target = "cameras:lista_substituicoes" if route == "cameras:detalhe_substituicao" else route
                self.assertIn(f'href="{reverse(active_target)}"', active[0])

    def test_navigation_adapter_is_selective_and_preserves_reference_routes(self):
        for route in (
            "core:inicio", "core:dashboard", "cameras:lista",
            "cameras:lista_substituicoes", "cameras:detalhe_substituicao",
            "eventos:lista",
        ):
            with self.subTest(route=route):
                kwargs = {"args": [self.substituicao.pk]} if route == "cameras:detalhe_substituicao" else {}
                response = self.client.get(reverse(route, **kwargs))
                reference = route in ("core:dashboard", "cameras:lista")
                adapter = 'href="/static/css/sidebar-active-recovery.css"'
                production = 'href="/static/css/ui-v2/hom-01-2.4.0/production.css"'
                if reference:
                    self.assertContains(response, production)
                    self.assertNotContains(response, adapter)
                    self.assertNotContains(response, 'data-argos-sidebar-visual="hom-01"')
                else:
                    self.assertContains(response, adapter)
                    self.assertNotContains(response, production)
                    self.assertContains(response, 'data-argos-sidebar-visual="hom-01"')
                    self.assertNotContains(response, "argos-ui-v2-production")

    def test_sidebar_adapter_matches_canonical_values_and_responsive_breakpoints(self):
        css = Path("static/css/sidebar-active-recovery.css").read_text(encoding="utf-8")
        for declaration in (
            "grid-template-columns: 232px minmax(0, 1fr)",
            "grid-template-columns: 190px minmax(0, 1fr)",
            "padding: 20px 16px",
            "background: var(--argos-color-surface-inverse, #182c3a)",
            "color: var(--argos-color-ink-inverse-muted, #d0dbe3)",
            "min-height: 40px",
            "padding: 8px 12px",
            "border-radius: 5px",
            "background: var(--argos-color-action, #2563a6)",
            "min-height: 44px",
            "padding: 12px",
            "outline: 3px solid var(--argos-color-ink-inverse, #ffffff)",
            "outline-offset: 2px",
            "scrollbar-width: auto",
            "scrollbar-color: var(--argos-color-action, #2563a6) var(--argos-color-surface-inverse, #182c3a)",
            "scroll-behavior: auto",
        ):
            with self.subTest(declaration=declaration):
                self.assertIn(declaration, css)
        self.assertIn("@media (max-width: 900px)", css)
        self.assertIn("@media (max-width: 680px)", css)
        self.assertIn("@media (prefers-reduced-motion: reduce)", css)
        self.assertIn("::-webkit-scrollbar {\n        height: 7px;", css)
