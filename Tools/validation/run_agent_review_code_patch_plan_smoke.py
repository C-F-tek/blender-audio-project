#!/usr/bin/env python3
"""Validate agent-review code patch-plan reports.

This smoke validator is report-only. It validates the proposed future
`agent_review_code_patch_plan` contract without applying patches, executing
providers, running Blender or writing source files.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

try:
    from report_utils import resolve_output_path, write_json_report
except ImportError:
    from Tools.validation.report_utils import resolve_output_path, write_json_report  # type: ignore


REPORT_KIND = "agent_review_code_patch_plan_smoke"
EXPECTED_PLAN_KIND = "agent_review_code_patch_plan"
EXPECTED_APPLY_MODE = "report_only_manual_review_code_patch_plan"
FORBIDDEN_TARGET_PREFIXES = (
    "output/",
    "renders/",
    "indexAI/code_chunks/",
    "indexAI/project_code_chunks/",
)
FORBIDDEN_TARGET_SUFFIXES = (
    ".db",
    ".sqlite",
    ".sqlite3",
)
FORBIDDEN_TARGET_FRAGMENTS = (
    "full_analysis",
    "analysis_full",
)


def load_json(path: Path) -> tuple[dict[str, Any], list[str]]:
    try:
        raw = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        return {}, [f"{type(exc).__name__}: {exc}"]
    if not isinstance(raw, dict):
        return {}, ["root JSON value must be an object"]
    return raw, []


def normalize_path(value: str) -> str:
    return value.replace("\\", "/").lstrip("./")


def target_path_errors(path_value: str) -> list[str]:
    path = normalize_path(path_value)
    errors: list[str] = []
    for prefix in FORBIDDEN_TARGET_PREFIXES:
        if path.startswith(prefix):
            errors.append(f"forbidden target prefix: {prefix}")
    for suffix in FORBIDDEN_TARGET_SUFFIXES:
        if path.lower().endswith(suffix):
            errors.append(f"forbidden target suffix: {suffix}")
    for fragment in FORBIDDEN_TARGET_FRAGMENTS:
        if fragment in path.lower():
            errors.append(f"forbidden target fragment: {fragment}")
    return errors


def validate_plan_item(repo_root: Path, item: Any, index: int) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    if not isinstance(item, dict):
        return {
            "index": index,
            "id": f"<invalid-{index}>",
            "ok": False,
            "errors": ["plan item must be an object"],
            "warnings": [],
        }

    plan_id = str(item.get("id") or f"<missing-{index}>")
    required_string_fields = ("id", "area", "risk", "status", "rationale", "edit_strategy")
    for field in required_string_fields:
        if not isinstance(item.get(field), str) or not item.get(field):
            errors.append(f"missing or invalid string field: {field}")

    if item.get("manual_review_required") is not True:
        errors.append("manual_review_required must be true on each plan")

    target_files = item.get("target_files")
    if not isinstance(target_files, list) or not target_files:
        errors.append("target_files must be a non-empty list")
        target_files = []
    for target in target_files:
        if not isinstance(target, str) or not target.strip():
            errors.append("target_files entries must be non-empty strings")
            continue
        normalized = normalize_path(target)
        errors.extend(f"{normalized}: {error}" for error in target_path_errors(normalized))
        full = repo_root / normalized
        if not full.exists():
            warnings.append(f"target file does not currently exist: {normalized}")

    validation_commands = item.get("validation_commands")
    if not isinstance(validation_commands, list) or not validation_commands:
        errors.append("validation_commands must be a non-empty list")
    elif not all(isinstance(command, str) and command.strip() for command in validation_commands):
        errors.append("validation_commands entries must be non-empty strings")

    stop_conditions = item.get("stop_conditions")
    if not isinstance(stop_conditions, list) or not stop_conditions:
        errors.append("stop_conditions must be a non-empty list")
    elif not all(isinstance(condition, str) and condition.strip() for condition in stop_conditions):
        errors.append("stop_conditions entries must be non-empty strings")

    proposed_patch = item.get("proposed_patch", "")
    if proposed_patch is not None and not isinstance(proposed_patch, str):
        errors.append("proposed_patch must be a string when present")
    if isinstance(proposed_patch, str):
        normalized_patch = normalize_path(proposed_patch)
        for prefix in FORBIDDEN_TARGET_PREFIXES:
            if prefix in normalized_patch:
                errors.append(f"proposed_patch references forbidden prefix: {prefix}")

    return {
        "index": index,
        "id": plan_id,
        "ok": not errors,
        "errors": errors,
        "warnings": warnings,
        "target_files": target_files,
    }


def validate_report(repo_root: Path, report_path: Path) -> dict[str, Any]:
    data, load_errors = load_json(report_path)
    checks: list[dict[str, Any]] = []
    errors: list[str] = list(load_errors)
    warnings: list[str] = []

    if data:
        if data.get("kind") != EXPECTED_PLAN_KIND:
            errors.append(f"kind must be {EXPECTED_PLAN_KIND}")
        if data.get("apply_mode") != EXPECTED_APPLY_MODE:
            errors.append(f"apply_mode must be {EXPECTED_APPLY_MODE}")
        for field in ("provider_execution_performed", "patch_application_performed", "source_writes_performed"):
            if data.get(field) is not False:
                errors.append(f"{field} must be false")
        if data.get("manual_review_required") is not True:
            errors.append("manual_review_required must be true")

        plans = data.get("code_patch_plans")
        if not isinstance(plans, list):
            errors.append("code_patch_plans must be a list")
            plans = []
        if data.get("patch_plan_count") != len(plans):
            errors.append("patch_plan_count must match len(code_patch_plans)")

        for index, item in enumerate(plans):
            check = validate_plan_item(repo_root, item, index)
            checks.append(check)
            errors.extend(f"{check['id']}: {error}" for error in check.get("errors", []))
            warnings.extend(f"{check['id']}: {warning}" for warning in check.get("warnings", []))

    return {
        "schema_version": 1,
        "kind": REPORT_KIND,
        "repo_root": str(repo_root),
        "report": str(report_path),
        "passed": not errors,
        "errors": errors,
        "warnings": warnings,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "plan_count": len(checks),
        "checks": checks,
        "guardrails": {
            "report_only": True,
            "providers_executed": False,
            "blender_runtime_executed": False,
            "patches_applied": False,
            "source_files_written": False,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--report", default="Tools/ai/fixtures/agent_review_code_patch_plan_fixture.json")
    parser.add_argument("--output", help="Optional JSON report path.")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    report_path = Path(args.report)
    if not report_path.is_absolute():
        report_path = repo_root / report_path
    report_path = report_path.resolve()

    report = validate_report(repo_root, report_path)
    output = resolve_output_path(repo_root, args.output) if args.output else None
    text = write_json_report(report, output)
    print(text, end="")
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
