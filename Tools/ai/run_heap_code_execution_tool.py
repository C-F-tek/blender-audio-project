#!/usr/bin/env python3
"""Build and run a report-only heap code execution matrix."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

try:
    from tools.ai.heap_code_execution_tool_core import (
        build_debug_lab_request,
        default_debug_lab_paths,
        git_diff_excerpt,
        now_iso,
        proposal_items,
        read_json,
        render_markdown,
        resolve_path,
        repo_rel,
        run_debug_lab,
        split_values,
        validate_target,
        validate_validation_script,
    )
    from tools.validation.report_utils import write_json_report, write_text_report
except ImportError:
    repo_root_for_import = Path(__file__).resolve().parents[2]
    if str(repo_root_for_import) not in sys.path:
        sys.path.insert(0, str(repo_root_for_import))
    from tools.ai.heap_code_execution_tool_core import (  # type: ignore
        build_debug_lab_request,
        default_debug_lab_paths,
        git_diff_excerpt,
        now_iso,
        proposal_items,
        read_json,
        render_markdown,
        resolve_path,
        repo_rel,
        run_debug_lab,
        split_values,
        validate_target,
        validate_validation_script,
    )
    from tools.validation.report_utils import write_json_report, write_text_report  # type: ignore

DEFAULT_OUTPUT = "output/validation/heap_code_execution_tool.json"
DEFAULT_MARKDOWN = "output/validation/heap_code_execution_tool.md"
DEFAULT_REQUEST = "output/validation/heap_code_execution_tool_debug_lab_request.json"


def validation_commands(
    target_files: list[str], validation_scripts: list[str], validation_args: list[str]
) -> list[str]:
    commands: list[str] = []
    if target_files:
        commands.append("python -m py_compile " + " ".join(target_files))
    commands.extend(
        f"python {script} {' '.join(validation_args)}".strip()
        for script in validation_scripts
    )
    commands.append("git diff --check")
    return commands


def build_report(args: argparse.Namespace) -> dict[str, Any]:
    repo_root = Path(args.repo_root).resolve()
    errors: list[str] = []
    target_files: list[str] = []
    for raw in split_values(args.target_file):
        rel, error = validate_target(repo_root, raw)
        if error:
            errors.append(f"{raw}: {error}")
        elif rel not in target_files:
            target_files.append(rel)
    validation_scripts: list[str] = []
    for raw in split_values(args.validation_script):
        rel, error = validate_validation_script(repo_root, raw)
        if error:
            errors.append(f"{raw}: {error}")
        elif rel not in validation_scripts:
            validation_scripts.append(rel)
    if not target_files:
        errors.append("at least one --target-file is required")

    validation_args = split_values(args.validation_arg)
    output = resolve_path(repo_root, args.output)
    markdown = resolve_path(repo_root, args.markdown_output)
    request_path = resolve_path(repo_root, args.request_output)
    default_debug_report, default_debug_markdown = default_debug_lab_paths(
        repo_root, output
    )
    debug_report = (
        resolve_path(repo_root, args.debug_lab_output)
        if args.debug_lab_output
        else default_debug_report
    )
    debug_markdown = (
        resolve_path(repo_root, args.debug_lab_markdown_output)
        if args.debug_lab_markdown_output
        else default_debug_markdown
    )
    request = build_debug_lab_request(target_files, validation_scripts, validation_args)
    request_path.parent.mkdir(parents=True, exist_ok=True)
    request_path.write_text(
        json.dumps(request, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    debug_lab_returncode: int | None = None
    debug_stdout = ""
    debug_stderr = ""
    if not errors and not args.no_execute:
        debug_lab_returncode, debug_stdout, debug_stderr = run_debug_lab(
            repo_root,
            request_path,
            debug_report,
            debug_markdown,
            max(1, int(args.timeout_seconds)),
            max(512, int(args.tail_chars)),
        )
    debug_data = read_json(debug_report)
    debug_passed = True if args.no_execute else debug_data.get("passed") is True
    if debug_lab_returncode not in (None, 0):
        errors.append(f"debug lab returned {debug_lab_returncode}")
    if debug_data.get("errors"):
        errors.extend(str(item) for item in debug_data.get("errors", []))

    commands = validation_commands(target_files, validation_scripts, validation_args)
    diffs = [
        git_diff_excerpt(repo_root, target, max(100, int(args.max_diff_chars)))
        for target in target_files
    ]
    return {
        "schema_version": 1,
        "kind": "heap_code_execution_tool",
        "generated_at": now_iso(),
        "repo_root": str(repo_root),
        "passed": not errors and debug_passed,
        "errors": errors,
        "warnings": [],
        "target_count": len(target_files),
        "validation_script_count": len(validation_scripts),
        "request_file": repo_rel(repo_root, request_path),
        "debug_lab_report": repo_rel(repo_root, debug_report),
        "debug_lab_markdown": repo_rel(repo_root, debug_markdown),
        "debug_lab_returncode": debug_lab_returncode,
        "debug_lab_passed": debug_passed,
        "debug_lab_stdout_tail": debug_stdout,
        "debug_lab_stderr_tail": debug_stderr,
        "concrete_code_proposal_count": len(target_files),
        "concrete_code_proposals": proposal_items(target_files, diffs, commands),
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "git_write_performed": False,
        "guardrails": {
            "free_shell_exposed": False,
            "allowlist_enforced": True,
            "provider_execution_performed": False,
            "patch_application_performed": False,
            "source_writes_performed": False,
            "git_write_performed": False,
            "debug_lab_required": True,
        },
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--target-file", action="append", default=[])
    parser.add_argument("--validation-script", action="append", default=[])
    parser.add_argument("--validation-arg", action="append", default=[])
    parser.add_argument("--request-output", default=DEFAULT_REQUEST)
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    parser.add_argument("--markdown-output", default=DEFAULT_MARKDOWN)
    parser.add_argument("--debug-lab-output", default="")
    parser.add_argument("--debug-lab-markdown-output", default="")
    parser.add_argument("--timeout-seconds", type=int, default=300)
    parser.add_argument("--tail-chars", type=int, default=4000)
    parser.add_argument("--max-diff-chars", type=int, default=3500)
    parser.add_argument("--no-execute", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    report = build_report(args)
    output = resolve_path(repo_root, args.output)
    markdown = resolve_path(repo_root, args.markdown_output)
    write_json_report(report, output)
    write_text_report(render_markdown(report), markdown)
    print(
        json.dumps(
            {"passed": report["passed"], "output": str(output), "markdown": str(markdown)},
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
