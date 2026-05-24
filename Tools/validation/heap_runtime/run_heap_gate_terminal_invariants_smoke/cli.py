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
    from ia_carmine.runtime.heap_gate.pointer_soft_lock import pointer_closure_summary
    from Tools.validation._shared.report_utils import write_json_report
except ImportError:
    repo_root_for_import = Path(__file__).resolve().parents[4]
    if str(repo_root_for_import) not in sys.path:
        sys.path.insert(0, str(repo_root_for_import))
    from ia_carmine.runtime.heap_gate.terminal_invariants import evaluate_terminal_invariants  # type: ignore
    from ia_carmine.runtime.heap_gate.pointer_soft_lock import pointer_closure_summary  # type: ignore
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
        "budget_exhausted": False,
        "provider_lane_count": 3,
        "provider_launch_started": True,
        "pre_provider_phase": False,
        "provider_start_missing_requirements": [],
        "provider_start_unattempted_requirement": "",
        "provider_textual_tool_call_count": 0,
        "provider_native_tool_loop_requested_count": 3,
        "provider_native_tool_loop_supported_count": 3,
        "provider_native_tool_missing_lanes": [],
        "missing_provider_lanes": [],
        "provider_native_tool_unavailable_required_lanes": [],
        "provider_native_tool_missing_required_lanes": [],
        "provider_semantic_missing_required_lanes": [],
        "provider_raw_response_text_chars": len(
            "GPU1 response with source-backed product evidence."
        ),
        "proposal_iteration_artifacts": ["output/validation/proposal_iteration_000.json"],
        "gpu1_closure_decision_packet_valid": True,
        "latest_gpu1_decision": "finalize_product",
        "latest_gpu1_block_id": "smoke:proposal:000",
        "latest_gpu1_revision": "0",
        "latest_gpu1_refine_continuity": {"required": False, "passed": True, "errors": []},
        "latest_proposal_quality_passed": True,
        "latest_proposal_exit_decision": "PATCHABLE_TARGET",
        "gpu0_secondary_schema_valid": True,
        "latest_gpu0_review_decision": "congruent",
        "latest_gpu0_model_decision": "congruent",
        "latest_gpu0_effective_decision": "congruent",
        "latest_gpu0_checked_current_packet": True,
        "latest_gpu0_packet_stale_after_gpu1_packet_rewrite": False,
        "latest_gpu1_block_requires_gpu0_review": True,
        "latest_gpu1_block_reviewed_by_gpu0": True,
        "gpu0_review_invalid_requires_gpu1_retry": False,
        "latest_gpu0_role_decision": "agree_close",
        "latest_gpu0_veto_reasons": [],
        "latest_gpu0_incongruence_reasons": [],
        "latest_gpu0_free_text_used_as_product": False,
        "latest_gpu0_free_text_used_as_decision": False,
        "latest_gpu0_missing_delta_sections": [],
        "npu_micro_activity_ok": True,
        "generic_write_followup_pending_count": 0,
        "gpu0_peer_followup_pending_count": 0,
        "npu_peer_followup_pending_count": 0,
        "generic_write_capture_failed_count": 0,
        "generic_write_document_product": {"eligible": False},
        "generic_write_refined_product": {"eligible": False},
        "context_hierarchy_valid": True,
        "gpu1_replight_valid": True,
        "gpu1_primary_workload_valid": True,
        "gpu1_primary_evidence_valid": True,
        "gpu1_primary_evidence_source": "native_tool_result",
        "leader_source": "native_tool_result",
        "gpu1_native_tool_call_count": 1,
        "gpu1_boot_leader_ready": True,
        "sidecars_start_policy": "after_gpu1_residency_handshake",
        "parallel_provider_overlap_seconds": 3.5,
        "gpu1_primary_workload_chars": 1200,
        "gpu1_primary_workload_tokens": 128,
        "gpu1_leader_valid": True,
        "gpu1_consumed_gpu0_peer": True,
        "gpu1_consumed_npu_peer": True,
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
    generic_ready["provider_raw_response_text_chars"] = 0
    generic_ready["response_text_complete"] = False
    generic_ready["quality_output_passed"] = False
    generic_ready["latest_proposal_quality_passed"] = False
    generic_ready["latest_proposal_reject_reason"] = "response_file_reference_quality failed"
    generic_ready["provider_revision_count"] = 3
    generic_ready["latest_gpu0_review_decision"] = "refine_required"
    generic_ready["latest_gpu0_role_decision"] = "refine_once"
    generic_ready["latest_gpu0_veto_reasons"] = ["gpu1_delta_requires_refine_before_gpu0_congruence"]
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
    generic_capture_failed = ready_metrics()
    generic_capture_failed["generic_write_capture_failed_count"] = 1
    generic_capture_failed_errors = evaluate_terminal_invariants(
        metrics=generic_capture_failed,
        missing_requirements=[],
        lane_gate_passed=True,
        degraded_lanes=[],
        final_bridge_reports=["output/validation/broker.json"],
        allow_provider_generation=True,
        provider_execution_performed=True,
        detailed_output_expected=True,
    )
    context_invalid = ready_metrics()
    context_invalid["context_hierarchy_valid"] = False
    context_invalid_errors = evaluate_terminal_invariants(
        metrics=context_invalid,
        missing_requirements=[],
        lane_gate_passed=True,
        degraded_lanes=[],
        final_bridge_reports=["output/validation/broker.json"],
        allow_provider_generation=True,
        provider_execution_performed=True,
        detailed_output_expected=True,
    )
    gpu0_schema_invalid = ready_metrics()
    gpu0_schema_invalid["gpu0_secondary_schema_valid"] = False
    gpu0_schema_invalid_errors = evaluate_terminal_invariants(
        metrics=gpu0_schema_invalid,
        missing_requirements=[],
        lane_gate_passed=True,
        degraded_lanes=[],
        final_bridge_reports=["output/validation/broker.json"],
        allow_provider_generation=True,
        provider_execution_performed=True,
        detailed_output_expected=True,
    )
    gpu0_free_text_decision = ready_metrics()
    gpu0_free_text_decision["latest_gpu0_free_text_used_as_decision"] = True
    gpu0_free_text_decision_errors = evaluate_terminal_invariants(
        metrics=gpu0_free_text_decision,
        missing_requirements=[],
        lane_gate_passed=True,
        degraded_lanes=[],
        final_bridge_reports=["output/validation/broker.json"],
        allow_provider_generation=True,
        provider_execution_performed=True,
        detailed_output_expected=True,
    )
    gpu1_packet_missing = ready_metrics()
    gpu1_packet_missing["gpu1_closure_decision_packet_valid"] = False
    gpu1_packet_missing["gpu0_closure_agreement"] = "veto_with_reason"
    gpu1_packet_missing_errors = evaluate_terminal_invariants(
        metrics=gpu1_packet_missing,
        missing_requirements=[],
        lane_gate_passed=True,
        degraded_lanes=[],
        final_bridge_reports=["output/validation/broker.json"],
        allow_provider_generation=True,
        provider_execution_performed=True,
        detailed_output_expected=True,
    )
    gpu0_wrong_packet = ready_metrics()
    gpu0_wrong_packet["latest_gpu0_checked_current_packet"] = False
    gpu0_wrong_packet_errors = evaluate_terminal_invariants(
        metrics=gpu0_wrong_packet,
        missing_requirements=[],
        lane_gate_passed=True,
        degraded_lanes=[],
        final_bridge_reports=["output/validation/broker.json"],
        allow_provider_generation=True,
        provider_execution_performed=True,
        detailed_output_expected=True,
    )
    gpu0_stale_packet = ready_metrics()
    gpu0_stale_packet["latest_gpu0_packet_stale_after_gpu1_packet_rewrite"] = True
    gpu0_stale_packet["latest_gpu1_block_reviewed_by_gpu0"] = False
    gpu0_stale_packet_errors = evaluate_terminal_invariants(
        metrics=gpu0_stale_packet,
        missing_requirements=[],
        lane_gate_passed=True,
        degraded_lanes=[],
        final_bridge_reports=["output/validation/broker.json"],
        allow_provider_generation=True,
        provider_execution_performed=True,
        detailed_output_expected=True,
    )
    gpu0_missing_review = ready_metrics()
    gpu0_missing_review["latest_gpu1_block_reviewed_by_gpu0"] = False
    gpu0_missing_review["gpu0_review_invalid_requires_gpu1_retry"] = True
    gpu0_missing_review_errors = evaluate_terminal_invariants(
        metrics=gpu0_missing_review,
        missing_requirements=[],
        lane_gate_passed=True,
        degraded_lanes=[],
        final_bridge_reports=["output/validation/broker.json"],
        allow_provider_generation=True,
        provider_execution_performed=True,
        detailed_output_expected=True,
    )
    soft_lock_closed_refine = ready_metrics()
    soft_lock_closed_refine["soft_lock_state"] = "closed"
    soft_lock_closed_refine["closure_quorum_status"] = "targeted_refine_allowed"
    soft_lock_closed_refine_errors = evaluate_terminal_invariants(
        metrics=soft_lock_closed_refine,
        missing_requirements=[],
        lane_gate_passed=True,
        degraded_lanes=[],
        final_bridge_reports=["output/validation/broker.json"],
        allow_provider_generation=True,
        provider_execution_performed=True,
        detailed_output_expected=True,
    )
    deferred_zero_open = ready_metrics()
    deferred_zero_open["open_pointer_count_final"] = 0
    deferred_zero_open["pointer_closure_table"] = [
        {"pointer_id": "smoke:gpu0:000", "closure_status": "deferred_to_resume"}
    ]
    deferred_zero_open_errors = evaluate_terminal_invariants(
        metrics=deferred_zero_open,
        missing_requirements=[],
        lane_gate_passed=True,
        degraded_lanes=[],
        final_bridge_reports=["output/validation/broker.json"],
        allow_provider_generation=True,
        provider_execution_performed=True,
        detailed_output_expected=True,
    )
    gpu1_unlinked_refine = ready_metrics()
    gpu1_unlinked_refine["latest_gpu1_refine_continuity"] = {
        "required": True,
        "passed": False,
        "errors": [
            "gpu1_refine_not_linked_to_gpu0_veto",
            "gpu1_refine_missing_consumed_gpu0_block_id",
        ],
    }
    gpu1_unlinked_refine_errors = evaluate_terminal_invariants(
        metrics=gpu1_unlinked_refine,
        missing_requirements=[],
        lane_gate_passed=True,
        degraded_lanes=[],
        final_bridge_reports=["output/validation/broker.json"],
        allow_provider_generation=True,
        provider_execution_performed=True,
        detailed_output_expected=True,
    )
    leader_missing = ready_metrics()
    leader_missing["gpu1_leader_valid"] = False
    leader_missing_errors = evaluate_terminal_invariants(
        metrics=leader_missing,
        missing_requirements=[],
        lane_gate_passed=True,
        degraded_lanes=[],
        final_bridge_reports=["output/validation/broker.json"],
        allow_provider_generation=True,
        provider_execution_performed=True,
        detailed_output_expected=True,
    )
    primary_workload_missing = ready_metrics()
    primary_workload_missing["gpu1_primary_workload_valid"] = False
    primary_workload_missing_errors = evaluate_terminal_invariants(
        metrics=primary_workload_missing,
        missing_requirements=[],
        lane_gate_passed=True,
        degraded_lanes=[],
        final_bridge_reports=["output/validation/broker.json"],
        allow_provider_generation=True,
        provider_execution_performed=True,
        detailed_output_expected=True,
    )
    primary_evidence_missing = ready_metrics()
    primary_evidence_missing["gpu1_primary_evidence_valid"] = False
    primary_evidence_missing_errors = evaluate_terminal_invariants(
        metrics=primary_evidence_missing,
        missing_requirements=[],
        lane_gate_passed=True,
        degraded_lanes=[],
        final_bridge_reports=["output/validation/broker.json"],
        allow_provider_generation=True,
        provider_execution_performed=True,
        detailed_output_expected=True,
    )
    pre_provider_tentable = ready_metrics()
    pre_provider_tentable.update(
        {
            "product_status": "blocked_with_reason",
            "provider_lane_count": 0,
            "provider_launch_started": False,
            "pre_provider_phase": True,
            "provider_start_missing_requirements": ["runtime_file_refs"],
            "provider_start_unattempted_requirement": "runtime_file_refs",
            "budget_exhausted": False,
            "missing_provider_lanes": ["gpu0_peer", "gpu1_planner", "npu_micro_task_auditor"],
            "provider_raw_response_text_chars": 0,
            "proposal_iteration_artifacts": [],
            "gpu1_closure_decision_packet_valid": False,
            "gpu0_secondary_schema_valid": False,
            "npu_micro_activity_ok": False,
        }
    )
    pre_provider_tentable_errors = evaluate_terminal_invariants(
        metrics=pre_provider_tentable,
        missing_requirements=["runtime_file_refs"],
        lane_gate_passed=True,
        degraded_lanes=[],
        final_bridge_reports=["output/validation/broker.json"],
        allow_provider_generation=True,
        provider_execution_performed=False,
        detailed_output_expected=True,
    )
    pre_provider_exhausted = dict(pre_provider_tentable)
    pre_provider_exhausted["provider_start_unattempted_requirement"] = ""
    pre_provider_exhausted["budget_exhausted"] = True
    pre_provider_exhausted_errors = evaluate_terminal_invariants(
        metrics=pre_provider_exhausted,
        missing_requirements=["runtime_file_refs"],
        lane_gate_passed=True,
        degraded_lanes=[],
        final_bridge_reports=["output/validation/broker.json"],
        allow_provider_generation=True,
        provider_execution_performed=False,
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
    if not any("generic_write_capture_failed" in error for error in generic_capture_failed_errors):
        errors.append("ready metric set must reject failed generic_write capture")
    if not any("context_hierarchy_invalid" in error for error in context_invalid_errors):
        errors.append("ready metric set must reject invalid GPU1/GPU0/NPU context hierarchy")
    if not any("gpu0_secondary_decision_schema_invalid" in error for error in gpu0_schema_invalid_errors):
        errors.append("ready metric set must reject invalid GPU0 secondary schema")
    if not any("GPU0 free text" in error for error in gpu0_free_text_decision_errors):
        errors.append("ready metric set must reject GPU0 free text as decision/product")
    if not any("gpu1_decision_missing" in error for error in gpu1_packet_missing_errors):
        errors.append("ready metric set must reject missing GPU1 decision packet")
    if not any("gpu0_veto_not_allowed_without_gpu1_decision" in error for error in gpu1_packet_missing_errors):
        errors.append("ready metric set must reject GPU0 veto without GPU1 packet")
    if not any("gpu0_checked_wrong_gpu1_packet" in error for error in gpu0_wrong_packet_errors):
        errors.append("ready metric set must reject GPU0 checking the wrong GPU1 packet")
    if not any(
        "gpu0_review_stale_after_gpu1_packet_rewrite" in error
        for error in gpu0_stale_packet_errors
    ):
        errors.append("ready metric set must reject stale GPU0 review after GPU1 packet rewrite")
    if not any(
        "gpu0_review_invalid_requires_gpu1_retry" in error
        for error in gpu0_missing_review_errors
    ):
        errors.append("ready metric set must reject GPU1 block without a current GPU0 review")
    if not any("soft_lock_closed_with_targeted_refine_allowed" in error for error in soft_lock_closed_refine_errors):
        errors.append("terminal invariants must reject closed soft-lock with targeted refine")
    if not any("open_pointer_count_zero_with_deferred_pointer_edges" in error for error in deferred_zero_open_errors):
        errors.append("terminal invariants must reject zero open count with deferred pointer edges")
    if not any("gpu1_refine_not_linked_to_gpu0_veto" in error for error in gpu1_unlinked_refine_errors):
        errors.append("ready metric set must reject unlinked GPU1 refine after GPU0 veto")
    if not any("gpu1_leader_missing" in error for error in leader_missing_errors):
        errors.append("ready metric set must reject missing GPU1 leader")
    if not any("gpu1_primary_workload_missing" in error for error in primary_workload_missing_errors):
        errors.append("ready metric set must reject missing GPU1 primary workload")
    if not any("gpu1_native_tool_evidence_missing_when_required" in error for error in primary_evidence_missing_errors):
        errors.append("ready metric set must reject missing GPU1 primary evidence")
    if not any(
        "pre_provider_closed_with_tentable_requirement:runtime_file_refs" in error
        for error in pre_provider_tentable_errors
    ):
        errors.append("pre-provider terminal invariants must reject closure with tentable runtime_file_refs")
    if any(
        fragment in error
        for error in pre_provider_tentable_errors
        for fragment in (
            "gpu1_primary_workload_missing",
            "GPU0 secondary decision schema",
            "NPU micro-lane",
            "provider generation requires all three provider lanes",
        )
    ):
        errors.append("pre-provider terminal invariants must not emit post-provider lane errors")
    if not any(
        "runtime_file_refs_missing_before_provider_start" in error
        for error in pre_provider_exhausted_errors
    ):
        errors.append("pre-provider exhausted state must report runtime_file_refs_missing_before_provider_start")
    if any(
        fragment in error
        for error in pre_provider_exhausted_errors
        for fragment in (
            "gpu1_primary_workload_missing",
            "GPU0 secondary decision schema",
            "NPU micro-lane",
            "provider generation requires all three provider lanes",
        )
    ):
        errors.append("pre-provider exhausted state must not emit post-provider lane errors")
    required_fragments = (
        "PROVIDER_TOOL_CALLS_REMAIN_TEXT",
        "code execution matrix passed",
    )
    for fragment in required_fragments:
        if not any(fragment in error for error in bad_errors):
            errors.append(f"missing expected terminal invariant: {fragment}")
    if not any("semantic GPU0/NPU model execution" in error for error in peer_degraded_errors):
        errors.append("ready metric set must reject missing GPU0/NPU semantic execution")
    gpu0_refine_pointer = pointer_closure_summary(
        [
            {
                "id": "smoke:proposal:000",
                "role": "gpu1_planner",
                "accepted": True,
                "quality_passed": True,
                "gpu1_closure_decision_packet": {"kind": "gpu1_closure_decision_packet"},
            },
            {
                "id": "smoke:gpu0:000",
                "role": "gpu0_reviewer_refiner",
                "provider_work_verified": True,
                "gpu0_secondary_schema_valid": True,
                "gpu0_checked_current_packet": True,
                "reviewed_gpu1_block_id": "smoke:proposal:000",
                "reviewed_revision": "0",
                "review_target_pointer": "smoke:proposal:000",
                "gpu0_effective_decision": "refine_required",
                "role_decision": "refine_once",
            },
        ]
    )
    if int(gpu0_refine_pointer.get("open_pointer_count_final") or 0) <= 0:
        errors.append("pointer closure must not close a GPU1 product on GPU0 refine_required")
    gpu1_refine_status = next(
        (
            str(row.get("closure_status") or "")
            for row in gpu0_refine_pointer.get("pointer_closure_table", [])
            if row.get("pointer_id") == "smoke:proposal:000"
        ),
        "",
    )
    if gpu1_refine_status == "merged_into_final_product":
        errors.append("GPU0 refine_required must not satisfy GPU1 close-review contract")
    arbiter_product = (repo_root / "ia_carmine/runtime/heap_gate/arbiter_product.py").read_text(
        encoding="utf-8", errors="replace"
    )
    if "product_blocked_reason" not in arbiter_product or "npu_peer_followup_pending" not in arbiter_product:
        errors.append("arbiter product must expose peer follow-up as product blocked reason")
    from Tools.validation._shared.codex_failure_counters import classify_codex_failure_counters
    pre_counters = classify_codex_failure_counters(returncodes=[2], errors=pre_provider_exhausted_errors)
    gpu0_text_counters = classify_codex_failure_counters(errors=gpu0_free_text_decision_errors)
    broken_counters = classify_codex_failure_counters(errors=bad_errors)
    if pre_counters.get("script_gaming_regression_increment") or pre_counters.get("provider_start_blocker_increment") != 1:
        errors.append("runtime_file_refs provider-start blocker must not increment script-gaming")
    if gpu0_text_counters.get("script_gaming_regression_increment") != 1:
        errors.append("GPU0 free text decision must increment script-gaming")
    if broken_counters.get("product_acceptance_blocker_increment") < 1:
        errors.append("ready matrix failure must increment product acceptance blocker")
    expected_negative_groups = (
        generic_claims_patch_errors, generic_claims_source_errors, gpu0_followup_errors,
        npu_followup_errors, generic_capture_failed_errors, context_invalid_errors,
        gpu0_schema_invalid_errors, gpu0_free_text_decision_errors, gpu1_packet_missing_errors,
        gpu0_wrong_packet_errors, gpu0_stale_packet_errors, gpu0_missing_review_errors,
        soft_lock_closed_refine_errors, deferred_zero_open_errors, gpu1_unlinked_refine_errors,
        leader_missing_errors, primary_workload_missing_errors, primary_evidence_missing_errors,
        pre_provider_tentable_errors, pre_provider_exhausted_errors, bad_errors, peer_degraded_errors,
    )
    return {
        "schema_version": 1,
        "kind": "heap_gate_terminal_invariants_smoke",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "repo_root": str(repo_root),
        "passed": not errors,
        "report_semantics": "nested *_errors are expected negative fixture outputs; top-level errors/unexpected_errors are real smoke failures",
        "unexpected_error_count": len(errors),
        "unexpected_errors": errors,
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
        "generic_capture_failed_error_count": len(generic_capture_failed_errors),
        "generic_capture_failed_errors": generic_capture_failed_errors,
        "context_invalid_error_count": len(context_invalid_errors),
        "context_invalid_errors": context_invalid_errors,
        "gpu0_schema_invalid_error_count": len(gpu0_schema_invalid_errors),
        "gpu0_schema_invalid_errors": gpu0_schema_invalid_errors,
        "gpu0_free_text_decision_error_count": len(gpu0_free_text_decision_errors),
        "gpu0_free_text_decision_errors": gpu0_free_text_decision_errors,
        "gpu1_packet_missing_error_count": len(gpu1_packet_missing_errors),
        "gpu1_packet_missing_errors": gpu1_packet_missing_errors,
        "gpu0_wrong_packet_error_count": len(gpu0_wrong_packet_errors),
        "gpu0_wrong_packet_errors": gpu0_wrong_packet_errors,
        "gpu0_stale_packet_error_count": len(gpu0_stale_packet_errors),
        "gpu0_stale_packet_errors": gpu0_stale_packet_errors,
        "gpu0_missing_review_error_count": len(gpu0_missing_review_errors),
        "gpu0_missing_review_errors": gpu0_missing_review_errors,
        "soft_lock_closed_refine_error_count": len(soft_lock_closed_refine_errors),
        "soft_lock_closed_refine_errors": soft_lock_closed_refine_errors,
        "deferred_zero_open_error_count": len(deferred_zero_open_errors),
        "deferred_zero_open_errors": deferred_zero_open_errors,
        "gpu1_unlinked_refine_error_count": len(gpu1_unlinked_refine_errors),
        "gpu1_unlinked_refine_errors": gpu1_unlinked_refine_errors,
        "leader_missing_error_count": len(leader_missing_errors),
        "leader_missing_errors": leader_missing_errors,
        "primary_workload_missing_error_count": len(primary_workload_missing_errors),
        "primary_workload_missing_errors": primary_workload_missing_errors,
        "primary_evidence_missing_error_count": len(primary_evidence_missing_errors),
        "primary_evidence_missing_errors": primary_evidence_missing_errors,
        "pre_provider_tentable_error_count": len(pre_provider_tentable_errors),
        "pre_provider_tentable_errors": pre_provider_tentable_errors,
        "pre_provider_exhausted_error_count": len(pre_provider_exhausted_errors),
        "pre_provider_exhausted_errors": pre_provider_exhausted_errors,
        "broken_error_count": len(bad_errors),
        "broken_errors": bad_errors,
        "peer_degraded_error_count": len(peer_degraded_errors),
        "peer_degraded_errors": peer_degraded_errors,
        "expected_negative_fixture_error_count": sum(len(items) for items in expected_negative_groups),
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
