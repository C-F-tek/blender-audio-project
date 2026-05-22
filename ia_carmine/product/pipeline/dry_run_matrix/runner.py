"""Execution helpers for the pipeline dry-run matrix."""

from __future__ import annotations

import json
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

from .common import MatrixCase

def run_case(repo_root: Path, output_dir: Path, case: MatrixCase) -> dict[str, Any]:
    case_output = output_dir / case.name
    case_output.mkdir(parents=True, exist_ok=True)
    command = [
        sys.executable,
        "-m",
        "ia_carmine",
        "run_parallel_artifact_pipeline",
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
        capture_output=True,
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
        "report_passed": (
            report_payload.get("passed") if isinstance(report_payload, dict) else None
        ),
        "step_count": (
            report_payload.get("step_count") if isinstance(report_payload, dict) else None
        ),
        "lanes": (report_payload.get("lanes") if isinstance(report_payload, dict) else None),
        "summary": (report_payload.get("summary") if isinstance(report_payload, dict) else None),
        "schedule": (report_payload.get("schedule") if isinstance(report_payload, dict) else None),
        "agent_state_packet": (
            report_payload.get("agent_state_packet") if isinstance(report_payload, dict) else None
        ),
    }

def run_cases(
    repo_root: Path,
    output_dir: Path,
    cases: tuple[MatrixCase, ...],
    matrix_workers: int,
    continue_on_error: bool,
) -> list[dict[str, Any]]:
    """Run matrix cases, preserving deterministic report order."""
    if matrix_workers <= 1:
        results: list[dict[str, Any]] = []
        for case in cases:
            result = run_case(repo_root, output_dir, case)
            results.append(result)
            if result["returncode"] != 0 and not continue_on_error:
                break
        return results

    results_by_index: dict[int, dict[str, Any]] = {}
    with ThreadPoolExecutor(max_workers=matrix_workers) as pool:
        futures = {
            pool.submit(run_case, repo_root, output_dir, case): index
            for index, case in enumerate(cases)
        }
        for future in as_completed(futures):
            index = futures[future]
            try:
                results_by_index[index] = future.result()
            except Exception as exc:
                case = cases[index]
                results_by_index[index] = {
                    "name": case.name,
                    "purpose": case.purpose,
                    "command": None,
                    "returncode": 1,
                    "duration_sec": 0.0,
                    "stdout_tail": "",
                    "stderr_tail": "",
                    "report_path": None,
                    "report_exists": False,
                    "report_passed": False,
                    "step_count": None,
                    "lanes": None,
                    "summary": None,
                    "schedule": None,
                    "agent_state_packet": None,
                    "matrix_error": f"{type(exc).__name__}: {exc}",
                }
    return [results_by_index[index] for index in sorted(results_by_index)]
