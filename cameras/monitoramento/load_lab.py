"""Laboratório sintético local para a MON-08B.

Este módulo não é parte do runtime operacional: ele só combina contratos puros
existentes para exercitar carga, identidade e confirmação sem rede, ORM ou
persistência.
"""

import asyncio
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from ipaddress import IPv4Address
from time import perf_counter
from typing import Awaitable, Callable, Iterable

from .confirmation import (
    ConfirmationMemory,
    ConfirmationPolicy,
    TechnicalDecisionAction,
    TechnicalState,
    reduce_confirmation,
)
from .contracts import ProbeRequest, ProbeResult, ProbeResultCode
from .fakes import FakeClock, FakeProbe
from .scheduler import execute_bounded


ASSET_COUNT = 2300
CONCURRENCY = 20
_START_AT = datetime(2026, 9, 22, tzinfo=timezone.utc)


@dataclass(frozen=True, slots=True)
class LoadRound:
    """Evidência medida de uma execução sintética bounded."""

    configured_concurrency: int
    observed_max_in_flight: int
    requested_ids: frozenset[int]
    result_ids: tuple[int, ...]
    returned_ids: frozenset[int]
    missing_ids: frozenset[int]
    duplicate_count: int
    requests: int
    results: tuple[ProbeResult, ...]
    wall_clock_seconds: float

    @property
    def missing_count(self) -> int:
        return len(self.missing_ids)


@dataclass(frozen=True, slots=True)
class ConfirmationRound:
    """Evidência de confirmação derivada exclusivamente do reducer canônico."""

    load: LoadRound
    memories: dict[int, ConfirmationMemory]
    online_confirmations: int
    offline_confirmations: int


@dataclass(frozen=True, slots=True)
class ConfirmationScenario:
    """Rodadas reais do cenário, com os campos antigos voltados à rodada final."""

    rounds: tuple[ConfirmationRound, ...]

    def __post_init__(self) -> None:
        if not self.rounds:
            raise ValueError("a confirmation scenario must contain at least one round")

    @property
    def _final_round(self) -> ConfirmationRound:
        return self.rounds[-1]

    @property
    def load(self) -> LoadRound:
        return self._final_round.load

    @property
    def memories(self) -> dict[int, ConfirmationMemory]:
        return self._final_round.memories

    @property
    def online_confirmations(self) -> int:
        return self._final_round.online_confirmations

    @property
    def offline_confirmations(self) -> int:
        return self._final_round.offline_confirmations

    @property
    def round_count(self) -> int:
        return len(self.rounds)

    @property
    def total_requests(self) -> int:
        return sum(round_result.load.requests for round_result in self.rounds)

    @property
    def total_results(self) -> int:
        return sum(len(round_result.load.results) for round_result in self.rounds)

    @property
    def total_missing(self) -> int:
        return sum(round_result.load.missing_count for round_result in self.rounds)

    @property
    def total_duplicates(self) -> int:
        return sum(round_result.load.duplicate_count for round_result in self.rounds)

    @property
    def offline_confirmations_by_round(self) -> tuple[int, ...]:
        return tuple(round_result.offline_confirmations for round_result in self.rounds)


def synthetic_requests(asset_count: int = ASSET_COUNT) -> tuple[ProbeRequest, ...]:
    """Cria requests verificáveis usando apenas o bloco IPv4 de documentação."""

    if isinstance(asset_count, bool) or not isinstance(asset_count, int):
        raise TypeError("asset_count must be an integer")
    if asset_count < 0:
        raise ValueError("asset_count must be non-negative")
    return tuple(
        ProbeRequest(
            camera_id=camera_id,
            address=IPv4Address(f"198.51.100.{((camera_id - 1) % 254) + 1}"),
            port=443,
            adapter_key="synthetic",
            timeout_seconds=1.0,
            endpoint=f"/synthetic/cameras/{camera_id}",
        )
        for camera_id in range(1, asset_count + 1)
    )


