#!/usr/bin/env python3
"""Smoke-test prepare_review_pr.py PR creation flag guardrails."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
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

TARGET = "docs/LOCAL_AI_TASKS/flag-smoke-target.md"


def run(command: list[str], cwd: Path, env: dict[str, str], timeout: int) -> dict[str, Any]:
    try:
        result = subprocess.run(
            command, cwd=cwd, env=env, capture_output=True, text=True, check=False, timeout=timeout
        )
        return {
            "command": command,
            "returncode": result.returncode,
            "stdout": result.stdout.strip()[:4000],
            "stderr": result.stderr.strip()[:4000],
            "ok": result.returncode == 0,
        }
    except subprocess.TimeoutExpired as exc:
        return {
            "command": command,
            "returncode": 124,
            "stdout": str(exc.stdout or "")[:4000],
            "stderr": str(exc.stderr or "")[:4000],
            "ok": False,
            "error": f"TimeoutExpired: {timeout}s",
        }


def seed_repo(root: Path) -> Path:
    repo = root / "repo"
    repo.mkdir()
    subprocess.run(
        ["git", "init", "-b", "master"], cwd=repo, check=True, capture_output=True, text=True
    )
    subprocess.run(["git", "config", "user.email", "smoke@example.invalid"], cwd=repo, check=True)
    subprocess.run(
        ["git", "config", "user.name", "Prepare Review PR Flag Smoke"], cwd=repo, check=True
    )
    target = repo / TARGET
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("# Flag Smoke Target\n\nSeed content.\n", encoding="utf-8")
    subprocess.run(["git", "add", TARGET], cwd=repo, check=True, capture_output=True, text=True)
    subprocess.run(
        ["git", "commit", "-m", "seed target"], cwd=repo, check=True, capture_output=True, text=True
    )
    return repo


def write_apply_report(
    repo: Path, *, source_writes_performed: bool, patch_application_performed: bool
) -> Path:
    report_path = repo / "output/validation/dry_run_apply_report.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report = {
        "schema_version": 1,
        "kind": "patch_suggestion_bundle_apply",
        "passed": True,
        "apply_requested": False,
        "patch_application_performed": patch_application_performed,
        "source_writes_performed": source_writes_performed,
        "operation_count": 1,
        "changed_count": 1 if source_writes_performed else 0,
        "results": [
            {
                "operation": "append_once",
                "path": TARGET,
                "ok": True,
                "changed": True,
                "applied": patch_application_performed,
            }
        ],
        "errors": [],
        "warnings": [],
    }
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return report_path


def prepare_command(
    source_repo: Path, repo: Path, output: str, extra_flags: list[str]
) -> list[str]:
    return [
        sys.executable,
        str(source_repo / "Tools/ai/prepare_review_pr.py"),
        "--repo-root",
        str(repo),
        "--Stamp",
        "prepare_review_pr_flag_smoke_20990101-010203",
        "--task-file",
        "docs/LOCAL_AI_TASKS/smoke-task.md",
        "--branch",
        "CARMINEai/prepare-review-pr-flag-smoke",
        "--base",
        "master",
        "--title",
        "docs(ai): prepare review PR flag smoke",
        "--commit-message",
        "docs(ai): prepare review PR flag smoke",
        "--include-path",
        TARGET,
        "--output",
        output,
        "--dry-run",
        *extra_flags,
    ]


def auto_include_command(
    source_repo: Path, repo: Path, output: str, apply_report: Path
) -> list[str]:
    return [
        sys.executable,
        str(source_repo / "Tools/ai/prepare_review_pr.py"),
        "--repo-root",
        str(repo),
        "--Stamp",
        "prepare_review_pr_flag_smoke_20990101-010203",
        "--task-file",
        "docs/LOCAL_AI_TASKS/smoke-task.md",
        "--branch",
        "CARMINEai/prepare-review-pr-auto-include-smoke",
        "--base",
        "master",
        "--title",
        "docs(ai): prepare review PR auto include smoke",
        "--commit-message",
        "docs(ai): prepare review PR auto include smoke",
        "--apply-report",
        str(apply_report),
        "--auto-include-from-apply-report",
        "--output",
        output,
        "--dry-run",
    ]


def run_case(
    source_repo: Path, repo: Path, env: dict[str, str], timeout: int, name: str, flags: list[str]
) -> dict[str, Any]:
    output = f"output/validation/{name}.json"
    command = prepare_command(source_repo, repo, output, flags)
    command_result = run(command, repo, env, timeout)
    report_path = repo / output
    report = json.loads(report_path.read_text(encoding="utf-8-sig")) if report_path.exists() else {}
    return {"name": name, "flags": flags, "command": command_result, "report": report}


def run_auto_include_case(
    source_repo: Path, repo: Path, env: dict[str, str], timeout: int
) -> dict[str, Any]:
    output = "output/validation/auto_include_dry_run_apply_report.json"
    apply_report = write_apply_report(
        repo, source_writes_performed=False, patch_application_performed=False
    )
    command = auto_include_command(source_repo, repo, output, apply_report)
    command_result = run(command, repo, env, timeout)
    report_path = repo / output
    report = json.loads(report_path.read_text(encoding="utf-8-sig")) if report_path.exists() else {}
    return {
        "name": "auto_include_dry_run_apply_report",
        "flags": ["--auto-include-from-apply-report"],
        "command": command_result,
        "report": report,
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Prepare Review PR Flag Smoke",
        "",
        f"- Passed: `{report['passed']}`",
        f"- Error count: `{len(report['errors'])}`",
        "",
    ]
    if report["errors"]:
        lines.extend(["## Errors", ""])
        lines.extend(f"- {error}" for error in report["errors"])
        lines.append("")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output", default="output/validation/prepare_review_pr_flag_smoke.json")
    parser.add_argument(
        "--markdown-output", default="output/validation/prepare_review_pr_flag_smoke.md"
    )
    parser.add_argument("--timeout-seconds", type=int, default=60)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    source_repo = Path(args.repo_root).resolve()
    env = dict(os.environ)
    env["PYTHONPATH"] = str(source_repo)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    errors: list[str] = []
    cases: list[dict[str, Any]] = []
    with tempfile.TemporaryDirectory(prefix="prepare-review-pr-flag-smoke-") as tmp_raw:
        repo = seed_repo(Path(tmp_raw))
        cases.append(
            run_case(
                source_repo,
                repo,
                env,
                args.timeout_seconds,
                "create_pr_without_push",
                ["--create-pr"],
            )
        )
        cases.append(
            run_case(
                source_repo,
                repo,
                env,
                args.timeout_seconds,
                "draft_without_create_pr",
                ["--draft-pr"],
            )
        )
        cases.append(run_auto_include_case(source_repo, repo, env, args.timeout_seconds))
    expected_errors = {
        "create_pr_without_push": "--create-pr requires --push",
        "draft_without_create_pr": "--draft-pr requires --create-pr",
        "auto_include_dry_run_apply_report": "auto include from apply report requires at least one report with source_writes_performed=true or patch_application_performed=true",
    }
    for case in cases:
        case_errors = case.get("report", {}).get("errors") or []
        if case.get("command", {}).get("returncode") == 0:
            errors.append(f"{case['name']}: command unexpectedly passed")
        if case.get("report", {}).get("passed") is not False:
            errors.append(f"{case['name']}: report did not fail as expected")
        if not any(str(error).startswith(expected_errors[case["name"]]) for error in case_errors):
            errors.append(f"{case['name']}: expected guardrail error missing: {case_errors}")
    report = {
        "schema_version": 1,
        "kind": "prepare_review_pr_flag_smoke",
        "repo_root": source_repo.as_posix(),
        "passed": not errors,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "git_push_performed": False,
        "github_pr_created": False,
        "cases": cases,
        "errors": errors,
        "warnings": [],
    }
    output = resolve_output_path(source_repo, args.output)
    markdown = resolve_output_path(source_repo, args.markdown_output)
    print(write_json_report(report, output), end="")
    write_text_report(render_markdown(report), markdown)
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
