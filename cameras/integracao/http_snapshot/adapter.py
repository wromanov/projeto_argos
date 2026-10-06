"""Bounded, fail-closed HTTP snapshot acquisition for an authorized target."""

from __future__ import annotations

import asyncio
import math
import warnings
from dataclasses import dataclass, field
from ipaddress import IPv4Address
from io import BytesIO

import httpx
from PIL import Image, UnidentifiedImageError

from cameras.integracao.credentials import ResolvedCameraCredential

from cameras.integracao.target_policy import (
    AuthorizedTargetRequest,
    TargetDecision,
    TargetValidation,
)

MAX_RESPONSE_BYTES = 10 * 1024 * 1024
MAX_IMAGE_PIXELS = 20_000_000
MAX_ATTEMPT_SECONDS = 30.0
SUPPORTED_CONTENT_TYPES = frozenset({"image/jpeg", "image/png", "image/webp"})
_FORMAT_CONTENT_TYPES = {
    "JPEG": "image/jpeg",
    "PNG": "image/png",
    "WEBP": "image/webp",
}


class SnapshotCaptureError(Exception):
    """A sanitized failure code; never carries a URL, body, or credential."""

    def __init__(self, code: str):
        self.code = code
        super().__init__(code)


@dataclass(frozen=True, slots=True)
class SnapshotRequest:
    """Profile/config values plus a target decision produced by CAM-INT-07."""

    target: TargetValidation
    auth_method: str = "NONE"
    credential_required: bool = False
    allowed_content_types: frozenset[str] = SUPPORTED_CONTENT_TYPES
    timeout_seconds: float = MAX_ATTEMPT_SECONDS


@dataclass(frozen=True, slots=True)
class SnapshotImage:
    """Validated, metadata-free image bytes; no model or storage side effect."""

    data: bytes = field(repr=False)
    content_type: str
    image_format: str
    width: int
    height: int


class HttpSnapshotAdapter:
    """Fetch and validate one snapshot, without persisting or mutating health."""

    def __init__(self, *, transport: httpx.AsyncBaseTransport | None = None):
        # The transport seam is for isolated fakes; production defaults to
        # HTTPX's direct transport and never reads proxy/environment settings.
        self._transport = transport

    async def capture(
        self, request: SnapshotRequest, *, credential: ResolvedCameraCredential | None = None
    ) -> SnapshotImage:
        """Return a sanitized snapshot or a code-only ``SnapshotCaptureError``."""
        target = _authorized_target(request)
        auth = _authentication(request, target.scheme, credential)
        timeout_seconds = _bounded_timeout(request.timeout_seconds)
        allowed_types = _allowed_types(request.allowed_content_types)
        url = f"{target.scheme}://{target.ipv4}:{target.port}{target.path}"
        timeout = httpx.Timeout(
            timeout_seconds,
            connect=timeout_seconds,
            read=timeout_seconds,
            write=timeout_seconds,
            pool=timeout_seconds,
        )
        client_options = {
            "auth": auth,
            "follow_redirects": False,
            "verify": True,
            "trust_env": False,
            "timeout": timeout,
            "headers": {"Accept-Encoding": "identity"},
        }
        if self._transport is not None:
            client_options["transport"] = self._transport

        try:
            return await asyncio.wait_for(
                self._capture_with_client(url, client_options, allowed_types),
                timeout=timeout_seconds,
            )
        except asyncio.TimeoutError:
            raise SnapshotCaptureError("READ_TIMEOUT") from None
        except httpx.ConnectTimeout:
            raise SnapshotCaptureError("CONNECT_TIMEOUT") from None
        except httpx.ReadTimeout:
            raise SnapshotCaptureError("READ_TIMEOUT") from None
        except httpx.ConnectError as exc:
            code = "TLS_ERROR" if _caused_by_tls_error(exc) else "CONNECT_ERROR"
            raise SnapshotCaptureError(code) from None
        except httpx.RequestError:
            raise SnapshotCaptureError("HTTP_TRANSPORT_ERROR") from None

    async def _capture_with_client(self, url: str, client_options: dict, allowed_types: frozenset[str]) -> SnapshotImage:
        async with httpx.AsyncClient(**client_options) as client:
            async with client.stream("GET", url) as response:
                if response.status_code in {401, 403}:
                    raise SnapshotCaptureError("AUTH_FAILURE")
                if response.status_code != 200:
                    raise SnapshotCaptureError("HTTP_STATUS_ERROR")

                declared_type = _response_content_type(response.headers.get("content-type"), allowed_types)
                content_encoding = response.headers.get("content-encoding", "identity").strip().lower()
                if content_encoding not in {"", "identity"}:
                    raise SnapshotCaptureError("CONTENT_TYPE_INVALID")
                _check_content_length(response.headers.get("content-length"))

                chunks = bytearray()
                async for chunk in response.aiter_raw():
                    if len(chunks) + len(chunk) > MAX_RESPONSE_BYTES:
                        raise SnapshotCaptureError("BODY_TOO_LARGE")
                    chunks.extend(chunk)
                if not chunks:
                    raise SnapshotCaptureError("IMAGE_INVALID")
                return _validate_and_sanitize_image(bytes(chunks), declared_type)


