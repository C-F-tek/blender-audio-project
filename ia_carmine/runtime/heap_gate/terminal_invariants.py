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


ANTI_GAMING = "anti_gaming"
PROVIDER_START_BLOCKER = "provider_start_blocker"
LANE_VIABILITY_BLOCKER = "lane_viability_blocker"
PRODUCT_ACCEPTANCE_BLOCKER = "product_acceptance_blocker"
CAUSALITY_BLOCKER = "causality_blocker"
RECOVERY_BLOCKER = "recovery_blocker"
METRIC_CONSISTENCY_BLOCKER = "metric_consistency_blocker"
PROVIDER_OUTPUT_CONTRACT_VIOLATION = "provider_output_contract_violation"

PREFIX_BY_CATEGORY = {
    ANTI_GAMING: "AI STAI GIOCANDO",
    PROVIDER_START_BLOCKER: "PROVIDER_START_BLOCKED",
    LANE_VIABILITY_BLOCKER: "LANE_UNVIABLE",
    PRODUCT_ACCEPTANCE_BLOCKER: "PRODUCT_ACCEPTANCE_BLOCKED",
    CAUSALITY_BLOCKER: "CAUSALITY_BLOCKED",
    RECOVERY_BLOCKER: "RECOVERY_REQUIRED",
    METRIC_CONSISTENCY_BLOCKER: "METRIC_CONSISTENCY_BLOCKED",
    PROVIDER_OUTPUT_CONTRACT_VIOLATION: "PROVIDER_OUTPUT_CONTRACT_VIOLATION",
}


def _code_from_message(message: str) -> str:
    head = str(message).split(":", 1)[0].strip()
    cleaned = "".join(ch if ch.isalnum() else "_" for ch in head.lower()).strip("_")
    return cleaned or "terminal_invariant_failed"


def _native_tool_evidence_required(metrics: dict[str, Any]) -> bool:
    return bool(
        metrics.get("gpu1_native_tool_evidence_required")
        or metrics.get("lab_called")
        or metrics.get("code_execution_matrix_required")
        or metrics.get("runtime_debug_lab_required")
        or metrics.get("virtual_dev_environment_required")
        or metrics.get("leader_source") == "native_tool_result"
    )


