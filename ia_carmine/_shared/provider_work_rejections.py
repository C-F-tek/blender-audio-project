from __future__ import annotations

from typing import Any

MIN_GPU1_WORK_TOKENS = 64


def normalize_bool(value: Any) -> bool:
    return value is True or str(value).strip().lower() == "true"


def gpu1_rejection_reason(
    *,
    report: dict[str, Any],
    response_text: str,
    token_count: int,
    residency_verified: bool,
    model_loaded: bool,
    useful_output: bool,
    compute_verified: bool,
    operator_blocked: bool,
) -> str:
    if normalize_bool(report.get("provider_work_verified")):
        return ""
    if operator_blocked:
        return str(report.get("product_blocked_reason") or "gpu1_no_observable_compute")
    if normalize_bool(report.get("replight_mode")) or looks_like_handshake(response_text):
        return "gpu1_no_verified_workload"
    if not residency_verified:
        return "gpu1_ollama_gpu_residency_unproven_or_cpu_bound"
    if not model_loaded:
        return "gpu1_model_not_loaded"
    if not compute_verified:
        return "gpu1_no_verified_workload"
    if token_count < MIN_GPU1_WORK_TOKENS:
        return "gpu1_generation_too_short_for_provider_work"
    if not useful_output:
        return "gpu1_no_useful_provider_output"
    return "gpu1_no_verified_workload"


def gpu0_rejection_reason(
    *,
    report: dict[str, Any],
    correct_device: bool,
    device_detected: bool,
    model_loaded: bool,
    semantic_execution: bool,
    useful_output: bool,
) -> str:
    if normalize_bool(report.get("provider_work_verified")):
        return ""
    if not correct_device:
        return "gpu0_invalid_provider_device"
    if not device_detected:
        return "gpu0_device_unverified"
    if not model_loaded:
        return "gpu0_semantic_provider_not_loaded"
    if not semantic_execution:
        return "gpu0_semantic_provider_execution_missing"
    if not useful_output:
        return "gpu0_no_useful_peer_output"
    return "gpu0_no_verified_workload"


def gpu0_ollama_rejection_reason(
    *,
    response_text: str,
    token_count: int,
    residency_verified: bool,
    vulkan_lane: bool,
    model_loaded: bool,
    useful_output: bool,
    compute_verified: bool,
    operator_blocked: bool,
) -> str:
    if operator_blocked:
        return "gpu0_ollama_vulkan_no_observable_compute"
    if looks_like_handshake(response_text):
        return "gpu0_ollama_vulkan_no_verified_workload"
    if not vulkan_lane or not residency_verified:
        return "gpu0_ollama_vulkan_unavailable"
    if not model_loaded:
        return "gpu0_ollama_vulkan_model_not_loaded"
    if not compute_verified:
        return "gpu0_ollama_vulkan_no_verified_workload"
    if token_count < MIN_GPU1_WORK_TOKENS:
        return "gpu0_ollama_vulkan_generation_too_short"
    if not useful_output:
        return "gpu0_ollama_vulkan_no_useful_peer_output"
    return "gpu0_ollama_vulkan_no_verified_workload"


def npu_rejection_reason(
    *,
    report: dict[str, Any],
    device_detected: bool,
    model_loaded: bool,
    provider_execution: bool,
    workload: bool,
    useful_output: bool,
) -> str:
    if normalize_bool(report.get("provider_work_verified")):
        return ""
    if normalize_bool(report.get("npu_peer_evidence_verified")):
        return ""
    classification = str(report.get("npu_micro_provider_classification") or "")
    if "timeout" in classification:
        return "npu_native_tool_loop_timeout_without_peer_evidence"
    if not device_detected:
        return "npu_device_unverified"
    if not model_loaded:
        return "npu_micro_provider_not_loaded"
    if not provider_execution:
        return "npu_micro_provider_execution_missing"
    if not workload:
        return "npu_micro_workload_missing"
    if not useful_output:
        return "npu_micro_no_useful_audit_output"
    return "npu_micro_provider_not_verified"


def role_for(provider_id: str, report: dict[str, Any], default_role: str) -> str:
    explicit = str(report.get("role") or report.get("provider_role") or default_role or "")
    if explicit and explicit not in {"primary", "peer", "micro", "provider", "worker", "auditor"}:
        return explicit
    if provider_id == "gpu1_planner":
        return "gpu1_planner"
    if provider_id == "gpu0_peer":
        return "gpu0_reviewer_refiner"
    if provider_id == "npu_micro_task_auditor":
        return "npu_auditor"
    return explicit or provider_id


def looks_like_handshake(text: str) -> bool:
    normalized = " ".join(str(text or "").strip().lower().split())
    if not normalized:
        return True
    markers = (
        '{"ok": true',
        '"lane": "ollama"',
        "sono caricato",
        "sono pronto",
        "i am loaded",
        "loaded and ready",
        "provider loaded",
        "ok true lane ollama",
    )
    return any(marker in normalized for marker in markers) and len(normalized) < 220


def stage(status: dict[str, Any]) -> str:
    if status.get("provider_work_verified"):
        return "verified_provider_work"
    if status.get("useful_output_produced") and status.get("workload_performed"):
        return "useful_output_unverified"
    if status.get("workload_performed"):
        return "workload_without_useful_output"
    if status.get("health_check_passed"):
        return "health_check_only"
    if status.get("model_loaded"):
        return "model_loaded_only"
    if status.get("device_detected"):
        return "device_detected_only"
    return ""
