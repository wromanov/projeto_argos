"""Testes do laboratório sintético local MON-08B."""

import asyncio
import ast
import inspect
from pathlib import Path
import unittest

from .monitoramento.confirmation import TechnicalState
from .monitoramento.contracts import ProbeResult, ProbeResultCode
from .monitoramento.load_lab import (
    ASSET_COUNT, CONCURRENCY, execute_synthetic_round,
    mass_failure_scenario, mass_recovery_scenario, normal_scenario, synthetic_requests,
)


class Mon08BLoadLabTests(unittest.IsolatedAsyncioTestCase):
    async def test_zero_assets(self) -> None:
        load = await execute_synthetic_round(synthetic_requests(0), ProbeResultCode.SUCCESS)
        self.assertEqual((load.requests, len(load.results), load.observed_max_in_flight), (0, 0, 0))

    async def test_one_asset_and_below_concurrency(self) -> None:
        for size in (1, CONCURRENCY - 1):
            with self.subTest(size=size):
                load = await execute_synthetic_round(synthetic_requests(size), ProbeResultCode.SUCCESS)
                self.assertEqual(load.missing_count, 0)
                self.assertEqual(load.duplicate_count, 0)
                self.assertLessEqual(load.observed_max_in_flight, CONCURRENCY)

    async def test_above_concurrency_and_full_envelope_are_bounded(self) -> None:
        for size in (CONCURRENCY + 1, ASSET_COUNT):
            with self.subTest(size=size):
                load = await execute_synthetic_round(synthetic_requests(size), ProbeResultCode.SUCCESS)
                self.assertEqual(load.requests, size)
                self.assertEqual(len(load.results), size)
                self.assertEqual(load.missing_count, 0)
                self.assertEqual(load.duplicate_count, 0)
                self.assertLessEqual(load.observed_max_in_flight, load.configured_concurrency)
        self.assertGreater(load.observed_max_in_flight, 1)

    async def test_normal_scenario_confirms_all_assets_online(self) -> None:
        scenario = await normal_scenario()
        self.assertEqual(scenario.online_confirmations, ASSET_COUNT)
        self.assertEqual(scenario.offline_confirmations, 0)
        self.assertTrue(all(memory.state is TechnicalState.ONLINE for memory in scenario.memories.values()))

    async def test_mass_failure_requires_two_real_reducer_rounds(self) -> None:
        scenario = await mass_failure_scenario()
        rounds = scenario.rounds
        self.assertEqual(scenario.round_count, 2)
        self.assertEqual(len(rounds), 2)

        for round_index, round_result in enumerate(rounds, start=1):
            with self.subTest(round_index=round_index):
                load = round_result.load
                self.assertEqual(load.requests, ASSET_COUNT)
                self.assertEqual(len(load.results), ASSET_COUNT)
                self.assertEqual(len(load.result_ids), ASSET_COUNT)
                self.assertEqual(load.requested_ids, frozenset(range(1, ASSET_COUNT + 1)))
                self.assertEqual(load.returned_ids, load.requested_ids)
                self.assertEqual(load.missing_count, 0)
                self.assertEqual(load.duplicate_count, 0)

        self.assertEqual(scenario.total_requests, 2 * ASSET_COUNT)
        self.assertEqual(scenario.total_results, 2 * ASSET_COUNT)
        self.assertEqual(scenario.total_missing, 0)
        self.assertEqual(scenario.total_duplicates, 0)
        self.assertEqual(scenario.offline_confirmations_by_round, (0, ASSET_COUNT))
        self.assertEqual(scenario.load.requests, ASSET_COUNT)
        self.assertEqual(scenario.offline_confirmations, ASSET_COUNT)

        first, final = rounds
        self.assertTrue(
            all(memory.state is TechnicalState.ONLINE and memory.is_suspect for memory in first.memories.values())
        )
        self.assertTrue(all(memory.state is TechnicalState.OFFLINE for memory in final.memories.values()))

    async def test_mass_recovery_confirms_online_on_first_success(self) -> None:
        scenario = await mass_recovery_scenario()
        self.assertEqual(scenario.load.requests, ASSET_COUNT)
        self.assertEqual(scenario.load.missing_count, 0)
        self.assertEqual(scenario.load.duplicate_count, 0)
        self.assertEqual(scenario.online_confirmations, ASSET_COUNT)

    async def test_handler_exception_propagates(self) -> None:
        async def failing_handler(_request: object) -> ProbeResult:
            raise RuntimeError("relevant failure")
        with self.assertRaisesRegex(RuntimeError, "relevant failure"):
            await execute_synthetic_round(synthetic_requests(1), ProbeResultCode.SUCCESS, handler=failing_handler)


