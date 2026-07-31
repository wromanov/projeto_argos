from io import StringIO
from pathlib import Path
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.core.management import call_command
from django.test import Client, RequestFactory, TestCase
from django.urls import reverse
from cameras.admin import AtividadeCameraAdmin, CameraAdmin
from cameras.models import AtividadeCamera, Camera
from usuarios.admin import PerfilUsuarioAdmin
from usuarios.models import PerfilUsuario


class SegurancaTests(TestCase):
    def setUp(self):
        call_command("configurar_perfis_argos",stdout=StringIO()); self.user=get_user_model().objects.create_user(username="seguro",password="Senha-forte-123",first_name="Nome"); self.camera=Camera.objects.create(nome="CAM",fabricante="A",modelo="M",ip="10.8.0.1",mascara_subrede="255.255.255.0",vlan=1); self.atividade=AtividadeCamera.objects.create(camera=self.camera,titulo="Atividade",descricao="D")
    def grupo(self,n): self.user.groups.set([Group.objects.get(name=n)]); self.client.force_login(self.user)
    def test_inicio_anonimo_redireciona_para_login(self): self.assertEqual(self.client.get("/").status_code,302)
    def test_dashboard_anonimo_redireciona_para_login(self): self.assertEqual(self.client.get("/dashboard/").status_code,302)
    def test_inventario_anonimo_redireciona_para_login(self): self.assertEqual(self.client.get("/cameras/").status_code,302)
    def test_perfil_anonimo_redireciona_para_login(self): self.assertEqual(self.client.get("/perfil/").status_code,302)
    def test_usuario_autenticado_sem_permissao_recebe_403(self): self.client.force_login(self.user); self.assertEqual(self.client.get("/cameras/").status_code,403)
    def test_monitoramento_nao_pode_criar_camera(self): self.grupo("Monitoramento ARGOS"); self.assertEqual(self.client.get(reverse("cameras:criar")).status_code,403)
    def test_operador_nao_possui_permissao_delete(self): self.grupo("Operador ARGOS"); self.assertFalse(self.user.has_perm("cameras.delete_camera"))
    def test_administrador_argos_nao_possui_permissao_delete(self): self.grupo("Administrador ARGOS"); self.assertFalse(any(p.startswith("cameras.delete_") for p in self.user.get_all_permissions()))
    def test_logout_get_retorna_405(self): self.client.force_login(self.user); self.assertEqual(self.client.get("/logout/").status_code,405)
    def csrf(self): c=Client(enforce_csrf_checks=True); c.force_login(self.user); return c
    def test_logout_post_sem_csrf_retorna_403(self): self.assertEqual(self.csrf().post("/logout/").status_code,403)
    def test_login_post_sem_csrf_retorna_403(self): self.assertEqual(Client(enforce_csrf_checks=True).post("/login/",{}).status_code,403)
    def test_editar_perfil_post_sem_csrf_retorna_403(self): self.assertEqual(self.csrf().post("/perfil/editar/",{}).status_code,403)
    def test_alterar_senha_post_sem_csrf_retorna_403(self): self.assertEqual(self.csrf().post("/perfil/alterar-senha/",{}).status_code,403)
    def test_criar_camera_post_sem_csrf_retorna_403(self): self.assertEqual(self.csrf().post("/cameras/nova/",{}).status_code,403)
    def test_alternar_camera_get_retorna_405(self): self.grupo("Operador ARGOS"); self.assertEqual(self.client.get(reverse("cameras:alternar_atividade",args=[self.camera.pk])).status_code,405)
    def login_next(self,next_value): return self.client.post("/login/",{"username":"seguro","password":"Senha-forte-123","next":next_value})
    def test_login_respeita_next_interno(self): self.assertEqual(self.login_next("/perfil/")["Location"],"/perfil/")
    def test_login_rejeita_next_externo(self): self.assertEqual(self.login_next("https://evil.example/")["Location"],"/")
    def test_login_rejeita_next_iniciado_por_duas_barras(self): self.assertEqual(self.login_next("//evil.example/")["Location"],"/")
    def test_login_rejeita_next_javascript(self): self.assertEqual(self.login_next("javascript:alert(1)")["Location"],"/")
    def test_nome_da_camera_e_escapado_no_html(self): self.camera.nome="<script>x</script>"; self.camera.save(); self.user.user_permissions.add(Permission.objects.get(codename="view_camera")); self.client.force_login(self.user); self.assertContains(self.client.get(reverse("cameras:detalhe",args=[self.camera.pk])),"&lt;script&gt;x&lt;/script&gt;")
    def test_titulo_da_atividade_e_escapado_no_html(self): self.atividade.titulo="<b>x</b>"; self.atividade.save(); self.user.user_permissions.add(Permission.objects.get(codename="view_camera")); self.client.force_login(self.user); self.assertContains(self.client.get(reverse("cameras:detalhe",args=[self.camera.pk])),"&lt;b&gt;x&lt;/b&gt;")
    def test_nome_do_usuario_e_escapado_no_html(self): self.user.first_name="<img>"; self.user.save(); self.client.force_login(self.user); self.assertContains(self.client.get("/perfil/"),"&lt;img&gt;")
    def test_pagina_403_nao_exibe_codename_da_permissao(self): self.client.force_login(self.user); self.assertNotContains(self.client.get("/cameras/"),"cameras.view_camera",status_code=403)
    def test_pagina_de_senha_nao_permite_cache(self): self.client.force_login(self.user); self.assertIn("no-cache",self.client.get("/perfil/alterar-senha/").get("Cache-Control"))
    def test_admin_camera_nao_permite_exclusao(self): self.assertFalse(CameraAdmin(Camera,admin.site).has_delete_permission(None))
    def test_admin_atividade_nao_permite_exclusao(self): self.assertFalse(AtividadeCameraAdmin(AtividadeCamera,admin.site).has_delete_permission(None))
    def test_admin_perfil_nao_permite_exclusao(self): self.assertFalse(PerfilUsuarioAdmin(PerfilUsuario,admin.site).has_delete_permission(None))
    def admin_request(self):
        request = RequestFactory().get("/admin/"); request.user = get_user_model().objects.create_superuser(username="admin-seguranca", email="", password="senha"); return request
    def test_acao_delete_selected_ausente_para_camera(self): self.assertNotIn("delete_selected",CameraAdmin(Camera,admin.site).get_actions(self.admin_request()))
    def test_acao_delete_selected_ausente_para_atividade(self): self.assertNotIn("delete_selected",AtividadeCameraAdmin(AtividadeCamera,admin.site).get_actions(self.admin_request()))
    def test_arquivos_sensiveis_estao_cobertos_pelo_gitignore(self):
        texto=Path(".gitignore").read_text(encoding="utf-8"); [self.assertIn(item,texto) for item in ("db.sqlite3",".env","*.pem","*.key","*.sqlite3")]
