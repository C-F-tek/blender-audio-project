#!/usr/bin/env python3
"""Build runtime tool usage telemetry from full-toolbox GPU/NPU reports.

Report-only utility. It reads orchestrator, GPU, GPU/NPU sync and runtime broker
reports, then writes a compact committable JSON/MD summary under
docs/LOCAL_VALIDATION_EVIDENCE. It never executes providers or tools.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    from tools.ai.code_patch_plan_common import now_iso, read_json_object, repo_rel
    from tools.ai.runtime_tool_telemetry_normalization import (
        normalize_tool_entry,
        status_quality,
    )
    from tools.validation.report_utils import (
        resolve_output_path,
        write_json_report,
        write_text_report,
    )
except ImportError:
    repo_root_for_import = Path(__file__).resolve().parents[2]
    if str(repo_root_for_import) not in sys.path:
        sys.path.insert(0, str(repo_root_for_import))
    from tools.ai.code_patch_plan_common import now_iso, read_json_object, repo_rel  # type: ignore
    from tools.ai.runtime_tool_telemetry_normalization import (  # type: ignore
        normalize_tool_entry,
        status_quality,
    )
    from tools.validation.report_utils import (  # type: ignore
        resolve_output_path,
        write_json_report,
        write_text_report,
    )

DEFAULT_OUTPUT = "docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_usage_telemetry.json"
DEFAULT_MARKDOWN = "docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_usage_telemetry.md"
MAX_SNIPPET_CHARS = 1200


def safe_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}

def safe_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []

def safe_int(value: Any, default: int = 0) -> int:
    if isinstance(value, bool):
        return default
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(value)
    if isinstance(value, str):
        try:
            return int(value)
        except ValueError:
            return default
    return default

def safe_float(value: Any, default: float = 0.0) -> float:
    if isinstance(value, bool):
        return default
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        try:
            return float(value.replace(",", "."))
        except ValueError:
            return default
    return default

def split_path_values(value: Any) -> list[str]:
    if value is None:
        return []
    raw_items = value if isinstance(value, list) else [value]
    out: list[str] = []
    for item in raw_items:
        for part in str(item).split(","):
            normalized = part.strip().strip("'\"")
            if normalized:
                out.append(normalized)
    return out

def compact_text(value: Any, max_chars: int = MAX_SNIPPET_CHARS) -> str:
    if value is None:
        return ""
    if isinstance(value, (dict, list)):
        text = json.dumps(value, ensure_ascii=False, sort_keys=True)
    else:
        text = str(value)
    text = text.replace("\x00", "").strip()
    return text[:max_chars] + ("...[truncated]" if len(text) > max_chars else "")

def parse_iso(value: Any) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(str(value))
    except ValueError:
        return None

def elapsed_from_timestamps(started: Any, finished: Any) -> float:
    start_dt = parse_iso(started)
    finish_dt = parse_iso(finished)
    if not start_dt or not finish_dt:
        return 0.0
    return round(max(0.0, (finish_dt - start_dt).total_seconds()), 3)

def read_optional_json(repo_root: Path, value: str) -> tuple[dict[str, Any], list[str], str]:
    if not value:
        return {}, [], ""
    path = resolve_output_path(repo_root, value)
    rel = repo_rel(repo_root, path)
    if not path.exists():
        return {}, [f"optional input missing: {rel}"], rel
    data, errors = read_json_object(path, missing_is_error=True)
    return data, errors, rel

def maybe_read_broker_report(repo_root: Path, value: Any) -> dict[str, Any]:
    if not value:
        return {}
    path = resolve_output_path(repo_root, str(value))
    if not path.exists():
        return {}
    data, errors = read_json_object(path, missing_is_error=False)
    if errors:
        return {}
    return data

def summarize_result_output(result: dict[str, Any]) -> dict[str, Any]:
    output_paths: list[str] = []
    for key in (
        "output",
        "output_file",
        "report_output",
        "markdown_output",
        "csv_written",
        "broker_output",
        "broker_markdown",
        "request_file",
        "path",
        "artifact",
    ):
        value = result.get(key)
        if isinstance(value, str) and value and value not in output_paths:
            output_paths.append(value)
    nested_output = result.get("output") if isinstance(result.get("output"), dict) else {}
    for key, value in nested_output.items():
        if isinstance(value, str) and value and value not in output_paths:
            output_paths.append(value)
    return {
        "passed": result.get("passed"),
        "returncode": result.get("returncode"),
        "ok": result.get("ok"),
        "kind": result.get("kind"),
        "output_paths": output_paths[:12],
        "stdout_tail": compact_text(result.get("stdout_tail"), 600),
        "stderr_tail": compact_text(result.get("stderr_tail"), 600),
        "error": compact_text(result.get("error"), 600),
        "summary": compact_text(
            result.get("summary") or result.get("message") or result.get("result"), 600
        ),
    }
