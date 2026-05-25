"""Allowlisted broker tool registry."""

from __future__ import annotations

from typing import Any

from ia_carmine._shared.file_backed_transport import MAX_FILE_WINDOW_CHARS

from .common import ToolSpec
from .context_builders import (
    build_ai_context_pack_tool,
    build_rag_context_pack_tool,
    build_semantic_evidence_chunk_manifest,
    run_agent_runtime_debug_lab,
    runtime_sqlite_memory,
)
from .inventory_builders import (
    build_agent_agnostic_tool_inventory,
    build_agent_memory_inventory,
    build_agent_transient_request_context,
    build_code_interpreter_report,
    build_python_line_count_csv,
    build_refactor_duplication_audit,
    build_semantic_code_chunk_selection,
    check_python_syntax,
)
from .runtime_builders import (
    analyze_code_product_artifact,
    generic_write,
    repo_find_fd,
    repo_json_query_jq,
    repo_powershell_readonly,
    repo_search_git_grep,
    repo_search_rg,
    repo_toolchain_command,
    repo_toolchain_probe,
    run_heap_code_execution_matrix,
    run_heap_virtual_dev_environment,
    runtime_file_window,
    runtime_file_refs,
    synthesize_patch_candidates,
)


STRING = {"type": "string"}
OBJECT = {"type": "object"}
STRING_OR_ARRAY = {"type": ["string", "array"]}
BOOL_OR_STRING = {"type": ["boolean", "string"]}
NUMBER_OR_STRING = {"type": ["integer", "number", "string"]}
NUMBER_OR_STRING_FILE_WINDOW_LIMIT = {
    "type": ["integer", "number", "string"],
    "minimum": 1,
    "maximum": MAX_FILE_WINDOW_CHARS,
}


def tool_input_schema(
    properties: dict[str, dict[str, Any]],
    *,
    required: tuple[str, ...] = (),
) -> dict[str, Any]:
    return {
        "type": "object",
        "properties": properties,
        "required": list(required),
        "additionalProperties": False,
    }


DEBUG_LAB_SCHEMA = tool_input_schema(
    {
        "request_file": STRING,
        "request_json": OBJECT,
        "output": STRING,
        "markdown_output": STRING,
        "timeout_seconds": NUMBER_OR_STRING,
        "tail_chars": NUMBER_OR_STRING,
    }
)

CODE_EXECUTION_MATRIX_SCHEMA = tool_input_schema(
    {
        "target_file": STRING_OR_ARRAY,
        "validation_script": STRING_OR_ARRAY,
        "validation_arg": STRING_OR_ARRAY,
        "timeout_seconds": NUMBER_OR_STRING,
        "tail_chars": NUMBER_OR_STRING,
        "max_diff_chars": NUMBER_OR_STRING,
        "operator_request": STRING,
        "operator_request_file": STRING,
        "evidence_report": STRING_OR_ARRAY,
        "synthesize_patch_candidates": BOOL_OR_STRING,
        "force_patch_candidate_synthesis": BOOL_OR_STRING,
        "max_patch_candidates": NUMBER_OR_STRING,
        "no_execute": BOOL_OR_STRING,
    }
)

PATCH_SYNTHESIS_SCHEMA = tool_input_schema(
    {
        "target_file": STRING_OR_ARRAY,
        "operator_request": STRING,
        "operator_request_file": STRING,
        "evidence_report": STRING_OR_ARRAY,
        "matrix_report": STRING,
        "max_candidates": NUMBER_OR_STRING,
        "timeout_seconds": NUMBER_OR_STRING,
    }
)

GENERIC_WRITE_SCHEMA = tool_input_schema(
    {
        "request_file": STRING,
        "operator_request": STRING,
        "provider_report": STRING,
        "proposal_text": STRING,
        "proposal_text_file": STRING,
        "capture_mode": STRING,
        "evidence_report": STRING_OR_ARRAY,
        "source_lane": STRING,
        "source_revision": STRING,
        "gpu1_followup_required": BOOL_OR_STRING,
        "peer_followup_required": BOOL_OR_STRING,
        "provider_role": STRING,
        "reason": STRING,
    }
)

