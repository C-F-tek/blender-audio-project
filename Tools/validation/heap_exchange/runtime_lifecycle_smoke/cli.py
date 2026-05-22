#!/usr/bin/env python3
"""Smoke-test heap/exchange runtime lifecycle entry/exit.

The smoke verifies boundary semantics only: entry creates a dynamic runtime
session, state records lane availability, exit fails without concrete product
and passes when concrete operations are present.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
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


def build_env(source_repo: Path) -> dict[str, str]:
    env = os.environ.copy()
    existing_pythonpath = env.get("PYTHONPATH", "")
    source_pythonpath = str(source_repo)
    env["PYTHONPATH"] = (
        source_pythonpath
        if not existing_pythonpath
        else source_pythonpath + os.pathsep + existing_pythonpath
    )
    return env


def run(command: list[str], cwd: Path, source_repo: Path) -> dict[str, Any]:
    result = subprocess.run(
        command,
        cwd=cwd,
        env=build_env(source_repo),
        capture_output=True,
        text=True,
        check=False,
        timeout=120,
    )
    return {
        "command": command,
        "returncode": result.returncode,
        "stdout_tail": result.stdout[-6000:],
        "stderr_tail": result.stderr[-6000:],
        "ok": result.returncode == 0,
    }


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def prepare_base(repo: Path, stamp: str) -> None:
    (repo / "output/local_ai_task_inputs").mkdir(parents=True, exist_ok=True)
    (repo / f"output/local_ai_task_inputs/task-{stamp}.md").write_text(
        "# Task\n\nRuntime lifecycle smoke.\n", encoding="utf-8"
    )
    write_json(
        repo / f"output/validation/openvino_gpu0_workload_{stamp}.json",
        {
            "kind": "openvino_gpu0_workload",
            "passed": True,
            "available_devices": ["CPU", "GPU.0", "GPU.1", "NPU"],
            "selected_device": "GPU.0",
            "openvino_gpu0_visible": True,
            "openvino_gpu0_workload_performed": True,
            "openvino_gpu0_workload_passed": True,
            "openvino_gpu1_reserved_visible": True,
        },
    )
    write_json(
        repo / f"output/validation/{stamp}_phase_official.json",
        {
            "kind": "unified_launcher_phase_status",
            "passed": True,
            "status": "passed",
            "return_code": 0,
        },
    )
    write_json(
        repo / "output/validation/ai_workload_report_quality.json",
        {"kind": "ai_workload_report_quality", "passed": True},
    )


def write_apply_report(repo: Path, stamp: str, *, concrete: bool) -> Path:
    path = repo / f"output/validation/patch_suggestion_bundle_apply_smoke_{stamp}.json"
    write_json(
        path,
        {
            "kind": "patch_suggestion_bundle_apply",
            "passed": True,
            "operation_count": 1 if concrete else 0,
            "changed_count": 1 if concrete else 0,
            "applied_count": 1 if concrete else 0,
            "manual_review_required": not concrete,
            "manual_review_items": []
            if concrete
            else [
                {
                    "id": "metadata",
                    "reason": "metadata-only draft operation has no concrete replacements",
                }
            ],
            "results": [
                {
                    "operation": "append_once",
                    "path": "docs/LOCAL_AI_TASKS/example.md",
                    "changed": True,
                    "applied": True,
                    "ok": True,
                }
            ]
            if concrete
            else [],
        },
    )
    return path


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Heap Exchange Runtime Lifecycle Smoke",
        "",
        f"- Passed: `{report.get('passed')}`",
        "",
    ]
    for case in report.get("cases") or []:
        lines.append(f"- `{case.get('name')}`: `{case.get('passed')}`")
    if report.get("errors"):
        lines.extend(["", "## Errors", ""])
        lines.extend(f"- {error}" for error in report["errors"])
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument(
        "--output", default="output/validation/heap_exchange_runtime_lifecycle_smoke.json"
    )
    parser.add_argument(
        "--markdown-output", default="output/validation/heap_exchange_runtime_lifecycle_smoke.md"
    )
    args = parser.parse_args()

    source_repo = Path(args.repo_root).resolve()
    cases: list[dict[str, Any]] = []
    errors: list[str] = []

    with tempfile.TemporaryDirectory(prefix="heap-exchange-lifecycle-") as tmp:
        repo = Path(tmp) / "repo"
        repo.mkdir()

        missing_stamp = "missing_concrete"
        prepare_base(repo, missing_stamp)
        missing_apply = write_apply_report(repo, missing_stamp, concrete=False)
        entry_result = run(
            [
                sys.executable,
                "-m",
                "ia_carmine",
                "heap_exchange_runtime_entry",
                "--repo-root",
                str(repo),
                "--stamp",
                missing_stamp,
                "--task-file",
                f"output/local_ai_task_inputs/task-{missing_stamp}.md",
                "--observer-dir",
                f"output/local_ai_runs/{missing_stamp}_observer",
            ],
            repo,
            source_repo,
        )
        exit_result = run(
            [
                sys.executable,
                "-m",
                "ia_carmine",
                "heap_exchange_runtime_exit",
                "--repo-root",
                str(repo),
                "--stamp",
                missing_stamp,
                "--apply-report",
                str(missing_apply),
                "--observer-dir",
                f"output/local_ai_runs/{missing_stamp}_observer",
                "--require-concrete-product",
            ],
            repo,
            source_repo,
        )
        lifecycle_result = run(
            [
                sys.executable,
                "-m",
                "Tools.validation",
                "check_heap_exchange_runtime_lifecycle",
                "--repo-root",
                str(repo),
                "--stamp",
                missing_stamp,
                "--observer-dir",
                f"output/local_ai_runs/{missing_stamp}_observer",
                "--require-public-events",
                "--require-concrete-exit",
                "--require-knowledge-surface",
                "--output",
                "output/validation/missing_lifecycle.json",
            ],
            repo,
            source_repo,
        )
        missing_ok = (
            entry_result["returncode"] == 0
            and exit_result["returncode"] == 2
            and lifecycle_result["returncode"] == 2
        )
        cases.append(
            {
                "name": "entry_passes_exit_blocks_without_concrete_product",
                "passed": missing_ok,
                "entry": entry_result,
                "exit": exit_result,
                "lifecycle": lifecycle_result,
            }
        )
        if not missing_ok:
            errors.append(
                "missing concrete product case did not produce expected entry pass / exit fail / lifecycle fail"
            )

        concrete_stamp = "concrete_product"
        prepare_base(repo, concrete_stamp)
        concrete_apply = write_apply_report(repo, concrete_stamp, concrete=True)
        entry_result = run(
            [
                sys.executable,
                "-m",
                "ia_carmine",
                "heap_exchange_runtime_entry",
                "--repo-root",
                str(repo),
                "--stamp",
                concrete_stamp,
                "--task-file",
                f"output/local_ai_task_inputs/task-{concrete_stamp}.md",
                "--observer-dir",
                f"output/local_ai_runs/{concrete_stamp}_observer",
            ],
            repo,
            source_repo,
        )
        exit_result = run(
            [
                sys.executable,
                "-m",
                "ia_carmine",
                "heap_exchange_runtime_exit",
                "--repo-root",
                str(repo),
                "--stamp",
                concrete_stamp,
                "--apply-report",
                str(concrete_apply),
                "--observer-dir",
                f"output/local_ai_runs/{concrete_stamp}_observer",
                "--require-concrete-product",
            ],
            repo,
            source_repo,
        )
        lifecycle_result = run(
            [
                sys.executable,
                "-m",
                "Tools.validation",
                "check_heap_exchange_runtime_lifecycle",
                "--repo-root",
                str(repo),
                "--stamp",
                concrete_stamp,
                "--observer-dir",
                f"output/local_ai_runs/{concrete_stamp}_observer",
                "--require-public-events",
                "--require-concrete-exit",
                "--require-knowledge-surface",
                "--output",
                "output/validation/concrete_lifecycle.json",
            ],
            repo,
            source_repo,
        )
        concrete_ok = (
            entry_result["returncode"] == 0
            and exit_result["returncode"] == 0
            and lifecycle_result["returncode"] == 0
        )
        cases.append(
            {
                "name": "entry_exit_lifecycle_pass_with_concrete_product",
                "passed": concrete_ok,
                "entry": entry_result,
                "exit": exit_result,
                "lifecycle": lifecycle_result,
            }
        )
        if not concrete_ok:
            errors.append("concrete product case did not pass lifecycle")

    report = {
        "schema_version": 1,
        "kind": "heap_exchange_runtime_lifecycle_smoke",
        "repo_root": source_repo.as_posix(),
        "passed": not errors,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "cases": cases,
        "errors": errors,
        "warnings": [],
    }
    output = resolve_output_path(source_repo, args.output)
    markdown = resolve_output_path(source_repo, args.markdown_output)
    print(write_json_report(report, output), end="")
    write_text_report(render_markdown(report), markdown)
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
