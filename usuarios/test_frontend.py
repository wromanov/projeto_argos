from django.contrib.auth import get_user_model
from django.templatetags.static import static
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
        self.assertContains(response, "<title>Entrar — ARGOS</title>")
        self.assertContains(response, f'href="{static("img/brand/favicon.ico")}"')
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


class ProfileFormsFrontendTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="perfil-frontend",
            password="Senha-forte-123",
            first_name="Pessoa",
            last_name="Usuária",
            email="pessoa@example.com",
        )
        self.client.force_login(self.user)

    def test_editar_perfil_usa_renderer_e_resumos_compartilhados_para_os_dois_forms(self):
        response = self.client.get(reverse("usuarios:editar_perfil"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<fieldset class="form-section">', count=2)
        self.assertContains(response, 'class="field__label"', count=5)
        self.assertContains(response, 'name="first_name"')
        self.assertContains(response, 'name="telefone"')
        self.assertNotContains(response, 'class="profile-field"')
        self.assertContains(response, '<div class="form-actions">')
        self.assertNotContains(response, 'profile-form-actions')

        response = self.client.post(
            reverse("usuarios:editar_perfil"),
            {
                "first_name": "Pessoa",
                "last_name": "Usuária",
                "email": "invalido",
                "telefone": "11999990000",
                "ramal": "123",
            },
        )

        self.assertContains(response, 'role="alert"')
        self.assertContains(response, "Revise seus dados pessoais.")
        self.assertContains(response, 'href="#id_email"')
        self.assertContains(response, 'id="id_email_errors"')
        self.assertContains(response, 'aria-describedby="id_email_errors"')

    def test_alterar_senha_preserva_help_text_estruturado_e_aria(self):
        response = self.client.get(reverse("usuarios:alterar_senha"))
        html = response.content.decode()

        self.assertEqual(response.status_code, 200)
        for nome in ("old_password", "new_password1", "new_password2"):
            self.assertContains(response, f'name="{nome}"')
        self.assertIn('id="id_new_password1_help"', html)
        self.assertIn('aria-describedby="id_new_password1_help"', html)
        self.assertIn("<ul>", html)
        self.assertContains(response, '<div class="form-actions">')
        self.assertNotContains(response, 'profile-form-actions')
        self.assertNotRegex(html, r'<p\b[^>]*class="field-help"')
        self.assertNotRegex(html, r'<p\b[^>]*>\s*<ul>')

    def test_alterar_senha_invalida_preserva_resumo_e_erros_por_campo(self):
        response = self.client.post(
            reverse("usuarios:alterar_senha"),
            {
                "old_password": "senha-incorreta",
                "new_password1": "curta",
                "new_password2": "diferente",
            },
        )

        self.assertContains(response, 'role="alert"')
        self.assertContains(response, "Revise os dados da sua senha.")
        self.assertContains(response, 'href="#id_old_password"')
        self.assertContains(response, 'id="id_old_password_errors"')
        self.assertContains(response, 'aria-errormessage="id_old_password_errors"')

    def test_perfil_quebra_valores_longos_sem_estourar_o_cartao(self):
        css = open("static/css/perfil.css", encoding="utf-8").read()

        self.assertIn(".profile-card{min-width:0", css)
        self.assertIn(".profile-card dd{margin:0;overflow-wrap:anywhere}", css)
