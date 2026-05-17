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
    if not lane_gate_passed:
        errors.append("runtime state degraded lane tolerance exceeded: " + ",".join(degraded_lanes))
    if metrics.get("product_status") == "ready" and missing_requirements:
        errors.append("ready product_status is forbidden while requirements are missing")
    if allow_provider_generation and metrics.get("missing_provider_lanes"):
        errors.append(
            "provider generation requires all three provider lanes; missing: "
            + ",".join(metrics.get("missing_provider_lanes") or [])
        )
    if allow_provider_generation and metrics.get("provider_native_tool_unavailable_required_lanes"):
        errors.append(
            "provider generation requires native tool capability from all three lanes; unavailable: "
            + ",".join(metrics.get("provider_native_tool_unavailable_required_lanes") or [])
        )
    if allow_provider_generation and metrics.get("provider_native_tool_missing_required_lanes"):
        errors.append(
            "provider requested native tool calls but these lanes emitted no native calls: "
            + ",".join(metrics.get("provider_native_tool_missing_required_lanes") or [])
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
    if detailed_output_expected and metrics.get("provider_native_tool_missing_lanes"):
        errors.append(
            "provider native tool loop requested but these lanes emitted no native tool_call: "
            + ",".join(metrics.get("provider_native_tool_missing_lanes") or [])
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
