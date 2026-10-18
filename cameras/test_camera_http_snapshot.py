from __future__ import annotations

from io import BytesIO
from unittest.mock import patch

import httpx
from django.test import SimpleTestCase
from PIL import Image

from cameras.integracao.http_snapshot.adapter import (
    MAX_RESPONSE_BYTES,
    HttpSnapshotAdapter,
    SnapshotCaptureError,
    SnapshotRequest,
)
from cameras.integracao.http_snapshot.fake import FakeHttpSnapshotAdapter, SyntheticResponse
from cameras.integracao.credentials import ResolvedCameraCredential
from cameras.integracao.target_policy import TargetPolicy


def _png(width=3, height=2):
    output = BytesIO()
    Image.new("RGB", (width, height), "red").save(output, format="PNG")
    return output.getvalue()


def _target(scheme="https", *, camera_ip="192.0.2.10"):
    policy = TargetPolicy.from_mapping(
        {
            "allowed_cidrs": ["192.0.2.0/24"],
            "ports_by_scheme": {"https": [443], "http": [80]},
            "allowed_paths_by_scheme": {"https": ["/snapshot"], "http": ["/snapshot"]},
        }
    )
    return policy.validate(
        camera_ip,
        f"{scheme}://{camera_ip}:{443 if scheme == 'https' else 80}/snapshot",
        allowed_schemes=(scheme,),
        allowed_ports=(443 if scheme == "https" else 80,),
        allowed_paths=("/snapshot",),
    )


def _request(target=None, **kwargs):
    return SnapshotRequest(target=target or _target(), **kwargs)


