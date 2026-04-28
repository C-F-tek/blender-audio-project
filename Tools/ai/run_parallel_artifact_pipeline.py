#!/usr/bin/env python3
"""Safe additive orchestrator for the AI artifact pipeline.

Schema v6 adds first-wave WAV entrypoint review. The pipeline can now review the
scripts that generate the earliest WAV-derived artifacts and feed their notes,
attention flags, and remediation requests into future guardrail decisions.
"""
from __future__ import annotations

import argparse
import json
import os
import platform
import re
import shlex
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

EXPECTED_WAVE_REVIEW_ARTIFACTS = ["wave_entrypoint_review.json"]
EXPECTED_MUSIC_ARTIFACTS = ["track_summary.json", "music_segments.json", "audio_event_map.json", "ai_scene_brief.json", "ai_resource_budget.json"]
EXPECTED_CHUNK_ARTIFACTS = ["indexAI/code_chunks/semantic_code_chunks.json", "indexAI/code_chunks/semantic_code_chunks_manifest.json"]
EXPECTED_SMART_CONTEXT_ARTIFACTS = ["smart_context/{track_slug}_smart_context_packet.json", "smart_context/{track_slug}_smart_context_manifest.json", "smart_context/{track_slug}_smart_context_packet.md"]


def slugify(value: str) -> str:
    value = re.sub(r"[^a-z0-9]+", "_", value.strip().lower())
    return re.sub(r"_+", "_", value).strip("_") or "track"


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


def load_json_if_exists(path: Path) -> Any | None:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8", errors="replace"))
    except Exception:
        return None


def file_meta(path: Path, root: Path) -> dict[str, Any]:
    exists = path.exists()
    meta: dict[str, Any] = {"path": rel(path, root), "exists": exists}
    if exists and path.is_file():
        stat = path.stat()
        meta.update({"size_bytes": stat.st_size, "modified_time": datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat()})
    return meta


def planned_outputs(repo: Path, out: Path, args: argparse.Namespace) -> list[dict[str, Any]]:
    outputs: list[Path] = []
    track_slug = slugify(args.track_stem)
    if args.review_wave_entrypoints:
        outputs += [out / item for item in EXPECTED_WAVE_REVIEW_ARTIFACTS]
    if args.build_chunks:
        outputs += [repo / item for item in EXPECTED_CHUNK_ARTIFACTS]
    if args.build_music_summary:
        outputs += [out / item for item in EXPECTED_MUSIC_ARTIFACTS]
    if args.smart_context:
        outputs += [out / item.format(track_slug=track_slug) for item in EXPECTED_SMART_CONTEXT_ARTIFACTS]
    if args.use_npu:
        outputs.append(out / "npu_artifact_review.json")
    if args.npu_guardrail:
        outputs += [out / "npu_guardrail_report.json", out / "npu_guardrail_report.md", out / "npu_guardrail_preflight.json", out / "npu_guardrail_action_queue.json"]
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
    if args.npu_guardrail and not args.smart_context:
        warnings.append("NPU guardrail works best with smart context; falling back to artifact directory review.")
    if args.guardrail_auto_remediate and not args.npu_guardrail:
        warnings.append("Guardrail auto-remediation was requested but npu_guardrail is disabled.")
    if args.review_wave_entrypoints and not (repo / "analyze_wav.py").exists():
        warnings.append("Wave entrypoint review enabled but analyze_wav.py was not found at repository root.")
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
    for item in ["analyze_wav.py", "build_track_summary.py", "docs/LOCAL_WORKSTATION_TARGET.md", "indexAI/task_capsules/blender_51_compat.json", "indexAI/task_capsules/resource_budget.json"]:
        input_files.append(file_meta(repo / item, repo))
    return {"passed": not errors, "errors": errors, "warnings": warnings, "input_files": input_files, "planned_outputs": planned_outputs(repo, out, args), "python_runtime": python_runtime(), "workstation_context": workstation_context(repo), "environment": {"cwd": os.getcwd(), "dry_run": args.dry_run}}


def step_meta(name: str, lane: str, purpose: str, expected_outputs: list[str], pass_index: int = 0) -> dict[str, Any]:
    return {"name": name, "lane": lane, "purpose": purpose, "expected_outputs": expected_outputs, "pass_index": pass_index}


