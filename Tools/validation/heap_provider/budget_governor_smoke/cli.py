#!/usr/bin/env python3
"""Smoke-test the heap provider budget governor contract."""

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
    from Tools.validation._shared.report_utils import resolve_output_path, write_json_report, write_text_report
except ImportError:  # pragma: no cover
    from Tools.validation._shared.report_utils import (  # type: ignore
        resolve_output_path,
        write_json_report,
        write_text_report,
    )


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def validate(report: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if report.get("kind") != "heap_provider_budget_governor":
        errors.append("unexpected report kind")
    if report.get("passed") is not True:
        errors.append("governor did not pass")
    if report.get("permit_allowed") is not False:
        errors.append("provider permit must be denied by default")
    for key in (
        "provider_execution_performed",
        "patch_application_performed",
        "source_writes_performed",
    ):
        if report.get(key) is not False:
            errors.append(f"guardrail {key} must be false")
    loop_budget = report.get("loop_budget") if isinstance(report.get("loop_budget"), dict) else {}
    if int(loop_budget.get("max_iterations") or 0) != 2:
        errors.append("requested max iterations must be clamped to 2")
    lanes = report.get("provider_lanes") if isinstance(report.get("provider_lanes"), dict) else {}
    for lane in ("gpu1_planner", "gpu0_peer", "npu_critic", "broker"):
        if lane not in lanes:
            errors.append(f"missing provider lane: {lane}")
    if any(isinstance(lane, dict) and lane.get("generation_allowed") for lane in lanes.values()):
        errors.append("no lane may allow generation by default")
    return errors


def render_markdown(report: dict[str, Any]) -> str:
    lines = ["# Heap Provider Budget Governor Smoke", "", f"- Passed: `{report.get('passed')}`"]
    inner = report.get("inner_report") if isinstance(report.get("inner_report"), dict) else {}
    lines.append(f"- Inner decision: `{inner.get('decision')}`")
    lines.append(f"- Permit allowed: `{inner.get('permit_allowed')}`")
    if report.get("errors"):
        lines.extend(["", "## Errors", ""])
        lines.extend(f"- {item}" for item in report.get("errors", []))
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument(
        "--output", default="output/validation/heap_provider_budget_governor_smoke.json"
    )
    parser.add_argument(
        "--markdown-output", default="output/validation/heap_provider_budget_governor_smoke.md"
    )
    parser.add_argument("--timeout-seconds", type=int, default=120)
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    inner_output = (
        repo_root
        / "output"
        / "validation"
        / f"heap_provider_budget_governor_smoke_inner_{stamp}.json"
    )
    inner_md = (
        repo_root
        / "output"
        / "validation"
        / f"heap_provider_budget_governor_smoke_inner_{stamp}.md"
    )
    env = os.environ.copy()
    env["PYTHONPATH"] = str(repo_root) + (
        os.pathsep + env["PYTHONPATH"] if env.get("PYTHONPATH") else ""
    )
    completed = subprocess.run(
        [
            sys.executable,
            "Tools/ai/heap_provider/budget_governor/cli.py",
            "--repo-root",
            ".",
            "--budget-minutes",
            "3",
            "--max-rounds",
            "8",
            "--requested-max-iterations",
            "2",
            "--output",
            inner_output.relative_to(repo_root).as_posix(),
            "--markdown-output",
            inner_md.relative_to(repo_root).as_posix(),
        ],
        cwd=repo_root,
        env=env,
        capture_output=True,
        text=True,
        check=False,
        timeout=args.timeout_seconds,
    )
    inner = read_json(inner_output)
    errors = []
    if completed.returncode != 0:
        errors.append(
            f"governor returned {completed.returncode}: {(completed.stderr or completed.stdout)[-1200:]}"
        )
    errors.extend(validate(inner))
    report = {
        "schema_version": 1,
        "kind": "heap_provider_budget_governor_smoke",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "passed": not errors,
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
