"""Basic pipeline dry-run matrix cases."""

from __future__ import annotations

from pathlib import Path

from .common import MatrixCase


def basic_cases(sample_analysis_json: Path) -> list[MatrixCase]:
    return [
        MatrixCase(
            name="base",
            args=("--dry-run", "--write-dry-run-report"),
            purpose="Default safe dry-run with guardrail and smart context enabled.",
        ),
        MatrixCase(
            name="no_auto_remediation",
            args=(
                "--dry-run",
                "--write-dry-run-report",
                "--no-guardrail-auto-remediate",
            ),
            purpose="Verify pipeline without automatic guardrail remediation passes.",
        ),
        MatrixCase(
            name="no_npu_guardrail",
            args=("--dry-run", "--write-dry-run-report", "--no-npu-guardrail"),
            purpose="Verify dry-run planning when NPU guardrail is disabled without executing NPU workloads.",
        ),
        MatrixCase(
            name="no_smart_context",
            args=("--dry-run", "--write-dry-run-report", "--no-smart-context"),
            purpose="Verify planning when smart context is disabled and guardrail input falls back to the output directory.",
        ),
        MatrixCase(
            name="no_wave_review",
            args=(
                "--dry-run",
                "--write-dry-run-report",
                "--no-review-wave-entrypoints",
            ),
            purpose="Verify planning when first-wave WAV entrypoint review is disabled.",
        ),
        MatrixCase(
            name="minimal_no_context_no_guardrail",
            args=(
                "--dry-run",
                "--write-dry-run-report",
                "--no-review-wave-entrypoints",
                "--no-smart-context",
                "--no-npu-guardrail",
            ),
            purpose="Verify the smallest no-op planning shape remains reportable.",
        ),
        MatrixCase(
            name="with_validation",
            args=("--dry-run", "--write-dry-run-report", "--validate"),
            purpose="Verify validate_ai_artifacts stage planning.",
        ),
        MatrixCase(
            name="validation_no_guardrail",
            args=(
                "--dry-run",
                "--write-dry-run-report",
                "--validate",
                "--no-npu-guardrail",
            ),
            purpose="Verify validation planning when NPU guardrail is disabled.",
        ),
        MatrixCase(
            name="with_chunks",
            args=("--dry-run", "--write-dry-run-report", "--build-chunks"),
            purpose="Verify semantic code chunk stage planning.",
        ),
        MatrixCase(
            name="chunks_no_smart_context",
            args=(
                "--dry-run",
                "--write-dry-run-report",
                "--build-chunks",
                "--no-smart-context",
            ),
            purpose="Verify chunk planning without smart context.",
        ),
        MatrixCase(
            name="with_music_summary_planned",
            args=(
                "--dry-run",
                "--write-dry-run-report",
                "--build-music-summary",
                "--analysis-json",
                str(sample_analysis_json),
            ),
            purpose="Verify music intermediate stage planning using a deterministic synthetic analysis JSON.",
        ),
        MatrixCase(
            name="music_no_smart_context",
            args=(
                "--dry-run",
                "--write-dry-run-report",
                "--build-music-summary",
                "--analysis-json",
                str(sample_analysis_json),
                "--no-smart-context",
            ),
            purpose="Verify music intermediate planning when smart context is disabled.",
        ),
        MatrixCase(
            name="smart_context_tiny_budget",
            args=(
                "--dry-run",
                "--write-dry-run-report",
                "--smart-max-packet-chars",
                "512",
                "--smart-max-capsule-chars",
                "128",
            ),
            purpose="Verify smart-context planning with a tiny packet/capsule budget.",
        ),
        MatrixCase(
            name="smart_context_small_budget",
            args=(
                "--dry-run",
                "--write-dry-run-report",
                "--smart-max-packet-chars",
                "2048",
                "--smart-max-capsule-chars",
                "512",
            ),
            purpose="Verify smart-context planning with a small packet/capsule budget.",
        ),
        MatrixCase(
            name="smart_context_large_budget",
            args=(
                "--dry-run",
                "--write-dry-run-report",
                "--smart-max-packet-chars",
                "64000",
                "--smart-max-capsule-chars",
                "8192",
            ),
            purpose="Verify smart-context planning with a larger packet/capsule budget.",
        ),
        MatrixCase(
            name="custom_track_stem_ascii",
            args=(
                "--dry-run",
                "--write-dry-run-report",
                "--track-stem",
                "dry_run_track_120bpm",
            ),
            purpose="Verify planning with a custom ASCII track stem.",
        ),
        MatrixCase(
            name="custom_track_stem_spaces",
            args=(
                "--dry-run",
                "--write-dry-run-report",
                "--track-stem",
                "Dry Run Track With Spaces",
            ),
            purpose="Verify slug/path planning with spaces in track stem.",
        ),
        MatrixCase(
            name="custom_track_stem_symbols",
            args=(
                "--dry-run",
                "--write-dry-run-report",
                "--track-stem",
                "Dry_Run-Track_120 BPM!",
            ),
            purpose="Verify slug/path planning with punctuation in track stem.",
        ),
        MatrixCase(
            name="custom_smart_task_short",
            args=(
                "--dry-run",
                "--write-dry-run-report",
                "--smart-task",
                "dry-run short planning task",
            ),
            purpose="Verify planning with a short custom smart-context task.",
        ),
        MatrixCase(
            name="custom_smart_task_multiclause",
            args=(
                "--dry-run",
                "--write-dry-run-report",
                "--smart-task",
                "dry-run plan: preserve audio timing; review generated paths; keep runtime packages unchanged",
            ),
            purpose="Verify planning with a multi-clause custom smart-context task.",
        )
    ]