def build_step_commands(repo: Path, out: Path, args: argparse.Namespace) -> dict[str, list[str]]:
    py = sys.executable
    track_slug = slugify(args.track_stem)

    def script(path: str) -> str:
        return str((repo / path).resolve())

    commands: dict[str, list[str]] = {}
    if args.review_wave_entrypoints:
        commands["review_wave_entrypoints"] = [py, script("Tools/ai/review_wave_entrypoints.py"), "--repo-root", str(repo), "--output", str(out / "wave_entrypoint_review.json")]
    if args.build_chunks:
        commands["build_semantic_code_chunks"] = [py, script("Tools/npu/build_semantic_code_chunks.py"), "--repo-root", str(repo)]
    if args.build_music_summary:
        commands["build_music_intermediates"] = [py, script("Tools/ai/build_music_intermediates.py"), "--analysis-json", str(Path(args.analysis_json).resolve()), "--output-dir", str(out)]
    if args.smart_context:
        commands["build_smart_ai_context"] = [py, script("Tools/workflow/smart_ai_context.py"), "--repo-root", str(repo), "--track-stem", args.track_stem, "--task", args.smart_task, "--output-dir", str(out / "smart_context"), "--max-packet-chars", str(args.smart_max_packet_chars), "--max-capsule-chars", str(args.smart_max_capsule_chars)]
    if args.use_npu:
        commands["npu_artifact_review"] = [py, script("Tools/npu/run_npu_artifact_reviewer.py"), "--input", str(out), "--output", str(out / "npu_artifact_review.json"), "--max-workers", str(args.npu_workers)]
    if args.npu_guardrail:
        guardrail_input = out / "smart_context" / f"{track_slug}_smart_context_packet.json" if args.smart_context else out
        commands["npu_guardrail"] = [py, script("Tools/npu/npu_guardrail_service.py"), "--input", str(guardrail_input), "--output", str(out / "npu_guardrail_report.json")]
    if args.validate:
        commands["validate_ai_artifacts"] = [py, script("Tools/ai/validate_ai_artifacts.py"), "--repo-root", str(repo), "--artifact-dir", str(out), "--output", str(out / "ai_validation_report.json"), "--allow-errors"]
    return commands


def guardrail_queue(out: Path) -> dict[str, Any]:
    payload = load_json_if_exists(out / "npu_guardrail_action_queue.json")
    if isinstance(payload, dict):
        return payload
    return {"schema_version": 1, "queue": []}


def auto_safe_requests(out: Path) -> list[dict[str, Any]]:
    queue = guardrail_queue(out).get("queue") or []
    return [item for item in queue if isinstance(item, dict) and item.get("auto_safe")]


def remediation_plan_from_requests(requests: list[dict[str, Any]]) -> dict[str, Any]:
    by_stage: dict[str, int] = {}
    by_type: dict[str, int] = {}
    for item in requests:
        stage = str(item.get("suggested_stage") or "unknown")
        action = str(item.get("action_type") or "unknown")
        by_stage[stage] = by_stage.get(stage, 0) + 1
        by_type[action] = by_type.get(action, 0) + 1
    return {"request_count": len(requests), "by_stage": by_stage, "by_type": by_type, "requests": requests}


