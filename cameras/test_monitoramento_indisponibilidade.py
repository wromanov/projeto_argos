"""Testes de schema e integridade do histórico MON-06B em SQLite real."""

from datetime import datetime, timedelta, timezone

from django.db import IntegrityError, connection, transaction
from django.db.models.deletion import ProtectedError
from django.test import TestCase

from cameras.models import (
    Camera,
    EventoAuditoria,
    Indisponibilidade,
    TransicaoEstadoMonitoramento,
)


START = datetime(2026, 1, 1, tzinfo=timezone.utc)


class IndisponibilidadeSchemaTests(TestCase):
    def camera(self, suffix=1):
        return Camera.objects.create(
            nome=f"CAM-{suffix}",
            fabricante="FAB",
            modelo="MOD",
            serial=f"SER-{suffix}",
            mac=f"00:11:22:33:44:{suffix:02X}",
            tipo=Camera.TipoCamera.BULLET,
            terminal="T",
            pavimento="P",
            setor="S",
            ambiente="A",
            ip=f"10.0.0.{suffix + 1}",
            mascara_subrede="255.255.255.0",
            gateway="10.0.0.1",
            vlan=10,
            farm="F",
            retencao_esperada_dias=1,
            codec="H264",
        )

    def transition(self, camera, suffix=1, at=START, before="ONLINE", after="OFFLINE"):
        return TransicaoEstadoMonitoramento.objects.create(
            camera=camera,
            estado_anterior=before,
            estado_atual=after,
            ocorrida_em=at + timedelta(seconds=suffix),
        )

    def interval(self, camera, *, origin="ONLINE_TO_OFFLINE", closed_at=None, reason=None,
                 opening=None, closing=None, opened_at=START):
        return Indisponibilidade.objects.create(
            camera=camera,
            opened_at=opened_at,
            closed_at=closed_at,
            open_origin=origin,
            close_reason=reason,
            opening_transition=opening or self.transition(camera),
            closing_transition=closing,
        )

    def assert_database_rejects(self, factory):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                factory()

    def test_schema_contains_checks_unique_open_and_justified_indexes(self):
        with connection.cursor() as cursor:
            constraints = connection.introspection.get_constraints(
                cursor, Indisponibilidade._meta.db_table
            )

        expected_constraints = {
            "indisp_open_origin_valid",
            "indisp_close_reason_valid",
            "indisp_closed_at_after_opened_at",
            "indisp_open_closed_coherent",
            "indisp_close_reason_transition_coherent",
            "indisp_one_open_camera",
        }
        self.assertTrue(expected_constraints.issubset(constraints))
        self.assertTrue(constraints["indisp_one_open_camera"]["unique"])
        self.assertTrue(constraints["indisp_one_open_camera"]["columns"] == ["camera_id"])
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT sql FROM sqlite_master WHERE name = %s",
                ["indisp_one_open_camera"],
            )
            unique_sql = cursor.fetchone()[0]
        self.assertIn("WHERE \"closed_at\" IS NULL", unique_sql)

        index_names = {
            index.name
            for index in Indisponibilidade._meta.indexes
        }
        self.assertEqual(index_names, {"indisp_camera_opened_idx"})

    def test_open_interval_is_valid_and_both_origins_are_accepted(self):
        for suffix, origin in enumerate(
            (Indisponibilidade.OrigemAbertura.INITIAL_OFFLINE,
             Indisponibilidade.OrigemAbertura.ONLINE_TO_OFFLINE),
            start=1,
        ):
            with self.subTest(origin=origin):
                interval = self.interval(self.camera(suffix), origin=origin)
                self.assertIsNone(interval.closed_at)
                self.assertIsNone(interval.close_reason)
                self.assertIsNone(interval.closing_transition)

    def test_invalid_open_origin_is_rejected_by_sqlite(self):
        camera = self.camera()
        self.assert_database_rejects(
            lambda: self.interval(camera, origin="MANUAL")
        )

    def test_only_one_open_interval_per_camera(self):
        camera = self.camera()
        self.interval(camera)
        second_transition = self.transition(camera, suffix=2)
        self.assert_database_rejects(
            lambda: self.interval(camera, opening=second_transition)
        )

    def test_distinct_cameras_can_have_open_intervals(self):
        first = self.interval(self.camera(1))
        second = self.interval(self.camera(2))
        self.assertIsNone(first.closed_at)
        self.assertIsNone(second.closed_at)

    def test_recovered_interval_is_valid_only_with_closing_transition(self):
        camera = self.camera()
        opening = self.transition(camera)
        closing = self.transition(camera, suffix=2, before="OFFLINE", after="ONLINE")
        interval = self.interval(
            camera,
            opening=opening,
            closing=closing,
            closed_at=START + timedelta(minutes=5),
            reason=Indisponibilidade.MotivoFechamento.RECUPERADA,
        )
        self.assertEqual(interval.close_reason, "RECUPERADA")

    def test_scope_exit_interval_is_valid_without_closing_transition(self):
        camera = self.camera()
        interval = self.interval(
            camera,
            closed_at=START + timedelta(minutes=5),
            reason=Indisponibilidade.MotivoFechamento.SAIU_DO_ESCOPO,
        )
        self.assertEqual(interval.close_reason, "SAIU_DO_ESCOPO")
        self.assertIsNone(interval.closing_transition)

    def test_open_interval_with_close_reason_is_rejected(self):
        camera = self.camera()
        self.assert_database_rejects(
            lambda: self.interval(
                camera, reason=Indisponibilidade.MotivoFechamento.RECUPERADA
            )
        )

    def test_open_interval_with_closing_transition_is_rejected(self):
        camera = self.camera()
        closing = self.transition(camera, suffix=2, before="OFFLINE", after="ONLINE")
        self.assert_database_rejects(
            lambda: self.interval(camera, closing=closing)
        )

    def test_closed_interval_without_close_reason_is_rejected(self):
        camera = self.camera()
        self.assert_database_rejects(
            lambda: self.interval(camera, closed_at=START + timedelta(minutes=5))
        )

    def test_recovered_interval_without_closing_transition_is_rejected(self):
        camera = self.camera()
        self.assert_database_rejects(
            lambda: self.interval(
                camera,
                closed_at=START + timedelta(minutes=5),
                reason="RECUPERADA",
            )
        )

    def test_scope_exit_interval_with_closing_transition_is_rejected(self):
        camera = self.camera()
        closing = self.transition(camera, suffix=2, before="OFFLINE", after="ONLINE")
        self.assert_database_rejects(
            lambda: self.interval(
                camera,
                closed_at=START + timedelta(minutes=5),
                reason="SAIU_DO_ESCOPO",
                closing=closing,
            )
        )

    def test_closed_before_opened_is_rejected(self):
        camera = self.camera()
        self.assert_database_rejects(
            lambda: self.interval(
                camera,
                opened_at=START,
                closed_at=START - timedelta(seconds=1),
                reason="SAIU_DO_ESCOPO",
            )
        )

    def test_opening_transition_cannot_be_reused(self):
        first_camera = self.camera(1)
        second_camera = self.camera(2)
        opening = self.transition(first_camera)
        self.interval(first_camera, opening=opening)
        self.assert_database_rejects(
            lambda: self.interval(second_camera, opening=opening)
        )

    def test_closing_transition_cannot_be_reused(self):
        first_camera = self.camera(1)
        second_camera = self.camera(2)
        closing = self.transition(first_camera, suffix=2, before="OFFLINE", after="ONLINE")
        self.interval(
            first_camera,
            closed_at=START + timedelta(minutes=5),
            reason="RECUPERADA",
            closing=closing,
        )
        self.assert_database_rejects(
            lambda: self.interval(
                second_camera,
                closed_at=START + timedelta(minutes=5),
                reason="RECUPERADA",
                closing=closing,
            )
        )

    def test_invalid_close_reason_is_rejected_by_sqlite(self):
        camera = self.camera()
        self.assert_database_rejects(
            lambda: self.interval(
                camera,
                closed_at=START + timedelta(minutes=5),
                reason="TIMEOUT",
            )
        )

    def test_camera_delete_is_protected_by_historical_foreign_key(self):
        camera = self.camera()
        self.interval(camera)
        with self.assertRaises(ProtectedError):
            camera.delete()
        self.assertTrue(Camera.objects.filter(pk=camera.pk).exists())

    def test_schema_does_not_create_audit_history_or_change_legacy_camera_columns(self):
        camera_columns = {
            column.name
            for column in connection.introspection.get_table_description(
                connection.cursor(), Camera._meta.db_table
            )
        }
        self.assertTrue({"status", "status_em", "ultima_verificacao"}.issubset(camera_columns))
        self.assertFalse({"opened_at", "closed_at", "open_origin"}.intersection(camera_columns))
        self.assertEqual(EventoAuditoria.objects.count(), 0)
        self.assertNotEqual(Indisponibilidade._meta.db_table, EventoAuditoria._meta.db_table)
