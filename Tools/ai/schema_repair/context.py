"""Schema repair context reports and retry prompts."""

from __future__ import annotations

import json
from typing import Any

from .common import (
    RECOMMENDATION_TEMPLATE,
    REQUIRED_TOP_LEVEL_KEYS,
    SCHEMA_REPAIR_CONTEXT_KIND,
    SCHEMA_REPAIR_TRIGGER_REASONS,
    TOOL_REQUEST_TEMPLATE,
)
from .evidence import collect_recent_runtime_tool_evidence, summarize_round_schema_failures

def should_emit_schema_repair_context(
    *,
    rounds: list[dict[str, Any]],
    context_reports: list[dict[str, Any]],
    evidence_ready_for_manual_patch_count: int,
) -> bool:
    """Return true when provider needs stronger schema-repair steering."""

    if evidence_ready_for_manual_patch_count > 0:
        return True
    if collect_recent_runtime_tool_evidence(context_reports, max_reports=1):
        return True
    for item in rounds[-6:]:
        if not isinstance(item, dict):
            continue
        reason = str(item.get("empty_recommendations_reason") or "")
        if reason in SCHEMA_REPAIR_TRIGGER_REASONS:
            return True
        if item.get("model_output_schema_mismatch") or item.get("context_echo_detected"):
            return True
    return False

def build_schema_repair_context_report(
    *,
    provider: str,
    rounds: list[dict[str, Any]],
    context_reports: list[dict[str, Any]],
    evidence_ready_for_manual_patch_count: int,
) -> dict[str, Any]:
    """Build a compact provider-facing schema-repair context report."""

    runtime_evidence = collect_recent_runtime_tool_evidence(context_reports)
    round_failures = summarize_round_schema_failures(rounds)
    has_runtime_evidence = bool(runtime_evidence)
    return {
        "kind": SCHEMA_REPAIR_CONTEXT_KIND,
        "provider": provider,
        "round_index_hint": len(rounds) + 1,
        "evidence_ready_for_manual_patch_count": evidence_ready_for_manual_patch_count,
        "runtime_tool_evidence_available": has_runtime_evidence,
        "runtime_tool_evidence_count": len(runtime_evidence),
        "round_schema_failures": round_failures,
        "runtime_tool_evidence": runtime_evidence,
        "directive": {
            "goal": "Convert available repository/tool evidence into schema-valid recommendations or explicit missing_evidence/tool_requests.",
            "must_not": [
                "Do not summarize the repository.",
                "Do not echo context files, execution plans or tool reports.",
                "Do not return Markdown or fenced code blocks when strict JSON is expected.",
                "Do not leave recommendations empty when evidence is ready unless missing_evidence explains the blocker.",
                "Do not request shell, git write, patch application, Blender runtime, provider execution or persistent memory writes.",
            ],
            "must_do": [
                "Return exactly one JSON object with all required top-level keys.",
                "Use runtime_tool_evidence as evidence, not as text to summarize.",
                "Prefer ready_for_patch_plan recommendations when target_files and validation_commands are known.",
                "When still uncertain, emit broker-compatible tool_requests instead of prose.",
                "Keep each recommendation small enough for manual review.",
            ],
            "required_top_level_keys": REQUIRED_TOP_LEVEL_KEYS,
            "recommendation_template": RECOMMENDATION_TEMPLATE,
            "tool_request_template": TOOL_REQUEST_TEMPLATE,
            "minimum_valid_response_when_ready": {
                "summary": "One sentence technical summary.",
                "confidence": "medium",
                "recommendations": [RECOMMENDATION_TEMPLATE],
                "tool_requests": [],
                "missing_evidence": [],
                "next_best_action": "python -m Tools.ai agent_review_patch_plan",
            },
            "minimum_valid_response_when_blocked": {
                "summary": "One sentence blocker summary.",
                "confidence": "low",
                "recommendations": [],
                "tool_requests": [TOOL_REQUEST_TEMPLATE],
                "missing_evidence": ["specific missing evidence"],
                "next_best_action": "run requested broker tools, then retry schema-valid recommendation generation",
            },
        },
        "decision": {
            "schema_repair_required": True,
            "manual_review_required": True,
            "feed_into_next_provider_round": True,
            "tools_already_executed": has_runtime_evidence,
            "expected_next_layer": "schema-valid recommendations or broker-compatible tool_requests",
        },
        "guardrails": {
            "report_only": True,
            "patch_application_performed": False,
            "provider_execution_performed": False,
            "sqlite_write_performed": False,
            "persistent_memory_write_performed": False,
            "blender_runtime_touched": False,
        },
    }

def build_schema_repair_context_stack(
    *,
    base_context_reports: list[dict[str, Any]],
    rounds: list[dict[str, Any]],
    evidence_ready_for_manual_patch_count: int,
    provider: str,
) -> list[dict[str, Any]]:
    """Return context reports with one fresh schema-repair report appended."""

    clean = [
        item
        for item in base_context_reports
        if not (isinstance(item, dict) and item.get("kind") == SCHEMA_REPAIR_CONTEXT_KIND)
    ]
    if not should_emit_schema_repair_context(
        rounds=rounds,
        context_reports=clean,
        evidence_ready_for_manual_patch_count=evidence_ready_for_manual_patch_count,
    ):
        return clean
    clean.append(
        build_schema_repair_context_report(
            provider=provider,
            rounds=rounds,
            context_reports=clean,
            evidence_ready_for_manual_patch_count=evidence_ready_for_manual_patch_count,
        )
    )
    return clean