def remedial_commands(repo: Path, out: Path, args: argparse.Namespace, requests: list[dict[str, Any]]) -> list[tuple[dict[str, Any], list[str]]]:
    commands = build_step_commands(repo, out, args)
    stages = {str(item.get("suggested_stage") or "") for item in requests}
    todo: list[tuple[dict[str, Any], list[str]]] = []

    if "wave_entrypoint_review" in stages and "review_wave_entrypoints" in commands:
        todo.append((step_meta("remediate_review_wave_entrypoints", "CPU", "Repeat first-wave script review requested by guardrail.", EXPECTED_WAVE_REVIEW_ARTIFACTS), commands["review_wave_entrypoints"]))
    if "enrich_intermediates" in stages and "build_music_intermediates" in commands:
        todo.append((step_meta("remediate_build_music_intermediates", "CPU", "Auto-safe enrichment pass requested by NPU guardrail.", EXPECTED_MUSIC_ARTIFACTS), commands["build_music_intermediates"]))
    if "compact_context_generation" in stages and "build_smart_ai_context" in commands:
        todo.append((step_meta("remediate_build_smart_ai_context_compact", "CPU", "Auto-safe compact context rebuild requested by NPU guardrail.", EXPECTED_SMART_CONTEXT_ARTIFACTS), commands["build_smart_ai_context"]))
    if "smart_context_generation" in stages and "build_smart_ai_context" in commands:
        todo.append((step_meta("remediate_build_smart_ai_context", "CPU", "Auto-safe smart context rebuild requested by NPU guardrail.", EXPECTED_SMART_CONTEXT_ARTIFACTS), commands["build_smart_ai_context"]))
    if "guardrail_second_pass" in stages and "npu_guardrail" in commands:
        todo.append((step_meta("remediate_npu_guardrail_second_pass", "NPU", "Second guardrail pass requested by NPU guardrail.", [str(out / "npu_guardrail_report.json")]), commands["npu_guardrail"]))

    if todo and "npu_guardrail" in commands and all(meta["name"] != "remediate_npu_guardrail_second_pass" for meta, _ in todo):
        todo.append((step_meta("remediate_npu_guardrail_verify", "NPU", "Verify artifact state after auto-safe remediation passes.", [str(out / "npu_guardrail_report.json")]), commands["npu_guardrail"]))

    return todo


