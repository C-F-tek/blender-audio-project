"""Tool-plan construction for the heap runtime gate."""

from __future__ import annotations

from Tools.ai.heap_gate.runtime_common import Any, repo_rel


def build_tool_plan(owner: Any) -> list[dict[str, Any]]:
    context_dir = owner.runtime_context_dir()
    request = owner.request_text()
    query = request or owner.args.objective
    memory_content = f"request={request}; objective={owner.args.objective}; stamp={owner.stamp}"
    return [
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
            "args": {"action": "search", "scope": "operational", "query": query, "limit": 5},
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
                    f"user_request={request}",
                ],
                "raw_file": ["AGENTS.md", "README.md", *owner.historical_tool_context_files()],
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
                "max_chunks": 12,
                "max_total_chars": min(int(owner.args.max_context_files) * 500, 24000),
                "max_excerpt_chars": min(int(owner.args.max_chars_per_file), 3000),
                "path_boost": ["tools/ai", "tools/npu", "tools/workflow"],
            },
            "reason": "select bounded semantic code chunks so provider lanes share connected logical context",
        },
        {
            "stage": 2,
            "requirement": "ai_context_pack",
            "id": "ai-context-pack",
            "tool": "build_ai_context_pack",
            "args": {
                "profile": "core_ai_backend",
                "basename": f"heap_runtime_context_pack_{owner.stamp}",
                "output_dir": repo_rel(owner.repo_root, context_dir / "ai_context_pack"),
                "evidence_dir": repo_rel(owner.repo_root, context_dir / "ai_context_pack_evidence"),
                "evidence_basename": f"heap_runtime_context_pack_evidence_{owner.stamp}",
                "max_total_chars": min(
                    int(owner.args.max_context_files) * int(owner.args.max_chars_per_file),
                    96000,
                ),
                "max_file_chars": int(owner.args.max_chars_per_file),
            },
            "reason": "assemble bounded final context pack from stable historical context builder",
        },
        {
            "stage": 3,
            "requirement": "semantic_evidence_chunks",
            "id": "semantic-evidence-chunk-manifest",
            "tool": "build_semantic_evidence_chunks",
            "args": {},
            "reason": "chunk oversized context/evidence into linked logical pieces before provider synthesis",
        },
        {
            "stage": 3,
            "requirement": "validation_evidence",
            "id": "planner-json-contract-validation",
            "tool": "run_gpu_planner_json_contract_smoke",
            "args": {},
            "reason": "prove validation tool evidence is consumed before arbiter decision",
        },
        *owner.virtual_dev_environment_plan_items(context_dir, request),
        *owner.code_execution_matrix_plan_items(context_dir, request),
        *owner.runtime_debug_lab_plan_items(context_dir, request),
    ]
