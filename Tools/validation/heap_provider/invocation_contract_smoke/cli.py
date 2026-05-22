#!/usr/bin/env python3
"""Smoke test for the heap provider invocation contract."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    from ia_carmine.runtime.heap_provider.budget_governor import (
        ProviderBudgetConfig,
        build_heap_provider_budget_governor,
    )
    from ia_carmine.runtime.heap_provider.invocation_contract import build_heap_provider_invocation_contract
    from Tools.validation._shared.report_utils import (
        resolve_output_path,
        write_json_report,
        write_text_report,
    )
except ImportError:  # pragma: no cover
    repo_root_for_import = Path(__file__).resolve().parents[3]
    if str(repo_root_for_import) not in sys.path:
        sys.path.insert(0, str(repo_root_for_import))
    from ia_carmine.runtime.heap_provider.budget_governor import (  # type: ignore
        ProviderBudgetConfig,
        build_heap_provider_budget_governor,
    )
    from ia_carmine.runtime.heap_provider.invocation_contract import (
        build_heap_provider_invocation_contract,  # type: ignore
    )
from Tools.validation._shared.report_utils import (  # type: ignore
        resolve_output_path,
        write_json_report,
        write_text_report,
    )

FORBIDDEN_CONTRACT_KEYS = {
    "provider_execution_performed",
    "generation_executes_now",
    "patch_application_performed",
    "source_writes_performed",
    "persistent_memory_write_performed",
    "warnings",
    "errors",
}


def render_markdown(report: dict[str, object]) -> str:
    lines = ["# Heap Provider Invocation Contract Smoke", ""]
    lines.append(f"- Passed: `{report.get('passed')}`")
    lines.append(f"- Scenario count: `{report.get('scenario_count')}`")
    if report.get("errors"):
        lines.extend(["", "## Errors", ""])
        lines.extend(f"- {item}" for item in report.get("errors", []))
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument(
        "--output", default="output/validation/heap_provider_invocation_contract_smoke.json"
    )
    parser.add_argument(
        "--markdown-output", default="output/validation/heap_provider_invocation_contract_smoke.md"
    )
    return parser.parse_args()


def build_contract(*, allow_provider_generation: bool, operator_intent: bool) -> dict[str, object]:
    config = ProviderBudgetConfig(
        objective="smoke heap provider invocation contract",
        budget_minutes=5,
        max_rounds=4,
        files_per_round=4,
        max_context_files=40,
        max_chars_per_file=4000,
        max_new_tokens=1200,
        keep_alive="10m",
        npu_micro_start_mode="deferred",
        npu_micro_timeout_seconds=60,
        npu_final_wait_seconds=60,
        npu_max_context_chars=8000,
        npu_max_prompt_chars=1200,
        npu_max_new_tokens=384,
        allow_provider_generation=allow_provider_generation,
        operator_intent=operator_intent,
    )
    governor = build_heap_provider_budget_governor(config, requested_max_iterations=4)
    return build_heap_provider_invocation_contract(
        governor,
        allow_provider_generation=allow_provider_generation,
        operator_intent=operator_intent,
    )


def find_forbidden_keys(value: object, path: str = "contract") -> list[str]:
    if isinstance(value, dict):
        found: list[str] = []
        for key, child in value.items():
            child_path = f"{path}.{key}"
            if key in FORBIDDEN_CONTRACT_KEYS:
                found.append(child_path)
            found.extend(find_forbidden_keys(child, child_path))
        return found
    if isinstance(value, list):
        found = []
        for index, child in enumerate(value):
            found.extend(find_forbidden_keys(child, f"{path}[{index}]"))
        return found
    return []


def validate_contract(
    name: str,
    contract: dict[str, object],
    *,
    expected_allowed: bool,
    expected_passed: bool,
) -> list[str]:
    errors: list[str] = []
    evidence_events = (
        contract.get("expected_evidence_event_contract")
        if isinstance(contract.get("expected_evidence_event_contract"), dict)
        else {}
    )
    gate = contract.get("real_run_gate") if isinstance(contract.get("real_run_gate"), dict) else {}
    lane_contract = (
        contract.get("lane_activation_contract")
        if isinstance(contract.get("lane_activation_contract"), dict)
        else {}
    )
    required_events = (
        evidence_events.get("events_required")
        if isinstance(evidence_events.get("events_required"), list)
        else []
    )
    if contract.get("kind") != "heap_provider_invocation_contract":
        errors.append(f"{name}: kind mismatch")
    for item in find_forbidden_keys(contract):
        errors.append(f"{name}: contract-only report must not expose {item}")
    if bool(contract.get("passed")) is not expected_passed:
        errors.append(f"{name}: contract passed state mismatch")
    if bool(gate.get("real_run_allowed")) is not expected_allowed:
        errors.append(f"{name}: real_run_allowed mismatch")
    if "product_signal" not in required_events:
        errors.append(f"{name}: product_signal required event missing")
    lanes = {
        str(item.get("provider_lane"))
        for item in lane_contract.get("required_lanes", [])
        if isinstance(item, dict)
    }
    if lanes != {"gpu1_planner", "gpu0_peer", "npu_micro_task_auditor"}:
        errors.append(f"{name}: lane activation contract must require GPU1/GPU0/NPU")
    if lane_contract.get("start_failure_policy") != "abort_universe":
        errors.append(f"{name}: lane start failure policy must abort universe")
    return errors


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    errors: list[str] = []
    scenarios = [
        ("not_selected", build_contract(allow_provider_generation=False, operator_intent=False), False, False),
        ("selected_missing_intent", build_contract(allow_provider_generation=True, operator_intent=False), False, False),
        ("selected_allowed", build_contract(allow_provider_generation=True, operator_intent=True), True, True),
    ]
    scenario_reports = []
    for name, contract, expected_allowed, expected_passed in scenarios:
        errors.extend(
            validate_contract(
                name,
                contract,
                expected_allowed=expected_allowed,
                expected_passed=expected_passed,
            )
        )
        gate = contract.get("real_run_gate") if isinstance(contract.get("real_run_gate"), dict) else {}
        scenario_reports.append(
            {
                "name": name,
                "contract_passed": contract.get("passed"),
                "real_run_allowed": gate.get("real_run_allowed"),
                "decision": gate.get("decision"),
            }
        )
    report = {
        "schema_version": 1,
        "kind": "heap_provider_invocation_contract_smoke",
        "passed": not errors,
        "scenario_count": len(scenario_reports),
        "scenarios": scenario_reports,
    }
    if errors:
        report["errors"] = errors
    output = resolve_output_path(repo_root, args.output)
    markdown = resolve_output_path(repo_root, args.markdown_output)
    write_json_report(report, output)
    write_text_report(render_markdown(report), markdown)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
