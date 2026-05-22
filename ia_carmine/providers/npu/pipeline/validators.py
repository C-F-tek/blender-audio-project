from __future__ import annotations

from typing import Any

from .artifact_paths import validate_generated_artifact_paths
from .config import DEFAULT_ALLOWED_ARTIFACT_PREFIXES

REQUIRED_IMPLEMENTATION_DRAFT_KEYS = (
    "implementation_kind",
    "safety",
    "reference_files",
    "proposed_files",
    "implementation_plan",
)


def validate_json_object(data: Any, *, label: str) -> dict[str, object]:
    """Validate that a parsed JSON value is an object."""

    return {
        "ok": isinstance(data, dict),
        "label": label,
        "type": type(data).__name__,
        "issues": [] if isinstance(data, dict) else [f"{label} root must be a JSON object"],
    }


def validate_required_keys(
    data: dict[str, Any],
    *,
    required_keys: tuple[str, ...],
    label: str,
) -> dict[str, object]:
    """Validate required top-level keys without rejecting unknown future fields."""

    missing = [key for key in required_keys if key not in data]
    return {
        "ok": not missing,
        "label": label,
        "missing_keys": missing,
        "issues": [f"{label} missing required key: {key}" for key in missing],
    }


def validate_implementation_draft_contract(
    draft: dict[str, Any],
    *,
    allowed_prefixes: tuple[str, ...] = DEFAULT_ALLOWED_ARTIFACT_PREFIXES,
) -> dict[str, object]:
    """Validate a generated implementation draft at contract level.

    This helper preserves unknown fields and only checks the stable contract
    surface needed by the NPU/AI pipeline.
    """

    key_report = validate_required_keys(
        draft,
        required_keys=REQUIRED_IMPLEMENTATION_DRAFT_KEYS,
        label="implementation_draft",
    )

    paths: list[str] = []
    for field_name in ("proposed_files", "support_files"):
        entries = draft.get(field_name) or []
        if not isinstance(entries, list):
            continue
        for entry in entries:
            if isinstance(entry, dict) and entry.get("file"):
                paths.append(str(entry["file"]))

    path_report = validate_generated_artifact_paths(
        paths,
        allowed_prefixes=allowed_prefixes,
    )

    issues = [*key_report["issues"], *path_report["invalid_paths"]]
    return {
        "ok": bool(key_report["ok"] and path_report["ok"]),
        "label": "implementation_draft",
        "required_key_report": key_report,
        "artifact_path_report": path_report,
        "issues": issues,
    }
