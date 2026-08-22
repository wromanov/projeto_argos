"""Testes do boundary canônico de leitura MON-07B."""

from datetime import datetime, timedelta, timezone
from inspect import getsource

from django.db import connection
from django.test import TestCase
from django.test.utils import CaptureQueriesContext

from cameras.models import (
    Camera,
    EstadoMonitoramento,
    EventoAuditoria,
    Indisponibilidade,
    TransicaoEstadoMonitoramento,
)
from cameras.monitoramento.read_service import (
    MonitoringEffectiveState,
    MonitoringFreshness,
    MonitoringReadService,
    MonitoringScopeReason,
)
from cameras.monitoramento.schemas import MonitoringConfig


NOW = datetime(2026, 1, 1, 12, tzinfo=timezone.utc)


class MonitoringReadServiceTests(TestCase):
    def setUp(self):
        self.service = MonitoringReadService(
            config=MonitoringConfig(cycle_interval_seconds=30, stale_after_seconds=60),
            now=lambda: NOW,
        )

    def camera(self, suffix=1, **overrides):
        values = {
            "nome": f"CAM-{suffix}",
            "fabricante": "FAB",
            "modelo": "MOD",
            "serial": f"SER-{suffix}",
            "mac": f"00:11:22:33:44:{suffix:02X}",
            "tipo": Camera.TipoCamera.BULLET,
            "terminal": "T",
            "pavimento": "P",
            "setor": "S",
            "ambiente": "A",
            "ip": f"10.0.0.{suffix + 1}",
            "mascara_subrede": "255.255.255.0",
            "gateway": "10.0.0.1",
            "vlan": 10,
            "farm": "F",
            "retencao_esperada_dias": 1,
            "codec": "H264",
            "status": Camera.StatusCamera.ONLINE,
            "status_em": NOW - timedelta(days=1),
            "ultima_verificacao": NOW - timedelta(days=1),
        }
        values.update(overrides)
        return Camera.objects.create(**values)

    def state(self, camera, stable="UNKNOWN", **overrides):
        values = {
            "estado_estavel": stable,
            "estado_alterado_em": NOW - timedelta(minutes=2),
            "ultima_evidencia_util_em": NOW - timedelta(seconds=10),
            "em_escopo": True,
        }
        values.update(overrides)
        return EstadoMonitoramento.objects.create(camera=camera, **values)

    def outage(self, camera, opened_at, *, closed_at=None, origin="INITIAL_OFFLINE", reason=None):
        transition = TransicaoEstadoMonitoramento.objects.create(
            camera=camera,
            estado_anterior="UNKNOWN",
            estado_atual="OFFLINE",
            ocorrida_em=opened_at,
        )
        closing_transition = None
        if closed_at is not None and reason == "RECUPERADA":
            closing_transition = TransicaoEstadoMonitoramento.objects.create(
                camera=camera,
                estado_anterior="OFFLINE",
                estado_atual="ONLINE",
                ocorrida_em=closed_at,
            )
        return Indisponibilidade.objects.create(
            camera=camera,
            opened_at=opened_at,
            closed_at=closed_at,
            open_origin=origin,
            close_reason=reason,
            opening_transition=transition,
            closing_transition=closing_transition,
        )

    def test_projection_uses_canonical_state_and_ignores_legacy_fields(self):
        camera = self.camera(status=Camera.StatusCamera.ONLINE)
        self.state(camera, "OFFLINE")

        projection = self.service.current(camera.pk)

        self.assertEqual(projection.stable_state, "OFFLINE")
        self.assertEqual(projection.effective_state, MonitoringEffectiveState.OFFLINE)
        self.assertNotEqual(projection.effective_state, MonitoringEffectiveState.ONLINE)

        Camera.objects.filter(pk=camera.pk).update(status=Camera.StatusCamera.OFFLINE)
        self.assertEqual(self.service.current(camera.pk).stable_state, "OFFLINE")

    def test_projection_preserves_stable_state_and_maps_stale_to_unknown(self):
        for suffix, stable in enumerate(("ONLINE", "OFFLINE", "UNKNOWN"), start=1):
            with self.subTest(stable=stable):
                camera = self.camera(suffix)
                self.state(camera, stable)
                projection = self.service.current(camera.pk)
                self.assertEqual(projection.effective_state.value, stable)
                self.assertEqual(projection.freshness, MonitoringFreshness.FRESH)

        stale_camera = self.camera(10)
        self.state(stale_camera, "ONLINE", ultima_evidencia_util_em=NOW - timedelta(seconds=60))
        projection = self.service.current(stale_camera.pk)
        self.assertEqual(projection.stable_state, "ONLINE")
        self.assertEqual(projection.effective_state, MonitoringEffectiveState.UNKNOWN)
        self.assertEqual(projection.freshness, MonitoringFreshness.STALE)
        self.assertTrue(projection.is_stale)
        self.assertEqual(EstadoMonitoramento.objects.get(camera=stale_camera).estado_estavel, "ONLINE")

        for suffix, stable in ((11, "OFFLINE"), (12, "UNKNOWN")):
            with self.subTest(stable=stable, freshness="stale"):
                camera = self.camera(suffix)
                self.state(
                    camera,
                    stable,
                    ultima_evidencia_util_em=NOW - timedelta(seconds=60),
                )
                projection = self.service.current(camera.pk)
                self.assertEqual(projection.stable_state, stable)
                self.assertEqual(projection.effective_state, MonitoringEffectiveState.UNKNOWN)
                self.assertEqual(projection.freshness, MonitoringFreshness.STALE)

    def test_stale_open_outage_is_projected_without_mutation(self):
        camera = self.camera()
        self.state(
            camera,
            "OFFLINE",
            ultima_evidencia_util_em=NOW - timedelta(seconds=60),
        )
        outage = self.outage(camera, NOW - timedelta(minutes=5))

        projection = self.service.current(camera.pk)

        self.assertEqual(projection.stable_state, "OFFLINE")
        self.assertEqual(projection.effective_state, MonitoringEffectiveState.UNKNOWN)
        self.assertEqual(projection.freshness, MonitoringFreshness.STALE)
        self.assertEqual(projection.open_outage.id, outage.pk)
        self.assertIsNone(Indisponibilidade.objects.get(pk=outage.pk).closed_at)

    def test_missing_state_is_unknown_and_incomplete_or_out_scope_is_not_offline(self):
        missing_state = self.camera(1)
        projection = self.service.current(missing_state.pk)
        self.assertEqual(projection.effective_state, MonitoringEffectiveState.UNKNOWN)
        self.assertTrue(projection.em_escopo)
        self.assertIsNone(projection.open_outage)

        incomplete = self.camera(2, ip=None)
        self.state(incomplete, "OFFLINE")
        projection = self.service.current(incomplete.pk)
        self.assertEqual(projection.effective_state, MonitoringEffectiveState.OUT_OF_SCOPE)
        self.assertFalse(projection.em_escopo)
        self.assertEqual(projection.scope_reason, MonitoringScopeReason.INCOMPLETE_CONFIGURATION)

        out_scope = self.camera(3)
        self.state(
            out_scope,
            "OFFLINE",
            em_escopo=False,
            ultima_evidencia_util_em=NOW - timedelta(seconds=60),
        )
        projection = self.service.current(out_scope.pk)
        self.assertEqual(projection.effective_state, MonitoringEffectiveState.OUT_OF_SCOPE)
        self.assertEqual(projection.freshness, MonitoringFreshness.STALE)
        self.assertEqual(projection.scope_reason, MonitoringScopeReason.OUT_OF_SCOPE)

    def test_open_outage_is_allowlisted_and_history_is_limited_ordered_and_derivable(self):
        camera = self.camera()
        self.state(camera, "OFFLINE")
        older = self.outage(camera, NOW - timedelta(hours=3), closed_at=NOW - timedelta(hours=2), reason="RECUPERADA")
        current = self.outage(camera, NOW - timedelta(hours=1), origin="ONLINE_TO_OFFLINE")

        projection = self.service.current(camera.pk)
        self.assertEqual(projection.open_outage.id, current.pk)
        self.assertEqual(projection.open_outage.opened_at, current.opened_at)
        self.assertEqual(projection.open_outage.open_origin, "ONLINE_TO_OFFLINE")

        page = self.service.history_page(camera.pk, limit=1)
        self.assertEqual(page.total, 2)
        self.assertEqual([item.id for item in page.items], [current.pk])
        self.assertIsNone(page.items[0].duration)
        self.assertEqual(page.items[0].close_reason, None)

        second_page = self.service.history_page(camera.pk, limit=1, offset=1)
        self.assertEqual(second_page.items[0].id, older.pk)
        self.assertEqual(second_page.items[0].duration, timedelta(hours=1))
        self.assertEqual(second_page.items[0].close_reason, "RECUPERADA")
        self.assertNotIn("transition", second_page.items[0].__slots__ if hasattr(second_page.items[0], "__slots__") else ())

    def test_closed_scope_interval_does_not_appear_as_open(self):
        camera = self.camera()
        self.state(camera, "UNKNOWN", em_escopo=False)
        interval = self.outage(
            camera,
            NOW - timedelta(hours=2),
            closed_at=NOW - timedelta(hours=1),
            reason="SAIU_DO_ESCOPO",
        )
        projection = self.service.current(camera.pk)
        self.assertIsNone(projection.open_outage)
        self.assertEqual(self.service.history_page(camera.pk).items[0].id, interval.pk)

    def test_restart_rebuilds_same_projection_from_database(self):
        camera = self.camera()
        self.state(camera, "ONLINE")
        first = self.service.current(camera.pk)
        restarted = MonitoringReadService(
            config=self.service.config,
            now=lambda: NOW,
        ).current(camera.pk)
        self.assertEqual(first, restarted)

    def test_aggregation_is_canonical_and_done_in_database(self):
        online = self.camera(1)
        self.state(online, "ONLINE")
        online_stale = self.camera(2)
        self.state(online_stale, "ONLINE", ultima_evidencia_util_em=NOW - timedelta(seconds=60))
        offline_fresh = self.camera(3)
        self.state(offline_fresh, "OFFLINE")
        offline_stale = self.camera(4)
        self.state(offline_stale, "OFFLINE", ultima_evidencia_util_em=NOW - timedelta(seconds=60))
        self.outage(offline_stale, NOW - timedelta(minutes=5))
        unknown = self.camera(5)
        self.state(unknown, "UNKNOWN")
        out_scope = self.camera(6)
        self.state(out_scope, "OFFLINE", em_escopo=False)
        incomplete = self.camera(7, ip=None)
        self.state(incomplete, "OFFLINE")

        with CaptureQueriesContext(connection) as queries:
            aggregate = self.service.aggregate()

        self.assertEqual(aggregate.total, 7)
        self.assertEqual(aggregate.in_scope, 5)
        self.assertEqual(aggregate.out_of_scope, 2)
        self.assertEqual(aggregate.online, 1)
        self.assertEqual(aggregate.offline, 1)
        self.assertEqual(aggregate.unknown, 3)
        self.assertEqual(aggregate.stale, 2)
        self.assertEqual(aggregate.fresh, 3)
        self.assertEqual(aggregate.open_outages, 1)
        self.assertEqual(len(queries), 1)

    def test_camera_read_path_has_constant_query_count_for_one_twenty_and_scale(self):
        cameras = [self.camera(index) for index in range(1, 101)]

        def read_count(size):
            with CaptureQueriesContext(connection) as queries:
                rows = list(
                    self.service.camera_queryset(
                        Camera.objects.filter(pk__in=[camera.pk for camera in cameras[:size]]).order_by("pk")
                    )
                )
                tuple(self.service.project(camera) for camera in rows)
            return len(queries)

        one = read_count(1)
        twenty = read_count(20)
        hundred = read_count(100)
        self.assertEqual((one, twenty, hundred), (1, 1, 1))
        self.assertEqual(one, twenty)
        self.assertEqual(twenty, hundred)

    def test_projection_allowlist_does_not_include_audit_or_probe_fields(self):
        camera = self.camera()
        projection = self.service.current(camera.pk)
        allowed = set(projection.__dataclass_fields__)
        self.assertEqual(
            allowed,
            {
                "camera_id", "stable_state", "freshness", "em_escopo",
                "effective_state", "evidence_at", "state_since",
                "scope_reason", "open_outage",
            },
        )
        source = getsource(MonitoringReadService)
        self.assertNotIn("EventoAuditoria", source)
        self.assertNotIn("ProbeRequest", source)
        self.assertNotIn("password", source.lower())
        self.assertEqual(EventoAuditoria.objects.count(), 0)
