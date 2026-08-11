from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class LoginFrontendTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="usuario", password="senha-forte")
        self.login_url = reverse("usuarios:login")

    def test_login_carrega_design_system_e_css_de_autenticacao(self):
        response = self.client.get(self.login_url)
        self.assertContains(response, "css/design-system.css")
        self.assertContains(response, "css/autenticacao.css")
        self.assertEqual(response.content.count(b"css/design-system.css"), 1)

    def test_login_consumes_brand_shared_and_preserves_identity(self):
        response = self.client.get(self.login_url)
        for texto in ("ARGOS", "Sistema de Inventário e Monitoramento de Câmeras", "Acesso restrito", "Usuário", "Senha", "Entrar"):
            self.assertContains(response, texto)
        self.assertContains(response, 'class="argos-brand"')
        self.assertContains(response, 'class="argos-brand__icon"')
        self.assertContains(response, 'class="argos-brand__subtitle"')
        self.assertContains(response, "argos-icon.svg")
        self.assertContains(response, 'aria-hidden="true"')
        self.assertContains(response, 'alt=""')
        self.assertNotContains(response, '<a class="argos-brand"')
        self.assertNotContains(response, 'class="auth-brand"')
        self.assertNotContains(response, 'class="auth-brand__symbol"')
        self.assertContains(response, 'autocomplete="username"')
        self.assertContains(response, 'autocomplete="current-password"')

    def test_login_preserves_form_and_accessible_error_contract(self):
        response = self.client.get(self.login_url)
        self.assertContains(response, '<form method="post" class="auth-form">', html=False)
        self.assertContains(response, 'name="username"')
        self.assertContains(response, 'name="password"')
        self.assertContains(response, 'autocomplete="username"')
        self.assertContains(response, 'autocomplete="current-password"')

        response = self.client.post(self.login_url, {"username": "usuario", "password": "senha-invalida"})
        self.assertContains(response, 'role="alert"')
        self.assertContains(response, "Usuário ou senha inválidos.")
        self.assertNotContains(response, "senha-invalida")
        self.assertNotContains(response, "não existe")