def _classify_message(message: str, metrics: dict[str, Any]) -> dict[str, Any]:
    text = str(message)
    category = PRODUCT_ACCEPTANCE_BLOCKER
    recovery_allowed = False
    counts_as_script_gaming = False
    counts_as_product_lie = False
    if "runtime_file_refs_missing_before_provider_start" in text or text.startswith(
        "provider_start_requirements_missing_before_provider_start"
    ) or text.startswith("pre_provider_closed_with_tentable_requirement"):
        category = PROVIDER_START_BLOCKER
    elif text.startswith("provider generation requires semantic GPU0/NPU model execution") or text.startswith(
        "provider generation requires all three provider lanes"
    ) or text.startswith("runtime state contains unviable lanes") or text.startswith("NPU micro-lane"):
        category = LANE_VIABILITY_BLOCKER
    elif "provider_native_tool_api_unavailable_for_code_delta" in text:
        category = PROVIDER_START_BLOCKER
    elif any(
        fragment in text
        for fragment in (
            "gpu0_checked_wrong_gpu1_packet",
            "gpu0_review_stale_after_gpu1_packet_rewrite",
            "gpu1_refine_not_linked_to_gpu0_veto",
            "gpu1_leader_not_consuming_peer_evidence",
        )
    ):
        category = CAUSALITY_BLOCKER
        recovery_allowed = True
    elif any(
        fragment in text
        for fragment in (
            "gpu0_review_invalid_requires_gpu1_retry",
            "gpu1_recovery_revision_missing_after_sidecar_join",
            "rejected GPU1 proposal did not trigger mandatory provider revision retry",
            "gpu1_tool_result_pending",
            "gpu1_requested_tool_result_not_consumed",
            "gpu1_one_turn_tool_result_not_consumed",
            "gpu1_one_turn_role_tool_reinjection_missing",
            "gpu1_one_turn_broker_result_missing",
        )
    ):
        category = RECOVERY_BLOCKER
        recovery_allowed = True
    elif any(
        fragment in text
        for fragment in (
            "open_pointer_count_zero_with_deferred_pointer_edges",
            "soft_lock_closed_with_targeted_refine_allowed",
            "context_hierarchy_invalid",
            "parallelism_lost_by_serial_leader_gate",
        )
    ):
        category = METRIC_CONSISTENCY_BLOCKER
    elif "PROVIDER_TOOL_CALLS_REMAIN_TEXT" in text:
        promoted = bool(
            metrics.get("provider_textual_tool_calls_counted_as_execution")
            or metrics.get("provider_textual_tool_call_promoted")
        )
        category = ANTI_GAMING if promoted else PROVIDER_OUTPUT_CONTRACT_VIOLATION
        counts_as_script_gaming = promoted
    elif any(
        fragment in text
        for fragment in (
            "GPU0 free text was used as product or decision",
            "gpu0_veto_not_allowed_without_gpu1_decision",
            "free text cannot drive veto/congruence",
            "provider prose cannot pass as product",
            "tool_declared_operational_without_broker_evidence",
            "textual_tool_call_counted_as_execution",
            "generic_write_capture_failed",
            "cannot claim patch application",
            "cannot claim source writes",
        )
    ):
        category = ANTI_GAMING
        counts_as_script_gaming = True
    elif "ready product_status" in text or "cannot pass without ready product" in text:
        category = PRODUCT_ACCEPTANCE_BLOCKER
        counts_as_product_lie = bool(metrics.get("product_status") == "ready")
    return {
        "code": _code_from_message(text),
        "message": text,
        "category": category,
        "severity": "error",
        "phase": "terminal",
        "counts_as_script_gaming": counts_as_script_gaming,
        "counts_as_product_lie": counts_as_product_lie,
        "recovery_allowed": recovery_allowed,
    }


def render_invariant(record: dict[str, Any]) -> str:
    prefix = PREFIX_BY_CATEGORY.get(str(record.get("category") or ""), "TERMINAL_BLOCKED")
    message = str(record.get("message") or "")
    return message if message.startswith(f"{prefix}:") else f"{prefix}: {message}"


