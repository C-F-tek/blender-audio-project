#!/usr/bin/env python3
"""Smoke test for the heap provider invocation contract."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    from Tools.ai.heap_provider_budget_governor import (
        ProviderBudgetConfig,
        build_heap_provider_budget_governor,
    )
    from Tools.ai.heap_provider_invocation_contract import build_heap_provider_invocation_contract
    from Tools.validation._shared.report_utils import (
        resolve_output_path,
        write_json_report,
        write_text_report,
    )
except ImportError:  # pragma: no cover
    repo_root_for_import = Path(__file__).resolve().parents[3]
    if str(repo_root_for_import) not in sys.path:
        sys.path.insert(0, str(repo_root_for_import))
    from Tools.ai.heap_provider_budget_governor import (  # type: ignore
        ProviderBudgetConfig,
        build_heap_provider_budget_governor,
    )
    from Tools.ai.heap_provider_invocation_contract import (
        build_heap_provider_invocation_contract,  # type: ignore
    )
    from Tools.validation._shared.report_utils import (  # type: ignore
        resolve_output_path,
        write_json_report,
        write_text_report,
    )


def render_markdown(report: dict[str, object]) -> str:
    lines = ["# Heap Provider Invocation Contract Smoke", ""]
    lines.append(f"- Passed: `{report.get('passed')}`")
    lines.append(f"- Contract passed: `{report.get('contract_passed')}`")
    lines.append(f"- Real run allowed: `{report.get('real_run_allowed')}`")
    lines.append(f"- Required event count: `{report.get('required_event_count')}`")
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


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
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
        allow_provider_generation=False,
        operator_intent=False,
    )
    governor = build_heap_provider_budget_governor(config, requested_max_iterations=4)
    contract = build_heap_provider_invocation_contract(governor)
    telemetry = (
        contract.get("expected_telemetry_contract")
        if isinstance(contract.get("expected_telemetry_contract"), dict)
        else {}
    )
    gate = contract.get("real_run_gate") if isinstance(contract.get("real_run_gate"), dict) else {}
    required_events = (
        telemetry.get("events_required")
        if isinstance(telemetry.get("events_required"), list)
        else []
    )
    errors: list[str] = []
    if contract.get("kind") != "heap_provider_invocation_contract":
        errors.append("kind mismatch")
    if contract.get("provider_execution_performed") is not False:
        errors.append("provider execution flag must be false")
    if gate.get("real_run_allowed") is not False:
        errors.append("real run must be blocked without explicit provider permit")
    if "product_signal" not in required_events:
        errors.append("product_signal required event missing")
    report = {
        "schema_version": 1,
        "kind": "heap_provider_invocation_contract_smoke",
        "passed": not errors,
        "contract_passed": bool(contract.get("passed")),
        "real_run_allowed": gate.get("real_run_allowed"),
        "required_event_count": len(required_events),
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "errors": errors,
        "warnings": contract.get("warnings", []),
    }
    output = resolve_output_path(repo_root, args.output)
    markdown = resolve_output_path(repo_root, args.markdown_output)
    write_json_report(report, output)
    write_text_report(render_markdown(report), markdown)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
