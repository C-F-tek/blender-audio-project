#!/usr/bin/env python3
"""Run core runtime guard smokes required by surface launcher/preflight checks."""

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
    from Tools.validation._shared.report_utils import write_json_report, write_text_report
except ImportError:
    repo_root_for_import = Path(__file__).resolve().parents[4]
    if str(repo_root_for_import) not in sys.path:
        sys.path.insert(0, str(repo_root_for_import))
    from Tools.validation._shared.report_utils import (  # type: ignore
        write_json_report,
        write_text_report,
    )


def discover_core_steps(repo_root: Path) -> list[tuple[str, str]]:
    steps: list[tuple[str, str]] = []
    validation_dir = repo_root / "Tools" / "validation"
    for path in sorted(validation_dir.rglob("cli.py")):
        if path.resolve(strict=False) == Path(__file__).resolve(strict=False):
            continue
        try:
            text = path.read_text(encoding="utf-8-sig", errors="replace")
        except OSError:
            continue
        if "CORE_RUNTIME_GUARD = True" not in text:
            continue
        name = path.parent.name.removeprefix("run_").removesuffix("_smoke")
        steps.append((name, path.relative_to(repo_root).as_posix()))
    return steps


def run_step(repo_root: Path, name: str, script: str, output_dir: Path, timeout: int) -> dict[str, Any]:
    output = output_dir / f"{name}.json"
    command = [
        sys.executable,
        script,
        "--repo-root",
        str(repo_root),
        "--output",
        str(output),
    ]
    if name == "patch_candidate_synthesis":
        command.extend(["--timeout-seconds", str(timeout)])
    env = dict(os.environ)
    env["PYTHONPATH"] = str(repo_root)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["IA_CARMINE_ALLOW_INTERNAL_DISPATCH"] = "1"
    env["IA_CARMINE_PYTHON"] = sys.executable
    completed = subprocess.run(
        command,
        cwd=repo_root,
        env=env,
        text=True,
        capture_output=True,
        check=False,
        timeout=max(30, timeout),
    )
    report: dict[str, Any] = {}
    if output.exists():
        try:
            report = json.loads(output.read_text(encoding="utf-8-sig"))
        except Exception as exc:  # noqa: BLE001
            report = {"passed": False, "errors": [f"parse failed: {type(exc).__name__}: {exc}"]}
    return {
        "name": name,
        "script": script,
        "output": output.as_posix(),
        "returncode": completed.returncode,
        "passed": completed.returncode == 0 and report.get("passed") is True,
        "report_kind": report.get("kind"),
        "report_errors": report.get("errors") or [],
        "report_warnings": report.get("warnings") or [],
        "stdout_tail": (completed.stdout or "")[-4000:],
        "stderr_tail": (completed.stderr or "")[-4000:],
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Core Runtime Guard Suite",
        "",
        f"- Passed: `{report.get('passed')}`",
        f"- Generated at: `{report.get('generated_at')}`",
        f"- Step count: `{len(report.get('steps') or [])}`",
        f"- Failed step count: `{len(report.get('failed_steps') or [])}`",
        "",
        "## Steps",
        "",
    ]
    for step in report.get("steps") or []:
        lines.append(
            f"- `{step.get('name')}`: passed=`{step.get('passed')}`, rc=`{step.get('returncode')}`"
        )
    if report.get("errors"):
        lines.extend(["", "## Errors", ""])
        lines.extend(f"- {error}" for error in report["errors"])
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output", default="output/validation/core_runtime_guard_suite.json")
    parser.add_argument(
        "--markdown-output", default="output/validation/core_runtime_guard_suite.md"
    )
    parser.add_argument("--step-output-dir", default="output/validation/core_runtime_guard_suite")
    parser.add_argument("--timeout-seconds", type=int, default=180)
    parser.add_argument(
        "--section",
        action="append",
        default=[],
        help="Optional discovered smoke name/path fragment to run. Omit to run all discovered guard smokes.",
    )
    parser.add_argument("--list", action="store_true")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    step_output_dir = Path(args.step_output_dir)
    if not step_output_dir.is_absolute():
        step_output_dir = repo_root / step_output_dir
    step_output_dir.mkdir(parents=True, exist_ok=True)

    discovered_steps = discover_core_steps(repo_root)
    sections = [str(item).strip() for item in args.section or [] if str(item).strip()]
    if sections:
        discovered_steps = [
            item
            for item in discovered_steps
            if any(section in item[0] or section in item[1] for section in sections)
        ]
    if args.list:
        report = {
            "schema_version": 1,
            "kind": "core_runtime_guard_suite_registry",
            "repo_root": repo_root.as_posix(),
            "sections": sections,
            "steps": [
                {"name": name, "script": script}
                for name, script in discovered_steps
            ],
        }
        print(write_json_report(report, None), end="")
        return 0
    steps = [
        run_step(repo_root, name, script, step_output_dir, args.timeout_seconds)
        for name, script in discovered_steps
    ]
    failed = [step for step in steps if not step.get("passed")]
    discovery_errors = [] if discovered_steps else ["no CORE_RUNTIME_GUARD smoke discovered"]
    report = {
        "schema_version": 1,
        "kind": "core_runtime_guard_suite",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "repo_root": repo_root.as_posix(),
        "passed": not failed and not discovery_errors,
        "discovered_step_count": len(discovered_steps),
        "steps": steps,
        "failed_steps": failed,
        "errors": discovery_errors + [f"core guard failed: {step.get('name')}" for step in failed],
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
    }

    output = Path(args.output)
    markdown = Path(args.markdown_output)
    if not output.is_absolute():
        output = repo_root / output
    if not markdown.is_absolute():
        markdown = repo_root / markdown
    print(write_json_report(report, output), end="")
    write_text_report(render_markdown(report), markdown)
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
