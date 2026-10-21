"""Optional GStreamer runtime. Auth values are element properties, never URI text."""
from datetime import datetime, timezone
from io import BytesIO
import errno
import socket
import time
from uuid import uuid4
from PIL import Image, UnidentifiedImageError
from cameras.monitoramento.contracts import ProbeResultCode
from .ports import RtspConnectionRequest, RtspFrameError, RtspJpegFrame, RtspSession, RtspStage, StageStatus, make_result

MAX_FRAME_BYTES = 32 * 1024 * 1024
MAX_RAW_BYTES = 12 * 1024 * 1024
MAX_JPEG_BYTES = 5 * 1024 * 1024
FRAME_DEADLINE_SECONDS = 15.0

class _BoundedJpegBuffer(BytesIO):
    def write(self, data):
        if self.tell() + len(data) > MAX_JPEG_BYTES:
            raise RtspFrameError("LIMIT_EXCEEDED")
        return super().write(data)
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

def _load_gst_video():
    try:
        import gi
        gi.require_version("GstVideo", "1.0")
        from gi.repository import GstVideo
        return GstVideo
    except (ImportError, ValueError):
        raise GStreamerUnavailable from None

def _copy_rgb_rows(data, *, width, height, stride, offset=0, buffer_size=None):
    """Validate the actual raw allocation and row layout before making one owned copy."""
    if any(isinstance(value, bool) or not isinstance(value, int) for value in (width, height, stride, offset)):
        raise RtspFrameError("INVALID_SAMPLE")
    if width <= 0 or height <= 0 or width > 1920 or height > 1080 or width * height > 2_073_600:
        raise RtspFrameError("LIMIT_EXCEEDED")
    if stride < width * 3 or stride > 8192 or offset < 0:
        raise RtspFrameError("INVALID_SAMPLE")
    try:
        size = len(data) if buffer_size is None else buffer_size
        if isinstance(size, bool) or not isinstance(size, int) or size <= 0:
            raise RtspFrameError("INVALID_SAMPLE")
        if size > MAX_RAW_BYTES or stride * height > MAX_RAW_BYTES:
            raise RtspFrameError("LIMIT_EXCEEDED")
        if offset + stride * height > size or len(data) < size:
            raise RtspFrameError("INVALID_SAMPLE")
        view = memoryview(data)
        row_size = width * 3
        return b"".join(view[offset + row * stride:offset + row * stride + row_size]
                        for row in range(height))
    except RtspFrameError:
        raise
    except (TypeError, ValueError, BufferError):
        raise RtspFrameError("INVALID_SAMPLE") from None

def _encode_validated_jpeg(rgb, width, height, *, check=lambda: None):
    """Encode with a fixed quality and independently decode the finished JPEG."""
    try:
        check()
        image = Image.frombytes("RGB", (width, height), rgb)
        output = _BoundedJpegBuffer()
        image.save(output, format="JPEG", quality=85)
        check()
        encoded = output.getvalue()
        if len(encoded) > MAX_JPEG_BYTES:
            raise RtspFrameError("LIMIT_EXCEEDED")
        if not encoded.startswith(b"\xff\xd8") or not encoded.endswith(b"\xff\xd9"):
            raise RtspFrameError("ENCODE_FAILED")
        with Image.open(BytesIO(encoded)) as decoded:
            if decoded.format != "JPEG" or decoded.size != (width, height):
                raise RtspFrameError("ENCODE_FAILED")
            decoded.load()
        check()
        return encoded
    except RtspFrameError:
        raise
    except (OSError, ValueError, TypeError, UnidentifiedImageError):
        raise RtspFrameError("ENCODE_FAILED") from None

