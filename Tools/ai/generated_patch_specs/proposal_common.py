"""Shared helpers for proposal-derived patch specs."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

DEFAULT_OUTPUT_DIR = "output/patch_specs"
DEFAULT_BASENAME = "proposal_patch_specs"
EXPECTED_PROPOSAL_KIND = "repository_change_proposals"
EXPECTED_APPLY_MODE = "manual_review_only"
SPEC_KIND = "proposal_patch_spec_draft"
MANIFEST_KIND = "proposal_patch_spec_manifest"

SUPPORTED_OUTPUT_KINDS = {
    "python_code",
    "markdown",
    "json",
    "powershell",
    "workflow_yaml",
    "text_or_config",
}
SKIPPED_OUTPUT_KINDS = {"path_group"}
CONCRETE_OPERATION_NAMES = {
    "replace_once",
    "append_once",
    "insert_after_once",
    "insert_before_once",
    "write_file",
}
FORBIDDEN_TARGET_PREFIXES = (
    "indexAI/",
    "indexAI/code_chunks/",
    "indexAI/project_code_chunks/",
    "output/",
    "docs/LOCAL_VALIDATION_EVIDENCE/",
    "renders/",
    "Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/",
    "patch_specs/inbox/",
)
FORBIDDEN_TARGET_EXACT = {"Scripting/shared/blender_compat.py"}
FORBIDDEN_TARGET_FRAGMENTS = ("full_analysis", "analysis_full")
DEFAULT_GUARDRAILS = [
    "Draft specs are metadata-only unless concrete_operations were explicitly supplied by a proposal.",
    "Do not copy drafts into patch_specs/inbox/ without explicit human approval.",
    "Run generated patch-spec apply in a review branch and inspect the result before PR creation.",
    "Keep provider execution explicit and report-bound.",
]

def split_path_values(items: list[str]) -> list[str]:
    values: list[str] = []
    for item in items:
        for part in str(item).split(","):
            normalized = part.strip().strip("'\"")
            if normalized:
                values.append(normalized)
    return values

def resolve_repo_path(repo_root: Path, raw: str) -> Path:
    path = Path(raw)
    if path.is_absolute():
        return path.resolve()
    return (repo_root / path).resolve()

def repo_relative(path: Path, repo_root: Path) -> str:
    try:
        return path.resolve().relative_to(repo_root).as_posix()
    except ValueError:
        return path.as_posix()

def normalize_repo_path(value: Any) -> str:
    return str(value or "").strip().replace("\\", "/")

def sanitize_filename(value: str) -> str:
    sanitized = re.sub(r"[^A-Za-z0-9._-]+", "_", value.strip())
    sanitized = sanitized.strip("._-")
    return sanitized or "proposal"

def read_json_object(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return data

def target_path_error(path: str, repo_root: Path) -> str | None:
    normalized = normalize_repo_path(path)
    if not normalized:
        return "empty target path"
    if Path(normalized).is_absolute():
        return "absolute target paths are not allowed"
    full = (repo_root / normalized).resolve()
    try:
        full.relative_to(repo_root)
    except ValueError:
        return "target path escapes repository root"
    if normalized in FORBIDDEN_TARGET_EXACT:
        return f"forbidden target path: {normalized}"
    if any(normalized.startswith(prefix) for prefix in FORBIDDEN_TARGET_PREFIXES):
        return f"forbidden target prefix: {normalized}"
    lower = normalized.lower()
    if any(fragment in lower for fragment in FORBIDDEN_TARGET_FRAGMENTS) and lower.endswith(
        ".json"
    ):
        return f"forbidden full-analysis JSON target: {normalized}"
    if "*" in normalized or normalized.endswith("/"):
        return "target is a path group, glob or directory"
    if not full.exists():
        return "target file does not exist"
    if not full.is_file():
        return "target is not a file"
    return None

def output_descriptor_from_target(path: str) -> dict[str, str]:
    suffix = Path(path).suffix.lower()
    if suffix == ".py":
        artifact_kind = "python_code"
    elif suffix == ".md":
        artifact_kind = "markdown"
    elif suffix == ".json":
        artifact_kind = "json"
    elif suffix == ".ps1":
        artifact_kind = "powershell"
    elif suffix in {".yml", ".yaml"}:
        artifact_kind = "workflow_yaml"
    else:
        artifact_kind = "text_or_config"
    return {
        "path": path,
        "artifact_kind": artifact_kind,
        "operation": "manual_patch_suggestion",
        "content_status": "proposal_only",
        "write_policy": EXPECTED_APPLY_MODE,
    }

def proposal_outputs(proposal: dict[str, Any]) -> list[dict[str, Any]]:
    raw_outputs = proposal.get("suggestion_outputs")
    if isinstance(raw_outputs, list) and raw_outputs:
        return [item for item in raw_outputs if isinstance(item, dict)]
    target_files = proposal.get("target_files")
    if not isinstance(target_files, list):
        return []
    return [output_descriptor_from_target(str(path)) for path in target_files if str(path).strip()]
