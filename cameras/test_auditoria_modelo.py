from datetime import datetime
from decimal import Decimal
from uuid import UUID

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.models.deletion import ProtectedError
from django.test import RequestFactory, TestCase

from .auditoria import calcular_alteracoes, obter_ip_requisicao, registrar_evento, sanitizar_dados
from .models import Camera, EventoAuditoria


class AuditoriaModeloTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="auditor", password="senha")
        self.camera = Camera.objects.create(nome="CAM-AUD", fabricante="Axis", modelo="M", ip="10.20.0.1", mascara_subrede="255.255.255.0", vlan=100)
        self.factory = RequestFactory()

    def evento(self, **kwargs):
        dados = {"codigo": "teste.evento", "resumo": "Evento de teste", "categoria": EventoAuditoria.Categoria.SISTEMA, "usuario": self.user, "camera": self.camera, "entidade": self.camera}
        dados.update(kwargs)
        return registrar_evento(**dados)

    def test_01_criacao_valida(self):
        self.assertEqual(self.evento().codigo, "teste.evento")

    def test_02_representacao_textual(self):
        self.assertIn("teste.evento", str(self.evento()))

    def test_03_camera_pode_ser_nula(self):
        self.assertIsNone(self.evento(camera=None).camera)

    def test_04_usuario_congelado(self):
        evento = self.evento()
        self.assertEqual(evento.usuario_username, "auditor")

    def test_05_usuario_congelado_permanece_apos_set_null(self):
        evento = self.evento(); self.user.delete(); evento.refresh_from_db()
        self.assertIsNone(evento.usuario)
        self.assertEqual(evento.usuario_username, "auditor")

    def test_06_save_impede_atualizacao(self):
        evento = self.evento(); evento.resumo = "Outro"
        with self.assertRaises(ValidationError): evento.save()

    def test_07_delete_impede_exclusao(self):
        with self.assertRaises(ValidationError): self.evento().delete()

    def test_08_queryset_update_impedido(self):
        evento = self.evento()
        with self.assertRaises(ValidationError): EventoAuditoria.objects.filter(pk=evento.pk).update(resumo="Outro")

    def test_09_queryset_delete_impedido(self):
        evento = self.evento()
        with self.assertRaises(ValidationError): EventoAuditoria.objects.filter(pk=evento.pk).delete()

    def test_10_ip_usa_remote_addr(self):
        request = self.factory.get("/", REMOTE_ADDR="192.0.2.10")
        self.assertEqual(obter_ip_requisicao(request), "192.0.2.10")

    def test_11_ip_ignora_x_forwarded_for(self):
        request = self.factory.get("/", REMOTE_ADDR="192.0.2.11", HTTP_X_FORWARDED_FOR="198.51.100.1")
        self.assertEqual(obter_ip_requisicao(request), "192.0.2.11")

    def test_12_sanitiza_chaves_sensiveis(self):
        dados = sanitizar_dados({"password": "valor"})  # pragma: allowlist secret
        self.assertEqual(dados["password"], "[REDACTED]")

    def test_13_sanitiza_estrutura_aninhada(self):
        valor = sanitizar_dados({"dados": [{"api_key": "valor"}], "decimal": Decimal("1.2"), "uuid": UUID(int=0), "data": datetime(2026, 1, 1)})
        self.assertEqual(valor["dados"][0]["api_key"], "[REDACTED]")
        self.assertEqual(valor["decimal"], "1.2")

    def test_14_calcula_apenas_campos_modificados(self):
        anterior = Camera.objects.get(pk=self.camera.pk); self.camera.nome = "CAM-NOVA"
        self.assertEqual(set(calcular_alteracoes(anterior, self.camera, ("nome", "modelo"))), {"nome"})

    def test_15_calculo_ignora_campo_nao_permitido(self):
        anterior = Camera.objects.get(pk=self.camera.pk); self.camera.observacoes = "segredo"
        self.assertEqual(calcular_alteracoes(anterior, self.camera, ("nome",)), {})

    def test_16_metadados_nao_incluem_query_string(self):
        request = self.factory.get("/rota/?token=valor", REMOTE_ADDR="192.0.2.1"); request.user = self.user
        evento = self.evento(request=request, usuario=None, metadados={"segredo": "ok"})
        self.assertEqual(evento.metadados["caminho"], "/rota/")
        self.assertNotIn("QUERY_STRING", evento.metadados)
        self.assertNotIn("token", str(evento.metadados))