#!/usr/bin/env python3
"""Validate workflow PowerShell scripts do not invoke bare/system Python.

The IA-Carmine workflow Python policy requires official/provider-capable lanes
to use the repository-owned interpreter resolved by Tools/workflow/python_env.ps1.
System PATH Python, WindowsApps Python and permissive fallback to bare `python`
are forbidden in workflow lanes.
"""

from __future__ import annotations

import argparse
import json
import re
from collections.abc import Iterable
from dataclasses import asdict, dataclass
from pathlib import Path

BARE_PYTHON_PATTERNS = (
    re.compile(r"^\s*(?:&\s*)?python(?:\.exe)?(?:\s|$)", re.IGNORECASE),
    re.compile(r"[;|{]\s*(?:&\s*)?python(?:\.exe)?(?:\s|$)", re.IGNORECASE),
)
FORBIDDEN_FALLBACK_PATTERNS = (
    re.compile(r"Get-Command\s+python\b", re.IGNORECASE),
    re.compile(r"\{\s*[\"']python(?:\.exe)?[\"']\s*\}", re.IGNORECASE),
    re.compile(r"=\s*[\"']python(?:\.exe)?[\"']\s*$", re.IGNORECASE),
)
NON_COMMAND_PATTERNS = (
    re.compile(r"^\s*python(?:\.exe)?\s*=", re.IGNORECASE),
    re.compile(r"^\s*[\"']python(?:\.exe)?[\"']\s*[=:]", re.IGNORECASE),
)
ALLOWED_BARE_PATHS = set()


@dataclass
class Violation:
    path: str
    line: int
    text: str
    reason: str


def repo_relative(repo_root: Path, path: Path) -> str:
    return path.resolve().relative_to(repo_root.resolve()).as_posix()


def iter_powershell_files(repo_root: Path, roots: Iterable[str]) -> Iterable[Path]:
    for root in roots:
        root_path = (repo_root / root).resolve()
        if not root_path.exists():
            continue
        if root_path.is_file() and root_path.suffix.lower() == ".ps1":
            yield root_path
            continue
        for path in root_path.rglob("*.ps1"):
            if path.is_file():
                yield path


def strip_line(line: str) -> str:
    if line.lstrip().startswith("#"):
        return ""
    return line.rstrip("\r\n")


def is_non_command_python_reference(line: str) -> bool:
    stripped = line.strip()
    if re.search(r"\[string\]\s*\$Label\s*=\s*[\"']python[\"']", stripped, re.IGNORECASE):
        return True
    if 'py = "python"; ps1 = "python"; scripts = "python"; script = "python"' in stripped:
        return True
    return any(pattern.search(line) for pattern in NON_COMMAND_PATTERNS)


def scan_file(repo_root: Path, path: Path) -> list[Violation]:
    rel = repo_relative(repo_root, path)
    if rel in ALLOWED_BARE_PATHS:
        return []
    violations: list[Violation] = []
    try:
        lines = path.read_text(encoding="utf-8-sig").splitlines()
    except UnicodeDecodeError:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    for index, raw_line in enumerate(lines, start=1):
        line = strip_line(raw_line)
        if not line.strip():
            continue
        if is_non_command_python_reference(line):
            continue
        for pattern in FORBIDDEN_FALLBACK_PATTERNS:
            if pattern.search(line):
                violations.append(
                    Violation(
                        path=rel,
                        line=index,
                        text=raw_line.strip(),
                        reason="system/PATH Python fallback is forbidden; use repository-owned IA_CARMINE_PYTHON",
                    )
                )
                break
        if violations and violations[-1].path == rel and violations[-1].line == index:
            continue
        for pattern in BARE_PYTHON_PATTERNS:
            if pattern.search(line):
                violations.append(
                    Violation(
                        path=rel,
                        line=index,
                        text=raw_line.strip(),
                        reason="bare python invocation; use resolved workflow Python variable or helper",
                    )
                )
                break
    return violations


def build_report(repo_root: Path, roots: list[str]) -> dict:
    checked_files = sorted(set(iter_powershell_files(repo_root, roots)))
    violations: list[Violation] = []
    for path in checked_files:
        violations.extend(scan_file(repo_root, path))
    return {
        "schema_version": 1,
        "kind": "workflow_python_invocation_policy",
        "repo_root": str(repo_root),
        "roots": roots,
        "checked_file_count": len(checked_files),
        "violation_count": len(violations),
        "passed": len(violations) == 0,
        "policy": {
            "required_interpreter_source": "repository-owned IA_CARMINE_PYTHON from Tools/workflow/python_env.ps1",
            "forbidden": [
                "bare python invocation",
                "bare python.exe invocation",
                "Get-Command python fallback",
                "fallback literal 'python' / 'python.exe'",
                "WindowsApps Python",
                "system PATH Python",
            ],
            "allowed_examples": [
                "$ProviderPythonExe",
                "$PipelinePythonExe",
                "$PacketPythonExe",
                "$WorkflowPythonExe",
                "Use-WorkflowPython",
                "Invoke-WorkflowPython",
            ],
        },
        "violations": [asdict(item) for item in violations],
        "errors": [] if not violations else ["workflow Python policy violations found"],
        "warnings": [],
    }


def write_markdown(report: dict, output: Path) -> None:
    lines = [
        "# Workflow Python invocation policy",
        "",
        f"- Passed: `{report['passed']}`",
        f"- Checked files: `{report['checked_file_count']}`",
        f"- Violations: `{report['violation_count']}`",
        "",
        "## Policy",
        "",
        "Workflow PowerShell scripts must use the repository-owned IA-Carmine Python interpreter, not system PATH Python.",
        "",
    ]
    if report["violations"]:
        lines += ["## Violations", "", "| File | Line | Reason | Text |", "|---|---:|---|---|"]
        for item in report["violations"]:
            text = str(item["text"]).replace("|", "\\|")
            lines.append(f"| `{item['path']}` | {item['line']} | {item['reason']} | `{text}` |")
    else:
        lines += ["## Violations", "", "None."]
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--root", action="append", default=None)
    parser.add_argument(
        "--output", default="output/validation/workflow_python_invocation_policy.json"
    )
    parser.add_argument("--markdown-output", default="")
    args = parser.parse_args()
    repo_root = Path(args.repo_root).resolve()
    roots = args.root or ["Tools/workflow"]
    report = build_report(repo_root, roots)
    output = repo_root / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    if args.markdown_output:
        write_markdown(report, repo_root / args.markdown_output)
    print(
        json.dumps(
            {
                "passed": report["passed"],
                "output": str(output),
                "violation_count": report["violation_count"],
            },
            indent=2,
        )
    )
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
