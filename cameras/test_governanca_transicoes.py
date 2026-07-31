from unittest.mock import patch
from django.contrib.auth import get_user_model
from django.test import TestCase

from .governanca import ErroGovernancaCamera, alterar_situacao_camera, desativar_camera, reativar_camera
from .models import Camera, EventoAuditoria


class GovernancaTransicoesTests(TestCase):
    def setUp(self): self.user=get_user_model().objects.create_user("operador")
    def camera(self, **extra):
        n=Camera.objects.count()+1; data=dict(nome=f"CAM-{n}", fabricante="Axis", modelo="P", serial=f"SER-{n}", mac=f"AA:BB:CC:DD:EE:{n:02X}", tipo="DOME", terminal="T1", pavimento="1", setor="S", ambiente="A", ip=f"10.0.0.{n}", mascara_subrede="255.255.255.0", gateway="10.0.0.254", vlan=10, farm="F1", retencao_esperada_dias=30, codec="H265"); data.update(extra); return Camera.objects.create(**data)
    def desativar(self,camera): return desativar_camera(camera=camera,motivo="Motivo operacional válido",usuario=self.user)
    def test_desativar_camera_de_producao(self): c=self.desativar(self.camera()); self.assertEqual(c.situacao_operacional,"DESATIVADA")
    def test_desativar_camera_de_estoque(self): c=self.desativar(self.camera(situacao_operacional="ESTOQUE")); self.assertEqual(c.situacao_operacional,"DESATIVADA")
    def test_desativacao_exige_motivo(self):
        with self.assertRaises(ErroGovernancaCamera): desativar_camera(camera=self.camera(),motivo="",usuario=self.user)
    def test_desativacao_rejeita_motivo_curto(self):
        with self.assertRaises(ErroGovernancaCamera): desativar_camera(camera=self.camera(),motivo="curto",usuario=self.user)
    def test_desativacao_registra_data_e_usuario(self): c=self.desativar(self.camera()); self.assertIsNotNone(c.desativada_em); self.assertEqual(c.desativada_por,self.user)
    def test_desativacao_gera_evento(self): self.desativar(self.camera()); self.assertTrue(EventoAuditoria.objects.filter(codigo="camera.desativada").exists())
    def test_camera_ja_desativada_nao_pode_ser_desativada_novamente(self):
        c=self.desativar(self.camera())
        with self.assertRaises(ErroGovernancaCamera): self.desativar(c)
    def test_reativar_camera_para_estoque(self): c=self.desativar(self.camera()); self.assertEqual(reativar_camera(camera=c,destino="ESTOQUE",justificativa="Retorno ao estoque",usuario=self.user).situacao_operacional,"ESTOQUE")
    def test_reativar_camera_para_producao(self): c=self.desativar(self.camera()); self.assertEqual(reativar_camera(camera=c,destino="PRODUCAO",justificativa="Retorno à produção",usuario=self.user).situacao_operacional,"PRODUCAO")
    def test_reativar_para_producao_exige_completude(self):
        c=self.desativar(self.camera(gateway=None))
        with self.assertRaises(ErroGovernancaCamera): reativar_camera(camera=c,destino="PRODUCAO",justificativa="Retorno à produção",usuario=self.user)
    def test_reativacao_exige_justificativa(self):
        c=self.desativar(self.camera())
        with self.assertRaises(ErroGovernancaCamera): reativar_camera(camera=c,destino="ESTOQUE",justificativa="",usuario=self.user)
    def test_producao_pode_ir_para_estoque(self): c=alterar_situacao_camera(camera=self.camera(),destino="ESTOQUE",justificativa="Movimento planejado",usuario=self.user); self.assertEqual(c.situacao_operacional,"ESTOQUE")
    def test_estoque_completo_pode_ir_para_producao(self): c=alterar_situacao_camera(camera=self.camera(situacao_operacional="ESTOQUE"),destino="PRODUCAO",justificativa="Instalação planejada",usuario=self.user); self.assertEqual(c.situacao_operacional,"PRODUCAO")
    def test_estoque_incompleto_nao_pode_ir_para_producao(self):
        c=self.camera(situacao_operacional="ESTOQUE",gateway=None)
        with self.assertRaises(ErroGovernancaCamera): alterar_situacao_camera(camera=c,destino="PRODUCAO",justificativa="Instalação planejada",usuario=self.user)
    def test_transicao_gera_evento_especifico(self): alterar_situacao_camera(camera=self.camera(),destino="ESTOQUE",justificativa="Movimento planejado",usuario=self.user); self.assertTrue(EventoAuditoria.objects.filter(codigo="camera.movida_estoque").exists())
    def test_falha_de_auditoria_reverte_transicao(self):
        c=self.camera()
        with patch("cameras.governanca.registrar_evento",side_effect=RuntimeError("falha")):
            with self.assertRaises(RuntimeError): desativar_camera(camera=c,motivo="Motivo operacional válido",usuario=self.user)
        c.refresh_from_db(); self.assertEqual(c.situacao_operacional,"PRODUCAO")