VIRTUAL_DEV_ENVIRONMENT_SCHEMA = tool_input_schema(
    {
        "target_file": STRING_OR_ARRAY,
        "validation_script": STRING_OR_ARRAY,
        "timeout_seconds": NUMBER_OR_STRING,
        "tail_chars": NUMBER_OR_STRING,
        "dynamic_import": BOOL_OR_STRING,
        "help_probe": BOOL_OR_STRING,
    }
)

RUNTIME_FILE_REFS_SCHEMA = tool_input_schema(
    {
        "path": STRING_OR_ARRAY,
        "text": STRING_OR_ARRAY,
        "text_file": STRING_OR_ARRAY,
        "target_file": STRING_OR_ARRAY,
        "validation_script": STRING_OR_ARRAY,
        "provenance": STRING,
        "strict_patchable_targets": BOOL_OR_STRING,
    }
)

RUNTIME_FILE_WINDOW_SCHEMA = tool_input_schema(
    {
        "path": STRING,
        "offset": NUMBER_OR_STRING,
        "limit": NUMBER_OR_STRING_FILE_WINDOW_LIMIT,
    },
    required=("path",),
)

RUNTIME_SQLITE_MEMORY_SCHEMA = tool_input_schema(
    {
        "action": STRING,
        "scope": STRING,
        "database": STRING,
        "persistent_database": STRING,
        "summary": STRING,
        "content_file": STRING,
        "role": STRING,
        "tag": STRING_OR_ARRAY,
        "query": STRING,
        "limit": NUMBER_OR_STRING,
        "confirm": STRING,
        "allow_persistent_write": BOOL_OR_STRING,
    }
)

REPO_TOOLCHAIN_PROBE_SCHEMA = tool_input_schema(
    {
        "tool": STRING_OR_ARRAY,
        "tools": STRING_OR_ARRAY,
        "timeout_seconds": NUMBER_OR_STRING,
    }
)

REPO_TOOLCHAIN_COMMAND_SCHEMA = tool_input_schema(
    {
        "command": STRING,
        "path": STRING,
        "target": STRING,
        "configuration": STRING,
        "timeout_seconds": NUMBER_OR_STRING,
    },
    required=("command",),
)

REPO_SEARCH_SCHEMA = tool_input_schema(
    {
        "query": STRING,
        "pattern": STRING,
        "path": STRING_OR_ARRAY,
        "glob": STRING_OR_ARRAY,
        "max_results": NUMBER_OR_STRING,
        "max_count": NUMBER_OR_STRING,
        "context": NUMBER_OR_STRING,
        "ignore_case": BOOL_OR_STRING,
        "fixed_strings": BOOL_OR_STRING,
        "hidden": BOOL_OR_STRING,
        "timeout_seconds": NUMBER_OR_STRING,
    }
)

REPO_FIND_FD_SCHEMA = tool_input_schema(
    {
        "query": STRING,
        "pattern": STRING,
        "path": STRING,
        "extension": STRING_OR_ARRAY,
        "max_results": NUMBER_OR_STRING,
        "hidden": BOOL_OR_STRING,
        "timeout_seconds": NUMBER_OR_STRING,
    }
)

REPO_JSON_QUERY_JQ_SCHEMA = tool_input_schema(
    {
        "path": STRING,
        "query": STRING,
        "filter": STRING,
        "timeout_seconds": NUMBER_OR_STRING,
    },
    required=("path",),
)

