"""Synthetic RTSP adapter for tests; never opens external sockets."""
from datetime import datetime, timezone
import time
from cameras.monitoramento.contracts import ProbeResultCode
from uuid import uuid4
from .ports import RtspConnectionRequest, RtspFrameError, RtspJpegFrame, RtspSession, RtspStage, StageStatus, make_result
from .gst_adapter import _encode_validated_jpeg

class FakeRtspAdapter:
    def __init__(self, outcomes=None, *, codec="H264", error_code="PROTOCOL_ERROR", monotonic=time.monotonic, now=lambda: datetime.now(timezone.utc)):
        self.outcomes = dict(outcomes or {})
        self.codec, self.error_code = codec, error_code
        self.monotonic, self.now = monotonic, now
        self.calls = 0
        self.last_uri = None
        self.last_transport = None
        self.authentication_configured = False
        self._sessions = {}
    def describe(self, request):
        """Synthetic A/B/C flow, returning only an opaque session handle."""
        self.calls += 1
        self.last_uri = request.uri
        self.last_transport = request.transport
        self.authentication_configured = request.credential is not None
        for stage in (RtspStage.NETWORK_REACHABILITY, RtspStage.RTSP_REACHABILITY, RtspStage.MEDIA_DESCRIPTION):
            if self.outcomes.get(stage, StageStatus.PASS) is not StageStatus.PASS:
                return None
        session = RtspSession(uuid4(), self.codec)
        self._sessions[session.id] = self.outcomes.get(RtspStage.MEDIA_DELIVERY, StageStatus.PASS)
        return session

    def receive_one_frame(self, session):
        if not isinstance(session, RtspSession):
            return False
        return self._sessions.pop(session.id, StageStatus.NOT_RUN) is StageStatus.PASS

    def cancel(self, target):
        if isinstance(target, RtspConnectionRequest):
            target.cancel_event.set()
        elif isinstance(target, RtspSession):
            self._sessions.pop(target.id, None)

    def extract_one_jpeg_frame(self, request: RtspConnectionRequest) -> RtspJpegFrame:
        """Synthetic bytes only; this does not establish GStreamer codec support."""
        if not isinstance(request, RtspConnectionRequest):
            raise RtspFrameError("INVALID_REQUEST")
        if request.cancel_event.is_set():
            raise RtspFrameError("CANCELLED")
        self.calls += 1
        self.last_uri = request.uri
        self.last_transport = request.transport
        self.authentication_configured = request.credential is not None
        if any(self.outcomes.get(stage, StageStatus.PASS) is not StageStatus.PASS for stage in RtspStage):
            code = self.error_code if self.error_code in {"INVALID_REQUEST", "TARGET_BLOCKED", "CREDENTIAL_UNAVAILABLE", "AUTH_FAILURE", "CODEC_UNAVAILABLE", "DECODE_FAILED", "ENCODE_FAILED", "INVALID_SAMPLE", "LIMIT_EXCEEDED", "TIMEOUT", "CANCELLED", "UNAUTHORIZED_REDIRECT", "TEARDOWN_FAILED", "RUNTIME_ERROR"} else "RUNTIME_ERROR"
            raise RtspFrameError(code)
        if self.codec not in {"H264", "H265"}:
            raise RtspFrameError("CODEC_UNAVAILABLE")
        encoded = _encode_validated_jpeg(bytes((255, 0, 0, 0, 255, 0, 0, 0, 255, 255, 255, 255)), 2, 2)
        if request.cancel_event.is_set():
            raise RtspFrameError("CANCELLED")
        return RtspJpegFrame(encoded, 2, 2, self.codec, self.now())

    def probe(self, request):
        started = self.monotonic()
        self.calls += 1
        self.last_uri = request.uri
        self.last_transport = request.transport
        self.authentication_configured = request.credential is not None
        statuses, stopped = [], False
        for stage in RtspStage:
            status = StageStatus.NOT_RUN if stopped else self.outcomes.get(stage, StageStatus.PASS)
            if not isinstance(status, StageStatus):
                status = StageStatus.FAIL
            statuses.append(status)
            stopped = stopped or status is not StageStatus.PASS
        failed = next((i for i, status in enumerate(statuses) if status is StageStatus.FAIL), None)
        code = self.error_code if failed is not None else None
        category = ProbeResultCode.SUCCESS
        if failed is not None:
            category = {"TIMEOUT": ProbeResultCode.TIMEOUT,
                        "CONNECTION_REFUSED": ProbeResultCode.CONNECTION_REFUSED,
                        "AUTH_FAILURE": ProbeResultCode.AUTH_FAILURE,
                        "TARGET_BLOCKED": ProbeResultCode.TARGET_BLOCKED}.get(code, ProbeResultCode.INCONCLUSIVE if code in {"CONFIG_ERROR", "ADAPTER_UNAVAILABLE", "CREDENTIAL_UNAVAILABLE", "UNSUPPORTED_CAPABILITY"} else ProbeResultCode.PROTOCOL_ERROR)
        return make_result(tuple(statuses), category, started, error_code=code,
                           codec=self.codec if statuses[2] is StageStatus.PASS else None,
                           monotonic=self.monotonic, now=self.now)
