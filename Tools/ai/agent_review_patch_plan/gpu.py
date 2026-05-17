"""GPU recommendation normalization."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .classification import is_cosmetic_recommendation
from .common import DEFAULT_VALIDATION_COMMANDS, target_path_error, unique_strings

def normalize_gpu_recommendation(
    *,
    rec: dict[str, Any],
    index: int,
    repo_root: Path,
    audit_refs: list[dict[str, Any]],
) -> tuple[dict[str, Any] | None, dict[str, str] | None]:
    if is_cosmetic_recommendation(rec):
        return None, {
            "id": str(rec.get("id") or f"gpu_{index:03d}"),
            "reason": "cosmetic/formatting-only recommendation suppressed",
        }
    target_files = unique_strings(
        rec.get("target_files", []) if isinstance(rec.get("target_files"), list) else []
    )
    if not target_files:
        return None, {
            "id": str(rec.get("id") or f"gpu_{index:03d}"),
            "reason": "GPU recommendation has no concrete target_files",
        }
    errors = [
        f"{path}: {target_path_error(path, repo_root)}"
        for path in target_files
        if target_path_error(path, repo_root)
    ]
    if errors:
        return None, {
            "id": str(rec.get("id") or f"gpu_{index:03d}"),
            "reason": "; ".join(errors),
        }
    return (
        {
            "id": str(rec.get("id") or f"gpu_{index:03d}"),
            "source": "gpu_recommendation",
            "area": rec.get("area") or "other",
            "status": "ready_for_manual_review",
            "target_files": target_files,
            "rationale": rec.get("rationale")
            or "GPU planner recommendation normalized for manual-review patch planning.",
            "edit_strategy": rec.get("proposed_strategy")
            or "Apply only a small, reviewable patch supported by the cited evidence.",
            "risk": rec.get("risk") or "medium",
            "validation_commands": rec.get("validation_commands") or DEFAULT_VALIDATION_COMMANDS,
            "stop_conditions": rec.get("stop_conditions")
            or [
                "Stop if target files changed since the review artifact was generated.",
                "Stop if the edit requires running Blender runtime or provider execution.",
                "Stop if the patch touches generated output, full analysis JSON, SQLite, or semantic indexes.",
            ],
            "source_evidence": {
                "gpu_recommendation": rec,
                "repository_consistency_finding": rec.get("repository_consistency_finding"),
                "npu_audit_refs": audit_refs,
            },
            "manual_review_required": True,
            "guardrails": {
                "cosmetic_patch_allowed": False,
                "manual_review_required": True,
                "patch_application_performed": False,
            },
        },
        None,
    )

def gpu_plans_from_report(
    *,
    gpu_report: dict[str, Any],
    repo_root: Path,
    audit_refs: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    plans: list[dict[str, Any]] = []
    skipped: list[dict[str, str]] = []
    recommendations = gpu_report.get("recommendations", [])
    if not isinstance(recommendations, list):
        return plans, [{"id": "gpu_report", "reason": "GPU report recommendations is not a list"}]
    for index, rec in enumerate(recommendations, start=1):
        if not isinstance(rec, dict):
            skipped.append({"id": f"gpu_{index:03d}", "reason": "recommendation is not an object"})
            continue
        if rec.get("status") != "ready_for_patch_plan":
            continue
        plan, skip = normalize_gpu_recommendation(
            rec=rec, index=index, repo_root=repo_root, audit_refs=audit_refs
        )
        if plan:
            plans.append(plan)
        if skip:
            skipped.append(skip)
    return plans, skipped
