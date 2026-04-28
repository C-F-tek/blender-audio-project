#!/usr/bin/env python3
"""Safe additive orchestrator for the AI artifact pipeline."""
from __future__ import annotations

import argparse
import json
import os
import platform
import shlex
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

EXPECTED_MUSIC_ARTIFACTS = [
    "track_summary.json",
    "music_segments.json",
    "audio_event_map.json",
    "ai_scene_brief.json",
    "ai_resource_budget.json",
]
EXPECTED_CHUNK_ARTIFACTS = [
    "indexAI/code_chunks/semantic_code_chunks.json",
    "indexAI/code_chunks/semantic_code_chunks_manifest.json",
]
EXPECTED_SMART_CONTEXT_ARTIFACTS = [
    "smart_context/{track_slug}_smart_context_packet.json",
    "smart_context/{track_slug}_smart_context_manifest.json",
    "smart_context/{track_slug}_smart_context_packet.md",
]


def slugify(value: str) -> str:
    import re
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    value = re.sub(r"_+", "_", value).strip("_")
    return value or "track"


def run(cmd: list[str], cwd: Path, dry: bool) -> dict[str, Any]:
    start = time.perf_counter()
    if dry:
        return {"command": cmd, "dry_run": True, "returncode": 0, "duration_sec": 0.0, "stdout": "", "stderr": "", "planned_only": True}
    done = subprocess.run(cmd, cwd=str(cwd), text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    return {"command": cmd, "dry_run": False, "returncode": done.returncode, "duration_sec": round(time.perf_counter() - start, 4), "stdout": done.stdout[-8000:], "stderr": done.stderr[-8000:], "planned_only": False}


def rel(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return str(path)


def read_text_if_exists(path: Path, limit: int = 6000) -> str | None:
    if not path.exists():
        return None
    return path.read_text(encoding="utf-8", errors="replace")[:limit]


def file_meta(path: Path, root: Path) -> dict[str, Any]:
    exists = path.exists()
    meta: dict[str, Any] = {"path": rel(path, root), "exists": exists}
    if exists and path.is_file():
        stat = path.stat()
        meta.update({"size_bytes": stat.st_size, "modified_time": datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat()})
    return meta


def planned_outputs(repo: Path, out: Path, args: argparse.Namespace) -> list[dict[str, Any]]:
    outputs: list[Path] = []
    if args.build_chunks:
        outputs += [repo / item for item in EXPECTED_CHUNK_ARTIFACTS]
    if args.build_music_summary:
        outputs += [out / item for item in EXPECTED_MUSIC_ARTIFACTS]
    if args.smart_context:
        track_slug = slugify(args.track_stem)
        outputs += [out / item.format(track_slug=track_slug) for item in EXPECTED_SMART_CONTEXT_ARTIFACTS]
    if args.use_npu:
        outputs.append(out / "npu_artifact_review.json")
    if args.npu_guardrail:
        outputs += [out / "npu_guardrail_report.json", out / "npu_guardrail_report.md", out / "npu_guardrail_preflight.json"]
    if args.gpu_command:
        outputs.append(out / "gpu_planner_output.json")
    if args.validate:
        outputs.append(out / "ai_validation_report.json")
    if not args.dry_run:
        outputs.append(out / "ai_pipeline_run_report.json")
    return [file_meta(path, repo) for path in outputs]


def python_runtime() -> dict[str, Any]:
    return {"executable": sys.executable, "version": sys.version.split()[0], "implementation": platform.python_implementation(), "platform": platform.platform()}


def workstation_context(repo: Path) -> dict[str, Any]:
    doc = repo / "docs" / "LOCAL_WORKSTATION_TARGET.md"
    text = read_text_if_exists(doc)
    return {"source": rel(doc, repo), "available": text is not None, "summary": text[:1200] if text else None}


def preflight(repo: Path, out: Path, args: argparse.Namespace) -> dict[str, Any]:
    warnings: list[str] = []
    errors: list[str] = []
    analysis = Path(args.analysis_json).resolve() if args.analysis_json else None
    if args.build_music_summary and not analysis:
        errors.append("--build-music-summary requires --analysis-json")
    if analysis and not analysis.exists():
        errors.append(f"Analysis JSON not found: {analysis}")
    if args.npu_workers > 4:
        warnings.append("npu_workers is greater than 4; local workstation policy recommends 4 or fewer.")
    if args.use_npu and not args.build_music_summary and not out.exists():
        warnings.append("NPU review was requested, but artifact directory does not exist yet.")
    if args.npu_guardrail and not args.smart_context:
        warnings.append("NPU guardrail works best with --smart-context; falling back to artifact directory review.")
    if args.gpu_command and "{brief}" not in args.gpu_command:
        warnings.append("GPU command does not include {brief}; planner may not receive ai_scene_brief.json.")
    if args.gpu_command and "{output}" not in args.gpu_command:
        warnings.append("GPU command does not include {output}; planner output may not be captured consistently.")
    blender_doc = repo / "docs" / "LOCAL_WORKSTATION_TARGET.md"
    if blender_doc.exists() and "blender command is not currently available in PATH" in blender_doc.read_text(encoding="utf-8", errors="replace"):
        warnings.append("Local workstation profile says blender is not in PATH; use full Blender executable path for CLI tests.")
    input_files = []
    if analysis:
        input_files.append(file_meta(analysis, repo))
    for item in ["docs/LOCAL_WORKSTATION_TARGET.md", "indexAI/task_capsules/blender_51_compat.json", "indexAI/task_capsules/resource_budget.json"]:
        input_files.append(file_meta(repo / item, repo))
    return {"passed": not errors, "errors": errors, "warnings": warnings, "input_files": input_files, "planned_outputs": planned_outputs(repo, out, args), "python_runtime": python_runtime(), "workstation_context": workstation_context(repo), "environment": {"cwd": os.getcwd(), "dry_run": args.dry_run}}


def step_meta(name: str, lane: str, purpose: str, expected_outputs: list[str]) -> dict[str, Any]:
    return {"name": name, "lane": lane, "purpose": purpose, "expected_outputs": expected_outputs}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("--analysis-json")
    ap.add_argument("--track-stem", default="track")
    ap.add_argument("--output-dir", default="output/ai_pipeline")
    ap.add_argument("--build-chunks", action="store_true")
    ap.add_argument("--build-music-summary", action="store_true")
    ap.add_argument("--smart-context", action="store_true", help="Build hierarchical capsule/manifest context packets for central AI.")
    ap.add_argument("--smart-task", default="Scene Director, Blender Python generation, audio-reactive keyframe preservation")
    ap.add_argument("--smart-max-packet-chars", type=int, default=22000)
    ap.add_argument("--smart-max-capsule-chars", type=int, default=3200)
    ap.add_argument("--use-npu", action="store_true")
    ap.add_argument("--npu-guardrail", action="store_true", help="Run always-on NPU-light guardrail/preflight on smart packets or artifacts.")
    ap.add_argument("--npu-workers", type=int, default=4)
    ap.add_argument("--gpu-command", help="External command with placeholders {brief} and {output}.")
    ap.add_argument("--validate", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--write-dry-run-report", action="store_true", help="Write ai_pipeline_dry_run_report.json even in dry-run mode.")
    ap.add_argument("--continue-on-error", action="store_true")
    args = ap.parse_args()
    repo = Path(args.repo_root).resolve()
    out = Path(args.output_dir).resolve()
    out.mkdir(parents=True, exist_ok=True)
    pf = preflight(repo, out, args)
    if not pf["passed"] and not args.continue_on_error:
        report = {"schema_version": 4, "generated_at": datetime.now(timezone.utc).isoformat(), "repo_root": str(repo), "output_dir": str(out), "dry_run": args.dry_run, "passed": False, "preflight": pf, "step_count": 0, "steps": []}
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return 2
    py = sys.executable
    serial: list[tuple[dict[str, Any], list[str]]] = []
    parallel: list[tuple[dict[str, Any], list[str]]] = []
    track_slug = slugify(args.track_stem)

    def script(path: str) -> str:
        return str((repo / path).resolve())

    if args.build_chunks:
        serial.append((step_meta("build_semantic_code_chunks", "CPU", "Build symbol-aware repository context for AI retrieval.", EXPECTED_CHUNK_ARTIFACTS), [py, script("Tools/npu/build_semantic_code_chunks.py"), "--repo-root", str(repo)]))
    if args.build_music_summary:
        serial.append((step_meta("build_music_intermediates", "CPU", "Build compact AI-friendly music artifacts from the full analysis JSON.", EXPECTED_MUSIC_ARTIFACTS), [py, script("Tools/ai/build_music_intermediates.py"), "--analysis-json", str(Path(args.analysis_json).resolve()), "--output-dir", str(out)]))
    if args.smart_context:
        serial.append((step_meta("build_smart_ai_context", "CPU", "Build hierarchical capsules and ranked smart context packet for central AI.", [item.format(track_slug=track_slug) for item in EXPECTED_SMART_CONTEXT_ARTIFACTS]), [py, script("Tools/workflow/smart_ai_context.py"), "--repo-root", str(repo), "--track-stem", args.track_stem, "--task", args.smart_task, "--output-dir", str(out / "smart_context"), "--max-packet-chars", str(args.smart_max_packet_chars), "--max-capsule-chars", str(args.smart_max_capsule_chars)]))
    if args.use_npu:
        parallel.append((step_meta("npu_artifact_review", "NPU", "Review compact artifacts for schema, size, blocked patterns, and obvious risks.", [str(out / "npu_artifact_review.json")]), [py, script("Tools/npu/run_npu_artifact_reviewer.py"), "--input", str(out), "--output", str(out / "npu_artifact_review.json"), "--max-workers", str(args.npu_workers)]))
    if args.npu_guardrail:
        guardrail_input = out / "smart_context" / f"{track_slug}_smart_context_packet.json" if args.smart_context else out
        parallel.append((step_meta("npu_guardrail", "NPU", "Always-on NPU-light guardrail/preflight for smart context and AI artifacts.", [str(out / "npu_guardrail_report.json"), str(out / "npu_guardrail_preflight.json")]), [py, script("Tools/npu/npu_guardrail_service.py"), "--input", str(guardrail_input), "--output", str(out / "npu_guardrail_report.json")]))
    if args.gpu_command:
        parallel.append((step_meta("gpu_command", "GPU", "Run optional heavy planner/generator command.", [str(out / "gpu_planner_output.json")]), shlex.split(args.gpu_command.format(brief=str(out / "ai_scene_brief.json"), output=str(out / "gpu_planner_output.json")))))
    if args.validate:
        serial.append((step_meta("validate_ai_artifacts", "CPU", "Validate generated artifacts and apply task-capsule guardrails.", [str(out / "ai_validation_report.json")]), [py, script("Tools/ai/validate_ai_artifacts.py"), "--repo-root", str(repo), "--artifact-dir", str(out), "--output", str(out / "ai_validation_report.json"), "--allow-errors"]))

    results: list[dict[str, Any]] = []
    for meta, cmd in serial:
        res = run(cmd, repo, args.dry_run)
        res.update(meta)
        results.append(res)
        if res["returncode"] and not args.continue_on_error:
            break
    if parallel and all(r["returncode"] == 0 for r in results):
        with ThreadPoolExecutor(max_workers=len(parallel)) as pool:
            futs = {pool.submit(run, cmd, repo, args.dry_run): meta for meta, cmd in parallel}
            for fut in as_completed(futs):
                res = fut.result()
                res.update(futs[fut])
                results.append(res)
    report = {"schema_version": 4, "generated_at": datetime.now(timezone.utc).isoformat(), "repo_root": str(repo), "output_dir": str(out), "dry_run": args.dry_run, "passed": pf["passed"] and all(r["returncode"] == 0 for r in results), "preflight": pf, "step_count": len(results), "lanes": {"CPU": [r["name"] for r in results if r.get("lane") == "CPU"], "NPU": [r["name"] for r in results if r.get("lane") == "NPU"], "GPU": [r["name"] for r in results if r.get("lane") == "GPU"]}, "smart_context": {"enabled": args.smart_context, "task": args.smart_task, "packet": str(out / "smart_context" / f"{track_slug}_smart_context_packet.json") if args.smart_context else None}, "steps": results, "post_run_expected_outputs": []}
    report["post_run_expected_outputs"] = planned_outputs(repo, out, args)
    if not args.dry_run:
        (out / "ai_pipeline_run_report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    elif args.write_dry_run_report:
        (out / "ai_pipeline_dry_run_report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
