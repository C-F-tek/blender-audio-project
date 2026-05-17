"""Rules for translating drift checks into patch-plan entries."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .code_patch_plan_deps import (
    COMMON_STOP_CONDITIONS,
    DEFAULT_VALIDATION_COMMANDS,
    line_count_for,
    normalize_repo_path,
    target_path_errors,
)

def list_len(value: Any) -> int:
    """Return list length only when the value is a list."""
    return len(value) if isinstance(value, list) else 0

def list_field(check: dict[str, Any], field: str) -> list[Any]:
    """Return a list-valued check field or an empty list."""
    value = check.get(field)
    return value if isinstance(value, list) else []

def stop_conditions_for(source_label: str) -> list[str]:
    """Return shared manual-review stop conditions for one evidence source."""
    return [
        f"Stop if the target file changed since {source_label} was generated.",
        *COMMON_STOP_CONDITIONS,
    ]

def source_kind_for(plan: dict[str, Any]) -> Any:
    """Return the source kind recorded on a code patch plan."""
    source_evidence = plan.get("source_evidence")
    return source_evidence.get("source_kind") if isinstance(source_evidence, dict) else None

def risk_for(path_value: str, check: dict[str, Any], counts: dict[str, int]) -> str:
    """Classify patch-plan risk from drift severity and file size."""
    lines = line_count_for(path_value, counts)
    base = (
        "medium"
        if list_len(check.get("missing_required_terms")) or list_len(check.get("errors"))
        else "low"
    )
    if lines is not None and lines >= 600:
        return "high" if base == "medium" else "medium"
    if list_len(check.get("warnings")) >= 5 and base == "low":
        return "medium"
    return base

def status_for(check: dict[str, Any]) -> str:
    """Return review status for one contract-drift check."""
    if check.get("ok") is False:
        return "ready_for_manual_review"
    if check.get("missing_recommended_terms") or check.get("warnings"):
        return "candidate_for_manual_review"
    return "informational"

def rationale_for(check: dict[str, Any]) -> str:
    """Build a concise rationale from one contract-drift check."""
    contract = check.get("contract") or "code contract"
    parts = [f"Contract drift check `{contract}` reported a code-review candidate."]
    for label, field in (
        ("Missing required terms", "missing_required_terms"),
        ("Missing recommended terms", "missing_recommended_terms"),
        ("Forbidden terms present", "forbidden_terms_present"),
    ):
        values = list_field(check, field)
        if values:
            parts.append(f"{label}: " + ", ".join(f"`{term}`" for term in values[:8]) + ".")
    return " ".join(parts)

def edit_strategy_for(path_value: str, check: dict[str, Any], counts: dict[str, int]) -> str:
    """Build the manual-review edit strategy for one code patch plan."""
    hint = first_safe_action_hint(check)
    lines = line_count_for(path_value, counts)
    size_note = (
        f" Current CSV sizing hint: {lines} lines; verify current count locally before editing."
        if lines is not None
        else ""
    )
    return (
        (
            hint
            or "Apply the smallest targeted code/config change that restores the documented contract terms."
        )
        + size_note
        + " Do not apply this plan automatically."
    )

def first_safe_action_hint(check: dict[str, Any]) -> str:
    """Return the first safe-action hint if present."""
    for action in list_field(check, "safe_actions"):
        if isinstance(action, dict) and action.get("hint"):
            return str(action["hint"])
    return ""

def validation_commands_for(path_value: str) -> list[str]:
    """Return validation commands recommended after manually applying a patch."""
    commands = list(DEFAULT_VALIDATION_COMMANDS)
    if Path(path_value).suffix.lower() == ".py":
        ps_path = path_value.replace("/", "\\")
        commands.insert(0, f"python -m py_compile .\\{ps_path}")
    return commands

def should_consider_check(check: Any) -> bool:
    """Return true when a contract-drift check can become a patch-plan candidate."""
    if not isinstance(check, dict):
        return False
    if check.get("ok") is False:
        return True
    return any(
        list_field(check, field)
        for field in (
            "missing_required_terms",
            "missing_recommended_terms",
            "errors",
            "warnings",
        )
    )

def check_is_clean(check: dict[str, Any]) -> bool:
    """Return true when a check has no actionable drift."""
    return (
        not list_field(check, "missing_required_terms")
        and not list_field(check, "missing_recommended_terms")
        and not list_field(check, "errors")
        and not list_field(check, "warnings")
        and check.get("ok") is not False
    )

def plan_from_check(
    index: int, repo_root: Path, check: dict[str, Any], counts: dict[str, int]
) -> tuple[dict[str, Any] | None, dict[str, str] | None]:
    """Convert one contract-drift check into one manual-review code patch plan."""
    path_value = normalize_repo_path(check.get("path"))
    skipped_id = f"code_contract_{index:03d}"
    if not path_value:
        return None, {"id": skipped_id, "reason": "check has no path"}
    errors = target_path_errors(repo_root, path_value)
    if errors:
        return None, {"id": skipped_id, "path": path_value, "reason": "; ".join(errors)}
    if check_is_clean(check):
        return None, {
            "id": skipped_id,
            "path": path_value,
            "reason": "check is already clean",
        }
    return build_plan(skipped_id, path_value, check, counts), None

def build_plan(
    plan_id: str, path_value: str, check: dict[str, Any], counts: dict[str, int]
) -> dict[str, Any]:
    """Build the code patch-plan JSON object for one target file."""
    return {
        "id": plan_id,
        "area": str(check.get("owner_lane") or check.get("contract") or "validation"),
        "risk": risk_for(path_value, check, counts),
        "status": status_for(check),
        "target_files": [path_value],
        "rationale": rationale_for(check),
        "edit_strategy": edit_strategy_for(path_value, check, counts),
        "proposed_patch": "",
        "validation_commands": validation_commands_for(path_value),
        "stop_conditions": stop_conditions_for("the drift report"),
        "manual_review_required": True,
        "source_evidence": {
            "contract": check.get("contract"),
            "owner_lane": check.get("owner_lane"),
            "consumed_by_lanes": list_field(check, "consumed_by_lanes"),
            "missing_required_terms": list_field(check, "missing_required_terms"),
            "missing_recommended_terms": list_field(check, "missing_recommended_terms"),
            "errors": list_field(check, "errors"),
            "warnings": list_field(check, "warnings"),
            "line_count_csv_hint": line_count_for(path_value, counts),
            "source_kind": "code_contract_drift",
        },
    }
