import re

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse


class GovernancaNavigationTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="teste-governanca-nav",
            password="teste",
        )

        permissoes = Permission.objects.filter(
            content_type__app_label="cameras",
            codename__in=(
                "view_camera",
                "consultar_substituicoescamera",
            ),
        )

        self.user.user_permissions.add(*permissoes)
        self.client.force_login(self.user)

    def test_historico_global_pertence_a_governanca(self):
        response = self.client.get(
            reverse("cameras:lista_substituicoes")
        )

        self.assertEqual(response.status_code, 200)

        self.assertContains(
            response,
            "<strong>Governan\u00e7a</strong>",
            html=True,
        )

        governance_url = reverse(
            "cameras:lista_substituicoes"
        )

        inventory_url = reverse(
            "cameras:lista"
        )

        html = response.content.decode()

        self.assertRegex(
            html,
            re.compile(
                r'<a[^>]*href="'
                + re.escape(governance_url)
                + r'"[^>]*aria-current="page"[^>]*>',
                re.S,
            ),
        )

        self.assertNotRegex(
            html,
            re.compile(
                r'<a[^>]*href="'
                + re.escape(inventory_url)
                + r'"[^>]*aria-current="page"[^>]*>',
                re.S,
            ),
        )

    def test_inventario_continua_pertencendo_ao_inventario(self):
        response = self.client.get(
            reverse("cameras:lista")
        )

        self.assertEqual(response.status_code, 200)

        self.assertContains(
            response,
            "<strong>Invent\u00e1rio</strong>",
            html=True,
        )

        inventory_url = reverse(
            "cameras:lista"
        )

        governance_url = reverse(
            "cameras:lista_substituicoes"
        )

        html = response.content.decode()

        self.assertRegex(
            html,
            re.compile(
                r'<a[^>]*href="'
                + re.escape(inventory_url)
                + r'"[^>]*aria-current="page"[^>]*>',
                re.S,
            ),
        )

        self.assertNotRegex(
            html,
            re.compile(
                r'<a[^>]*href="'
                + re.escape(governance_url)
                + r'"[^>]*aria-current="page"[^>]*>',
                re.S,
            ),
        )

    def test_governanca_respeita_permissao_de_consulta(self):
        outro_usuario = get_user_model().objects.create_user(
            username="teste-sem-governanca",
            password="teste",
        )

        permissao = Permission.objects.get(
            content_type__app_label="cameras",
            codename="view_camera",
        )

        outro_usuario.user_permissions.add(permissao)

        self.client.force_login(outro_usuario)

        response = self.client.get(
            reverse("cameras:lista")
        )

        self.assertEqual(response.status_code, 200)

        governance_url = reverse(
            "cameras:lista_substituicoes"
        )

        self.assertNotContains(
            response,
            f'href="{governance_url}"',
        )



class GovernancaPortalTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="teste-governanca-portal",
            password="teste",
        )

    def test_portal_exibe_governanca_com_permissao(self):
        permissao = Permission.objects.get(
            content_type__app_label="cameras",
            codename="consultar_substituicoescamera",
        )

        self.user.user_permissions.add(permissao)
        self.client.force_login(self.user)

        response = self.client.get(
            reverse("core:inicio")
        )

        self.assertEqual(response.status_code, 200)

        governance_url = reverse(
            "cameras:lista_substituicoes"
        )

        self.assertContains(
            response,
            f'class="module-card" href="{governance_url}"',
        )

        self.assertContains(
            response,
            "Governan\u00e7a",
        )

        self.assertContains(
            response,
            "Consulte o hist\u00f3rico de substitui\u00e7\u00f5es de c\u00e2meras.",
        )

        self.assertNotContains(
            response,
            "Acesso operacional indispon\u00edvel",
        )

    def test_portal_oculta_governanca_sem_permissao(self):
        self.client.force_login(self.user)

        response = self.client.get(
            reverse("core:inicio")
        )

        self.assertEqual(response.status_code, 200)

        governance_url = reverse(
            "cameras:lista_substituicoes"
        )

        self.assertNotContains(
            response,
            f'class="module-card" href="{governance_url}"',
        )

        self.assertContains(
            response,
            "Acesso operacional indispon\u00edvel",
        )
