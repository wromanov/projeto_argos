"""Fake-only tests for the RTSP stages and their application boundaries."""
from datetime import datetime, timezone
from ipaddress import IPv4Address
from types import SimpleNamespace
from unittest import TestCase
from unittest.mock import patch
import socket

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.exceptions import PermissionDenied
from django.test import TestCase as DjangoTestCase

from cameras.integracao.credentials import CredentialOperationError, ResolvedCameraCredential
from cameras.integracao.target_policy import AuthorizedTargetRequest, TargetPolicy
from cameras.models import Camera, CameraCapabilityProfile, CameraConnectionConfig, CameraCredential, EstadoMonitoramento
from cameras.monitoramento.contracts import ProbeResultCode
from cameras.integracao.rtsp.fake import FakeRtspAdapter
from cameras.integracao.rtsp.gst_adapter import GStreamerRtspAdapter, GStreamerUnavailable, MAX_FRAME_BYTES, _DEPAYLOADERS
from cameras.integracao.rtsp.ports import RtspConnectionRequest, RtspStage, StageStatus
from cameras.integracao.rtsp.service import run_camera_connection_test


def request(credential=None, transport="AUTO", timeout=5, connect_timeout=3):
    target = AuthorizedTargetRequest(IPv4Address("10.42.0.10"), 554, "rtsp", "/stream1")
    return RtspConnectionRequest(1, target, timeout, connect_timeout, transport, credential)


class _FakeElement:
    def __init__(self, name): self.name, self.props, self.linked = name, {}, False
    def set_property(self, name, value): self.props[name] = value
    def find_property(self, name): return object() if name == "max-bytes" else None
    def link(self, other): return True
    def get_static_pad(self, name): return SimpleNamespace(is_linked=lambda: self.linked)

class _FakePipeline:
    def __init__(self): self.elements = []
    @classmethod
    def new(cls, _name): return cls()
    def add(self, item): self.elements.append(item)

class _FakeFactory:
    @staticmethod
    def make(name, _instance): return _FakeElement(name)

class _FakeCaps:
    @staticmethod
    def from_string(value): return value

class _FakeGst:
    Pipeline = _FakePipeline
    ElementFactory = _FakeFactory
    Caps = _FakeCaps

class _FakeRtsp:
    RTSPLowerTrans = SimpleNamespace(TCP=1, UDP=2)


class _TemporalPad:
    def __init__(self): self.link_calls, self.flow_active = 0, False
    def get_current_caps(self): return self
    def query_caps(self, _value): return self
    def get_size(self): return 1
    def get_structure(self, _index): return self
    def get_string(self, key): return {"media": "video", "encoding-name": "H264"}.get(key)
    def link(self, target):
        self.link_calls += 1
        self.flow_active = target.owner.state == "PLAYING"
        return 0

class _TemporalSinkPad:
    def __init__(self, owner): self.owner, self.linked = owner, False
    def is_linked(self): return self.linked

class _TemporalElement:
    def __init__(self, sync_result=True):
        self.signals, self.props = {}, {}
        self.sync_result, self.state, self.sync_calls = sync_result, "NULL", 0
    def connect(self, signal, callback): self.signals[signal] = callback
    def set_property(self, name, value): self.props[name] = value
    def link(self, _other): return True
    def sync_state_with_parent(self):
        self.sync_calls += 1
        if self.sync_result: self.state = "PLAYING"
        return self.sync_result
    def get_static_pad(self, _name): return _TemporalSinkPad(self)
    def emit(self, _signal): return SimpleNamespace(get_buffer=lambda: SimpleNamespace(get_size=lambda: 1024))

class _TemporalBus:
    def __init__(self, clock): self.clock, self.actions, self.quanta = clock, [], []
    def timed_pop_filtered(self, timeout_ns, _mask):
        self.quanta.append(timeout_ns)
        if len(self.quanta) > 20: raise AssertionError(1)
        action = self.actions.pop(0) if self.actions else None
        if callable(action): action()
        elif action is not None: return action
        else: self.clock[0] += timeout_ns / 1_000_000_000
        return None

