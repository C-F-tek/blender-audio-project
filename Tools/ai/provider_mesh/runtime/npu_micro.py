#!/usr/bin/env python3
"""NPU micro/deferred support helper functions.

This phase extracts the NPU micro lane path, context and command builders while
leaving orchestration, deferral policy, broker execution and final harvesting in
run_agent_gpu_npu_parallel_orchestrator.py.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from Tools.ai.provider_mesh.runtime.python_runtime import resolve_child_python


def resolve_path(repo_root: Path, value: str | Path) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = repo_root / path
    return path.resolve()


def collect_runtime_tool_context_reports(
    args: argparse.Namespace, repo_root: Path, round_id: int
) -> list[Path]:
    if not getattr(args, "enable_runtime_tool_broker", False):
        return []
    base = resolve_path(repo_root, args.runtime_tool_output_dir)
    candidates = [
        base / "round_000" / "round_000_runtime_tool_broker.json",
        base / f"round_{round_id:03d}" / f"round_{round_id:03d}_runtime_tool_broker.json",
    ]
    reports: list[Path] = []
    seen: set[str] = set()
    for candidate in candidates:
        key = str(candidate.resolve(strict=False))
        if key in seen or not candidate.exists():
            continue
        seen.add(key)
        reports.append(candidate)
    return reports


def npu_micro_support_output_path(args: argparse.Namespace, repo_root: Path, round_id: int) -> Path:
    support_dir = resolve_path(repo_root, args.npu_micro_support_dir)
    support_dir.mkdir(parents=True, exist_ok=True)
    return support_dir / f"round_{round_id:03d}_npu_micro_support.json"


def npu_micro_context_reports(
    args: argparse.Namespace, repo_root: Path, round_id: int
) -> list[Path]:
    reports = collect_runtime_tool_context_reports(args, repo_root, round_id)
    snapshot_value = str(getattr(args, "runtime_heap_snapshot", "") or "")
    if snapshot_value:
        snapshot = resolve_path(repo_root, snapshot_value)
        if snapshot.exists():
            reports.append(snapshot)
    seen: set[str] = set()
    unique: list[Path] = []
    for report in reports:
        key = str(report.resolve(strict=False))
        if key in seen:
            continue
        seen.add(key)
        unique.append(report)
    return unique


def build_npu_micro_support_command(
    args: argparse.Namespace,
    repo_root: Path,
    source_report: Path,
    output_json: Path,
    round_id: int,
) -> list[str]:
    command = [
        resolve_child_python(),
        "Tools/ai/provider_mesh/npu_gpu_deep_review_auditor/cli.py",
        "--repo-root",
        ".",
        "--gpu-review",
        str(source_report),
        "--run-npu",
        "--context-output",
        str(output_json.with_name(output_json.stem + "_context.md")),
        "--npu-output",
        str(output_json.with_name(output_json.stem + "_npu.md")),
        "--npu-notes-output",
        str(output_json.with_name(output_json.stem + "_npu_notes.md")),
        "--npu-metadata-output",
        str(output_json.with_name(output_json.stem + "_metadata.json")),
        "--output",
        str(output_json),
        "--markdown-output",
        str(output_json.with_suffix(".md")),
        "--timeout-seconds",
        str(args.npu_micro_support_timeout_seconds),
        "--max-context-chars",
        str(args.npu_micro_support_max_context_chars),
        "--max-prompt-chars",
        str(args.npu_micro_support_max_prompt_chars),
        "--max-new-tokens",
        str(args.npu_micro_support_max_new_tokens),
        "--max-runtime-tool-context-chars",
        str(args.npu_micro_support_max_runtime_tool_context_chars),
        "--max-npu-tool-requests",
        str(args.npu_micro_support_max_tool_requests),
    ]
    for context_report in npu_micro_context_reports(args, repo_root, round_id):
        command.extend(["--runtime-tool-context-report", str(context_report)])
    if args.npu_python:
        command.extend(["--npu-python", args.npu_python])
    return command