REPO_POWERSHELL_READONLY_SCHEMA = tool_input_schema(
    {
        "operation": STRING,
        "path": STRING,
        "pattern": STRING,
        "filter": STRING,
        "max_results": NUMBER_OR_STRING,
        "recurse": BOOL_OR_STRING,
        "simple_match": BOOL_OR_STRING,
        "timeout_seconds": NUMBER_OR_STRING,
    }
)


TOOL_SPECS: dict[str, ToolSpec] = {
    "build_python_line_count_csv": ToolSpec(
        name="build_python_line_count_csv",
        description="Build full Python line-count CSV/JSON/MD evidence.",
        allowed_args=("exclude_dir",),
        builder=build_python_line_count_csv,
    ),
    "build_agent_memory_inventory": ToolSpec(
        name="build_agent_memory_inventory",
        description="Read-only SQLite/JSONL agent memory inventory.",
        allowed_args=("objective", "memory_db"),
        builder=build_agent_memory_inventory,
    ),
    "build_agent_agnostic_tool_inventory": ToolSpec(
        name="build_agent_agnostic_tool_inventory",
        description="Inventory existing reusable IA-Carmine tools and guardrails.",
        allowed_args=("root",),
        builder=build_agent_agnostic_tool_inventory,
    ),
    "build_agent_transient_request_context": ToolSpec(
        name="build_agent_transient_request_context",
        description="Build request-scoped context from memory notes, raw files and reports.",
        allowed_args=(
            "objective",
            "memory_note",
            "raw_file",
            "report_file",
            "max_raw_files",
            "max_chars_per_file",
        ),
        builder=build_agent_transient_request_context,
    ),
    "check_python_syntax": ToolSpec(
        name="check_python_syntax",
        description="Validate Python syntax across repository.",
        allowed_args=(),
        builder=check_python_syntax,
    ),
    "build_code_interpreter_report": ToolSpec(
        name="build_code_interpreter_report",
        description="Build static code-interpreter style report over selected roots.",
        allowed_args=("input",),
        builder=build_code_interpreter_report,
    ),
    "refactor_duplication_audit": ToolSpec(
        name="refactor_duplication_audit",
        description="Build a report-only duplicated-helper/refactor audit over selected code roots and existing evidence reports.",
        allowed_args=(
            "root",
            "report",
            "input_audit_report",
            "line_count_report",
            "code_interpreter_report",
            "python_syntax_report",
            "bundle_smoke_report",
            "memory_routing_report",
        ),
        builder=build_refactor_duplication_audit,
    ),
    "select_semantic_code_chunks": ToolSpec(
        name="select_semantic_code_chunks",
        description="Select bounded semantic code chunks for provider context from current source or an explicit chunk index.",
        allowed_args=(
            "query",
            "chunks",
            "output",
            "markdown_output",
            "max_chunks",
            "max_total_chars",
            "max_excerpt_chars",
            "path_boost",
            "no_code",
        ),
        builder=build_semantic_code_chunk_selection,
    ),
    "ai_context_pack": ToolSpec(
        name="ai_context_pack",
        description="Build a bounded final AI context pack from stable project profiles.",
        allowed_args=(
            "profile",
            "basename",
            "output_dir",
            "evidence_dir",
            "evidence_basename",
            "max_total_chars",
            "max_file_chars",
            "no_evidence",
        ),
        builder=build_ai_context_pack_tool,
    ),
    "semantic_evidence_chunks": ToolSpec(
        name="semantic_evidence_chunks",
        description="Build linked semantic evidence chunks with previous/next context and deterministic summaries.",
        allowed_args=(
            "basename",
            "source",
            "output_dir",
            "chunk_output_dir",
            "chunk_max_chars",
            "chunk_overlap_lines",
            "zip_output",
        ),
        builder=build_semantic_evidence_chunk_manifest,
    ),
    "rag_context_pack": ToolSpec(
        name="rag_context_pack",
        description="Build a heap-consumable internal RAG context pack from SQLite/FTS5/vector retrieval.",
        allowed_args=(
            "query",
            "task_file",
            "db",
            "top_k",
            "char_budget",
            "embedding_endpoint",
            "embedding_model",
            "skip_query_embedding",
            "allow_missing_query_embedding",
            "allow_empty_results",
        ),
        builder=build_rag_context_pack_tool,
    ),
    "agent_runtime_debug_lab": ToolSpec(
        name="agent_runtime_debug_lab",
        description="Run the controlled report-only Python debug lab with an in-memory or allowlisted request.",
        allowed_args=(
            "request_file",
            "request_json",
            "output",
            "markdown_output",
            "timeout_seconds",
            "tail_chars",
        ),
        builder=run_agent_runtime_debug_lab,
        input_schema=DEBUG_LAB_SCHEMA,
    ),
    "runtime_sqlite_memory": ToolSpec(
        name="runtime_sqlite_memory",
        description="Use protected persistent SQLite read-only or operational scratch SQLite memory under output/**.",
        allowed_args=(
            "action",
            "scope",
            "database",
            "persistent_database",
            "summary",
            "content_file",
            "role",
            "tag",
            "query",
            "limit",
            "confirm",
            "allow_persistent_write",
        ),
        builder=runtime_sqlite_memory,
        input_schema=RUNTIME_SQLITE_MEMORY_SCHEMA,
    ),
    "repo_toolchain_probe": ToolSpec(
        name="repo_toolchain_probe",
        description="Probe concrete local tools available to the repository: rg, fd, jq, PowerShell, dotnet, msbuild, ninja and VS Code CLI.",
        allowed_args=("tool", "tools", "timeout_seconds"),
        builder=repo_toolchain_probe,
        input_schema=REPO_TOOLCHAIN_PROBE_SCHEMA,
    ),
    "repo_toolchain_command": ToolSpec(
        name="repo_toolchain_command",
        description="Run allowlisted concrete toolchain commands only: dotnet_info/build/test, msbuild_version, ninja_version/build, code_version.",
        allowed_args=("command", "path", "target", "configuration", "timeout_seconds"),
        builder=repo_toolchain_command,
        input_schema=REPO_TOOLCHAIN_COMMAND_SCHEMA,
    ),
    "repo_search_rg": ToolSpec(
        name="repo_search_rg",
        description="Search repository text through ripgrep with bounded file-backed output.",
        allowed_args=(
            "query",
            "pattern",
            "path",
            "glob",
            "max_results",
            "max_count",
            "context",
            "ignore_case",
            "fixed_strings",
            "hidden",
            "timeout_seconds",
        ),
        builder=repo_search_rg,
        input_schema=REPO_SEARCH_SCHEMA,
    ),
    "repo_search_git_grep": ToolSpec(
        name="repo_search_git_grep",
        description="Search tracked repository text through git grep with bounded file-backed output.",
        allowed_args=(
            "query",
            "pattern",
            "path",
            "max_results",
            "ignore_case",
            "fixed_strings",
            "timeout_seconds",
        ),
        builder=repo_search_git_grep,
        input_schema=REPO_SEARCH_SCHEMA,
    ),
    "repo_find_fd": ToolSpec(
        name="repo_find_fd",
        description="Discover repository files through fd with bounded file-backed output.",
        allowed_args=("query", "pattern", "path", "extension", "max_results", "hidden", "timeout_seconds"),
        builder=repo_find_fd,
        input_schema=REPO_FIND_FD_SCHEMA,
    ),
    "repo_json_query_jq": ToolSpec(
        name="repo_json_query_jq",
        description="Query repository JSON artifacts/files through jq with bounded file-backed output.",
        allowed_args=("path", "query", "filter", "timeout_seconds"),
        builder=repo_json_query_jq,
        input_schema=REPO_JSON_QUERY_JQ_SCHEMA,
    ),
    "repo_powershell_readonly": ToolSpec(
        name="repo_powershell_readonly",
        description="Run read-only PowerShell Get-ChildItem or Select-String over repo paths; no arbitrary shell command.",
        allowed_args=(
            "operation",
            "path",
            "pattern",
            "filter",
            "max_results",
            "recurse",
            "simple_match",
            "timeout_seconds",
        ),
        builder=repo_powershell_readonly,
        input_schema=REPO_POWERSHELL_READONLY_SCHEMA,
    ),
    "run_heap_code_execution_matrix": ToolSpec(
        name="run_heap_code_execution_matrix",
        description="Generate and execute a guarded compile/test/diff matrix for concrete heap code proposals.",
        allowed_args=(
            "target_file",
            "validation_script",
            "validation_arg",
            "timeout_seconds",
            "tail_chars",
            "max_diff_chars",
            "operator_request",
            "operator_request_file",
            "evidence_report",
            "synthesize_patch_candidates",
            "force_patch_candidate_synthesis",
            "max_patch_candidates",
            "no_execute",
        ),
        builder=run_heap_code_execution_matrix,
        input_schema=CODE_EXECUTION_MATRIX_SCHEMA,
    ),
    "synthesize_patch_candidates": ToolSpec(
        name="synthesize_patch_candidates",
        description="Create artifact-owned validated patch candidates from verified local source targets.",
        allowed_args=(
            "target_file",
            "operator_request",
            "operator_request_file",
            "evidence_report",
            "matrix_report",
            "max_candidates",
            "timeout_seconds",
        ),
        builder=synthesize_patch_candidates,
        input_schema=PATCH_SYNTHESIS_SCHEMA,
    ),
    "generic_write": ToolSpec(
        name="generic_write",
        description="Write report-only refined request/action-plan evidence for the next GPU1 turn when code is not yet safely producible.",
        allowed_args=(
            "request_file",
            "operator_request",
            "provider_report",
            "proposal_text",
            "proposal_text_file",
            "capture_mode",
            "evidence_report",
            "source_lane",
            "source_revision",
            "gpu1_followup_required",
            "peer_followup_required",
            "provider_role",
            "reason",
        ),
        builder=generic_write,
        input_schema=GENERIC_WRITE_SCHEMA,
    ),
    "run_heap_virtual_dev_environment": ToolSpec(
        name="run_heap_virtual_dev_environment",
        description="Probe target scripts in a controlled virtual development environment with AST, import, help, compile and product-check evidence.",
        allowed_args=(
            "target_file",
            "validation_script",
            "timeout_seconds",
            "tail_chars",
            "dynamic_import",
            "help_probe",
        ),
        builder=run_heap_virtual_dev_environment,
        input_schema=VIRTUAL_DEV_ENVIRONMENT_SCHEMA,
    ),
    "runtime_file_refs": ToolSpec(
        name="runtime_file_refs",
        description="Resolve provider/operator file refs into local patchable targets, validation refs and rejected artifact refs.",
        allowed_args=(
            "path",
            "text",
            "text_file",
            "target_file",
            "validation_script",
            "provenance",
            "strict_patchable_targets",
        ),
        builder=runtime_file_refs,
        input_schema=RUNTIME_FILE_REFS_SCHEMA,
    ),
    "runtime_file_window": ToolSpec(
        name="runtime_file_window",
        description="Read a bounded text window from a file-backed runtime artifact by stable path/ref.",
        allowed_args=("path", "offset", "limit"),
        builder=runtime_file_window,
        input_schema=RUNTIME_FILE_WINDOW_SCHEMA,
    ),
    "analyze_code_product_artifact": ToolSpec(
        name="analyze_code_product_artifact",
        description="Analyze CODE_PRODUCT_FULL_PATCH artifacts and optionally apply only safe forward-applicable sections.",
        allowed_args=("code_product", "require_all_integrated", "apply_safe", "confirm"),
        builder=analyze_code_product_artifact,
    ),
}
