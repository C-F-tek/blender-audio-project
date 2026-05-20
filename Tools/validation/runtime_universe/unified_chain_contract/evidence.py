"""Evidence classifiers for unified chain contract validation."""

from __future__ import annotations

import json
from typing import Any

from .common import (
    CONCRETE_OPERATION_NAMES,
    EXCHANGE_EVENT_HINTS,
    REQUIRED_HEAP_PEERS,
    SHARED_MEMORY_HINTS,
    TOOL_EVIDENCE_HINTS,
)

def event_kind(event: dict[str, Any]) -> str:
    for key in ("kind", "type", "event", "phase", "status"):
        value = event.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip().lower()
    return ""

def has_productive_exchange_event(events: list[dict[str, Any]]) -> bool:
    for event in events:
        kind = event_kind(event)
        text = json.dumps(event, ensure_ascii=False).lower()
        if any(hint in kind or hint in text for hint in EXCHANGE_EVENT_HINTS):
            return True
    return False

def has_tool_capability_evidence(report: dict[str, Any] | None) -> bool:
    if not report:
        return False
    if report.get("passed") is False:
        return False
    text = json.dumps(report, ensure_ascii=False).lower()
    explicit_count = 0
    for key in ("tool_count", "capability_count", "runtime_tool_count", "available_tool_count"):
        try:
            explicit_count = max(explicit_count, int(report.get(key) or 0))
        except (TypeError, ValueError):
            pass
    if explicit_count > 0:
        return True
    for key in ("tools", "capabilities", "tool_capabilities", "runtime_tools", "available_tools"):
        value = report.get(key)
        if isinstance(value, list) and value:
            return True
        if isinstance(value, dict) and value:
            return True
    return "tool" in text and any(hint in text for hint in TOOL_EVIDENCE_HINTS)

def peer_presence(report: dict[str, Any] | None, events: list[dict[str, Any]]) -> dict[str, bool]:
    text_parts: list[str] = []
    if report:
        text_parts.append(json.dumps(report, ensure_ascii=False).lower())
    if events:
        text_parts.append(json.dumps(events, ensure_ascii=False).lower())
    text = "\n".join(text_parts)

    found: dict[str, bool] = {}
    for peer, hints in REQUIRED_HEAP_PEERS.items():
        found[peer] = peer in text and any(hint in text for hint in hints)
    return found

def has_shared_memory_evidence(report: dict[str, Any] | None, events: list[dict[str, Any]]) -> bool:
    text_parts: list[str] = []
    if report:
        text_parts.append(json.dumps(report, ensure_ascii=False).lower())
    if events:
        text_parts.append(json.dumps(events, ensure_ascii=False).lower())
    text = "\n".join(text_parts)
    if not text:
        return False
    return any(hint in text for hint in SHARED_MEMORY_HINTS)

def has_closure_audit_evidence(report: dict[str, Any] | None) -> bool:
    if not report:
        return False
    if report.get("passed") is not True:
        return False
    text = json.dumps(report, ensure_ascii=False).lower()
    return (
        report.get("closure_state") == "ready_for_final_chain_contract"
        and "deterministic" in text
        and "audit" in text
        and "microoperation" in text
    )

def concrete_operation_count_from_apply(report: dict[str, Any]) -> int:
    count = int(report.get("operation_count") or 0)
    if count > 0:
        return count
    concrete = 0
    for item in report.get("results") or []:
        if not isinstance(item, dict):
            continue
        op = str(item.get("operation") or "").strip().lower()
        if op in CONCRETE_OPERATION_NAMES:
            concrete += 1
    return concrete
