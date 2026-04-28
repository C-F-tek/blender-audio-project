#!/usr/bin/env python3
"""Additive orchestrator for the AI artifact pipeline."""
from __future__ import annotations

import argparse
import json
import shlex
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def script(repo: Path, rel: str) -> str:
    return str((repo / rel).resolve())


def run(command: list[str], cwd: Path, dry_run: bool) -> dict[str, Any]:
    start = time.perf_counter()
    if dry_run:
        return {"command": command, "dry_run": True, "returncode": 0, "duration_sec": 0.0, "stdout": "", "stderr": ""}
    done = subprocess.run(command, cwd=str(cwd), text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    return {
        "command": command,
        "dry_run": False,
        "returncode": done.returncode,
        "duration_sec": round(time.perf_counter() - start, 4),
        "stdout": done.stdout[-8000:],
        "stderr": done.stderr[-8000:],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--analysis-json")
    parser.add_argument("--output-dir", default="output/ai_pipeline")
    parser.add_argument("--build-chunks", action="store_true")
    parser.add_argument("--build-music-summary", action="store_true")
    parser.add_argument("--use-npu", action="store_true")
    parser.add_argument("--npu-workers", type=int, default=4)
    parser.add_argument("--gpu-command", help="External command with placeholders {brief} and {output}.")
    parser.add_argument("--validate", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--continue-on-error", action="store_true")
    args = parser.parse_args()

    repo = Path(args.repo_root).resolve()
    out = Path(args.output_dir).resolve()
    out.mkdir(parents=True, exist_ok=True)
    py = sys.executable
    serial: list[tuple[str, list[str]]] = []
    parallel: list[tuple[str, list[str]]] = []

    if args.build_chunks:
        serial.append(("build_semantic_code_chunks", [py, script(repo, "Tools/npu/build_semantic_code_chunks.py"), "--repo-root", str(repo)]))
    if args.build_music_summary:
        if not args.analysis_json:
            raise SystemExit("--build-music-summary requires --analysis-json")
        serial.append(("build_music_intermediates", [py, script(repo, "Tools/ai/build_music_intermediates.py"), "--analysis-json", str(Path(args.analysis_json).resolve()), "--output-dir", str(out)]))
    if args.use_npu:
        parallel.append(("npu_artifact_review", [py, script(repo, "Tools/npu/run_npu_artifact_reviewer.py"), "--input", str(out), "--output", str(out / "npu_artifact_review.json"), "--max-workers", str(args.npu_workers)]))
    if args.gpu_command:
        command = args.gpu_command.format(brief=str(out / "ai_scene_brief.json"), output=str(out / "gpu_planner_output.json"))
        parallel.append(("gpu_command", shlex.split(command)))
    if args.validate:
        serial.append(("validate_ai_artifacts", [py, script(repo, "Tools/ai/validate_ai_artifacts.py"), "--repo-root", str(repo), "--artifact-dir", str(out), "--output", str(out / "ai_validation_report.json"), "--allow-errors"]))

    results: list[dict[str, Any]] = []
    for name, command in serial:
        result = run(command, repo, args.dry_run)
        result["name"] = name
        results.append(result)
        if result["returncode"] and not args.continue_on_error:
            break

    if parallel and all(r["returncode"] == 0 for r in results):
        with ThreadPoolExecutor(max_workers=len(parallel)) as pool:
            futures = {pool.submit(run, cmd, repo, args.dry_run): name for name, cmd in parallel}
            for future in as_completed(futures):
                result = future.result()
                result["name"] = futures[future]
                results.append(result)

    report = {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "repo_root": str(repo),
        "output_dir": str(out),
        "dry_run": args.dry_run,
        "passed": all(r["returncode"] == 0 for r in results),
        "step_count": len(results),
        "steps": results,
    }
    if not args.dry_run:
        (out / "ai_pipeline_run_report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
