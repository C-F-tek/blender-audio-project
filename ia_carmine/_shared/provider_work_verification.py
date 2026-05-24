from __future__ import annotations

from pathlib import Path
from typing import Any

from ia_carmine._shared.file_backed_transport import report_text_required_full
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

    workload_passed = bool(
        status.get("device_detected")
        and status.get("model_loaded")
        and status.get("workload_performed")
        and status.get("useful_output_produced")
    )
    semantic_contract_passed = bool(
        status.get("provider_work_verified")
        and _semantic_contract_passed(provider_id, report)
    )
    provider_requirement_complete = bool(workload_passed and semantic_contract_passed)
    status["workload_passed"] = workload_passed
    status["semantic_contract_passed"] = semantic_contract_passed
    status["provider_requirement_complete"] = provider_requirement_complete
    status["provider_work_verified"] = provider_requirement_complete
    explicit_rejection = str(report.get("provider_rejection_reason") or "").strip()
    if explicit_rejection:
        status["provider_work_verified"] = False
        status["provider_requirement_complete"] = False
        status["semantic_contract_passed"] = False
        status["provider_rejection_reason"] = explicit_rejection

    status["provider_id"] = provider_id
    status["provider_role"] = role
    status["provider_role_counted"] = bool(status["provider_requirement_complete"])
    base_rejection_reason = str(status.get("provider_rejection_reason") or "").strip()
    generic_rejection_reasons = {
        "",
        "provider_no_verified_workload",
        "gpu1_no_verified_workload",
        "gpu0_ollama_vulkan_no_verified_workload",
        "npu_micro_provider_not_verified",
    }
    if status["provider_requirement_complete"]:
        rejection_reason = ""
    elif workload_passed and not semantic_contract_passed:
        rejection_reason = (
            base_rejection_reason
            if base_rejection_reason not in generic_rejection_reasons
            else "provider_semantic_contract_failed"
        )
    else:
        rejection_reason = base_rejection_reason or "provider_semantic_contract_failed"
    status["provider_rejection_reason"] = rejection_reason
    status["role_rejection_reason"] = status["provider_rejection_reason"]
    status["provider_stage"] = stage(status)
    return status


def _semantic_contract_passed(provider_id: str, report: dict[str, Any]) -> bool:
    if provider_id == "npu_micro_task_auditor":
        for key in ("semantic_contract_passed", "provider_requirement_complete", "provider_work_verified"):
            if key in report and normalize_bool(report.get(key)) is False:
                return False
        if str(report.get("provider_rejection_reason") or "").strip():
            return False
        if normalize_bool(report.get("npu_peer_followup_required")):
            return False
        if str(report.get("npu_native_tool_loop_error") or "").strip():
            return False
    if provider_id == "gpu1_planner":
        for key in (
            "quality_passed",
            "proposal_quality_passed",
            "semantic_contract_passed",
            "provider_requirement_complete",
        ):
            if key in report and normalize_bool(report.get(key)) is False:
                return False
        for key in ("implementation_quality", "proposal_progress", "response_file_reference_quality"):
            value = report.get(key)
            if isinstance(value, dict) and value.get("passed") is False:
                return False
        if normalize_bool(report.get("proposal_requires_refinement")):
            return False
    return True


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
        "workload_passed": status["workload_passed"],
        "semantic_contract_passed": status["semantic_contract_passed"],
        "provider_requirement_complete": status["provider_requirement_complete"],
        "provider_work_verified": status["provider_work_verified"],
        "provider_role_counted": status["provider_role_counted"],
        "npu_peer_evidence_verified": status.get("npu_peer_evidence_verified", False),
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
        or report.get("device_identity_verified")
        or report.get("gpu0_vulkan_policy_verified")
    )
    model_loaded = normalize_bool(report.get("provider_loaded")) or bool(
        str(report.get("selected_model") or report.get("provider_model") or "").strip()
        and token_count > 0
        and normalize_bool(report.get("done"))
    )
    compute_verified = normalize_bool(
        report.get("ollama_compute_verified")
        or report.get("gpu0_vulkan_workload_verified")
        or report.get("gpu0_vulkan_sdk_workload_verified")
    )
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
    schema_valid = report.get("gpu0_secondary_schema_valid") is True
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
        and schema_valid
        and token_count >= MIN_GPU1_WORK_TOKENS
        and useful_output
    )
    rejection_reason = gpu0_ollama_rejection_reason(
        response_text=response_text,
        token_count=token_count,
        residency_verified=residency_verified,
        vulkan_lane=vulkan_lane,
        model_loaded=model_loaded,
        useful_output=useful_output,
        compute_verified=compute_verified,
        operator_blocked=operator_blocked,
    )
    if not schema_valid and not rejection_reason.startswith("gpu0_ollama_vulkan_"):
        rejection_reason = "gpu0_secondary_schema_invalid"
    elif not schema_valid and residency_verified and vulkan_lane and model_loaded and compute_verified:
        rejection_reason = "gpu0_secondary_schema_invalid"
    return {
        "device_detected": residency_verified and vulkan_lane,
        "model_loaded": model_loaded,
        "health_check_passed": health,
        "workload_performed": workload,
        "useful_output_produced": useful_output,
        "provider_work_verified": verified,
        "provider_rejection_reason": rejection_reason,
    }


def _npu_status(report: dict[str, Any]) -> dict[str, Any]:
    compute_device = str(report.get("provider_compute_device") or "")
    device_detected = bool(
        normalize_bool(report.get("provider_device_verified")) and "NPU" in compute_device
    )
    peer_evidence = normalize_bool(report.get("npu_peer_evidence_verified"))
    native_model_loaded = normalize_bool(report.get("npu_micro_provider_model_loaded"))
    model_loaded = bool(native_model_loaded or peer_evidence)
    provider_execution = normalize_bool(report.get("npu_micro_provider_execution_performed"))
    workload = bool(
        peer_evidence
        or (
            provider_execution
            and normalize_bool(report.get("npu_device_workload_performed"))
        )
    )
    useful_output = bool(
        (provider_execution or peer_evidence)
        and (_useful_output(report) or normalize_bool(report.get("npu_response_schema_valid")))
    )
    verified = bool(device_detected and model_loaded and workload and useful_output)
    return {
        "device_detected": device_detected,
        "model_loaded": model_loaded,
        "npu_peer_evidence_verified": peer_evidence,
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
    repo_root = Path(str(report.get("repo_root") or ".")).resolve()
    text = str(report_text_required_full(repo_root, report).get("text") or "").strip()
    if text:
        return text
    text = str(
        report_text_required_full(repo_root, report, ("provider_heap_delta_text",)).get("text") or ""
    ).strip()
    return text


def _useful_output(report: dict[str, Any]) -> bool:
    text = _response_text(report)
    if looks_like_handshake(text):
        return False
    if int_value(report.get("native_tool_call_count")) > 0:
        return True
    if report.get("target_files") or report.get("validation_commands") or report.get("tool_calls"):
        return True
    return len(text.split()) >= 8
