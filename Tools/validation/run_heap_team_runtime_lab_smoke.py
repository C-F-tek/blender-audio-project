#!/usr/bin/env python3
"""Smoke-test the deterministic heap/team runtime lab."""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    from report_utils import resolve_output_path, write_json_report, write_text_report
except ImportError:  # pragma: no cover
    from Tools.validation.report_utils import resolve_output_path, write_json_report, write_text_report  # type: ignore


def now_stamp() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    return data if isinstance(data, dict) else {}


def run_lab(repo_root: Path, stamp: str, timeout_seconds: int) -> tuple[subprocess.CompletedProcess[str], dict[str, Any]]:
    output = repo_root / "output" / "validation" / f"heap_team_runtime_lab_smoke_inner_{stamp}.json"
    markdown = repo_root / "output" / "validation" / f"heap_team_runtime_lab_smoke_inner_{stamp}.md"
    env = os.environ.copy()
    env["PYTHONPATH"] = str(repo_root) + (os.pathsep + env["PYTHONPATH"] if env.get("PYTHONPATH") else "")
    command = [
        sys.executable,
        "Tools/ai/run_heap_team_runtime_lab.py",
        "--repo-root", ".",
        "--stamp", stamp,
        "--max-iterations", "4",
        "--budget-minutes", "5",
        "--max-rounds", "3",
        "--timeout-seconds", str(timeout_seconds),
        "--output", output.relative_to(repo_root).as_posix(),
        "--markdown-output", markdown.relative_to(repo_root).as_posix(),
    ]
    completed = subprocess.run(command, cwd=repo_root, env=env, capture_output=True, text=True, check=False, timeout=timeout_seconds + 60)
    return completed, read_json(output)


def validate_lab(report: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if report.get("passed") is not True:
        errors.append("inner heap team lab did not pass")
    metrics = report.get("metrics") if isinstance(report.get("metrics"), dict) else {}
    required_positive = (
        "heap_read_count",
        "heap_write_count",
        "tool_request_count",
        "tool_execution_count",
        "decision_count",
        "candidate_operation_count",
    )
    for key in required_positive:
        if int(metrics.get(key) or 0) <= 0:
            errors.append(f"metric {key} must be >0")
    if metrics.get("product_status") not in {"ready", "blocked_with_reason"}:
        errors.append("product_status must be ready or blocked_with_reason")
    if metrics.get("budget_decision") != "deny_provider_generation":
        errors.append("budget_decision must deny provider generation by default")
    if int(metrics.get("budget_max_iterations") or 0) <= 0:
        errors.append("budget_max_iterations must be >0")
    state = report.get("state") if isinstance(report.get("state"), dict) else {}
    if not isinstance(state.get("budget_governor"), dict) or not state.get("budget_governor"):
        errors.append("state.budget_governor must be present")
    for key in ("facts", "needs", "tool_requests", "claims", "decisions", "candidate_operations"):
        value = state.get(key)
        if not isinstance(value, list) or not value:
            errors.append(f"state.{key} must contain at least one item")
    guardrails = report.get("guardrails") if isinstance(report.get("guardrails"), dict) else {}
    for key in ("provider_execution_performed", "patch_application_performed", "source_writes_performed"):
        if report.get(key) is not False or guardrails.get(key) is not False:
            errors.append(f"guardrail {key} must be false")
    return errors


def render_markdown(report: dict[str, Any]) -> str:
    lines = ["# Heap Team Runtime Lab Smoke", "", f"- Passed: `{report.get('passed')}`"]
    inner = report.get("inner_report") if isinstance(report.get("inner_report"), dict) else {}
    metrics = inner.get("metrics") if isinstance(inner.get("metrics"), dict) else {}
    lines.extend(["", "## Metrics", ""])
    for key, value in metrics.items():
        lines.append(f"- {key}: `{value}`")
    if report.get("errors"):
        lines.extend(["", "## Errors", ""])
        lines.extend(f"- {error}" for error in report["errors"])
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output", default="output/validation/heap_team_runtime_lab_smoke.json")
    parser.add_argument("--markdown-output", default="output/validation/heap_team_runtime_lab_smoke.md")
    parser.add_argument("--timeout-seconds", type=int, default=180)
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    stamp = f"heap_team_smoke_{now_stamp()}"
    completed, inner = run_lab(repo_root, stamp, args.timeout_seconds)
    errors = []
    if completed.returncode != 0:
        errors.append(f"heap team lab returned {completed.returncode}: {(completed.stderr or completed.stdout)[-1500:]}")
    errors.extend(validate_lab(inner))

    report = {
        "schema_version": 1,
        "kind": "heap_team_runtime_lab_smoke",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "repo_root": repo_root.as_posix(),
        "passed": not errors,
        "inner_returncode": completed.returncode,
        "inner_report": inner,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
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
