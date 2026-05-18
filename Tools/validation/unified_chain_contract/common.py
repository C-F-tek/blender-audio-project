"""Common helpers for unified chain contract validation."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from Tools.ai.heap_exchange.io import load_jsonl

try:
    from Tools.validation._shared.report_utils import resolve_output_path, write_json_report, write_text_report
except ImportError:
    from Tools.validation._shared.report_utils import (  # type: ignore
        resolve_output_path,
        write_json_report,
        write_text_report,
    )

DEFAULT_MODE_NAME = "agent_state_chunks_context_pack_contract_evidence_full_validation_json_md_official_patch_specs_provider_python_smoke"
CONCRETE_OPERATION_NAMES = {
    "replace_once",
    "append_once",
    "insert_after_once",
    "insert_before_once",
    "write_file",
}
EXCHANGE_EVENT_HINTS = (
    "proposal",
    "decision",
    "patch",
    "patch_spec",
    "recommendation",
    "summary",
    "tool_result",
)

TOOL_EVIDENCE_HINTS = (
    "tool",
    "capability",
    "capabilities",
    "tool_usage",
    "runtime_tool",
    "telemetry",
)

REQUIRED_HEAP_PEERS = {
    "gpu1": ("gpu1", "primary", "advisory", "planner"),
    "gpu0": ("gpu0", "companion", "tool", "openvino", "worker"),
    "npu": (
        "npu",
        "microoperation",
        "micro-operation",
        "micro_ops",
        "micro-ops",
        "efficiency",
        "peer",
    ),
}

SHARED_MEMORY_HINTS = (
    "shared_memory",
    "memory",
    "bundle",
    "ai_to_ai",
    "heap",
    "exchange",
    "context",
)

def repo_path(repo_root: Path, value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else repo_root / path

def load_json(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    if not path.exists():
        return None, "missing"
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:  # noqa: BLE001 - report validator must not crash on bad evidence
        return None, f"{type(exc).__name__}: {exc}"
    if not isinstance(data, dict):
        return None, "json root is not an object"
    return data, None

def discover_first(repo_root: Path, patterns: list[str]) -> Path | None:
    for pattern in patterns:
        matches = sorted(
            repo_root.glob(pattern),
            key=lambda item: item.stat().st_mtime if item.exists() else 0,
            reverse=True,
        )
        if matches:
            return matches[0]
    return None

def discover_apply_report(repo_root: Path, stamp: str, mode_name: str) -> Path | None:
    patterns = [
        f"output/validation/patch_suggestion_bundle_apply_{mode_name}_{stamp}.json",
        f"output/validation/generated_patch_specs_review_pr_apply*{stamp}*.json",
        f"output/validation/*generated_patch_specs*{stamp}*.json",
        f"output/validation/*patch_suggestion_bundle_apply*{stamp}*.json",
    ]
    for pattern in patterns:
        for path in sorted(
            repo_root.glob(pattern), key=lambda item: item.stat().st_mtime, reverse=True
        ):
            data, error = load_json(path)
            if error:
                continue
            if data and data.get("kind") == "patch_suggestion_bundle_apply":
                return path
    return None

def discover_observer_dir(repo_root: Path, stamp: str) -> Path | None:
    candidates = sorted(
        repo_root.glob(f"output/local_ai_runs/*{stamp}*_observer"),
        key=lambda item: item.stat().st_mtime if item.exists() else 0,
        reverse=True,
    )
    return candidates[0] if candidates else None

def add_edge(
    edges: list[dict[str, Any]],
    *,
    name: str,
    producer: str,
    consumer: str,
    expected: str,
    actual: str,
    passed: bool,
    action: str,
    artifacts: list[str] | None = None,
) -> None:
    edges.append(
        {
            "edge": name,
            "producer": producer,
            "consumer": consumer,
            "expected": expected,
            "actual": actual,
            "passed": passed,
            "action": action,
            "artifacts": artifacts or [],
        }
    )

def rel(repo_root: Path, path: Path | None) -> str:
    if path is None:
        return ""
    try:
        return path.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()
