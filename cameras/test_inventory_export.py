import csv
import importlib.util
import io
import unittest

from django.contrib.auth import get_user_model
from django.http import QueryDict
from django.test import TestCase
from django.urls import reverse

from .inventory_export import (
    EXPORT_FIELDS,
    PDF_MAX_FREE_TEXT_CHARS,
    PDF_MAX_RECORDS,
    PdfExportLimitExceeded,
    _wrap_text,
    selected_fields,
    validate_pdf_limits,
)
from .inventory_filters import FiltrosInventario
from .models import (
    Camera,
    CameraCaptureJob,
    CameraCredential,
    CameraCredentialVersion,
    CameraImageRecord,
)


REPORTLAB_AVAILABLE = importlib.util.find_spec("reportlab") is not None


class InventarioExportacaoTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_superuser(
            username="e6-export-admin",
            password="test-password",
            email="",
        )

    def setUp(self):
        self.client.force_login(self.user)

    def criar_camera(self, indice, **atributos):
        valores = {
            "patrimonio": f"E6-{indice:05d}",
            "nome": f"CAM-E6-{indice:05d}",
            "fabricante": "AXIS",
            "modelo": "MODELO E6",
            "serial": f"E6-SERIAL-{indice:05d}",
            "mac": f"AA:BB:CC:DD:{indice // 256:02X}:{indice % 256:02X}",
            "tipo": Camera.TipoCamera.DOME,
            "situacao_operacional": Camera.SituacaoOperacional.PRODUCAO,
            "terminal": "TPS1",
            "pavimento": "Terreo",
            "setor": "Seguranca",
            "ambiente": "Sala de controle",
            "ip": f"10.20.{indice // 250}.{indice % 250 + 1}",
            "mascara_subrede": "255.255.255.0",
            "gateway": "10.20.0.254",
            "vlan": 100,
            "farm": "Farm E6",
            "retencao_esperada_dias": 30,
            "codec": "H.264",
            "origem_cadastro": Camera.OrigemCadastro.MANUAL,
            "status": Camera.StatusCamera.ONLINE,
        }
        valores.update(atributos)
        return Camera.objects.create(**valores)

    def exportar_csv(self, **params):
        response = self.client.get(
            reverse("cameras:exportar"),
            {"formato": "csv", "campos": ["nome", "ip"], **params},
        )
        if response.status_code != 200:
            return response, []
        content = (
            b"".join(response.streaming_content)
            if response.streaming
            else response.content
        )
        response.e6_export_body = content
        rows = list(csv.reader(io.StringIO(content.decode("utf-8-sig"))))
        return response, rows

    def test_exportacao_usa_os_filtros_atuais_sem_paginar_e_mantem_ordem(self):
        alvo = self.criar_camera(1, nome="ALVO E6 A")
        self.criar_camera(2, nome="ALVO E6 B")
        self.criar_camera(3, nome="ALVO E6 C", status=Camera.StatusCamera.OFFLINE)
        self.criar_camera(4, nome="OUTRO E6")

        response, rows = self.exportar_csv(
            q="ALVO E6",
            status="ONLINE",
            situacao_operacional="PRODUCAO",
            ordenacao="-nome",
            page="99",
            parametro_desconhecido="nao-exportar",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"].split(";")[0], "text/csv")
        self.assertEqual(rows[0][0], "Nome")
        self.assertEqual(len(rows[0]), 2)
        self.assertEqual([row[0] for row in rows[1:]], ["ALVO E6 B", "ALVO E6 A"])
        self.assertNotIn("CAM-E6-00003", str(rows))
        self.assertNotIn("OUTRO E6", str(rows))
        self.assertEqual(Camera.objects.count(), 4)
        self.assertTrue(Camera.objects.filter(pk=alvo.pk).exists())

    def test_exportacao_aplica_individualmente_os_filtros_do_inventario(self):
        camera = self.criar_camera(
            1,
            nome="CAMERA ALVO E6",
            status=Camera.StatusCamera.ONLINE,
            situacao_operacional=Camera.SituacaoOperacional.PRODUCAO,
        )
        filtros = (
            {"q": "ALVO E6"},
            {"status": "ONLINE"},
            {"situacao_operacional": "PRODUCAO"},
            {"completude": "COMPLETO"},
            {"terminal": "TPS1"},
            {"tipo": Camera.TipoCamera.DOME},
            {"fabricante": "axis"},
            {"vlan": "0100"},
            {"farm": "farm e6"},
        )

        for filtro in filtros:
            with self.subTest(filtro=filtro):
                response, rows = self.exportar_csv(**filtro)
                self.assertEqual(response.status_code, 200)
                self.assertEqual([row[0] for row in rows[1:]], [camera.nome])

    def test_csv_trata_unicode_nulos_formulas_e_exclui_dados_internos(self):
        camera = self.criar_camera(
            1,
            nome="=1+1",
            ip=None,
            firmware_version="SEGREDO-FIRMWARE-E6",
            motivo_desativacao="SEGREDO-MOTIVO-E6",
        )
        response, rows = self.exportar_csv(q="=1+1")

        self.assertEqual(response.status_code, 200)
        self.assertTrue(rows[1][0].startswith("'"))
        self.assertEqual(rows[1][1], "")
        self.assertNotIn("SEGREDO-FIRMWARE-E6", response_content(response))
        self.assertNotIn("SEGREDO-MOTIVO-E6", response_content(response))
        self.assertTrue(Camera.objects.filter(pk=camera.pk).exists())

        unicode_camera = self.criar_camera(2, nome="Câmera São José — Pátio")
        unicode_response, unicode_rows = self.exportar_csv(campos=["nome"])
        self.assertEqual(unicode_response.status_code, 200)
        self.assertIn(unicode_camera.nome, [row[0] for row in unicode_rows[1:]])

    def test_csv_protege_todos_os_prefixos_de_formula_planilhada(self):
        valores_perigosos = (
            "=1+1",
            "+SUM(1,1)",
            "-1+1",
            "@SUM(A1:A2)",
            "  =HYPERLINK(\"https://example.invalid\")",
        )
        for indice, nome in enumerate(valores_perigosos, start=1):
            self.criar_camera(indice, nome=nome)

        response, rows = self.exportar_csv(campos=["nome"])

        self.assertEqual(response.status_code, 200)
        self.assertEqual(rows[0], ["Nome"])
        self.assertEqual(len(rows) - 1, len(valores_perigosos))
        self.assertTrue(all(row[0].startswith("'") for row in rows[1:]))

    def test_campos_tamperados_sao_rejeitados_sem_expor_atributos_internos(self):
        self.criar_camera(1, firmware_version="NAO-EXPORTAR-E6")
        response = self.client.get(
            reverse("cameras:exportar"),
            {
                "formato": "csv",
                "campos": ["nome", "firmware_version", "__class__"],
                "q": "CAM-E6",
            },
        )

        self.assertNotEqual(response.status_code, 200)
        self.assertNotIn("NAO-EXPORTAR-E6", response_content(response))

    def test_exportacao_omite_credenciais_e_versoes_criptografadas(self):
        camera = self.criar_camera(1)
        credential = CameraCredential.objects.create(
            camera=camera,
            state=CameraCredential.State.ACTIVE,
        )
        version = CameraCredentialVersion.objects.create(
            credential=credential,
            version=1,
            ciphertext="SEGREDO-CIFRADO-E6",
            key_version="fixture-e6",
            state=CameraCredentialVersion.State.ACTIVE,
        )
        credential.active_version = version
        credential.save(update_fields=["active_version"])

        response = self.client.get(
            reverse("cameras:exportar"),
            {
                "formato": "csv",
                "campos": [field["key"] for field in EXPORT_FIELDS],
            },
        )
        body = response_content(response)

        self.assertEqual(response.status_code, 200)
        self.assertNotIn("SEGREDO-CIFRADO-E6", body)
        self.assertNotIn("ciphertext", body.casefold())

    def test_inventario_vazio_retorna_feedback_sem_arquivo_vazio(self):
        response = self.client.get(
            reverse("cameras:exportar"),
            {"formato": "csv", "campos": ["nome"], "q": "sem-resultados"},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Nenhuma câmera")
        self.assertNotIn("text/csv", response.get("Content-Type", ""))

    def test_formulario_de_exportacao_preserva_filtros_multiplos_e_ignora_pagina(self):
        response = self.client.get(
            reverse("cameras:lista"),
            {"status": ["ONLINE", "OFFLINE"], "terminal": ["TPS1", "TPS2"], "page": "2"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["query_params"].getlist("status"), ["ONLINE", "OFFLINE"])
        export_params = response.context["export_query_params"]
        self.assertEqual(
            [value for name, value in export_params if name == "status"],
            ["ONLINE", "OFFLINE"],
        )
        self.assertEqual(
            [value for name, value in export_params if name == "terminal"],
            ["TPS1", "TPS2"],
        )
        self.assertNotIn("page", [name for name, _ in export_params])

    def test_exportacao_exige_a_mesma_permissao_de_leitura_do_inventario(self):
        sem_permissao = get_user_model().objects.create_user(
            username="e6-export-sem-permissao",
            password="test-password",
        )
        self.client.force_login(sem_permissao)

        response = self.client.get(
            reverse("cameras:exportar"),
            {"formato": "csv", "campos": ["nome"]},
        )

        self.assertEqual(response.status_code, 403)

    @unittest.skipUnless(REPORTLAB_AVAILABLE, "ReportLab não está instalado neste ambiente.")
    def test_pdf_gera_documento_com_assinatura_pdf(self):
        self.criar_camera(
            1,
            nome="Câmera São José",
            observacoes="São José — câmera dômica; conteúdo Unicode.",
        )

        response = self.client.get(
            reverse("cameras:exportar"),
            {"formato": "pdf", "campos": ["nome", "observacoes"]},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"].split(";")[0], "application/pdf")
        body = (
            b"".join(response.streaming_content)
            if response.streaming
            else response.content
        )
        self.assertTrue(body.startswith(b"%PDF-"))

    @unittest.skipIf(REPORTLAB_AVAILABLE, "A dependência PDF está disponível.")
    def test_pdf_indisponivel_retorna_feedback_sem_erro_tecnico(self):
        self.criar_camera(1)

        response = self.client.get(
            reverse("cameras:exportar"),
            {"formato": "pdf", "campos": ["nome"]},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertNotIn("application/pdf", response.get("Content-Type", ""))
        self.assertContains(response, "PDF")
        self.assertNotContains(response, "ImportError")

    def test_pdf_aplica_orcamento_de_registros_e_campos_de_texto(self):
        camera = self.criar_camera(1, observacoes="x" * (PDF_MAX_FREE_TEXT_CHARS + 1))
        campos = selected_fields(["observacoes"])

        with self.assertRaises(PdfExportLimitExceeded):
            validate_pdf_limits(
                Camera.objects.filter(pk=camera.pk),
                campos,
                1,
            )
        with self.assertRaises(PdfExportLimitExceeded):
            validate_pdf_limits(Camera.objects.none(), selected_fields(["nome"]), PDF_MAX_RECORDS + 1)

    def test_pdf_quebra_texto_longo_com_medicoes_lineares(self):
        class CountingMetrics:
            calls = 0

            def stringWidth(self, text, _font_name, font_size):
                self.calls += 1
                return len(text) * font_size

        text = "x" * 10_000
        metrics = CountingMetrics()
        lines = _wrap_text(text, "fake", 1, 20, metrics)

        self.assertEqual("".join(lines), text)
        self.assertLessEqual(metrics.calls, len(text) + 2)

    @unittest.skip(
        "BC-AUTH concede cameras.view_camera em nível de modelo e não define escopo por registro/tenant."
    )
    def test_usuario_fora_do_escopo_de_registros_e_negado(self):
        self.fail("Não existe escopo por registro definido no contrato vigente.")

    def test_exporta_2300_registros_mesmo_quando_pagina_solicitada_nao_existe(self):
        quantidade = 2300
        Camera.objects.bulk_create(
            [
                Camera(
                    patrimonio=f"VOLUME-{indice:05d}",
                    nome=f"VOLUME E6 {indice:05d}",
                    fabricante="AXIS",
                    modelo="MODELO VOLUME",
                    serial=f"VOL-SERIAL-{indice:05d}",
                    situacao_operacional=Camera.SituacaoOperacional.PRODUCAO,
                )
                for indice in range(quantidade)
            ],
            batch_size=500,
        )

        response, rows = self.exportar_csv(campos="nome", page="999")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(rows) - 1, quantidade)
        self.assertEqual(rows[0], ["Nome"])
        self.assertEqual(Camera.objects.count(), quantidade)

    def test_exportacao_nao_muta_camera_captura_ou_galeria_lifecycle(self):
        camera = self.criar_camera(1)
        before = {
            "camera": tuple(Camera.objects.values_list("status", "status_em", "ultima_verificacao").get(pk=camera.pk)),
            "captures": CameraCaptureJob.objects.count(),
            "images": CameraImageRecord.objects.count(),
        }

        response, _ = self.exportar_csv(q="CAM-E6-00001")

        self.assertEqual(response.status_code, 200)
        after = {
            "camera": tuple(Camera.objects.values_list("status", "status_em", "ultima_verificacao").get(pk=camera.pk)),
            "captures": CameraCaptureJob.objects.count(),
            "images": CameraImageRecord.objects.count(),
        }
        self.assertEqual(after, before)


def response_content(response):
    if hasattr(response, "e6_export_body"):
        body = response.e6_export_body
    elif getattr(response, "streaming", False):
        body = b"".join(response.streaming_content)
    else:
        body = response.content
    return body.decode("utf-8", errors="replace")


class FiltrosInventarioTests(TestCase):
    def test_parametros_invalidos_e_desconhecidos_sao_canonizados(self):
        params = QueryDict(
            "status=INVALIDO&status=ONLINE&status=ONLINE&vlan=0&vlan=0100"
            "&ordenacao=__class__&foo=bar&q=++CAMERA++"
        )

        filtros = FiltrosInventario.de_parametros(params)
        query = filtros.para_querydict()

        self.assertEqual(filtros.q, "CAMERA")
        self.assertEqual(filtros.status, ("ONLINE",))
        self.assertEqual(filtros.vlan, ("100",))
        self.assertEqual(filtros.ordenacao, "nome")
        self.assertEqual(query.getlist("status"), ["ONLINE"])
        self.assertEqual(query.getlist("vlan"), ["100"])
        self.assertNotIn("foo", query)
        self.assertNotIn("page", query)
