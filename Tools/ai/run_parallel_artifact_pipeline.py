#!/usr/bin/env python3
"""Safe additive orchestrator for the AI artifact pipeline.

The heavy implementation details are intentionally split into reusable modules
under ``Tools/ai/pipeline/`` so each area can be validated and dry-run tested
independently.
"""
from __future__ import annotations

import argparse
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

try:
    from pipeline.artifact_contracts import planned_outputs, slugify
    from pipeline.compat import run_pipeline_step
    from pipeline.models import PipelineStep
    from pipeline.preflight import preflight
    from pipeline.remediation import execute_remediation_loop
    from pipeline.steps import build_parallel_steps, build_serial_steps, build_step_commands
except ImportError:  # Allows package-style imports during external checks.
    from Tools.ai.pipeline.artifact_contracts import planned_outputs, slugify  # type: ignore
    from Tools.ai.pipeline.compat import run_pipeline_step  # type: ignore
    from Tools.ai.pipeline.models import PipelineStep  # type: ignore
    from Tools.ai.pipeline.preflight import preflight  # type: ignore
    from Tools.ai.pipeline.remediation import execute_remediation_loop  # type: ignore
    from Tools.ai.pipeline.steps import build_parallel_steps, build_serial_steps, build_step_commands  # type: ignore


SCHEMA_VERSION = 6


def build_parser() -> argparse.ArgumentParser:
    """Build CLI parser for the AI artifact pipeline."""
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
    return ap


def empty_failed_report(repo: Path, out: Path, dry_run: bool, pf: dict) -> dict:
    """Return a schema-compatible report when preflight fails."""
    return {
        "schema_version": SCHEMA_VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "repo_root": str(repo),
        "output_dir": str(out),
        "dry_run": dry_run,
        "passed": False,
        "preflight": pf,
        "step_count": 0,
        "steps": [],
    }


def run_serial_steps(steps: list[PipelineStep], repo: Path, dry_run: bool, continue_on_error: bool) -> list[dict]:
    """Run ordered pipeline steps and stop on failure unless configured otherwise."""
    results: list[dict] = []
    for step in steps:
        result = run_pipeline_step(step, repo, dry_run)
        results.append(result)
        if result["returncode"] and not continue_on_error:
            break
    return results


def run_parallel_steps(steps: list[PipelineStep], repo: Path, dry_run: bool) -> list[dict]:
    """Run independent pipeline steps concurrently."""
    if not steps:
        return []
    results: list[dict] = []
    with ThreadPoolExecutor(max_workers=len(steps)) as pool:
        futures = {pool.submit(run_pipeline_step, step, repo, dry_run): step for step in steps}
        for future in as_completed(futures):
            results.append(future.result())
    return results


def build_report(repo: Path, out: Path, args: argparse.Namespace, pf: dict, results: list[dict], remediation_loop: dict) -> dict:
    """Build the schema-v6 pipeline report."""
    track_slug = slugify(args.track_stem)
    return {
        "schema_version": SCHEMA_VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "repo_root": str(repo),
        "output_dir": str(out),
        "dry_run": args.dry_run,
        "passed": pf["passed"] and all(item["returncode"] == 0 for item in results),
        "preflight": pf,
        "step_count": len(results),
        "lanes": {
            "CPU": [item["name"] for item in results if item.get("lane") == "CPU"],
            "NPU": [item["name"] for item in results if item.get("lane") == "NPU"],
            "GPU": [item["name"] for item in results if item.get("lane") == "GPU"],
        },
        "wave_entrypoint_review": {
            "enabled": args.review_wave_entrypoints,
            "report": str(out / "wave_entrypoint_review.json") if args.review_wave_entrypoints else None,
        },
        "smart_context": {
            "enabled": args.smart_context,
            "task": args.smart_task,
            "packet": str(out / "smart_context" / f"{track_slug}_smart_context_packet.json") if args.smart_context else None,
        },
        "guardrail_remediation_loop": remediation_loop,
        "steps": results,
        "post_run_expected_outputs": planned_outputs(repo, out, args),
    }


def write_report_if_requested(out: Path, args: argparse.Namespace, report: dict) -> None:
    """Write final or dry-run report when requested by the invocation mode."""
    if not args.dry_run:
        target = out / "ai_pipeline_run_report.json"
    elif args.write_dry_run_report:
        target = out / "ai_pipeline_dry_run_report.json"
    else:
        return
    target.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    args = build_parser().parse_args()

    repo = Path(args.repo_root).resolve()
    out = Path(args.output_dir).resolve()
    out.mkdir(parents=True, exist_ok=True)

    pf = preflight(repo, out, args)
    if not pf["passed"] and not args.continue_on_error:
        report = empty_failed_report(repo, out, args.dry_run, pf)
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return 2

    commands = build_step_commands(repo, out, args)
    track_slug = slugify(args.track_stem)
    serial = build_serial_steps(commands, track_slug)
    parallel = build_parallel_steps(commands, out, args)

    results = run_serial_steps(serial, repo, args.dry_run, args.continue_on_error)
    if parallel and all(item["returncode"] == 0 for item in results):
        results.extend(run_parallel_steps(parallel, repo, args.dry_run))

    remediation_loop = execute_remediation_loop(repo, out, args, results)
    report = build_report(repo, out, args, pf, results, remediation_loop)
    write_report_if_requested(out, args, report)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
