"""Testes unitários puros do contrato MON-03B."""

from datetime import datetime, timedelta, timezone
from ipaddress import IPv4Address, IPv6Address
import inspect
import math
import unittest

from .monitoramento.clock import SystemClock
from .monitoramento.contracts import (
    ProbeAdapter,
    ProbeRequest,
    ProbeResult,
    ProbeResultCode,
)
from .monitoramento.fakes import FakeClock, FakeProbe


def make_request(timeout_seconds: float = 5.0) -> ProbeRequest:
    return ProbeRequest(
        camera_id=7,
        address=IPv4Address("192.0.2.10"),
        port=554,
        adapter_key="synthetic",
        timeout_seconds=timeout_seconds,
        endpoint="/health",
    )


async def call_probe(adapter: ProbeAdapter, request: ProbeRequest) -> ProbeResult:
    return await adapter.probe(request)


class ProbeResultCodeTests(unittest.TestCase):
    def test_has_exact_expected_codes_and_only_success_is_success(self) -> None:
        expected = {
            "SUCCESS",
            "TIMEOUT",
            "CONNECTION_REFUSED",
            "AUTH_FAILURE",
            "TLS_ERROR",
            "PROTOCOL_ERROR",
            "CONFIG_ERROR",
            "TARGET_BLOCKED",
            "CANCELLED",
            "INCONCLUSIVE",
        }
        self.assertEqual({member.name for member in ProbeResultCode}, expected)
        self.assertEqual(ProbeResultCode.SUCCESS.value, "SUCCESS")
        self.assertEqual(
            [member for member in ProbeResultCode if member is ProbeResultCode.SUCCESS],
            [ProbeResultCode.SUCCESS],
        )


class ProbeRequestTests(unittest.TestCase):
    def test_valid_request_is_immutable_and_has_no_credential_ref(self) -> None:
        request = make_request()
        self.assertEqual(request.timeout_seconds, 5.0)
        self.assertFalse(hasattr(request, "credential_ref"))
        with self.assertRaises(AttributeError):
            request.port = 443

    def test_requires_positive_integer_camera_id(self) -> None:
        for value in (0, -1, True, "7"):
            with self.subTest(value=value):
                with self.assertRaises((TypeError, ValueError)):
                    ProbeRequest(value, IPv4Address("192.0.2.10"), 80, "tcp", 1.0)

    def test_requires_ipv4_address(self) -> None:
        with self.assertRaises(TypeError):
            ProbeRequest(1, "192.0.2.10", 80, "tcp", 1.0)
        with self.assertRaises(TypeError):
            ProbeRequest(1, IPv6Address("2001:db8::10"), 80, "tcp", 1.0)

    def test_rejects_invalid_ports_and_timeout(self) -> None:
        for port in (0, 65536, True):
            with self.subTest(port=port):
                with self.assertRaises((TypeError, ValueError)):
                    ProbeRequest(1, IPv4Address("192.0.2.10"), port, "tcp", 1.0)
        for timeout in (0, -1, True, "1", math.nan, math.inf, -math.inf):
            with self.subTest(timeout=timeout):
                with self.assertRaises((TypeError, ValueError)):
                    ProbeRequest(1, IPv4Address("192.0.2.10"), 80, "tcp", timeout)

    def test_rejects_empty_adapter_key(self) -> None:
        for adapter_key in ("", " \t"):
            with self.subTest(adapter_key=adapter_key):
                with self.assertRaises(ValueError):
                    ProbeRequest(1, IPv4Address("192.0.2.10"), 80, adapter_key, 1.0)

    def test_endpoint_is_relative_path_only(self) -> None:
        for endpoint in (
            "https://camera.example/health",
            "//camera.example/health",
            "user:secret@camera/health",
        ):
            with self.subTest(endpoint=endpoint):
                with self.assertRaises(ValueError):
                    ProbeRequest(1, IPv4Address("192.0.2.10"), 80, "tcp", 1.0, endpoint)
        self.assertIsNone(
            ProbeRequest(1, IPv4Address("192.0.2.10"), 80, "tcp", 1.0).endpoint
        )