def execute_remediation_loop(repo: Path, out: Path, args: argparse.Namespace, results: list[dict[str, Any]]) -> dict[str, Any]:
    if not args.guardrail_auto_remediate or not args.npu_guardrail:
        return {"enabled": False, "reason": "disabled", "passes": []}

    passes: list[dict[str, Any]] = []
    seen_signatures: set[str] = set()
    for pass_index in range(1, max(1, args.guardrail_max_passes) + 1):
        requests = auto_safe_requests(out)
        plan = remediation_plan_from_requests(requests)
        signature = json.dumps(plan.get("by_stage", {}), sort_keys=True)
        if not requests:
            passes.append({"pass_index": pass_index, "status": "no_auto_safe_requests", "plan": plan, "steps": []})
            break
        if signature in seen_signatures:
            passes.append({"pass_index": pass_index, "status": "repeated_plan_stopped", "plan": plan, "steps": []})
            break
        seen_signatures.add(signature)

        todo = remedial_commands(repo, out, args, requests)
        if not todo:
            passes.append({"pass_index": pass_index, "status": "no_supported_remediation_commands", "plan": plan, "steps": []})
            break

        step_results = []
        for meta, cmd in todo:
            meta["pass_index"] = pass_index
            res = run(cmd, repo, args.dry_run)
            res.update(meta)
            step_results.append(res)
            results.append(res)
            if res["returncode"] and not args.continue_on_error:
                break
        passes.append({"pass_index": pass_index, "status": "executed", "plan": plan, "steps": step_results})
        if any(item["returncode"] for item in step_results) and not args.continue_on_error:
            break
    return {"enabled": True, "max_passes": args.guardrail_max_passes, "passes": passes}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("--analysis-json")
    ap.add_argument("--track-stem", default="track")
    ap.add_argument("--output-dir", default="output/ai_pipeline")
    ap.add_argument("--review-wave-entrypoints", dest="review_wave_entrypoints", action="store_true", default=True)
    ap.add_argument("--no-review-wave-entrypoints", dest="review_wave_entrypoints", action="store_false")
    ap.add_argument("--build-chunks", action="store_true")
    ap.add_argument("--build-music-summary", action="store_true")
    ap.add_argument("--smart-context", dest="smart_context", action="store_true", default=True)
    ap.add_argument("--no-smart-context", dest="smart_context", action="store_false")
    ap.add_argument("--smart-task", default="Scene Director Blender Python generation audio-reactive full keyframe preservation asset-aware composition")
    ap.add_argument("--smart-max-packet-chars", type=int, default=22000)
    ap.add_argument("--smart-max-capsule-chars", type=int, default=3200)
    ap.add_argument("--use-npu", action="store_true")
    ap.add_argument("--npu-guardrail", dest="npu_guardrail", action="store_true", default=True)
    ap.add_argument("--no-npu-guardrail", dest="npu_guardrail", action="store_false")
    ap.add_argument("--npu-workers", type=int, default=4)
    ap.add_argument("--guardrail-auto-remediate", dest="guardrail_auto_remediate", action="store_true", default=True)
    ap.add_argument("--no-guardrail-auto-remediate", dest="guardrail_auto_remediate", action="store_false")
    ap.add_argument("--guardrail-max-passes", type=int, default=2)
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
        report = {"schema_version": 6, "generated_at": datetime.now(timezone.utc).isoformat(), "repo_root": str(repo), "output_dir": str(out), "dry_run": args.dry_run, "passed": False, "preflight": pf, "step_count": 0, "steps": []}
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return 2

    commands = build_step_commands(repo, out, args)
    serial: list[tuple[dict[str, Any], list[str]]] = []
    parallel: list[tuple[dict[str, Any], list[str]]] = []
    track_slug = slugify(args.track_stem)

    if "review_wave_entrypoints" in commands:
        serial.append((step_meta("review_wave_entrypoints", "CPU", "Review first-wave WAV artifact scripts and emit future guardrail flags.", EXPECTED_WAVE_REVIEW_ARTIFACTS), commands["review_wave_entrypoints"]))
    if "build_semantic_code_chunks" in commands:
        serial.append((step_meta("build_semantic_code_chunks", "CPU", "Build symbol-aware repository context for AI retrieval.", EXPECTED_CHUNK_ARTIFACTS), commands["build_semantic_code_chunks"]))
    if "build_music_intermediates" in commands:
        serial.append((step_meta("build_music_intermediates", "CPU", "Build compact AI-friendly music artifacts from the full analysis JSON.", EXPECTED_MUSIC_ARTIFACTS), commands["build_music_intermediates"]))
    if "build_smart_ai_context" in commands:
        serial.append((step_meta("build_smart_ai_context", "CPU", "Build hierarchical capsules and ranked smart context packet for central AI.", [item.format(track_slug=track_slug) for item in EXPECTED_SMART_CONTEXT_ARTIFACTS]), commands["build_smart_ai_context"]))
    if "npu_artifact_review" in commands:
        parallel.append((step_meta("npu_artifact_review", "NPU", "Review compact artifacts for schema, size, blocked patterns, and obvious risks.", [str(out / "npu_artifact_review.json")]), commands["npu_artifact_review"]))
    if "npu_guardrail" in commands:
        parallel.append((step_meta("npu_guardrail", "NPU", "Always-on guardrail/preflight plus action queue for corrections and enrichment.", [str(out / "npu_guardrail_report.json"), str(out / "npu_guardrail_action_queue.json")]), commands["npu_guardrail"]))
    if args.gpu_command:
        parallel.append((step_meta("gpu_command", "GPU", "Run optional heavy planner/generator command.", [str(out / "gpu_planner_output.json")]), shlex.split(args.gpu_command.format(brief=str(out / "ai_scene_brief.json"), output=str(out / "gpu_planner_output.json")))))
    if "validate_ai_artifacts" in commands:
        serial.append((step_meta("validate_ai_artifacts", "CPU", "Validate generated artifacts and apply task-capsule guardrails.", [str(out / "ai_validation_report.json")]), commands["validate_ai_artifacts"]))

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

    remediation_loop = execute_remediation_loop(repo, out, args, results)

    report = {
        "schema_version": 6,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "repo_root": str(repo),
        "output_dir": str(out),
        "dry_run": args.dry_run,
        "passed": pf["passed"] and all(r["returncode"] == 0 for r in results),
        "preflight": pf,
        "step_count": len(results),
        "lanes": {"CPU": [r["name"] for r in results if r.get("lane") == "CPU"], "NPU": [r["name"] for r in results if r.get("lane") == "NPU"], "GPU": [r["name"] for r in results if r.get("lane") == "GPU"]},
        "wave_entrypoint_review": {"enabled": args.review_wave_entrypoints, "report": str(out / "wave_entrypoint_review.json") if args.review_wave_entrypoints else None},
        "smart_context": {"enabled": args.smart_context, "task": args.smart_task, "packet": str(out / "smart_context" / f"{track_slug}_smart_context_packet.json") if args.smart_context else None},
        "guardrail_remediation_loop": remediation_loop,
        "steps": results,
        "post_run_expected_outputs": planned_outputs(repo, out, args),
    }
    if not args.dry_run:
        (out / "ai_pipeline_run_report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    elif args.write_dry_run_report:
        (out / "ai_pipeline_dry_run_report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
