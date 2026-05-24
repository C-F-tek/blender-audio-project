"""Terminal product invariants for the heap completeness gate."""

from __future__ import annotations

from typing import Any


def safe_int(value: Any) -> int:
    try:
        return int(value or 0)
    except (TypeError, ValueError):
        return 0


def safe_float(value: Any) -> float:
    try:
        return float(value or 0.0)
    except (TypeError, ValueError):
        return 0.0


def prefixed_errors(errors: list[str]) -> list[str]:
    return [
        error if str(error).startswith("AI STAI GIOCANDO:") else f"AI STAI GIOCANDO: {error}"
        for error in errors
    ]


def evaluate_terminal_invariants(
    *,
    metrics: dict[str, Any],
    missing_requirements: list[str],
    lane_gate_passed: bool,
    degraded_lanes: list[str],
    final_bridge_reports: list[str],
    allow_provider_generation: bool,
    provider_execution_performed: bool,
    detailed_output_expected: bool,
) -> list[str]:
    errors: list[str] = []
    for key in (
        "heap_read_count",
        "heap_write_count",
        "tool_request_count",
        "tool_execution_count",
        "decision_count",
        "candidate_operation_count",
    ):
        if safe_int(metrics.get(key)) <= 0:
            errors.append(f"{key} must be >0")
    if metrics.get("product_status") not in {"ready", "blocked_with_reason"}:
        errors.append("product_status must be ready or blocked_with_reason")
    generic_product = metrics.get("generic_write_refined_product") or metrics.get(
        "generic_write_document_product"
    )
    generic_product = generic_product if isinstance(generic_product, dict) else {}
    generic_product_ready = bool(generic_product.get("eligible"))
    generic_write_capture_failed_count = safe_int(
        metrics.get("generic_write_capture_failed_count")
        or generic_product.get("generic_write_capture_failed_count")
    )
    provider_start_missing = [
        str(item)
        for item in (metrics.get("provider_start_missing_requirements") or [])
        if str(item).strip()
    ]
    provider_start_unattempted = str(
        metrics.get("provider_start_unattempted_requirement") or ""
    ).strip()
    provider_launch_started = bool(metrics.get("provider_launch_started"))
    pre_provider = bool(
        allow_provider_generation
        and not provider_execution_performed
        and not provider_launch_started
        and safe_int(metrics.get("provider_lane_count")) <= 0
    )
    budget_exhausted = bool(metrics.get("budget_exhausted"))
    soft_close_sampled_exit = bool(
        metrics.get("soft_close_reached")
        and metrics.get("product_status") == "blocked_with_reason"
    )
    if pre_provider:
        if metrics.get("product_status") == "ready":
            errors.append("ready product_status is forbidden before provider start")
        if provider_start_unattempted and not budget_exhausted:
            errors.append(
                "pre_provider_closed_with_tentable_requirement:"
                + provider_start_unattempted
            )
        elif "runtime_file_refs" in provider_start_missing:
            errors.append("runtime_file_refs_missing_before_provider_start")
        elif provider_start_missing:
            errors.append(
                "provider_start_requirements_missing_before_provider_start:"
                + ",".join(provider_start_missing)
            )
    if allow_provider_generation and not pre_provider and generic_write_capture_failed_count > 0:
        errors.append(
            "generic_write_capture_failed: provider prose/MD evidence channel failed before producing valid JSON/Markdown capture"
        )
    if allow_provider_generation and not pre_provider and metrics.get("context_hierarchy_valid") is not True:
        errors.append(
            "context_hierarchy_invalid: GPU1 must have the largest context, GPU0 a smaller coworker context, and NPU a short micro-task context"
        )
    if allow_provider_generation and not pre_provider and metrics.get("gpu1_primary_workload_valid") is not True:
        errors.append(
            "gpu1_primary_workload_missing: GPU1 primary cannot be proven by replight, handshake, or report existence"
        )
    if allow_provider_generation and not pre_provider and metrics.get("gpu1_primary_evidence_valid") is not True:
        errors.append(
            "gpu1_primary_evidence_missing: GPU1 leader requires brokered API-native tool evidence; generic_write prose is raw text evidence only"
        )
    if (
        allow_provider_generation
        and not pre_provider
        and metrics.get("leader_source") == "native_tool_result"
        and safe_int(metrics.get("gpu1_native_tool_call_count")) <= 0
    ):
        errors.append(
            "gpu1_native_tool_result_invalid: leader_source cannot be native_tool_result when GPU1 native_tool_call_count is 0"
        )
    if (
        allow_provider_generation
        and not pre_provider
        and metrics.get("sidecars_start_policy") == "after_gpu1_residency_handshake"
        and safe_float(metrics.get("parallel_provider_overlap_seconds")) <= 0
        and metrics.get("gpu1_boot_leader_ready") is True
    ):
        errors.append(
            "parallelism_lost_by_serial_leader_gate: GPU0/NPU did not overlap with the GPU1 primary lane"
        )
    if allow_provider_generation and not pre_provider and metrics.get("gpu1_leader_valid") is not True:
        errors.append(
            "gpu1_leader_missing: GPU0/NPU sidecar evidence requires a prior valid GPU1 leader packet/proposal"
        )
    if allow_provider_generation and not pre_provider:
        if (
            metrics.get("soft_lock_state") == "closed"
            and metrics.get("closure_quorum_status") == "targeted_refine_allowed"
        ):
            errors.append("soft_lock_closed_with_targeted_refine_allowed")
        pointer_rows = metrics.get("pointer_closure_table")
        pointer_rows = pointer_rows if isinstance(pointer_rows, list) else []
        if safe_int(metrics.get("open_pointer_count_final")) <= 0 and any(
            isinstance(row, dict) and row.get("closure_status") == "deferred_to_resume"
            for row in pointer_rows
        ):
            errors.append("open_pointer_count_zero_with_deferred_pointer_edges")
    if allow_provider_generation and not pre_provider and detailed_output_expected:
        if metrics.get("product_status") != "ready":
            if not soft_close_sampled_exit:
                errors.append(
                    "complete provider product run cannot pass without ready product; "
                    f"product_status={metrics.get('product_status')}"
                )
        if safe_int(metrics.get("provider_raw_response_text_chars")) <= 0 and not generic_product_ready:
            errors.append("GPU1 primary center produced no provider response text")
        if not metrics.get("proposal_iteration_artifacts"):
            errors.append("provider product run requires GPU1 proposal/pointer iteration artifacts")
        if soft_close_sampled_exit:
            return prefixed_errors(errors)
        if (
            metrics.get("gpu1_closure_decision_packet_valid") is not True
            and not generic_product_ready
        ):
            errors.append(
                "gpu1_decision_missing: GPU1 provider work requires a valid gpu1_closure_decision_packet before GPU0 quorum"
            )
        if (
            metrics.get("gpu0_closure_agreement") == "veto_with_reason"
            and metrics.get("gpu1_closure_decision_packet_valid") is not True
            and not generic_product_ready
        ):
            errors.append("gpu0_veto_not_allowed_without_gpu1_decision")
        if metrics.get("quality_output_passed") is not True and not generic_product_ready:
            errors.append(
                "GPU1/pointer proposal quality failed; provider prose cannot pass as product"
            )
        if metrics.get("provider_recovery_required") and not generic_product_ready:
            if not metrics.get("provider_recovery_attempted") and not metrics.get(
                "provider_revision_budget_exhausted"
            ):
                errors.append("gpu1_recovery_revision_missing_after_sidecar_join")
            if metrics.get("product_status") == "ready":
                errors.append("ready product_status is forbidden while provider recovery edges are pending")
        if metrics.get("latest_proposal_quality_passed") is False and not generic_product_ready:
            errors.append(
                "latest proposal iteration was rejected by same-heap quality gate: "
                + str(metrics.get("latest_proposal_reject_reason") or "")
            )
            if (
                safe_int(metrics.get("provider_revision_count")) <= 0
                and str(metrics.get("latest_proposal_exit_decision") or "").upper()
                != "NO_PATCHABLE_TARGET"
            ):
                errors.append(
                    "rejected GPU1 proposal did not trigger mandatory provider revision retry"
                )
        if metrics.get("gpu0_secondary_schema_valid") is not True and not generic_product_ready:
            errors.append(
                "GPU0 secondary decision schema is invalid or missing; free text cannot drive veto/congruence"
            )
        if (
            metrics.get("gpu0_secondary_schema_valid") is True
            and metrics.get("latest_gpu0_checked_current_packet") is not True
            and not generic_product_ready
        ):
            errors.append("gpu0_checked_wrong_gpu1_packet")
        if (
            metrics.get("latest_gpu0_packet_stale_after_gpu1_packet_rewrite") is True
            and not generic_product_ready
        ):
            errors.append("gpu0_review_stale_after_gpu1_packet_rewrite")
        if (
            metrics.get("latest_gpu1_block_requires_gpu0_review") is True
            and metrics.get("latest_gpu1_block_reviewed_by_gpu0") is not True
            and not generic_product_ready
        ):
            errors.append("gpu0_review_invalid_requires_gpu1_retry")
        if (
            metrics.get("latest_gpu0_free_text_used_as_product")
            or metrics.get("latest_gpu0_free_text_used_as_decision")
        ) and not generic_product_ready:
            errors.append("GPU0 free text was used as product or decision")
        gpu0_decision = str(metrics.get("latest_gpu0_review_decision") or "")
        if gpu0_decision in {"veto", "refine_required", "incongruent"} and not generic_product_ready:
            errors.append(f"GPU0 structured secondary decision blocks current GPU1 delta: {gpu0_decision}")
        if (
            metrics.get("product_status") == "ready"
            and gpu0_decision != "congruent"
            and not generic_product_ready
        ):
            errors.append("ready product_status requires GPU0 structured decision congruent")
        missing_sections = metrics.get("latest_gpu0_missing_delta_sections") or []
        if missing_sections and not generic_product_ready:
            errors.append(
                "GPU1 delta is missing required pointer/product sections: "
                + ",".join(str(item) for item in missing_sections)
            )
        continuity = metrics.get("latest_gpu1_refine_continuity")
        continuity = continuity if isinstance(continuity, dict) else {}
        if continuity.get("required") and not continuity.get("passed") and not generic_product_ready:
            errors.append(
                "gpu1_refine_not_linked_to_gpu0_veto: "
                + ",".join(str(item) for item in continuity.get("errors") or [])
            )
        if not metrics.get("npu_micro_activity_ok"):
            errors.append("NPU micro-lane did not produce valid micro/audit evidence")
    if not lane_gate_passed:
        errors.append(
            "runtime state contains unviable lanes; degraded/unavailable lanes cannot pass complete/full mode: "
            + ",".join(degraded_lanes)
        )
    if metrics.get("product_status") == "ready" and missing_requirements:
        errors.append("ready product_status is forbidden while requirements are missing")
    if (
        metrics.get("product_status") == "ready"
        and safe_int(metrics.get("generic_write_followup_pending_count")) > 0
    ):
        errors.append("ready product_status is forbidden while generic_write follow-up is pending")
    if (
        metrics.get("product_status") == "ready"
        and safe_int(metrics.get("gpu0_peer_followup_pending_count")) > 0
    ):
        errors.append("ready product_status is forbidden while GPU0 peer follow-up is pending")
    if (
        metrics.get("product_status") == "ready"
        and safe_int(metrics.get("npu_peer_followup_pending_count")) > 0
    ):
        errors.append("ready product_status is forbidden while NPU peer follow-up is pending")
    if (
        metrics.get("product_status") == "ready"
        and (
            safe_int(metrics.get("gpu0_peer_followup_pending_count")) > 0
            or safe_int(metrics.get("npu_peer_followup_pending_count")) > 0
        )
    ):
        errors.append(
            "gpu1_leader_not_consuming_peer_evidence: ready product requires a later GPU1 block that consumes GPU0/NPU peer evidence"
        )
    if metrics.get("product_status") == "ready" and generic_product.get("eligible"):
        if safe_int(generic_product.get("refinement_count")) < safe_int(
            generic_product.get("minimum_refinements")
        ):
            errors.append("generic_write refined product requires the configured minimum refinements")
        if generic_product.get("patch_application_performed"):
            errors.append("generic_write refined product cannot claim patch application")
        if generic_product.get("source_writes_performed"):
            errors.append("generic_write refined product cannot claim source writes")
    if allow_provider_generation and not pre_provider and metrics.get("missing_provider_lanes"):
        errors.append(
            "provider generation requires all three provider lanes; missing: "
            + ",".join(metrics.get("missing_provider_lanes") or [])
        )
    if allow_provider_generation and not pre_provider and metrics.get("provider_native_tool_unavailable_required_lanes"):
        errors.append(
            "provider generation requested a native tool call on unavailable provider lanes: "
            + ",".join(metrics.get("provider_native_tool_unavailable_required_lanes") or [])
        )
    if allow_provider_generation and not pre_provider and metrics.get("provider_semantic_missing_required_lanes"):
        errors.append(
            "provider generation requires semantic GPU0/NPU model execution; missing: "
            + ",".join(metrics.get("provider_semantic_missing_required_lanes") or [])
        )
    if (
        metrics.get("product_status") == "ready"
        and safe_int(metrics.get("provider_lane_count")) < 3
    ):
        errors.append("ready product_status requires all three provider lanes")
    if metrics.get("product_status") == "ready" and not provider_execution_performed:
        errors.append("ready product_status requires observable provider execution")
    if safe_int(metrics.get("provider_textual_tool_call_count")) > 0:
        errors.append(
            "PROVIDER_TOOL_CALLS_REMAIN_TEXT: provider emitted tool calls as JSON/text instead of native tool calls"
        )
    if (
        safe_int(metrics.get("provider_native_tool_loop_requested_count")) > 0
        and safe_int(metrics.get("provider_native_tool_loop_supported_count")) <= 0
    ):
        errors.append(
            "provider native tool loop was requested but no provider lane reported supported native tool calls"
        )
    if metrics.get("product_status") == "ready" and not final_bridge_reports:
        errors.append("ready product_status requires broker bridge reports")
    if metrics.get("product_status") == "ready" and not metrics.get("context_artifact_refs"):
        errors.append("ready product_status requires memory/chunk/context artifacts")
    if (
        metrics.get("product_status") == "ready"
        and not metrics.get("response_text_complete")
        and not generic_product_ready
    ):
        errors.append("ready product_status requires a complete provider response_text")
    if (
        metrics.get("product_status") == "ready"
        and detailed_output_expected
        and not metrics.get("quality_output_passed")
        and not generic_product_ready
    ):
        errors.append(
            "ready product_status requires detailed heap/tool/provider quality output for complex requests"
        )
    if (
        metrics.get("product_status") == "ready"
        and metrics.get("virtual_dev_environment_required")
        and not metrics.get("virtual_dev_environment_passed")
        and not generic_product_ready
    ):
        errors.append(
            "ready product_status requires virtual development environment passed for debug/runtime requests"
        )
    if (
        metrics.get("product_status") == "ready"
        and metrics.get("code_execution_matrix_required")
        and not metrics.get("code_execution_matrix_passed")
        and not generic_product_ready
    ):
        errors.append(
            "ready product_status requires code execution matrix passed for coding requests"
        )
    if (
        metrics.get("patch_candidate_synthesis_required")
        and metrics.get("code_execution_matrix_passed") is True
        and safe_int(metrics.get("matrix_verified_target_count")) > 0
        and safe_int(metrics.get("concrete_code_proposal_count")) == 0
    ):
        errors.append(
            "TARGETS_FOUND_BUT_NO_VALID_PATCH_CANDIDATE: verified local targets exist but matrix produced no validated diff/code product"
        )
    if (
        metrics.get("product_status") == "ready"
        and metrics.get("runtime_debug_lab_required")
        and not metrics.get("runtime_debug_lab_passed")
        and not generic_product_ready
    ):
        errors.append(
            "ready product_status requires runtime debug lab execution passed for MVP/lab requests"
        )
    return prefixed_errors(errors)
