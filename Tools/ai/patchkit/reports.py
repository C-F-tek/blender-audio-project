#!/usr/bin/env python3
"""Report helpers for controlled patch bundles."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from Tools.ai._shared.report_markdown import append_errors_and_warnings, report_header


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = dict(data)
    payload.setdefault("generated_at", datetime.now().isoformat(timespec="seconds"))
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def render_markdown(report: dict[str, Any]) -> str:
    lines = report_header(
        "Patchkit Bundle Report",
        [
            ("Passed", report.get("passed")),
            ("Bundle", report.get("bundle")),
            ("Operation count", report.get("operation_count")),
            ("Changed count", report.get("changed_count")),
        ],
    )
    lines.extend(["", "## Operations", "", "| Operation | Target | Changed | Reason |", "|---|---|---:|---|"])
    for item in report.get("results") or []:
        lines.append(
            f"| `{item.get('operation')}` | `{item.get('target')}` | `{item.get('changed')}` | {str(item.get('reason', '')).replace('|', '/')} |"
        )
    append_errors_and_warnings(lines, report)
    return "\n".join(lines) + "\n"


def write_markdown(path: Path, report: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(report), encoding="utf-8")
