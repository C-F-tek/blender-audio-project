#!/usr/bin/env python3
from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

from ia_carmine._shared.file_backed_transport import (
    INLINE_TEXT_MAX_CHARS,
    text_sha256,
    write_large_text_evidence,
)

_REPORT_KEYS = (
    "passed",
    "require_gpu_residency",
    "residency",
    "selection",
    "ollama_ps_snapshots",
    "gpu_runtime_summary",
    "ollama_residency_verified",
    "ollama_compute_verified",
    "work_status",
    "provider_work_verified",
    "provider_execution_performed",
    "provider_execution_attempted",
    "provider_io_observed",
    "generation_stats",
    "replight",
    "replight_mode",
    "started",
    "selected_model",
    "operator_gpu_observation",
    "num_ctx",
    "gpu_layers",
    "num_thread",
    "prompt",
    "prompt_ref",
    "repo_root",
    "response_text",
    "text",
    "propagated_max_new_tokens",
    "heap_delta_text_required",
    "parsed",
    "parsed_json",
    "response_likely_incomplete",
    "native_tool_calls",
    "textual_tool_calls",
    "native_tool_loop_requested",
    "native_tool_loop_relevant",
    "native_tool_api_attempted",
    "native_tool_api_completed",
    "provider_native_tool_call_required",
    "provider_native_tool_api_adapter_available",
    "provider_native_tool_api_supported",
    "provider_native_tool_api_error",
    "provider_native_tool_api_attempt_error",
    "provider_native_tool_api_unavailable",
    "provider_native_tool_api_attempt_failed",
    "provider_native_tool_call_required_unmet",
    "native_tool_decision_prompted",
    "native_classification",
    "errors",
    "warnings",
    "raw_chat_response",
    "target_files",
    "validation_commands",
    "rejected_validation_refs",
    "models",
    "is_server_ready",
    "empty_output",
    "prompt_attempts",
    "partial_json",
    "provider_lane",
    "provider_role",
    "effective_base_url",
    "server_ready",
    "server_process",
    "unload_model",
    "unload_performed",
    "unload_verified",
    "gpu0_vulkan_compute_observed",
    "gpu0_vulkan_sdk_workload_verified",
    "gpu0_vulkan_policy_verified",
)


def ollama_report_context(scope: dict[str, Any]) -> dict[str, Any]:
    return {key: scope.get(key) for key in _REPORT_KEYS}


def _response_text_fields(ctx: dict[str, Any], text: str) -> dict[str, Any]:
    response_text = str(ctx.get("response_text") or "")
    partial_json = ctx.get("partial_json")
    repo_root = Path(str(ctx.get("repo_root") or ".")).resolve()
    fields: dict[str, Any] = {
        "response_text_chars": len(response_text),
        "response_text_sha256": text_sha256(response_text),
        "response_text_tail": response_text[-4000:] if response_text else "",
        "response_text_tail_chars": min(len(response_text), 4000),
        "response_text_full_text_in_json": len(response_text) <= INLINE_TEXT_MAX_CHARS,
        "response_text_transport": "inline_small_control",
    }
    if len(response_text) <= INLINE_TEXT_MAX_CHARS:
        fields["response_text"] = response_text
        return fields

    base_dir = (
        Path(str(partial_json)).resolve().parent
        if partial_json
        else repo_root / "output" / "validation"
    )
    evidence = write_large_text_evidence(
        repo_root,
        base_dir / "provider_response_artifacts",
        name="provider_ollama_response",
        text=response_text,
        kind="provider_ollama_response_text",
        producer="provider_ollama_probe",
        suffix=".md",
    )
    fields.update(
        {
            "response_text_ref": evidence.get("ref") or {},
            "response_text_tail": evidence.get("tail") or fields["response_text_tail"],
            "response_text_tail_chars": evidence.get(
                "tail_chars", fields["response_text_tail_chars"]
            ),
            "response_text_full_text_in_json": False,
            "response_text_transport": "artifact_ref",
            "raw_response_chars": len(text.strip()),
        }
    )
    return fields


