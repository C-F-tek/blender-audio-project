"""Terminal product invariants for the heap completeness gate."""

from __future__ import annotations

from typing import Any


def safe_int(value: Any) -> int:
    try:
        return int(value or 0)
    except (TypeError, ValueError):
        return 0


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
    if allow_provider_generation and detailed_output_expected:
        if metrics.get("product_status") != "ready":
            errors.append(
                "complete provider product run cannot pass without ready product; "
                f"product_status={metrics.get('product_status')}"
            )
        if not metrics.get("provider_raw_response_text"):
            errors.append("GPU1 primary center produced no provider response text")
        if not metrics.get("proposal_iteration_artifacts"):
            errors.append("provider product run requires GPU1 proposal/pointer iteration artifacts")
        if metrics.get("quality_output_passed") is not True:
            errors.append(
                "GPU1/pointer proposal quality failed; provider prose cannot pass as product"
            )
        if metrics.get("latest_proposal_quality_passed") is False:
            errors.append(
                "latest proposal iteration was rejected by same-heap quality gate: "
                + str(metrics.get("latest_proposal_reject_reason") or "")
            )
        gpu0_decision = str(metrics.get("latest_gpu0_review_decision") or "")
        if gpu0_decision.startswith("reject"):
            errors.append(f"GPU0 peer rejected current GPU1 delta: {gpu0_decision}")
        missing_sections = metrics.get("latest_gpu0_missing_delta_sections") or []
        if missing_sections:
            errors.append(
                "GPU1 delta is missing required pointer/product sections: "
                + ",".join(str(item) for item in missing_sections)
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
    if allow_provider_generation and metrics.get("missing_provider_lanes"):
        errors.append(
            "provider generation requires all three provider lanes; missing: "
            + ",".join(metrics.get("missing_provider_lanes") or [])
        )
    if allow_provider_generation and metrics.get("provider_native_tool_unavailable_required_lanes"):
        errors.append(
            "provider generation requested a native tool call on unavailable provider lanes: "
            + ",".join(metrics.get("provider_native_tool_unavailable_required_lanes") or [])
        )
    if allow_provider_generation and metrics.get("provider_semantic_missing_required_lanes"):
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
    if metrics.get("product_status") == "ready" and not metrics.get("response_text_complete"):
        errors.append("ready product_status requires a complete provider response_text")
    if (
        metrics.get("product_status") == "ready"
        and detailed_output_expected
        and not metrics.get("quality_output_passed")
    ):
        errors.append(
            "ready product_status requires detailed heap/tool/provider quality output for complex requests"
        )
    if (
        metrics.get("product_status") == "ready"
        and metrics.get("virtual_dev_environment_required")
        and not metrics.get("virtual_dev_environment_passed")
    ):
        errors.append(
            "ready product_status requires virtual development environment passed for debug/runtime requests"
        )
    if (
        metrics.get("product_status") == "ready"
        and metrics.get("code_execution_matrix_required")
        and not metrics.get("code_execution_matrix_passed")
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
    ):
        errors.append(
            "ready product_status requires runtime debug lab execution passed for MVP/lab requests"
        )
    return prefixed_errors(errors)
