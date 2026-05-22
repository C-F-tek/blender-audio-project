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
        "provider_semantic_missing_required_lanes": [],
        "provider_raw_response_text": "GPU1 response with source-backed product evidence.",
        "proposal_iteration_artifacts": ["output/validation/proposal_iteration_000.json"],
        "latest_proposal_quality_passed": True,
        "latest_proposal_exit_decision": "PATCHABLE_TARGET",
        "latest_gpu0_review_decision": "agree_close",
        "latest_gpu0_missing_delta_sections": [],
        "npu_micro_activity_ok": True,
        "generic_write_followup_pending_count": 0,
        "gpu0_peer_followup_pending_count": 0,
        "npu_peer_followup_pending_count": 0,
        "generic_write_document_product": {"eligible": False},
        "generic_write_refined_product": {"eligible": False},
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
    generic_ready = ready_metrics()
    generic_ready["provider_raw_response_text"] = ""
    generic_ready["response_text_complete"] = False
    generic_ready["quality_output_passed"] = False
    generic_ready["latest_proposal_quality_passed"] = False
    generic_ready["latest_proposal_reject_reason"] = "response_file_reference_quality failed"
    generic_ready["provider_revision_count"] = 3
    generic_ready["latest_gpu0_review_decision"] = "reject_until_concrete_repo_relative_delta"
    generic_ready["latest_gpu0_missing_delta_sections"] = ["TARGET_FILES"]
    generic_ready["virtual_dev_environment_passed"] = False
    generic_ready["code_execution_matrix_passed"] = False
    generic_ready["matrix_verified_target_count"] = 0
    generic_ready["concrete_code_proposal_count"] = 0
    generic_ready["runtime_debug_lab_passed"] = False
    generic_ready["generic_write_document_product"] = {
        "eligible": True,
        "kind": "generic_write_refined_product",
        "minimum_refinements": 3,
        "refinement_count": 3,
        "capture_count": 3,
        "latest_consumed_by_gpu1": True,
        "latest_refined_request": "Readable product after three refinements:\n```python\nprint('refined')\n```",
        "code_product_allowed_after_three_refinements": True,
        "patch_application_performed": False,
        "source_writes_performed": False,
    }
    generic_ready["generic_write_refined_product"] = dict(
        generic_ready["generic_write_document_product"]
    )
    generic_errors = evaluate_terminal_invariants(
        metrics=generic_ready,
        missing_requirements=[],
        lane_gate_passed=True,
        degraded_lanes=[],
        final_bridge_reports=["output/validation/broker.json"],
        allow_provider_generation=True,
        provider_execution_performed=True,
        detailed_output_expected=True,
    )
    generic_claims_patch = dict(generic_ready)
    generic_claims_patch["generic_write_refined_product"] = dict(
        generic_ready["generic_write_refined_product"]
    )
    generic_claims_patch["generic_write_refined_product"]["patch_application_performed"] = True
    generic_claims_patch_errors = evaluate_terminal_invariants(
        metrics=generic_claims_patch,
        missing_requirements=[],
        lane_gate_passed=True,
        degraded_lanes=[],
        final_bridge_reports=["output/validation/broker.json"],
        allow_provider_generation=True,
        provider_execution_performed=True,
        detailed_output_expected=True,
    )
    generic_claims_source = dict(generic_ready)
    generic_claims_source["generic_write_refined_product"] = dict(
        generic_ready["generic_write_refined_product"]
    )
    generic_claims_source["generic_write_refined_product"]["source_writes_performed"] = True
    generic_claims_source_errors = evaluate_terminal_invariants(
        metrics=generic_claims_source,
        missing_requirements=[],
        lane_gate_passed=True,
        degraded_lanes=[],
        final_bridge_reports=["output/validation/broker.json"],
        allow_provider_generation=True,
        provider_execution_performed=True,
        detailed_output_expected=True,
    )
    gpu0_followup_pending = ready_metrics()
    gpu0_followup_pending["gpu0_peer_followup_pending_count"] = 1
    gpu0_followup_errors = evaluate_terminal_invariants(
        metrics=gpu0_followup_pending,
        missing_requirements=[],
        lane_gate_passed=True,
        degraded_lanes=[],
        final_bridge_reports=["output/validation/broker.json"],
        allow_provider_generation=True,
        provider_execution_performed=True,
        detailed_output_expected=True,
    )
    npu_followup_pending = ready_metrics()
    npu_followup_pending["npu_peer_followup_pending_count"] = 1
    npu_followup_errors = evaluate_terminal_invariants(
        metrics=npu_followup_pending,
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
    if generic_errors:
        errors.append("generic_write three-refinement product produced terminal errors")
    if not any("cannot claim patch application" in error for error in generic_claims_patch_errors):
        errors.append("generic_write product must reject fake patch application claims")
    if not any("cannot claim source writes" in error for error in generic_claims_source_errors):
        errors.append("generic_write product must reject fake source write claims")
    if not any("GPU0 peer follow-up is pending" in error for error in gpu0_followup_errors):
        errors.append("ready metric set must reject pending GPU0 peer follow-up")
    if not any("NPU peer follow-up is pending" in error for error in npu_followup_errors):
        errors.append("ready metric set must reject pending NPU peer follow-up")
    required_fragments = (
        "PROVIDER_TOOL_CALLS_REMAIN_TEXT",
        "code execution matrix passed",
    )
    for fragment in required_fragments:
        if not any(fragment in error for error in bad_errors):
            errors.append(f"missing expected terminal invariant: {fragment}")
    if not any("semantic GPU0/NPU model execution" in error for error in peer_degraded_errors):
        errors.append("ready metric set must reject missing GPU0/NPU semantic execution")
    arbiter_product = (repo_root / "ia_carmine/runtime/heap_gate/arbiter_product.py").read_text(
        encoding="utf-8", errors="replace"
    )
    if "product_blocked_reason" not in arbiter_product or "npu_peer_followup_pending" not in arbiter_product:
        errors.append("arbiter product must expose peer follow-up as product blocked reason")
    if not all(error.startswith("AI STAI GIOCANDO:") for error in bad_errors):
        errors.append("terminal errors must use AI STAI GIOCANDO prefix")
    return {
        "schema_version": 1,
        "kind": "heap_gate_terminal_invariants_smoke",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "repo_root": str(repo_root),
        "passed": not errors,
        "ready_error_count": len(ok_errors),
        "generic_write_ready_error_count": len(generic_errors),
        "generic_write_claims_patch_error_count": len(generic_claims_patch_errors),
        "generic_write_claims_patch_errors": generic_claims_patch_errors,
        "generic_write_claims_source_error_count": len(generic_claims_source_errors),
        "generic_write_claims_source_errors": generic_claims_source_errors,
        "gpu0_followup_error_count": len(gpu0_followup_errors),
        "gpu0_followup_errors": gpu0_followup_errors,
        "npu_followup_error_count": len(npu_followup_errors),
        "npu_followup_errors": npu_followup_errors,
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
