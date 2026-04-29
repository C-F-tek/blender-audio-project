"""Schema-v6 report builders for the AI artifact pipeline."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from .artifact_contracts import planned_outputs, slugify


SCHEMA_VERSION = 6


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
