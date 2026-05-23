from __future__ import annotations

from typing import Any

from ia_carmine._shared.provider_tool_loop import ollama_tool_call_tool_names
from ia_carmine._shared.provider_work_verification import provider_work_status


def estimated_token_count(text: Any) -> int:
    value = str(text or "").strip()
    if not value:
        return 0
    return max(1, len(value.split()))


def provider_replight_fields(
    *,
    lane: str,
    role: str,
    report: dict[str, Any],
    default_model: str = "",
    functionalities: list[str] | None = None,
) -> dict[str, Any]:
    provider_id = str(lane or report.get("lane") or "").strip()
    provider_role = str(role or report.get("role") or provider_id).strip()
    provider_model = str(
        report.get("provider_model")
        or report.get("selected_model")
        or report.get("semantic_provider_model_dir")
        or report.get("npu_micro_provider_model_dir")
        or default_model
        or ""
    ).strip()
    response_text = str(
        report.get("response_text")
        or report.get("provider_heap_delta_text")
        or report.get("tool_result_summary")
        or report.get("micro_task_result_summary")
        or ""
    ).strip()
    generated_phrase = _first_sentence(response_text)
    prompt_tokens = _int_first(
        report.get("prompt_token_count"),
        report.get("prompt_eval_count"),
        estimated_token_count(report.get("request_prompt") or report.get("request_input")),
    )
    completion_tokens = _int_first(
        report.get("completion_token_count"),
        report.get("eval_count"),
        estimated_token_count(response_text),
    )
    elapsed = _float_value(report.get("eval_duration_seconds")) or _float_value(
        report.get("elapsed_sec") or report.get("elapsed_seconds")
    )
    tokens_per_second = _float_value(report.get("tokens_per_second"))
    if tokens_per_second is None and elapsed and elapsed > 0 and completion_tokens > 0:
        tokens_per_second = round(float(completion_tokens) / elapsed, 4)
    provider_loaded = _provider_loaded(provider_id, report, provider_model, generated_phrase)
    available_tools = ollama_tool_call_tool_names()
    native_supported = bool(
        report.get("native_tool_loop_supported")
        or report.get("native_tool_calling_supported")
        or provider_id == "gpu1_planner"
    )
    functionality_values = functionalities or _default_functionalities(provider_id)
    replight_blocked_reason = ""
    if not provider_loaded:
        detail = _provider_loaded_failure(provider_id, report, provider_model, generated_phrase)
        replight_blocked_reason = f"provider_replight_failed:{provider_id}:{detail}"
    elif prompt_tokens <= 0 or completion_tokens <= 0:
        replight_blocked_reason = f"provider_replight_failed:{provider_id}:missing_token_metrics"
    elif not available_tools:
        replight_blocked_reason = f"provider_replight_failed:{provider_id}:missing_tool_catalog"
    elif not functionality_values:
        replight_blocked_reason = f"provider_replight_failed:{provider_id}:missing_functionalities"
    replight_passed = not replight_blocked_reason
    work_status = provider_work_status(
        lane=provider_id,
        report={**report, "provider_loaded": provider_loaded, "replight_passed": replight_passed},
        default_role=provider_role,
    )
    return {
        "provider_replight_required": True,
        "provider_id": provider_id,
        "provider_role": provider_role,
        "provider_model": provider_model,
        "provider_loaded": provider_loaded,
        "generated_phrase": generated_phrase,
        "prompt_token_count": prompt_tokens,
        "completion_token_count": completion_tokens,
        "token_metric_source": (
            "provider_native_metrics"
            if report.get("eval_count") or report.get("prompt_eval_count")
            else "deterministic_estimate"
        ),
        "tokens_per_second": tokens_per_second,
        "native_tool_calling_supported": native_supported,
        "broker_tools_available_count": len(available_tools),
        "available_tool_names": available_tools,
        "functionalities": functionality_values,
        "replight_passed": replight_passed,
        "replight_blocked_reason": replight_blocked_reason,
        "device_detected": work_status["device_detected"],
        "model_loaded": work_status["model_loaded"],
        "health_check_passed": work_status["health_check_passed"],
        "workload_performed": work_status["workload_performed"],
        "useful_output_produced": work_status["useful_output_produced"],
        "provider_work_verified": work_status["provider_work_verified"],
        "provider_role_counted": work_status["provider_role_counted"],
        "provider_stage": work_status["provider_stage"],
        "provider_rejection_reason": work_status["provider_rejection_reason"],
        "role_rejection_reason": work_status["role_rejection_reason"],
    }


def provider_replight_failure_reason(reports: list[dict[str, Any]]) -> str:
    for report in reports:
        lane = str(report.get("lane") or report.get("provider_id") or "provider").strip()
        if report.get("replight_passed") is True:
            continue
        reason = str(report.get("replight_blocked_reason") or "").strip()
        if not reason:
            reason = f"provider_replight_failed:{lane}"
        return reason
    return ""


