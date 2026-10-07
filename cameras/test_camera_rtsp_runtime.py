from datetime import datetime, timezone
import inspect
import os
import socket
from unittest import TestCase
from unittest.mock import Mock, patch

from cameras.integracao.rtsp import service
from cameras.integracao.rtsp.runtime import run_camera_connection_test_from_environment
from cameras.integracao.rtsp.ports import RtspStage, StageStatus
from cameras.monitoramento.contracts import ProbeResultCode


def environment(**overrides):
    values = {
        "ARGOS_CAMERA_ALLOWED_CIDRS": "10.42.0.0/24",
        "ARGOS_CAMERA_ALLOWED_PORTS": "rtsp:554",
        "ARGOS_CAMERA_ALLOWED_PATHS": "rtsp:/stream-a",
    }
    values.update(overrides)
    return values


class RtspRuntimeCompositionTests(TestCase):
    def setUp(self):
        self.actor = object()
        self.camera_id = 23
        self.result = object()
        self.adapter = object()
        self.monotonic = Mock(return_value=12.5)
        self.now = Mock(return_value=datetime(2026, 10, 7, tzinfo=timezone.utc))

    def test_explicit_trusted_mapping_builds_and_injects_complete_policy(self):
        source = environment(
            **{
                "ARGOS_CAMERA_DENIED_CIDRS": "10.42.0.128/25",
                "ARGOS_CAMERA_ALLOWED_FARMS": "FARM-A",
                "ARGOS_CAMERA_ALLOWED_PORTS": "rtsp:554,8554;http:80",
                "ARGOS_CAMERA_ALLOWED_PATHS": "rtsp:/stream-a,/stream-b;http:/image.jpg",
            }
        )
        with patch("cameras.integracao.rtsp.runtime.run_camera_connection_test", return_value=self.result) as run:
            returned = run_camera_connection_test_from_environment(
                actor=self.actor,
                camera_id=self.camera_id,
                environ=source,
                adapter=self.adapter,
                timeout_seconds=8.0,
                connect_timeout_seconds=2.5,
                monotonic=self.monotonic,
                now=self.now,
            )

        self.assertIs(returned, self.result)
        run.assert_called_once()
        kwargs = run.call_args.kwargs
        self.assertIs(kwargs["actor"], self.actor)
        self.assertEqual(kwargs["camera_id"], self.camera_id)
        self.assertIs(kwargs["adapter"], self.adapter)
        self.assertEqual(kwargs["timeout_seconds"], 8.0)
        self.assertEqual(kwargs["connect_timeout_seconds"], 2.5)
        self.assertIs(kwargs["monotonic"], self.monotonic)
        self.assertIs(kwargs["now"], self.now)
        policy = kwargs["target_policy"]
        self.assertEqual(tuple(str(cidr) for cidr in policy.allowed_cidrs), ("10.42.0.0/24",))
        self.assertEqual(tuple(str(cidr) for cidr in policy.denied_cidrs), ("10.42.0.128/25",))
        self.assertEqual(policy.ports_by_scheme["rtsp"], (554, 8554))
        self.assertEqual(policy.ports_by_scheme["http"], (80,))
        self.assertEqual(policy.allowed_paths_by_scheme["rtsp"], ("/stream-a", "/stream-b"))
        self.assertEqual(policy.allowed_paths_by_scheme["http"], ("/image.jpg",))
        self.assertEqual(policy.allowed_farms, frozenset({"FARM-A"}))
        self.assertIs(kwargs["environment_allowed_ports"], policy.ports_by_scheme["rtsp"])

    def test_none_environment_reads_process_environment_at_composition_boundary(self):
        with patch.dict(os.environ, environment(), clear=True):
            with patch("cameras.integracao.rtsp.runtime.run_camera_connection_test", return_value=self.result) as run:
                returned = run_camera_connection_test_from_environment(
                    actor=self.actor,
                    camera_id=self.camera_id,
                    adapter=self.adapter,
                )
        self.assertIs(returned, self.result)
        self.assertEqual(run.call_args.kwargs["target_policy"].allowed_paths_by_scheme["rtsp"], ("/stream-a",))

    def test_policy_is_rebuilt_each_invocation_and_observes_mapping_changes(self):
        source = environment()
        with patch("cameras.integracao.rtsp.runtime.run_camera_connection_test", return_value=self.result) as run:
            run_camera_connection_test_from_environment(actor=self.actor, camera_id=self.camera_id, environ=source)
            source["ARGOS_CAMERA_ALLOWED_PORTS"] = "rtsp:8554"
            source["ARGOS_CAMERA_ALLOWED_PATHS"] = "rtsp:/stream-b"
            run_camera_connection_test_from_environment(actor=self.actor, camera_id=self.camera_id, environ=source)

        first_policy = run.call_args_list[0].kwargs["target_policy"]
        second_policy = run.call_args_list[1].kwargs["target_policy"]
        self.assertIsNot(first_policy, second_policy)
        self.assertEqual(run.call_args_list[0].kwargs["environment_allowed_ports"], (554,))
        self.assertEqual(run.call_args_list[1].kwargs["environment_allowed_ports"], (8554,))
        self.assertEqual(second_policy.allowed_paths_by_scheme["rtsp"], ("/stream-b",))

    def test_invalid_bootstrap_fails_before_service_credentials_adapter_or_socket(self):
        http_only = environment(
            **{
                "ARGOS_CAMERA_ALLOWED_PORTS": "http:80",
                "ARGOS_CAMERA_ALLOWED_PATHS": "http:/image.jpg",
            }
        )
        missing_paths = environment()
        missing_paths.pop("ARGOS_CAMERA_ALLOWED_PATHS")
        missing_cidr = environment()
        missing_cidr.pop("ARGOS_CAMERA_ALLOWED_CIDRS")
        missing_ports = environment()
        missing_ports.pop("ARGOS_CAMERA_ALLOWED_PORTS")
        invalid_sources = (
            missing_cidr,
            missing_ports,
            environment(**{"ARGOS_CAMERA_ALLOWED_PORTS": "http:80", "ARGOS_CAMERA_ALLOWED_PATHS": "http:/image.jpg"}),
            missing_paths,
            environment(**{"ARGOS_CAMERA_ALLOWED_PATHS": "rtsp:/stream-a,"}),
            http_only,
        )
        adapter = Mock()
        with (
            patch("cameras.integracao.rtsp.runtime.run_camera_connection_test") as run,
            patch("cameras.integracao.rtsp.service.resolve_active_credential_for_execution") as resolve_credential,
            patch("cameras.integracao.rtsp.gst_adapter.socket.socket", wraps=socket.socket) as open_socket,
        ):
            for source in invalid_sources:
                with self.subTest(source=source):
                    self.now.return_value = datetime(2026, 10, 7, 12, 0)
                    result = run_camera_connection_test_from_environment(
                        actor=self.actor,
                        camera_id=self.camera_id,
                        environ=source,
                        adapter=adapter,
                        now=self.now,
                    )
                    self.assertEqual(result.error_code, "MISCONFIGURED_POLICY")
                    self.assertEqual(result.category, ProbeResultCode.TARGET_BLOCKED)
                    self.assertEqual(tuple(stage.status for stage in result.stages), (StageStatus.NOT_RUN,) * 4)
                    self.assertEqual(tuple(stage.stage for stage in result.stages), tuple(RtspStage))
                    self.assertEqual(result.duration_seconds, 0)
                    self.assertEqual(result.observed_at.utcoffset().total_seconds(), 0)
        run.assert_not_called()
        resolve_credential.assert_not_called()
        adapter.probe.assert_not_called()
        open_socket.assert_not_called()

    def test_service_remains_environment_independent_and_requires_injected_policy(self):
        parameters = inspect.signature(service.run_camera_connection_test).parameters
        self.assertIn("target_policy", parameters)
        self.assertIs(parameters["target_policy"].default, inspect.Parameter.empty)
        self.assertIn("environment_allowed_ports", parameters)
        self.assertIs(parameters["environment_allowed_ports"].default, inspect.Parameter.empty)
        self.assertNotIn("environ", parameters)
        self.assertFalse(hasattr(service, "os"))
