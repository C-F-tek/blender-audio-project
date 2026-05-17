"""Common model and helpers for the pipeline dry-run matrix."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class MatrixCase:
    name: str
    args: tuple[str, ...]
    purpose: str


def default_matrix_workers() -> int:
    """Return a conservative default for matrix-level parallel dry-run execution."""
    cpu_count = os.cpu_count() or 1
    return max(1, min(8, cpu_count))

def _planned_gpu_command() -> str:
    """Return a harmless command string used only for dry-run GPU planning."""
    return "python -c \"print('gpu planner dry run only')\""

def _planned_gpu_placeholder_command() -> str:
    """Return a harmless placeholder-aware GPU command used only for dry-run planning."""
    return "python -c \"import sys; print('gpu placeholder dry run only'); print(sys.argv[1]); print(sys.argv[2])\" {brief} {output}"

def ensure_sample_analysis_json(repo_root: Path) -> Path:
    """Create a tiny deterministic analysis JSON so music-summary dry-runs pass preflight."""
    sample = repo_root / "output" / "ai_pipeline" / "dry_run_matrix_inputs" / "sample_analysis.json"
    sample.parent.mkdir(parents=True, exist_ok=True)
    if not sample.exists():
        payload = {
            "schema_version": 1,
            "source": "dry_run_matrix_sample",
            "duration_sec": 1.0,
            "sample_rate": 44100,
            "bpm": 120.0,
            "segments": [
                {
                    "start_sec": 0.0,
                    "end_sec": 1.0,
                    "label": "dry_run_sample",
                    "energy": 0.5,
                }
            ],
            "notes": [
                "Synthetic sample used only to satisfy preflight during dry-run matrix planning.",
                "Do not treat this as real audio analysis output.",
            ],
        }
        sample.write_text(
            json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
    return sample

def repeat_cases(cases: tuple[MatrixCase, ...], repeat_count: int) -> tuple[MatrixCase, ...]:
    """Repeat matrix cases for stress testing while keeping output directories unique."""
    repeat_count = max(1, repeat_count)
    if repeat_count == 1:
        return cases
    repeated: list[MatrixCase] = []
    for round_index in range(1, repeat_count + 1):
        suffix = f"_r{round_index:02d}"
        for case in cases:
            repeated.append(
                MatrixCase(
                    name=f"{case.name}{suffix}",
                    args=case.args,
                    purpose=f"Repeat {round_index}/{repeat_count}: {case.purpose}",
                )
            )
    return tuple(repeated)