class HttpSnapshotAdapterTests(SimpleTestCase):
    async def test_authorized_target_returns_decoded_metadata_free_bytes_without_side_effect_api(self):
        fake = FakeHttpSnapshotAdapter([SyntheticResponse(body=_png())])
        result = await fake.capture(_request())

        self.assertEqual((result.content_type, result.image_format, result.width, result.height), ("image/png", "PNG", 3, 2))
        with Image.open(BytesIO(result.data)) as image:
            self.assertEqual(image.size, (3, 2))
            self.assertEqual(image.info, {})
        self.assertEqual(len(fake.requests), 1)
        self.assertEqual(str(fake.requests[0].url), "https://192.0.2.10/snapshot")
        self.assertEqual(fake.requests[0].url.port or 443, 443)
        self.assertTrue(fake.streams[0].closed)

    async def test_client_disables_redirects_and_environment_proxy_and_keeps_tls_verification(self):
        fake = FakeHttpSnapshotAdapter([SyntheticResponse(body=_png())])
        real_client = httpx.AsyncClient
        options = {}

        def make_client(**kwargs):
            options.update(kwargs)
            return real_client(**kwargs)

        with patch("cameras.integracao.http_snapshot.adapter.httpx.AsyncClient", side_effect=make_client):
            await fake.capture(_request())

        self.assertFalse(options["follow_redirects"])
        self.assertFalse(options["trust_env"])
        self.assertIs(options["verify"], True)
        self.assertNotIn("proxy", options)
        self.assertIsNotNone(options["transport"])

    async def test_redirect_is_not_followed_and_response_stream_is_closed(self):
        fake = FakeHttpSnapshotAdapter(
            [SyntheticResponse(status_code=302, headers=(("location", "https://198.51.100.2/other"),), body=b"redirect")]
        )
        with self.assertRaises(SnapshotCaptureError) as raised:
            await fake.capture(_request())

        self.assertEqual(raised.exception.code, "HTTP_STATUS_ERROR")
        self.assertEqual(len(fake.requests), 1)
        self.assertEqual(str(fake.requests[0].url), "https://192.0.2.10/snapshot")
        self.assertEqual(fake.requests[0].url.port or 443, 443)
        self.assertTrue(fake.streams[0].closed)

    async def test_denied_target_fails_before_client_creation(self):
        denied = _target(camera_ip="203.0.113.7")
        with patch("cameras.integracao.http_snapshot.adapter.httpx.AsyncClient") as client:
            with self.assertRaises(SnapshotCaptureError) as raised:
                await HttpSnapshotAdapter().capture(_request(denied))

        self.assertEqual(raised.exception.code, "TARGET_DENIED")
        client.assert_not_called()

    async def test_http_auth_requires_explicit_https_environment_policy(self):
        with self.assertRaises(SnapshotCaptureError) as raised:
            await HttpSnapshotAdapter().capture(
                _request(
                    target=_target("http"),
                    auth_method="BASIC",
                ),
                credential=ResolvedCameraCredential("camera-user", "camera-password"),
            )
        self.assertEqual(raised.exception.code, "CONFIG_INVALID")

    async def test_basic_auth_is_transient_and_credentials_are_not_exposed_by_repr_or_error(self):
        credentials = ResolvedCameraCredential("camera-user", "camera-password")
        fake = FakeHttpSnapshotAdapter([SyntheticResponse(status_code=401, body=b"sensitive server response")])

        with self.assertRaises(SnapshotCaptureError) as raised:
            await fake.capture(_request(auth_method="BASIC"), credential=credentials)

        self.assertEqual(raised.exception.code, "AUTH_FAILURE")
        self.assertNotIn("camera-user", repr(credentials))
        self.assertNotIn("camera-password", repr(credentials))
        self.assertNotIn("camera-user", str(raised.exception))
        self.assertNotIn("camera-password", str(raised.exception))
        self.assertNotIn("sensitive server response", str(raised.exception))
        self.assertTrue(fake.requests[0].headers.get("authorization", "").startswith("Basic "))
        self.assertNotIn("@", str(fake.requests[0].url))
        self.assertTrue(fake.streams[0].closed)

    async def test_resolved_credential_is_separate_from_serializable_request(self):
        from dataclasses import asdict

        credential = ResolvedCameraCredential("camera-user", "camera-password")
        request = _request(auth_method="BASIC")
        self.assertNotIn("credentials", asdict(request))
        self.assertNotIn("camera-user", repr(request))
        self.assertNotIn("camera-password", repr(request))
        self.assertNotIn("camera-user", str(credential))
        self.assertNotIn("camera-password", str(credential))

    async def test_missing_required_credential_fails_closed(self):
        with self.assertRaises(SnapshotCaptureError) as raised:
            await HttpSnapshotAdapter().capture(_request(auth_method="DIGEST", credential_required=True))
        self.assertEqual(raised.exception.code, "CREDENTIAL_MISSING")

    async def test_timeout_budget_is_finite_positive_and_capped(self):
        for timeout in (0, -1, float("inf"), float("nan"), True):
            with self.subTest(timeout=timeout):
                with self.assertRaises(SnapshotCaptureError) as raised:
                    await HttpSnapshotAdapter().capture(_request(timeout_seconds=timeout))
                self.assertEqual(raised.exception.code, "CONFIG_INVALID")

        fake = FakeHttpSnapshotAdapter([SyntheticResponse(body=_png())])
        real_client = httpx.AsyncClient
        options = {}

        def make_client(**kwargs):
            options.update(kwargs)
            return real_client(**kwargs)

        with patch("cameras.integracao.http_snapshot.adapter.httpx.AsyncClient", side_effect=make_client):
            await fake.capture(_request(timeout_seconds=60))
        self.assertEqual(options["timeout"].connect, 30.0)
        self.assertEqual(options["timeout"].read, 30.0)

    async def test_invalid_status_content_type_empty_body_and_image_decode_fail_closed(self):
        cases = (
            (SyntheticResponse(status_code=503, body=b"private response"), "HTTP_STATUS_ERROR"),
            (SyntheticResponse(headers=(("content-type", "text/html"),), body=b"<html>error</html>"), "CONTENT_TYPE_INVALID"),
            (SyntheticResponse(body=b""), "IMAGE_INVALID"),
            (SyntheticResponse(body=b"not a png"), "IMAGE_INVALID"),
        )
        for response, expected in cases:
            with self.subTest(expected=expected, status=response.status_code):
                fake = FakeHttpSnapshotAdapter([response])
                with self.assertRaises(SnapshotCaptureError) as raised:
                    await fake.capture(_request())
                self.assertEqual(raised.exception.code, expected)
                if response.body:
                    self.assertNotIn(response.body.decode("latin1", errors="ignore"), str(raised.exception))
                self.assertTrue(fake.streams[0].closed)

    async def test_streaming_body_bound_wins_even_when_content_length_lies(self):
        fake = FakeHttpSnapshotAdapter(
            [SyntheticResponse(headers=(("content-type", "image/png"), ("content-length", "1")), body=b"x" * (MAX_RESPONSE_BYTES + 1))]
        )
        with self.assertRaises(SnapshotCaptureError) as raised:
            await fake.capture(_request())
        self.assertEqual(raised.exception.code, "BODY_TOO_LARGE")
        self.assertTrue(fake.streams[0].closed)

    async def test_pixel_limit_is_enforced_before_decoding_large_image(self):
        oversized_pixels = _png(width=5000, height=5000)
        fake = FakeHttpSnapshotAdapter([SyntheticResponse(body=oversized_pixels)])
        with self.assertRaises(SnapshotCaptureError) as raised:
            await fake.capture(_request())
        self.assertEqual(raised.exception.code, "IMAGE_INVALID")
        self.assertTrue(fake.streams[0].closed)

    async def test_digest_auth_uses_transient_challenge_response(self):
        fake = FakeHttpSnapshotAdapter(
            [
                SyntheticResponse(
                    status_code=401,
                    headers=(("www-authenticate", 'Digest realm="camera", nonce="test-nonce", algorithm=MD5, qop="auth"'),),
                    body=b"challenge",
                ),
                SyntheticResponse(body=_png()),
            ]
        )
        result = await fake.capture(
            _request(
                auth_method="DIGEST",
            ),
            credential=ResolvedCameraCredential("camera-user", "camera-password"),
        )
        self.assertEqual(result.image_format, "PNG")
        self.assertEqual(len(fake.requests), 2)
        self.assertTrue(fake.requests[1].headers.get("authorization", "").startswith("Digest "))
        self.assertTrue(all("@" not in str(request.url) for request in fake.requests))
        self.assertTrue(all(stream.closed for stream in fake.streams))

    async def test_encoded_response_is_not_unboundedly_decompressed(self):
        fake = FakeHttpSnapshotAdapter(
            [SyntheticResponse(headers=(("content-type", "image/png"), ("content-encoding", "gzip")), body=_png())]
        )
        with self.assertRaises(SnapshotCaptureError) as raised:
            await fake.capture(_request())
        self.assertEqual(raised.exception.code, "CONTENT_TYPE_INVALID")
        self.assertTrue(fake.streams[0].closed)

    async def test_timeout_and_cancellation_close_response_stream(self):
        delayed = FakeHttpSnapshotAdapter([SyntheticResponse(body=_png(), delay_before_body=0.1)])
        with self.assertRaises(SnapshotCaptureError) as raised:
            await delayed.capture(_request(timeout_seconds=0.01))
        self.assertEqual(raised.exception.code, "READ_TIMEOUT")
        self.assertTrue(delayed.streams[0].closed)

        cancelled = FakeHttpSnapshotAdapter([SyntheticResponse(body=_png(), delay_before_body=5)])
        task = __import__("asyncio").create_task(cancelled.capture(_request(timeout_seconds=10)))
        await __import__("asyncio").sleep(0.01)
        task.cancel()
        with self.assertRaises(__import__("asyncio").CancelledError):
            await task
        self.assertTrue(cancelled.streams[0].closed)
