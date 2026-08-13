"""Laboratório sintético amplo da confirmação e do anti-flapping MON-04C.

Este módulo exercita ``reduce_confirmation`` como uma caixa determinística:
memória + resultado + policy -> memória nova + decisão. Não há câmera,
rede, ORM, worker, relógio real ou persistência neste laboratório.
"""

from dataclasses import FrozenInstanceError, fields
from datetime import datetime, timedelta, timezone
from itertools import product
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


START_AT = datetime(2026, 8, 12, 15, 0, tzinfo=timezone.utc)
LOCAL_MINUS_THREE = timezone(timedelta(hours=-3))

ALL_CODES = (
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

NEGATIVE_CODES = (ProbeResultCode.TIMEOUT, ProbeResultCode.CONNECTION_REFUSED)
NEUTRAL_CODES = (
    ProbeResultCode.AUTH_FAILURE,
    ProbeResultCode.TLS_ERROR,
    ProbeResultCode.PROTOCOL_ERROR,
    ProbeResultCode.CONFIG_ERROR,
    ProbeResultCode.TARGET_BLOCKED,
    ProbeResultCode.INCONCLUSIVE,
)


def make_policy(
    *, failures_to_offline: int = 2, successes_to_online: int = 2, version: str = "v1"
) -> ConfirmationPolicy:
    return ConfirmationPolicy(
        failures_to_offline=failures_to_offline,
        successes_to_online=successes_to_online,
        version=version,
    )


def make_result(
    code: ProbeResultCode,
    offset_seconds: int | float,
    *,
    base: datetime = START_AT,
    display_timezone: timezone | None = None,
) -> ProbeResult:
    observed_at = base + timedelta(seconds=offset_seconds)
    if display_timezone is not None:
        observed_at = observed_at.astimezone(display_timezone)
    return ProbeResult(code=code, observed_at=observed_at, duration_seconds=0.0)


def memory_for(
    state: TechnicalState,
    *,
    positive_streak: int = 0,
    negative_streak: int = 0,
    last_observed_at: datetime | None = START_AT,
    policy_version: str = "v1",
) -> ConfirmationMemory:
    return ConfirmationMemory(
        state=state,
        positive_streak=positive_streak,
        negative_streak=negative_streak,
        last_observed_at=last_observed_at,
        policy_version=policy_version,
    )


def apply_codes(
    memory: ConfirmationMemory,
    codes: tuple[ProbeResultCode, ...] | list[ProbeResultCode],
    policy: ConfirmationPolicy,
    *,
    first_offset: int = 1,
) -> tuple[ConfirmationMemory, list[object]]:
    decisions = []
    for index, code in enumerate(codes, start=first_offset):
        memory, decision = reduce_confirmation(
            memory, make_result(code, index), policy
        )
        decisions.append(decision)
    return memory, decisions


def assert_canonical(
    testcase: unittest.TestCase,
    memory: ConfirmationMemory,
    decision: object | None = None,
) -> None:
    testcase.assertFalse(
        memory.positive_streak > 0 and memory.negative_streak > 0,
        "positive and negative streaks cannot coexist",
    )
    if memory.state is TechnicalState.ONLINE:
        testcase.assertEqual(memory.positive_streak, 0)
    if memory.state is TechnicalState.OFFLINE:
        testcase.assertEqual(memory.negative_streak, 0)
    testcase.assertEqual(
        memory.is_suspect,
        memory.positive_streak > 0 or memory.negative_streak > 0,
    )
    if decision is not None:
        testcase.assertEqual(decision.positive_streak, memory.positive_streak)
        testcase.assertEqual(decision.negative_streak, memory.negative_streak)
        testcase.assertEqual(decision.current_state, memory.state)


class ConfirmationLaboratoryTests(unittest.TestCase):
    def test_lab_covers_the_closed_contract_without_production_convenience_api(self) -> None:
        self.assertEqual(set(ProbeResultCode), set(ALL_CODES))
        confirmation_source = inspect.getsource(
            __import__(
                "cameras.monitoramento.confirmation", fromlist=["reduce_confirmation"]
            )
        )
        forbidden_contract_concepts = (
            "attempt_id",
            "sequence_id",
            "DUPLICATE",
            "STALE",
            "stale_after",
            "datetime.now",
            "time.time",
            "sleep(",
            "import django",
            "import socket",
            "import requests",
            "import httpx",
            "import aiohttp",
        )
        for concept in forbidden_contract_concepts:
            with self.subTest(concept=concept):
                self.assertNotIn(concept, confirmation_source)

        self.assertNotIn("SUSPECT", {member.name for member in TechnicalState})
        self.assertNotIn("freshness", confirmation_source.lower())
        self.assertNotIn("exit_scope", confirmation_source)
        self.assertNotIn("incident", confirmation_source.lower())
        self.assertNotIn("attempt_id", {field.name for field in fields(ProbeResult)})
        self.assertNotIn("sequence_id", {field.name for field in fields(ProbeResult)})

    def test_all_ten_probe_result_codes_have_explicit_semantic_scenarios(self) -> None:
        policy = make_policy()
        for code in ALL_CODES:
            with self.subTest(code=code):
                memory, decision = reduce_confirmation(
                    ConfirmationMemory.initial(policy.version),
                    make_result(code, 1),
                    policy,
                )
                self.assertEqual(decision.observed_code, code)
                self.assertEqual(decision.disposition, ProcessingDisposition.ACCEPTED)
                self.assertEqual(decision.action, TechnicalDecisionAction.NO_CHANGE)
                if code is ProbeResultCode.SUCCESS:
                    self.assertEqual(decision.reason, TechnicalDecisionReason.POSITIVE_EVIDENCE)
                    self.assertEqual(memory.positive_streak, 1)
                elif code in NEGATIVE_CODES:
                    self.assertEqual(decision.reason, TechnicalDecisionReason.NEGATIVE_EVIDENCE)
                    self.assertEqual(memory.negative_streak, 1)
                elif code is ProbeResultCode.CANCELLED:
                    self.assertEqual(decision.reason, TechnicalDecisionReason.CANCELLED_BARRIER)
                    self.assertEqual((memory.positive_streak, memory.negative_streak), (0, 0))
                else:
                    self.assertIn(code, NEUTRAL_CODES)
                    self.assertEqual(decision.reason, TechnicalDecisionReason.NEUTRAL_BARRIER)
                    self.assertEqual((memory.positive_streak, memory.negative_streak), (0, 0))
                assert_canonical(self, memory, decision)

    def test_positive_thresholds_confirm_exactly_once_from_unknown_and_offline(self) -> None:
        for threshold in (1, 2, 3):
            policy = make_policy(successes_to_online=threshold)
            for initial_state in (TechnicalState.UNKNOWN, TechnicalState.OFFLINE):
                with self.subTest(threshold=threshold, initial_state=initial_state):
                    memory = memory_for(initial_state)
                    actions = []
                    for step in range(1, threshold + 1):
                        memory, decision = reduce_confirmation(
                            memory, make_result(ProbeResultCode.SUCCESS, step), policy
                        )
                        actions.append(decision.action)
                        if step < threshold:
                            self.assertEqual(decision.action, TechnicalDecisionAction.NO_CHANGE)
                            self.assertEqual(memory.state, initial_state)
                            self.assertEqual(memory.positive_streak, step)
                            self.assertTrue(memory.is_suspect)
                        else:
                            self.assertEqual(decision.action, TechnicalDecisionAction.CONFIRM_ONLINE)
                            self.assertEqual(memory.state, TechnicalState.ONLINE)
                            self.assertEqual((memory.positive_streak, memory.negative_streak), (0, 0))
                        assert_canonical(self, memory, decision)

                    self.assertEqual(actions.count(TechnicalDecisionAction.CONFIRM_ONLINE), 1)
                    memory, decision = reduce_confirmation(
                        memory, make_result(ProbeResultCode.SUCCESS, threshold + 1), policy
                    )
                    self.assertEqual(memory.state, TechnicalState.ONLINE)
                    self.assertEqual(decision.action, TechnicalDecisionAction.NO_CHANGE)
                    self.assertEqual(decision.reason, TechnicalDecisionReason.STABLE_STATE_REAFFIRMED)
                    self.assertEqual((memory.positive_streak, memory.negative_streak), (0, 0))

    def test_negative_thresholds_confirm_exactly_at_two_three_or_four(self) -> None:
        for threshold in (2, 3, 4):
            policy = make_policy(failures_to_offline=threshold)
            codes = tuple(NEGATIVE_CODES[index % len(NEGATIVE_CODES)] for index in range(threshold))
            for initial_state in (TechnicalState.UNKNOWN, TechnicalState.ONLINE):
                with self.subTest(threshold=threshold, initial_state=initial_state):
                    memory = memory_for(initial_state)
                    actions = []
                    for step, code in enumerate(codes, start=1):
                        memory, decision = reduce_confirmation(
                            memory, make_result(code, step), policy
                        )
                        actions.append(decision.action)
                        if step < threshold:
                            self.assertEqual(decision.action, TechnicalDecisionAction.NO_CHANGE)
                            self.assertEqual(memory.state, initial_state)
                            self.assertEqual(memory.negative_streak, step)
                            self.assertTrue(memory.is_suspect)
                        else:
                            self.assertEqual(decision.action, TechnicalDecisionAction.CONFIRM_OFFLINE)
                            self.assertEqual(memory.state, TechnicalState.OFFLINE)
                            self.assertEqual((memory.positive_streak, memory.negative_streak), (0, 0))
                        assert_canonical(self, memory, decision)

                    self.assertEqual(actions.count(TechnicalDecisionAction.CONFIRM_OFFLINE), 1)
                    memory, decision = reduce_confirmation(
                        memory,
                        make_result(ProbeResultCode.TIMEOUT, threshold + 1),
                        policy,
                    )
                    self.assertEqual(memory.state, TechnicalState.OFFLINE)
                    self.assertEqual(decision.action, TechnicalDecisionAction.NO_CHANGE)
                    self.assertEqual(decision.reason, TechnicalDecisionReason.STABLE_STATE_REAFFIRMED)
                    self.assertEqual((memory.positive_streak, memory.negative_streak), (0, 0))

    def test_asymmetric_policies_keep_recovery_and_fall_thresholds_independent(self) -> None:
        cases = (
            (2, 1, TechnicalState.UNKNOWN, (ProbeResultCode.SUCCESS,), TechnicalState.ONLINE),
            (2, 3, TechnicalState.UNKNOWN, (ProbeResultCode.SUCCESS,) * 3, TechnicalState.ONLINE),
            (4, 2, TechnicalState.OFFLINE, (ProbeResultCode.SUCCESS,) * 2, TechnicalState.ONLINE),
        )
        for failures, successes, state, codes, expected_state in cases:
            with self.subTest(failures=failures, successes=successes, state=state):
                policy = make_policy(
                    failures_to_offline=failures,
                    successes_to_online=successes,
                )
                memory, decisions = apply_codes(memory_for(state), codes, policy)
                self.assertEqual(memory.state, expected_state)
                self.assertEqual(decisions[-1].action, TechnicalDecisionAction.CONFIRM_ONLINE)
                self.assertEqual((memory.positive_streak, memory.negative_streak), (0, 0))

        policy = make_policy(failures_to_offline=4, successes_to_online=2)
        memory, decisions = apply_codes(
            memory_for(TechnicalState.ONLINE),
            (ProbeResultCode.TIMEOUT,) * 3,
            policy,
        )
        self.assertEqual(memory.state, TechnicalState.ONLINE)
        self.assertEqual(memory.negative_streak, 3)
        self.assertTrue(all(d.action is TechnicalDecisionAction.NO_CHANGE for d in decisions))

    def test_unknown_matrix_covers_partial_confirmation_barriers_and_mixed_evidence(self) -> None:
        policy = make_policy()
        cases = (
            ((ProbeResultCode.SUCCESS,), TechnicalState.UNKNOWN, 1, 0, TechnicalDecisionReason.POSITIVE_EVIDENCE),
            ((ProbeResultCode.SUCCESS,) * 2, TechnicalState.ONLINE, 0, 0, TechnicalDecisionReason.CONFIRMED_ONLINE),
            ((ProbeResultCode.TIMEOUT,), TechnicalState.UNKNOWN, 0, 1, TechnicalDecisionReason.NEGATIVE_EVIDENCE),
            ((ProbeResultCode.TIMEOUT,) * 2, TechnicalState.OFFLINE, 0, 0, TechnicalDecisionReason.CONFIRMED_OFFLINE),
            ((ProbeResultCode.CONNECTION_REFUSED,), TechnicalState.UNKNOWN, 0, 1, TechnicalDecisionReason.NEGATIVE_EVIDENCE),
            ((ProbeResultCode.TIMEOUT, ProbeResultCode.CONNECTION_REFUSED), TechnicalState.OFFLINE, 0, 0, TechnicalDecisionReason.CONFIRMED_OFFLINE),
            ((ProbeResultCode.SUCCESS, ProbeResultCode.TIMEOUT), TechnicalState.UNKNOWN, 0, 1, TechnicalDecisionReason.NEGATIVE_EVIDENCE),
            ((ProbeResultCode.TIMEOUT, ProbeResultCode.SUCCESS), TechnicalState.UNKNOWN, 1, 0, TechnicalDecisionReason.POSITIVE_EVIDENCE),
            ((ProbeResultCode.AUTH_FAILURE,), TechnicalState.UNKNOWN, 0, 0, TechnicalDecisionReason.NEUTRAL_BARRIER),
            ((ProbeResultCode.TLS_ERROR,), TechnicalState.UNKNOWN, 0, 0, TechnicalDecisionReason.NEUTRAL_BARRIER),
            ((ProbeResultCode.PROTOCOL_ERROR,), TechnicalState.UNKNOWN, 0, 0, TechnicalDecisionReason.NEUTRAL_BARRIER),
            ((ProbeResultCode.CONFIG_ERROR,), TechnicalState.UNKNOWN, 0, 0, TechnicalDecisionReason.NEUTRAL_BARRIER),
            ((ProbeResultCode.TARGET_BLOCKED,), TechnicalState.UNKNOWN, 0, 0, TechnicalDecisionReason.NEUTRAL_BARRIER),
            ((ProbeResultCode.CANCELLED,), TechnicalState.UNKNOWN, 0, 0, TechnicalDecisionReason.CANCELLED_BARRIER),
            ((ProbeResultCode.INCONCLUSIVE,), TechnicalState.UNKNOWN, 0, 0, TechnicalDecisionReason.NEUTRAL_BARRIER),
        )
        for codes, state, positive, negative, reason in cases:
            with self.subTest(codes=codes):
                memory, decisions = apply_codes(memory_for(TechnicalState.UNKNOWN), codes, policy)
                self.assertEqual(memory.state, state)
                self.assertEqual(memory.positive_streak, positive)
                self.assertEqual(memory.negative_streak, negative)
                self.assertEqual(decisions[-1].reason, reason)
                assert_canonical(self, memory, decisions[-1])

    def test_online_to_offline_sequences_use_the_fall_threshold_and_emit_one_action(self) -> None:
        cases = (
            ((ProbeResultCode.TIMEOUT,), 2, TechnicalState.ONLINE),
            ((ProbeResultCode.TIMEOUT, ProbeResultCode.SUCCESS), 2, TechnicalState.ONLINE),
            ((ProbeResultCode.TIMEOUT, ProbeResultCode.TIMEOUT), 2, TechnicalState.OFFLINE),
            ((ProbeResultCode.CONNECTION_REFUSED, ProbeResultCode.TIMEOUT), 2, TechnicalState.OFFLINE),
            ((ProbeResultCode.TIMEOUT, ProbeResultCode.CONNECTION_REFUSED), 2, TechnicalState.OFFLINE),
            ((ProbeResultCode.TIMEOUT,) * 3, 3, TechnicalState.OFFLINE),
        )
        for codes, failures, expected_state in cases:
            with self.subTest(codes=codes, failures=failures):
                policy = make_policy(failures_to_offline=failures)
                memory, decisions = apply_codes(memory_for(TechnicalState.ONLINE), codes, policy)
                self.assertEqual(memory.state, expected_state)
                if expected_state is TechnicalState.OFFLINE:
                    self.assertEqual(
                        sum(d.action is TechnicalDecisionAction.CONFIRM_OFFLINE for d in decisions),
                        1,
                    )
                else:
                    self.assertEqual(
                        sum(d.action is TechnicalDecisionAction.CONFIRM_OFFLINE for d in decisions),
                        0,
                    )
                assert_canonical(self, memory, decisions[-1])

    def test_offline_to_online_sequences_use_the_recovery_threshold_and_emit_one_action(self) -> None:
        cases = (
            ((ProbeResultCode.SUCCESS,), 2, TechnicalState.OFFLINE),
            ((ProbeResultCode.SUCCESS, ProbeResultCode.SUCCESS), 2, TechnicalState.ONLINE),
            ((ProbeResultCode.SUCCESS, ProbeResultCode.TIMEOUT), 2, TechnicalState.OFFLINE),
            ((ProbeResultCode.SUCCESS,) * 3, 3, TechnicalState.ONLINE),
            ((ProbeResultCode.SUCCESS, ProbeResultCode.CONNECTION_REFUSED, ProbeResultCode.SUCCESS), 2, TechnicalState.OFFLINE),
        )
        for codes, successes, expected_state in cases:
            with self.subTest(codes=codes, successes=successes):
                policy = make_policy(successes_to_online=successes)
                memory, decisions = apply_codes(memory_for(TechnicalState.OFFLINE), codes, policy)
                self.assertEqual(memory.state, expected_state)
                self.assertEqual(
                    sum(d.action is TechnicalDecisionAction.CONFIRM_ONLINE for d in decisions),
                    int(expected_state is TechnicalState.ONLINE),
                )
                self.assertEqual(
                    sum(d.action is TechnicalDecisionAction.CONFIRM_OFFLINE for d in decisions), 0
                )
                assert_canonical(self, memory, decisions[-1])

    def test_flapping_does_not_create_false_transitions(self) -> None:
        policy = make_policy(failures_to_offline=2, successes_to_online=2)
        online, online_decisions = apply_codes(
            memory_for(TechnicalState.ONLINE),
            (
                ProbeResultCode.TIMEOUT,
                ProbeResultCode.SUCCESS,
                ProbeResultCode.TIMEOUT,
                ProbeResultCode.SUCCESS,
                ProbeResultCode.TIMEOUT,
                ProbeResultCode.SUCCESS,
            ),
            policy,
        )
        self.assertEqual(online.state, TechnicalState.ONLINE)
        self.assertEqual(sum(d.action is not TechnicalDecisionAction.NO_CHANGE for d in online_decisions), 0)

        offline, offline_decisions = apply_codes(
            memory_for(TechnicalState.OFFLINE),
            (
                ProbeResultCode.SUCCESS,
                ProbeResultCode.TIMEOUT,
                ProbeResultCode.SUCCESS,
                ProbeResultCode.TIMEOUT,
                ProbeResultCode.SUCCESS,
            ),
            policy,
        )
        self.assertEqual(offline.state, TechnicalState.OFFLINE)
        self.assertEqual(sum(d.action is not TechnicalDecisionAction.NO_CHANGE for d in offline_decisions), 0)

        unknown, unknown_decisions = apply_codes(
            ConfirmationMemory.initial(policy.version),
            (
                ProbeResultCode.SUCCESS,
                ProbeResultCode.TIMEOUT,
                ProbeResultCode.SUCCESS,
                ProbeResultCode.TIMEOUT,
            ),
            policy,
        )
        self.assertEqual(unknown.state, TechnicalState.UNKNOWN)
        self.assertEqual(sum(d.action is not TechnicalDecisionAction.NO_CHANGE for d in unknown_decisions), 0)
        self.assertEqual((unknown.positive_streak, unknown.negative_streak), (0, 1))

    def test_opposite_evidence_breaks_pending_streaks_in_each_applicable_state(self) -> None:
        policy = make_policy()
        scenarios = (
            (TechnicalState.UNKNOWN, 1, 0, ProbeResultCode.TIMEOUT, 0, 1),
            (TechnicalState.UNKNOWN, 0, 1, ProbeResultCode.SUCCESS, 1, 0),
            (TechnicalState.ONLINE, 0, 1, ProbeResultCode.SUCCESS, 0, 0),
            (TechnicalState.OFFLINE, 1, 0, ProbeResultCode.TIMEOUT, 0, 0),
        )
        for state, positive, negative, code, expected_positive, expected_negative in scenarios:
            with self.subTest(state=state, code=code):
                memory = memory_for(
                    state,
                    positive_streak=positive,
                    negative_streak=negative,
                )
                updated, decision = reduce_confirmation(memory, make_result(code, 1), policy)
                self.assertEqual((updated.positive_streak, updated.negative_streak), (expected_positive, expected_negative))
                self.assertEqual(decision.action, TechnicalDecisionAction.NO_CHANGE)
                assert_canonical(self, updated, decision)

    def test_every_neutral_barrier_breaks_both_directions_without_transition(self) -> None:
        policy = make_policy(failures_to_offline=2, successes_to_online=2)
        for barrier in NEUTRAL_CODES:
            with self.subTest(barrier=barrier):
                online, decisions = apply_codes(
                    memory_for(TechnicalState.ONLINE, negative_streak=1),
                    (barrier, ProbeResultCode.TIMEOUT),
                    policy,
                )
                self.assertEqual(online.state, TechnicalState.ONLINE)
                self.assertEqual(online.negative_streak, 1)
                self.assertEqual(decisions[0].reason, TechnicalDecisionReason.NEUTRAL_BARRIER)
                self.assertEqual(decisions[1].action, TechnicalDecisionAction.NO_CHANGE)

                offline, decisions = apply_codes(
                    memory_for(TechnicalState.OFFLINE, positive_streak=1),
                    (barrier, ProbeResultCode.SUCCESS),
                    policy,
                )
                self.assertEqual(offline.state, TechnicalState.OFFLINE)
                self.assertEqual(offline.positive_streak, 1)
                self.assertEqual(decisions[0].reason, TechnicalDecisionReason.NEUTRAL_BARRIER)
                self.assertEqual(decisions[1].action, TechnicalDecisionAction.NO_CHANGE)
                assert_canonical(self, offline, decisions[-1])

    def test_cancelled_is_a_strong_barrier_and_preserves_state(self) -> None:
        policy = make_policy()
        cases = (
            (TechnicalState.ONLINE, (ProbeResultCode.TIMEOUT, ProbeResultCode.CANCELLED, ProbeResultCode.TIMEOUT), 0, 1),
            (TechnicalState.OFFLINE, (ProbeResultCode.SUCCESS, ProbeResultCode.CANCELLED, ProbeResultCode.SUCCESS), 1, 0),
            (TechnicalState.UNKNOWN, (ProbeResultCode.TIMEOUT, ProbeResultCode.CANCELLED, ProbeResultCode.TIMEOUT), 0, 1),
            (TechnicalState.UNKNOWN, (ProbeResultCode.SUCCESS, ProbeResultCode.CANCELLED, ProbeResultCode.SUCCESS), 1, 0),
        )
        for state, codes, expected_positive, expected_negative in cases:
            with self.subTest(state=state, codes=codes):
                memory, decisions = apply_codes(memory_for(state), codes, policy)
                self.assertEqual(memory.state, state)
                self.assertEqual((memory.positive_streak, memory.negative_streak), (expected_positive, expected_negative))
                cancelled = decisions[1]
                self.assertEqual(cancelled.action, TechnicalDecisionAction.NO_CHANGE)
                self.assertEqual(cancelled.reason, TechnicalDecisionReason.CANCELLED_BARRIER)
                self.assertEqual(cancelled.disposition, ProcessingDisposition.ACCEPTED)
                self.assertFalse(cancelled.is_suspect)
                assert_canonical(self, memory, decisions[-1])

    def test_cancelled_and_neutral_barrier_semantics_are_checked_after_temporal_validation(self) -> None:
        policy = make_policy()
        memory = memory_for(TechnicalState.UNKNOWN, positive_streak=1, last_observed_at=START_AT + timedelta(seconds=10))
        for code in (ProbeResultCode.CANCELLED, *NEUTRAL_CODES):
            with self.subTest(code=code):
                result = make_result(code, 9)
                returned, decision = reduce_confirmation(memory, result, policy)
                self.assertIs(returned, memory)
                self.assertEqual(decision.disposition, ProcessingDisposition.OUT_OF_ORDER)
                self.assertEqual(decision.reason, TechnicalDecisionReason.OUT_OF_ORDER)
                self.assertEqual(decision.action, TechnicalDecisionAction.NO_CHANGE)
                self.assertEqual((returned.positive_streak, returned.negative_streak), (1, 0))

    def test_out_of_order_results_return_the_same_memory_for_representative_codes(self) -> None:
        policy = make_policy()
        memory = memory_for(
            TechnicalState.UNKNOWN,
            positive_streak=1,
            last_observed_at=START_AT + timedelta(seconds=10),
        )
        for code in (
            ProbeResultCode.SUCCESS,
            ProbeResultCode.TIMEOUT,
            ProbeResultCode.CANCELLED,
            ProbeResultCode.CONFIG_ERROR,
        ):
            with self.subTest(code=code):
                returned, decision = reduce_confirmation(memory, make_result(code, 9), policy)
                self.assertIs(returned, memory)
                self.assertEqual(returned.state, memory.state)
                self.assertEqual(returned.positive_streak, memory.positive_streak)
                self.assertEqual(returned.negative_streak, memory.negative_streak)
                self.assertEqual(returned.last_observed_at, memory.last_observed_at)
                self.assertEqual(decision.action, TechnicalDecisionAction.NO_CHANGE)
                self.assertEqual(decision.reason, TechnicalDecisionReason.OUT_OF_ORDER)
                self.assertEqual(decision.disposition, ProcessingDisposition.OUT_OF_ORDER)

    def test_ambiguous_order_never_invents_duplicate_semantics_and_keeps_memory(self) -> None:
        policy = make_policy()
        memory = memory_for(
            TechnicalState.ONLINE,
            negative_streak=1,
            last_observed_at=START_AT + timedelta(seconds=10),
        )
        for code in (
            ProbeResultCode.SUCCESS,
            ProbeResultCode.TIMEOUT,
            ProbeResultCode.CANCELLED,
            ProbeResultCode.AUTH_FAILURE,
        ):
            with self.subTest(code=code):
                returned, decision = reduce_confirmation(memory, make_result(code, 10), policy)
                self.assertIs(returned, memory)
                self.assertEqual(decision.disposition, ProcessingDisposition.AMBIGUOUS_ORDER)
                self.assertEqual(decision.reason, TechnicalDecisionReason.AMBIGUOUS_ORDER)
                self.assertEqual(decision.action, TechnicalDecisionAction.NO_CHANGE)
                self.assertEqual((returned.positive_streak, returned.negative_streak), (0, 1))

    def test_same_instant_with_different_timezone_is_ambiguous_after_probe_normalization(self) -> None:
        policy = make_policy()
        memory = memory_for(
            TechnicalState.UNKNOWN,
            positive_streak=1,
            last_observed_at=START_AT,
        )
        result = make_result(
            ProbeResultCode.SUCCESS,
            0,
            display_timezone=LOCAL_MINUS_THREE,
        )
        self.assertEqual(result.observed_at, START_AT)
        returned, decision = reduce_confirmation(memory, result, policy)
        self.assertIs(returned, memory)
        self.assertEqual(decision.disposition, ProcessingDisposition.AMBIGUOUS_ORDER)
        self.assertEqual(decision.reason, TechnicalDecisionReason.AMBIGUOUS_ORDER)

    def test_first_temporally_valid_observation_is_accepted_without_inventing_prior_state(self) -> None:
        policy = make_policy()
        for code in (
            ProbeResultCode.SUCCESS,
            ProbeResultCode.TIMEOUT,
            ProbeResultCode.CANCELLED,
            ProbeResultCode.AUTH_FAILURE,
        ):
            with self.subTest(code=code):
                memory, decision = reduce_confirmation(
                    ConfirmationMemory.initial(policy.version),
                    make_result(code, 1),
                    policy,
                )
                self.assertEqual(decision.disposition, ProcessingDisposition.ACCEPTED)
                self.assertEqual(decision.previous_state, TechnicalState.UNKNOWN)
                self.assertEqual(memory.last_observed_at, START_AT + timedelta(seconds=1))

    def test_watermark_is_ordering_only_and_advances_only_for_accepted_results(self) -> None:
        policy = make_policy()
        initial = memory_for(TechnicalState.UNKNOWN, positive_streak=1)
        accepted, decision = reduce_confirmation(initial, make_result(ProbeResultCode.SUCCESS, 1), policy)
        self.assertEqual(decision.disposition, ProcessingDisposition.ACCEPTED)
        self.assertEqual(accepted.last_observed_at, START_AT + timedelta(seconds=1))

        rejected_old, old_decision = reduce_confirmation(
            accepted, make_result(ProbeResultCode.TIMEOUT, 0), policy
        )
        self.assertIs(rejected_old, accepted)
        self.assertEqual(old_decision.disposition, ProcessingDisposition.OUT_OF_ORDER)
        self.assertEqual(rejected_old.last_observed_at, START_AT + timedelta(seconds=1))

        rejected_equal, equal_decision = reduce_confirmation(
            accepted, make_result(ProbeResultCode.TIMEOUT, 1), policy
        )
        self.assertIs(rejected_equal, accepted)
        self.assertEqual(equal_decision.disposition, ProcessingDisposition.AMBIGUOUS_ORDER)
        self.assertEqual(rejected_equal.last_observed_at, START_AT + timedelta(seconds=1))

        barrier, barrier_decision = reduce_confirmation(
            accepted, make_result(ProbeResultCode.AUTH_FAILURE, 2), policy
        )
        self.assertEqual(barrier_decision.disposition, ProcessingDisposition.ACCEPTED)
        self.assertEqual(barrier.last_observed_at, START_AT + timedelta(seconds=2))
        cancelled, cancelled_decision = reduce_confirmation(
            barrier, make_result(ProbeResultCode.CANCELLED, 3), policy
        )
        self.assertEqual(cancelled_decision.disposition, ProcessingDisposition.ACCEPTED)
        self.assertEqual(cancelled.last_observed_at, START_AT + timedelta(seconds=3))
        self.assertEqual(cancelled.last_observed_at, cancelled_decision.observed_at)

    def test_policy_version_change_discards_old_positive_negative_and_barrier_streaks(self) -> None:
        old = make_policy(version="v1")
        new = make_policy(version="v2")
        scenarios = (
            (TechnicalState.UNKNOWN, 1, 0, ProbeResultCode.SUCCESS, 1),
            (TechnicalState.ONLINE, 0, 1, ProbeResultCode.TIMEOUT, 1),
            (TechnicalState.OFFLINE, 1, 0, ProbeResultCode.SUCCESS, 1),
        )
        for state, positive, negative, code, expected_streak in scenarios:
            with self.subTest(state=state, code=code):
                memory = memory_for(
                    state,
                    positive_streak=positive,
                    negative_streak=negative,
                    policy_version=old.version,
                )
                updated, decision = reduce_confirmation(
                    memory, make_result(code, 1), new
                )
                self.assertTrue(decision.policy_version_reset)
                self.assertEqual(updated.policy_version, new.version)
                if code is ProbeResultCode.SUCCESS:
                    self.assertEqual(updated.positive_streak, expected_streak)
                else:
                    self.assertEqual(updated.negative_streak, expected_streak)
                self.assertEqual(updated.state, state if state is not TechnicalState.UNKNOWN else TechnicalState.UNKNOWN)
                assert_canonical(self, updated, decision)

        for code, reason in (
            (ProbeResultCode.AUTH_FAILURE, TechnicalDecisionReason.NEUTRAL_BARRIER),
            (ProbeResultCode.CANCELLED, TechnicalDecisionReason.CANCELLED_BARRIER),
        ):
            with self.subTest(code=code):
                memory = memory_for(
                    TechnicalState.UNKNOWN,
                    positive_streak=1,
                    policy_version=old.version,
                )
                updated, decision = reduce_confirmation(memory, make_result(code, 1), new)
                self.assertTrue(decision.policy_version_reset)
                self.assertEqual(decision.reason, reason)
                self.assertEqual((updated.positive_streak, updated.negative_streak), (0, 0))

    def test_temporal_rejection_precedes_policy_version_reset(self) -> None:
        old = make_policy(version="v1")
        new = make_policy(version="v2")
        memory = memory_for(
            TechnicalState.UNKNOWN,
            positive_streak=1,
            last_observed_at=START_AT + timedelta(seconds=10),
            policy_version=old.version,
        )
        returned, decision = reduce_confirmation(memory, make_result(ProbeResultCode.SUCCESS, 9), new)
        self.assertIs(returned, memory)
        self.assertEqual(returned.policy_version, old.version)
        self.assertFalse(decision.policy_version_reset)
        self.assertEqual(decision.disposition, ProcessingDisposition.OUT_OF_ORDER)
        self.assertEqual(decision.reason, TechnicalDecisionReason.OUT_OF_ORDER)

    def test_new_policy_applies_to_the_current_result_after_reset(self) -> None:
        old = make_policy(version="v1", successes_to_online=3, failures_to_offline=4)
        new = make_policy(version="v2", successes_to_online=1, failures_to_offline=2)

        for state in (TechnicalState.UNKNOWN, TechnicalState.OFFLINE):
            with self.subTest(state=state):
                memory = memory_for(state, positive_streak=1, policy_version=old.version)
                updated, decision = reduce_confirmation(memory, make_result(ProbeResultCode.SUCCESS, 1), new)
                self.assertEqual(updated.state, TechnicalState.ONLINE)
                self.assertEqual(decision.action, TechnicalDecisionAction.CONFIRM_ONLINE)
                self.assertTrue(decision.policy_version_reset)

        memory = memory_for(TechnicalState.ONLINE, negative_streak=1, policy_version=old.version)
        updated, decision = reduce_confirmation(memory, make_result(ProbeResultCode.TIMEOUT, 1), new)
        self.assertEqual(updated.state, TechnicalState.ONLINE)
        self.assertEqual(updated.negative_streak, 1)
        self.assertEqual(decision.action, TechnicalDecisionAction.NO_CHANGE)
        self.assertTrue(decision.policy_version_reset)

    def test_canonicalization_and_suspect_are_checked_after_each_replayed_step(self) -> None:
        policy = make_policy()
        starting_memories = (
            memory_for(TechnicalState.UNKNOWN),
            memory_for(TechnicalState.ONLINE),
            memory_for(TechnicalState.OFFLINE),
        )
        sequences = (
            (ProbeResultCode.SUCCESS, ProbeResultCode.TIMEOUT, ProbeResultCode.SUCCESS),
            (ProbeResultCode.TIMEOUT, ProbeResultCode.SUCCESS, ProbeResultCode.TIMEOUT),
            (ProbeResultCode.AUTH_FAILURE, ProbeResultCode.CANCELLED, ProbeResultCode.SUCCESS),
        )
        for starting in starting_memories:
            for sequence in sequences:
                with self.subTest(starting=starting.state, sequence=sequence):
                    memory = starting
                    for offset, code in enumerate(sequence, start=1):
                        memory, decision = reduce_confirmation(
                            memory, make_result(code, offset), policy
                        )
                        assert_canonical(self, memory, decision)
                        self.assertFalse(
                            memory.positive_streak > 0 and memory.negative_streak > 0
                        )

    def test_actions_and_reasons_are_transitions_not_repeated_state_notifications(self) -> None:
        policy = make_policy()
        memory = ConfirmationMemory.initial(policy.version)
        memory, decision = reduce_confirmation(memory, make_result(ProbeResultCode.SUCCESS, 1), policy)
        self.assertEqual(decision.action, TechnicalDecisionAction.NO_CHANGE)
        self.assertEqual(decision.reason, TechnicalDecisionReason.POSITIVE_EVIDENCE)
        memory, decision = reduce_confirmation(memory, make_result(ProbeResultCode.SUCCESS, 2), policy)
        self.assertEqual(decision.action, TechnicalDecisionAction.CONFIRM_ONLINE)
        self.assertEqual(decision.reason, TechnicalDecisionReason.CONFIRMED_ONLINE)
        memory, decision = reduce_confirmation(memory, make_result(ProbeResultCode.SUCCESS, 3), policy)
        self.assertEqual(decision.action, TechnicalDecisionAction.NO_CHANGE)
        self.assertEqual(decision.reason, TechnicalDecisionReason.STABLE_STATE_REAFFIRMED)

        memory, decision = reduce_confirmation(memory, make_result(ProbeResultCode.TIMEOUT, 4), policy)
        self.assertEqual(decision.action, TechnicalDecisionAction.NO_CHANGE)
        memory, decision = reduce_confirmation(memory, make_result(ProbeResultCode.TIMEOUT, 5), policy)
        self.assertEqual(decision.action, TechnicalDecisionAction.CONFIRM_OFFLINE)
        self.assertEqual(decision.reason, TechnicalDecisionReason.CONFIRMED_OFFLINE)
        memory, decision = reduce_confirmation(memory, make_result(ProbeResultCode.TIMEOUT, 6), policy)
        self.assertEqual(decision.action, TechnicalDecisionAction.NO_CHANGE)
        self.assertEqual(decision.reason, TechnicalDecisionReason.STABLE_STATE_REAFFIRMED)

    def test_memory_policy_decision_and_probe_are_immutable_and_reductions_do_not_mutate_input(self) -> None:
        policy = make_policy()
        memory = memory_for(TechnicalState.UNKNOWN, positive_streak=1)
        result = make_result(ProbeResultCode.SUCCESS, 1)
        original_memory = memory
        updated, decision = reduce_confirmation(memory, result, policy)
        self.assertIsNot(updated, original_memory)
        self.assertEqual(original_memory.state, TechnicalState.UNKNOWN)
        self.assertEqual(original_memory.positive_streak, 1)
        self.assertEqual(original_memory.last_observed_at, START_AT)
        with self.assertRaises((FrozenInstanceError, AttributeError)):
            policy.version = "v2"  # type: ignore[misc]
        with self.assertRaises((FrozenInstanceError, AttributeError)):
            decision.action = TechnicalDecisionAction.CONFIRM_OFFLINE  # type: ignore[misc]
        with self.assertRaises((FrozenInstanceError, AttributeError)):
            result.code = ProbeResultCode.TIMEOUT  # type: ignore[misc]

        rejected, rejected_decision = reduce_confirmation(
            updated, make_result(ProbeResultCode.TIMEOUT, 0), policy
        )
        self.assertIs(rejected, updated)
        self.assertEqual(rejected_decision.action, TechnicalDecisionAction.NO_CHANGE)

    def test_same_inputs_are_deterministic_and_replay_trajectories_are_equivalent(self) -> None:
        policy_one = make_policy(failures_to_offline=3, successes_to_online=2)
        policy_two = make_policy(failures_to_offline=3, successes_to_online=2)
        codes = (
            ProbeResultCode.SUCCESS,
            ProbeResultCode.TIMEOUT,
            ProbeResultCode.TIMEOUT,
            ProbeResultCode.CANCELLED,
            ProbeResultCode.SUCCESS,
            ProbeResultCode.SUCCESS,
        )

        def replay(policy: ConfirmationPolicy) -> tuple[ConfirmationMemory, tuple[object, ...]]:
            memory = ConfirmationMemory.initial(policy.version)
            trajectory = []
            for offset, code in enumerate(codes, start=1):
                memory, decision = reduce_confirmation(
                    memory, make_result(code, offset), policy
                )
                trajectory.append(decision)
            return memory, tuple(trajectory)

        final_one, trajectory_one = replay(policy_one)
        final_two, trajectory_two = replay(policy_two)
        self.assertEqual(final_one, final_two)
        self.assertEqual(trajectory_one, trajectory_two)
        self.assertEqual(final_one.state, TechnicalState.ONLINE)

    def test_long_sequences_remain_canonical_deterministic_and_do_not_explode_actions(self) -> None:
        policy = make_policy(failures_to_offline=3, successes_to_online=3)
        online, decisions = apply_codes(
            memory_for(TechnicalState.ONLINE),
            (ProbeResultCode.SUCCESS,) * 50,
            policy,
        )
        self.assertEqual(online.state, TechnicalState.ONLINE)
        self.assertEqual(sum(d.action is not TechnicalDecisionAction.NO_CHANGE for d in decisions), 0)

        offline, decisions = apply_codes(
            memory_for(TechnicalState.OFFLINE),
            (ProbeResultCode.TIMEOUT,) * 50,
            policy,
        )
        self.assertEqual(offline.state, TechnicalState.OFFLINE)
        self.assertEqual(sum(d.action is not TechnicalDecisionAction.NO_CHANGE for d in decisions), 0)

        alternating = tuple(
            ProbeResultCode.SUCCESS if index % 2 == 0 else ProbeResultCode.TIMEOUT
            for index in range(100)
        )
        final, decisions = apply_codes(memory_for(TechnicalState.ONLINE), alternating, policy)
        self.assertEqual(final.state, TechnicalState.ONLINE)
        self.assertEqual(sum(d.action is not TechnicalDecisionAction.NO_CHANGE for d in decisions), 0)
        memory, decisions = apply_codes(
            memory_for(TechnicalState.UNKNOWN),
            tuple(
                code
                for index in range(1, 51)
                for code in (
                    ProbeResultCode.TIMEOUT,
                    ProbeResultCode.INCONCLUSIVE,
                    ProbeResultCode.SUCCESS,
                )
            ),
            policy,
        )
        self.assertEqual(memory.state, TechnicalState.UNKNOWN)
        self.assertTrue(all(d.disposition is ProcessingDisposition.ACCEPTED for d in decisions))
        assert_canonical(self, memory, decisions[-1])

    def test_small_exhaustive_sequences_preserve_invariants(self) -> None:
        policy = make_policy(failures_to_offline=3, successes_to_online=2)
        subset = (
            ProbeResultCode.SUCCESS,
            ProbeResultCode.TIMEOUT,
            ProbeResultCode.CANCELLED,
            ProbeResultCode.INCONCLUSIVE,
        )
        examined = 0
        for sequence in product(subset, repeat=4):
            memory = ConfirmationMemory.initial(policy.version)
            for offset, code in enumerate(sequence, start=1):
                memory, decision = reduce_confirmation(
                    memory, make_result(code, offset), policy
                )
                self.assertEqual(decision.disposition, ProcessingDisposition.ACCEPTED)
                assert_canonical(self, memory, decision)
            examined += 1
        self.assertEqual(examined, len(subset) ** 4)

    def test_independent_memories_have_no_shared_state_for_conceptual_targets(self) -> None:
        policy = make_policy()
        memories = [ConfirmationMemory.initial(policy.version) for _ in range(2300)]
        for index, memory in enumerate(memories, start=1):
            updated, decision = reduce_confirmation(
                memory,
                make_result(
                    ProbeResultCode.SUCCESS if index % 2 else ProbeResultCode.TIMEOUT,
                    1,
                ),
                policy,
            )
            self.assertIsNot(updated, memory)
            assert_canonical(self, updated, decision)

        first, _ = reduce_confirmation(
            memories[0], make_result(ProbeResultCode.SUCCESS, 1), policy
        )
        second, _ = reduce_confirmation(
            memories[1], make_result(ProbeResultCode.TIMEOUT, 1), policy
        )
        self.assertEqual(first.positive_streak, 1)
        self.assertEqual(first.negative_streak, 0)
        self.assertEqual(second.positive_streak, 0)
        self.assertEqual(second.negative_streak, 1)
        self.assertEqual(memories[2], ConfirmationMemory.initial(policy.version))


if __name__ == "__main__":
    unittest.main()
