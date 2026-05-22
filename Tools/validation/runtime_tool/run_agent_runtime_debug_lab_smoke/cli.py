#!/usr/bin/env python3
"""Smoke-test the report-only agent runtime debug lab."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any

try:
    from ia_carmine.runtime.runtime_tool.agent_runtime_debug_lab.reporting import (
        render_markdown as render_debug_lab_markdown,
        write_reports as write_debug_lab_reports,
    )
    from ia_carmine.runtime.runtime_tool.agent_runtime_debug_lab.runner import run_request
    from Tools.validation._shared.report_utils import resolve_output_path, write_json_report, write_text_report
except ImportError:
    from ia_carmine.runtime.runtime_tool.agent_runtime_debug_lab.reporting import (  # type: ignore
        render_markdown as render_debug_lab_markdown,
        write_reports as write_debug_lab_reports,
    )
    from ia_carmine.runtime.runtime_tool.agent_runtime_debug_lab.runner import run_request  # type: ignore
    from Tools.validation._shared.report_utils import (  # type: ignore
        resolve_output_path,
        write_json_report,
        write_text_report,
    )


def run(command: list[str], cwd: Path, timeout: int) -> dict[str, Any]:
    result = subprocess.run(
        command, cwd=cwd, capture_output=True, text=True, check=False, timeout=timeout
    )
    return {
        "command": command,
        "returncode": result.returncode,
        "stdout": result.stdout[-4000:],
        "stderr": result.stderr[-4000:],
        "ok": result.returncode == 0,
    }


def build_request(operations: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "kind": "agent_runtime_debug_lab_request",
        "schema_version": 1,
        "operations": operations,
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Agent Runtime Debug Lab Smoke",
        "",
        f"- Passed: `{report.get('passed')}`",
        f"- Errors: `{len(report.get('errors', []))}`",
        "",
        "## Commands",
        "",
    ]
    for item in report.get("commands") or []:
        lines.append(
            f"- `{item['name']}` rc=`{item['result'].get('returncode')}` ok=`{item['result'].get('ok')}`"
        )
    if report.get("errors"):
        lines.extend(["", "## Errors", ""])
        lines.extend(f"- {error}" for error in report["errors"])
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output", default="output/validation/agent_runtime_debug_lab_smoke.json")
    parser.add_argument(
        "--markdown-output", default="output/validation/agent_runtime_debug_lab_smoke.md"
    )
    parser.add_argument("--timeout-seconds", type=int, default=120)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    valid_report = repo_root / "output/validation/agent_runtime_debug_lab_valid.json"
    valid_md = repo_root / "output/validation/agent_runtime_debug_lab_valid.md"
    invalid_report = repo_root / "output/validation/agent_runtime_debug_lab_invalid.json"
    invalid_md = repo_root / "output/validation/agent_runtime_debug_lab_invalid.md"

    valid_request = build_request(
        [
            {
                "id": "compile_report_utils",
                "type": "python_compile",
                "paths": ["Tools/validation/_shared/report_utils.py"],
            },
            {
                "id": "parse_launcher",
                "type": "powershell_parse",
                "paths": ["Tools/workflow/_powershell/run_unified_local_ai_refactor.ps1"],
            },
            {"id": "diff_check", "type": "git_diff_check"},
            {"id": "status_short", "type": "git_status_short"},
        ],
    )
    invalid_request = build_request(
        [
            {"id": "forbid_shell", "type": "free_shell", "command": "echo unsafe"},
            {
                "id": "forbid_output_source",
                "type": "python_compile",
                "paths": ["output/validation/generated.py"],
            },
        ],
    )

    valid_data = run_request(
        repo_root=repo_root,
        request=valid_request,
        timeout_seconds=args.timeout_seconds,
        tail_chars=4000,
    )
    write_debug_lab_reports(
        repo_root=repo_root,
        output=str(valid_report),
        markdown_output=str(valid_md),
        report=valid_data,
        markdown=render_debug_lab_markdown(valid_data),
    )
    valid_returncode = 0 if valid_data.get("passed") is True else 2

    invalid_data = run_request(
        repo_root=repo_root,
        request=invalid_request,
        timeout_seconds=args.timeout_seconds,
        tail_chars=4000,
    )
    write_debug_lab_reports(
        repo_root=repo_root,
        output=str(invalid_report),
        markdown_output=str(invalid_md),
        report=invalid_data,
        markdown=render_debug_lab_markdown(invalid_data),
    )
    invalid_returncode = 0 if invalid_data.get("passed") is True else 2

    errors: list[str] = []
    if valid_returncode != 0 or valid_data.get("passed") is not True:
        errors.append("valid debug lab request did not pass")
    guardrails = valid_data.get("guardrails") or {}
    for key in (
        "free_shell_exposed",
        "provider_execution_performed",
        "patch_application_performed",
        "source_writes_performed",
        "git_write_performed",
        "blender_runtime_execution_performed",
        "ffmpeg_runtime_execution_performed",
    ):
        if guardrails.get(key) is not False:
            errors.append(f"guardrail {key} must be false")
    if guardrails.get("allowlist_enforced") is not True:
        errors.append("allowlist_enforced must be true")
    if invalid_returncode == 0 or invalid_data.get("passed") is not False:
        errors.append("invalid debug lab request was not rejected")
    if invalid_data.get("failed_count", 0) < 1:
        errors.append("invalid request did not report failures")

    report = {
        "schema_version": 1,
        "kind": "agent_runtime_debug_lab_smoke",
        "repo_root": repo_root.as_posix(),
        "passed": not errors,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "git_write_performed": False,
        "commands": [
            {
                "name": "valid_request",
                "result": {
                    "returncode": valid_returncode,
                    "ok": valid_returncode == 0,
                    "request_transport": "in_memory",
                },
            },
            {
                "name": "invalid_request",
                "result": {
                    "returncode": invalid_returncode,
                    "ok": invalid_returncode != 0,
                    "request_transport": "in_memory",
                },
            },
        ],
        "valid_report": valid_data,
        "invalid_report": invalid_data,
        "errors": errors,
        "warnings": [],
    }
    output = resolve_output_path(repo_root, args.output)
    markdown = resolve_output_path(repo_root, args.markdown_output)
    print(write_json_report(report, output), end="")
    write_text_report(render_markdown(report), markdown)
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
