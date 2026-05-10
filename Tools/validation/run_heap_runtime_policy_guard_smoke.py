#!/usr/bin/env python3
"""Guard heap-runtime provider policy regressions.

This smoke is intentionally static and narrow: it protects the runtime universe
entry points from regressions that previously broke the heap/provider path.
It must distinguish forbidden runtime tokens from legitimate report field names
such as provider_results/provider_result_count.
"""
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    from report_utils import resolve_output_path, write_json_report, write_text_report
except ImportError:  # pragma: no cover
    from Tools.validation.report_utils import resolve_output_path, write_json_report, write_text_report  # type: ignore

POLICY_FILES = (
    "Tools/ai/run_heap_runtime_completeness_gate.py",
    "Tools/validation/run_heap_runtime_completeness_gate_smoke.py",
)

FORBIDDEN_LITERAL_PATTERNS = (
    ("banned_model_literal", re.compile(r"(?P<quote>[\"'])gpt-oss:20b(?P=quote)"), "gpt-oss:20b is banned from heap runtime/provider gate defaults"),
    ("duplicate_provider_python_resolver", re.compile(r"\bdef\s+provider_python_exe\s*\("), "provider subprocesses must use Tools.ai.provider_mesh_runtime.python_runtime"),
    ("duplicate_provider_python_resolver_call", re.compile(r"\bprovider_python_exe\s*\("), "provider subprocesses must call resolve_child_python, not a local resolver"),
    ("system_python_subprocess", re.compile(r"\bsys\.executable\b"), "heap provider subprocesses must not use the current/system interpreter"),
    ("unsupported_provider_request_event", re.compile(r"(?P<quote>[\"'])provider_request(?P=quote)"), "provider_request is not a supported provider_runtime_heap event type"),
    ("unsupported_provider_result_event", re.compile(r"(?P<quote>[\"'])provider_result(?P=quote)"), "provider_result is not a supported provider_runtime_heap event type; use telemetry_signal for provider reports"),
    ("unsupported_arbiter_lane", re.compile(r"target\s*=\s*[\"']arbiter[\"']"), "arbiter is not a provider_runtime_heap lane"),
)


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def repo_rel(repo_root: Path, path: Path) -> str:
    return path.resolve().relative_to(repo_root.resolve()).as_posix()


def scan_file(repo_root: Path, rel_path: str) -> tuple[list[dict[str, Any]], list[str]]:
    path = repo_root / rel_path
    violations: list[dict[str, Any]] = []
    warnings: list[str] = []
    if not path.exists():
        violations.append({
            "path": rel_path,
            "line": 0,
            "policy": "required_file_missing",
            "reason": "required heap runtime policy file is missing",
            "text": "",
        })
        return violations, warnings

    text = read_text(path)
    lines = text.splitlines()
    for line_no, line in enumerate(lines, start=1):
        for policy, pattern, reason in FORBIDDEN_LITERAL_PATTERNS:
            if pattern.search(line):
                violations.append({
                    "path": rel_path,
                    "line": line_no,
                    "policy": policy,
                    "reason": reason,
                    "text": line.strip(),
                })

    if "subprocess.run" in text:
        if "resolve_child_python" not in text:
            violations.append({
                "path": rel_path,
                "line": 0,
                "policy": "canonical_python_resolver_missing",
                "reason": "subprocess-running heap runtime files must import/use resolve_child_python",
                "text": "",
            })
        if "command_env" not in text:
            violations.append({
                "path": rel_path,
                "line": 0,
                "policy": "canonical_python_env_missing",
                "reason": "subprocess-running heap runtime files must pass command_env(repo_root) into child processes",
                "text": "",
            })

    return violations, warnings


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Heap Runtime Policy Guard Smoke",
        "",
        f"- Passed: `{report.get('passed')}`",
        f"- Checked files: `{report.get('checked_file_count')}`",
        f"- Violation count: `{report.get('violation_count')}`",
        "",
        "## Policy",
        "",
        "- Heap/provider subprocesses must use `resolve_child_python()` plus `command_env()`.",
        "- `gpt-oss:20b` is forbidden in heap runtime/provider gate defaults.",
        "- Unsupported heap event literals `provider_request` / `provider_result` are forbidden.",
        "- `target=\"arbiter\"` is forbidden because `arbiter` is not a physical heap lane.",
        "",
    ]
    if report.get("violations"):
        lines.extend(["## Violations", "", "| File | Line | Policy | Reason | Text |", "|---|---:|---|---|---|"])
        for item in report["violations"]:
            text = str(item.get("text") or "").replace("|", "\\|")
            lines.append(f"| `{item.get('path')}` | {item.get('line')} | `{item.get('policy')}` | {item.get('reason')} | `{text}` |")
    else:
        lines.extend(["## Violations", "", "None."])
    return "\n".join(lines) + "\n"


def build_report(repo_root: Path) -> dict[str, Any]:
    violations: list[dict[str, Any]] = []
    warnings: list[str] = []
    for rel_path in POLICY_FILES:
        file_violations, file_warnings = scan_file(repo_root, rel_path)
        violations.extend(file_violations)
        warnings.extend(file_warnings)
    return {
        "schema_version": 1,
        "kind": "heap_runtime_policy_guard_smoke",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "repo_root": repo_root.as_posix(),
        "checked_files": list(POLICY_FILES),
        "checked_file_count": len(POLICY_FILES),
        "violation_count": len(violations),
        "violations": violations,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "passed": not violations,
        "errors": [] if not violations else ["heap runtime policy guard violations found"],
        "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output", default="output/validation/heap_runtime_policy_guard_smoke.json")
    parser.add_argument("--markdown-output", default="output/validation/heap_runtime_policy_guard_smoke.md")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    report = build_report(repo_root)
    output = resolve_output_path(repo_root, args.output)
    markdown_output = resolve_output_path(repo_root, args.markdown_output)
    write_json_report(report, output)
    write_text_report(render_markdown(report), markdown_output)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
