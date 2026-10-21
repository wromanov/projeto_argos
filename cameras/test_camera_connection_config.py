from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.exceptions import ValidationError
from django.test import RequestFactory, TestCase
from unittest.mock import patch

from cameras.integracao.configuration import (
    invalidate_target_config_generation_if_ip_changed,
    save_connection_config,
    resolve_connection_config,
)
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

    def test_ip_change_invalidates_target_generation_without_changing_config_version(self):
        config = save_connection_config(
            actor=self.user, camera_id=self.camera.pk,
            values={"profile": self.profile, "rtsp_uri": "rtsp://192.0.2.10/path"},
            environment_allowed_ports=self.policy_ports,
        )
        previous_generation = EstadoMonitoramento.objects.get(camera=self.camera).ultima_geracao_configuracao
        previous_version = config.config_version

        invalidate_target_config_generation_if_ip_changed(
            camera_id=self.camera.pk,
            previous_ip="192.0.2.10",
            current_ip="192.0.2.11",
        )
        state = EstadoMonitoramento.objects.get(camera=self.camera)
        config.refresh_from_db()
        self.assertEqual(state.ultima_geracao_configuracao, previous_generation + 1)
        self.assertEqual(config.config_version, previous_version)

        invalidate_target_config_generation_if_ip_changed(
            camera_id=self.camera.pk,
            previous_ip="192.0.2.11",
            current_ip="192.0.2.11",
        )
        state.refresh_from_db()
        self.assertEqual(state.ultima_geracao_configuracao, previous_generation + 1)

    def test_camera_edit_view_invalidates_generation_when_persisted_ip_changes(self):
        self.user.user_permissions.add(Permission.objects.get(codename="change_camera"))
        state = EstadoMonitoramento.objects.create(camera=self.camera, ultima_geracao_configuracao=7)
        request = RequestFactory().post(f"/cameras/{self.camera.pk}/editar/")
        request.user = self.user

        def save_camera(*, commit):
            self.camera.ip = "192.0.2.11"
            return self.camera

        with (
            patch("cameras.views.CameraEdicaoForm") as form_class,
            patch("cameras.views.registrar_evento"),
            patch("cameras.views.messages.success"),
        ):
            form_class.return_value.is_valid.return_value = True
            form_class.return_value.save.side_effect = save_camera
            from cameras.views import editar_camera

            response = editar_camera(request, self.camera.pk)

        self.assertEqual(response.status_code, 302)
        self.camera.refresh_from_db()
        state.refresh_from_db()
        self.assertEqual(self.camera.ip, "192.0.2.11")
        self.assertEqual(state.ultima_geracao_configuracao, 8)

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

    def test_resolver_preserves_explicit_authorized_rtsp_port(self):
        profile = CameraCapabilityProfile.objects.create(
            profile_key="RTSP_EXPLICIT_PORT_TEST", version=1, active=True,
            adapter_key=CameraCapabilityProfile.Adapter.RTSP,
            allowed_schemes=["rtsp"], allowed_ports=[554, 8554],
            tls_policy=CameraCapabilityProfile.TLSPolicy.NOT_APPLICABLE,
            auth_method=CameraCapabilityProfile.AuthMethod.RTSP_NEGOTIATE,
            credential_required=False,
            endpoint_policy=CameraCapabilityProfile.EndpointPolicy.TECHNICIAN_OVERRIDE,
            default_path="/stream", allowed_override_fields=["port"],
            probe_evidence_stage=CameraCapabilityProfile.ProbeStage.D,
            source_ref="test fixture",
        )
        config = save_connection_config(
            actor=self.user, camera_id=self.camera.pk,
            values={
                "profile": profile,
                "rtsp_uri": "rtsp://192.0.2.10:8554/stream",
                "enabled": True,
            },
            environment_allowed_ports={554, 8554},
        )

        resolved = resolve_connection_config(
            camera_id=self.camera.pk, environment_allowed_ports={554, 8554},
        )

        self.assertEqual(config.rtsp_uri, "rtsp://192.0.2.10:8554/stream")
        self.assertEqual(resolved["rtsp_uri"], "rtsp://192.0.2.10:8554/stream")
        with self.assertRaises(ValidationError):
            resolve_connection_config(camera_id=self.camera.pk, environment_allowed_ports={554})


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
