#!/usr/bin/env python3
"""Validate Markdown command blocks for copy/paste hygiene.

This validator is intentionally lightweight and report-only. It detects common
Markdown documentation hazards that can break local PowerShell copy/paste runs:
control characters, unbalanced fenced code blocks and suspicious control-like
escapes inside command fences.

It does not execute commands, invoke providers, run Blender, apply patches or
rewrite Markdown files.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Any

try:
    from report_utils import resolve_output_path, write_json_report
except ImportError:
    from Tools.validation.report_utils import resolve_output_path, write_json_report  # type: ignore


REPORT_KIND = "markdown_command_hygiene"
COMMAND_FENCE_LANGS = {"powershell", "pwsh", "bash", "sh", "shell", "cmd", "text"}
ALLOWED_CONTROL_CODES = {9, 10, 13}
DEFAULT_PATHS = (
    "README.md",
    "AGENTS.md",
    "WORKFLOW.md",
    "docs/README.md",
    "docs/LOCAL_AI_CORE_TOOL_ACTIVATION.md",
    "docs/CONTRACT_DRIFT_VALIDATION.md",
    "docs/AGENT_REVIEW_CODE_PATCH_PLAN.md",
    "docs/LOCAL_AI_TASKS/design-agent-review-code-patch-plan.md",
    "docs/LOCAL_AI_TASKS/macro-local-validation-prototype-gate.md",
)

FENCE_RE = re.compile(r"^\s*```(?P<lang>[^`\s]*)")
SUSPICIOUS_PATH_RE = re.compile(r"(?:Tools|output|docs|indexAI|Scripting)[\x00-\x08\x0b\x0c\x0e-\x1f]+", re.IGNORECASE)


def iter_default_paths(repo_root: Path) -> list[Path]:
    paths: list[Path] = []
    for rel in DEFAULT_PATHS:
        path = repo_root / rel
        if path.is_file():
            paths.append(path)
    return paths


def rel_path(repo_root: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        return path.resolve().as_posix()


def control_locations(text: str) -> list[dict[str, Any]]:
    locations: list[dict[str, Any]] = []
    line = 1
    col = 0
    for index, char in enumerate(text):
        code = ord(char)
        if char == "\n":
            line += 1
            col = 0
            continue
        col += 1
        if code < 32 and code not in ALLOWED_CONTROL_CODES:
            locations.append({"index": index, "line": line, "column": col, "codepoint": code})
    return locations


def fence_issues(text: str) -> tuple[list[dict[str, Any]], list[str]]:
    fences: list[dict[str, Any]] = []
    warnings: list[str] = []
    in_fence = False
    fence_start = 0
    fence_lang = ""
    for line_number, line in enumerate(text.splitlines(), start=1):
        match = FENCE_RE.match(line)
        if not match:
            continue
        if not in_fence:
            in_fence = True
            fence_start = line_number
            fence_lang = (match.group("lang") or "").lower()
            fences.append({"start_line": line_number, "lang": fence_lang})
        else:
            fences[-1]["end_line"] = line_number
            in_fence = False
            fence_lang = ""
    if in_fence:
        warnings.append(f"unclosed fenced code block starting at line {fence_start} ({fence_lang or 'no language'})")
    return fences, warnings


def command_fence_findings(text: str) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    in_fence = False
    fence_lang = ""
    start_line = 0
    body_lines: list[str] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        match = FENCE_RE.match(line)
        if match and not in_fence:
            in_fence = True
            fence_lang = (match.group("lang") or "").lower()
            start_line = line_number
            body_lines = []
            continue
        if match and in_fence:
            if fence_lang in COMMAND_FENCE_LANGS:
                body = "\n".join(body_lines)
                suspicious = SUSPICIOUS_PATH_RE.findall(body)
                if suspicious:
                    findings.append(
                        {
                            "start_line": start_line,
                            "end_line": line_number,
                            "lang": fence_lang,
                            "issue": "control_character_inside_path_like_command",
                            "match_count": len(suspicious),
                        }
                    )
            in_fence = False
            fence_lang = ""
            body_lines = []
            continue
        if in_fence:
            body_lines.append(line)
    return findings


def check_file(repo_root: Path, path: Path) -> dict[str, Any]:
    rel = rel_path(repo_root, path)
    errors: list[str] = []
    warnings: list[str] = []
    controls: list[dict[str, Any]] = []
    command_findings: list[dict[str, Any]] = []
    fences: list[dict[str, Any]] = []

    try:
        text = path.read_text(encoding="utf-8-sig")
    except OSError as exc:
        return {
            "path": rel,
            "exists": path.exists(),
            "ok": False,
            "errors": [f"{type(exc).__name__}: {exc}"],
            "warnings": [],
            "control_character_count": 0,
            "command_fence_issue_count": 0,
            "fence_count": 0,
        }

    controls = control_locations(text)
    fences, fence_warnings = fence_issues(text)
    command_findings = command_fence_findings(text)
    warnings.extend(fence_warnings)

    if controls:
        for item in controls[:20]:
            errors.append(
                f"control character U+{item['codepoint']:04X} at line {item['line']}, column {item['column']}"
            )
        if len(controls) > 20:
            errors.append(f"additional control characters omitted from report: {len(controls) - 20}")
    if command_findings:
        for item in command_findings:
            errors.append(
                "suspicious command fence path/control sequence "
                f"at lines {item['start_line']}-{item['end_line']} ({item['lang']})"
            )

    return {
        "path": rel,
        "exists": True,
        "ok": not errors,
        "errors": errors,
        "warnings": warnings,
        "control_character_count": len(controls),
        "command_fence_issue_count": len(command_findings),
        "fence_count": len(fences),
        "command_fence_findings": command_findings,
    }


def build_report(repo_root: Path, paths: list[Path]) -> dict[str, Any]:
    checks = [check_file(repo_root, path) for path in paths]
    errors = [f"{check['path']}: {error}" for check in checks for error in check.get("errors", [])]
    warnings = [f"{check['path']}: {warning}" for check in checks for warning in check.get("warnings", [])]
    return {
        "schema_version": 1,
        "kind": REPORT_KIND,
        "repo_root": str(repo_root),
        "passed": not errors,
        "errors": errors,
        "warnings": warnings,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "checked_count": len(checks),
        "failed_count": sum(1 for check in checks if not check.get("ok")),
        "checks": checks,
        "guardrails": {
            "report_only": True,
            "commands_executed": False,
            "blender_runtime_touched": False,
            "provider_execution_performed": False,
            "patch_application_performed": False,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--path", action="append", default=[], help="Markdown file to check; may be repeated.")
    parser.add_argument("--output", help="Optional JSON report path.")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    if args.path:
        paths = [(repo_root / value).resolve() if not Path(value).is_absolute() else Path(value).resolve() for value in args.path]
    else:
        paths = iter_default_paths(repo_root)

    report = build_report(repo_root, paths)
    output = resolve_output_path(repo_root, args.output) if args.output else None
    text = write_json_report(report, output)
    print(text, end="")
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
