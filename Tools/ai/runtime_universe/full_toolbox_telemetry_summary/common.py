"""Shared helpers for full-toolbox telemetry summaries."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

REPO_ROOT_FOR_IMPORT = Path(__file__).resolve().parents[4]
if str(REPO_ROOT_FOR_IMPORT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT_FOR_IMPORT))

from Tools.ai._shared.code_patch_plan_common import now_iso, read_json_object, repo_rel
from Tools.validation._shared.report_utils import (
    resolve_output_path,
    write_json_report,
    write_text_report,
)

DEFAULT_OUTPUT = "docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_run_telemetry_summary.json"
DEFAULT_MARKDOWN = "docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_run_telemetry_summary.md"

def read_optional_json(repo_root: Path, value: str) -> tuple[dict[str, Any], list[str], str]:
    if not value:
        return {}, [], ""
    path = resolve_output_path(repo_root, value)
    path_rel = repo_rel(repo_root, path)
    if not path.exists():
        return {}, [f"optional input missing: {path_rel}"], path_rel
    data, errors = read_json_object(path, missing_is_error=True)
    return data, errors, path_rel

def safe_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []

def safe_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}

def safe_int(value: Any, default: int = 0) -> int:
    if isinstance(value, bool):
        return default
    try:
        if value in (None, ""):
            return default
        return int(value)
    except (TypeError, ValueError):
        return default