def _authorized_target(request: SnapshotRequest):
    if not isinstance(request, SnapshotRequest):
        raise SnapshotCaptureError("CONFIG_INVALID")
    target_validation = request.target
    if (
        not isinstance(target_validation, TargetValidation)
        or target_validation.decision is not TargetDecision.AUTHORIZED_TARGET
        or target_validation.request is None
    ):
        raise SnapshotCaptureError("TARGET_DENIED")
    target = target_validation.request
    if (
        not isinstance(target, AuthorizedTargetRequest)
        or not isinstance(target.ipv4, IPv4Address)
        or target.scheme not in {"http", "https"}
        or type(target.port) is not int
        or not isinstance(target.path, str)
        or not target.path.startswith("/")
        or target.path.startswith("//")
        or "\\" in target.path
        or "?" in target.path
        or "#" in target.path
        or any(ord(char) < 32 for char in target.path)
        or not 1 <= target.port <= 65535
    ):
        raise SnapshotCaptureError("TARGET_DENIED")
    return target


def _authentication(
    request: SnapshotRequest, scheme: str, credential: ResolvedCameraCredential | None
):
    auth_method = request.auth_method
    if auth_method not in {"NONE", "BASIC", "DIGEST"}:
        raise SnapshotCaptureError("CAPABILITY_UNSUPPORTED")
    if auth_method == "NONE":
        if request.credential_required or credential is not None:
            raise SnapshotCaptureError("CONFIG_INVALID")
        return None
    if not isinstance(credential, ResolvedCameraCredential):
        raise SnapshotCaptureError("CREDENTIAL_MISSING")
    if not credential.username or not credential.password:
        raise SnapshotCaptureError("CREDENTIAL_MISSING")
    if scheme != "https":
        # This lane has no homologated environment policy that authorizes
        # credentials over cleartext HTTP.
        raise SnapshotCaptureError("CONFIG_INVALID")
    if auth_method == "BASIC":
        return httpx.BasicAuth(credential.username, credential.password)
    return httpx.DigestAuth(credential.username, credential.password)


def _bounded_timeout(value: object) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise SnapshotCaptureError("CONFIG_INVALID")
    try:
        timeout = float(value)
    except (OverflowError, ValueError):
        raise SnapshotCaptureError("CONFIG_INVALID") from None
    if not math.isfinite(timeout) or timeout <= 0:
        raise SnapshotCaptureError("CONFIG_INVALID")
    return min(timeout, MAX_ATTEMPT_SECONDS)


def _allowed_types(values: object) -> frozenset[str]:
    if not isinstance(values, (set, frozenset, tuple, list)):
        raise SnapshotCaptureError("CONFIG_INVALID")
    normalized = frozenset(value.strip().lower() for value in values if isinstance(value, str))
    if len(normalized) != len(values) or not normalized or not normalized <= SUPPORTED_CONTENT_TYPES:
        raise SnapshotCaptureError("CONFIG_INVALID")
    return normalized


def _response_content_type(value: str | None, allowed_types: frozenset[str]) -> str:
    if not value:
        raise SnapshotCaptureError("CONTENT_TYPE_INVALID")
    normalized = value.split(";", 1)[0].strip().lower()
    if normalized not in allowed_types:
        raise SnapshotCaptureError("CONTENT_TYPE_INVALID")
    return normalized


def _check_content_length(value: str | None) -> None:
    if value is None:
        return
    try:
        size = int(value)
    except (TypeError, ValueError):
        return
    if size < 0:
        raise SnapshotCaptureError("IMAGE_INVALID")
    if size > MAX_RESPONSE_BYTES:
        raise SnapshotCaptureError("BODY_TOO_LARGE")


def _validate_and_sanitize_image(data: bytes, declared_type: str) -> SnapshotImage:
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("error", Image.DecompressionBombWarning)
            with Image.open(BytesIO(data)) as image:
                image_format = image.format
                width, height = image.size
                if (
                    image_format not in _FORMAT_CONTENT_TYPES
                    or _FORMAT_CONTENT_TYPES[image_format] != declared_type
                    or not width
                    or not height
                    or width * height > MAX_IMAGE_PIXELS
                    or getattr(image, "n_frames", 1) != 1
                ):
                    raise SnapshotCaptureError("IMAGE_INVALID")
                image.verify()
            with Image.open(BytesIO(data)) as image:
                image.load()
                if image_format == "JPEG":
                    clean = image.convert("RGB")
                elif image_format == "WEBP":
                    clean = image.convert("RGB")
                else:
                    clean = image.convert("RGB")
                output = BytesIO()
                clean.save(output, format=image_format)
                sanitized = output.getvalue()
                if not sanitized or len(sanitized) > MAX_RESPONSE_BYTES:
                    raise SnapshotCaptureError("BODY_TOO_LARGE")
                return SnapshotImage(sanitized, declared_type, image_format, width, height)
    except SnapshotCaptureError:
        raise
    except (OSError, ValueError, SyntaxError, UnidentifiedImageError, Image.DecompressionBombError, Image.DecompressionBombWarning):
        raise SnapshotCaptureError("IMAGE_INVALID") from None


def _caused_by_tls_error(exc: BaseException) -> bool:
    current: BaseException | None = exc
    while current is not None:
        if current.__class__.__module__ == "ssl" and current.__class__.__name__ in {"SSLError", "CertificateError"}:
            return True
        current = current.__cause__ or current.__context__
    return False