class _TemporalPipeline:
    def __init__(self, bus):
        self.bus, self.states = bus, []
        self.current_state, self.pending_state, self.added_dynamic_state = "NULL", None, None
    def add(self, item):
        if self.pending_state == "PLAYING":
            item.state = "NULL"
            self.added_dynamic_state = (self.current_state, self.pending_state, item.state)
    def set_state(self, state):
        self.states.append(state)
        if state == 1:
            self.current_state, self.pending_state = "PAUSED", "PLAYING"
        elif state == 0:
            self.current_state, self.pending_state = "NULL", None
        return 0
    def get_bus(self): return self.bus

def _temporal_gstreamer_adapter(sync_result=True):
    clock = [0.0]
    bus = _TemporalBus(clock)
    pipeline, src, decoder, sink = _TemporalPipeline(bus), _TemporalElement(), _TemporalElement(), _TemporalElement()
    elements = []
    class Factory:
        @staticmethod
        def make(name, _instance):
            element = _TemporalElement(sync_result=sync_result)
            element.name = name
            elements.append(element)
            return element
    gst = SimpleNamespace(
        SECOND=1_000_000_000,
        MessageType=SimpleNamespace(ERROR=1, EOS=2, ELEMENT=4, REDIRECT=8),
        State=SimpleNamespace(PLAYING=1, NULL=0),
        StateChangeReturn=SimpleNamespace(FAILURE=-1),
        FlowReturn=SimpleNamespace(OK=0),
        PadLinkReturn=SimpleNamespace(OK=0),
        ElementFactory=Factory,
    )
    adapter = GStreamerRtspAdapter(socket_factory=lambda *_: _FakeSocket(),
        loader=lambda: (gst, object()), monotonic=lambda: clock[0])
    adapter._pipeline = lambda *_: (pipeline, src, decoder, sink)
    rtp_pad = _TemporalPad()
    def deliver_frame():
        src.signals["on-sdp"](src, None)
        src.signals["pad-added"](src, rtp_pad)
        if rtp_pad.flow_active:
            sink.signals["new-sample"](sink)
    bus.deliver_frame = deliver_frame
    return adapter, bus, clock, pipeline, gst, elements, rtp_pad

class _FakeSocket:
    def settimeout(self, _value): pass
    def connect(self, _address): pass
    def close(self): pass
