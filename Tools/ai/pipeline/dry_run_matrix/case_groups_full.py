"""Full-surface pipeline dry-run matrix cases."""

from __future__ import annotations

from pathlib import Path

from .common import MatrixCase, _planned_gpu_placeholder_command


def full_surface_cases(sample_analysis_json: Path) -> list[MatrixCase]:
    return [
        MatrixCase(
            name="validation_chunks_music",
            args=(
                "--dry-run",
                "--write-dry-run-report",
                "--validate",
                "--build-chunks",
                "--build-music-summary",
                "--analysis-json",
                str(sample_analysis_json),
            ),
            purpose="Verify combined validation, chunk and music-summary planning.",
        ),
        MatrixCase(
            name="validation_music_no_smart_context",
            args=(
                "--dry-run",
                "--write-dry-run-report",
                "--validate",
                "--build-music-summary",
                "--analysis-json",
                str(sample_analysis_json),
                "--no-smart-context",
            ),
            purpose="Verify validation and music-summary planning with smart context disabled.",
        ),
        MatrixCase(
            name="full_planning_surface",
            args=(
                "--dry-run",
                "--write-dry-run-report",
                "--build-chunks",
                "--build-music-summary",
                "--analysis-json",
                str(sample_analysis_json),
                "--validate",
                "--use-npu",
                "--npu-workers",
                "4",
                "--gpu-command",
                _planned_gpu_placeholder_command(),
            ),
            purpose="Verify the widest planned CPU/NPU/GPU dry-run surface without executing heavy workloads.",
        ),
        MatrixCase(
            name="full_planning_no_auto_remediation",
            args=(
                "--dry-run",
                "--write-dry-run-report",
                "--build-chunks",
                "--build-music-summary",
                "--analysis-json",
                str(sample_analysis_json),
                "--validate",
                "--use-npu",
                "--npu-workers",
                "4",
                "--gpu-command",
                _planned_gpu_placeholder_command(),
                "--no-guardrail-auto-remediate",
            ),
            purpose="Verify widest planned dry-run surface with guardrail auto-remediation disabled.",
        ),
        MatrixCase(
            name="full_planning_no_smart_context",
            args=(
                "--dry-run",
                "--write-dry-run-report",
                "--build-chunks",
                "--build-music-summary",
                "--analysis-json",
                str(sample_analysis_json),
                "--validate",
                "--use-npu",
                "--npu-workers",
                "4",
                "--gpu-command",
                _planned_gpu_placeholder_command(),
                "--no-smart-context",
            ),
            purpose="Verify widest planned dry-run surface with smart context disabled.",
        )
    ]
