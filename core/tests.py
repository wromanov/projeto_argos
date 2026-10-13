from io import StringIO

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from cameras.models import AtividadeCamera, Camera


class CoreTests(TestCase):
    def setUp(self):
        call_command("configurar_perfis_argos",stdout=StringIO())
        self.user=get_user_model().objects.create_user(username="teste",password="senha")
        self.camera=Camera.objects.create(nome="CAM-PORTAL",fabricante="Axis",modelo="M1",ip="10.1.1.1",mascara_subrede="255.255.255.0",vlan=100)
        self.atividade=AtividadeCamera.objects.create(camera=self.camera,titulo="Inspeção",descricao="Teste",tipo="INSPECAO")
    def login_grupo(self,nome): self.user.groups.set([Group.objects.get(name=nome)]); self.client.force_login(self.user)
    def test_inicio_anônimo_redireciona_para_login(self): self.assertRedirects(self.client.get("/"),"/login/?next=/",fetch_redirect_response=False)
    def test_dashboard_anônimo_redireciona_para_login(self): self.assertRedirects(self.client.get("/dashboard/"),"/login/?next=/dashboard/",fetch_redirect_response=False)
    def test_inventario_anônimo_redireciona_para_login(self): self.assertRedirects(self.client.get("/cameras/"),"/login/?next=/cameras/",fetch_redirect_response=False)
    def test_detalhe_camera_anônimo_redireciona_para_login(self): self.assertRedirects(self.client.get(reverse("cameras:detalhe",args=[self.camera.pk])),f"/login/?next=/cameras/{self.camera.pk}/",fetch_redirect_response=False)
    def test_inicio_autenticado_retorna_200(self): self.client.force_login(self.user); self.assertEqual(self.client.get("/").status_code,200)
    def test_inicio_exibe_inventario_e_dashboard_com_permissao(self): self.login_grupo("Monitoramento ARGOS"); response=self.client.get("/"); self.assertContains(response,"Inventário"); self.assertContains(response,"Dashboard")
    def test_inicio_oculta_modulos_sem_permissao(self): self.client.force_login(self.user); self.assertNotContains(self.client.get("/"),"Consulte e gerencie")
    def test_inicio_nao_exibe_modulos_futuros(self):
        self.client.force_login(self.user); response=self.client.get("/"); [self.assertNotContains(response,nome) for nome in ("Eventos","Credenciais","Snapshots","RTSP")]
    def test_dashboard_retorna_200_com_permissao(self): self.login_grupo("Monitoramento ARGOS"); self.assertEqual(self.client.get("/dashboard/").status_code,200)
    def test_dashboard_exibe_contadores_de_camera(self): self.login_grupo("Monitoramento ARGOS"); response=self.client.get("/dashboard/"); self.assertContains(response,"Total"); self.assertContains(response,"Produção")
    def test_dashboard_exibe_status_de_monitoramento(self): self.login_grupo("Monitoramento ARGOS"); response=self.client.get("/dashboard/"); [self.assertContains(response, label) for label in ("Monitoramento e completude", "Online", "Offline", "Desconhecido", "Não monitorada", "Estados técnicos das câmeras")]; self.assertEqual(response.context["monitoring_state_labels"]["OUT_OF_SCOPE"], "Não monitorada")
    def test_dashboard_exibe_atividades_recentes(self): self.login_grupo("Monitoramento ARGOS"); self.assertContains(self.client.get("/dashboard/"),"Inspeção")
    def test_dashboard_exibe_cameras_atualizadas(self): self.login_grupo("Monitoramento ARGOS"); self.assertContains(self.client.get("/dashboard/"),"CAM-PORTAL")
    def test_dashboard_conta_cameras_afetadas_por_ip_duplicado(self):
        self.login_grupo("Monitoramento ARGOS")
        Camera.objects.create(nome="CAM-PORTAL-2", fabricante="Axis", modelo="M2", ip="10.1.1.1", mascara_subrede="255.255.255.0", vlan=100)

        response = self.client.get(reverse("core:dashboard"))

        self.assertEqual(response.context["cameras_com_ip_duplicado"], 2)
        self.assertContains(response, "Câmeras com IP duplicado")
    def test_dashboard_renderiza_estado_vazio(self):
        self.login_grupo("Monitoramento ARGOS")
        self.atividade.delete()
        Camera.objects.all().delete()

        response = self.client.get(reverse("core:dashboard"))

        self.assertEqual(response.context["total_cameras"], 0)
        self.assertContains(response, "Nenhuma atividade registrada.")
        self.assertContains(response, "Nenhuma câmera cadastrada.")
    def test_dashboard_preserva_nome_longo_nas_listas_recentes(self):
        self.login_grupo("Monitoramento ARGOS")
        nome_longo = "CÂMERA QA — " + "TERMINAL LESTE — ÁREA DE CONTROLE " * 3
        self.camera.nome = nome_longo[:150]
        self.camera.save(update_fields=["nome"])

        response = self.client.get(reverse("core:dashboard"))

        self.assertContains(response, nome_longo[:150])
    def test_dashboard_renderiza_agregados_com_2300_cameras_sinteticas(self):
        self.login_grupo("Monitoramento ARGOS")
        Camera.objects.bulk_create(
            [
                Camera(nome=f"CAM-ESCALA-{index:04}", fabricante="QA fictício", modelo="ESCALA")
                for index in range(2299)
            ],
            batch_size=500,
        )

        response = self.client.get(reverse("core:dashboard"))

        self.assertEqual(response.context["total_cameras"], 2300)
        self.assertEqual(len(response.context["cameras_recentes"]), 5)
        self.assertContains(response, "Câmeras exibidas <strong>5</strong>")
    def test_monitoramento_possui_acesso_somente_leitura(self):
        self.login_grupo("Monitoramento ARGOS"); self.assertEqual(self.client.get(reverse("cameras:lista")).status_code,200); self.assertEqual(self.client.get(reverse("cameras:detalhe",args=[self.camera.pk])).status_code,200); self.assertEqual(self.client.get(reverse("cameras:criar")).status_code,403); self.assertEqual(self.client.get(reverse("cameras:editar",args=[self.camera.pk])).status_code,403); self.assertEqual(self.client.post(reverse("cameras:desativar",args=[self.camera.pk]), {"motivo": "Motivo operacional valido"}).status_code,403); self.assertEqual(self.client.get(reverse("cameras:criar_atividade",args=[self.camera.pk])).status_code,403)
    def test_operador_possui_acesso_operacional(self):
        self.login_grupo("Operador ARGOS"); self.assertEqual(self.client.get(reverse("cameras:lista")).status_code,200); self.assertEqual(self.client.get(reverse("cameras:detalhe",args=[self.camera.pk])).status_code,200); self.assertEqual(self.client.get(reverse("cameras:criar")).status_code,200); self.assertEqual(self.client.get(reverse("cameras:editar",args=[self.camera.pk])).status_code,200); self.assertEqual(self.client.get(reverse("cameras:criar_atividade",args=[self.camera.pk])).status_code,200); self.assertEqual(self.client.get(reverse("cameras:editar_atividade",args=[self.atividade.pk])).status_code,200)
    def test_usuario_autenticado_sem_permissao_recebe_403(self): self.client.force_login(self.user); self.assertEqual(self.client.get(reverse("cameras:lista")).status_code,403)