class RtspPortTests(TestCase):
    def test_fake_passes_all_stages_without_authenticated_uri_or_serializable_request(self):
        secret = ResolvedCameraCredential("camera-user-secret", "camera-password-secret")
        value = request(secret)
        adapter = FakeRtspAdapter()
        result = adapter.probe(value)
        self.assertTrue(result.is_success)
        self.assertEqual(tuple(stage.status for stage in result.stages), (StageStatus.PASS,) * 4)
        self.assertEqual(adapter.last_uri, "rtsp://10.42.0.10:554/stream1")
        self.assertNotIn("camera-user-secret", adapter.last_uri)
        self.assertNotIn("camera-password-secret", repr(value))
        self.assertTrue(adapter.authentication_configured)
        with self.assertRaises(TypeError):
            value.__reduce_ex__(4)

    def test_fake_describe_frame_and_cancel_use_opaque_session(self):
        adapter = FakeRtspAdapter()
        value = request()
        session = adapter.describe(value)
        self.assertIsNotNone(session)
        self.assertEqual(session.codec, "H264")
        self.assertTrue(adapter.receive_one_frame(session))
        cancelled = adapter.describe(value)
        adapter.cancel(cancelled)
        self.assertFalse(adapter.receive_one_frame(cancelled))
        adapter.cancel(value)
        self.assertTrue(value.cancel_event.is_set())

    def test_failed_stage_stops_later_diagnostics(self):
        adapter = FakeRtspAdapter({RtspStage.MEDIA_DESCRIPTION: StageStatus.FAIL}, error_code="SDP_INVALID")
        result = adapter.probe(request())
        self.assertEqual(tuple(stage.status for stage in result.stages),
                         (StageStatus.PASS, StageStatus.PASS, StageStatus.FAIL, StageStatus.NOT_RUN))
        self.assertEqual(result.category, ProbeResultCode.PROTOCOL_ERROR)
        self.assertEqual(result.error_code, "SDP_INVALID")

    def test_gstreamer_absence_is_neutral_and_closes_socket(self):
        class Socket:
            closed = False
            address = None
            def settimeout(self, value): self.timeout = value
            def connect(self, address): self.address = address
            def close(self): self.closed = True
        sock = Socket()
        def missing(): raise GStreamerUnavailable
        result = GStreamerRtspAdapter(socket_factory=lambda *_: sock, loader=missing).probe(request())
        self.assertEqual(result.category, ProbeResultCode.INCONCLUSIVE)
        self.assertEqual(result.error_code, "ADAPTER_UNAVAILABLE")
        self.assertEqual(result.stages[0].status, StageStatus.PASS)
        self.assertTrue(sock.closed)
        self.assertEqual(sock.address, ("10.42.0.10", 554))

    def test_stage_a_timeout_and_refusal_close_fake_sockets(self):
        class Socket:
            def __init__(self, error): self.error, self.closed = error, False
            def settimeout(self, value): self.timeout = value
            def connect(self, address): raise self.error
            def close(self): self.closed = True
        for failure, expected in ((socket.timeout(), ProbeResultCode.TIMEOUT),
                                  (OSError(10061, "refused"), ProbeResultCode.CONNECTION_REFUSED)):
            with self.subTest(expected=expected):
                sock = Socket(failure)
                result = GStreamerRtspAdapter(socket_factory=lambda *_: sock).probe(request())
                self.assertEqual(result.category, expected)
                self.assertEqual(result.stages[0].status, StageStatus.FAIL)
                self.assertTrue(sock.closed)
                self.assertNotIn("refused", result.error_code or "")
    def test_gstreamer_uses_out_of_uri_credentials_no_proxy_and_selected_transport(self):
        secret = ResolvedCameraCredential("runtime-user", "runtime-password")
        for transport, expected in (("AUTO", 3), ("TCP", 1), ("UDP", 2)):
            with self.subTest(transport=transport):
                value = request(secret, transport)
                pipeline, source, decoder, sink = GStreamerRtspAdapter._pipeline(_FakeGst, _FakeRtsp, value)
                self.assertEqual(source.props["location"], "rtsp://10.42.0.10:554/stream1")
                self.assertNotIn("runtime-user", source.props["location"])
                self.assertNotIn("runtime-password", source.props["location"])
                self.assertEqual(source.props["user-id"], "runtime-user")
                self.assertEqual(source.props["user-pw"], "runtime-password")
                self.assertEqual(source.props["proxy"], None)
                self.assertEqual(source.props["protocols"], expected)
                self.assertEqual(sink.props["max-buffers"], 1)
                self.assertEqual(sink.props["max-bytes"], MAX_FRAME_BYTES)

    def test_gstreamer_auth_and_decoder_errors_are_closed_and_sanitized(self):
        classify = GStreamerRtspAdapter._classify_error
        self.assertEqual(classify("401 unauthorized secret-user"), "AUTH_FAILURE")
        self.assertEqual(classify("no suitable plugin for secret-camera"), "CONFIG_ERROR")
        self.assertEqual(classify("RTSP parse error"), "PROTOCOL_ERROR")
    def test_only_known_generic_rtp_codecs_select_depayloaders(self):
        self.assertEqual(_DEPAYLOADERS["H264"], "rtph264depay")
        self.assertEqual(_DEPAYLOADERS["H265"], "rtph265depay")
        self.assertEqual(_DEPAYLOADERS["JPEG"], "rtpjpegdepay")
        self.assertNotIn("VENDOR-MODE", _DEPAYLOADERS)


    def test_gstreamer_empty_polls_continue_until_later_contract_success(self):
        adapter, bus, _clock, _pipeline, _gst, _elements, _rtp_pad = _temporal_gstreamer_adapter()
        bus.actions = [None, None, bus.deliver_frame]
        result = adapter.probe(request())
        self.assertTrue(result.is_success)
        self.assertEqual(len(bus.quanta), 3)
        self.assertEqual(tuple(stage.status for stage in result.stages), (StageStatus.PASS,) * 4)

    def test_dynamic_depayloader_syncs_to_parent_target_before_rtp_flow(self):
        adapter, bus, _clock, pipeline, _gst, elements, rtp_pad = _temporal_gstreamer_adapter()
        bus.actions = [bus.deliver_frame]
        result = adapter.probe(request())
        depay = next(element for element in elements if element.name == "rtph264depay")
        self.assertEqual(pipeline.added_dynamic_state, ("PAUSED", "PLAYING", "NULL"))
        self.assertEqual(depay.sync_calls, 1)
        self.assertEqual(depay.state, "PLAYING")
        self.assertEqual(rtp_pad.link_calls, 1)
        self.assertTrue(rtp_pad.flow_active)
        self.assertTrue(result.is_success)
        self.assertEqual(tuple(stage.status for stage in result.stages), (StageStatus.PASS,) * 4)

    def test_dynamic_depay_sync_failure_fails_closed_before_rtp_release(self):
        adapter, bus, _clock, pipeline, _gst, elements, rtp_pad = _temporal_gstreamer_adapter(sync_result=False)
        bus.actions = [bus.deliver_frame]
        result = adapter.probe(request())
        depay = next(element for element in elements if element.name == "rtph264depay")
        self.assertEqual(depay.sync_calls, 1)
        self.assertEqual(depay.state, "NULL")
        self.assertEqual(rtp_pad.link_calls, 0)
        self.assertFalse(rtp_pad.flow_active)
        self.assertEqual(tuple(stage.status for stage in result.stages),
                         (StageStatus.PASS, StageStatus.PASS, StageStatus.FAIL, StageStatus.NOT_RUN))
        self.assertEqual(result.error_code, "DYNAMIC_ELEMENT_SYNC_FAILED")
        self.assertEqual(result.category, ProbeResultCode.PROTOCOL_ERROR)
        self.assertEqual(pipeline.states[-1], _gst.State.NULL)

    def test_gstreamer_empty_polls_consume_one_overall_deadline(self):
        adapter, bus, _clock, pipeline, gst, _elements, _rtp_pad = _temporal_gstreamer_adapter()
        result = adapter.probe(request(timeout=0.2, connect_timeout=0.15))
        self.assertEqual(result.category, ProbeResultCode.TIMEOUT)
        self.assertEqual(result.error_code, "TIMEOUT")
        self.assertEqual(len(bus.quanta), 2)
        self.assertTrue(all(0 < quantum <= int(0.1 * gst.SECOND) for quantum in bus.quanta))
        self.assertLessEqual(sum(bus.quanta), int(0.2 * gst.SECOND))
        self.assertGreaterEqual(sum(bus.quanta), int(0.2 * gst.SECOND) - 2)
        self.assertEqual(pipeline.states[-1], gst.State.NULL)
    def test_gstreamer_terminal_auth_error_does_not_wait_for_deadline(self):
        adapter, bus, _clock, pipeline, gst, _elements, _rtp_pad = _temporal_gstreamer_adapter()
        bus.actions = [SimpleNamespace(type=gst.MessageType.ERROR,
            parse_error=lambda: ("401 unauthorized", None))]
        result = adapter.probe(request())
        self.assertEqual(result.category, ProbeResultCode.AUTH_FAILURE)
        self.assertEqual(result.error_code, "AUTH_FAILURE")
        self.assertEqual(len(bus.quanta), 1)
        self.assertEqual(pipeline.states[-1], gst.State.NULL)
