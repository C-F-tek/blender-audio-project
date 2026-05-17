#!/usr/bin/env python3
"""Compact runtime heap event-pointer extraction helpers."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

POINTER_PROTOCOL = "runtime_heap_event_log_v1"
POINTER_KEYS = (
    "output",
    "provider_report",
    "broker_output",
    "report",
    "source_report",
    "checkpoint",
    "markdown",
    "path",
    "json",
    "snapshot",
)


def safe_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def append_pointer_ref(refs: list[str], value: Any) -> None:
    if isinstance(value, str) and value.strip() and value not in refs:
        refs.append(value)


def payload_pointer_refs(payload: dict[str, Any]) -> list[str]:
    refs: list[str] = []
    for key in POINTER_KEYS:
        value = payload.get(key)
        if isinstance(value, list):
            for item in value:
                append_pointer_ref(refs, item)
        else:
            append_pointer_ref(refs, value)
    details = payload.get("details")
    if isinstance(details, dict):
        for key in POINTER_KEYS:
            append_pointer_ref(refs, details.get(key))
    return refs


def resolve_event_log(repo_root: Path, snapshot: dict[str, Any]) -> Path | None:
    event_log = str(snapshot.get("event_log") or "").strip()
    if not event_log:
        return None
    path = Path(event_log)
    return path if path.is_absolute() else repo_root / path


def load_event_pointers(
    repo_root: Path, snapshot: dict[str, Any], limit: int = 6
) -> list[dict[str, Any]]:
    path = resolve_event_log(repo_root, snapshot)
    if path is None:
        return []
    pointers: list[dict[str, Any]] = []
    try:
        lines = path.read_text(encoding="utf-8-sig").splitlines()
    except OSError:
        return []
    for line in reversed(lines):
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        payload = safe_dict(event.get("payload"))
        refs = payload_pointer_refs(payload)
        if not refs:
            continue
        pointers.append(
            {
                "lane": event.get("source") or event.get("target"),
                "event_type": event.get("event_type"),
                "correlation_id": event.get("correlation_id"),
                "status": payload.get("status") or payload.get("state"),
                "message": payload.get("message") or payload.get("summary"),
                "artifact_refs": refs[:4],
            }
        )
        if len(pointers) >= limit:
            break
    return list(reversed(pointers))


def source_pointer_bundle(repo_root: Path | None, snapshot: dict[str, Any]) -> dict[str, Any]:
    return {
        "event_log": snapshot.get("event_log"),
        "snapshot_kind": snapshot.get("kind"),
        "tool_pointer_protocol": POINTER_PROTOCOL,
        "evidence_pointers": load_event_pointers(repo_root, snapshot) if repo_root else [],
    }
