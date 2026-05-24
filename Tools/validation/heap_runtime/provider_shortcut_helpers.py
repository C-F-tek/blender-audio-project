"""Helpers for provider shortcut validation fixtures."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ia_carmine._shared.file_backed_transport import write_text_evidence_fields


def response_fields(repo_root: Path, name: str, text: str) -> dict[str, Any]:
    return write_text_evidence_fields(
        repo_root,
        repo_root / "output" / "validation" / "provider_shortcut_negative_smoke_artifacts",
        prefix="response_text",
        name=name,
        text=text,
        kind="provider_shortcut_negative_smoke_response_text",
        producer="provider_shortcut_negative_smoke",
        suffix=".md",
    )


def tool_report(lane: str, output: str) -> dict[str, Any]:
    return {
        "lane": lane,
        "output": output,
        "revision": 0,
        "response_text": f"{lane} sidecar text",
        "tool_calls": [{"id": f"{lane}_generic", "tool": "generic_write", "args": {}}],
    }


def write_json_file(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
