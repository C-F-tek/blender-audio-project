#!/usr/bin/env python3
"""Smoke-test task patch suggestion Markdown authoring and script-path imports."""

from __future__ import annotations

import argparse
import json
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


def run(command: list[str], cwd: Path, timeout: int = 120) -> dict[str, Any]:
    result = subprocess.run(
        command, cwd=cwd, capture_output=True, text=True, check=False, timeout=timeout
    )
    return {
        "command": command,
        "returncode": result.returncode,
        "stdout_tail": result.stdout[-4000:],
        "stderr_tail": result.stderr[-4000:],
        "ok": result.returncode == 0,
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Task Patch Suggestion Markdown Authoring Smoke",
        "",
        f"- Passed: `{report.get('passed')}`",
        f"- Commands: `{len(report.get('commands') or [])}`",
        "",
        "## Commands",
        "",
    ]
    for item in report.get("commands") or []:
        lines.append(
            f"- `{item['name']}` rc=`{item['result']['returncode']}` ok=`{item['result']['ok']}`"
        )
    if report.get("errors"):
        lines.extend(["", "## Errors", ""])
        lines.extend(f"- {error}" for error in report["errors"])
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument(
        "--output", default="output/validation/task_patch_suggestion_markdown_authoring_smoke.json"
    )
    parser.add_argument(
        "--markdown-output",
        default="output/validation/task_patch_suggestion_markdown_authoring_smoke.md",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    source_repo = Path(args.repo_root).resolve()
    errors: list[str] = []
    commands: list[dict[str, Any]] = []

    with tempfile.TemporaryDirectory(prefix="task-patch-md-smoke-") as tmp:
        repo = Path(tmp) / "repo"
        repo.mkdir()
        run(["git", "init"], repo)
        task = "docs/LOCAL_AI_TASKS/task-patch-md-authoring-smoke.md"
        target = "docs/LOCAL_AI_TASKS/task-patch-md-authoring-target.md"
        report_json = "output/validation/task_patch_suggestion_report.json"
        dry_json = "output/validation/patch_suggestion_dry.json"
        create_json = "output/validation/create_task_patch_suggestion_markdown.json"
        create_cmd = [
            sys.executable,
            str(source_repo / "ia_carmine/product/patch_product/task_patch_suggestion_markdown/cli.py"),
            "--repo-root",
            str(repo),
            "--task-file",
            task,
            "--title",
            "Task Patch Markdown Authoring Smoke",
            "--goal",
            "Verify helper emits a parseable patch_suggestion fenced JSON block.",
            "--suggestion-id",
            "task-patch-md-authoring-smoke",
            "--suggestion-title",
            "Append operator gate",
            "--target-path",
            target,
            "--marker",
            "<!-- TASK_PATCH_MD_AUTHORING_SMOKE -->",
            "--content",
            "\n<!-- TASK_PATCH_MD_AUTHORING_SMOKE -->\n\nOperator confirmation gate.\n",
            "--output",
            create_json,
        ]
        create_result = run(create_cmd, source_repo)
        commands.append({"name": "create_task_patch_suggestion_markdown", "result": create_result})

        report_cmd = [
            sys.executable,
            str(source_repo / "ia_carmine/product/patch_product/task_patch_suggestion_report/cli.py"),
            "--repo-root",
            str(repo),
            "--task-file",
            task,
            "--output",
            report_json,
            "--markdown-output",
            "output/validation/task_patch_suggestion_report.md",
        ]
        report_result = run(report_cmd, source_repo)
        commands.append(
            {"name": "build_task_patch_suggestion_report_script_path", "result": report_result}
        )

        dry_cmd = [
            sys.executable,
            str(source_repo / "ia_carmine/product/patch_product/patch_suggestion_bundle/cli.py"),
            "--repo-root",
            str(repo),
            "--suggestion-report",
            report_json,
            "--output",
            dry_json,
        ]
        dry_result = run(dry_cmd, source_repo)
        commands.append({"name": "apply_patch_suggestion_bundle_dry", "result": dry_result})

        task_text = (repo / task).read_text(encoding="utf-8") if (repo / task).exists() else ""
        report_data = (
            json.loads((repo / report_json).read_text(encoding="utf-8-sig"))
            if (repo / report_json).exists()
            else {}
        )
        dry_data = (
            json.loads((repo / dry_json).read_text(encoding="utf-8-sig"))
            if (repo / dry_json).exists()
            else {}
        )

        if "```patch_suggestion" not in task_text:
            errors.append("generated task Markdown is missing patch_suggestion fence")
        if report_data.get("passed") is not True or report_data.get("operation_count") != 1:
            errors.append("generated task Markdown did not produce one deterministic operation")
        if dry_data.get("passed") is not True or dry_data.get("changed_count") != 1:
            errors.append("dry-run did not detect one changed target")
        result_paths = [
            item.get("path") for item in dry_data.get("results") or [] if isinstance(item, dict)
        ]
        if target not in result_paths:
            errors.append("dry-run did not target the separate generated target file")
        for item in commands:
            if item["result"].get("ok") is not True:
                errors.append(f"{item['name']} failed")

    report = {
        "schema_version": 1,
        "kind": "task_patch_suggestion_markdown_authoring_smoke",
        "repo_root": source_repo.as_posix(),
        "passed": not errors,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "commands": commands,
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
