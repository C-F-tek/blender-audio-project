from __future__ import annotations

from typing import Any

from ia_carmine._shared.provider_work_rejections import (
    MIN_GPU1_WORK_TOKENS,
    gpu0_ollama_rejection_reason,
    gpu1_rejection_reason,
    looks_like_handshake,
    normalize_bool,
    npu_rejection_reason,
    role_for,
    stage,
)


def int_value(value: Any) -> int:
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return 0
    return parsed


def full_gpu_requested(value: str | int | None) -> bool:
    return str(value if value is not None else "").strip().lower() in {"all", "-1"}


def response_likely_incomplete(text: str) -> bool:
    stripped = (text or "").rstrip()
    if not stripped:
        return False
    if stripped.count("```") % 2 == 1:
        return True
    if stripped[-1] in {",", ":", ";", "(", "[", "{"}:
        return True
    lowered = stripped.lower()
    return lowered.endswith(
        (" in", " con", " e", " di", " del", " alla", " che", " per", " from", " with", " and", " or")
    )


def provider_work_status(
    *, lane: str, report: dict[str, Any], default_role: str = ""
) -> dict[str, Any]:
    provider_id = str(lane or report.get("provider_id") or report.get("lane") or "").strip()
    if provider_id in {"ollama", "gpu1", "gpu1_primary"}:
        provider_id = "gpu1_planner"
    if provider_id in {"npu", "npu_auditor"}:
        provider_id = "npu_micro_task_auditor"
    if provider_id in {"gpu0", "gpu0_reviewer_refiner"}:
        provider_id = "gpu0_peer"
    role = role_for(provider_id, report, default_role)

    if provider_id == "gpu1_planner":
        status = _gpu1_status(report)
    elif provider_id == "gpu0_peer":
        status = _gpu0_status(report)
    elif provider_id == "npu_micro_task_auditor":
        status = _npu_status(report)
    else:
        status = _generic_status(report)

    status["provider_id"] = provider_id
    status["provider_role"] = role
    status["provider_role_counted"] = bool(status["provider_work_verified"])
    status["provider_rejection_reason"] = (
        "" if status["provider_work_verified"] else status["provider_rejection_reason"]
    )
    status["role_rejection_reason"] = status["provider_rejection_reason"]
    status["provider_stage"] = stage(status)
    return status


def provider_rejection_record(
    *, path: str, lane: str, report: dict[str, Any], default_role: str = ""
) -> dict[str, Any]:
    status = provider_work_status(lane=lane, report=report, default_role=default_role)
    return {
        "source_path": path,
        "provider_id": status["provider_id"],
        "provider_role": status["provider_role"],
        "provider_stage": status["provider_stage"],
        "provider_rejection_reason": status["provider_rejection_reason"],
        "device_detected": status["device_detected"],
        "model_loaded": status["model_loaded"],
        "health_check_passed": status["health_check_passed"],
        "workload_performed": status["workload_performed"],
        "useful_output_produced": status["useful_output_produced"],
        "provider_work_verified": status["provider_work_verified"],
        "provider_role_counted": status["provider_role_counted"],
    }


def _gpu1_status(report: dict[str, Any]) -> dict[str, Any]:
    operator_blocked = normalize_bool(report.get("operator_gpu_observation_blocked"))
    token_count = int_value(report.get("eval_count") or report.get("completion_token_count"))
    response_text = _response_text(report)
    useful_output = _useful_output(report)
    residency_verified = normalize_bool(
        report.get("ollama_residency_verified")
        or report.get("provider_device_verified")
        or report.get("ollama_full_gpu_verified")
    )
    model_loaded = normalize_bool(report.get("provider_loaded")) or bool(
        str(report.get("selected_model") or report.get("provider_model") or "").strip()
        and token_count > 0
        and normalize_bool(report.get("done"))
    )
    compute_verified = normalize_bool(report.get("ollama_compute_verified"))
    workload = bool(
        compute_verified
        or (
            not normalize_bool(report.get("replight_mode"))
            and token_count >= MIN_GPU1_WORK_TOKENS
            and useful_output
        )
    )
    health = normalize_bool(report.get("replight_passed")) or bool(
        residency_verified and model_loaded and token_count > 0
    )
    verified = bool(
        residency_verified
        and model_loaded
        and not operator_blocked
        and not normalize_bool(report.get("replight_mode"))
        and compute_verified
        and token_count >= MIN_GPU1_WORK_TOKENS
        and useful_output
    )
    return {
        "device_detected": residency_verified,
        "model_loaded": model_loaded,
        "health_check_passed": health,
        "workload_performed": workload,
        "useful_output_produced": useful_output,
        "provider_work_verified": verified,
        "provider_rejection_reason": gpu1_rejection_reason(
            report=report,
            response_text=response_text,
            token_count=token_count,
            residency_verified=residency_verified,
            model_loaded=model_loaded,
            useful_output=useful_output,
            compute_verified=compute_verified,
            operator_blocked=operator_blocked,
        ),
    }


