#!/usr/bin/env python3
"""Smoke-test external heap launcher command generation.

This smoke does not run providers and does not execute the heap runtime. It only
checks that profile-driven command generation exposes the expected external heap
operator commands and, when a prior revision context exists, injects it into the
reviewable launcher request.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

try:
    from report_utils import resolve_output_path, write_json_report, write_text_report
except ImportError:  # pragma: no cover
    from Tools.validation.report_utils import resolve_output_path, write_json_report, write_text_report  # type: ignore


def env_for(repo_root: Path) -> dict[str, str]:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(repo_root) + (os.pathsep + env["PYTHONPATH"] if env.get("PYTHONPATH") else "")
    return env


def run(command: list[str], repo_root: Path) -> dict[str, Any]:
    completed = subprocess.run(
        command,
        cwd=repo_root,
        env=env_for(repo_root),
        capture_output=True,
        text=True,
        check=False,
        timeout=120,
    )
    return {
        "command": command,
        "returncode": completed.returncode,
        "passed": completed.returncode == 0,
        "stdout_tail": (completed.stdout or "")[-4000:],
        "stderr_tail": (completed.stderr or "")[-4000:],
    }


def read_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def latest_revision_context_exists(repo_root: Path) -> bool:
    validation_dir = repo_root / "output" / "validation"
    if not validation_dir.exists():
        return False
    return any(validation_dir.glob("heap_context_closure_*/external_heap_revision_context.json"))


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Heap Runtime Launcher Command Smoke",
        "",
        f"- Passed: `{report.get('passed')}`",
        f"- Revision context fixture used: `{report.get('revision_context_fixture_used')}`",
        f"- Output artifact writes performed: `{report.get('output_artifact_writes_performed')}`",
        "",
        "## Checks",
        "",
    ]
    for check in report.get("checks") or []:
        lines.append(f"- `{check.get('name')}`: `{check.get('passed')}`")
    if report.get("errors"):
        lines.extend(["", "## Errors", ""])
        lines.extend(f"- {error}" for error in report.get("errors") or [])
    return "\n".join(lines) + "\n"


def ensure_revision_context_fixture(repo_root: Path) -> tuple[bool, Path]:
    if latest_revision_context_exists(repo_root):
        return False, Path("")
    run_dir = repo_root / "output" / "validation" / "heap_context_closure_smoke_revision_context"
    run_dir.mkdir(parents=True, exist_ok=True)
    fixture = run_dir / "external_heap_revision_context.json"
    fixture.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "kind": "external_heap_revision_context",
                "protocol": "external_heap_revision_context_v1",
                "product_acceptance_status": "blocked",
                "resume_from_block_id": "proposal_smoke_previous",
                "latest_block_id": "proposal_smoke_latest",
                "tasks": [
                    {
                        "task_id": "gpu1_rewrite_rejected_proposal_smoke",
                        "role": "gpu1_planner",
                        "task_type": "rewrite_rejected_block",
                        "target_block_id": "proposal_smoke_latest",
                        "resume_from_block_id": "proposal_smoke_previous",
                        "instruction": "Smoke fixture task.",
                    }
                ],
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    return True, fixture


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output", default="output/validation/heap_runtime_launcher_command_smoke.json")
    parser.add_argument("--markdown-output", default="output/validation/heap_runtime_launcher_command_smoke.md")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    fixture_used, fixture_path = ensure_revision_context_fixture(repo_root)
    output_json = repo_root / "output" / "validation" / "heap_launcher_command_smoke.json"
    command = [
        sys.executable,
        "Tools/ai/build_heap_runtime_launcher_command.py",
        "--repo-root",
        ".",
        "--profile",
        "balanced_external_heap",
        "--include-postrun-package-command",
        "--output",
        str(output_json),
    ]
    result = run(command, repo_root)
    payload = read_json(output_json)
    generated_command = str(payload.get("command") or "")
    checks = [
        {"name": "command_builder_returncode_zero", "passed": result.get("passed") is True},
        {"name": "schema_version_5", "passed": payload.get("schema_version") == 5},
        {"name": "profile_balanced", "passed": payload.get("profile_name") == "balanced_external_heap"},
        {"name": "postrun_package_command_present", "passed": bool(payload.get("postrun_package_command"))},
        {"name": "revision_context_loaded", "passed": payload.get("revision_context_loaded") is True},
        {
            "name": "revision_context_injected_into_request",
            "passed": "EXTERNAL HEAP REVISION CONTEXT FROM PREVIOUS RUN" in generated_command,
        },
        {
            "name": "main_command_targets_heap_closure",
            "passed": "run_heap_runtime_context_closure.py" in generated_command,
        },
        {
            "name": "postrun_command_targets_orchestrator",
            "passed": "run_external_heap_postrun_package.py" in str(payload.get("postrun_package_command") or ""),
        },
    ]
    errors = [check["name"] for check in checks if not check.get("passed")]
    report = {
        "schema_version": 1,
        "kind": "heap_runtime_launcher_command_smoke",
        "repo_root": repo_root.as_posix(),
        "passed": not errors,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "output_artifact_writes_performed": bool(fixture_used),
        "revision_context_fixture_used": fixture_used,
        "revision_context_fixture_path": str(fixture_path) if fixture_used else "",
        "generated_command_json": str(output_json),
        "checks": checks,
        "command_result": result,
        "errors": errors,
        "warnings": [],
    }
    print(write_json_report(report, resolve_output_path(repo_root, args.output)), end="")
    write_text_report(render_markdown(report), resolve_output_path(repo_root, args.markdown_output))
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
