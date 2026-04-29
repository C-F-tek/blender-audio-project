#!/usr/bin/env python3
"""Run a matrix of safe dry-run checks for the AI artifact pipeline.

The matrix invokes ``Tools/ai/run_parallel_artifact_pipeline.py`` with several
non-invasive configurations and writes compact JSON and Markdown summaries.
It does not run NPU/GPU/Blender workloads because every invocation includes
``--dry-run``.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

try:
    from pipeline.markdown_report import write_dry_run_matrix_markdown
except ImportError:  # Allows package-style imports during external checks.
    from Tools.ai.pipeline.markdown_report import write_dry_run_matrix_markdown  # type: ignore


@dataclass(frozen=True)
class MatrixCase:
    name: str
    args: tuple[str, ...]
    purpose: str


def default_cases() -> tuple[MatrixCase, ...]:
    return (
        MatrixCase(
            name="base",
            args=("--dry-run", "--write-dry-run-report"),
            purpose="Default safe dry-run with guardrail and smart context enabled.",
        ),
        MatrixCase(
            name="no_auto_remediation",
            args=("--dry-run", "--write-dry-run-report", "--no-guardrail-auto-remediate"),
            purpose="Verify pipeline without automatic guardrail remediation passes.",
        ),
        MatrixCase(
            name="no_npu_guardrail",
            args=("--dry-run", "--write-dry-run-report", "--no-npu-guardrail"),
            purpose="Verify pipeline when NPU guardrail is disabled.",
        ),
        MatrixCase(
            name="with_validation",
            args=("--dry-run", "--write-dry-run-report", "--validate"),
            purpose="Verify validate_ai_artifacts stage planning.",
        ),
        MatrixCase(
            name="with_chunks",
            args=("--dry-run", "--write-dry-run-report", "--build-chunks"),
            purpose="Verify semantic code chunk stage planning.",
        ),
    )


def run_case(repo_root: Path, output_dir: Path, case: MatrixCase) -> dict[str, Any]:
    script = repo_root / "Tools" / "ai" / "run_parallel_artifact_pipeline.py"
    case_output = output_dir / case.name
    case_output.mkdir(parents=True, exist_ok=True)
    command = [
        sys.executable,
        str(script),
        "--repo-root",
        str(repo_root),
        "--output-dir",
        str(case_output),
        *case.args,
    ]

    started = time.perf_counter()
    completed = subprocess.run(
        command,
        cwd=str(repo_root),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    duration_sec = round(time.perf_counter() - started, 4)
    report_path = case_output / "ai_pipeline_dry_run_report.json"
    report_payload: dict[str, Any] | None = None
    if report_path.exists():
        try:
            report_payload = json.loads(report_path.read_text(encoding="utf-8"))
        except Exception as exc:
            report_payload = {"parse_error": f"{type(exc).__name__}: {exc}"}

    return {
        "name": case.name,
        "purpose": case.purpose,
        "command": command,
        "returncode": completed.returncode,
        "duration_sec": duration_sec,
        "stdout_tail": completed.stdout[-6000:],
        "stderr_tail": completed.stderr[-6000:],
        "report_path": str(report_path),
        "report_exists": report_path.exists(),
        "report_passed": report_payload.get("passed") if isinstance(report_payload, dict) else None,
        "step_count": report_payload.get("step_count") if isinstance(report_payload, dict) else None,
        "lanes": report_payload.get("lanes") if isinstance(report_payload, dict) else None,
        "summary": report_payload.get("summary") if isinstance(report_payload, dict) else None,
        "schedule": report_payload.get("schedule") if isinstance(report_payload, dict) else None,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output-dir", default="output/ai_pipeline/dry_run_matrix")
    parser.add_argument("--output", default="output/ai_pipeline/dry_run_matrix_report.json")
    parser.add_argument("--markdown-output", default="output/ai_pipeline/dry_run_matrix_report.md")
    parser.add_argument("--continue-on-error", action="store_true")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    results: list[dict[str, Any]] = []
    for case in default_cases():
        result = run_case(repo_root, output_dir, case)
        results.append(result)
        if result["returncode"] != 0 and not args.continue_on_error:
            break

    passed = all(item["returncode"] == 0 and item.get("report_passed") is True for item in results)
    report = {
        "schema_version": 1,
        "repo_root": str(repo_root),
        "output_dir": str(output_dir),
        "case_count": len(results),
        "passed": passed,
        "results": results,
    }

    output = Path(args.output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    markdown_output = write_dry_run_matrix_markdown(args.markdown_output, report)
    report["markdown_output"] = str(markdown_output)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if passed else 2


if __name__ == "__main__":
    raise SystemExit(main())
