from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.test import TestCase

from .models import Camera
from .validadores import normalizar_mac


class GovernancaModeloTests(TestCase):
    def camera(self, **extra):
        data = dict(nome="CAM-01", fabricante="Axis", modelo="P", serial="SER-01", mac="AA:BB:CC:DD:EE:01", tipo="DOME", terminal="T1", pavimento="1", setor="S", ambiente="A", ip="10.0.0.1", mascara_subrede="255.255.255.0", gateway="10.0.0.254", vlan=10, farm="F1", retencao_esperada_dias=30, codec="H265")
        data.update(extra); return Camera.objects.create(**data)

    def test_choices_situacao_operacional(self): self.assertEqual(set(Camera.SituacaoOperacional.values), {"PRODUCAO", "ESTOQUE", "DESATIVADA"})
    def test_camera_nova_tem_situacao_producao_por_padrao(self): self.assertEqual(self.camera().situacao_operacional, "PRODUCAO")
    def test_normalizar_mac_com_dois_pontos(self): self.assertEqual(normalizar_mac("aa:bb:cc:dd:ee:ff"), "AA:BB:CC:DD:EE:FF")
    def test_normalizar_mac_com_hifens(self): self.assertEqual(normalizar_mac("aa-bb-cc-dd-ee-ff"), "AA:BB:CC:DD:EE:FF")
    def test_normalizar_mac_formato_cisco(self): self.assertEqual(normalizar_mac("aabb.ccdd.eeff"), "AA:BB:CC:DD:EE:FF")
    def test_normalizar_mac_sem_separadores(self): self.assertEqual(normalizar_mac("aabbccddeeff"), "AA:BB:CC:DD:EE:FF")
    def test_normalizar_mac_vazio_retorna_none(self): self.assertIsNone(normalizar_mac("  "))
    def test_normalizar_mac_invalido_gera_validationerror(self):
        with self.assertRaises(ValidationError): normalizar_mac("invalido")
    def test_mac_duplicado_e_rejeitado(self):
        self.camera()
        with self.assertRaises(IntegrityError):
            with transaction.atomic(): self.camera(nome="CAM-02", serial="SER-02", mac="aa-bb-cc-dd-ee-01")
    def test_ip_duplicado_e_permitido(self): self.camera(); self.assertIsNotNone(self.camera(nome="CAM-02", serial="SER-02", mac="AA:BB:CC:DD:EE:02").pk)
    def test_nome_duplicado_ativo_case_insensitive_e_rejeitado(self):
        self.camera()
        with self.assertRaises(IntegrityError):
            with transaction.atomic(): self.camera(nome="cam-01", serial="SER-02", mac="AA:BB:CC:DD:EE:02", situacao_operacional="ESTOQUE")
    def test_nome_de_camera_desativada_pode_ser_reutilizado(self): self.camera(situacao_operacional="DESATIVADA"); self.assertIsNotNone(self.camera(serial="SER-02", mac="AA:BB:CC:DD:EE:02").pk)
    def test_camera_producao_completa(self): self.assertTrue(self.camera().cadastro_completo)
    def test_camera_producao_incompleta_lista_campos(self): self.assertIn("gateway", self.camera(gateway=None).campos_incompletos())
    def test_camera_estoque_nao_exige_rede(self): self.assertTrue(self.camera(situacao_operacional="ESTOQUE", ip=None, mascara_subrede=None, gateway=None, vlan=None, terminal="", pavimento="", setor="", ambiente="", farm="", retencao_esperada_dias=None, codec="").cadastro_completo)
    def test_camera_desativada_legada_aceita_dados_minimos(self): self.assertTrue(Camera.objects.create(nome="Legada", fabricante="", modelo="", situacao_operacional="DESATIVADA").cadastro_completo)
