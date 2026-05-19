from __future__ import annotations

import argparse
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class OrchestratorRunState:
    args: argparse.Namespace
    repo_root: Path
    start: float
    checkpoint_dir: Path
    gpu_output: Path
    gpu_markdown: Path
    orchestrator_runtime_tool_bootstrap: dict[str, Any]
    mesh_bootstrap_seed: Path
    gpu_command: list[str]
    gpu_process: subprocess.Popen[str]
    launched_rounds: set[int] = field(default_factory=set)
    active_audits: dict[int, subprocess.Popen[str]] = field(default_factory=dict)
    audit_records: list[dict[str, Any]] = field(default_factory=list)
    launched_gpu0_support_rounds: set[int] = field(default_factory=set)
    active_gpu0_supports: dict[int, subprocess.Popen[str]] = field(default_factory=dict)
    gpu0_support_records: list[dict[str, Any]] = field(default_factory=list)
    launched_npu_micro_rounds: set[int] = field(default_factory=set)
    active_npu_micro_supports: dict[int, subprocess.Popen[str]] = field(default_factory=dict)
    npu_micro_support_records: list[dict[str, Any]] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    gpu_stdout: str = ""
    gpu_stderr: str = ""
    gpu_report: dict[str, Any] = field(default_factory=dict)
    gpu_runtime_tool_brokers: list[dict[str, Any]] = field(default_factory=list)
