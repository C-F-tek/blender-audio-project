"""Helpers for the file-backed transport contract smoke."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path


class ParsedSmokeJson:
    json_ok = True

    def to_dict(self) -> dict[str, object]:
        return {"ok": True}


def fake_ollama_report_context(
    repo_root: Path, prompt: str, response_text: str = "response"
) -> dict[str, object]:
    partial_json = (
        repo_root
        / "output"
        / "validation"
        / "file_backed_transport_contract_smoke"
        / "fake_provider.json"
    )
    return {
        "selection": {"requested_provider_model": "fake", "selected_provider_model": "fake"},
        "raw_chat_response": {},
        "native_tool_calls": [],
        "text": response_text,
        "prompt": prompt,
        "prompt_ref": {
            "path": "output/validation/fake_prompt.md",
            "bytes": len(prompt),
            "sha256": "fake",
            "source": "smoke",
        },
        "repo_root": str(repo_root),
        "partial_json": str(partial_json),
        "parsed": ParsedSmokeJson(),
        "provider_lane": "gpu1_planner",
        "provider_role": "planner",
        "passed": True,
        "provider_execution_performed": True,
        "provider_execution_attempted": True,
        "provider_io_observed": True,
        "require_gpu_residency": False,
        "residency": {"provider_device_verified": True, "ollama_full_gpu_verified": True},
        "ollama_ps_snapshots": [],
        "gpu_runtime_summary": {},
        "ollama_residency_verified": True,
        "ollama_compute_verified": True,
        "generation_stats": {"eval_count": 1, "prompt_eval_count": 1, "done": True},
        "replight": {"replight_passed": True, "replight_blocked_reason": ""},
        "work_status": {"provider_role_counted": True},
        "provider_work_verified": True,
        "replight_mode": False,
        "started": datetime.now().timestamp(),
        "selected_model": "fake",
        "operator_gpu_observation": "",
        "num_ctx": 16384,
        "gpu_layers": "all",
        "num_thread": None,
        "response_text": response_text,
        "propagated_max_new_tokens": 64,
        "heap_delta_text_required": False,
        "parsed_json": {"ok": True},
        "response_likely_incomplete": False,
        "textual_tool_calls": [],
        "native_tool_loop_requested": False,
        "native_tool_loop_relevant": False,
        "native_tool_api_attempted": False,
        "native_tool_api_completed": False,
        "provider_native_tool_call_required": False,
        "provider_native_tool_api_adapter_available": True,
        "provider_native_tool_api_supported": True,
        "provider_native_tool_api_error": "",
        "provider_native_tool_api_attempt_error": "",
        "provider_native_tool_api_unavailable": False,
        "provider_native_tool_api_attempt_failed": False,
        "provider_native_tool_call_required_unmet": False,
        "native_tool_decision_prompted": False,
        "native_classification": "smoke",
        "errors": [],
        "warnings": [],
        "target_files": [],
        "validation_commands": [],
        "rejected_validation_refs": [],
        "models": ["fake"],
        "server_ready": True,
        "effective_base_url": "http://127.0.0.1:11434",
        "server_process": {},
        "unload_model": False,
        "unload_performed": False,
        "unload_verified": False,
        "gpu0_vulkan_compute_observed": False,
        "gpu0_vulkan_sdk_workload_verified": False,
        "gpu0_vulkan_policy_verified": False,
        "empty_output": False,
        "prompt_attempts": [],
    }