def _gpu0_status(report: dict[str, Any]) -> dict[str, Any]:
    if str(report.get("provider_backend") or "").strip().lower() == "ollama":
        return _gpu0_ollama_status(report)
    return {
        "device_detected": False,
        "model_loaded": False,
        "health_check_passed": False,
        "workload_performed": False,
        "useful_output_produced": False,
        "provider_work_verified": False,
        "provider_rejection_reason": "gpu0_ollama_vulkan_required",
    }


def _gpu0_ollama_status(report: dict[str, Any]) -> dict[str, Any]:
    operator_blocked = normalize_bool(report.get("operator_gpu_observation_blocked"))
    token_count = int_value(report.get("eval_count") or report.get("completion_token_count"))
    response_text = _response_text(report)
    useful_output = _useful_output(report)
    compute_device = str(report.get("provider_compute_device") or "")
    residency_verified = normalize_bool(
        report.get("ollama_residency_verified")
        or report.get("provider_device_verified")
        or report.get("ollama_full_gpu_verified")
    )
    vulkan_lane = "gpu0-vulkan" in compute_device or normalize_bool(
        report.get("ollama_vulkan_required")
    )
    model_loaded = bool(
        str(report.get("selected_model") or report.get("provider_model") or "").strip()
        and (token_count > 0 or normalize_bool(report.get("provider_loaded")))
    )
    compute_verified = normalize_bool(report.get("ollama_compute_verified"))
    workload = bool(
        compute_verified
        or (
            not normalize_bool(report.get("replight_mode"))
            and token_count >= MIN_GPU1_WORK_TOKENS
            and useful_output
        )
    )
    health = normalize_bool(report.get("replight_passed")) or bool(
        residency_verified and model_loaded and token_count > 0
    )
    verified = bool(
        residency_verified
        and vulkan_lane
        and model_loaded
        and not operator_blocked
        and not normalize_bool(report.get("replight_mode"))
        and compute_verified
        and token_count >= MIN_GPU1_WORK_TOKENS
        and useful_output
    )
    return {
        "device_detected": residency_verified and vulkan_lane,
        "model_loaded": model_loaded,
        "health_check_passed": health,
        "workload_performed": workload,
        "useful_output_produced": useful_output,
        "provider_work_verified": verified,
        "provider_rejection_reason": gpu0_ollama_rejection_reason(
            response_text=response_text,
            token_count=token_count,
            residency_verified=residency_verified,
            vulkan_lane=vulkan_lane,
            model_loaded=model_loaded,
            useful_output=useful_output,
            compute_verified=compute_verified,
            operator_blocked=operator_blocked,
        ),
    }


def _npu_status(report: dict[str, Any]) -> dict[str, Any]:
    compute_device = str(report.get("provider_compute_device") or "")
    device_detected = bool(
        normalize_bool(report.get("provider_device_verified")) and "NPU" in compute_device
    )
    model_loaded = normalize_bool(report.get("npu_micro_provider_model_loaded"))
    provider_execution = normalize_bool(report.get("npu_micro_provider_execution_performed"))
    workload = bool(
        provider_execution and normalize_bool(report.get("npu_device_workload_performed"))
    )
    useful_output = bool(provider_execution and _useful_output(report))
    verified = bool(device_detected and model_loaded and workload and useful_output)
    return {
        "device_detected": device_detected,
        "model_loaded": model_loaded,
        "health_check_passed": bool(normalize_bool(report.get("replight_passed")) or device_detected),
        "workload_performed": workload,
        "useful_output_produced": useful_output,
        "provider_work_verified": verified,
        "provider_rejection_reason": npu_rejection_reason(
            report=report,
            device_detected=device_detected,
            model_loaded=model_loaded,
            provider_execution=provider_execution,
            workload=workload,
            useful_output=useful_output,
        ),
    }


def _generic_status(report: dict[str, Any]) -> dict[str, Any]:
    device_detected = normalize_bool(report.get("provider_device_verified"))
    model_loaded = normalize_bool(report.get("provider_loaded"))
    workload = normalize_bool(report.get("workload_performed"))
    useful_output = _useful_output(report)
    verified = bool(device_detected and model_loaded and workload and useful_output)
    return {
        "device_detected": device_detected,
        "model_loaded": model_loaded,
        "health_check_passed": bool(report.get("passed") is True),
        "workload_performed": workload,
        "useful_output_produced": useful_output,
        "provider_work_verified": verified,
        "provider_rejection_reason": "" if verified else "provider_no_verified_workload",
    }


def _response_text(report: dict[str, Any]) -> str:
    return str(
        report.get("response_text")
        or report.get("provider_heap_delta_text")
        or report.get("tool_result_summary")
        or report.get("micro_task_result_summary")
        or ""
    ).strip()


def _useful_output(report: dict[str, Any]) -> bool:
    text = _response_text(report)
    if looks_like_handshake(text):
        return False
    if int_value(report.get("native_tool_call_count")) > 0:
        return True
    if report.get("target_files") or report.get("validation_commands") or report.get("tool_calls"):
        return True
    return len(text.split()) >= 8
