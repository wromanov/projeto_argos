"""Laboratório sintético determinístico da MON-03C.

Estes testes exercitam somente a evidência de uma tentativa produzida pelo
contrato MON-03B. Nenhum teste interpreta uma sequência como estado de
domínio ou cria uma instância de Camera.
"""

from datetime import datetime, timedelta, timezone
from ipaddress import IPv4Address
import inspect
import unittest

from .monitoramento import contracts as contracts_module
from .monitoramento import fakes as fakes_module
from .monitoramento.contracts import ProbeRequest, ProbeResult, ProbeResultCode
from .monitoramento.fakes import FakeClock, FakeProbe


START_AT = datetime(2026, 8, 12, 12, 0, tzinfo=timezone.utc)
DOMAIN_STATE_NAMES = {"ONLINE", "OFFLINE", "UNKNOWN", "SUSPECT"}
DOMAIN_RESULT_FIELDS = {
    "status",
    "camera_status",
    "incident",
    "outage",
    "recovery",
}


def make_request(timeout_seconds: float = 5.0) -> ProbeRequest:
    return ProbeRequest(
        camera_id=7,
        address=IPv4Address("192.0.2.10"),
        port=554,
        adapter_key="synthetic",
        timeout_seconds=timeout_seconds,
        endpoint="/health",
    )


