#!/usr/bin/env python3
"""Runtime heap helpers for provider mesh orchestration.

Extracted from run_agent_gpu_npu_parallel_orchestrator.py to keep the
orchestrator focused on scheduling while preserving report-only behavior.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

try:
    from Tools.ai.provider_runtime_heap import ProviderRuntimeHeap
except ImportError:
    repo_root_for_import = Path(__file__).resolve().parents[3]
    if str(repo_root_for_import) not in sys.path:
        sys.path.insert(0, str(repo_root_for_import))
    from Tools.ai.provider_runtime_heap import ProviderRuntimeHeap  # type: ignore


def append_runtime_heap_event(
    *,
    args: argparse.Namespace,
    repo_root: Path,
    warnings: list[str],
    source: str,
    event_type: str,
    payload: dict[str, Any],
    round_id: int | None = None,
    target: str | None = None,
    correlation_id: str | None = None,
) -> None:
    if not getattr(args, "runtime_heap_stamp", ""):
        return
    try:
        heap = ProviderRuntimeHeap.from_args(
            repo_root,
            args.runtime_heap_stamp,
            getattr(args, "runtime_heap_events", ""),
            getattr(args, "runtime_heap_snapshot", ""),
            getattr(args, "runtime_heap_markdown", ""),
        )
        heap.append_event(
            source=source,
            target=target,
            event_type=event_type,
            round_id=round_id,
            correlation_id=correlation_id,
            payload=payload,
        )
    except Exception as exc:  # noqa: BLE001 - heap telemetry must not block provider orchestration.
        warnings.append(f"runtime heap append failed for {source}:{event_type}: {type(exc).__name__}: {exc}")


def write_runtime_heap_snapshot(*, args: argparse.Namespace, repo_root: Path, warnings: list[str]) -> dict[str, Any]:
    if not getattr(args, "runtime_heap_stamp", ""):
        return {}
    try:
        heap = ProviderRuntimeHeap.from_args(
            repo_root,
            args.runtime_heap_stamp,
            getattr(args, "runtime_heap_events", ""),
            getattr(args, "runtime_heap_snapshot", ""),
            getattr(args, "runtime_heap_markdown", ""),
        )
        return heap.write_snapshot()
    except Exception as exc:  # noqa: BLE001 - heap telemetry must not block provider orchestration.
        warnings.append(f"runtime heap snapshot failed: {type(exc).__name__}: {exc}")
        return {}
