#!/usr/bin/env python3
"""Smoke-test task ingress contract builder."""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    from report_utils import resolve_output_path, write_json_report
except ImportError:
    from Tools.validation.report_utils import resolve_output_path, write_json_report  # type: ignore


STAMP = "task_ingress_contract_smoke_20990101-010203"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output", default="output/validation/task_ingress_contract_smoke.json")
    args = parser.parse_args()

    source_repo = Path(args.repo_root).resolve()
    errors: list[str] = []

    with tempfile.TemporaryDirectory(prefix="task-ingress-contract-") as tmp_raw:
        repo = Path(tmp_raw) / "repo"
        repo.mkdir()
        task = repo / "docs/LOCAL_AI_TASKS/smoke-task.md"
        task.parent.mkdir(parents=True, exist_ok=True)
        task.write_text(
            "# Smoke Task\n\nUse heap/exchange with GPU1 GPU0 NPU and create a review PR patch product.\n",
            encoding="utf-8",
        )

        runtime_state = repo / "output/ai_packets/stamp/heap_exchange_runtime_state.jsonl"
        observer = repo / "output/local_ai_runs/stamp_observer"
        output = repo / "output/ai_packets/stamp/task_ingress_contract.json"
        markdown = repo / "output/ai_packets/stamp/task_ingress_contract.md"

        env = dict(os.environ)
        env["PYTHONPATH"] = str(source_repo)
        result = subprocess.run(
            [
                sys.executable,
                str(source_repo / "Tools/ai/build_task_ingress_contract.py"),
                "--repo-root",
                str(repo),
                "--stamp",
                STAMP,
                "--task-file",
                str(task),
                "--runtime-state",
                str(runtime_state),
                "--observer-dir",
                str(observer),
                "--output",
                str(output),
                "--markdown-output",
                str(markdown),
            ],
            cwd=repo,
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )

        report = json.loads(output.read_text(encoding="utf-8-sig")) if output.exists() else {}
        if result.returncode != 0:
            errors.append(f"builder failed: {result.stderr[-500:]}")
        if report.get("passed") is not True:
            errors.append(f"ingress report did not pass: {report.get('errors')}")
        if not report.get("task_sha256"):
            errors.append("task sha256 missing")
        if report.get("intent", {}).get("requires_heap_exchange") is not True:
            errors.append("requires_heap_exchange not detected")
        if report.get("intent", {}).get("requires_reviewable_product") is not True:
            errors.append("requires_reviewable_product not detected")
        if not runtime_state.exists():
            errors.append("runtime state event missing")
        if not (observer / "ai_public_events.jsonl").exists():
            errors.append("observer public event missing")
        if not markdown.exists():
            errors.append("markdown output missing")

    final = {
        "schema_version": 1,
        "kind": "task_ingress_contract_smoke",
        "repo_root": source_repo.as_posix(),
        "passed": not errors,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "errors": errors,
        "warnings": [],
    }

    output_path = resolve_output_path(source_repo, args.output)
    print(write_json_report(final, output_path), end="")
    return 0 if final["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
