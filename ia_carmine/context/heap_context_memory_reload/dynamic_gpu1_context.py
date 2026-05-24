"""Per-run GPU1 dynamic context pack for heap startup reload."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ia_carmine._shared.provider_tool_schemas import (
    broker_tool_api_definitions,
    validate_broker_tool_api_definitions,
)
from ia_carmine.context.heap_context_memory_reload.common import write_json


LAB_TOOL_NAMES = {
    "agent_runtime_debug_lab",
    "run_heap_code_execution_matrix",
    "run_heap_virtual_dev_environment",
    "synthesize_patch_candidates",
    "runtime_file_refs",
}


def build_gpu1_dynamic_context_pack(
    *,
    repo_root: Path,
    output_dir: Path,
    stamp: str,
    artifacts: dict[str, str],
    commands: list[dict[str, Any]],
    request_text: str,
) -> tuple[dict[str, Any], Path, Path]:
    """Write the active GPU1 context artifact for the current run."""
    output_json = output_dir / "startup_gpu1_dynamic_context_pack.json"
    output_md = output_dir / "startup_gpu1_dynamic_context_pack.md"
    tool_definitions = broker_tool_api_definitions()
    tool_validation = validate_broker_tool_api_definitions(tool_definitions)
    selected_refs = _artifact_refs(artifacts)
    capability_map = _capability_map(tool_definitions)
    runtime_file_refs = _runtime_file_refs(artifacts)
    errors: list[str] = []
    if not selected_refs:
        errors.append("gpu1_dynamic_context_pack_has_no_artifact_refs")
    if not tool_validation.get("passed"):
        errors.extend(str(item) for item in tool_validation.get("errors") or [])
    payload: dict[str, Any] = {
        "schema_version": 1,
        "kind": "gpu1_dynamic_context_pack",
        "stamp": stamp,
        "active_context_pack": True,
        "passed": not errors,
        "request_chars": len(request_text or ""),
        "request_preview": (request_text or "")[:1200],
        "artifact_refs": selected_refs,
        "runtime_file_refs": runtime_file_refs,
        "tool_api_contract": {
            "api_native_required": True,
            "textual_tool_calls_are_not_executable": True,
            "provider_textual_tool_call_rejection": "provider_textual_tool_call_not_executable",
            "generic_write_without_native_tool_call_is_raw_gpu1_text_evidence": True,
            "tool_request_counter_source": "broker_request_artifacts_only",
        },
        "tool_definitions": tool_definitions,
        "tool_definition_validation": tool_validation,
        "broker_tool_schema_count": len(tool_definitions),
        "api_native_tool_contract_ready": tool_validation.get("passed") is True,
        "capability_map": capability_map,
        "startup_tool_execution_count": len(commands),
        "side_effect_policy": {
            "provider_source_writes": "forbidden",
            "provider_patch_application": "forbidden",
            "allowed_outputs": "broker_report_artifacts_under_output",
        },
        "missing_value_policy": {
            "optional_missing": "empty_or_null",
            "required_missing": "typed_block_or_exception",
            "placeholder_strings_forbidden": ["not_available", "*_not_available"],
        },
        "errors": errors,
        "warnings": [],
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
    }
    write_json(output_json, payload)
    output_md.write_text(render_gpu1_dynamic_context_markdown(payload), encoding="utf-8")
    return payload, output_json, output_md


def render_gpu1_dynamic_context_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# GPU1 Dynamic Context Pack",
        "",
        f"- Active context pack: `{payload.get('active_context_pack')}`",
        f"- Passed: `{payload.get('passed')}`",
        f"- Tool API contract ready: `{payload.get('api_native_tool_contract_ready')}`",
        f"- Tool definition count: `{payload.get('broker_tool_schema_count')}`",
        f"- Startup tool execution count: `{payload.get('startup_tool_execution_count')}`",
        "",
        "## Runtime Contract",
        "",
        "- GPU1 receives this compact dynamic pack as context.",
        "- Broker tools are exposed through API-ready definitions, not as prose commands.",
        "- Tool/lab/matrix/debug evidence counts only after broker request/result artifacts.",
        "- Textual JSON/Markdown tool calls are classified as `provider_textual_tool_call_not_executable`.",
        "",
        "## Artifact Refs",
        "",
    ]
    for key, value in (payload.get("artifact_refs") or {}).items():
        lines.append(f"- {key}: `{value}`")
    lines.extend(["", "## Capability Map", ""])
    for key, value in (payload.get("capability_map") or {}).items():
        lines.append(f"### {key}")
        for field in ("tool", "prerequisites", "expected_artifacts", "side_effect_policy"):
            lines.append(f"- {field}: `{value.get(field)}`")
        lines.append("")
    lines.extend(["## Tool Definitions", ""])
    for item in payload.get("tool_definitions") or []:
        lines.append(
            "- "
            + f"`{item.get('name')}` "
            + f"policy=`{item.get('side_effect_policy')}` "
            + f"timeout=`{item.get('timeout_seconds')}` "
            + f"artifacts=`{item.get('expected_artifacts')}`"
        )
    errors = payload.get("errors") or []
    if errors:
        lines.extend(["", "## Errors", ""])
        lines.extend(f"- {item}" for item in errors)
    return "\n".join(lines).rstrip() + "\n"


def _artifact_refs(artifacts: dict[str, str]) -> dict[str, str]:
    preferred = (
        "startup_context_pack_json",
        "startup_context_pack_markdown",
        "startup_repo_scan_index_json",
        "tool_catalog_json",
        "tool_catalog_markdown",
        "semantic_code_chunks_json",
        "semantic_evidence_chunks_json",
        "shared_memory_json",
        "operational_memory_status_json",
        "operational_memory_search_json",
        "rag_context_pack_json",
        "ai_context_pack_json",
        "required_context_files_json",
        "repo_docs_map_json",
    )
    return {
        key: str(artifacts.get(key) or "")
        for key in preferred
        if str(artifacts.get(key) or "").strip()
    }


def _runtime_file_refs(artifacts: dict[str, str]) -> dict[str, Any]:
    return {
        "policy": "runtime_file_refs_is_hard_gate_before_provider",
        "source_ref_surfaces": [
            value
            for key, value in artifacts.items()
            if key
            in {
                "startup_repo_scan_index_json",
                "semantic_code_chunks_json",
                "semantic_evidence_chunks_json",
                "repo_docs_map_json",
            }
            and value
        ],
        "no_placeholder_refs": True,
    }


def _capability_map(tool_definitions: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    by_name = {str(item.get("name") or ""): item for item in tool_definitions}
    entries = {
        "runtime_file_refs": "Resolve provider/operator refs before provider product claims.",
        "virtual_dev_environment": "Probe AST/import/help/compile for concrete source targets.",
        "code_execution_matrix": "Execute guarded matrix for verified code proposals.",
        "runtime_debug_lab": "Run report-only Python debug lab.",
        "patch_candidate_synthesis": "Create artifact-owned patch candidates from verified targets.",
    }
    tool_for = {
        "virtual_dev_environment": "run_heap_virtual_dev_environment",
        "code_execution_matrix": "run_heap_code_execution_matrix",
        "runtime_debug_lab": "agent_runtime_debug_lab",
        "patch_candidate_synthesis": "synthesize_patch_candidates",
        "runtime_file_refs": "runtime_file_refs",
    }
    mapped: dict[str, dict[str, Any]] = {}
    for name, description in entries.items():
        tool = tool_for[name]
        definition = by_name.get(tool, {})
        mapped[name] = {
            "description": description,
            "tool": tool,
            "input_schema": definition.get("input_schema") or {},
            "expected_artifacts": definition.get("expected_artifacts") or [],
            "side_effect_policy": definition.get("side_effect_policy") or "",
            "prerequisites": _prerequisites(name),
            "counts_as_called_when": "native_tool_call_and_broker_request_artifact_exist",
            "counts_as_usable_when": "expected_report_written_schema_valid_and_targets_present",
        }
    return mapped


def _prerequisites(name: str) -> list[str]:
    if name == "runtime_file_refs":
        return ["startup_repo_scan_index_json", "semantic_code_chunks_json"]
    if name == "code_execution_matrix":
        return ["runtime_file_refs_passed", "verified_target_files"]
    if name == "virtual_dev_environment":
        return ["verified_target_files"]
    if name == "runtime_debug_lab":
        return ["broker_request_args_schema_valid"]
    return ["verified_target_files", "matrix_or_provider_evidence"]
