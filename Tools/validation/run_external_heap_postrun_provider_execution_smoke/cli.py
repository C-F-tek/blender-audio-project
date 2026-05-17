#!/usr/bin/env python3
"""Smoke-test post-run preservation of explicit provider execution evidence.

The historical failure mode is an external heap run where provider/NPU workload
files contain explicit execution evidence, for example ``performed=True``, while
the final external_heap_postrun_package.json reports
``provider_execution_performed=false``. This smoke creates a tiny heap run fixture
and executes the existing post-run orchestrator end-to-end. It does not execute
providers, Blender, patch application or source writes.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
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


def env_for(repo_root: Path) -> dict[str, str]:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(repo_root) + (
        os.pathsep + env["PYTHONPATH"] if env.get("PYTHONPATH") else ""
    )
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


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def read_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def write_fixture_run(repo_root: Path) -> Path:
    run_dir = (
        repo_root
        / "output"
        / "validation"
        / "heap_context_closure_postrun_provider_execution_smoke"
    )
    shutil.rmtree(run_dir, ignore_errors=True)
    provider_dir = run_dir / "provider_teamwork"
    provider_dir.mkdir(parents=True, exist_ok=True)

    response_text = (
        "NPU micro-task eseguita: mode=npu_ready, devices=['CPU', 'GPU.0', 'GPU.1', 'NPU'], "
        "npu_available=True. Workload NPU reale richiesto: performed=True, passed=True, "
        "iterations=42, seconds=0.01."
    )
    provider_report = {
        "schema_version": 1,
        "kind": "npu_micro_task_auditor",
        "lane": "npu_micro_task_auditor",
        "passed": True,
        "provider_execution_performed": None,
        "response_text": response_text,
        "patch_application_performed": False,
        "source_writes_performed": False,
    }
    write_json(provider_dir / "npu_micro_task_auditor.json", provider_report)

    composer = {
        "schema_version": 1,
        "kind": "heap_final_proposal_composer",
        "product_status": "blocked_with_reason",
        "quality_output_passed": False,
        "proposal_count": 0,
        "accepted_proposal_count": 0,
        "rejected_proposal_count": 0,
        "provider_report_count": 1,
        "gpu0_review_count": 0,
        "npu_audit_count": 1,
        "blocking_issues": ["smoke blocked product"],
        "startup_manifest": {
            "input_ready_before_heap": True,
            "contract": {"input_ready_before_heap": True},
            "artifacts": {"tool_catalog_json": "output/validation/smoke_tool_catalog.json"},
        },
        "provider_reports": [
            {
                "kind": provider_report["kind"],
                "lane": provider_report["lane"],
                "passed": provider_report["passed"],
                "provider_execution_performed": provider_report["provider_execution_performed"],
                "response_text": response_text,
            }
        ],
        "npu_audits": [{"provider_execution_performed": None, "summary": response_text}],
        "patch_application_performed": False,
        "source_writes_performed": False,
    }
    write_json(run_dir / "heap_final_proposal_composer.json", composer)
    return run_dir


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# External Heap Postrun Provider Execution Smoke",
        "",
        f"- Passed: `{report.get('passed')}`",
        f"- Fixture run dir: `{report.get('fixture_run_dir')}`",
        f"- Postrun provider execution: `{report.get('postrun_provider_execution_performed')}`",
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


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument(
        "--output", default="output/validation/external_heap_postrun_provider_execution_smoke.json"
    )
    parser.add_argument(
        "--markdown-output",
        default="output/validation/external_heap_postrun_provider_execution_smoke.md",
    )
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    run_dir = write_fixture_run(repo_root)
    command = [
        sys.executable,
        "Tools/ai/run_external_heap_postrun_package/cli.py",
        "--repo-root",
        ".",
        "--run-dir",
        str(run_dir),
        "--include-peer-blocks",
        "--include-rejected-history",
        "--no-documents-copy",
    ]
    command_result = run(command, repo_root)
    postrun = read_json(run_dir / "external_heap_postrun_package.json")
    pointer = read_json(run_dir / "external_heap_block_pointer_manifest.json")
    causality = read_json(run_dir / "heap_final_causality_normalized.json")
    long_response = read_json(run_dir / "external_heap_primary_long_response.json")
    revision = read_json(run_dir / "external_heap_revision_context.json")

    checks = [
        {"name": "postrun_returncode_zero", "passed": command_result.get("passed") is True},
        {"name": "postrun_package_passed", "passed": postrun.get("passed") is True},
        {
            "name": "postrun_provider_execution_true",
            "passed": postrun.get("provider_execution_performed") is True,
        },
        {
            "name": "pointer_provider_execution_true",
            "passed": pointer.get("provider_execution_performed") is True,
        },
        {
            "name": "causality_provider_execution_true",
            "passed": causality.get("provider_execution_performed") is True,
        },
        {
            "name": "long_response_provider_execution_true",
            "passed": long_response.get("provider_execution_performed") is True,
        },
        {
            "name": "revision_provider_execution_true",
            "passed": revision.get("provider_execution_performed") is True,
        },
        {
            "name": "no_patch_application",
            "passed": postrun.get("patch_application_performed") is False,
        },
        {"name": "no_source_writes", "passed": postrun.get("source_writes_performed") is False},
    ]
    errors = [str(check["name"]) for check in checks if check.get("passed") is not True]
    report = {
        "schema_version": 1,
        "kind": "external_heap_postrun_provider_execution_smoke",
        "repo_root": repo_root.as_posix(),
        "fixture_run_dir": str(run_dir),
        "passed": not errors,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "output_artifact_writes_performed": True,
        "postrun_provider_execution_performed": postrun.get("provider_execution_performed"),
        "checks": checks,
        "command_result": command_result,
        "errors": errors,
        "warnings": [],
    }
    print(write_json_report(report, resolve_output_path(repo_root, args.output)), end="")
    write_text_report(render_markdown(report), resolve_output_path(repo_root, args.markdown_output))
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
