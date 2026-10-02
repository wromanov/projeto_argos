from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from unittest.mock import patch

from cameras.integracao.configuration import save_connection_config, resolve_connection_config
from cameras.models import Camera, CameraCapabilityProfile, CameraConnectionConfig, EstadoMonitoramento, EventoAuditoria
from cameras.monitoramento.repository import DjangoMonitoringRepository


class CameraConnectionConfigurationTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="tech", password="test")
        permission = self.user.user_permissions.model.objects.get(codename="change_camera_connection")
        self.user.user_permissions.add(permission)
        self.camera = Camera.objects.create(nome="Camera A", fabricante="Livre", modelo="Modelo Livre", ip="192.0.2.10")
        self.profile = CameraCapabilityProfile.objects.get(profile_key="RTSP_DISCOVERY_V1", version=1)
        self.policy_ports = {554}

    def test_config_change_increments_versions_generation_and_audits_sanitized_fields(self):
        config = save_connection_config(
            actor=self.user, camera_id=self.camera.pk,
            values={"profile": self.profile, "rtsp_uri": "rtsp://192.0.2.10/path", "enabled": True},
            environment_allowed_ports=self.policy_ports,
        )
        state = EstadoMonitoramento.objects.get(camera=self.camera)
        self.assertEqual(config.config_version, 1)
        self.assertEqual(state.ultima_geracao_configuracao, 2)
        first_generation = DjangoMonitoringRepository().current_generation(self.camera.pk)
        config = save_connection_config(
            actor=self.user, camera_id=self.camera.pk,
            values={"rtsp_uri": "rtsp://192.0.2.10/other"},
            environment_allowed_ports=self.policy_ports,
        )
        state.refresh_from_db()
        self.assertEqual(config.config_version, 2)
        self.assertEqual(state.ultima_geracao_configuracao, first_generation + 1)
        self.assertEqual(EventoAuditoria.objects.filter(camera=self.camera, codigo="camera.connection.created").count(), 1)
        self.assertEqual(EventoAuditoria.objects.filter(camera=self.camera, codigo="camera.connection.updated").count(), 1)
        for event in EventoAuditoria.objects.filter(camera=self.camera):
            self.assertNotIn("rtsp://", str(event.alteracoes))
            self.assertNotIn("/other", str(event.alteracoes))

    def test_noop_does_not_increment_generation_or_version(self):
        config = save_connection_config(
            actor=self.user, camera_id=self.camera.pk,
            values={"profile": self.profile, "rtsp_uri": "rtsp://192.0.2.10/path"},
            environment_allowed_ports=self.policy_ports,
        )
        version = config.config_version
        generation = EstadoMonitoramento.objects.get(camera=self.camera).ultima_geracao_configuracao
        save_connection_config(
            actor=self.user, camera_id=self.camera.pk,
            values={"profile": self.profile, "rtsp_uri": "rtsp://192.0.2.10/path"},
            environment_allowed_ports=self.policy_ports,
        )
        self.assertEqual(CameraConnectionConfig.objects.get(camera=self.camera).config_version, version)
        self.assertEqual(EstadoMonitoramento.objects.get(camera=self.camera).ultima_geracao_configuracao, generation)
        self.assertEqual(EventoAuditoria.objects.filter(camera=self.camera).count(), 1)

    def test_rejects_credentials_query_fragments_hosts_schemes_and_unapproved_ports(self):
        invalid_uris = [
            "rtsp://user:password@192.0.2.10/path",
            "rtsp://192.0.2.10/path?token=x",
            "rtsp://192.0.2.10/path#fragment",
            "rtsp://192.0.2.11/path",
            "rtsp://camera.example/path",
            "https://192.0.2.10/path",
            "rtsp://192.0.2.10:8554/path",
        ]
        for uri in invalid_uris:
            with self.subTest(uri=uri), self.assertRaises(ValidationError):
                save_connection_config(
                    actor=self.user, camera_id=self.camera.pk,
                    values={"profile": self.profile, "rtsp_uri": uri},
                    environment_allowed_ports=self.policy_ports,
                )
        self.assertFalse(CameraConnectionConfig.objects.filter(camera=self.camera).exists())
        self.assertFalse(EstadoMonitoramento.objects.filter(camera=self.camera).exists())
        self.assertFalse(EventoAuditoria.objects.filter(camera=self.camera).exists())

    def test_resolver_blocks_unverified_automatic_execution(self):
        save_connection_config(
            actor=self.user, camera_id=self.camera.pk,
            values={"profile": self.profile, "rtsp_uri": "rtsp://192.0.2.10/path", "enabled": True},
            environment_allowed_ports=self.policy_ports,
        )
        result = resolve_connection_config(camera_id=self.camera.pk, environment_allowed_ports=self.policy_ports)
        self.assertEqual(result["compatibility"], "UNVERIFIED")
        with self.assertRaises(ValidationError):
            resolve_connection_config(camera_id=self.camera.pk, environment_allowed_ports=self.policy_ports, automatic=True)

    def test_resolves_default_rtsp_host_and_port(self):
        save_connection_config(
            actor=self.user, camera_id=self.camera.pk,
            values={"profile": self.profile, "enabled": True},
            environment_allowed_ports=self.policy_ports,
        )
        resolved = resolve_connection_config(camera_id=self.camera.pk, environment_allowed_ports=self.policy_ports)
        self.assertEqual(resolved["rtsp_uri"], "rtsp://192.0.2.10:554")


    def test_audit_failure_rolls_back_config_and_generation(self):
        with patch("cameras.auditoria.registrar_evento", side_effect=RuntimeError("audit unavailable")):
            with self.assertRaises(RuntimeError):
                save_connection_config(
                    actor=self.user, camera_id=self.camera.pk,
                    values={"profile": self.profile, "rtsp_uri": "rtsp://192.0.2.10/path"},
                    environment_allowed_ports=self.policy_ports,
                )
        self.assertFalse(CameraConnectionConfig.objects.filter(camera=self.camera).exists())
        self.assertFalse(EstadoMonitoramento.objects.filter(camera=self.camera).exists())
        self.assertFalse(EventoAuditoria.objects.filter(camera=self.camera).exists())