def build_ollama_probe_report(ctx: dict[str, Any]) -> dict[str, Any]:
    selection = ctx["selection"]
    raw_chat_response = ctx["raw_chat_response"]
    native_tool_calls = ctx["native_tool_calls"]
    text = str(ctx["text"] or "")
    prompt = str(ctx["prompt"] or "")
    prompt_ref = ctx.get("prompt_ref") if isinstance(ctx.get("prompt_ref"), dict) else {}
    partial_json = ctx["partial_json"]
    parsed = ctx["parsed"]
    response_text_fields = _response_text_fields(ctx, text)
    import time

    return {
        "lane": ctx["provider_lane"],
        "role": ctx["provider_role"],
        "passed": ctx["passed"],
        "provider_execution_performed": bool(ctx["provider_execution_performed"]),
        "provider_execution_attempted": bool(ctx["provider_execution_attempted"]),
        "provider_io_observed": bool(ctx["provider_io_observed"]),
        "require_ollama_gpu_residency": bool(ctx["require_gpu_residency"]),
        **ctx["residency"],
        **selection,
        "ollama_ps_snapshots": ctx["ollama_ps_snapshots"],
        **ctx["gpu_runtime_summary"],
        "ollama_residency_verified": bool(ctx["ollama_residency_verified"]),
        "ollama_compute_verified": bool(ctx["ollama_compute_verified"]),
        **ctx["generation_stats"],
        **ctx["replight"],
        **ctx["work_status"],
        "provider_work_verified": bool(ctx["provider_work_verified"]),
        "provider_role_counted": bool(ctx["work_status"].get("provider_role_counted")),
        "replight_mode": bool(ctx["replight_mode"]),
        "elapsed_sec": round(time.perf_counter() - ctx["started"], 4),
        "selected_model": ctx["selected_model"],
        "requested_provider_model": selection.get("requested_provider_model"),
        "selected_provider_model": selection.get("selected_provider_model"),
        "model_switch_reason": selection.get("model_switch_reason"),
        "operator_gpu_observation": ctx["operator_gpu_observation"],
        "num_ctx": ctx["num_ctx"],
        "ollama_gpu_layers_requested": str(ctx["gpu_layers"] or "default"),
        "num_thread": ctx["num_thread"],
        "request_prompt_ref": prompt_ref,
        "request_prompt_chars": len(prompt),
        "request_prompt_sha256": hashlib.sha256(
            prompt.encode("utf-8", errors="replace")
        ).hexdigest(),
        "request_prompt_transport": "artifact_ref" if prompt_ref else "inline_small_control",
        **response_text_fields,
        "raw_response_chars": len(text.strip()),
        "max_new_tokens": ctx["propagated_max_new_tokens"],
        "max_new_tokens_source": "operator_heap_propagated",
        "json_contract_requested": ctx["heap_delta_text_required"],
        "json_contract_passed": bool(parsed.json_ok and isinstance(ctx["parsed_json"], dict)),
        "heap_delta_text_required": ctx["heap_delta_text_required"],
        "heap_delta_text_present": bool(response_text_fields.get("response_text_chars")),
        "provider_output_complete": not ctx["response_likely_incomplete"],
        "response_likely_incomplete": ctx["response_likely_incomplete"],
        "proposal_requires_refinement": ctx["response_likely_incomplete"],
        "tool_calls": native_tool_calls,
        "textual_tool_calls": ctx["textual_tool_calls"],
        "native_tool_loop_provider": "ollama",
        "native_tool_loop_requested": ctx["native_tool_loop_requested"],
        "native_tool_loop_relevant": ctx["native_tool_loop_relevant"],
        "provider_native_tool_api_attempted": ctx["native_tool_api_attempted"],
        "provider_native_tool_api_completed": ctx["native_tool_api_completed"],
        "provider_native_tool_call_required": ctx["provider_native_tool_call_required"],
        "provider_native_tool_api_adapter_available": ctx[
            "provider_native_tool_api_adapter_available"
        ],
        "provider_native_tool_api_supported": ctx["provider_native_tool_api_supported"],
        "provider_native_tool_api_error": ctx["provider_native_tool_api_error"],
        "provider_native_tool_api_attempt_error": ctx[
            "provider_native_tool_api_attempt_error"
        ],
        "provider_native_tool_api_unavailable": ctx["provider_native_tool_api_unavailable"],
        "provider_native_tool_api_attempt_failed": ctx[
            "provider_native_tool_api_attempt_failed"
        ],
        "provider_native_tool_call_required_unmet": ctx["provider_native_tool_call_required_unmet"],
        "native_tool_loop_supported": bool(ctx["provider_native_tool_api_supported"]),
        "native_tool_loop_performed": bool(ctx["native_tool_api_completed"]),
        "native_tool_decision_prompted": ctx["native_tool_decision_prompted"],
        "native_tool_decision": "call_tool" if native_tool_calls else "no_tool_needed",
        "native_tool_loop_classification": ctx["native_classification"],
        "native_tool_call_count": len(native_tool_calls),
        "errors": ctx["errors"],
        "warnings": ctx["warnings"],
        "raw_chat_response_summary": {
            "present": bool(raw_chat_response),
            "native_tool_call_count": len(native_tool_calls),
            "message_present": bool(raw_chat_response.get("message")) if raw_chat_response else False,
        },
        "target_files": [str(item) for item in ctx["target_files"] if str(item).strip()],
        "validation_commands": [
            str(item) for item in ctx["validation_commands"] if str(item).strip()
        ],
        "rejected_validation_refs": [
            str(item) for item in ctx["rejected_validation_refs"] if str(item).strip()
        ],
        "model_count": len(ctx["models"]),
        "server_ready": bool(ctx["server_ready"]),
        "ollama_base_url": ctx["effective_base_url"],
        "ollama_server_process": ctx["server_process"],
        "ollama_unload_performed": bool(ctx["unload_performed"]),
        "ollama_unload_verified": bool(ctx["unload_verified"]),
        "ollama_unload_deferred_until_provider_cleanup": not bool(ctx["unload_model"]),
        "gpu0_vulkan_compute_observed": bool(ctx["gpu0_vulkan_compute_observed"]),
        "gpu0_vulkan_sdk_workload_verified": bool(ctx["gpu0_vulkan_sdk_workload_verified"]),
        "gpu0_vulkan_policy_verified": bool(ctx["gpu0_vulkan_policy_verified"]),
        "ollama_inactivity_unload_seconds": 120,
        "server_ready_for_base_url": bool(ctx["server_ready"]),
        "empty_output": ctx["empty_output"],
        "error": "empty Ollama generation output" if ctx["empty_output"] else None,
        "parsed_result": parsed.to_dict(),
        "prompt_attempts": ctx["prompt_attempts"],
        "partial_output": str(partial_json) if partial_json else "",
    }
