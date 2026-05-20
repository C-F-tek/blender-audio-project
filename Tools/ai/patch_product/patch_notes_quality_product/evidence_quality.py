from __future__ import annotations

from typing import Any


def safe_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def safe_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def build_evidence_coverage(
    loaded: dict[str, dict[str, Any]], input_status: dict[str, str]
) -> dict[str, Any]:
    expected = [
        "patch_quality",
        "decision_loop",
        "repository_consistency",
        "memory_bundle",
        "github_evidence_bundle",
    ]
    coverage = {key: bool(loaded.get(key)) for key in expected}
    missing = [key for key in expected if not coverage[key]]
    score = round(100.0 * (len(expected) - len(missing)) / len(expected), 2)
    return {
        "score": score,
        "coverage": coverage,
        "missing_evidence": missing,
        "input_status": input_status,
    }


def build_success_cases(report: dict[str, Any], loaded: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    coverage = safe_dict(report.get("evidence_coverage"))
    patch_summary = safe_dict(report.get("patch_plan_summary"))
    decision = safe_dict(loaded.get("decision_loop"))
    return [
        {
            "case": "patch_notes_quality_product",
            "quality_gate_passed": report.get("quality_gate_passed"),
            "score": report.get("quality_score"),
            "evidence_coverage_score": coverage.get("score"),
            "manual_review_required": report.get("manual_review_required"),
        },
        {
            "case": "patch_plan_quality_product",
            "quality_gate_passed": patch_summary.get("patch_quality_gate_passed"),
            "score": patch_summary.get("average_plan_score"),
            "patch_plan_count": patch_summary.get("patch_plan_count"),
        },
        {
            "case": "decision_loop_product",
            "passed": decision.get("passed"),
            "recommendation_count": decision.get("recommendation_count"),
            "patch_plan_count": decision.get("patch_plan_count"),
        },
    ]


def build_fallback_cases(
    report: dict[str, Any], loaded: dict[str, dict[str, Any]], min_quality_score: float
) -> list[dict[str, Any]]:
    cases: list[dict[str, Any]] = []
    evidence_paths = (
        safe_dict(report.get("inputs")).get("paths")
        if isinstance(report.get("inputs"), dict)
        else {}
    )
    if report.get("quality_score", 0) < min_quality_score or not report.get("quality_gate_passed"):
        cases.append(
            {
                "fallback_type": "patch_notes_quality_gate_fallback",
                "trigger": "quality_gate_passed_false_or_score_below_threshold",
                "primary_lane": "patch_notes_quality_product",
                "fallback_lane": "manual_review_patch_notes_fallback",
                "recovered": bool(report.get("patch_notes")),
                "product_blocker": False,
                "evidence_paths": safe_dict(evidence_paths),
            }
        )
    return cases
