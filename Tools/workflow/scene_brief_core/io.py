"""IO helpers for scene director brief/chat."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from .config import QUESTION_FIELDS

def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def append_scene_runtime_event(event: str, payload: dict) -> None:
    try:
        root = Path(__file__).resolve().parents[3]
        path = root / "output" / "workflow_logs" / "scene_director_runtime_events.jsonl"
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as handle:
            handle.write(
                json.dumps(
                    {"time": now_iso(), "event": event, "payload": payload}, ensure_ascii=False
                )
                + "\n"
            )
    except Exception:
        pass


def default_scene_preferences() -> dict[str, str]:
    return {field: default for field, _label, _question, default in QUESTION_FIELDS}


def compact_text(value: object, limit: int = 900) -> str:
    text = " ".join(str(value or "").split())
    if len(text) <= limit:
        return text
    return text[: max(0, limit - 3)].rstrip() + "..."


def trim_jsonable(value: object, limit: int = 1200) -> object:
    if isinstance(value, dict):
        return {str(k): trim_jsonable(v, max(240, limit // 2)) for k, v in list(value.items())[:24]}
    if isinstance(value, list):
        return [trim_jsonable(item, max(240, limit // 2)) for item in value[:16]]
    if isinstance(value, str):
        return compact_text(value, limit)
    return value
