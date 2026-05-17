#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    from report_utils import resolve_output_path, write_json_report, write_text_report
except ImportError:
    from Tools.validation.report_utils import (  # type: ignore
        resolve_output_path,
        write_json_report,
        write_text_report,
    )


def load_json(path: Path) -> tuple[dict[str, Any] | None, str]:
    if not path.exists() or not path.is_file():
        return None, f"missing file: {path.as_posix()}"
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        return None, f"{type(exc).__name__}: {exc}"
    if not isinstance(data, dict):
        return None, "JSON root must be an object"
    return data, ""


def truthy(value: Any) -> bool:
    return value is True


def nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def write_markdown(report: dict[str, Any], output: Path) -> str:
    lines = [
        "# Review PR Final Product Contract",
        "",
        f"- Passed: `{report.get('passed')}`",
        f"- Mode: `{report.get('contract_mode')}`",
        f"- Branch: `{report.get('branch')}`",
        f"- Product commit: `{report.get('product_commit')}`",
        f"- Push performed: `{report.get('git_push_performed')}`",
        f"- GitHub PR created: `{report.get('github_pr_created')}`",
        f"- GitHub PR URL: `{report.get('github_pr_url') or ''}`",
        "",
        "## Checks",
        "",
    ]
    for key, value in sorted((report.get("checks") or {}).items()):
        lines.append(f"- `{key}`: `{value}`")
    if report.get("errors"):
        lines.extend(["", "## Errors", ""])
        lines.extend(f"- {item}" for item in report["errors"])
    if report.get("warnings"):
        lines.extend(["", "## Warnings", ""])
        lines.extend(f"- {item}" for item in report["warnings"])
    return write_text_report("\n".join(lines) + "\n", output)


def build_report(
    repo_root: Path, review_pr_report: Path, require_remote_pr: bool
) -> dict[str, Any]:
    data, error = load_json(review_pr_report)
    errors: list[str] = []
    warnings: list[str] = []
    if error:
        errors.append(error)
        data = {}

    commands = data.get("commands") if isinstance(data, dict) else []
    if not isinstance(commands, list):
        commands = []

    branch = data.get("branch") if isinstance(data, dict) else ""
    base_branch = data.get("base_branch") if isinstance(data, dict) else ""
    include_paths = data.get("include_paths") if isinstance(data, dict) else []
    product_commit = data.get("product_commit") if isinstance(data, dict) else ""
    github_pr_url = data.get("github_pr_url") if isinstance(data, dict) else ""
    report_passed = truthy(data.get("passed")) if isinstance(data, dict) else False
    git_commit_performed = (
        truthy(data.get("git_commit_performed")) if isinstance(data, dict) else False
    )
    git_push_performed = truthy(data.get("git_push_performed")) if isinstance(data, dict) else False
    github_pr_created = truthy(data.get("github_pr_created")) if isinstance(data, dict) else False
    draft_requested = (
        truthy(data.get("github_pr_draft_requested")) if isinstance(data, dict) else False
    )

    checks = {
        "review_pr_report_passed": report_passed,
        "branch_present": nonempty_string(branch),
        "base_branch_supported": base_branch in {"master", "main"},
        "include_paths_present": isinstance(include_paths, list) and len(include_paths) > 0,
        "product_commit_performed": git_commit_performed,
        "product_commit_present": nonempty_string(product_commit),
        "no_provider_execution": data.get("provider_execution_performed") is False
        if isinstance(data, dict)
        else False,
        "no_patch_application_in_prepare_step": data.get("patch_application_performed") is False
        if isinstance(data, dict)
        else False,
        "no_source_writes_in_prepare_step": data.get("source_writes_performed") is False
        if isinstance(data, dict)
        else False,
        "no_force_push_command": not any(
            "--force" in " ".join(str(part) for part in (cmd.get("command") or []))
            for cmd in commands
            if isinstance(cmd, dict)
        ),
    }

    if require_remote_pr:
        checks.update(
            {
                "remote_push_performed": git_push_performed,
                "github_pr_created": github_pr_created,
                "github_pr_url_present": nonempty_string(github_pr_url)
                and "github.com/" in github_pr_url,
            }
        )
    else:
        checks.update(
            {
                "remote_push_not_required": True,
                "github_pr_not_required": True,
            }
        )
        if git_push_performed and not github_pr_created:
            warnings.append("git push performed but GitHub PR was not created")

    for name, passed in checks.items():
        if not passed:
            errors.append(f"review PR final product check failed: {name}")

    return {
        "schema_version": 1,
        "kind": "review_pr_final_product_contract",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "repo_root": repo_root.as_posix(),
        "review_pr_report": review_pr_report.as_posix(),
        "contract_mode": "remote_pr_required"
        if require_remote_pr
        else "local_review_branch_required",
        "branch": branch,
        "base_branch": base_branch,
        "include_paths": include_paths if isinstance(include_paths, list) else [],
        "product_commit": product_commit,
        "git_push_performed": git_push_performed,
        "github_pr_created": github_pr_created,
        "github_pr_draft_requested": draft_requested,
        "github_pr_url": github_pr_url,
        "checks": checks,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "passed": not errors,
        "errors": errors,
        "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--review-pr-report", required=True)
    parser.add_argument("--require-remote-pr", action="store_true")
    parser.add_argument(
        "--output", default="output/validation/review_pr_final_product_contract.json"
    )
    parser.add_argument("--markdown-output", default="")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    review_pr_report = Path(args.review_pr_report)
    if not review_pr_report.is_absolute():
        review_pr_report = repo_root / review_pr_report

    report = build_report(repo_root, review_pr_report, bool(args.require_remote_pr))
    output = resolve_output_path(repo_root, args.output)
    write_json_report(report, output)
    if args.markdown_output:
        write_markdown(report, resolve_output_path(repo_root, args.markdown_output))
    print(write_json_report(report), end="")
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
