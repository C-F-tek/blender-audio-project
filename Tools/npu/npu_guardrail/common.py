"""Common IO and scanning helpers for NPU guardrails."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .config import EVENT_LOG, INTERMEDIATE_ENRICHMENT_FIELDS

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def append_event(event: str, payload: dict[str, Any]) -> None:
    try:
        EVENT_LOG.parent.mkdir(parents=True, exist_ok=True)
        with EVENT_LOG.open("a", encoding="utf-8") as handle:
            handle.write(
                json.dumps(
                    {"time": now_iso(), "event": event, "payload": payload}, ensure_ascii=False
                )
                + "\n"
            )
    except Exception:
        pass


def read_json(path: Path) -> tuple[Any, list[str]]:
    try:
        return json.loads(path.read_text(encoding="utf-8", errors="replace")), []
    except Exception as exc:
        return {"read_error": str(exc), "path": str(path)}, [f"json_read_error:{exc}"]


def targets(path: Path, recursive: bool = False) -> list[Path]:
    if path.is_file():
        return [path]
    if path.is_dir():
        pattern = "**/*.json" if recursive else "*.json"
        return sorted(p for p in path.glob(pattern) if p.is_file())
    return []


def pattern_findings(text: str, patterns: dict[str, str], prefix: str) -> list[str]:
    findings: list[str] = []
    for pattern, reason in patterns.items():
        if pattern in text:
            findings.append(f"{prefix}:{pattern}: {reason}")
    return findings


def idea_scan(
    text: str, ideas: list[str], prefix: str, required: bool
) -> tuple[list[str], list[str]]:
    warnings: list[str] = []
    positives: list[str] = []
    for idea in ideas:
        if re.search(re.escape(idea), text, re.IGNORECASE):
            positives.append(f"{prefix}_present:{idea}")
        elif required:
            warnings.append(f"{prefix}_missing:{idea}")
    return warnings, positives


def artifact_type(path: Path, payload: Any) -> str:
    if isinstance(payload, dict):
        if payload.get("kind"):
            return str(payload.get("kind"))
        if payload.get("selected_capsules") or payload.get("capsule_manifest"):
            return "smart_context_packet"
        if payload.get("segments"):
            return "music_segments"
        if payload.get("peak_events") or payload.get("beats_sec"):
            return "audio_event_map"
        if payload.get("creative_intent") or payload.get("technical_intent"):
            return "scene_brief"
        if path.name == "track_summary.json":
            return "track_summary"
    return path.stem


def is_pythonish(path: Path, payload: Any, text: str) -> bool:
    if path.suffix == ".py":
        return True
    lowered = text.lower()
    return any(token in lowered for token in ("python", "bpy.", "script", "traceback", ".py"))
