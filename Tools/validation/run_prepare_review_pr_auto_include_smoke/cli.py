#!/usr/bin/env python3
"""Smoke test for prepare_review_pr.py apply-report include-path autodiscovery."""

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
    from Tools.validation._shared.report_utils import resolve_output_path, write_json_report, write_text_report
except ImportError:
    from Tools.validation._shared.report_utils import (  # type: ignore
        resolve_output_path,
        write_json_report,
        write_text_report,
    )

STAMP = "prepare_review_pr_auto_include_smoke_20990101-010203"
TARGET = "docs/LOCAL_AI_TASKS/auto-include-target.md"
MARKER = "prepare_review_pr_auto_include_marker"


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
    subprocess.run(["git", "config", "user.name", "Prepare Review PR Smoke"], cwd=repo, check=True)
    target = repo / TARGET
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("# Auto Include Target\n\nSeed content.\n", encoding="utf-8")
    subprocess.run(["git", "add", TARGET], cwd=repo, check=True, capture_output=True, text=True)
    subprocess.run(
        ["git", "commit", "-m", "seed target"], cwd=repo, check=True, capture_output=True, text=True
    )
    target.write_text(target.read_text(encoding="utf-8") + f"\n{MARKER}\n", encoding="utf-8")
    report = {
        "schema_version": 1,
        "kind": "patch_suggestion_bundle_apply",
        "passed": True,
        "apply_requested": True,
        "patch_application_performed": True,
        "source_writes_performed": True,
        "results": [
            {
                "operation": "append_once",
                "path": TARGET,
                "ok": True,
                "changed": True,
                "applied": True,
                "line_count_after": 5,
            }
        ],
        "manual_review_product": {
            "ready_for_patch_suggestion_review": True,
            "product_facing_manual_review_items": [
                {
                    "id": "auto-include-smoke",
                    "target_files": [TARGET],
                    "title": "Auto include smoke",
                }
            ],
        },
    }
    apply_report = repo / "output/validation/patch_suggestion_bundle_apply.json"
    apply_report.parent.mkdir(parents=True, exist_ok=True)
    apply_report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return repo


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Prepare Review PR Auto Include Smoke",
        "",
        f"- Passed: `{report['passed']}`",
        f"- Command return code: `{report.get('command', {}).get('returncode')}`",
        f"- Auto include paths: `{report.get('review_report', {}).get('auto_include_paths')}`",
        f"- Product commit: `{report.get('review_report', {}).get('product_commit')}`",
    ]
    if report.get("errors"):
        lines.extend(["", "## Errors", ""])
        lines.extend(f"- {error}" for error in report["errors"])
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument(
        "--output", default="output/validation/prepare_review_pr_auto_include_smoke.json"
    )
    parser.add_argument(
        "--markdown-output", default="output/validation/prepare_review_pr_auto_include_smoke.md"
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
    with tempfile.TemporaryDirectory(prefix="prepare-review-pr-auto-include-") as tmp_raw:
        repo = seed_repo(Path(tmp_raw))
        review_json = repo / "output/validation/review_pr_prepare.json"
        command = [
            sys.executable,
            "-m",
            "Tools.ai",
            "prepare_review_pr",
            "--repo-root",
            str(repo),
            "--Stamp",
            STAMP,
            "--task-file",
            "docs/LOCAL_AI_TASKS/smoke-task.md",
            "--branch",
            f"CARMINEai/auto-include-smoke-{STAMP}",
            "--base",
            "master",
            "--title",
            "docs(ai): prepare review PR auto include smoke",
            "--commit-message",
            "docs(ai): prepare review PR auto include smoke",
            "--apply-report",
            "output/validation/patch_suggestion_bundle_apply.json",
            "--auto-include-from-apply-report",
            "--output",
            str(review_json),
            "--allow-dirty-branch",
        ]
        command_result = run(command, repo, env, args.timeout_seconds)
        review_report = (
            json.loads(review_json.read_text(encoding="utf-8-sig")) if review_json.exists() else {}
        )
        if not command_result["ok"]:
            errors.append(f"prepare_review_pr.py failed rc={command_result['returncode']}")
        if review_report.get("passed") is not True:
            errors.append("review PR prepare report did not pass")
        if review_report.get("auto_include_paths") != [TARGET]:
            errors.append(
                f"unexpected auto include paths: {review_report.get('auto_include_paths')}"
            )
        if review_report.get("manual_include_paths"):
            errors.append("manual include paths should be empty in auto-include smoke")
        if review_report.get("git_commit_performed") is not True:
            errors.append("product commit was not performed")
        if review_report.get("github_pr_created") or review_report.get("git_push_performed"):
            errors.append("smoke unexpectedly pushed or created a PR")
    report = {
        "schema_version": 1,
        "kind": "prepare_review_pr_auto_include_smoke",
        "repo_root": source_repo.as_posix(),
        "passed": not errors,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "git_push_performed": False,
        "github_pr_created": False,
        "command": command_result,
        "review_report": review_report,
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
