#!/usr/bin/env python3
"""Build argv for agent_review_prepare_pr.py.

PowerShell remains the Windows wrapper. This helper owns review-PR argument
construction so product-output wiring is testable outside the large launcher.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any


def as_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return value != 0
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "y", "on"}
    return False


def split_include_paths(values: Any) -> list[str]:
    if values is None:
        return []
    if isinstance(values, str):
        raw_values = [values]
    elif isinstance(values, list):
        raw_values = values
    else:
        raw_values = [str(values)]

    result: list[str] = []
    for raw in raw_values:
        for part in str(raw).split(","):
            value = part.strip().strip("'").strip('"')
            if value and value not in result:
                result.append(value)
    return result


def repo_path(repo_root: Path, raw: str) -> Path:
    path = Path(raw)
    return path if path.is_absolute() else repo_root / path


def existing_or_blank(repo_root: Path, raw: Any) -> str:
    value = str(raw or "").strip()
    if not value:
        return ""
    path = repo_path(repo_root, value)
    return value if path.exists() else ""


def load_apply_report(repo_root: Path, raw: Any) -> tuple[dict[str, Any] | None, str]:
    value = str(raw or "").strip()
    if not value:
        return None, ""
    path = repo_path(repo_root, value)
    if not path.exists() or not path.is_file():
        return None, ""
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception:  # noqa: BLE001 - report validation is handled by agent_review_prepare_pr.py
        return None, value
    if not isinstance(data, dict):
        return None, value
    return data, value


def apply_report_has_product(report: dict[str, Any] | None) -> bool:
    if not isinstance(report, dict):
        return False
    if as_bool(report.get("source_writes_performed")) or as_bool(
        report.get("patch_application_performed")
    ):
        return True
    for item in report.get("results") or []:
        if (
            isinstance(item, dict)
            and item.get("ok") is not False
            and (item.get("changed") or item.get("applied"))
        ):
            return True
    return False


def add_pair(argv: list[str], flag: str, value: Any) -> None:
    text = str(value or "").strip()
    if text:
        argv.extend([flag, text])


def build_args(context: dict[str, Any]) -> dict[str, Any]:
    repo_root = Path(str(context.get("repo_root") or ".")).resolve()

    errors: list[str] = []
    warnings: list[str] = []

    required = [
        "stamp",
        "task_file",
        "branch",
        "base",
        "remote",
        "title",
        "commit_message",
        "output",
        "markdown_output",
        "evidence_output",
        "evidence_markdown_output",
    ]
    for key in required:
        if not str(context.get(key) or "").strip():
            errors.append(f"{key} is required")

    argv = [
        "-m",
        "ia_carmine",
        "agent_review_prepare_pr",
        "--repo-root",
        ".",
    ]
    add_pair(argv, "--Stamp", context.get("stamp"))
    add_pair(argv, "--task-file", context.get("task_file"))
    add_pair(argv, "--branch", context.get("branch"))
    add_pair(argv, "--base", context.get("base"))
    add_pair(argv, "--remote", context.get("remote"))
    add_pair(argv, "--title", context.get("title"))
    add_pair(argv, "--commit-message", context.get("commit_message"))
    add_pair(argv, "--output", context.get("output"))
    add_pair(argv, "--markdown-output", context.get("markdown_output"))
    add_pair(argv, "--evidence-output", context.get("evidence_output"))
    add_pair(argv, "--evidence-markdown-output", context.get("evidence_markdown_output"))

    if as_bool(context.get("allow_dirty_branch", True)):
        argv.append("--allow-dirty-branch")

    include_paths = split_include_paths(context.get("include_paths"))
    for path in include_paths:
        argv.extend(["--include-path", path])

    apply_report_requested = str(context.get("apply_report") or "").strip()
    apply_report_data, apply_report = load_apply_report(repo_root, apply_report_requested)
    auto_include = as_bool(context.get("auto_include_from_apply_report"))
    apply_report_product = apply_report_has_product(apply_report_data)
    require_product_input = as_bool(context.get("require_product_input"))
    if apply_report and auto_include:
        argv.extend(["--apply-report", apply_report, "--auto-include-from-apply-report"])
    elif apply_report_requested and auto_include:
        warnings.append(f"apply_report not found, auto include omitted: {apply_report_requested}")

    if require_product_input and not include_paths and not apply_report:
        errors.append(
            "review PR product input missing: provide explicit include_paths or a generated apply_report "
            "before invoking agent_review_prepare_pr.py"
        )
    elif require_product_input and not include_paths and apply_report and not apply_report_product:
        errors.append(
            "review PR product input is not concrete: apply_report exists but does not declare "
            "source_writes_performed=true, patch_application_performed=true, or changed/applied results"
        )

    push_requested = as_bool(context.get("push"))
    create_pr_requested = as_bool(context.get("create_pr"))
    draft_pr_requested = as_bool(context.get("draft_pr"))
    dry_run_requested = as_bool(context.get("dry_run"))

    if create_pr_requested and not push_requested:
        errors.append("create_pr requires push so the review branch exists on the remote")
    if draft_pr_requested and not create_pr_requested:
        errors.append("draft_pr requires create_pr")

    if push_requested:
        argv.append("--push")
    if create_pr_requested:
        argv.append("--create-pr")
    if draft_pr_requested:
        argv.append("--draft-pr")
    if dry_run_requested:
        argv.append("--dry-run")

    return {
        "schema_version": 1,
        "kind": "review_pr_prepare_args",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "repo_root": repo_root.as_posix(),
        "passed": not errors,
        "argv": argv,
        "derived": {
            "include_path_count": len(include_paths),
            "apply_report": apply_report,
            "apply_report_product": apply_report_product,
            "require_product_input": require_product_input,
            "auto_include_from_apply_report": bool(apply_report and auto_include),
            "push": push_requested,
            "create_pr": create_pr_requested,
            "draft_pr": draft_pr_requested,
            "dry_run": dry_run_requested,
        },
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "errors": errors,
        "warnings": warnings,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--context", required=True)
    parser.add_argument("--output", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    context_path = Path(args.context)
    output_path = Path(args.output)

    context = json.loads(context_path.read_text(encoding="utf-8-sig"))
    if not isinstance(context, dict):
        raise SystemExit("context JSON root must be an object")

    report = build_args(context)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
