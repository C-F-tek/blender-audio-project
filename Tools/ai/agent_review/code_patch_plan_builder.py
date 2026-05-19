"""Report builder for agent-review code patch plans."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .code_patch_plan_deps import (
    APPLY_MODE,
    PLAN_KIND,
    line_count_for,
    load_line_counts,
    now_iso,
    read_json_object,
    repo_rel,
    report_only_guardrails,
)
from .code_patch_plan_rules import plan_from_check, should_consider_check, source_kind_for
from .code_patch_plan_static import build_static_plans, validate_code_drift_report

def build_code_patch_plan(
    repo_root: Path,
    code_drift_path: Path,
    line_count_csv: Path,
    code_interpreter_path: Path | None = None,
) -> dict[str, Any]:
    """Build the full agent_review_code_patch_plan report."""
    errors: list[str] = []
    warnings: list[str] = []
    code_drift, load_errors = read_json_object(code_drift_path)
    errors.extend(f"code drift report: {error}" for error in load_errors)
    counts, count_warnings = load_line_counts(repo_root, line_count_csv)
    warnings.extend(count_warnings)

    plans: list[dict[str, Any]] = []
    skipped: list[dict[str, str]] = []
    if code_drift:
        checks = validate_code_drift_report(code_drift, errors)
        for index, check in enumerate(checks, start=1):
            if not should_consider_check(check):
                continue
            plan, skip = plan_from_check(index, repo_root, check, counts)
            if plan:
                plans.append(plan)
            if skip:
                skipped.append(skip)

    static_plans, static_skipped, static_report_loaded = build_static_plans(
        repo_root, code_interpreter_path, counts, errors, warnings
    )
    plans.extend(static_plans)
    skipped.extend(static_skipped)

    if code_drift and not plans:
        warnings.append("no code patch plans were produced from supplied evidence")

    return build_report(
        repo_root,
        code_drift_path,
        line_count_csv,
        code_interpreter_path,
        static_report_loaded,
        counts,
        plans,
        skipped,
        errors,
        warnings,
    )

def build_report(
    repo_root: Path,
    code_drift_path: Path,
    line_count_csv: Path,
    code_interpreter_path: Path | None,
    static_report_loaded: bool,
    counts: dict[str, int],
    plans: list[dict[str, Any]],
    skipped: list[dict[str, str]],
    errors: list[str],
    warnings: list[str],
) -> dict[str, Any]:
    """Assemble the final report object."""
    static_count = sum(1 for plan in plans if source_kind_for(plan) == "code_interpreter_report")
    drift_count = sum(1 for plan in plans if source_kind_for(plan) == "code_contract_drift")
    return {
        "schema_version": 1,
        "kind": PLAN_KIND,
        "generated_at": now_iso(),
        "repo_root": str(repo_root),
        "passed": not errors,
        "errors": errors,
        "warnings": warnings,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "manual_review_required": True,
        "apply_mode": APPLY_MODE,
        "inputs": {
            "code_contract_drift_report": repo_rel(repo_root, code_drift_path),
            "line_count_csv": repo_rel(repo_root, line_count_csv),
            "line_count_csv_loaded": bool(counts),
            "code_interpreter_report": (
                repo_rel(repo_root, code_interpreter_path) if code_interpreter_path else None
            ),
            "code_interpreter_report_loaded": static_report_loaded,
        },
        "patch_plan_count": len(plans),
        "code_contract_patch_plan_count": drift_count,
        "static_code_patch_plan_count": static_count,
        "code_patch_plans": plans,
        "skipped_candidate_count": len(skipped),
        "skipped_candidates": skipped,
        "decision": {
            "ready_for_manual_review": bool(plans) and not errors,
            "patch_plan_count": len(plans),
            "manual_review_required": True,
            "recommended_next_layer": (
                "manual_review_then_targeted_code_pr"
                if plans and not errors
                else "collect_or_fix_code_review_evidence"
            ),
        },
        "guardrails": report_only_guardrails(
            npu_primary_advisory=False,
            openvino_gpu_primary_lane=False,
            static_code_interpreter_consumed=static_report_loaded,
        ),
    }
