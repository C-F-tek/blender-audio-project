"""Shared primitives for AI pipeline report contract validation."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

PIPELINE_SCHEMA_VERSION = 6
KNOWN_LANES = {"CPU", "NPU", "GPU", "IO", "VALIDATION"}

BASE_PIPELINE_REPORT_FIELDS = {
    "schema_version",
    "generated_at",
    "repo_root",
    "output_dir",
    "dry_run",
    "passed",
    "preflight",
    "step_count",
    "summary",
    "schedule",
    "steps",
}

EXTENDED_PIPELINE_REPORT_FIELDS = {
    "lanes",
    "wave_entrypoint_review",
    "smart_context",
    "agent_state_packet",
    "guardrail_remediation_loop",
    "post_run_expected_outputs",
}


def is_non_empty_string(value: Any) -> bool:
    """Return True when value is a non-empty string after trimming whitespace."""
    return isinstance(value, str) and bool(value.strip())


def is_int(value: Any) -> bool:
    """Return True for integers while excluding booleans."""
    return isinstance(value, int) and not isinstance(value, bool)


def is_non_negative_int(value: Any) -> bool:
    """Return True for non-negative integers while excluding booleans."""
    return is_int(value) and value >= 0


def is_number(value: Any) -> bool:
    """Return True for numeric values while excluding booleans."""
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def is_non_negative_number(value: Any) -> bool:
    """Return True for non-negative numeric values while excluding booleans."""
    return is_number(value) and value >= 0


def add_error(errors: list[str], path: str, message: str) -> None:
    """Append a path-qualified validation error."""
    errors.append(f"{path}: {message}")


def add_warning(warnings: list[str], path: str, message: str) -> None:
    """Append a path-qualified validation warning."""
    warnings.append(f"{path}: {message}")


def load_json_object(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    """Load a JSON object with tolerant UTF-8 BOM handling."""
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except FileNotFoundError:
        return None, f"not found: {path}"
    except json.JSONDecodeError as exc:
        return None, f"invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}"
    except OSError as exc:
        return None, f"read error: {exc}"
    if not isinstance(data, dict):
        return None, f"expected JSON object, got {type(data).__name__}"
    return data, None
