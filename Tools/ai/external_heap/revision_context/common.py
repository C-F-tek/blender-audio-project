"""Shared constants and low-level helpers for heap revision context."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

REVISION_TASK_PREVIEW_CHARS = 1600
REJECTION_MARKER_PATTERNS = (
    ("placeholder/stub", re.compile(r"placeholder/stub", re.IGNORECASE)),
    ("similarity=1.000", re.compile(r"similarity\s*=\s*1\.000", re.IGNORECASE)),
    ("TODO", re.compile(r"(^|\n)\s*(#|//)?\s*TODO\s*[:(]", re.IGNORECASE)),
    ("pass", re.compile(r"(^|[^A-Za-z0-9_])pass([^A-Za-z0-9_]|$)", re.IGNORECASE)),
    ("path/to/artifact", re.compile(r"path/to/artifact", re.IGNORECASE)),
)

CANDIDATE_APPLICABILITY_PATTERNS = (
    (
        "invented_source_path",
        re.compile(
            r"(?:no verified source file references|unverified source file refs?|source refs non verificati|"
            r"invented_source_path|non-allowlisted source|invented/non-allowlisted source path refs)",
            re.IGNORECASE,
        ),
    ),
    ("unresolved_pointer_placeholder", re.compile(r"<id-or-empty>", re.IGNORECASE)),
    ("generic_patch_sketch", re.compile(r"\bCODE_OR_PATCH_SKETCH\b", re.IGNORECASE)),
    (
        "generic_missing_functionality",
        re.compile(r"implementa(?:re|zione)\s+(?:le\s+)?funzionalit", re.IGNORECASE),
    ),
    (
        "synthetic_stub_function",
        re.compile(
            r"def\s+[A-Za-z_][A-Za-z0-9_]*\s*\([^)]*\)\s*:"
            r"\s*(?:\n\s*#\s*Implementazione|\n\s*context_pack\s*=\s*\{)",
            re.IGNORECASE,
        ),
    ),
    (
        "comment_only_implementation",
        re.compile(r"^\s*#\s*Implementazione\b", re.IGNORECASE | re.MULTILINE),
    ),
    (
        "unverified_unit_test_path",
        re.compile(
            r"\bpytest\s+(?:\.\\)?Tests[/\\]unit[/\\]test_[A-Za-z0-9_./\\-]+\.py\b",
            re.IGNORECASE,
        ),
    ),
    (
        "run_script_as_validation_only",
        re.compile(r"\bpython\s+Tools[/\\]ai[/\\][A-Za-z0-9_./\\-]+\.py\b", re.IGNORECASE),
    ),
    ("bare_pass", re.compile(r"(^|[^A-Za-z0-9_])pass([^A-Za-z0-9_]|$)", re.IGNORECASE)),
    (
        "comment_only_function_stub",
        re.compile(
            r"comment_only_function_stub|def\s+[A-Za-z_][A-Za-z0-9_]*\([^)]*\):\s*(?:#.*\n\s*)*pass\b",
            re.IGNORECASE,
        ),
    ),
    (
        "unresolved_angle_bracket_token",
        re.compile(r"<(?:id-or-empty|[^>\n]*placeholder[^>\n]*)>", re.IGNORECASE),
    ),
    (
        "invalid_ps1_py_compile_validation",
        re.compile(r"py_compile\s+[^\n`]*\.ps1\b", re.IGNORECASE),
    ),
    (
        "generic_diff_without_file_context",
        re.compile(
            r"generic_diff_without_file_context|PATCH_SKETCH:\s*```diff\s*diff --git[^\n]*\n@@\s*\n\s*#",
            re.IGNORECASE | re.DOTALL,
        ),
    ),
)

def read_json(path_value: str) -> dict[str, Any]:
    if not path_value:
        return {}
    try:
        data = json.loads(Path(path_value).read_text(encoding="utf-8-sig"))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}

def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")

def normalize_bool(value: Any) -> bool:
    return value is True or str(value).strip().lower() == "true"

def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []

def compact_text(value: Any, limit: int) -> str:
    text = str(value or "")
    if limit > 0 and len(text) > limit:
        return text[:limit] + "\n...[truncated]"
    return text
