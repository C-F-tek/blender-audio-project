#!/usr/bin/env python3
"""Smoke-check reusable AI pipeline modules without running heavy workloads.

This validator imports the modular AI artifact pipeline, builds representative
steps and reports, and verifies that the thin entrypoint can be imported.
It does not execute NPU, GPU, Blender, FFmpeg or long-running artifact jobs.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from types import SimpleNamespace
from typing import Any


def import_pipeline_modules(repo_root: Path) -> dict[str, Any]:
    """Import pipeline modules after ensuring the repository root is importable."""
    import sys

    root_text = str(repo_root)
    if root_text not in sys.path:
        sys.path.insert(0, root_text)

    from Tools.ai.pipeline.artifact_contracts import planned_outputs, slugify
    from Tools.ai.pipeline.cli import build_parser
    from Tools.ai.pipeline.compat import pipeline_step, run_pipeline_step
    from Tools.ai.pipeline.models import PipelineLane, PipelineStep
    from Tools.ai.pipeline.orchestrator import run_parallel_steps, run_serial_steps
    from Tools.ai.pipeline.preflight import preflight
    from Tools.ai.pipeline.remediation import remediation_plan_from_requests, remedial_steps
    from Tools.ai.pipeline.schema_report import build_report, empty_failed_report
    from Tools.ai.pipeline.steps import build_parallel_steps, build_serial_steps, build_step_commands
    from Tools.ai.run_parallel_artifact_pipeline import main as entrypoint_main

    return {
        "planned_outputs": planned_outputs,
        "slugify": slugify,
        "build_parser": build_parser,
        "pipeline_step": pipeline_step,
        "run_pipeline_step": run_pipeline_step,
        "PipelineLane": PipelineLane,
        "PipelineStep": PipelineStep,
        "run_parallel_steps": run_parallel_steps,
        "run_serial_steps": run_serial_steps,
        "preflight": preflight,
        "remediation_plan_from_requests": remediation_plan_from_requests,
        "remedial_steps": remedial_steps,
        "build_report": build_report,
        "empty_failed_report": empty_failed_report,
        "build_parallel_steps": build_parallel_steps,
        "build_serial_steps": build_serial_steps,
        "build_step_commands": build_step_commands,
        "entrypoint_main": entrypoint_main,
    }


def make_args(repo_root: Path) -> SimpleNamespace:
    """Build a representative dry-run namespace without requiring input artifacts."""
    return SimpleNamespace(
        repo_root=str(repo_root),
        analysis_json=None,
        track_stem="Smoke Test Track",
        output_dir=str(repo_root / "output" / "ai_pipeline_smoke"),
        review_wave_entrypoints=True,
        build_chunks=False,
        build_music_summary=False,
        smart_context=True,
        smart_task="Smoke test task",
        smart_max_packet_chars=22000,
        smart_max_capsule_chars=3200,
        use_npu=False,
        npu_guardrail=True,
        npu_workers=4,
        guardrail_auto_remediate=True,
        guardrail_max_passes=2,
        gpu_command=None,
        validate=True,
        dry_run=True,
        write_dry_run_report=True,
        continue_on_error=False,
    )


def check_modules(repo_root: Path) -> dict[str, Any]:
    modules = import_pipeline_modules(repo_root)
    args = make_args(repo_root)
    out = Path(args.output_dir).resolve()
    out.mkdir(parents=True, exist_ok=True)

    parser = modules["build_parser"]()
    parsed = parser.parse_args(["--repo-root", str(repo_root), "--dry-run"])

    step = modules["pipeline_step"](
        "smoke_step",
        "CPU",
        "Smoke-check command runner integration.",
        ["output/ai_pipeline_smoke/smoke.json"],
        ["python", "--version"],
    )
    step_payload = step.to_dict()
    dry_result = modules["run_pipeline_step"](step, repo_root, True)

    commands = modules["build_step_commands"](repo_root, out, args)
    serial = modules["build_serial_steps"](commands, modules["slugify"](args.track_stem))
    parallel = modules["build_parallel_steps"](commands, out, args)
    pf = modules["preflight"](repo_root, out, args)
    plan = modules["remediation_plan_from_requests"](
        [
            {
                "suggested_stage": "smart_context_generation",
                "action_type": "rerun_stage",
                "auto_safe": True,
            }
        ]
    )
    remediation = modules["remedial_steps"](repo_root, out, args, plan["requests"], 1)
    report = modules["build_report"](repo_root, out, args, pf, [dry_result], {"enabled": False, "reason": "smoke", "passes": []})
    failed_report = modules["empty_failed_report"](repo_root, out, True, {"passed": False, "errors": ["smoke"], "warnings": []})
    planned = modules["planned_outputs"](repo_root, out, args)

    checks = {
        "parser_type": type(parser).__name__,
        "parsed_dry_run": bool(parsed.dry_run),
        "step_lane": step_payload["lane"],
        "dry_result_returncode": dry_result["returncode"],
        "dry_result_planned_only": dry_result["planned_only"],
        "command_count": len(commands),
        "serial_step_count": len(serial),
        "parallel_step_count": len(parallel),
        "preflight_passed": pf["passed"],
        "remediation_request_count": plan["request_count"],
        "remediation_step_count": len(remediation),
        "report_schema_version": report["schema_version"],
        "failed_report_schema_version": failed_report["schema_version"],
        "planned_output_count": len(planned),
        "entrypoint_imported": callable(modules["entrypoint_main"]),
    }

    errors: list[str] = []
    if checks["step_lane"] != "CPU":
        errors.append("pipeline_step did not preserve CPU lane")
    if checks["dry_result_returncode"] != 0 or not checks["dry_result_planned_only"]:
        errors.append("run_pipeline_step dry-run did not produce a planned successful result")
    if checks["serial_step_count"] < 1:
        errors.append("serial step builder produced no steps for smoke configuration")
    if checks["report_schema_version"] != 6:
        errors.append("build_report did not produce schema version 6")
    if not checks["entrypoint_imported"]:
        errors.append("artifact pipeline entrypoint was not importable")

    return {
        "schema_version": 1,
        "repo_root": str(repo_root),
        "passed": not errors,
        "errors": errors,
        "checks": checks,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output", help="Optional JSON report path.")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    report = check_modules(repo_root)
    text = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        output = Path(args.output).resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(text, encoding="utf-8")
    print(text, end="")
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