class ProbeResultTests(unittest.TestCase):
    def test_success_and_timeout_are_valid_and_success_is_derived(self) -> None:
        observed_at = datetime(2026, 8, 12, 12, 0, tzinfo=timezone.utc)
        success = ProbeResult(ProbeResultCode.SUCCESS, observed_at, 0)
        timeout = ProbeResult(ProbeResultCode.TIMEOUT, observed_at, 0.25, "READ_TIMEOUT")
        self.assertTrue(success.is_success)
        self.assertFalse(timeout.is_success)
        self.assertEqual(success.duration_seconds, 0.0)

    def test_observed_at_is_aware_and_normalized_to_utc(self) -> None:
        local = timezone(timedelta(hours=-3))
        result = ProbeResult(
            ProbeResultCode.SUCCESS,
            datetime(2026, 8, 12, 9, 0, tzinfo=local),
            0,
        )
        self.assertEqual(result.observed_at, datetime(2026, 8, 12, 12, 0, tzinfo=timezone.utc))
        self.assertIs(result.observed_at.tzinfo, timezone.utc)

    def test_rejects_invalid_duration_and_contradictory_success(self) -> None:
        observed_at = datetime.now(timezone.utc)
        for duration in (-0.01, math.nan, math.inf, True, "1"):
            with self.subTest(duration=duration):
                with self.assertRaises((TypeError, ValueError)):
                    ProbeResult(ProbeResultCode.TIMEOUT, observed_at, duration)
        with self.assertRaises(ValueError):
            ProbeResult(ProbeResultCode.SUCCESS, observed_at, 0, "UNEXPECTED")

    def test_rejects_unsafe_error_codes(self) -> None:
        observed_at = datetime.now(timezone.utc)
        for error_code in ("bad code", "line\nbreak", "https://secret", "x" * 65):
            with self.subTest(error_code=error_code):
                with self.assertRaises(ValueError):
                    ProbeResult(ProbeResultCode.TIMEOUT, observed_at, 0, error_code)


class ClockTests(unittest.TestCase):
    def test_system_clock_is_utc_aware_and_monotonic_is_numeric(self) -> None:
        clock = SystemClock()
        self.assertIsNotNone(clock.now().tzinfo)
        self.assertEqual(clock.now().utcoffset(), timedelta(0))
        self.assertIsInstance(clock.monotonic(), float)

    def test_fake_clock_advances_wall_and_monotonic_without_sleep(self) -> None:
        initial = datetime(2026, 8, 12, 12, 0, tzinfo=timezone.utc)
        clock = FakeClock(start_at=initial, monotonic_start=10.0)
        clock.advance(2.5)
        self.assertEqual(clock.now(), initial + timedelta(seconds=2.5))
        self.assertEqual(clock.monotonic(), 12.5)

    def test_fake_clock_rejects_invalid_advance(self) -> None:
        clock = FakeClock()
        for value in (-1, True, "1", math.nan, math.inf):
            with self.subTest(value=value):
                with self.assertRaises((TypeError, ValueError)):
                    clock.advance(value)


class FakeProbeTests(unittest.IsolatedAsyncioTestCase):
    async def test_configured_success_and_functional_protocol_substitution(self) -> None:
        clock = FakeClock()
        probe = FakeProbe([ProbeResultCode.SUCCESS], clock=clock)
        result = await call_probe(probe, make_request())
        self.assertEqual(result.code, ProbeResultCode.SUCCESS)
        self.assertTrue(result.is_success)
        self.assertIsInstance(result, ProbeResult)

    async def test_fifo_timeout_timeout_success(self) -> None:
        clock = FakeClock()
        probe = FakeProbe(
            [ProbeResultCode.TIMEOUT, ProbeResultCode.TIMEOUT, ProbeResultCode.SUCCESS],
            clock=clock,
        )
        results = [await probe.probe(make_request()) for _ in range(3)]
        self.assertEqual(
            [result.code for result in results],
            [ProbeResultCode.TIMEOUT, ProbeResultCode.TIMEOUT, ProbeResultCode.SUCCESS],
        )

    async def test_empty_queue_fails_explicitly(self) -> None:
        probe = FakeProbe([], clock=FakeClock())
        with self.assertRaises(AssertionError):
            await probe.probe(make_request())

    async def test_synthetic_latency_advances_clock_and_duration(self) -> None:
        clock = FakeClock()
        probe = FakeProbe([ProbeResultCode.SUCCESS], clock=clock, latency_seconds=1.25)
        result = await probe.probe(make_request(timeout_seconds=2.0))
        self.assertEqual(result.duration_seconds, 1.25)
        self.assertEqual(clock.monotonic(), 1.25)
        self.assertEqual(result.observed_at, datetime(2000, 1, 1, 0, 0, 1, 250000, tzinfo=timezone.utc))

    async def test_latency_over_budget_returns_timeout_at_budget(self) -> None:
        clock = FakeClock()
        probe = FakeProbe([ProbeResultCode.SUCCESS], clock=clock, latency_seconds=3.0)
        result = await probe.probe(make_request(timeout_seconds=1.5))
        self.assertEqual(result.code, ProbeResultCode.TIMEOUT)
        self.assertEqual(result.duration_seconds, 1.5)
        self.assertEqual(clock.monotonic(), 1.5)

    async def test_cancelled_outcome_remains_cancelled(self) -> None:
        probe = FakeProbe([ProbeResultCode.CANCELLED], clock=FakeClock())
        result = await probe.probe(make_request())
        self.assertEqual(result.code, ProbeResultCode.CANCELLED)
        self.assertFalse(result.is_success)

    def test_fake_probe_has_no_real_sleep(self) -> None:
        source = inspect.getsource(FakeProbe)
        self.assertNotIn("sleep(", source)
