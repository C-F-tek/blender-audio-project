#!/usr/bin/env python3
"""GPU0/OpenVINO peer support helper functions.

This module contains pure path/command/scheduling helpers extracted from the
provider mesh orchestrator. Launching, harvesting and telemetry remain in the
orchestrator for this phase.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from tools.ai.provider_mesh_runtime.python_runtime import resolve_child_python


def resolve_path(repo_root: Path, value: str | Path) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = repo_root / path
    return path.resolve()


def gpu0_peer_support_output_path(args: argparse.Namespace, repo_root: Path, round_id: int) -> Path:
    support_dir = resolve_path(repo_root, args.gpu0_peer_support_dir)
    support_dir.mkdir(parents=True, exist_ok=True)
    return support_dir / f"round_{round_id:03d}_gpu0_peer_support.json"


def build_gpu0_peer_support_command(
    args: argparse.Namespace, support_json: Path, round_id: int
) -> list[str]:
    return [
        resolve_child_python(),
        "tools/ai/build_openvino_gpu0_workload_report.py",
        "--repo-root",
        ".",
        "--output",
        str(support_json),
        "--markdown-output",
        str(support_json.with_suffix(".md")),
        "--iterations",
        str(args.gpu0_peer_support_iterations),
        "--min-seconds",
        str(args.gpu0_peer_support_min_seconds),
        "--role",
        f"peer_support_round_{round_id:03d}",
        "--production-support",
    ]


def should_launch_gpu0_peer_support(round_id: int, every_rounds: int) -> bool:
    return round_id == 1 or round_id % max(1, every_rounds) == 0
