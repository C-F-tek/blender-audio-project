"""Static recommendation support for agent-review code patch plans."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .code_patch_plan_deps import (
    MAX_STATIC_RECOMMENDATIONS,
    line_count_for,
    normalize_repo_path,
    read_json_object,
    target_path_errors,
)
from .code_patch_plan_rules import stop_conditions_for, validation_commands_for

def validate_code_drift_report(
    code_drift: dict[str, Any], errors: list[str]
) -> list[dict[str, Any]]:
    """Validate the code_contract_drift source report and return its checks."""
    if code_drift.get("kind") != "code_contract_drift":
        errors.append("code drift report kind must be code_contract_drift")
    for field in (
        "provider_execution_performed",
        "patch_application_performed",
        "source_writes_performed",
    ):
        if code_drift.get(field) is not False:
            errors.append(f"code drift report {field} must be false")
    checks = code_drift.get("checks", [])
    if not isinstance(checks, list):
        errors.append("code drift report checks must be a list")
        return []
    return [check for check in checks if isinstance(check, dict)]

def validate_code_interpreter_report(
    code_report: dict[str, Any], errors: list[str]
) -> list[dict[str, Any]]:
    """Validate optional code_interpreter_report and return recommendations."""
    if code_report.get("kind") != "code_interpreter_report":
        errors.append("code interpreter report kind must be code_interpreter_report")
    for field in (
        "provider_execution_performed",
        "patch_application_performed",
        "source_writes_performed",
    ):
        if code_report.get(field) is not False:
            errors.append(f"code interpreter report {field} must be false")
    recommendations = code_report.get("recommendations", [])
    if not isinstance(recommendations, list):
        errors.append("code interpreter report recommendations must be a list")
        return []
    return [item for item in recommendations if isinstance(item, dict)]

def static_rationale_for(recommendation: dict[str, Any]) -> str:
    """Build rationale for static interpreter recommendations."""
    reasons = (
        recommendation.get("reasons") if isinstance(recommendation.get("reasons"), list) else []
    )
    reason_text = ", ".join(str(item) for item in reasons[:8]) or "static interpreter review signal"
    return f"Static code interpreter recommendation `{recommendation.get('id')}` flagged `{recommendation.get('target_file')}` for manual review: {reason_text}."

def static_strategy_for(
    path_value: str, recommendation: dict[str, Any], counts: dict[str, int]
) -> str:
    """Build manual-review strategy for static interpreter recommendations."""
    lines = line_count_for(path_value, counts)
    size_note = (
        f" Current CSV sizing hint: {lines} lines; verify current count locally before editing."
        if lines is not None
        else ""
    )
    next_layer = recommendation.get("recommended_next_layer") or "agent_review_code_patch_plan"
    return (
        f"Inspect the static interpreter signals and decide whether a focused refactor, split, simplification, or guardrail improvement is warranted. Next layer: `{next_layer}`."
        + size_note
        + " Do not apply this plan automatically."
    )

def plan_from_static_recommendation(
    index: int,
    repo_root: Path,
    recommendation: dict[str, Any],
    counts: dict[str, int],
) -> tuple[dict[str, Any] | None, dict[str, str] | None]:
    """Convert one static interpreter recommendation into one patch-plan candidate."""
    path_value = normalize_repo_path(recommendation.get("target_file"))
    skipped_id = f"code_static_{index:03d}"
    if not path_value:
        return None, {
            "id": skipped_id,
            "reason": "static recommendation has no target_file",
        }
    errors = target_path_errors(repo_root, path_value)
    if errors:
        return None, {"id": skipped_id, "path": path_value, "reason": "; ".join(errors)}
    risk = str(recommendation.get("risk") or "medium")
    status = str(recommendation.get("status") or "candidate_for_manual_review")
    plan = {
        "id": skipped_id,
        "area": "static_code_interpreter",
        "risk": risk if risk in {"low", "medium", "high"} else "medium",
        "status": status,
        "target_files": [path_value],
        "rationale": static_rationale_for(recommendation),
        "edit_strategy": static_strategy_for(path_value, recommendation, counts),
        "proposed_patch": "",
        "validation_commands": validation_commands_for(path_value),
        "stop_conditions": stop_conditions_for("the static code interpreter report"),
        "manual_review_required": True,
        "source_evidence": {
            "source_kind": "code_interpreter_report",
            "static_recommendation_id": recommendation.get("id"),
            "reasons": (
                recommendation.get("reasons")
                if isinstance(recommendation.get("reasons"), list)
                else []
            ),
            "recommended_next_layer": recommendation.get("recommended_next_layer"),
            "line_count_csv_hint": line_count_for(path_value, counts),
        },
    }
    return plan, None

def build_static_plans(
    repo_root: Path,
    code_interpreter_path: Path | None,
    counts: dict[str, int],
    errors: list[str],
    warnings: list[str],
) -> tuple[list[dict[str, Any]], list[dict[str, str]], bool]:
    """Build static interpreter patch-plan candidates when a report is supplied."""
    if code_interpreter_path is None:
        return [], [], False
    code_report, load_errors = read_json_object(code_interpreter_path)
    errors.extend(f"code interpreter report: {error}" for error in load_errors)
    if not code_report:
        return [], [], True
    recommendations = validate_code_interpreter_report(code_report, errors)
    plans: list[dict[str, Any]] = []
    skipped: list[dict[str, str]] = []
    for index, recommendation in enumerate(recommendations[:MAX_STATIC_RECOMMENDATIONS], start=1):
        plan, skip = plan_from_static_recommendation(index, repo_root, recommendation, counts)
        if plan:
            plans.append(plan)
        if skip:
            skipped.append(skip)
    if len(recommendations) > MAX_STATIC_RECOMMENDATIONS:
        warnings.append(
            f"static recommendations capped at {MAX_STATIC_RECOMMENDATIONS} of {len(recommendations)}"
        )
    return plans, skipped, True
