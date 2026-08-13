"""Testes focados do contrato puro MON-04B."""

from datetime import datetime, timedelta, timezone
import inspect
import unittest

from .monitoramento.confirmation import (
    ConfirmationMemory,
    ConfirmationPolicy,
    ProcessingDisposition,
    TechnicalDecisionAction,
    TechnicalDecisionReason,
    TechnicalState,
    reduce_confirmation,
)
from .monitoramento.contracts import ProbeResult, ProbeResultCode


START_AT = datetime(2026, 8, 12, 12, 0, tzinfo=timezone.utc)


def make_policy(
    *, failures_to_offline: int = 2, successes_to_online: int = 2, version: str = "v1"
) -> ConfirmationPolicy:
    return ConfirmationPolicy(
        failures_to_offline=failures_to_offline,
        successes_to_online=successes_to_online,
        version=version,
    )


def make_result(code: ProbeResultCode, offset_seconds: int) -> ProbeResult:
    return ProbeResult(
        code=code,
        observed_at=START_AT + timedelta(seconds=offset_seconds),
        duration_seconds=0.0,
    )


def apply_code(
    memory: ConfirmationMemory,
    code: ProbeResultCode,
    offset_seconds: int,
    policy: ConfirmationPolicy,
) -> tuple[ConfirmationMemory, object]:
    return reduce_confirmation(memory, make_result(code, offset_seconds), policy)


class ConfirmationPolicyTests(unittest.TestCase):
    def test_thresholds_are_required_and_have_structural_minimums(self) -> None:
        with self.assertRaises(ValueError):
            make_policy(failures_to_offline=1)
        self.assertEqual(make_policy(failures_to_offline=2).failures_to_offline, 2)

        with self.assertRaises(TypeError):
            make_policy(failures_to_offline=True)
        with self.assertRaises(ValueError):
            make_policy(successes_to_online=0)
        self.assertEqual(make_policy(successes_to_online=1).successes_to_online, 1)
        with self.assertRaises(ValueError):
            make_policy(version="")

        with self.assertRaises(TypeError):
            ConfirmationPolicy(2, 1, None)  # type: ignore[arg-type]

    def test_policy_is_immutable_and_version_is_machine_safe(self) -> None:
        policy = make_policy()
        with self.assertRaises(AttributeError):
            policy.version = "v2"
        for version in (" ", "v 1", "v/1", "x" * 65):
            with self.subTest(version=version):
                with self.assertRaises(ValueError):
                    make_policy(version=version)


class ConfirmationMemoryTests(unittest.TestCase):
    def test_initial_requires_explicit_policy_version_and_is_unknown(self) -> None:
        memory = ConfirmationMemory.initial("v1")
        self.assertEqual(memory.state, TechnicalState.UNKNOWN)
        self.assertEqual(memory.positive_streak, 0)
        self.assertEqual(memory.negative_streak, 0)
        self.assertIsNone(memory.last_observed_at)
        self.assertFalse(memory.is_suspect)
        with self.assertRaises(TypeError):
            ConfirmationMemory.initial(None)  # type: ignore[arg-type]

    def test_memory_is_frozen_and_normalizes_aware_timestamp_to_utc(self) -> None:
        local = timezone(timedelta(hours=-3))
        memory = ConfirmationMemory(
            state=TechnicalState.UNKNOWN,
            positive_streak=1,
            negative_streak=0,
            last_observed_at=datetime(2026, 8, 12, 9, 0, tzinfo=local),
            policy_version="v1",
        )
        self.assertEqual(
            memory.last_observed_at,
            datetime(2026, 8, 12, 12, 0, tzinfo=timezone.utc),
        )
        self.assertTrue(memory.is_suspect)
        with self.assertRaises(AttributeError):
            memory.state = TechnicalState.ONLINE

    def test_memory_rejects_invalid_streaks_and_two_directions(self) -> None:
        for value in (-1, True, "1"):
            with self.subTest(value=value):
                with self.assertRaises((TypeError, ValueError)):
                    ConfirmationMemory(TechnicalState.UNKNOWN, value, 0, None, "v1")
        with self.assertRaises(ValueError):
            ConfirmationMemory(TechnicalState.UNKNOWN, 1, 1, None, "v1")
        with self.assertRaises(ValueError):
            ConfirmationMemory(TechnicalState.ONLINE, 1, 0, None, "v1")
        with self.assertRaises(ValueError):
            ConfirmationMemory(TechnicalState.OFFLINE, 0, 1, None, "v1")
        with self.assertRaises(ValueError):
            ConfirmationMemory(
                TechnicalState.UNKNOWN,
                0,
                0,
                datetime(2026, 8, 12, 12, 0),
                "v1",
            )


