"""CLI parser for the AI artifact pipeline."""
from __future__ import annotations

import argparse


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
