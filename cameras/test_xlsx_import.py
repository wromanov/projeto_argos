import hashlib
import io
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .auditoria import registrar_evento as registrar_evento_real
from .models import Camera, CameraImportPreview, EventoAuditoria
from .xlsx_import import ImportFileError, _validated_plan, build_template, confirm_preview, parse_xlsx, preview_xlsx


class CameraXlsxImportTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="importer", password="unused")
        self.user.user_permissions.add(*Permission.objects.filter(
            content_type__app_label="cameras",
            codename__in=("importar_cameras", "add_camera", "change_camera"),
        ))

    def row(self, line=2, **values):
        defaults = {
            "operacao": "CRIAR", "patrimonio": f"P-{line}", "nome": f"Camera {line}",
            "fabricante": "Acme", "modelo": "M1", "serial": f"S-{line}",
            "situacao_operacional": "ESTOQUE",
        }
        defaults.update(values)
        if defaults["operacao"] == "ATUALIZAR" and "situacao_operacional" not in values:
            defaults["situacao_operacional"] = ""
        return {"line": line, "values": defaults}

    def make_preview(self, rows):
        raw = b"synthetic-xlsx-payload"
        with patch("cameras.xlsx_import.parse_xlsx", return_value=(raw, rows)):
            return preview_xlsx(object(), self.user)

    def test_create_update_and_audit_are_persisted_together(self):
        camera = Camera.objects.create(nome="Existing", fabricante="Acme", modelo="M1", patrimonio="P-OLD", serial="S-OLD", situacao_operacional="ESTOQUE")
        old_name = camera.nome
        preview = self.make_preview([
            self.row(2),
            self.row(3, operacao="ATUALIZAR", patrimonio="P-OLD", serial="", nome="Renamed", fabricante="", modelo=""),
        ])
        self.assertTrue(preview.resumo["can_confirm"], preview.resumo)
        self.assertEqual(preview.resumo["update"], 1)
        self.assertEqual(preview.resumo["changes"], 1)
        update_row = preview.plano[1]
        self.assertEqual(update_row["target_label"], old_name)
        self.assertEqual(update_row["changes"]["nome"]["anterior"], old_name)
        self.assertEqual(update_row["changes"]["nome"]["atual"], "RENAMED")
        result = confirm_preview(preview, self.user)
        self.assertEqual((result["created"], result["updated"]), (1, 1))
        camera.refresh_from_db()
        self.assertEqual(camera.nome, "RENAMED")
        self.assertEqual(camera.fabricante, "ACME")
        self.assertEqual(camera.origem_cadastro, Camera.OrigemCadastro.MANUAL)
        self.assertEqual(EventoAuditoria.objects.filter(codigo="camera.importada").count(), 2)
        update_event = EventoAuditoria.objects.get(codigo="camera.importada", camera=camera)
        self.assertEqual(update_event.alteracoes["nome"], {"anterior": old_name, "atual": "RENAMED"})
        self.assertEqual(EventoAuditoria.objects.get(codigo="camera.importacao.concluida").metadados["resultado"], "SUCESSO")

    def test_unchanged_update_preview_has_no_field_changes(self):
        camera = Camera.objects.create(nome="Existing", fabricante="Acme", modelo="M1", patrimonio="P-OLD", serial="S-OLD", situacao_operacional="ESTOQUE")
        preview = self.make_preview([
            self.row(2, operacao="ATUALIZAR", patrimonio="P-OLD", serial="", nome="", fabricante="", modelo=""),
        ])
        self.assertEqual(preview.resumo["update"], 1)
        self.assertEqual(preview.resumo["changes"], 0)
        self.assertEqual(preview.plano[0]["target_label"], camera.nome)
        self.assertEqual(preview.plano[0]["changes"], {})

    def test_identifier_split_and_duplicate_targets_block_whole_preview(self):
        Camera.objects.create(nome="One", fabricante="A", modelo="1", patrimonio="P1", serial="S1", situacao_operacional="ESTOQUE")
        Camera.objects.create(nome="Two", fabricante="A", modelo="1", patrimonio="P2", serial="S2", situacao_operacional="ESTOQUE")
        plan, errors = _validated_plan([
            self.row(2, operacao="ATUALIZAR", patrimonio="P1", serial="S2"),
            self.row(3, operacao="ATUALIZAR", patrimonio="P1", serial=""),
            self.row(4, operacao="ATUALIZAR", patrimonio="P1", serial=""),
        ])
        self.assertTrue(errors)
        self.assertEqual(Camera.objects.count(), 2)
        self.assertTrue(any("câmeras diferentes" in error["message"] for error in errors))
        self.assertTrue(any("também é referenciada" in error["message"] for error in errors))

    def test_explicit_clear_and_empty_update_semantics(self):
        camera = Camera.objects.create(nome="Before", fabricante="Acme", modelo="M1", patrimonio="P-1", serial="S-1", terminal="T1", situacao_operacional="ESTOQUE")
        preview = self.make_preview([self.row(2, operacao="ATUALIZAR", patrimonio="P-1", serial="", nome="", fabricante="", modelo="", terminal="LIMPAR")])
        confirm_preview(preview, self.user)
        camera.refresh_from_db()
        self.assertEqual(camera.nome, "BEFORE")
        self.assertEqual(camera.terminal, "")

    def test_update_can_complement_a_missing_identifier_after_preview(self):
        camera = Camera.objects.create(nome="Legacy", fabricante="Acme", modelo="M1", patrimonio="P-LEGACY", serial=None, situacao_operacional="ESTOQUE")
        preview = self.make_preview([self.row(2, operacao="ATUALIZAR", patrimonio=" p-legacy ", serial="s-added", nome="", fabricante="", modelo="")])
        self.assertTrue(preview.resumo["can_confirm"], preview.resumo)
        confirm_preview(preview, self.user)
        camera.refresh_from_db()
        self.assertEqual(camera.serial, "S-ADDED")

    def test_preview_expiry_and_single_use_are_enforced(self):
        preview = self.make_preview([self.row()])
        preview.expira_em = timezone.now()
        preview.save(update_fields=("expira_em",))
        with self.assertRaises(TimeoutError):
            confirm_preview(preview, self.user)

    def test_audit_failure_rolls_back_every_camera(self):
        preview = self.make_preview([self.row(2), self.row(3)])
        calls = {"count": 0}

        def fail_on_second(**kwargs):
            calls["count"] += 1
            if calls["count"] == 2:
                raise RuntimeError("simulated audit failure")
            return registrar_evento_real(**kwargs)

        with patch("cameras.xlsx_import.registrar_evento", side_effect=fail_on_second):
            with self.assertRaises(RuntimeError):
                confirm_preview(preview, self.user)
        self.assertEqual(Camera.objects.count(), 0)
        self.assertEqual(EventoAuditoria.objects.count(), 0)
        preview.refresh_from_db()
        self.assertIsNone(preview.consumido_em)

    def test_scale_validation_for_2300_synthetic_rows(self):
        rows = [self.row(i + 2) for i in range(2300)]
        preview = self.make_preview(rows)
        self.assertTrue(preview.resumo["can_confirm"])
        result = confirm_preview(preview, self.user)
        self.assertEqual(result["created"], 2300)
        self.assertEqual(Camera.objects.count(), 2300)

    def test_upload_payload_is_bound_by_sha256(self):
        preview = self.make_preview([self.row()])
        self.assertEqual(preview.file_sha256, hashlib.sha256(b"synthetic-xlsx-payload").hexdigest())

    def test_preview_has_no_camera_write_and_rechecks_create_conflicts(self):
        preview = self.make_preview([self.row()])
        self.assertEqual(Camera.objects.count(), 0)
        Camera.objects.create(nome="Competing", fabricante="A", modelo="1", patrimonio="P-2", serial="S-2", situacao_operacional="ESTOQUE")
        with self.assertRaises(ValueError):
            confirm_preview(preview, self.user)
        self.assertEqual(Camera.objects.count(), 1)

    def test_import_permission_is_required_before_preview_creation(self):
        self.user.user_permissions.clear()
        with patch("cameras.xlsx_import.parse_xlsx", return_value=(b"data", [self.row()])):
            with self.assertRaises(PermissionError):
                preview_xlsx(object(), self.user)
        self.assertEqual(CameraImportPreview.objects.count(), 0)

    def test_malformed_and_oversized_uploads_are_rejected(self):
        malformed = SimpleUploadedFile("bad.xlsx", b"PKnot-a-zip")
        with self.assertRaises(ImportFileError):
            parse_xlsx(malformed)
        oversized = SimpleUploadedFile("large.xlsx", b"PK" + b"0" * (10 * 1024 * 1024))
        with self.assertRaises(ImportFileError):
            parse_xlsx(oversized)

    def test_official_template_round_trips_and_formula_is_rejected(self):
        from openpyxl import load_workbook

        workbook = load_workbook(io.BytesIO(build_template()))
        sheet = workbook["Cameras"]
        columns = {cell.value: cell.column for cell in sheet[1]}
        values = {
            "OPERAÇÃO": "CRIAR", "PATRIMÔNIO": "XLSX-001", "NOME": "Sample",
            "FABRICANTE": "Acme", "MODELO": "M1", "SITUAÇÃO OPERACIONAL": "ESTOQUE",
        }
        for header, value in values.items():
            sheet.cell(2, columns[header]).value = value
        output = io.BytesIO()
        workbook.save(output)
        parsed = parse_xlsx(SimpleUploadedFile("template.xlsx", output.getvalue()))
        self.assertEqual(parsed[1][0]["values"]["operacao"], "CRIAR")
        self.assertEqual(parsed[1][0]["values"]["patrimonio"], "XLSX-001")

        sheet["B2"] = "=1+1"
        output = io.BytesIO()
        workbook.save(output)
        with self.assertRaises(ImportFileError):
            parse_xlsx(SimpleUploadedFile("formula.xlsx", output.getvalue()))

    def test_ssr_upload_preview_and_explicit_confirmation_flow(self):
        self.client.force_login(self.user)
        template_response = self.client.get(reverse("cameras:importar_template"))
        self.assertEqual(template_response.status_code, 200)
        self.assertEqual(template_response["Content-Type"], "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        self.assertTrue(template_response.content.startswith(b"PK"))
        upload = SimpleUploadedFile("cameras.xlsx", b"PKmock-content")
        with patch("cameras.views.preview_xlsx") as create_preview:
            preview = self.make_preview([self.row()])
            create_preview.return_value = preview
            response = self.client.post(reverse("cameras:importar"), {"arquivo": upload})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Confirmar importação completa")
        self.assertEqual(Camera.objects.count(), 0)
        response = self.client.post(reverse("cameras:confirmar_importacao", args=(preview.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Lote aplicado integralmente")
        self.assertEqual(Camera.objects.count(), 1)
