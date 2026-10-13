"""Integração server-rendered do boundary MON-07B (MON-07C)."""

from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db import connection
from django.test import TestCase
from django.test.utils import CaptureQueriesContext
from django.urls import reverse
from django.utils import timezone

from cameras.models import Camera, EstadoMonitoramento, Indisponibilidade, TransicaoEstadoMonitoramento
from cameras.monitoramento.presentation import camera_health_presentation_labels


class MonitoringUITests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_superuser("monitor-ui", "monitor@example.com", "senha")
        self.client.force_login(self.user)
        self.now = timezone.now()

    def camera(self, number=1, **overrides):
        values = {"nome": f"CAM-UI-{number}", "patrimonio": f"PAT-{number}", "fabricante": "Fab", "modelo": "Model",
                  "serial": f"SER-{number}", "mac": f"00:11:22:33:44:{number:02X}", "tipo": "BULLET", "terminal": "T",
                  "pavimento": "P", "setor": "S", "ambiente": "A", "ip": f"10.0.0.{number}", "mascara_subrede": "255.255.255.0",
                  "gateway": "10.0.0.1", "vlan": 1, "farm": "F", "retencao_esperada_dias": 1, "codec": "H264",
                  "status": "ONLINE", "situacao_operacional": Camera.SituacaoOperacional.PRODUCAO}
        values.update(overrides)
        return Camera.objects.create(**values)

    def state(self, camera, stable="ONLINE", evidence=None, **overrides):
        values = {"estado_estavel": stable, "estado_alterado_em": self.now - timedelta(hours=1),
                  "ultima_evidencia_util_em": evidence or self.now, "em_escopo": True}
        values.update(overrides)
        return EstadoMonitoramento.objects.create(camera=camera, **values)

    def outage(self, camera, opened_at, closed_at=None):
        opening = TransicaoEstadoMonitoramento.objects.create(camera=camera, estado_anterior="ONLINE", estado_atual="OFFLINE", ocorrida_em=opened_at)
        closing = None
        if closed_at:
            closing = TransicaoEstadoMonitoramento.objects.create(camera=camera, estado_anterior="OFFLINE", estado_atual="ONLINE", ocorrida_em=closed_at)
        return Indisponibilidade.objects.create(camera=camera, opened_at=opened_at, closed_at=closed_at,
            open_origin="ONLINE_TO_OFFLINE", close_reason="RECUPERADA" if closed_at else None,
            opening_transition=opening, closing_transition=closing)

    def test_inventory_and_detail_follow_canonical_state_not_legacy_status(self):
        camera = self.camera(status="ONLINE")
        self.state(camera, stable="OFFLINE", evidence=self.now)
        response = self.client.get(reverse("cameras:lista"))
        self.assertContains(response, "OFFLINE")
        self.assertNotContains(response, "Status técnico</th>")
        detail = self.client.get(reverse("cameras:detalhe", args=[camera.pk]))
        self.assertContains(detail, "Estado atual")
        self.assertContains(detail, "Offline")
        self.assertNotContains(detail, "Última verificação")

    def test_stale_and_out_of_scope_are_not_rendered_as_current_offline(self):
        stale = self.camera(2, status="OFFLINE")
        self.state(stale, stable="OFFLINE", evidence=self.now - timedelta(days=1))
        self.outage(stale, self.now - timedelta(hours=2))
        scoped_out = self.camera(3, status="OFFLINE", situacao_operacional=Camera.SituacaoOperacional.ESTOQUE)
        self.state(scoped_out, stable="OFFLINE", evidence=self.now)
        response = self.client.get(reverse("cameras:lista"))
        self.assertContains(response, "Dados desatualizados")
        self.assertContains(response, "Desconhecido")
        self.assertContains(response, "Não monitorada")
        self.assertContains(response, "Dados desatualizados · último estado Offline")
        self.assertNotContains(response, "Offline há")

    def test_inventory_uses_canonical_labels_for_every_effective_state(self):
        online = self.camera(4)
        offline = self.camera(5)
        stale = self.camera(6)
        out_of_scope = self.camera(7, situacao_operacional=Camera.SituacaoOperacional.ESTOQUE)
        self.state(online, stable="ONLINE", evidence=self.now)
        self.state(offline, stable="OFFLINE", evidence=self.now)
        self.state(stale, stable="OFFLINE", evidence=self.now - timedelta(days=1))
        self.state(out_of_scope, stable="ONLINE", evidence=self.now)

        response = self.client.get(reverse("cameras:lista"))
        html = response.content.decode("utf-8")
        for label in ("Online", "Offline", "Desconhecido", "Não monitorada"):
            self.assertIn(label, html)
        for variant in ("badge--online", "badge--offline", "badge--unknown", "badge--out_of_scope"):
            self.assertIn(variant, html)
        self.assertIn('data-label="Monitoramento"', html)
        self.assertIn("Dados desatualizados · último estado Offline", html)
        self.assertEqual(response.context["monitoring_state_labels"]["UNKNOWN"], "Desconhecido")
        self.assertEqual(response.context["monitoring_state_labels"]["OUT_OF_SCOPE"], "Não monitorada")

    def test_camera_health_summary_localizes_values_without_changing_technical_projection(self):
        camera = self.camera(8)
        response = self.client.get(reverse("cameras:detalhe", args=[camera.pk]))

        self.assertEqual(
            response.context["camera_health_labels"],
            {"evidence_state": "Não determinada", "freshness": "Não determinado"},
        )
        self.assertEqual(response.context["camera_health"].evidence_state, "UNKNOWN")
        self.assertEqual(response.context["camera_health"].freshness, "UNKNOWN")
        self.assertContains(response, "Não determinada")
        self.assertContains(response, "Não determinado")
        for code in ("UNKNOWN", "CURRENT", "FRESH", "STALE"):
            self.assertNotContains(response, code)
        self.assertEqual(
            camera_health_presentation_labels("CURRENT", "FRESH"),
            {"evidence_state": "Atual", "freshness": "Atualizado"},
        )
        self.assertEqual(
            camera_health_presentation_labels("UNKNOWN", "STALE"),
            {"evidence_state": "Não determinada", "freshness": "Desatualizado"},
        )

    def test_unknown_is_not_presented_as_a_confirmed_last_state(self):
        camera = self.camera(9)
        self.state(camera, stable="UNKNOWN", evidence=self.now - timedelta(days=1))

        response = self.client.get(reverse("cameras:detalhe", args=[camera.pk]))

        self.assertFalse(response.context["monitoring"]["has_confirmed_state"])
        self.assertNotContains(response, "Último estado confirmado")
        self.assertContains(response, "Estado atual")
        self.assertContains(response, "Desconhecido")

    def test_last_confirmed_state_remains_for_confirmed_online_or_offline_values(self):
        for index, stable in enumerate(("ONLINE", "OFFLINE"), start=10):
            with self.subTest(stable=stable):
                camera = self.camera(index)
                self.state(camera, stable=stable, evidence=self.now - timedelta(days=1))

                response = self.client.get(reverse("cameras:detalhe", args=[camera.pk]))

                self.assertTrue(response.context["monitoring"]["has_confirmed_state"])
                self.assertContains(response, "Último estado confirmado")
                self.assertContains(response, "Online" if stable == "ONLINE" else "Offline")

    def test_detail_preview_and_paginated_history_are_technical_only(self):
        camera = self.camera()
        self.state(camera, stable="OFFLINE")
        for index in range(23):
            self.outage(camera, self.now - timedelta(days=index + 1), self.now - timedelta(days=index, hours=23))
        detail = self.client.get(reverse("cameras:detalhe", args=[camera.pk]))
        self.assertContains(detail, "Histórico técnico de indisponibilidades")
        self.assertContains(detail, "Ver histórico completo")
        history = self.client.get(reverse("cameras:historico_monitoramento", args=[camera.pk]), {"page": 2})
        self.assertEqual(history.status_code, 200)
        self.assertEqual(len(history.context["history_items"]), 3)
        self.assertContains(history, "Recuperada")
        self.assertNotContains(history, "EventoAuditoria")

    def test_dashboard_uses_canonical_aggregate(self):
        online = self.camera(1, status="OFFLINE")
        offline = self.camera(2, status="ONLINE")
        stale = self.camera(3, status="ONLINE")
        out = self.camera(4, status="ONLINE", situacao_operacional=Camera.SituacaoOperacional.ESTOQUE)
        self.state(online, "ONLINE", self.now)
        self.state(offline, "OFFLINE", self.now)
        self.state(stale, "ONLINE", self.now - timedelta(days=1))
        self.state(out, "ONLINE", self.now)
        response = self.client.get(reverse("core:dashboard"))
        aggregate = response.context["monitoring"]
        self.assertEqual((aggregate.online, aggregate.offline, aggregate.unknown, aggregate.out_of_scope), (1, 1, 1, 1))

    def test_view_permission_covers_history_without_pk_bypass(self):
        camera = self.camera()
        other = get_user_model().objects.create_user("without-view", password="senha")
        self.client.force_login(other)
        self.assertEqual(self.client.get(reverse("cameras:historico_monitoramento", args=[camera.pk])).status_code, 403)

    def test_inventory_monitoring_queries_do_not_grow_per_camera(self):
        self.state(self.camera())
        with CaptureQueriesContext(connection) as one_camera:
            self.client.get(reverse("cameras:lista"))
        for number in range(2, 21):
            self.state(self.camera(number))
        with CaptureQueriesContext(connection) as twenty_cameras:
            self.client.get(reverse("cameras:lista"))
        self.assertEqual(len(one_camera), len(twenty_cameras))

    def test_detail_and_history_queries_are_constant_for_preview_and_page(self):
        camera = self.camera()
        self.state(camera, "OFFLINE")
        self.outage(camera, self.now - timedelta(hours=2))
        with CaptureQueriesContext(connection) as detail_one:
            self.client.get(reverse("cameras:detalhe", args=[camera.pk]))
        with CaptureQueriesContext(connection) as history_one:
            self.client.get(reverse("cameras:historico_monitoramento", args=[camera.pk]))
        for index in range(1, 24):
            self.outage(camera, self.now - timedelta(days=index + 2), self.now - timedelta(days=index + 1))
        with CaptureQueriesContext(connection) as detail_many:
            self.client.get(reverse("cameras:detalhe", args=[camera.pk]))
        with CaptureQueriesContext(connection) as history_many:
            self.client.get(reverse("cameras:historico_monitoramento", args=[camera.pk]))
        self.assertEqual(len(detail_one), len(detail_many))
        self.assertEqual(len(history_one), len(history_many))
