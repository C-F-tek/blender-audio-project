#!/usr/bin/env python3
"""Smoke-test generated patch specs -> apply report -> prepare_review_pr chain."""

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

STAMP = "generated_patch_specs_review_pr_lane_smoke_20990101-010203"
TARGET = "docs/LOCAL_AI_TASKS/generated-spec-target.md"
MARKER = "generated_patch_specs_review_pr_lane_marker"


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
        ["git", "config", "user.name", "Generated Patch Specs Smoke"], cwd=repo, check=True
    )

    target = repo / TARGET
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("# Generated Spec Target\n\nSeed content.\n", encoding="utf-8")
    subprocess.run(["git", "add", TARGET], cwd=repo, check=True, capture_output=True, text=True)
    subprocess.run(
        ["git", "commit", "-m", "seed generated spec target"],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
    )

    spec_dir = repo / "output/patch_specs/generated_spec_smoke"
    spec_dir.mkdir(parents=True, exist_ok=True)
    spec_path = spec_dir / "generated_spec_smoke.json"
    spec = {
        "schema_version": 1,
        "kind": "proposal_patch_spec_draft",
        "draft_status": "reviewed_concrete_operations",
        "operations": [
            {
                "operation": "append_once",
                "path": TARGET,
                "content": f"\n{MARKER}\n",
                "marker": MARKER,
                "proposal_id": "generated-spec-smoke",
                "artifact_kind": "markdown",
                "description": "append generated-spec smoke marker",
            }
        ],
    }
    spec_path.write_text(json.dumps(spec, indent=2) + "\n", encoding="utf-8")

    manifest = {
        "schema_version": 1,
        "kind": "proposal_patch_spec_manifest",
        "passed": True,
        "specs": [
            {
                "proposal_id": "generated-spec-smoke",
                "path": "output/patch_specs/generated_spec_smoke/generated_spec_smoke.json",
                "operation_count": 1,
            }
        ],
    }
    (repo / "output/patch_specs/generated_spec_smoke_manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n",
        encoding="utf-8",
    )
    return repo


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Generated Patch Specs Review PR Lane Smoke",
        "",
        f"- Passed: `{report['passed']}`",
        f"- Apply command return code: `{report.get('apply_command', {}).get('returncode')}`",
        f"- Prepare command return code: `{report.get('prepare_command', {}).get('returncode')}`",
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
        "--output", default="output/validation/generated_patch_specs_review_pr_lane_smoke.json"
    )
    parser.add_argument(
        "--markdown-output",
        default="output/validation/generated_patch_specs_review_pr_lane_smoke.md",
    )
    parser.add_argument("--timeout-seconds", type=int, default=90)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    source_repo = Path(args.repo_root).resolve()
    env = dict(os.environ)
    env["PYTHONPATH"] = str(source_repo)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    errors: list[str] = []

    with tempfile.TemporaryDirectory(prefix="generated-patch-specs-review-pr-lane-") as tmp_raw:
        repo = seed_repo(Path(tmp_raw))
        branch = f"codex/generated-spec-smoke-{STAMP}"
        apply_report_path = repo / "output/validation/generated_patch_specs_review_pr_apply.json"
        review_report_path = repo / "output/validation/review_pr_prepare.json"

        apply_command = [
            sys.executable,
            str(source_repo / "Tools/ai/apply_generated_patch_specs_for_review_pr.py"),
            "--repo-root",
            str(repo),
            "--manifest",
            "output/patch_specs/generated_spec_smoke_manifest.json",
            "--output",
            str(apply_report_path),
            "--max-applied-patches",
            "5",
            "--apply",
            "--create-review-branch",
            branch,
            "--require-all-validators",
        ]
        apply_result = run(apply_command, repo, env, args.timeout_seconds)
        apply_report = (
            json.loads(apply_report_path.read_text(encoding="utf-8-sig"))
            if apply_report_path.exists()
            else {}
        )

        if not apply_result["ok"]:
            errors.append(f"generated patch spec bridge failed rc={apply_result['returncode']}")
        if apply_report.get("passed") is not True:
            errors.append("generated patch spec apply report did not pass")
        if apply_report.get("patch_application_performed") is not True:
            errors.append("generated patch spec bridge did not apply the concrete operation")
        if apply_report.get("git_unsafe_status_before"):
            errors.append(
                f"safe output-only dirtiness should not be treated as unsafe: {apply_report.get('git_unsafe_status_before')}"
            )
        branch_prepare = (
            apply_report.get("git_review_branch_prepare") if isinstance(apply_report, dict) else {}
        )
        if isinstance(branch_prepare, dict) and branch_prepare.get("unsafe_status_before"):
            errors.append(
                f"branch preparation should ignore output-only dirtiness: {branch_prepare.get('unsafe_status_before')}"
            )
        if MARKER not in (repo / TARGET).read_text(encoding="utf-8"):
            errors.append("target marker was not written")

        prepare_command = [
            sys.executable,
            str(source_repo / "Tools/ai/prepare_review_pr.py"),
            "--repo-root",
            str(repo),
            "--Stamp",
            STAMP,
            "--task-file",
            "docs/LOCAL_AI_TASKS/generated-spec-smoke-task.md",
            "--branch",
            branch,
            "--base",
            "master",
            "--title",
            "docs(ai): generated patch specs review PR smoke",
            "--commit-message",
            "docs(ai): generated patch specs review PR smoke",
            "--apply-report",
            "output/validation/generated_patch_specs_review_pr_apply.json",
            "--auto-include-from-apply-report",
            "--output",
            str(review_report_path),
            "--allow-dirty-branch",
        ]
        prepare_result = run(prepare_command, repo, env, args.timeout_seconds)
        review_report = (
            json.loads(review_report_path.read_text(encoding="utf-8-sig"))
            if review_report_path.exists()
            else {}
        )

        if not prepare_result["ok"]:
            errors.append(f"prepare_review_pr.py failed rc={prepare_result['returncode']}")
        if review_report.get("passed") is not True:
            errors.append("review PR prepare report did not pass")
        if review_report.get("auto_include_paths") != [TARGET]:
            errors.append(
                f"unexpected auto include paths: {review_report.get('auto_include_paths')}"
            )
        if review_report.get("git_commit_performed") is not True:
            errors.append("review PR product commit was not performed")
        if review_report.get("github_pr_created") or review_report.get("git_push_performed"):
            errors.append("smoke unexpectedly pushed or created a PR")

    report = {
        "schema_version": 1,
        "kind": "generated_patch_specs_review_pr_lane_smoke",
        "repo_root": source_repo.as_posix(),
        "passed": not errors,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "git_push_performed": False,
        "github_pr_created": False,
        "apply_command": apply_result,
        "apply_report": apply_report,
        "prepare_command": prepare_result,
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
