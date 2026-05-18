"""Shared helpers for patch-notes quality smoke."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

def now_stamp() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def write_fixture(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def render_markdown(report: dict[str, Any]) -> str:
    lines = ["# Patch Notes Quality Product Smoke", ""]
    lines.append(f"- Passed: `{report['passed']}`")
    lines.append(f"- Positive passed: `{report['positive']['passed']}`")
    lines.append(f"- Positive quality gate: `{report['positive']['quality_gate_passed']}`")
    lines.append(f"- Negative passed: `{report['negative']['passed']}`")
    lines.append(f"- Negative quality gate: `{report['negative']['quality_gate_passed']}`")
    if report["errors"]:
        lines += ["", "## Errors", ""]
        lines.extend(f"- {item}" for item in report["errors"])
    return "\n".join(lines) + "\n"