class Mon08BIsolationTests(unittest.TestCase):
    def test_requests_use_documentation_addresses_and_verifiable_identity(self) -> None:
        requests = synthetic_requests(ASSET_COUNT)
        self.assertEqual({request.camera_id for request in requests}, set(range(1, ASSET_COUNT + 1)))
        self.assertTrue(all(str(request.address).startswith("198.51.100.") and request.adapter_key == "synthetic" for request in requests))

    def test_no_network_or_runtime_import_and_no_material_sleep(self) -> None:
        import cameras.monitoramento.load_lab as load_lab
        source = inspect.getsource(load_lab)
        tree = ast.parse(source)
        imported_modules = {
            alias.name.split(".")[0]
            for node in ast.walk(tree)
            if isinstance(node, ast.Import)
            for alias in node.names
        }
        imported_modules.update(
            node.module.split(".")[0]
            for node in ast.walk(tree)
            if isinstance(node, ast.ImportFrom) and node.module
        )
        self.assertTrue({"socket", "requests", "httpx", "django"}.isdisjoint(imported_modules))
        self.assertNotIn("time.sleep", source)

        asyncio_modules: set[str] = set()
        sleep_functions: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                asyncio_modules.update(
                    alias.asname or alias.name
                    for alias in node.names
                    if alias.name == "asyncio"
                )
            elif isinstance(node, ast.ImportFrom) and node.module == "asyncio":
                sleep_functions.update(
                    alias.asname or alias.name
                    for alias in node.names
                    if alias.name == "sleep"
                )

        sleep_calls = [
            node
            for node in ast.walk(tree)
            if isinstance(node, ast.Call)
            and (
                (
                    isinstance(node.func, ast.Attribute)
                    and node.func.attr == "sleep"
                    and isinstance(node.func.value, ast.Name)
                    and node.func.value.id in asyncio_modules
                )
                or (isinstance(node.func, ast.Name) and node.func.id in sleep_functions)
            )
        ]
        self.assertTrue(sleep_calls, "the lab must retain its cooperative asyncio yield")

        def numeric_literal_value(node: ast.expr) -> int | float | None:
            if isinstance(node, ast.Constant) and type(node.value) in (int, float):
                return node.value
            if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
                value = numeric_literal_value(node.operand)
                if value is not None:
                    return value if isinstance(node.op, ast.UAdd) else -value
            return None

        for call in sleep_calls:
            with self.subTest(line=call.lineno):
                if call.args:
                    delay = call.args[0]
                    self.assertFalse(any(keyword.arg == "delay" for keyword in call.keywords))
                else:
                    delay_keywords = [keyword.value for keyword in call.keywords if keyword.arg == "delay"]
                    self.assertEqual(len(delay_keywords), 1, "asyncio.sleep must have an explicit delay")
                    delay = delay_keywords[0]
                self.assertEqual(numeric_literal_value(delay), 0, "asyncio.sleep delay must be numeric zero")

    def test_operational_paths_do_not_import_load_lab(self) -> None:
        root = Path(__file__).resolve().parent
        paths = [root / "views.py", root / "apps.py", root / "__init__.py", root / "monitoramento" / "__init__.py", root / "monitoramento" / "scheduler.py", root.parent / "argos" / "settings.py"]
        for path in paths:
            if path.exists():
                with self.subTest(path=path):
                    self.assertNotIn("load_lab", path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
