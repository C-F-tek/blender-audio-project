"""Tool-plan construction for the heap runtime gate."""

from __future__ import annotations

from hashlib import sha256

from Tools.ai.heap_gate.runtime_common import Any, repo_rel
from Tools.ai.heap_gate.target_planner import request_focus_text


def bounded_text(value: str, limit: int = 1200) -> str:
    text = " ".join(str(value or "").split())
    return text[:limit]


def request_query(request: str, objective: str) -> str:
    return bounded_text(request_focus_text(request), 1200) or bounded_text(objective, 400)


def request_memory_content(request: str, objective: str, stamp: str) -> str:
    digest = sha256(request.encode("utf-8", errors="replace")).hexdigest() if request else ""
    preview = bounded_text(request, 1000)
    return (
        f"request_sha256={digest}; request_preview={preview}; "
        f"objective={bounded_text(objective, 400)}; stamp={stamp}"
    )


def positive_arg(owner: Any, name: str, default: int) -> int:
    try:
        value = int(getattr(owner.args, name, default) or default)
    except (TypeError, ValueError):
        value = default
    return max(1, value)


def build_tool_plan(owner: Any) -> list[dict[str, Any]]:
    context_dir = owner.runtime_context_dir()
    request = owner.request_text()
    query = request_query(request, owner.args.objective)
    memory_content = request_memory_content(request, owner.args.objective, owner.stamp)
    source_targets = owner.real_source_file_candidates(limit=32)
    memory_limit = positive_arg(owner, "memory_search_limit", 8)
    context_count = positive_arg(owner, "context_document_count", owner.args.max_context_files)
    context_preview = positive_arg(
        owner, "context_document_preview_chars", owner.args.max_chars_per_file
    )
    code_chunk_limit = positive_arg(owner, "semantic_code_chunk_limit", 12)
    code_preview = positive_arg(
        owner, "semantic_code_chunk_preview_chars", owner.args.max_chars_per_file
    )
    startup_text_files: list[str] = []
    operator_request_file = str(getattr(owner.args, "request_file", "") or "").strip()
    if operator_request_file:
        startup_text_files.append(operator_request_file)
    try:
        manifest_path, manifest = owner.startup_manifest_from_task_file()
    except Exception:  # noqa: BLE001 - runtime plan construction must stay non-fatal.
        manifest_path, manifest = None, {}
    if manifest_path:
        startup_text_files.append(repo_rel(owner.repo_root, manifest_path))
    artifacts = manifest.get("artifacts") if isinstance(manifest, dict) else {}
    if isinstance(artifacts, dict):
        for key in (
            "tool_catalog_json",
            "shared_memory_json",
            "operational_memory_search_json",
            "semantic_code_chunks_json",
            "semantic_evidence_chunks_json",
            "ai_context_pack_json",
            "shared_context_json",
            "repo_docs_map_json",
        ):
            value = str(artifacts.get(key) or "").strip()
            if value:
                startup_text_files.append(value)
    runtime_file_ref_args: dict[str, Any] = {
        "text_file": startup_text_files,
        "target_file": source_targets,
        "provenance": "startup_context",
        "strict_patchable_targets": owner.implementation_output_required(),
    }
    runtime_ref_text = []
    if not operator_request_file:
        if query:
            runtime_ref_text.append(query)
        objective = bounded_text(owner.args.objective, 400)
        if objective:
            runtime_ref_text.append(objective)
    if runtime_ref_text:
        runtime_file_ref_args["text"] = runtime_ref_text
    plan = [
        {
            "stage": 1,
            "requirement": "tool_catalog",
            "id": "tool-catalog-inventory",
            "tool": "build_agent_agnostic_tool_inventory",
            "args": {"root": ["tools/ai", "tools/validation", "tools/workflow", "tools/npu"]},
            "reason": "discover allowlisted project tools before deciding product readiness",
        },
        {
            "stage": 1,
            "requirement": "shared_memory",
            "id": "shared-memory-inventory",
            "tool": "build_agent_memory_inventory",
            "args": {"objective": owner.args.objective},
            "reason": "load read-only shared memory state into heap-visible evidence",
        },
        {
            "stage": 1,
            "requirement": "persistent_memory_status",
            "id": "persistent-memory-status",
            "tool": "runtime_sqlite_memory",
            "args": {"action": "status", "scope": "persistent"},
            "reason": "inspect durable SQLite memory state before current-cycle planning",
        },
        {
            "stage": 1,
            "requirement": "persistent_memory_search",
            "id": "persistent-memory-search",
            "tool": "runtime_sqlite_memory",
            "args": {
                "action": "search",
                "scope": "persistent",
                "query": query,
                "limit": memory_limit,
            },
            "reason": "search durable SQLite/FTS memory for prior decisions, targets and blocked products",
        },
        {
            "stage": 1,
            "requirement": "operational_memory_write",
            "id": "operational-memory-write",
            "tool": "runtime_sqlite_memory",
            "args": {
                "action": "remember",
                "scope": "operational",
                "summary": "heap heartbeat request",
                "content": memory_content,
                "role": "heap_runtime_heartbeat",
                "tag": ["heap", "heartbeat", "teamwork"],
            },
            "reason": "write request-scoped operational memory before provider synthesis",
        },
        {
            "stage": 1,
            "requirement": "operational_memory_search",
            "id": "operational-memory-search",
            "tool": "runtime_sqlite_memory",
            "args": {
                "action": "search",
                "scope": "operational",
                "query": query,
                "limit": memory_limit,
            },
            "reason": "read request-scoped operational memory before provider synthesis",
        },
        {
            "stage": 2,
            "requirement": "shared_context_chunks",
            "id": "shared-request-context",
            "tool": "build_agent_transient_request_context",
            "args": {
                "objective": owner.args.objective,
                "memory_note": [
                    "heap runtime completeness gate must prove tool, memory, context, chunks and validation evidence before product signal",
                    "budget/iterations define convergence and prevent endless repository loops",
                    f"user_request_focus={query}",
                ],
                "raw_file": ["AGENTS.md", "README.md", *owner.historical_tool_context_files()],
                "max_raw_files": context_count,
                "max_chars_per_file": context_preview,
            },
            "reason": "materialize request-scoped shared context/chunks from repository policy and historical tool maps",
        },
        {
            "stage": 2,
            "requirement": "semantic_code_chunks",
            "id": "semantic-code-chunk-selection",
            "tool": "select_semantic_code_chunks",
            "args": {
                "query": query,
                "output": repo_rel(owner.repo_root, context_dir / "selected_semantic_code_chunks.json"),
                "markdown_output": repo_rel(owner.repo_root, context_dir / "selected_semantic_code_chunks.md"),
                "max_chunks": code_chunk_limit,
                "max_total_chars": code_chunk_limit * code_preview,
                "max_excerpt_chars": code_preview,
                "path_boost": ["tools/ai", "tools/npu", "tools/workflow"],
            },
            "reason": "select bounded semantic code chunks so provider lanes share connected logical context",
        },
        {
            "stage": 2,
            "requirement": "ai_context_pack",
            "id": "ai-context-pack",
            "tool": "ai_context_pack",
            "args": {
                "profile": "core_ai_backend",
                "basename": f"heap_runtime_context_pack_{owner.stamp}",
                "output_dir": repo_rel(owner.repo_root, context_dir / "ai_context_pack"),
                "evidence_dir": repo_rel(owner.repo_root, context_dir / "ai_context_pack_evidence"),
                "evidence_basename": f"heap_runtime_context_pack_evidence_{owner.stamp}",
                "max_total_chars": context_count * context_preview,
                "max_file_chars": context_preview,
            },
            "reason": "assemble bounded final context pack from stable historical context builder",
        },
        {
            "stage": 2,
            "requirement": "python_line_count_evidence",
            "id": "python-line-count-evidence",
            "tool": "build_python_line_count_csv",
            "args": {"exclude_dir": ["output", "indexAI/code_chunks", "renders"]},
            "reason": "broker existing line-budget evidence so it can be chunked and referenced by the heap",
            "nonblocking": True,
            "post_provider": True,
        },
        {
            "stage": 2,
            "requirement": "python_syntax_evidence",
            "id": "python-syntax-evidence",
            "tool": "check_python_syntax",
            "args": {},
            "reason": "broker existing syntax evidence as runtime context, not as standalone product proof",
            "nonblocking": True,
            "post_provider": True,
        },
        {
            "stage": 2,
            "requirement": "code_interpreter_evidence",
            "id": "code-interpreter-evidence",
            "tool": "build_code_interpreter_report",
            "args": {"input": ["Tools/ai", "Tools/validation", "Tools/workflow", "Tools/npu"]},
            "reason": "broker existing static interpretation evidence for later memory/chunk consumption",
            "nonblocking": True,
            "post_provider": True,
        },
        {
            "stage": 3,
            "requirement": "semantic_evidence_chunks",
            "id": "semantic-evidence-chunk-manifest",
            "tool": "semantic_evidence_chunks",
            "args": {},
            "reason": "chunk oversized context/evidence into linked logical pieces before provider synthesis",
        },
        {
            "stage": 3,
            "requirement": "runtime_file_refs",
            "id": "runtime-file-ref-resolution",
            "tool": "runtime_file_refs",
            "args": runtime_file_ref_args,
            "reason": "resolve operator/startup/provider-visible file refs before provider synthesis and matrix/lab consumption",
        },
        {
            "stage": 3,
            "requirement": "validation_evidence",
            "id": "planner-json-contract-validation",
            "tool": "run_gpu_planner_json_contract_smoke",
            "args": {},
            "reason": "prove validation tool evidence is consumed before arbiter decision",
            "post_provider": True,
        },
        {
            "stage": 3,
            "requirement": "validation_report_contract_evidence",
            "id": "validation-report-contract-evidence",
            "tool": "check_validation_report_contract",
            "args": {},
            "reason": "broker validation-report contract evidence for generated reports without making it the run product",
            "nonblocking": True,
            "post_provider": True,
        },
        {
            "stage": 3,
            "requirement": "refactor_duplication_audit_evidence",
            "id": "refactor-duplication-audit-evidence",
            "tool": "refactor_duplication_audit",
            "args": {"root": ["Tools/ai", "Tools/validation", "Tools/workflow", "Tools/npu"]},
            "reason": "broker existing duplication/refactor evidence for provider and matrix context",
            "nonblocking": True,
            "post_provider": True,
        },
    ]
    if getattr(owner, "provider_reports", []):
        plan.extend(owner.virtual_dev_environment_plan_items(context_dir, request))
        plan.extend(owner.code_execution_matrix_plan_items(context_dir, request))
        plan.extend(owner.runtime_debug_lab_plan_items(context_dir, request))
    return plan
