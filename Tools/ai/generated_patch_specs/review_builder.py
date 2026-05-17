"""Builder for reviewed patch specs."""

from __future__ import annotations

import copy
import json
from datetime import datetime
from pathlib import Path
from typing import Any

from .review_common import (
    DEFAULT_GUARDRAILS,
    EXPECTED_APPLY_MODE,
    EXPECTED_REVIEW_STATUS,
    REVIEWED_MANIFEST_KIND,
    REVIEWED_SPEC_KIND,
    load_patch_runner,
    normalize_repo_path,
    read_json_object,
    repo_relative,
    validate_inputs,
)
from .review_markdown import render_manifest_markdown

def draft_operations_by_path(draft: dict[str, Any]) -> dict[str, dict[str, Any]]:
    operations = draft.get("operations") or []
    return {
        normalize_repo_path(op.get("path")): op
        for op in operations
        if isinstance(op, dict) and normalize_repo_path(op.get("path"))
    }

def build_reviewed_operation(
    plan_operation: dict[str, Any], draft_operation: dict[str, Any]
) -> dict[str, Any]:
    output: dict[str, Any] = {
        "path": normalize_repo_path(plan_operation.get("path")),
        "replacements": copy.deepcopy(plan_operation.get("replacements") or []),
        "proposal_id": draft_operation.get("proposal_id"),
        "artifact_kind": draft_operation.get("artifact_kind"),
        "operation": draft_operation.get("operation") or "manual_patch_suggestion",
        "content_status": "reviewed_patch_spec",
        "review_status": EXPECTED_REVIEW_STATUS,
        "require_contains_before": plan_operation.get("require_contains_before") or [],
        "forbid_contains_before": plan_operation.get("forbid_contains_before") or [],
        "require_contains_after": plan_operation.get("require_contains_after") or [],
        "forbid_contains_after": plan_operation.get("forbid_contains_after") or [],
    }
    for optional_key in ("expected_line_delta", "normalize_replacement_newlines"):
        if optional_key in plan_operation:
            output[optional_key] = plan_operation[optional_key]
    if plan_operation.get("review_notes"):
        output["review_notes"] = plan_operation["review_notes"]
    return output

def dry_run_spec(repo_root: Path, spec: dict[str, Any]) -> tuple[bool, list[dict[str, Any]], str]:
    apply_spec, patch_error = load_patch_runner(repo_root)
    try:
        reports = apply_spec(repo_root, copy.deepcopy(spec), write=False, no_backup=True)
    except patch_error as exc:
        return False, [], str(exc)
    return (
        True,
        [
            {
                "path": repo_relative(report.path, repo_root),
                "changed": report.changed,
                "before_lines": report.before_lines,
                "after_lines": report.after_lines,
                "replacements_applied": report.replacements_applied,
                "bom_removed": report.bom_removed,
            }
            for report in reports
        ],
        "",
    )

def build_reviewed_spec(
    *,
    repo_root: Path,
    draft_path: Path,
    plan_path: Path,
    output_dir: Path,
    basename: str,
) -> dict[str, Any]:
    draft = read_json_object(draft_path)
    plan = read_json_object(plan_path)
    errors = validate_inputs(draft, plan, repo_root)
    warnings: list[str] = []

    draft_by_path = draft_operations_by_path(draft)
    reviewed_operations: list[dict[str, Any]] = []
    for plan_operation in plan.get("operations") or []:
        if not isinstance(plan_operation, dict):
            continue
        path = normalize_repo_path(plan_operation.get("path"))
        draft_operation = draft_by_path.get(path)
        if draft_operation is None:
            continue
        reviewed_operations.append(build_reviewed_operation(plan_operation, draft_operation))

    reviewed_spec = {
        "version": 1,
        "schema_version": 1,
        "kind": REVIEWED_SPEC_KIND,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "repo_root": str(repo_root),
        "source_draft_spec": repo_relative(draft_path, repo_root),
        "source_replacement_plan": repo_relative(plan_path, repo_root),
        "source_proposal_report": draft.get("source_proposal_report") or "",
        "proposal_id": draft.get("proposal_id") or "",
        "proposal_title": draft.get("proposal_title") or "",
        "apply_mode": EXPECTED_APPLY_MODE,
        "review_status": EXPECTED_REVIEW_STATUS,
        "provider_execution_performed": False,
        "description": plan.get("description") or draft.get("description") or "Reviewed patch spec",
        "operations": reviewed_operations,
        "validation_commands": plan.get("validation_commands")
        or draft.get("validation_commands")
        or [],
        "stop_conditions": plan.get("stop_conditions") or draft.get("stop_conditions") or [],
        "do_not_touch": draft.get("do_not_touch") or [],
        "guardrails": DEFAULT_GUARDRAILS,
    }

    if not reviewed_operations and not errors:
        errors.append("no reviewed operations were produced")

    dry_run_passed = False
    dry_run_reports: list[dict[str, Any]] = []
    dry_run_error = ""
    if not errors:
        dry_run_passed, dry_run_reports, dry_run_error = dry_run_spec(repo_root, reviewed_spec)
        if not dry_run_passed:
            errors.append(f"dry-run failed: {dry_run_error}")
        elif not any(item.get("changed") for item in dry_run_reports):
            errors.append("dry-run passed but no target would change")

    reviewed_spec["dry_run"] = {
        "passed": dry_run_passed and not errors,
        "error": dry_run_error,
        "reports": dry_run_reports,
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    spec_path = output_dir / f"{basename}.json"
    manifest_path = output_dir / f"{basename}_manifest.json"
    markdown_path = output_dir / f"{basename}_manifest.md"
    spec_path.write_text(
        json.dumps(reviewed_spec, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    manifest = {
        "schema_version": 1,
        "kind": REVIEWED_MANIFEST_KIND,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "repo_root": str(repo_root),
        "passed": not errors,
        "errors": errors,
        "warnings": warnings,
        "provider_execution_performed": False,
        "apply_mode": EXPECTED_APPLY_MODE,
        "review_status": EXPECTED_REVIEW_STATUS,
        "source_draft_spec": repo_relative(draft_path, repo_root),
        "source_replacement_plan": repo_relative(plan_path, repo_root),
        "reviewed_spec_count": 1,
        "specs": [
            {
                "path": repo_relative(spec_path, repo_root),
                "kind": REVIEWED_SPEC_KIND,
                "operation_count": len(reviewed_operations),
                "dry_run_passed": reviewed_spec["dry_run"]["passed"],
                "operations": [
                    {
                        "path": operation.get("path"),
                        "artifact_kind": operation.get("artifact_kind"),
                        "replacement_count": len(operation.get("replacements") or []),
                    }
                    for operation in reviewed_operations
                ],
            }
        ],
        "guardrails": DEFAULT_GUARDRAILS,
    }
    manifest["manifest_json"] = repo_relative(manifest_path, repo_root)
    manifest["manifest_markdown"] = repo_relative(markdown_path, repo_root)
    manifest["reviewed_spec"] = repo_relative(spec_path, repo_root)
    manifest_path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    markdown_path.write_text(render_manifest_markdown(manifest), encoding="utf-8")
    return manifest