def _sample_rgb(sample, Gst, GstVideo, check):
    """Read effective row layout from video metadata or caps, then copy once."""
    if sample is None:
        raise RtspFrameError("INVALID_SAMPLE")
    caps, buffer = sample.get_caps(), sample.get_buffer()
    if caps is None or buffer is None or caps.get_size() != 1:
        raise RtspFrameError("INVALID_SAMPLE")
    structure = caps.get_structure(0)
    if structure.get_name() != "video/x-raw" or structure.get_string("format") != "RGB":
        raise RtspFrameError("INVALID_SAMPLE")
    info = GstVideo.VideoInfo()
    if not info.from_caps(caps):
        raise RtspFrameError("INVALID_SAMPLE")
    width, height = int(info.width), int(info.height)
    actual_size = buffer.get_size()
    if actual_size > MAX_RAW_BYTES:
        raise RtspFrameError("LIMIT_EXCEEDED")
    if actual_size <= 0:
        raise RtspFrameError("INVALID_SAMPLE")
    meta = GstVideo.buffer_get_video_meta(buffer)
    stride = int(meta.stride[0] if meta is not None else info.stride[0])
    offset = int(meta.offset[0] if meta is not None else info.offset[0])
    # Validate the declared layout before Gst.Buffer.map may merge memory blocks.
    if width <= 0 or height <= 0 or width > 1920 or height > 1080 or width * height > 2_073_600 or stride * height > MAX_RAW_BYTES:
        raise RtspFrameError("LIMIT_EXCEEDED")
    if stride < width * 3 or stride > 8192 or offset < 0 or offset + stride * height > actual_size:
        raise RtspFrameError("INVALID_SAMPLE")
    check()
    mapped, map_info = buffer.map(Gst.MapFlags.READ)
    if not mapped:
        raise RtspFrameError("INVALID_SAMPLE")
    try:
        rgb = _copy_rgb_rows(map_info.data, width=width, height=height, stride=stride,
                             offset=offset, buffer_size=actual_size)
    finally:
        buffer.unmap(map_info)
    check()
    return rgb, width, height

