from datetime import datetime, timedelta, timezone
from uuid import uuid4

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import TestCase

from cameras.models import (
    Camera,
    CameraHealthSnapshot,
    EstadoMonitoramento,
    Indisponibilidade,
    TransicaoEstadoMonitoramento,
)
from cameras.monitoramento.read_service import MonitoringReadService
from cameras.monitoramento.schemas import MonitoringConfig


NOW = datetime(2026, 10, 10, 12, tzinfo=timezone.utc)


class CameraHealthProjectionTests(TestCase):
    def setUp(self):
        self.service = MonitoringReadService(
            config=MonitoringConfig(cycle_interval_seconds=30, stale_after_seconds=60),
            now=lambda: NOW,
        )
        self.camera = self.make_camera(1)

    def make_camera(self, suffix):
        return Camera.objects.create(
            nome=f"Health {suffix}", fabricante="Vendor", modelo="Model", serial=f"SER-{suffix}",
            mac=f"00:11:22:33:44:{suffix:02X}", tipo=Camera.TipoCamera.BULLET,
            terminal="T", pavimento="P", setor="S", ambiente="A", ip=f"10.0.0.{suffix + 1}",
            mascara_subrede="255.255.255.0", gateway="10.0.0.1", vlan=10, farm="F",
            retencao_esperada_dias=1, codec="H264", status=Camera.StatusCamera.ONLINE,
            status_em=NOW, ultima_verificacao=NOW,
        )

    def save_snapshot(self, camera=None, *, observed_at=NOW - timedelta(seconds=1), states=None, errors=None):
        camera = camera or self.camera
        states = states or ("PASS", "PASS", "PASS", "PASS")
        errors = errors or ("", "", "", "")
        values = {
            "camera": camera,
            "observed_at": observed_at,
            "config_generation": 1,
            "reached_stage": "D" if states[-1] != "NOT_RUN" else "C",
            "correlation_id": uuid4(),
        }
        for stage, state, error in zip("abcd", states, errors):
            values.update({
                f"stage_{stage}_state": state,
                f"stage_{stage}_observed_at": observed_at,
                f"stage_{stage}_duration_seconds": 0.25,
                f"stage_{stage}_error_code": error,
            })
        return CameraHealthSnapshot.objects.create(**values)

    def test_absent_snapshot_is_unknown_without_mutating_monitoring(self):
        state = EstadoMonitoramento.objects.create(
            camera=self.camera, estado_estavel="ONLINE", estado_alterado_em=NOW,
            ultima_evidencia_util_em=NOW, em_escopo=True,
        )
        before = (state.estado_estavel, state.ultima_evidencia_util_em,
                  TransicaoEstadoMonitoramento.objects.count(), Indisponibilidade.objects.count())
        projection = self.service.camera_health(self.camera, include_details=True)
        self.assertEqual((projection.evidence_state, projection.freshness), ("UNKNOWN", "UNKNOWN"))
        self.assertIsNone(projection.stages)
        state.refresh_from_db()
        after = (state.estado_estavel, state.ultima_evidencia_util_em,
                 TransicaoEstadoMonitoramento.objects.count(), Indisponibilidade.objects.count())
        self.assertEqual(before, after)

    def test_fresh_at_limit_and_beyond_limit_use_mon_threshold(self):
        cases = (
            (NOW - timedelta(seconds=59), "FRESH", "CURRENT"),
            (NOW - timedelta(seconds=60), "STALE", "UNKNOWN"),
            (NOW - timedelta(seconds=61), "STALE", "UNKNOWN"),
        )
        for index, (observed_at, freshness, evidence_state) in enumerate(cases, start=1):
            with self.subTest(freshness=freshness, observed_at=observed_at):
                camera = self.make_camera(index + 1)
                self.save_snapshot(camera, observed_at=observed_at)
                projection = self.service.camera_health(camera)
                self.assertEqual((projection.freshness, projection.evidence_state), (freshness, evidence_state))

    def test_future_and_invalid_timestamps_never_count_as_current(self):
        future_camera = self.make_camera(10)
        future = self.save_snapshot(future_camera, observed_at=NOW + timedelta(seconds=1))
        future_projection = self.service.camera_health(future_camera)
        self.assertEqual((future_projection.freshness, future_projection.evidence_state), ("UNKNOWN", "UNKNOWN"))

        invalid_camera = self.make_camera(11)
        invalid = self.save_snapshot(invalid_camera)
        invalid.observed_at = "not-a-timestamp"
        invalid_projection = self.service.camera_health(invalid_camera, snapshot=invalid)
        self.assertEqual((invalid_projection.freshness, invalid_projection.evidence_state), ("UNKNOWN", "UNKNOWN"))
        self.assertIsNone(invalid_projection.evidence_at)

    def test_stages_are_faithful_for_complete_incomplete_and_inconclusive_sequences(self):
        cases = (
            (("PASS",) * 4, ("PASS",) * 4),
            (("PASS", "PASS", "PASS", "NOT_RUN"), ("PASS", "PASS", "PASS", "NOT_RUN")),
            (("PASS", "FAIL", "NOT_RUN", "NOT_RUN"), ("PASS", "FAIL", "NOT_RUN", "NOT_RUN")),
        )
        for index, (states, expected) in enumerate(cases, start=1):
            with self.subTest(states=states):
                camera = self.make_camera(index + 20)
                self.save_snapshot(camera, states=states)
                projection = self.service.camera_health(camera, include_details=True)
                self.assertEqual(tuple(stage.state for stage in projection.stages), expected)

    def test_only_allowlisted_details_are_projected_and_monitoring_state_stays_separate(self):
        state = EstadoMonitoramento.objects.create(
            camera=self.camera, estado_estavel="OFFLINE", estado_alterado_em=NOW,
            ultima_evidencia_util_em=NOW, em_escopo=True,
        )
        snapshot = self.save_snapshot(errors=("", "", "", "TIMEOUT"))
        before = (state.estado_estavel, TransicaoEstadoMonitoramento.objects.count(),
                  Indisponibilidade.objects.count(), snapshot.updated_at)
        projection = self.service.camera_health(self.camera, include_details=True)
        fields = set(projection.__dataclass_fields__)
        self.assertEqual(fields, {"camera_id", "evidence_at", "freshness", "evidence_state", "stages"})
        self.assertEqual(projection.stages[3].error_code, "TIMEOUT")
        self.assertNotIn("correlation_id", repr(projection))
        state.refresh_from_db()
        snapshot.refresh_from_db()
        self.assertEqual(before, (state.estado_estavel, TransicaoEstadoMonitoramento.objects.count(),
                                  Indisponibilidade.objects.count(), snapshot.updated_at))


