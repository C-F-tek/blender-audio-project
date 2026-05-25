"""Broker tool schema helpers shared by provider lanes."""

from __future__ import annotations

import json
from typing import Any

from ia_carmine.runtime.runtime_tool.broker.common import default_input_schema

API_NATIVE_TOOL_CALL_SHAPES = {
    ("ollama", "ollama-python.message.tool_calls[].function"),
    ("ollama", "ollama-qwen-template.content.<tool_call>"),
    ("ollama", "ollama-qwen2.5-coder.chat_tools.content_json_adapter"),
}


def provider_tool_protocol(model: str = "") -> dict[str, Any]:
    normalized = (model or "").lower()
    if "qwen3-coder" in normalized:
        return {
            "model_family": "qwen3-coder",
            "allow_template_adapter": False,
            "allow_content_json_adapter": False,
            "accepted_shapes": {("ollama", "ollama-python.message.tool_calls[].function")},
        }
    if "qwen2.5-coder" in normalized or "qwen2.5" in normalized:
        return {
            "model_family": "qwen2.5-coder",
            "allow_template_adapter": True,
            "allow_content_json_adapter": True,
            "accepted_shapes": API_NATIVE_TOOL_CALL_SHAPES,
        }
    return {
        "model_family": "default-native-only",
        "allow_template_adapter": False,
        "allow_content_json_adapter": False,
        "accepted_shapes": {("ollama", "ollama-python.message.tool_calls[].function")},
    }


def is_api_native_tool_call(call: dict[str, Any], *, lane: str = "", model: str = "") -> bool:
    """Return true only for provider API tool-call objects, not text JSON."""
    provider = str(call.get("native_provider") or "").strip()
    shape = str(call.get("native_shape") or "").strip()
    accepted = provider_tool_protocol(model).get("accepted_shapes") or API_NATIVE_TOOL_CALL_SHAPES
    if (provider, shape) in accepted:
        return True
    if lane == "npu_micro_task_auditor" and provider == "openvino_genai":
        return False
    return False


def broker_tool_schemas(
    tool_names: list[str] | tuple[str, ...] | None = None,
    *,
    compact: bool = False,
) -> list[dict[str, Any]]:
    try:
        from ia_carmine.runtime.runtime_tool.broker.registry import TOOL_SPECS
    except ImportError:  # pragma: no cover
        from ia_carmine.runtime.runtime_tool.broker.registry import TOOL_SPECS  # type: ignore

    allowed = set(tool_names or [])
    schemas: list[dict[str, Any]] = []
    for name, spec in sorted(TOOL_SPECS.items()):
        if allowed and name not in allowed:
            continue
        input_schema = (
            spec.input_schema
            if getattr(spec, "input_schema", None) and not compact
            else _input_schema(spec.allowed_args, compact=compact)
        )
        schemas.append(
            {
                "type": "function",
                "function": {
                    "name": name,
                    "description": "IA-Carmine broker tool." if compact else spec.description,
                    "parameters": input_schema,
                },
            }
        )
    return schemas


def broker_tool_api_definitions(
    tool_names: list[str] | tuple[str, ...] | None = None,
    *,
    compact: bool = False,
) -> list[dict[str, Any]]:
    """Return broker tools in the runtime API contract shape.

    These definitions are separate from the provider SDK `tools=` payload above:
    startup and packet reports use them to prove that published tools are
    registry-backed, schema-serializable and lane-scoped before GPU1 sees them.
    """
    try:
        from ia_carmine.runtime.runtime_tool.broker.registry import TOOL_SPECS
    except ImportError:  # pragma: no cover
        from ia_carmine.runtime.runtime_tool.broker.registry import TOOL_SPECS  # type: ignore

    allowed = set(tool_names or [])
    definitions: list[dict[str, Any]] = []
    for name, spec in sorted(TOOL_SPECS.items()):
        if allowed and name not in allowed:
            continue
        input_schema = (
            spec.input_schema
            if getattr(spec, "input_schema", None) and not compact
            else _input_schema(spec.allowed_args, compact=compact)
        )
        definition = {
            "name": name,
            "description": spec.description,
            "input_schema": input_schema,
            "side_effect_policy": _side_effect_policy(name),
            "expected_artifacts": _expected_artifacts(name),
            "timeout_seconds": _timeout_seconds(name),
            "lane_permissions": _lane_permissions(name),
            "transport_policy": _transport_policy(name),
            "handler_resolvable": callable(getattr(spec, "builder", None)),
            "schema_serializable": _json_schema_serializable(input_schema),
        }
        definitions.append(definition)
    return definitions


def validate_broker_tool_api_definitions(
    definitions: list[dict[str, Any]],
) -> dict[str, Any]:
    errors: list[str] = []
    for item in definitions:
        name = str(item.get("name") or "").strip()
        if not name:
            errors.append("tool_definition_missing_name")
        if not isinstance(item.get("input_schema"), dict):
            errors.append(f"{name}:input_schema_missing")
        elif not item.get("schema_serializable"):
            errors.append(f"{name}:input_schema_not_serializable")
        if not item.get("handler_resolvable"):
            errors.append(f"{name}:handler_not_resolvable")
        if not item.get("expected_artifacts"):
            errors.append(f"{name}:expected_artifacts_missing")
        if not item.get("lane_permissions"):
            errors.append(f"{name}:lane_permissions_missing")
    return {
        "passed": not errors,
        "tool_definition_count": len(definitions),
        "errors": errors,
    }