def should_attempt_schema_repair_retry(
    *,
    parsed_response: dict[str, Any],
    parse_diagnostics: dict[str, Any],
    evidence_ready_for_manual_patch_count: int,
    valid_tool_request_count: int = 0,
) -> bool:
    """Return true when a repair-only provider pass is worth attempting."""

    if valid_tool_request_count > 0:
        return False
    if not isinstance(parsed_response, dict):
        return True
    recommendations = parsed_response.get("recommendations")
    if isinstance(recommendations, list) and recommendations:
        return False

    if parse_diagnostics.get("context_echo_detected"):
        return True
    if not parse_diagnostics.get("json_ok", True):
        return True
    if parse_diagnostics.get("model_output_schema_mismatch") or not parse_diagnostics.get(
        "schema_ok", False
    ):
        return True
    reason = str(
        parse_diagnostics.get("empty_recommendations_reason")
        or parse_diagnostics.get("contract_empty_recommendations_reason")
        or ""
    )
    if reason in SCHEMA_REPAIR_TRIGGER_REASONS:
        return True
    return evidence_ready_for_manual_patch_count > 0

def build_schema_repair_retry_prompt(
    *,
    provider: str,
    round_index: int,
    objective: str,
    raw_response: str,
    parsed_response: dict[str, Any],
    parse_diagnostics: dict[str, Any],
    context_reports: list[dict[str, Any]],
    rounds: list[dict[str, Any]],
    evidence_ready_for_manual_patch_count: int,
) -> str:
    """Build a strict repair-only prompt for a schema-mismatched provider reply."""

    runtime_evidence = collect_recent_runtime_tool_evidence(
        context_reports, max_reports=8, max_results_per_report=6
    )
    round_failures = summarize_round_schema_failures(rounds)
    payload = {
        "kind": "schema_repair_retry_prompt",
        "provider": provider,
        "round_index": round_index,
        "objective": objective,
        "task": "Repair the previous provider response into one valid JSON object only.",
        "hard_rules": [
            "Return JSON only: no Markdown, no prose, no fenced code block.",
            "Use exactly the required top-level keys.",
            "Do not echo files, docs, tool reports, or context previews.",
            "If runtime evidence is enough, produce at least one ready_for_patch_plan recommendation.",
            "If runtime evidence is not enough, recommendations must be empty and tool_requests or missing_evidence must explain the blocker.",
            "Do not request shell, git write, patch application, Blender runtime, provider execution, or persistent memory writes.",
            "Every recommendation must be small, manually reviewable, evidence-backed and non-destructive.",
        ],
        "required_top_level_keys": REQUIRED_TOP_LEVEL_KEYS,
        "recommendation_template": RECOMMENDATION_TEMPLATE,
        "tool_request_template": TOOL_REQUEST_TEMPLATE,
        "minimum_valid_response_when_ready": {
            "summary": "One sentence technical summary.",
            "confidence": "medium",
            "recommendations": [RECOMMENDATION_TEMPLATE],
            "tool_requests": [],
            "missing_evidence": [],
            "next_best_action": "python -m Tools.ai agent_review_patch_plan",
        },
        "minimum_valid_response_when_blocked": {
            "summary": "One sentence blocker summary.",
            "confidence": "low",
            "recommendations": [],
            "tool_requests": [TOOL_REQUEST_TEMPLATE],
            "missing_evidence": ["specific missing evidence"],
            "next_best_action": "run requested broker tools, then retry schema-valid recommendation generation",
        },
        "evidence_ready_for_manual_patch_count": evidence_ready_for_manual_patch_count,
        "parse_diagnostics": {
            "json_ok": parse_diagnostics.get("json_ok"),
            "schema_ok": parse_diagnostics.get("schema_ok"),
            "schema_errors": parse_diagnostics.get("schema_errors", []),
            "context_echo_detected": parse_diagnostics.get("context_echo_detected"),
            "model_output_schema_mismatch": parse_diagnostics.get("model_output_schema_mismatch"),
            "empty_recommendations_reason": parse_diagnostics.get("empty_recommendations_reason")
            or parse_diagnostics.get("contract_empty_recommendations_reason"),
        },
        "round_failures": round_failures,
        "runtime_tool_evidence": runtime_evidence,
        "bad_response": {
            "raw_preview": raw_response[:4000],
            "parsed_keys": (
                sorted(parsed_response.keys()) if isinstance(parsed_response, dict) else []
            ),
            "parsed_response": parsed_response,
        },
        "output_contract": {
            "summary": "string",
            "confidence": "low|medium|high",
            "recommendations": [RECOMMENDATION_TEMPLATE],
            "tool_requests": [TOOL_REQUEST_TEMPLATE],
            "missing_evidence": ["string"],
            "next_best_action": "string",
        },
    }
    import json

    return (
        "You are a strict JSON repair adapter inside IA-Carmine. "
        "Repair the previous provider response into schema-valid planner JSON. "
        "Do not perform new analysis beyond the supplied evidence.\n\n"
        + json.dumps(payload, indent=2, ensure_ascii=False)
    )

def summarize_schema_repair_retry(attempt: dict[str, Any]) -> dict[str, Any]:
    """Return compact telemetry for a repair attempt."""

    return {
        "attempted": bool(attempt.get("attempted")),
        "accepted": bool(attempt.get("accepted")),
        "reason": attempt.get("reason", ""),
        "json_ok": attempt.get("parse_diagnostics", {}).get("json_ok"),
        "schema_ok": attempt.get("parse_diagnostics", {}).get("schema_ok"),
        "recommendation_count": attempt.get("recommendation_diagnostics", {}).get(
            "recommendation_count", 0
        ),
        "valid_tool_request_count": attempt.get("parse_diagnostics", {}).get(
            "valid_tool_request_count", 0
        ),
        "empty_recommendations_reason": attempt.get("recommendation_diagnostics", {}).get(
            "empty_recommendations_reason", ""
        ),
    }