class CameraHealthAuthorizationViewTests(CameraHealthProjectionTests):
    def setUp(self):
        super().setUp()
        self.user = get_user_model().objects.create_user(username="camera-viewer", password="test-password")
        self.user.user_permissions.add(Permission.objects.get(codename="view_camera"))
        self.client.force_login(self.user)

    def test_view_camera_receives_summary_but_not_diagnostic_details(self):
        self.save_snapshot(errors=("", "", "", "TIMEOUT"))
        response = self.client.get(f"/cameras/{self.camera.pk}/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Evidência automática")
        self.assertNotContains(response, "Resultados dos estágios do diagnóstico")
        self.assertNotContains(response, "TIMEOUT")
        self.assertNotContains(response, "TIMEOUT")

    def test_diagnostic_permission_adds_stages_and_snapshot_is_camera_scoped(self):
        other = self.make_camera(99)
        self.save_snapshot(self.camera, states=("PASS", "FAIL", "NOT_RUN", "NOT_RUN"))
        self.save_snapshot(other, states=("PASS", "PASS", "PASS", "PASS"))
        self.user.user_permissions.add(Permission.objects.get(codename="view_camera_diagnostic"))
        response = self.client.get(f"/cameras/{self.camera.pk}/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Resultados dos estágios do diagnóstico")
        self.assertContains(response, "FAIL")
        self.assertNotContains(response, "Health 99")
        self.assertNotContains(response, "rtsp://")
        self.assertNotContains(response, "correlation_id")

    def test_camera_summary_permission_is_required(self):
        user = get_user_model().objects.create_user(username="no-camera-access", password="test-password")
        self.client.force_login(user)
        response = self.client.get(f"/cameras/{self.camera.pk}/")
        self.assertEqual(response.status_code, 403)
        self.assertNotContains(response, "Evidência automática", status_code=403)