def _input_schema(args: tuple[str, ...], *, compact: bool) -> dict[str, Any]:
    if compact:
        return {"type": "object", "properties": {}, "additionalProperties": False}
    schema = default_input_schema(args)
    for arg, field in schema.get("properties", {}).items():
        if isinstance(field, dict):
            field["description"] = f"Broker-validated argument `{arg}`."
    return schema


def _side_effect_policy(name: str) -> str:
    read_only = {
        "build_agent_memory_inventory",
        "build_agent_agnostic_tool_inventory",
        "build_agent_transient_request_context",
        "check_python_syntax",
        "select_semantic_code_chunks",
        "runtime_file_window",
        "runtime_file_refs",
        "repo_toolchain_probe",
        "repo_toolchain_command",
        "repo_search_rg",
        "repo_search_git_grep",
        "repo_find_fd",
        "repo_json_query_jq",
        "repo_powershell_readonly",
    }
    source_forbidden = {"analyze_code_product_artifact"}
    if name in source_forbidden:
        return "source_write_forbidden"
    if name in read_only:
        return "read_only"
    return "writes_artifact"


def _expected_artifacts(name: str) -> list[str]:
    if name == "runtime_file_refs":
        return ["runtime_file_refs_json", "runtime_file_refs_markdown"]
    if name == "runtime_file_window":
        return ["runtime_file_window_json", "runtime_file_window_markdown"]
    if name in {
        "repo_toolchain_probe",
        "repo_toolchain_command",
        "repo_search_rg",
        "repo_search_git_grep",
        "repo_find_fd",
        "repo_json_query_jq",
        "repo_powershell_readonly",
    }:
        return [f"{name}_json", f"{name}_markdown"]
    if name == "run_heap_code_execution_matrix":
        return ["code_execution_matrix_json", "code_execution_matrix_markdown"]
    if name == "run_heap_virtual_dev_environment":
        return ["virtual_dev_environment_json", "virtual_dev_environment_markdown"]
    if name == "agent_runtime_debug_lab":
        return ["runtime_debug_lab_json", "runtime_debug_lab_markdown"]
    if name == "synthesize_patch_candidates":
        return ["patch_candidate_synthesis_json", "patch_candidate_synthesis_markdown"]
    if name == "generic_write":
        return ["generic_write_json", "generic_write_markdown"]
    return [f"{name}_json", f"{name}_markdown"]


def _timeout_seconds(name: str) -> int:
    if name in {"run_heap_code_execution_matrix", "run_heap_virtual_dev_environment"}:
        return 120
    if name in {"agent_runtime_debug_lab", "synthesize_patch_candidates"}:
        return 90
    return 60


def _transport_policy(name: str) -> dict[str, Any]:
    blob_args = {
        "agent_runtime_debug_lab": ["request_json"],
        "run_heap_code_execution_matrix": ["operator_request"],
        "synthesize_patch_candidates": ["operator_request"],
        "generic_write": ["operator_request", "proposal_text"],
        "runtime_file_refs": ["text"],
    }.get(name, [])
    artifact_args = {
        "agent_runtime_debug_lab": ["request_file"],
        "run_heap_code_execution_matrix": ["operator_request_file", "evidence_report"],
        "synthesize_patch_candidates": ["operator_request_file", "evidence_report", "matrix_report"],
        "generic_write": ["request_file", "proposal_text_file", "provider_report", "evidence_report"],
        "runtime_file_refs": ["text_file", "target_file", "validation_script"],
        "runtime_file_window": ["path", "ref_id", "startup_manifest"],
        "repo_search_rg": ["path"],
        "repo_search_git_grep": ["path"],
        "repo_find_fd": ["path"],
        "repo_json_query_jq": ["path"],
        "repo_powershell_readonly": ["path"],
        "repo_toolchain_command": ["path", "target"],
    }.get(name, [])
    return {
        "principle": "http_coordinates_filesystem_transports_mass",
        "large_payload_transport": "artifact_ref_or_payload_file",
        "inline_arg_max_bytes": 16000,
        "forbidden_inline_blob_args": blob_args,
        "artifact_ref_args": artifact_args,
        "responses_return_paths_not_large_blobs": True,
    }


def _lane_permissions(name: str) -> dict[str, str]:
    permissions = {
        "gpu1_planner": "operative_broker_request_allowed",
        "gpu0_peer": "peer_evidence_only_requires_later_gpu1_consumption",
        "npu_micro_task_auditor": "diagnostic_only_no_product_close",
    }
    if name == "analyze_code_product_artifact":
        permissions["gpu1_planner"] = "report_only_apply_forbidden_without_boundary"
    return permissions


def _json_schema_serializable(schema: dict[str, Any]) -> bool:
    try:
        json.dumps(schema, ensure_ascii=False)
    except TypeError:
        return False
    return True
