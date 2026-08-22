"""Integração server-rendered do boundary MON-07B (MON-07C)."""

from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db import connection
from django.test import TestCase
from django.test.utils import CaptureQueriesContext
from django.urls import reverse
from django.utils import timezone

from cameras.models import Camera, EstadoMonitoramento, Indisponibilidade, TransicaoEstadoMonitoramento


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
        self.assertContains(detail, "OFFLINE")
        self.assertNotContains(detail, "Última verificação")

    def test_stale_and_out_of_scope_are_not_rendered_as_current_offline(self):
        stale = self.camera(2, status="OFFLINE")
        self.state(stale, stable="OFFLINE", evidence=self.now - timedelta(days=1))
        self.outage(stale, self.now - timedelta(hours=2))
        scoped_out = self.camera(3, status="OFFLINE", situacao_operacional=Camera.SituacaoOperacional.ESTOQUE)
        self.state(scoped_out, stable="OFFLINE", evidence=self.now)
        response = self.client.get(reverse("cameras:lista"))
        self.assertContains(response, "Dados desatualizados")
        self.assertContains(response, "NÃO MONITORADA")
        self.assertNotContains(response, "Offline há")

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