async def execute_synthetic_round(
    requests: Iterable[ProbeRequest],
    code: ProbeResultCode,
    *,
    concurrency: int = CONCURRENCY,
    round_index: int = 0,
    handler: Callable[[ProbeRequest], Awaitable[ProbeResult]] | None = None,
) -> LoadRound:
    """Executa requests com o executor existente e mede somente o laboratório."""

    request_list = tuple(requests)
    if not isinstance(code, ProbeResultCode):
        raise TypeError("code must be a ProbeResultCode")
    if isinstance(round_index, bool) or not isinstance(round_index, int) or round_index < 0:
        raise ValueError("round_index must be a non-negative integer")

    in_flight = 0
    observed_max = 0
    counter_lock = asyncio.Lock()

    async def synthetic_handler(request: ProbeRequest) -> tuple[int, ProbeResult]:
        nonlocal in_flight, observed_max
        async with counter_lock:
            in_flight += 1
            observed_max = max(observed_max, in_flight)
        try:
            await asyncio.sleep(0)
            if handler is not None:
                result = await handler(request)
            else:
                observed_at = _START_AT + timedelta(
                    seconds=round_index * (len(request_list) + 1) + request.camera_id
                )
                probe = FakeProbe([code], FakeClock(start_at=observed_at))
                result = await probe.probe(request)
            return request.camera_id, result
        finally:
            async with counter_lock:
                in_flight -= 1

    started_at = perf_counter()
    completed = await execute_bounded(request_list, synthetic_handler, concurrency=concurrency)
    elapsed = perf_counter() - started_at
    requested_ids = frozenset(request.camera_id for request in request_list)
    result_ids = tuple(camera_id for camera_id, _result in completed)
    results = tuple(result for _camera_id, result in completed)
    returned_ids = frozenset(result_ids)
    return LoadRound(
        configured_concurrency=concurrency,
        observed_max_in_flight=observed_max,
        requested_ids=requested_ids,
        result_ids=result_ids,
        returned_ids=returned_ids,
        missing_ids=requested_ids - returned_ids,
        duplicate_count=len(results) - len(returned_ids),
        requests=len(request_list),
        results=results,
        wall_clock_seconds=elapsed,
    )


def apply_confirmation(
    load: LoadRound,
    policy: ConfirmationPolicy,
    memories: dict[int, ConfirmationMemory] | None = None,
) -> ConfirmationRound:
    """Aplica a confirmação existente preservando a identidade dos resultados."""

    current = {} if memories is None else dict(memories)
    online_confirmations = 0
    offline_confirmations = 0
    for camera_id, result in zip(load.result_ids, load.results, strict=True):
        memory = current.get(camera_id, ConfirmationMemory.initial(policy.version))
        updated, decision = reduce_confirmation(memory, result, policy)
        current[camera_id] = updated
        online_confirmations += decision.action is TechnicalDecisionAction.CONFIRM_ONLINE
        offline_confirmations += decision.action is TechnicalDecisionAction.CONFIRM_OFFLINE
    return ConfirmationRound(load, current, online_confirmations, offline_confirmations)


async def normal_scenario(asset_count: int = ASSET_COUNT) -> ConfirmationScenario:
    policy = ConfirmationPolicy(failures_to_offline=2, successes_to_online=1, version="mon08b")
    load = await execute_synthetic_round(synthetic_requests(asset_count), ProbeResultCode.SUCCESS)
    return ConfirmationScenario((apply_confirmation(load, policy),))


async def mass_failure_scenario(asset_count: int = ASSET_COUNT) -> ConfirmationScenario:
    policy = ConfirmationPolicy(failures_to_offline=2, successes_to_online=1, version="mon08b")
    requests = synthetic_requests(asset_count)
    initial = {request.camera_id: ConfirmationMemory(TechnicalState.ONLINE, 0, 0, None, policy.version) for request in requests}
    first = await execute_synthetic_round(requests, ProbeResultCode.CONNECTION_REFUSED, round_index=1)
    first_confirmation = apply_confirmation(first, policy, initial)
    second = await execute_synthetic_round(requests, ProbeResultCode.CONNECTION_REFUSED, round_index=2)
    second_confirmation = apply_confirmation(second, policy, first_confirmation.memories)
    return ConfirmationScenario((first_confirmation, second_confirmation))


async def mass_recovery_scenario(asset_count: int = ASSET_COUNT) -> ConfirmationScenario:
    policy = ConfirmationPolicy(failures_to_offline=2, successes_to_online=1, version="mon08b")
    requests = synthetic_requests(asset_count)
    initial = {request.camera_id: ConfirmationMemory(TechnicalState.OFFLINE, 0, 0, None, policy.version) for request in requests}
    load = await execute_synthetic_round(requests, ProbeResultCode.SUCCESS, round_index=1)
    return ConfirmationScenario((apply_confirmation(load, policy, initial),))


__all__ = [
    "ASSET_COUNT", "CONCURRENCY", "ConfirmationRound", "ConfirmationScenario", "LoadRound", "apply_confirmation",
    "execute_synthetic_round", "mass_failure_scenario", "mass_recovery_scenario",
    "normal_scenario", "synthetic_requests",
]
