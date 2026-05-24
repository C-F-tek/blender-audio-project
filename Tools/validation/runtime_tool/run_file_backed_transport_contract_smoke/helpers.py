"""Helpers for the file-backed transport contract smoke."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from ia_carmine._shared.file_backed_transport import (
    artifact_ref,
    compact_text_fields,
    report_text_preview,
    report_text_required_full,
    write_text_evidence_fields,
)


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


def legacy_dispatch_absent_errors() -> list[str]:
    from ia_carmine.dispatch import LEGACY_NON_RUN_UNICA_COMMANDS, TOOL_MAIN_TARGETS
    from Tools.validation.dispatch import (
        LEGACY_NON_RUN_UNICA_VALIDATION_COMMANDS,
        TOOL_MAIN_TARGETS as VALIDATION_TOOL_MAIN_TARGETS,
    )

    old_legacy = {
        "ollama_tool_gateway",
        "gpu_deep_planning_review",
        "gpu_deep_planning_supervised",
        "gpu_npu_parallel_orchestrator",
        "npu_gpu_deep_review_auditor",
        "build_openvino_gpu0_workload_report",
    }
    legacy_names = old_legacy | {
        "legacy_ollama_tool_gateway",
        "legacy_gpu_deep_planning_review",
        "legacy_gpu_deep_planning_supervised",
        "legacy_gpu_npu_parallel_orchestrator",
        "legacy_npu_gpu_deep_review_auditor",
        "legacy_build_openvino_gpu0_workload_report",
    }
    if (
        legacy_names.isdisjoint(set(TOOL_MAIN_TARGETS))
        and not set(LEGACY_NON_RUN_UNICA_COMMANDS)
        and not set(LEGACY_NON_RUN_UNICA_VALIDATION_COMMANDS)
        and "legacy_run_ollama_tool_gateway_smoke" not in set(VALIDATION_TOOL_MAIN_TARGETS)
        and "run_ollama_tool_gateway_smoke" not in set(VALIDATION_TOOL_MAIN_TARGETS)
    ):
        return []
    return ["legacy gateway/deep-planning commands must be absent from live dispatchers"]


def strict_text_accessor_errors(repo_root: Path, smoke_dir: Path) -> list[str]:
    errors: list[str] = []
    full_text = "FULL_REF_SENTINEL\n" + ("complete evidence " * 200)
    fields = write_text_evidence_fields(
        repo_root,
        smoke_dir / "strict_text_artifacts",
        prefix="response_text",
        name="strict_response_text",
        text=full_text,
        kind="strict_response_text",
        producer="file_backed_transport_contract_smoke",
        suffix=".md",
    )
    ref_payload = {
        **fields,
        "response_text_tail": "TAIL_FALSE_SENTINEL",
    }
    strict = report_text_required_full(repo_root, ref_payload)
    preview = report_text_preview(repo_root, ref_payload)
    if strict.get("text") != full_text or preview.get("text") != full_text:
        errors.append("strict/preview accessors must prefer verified ref over false tail")

    tail_only = {
        "response_text_ref": {"path": "output/validation/missing-response.txt", "sha256": "bad"},
        "response_text_sha256": "bad",
        "response_text_tail": "TAIL_ONLY_SHOULD_NOT_PASS",
    }
    strict_tail = report_text_required_full(repo_root, tail_only)
    preview_tail = report_text_preview(repo_root, tail_only)
    if strict_tail.get("text") or not strict_tail.get("reason") or preview_tail.get("text") != "TAIL_ONLY_SHOULD_NOT_PASS":
        errors.append("strict full accessor must reject missing/corrupt refs while preview may use tail")

    compact = compact_text_fields(
        repo_root,
        smoke_dir / "compact_text_artifacts",
        {"response_text": "COMPACT_FULL_SENTINEL\n" + ("x" * 120)},
        ("response_text",),
        name="compact_contract",
        producer="file_backed_transport_contract_smoke",
        kind_prefix="compact_contract",
    )
    compact_strict = report_text_required_full(repo_root, compact)
    if "response_text" in compact or "COMPACT_FULL_SENTINEL" not in str(compact_strict.get("text") or ""):
        errors.append("compact_text_fields must materialize full text before removing inline body")

    ref = artifact_ref(
        (smoke_dir / "strict_text_artifacts" / "strict_response_text.md"),
        repo_root,
        kind="strict_response_text",
        producer="file_backed_transport_contract_smoke",
    )
    if not ref.get("source") or not ref.get("sha256") or not ref.get("bytes"):
        errors.append("artifact_ref must expose source, bytes and sha256 for strict evidence")
    return errors
