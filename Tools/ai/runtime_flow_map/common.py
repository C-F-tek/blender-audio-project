"""Shared helpers for runtime flow-map evidence."""

from __future__ import annotations

import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DEFAULT_OUTPUT_DIR = "docs/LOCAL_VALIDATION_EVIDENCE"
DEFAULT_ENTRYPOINT = "tools/ai/run_agent_gpu_npu_parallel_orchestrator.py"
STAMP_RE = re.compile(r"\d{8}-\d{6}")
CANONICAL_COMPONENTS = {
    "orchestrator": {"type": "process", "label": "orchestrator"},
    "gpu_planner": {"type": "provider", "label": "GPU1 / Ollama planner"},
    "gpu0_peer": {"type": "provider", "label": "GPU0 / OpenVINO peer"},
    "npu_peer": {"type": "provider", "label": "NPU / OpenVINO micro-peer"},
    "broker": {"type": "broker", "label": "runtime tool broker"},
    "heap": {"type": "exchange_memory", "label": "runtime heap / exchange"},
    "decision_loop": {"type": "decision", "label": "decision loop"},
    "recommendations": {"type": "artifact", "label": "recommendations"},
    "patch_plan": {"type": "artifact", "label": "patch plan"},
    "validation": {"type": "validator", "label": "validation"},
    "evidence_bundle": {"type": "artifact", "label": "evidence bundle"},
}

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")

def repo_rel(path: Path, repo_root: Path) -> str:
    try:
        return path.resolve(strict=False).relative_to(repo_root.resolve(strict=False)).as_posix()
    except ValueError:
        return str(path)

def unique(items: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            out.append(item)
    return out

def infer_stamp(values: list[str]) -> str:
    for value in values:
        matches = STAMP_RE.findall(str(value or ""))
        if matches:
            return matches[-1]
    return datetime.now().strftime("%Y%m%d-%H%M%S")

def safe_int(value: Any, default: int = 0) -> int:
    try:
        if isinstance(value, bool):
            return default
        return int(value)
    except (TypeError, ValueError):
        return default

def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []

def as_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}

def read_json(path: Path) -> tuple[dict[str, Any], str]:
    if not path.exists():
        return {}, "missing"
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:  # noqa: BLE001 - evidence summary should capture parse failures.
        return {}, f"{type(exc).__name__}: {exc}"
    if not isinstance(data, dict):
        return {}, "json root is not an object"
    return data, ""

def component_from_report(path: str, data: dict[str, Any]) -> str:
    lower_path = path.lower().replace("\\", "/")
    kind = str(data.get("kind") or "").lower()
    if "runtime_heap" in kind or "ai_runtime_heap" in lower_path or "heap" in lower_path:
        return "heap"
    if "orchestrator" in kind or "orchestrator" in lower_path:
        return "orchestrator"
    if "parallel_gpu" in lower_path or "gpu_deep" in lower_path or "gpu_planner" in lower_path:
        return "gpu_planner"
    if "gpu0" in lower_path or "openvino_gpu0" in kind:
        return "gpu0_peer"
    if "npu" in lower_path or "npu" in kind:
        return "npu_peer"
    if "broker" in kind or "broker" in lower_path or "runtime_tool" in lower_path:
        return "broker"
    if "decision" in kind or "decision_loop" in lower_path:
        return "decision_loop"
    if "patch_plan" in kind or "patch_plan" in lower_path or "patch_specs" in lower_path:
        return "patch_plan"
    if (
        "recommend" in kind
        or "proposal" in kind
        or "recommend" in lower_path
        or "proposal" in lower_path
    ):
        return "recommendations"
    if "bundle" in kind or "evidence_bundle" in lower_path:
        return "evidence_bundle"
    if "validation" in lower_path or kind.startswith("check_"):
        return "validation"
    return "validation"

def add_node(
    nodes: dict[str, dict[str, Any]],
    node_id: str,
    node_type: str,
    label: str,
    **extra: Any,
) -> None:
    item = nodes.setdefault("node:" + node_id, {"id": node_id, "type": node_type, "label": label})
    item.update({key: value for key, value in extra.items() if value not in (None, "", [])})

def add_edge(
    edges: dict[tuple[str, str, str], dict[str, Any]],
    source: str,
    target: str,
    kind: str,
    count: int = 1,
    **extra: Any,
) -> None:
    key = (source, target, kind)
    item = edges.setdefault(key, {"from": source, "to": target, "kind": kind, "count": 0})
    item["count"] = safe_int(item.get("count")) + max(1, count)
    for extra_key, value in extra.items():
        if value not in (None, "", []):
            item[extra_key] = value

def append_event(
    events: list[dict[str, Any]],
    *,
    component: str,
    action: str,
    status: str = "observed",
    span: str = "",
    duration_ms: int | None = None,
    **extra: Any,
) -> None:
    event: dict[str, Any] = {
        "ts": now_iso(),
        "span": span,
        "component": component,
        "action": action,
        "status": status,
    }
    if duration_ms is not None:
        event["duration_ms"] = duration_ms
    event.update({key: value for key, value in extra.items() if value not in (None, "", [])})
    events.append(event)

def compact_report_summary(path: str, data: dict[str, Any], parse_error: str) -> dict[str, Any]:
    return {
        "path": path,
        "exists": parse_error != "missing",
        "json_ok": not parse_error,
        "parse_error": parse_error,
        "kind": data.get("kind"),
        "passed": data.get("passed"),
        "provider_execution_performed": data.get("provider_execution_performed"),
        "patch_application_performed": data.get("patch_application_performed"),
        "source_writes_performed": data.get("source_writes_performed"),
        "errors": as_list(data.get("errors"))[:10],
        "warnings": as_list(data.get("warnings"))[:10],
    }
