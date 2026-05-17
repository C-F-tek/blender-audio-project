"""Decision summary for agent review patch plans."""

from __future__ import annotations

from typing import Any

def build_decision(
    *,
    plans: list[dict[str, Any]],
    skipped: list[dict[str, str]],
    gpu_report: dict[str, Any],
    evidence: dict[str, Any],
    fallback_used: bool,
) -> dict[str, Any]:
    evidence_decision = (
        evidence.get("decision", {}) if isinstance(evidence.get("decision"), dict) else {}
    )
    gpu_decision = (
        gpu_report.get("decision", {}) if isinstance(gpu_report.get("decision"), dict) else {}
    )
    return {
        "ready_for_manual_review": bool(plans),
        "patch_plan_count": len(plans),
        "skipped_candidate_count": len(skipped),
        "gpu_recommendation_count": gpu_report.get("recommendation_count", 0),
        "gpu_ready_count": gpu_decision.get("ready_count", 0),
        "fallback_used": fallback_used,
        "evidence_ready_for_manual_patch_count": evidence_decision.get(
            "ready_for_manual_patch_count"
        ),
        "evidence_sufficient_for_real_pr": evidence_decision.get("sufficient_for_real_pr"),
        "recommended_next_layer": (
            "manual_review_then_targeted_patch" if plans else "collect_more_evidence"
        ),
        "manual_review_required": True,
        "cosmetic_patch_suppression_enabled": True,
    }
