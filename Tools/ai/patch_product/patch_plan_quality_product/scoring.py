from __future__ import annotations

from pathlib import Path
from typing import Any

FORBIDDEN_PREFIXES = (
    "output/",
    "renders/",
    ".git/",
    "indexAI/code_chunks/",
    "indexAI/project_code_chunks/",
)


def list_plans(patch_plan: dict[str, Any]) -> list[dict[str, Any]]:
    for key in ("patch_plans", "plans", "items", "recommendations"):
        value = patch_plan.get(key)
        if isinstance(value, list):
            return [item for item in value if isinstance(item, dict)]
    return []


def has_useful_text_or_dict(value: Any, min_chars: int = 24) -> bool:
    return (isinstance(value, dict) and bool(value)) or (
        isinstance(value, str) and len(value.strip()) >= min_chars
    )


def target_findings(targets: list[str], repo_root: Path) -> tuple[int, list[str]]:
    notes = []
    valid = 0
    for raw in targets:
        target = str(raw or "").replace("\\", "/").strip("/")
        if not target:
            notes.append("empty target")
            continue
        if any(target.startswith(prefix) for prefix in FORBIDDEN_PREFIXES):
            notes.append(f"{target}: forbidden generated/runtime target")
            continue
        full = (repo_root / target).resolve()
        try:
            full.relative_to(repo_root.resolve())
        except ValueError:
            notes.append(f"{target}: escapes repository root")
            continue
        if not full.exists():
            notes.append(f"{target}: target file missing")
            continue
        valid += 1
    return valid, notes


def score_plan(plan: dict[str, Any], repo_root: Path, index: int) -> dict[str, Any]:
    plan_id = str(plan.get("id") or plan.get("title") or f"plan_{index:03d}")
    targets = (
        [str(item) for item in plan.get("target_files", [])]
        if isinstance(plan.get("target_files"), list)
        else []
    )
    valid_targets, target_notes = target_findings(targets, repo_root)
    checks = {
        "has_existing_targets": bool(targets) and valid_targets == len(targets),
        "has_rationale": has_useful_text_or_dict(plan.get("rationale")),
        "has_edit_strategy": has_useful_text_or_dict(plan.get("edit_strategy")),
        "has_source_evidence": has_useful_text_or_dict(plan.get("source_evidence")),
        "has_validation_commands": isinstance(plan.get("validation_commands"), list)
        and bool(plan.get("validation_commands")),
        "has_stop_conditions": isinstance(plan.get("stop_conditions"), list)
        and bool(plan.get("stop_conditions")),
        "manual_review_marked": plan.get("manual_review_required") is True
        or str(plan.get("status", "")).lower() == "ready_for_manual_review",
    }
    weights = {
        "has_existing_targets": 20,
        "has_rationale": 15,
        "has_edit_strategy": 20,
        "has_source_evidence": 15,
        "has_validation_commands": 15,
        "has_stop_conditions": 10,
        "manual_review_marked": 5,
    }
    score = sum(weights[key] for key, ok in checks.items() if ok)
    weak = [key for key, ok in checks.items() if not ok]
    notes = list(target_notes)
    notes.extend(
        f"missing_or_weak:{key}"
        for key in weak
        if key != "has_existing_targets" or not target_notes
    )
    return {
        "id": plan_id,
        "score": min(score, 100),
        "target_files": targets,
        "valid_target_count": valid_targets,
        "checks": checks,
        "notes": notes,
    }


def classify(
    fatal_errors: list[str], quality_gate_passed: bool, avg_score: float, hit_count: int
) -> str:
    if fatal_errors:
        return "blocked_by_missing_required_inputs"
    if quality_gate_passed:
        return "ready_for_manual_patch_review"
    if avg_score <= 35 or hit_count <= 0:
        return "completed_with_low_confidence_patch_notes"
    return "completed_with_fallback_notes"
