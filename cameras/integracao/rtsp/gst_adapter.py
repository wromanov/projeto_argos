"""Optional GStreamer runtime. Auth values are element properties, never URI text."""
from datetime import datetime, timezone
import errno
import socket
import time
from uuid import uuid4
from cameras.monitoramento.contracts import ProbeResultCode
from .ports import RtspConnectionRequest, RtspSession, RtspStage, StageStatus, make_result

MAX_FRAME_BYTES = 32 * 1024 * 1024
_DEPAYLOADERS = {
    "H264": "rtph264depay",
    "H265": "rtph265depay",
    "HEVC": "rtph265depay",
    "JPEG": "rtpjpegdepay",
    "MP4V-ES": "rtpmp4vdepay",
}

class GStreamerUnavailable(Exception):
    pass
class _Failure(Exception):
    def __init__(self, code):
        self.code = code
        super().__init__(code)

def _load_gstreamer():
    try:
        import gi
        gi.require_version("Gst", "1.0")
        gi.require_version("GstRtsp", "1.0")
        from gi.repository import Gst, GstRtsp
    except (ImportError, ValueError):
        raise GStreamerUnavailable from None
    Gst.init(None)
    return Gst, GstRtsp

class GStreamerRtspAdapter:
    def __init__(self, *, socket_factory=socket.socket, loader=_load_gstreamer, monotonic=time.monotonic, now=lambda: datetime.now(timezone.utc)):
        self.socket_factory, self.loader = socket_factory, loader
        self.monotonic, self.now = monotonic, now
        self._sessions = {}
    def describe(self, request):
        """Run a bounded RTSP attempt and return an opaque handle after SDP video is identified."""
        result = self.probe(request)
        if result.stages[2].status is not StageStatus.PASS or not result.codec:
            return None
        session = RtspSession(uuid4(), result.codec)
        self._sessions[session.id] = result.stages[3].status is StageStatus.PASS
        return session
    def receive_one_frame(self, session):
        """Consume the bounded frame outcome associated with an opaque session."""
        if not isinstance(session, RtspSession):
            return False
        return self._sessions.pop(session.id, False)
    def cancel(self, target):
        if isinstance(target, RtspConnectionRequest):
            target.cancel_event.set()
        elif isinstance(target, RtspSession):
            self._sessions.pop(target.id, None)

    def probe(self, request):
        started = self.monotonic()
        deadline = started + request.timeout_seconds
        statuses = [StageStatus.NOT_RUN] * 4
        code, category, codec = None, ProbeResultCode.INCONCLUSIVE, None
        sock = pipeline = None
        Gst = None
        seen = None
        try:
            if request.cancel_event.is_set():
                raise _Failure("CANCELLED")
            sock = self.socket_factory(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(min(request.connect_timeout_seconds, max(0.001, deadline - self.monotonic())))
            sock.connect((str(request.target.ipv4), request.target.port))
            if request.cancel_event.is_set():
                raise _Failure("CANCELLED")
            statuses[0] = StageStatus.PASS
            sock.close(); sock = None
            Gst, GstRtsp = self.loader()
            pipeline, src, decoder, sink = self._pipeline(Gst, GstRtsp, request)
            seen = {"sdp": False, "codec": None, "frame": False, "unsupported": False}
            def on_sdp(_src, _sdp):
                seen["sdp"] = True
            def source_pad(_src, pad):
                caps = pad.get_current_caps() or pad.query_caps(None)
                if not caps or not caps.get_size(): return
                structure = caps.get_structure(0)
                if structure.get_string("media") != "video": return
                encoding = structure.get_string("encoding-name")
                if not encoding: return
                name = _DEPAYLOADERS.get(encoding.upper())
                if name is None:
                    seen["unsupported"] = True
                    return
                depay = Gst.ElementFactory.make(name, f"video-depay-{encoding.lower()}")
                if depay is None:
                    seen["unsupported"] = True
                    return
                pipeline.add(depay)
                if not depay.link(decoder):
                    raise _Failure("PROTOCOL_ERROR")
                target = depay.get_static_pad("sink")
                if target is None or pad.link(target) != Gst.PadLinkReturn.OK:
                    raise _Failure("PROTOCOL_ERROR")
                seen["codec"] = encoding[:32]
            def decoder_pad(_decoder, pad):
                caps = pad.get_current_caps() or pad.query_caps(None)
                if caps and caps.get_size() and caps.get_structure(0).get_name().startswith("video/x-raw"):
                    target = sink.get_static_pad("sink")
                    if target and not target.is_linked(): pad.link(target)
            def sample(_sink):
                value = sink.emit("pull-sample")
                if value and value.get_buffer() and 0 < value.get_buffer().get_size() <= MAX_FRAME_BYTES:
                    seen["frame"] = True
                return Gst.FlowReturn.OK
            src.connect("on-sdp", on_sdp); src.connect("pad-added", source_pad)
            decoder.connect("pad-added", decoder_pad); sink.connect("new-sample", sample)
            if pipeline.set_state(Gst.State.PLAYING) == Gst.StateChangeReturn.FAILURE:
                raise _Failure("PROTOCOL_ERROR")
            bus = pipeline.get_bus()
            mask = Gst.MessageType.ERROR | Gst.MessageType.EOS | Gst.MessageType.ELEMENT | Gst.MessageType.REDIRECT
            while self.monotonic() < deadline and not seen["frame"]:
                if request.cancel_event.is_set():
                    raise _Failure("CANCELLED")
                remaining = deadline - self.monotonic()
                if remaining <= 0:
                    break
                poll_quantum_ns = max(1, min(int(remaining * Gst.SECOND), int(0.1 * Gst.SECOND)))
                message = bus.timed_pop_filtered(poll_quantum_ns, mask)
                if message is None:
                    continue
                if message.type == Gst.MessageType.ERROR:
                    err, _debug = message.parse_error()
                    code = self._classify_error(err)
                    if seen["codec"] and code == "PROTOCOL_ERROR": code = "MEDIA_DELIVERY_FAILED"
                    raise _Failure(code)
                if message.type == Gst.MessageType.REDIRECT: raise _Failure("UNAUTHORIZED_REDIRECT")
                if message.type == Gst.MessageType.EOS: break
                if message.type == Gst.MessageType.ELEMENT:
                    struct = message.get_structure()
                    if struct and struct.get_name() == "redirect": raise _Failure("UNAUTHORIZED_REDIRECT")
            if seen["sdp"]:
                statuses[1] = StageStatus.PASS
                if seen["codec"]:
                    statuses[2] = StageStatus.PASS; codec = seen["codec"]
                    if seen["frame"]:
                        statuses[3] = StageStatus.PASS; category = ProbeResultCode.SUCCESS
                    else:
                        statuses[3] = StageStatus.FAIL
                        code = "TIMEOUT" if self.monotonic() >= deadline else "MEDIA_DELIVERY_FAILED"
                        category = ProbeResultCode.TIMEOUT if code == "TIMEOUT" else ProbeResultCode.INCONCLUSIVE
                else:
                    statuses[2] = StageStatus.FAIL
                    code = "UNSUPPORTED_CAPABILITY" if seen["unsupported"] else "VIDEO_NOT_ANNOUNCED"
                    category = ProbeResultCode.INCONCLUSIVE
            elif self.monotonic() >= deadline:
                statuses[1] = StageStatus.FAIL; code = "TIMEOUT"; category = ProbeResultCode.TIMEOUT
            else:
                statuses[1] = StageStatus.FAIL; code = "PROTOCOL_ERROR"; category = ProbeResultCode.PROTOCOL_ERROR
        except GStreamerUnavailable:
            if statuses[0] is StageStatus.PASS: statuses[1] = StageStatus.FAIL
            code, category = "ADAPTER_UNAVAILABLE", ProbeResultCode.INCONCLUSIVE
        except socket.timeout:
            idx = 0 if statuses[0] is StageStatus.NOT_RUN else 1
            statuses[idx] = StageStatus.FAIL; code, category = "TIMEOUT", ProbeResultCode.TIMEOUT
        except OSError as exc:
            idx = 0 if statuses[0] is StageStatus.NOT_RUN else 1
            statuses[idx] = StageStatus.FAIL
            code = "CONNECTION_REFUSED" if exc.errno in {errno.ECONNREFUSED, errno.EHOSTUNREACH, errno.ENETUNREACH} else "PROTOCOL_ERROR"
            category = ProbeResultCode.CONNECTION_REFUSED if code == "CONNECTION_REFUSED" else ProbeResultCode.PROTOCOL_ERROR
        except _Failure as exc:
            if seen and seen["sdp"]:
                statuses[1] = StageStatus.PASS
                if seen["codec"]:
                    statuses[2] = StageStatus.PASS; codec = seen["codec"]
            idx = 1 if statuses[1] is StageStatus.NOT_RUN else 2 if statuses[2] is StageStatus.NOT_RUN else 3
            statuses[idx] = StageStatus.FAIL; code = exc.code
            category = ProbeResultCode.CANCELLED if code == "CANCELLED" else ProbeResultCode.AUTH_FAILURE if code == "AUTH_FAILURE" else ProbeResultCode.INCONCLUSIVE if code in {"UNAUTHORIZED_REDIRECT", "MEDIA_DELIVERY_FAILED", "VIDEO_NOT_ANNOUNCED", "UNSUPPORTED_CAPABILITY", "CONFIG_ERROR"} else ProbeResultCode.PROTOCOL_ERROR
        except Exception:
            idx = 1 if statuses[1] is StageStatus.NOT_RUN else 2 if statuses[2] is StageStatus.NOT_RUN else 3
            statuses[idx] = StageStatus.FAIL; code, category = "PROTOCOL_ERROR", ProbeResultCode.PROTOCOL_ERROR
        finally:
            if sock is not None:
                try: sock.close()
                except OSError: pass
            if pipeline is not None and Gst is not None:
                try: pipeline.set_state(Gst.State.NULL)
                except Exception: pass
        return make_result(tuple(statuses), category, started, error_code=code, codec=codec,
                           monotonic=self.monotonic, now=self.now)
    @staticmethod
    def _classify_error(error):
        # Provider text is inspected transiently and never returned or logged.
        value = str(error).lower()
        if any(marker in value for marker in ("401", "unauthorized", "authentication")):
            return "AUTH_FAILURE"
        if any(marker in value for marker in ("no suitable plugin", "missing decoder", "no decoder", "not-linked")):
            return "CONFIG_ERROR"
        return "PROTOCOL_ERROR"
    @staticmethod
    def _pipeline(Gst, GstRtsp, request):
        pipeline = Gst.Pipeline.new(None)
        source = Gst.ElementFactory.make("rtspsrc", "rtsp-source")
        decoder = Gst.ElementFactory.make("decodebin", "video-decoder")
        sink = Gst.ElementFactory.make("appsink", "frame-sink")
        if any(item is None for item in (pipeline, source, decoder, sink)): raise GStreamerUnavailable
        protocols = {"AUTO": GstRtsp.RTSPLowerTrans.TCP | GstRtsp.RTSPLowerTrans.UDP,
                     "TCP": GstRtsp.RTSPLowerTrans.TCP, "UDP": GstRtsp.RTSPLowerTrans.UDP}[request.transport]
        source.set_property("location", request.uri); source.set_property("protocols", protocols)
        source.set_property("proxy", None); source.set_property("debug", False)
        timeout_us = max(1, int(request.connect_timeout_seconds * 1_000_000))
        source.set_property("timeout", timeout_us); source.set_property("tcp-timeout", timeout_us)
        source.set_property("nat-method", 0); source.set_property("udp-reconnect", False)
        source.set_property("teardown-timeout", 0)
        if request.credential is not None:
            source.set_property("user-id", request.credential.username)
            source.set_property("user-pw", request.credential.password)
        sink.set_property("emit-signals", True); sink.set_property("max-buffers", 1)
        sink.set_property("drop", True); sink.set_property("sync", False)
        if sink.find_property("max-bytes") is None: raise GStreamerUnavailable
        sink.set_property("max-bytes", MAX_FRAME_BYTES)
        sink.set_property("enable-last-sample", False); sink.set_property("caps", Gst.Caps.from_string("video/x-raw"))
        pipeline.add(source); pipeline.add(decoder); pipeline.add(sink)
        if not decoder.link(sink): raise GStreamerUnavailable
        return pipeline, source, decoder, sink
