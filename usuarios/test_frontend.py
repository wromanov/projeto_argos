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

    def test_login_exibe_identidade_labels_autocomplete_e_acesso_restrito(self):
        response = self.client.get(self.login_url)
        for texto in ("ARGOS", "Sistema de Inventário", "Acesso restrito", "Usuário", "Senha", "Entrar"):
            self.assertContains(response, texto)
        self.assertContains(response, 'autocomplete="username"')
        self.assertContains(response, 'autocomplete="current-password"')

    def test_login_invalido_exibe_erro_acessivel_sem_dados_sensiveis(self):
        response = self.client.post(self.login_url, {"username": "usuario", "password": "senha-invalida"})
        self.assertContains(response, 'role="alert"')
        self.assertContains(response, "Usuário ou senha inválidos.")
        self.assertNotContains(response, "senha-invalida")
        self.assertNotContains(response, "não existe")
