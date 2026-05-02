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
from dataclasses import dataclass
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


@dataclass(slots=True)
class FenceState:
    """State for one Markdown fenced code block while scanning."""

    open: bool = False
    start_line: int = 0
    lang: str = ""
    body_lines: list[str] | None = None


def iter_default_paths(repo_root: Path) -> list[Path]:
    """Return default Markdown files that exist in the repository."""
    return [repo_root / rel for rel in DEFAULT_PATHS if (repo_root / rel).is_file()]


def resolve_input_paths(repo_root: Path, values: list[str]) -> list[Path]:
    """Resolve CLI paths or fall back to default Markdown targets."""
    if not values:
        return iter_default_paths(repo_root)
    return [(repo_root / value).resolve() if not Path(value).is_absolute() else Path(value).resolve() for value in values]


def rel_path(repo_root: Path, path: Path) -> str:
    """Return a repository-relative display path when possible."""
    try:
        return path.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        return path.resolve().as_posix()


def control_locations(text: str) -> list[dict[str, Any]]:
    """Return locations of disallowed ASCII control characters."""
    locations: list[dict[str, Any]] = []
    line = 1
    col = 0
    for index, char in enumerate(text):
        if char == "\n":
            line += 1
            col = 0
            continue
        col += 1
        code = ord(char)
        if code < 32 and code not in ALLOWED_CONTROL_CODES:
            locations.append({"index": index, "line": line, "column": col, "codepoint": code})
    return locations


def fence_scan(text: str) -> tuple[list[dict[str, Any]], list[str], list[dict[str, Any]]]:
    """Scan fenced blocks and return fence metadata, warnings and command findings."""
    fences: list[dict[str, Any]] = []
    warnings: list[str] = []
    command_findings: list[dict[str, Any]] = []
    state = FenceState(body_lines=[])

    for line_number, line in enumerate(text.splitlines(), start=1):
        match = FENCE_RE.match(line)
        if not match:
            if state.open and state.body_lines is not None:
                state.body_lines.append(line)
            continue
        if not state.open:
            state = FenceState(True, line_number, (match.group("lang") or "").lower(), [])
            fences.append({"start_line": line_number, "lang": state.lang})
            continue
        fences[-1]["end_line"] = line_number
        command_findings.extend(command_fence_findings(state, line_number))
        state = FenceState(body_lines=[])

    if state.open:
        warnings.append(f"unclosed fenced code block starting at line {state.start_line} ({state.lang or 'no language'})")
    return fences, warnings, command_findings


def command_fence_findings(state: FenceState, end_line: int) -> list[dict[str, Any]]:
    """Return suspicious command-fence findings for one closed fence."""
    if state.lang not in COMMAND_FENCE_LANGS:
        return []
    body = "\n".join(state.body_lines or [])
    suspicious = SUSPICIOUS_PATH_RE.findall(body)
    if not suspicious:
        return []
    return [
        {
            "start_line": state.start_line,
            "end_line": end_line,
            "lang": state.lang,
            "issue": "control_character_inside_path_like_command",
            "match_count": len(suspicious),
        }
    ]


def errors_from_controls(controls: list[dict[str, Any]]) -> list[str]:
    """Format control-character findings as report errors."""
    errors = [
        f"control character U+{item['codepoint']:04X} at line {item['line']}, column {item['column']}"
        for item in controls[:20]
    ]
    if len(controls) > 20:
        errors.append(f"additional control characters omitted from report: {len(controls) - 20}")
    return errors


def errors_from_command_findings(findings: list[dict[str, Any]]) -> list[str]:
    """Format command-fence findings as report errors."""
    return [
        "suspicious command fence path/control sequence "
        f"at lines {item['start_line']}-{item['end_line']} ({item['lang']})"
        for item in findings
    ]


def check_file(repo_root: Path, path: Path) -> dict[str, Any]:
    """Check one Markdown file for hygiene issues."""
    rel = rel_path(repo_root, path)
    try:
        text = path.read_text(encoding="utf-8-sig")
    except OSError as exc:
        return failed_file_check(rel, path.exists(), f"{type(exc).__name__}: {exc}")

    controls = control_locations(text)
    fences, warnings, command_findings = fence_scan(text)
    errors = errors_from_controls(controls) + errors_from_command_findings(command_findings)
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


def failed_file_check(rel: str, exists: bool, error: str) -> dict[str, Any]:
    """Return a standardized failed check for unreadable files."""
    return {
        "path": rel,
        "exists": exists,
        "ok": False,
        "errors": [error],
        "warnings": [],
        "control_character_count": 0,
        "command_fence_issue_count": 0,
        "fence_count": 0,
    }


def flatten_check_messages(checks: list[dict[str, Any]], field: str) -> list[str]:
    """Flatten per-file errors or warnings into top-level report messages."""
    return [f"{check['path']}: {message}" for check in checks for message in check.get(field, [])]


def build_report(repo_root: Path, paths: list[Path]) -> dict[str, Any]:
    """Build the full markdown_command_hygiene report."""
    checks = [check_file(repo_root, path) for path in paths]
    errors = flatten_check_messages(checks, "errors")
    warnings = flatten_check_messages(checks, "warnings")
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
    report = build_report(repo_root, resolve_input_paths(repo_root, args.path))
    output = resolve_output_path(repo_root, args.output) if args.output else None
    print(write_json_report(report, output), end="")
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