def _provider_loaded(
    lane: str,
    report: dict[str, Any],
    provider_model: str,
    generated_phrase: str,
) -> bool:
    if lane == "gpu1_planner":
        return bool(
            provider_model
            and generated_phrase
            and report.get("passed") is not False
            and (
                report.get("provider_execution_attempted") is True
                or report.get("provider_io_observed") is True
                or report.get("provider_execution_performed") is True
            )
            and report.get("provider_device_verified") is True
            and report.get("ollama_full_gpu_verified") is True
            and report.get("done") is True
            and _int_first(report.get("eval_count")) > 0
        )
    if lane == "gpu0_peer":
        if str(report.get("provider_backend") or "").lower() == "ollama":
            return bool(
                provider_model
                and generated_phrase
                and report.get("provider_device_verified") is True
                and report.get("ollama_residency_verified") is True
                and report.get("done") is True
                and _int_first(report.get("eval_count")) > 0
            )
        return bool(
            provider_model
            and generated_phrase
            and report.get("passed") is True
            and report.get("provider_device_verified") is True
            and report.get("device_workload_execution_performed") is True
            and report.get("semantic_provider_model_loaded") is True
            and report.get("semantic_provider_execution_performed") is True
        )
    if lane == "npu_micro_task_auditor":
        if report.get("npu_peer_evidence_verified") is True:
            return bool(
                provider_model
                and generated_phrase
                and report.get("provider_device_verified") is True
                and report.get("npu_device_workload_requested") is True
                and report.get("npu_device_workload_performed") is True
                and report.get("npu_micro_audit_performed") is True
            )
        return bool(
            provider_model
            and generated_phrase
            and report.get("passed") is True
            and report.get("provider_device_verified") is True
            and report.get("npu_device_workload_requested") is True
            and report.get("npu_device_workload_performed") is True
            and report.get("npu_micro_provider_model_loaded") is True
            and report.get("npu_micro_provider_execution_performed") is True
        )
    return bool(
        generated_phrase
        and report.get("provider_device_verified") is True
        and (
            report.get("provider_execution_performed")
            or report.get("device_workload_execution_performed")
            or report.get("npu_micro_audit_performed")
        )
    )


def _provider_loaded_failure(
    lane: str,
    report: dict[str, Any],
    provider_model: str,
    generated_phrase: str,
) -> str:
    if lane == "gpu1_planner":
        if not provider_model:
            return "provider_model_missing"
        if report.get("provider_execution_performed") is not True:
            return "provider_execution_missing"
        if report.get("provider_device_verified") is not True:
            return "provider_device_unverified"
        if report.get("ollama_full_gpu_verified") is not True:
            return "ollama_full_gpu_not_verified"
        if report.get("done") is not True:
            return "generation_not_done"
        if _int_first(report.get("eval_count")) <= 0:
            return "missing_generation_token_metrics"
        if not generated_phrase:
            return "no_generated_phrase"
        return "passed_false"
    if lane == "gpu0_peer":
        if str(report.get("provider_backend") or "").lower() == "ollama":
            if not provider_model:
                return "provider_model_missing"
            if report.get("provider_device_verified") is not True:
                return "gpu0_ollama_vulkan_unavailable"
            if report.get("ollama_residency_verified") is not True:
                return "gpu0_ollama_vulkan_residency_unproven"
            if report.get("done") is not True:
                return "generation_not_done"
            if _int_first(report.get("eval_count")) <= 0:
                return "missing_generation_token_metrics"
            if not generated_phrase:
                return "no_generated_phrase"
            return "passed_false"
        if not provider_model:
            return "provider_model_missing"
        if report.get("provider_device_verified") is not True:
            return "provider_device_unverified"
        if report.get("device_workload_execution_performed") is not True:
            return "device_workload_missing"
        if report.get("semantic_provider_model_loaded") is not True:
            return "semantic_provider_model_not_loaded"
        if report.get("semantic_provider_execution_performed") is not True:
            return "semantic_provider_execution_missing"
        if not generated_phrase:
            return "no_generated_phrase"
        return "passed_false"
    if lane == "npu_micro_task_auditor":
        if not provider_model:
            return "provider_model_missing"
        if report.get("provider_device_verified") is not True:
            return "provider_device_unverified"
        if (
            report.get("npu_device_workload_requested") is not True
            or report.get("npu_device_workload_performed") is not True
        ):
            return "npu_device_workload_missing"
        if report.get("npu_peer_evidence_verified") is True:
            if report.get("npu_micro_audit_performed") is not True:
                return "npu_micro_audit_missing"
            if not generated_phrase:
                return "no_generated_phrase"
            return "passed_false"
        native_error = str(report.get("npu_native_tool_loop_error") or "").strip()
        if native_error:
            return native_error
        if report.get("npu_micro_provider_model_loaded") is not True:
            return "npu_micro_provider_model_not_loaded"
        if report.get("npu_micro_provider_execution_performed") is not True:
            return "npu_micro_provider_execution_missing"
        if not generated_phrase:
            return "no_generated_phrase"
        return "passed_false"
    return "not_loaded_or_no_phrase"


def _default_functionalities(lane: str) -> list[str]:
    if lane == "gpu1_planner":
        return ["planning", "synthesis", "closure_owner", "native_tool_calling"]
    if lane == "gpu0_peer":
        return ["review", "refine", "ollama_gpu0_vulkan_workload", "native_tool_calling"]
    if lane == "npu_micro_task_auditor":
        return ["micro_audit", "openvino_npu_workload", "guardrail_check"]
    return ["provider_evidence"]


def _first_sentence(text: str, limit: int = 240) -> str:
    cleaned = " ".join(str(text or "").split())
    if not cleaned:
        return ""
    for marker in (". ", "\n", "; "):
        if marker in cleaned:
            cleaned = cleaned.split(marker, 1)[0]
            break
    return cleaned[:limit]


def _int_first(*values: Any) -> int:
    for value in values:
        try:
            parsed = int(value)
        except (TypeError, ValueError):
            continue
        if parsed > 0:
            return parsed
    return 0


def _float_value(value: Any) -> float | None:
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return None
    return parsed if parsed >= 0 else None
