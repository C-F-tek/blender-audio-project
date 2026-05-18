"""Shared provider runtime blackboard helpers."""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from .state import RuntimeState, normalize_status
from Tools.validation._shared.report_utils import resolve_output_path, write_json_report, write_text_report

LANES = (
    "gpu1",
    "gpu0",
    "npu",
    "broker",
    "context_memory",
    "deterministic",
    "telemetry",
    "orchestrator",
)
EVENT_TYPES = (
    "user_request",
    "provider_state",
    "task_state",
    "fact",
    "need",
    "tool_catalog_request",
    "tool_catalog_response",
    "evidence_request",
    "evidence_response",
    "lane_evidence",
    "broker_request",
    "broker_result",
    "claim",
    "validation_signal",
    "decision",
    "recommendation",
    "candidate_operation",
    "patch_plan",
    "patch_plan_signal",
    "validation",
    "product_signal",
    "telemetry_signal",
    "startup_task_file_context",
)
DEFAULT_EVENTS = "output/ai_runtime_heap/{stamp}/events.jsonl"
DEFAULT_SNAPSHOT = "output/ai_runtime_heap/{stamp}/snapshot.json"
DEFAULT_MARKDOWN = "output/ai_runtime_heap/{stamp}/snapshot.md"

def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")

def safe_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}

def safe_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []

def safe_int(value: Any, default: int = 0) -> int:
    try:
        if isinstance(value, bool):
            return default
        return int(value)
    except (TypeError, ValueError):
        return default

def repo_rel(repo_root: Path, path: Path) -> str:
    try:
        return path.resolve(strict=False).relative_to(repo_root.resolve(strict=False)).as_posix()
    except ValueError:
        return str(path)

def normalize_lane(value: str) -> str:
    lane = str(value or "").strip().lower()
    if lane not in LANES:
        raise ValueError(f"unsupported provider lane: {value!r}; allowed={list(LANES)}")
    return lane

def normalize_event_type(value: str) -> str:
    event_type = str(value or "").strip().lower()
    if event_type not in EVENT_TYPES:
        raise ValueError(
            f"unsupported runtime heap event type: {value!r}; allowed={list(EVENT_TYPES)}"
        )
    return event_type

def compact_payload(value: Any, max_chars: int = 8000) -> Any:
    text = json.dumps(value, ensure_ascii=False, default=str)
    if len(text) <= max_chars:
        return value
    return {
        "truncated": True,
        "max_chars": max_chars,
        "preview": text[:max_chars],
    }

def load_tool_specs() -> dict[str, Any]:
    """Load the existing broker allowlist lazily to avoid import cycles."""
    try:
        from Tools.ai.runtime_tool.broker.registry import (
            TOOL_SPECS,  # pylint: disable=import-outside-toplevel
        )
    except ImportError:
        repo_root_for_import = Path(__file__).resolve().parents[2]
        if str(repo_root_for_import) not in sys.path:
            sys.path.insert(0, str(repo_root_for_import))
        from Tools.ai.runtime_tool.broker.registry import (
            TOOL_SPECS,  # type: ignore  # pylint: disable=import-outside-toplevel
        )
    return TOOL_SPECS

def tool_catalog_snapshot() -> dict[str, Any]:
    specs = load_tool_specs()
    tools: list[dict[str, Any]] = []
    for name in sorted(specs):
        spec = specs[name]
        tools.append(
            {
                "tool": spec.name,
                "description": spec.description,
                "allowed_args": list(spec.allowed_args),
                "broker_builder": getattr(spec.builder, "__name__", ""),
                "execution_rule": "request_only; execution must be mediated by agent_runtime_tool_broker",
            }
        )
    return {
        "schema_version": 1,
        "kind": "semantic_tool_catalog_snapshot",
        "generated_at": now_iso(),
        "tool_count": len(tools),
        "tools": tools,
        "guardrails": {
            "free_shell_exposed": False,
            "broker_allowlist_required": True,
            "provider_direct_tool_execution_allowed": False,
        },
    }

class RuntimeHeapPaths:
    events: Path
    snapshot: Path
    markdown: Path
