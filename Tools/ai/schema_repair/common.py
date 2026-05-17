"""Shared constants for schema repair context."""

from __future__ import annotations

from typing import Any

SCHEMA_REPAIR_CONTEXT_KIND = "schema_repair_provider_context"
SCHEMA_REPAIR_TRIGGER_REASONS = {
    "context_echo_detected",
    "json_parse_failure",
    "model_output_schema_mismatch",
    "valid_json_empty_recommendations",
    "recommendations_filtered_out",
    "evidence_ready_but_no_gpu_plan",
    "evidence_ready_but_no_tool_requests",
    "model_output_missing_required_fields",
    "repair_attempt_failed",
    "tool_requests_pending",
}
REQUIRED_TOP_LEVEL_KEYS = [
    "summary",
    "confidence",
    "recommendations",
    "tool_requests",
    "missing_evidence",
    "next_best_action",
]
RECOMMENDATION_TEMPLATE = {
    "id": "rec_short_snake_case_id",
    "area": "doc_code|doc_doc|code_code|workflow|validation|other",
    "status": "ready_for_patch_plan|needs_more_context|advisory_only",
    "target_files": ["relative/path.ext"],
    "rationale": "evidence-backed technical reason",
    "proposed_strategy": "small manual-review patch strategy",
    "risk": "low|medium|high",
    "validation_commands": ["command that does not apply patches or run Blender"],
    "stop_conditions": ["condition requiring human/manual review"],
}
TOOL_REQUEST_TEMPLATE = {
    "id": "need_specific_evidence",
    "tool": "allowlisted_runtime_tool_name",
    "reason": "specific missing evidence needed before deciding",
    "args": {},
}

def _as_int(value: Any) -> int:
    try:
        return int(value or 0)
    except (TypeError, ValueError):
        return 0

def _compact_tool_result(result: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": result.get("id"),
        "tool": result.get("tool"),
        "executed": result.get("executed"),
        "blocked": result.get("blocked"),
        "returncode": result.get("returncode"),
        "outputs": result.get("outputs", {}),
        "summary": result.get("summary", {}),
        "guardrails": result.get("guardrails", {}),
        "errors": result.get("errors", []),
    }