class ManualRtspServiceTests(DjangoTestCase):
    def setUp(self):
        self.actor = get_user_model().objects.create_user(username="rtsp-tech", password="test")
        permission = Permission.objects.get(content_type__app_label="cameras", codename="run_camera_connection_test")
        self.actor.user_permissions.add(permission)
        self.camera = Camera.objects.create(nome="RTSP Camera", fabricante="Livre", modelo="Livre", ip="10.42.0.10", farm="FARM-A")
        self.profile = CameraCapabilityProfile.objects.get(profile_key="RTSP_DISCOVERY_V1", version=1)
        self.path = self.profile.default_path or "/stream1"
        self.config = CameraConnectionConfig.objects.create(camera=self.camera, profile=self.profile, enabled=True,
            rtsp_uri=f"rtsp://10.42.0.10{self.path}")
        self.policy = TargetPolicy.from_mapping({
            "allowed_cidrs": ["10.42.0.0/24"], "denied_cidrs": [],
            "ports_by_scheme": {"rtsp": [554]},
            "allowed_paths_by_scheme": {"rtsp": [self.path]}, "allowed_farms": ["FARM-A"],
        })
    def _run(self, adapter, policy=None):
        return run_camera_connection_test(actor=self.actor, camera_id=self.camera.pk,
            target_policy=policy or self.policy, environment_allowed_ports=(554,), adapter=adapter)
    def test_manual_service_calls_no_resolver_without_configured_credential_and_does_not_mutate_monitoring(self):
        adapter = FakeRtspAdapter()
        before = list(EstadoMonitoramento.objects.filter(camera=self.camera).values())
        with patch("cameras.integracao.rtsp.service.resolve_active_credential_for_execution") as resolver:
            result = self._run(adapter)
        resolver.assert_not_called()
        self.assertTrue(result.is_success)
        self.assertEqual(before, list(EstadoMonitoramento.objects.filter(camera=self.camera).values()))
    def test_configured_credential_resolution_failure_stays_closed(self):
        credential = CameraCredential.objects.create(camera=self.camera, state="ACTIVE")
        self.config.credential = credential; self.config.save(update_fields=["credential"])
        adapter = FakeRtspAdapter()
        with patch("cameras.integracao.rtsp.service.resolve_active_credential_for_execution",
                   side_effect=CredentialOperationError("CROSS_CAMERA_REFERENCE")) as resolver:
            result = self._run(adapter)
        resolver.assert_called_once()
        self.assertEqual(result.error_code, "CREDENTIAL_UNAVAILABLE")
        self.assertEqual(adapter.calls, 0)
    def test_active_credential_from_r1_is_given_to_adapter_in_memory(self):
        credential = CameraCredential.objects.create(camera=self.camera, state="ACTIVE")
        self.config.credential = credential; self.config.save(update_fields=["credential"])
        secret = ResolvedCameraCredential("active-user", "active-password")
        adapter = FakeRtspAdapter()
        with patch("cameras.integracao.rtsp.service.resolve_active_credential_for_execution", return_value=secret) as resolver:
            result = self._run(adapter)
        resolver.assert_called_once()
        self.assertTrue(result.is_success)
        self.assertTrue(adapter.authentication_configured)
        self.assertNotIn("active-user", adapter.last_uri)
        self.assertNotIn("active-password", adapter.last_uri)
    def test_denied_target_never_resolves_credential_or_calls_adapter(self):
        adapter = FakeRtspAdapter()
        denied = TargetPolicy.from_mapping({"allowed_cidrs": ["10.43.0.0/24"],
            "ports_by_scheme": {"rtsp": [554]}, "allowed_paths_by_scheme": {"rtsp": [self.path]},
            "allowed_farms": ["FARM-A"]})
        with patch("cameras.integracao.rtsp.service.resolve_active_credential_for_execution") as resolver:
            result = self._run(adapter, denied)
        resolver.assert_not_called(); self.assertEqual(adapter.calls, 0)
        self.assertEqual(result.category, ProbeResultCode.TARGET_BLOCKED)
        self.assertEqual(result.stages[0].status, StageStatus.NOT_RUN)
    def test_stage_d_failure_remains_diagnostic_only_and_does_not_mutate_monitoring(self):
        adapter = FakeRtspAdapter({RtspStage.MEDIA_DELIVERY: StageStatus.FAIL}, error_code="MEDIA_DELIVERY_FAILED")
        before = list(EstadoMonitoramento.objects.filter(camera=self.camera).values())
        result = self._run(adapter)
        self.assertEqual(tuple(stage.status for stage in result.stages),
                         (StageStatus.PASS, StageStatus.PASS, StageStatus.PASS, StageStatus.FAIL))
        self.assertFalse(result.is_success)
        self.assertEqual(before, list(EstadoMonitoramento.objects.filter(camera=self.camera).values()))
    def test_permission_denial_precedes_config_and_network(self):
        self.actor.user_permissions.clear()
        adapter = FakeRtspAdapter()
        with self.assertRaises(PermissionDenied): self._run(adapter)
        self.assertEqual(adapter.calls, 0)