class ProbeResultMatrixTests(unittest.IsolatedAsyncioTestCase):
    async def test_all_published_codes_are_emittable_as_probe_results(self) -> None:
        published_codes = (
            ProbeResultCode.SUCCESS,
            ProbeResultCode.TIMEOUT,
            ProbeResultCode.CONNECTION_REFUSED,
            ProbeResultCode.AUTH_FAILURE,
            ProbeResultCode.TLS_ERROR,
            ProbeResultCode.PROTOCOL_ERROR,
            ProbeResultCode.CONFIG_ERROR,
            ProbeResultCode.TARGET_BLOCKED,
            ProbeResultCode.CANCELLED,
            ProbeResultCode.INCONCLUSIVE,
        )
        clock = FakeClock(start_at=START_AT)
        probe = FakeProbe(published_codes, clock=clock)

        results = [await probe.probe(make_request()) for _ in published_codes]

        self.assertEqual([result.code for result in results], list(published_codes))
        self.assertTrue(all(isinstance(result, ProbeResult) for result in results))
        self.assertTrue(
            all(result.observed_at.tzinfo is timezone.utc for result in results)
        )
        self.assertTrue(all(result.duration_seconds >= 0 for result in results))

    async def test_only_success_has_is_success_true(self) -> None:
        codes = tuple(ProbeResultCode)
        probe = FakeProbe(codes, clock=FakeClock(start_at=START_AT))

        results = [await probe.probe(make_request()) for _ in codes]

        for result, code in zip(results, codes):
            with self.subTest(code=code):
                self.assertIs(result.is_success, code is ProbeResultCode.SUCCESS)

    async def test_fifo_preserves_the_programmed_matrix_order(self) -> None:
        programmed = (
            ProbeResultCode.AUTH_FAILURE,
            ProbeResultCode.SUCCESS,
            ProbeResultCode.INCONCLUSIVE,
            ProbeResultCode.CANCELLED,
        )
        probe = FakeProbe(programmed, clock=FakeClock(start_at=START_AT))

        results = [await probe.probe(make_request()) for _ in programmed]

        self.assertEqual(tuple(result.code for result in results), programmed)

    async def assert_sequence(self, programmed: tuple[ProbeResultCode, ...]) -> None:
        probe = FakeProbe(programmed, clock=FakeClock(start_at=START_AT))
        results = [await probe.probe(make_request()) for _ in programmed]
        self.assertEqual(tuple(result.code for result in results), programmed)
        self.assertTrue(all(isinstance(result, ProbeResult) for result in results))

    async def test_sequence_success_success(self) -> None:
        await self.assert_sequence(
            (ProbeResultCode.SUCCESS, ProbeResultCode.SUCCESS)
        )

    async def test_sequence_timeout_success(self) -> None:
        await self.assert_sequence(
            (ProbeResultCode.TIMEOUT, ProbeResultCode.SUCCESS)
        )

    async def test_sequence_timeout_timeout_success(self) -> None:
        await self.assert_sequence(
            (
                ProbeResultCode.TIMEOUT,
                ProbeResultCode.TIMEOUT,
                ProbeResultCode.SUCCESS,
            )
        )

    async def test_sequence_success_timeout_success(self) -> None:
        await self.assert_sequence(
            (
                ProbeResultCode.SUCCESS,
                ProbeResultCode.TIMEOUT,
                ProbeResultCode.SUCCESS,
            )
        )

    async def test_sequence_auth_failure_success(self) -> None:
        await self.assert_sequence(
            (ProbeResultCode.AUTH_FAILURE, ProbeResultCode.SUCCESS)
        )

    async def test_sequence_target_blocked_success(self) -> None:
        await self.assert_sequence(
            (ProbeResultCode.TARGET_BLOCKED, ProbeResultCode.SUCCESS)
        )

    async def test_sequence_inconclusive_success(self) -> None:
        await self.assert_sequence(
            (ProbeResultCode.INCONCLUSIVE, ProbeResultCode.SUCCESS)
        )

    async def test_sequence_cancelled_success(self) -> None:
        await self.assert_sequence(
            (ProbeResultCode.CANCELLED, ProbeResultCode.SUCCESS)
        )

    async def test_sequence_connection_refused_connection_refused_success(self) -> None:
        await self.assert_sequence(
            (
                ProbeResultCode.CONNECTION_REFUSED,
                ProbeResultCode.CONNECTION_REFUSED,
                ProbeResultCode.SUCCESS,
            )
        )

    async def test_sequence_tls_error_protocol_error_success(self) -> None:
        await self.assert_sequence(
            (
                ProbeResultCode.TLS_ERROR,
                ProbeResultCode.PROTOCOL_ERROR,
                ProbeResultCode.SUCCESS,
            )
        )

    async def test_latency_below_budget_preserves_configured_outcome(self) -> None:
        clock = FakeClock(start_at=START_AT)
        probe = FakeProbe(
            [ProbeResultCode.AUTH_FAILURE], clock=clock, latency_seconds=1.5
        )

        result = await probe.probe(make_request(timeout_seconds=2.0))

        self.assertEqual(result.code, ProbeResultCode.AUTH_FAILURE)
        self.assertEqual(result.duration_seconds, 1.5)
        self.assertEqual(clock.monotonic(), 1.5)

    async def test_latency_equal_to_budget_preserves_configured_outcome(self) -> None:
        clock = FakeClock(start_at=START_AT)
        probe = FakeProbe(
            [ProbeResultCode.TLS_ERROR], clock=clock, latency_seconds=2.0
        )

        result = await probe.probe(make_request(timeout_seconds=2.0))

        self.assertEqual(result.code, ProbeResultCode.TLS_ERROR)
        self.assertEqual(result.duration_seconds, 2.0)
        self.assertEqual(clock.monotonic(), 2.0)

    async def test_latency_above_budget_returns_timeout_at_the_budget(self) -> None:
        clock = FakeClock(start_at=START_AT)
        probe = FakeProbe(
            [ProbeResultCode.CONFIG_ERROR], clock=clock, latency_seconds=3.0
        )

        result = await probe.probe(make_request(timeout_seconds=2.0))

        self.assertEqual(result.code, ProbeResultCode.TIMEOUT)
        self.assertNotEqual(result.code, ProbeResultCode.CONFIG_ERROR)
        self.assertEqual(result.duration_seconds, 2.0)
        self.assertEqual(clock.monotonic(), 2.0)
        self.assertEqual(clock.now(), START_AT + timedelta(seconds=2.0))

    async def test_timeout_consumes_one_outcome_and_does_not_retry_it(self) -> None:
        clock = FakeClock(start_at=START_AT)
        probe = FakeProbe(
            [ProbeResultCode.SUCCESS, ProbeResultCode.CONNECTION_REFUSED],
            clock=clock,
            latency_seconds=3.0,
        )

        timed_out = await probe.probe(make_request(timeout_seconds=1.0))
        next_attempt = await probe.probe(make_request(timeout_seconds=5.0))

        self.assertEqual(timed_out.code, ProbeResultCode.TIMEOUT)
        self.assertEqual(next_attempt.code, ProbeResultCode.CONNECTION_REFUSED)
        self.assertEqual(clock.monotonic(), 4.0)

    async def test_multiple_attempts_accumulate_wall_and_monotonic_clocks(self) -> None:
        clock = FakeClock(start_at=START_AT, monotonic_start=10.0)
        attempts = (
            (ProbeResultCode.SUCCESS, 1.0, 5.0),
            (ProbeResultCode.TIMEOUT, 2.0, 2.0),
            (ProbeResultCode.SUCCESS, 0.5, 5.0),
        )
        expected_at = START_AT
        expected_monotonic = 10.0

        for code, latency, timeout in attempts:
            probe = FakeProbe([code], clock=clock, latency_seconds=latency)
            result = await probe.probe(make_request(timeout_seconds=timeout))
            expected_at += timedelta(seconds=latency)
            expected_monotonic += latency

            self.assertEqual(result.code, code)
            self.assertEqual(result.observed_at, expected_at)
            self.assertEqual(result.duration_seconds, latency)
            self.assertEqual(clock.now(), expected_at)
            self.assertEqual(clock.monotonic(), expected_monotonic)

    async def test_empty_queue_raises_assertion_error_instead_of_result(self) -> None:
        probe = FakeProbe([], clock=FakeClock(start_at=START_AT))

        with self.assertRaises(AssertionError):
            await probe.probe(make_request())

    async def test_invalid_outcome_raises_type_error_instead_of_inconclusive(self) -> None:
        probe = FakeProbe([object()], clock=FakeClock(start_at=START_AT))

        with self.assertRaises(TypeError):
            await probe.probe(make_request())

    async def test_configured_cancelled_is_evidence_not_offline(self) -> None:
        probe = FakeProbe(
            [ProbeResultCode.CANCELLED], clock=FakeClock(start_at=START_AT)
        )

        result = await probe.probe(make_request())

        self.assertEqual(result.code, ProbeResultCode.CANCELLED)
        self.assertFalse(result.is_success)
        self.assertNotIn(result.code.name, DOMAIN_STATE_NAMES)

    def test_real_task_cancellation_is_not_captured_by_fake_probe(self) -> None:
        source = inspect.getsource(FakeProbe.probe)

        self.assertNotIn("CancelledError", source)
        self.assertNotIn("BaseException", source)

    def test_probe_contract_has_no_domain_state_or_io_dependency(self) -> None:
        self.assertTrue(
            DOMAIN_STATE_NAMES.isdisjoint(
                {member.name for member in ProbeResultCode}
            )
        )
        self.assertTrue(
            DOMAIN_RESULT_FIELDS.isdisjoint(ProbeResult.__dataclass_fields__)
        )
        self.assertNotIn("Camera", contracts_module.__dict__)
        self.assertNotIn("Camera", fakes_module.__dict__)
        self.assertNotIn("django", contracts_module.__dict__)
        self.assertNotIn("django", fakes_module.__dict__)
        self.assertNotIn("sleep(", inspect.getsource(FakeProbe))
