from io import StringIO

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management import call_command
from django.test import RequestFactory, TestCase
from django.urls import reverse

from .admin import EventoAuditoriaAdmin
from .forms import CAMPOS_CAMERA
from .models import AtividadeCamera, Camera, EventoAuditoria


class AuditoriaIntegracaoTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="integracao", password="Senha-segura-123", first_name="Nome", last_name="Teste", email="teste@example.com")
        self.user.user_permissions.add(*self._permissoes("add_camera", "change_camera", "view_camera", "add_atividadecamera", "change_atividadecamera", "view_atividadecamera", "desativar_camera", "reativar_camera"))
        self.camera = Camera.objects.create(nome="CAM-INT", fabricante="Axis", modelo="M", serial="SER-INT", mac="AA:BB:CC:DD:EE:99", tipo="DOME", terminal="T1", pavimento="1", setor="S", ambiente="A", ip="10.22.0.1", mascara_subrede="255.255.255.0", gateway="10.22.0.254", vlan=100, farm="STVV", retencao_esperada_dias=30, codec="H.265")
        self.factory = RequestFactory()

    def _permissoes(self, *codenames):
        from django.contrib.auth.models import Permission
        return Permission.objects.filter(codename__in=codenames, content_type__app_label="cameras")

    def dados_camera(self, **kwargs):
        dados = {"nome": "CAM-NOVA", "fabricante": "Axis", "modelo": "M2", "serial": "SER-NOVA", "mac": "AA:BB:CC:DD:EE:98", "tipo": "DOME", "terminal": "T1", "pavimento": "1", "setor": "S", "ambiente": "A", "ip": "10.22.0.2", "mascara_subrede": "255.255.255.0", "gateway": "10.22.0.254", "vlan": "101", "farm": "STVV", "retencao_esperada_dias": "30", "codec": "H.265", "origem_cadastro": "MANUAL", "situacao_operacional": "PRODUCAO"}
        dados.update(kwargs); return dados

    def test_01_login_sucesso(self):
        self.client.post(reverse("usuarios:login"), {"username": "integracao", "password": "Senha-segura-123"})  # pragma: allowlist secret
        self.assertTrue(EventoAuditoria.objects.filter(codigo="autenticacao.login_sucesso").exists())

    def test_02_login_falha_sem_identificador_ou_senha(self):
        self.client.post(reverse("usuarios:login"), {"username": "alguem", "password": "valor-invalido"})  # pragma: allowlist secret
        evento = EventoAuditoria.objects.get(codigo="autenticacao.login_falha")
        self.assertEqual(evento.usuario_username, "")
        self.assertNotIn("alguem", str(evento.metadados))
        self.assertNotIn("valor-invalido", str(evento.metadados))

    def test_03_logout(self):
        self.client.force_login(self.user); self.client.post(reverse("usuarios:logout"))
        self.assertTrue(EventoAuditoria.objects.filter(codigo="autenticacao.logout").exists())

    def test_04_edicao_perfil_registra_diferencas(self):
        self.client.force_login(self.user)
        self.client.post(reverse("usuarios:editar_perfil"), {"first_name": "Novo", "last_name": "Teste", "email": "teste@example.com", "telefone": "123", "ramal": "4"})
        evento = EventoAuditoria.objects.get(codigo="perfil.atualizado")
        self.assertIn("first_name", evento.alteracoes)

    def test_05_edicao_perfil_sem_mudanca_nao_registra(self):
        perfil = self.user.perfil; self.client.force_login(self.user)
        self.client.post(reverse("usuarios:editar_perfil"), {"first_name": self.user.first_name, "last_name": self.user.last_name, "email": self.user.email, "telefone": perfil.telefone, "ramal": perfil.ramal})
        self.assertFalse(EventoAuditoria.objects.filter(codigo="perfil.atualizado").exists())

    def test_06_senha_registrada_sem_valores(self):
        self.client.force_login(self.user)
        self.client.post(reverse("usuarios:alterar_senha"), {"old_password": "Senha-segura-123", "new_password1": "Nova-senha-segura-456", "new_password2": "Nova-senha-segura-456"})  # pragma: allowlist secret
        evento = EventoAuditoria.objects.get(codigo="perfil.senha_alterada")
        self.assertEqual(evento.alteracoes, {})
        self.assertNotIn("Nova-senha", str(evento.metadados))

    def test_07_criacao_camera(self):
        self.client.force_login(self.user); self.client.post(reverse("cameras:criar"), self.dados_camera())
        self.assertTrue(EventoAuditoria.objects.filter(codigo="camera.criada").exists())

    def test_08_edicao_camera(self):
        self.client.force_login(self.user); dados = {campo: getattr(self.camera, campo) or "" for campo in CAMPOS_CAMERA}; dados["modelo"] = "ALTERADO"
        self.client.post(reverse("cameras:editar", args=[self.camera.pk]), dados)
        self.assertIn("modelo", EventoAuditoria.objects.get(codigo="camera.atualizada").alteracoes)

    def test_09_edicao_camera_sem_mudanca_nao_registra(self):
        self.client.force_login(self.user); dados = {campo: getattr(self.camera, campo) or "" for campo in CAMPOS_CAMERA}
        self.client.post(reverse("cameras:editar", args=[self.camera.pk]), dados)
        self.assertFalse(EventoAuditoria.objects.filter(codigo="camera.atualizada").exists())

    def test_10_inativacao_camera(self):
        self.client.force_login(self.user); self.client.post(reverse("cameras:desativar", args=[self.camera.pk]), {"motivo": "Motivo operacional válido"})
        self.assertTrue(EventoAuditoria.objects.filter(codigo="camera.desativada").exists())

    def test_11_reativacao_camera(self):
        self.camera.situacao_operacional = Camera.SituacaoOperacional.DESATIVADA; self.camera.save(); self.client.force_login(self.user)
        self.client.post(reverse("cameras:reativar", args=[self.camera.pk]), {"destino": "ESTOQUE", "justificativa": "Retorno operacional válido"})
        self.assertTrue(EventoAuditoria.objects.filter(codigo="camera.reativada").exists())

    def test_12_criacao_atividade(self):
        self.client.force_login(self.user)
        self.client.post(reverse("cameras:criar_atividade", args=[self.camera.pk]), {"tipo": "INSPECAO", "titulo": "Inspeção", "descricao": "Tudo certo", "ocorrida_em": "2026-07-31T10:00", "responsavel": "Equipe"})
        self.assertTrue(EventoAuditoria.objects.filter(codigo="atividade.criada").exists())

    def test_13_edicao_atividade(self):
        atividade = AtividadeCamera.objects.create(camera=self.camera, titulo="Antes", descricao="D")
        self.client.force_login(self.user)
        self.client.post(reverse("cameras:editar_atividade", args=[atividade.pk]), {"tipo": "OUTRO", "titulo": "Depois", "descricao": "D", "ocorrida_em": atividade.ocorrida_em.strftime("%Y-%m-%dT%H:%M"), "responsavel": ""})
        self.assertTrue(EventoAuditoria.objects.filter(codigo="atividade.atualizada").exists())

    def test_14_admin_evento_e_imutavel(self):
        model_admin = EventoAuditoriaAdmin(EventoAuditoria, admin.site); request = self.factory.get("/admin/"); request.user = self.user
        self.assertFalse(model_admin.has_add_permission(request))
        self.assertFalse(model_admin.has_delete_permission(request))

    def test_15_grupos_recebem_consulta_sem_mutacao(self):
        call_command("configurar_perfis_argos", stdout=StringIO())
        for grupo in Group.objects.filter(name__endswith="ARGOS"):
            codigos = set(grupo.permissions.filter(content_type__app_label="cameras").values_list("codename", flat=True))
            self.assertTrue({"view_eventoauditoria", "consultar_eventos"} <= codigos)
            self.assertFalse({"add_eventoauditoria", "change_eventoauditoria", "delete_eventoauditoria"} & codigos)

    def test_16_evento_protege_camera(self):
        from django.db.models.deletion import ProtectedError
        EventoAuditoria.objects.create(categoria="CAMERA", codigo="camera.teste", resumo="Teste", camera=self.camera)
        with self.assertRaises(ProtectedError): self.camera.delete()