class ConfirmationReducerTests(unittest.TestCase):
    def test_unknown_success_and_timeout_confirm_only_at_threshold(self) -> None:
        policy = make_policy()

        memory = ConfirmationMemory.initial(policy.version)
        memory, decision = apply_code(memory, ProbeResultCode.SUCCESS, 1, policy)
        self.assertEqual(memory.state, TechnicalState.UNKNOWN)
        self.assertEqual(memory.positive_streak, 1)
        self.assertEqual(decision.reason, TechnicalDecisionReason.POSITIVE_EVIDENCE)

        memory, decision = apply_code(memory, ProbeResultCode.SUCCESS, 2, policy)
        self.assertEqual(memory.state, TechnicalState.ONLINE)
        self.assertEqual(decision.action, TechnicalDecisionAction.CONFIRM_ONLINE)
        self.assertEqual(decision.reason, TechnicalDecisionReason.CONFIRMED_ONLINE)
        self.assertEqual((memory.positive_streak, memory.negative_streak), (0, 0))

        memory = ConfirmationMemory.initial(policy.version)
        memory, _ = apply_code(memory, ProbeResultCode.TIMEOUT, 1, policy)
        self.assertEqual(memory.state, TechnicalState.UNKNOWN)
        self.assertEqual(memory.negative_streak, 1)
        memory, decision = apply_code(memory, ProbeResultCode.TIMEOUT, 2, policy)
        self.assertEqual(memory.state, TechnicalState.OFFLINE)
        self.assertEqual(decision.action, TechnicalDecisionAction.CONFIRM_OFFLINE)
        self.assertEqual(decision.reason, TechnicalDecisionReason.CONFIRMED_OFFLINE)
        self.assertEqual((memory.positive_streak, memory.negative_streak), (0, 0))

    def test_online_failure_isolated_and_opposite_success(self) -> None:
        policy = make_policy()
        memory = ConfirmationMemory(
            TechnicalState.ONLINE,
            0,
            0,
            START_AT,
            policy.version,
        )
        memory, decision = apply_code(memory, ProbeResultCode.TIMEOUT, 1, policy)
        self.assertEqual(memory.state, TechnicalState.ONLINE)
        self.assertEqual(memory.negative_streak, 1)
        self.assertTrue(decision.is_suspect)

        memory, decision = apply_code(memory, ProbeResultCode.SUCCESS, 2, policy)
        self.assertEqual(memory.state, TechnicalState.ONLINE)
        self.assertEqual((memory.positive_streak, memory.negative_streak), (0, 0))
        self.assertEqual(decision.reason, TechnicalDecisionReason.STABLE_STATE_REAFFIRMED)

        memory, _ = apply_code(memory, ProbeResultCode.TIMEOUT, 3, policy)
        memory, decision = apply_code(memory, ProbeResultCode.TIMEOUT, 4, policy)
        self.assertEqual(memory.state, TechnicalState.OFFLINE)
        self.assertEqual(decision.action, TechnicalDecisionAction.CONFIRM_OFFLINE)

    def test_offline_recovery_and_opposite_failure(self) -> None:
        policy = make_policy()
        memory = ConfirmationMemory(
            TechnicalState.OFFLINE,
            0,
            0,
            START_AT,
            policy.version,
        )
        memory, decision = apply_code(memory, ProbeResultCode.SUCCESS, 1, policy)
        self.assertEqual(memory.state, TechnicalState.OFFLINE)
        self.assertEqual(memory.positive_streak, 1)
        self.assertEqual(decision.action, TechnicalDecisionAction.NO_CHANGE)

        memory, decision = apply_code(memory, ProbeResultCode.TIMEOUT, 2, policy)
        self.assertEqual(memory.state, TechnicalState.OFFLINE)
        self.assertEqual((memory.positive_streak, memory.negative_streak), (0, 0))
        self.assertEqual(decision.reason, TechnicalDecisionReason.STABLE_STATE_REAFFIRMED)

        memory, _ = apply_code(memory, ProbeResultCode.SUCCESS, 3, policy)
        memory, decision = apply_code(memory, ProbeResultCode.SUCCESS, 4, policy)
        self.assertEqual(memory.state, TechnicalState.ONLINE)
        self.assertEqual(decision.action, TechnicalDecisionAction.CONFIRM_ONLINE)

    def test_timeout_and_connection_refused_share_negative_streak(self) -> None:
        policy = make_policy()
        memory = ConfirmationMemory.initial(policy.version)
        memory, _ = apply_code(memory, ProbeResultCode.TIMEOUT, 1, policy)
        memory, decision = apply_code(
            memory, ProbeResultCode.CONNECTION_REFUSED, 2, policy
        )
        self.assertEqual(memory.state, TechnicalState.OFFLINE)
        self.assertEqual(decision.action, TechnicalDecisionAction.CONFIRM_OFFLINE)

    def test_neutral_barriers_reset_pending_without_changing_state(self) -> None:
        policy = make_policy()
        neutral_codes = (
            ProbeResultCode.AUTH_FAILURE,
            ProbeResultCode.TLS_ERROR,
            ProbeResultCode.PROTOCOL_ERROR,
            ProbeResultCode.CONFIG_ERROR,
            ProbeResultCode.TARGET_BLOCKED,
            ProbeResultCode.INCONCLUSIVE,
        )
        for code in neutral_codes:
            with self.subTest(code=code):
                memory = ConfirmationMemory(
                    TechnicalState.ONLINE,
                    0,
                    1,
                    START_AT,
                    policy.version,
                )
                updated, decision = apply_code(memory, code, 1, policy)
                self.assertEqual(updated.state, TechnicalState.ONLINE)
                self.assertEqual((updated.positive_streak, updated.negative_streak), (0, 0))
                self.assertEqual(decision.action, TechnicalDecisionAction.NO_CHANGE)
                self.assertEqual(decision.reason, TechnicalDecisionReason.NEUTRAL_BARRIER)
                self.assertGreater(updated.last_observed_at, memory.last_observed_at)

    def test_cancelled_is_a_barrier_and_breaks_both_sequences(self) -> None:
        policy = make_policy()
        memory = ConfirmationMemory.initial(policy.version)
        memory, _ = apply_code(memory, ProbeResultCode.TIMEOUT, 1, policy)
        memory, decision = apply_code(memory, ProbeResultCode.CANCELLED, 2, policy)
        self.assertEqual(memory.state, TechnicalState.UNKNOWN)
        self.assertEqual((memory.positive_streak, memory.negative_streak), (0, 0))
        self.assertEqual(decision.reason, TechnicalDecisionReason.CANCELLED_BARRIER)
        memory, _ = apply_code(memory, ProbeResultCode.TIMEOUT, 3, policy)
        self.assertEqual(memory.negative_streak, 1)

        memory = ConfirmationMemory.initial(policy.version)
        memory, _ = apply_code(memory, ProbeResultCode.SUCCESS, 1, policy)
        memory, _ = apply_code(memory, ProbeResultCode.CANCELLED, 2, policy)
        memory, _ = apply_code(memory, ProbeResultCode.SUCCESS, 3, policy)
        self.assertEqual(memory.state, TechnicalState.UNKNOWN)
        self.assertEqual(memory.positive_streak, 1)

    def test_temporal_order_is_fail_closed_and_rejections_return_same_memory(self) -> None:
        policy = make_policy()
        memory = ConfirmationMemory(
            TechnicalState.UNKNOWN,
            1,
            0,
            START_AT + timedelta(seconds=2),
            policy.version,
        )

        older, older_decision = reduce_confirmation(
            memory, make_result(ProbeResultCode.TIMEOUT, 1), policy
        )
        self.assertIs(older, memory)
        self.assertEqual(older_decision.disposition, ProcessingDisposition.OUT_OF_ORDER)
        self.assertEqual(older_decision.action, TechnicalDecisionAction.NO_CHANGE)
        self.assertEqual(older_decision.reason, TechnicalDecisionReason.OUT_OF_ORDER)

        equal, equal_decision = reduce_confirmation(
            memory, make_result(ProbeResultCode.SUCCESS, 2), policy
        )
        self.assertIs(equal, memory)
        self.assertEqual(equal_decision.disposition, ProcessingDisposition.AMBIGUOUS_ORDER)
        self.assertEqual(equal_decision.reason, TechnicalDecisionReason.AMBIGUOUS_ORDER)

        newer, newer_decision = reduce_confirmation(
            memory, make_result(ProbeResultCode.SUCCESS, 3), policy
        )
        self.assertIsNot(newer, memory)
        self.assertEqual(newer_decision.disposition, ProcessingDisposition.ACCEPTED)
        self.assertEqual(newer.last_observed_at, START_AT + timedelta(seconds=3))

    def test_policy_version_reset_does_not_reuse_pending_streak(self) -> None:
        old_policy = make_policy(version="v1")
        new_policy = make_policy(version="v2")
        memory = ConfirmationMemory.initial(old_policy.version)
        memory, _ = apply_code(memory, ProbeResultCode.SUCCESS, 1, old_policy)

        updated, decision = apply_code(memory, ProbeResultCode.SUCCESS, 2, new_policy)
        self.assertEqual(updated.state, TechnicalState.UNKNOWN)
        self.assertEqual(updated.positive_streak, 1)
        self.assertEqual(updated.policy_version, "v2")
        self.assertTrue(decision.policy_version_reset)

        online = ConfirmationMemory(
            TechnicalState.ONLINE,
            0,
            0,
            START_AT,
            old_policy.version,
        )
        updated, decision = apply_code(
            online, ProbeResultCode.AUTH_FAILURE, 1, new_policy
        )
        self.assertEqual(updated.state, TechnicalState.ONLINE)
        self.assertFalse(decision.action is TechnicalDecisionAction.CONFIRM_OFFLINE)
        self.assertTrue(decision.policy_version_reset)

        rejected, rejected_decision = reduce_confirmation(
            memory,
            make_result(ProbeResultCode.SUCCESS, 0),
            new_policy,
        )
        self.assertIs(rejected, memory)
        self.assertFalse(rejected_decision.policy_version_reset)

    def test_state_specific_canonicalization(self) -> None:
        policy = make_policy()
        online = ConfirmationMemory(
            TechnicalState.ONLINE,
            0,
            1,
            START_AT,
            policy.version,
        )
        online, _ = apply_code(online, ProbeResultCode.SUCCESS, 1, policy)
        self.assertEqual((online.positive_streak, online.negative_streak), (0, 0))

        offline = ConfirmationMemory(
            TechnicalState.OFFLINE,
            1,
            0,
            START_AT,
            policy.version,
        )
        offline, _ = apply_code(offline, ProbeResultCode.CONNECTION_REFUSED, 1, policy)
        self.assertEqual((offline.positive_streak, offline.negative_streak), (0, 0))

    def test_all_outputs_are_immutable_and_module_is_pure(self) -> None:
        policy = make_policy()
        memory = ConfirmationMemory.initial(policy.version)
        _, decision = apply_code(memory, ProbeResultCode.SUCCESS, 1, policy)
        with self.assertRaises(AttributeError):
            decision.action = TechnicalDecisionAction.CONFIRM_OFFLINE

        module = __import__("cameras.monitoramento.confirmation", fromlist=["*"])
        source = inspect.getsource(module)
        for forbidden in (
            "import django",
            "cameras.models",
            "import socket",
            "import requests",
            "import httpx",
            "import aiohttp",
            "urllib.request",
            "datetime.now",
            "time.time",
            "sleep(",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, source)


if __name__ == "__main__":
    unittest.main()
