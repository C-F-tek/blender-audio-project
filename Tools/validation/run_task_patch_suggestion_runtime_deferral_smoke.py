#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import tempfile
from pathlib import Path
from typing import Any

try:
    from report_utils import resolve_output_path, write_json_report
except ImportError:
    from Tools.validation.report_utils import resolve_output_path, write_json_report  # type: ignore


def run_case(source_repo: Path, repo: Path, task_rel: str, name: str) -> dict[str, Any]:
    task_path = repo / task_rel
    task_path.parent.mkdir(parents=True, exist_ok=True)
    task_path.write_text(
        "# Runtime entry task\n\nNo embedded patch suggestions.\n", encoding="utf-8"
    )
    out = repo / "output/validation" / f"{name}.json"
    cmd = [
        "python",
        str(source_repo / "Tools/ai/build_task_patch_suggestion_report.py"),
        "--repo-root",
        str(repo),
        "--task-file",
        task_rel,
        "--Stamp",
        "runtime_deferral_smoke_20990101-010203",
        "--output",
        str(out),
    ]
    proc = subprocess.run(cmd, cwd=repo, text=True, capture_output=True, check=False)
    report = json.loads(out.read_text(encoding="utf-8")) if out.exists() else {}
    return {
        "name": name,
        "returncode": proc.returncode,
        "stdout_tail": proc.stdout[-2000:],
        "stderr_tail": proc.stderr[-2000:],
        "report": report,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument(
        "--output", default="output/validation/task_patch_suggestion_runtime_deferral_smoke.json"
    )
    args = parser.parse_args()

    source_repo = Path(args.repo_root).resolve()
    errors: list[str] = []
    with tempfile.TemporaryDirectory(prefix="task-patch-deferral-smoke-") as temp_dir:
        repo = Path(temp_dir) / "repo"
        repo.mkdir(parents=True)
        cases = [
            run_case(
                source_repo,
                repo,
                "output/local_ai_task_inputs/process-gate.md",
                "process_gate_entry",
            ),
            run_case(source_repo, repo, "docs/LOCAL_AI_TASKS/plain-task.md", "plain_task"),
        ]
    process_report = cases[0]["report"]
    plain_report = cases[1]["report"]
    if cases[0]["returncode"] != 0:
        errors.append("process gate task should pass by deferring to runtime product")
    if not process_report.get("deferred_to_runtime_product"):
        errors.append("process gate task did not mark deferred_to_runtime_product")
    if process_report.get("suggestion_count") != 0:
        errors.append("process gate task should not fabricate suggestions")
    if cases[1]["returncode"] == 0:
        errors.append("plain task without suggestions should still fail")
    if plain_report.get("deferred_to_runtime_product"):
        errors.append("plain task should not defer to runtime product")

    report: dict[str, Any] = {
        "schema_version": 1,
        "kind": "task_patch_suggestion_runtime_deferral_smoke",
        "repo_root": source_repo.as_posix(),
        "passed": not errors,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "cases": cases,
        "errors": errors,
        "warnings": [],
    }
    print(write_json_report(report, resolve_output_path(source_repo, args.output)), end="")
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
