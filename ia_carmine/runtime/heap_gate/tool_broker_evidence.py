"""Evidence source selection for heap broker context chunking."""

from __future__ import annotations

from ia_carmine.runtime.heap_gate.runtime_common import Any, safe_int

CHUNKABLE_REQUIREMENTS = {
    "shared_context_chunks",
    "semantic_code_chunks",
    "ai_context_pack",
    "persistent_memory_search",
    "operational_memory_search",
    "python_line_count_evidence",
    "python_syntax_evidence",
    "code_interpreter_evidence",
    "tool_evidence_memory_write",
    "runtime_file_refs",
    "refactor_duplication_audit_evidence",
}


def semantic_evidence_sources(owner: Any, events: list[dict[str, Any]]) -> list[str]:
    sources: list[str] = []
    for payload in owner.broker_results(events):
        requirement = str(
            payload.get("requirement")
            or owner.requirement_for_tool(str(payload.get("tool") or ""))
        )
        if requirement not in CHUNKABLE_REQUIREMENTS:
            continue
        outputs = payload.get("outputs") if isinstance(payload.get("outputs"), dict) else {}
        for key in ("json_report", "markdown_report", "evidence_json", "evidence_markdown"):
            value = str(outputs.get(key) or "").strip()
            if value and value not in sources:
                sources.append(value)
    limit = max(1, safe_int(getattr(owner.args, "semantic_evidence_chunk_limit", 8), 8))
    return sources[:limit]
