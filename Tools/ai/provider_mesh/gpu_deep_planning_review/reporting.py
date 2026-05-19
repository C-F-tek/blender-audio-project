from __future__ import annotations

from .common import *  # noqa: F403

def merge_recommendations(rounds: list[dict[str, Any]]) -> list[dict[str, Any]]:
    merged: list[dict[str, Any]] = []
    seen: set[str] = set()
    for round_result in rounds:
        parsed = round_result.get("parsed_response") or {}
        for rec in parsed.get("recommendations", []) if isinstance(parsed, dict) else []:
            if not isinstance(rec, dict):
                continue
            if validate_recommendation_object(rec, len(merged)):
                continue
            key = json.dumps(
                [
                    rec.get("area"),
                    rec.get("status"),
                    rec.get("target_files"),
                    rec.get("proposed_strategy"),
                ],
                sort_keys=True,
                ensure_ascii=False,
            )
            if key in seen:
                continue
            seen.add(key)
            merged.append(rec)
    return merged
def build_markdown(report: dict[str, Any]) -> str:
    lines = ["# Agent GPU Deep Planning Review", ""]
    lines.append(f"- Passed: `{report['passed']}`")
    lines.append(f"- Provider execution performed: `{report['provider_execution_performed']}`")
    lines.append(f"- Patch application performed: `{report['patch_application_performed']}`")
    lines.append(f"- Model: `{report.get('model_used')}`")
    lines.append(f"- Elapsed seconds: `{report['elapsed_seconds']}`")
    lines.append(f"- Round count: `{report['round_count']}`")
    lines.append(f"- Recommendation count: `{report['recommendation_count']}`")
    lines.append(
        f"- Raw recommendation candidates: `{report.get('raw_recommendation_candidate_count')}`"
    )
    lines.append(
        f"- Filtered recommendation count: `{report.get('filtered_recommendation_count')}`"
    )
    lines.append(f"- Tool request count: `{report.get('tool_request_count')}`")
    lines.append(f"- Valid tool request count: `{report.get('valid_tool_request_count')}`")
    lines.append(f"- Invalid tool request count: `{report.get('invalid_tool_request_count')}`")
    lines.append(f"- JSON parse error count: `{report.get('json_parse_error_count')}`")
    lines.append(f"- Context echo detected count: `{report.get('context_echo_detected_count')}`")
    lines.append(
        f"- Model output schema mismatch count: `{report.get('model_output_schema_mismatch_count')}`"
    )
    lines.append(f"- Empty recommendations reason: `{report.get('empty_recommendations_reason')}`")
    lines.append(
        f"- Evidence ready for manual patch count: `{report.get('evidence_ready_for_manual_patch_count')}`"
    )
    lines.append("")
    lines.append("## Decision")
    lines.append("")
    for key, value in report.get("decision", {}).items():
        lines.append(f"- `{key}`: `{value}`")
    lines.append("")
    lines.append("## Recommendations")
    lines.append("")
    for rec in report.get("recommendations", []):
        lines.append(f"### {rec.get('id', 'recommendation')} — {rec.get('area')}")
        lines.append(f"- Status: `{rec.get('status')}`")
        lines.append(f"- Risk: `{rec.get('risk')}`")
        lines.append(f"- Target files: `{rec.get('target_files')}`")
        lines.append(f"- Rationale: {rec.get('rationale')}")
        lines.append(f"- Strategy: {rec.get('proposed_strategy')}")
        lines.append("")
    return "\n".join(lines) + "\n"
