from __future__ import annotations

from typing import Any

from Tools.ai.patch_plan_quality_product.scoring import list_plans


def safe_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def safe_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _text(value: Any, limit: int = 500) -> str:
    text = str(value or "").strip()
    return text if len(text) <= limit else text[:limit] + "...[truncated]"


def _unique_strings(items: list[Any], limit: int = 16) -> list[str]:
    out: list[str] = []
    for item in items:
        value = str(item or "").strip()
        if value and value not in out:
            out.append(value)
        if len(out) >= limit:
            break
    return out


def patch_plan_summary(patch_plan: dict[str, Any], patch_quality: dict[str, Any]) -> dict[str, Any]:
    plans = list_plans(patch_plan)
    targets: list[Any] = []
    validations: list[Any] = []
    stops: list[Any] = []
    for plan in plans:
        targets.extend(safe_list(plan.get("target_files")))
        validations.extend(safe_list(plan.get("validation_commands")))
        stops.extend(safe_list(plan.get("stop_conditions")))
    quality = safe_dict(patch_quality.get("quality"))
    return {
        "patch_plan_count": len(plans),
        "patch_quality_seen": bool(patch_quality),
        "patch_quality_gate_passed": patch_quality.get("quality_gate_passed"),
        "patch_quality_classification": patch_quality.get("classification"),
        "average_plan_score": quality.get("average_plan_score"),
        "target_files": _unique_strings(targets, limit=24),
        "validation_commands": _unique_strings(validations, limit=24),
        "stop_conditions": _unique_strings(stops, limit=24),
    }


def build_patch_notes(patch_plan: dict[str, Any], patch_quality: dict[str, Any], limit: int = 20) -> list[dict[str, Any]]:
    quality_scores = {}
    for item in safe_list(safe_dict(patch_quality.get("quality")).get("plan_scores")):
        if isinstance(item, dict):
            quality_scores[str(item.get("id") or "")] = item
    notes: list[dict[str, Any]] = []
    for index, plan in enumerate(list_plans(patch_plan)[:limit], 1):
        plan_id = str(plan.get("id") or plan.get("title") or f"plan_{index:03d}")
        score = quality_scores.get(plan_id, {})
        notes.append(
            {
                "id": plan_id,
                "area": plan.get("area"),
                "status": plan.get("status"),
                "target_files": _unique_strings(safe_list(plan.get("target_files")), limit=12),
                "summary": _text(plan.get("rationale") or plan.get("edit_strategy"), 700),
                "edit_strategy": _text(plan.get("edit_strategy"), 700),
                "quality_score": score.get("score"),
                "quality_notes": safe_list(score.get("notes"))[:8],
                "validation_commands": _unique_strings(safe_list(plan.get("validation_commands")), limit=8),
                "stop_conditions": _unique_strings(safe_list(plan.get("stop_conditions")), limit=8),
                "manual_review_required": plan.get("manual_review_required") is True,
                "evidence_basis": safe_dict(plan.get("source_evidence")),
            }
        )
    return notes


def score_product(report: dict[str, Any]) -> tuple[float, list[dict[str, Any]], list[dict[str, Any]]]:
    checks = {
        "request_summary": bool(safe_dict(report.get("request_summary")).get("title")),
        "normalized_objective": len(str(report.get("normalized_objective") or "")) >= 24,
        "patch_plan_summary": safe_dict(report.get("patch_plan_summary")).get("patch_plan_count", 0) > 0,
        "patch_notes_concrete": bool(report.get("patch_notes")),
        "evidence_coverage": safe_dict(report.get("evidence_coverage")).get("score", 0) >= 60,
        "telemetry_quality": safe_dict(report.get("telemetry_quality")).get("score", 0) >= 50,
        "validation_commands": bool(safe_dict(report.get("patch_plan_summary")).get("validation_commands")),
        "stop_conditions_guardrails": bool(safe_dict(report.get("patch_plan_summary")).get("stop_conditions")) and safe_dict(report.get("guardrails")).get("report_only") is True,
    }
    weights = {
        "request_summary": 10,
        "normalized_objective": 10,
        "patch_plan_summary": 15,
        "patch_notes_concrete": 20,
        "evidence_coverage": 15,
        "telemetry_quality": 15,
        "validation_commands": 10,
        "stop_conditions_guardrails": 5,
    }
    score = float(sum(weights[key] for key, ok in checks.items() if ok))
    findings = [{"severity": "medium", "reason": f"missing_or_weak:{key}"} for key, ok in checks.items() if not ok]
    fallback = [{"reason": f"patch_notes_quality_missing:{key}", "recommended_followup": "rerun Full0To10 with patch specs, telemetry, capability manifest and evidence bundle enabled"} for key, ok in checks.items() if not ok]
    return score, findings, fallback


def classify(errors: list[str], quality_gate_passed: bool, score: float) -> str:
    if errors:
        return "blocked_by_missing_required_inputs"
    if quality_gate_passed:
        return "ready_for_patch_notes_review"
    if score < 50:
        return "completed_with_low_confidence_patch_notes"
    return "completed_with_patch_notes_fallback"
