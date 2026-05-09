#!/usr/bin/env python3
"""Smoke-test that unified launcher forbids ContinueOnValidationError."""
from __future__ import annotations

import argparse
import subprocess
from pathlib import Path
from typing import Any

try:
    from report_utils import resolve_output_path, write_json_report, write_text_report
except ImportError:
    from Tools.validation.report_utils import resolve_output_path, write_json_report, write_text_report  # type: ignore


def run(command: list[str], cwd: Path) -> dict[str, Any]:
    result = subprocess.run(command, cwd=cwd, capture_output=True, text=True, check=False, timeout=120)
    return {
        "command": command,
        "returncode": result.returncode,
        "stdout_tail": result.stdout[-4000:],
        "stderr_tail": result.stderr[-4000:],
        "ok": result.returncode == 0,
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Unified Launcher ContinueOnValidationError Guard Smoke",
        "",
        f"- Passed: `{report.get('passed')}`",
        f"- Return code: `{report.get('command', {}).get('returncode')}`",
        "",
    ]
    if report.get("errors"):
        lines.extend(["## Errors", ""])
        lines.extend(f"- {error}" for error in report["errors"])
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output", default="output/validation/unified_launcher_forbid_continue_on_validation_error_smoke.json")
    parser.add_argument("--markdown-output", default="output/validation/unified_launcher_forbid_continue_on_validation_error_smoke.md")
    args = parser.parse_args()

    repo = Path(args.repo_root).resolve()
    command = [
        "powershell.exe",
        "-NoProfile",
        "-ExecutionPolicy",
        "Bypass",
        "-File",
        str(repo / "Tools/workflow/run_unified_local_ai_refactor.ps1"),
        "-RepoRoot",
        str(repo),
        "-Mode",
        "smoke",
        "-NoBranch",
        "-SkipGitSync",
        "-ContinueOnValidationError",
    ]
    result = run(command, repo)
    combined = f"{result.get('stdout_tail', '')}\n{result.get('stderr_tail', '')}"
    errors: list[str] = []

    if result["returncode"] == 0:
        errors.append("launcher accepted forbidden -ContinueOnValidationError")
    if "-ContinueOnValidationError is forbidden" not in combined:
        errors.append("forbidden flag error message was not emitted")

    report = {
        "schema_version": 1,
        "kind": "unified_launcher_forbid_continue_on_validation_error_smoke",
        "repo_root": repo.as_posix(),
        "passed": not errors,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "command": result,
        "errors": errors,
        "warnings": [],
    }

    output = resolve_output_path(repo, args.output)
    markdown = resolve_output_path(repo, args.markdown_output)
    print(write_json_report(report, output), end="")
    write_text_report(render_markdown(report), markdown)
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
