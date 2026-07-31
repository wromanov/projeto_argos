from unittest.mock import patch
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from .governanca import ErroGovernancaCamera, substituir_camera
from .models import Camera, EventoAuditoria, SubstituicaoCamera


class GovernancaSubstituicoesTests(TestCase):
    def setUp(self): self.user=get_user_model().objects.create_user("operador",first_name="Op")
    def camera(self,n,situacao,**extra):
        data=dict(nome=f"CAM-{n}",patrimonio=f"PAT-{n}",fabricante=f"Fab-{n}",modelo=f"Mod-{n}",serial=f"SER-{n}",mac=f"AA:BB:CC:DD:EE:{n:02X}",tipo="DOME",terminal=f"T{n}",pavimento=str(n),setor=f"S{n}",ambiente=f"A{n}",descricao_detalhada=f"Desc {n}",ponto_referencia=f"Ponto {n}",ip=f"10.0.0.{n}",mascara_subrede="255.255.255.0",gateway="10.0.0.254",vlan=10+n,farm=f"F{n}",retencao_esperada_dias=30,codec="H265",situacao_operacional=situacao); data.update(extra); return Camera.objects.create(**data)
    def par(self): return self.camera(1,"PRODUCAO"),self.camera(2,"ESTOQUE")
    def trocar(self): a,s=self.par(); return a,s,substituir_camera(camera_anterior=a,camera_substituta=s,motivo="Falha física confirmada",usuario=self.user)
    def test_criacao_substituicao_valida(self): self.assertIsNotNone(self.trocar()[2].pk)
    def test_substituicao_bloqueia_mesma_camera(self):
        a=self.camera(1,"PRODUCAO")
        with self.assertRaises(ErroGovernancaCamera): substituir_camera(camera_anterior=a,camera_substituta=a,motivo="Falha física confirmada",usuario=self.user)
    def test_camera_anterior_deve_estar_em_producao(self):
        a,s=self.camera(1,"ESTOQUE"),self.camera(2,"ESTOQUE")
        with self.assertRaises(ErroGovernancaCamera): substituir_camera(camera_anterior=a,camera_substituta=s,motivo="Falha física confirmada",usuario=self.user)
    def test_camera_substituta_deve_estar_em_estoque(self):
        a,s=self.camera(1,"PRODUCAO"),self.camera(2,"PRODUCAO")
        with self.assertRaises(ErroGovernancaCamera): substituir_camera(camera_anterior=a,camera_substituta=s,motivo="Falha física confirmada",usuario=self.user)
    def test_substituicao_transfere_nome_operacional(self): a,s,_=self.trocar(); s.refresh_from_db(); self.assertEqual(s.nome,a.nome)
    def test_substituicao_transfere_localizacao(self): a,s,_=self.trocar(); s.refresh_from_db(); self.assertEqual((s.terminal,s.pavimento,s.setor,s.ambiente),(a.terminal,a.pavimento,a.setor,a.ambiente))
    def test_substituicao_transfere_rede(self): a,s,_=self.trocar(); s.refresh_from_db(); self.assertEqual((s.ip,s.gateway,s.vlan),(a.ip,a.gateway,a.vlan))
    def test_substituicao_transfere_configuracao_de_gravacao(self): a,s,_=self.trocar(); s.refresh_from_db(); self.assertEqual((s.farm,s.retencao_esperada_dias,s.codec),(a.farm,a.retencao_esperada_dias,a.codec))
    def test_substituicao_preserva_identidade_fisica_da_substituta(self): a,s,_=self.trocar(); original=(s.patrimonio,s.fabricante,s.modelo,s.serial,s.mac,s.tipo); s.refresh_from_db(); self.assertEqual((s.patrimonio,s.fabricante,s.modelo,s.serial,s.mac,s.tipo),original)
    def test_substituicao_desativa_camera_anterior(self): a,s,_=self.trocar(); a.refresh_from_db(); self.assertEqual(a.situacao_operacional,"DESATIVADA")
    def test_substituicao_coloca_substituta_em_producao(self): a,s,_=self.trocar(); s.refresh_from_db(); self.assertEqual(s.situacao_operacional,"PRODUCAO")
    def test_substituicao_congela_nome_anterior_da_substituta(self): a,s,reg=self.trocar(); self.assertEqual(reg.nome_anterior_substituta,"CAM-2")
    def test_substituicao_gera_evento_para_camera_anterior(self): a,s,_=self.trocar(); self.assertTrue(EventoAuditoria.objects.filter(camera=a,codigo="camera.substituida").exists())
    def test_substituicao_gera_evento_para_camera_substituta(self): a,s,_=self.trocar(); self.assertTrue(EventoAuditoria.objects.filter(camera=s,codigo="camera.assumiu_posicao").exists())
    def test_substituicao_e_imutavel(self):
        reg=self.trocar()[2]; reg.motivo="Outro"
        with self.assertRaises(ValidationError): reg.save()
        with self.assertRaises(ValidationError): SubstituicaoCamera.objects.filter(pk=reg.pk).delete()
    def test_falha_na_substituicao_reverte_toda_transacao(self):
        a,s=self.par()
        with patch("cameras.governanca.registrar_evento",side_effect=[None,RuntimeError("falha")]):
            with self.assertRaises(RuntimeError): substituir_camera(camera_anterior=a,camera_substituta=s,motivo="Falha física confirmada",usuario=self.user)
        a.refresh_from_db(); s.refresh_from_db(); self.assertEqual((a.situacao_operacional,s.situacao_operacional),("PRODUCAO","ESTOQUE")); self.assertFalse(SubstituicaoCamera.objects.exists())
