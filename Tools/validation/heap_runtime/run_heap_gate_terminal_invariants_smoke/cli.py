#!/usr/bin/env python3
"""Smoke test terminal heap gate invariants."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

CORE_RUNTIME_GUARD = True

try:
    from ia_carmine.runtime.heap_gate.terminal_invariants import evaluate_terminal_invariants
    from Tools.validation._shared.report_utils import write_json_report
except ImportError:
    repo_root_for_import = Path(__file__).resolve().parents[4]
    if str(repo_root_for_import) not in sys.path:
        sys.path.insert(0, str(repo_root_for_import))
    from ia_carmine.runtime.heap_gate.terminal_invariants import evaluate_terminal_invariants  # type: ignore
    from Tools.validation._shared.report_utils import write_json_report  # type: ignore


def ready_metrics() -> dict[str, Any]:
    return {
        "heap_read_count": 1,
        "heap_write_count": 1,
        "tool_request_count": 1,
        "tool_execution_count": 1,
        "decision_count": 1,
        "candidate_operation_count": 1,
        "product_status": "ready",
        "provider_lane_count": 3,
        "provider_textual_tool_call_count": 0,
        "provider_native_tool_loop_requested_count": 3,
        "provider_native_tool_loop_supported_count": 3,
        "provider_native_tool_missing_lanes": [],
        "missing_provider_lanes": [],
        "provider_native_tool_unavailable_required_lanes": [],
        "provider_native_tool_missing_required_lanes": [],
        "context_artifact_refs": ["output/validation/context.json"],
        "response_text_complete": True,
        "quality_output_passed": True,
        "virtual_dev_environment_required": True,
        "virtual_dev_environment_passed": True,
        "code_execution_matrix_required": True,
        "code_execution_matrix_passed": True,
        "patch_candidate_synthesis_required": True,
        "matrix_verified_target_count": 1,
        "concrete_code_proposal_count": 1,
        "runtime_debug_lab_required": True,
        "runtime_debug_lab_passed": True,
    }


def run_smoke(repo_root: Path) -> dict[str, Any]:
    ok_errors = evaluate_terminal_invariants(
        metrics=ready_metrics(),
        missing_requirements=[],
        lane_gate_passed=True,
        degraded_lanes=[],
        final_bridge_reports=["output/validation/broker.json"],
        allow_provider_generation=True,
        provider_execution_performed=True,
        detailed_output_expected=True,
    )
    broken = ready_metrics()
    broken["provider_textual_tool_call_count"] = 1
    broken["code_execution_matrix_passed"] = False
    broken["concrete_code_proposal_count"] = 0
    bad_errors = evaluate_terminal_invariants(
        metrics=broken,
        missing_requirements=[],
        lane_gate_passed=True,
        degraded_lanes=[],
        final_bridge_reports=["output/validation/broker.json"],
        allow_provider_generation=True,
        provider_execution_performed=True,
        detailed_output_expected=True,
    )
    peer_degraded = ready_metrics()
    peer_degraded["provider_semantic_missing_required_lanes"] = [
        "gpu0_peer",
        "npu_micro_task_auditor",
    ]
    peer_degraded_errors = evaluate_terminal_invariants(
        metrics=peer_degraded,
        missing_requirements=[],
        lane_gate_passed=True,
        degraded_lanes=[],
        final_bridge_reports=["output/validation/broker.json"],
        allow_provider_generation=True,
        provider_execution_performed=True,
        detailed_output_expected=True,
    )
    errors: list[str] = []
    if ok_errors:
        errors.append("ready metric set produced terminal errors")
    required_fragments = (
        "PROVIDER_TOOL_CALLS_REMAIN_TEXT",
        "code execution matrix passed",
    )
    for fragment in required_fragments:
        if not any(fragment in error for error in bad_errors):
            errors.append(f"missing expected terminal invariant: {fragment}")
    if not any("semantic GPU0/NPU model execution" in error for error in peer_degraded_errors):
        errors.append("ready metric set must reject missing GPU0/NPU semantic execution")
    if not all(error.startswith("AI STAI GIOCANDO:") for error in bad_errors):
        errors.append("terminal errors must use AI STAI GIOCANDO prefix")
    return {
        "schema_version": 1,
        "kind": "heap_gate_terminal_invariants_smoke",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "repo_root": str(repo_root),
        "passed": not errors,
        "ready_error_count": len(ok_errors),
        "broken_error_count": len(bad_errors),
        "broken_errors": bad_errors,
        "peer_degraded_error_count": len(peer_degraded_errors),
        "peer_degraded_errors": peer_degraded_errors,
        "errors": errors,
        "source_writes_performed": False,
        "patch_application_performed": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output", default="output/validation/heap_gate_terminal_invariants.json")
    args = parser.parse_args()
    repo_root = Path(args.repo_root).resolve()
    report = run_smoke(repo_root)
    output = Path(args.output)
    if not output.is_absolute():
        output = repo_root / output
    print(write_json_report(report, output), end="")
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
