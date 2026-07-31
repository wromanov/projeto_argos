from io import StringIO

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse


class UsuariosTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="usuario", password="senha-forte")
        self.login_url = reverse("usuarios:login")

    def test_login_publico_retorna_200(self): self.assertEqual(self.client.get(self.login_url).status_code, 200)
    def test_login_usa_template_personalizado(self): self.assertTemplateUsed(self.client.get(self.login_url), "usuarios/login.html")
    def test_login_exibe_usuario_e_senha(self):
        response=self.client.get(self.login_url); self.assertContains(response,'name="username"'); self.assertContains(response,'name="password"')
    def test_login_contem_protecao_csrf(self): self.assertContains(self.client.get(self.login_url), "csrfmiddlewaretoken")
    def test_login_valido_redireciona_para_inicio(self): self.assertRedirects(self.client.post(self.login_url,{"username":"usuario","password":"senha-forte"}), reverse("core:inicio"))
    def test_login_respeita_next_interno(self): self.assertRedirects(self.client.post(self.login_url,{"username":"usuario","password":"senha-forte","next":"/cameras/"}), "/cameras/", fetch_redirect_response=False)
    def test_login_invalido_nao_autentica(self):
        self.client.post(self.login_url,{"username":"usuario","password":"errada"}); self.assertNotIn("_auth_user_id",self.client.session)
    def test_login_invalido_exibe_mensagem_generica(self): self.assertContains(self.client.post(self.login_url,{"username":"usuario","password":"errada"}),"Usuário ou senha inválidos.")
    def test_usuario_inativo_nao_autentica(self):
        self.user.is_active=False; self.user.save(); self.assertContains(self.client.post(self.login_url,{"username":"usuario","password":"senha-forte"}),"Usuário ou senha inválidos.")
    def test_usuario_autenticado_e_redirecionado_do_login(self): self.client.force_login(self.user); self.assertRedirects(self.client.get(self.login_url),reverse("core:inicio"))
    def test_logout_post_encerra_sessao(self):
        self.client.force_login(self.user); self.client.post(reverse("usuarios:logout")); self.assertNotIn("_auth_user_id",self.client.session)
    def test_logout_get_nao_e_permitido(self): self.client.force_login(self.user); self.assertEqual(self.client.get(reverse("usuarios:logout")).status_code,405)
    def test_login_nao_oferece_cadastro_publico(self): self.assertNotContains(self.client.get(self.login_url),"Cadastre-se")
    def test_comando_cria_tres_grupos(self):
        call_command("configurar_perfis_argos",stdout=StringIO()); self.assertEqual(Group.objects.filter(name__endswith="ARGOS").count(),3)
    def test_comando_e_idempotente(self):
        call_command("configurar_perfis_argos",stdout=StringIO()); call_command("configurar_perfis_argos",stdout=StringIO()); self.assertEqual(Group.objects.filter(name__endswith="ARGOS").count(),3)
    def test_matriz_de_permissoes_dos_tres_grupos(self):
        quantidade_usuarios=get_user_model().objects.count(); call_command("configurar_perfis_argos",stdout=StringIO())
        monitor=set(Group.objects.get(name="Monitoramento ARGOS").permissions.values_list("codename",flat=True)); operador=set(Group.objects.get(name="Operador ARGOS").permissions.values_list("codename",flat=True)); admin=set(Group.objects.get(name="Administrador ARGOS").permissions.values_list("codename",flat=True))
        consulta_eventos={"view_eventoauditoria","consultar_eventos","view_substituicaocamera","consultar_substituicoescamera"}; mutacao_eventos={"add_eventoauditoria","change_eventoauditoria","delete_eventoauditoria"}
        self.assertEqual(monitor,{"view_camera","view_atividadecamera"} | consulta_eventos); self.assertTrue({"view_camera","add_camera","change_camera","view_atividadecamera","add_atividadecamera","change_atividadecamera"} | consulta_eventos <= operador); self.assertTrue({"view_user","add_user","change_user","view_group","add_group","change_group","view_permission","view_perfilusuario","change_perfilusuario"} | consulta_eventos <= admin); self.assertFalse(mutacao_eventos & (monitor | operador | admin)); self.assertFalse({"view_perfilusuario","change_perfilusuario","add_perfilusuario","delete_perfilusuario"} & (monitor | operador)); self.assertFalse({"add_perfilusuario","delete_perfilusuario"} & admin); self.assertFalse(any(p.startswith("delete_") for p in monitor|operador|admin)); self.assertEqual(get_user_model().objects.count(),quantidade_usuarios)
