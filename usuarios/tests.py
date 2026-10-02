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
    def test_comando_cria_quatro_grupos_sem_promover_usuarios(self):
        user_count = get_user_model().objects.count()
        call_command("configurar_perfis_argos", stdout=StringIO())
        self.assertEqual(
            set(Group.objects.filter(name__endswith="ARGOS").values_list("name", flat=True)),
            {
                "Monitoramento ARGOS",
                "Operador ARGOS",
                "Técnico ARGOS",
                "Administrador ARGOS",
            },
        )
        self.assertEqual(get_user_model().objects.count(), user_count)
        self.assertFalse(self.user.groups.exists())

    def test_comando_e_idempotente_e_reconcilia_matriz_sem_promover_usuarios(self):
        self.user.groups.add(Group.objects.create(name="Monitoramento ARGOS"))
        user_groups_before = set(self.user.groups.values_list("name", flat=True))

        def snapshot():
            return {
                group.name: set(group.permissions.values_list("codename", flat=True))
                for group in Group.objects.filter(name__endswith="ARGOS")
            }

        call_command("configurar_perfis_argos", stdout=StringIO())
        first = snapshot()
        call_command("configurar_perfis_argos", stdout=StringIO())

        self.assertEqual(snapshot(), first)
        self.assertEqual(len(first), 4)
        self.assertEqual(set(self.user.groups.values_list("name", flat=True)), user_groups_before)

    def test_matriz_de_permissoes_dos_quatro_grupos(self):
        call_command("configurar_perfis_argos", stdout=StringIO())
        groups = {
            name: set(Group.objects.get(name=f"{name} ARGOS").permissions.values_list("codename", flat=True))
            for name in ("Monitoramento", "Operador", "Técnico", "Administrador")
        }
        monitor, operator, technician, admin = (
            groups["Monitoramento"], groups["Operador"], groups["Técnico"], groups["Administrador"]
        )
        consulta_eventos = {"view_eventoauditoria", "consultar_eventos", "view_substituicaocamera", "consultar_substituicoescamera"}
        operational_write = {"add_camera", "change_camera", "add_atividadecamera", "change_atividadecamera", "desativar_camera", "reativar_camera", "alterar_situacao_camera", "registrar_substituicao_camera"}
        tecnico_only = {"change_camera_connection", "manage_camera_capability", "view_camera_credential", "change_camera_credential", "reveal_camera_credential", "run_camera_connection_test", "view_camera_diagnostic", "capture_camera_image"}
        global_admin = {"manage_camera_target_policy", "manage_monitoring_runtime"}
        mutacao_eventos = {"add_eventoauditoria", "change_eventoauditoria", "delete_eventoauditoria"}

        self.assertEqual(monitor, {"view_camera", "view_atividadecamera"} | consulta_eventos)
        self.assertTrue(operational_write | consulta_eventos | {"view_camera_connection", "add_cameraimagerecord"} <= operator)
        self.assertEqual(technician, operator | tecnico_only)
        self.assertTrue(technician | global_admin | {"view_user", "add_user", "change_user", "view_perfilusuario", "change_perfilusuario"} <= admin)
        self.assertFalse((operational_write | {"add_cameraimagerecord", "view_camera_connection"}) & monitor)
        self.assertFalse((tecnico_only | global_admin) & operator)
        self.assertFalse(global_admin & technician)
        administration_permissions = {"view_user", "add_user", "change_user", "view_perfilusuario", "change_perfilusuario"}
        self.assertFalse(administration_permissions & (monitor | operator | technician))
        self.assertFalse({"view_group", "add_group", "change_group", "delete_group", "view_permission"} & technician)
        self.assertFalse({"view_group", "add_group", "change_group", "delete_group", "view_permission"} & admin)
        self.assertFalse(mutacao_eventos & (monitor | operator | technician | admin))
        self.assertFalse({"view_perfilusuario", "change_perfilusuario", "add_perfilusuario", "delete_perfilusuario"} & (monitor | operator | technician))
        self.assertFalse({"add_perfilusuario", "delete_perfilusuario"} & admin)
        self.assertFalse(any(permission.startswith("delete_") for permissions in groups.values() for permission in permissions))