class GStreamerRtspAdapter:
    def __init__(self, *, socket_factory=socket.socket, loader=_load_gstreamer, video_loader=_load_gst_video, monotonic=time.monotonic, now=lambda: datetime.now(timezone.utc)):
        self.socket_factory, self.loader = socket_factory, loader
        self.video_loader = video_loader
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

    def extract_one_jpeg_frame(self, request: RtspConnectionRequest) -> RtspJpegFrame:
        """Extract one RGB sample and return only a validated in-memory JPEG.

        The typed request is an internal input, not evidence of source authorization.
        The caller must obtain its target and credential from the authorized boundary.
        """
        if not isinstance(request, RtspConnectionRequest):
            raise RtspFrameError("INVALID_REQUEST")
        started = self.monotonic()
        deadline = started + min(request.timeout_seconds, FRAME_DEADLINE_SECONDS)
        pipeline = Gst = None
        result = failure = None
        seen = {"rgb": None, "codec": None, "failure": None}

        def check():
            if request.cancel_event.is_set():
                raise RtspFrameError("CANCELLED")
            if self.monotonic() >= deadline:
                raise RtspFrameError("TIMEOUT")

        def record(code):
            if seen["failure"] is None:
                seen["failure"] = code

        try:
            check()
            Gst, GstRtsp = self.loader()
            GstVideo = self.video_loader()
            check()
            pipeline, source, decoder, converter, sink = self._frame_pipeline(
                Gst, GstRtsp, request, lambda: deadline - self.monotonic())

            def source_pad(_source, pad):
                try:
                    check()
                    caps = pad.get_current_caps() or pad.query_caps(None)
                    if caps is None or not caps.get_size():
                        return
                    structure = caps.get_structure(0)
                    if structure.get_string("media") != "video":
                        return
                    encoding = structure.get_string("encoding-name")
                    codec = encoding.upper() if isinstance(encoding, str) else ""
                    if codec == "HEVC":
                        codec = "H265"
                    if codec not in {"H264", "H265"}:
                        record("CODEC_UNAVAILABLE")
                        return
                    depay = Gst.ElementFactory.make(_DEPAYLOADERS[codec], "frame-depay")
                    if depay is None:
                        record("CODEC_UNAVAILABLE")
                        return
                    pipeline.add(depay)
                    if not depay.link(decoder) or not depay.sync_state_with_parent():
                        record("DECODE_FAILED")
                        return
                    target = depay.get_static_pad("sink")
                    if target is None or pad.link(target) != Gst.PadLinkReturn.OK:
                        record("DECODE_FAILED")
                        return
                    seen["codec"] = codec
                except RtspFrameError as exc:
                    record(exc.code)
                except Exception:
                    record("RUNTIME_ERROR")

            def decoder_pad(_decoder, pad):
                try:
                    check()
                    caps = pad.get_current_caps() or pad.query_caps(None)
                    if caps is None or not caps.get_size() or not caps.get_structure(0).get_name().startswith("video/x-raw"):
                        return
                    target = converter.get_static_pad("sink")
                    if target is None or (not target.is_linked() and pad.link(target) != Gst.PadLinkReturn.OK):
                        record("DECODE_FAILED")
                except RtspFrameError as exc:
                    record(exc.code)
                except Exception:
                    record("RUNTIME_ERROR")

            def sample(_sink):
                try:
                    check()
                    if seen["rgb"] is None:
                        value = sink.emit("pull-sample")
                        seen["rgb"] = _sample_rgb(value, Gst, GstVideo, check)
                except RtspFrameError as exc:
                    record(exc.code)
                except Exception:
                    record("INVALID_SAMPLE")
                return Gst.FlowReturn.OK

            source.connect("pad-added", source_pad)
            decoder.connect("pad-added", decoder_pad)
            sink.connect("new-sample", sample)
            check()
            if pipeline.set_state(Gst.State.PLAYING) == Gst.StateChangeReturn.FAILURE:
                raise RtspFrameError("DECODE_FAILED")
            bus = pipeline.get_bus()
            mask = Gst.MessageType.ERROR | Gst.MessageType.EOS | Gst.MessageType.ELEMENT | Gst.MessageType.REDIRECT

            def inspect_message(message):
                if message is None:
                    return
                if message.type == Gst.MessageType.REDIRECT:
                    raise RtspFrameError("UNAUTHORIZED_REDIRECT")
                if message.type == Gst.MessageType.ELEMENT:
                    structure = message.get_structure()
                    if structure is not None and structure.get_name() == "redirect":
                        raise RtspFrameError("UNAUTHORIZED_REDIRECT")
                if message.type == Gst.MessageType.ERROR:
                    error, _debug = message.parse_error()
                    classified = self._classify_error(error)
                    raise RtspFrameError("AUTH_FAILURE" if classified == "AUTH_FAILURE" else
                                         "CODEC_UNAVAILABLE" if classified == "CONFIG_ERROR" else "DECODE_FAILED")
                if message.type == Gst.MessageType.EOS and seen["rgb"] is None:
                    raise RtspFrameError("DECODE_FAILED")

            while seen["rgb"] is None:
                check()
                if seen["failure"]:
                    raise RtspFrameError(seen["failure"])
                remaining = deadline - self.monotonic()
                message = bus.timed_pop_filtered(max(1, min(int(remaining * Gst.SECOND), int(0.1 * Gst.SECOND))), mask)
                inspect_message(message)
            if seen["failure"]:
                raise RtspFrameError(seen["failure"])
            # Reject redirects already visible on the bus; late redirects are not
            # pre-connect enforcement and require separate runtime validation.
            while True:
                message = bus.timed_pop_filtered(0, mask)
                if message is None:
                    break
                inspect_message(message)
            check()
            if seen["codec"] not in {"H264", "H265"}:
                raise RtspFrameError("CODEC_UNAVAILABLE")
            rgb, width, height = seen["rgb"]
            encoded = _encode_validated_jpeg(rgb, width, height, check=check)
            check()
            result = RtspJpegFrame(encoded, width, height, seen["codec"], self.now())
        except RtspFrameError as exc:
            failure = exc
        except GStreamerUnavailable:
            failure = RtspFrameError("RUNTIME_ERROR")
        except Exception:
            failure = RtspFrameError("RUNTIME_ERROR")
        finally:
            if pipeline is not None and Gst is not None:
                try:
                    if pipeline.set_state(Gst.State.NULL) == Gst.StateChangeReturn.FAILURE:
                        raise RuntimeError
                    remaining_ns = max(0, int((deadline - self.monotonic()) * Gst.SECOND))
                    state_result, current, _pending = pipeline.get_state(remaining_ns)
                    if state_result == Gst.StateChangeReturn.FAILURE or current != Gst.State.NULL:
                        raise RuntimeError
                except Exception:
                    failure = RtspFrameError("TEARDOWN_FAILED")
            if failure is None:
                if request.cancel_event.is_set():
                    failure = RtspFrameError("CANCELLED")
                elif self.monotonic() >= deadline:
                    failure = RtspFrameError("TIMEOUT")
        if failure is not None:
            raise failure
        return result

    @staticmethod
    def _frame_pipeline(Gst, GstRtsp, request, remaining_seconds=None):
        pipeline = Gst.Pipeline.new(None)
        if pipeline is None:
            raise GStreamerUnavailable
        try:
            source = Gst.ElementFactory.make("rtspsrc", "frame-rtsp-source")
            decoder = Gst.ElementFactory.make("decodebin", "frame-video-decoder")
            converter = Gst.ElementFactory.make("videoconvert", "frame-video-converter")
            sink = Gst.ElementFactory.make("appsink", "frame-rgb-sink")
            if any(item is None for item in (source, decoder, converter, sink)):
                raise GStreamerUnavailable
            protocols = {"AUTO": GstRtsp.RTSPLowerTrans.TCP | GstRtsp.RTSPLowerTrans.UDP,
                         "TCP": GstRtsp.RTSPLowerTrans.TCP, "UDP": GstRtsp.RTSPLowerTrans.UDP}[request.transport]
            source.set_property("location", request.uri)
            source.set_property("protocols", protocols)
            source.set_property("proxy", None)
            source.set_property("debug", False)
            remaining = remaining_seconds() if callable(remaining_seconds) else (
                FRAME_DEADLINE_SECONDS if remaining_seconds is None else remaining_seconds)
            timeout_us = min(int(request.connect_timeout_seconds * 1_000_000), int(remaining * 1_000_000))
            if timeout_us <= 0:
                raise RtspFrameError("TIMEOUT")
            source.set_property("timeout", timeout_us)
            source.set_property("tcp-timeout", timeout_us)
            source.set_property("nat-method", 0)
            source.set_property("udp-reconnect", False)
            source.set_property("teardown-timeout", 0)
            if request.credential is not None:
                source.set_property("user-id", request.credential.username)
                source.set_property("user-pw", request.credential.password)
            sink.set_property("emit-signals", True)
            sink.set_property("max-buffers", 1)
            sink.set_property("drop", True)
            sink.set_property("sync", False)
            sink.set_property("enable-last-sample", False)
            if sink.find_property("max-bytes") is not None:
                sink.set_property("max-bytes", MAX_RAW_BYTES)
            sink.set_property("caps", Gst.Caps.from_string("video/x-raw,format=RGB"))
            pipeline.add(source)
            pipeline.add(decoder)
            pipeline.add(converter)
            pipeline.add(sink)
            if not converter.link(sink):
                raise GStreamerUnavailable
            return pipeline, source, decoder, converter, sink
        except Exception:
            try:
                if pipeline.set_state(Gst.State.NULL) == Gst.StateChangeReturn.FAILURE:
                    raise RuntimeError
                state_result, current, _pending = pipeline.get_state(0)
                if state_result == Gst.StateChangeReturn.FAILURE or current != Gst.State.NULL:
                    raise RuntimeError
            except Exception:
                raise RtspFrameError("TEARDOWN_FAILED") from None
            raise

    def probe(self, request):
        started = self.monotonic()
        deadline = started + request.timeout_seconds
        statuses = [StageStatus.NOT_RUN] * 4
        stage_started = [started, None, None, None]
        stage_ended = [None, None, None, None]
        stage_observed = [None, None, None, None]
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
            stage_ended[0] = self.monotonic(); stage_observed[0] = self.now()
            stage_started[1] = stage_ended[0]
            sock.close(); sock = None
            Gst, GstRtsp = self.loader()
            pipeline, src, decoder, sink = self._pipeline(Gst, GstRtsp, request)
            seen = {"sdp": False, "codec": None, "frame": False, "unsupported": False, "failure": None}
            def on_sdp(_src, _sdp):
                seen["sdp"] = True
                if stage_ended[1] is None:
                    stage_ended[1] = self.monotonic(); stage_observed[1] = self.now()
                    stage_started[2] = stage_ended[1]
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
                try:
                    synchronized = depay.sync_state_with_parent()
                except Exception:
                    synchronized = False
                if not synchronized:
                    # PyGObject callback exceptions do not reliably reach the probe loop.
                    seen["failure"] = "DYNAMIC_ELEMENT_SYNC_FAILED"
                    return
                target = depay.get_static_pad("sink")
                if target is None or pad.link(target) != Gst.PadLinkReturn.OK:
                    raise _Failure("PROTOCOL_ERROR")
                seen["codec"] = encoding[:32]
                if stage_ended[2] is None:
                    stage_ended[2] = self.monotonic(); stage_observed[2] = self.now()
                    stage_started[3] = stage_ended[2]
            def decoder_pad(_decoder, pad):
                caps = pad.get_current_caps() or pad.query_caps(None)
                if caps and caps.get_size() and caps.get_structure(0).get_name().startswith("video/x-raw"):
                    target = sink.get_static_pad("sink")
                    if target and not target.is_linked(): pad.link(target)
            def sample(_sink):
                value = sink.emit("pull-sample")
                if value and value.get_buffer() and 0 < value.get_buffer().get_size() <= MAX_FRAME_BYTES:
                    seen["frame"] = True
                    stage_ended[3] = self.monotonic(); stage_observed[3] = self.now()
                return Gst.FlowReturn.OK
            src.connect("on-sdp", on_sdp); src.connect("pad-added", source_pad)
            decoder.connect("pad-added", decoder_pad); sink.connect("new-sample", sample)
            if pipeline.set_state(Gst.State.PLAYING) == Gst.StateChangeReturn.FAILURE:
                raise _Failure("PROTOCOL_ERROR")
            bus = pipeline.get_bus()
            mask = Gst.MessageType.ERROR | Gst.MessageType.EOS | Gst.MessageType.ELEMENT | Gst.MessageType.REDIRECT
            while self.monotonic() < deadline and not seen["frame"]:
                if seen["failure"]:
                    raise _Failure(seen["failure"])
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
            if seen["failure"]:
                raise _Failure(seen["failure"])
            if seen["sdp"]:
                statuses[1] = StageStatus.PASS
                if stage_ended[1] is None:
                    stage_ended[1] = self.monotonic(); stage_observed[1] = self.now()
                    stage_started[2] = stage_ended[1]
                if seen["codec"]:
                    statuses[2] = StageStatus.PASS; codec = seen["codec"]
                    if stage_ended[2] is None:
                        stage_ended[2] = self.monotonic(); stage_observed[2] = self.now()
                        stage_started[3] = stage_ended[2]
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
            code = exc.code
            category = ProbeResultCode.CANCELLED if code == "CANCELLED" else ProbeResultCode.AUTH_FAILURE if code == "AUTH_FAILURE" else ProbeResultCode.INCONCLUSIVE if code in {"UNAUTHORIZED_REDIRECT", "MEDIA_DELIVERY_FAILED", "VIDEO_NOT_ANNOUNCED", "UNSUPPORTED_CAPABILITY", "CONFIG_ERROR"} else ProbeResultCode.PROTOCOL_ERROR
            if code != "CANCELLED":
                idx = 1 if statuses[1] is StageStatus.NOT_RUN else 2 if statuses[2] is StageStatus.NOT_RUN else 3
                statuses[idx] = StageStatus.FAIL
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
        finished = self.monotonic()
        finished_at = self.now()
        stage_timings = {}
        for index, stage in enumerate(RtspStage):
            if statuses[index] is StageStatus.NOT_RUN:
                stage_timings[stage] = (finished_at, 0.0)
                continue
            end = stage_ended[index] if stage_ended[index] is not None else finished
            start = stage_started[index] if stage_started[index] is not None else end
            stage_timings[stage] = (
                stage_observed[index] if stage_observed[index] is not None else finished_at,
                max(0.0, end - start),
            )
        return make_result(tuple(statuses), category, started, error_code=code, codec=codec,
                           stage_timings=stage_timings, monotonic=self.monotonic, now=self.now)
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
        return pipeline, source, decoder, sink
