"""Patch-note generation and quality scoring."""

from __future__ import annotations

from typing import Any

from Tools.ai.patch_product.patch_plan_quality_product.scoring import list_plans

from .scoring_common import _text, _unique_strings, safe_dict, safe_list

def _canonical_note_area(area: Any) -> str:
    aliases = {
        "md_md": "doc_doc",
        "markdown_markdown": "doc_doc",
        "doc_code": "doc_python",
        "md_python": "doc_python",
        "md_powershell": "doc_python",
        "python_validation": "python_doc",
        "repository_consistency": "refactor_candidate",
    }
    value = str(area or "").strip()
    return aliases.get(value, value)


def _area_diverse_plans(plans: list[dict[str, Any]], limit: int) -> list[dict[str, Any]]:
    preferred_areas = [
        "python_python",
        "doc_python",
        "doc_doc",
        "python_doc",
        "policy_violation",
        "refactor_candidate",
        "telemetry_gap",
        "evidence_gap",
    ]
    by_area: dict[str, list[dict[str, Any]]] = {area: [] for area in preferred_areas}
    other: list[dict[str, Any]] = []
    for plan in plans:
        area = _canonical_note_area(plan.get("area"))
        if area in by_area:
            by_area[area].append(plan)
        else:
            other.append(plan)
    selected: list[dict[str, Any]] = []
    # Coverage-first: include one item per available preferred area before filling
    # the remaining window. This prevents a valid ALL_ALL area from disappearing
    # when the final patch-note limit is lower than the upstream patch-plan count.
    for area in preferred_areas:
        bucket = by_area[area]
        if bucket and len(selected) < limit:
            selected.append(bucket.pop(0))
    while len(selected) < limit and any(by_area.values()):
        for area in preferred_areas:
            bucket = by_area[area]
            if bucket and len(selected) < limit:
                selected.append(bucket.pop(0))
    for plan in other:
        if len(selected) >= limit:
            break
        selected.append(plan)
    return selected


def build_patch_notes(
    patch_plan: dict[str, Any], patch_quality: dict[str, Any], limit: int = 20
) -> list[dict[str, Any]]:
    quality_scores = {}
    for item in safe_list(safe_dict(patch_quality.get("quality")).get("plan_scores")):
        if isinstance(item, dict):
            quality_scores[str(item.get("id") or "")] = item
    notes: list[dict[str, Any]] = []
    selected_plans = _area_diverse_plans(
        [plan for plan in list_plans(patch_plan) if isinstance(plan, dict)], limit
    )
    for index, plan in enumerate(selected_plans, 1):
        plan_id = str(plan.get("id") or plan.get("title") or f"plan_{index:03d}")
        score = quality_scores.get(plan_id, {})
        notes.append(
            {
                "id": plan_id,
                "area": _canonical_note_area(plan.get("area")),
                "status": plan.get("status"),
                "target_files": _unique_strings(safe_list(plan.get("target_files")), limit=12),
                "summary": _text(plan.get("rationale") or plan.get("edit_strategy"), 700),
                "edit_strategy": _text(plan.get("edit_strategy"), 700),
                "quality_score": score.get("score"),
                "quality_notes": safe_list(score.get("notes"))[:8],
                "validation_commands": _unique_strings(
                    safe_list(plan.get("validation_commands")), limit=8
                ),
                "stop_conditions": _unique_strings(safe_list(plan.get("stop_conditions")), limit=8),
                "manual_review_required": plan.get("manual_review_required") is True,
                "evidence_basis": safe_dict(plan.get("source_evidence")),
            }
        )
    return notes


def patch_notes_applicability(notes: Any) -> dict[str, Any]:
    items = [item for item in safe_list(notes) if isinstance(item, dict)]
    invalid_notes: list[dict[str, Any]] = []
    required_text_min = 24

    for index, note in enumerate(items, 1):
        missing: list[str] = []
        if not str(note.get("id") or "").strip():
            missing.append("id")
        if not str(note.get("area") or "").strip():
            missing.append("area")
        if not safe_list(note.get("target_files")):
            missing.append("target_files")
        if len(str(note.get("summary") or "").strip()) < required_text_min:
            missing.append("summary")
        if len(str(note.get("edit_strategy") or "").strip()) < required_text_min:
            missing.append("edit_strategy")
        if not safe_list(note.get("validation_commands")):
            missing.append("validation_commands")
        if not safe_list(note.get("stop_conditions")):
            missing.append("stop_conditions")
        if note.get("manual_review_required") is not True:
            missing.append("manual_review_required")
        if missing:
            invalid_notes.append(
                {
                    "index": index,
                    "id": note.get("id"),
                    "missing": missing,
                    "target_files": safe_list(note.get("target_files"))[:8],
                }
            )

    return {
        "note_count": len(items),
        "applicable_count": len(items) - len(invalid_notes),
        "invalid_note_count": len(invalid_notes),
        "invalid_notes": invalid_notes[:20],
        "all_applicable": bool(items) and not invalid_notes,
        "required_fields": [
            "id",
            "area",
            "target_files",
            "summary",
            "edit_strategy",
            "validation_commands",
            "stop_conditions",
            "manual_review_required",
        ],
    }


def score_product(
    report: dict[str, Any],
) -> tuple[float, list[dict[str, Any]], list[dict[str, Any]]]:
    applicability = safe_dict(report.get("patch_notes_applicability")) or patch_notes_applicability(
        report.get("patch_notes")
    )
    checks = {
        "request_summary": bool(safe_dict(report.get("request_summary")).get("title")),
        "normalized_objective": len(str(report.get("normalized_objective") or "")) >= 24,
        "patch_plan_summary": safe_dict(report.get("patch_plan_summary")).get("patch_plan_count", 0)
        > 0,
        "patch_notes_concrete": bool(report.get("patch_notes")),
        "patch_notes_applicable": applicability.get("all_applicable") is True,
        "evidence_coverage": safe_dict(report.get("evidence_coverage")).get("score", 0) >= 60,
        "telemetry_quality": safe_dict(report.get("telemetry_quality")).get("score", 0) >= 50,
        "validation_commands": bool(
            safe_dict(report.get("patch_plan_summary")).get("validation_commands")
        ),
        "stop_conditions_guardrails": bool(
            safe_dict(report.get("patch_plan_summary")).get("stop_conditions")
        )
        and safe_dict(report.get("guardrails")).get("report_only") is True,
    }
    weights = {
        "request_summary": 8,
        "normalized_objective": 8,
        "patch_plan_summary": 12,
        "patch_notes_concrete": 10,
        "patch_notes_applicable": 20,
        "evidence_coverage": 12,
        "telemetry_quality": 12,
        "validation_commands": 10,
        "stop_conditions_guardrails": 8,
    }
    score = float(sum(weights[key] for key, ok in checks.items() if ok))
    findings = [
        {"severity": "medium", "reason": f"missing_or_weak:{key}"}
        for key, ok in checks.items()
        if not ok
    ]
    fallback = [
        {
            "reason": f"patch_notes_quality_missing:{key}",
            "recommended_followup": "rerun the heap-runtime workflow with patch specs, telemetry, capability manifest and evidence bundle enabled",
        }
        for key, ok in checks.items()
        if not ok
    ]
    return score, findings, fallback


def classify(errors: list[str], quality_gate_passed: bool, score: float) -> str:
    if errors:
        return "blocked_by_missing_required_inputs"
    if quality_gate_passed:
        return "ready_for_patch_notes_review"
    if score < 50:
        return "completed_with_low_confidence_patch_notes"
    return "completed_with_patch_notes_fallback"