def _evaluate_terminal_invariant_messages(
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
    generic_product = (
        metrics.get("generic_write_refined_request")
        or metrics.get("compat_legacy_generic_write_refined_product")
        or metrics.get("compat_legacy_generic_write_document_product")
        or metrics.get("generic_write_refined_product")
        or metrics.get("generic_write_document_product")
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
        if _native_tool_evidence_required(metrics):
            errors.append(
                "gpu1_native_tool_evidence_missing_when_required: GPU1 tool/lab/matrix/debug evidence requires brokered API-native tool evidence"
            )
        else:
            errors.append(
                "gpu1_generation_evidence_missing: GPU1 prompt/chat/proposal evidence is missing or unverified"
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
            return errors
        if metrics.get("gpu1_one_turn_runtime_gate_passed") is not True:
            blocker = str(
                metrics.get("gpu1_one_turn_blocker")
                or "gpu1_one_turn_runtime_gate_missing"
            )
            errors.append(f"gpu1_one_turn_runtime_gate_missing_or_failed:{blocker}")
            if blocker:
                errors.append(blocker)
        if metrics.get("latest_final_product_delta_valid") is not True:
            final_product_protocol_errors = [
                str(item)
                for item in (metrics.get("latest_final_product_protocol_errors") or [])
                if str(item).strip()
            ]
            detail = ",".join(
                final_product_protocol_errors
            )
            errors.append("gpu1_final_product_delta_missing" + (f": {detail}" if detail else ""))
            if "gpu1_blocked_not_allowed_as_final_product_delta" in final_product_protocol_errors:
                errors.append("gpu1_blocked_not_allowed_as_final_product_delta")
        if metrics.get("gpu1_resume_after_tool_result_required"):
            blocker = str(
                metrics.get("gpu1_tool_result_blocker")
                or "gpu1_requested_tool_result_not_consumed"
            )
            errors.append(blocker)
        if (
            metrics.get("latest_final_product_requires_file_read")
            and metrics.get("latest_final_product_file_read_verified") is not True
        ):
            file_read_errors = [
                str(item)
                for item in (metrics.get("latest_final_product_file_read_errors") or [])
                if str(item).strip()
            ]
            detail = ",".join(file_read_errors) or "runtime_file_window_result_missing_or_not_consumed"
            errors.append(f"gpu1_code_delta_without_file_read: {detail}")
            if (
                safe_int(metrics.get("provider_native_tool_loop_requested_count")) > 0
                and safe_int(metrics.get("provider_native_tool_loop_supported_count")) <= 0
            ):
                errors.append("provider_native_tool_api_unavailable_for_code_delta")
            if (
                safe_int(metrics.get("provider_native_tool_call_count")) <= 0
                and safe_int(metrics.get("tool_execution_count")) > 0
            ):
                errors.append(
                    "tool_declared_operational_without_broker_evidence: code delta requires brokered native runtime_file_window result"
                )
            if metrics.get("latest_final_product_file_read_tool_api_ready") is not True:
                tool_api_errors = [
                    str(item)
                    for item in (metrics.get("latest_final_product_file_read_tool_api_errors") or [])
                    if str(item).strip()
                ]
                errors.append(
                    "tool_declared_operational_without_broker_evidence: runtime_file_window API definition is not broker-ready"
                    + (": " + ",".join(tool_api_errors) if tool_api_errors else "")
                )
        if (
            metrics.get("latest_final_product_pointer_protocol_operational") is not True
        ):
            errors.append("gpu1_pointer_protocol_not_operational")
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
            if any(
                str(metrics.get(key) or "").strip()
                for key in (
                    "latest_gpu0_review_decision",
                    "latest_gpu0_model_decision",
                    "latest_gpu0_effective_decision",
                    "latest_gpu0_role_decision",
                )
            ):
                errors.append(
                    "gpu0_secondary_decision_schema_invalid: GPU0 structured/free-text decision exists but schema is invalid; free text cannot drive veto/congruence"
                )
            else:
                errors.append(
                    "gpu0_secondary_decision_schema_missing: GPU0 review is missing or pending"
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
        errors.append("generic_write refined request evidence cannot make product eligible")
        if safe_int(generic_product.get("refinement_count")) < safe_int(
            generic_product.get("minimum_refinements")
        ):
            errors.append("generic_write refined request evidence requires the configured minimum refinements")
        if generic_product.get("patch_application_performed"):
            errors.append("generic_write refined request evidence cannot claim patch application")
        if generic_product.get("source_writes_performed"):
            errors.append("generic_write refined request evidence cannot claim source writes")
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
    return errors


def evaluate_terminal_invariant_records(
    *,
    metrics: dict[str, Any],
    missing_requirements: list[str],
    lane_gate_passed: bool,
    degraded_lanes: list[str],
    final_bridge_reports: list[str],
    allow_provider_generation: bool,
    provider_execution_performed: bool,
    detailed_output_expected: bool,
) -> list[dict[str, Any]]:
    messages = _evaluate_terminal_invariant_messages(
        metrics=metrics,
        missing_requirements=missing_requirements,
        lane_gate_passed=lane_gate_passed,
        degraded_lanes=degraded_lanes,
        final_bridge_reports=final_bridge_reports,
        allow_provider_generation=allow_provider_generation,
        provider_execution_performed=provider_execution_performed,
        detailed_output_expected=detailed_output_expected,
    )
    return [_classify_message(message, metrics) for message in messages]


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
    records = evaluate_terminal_invariant_records(
        metrics=metrics,
        missing_requirements=missing_requirements,
        lane_gate_passed=lane_gate_passed,
        degraded_lanes=degraded_lanes,
        final_bridge_reports=final_bridge_reports,
        allow_provider_generation=allow_provider_generation,
        provider_execution_performed=provider_execution_performed,
        detailed_output_expected=detailed_output_expected,
    )
    return [render_invariant(record) for record in records]
