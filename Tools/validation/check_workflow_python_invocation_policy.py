#!/usr/bin/env python3
"""Validate workflow PowerShell scripts do not invoke bare python.

The IA-Carmine workflow Python policy requires provider-capable lanes to use the
resolved interpreter from Tools/workflow/python_env.ps1, IA_CARMINE_PYTHON or the
repository .venv. PowerShell workflow scripts should therefore call a resolved
variable such as $RepoPythonExe, $ProviderPythonExe, $PipelinePythonExe or an
explicit function such as Invoke-RepoPython instead of relying on PATH lookup for
`python` / `python.exe`.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

BARE_PYTHON_PATTERNS = (
    re.compile(r"^\s*(?:&\s*)?python(?:\.exe)?(?:\s|$)", re.IGNORECASE),
    re.compile(r"[;|{]\s*(?:&\s*)?python(?:\.exe)?(?:\s|$)", re.IGNORECASE),
)

ALLOWED_BARE_PATHS = {
    "Tools/workflow/python_env.ps1",
}


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
            "required_interpreter_source": "Tools/workflow/python_env.ps1 / IA_CARMINE_PYTHON / repository .venv",
            "forbidden": ["bare python invocation", "bare python.exe invocation"],
            "allowed_examples": [
                "$RepoPythonExe",
                "$ProviderPythonExe",
                "$PipelinePythonExe",
                "Invoke-RepoPython",
                "Use-WorkflowPython",
            ],
        },
        "violations": [asdict(item) for item in violations],
        "errors": [] if not violations else ["bare workflow Python invocations found"],
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
        "Workflow PowerShell scripts must use the resolved IA-Carmine Python interpreter, not bare `python` or `python.exe` PATH lookup.",
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
    parser.add_argument(
        "--root",
        action="append",
        default=None,
        help="Root path or file to scan. Defaults to Tools/workflow.",
    )
    parser.add_argument("--output", default="output/validation/workflow_python_invocation_policy.json")
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

    print(json.dumps({"passed": report["passed"], "output": str(output), "violation_count": report["violation_count"]}, indent=2))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
