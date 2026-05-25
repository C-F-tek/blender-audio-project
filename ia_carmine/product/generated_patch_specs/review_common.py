"""Shared helpers for reviewed patch-spec promotion."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

DEFAULT_OUTPUT_DIR = "output/patch_specs"
DEFAULT_BASENAME = "reviewed_patch_spec"
EXPECTED_DRAFT_KIND = "proposal_patch_spec_draft"
EXPECTED_PLAN_KIND = "patch_spec_replacement_plan"
REVIEWED_SPEC_KIND = "reviewed_patch_spec"
REVIEWED_MANIFEST_KIND = "reviewed_patch_spec_manifest"
EXPECTED_APPLY_MODE = "manual_review_only"
EXPECTED_REVIEW_STATUS = "dry_run_passed"
SUPPORTED_REPLACEMENT_TYPES = {"exact", "regex", "insert_after", "insert_before"}
FORBIDDEN_TARGET_PREFIXES = (
    "indexAI/",
    "Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/",
    "patch_specs/inbox/",
)
FORBIDDEN_TARGET_EXACT = {"Scripting/shared/blender_compat.py"}
FORBIDDEN_TARGET_FRAGMENTS = ("full_analysis", "analysis_full")
FORBIDDEN_COMMAND_FRAGMENTS = (
    "git reset --hard",
    "git clean",
    "Remove-Item -Recurse",
    "Remove-Item -Force -Recurse",
    "patch_specs/inbox/",
)
DEFAULT_GUARDRAILS = [
    "Reviewed specs are still manual-review-only.",
    "This tool only dry-runs; it never writes source targets.",
    "Do not copy reviewed specs into patch_specs/inbox/ without explicit approval.",
    "Keep provider execution explicit and report-bound.",
]

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
    return sanitized or "reviewed_patch_spec"

def read_json_object(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return data

def load_patch_runner(repo_root: Path) -> tuple[Any, Any]:
    sys.path.insert(0, str(repo_root))
    from ia_carmine._shared.apply_repo_mods import PatchError, apply_spec

    return apply_spec, PatchError

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

def validation_command_error(command: Any) -> str | None:
    lower = str(command).lower()
    for fragment in FORBIDDEN_COMMAND_FRAGMENTS:
        if fragment.lower() in lower:
            return f"forbidden command fragment: {fragment}"
    return None

def validate_replacement(item: Any) -> str | None:
    if not isinstance(item, dict):
        return "replacement item must be an object"
    kind = item.get("type", "exact")
    if kind not in SUPPORTED_REPLACEMENT_TYPES:
        return f"unsupported replacement type: {kind}"
    count = item.get("count", 1)
    try:
        if int(count) < 1:
            return "replacement count must be >= 1"
    except (TypeError, ValueError):
        return "replacement count must be an integer"
    if kind in {"exact", "regex"} and not isinstance(item.get("new"), str):
        return f"{kind} replacement requires new string"
    if kind == "exact" and not isinstance(item.get("old"), str):
        return "exact replacement requires old string"
    if kind == "regex" and not isinstance(item.get("pattern"), str):
        return "regex replacement requires pattern string"
    if kind in {"insert_after", "insert_before"}:
        if not isinstance(item.get("anchor"), str) or not isinstance(item.get("insert"), str):
            return f"{kind} replacement requires anchor and insert strings"
    return None

def validate_inputs(draft: dict[str, Any], plan: dict[str, Any], repo_root: Path) -> list[str]:
    errors: list[str] = []
    if draft.get("kind") != EXPECTED_DRAFT_KIND:
        errors.append(f"draft kind must be {EXPECTED_DRAFT_KIND}")
    if draft.get("apply_mode") != EXPECTED_APPLY_MODE:
        errors.append("draft apply_mode must be manual_review_only")
    if draft.get("provider_execution_performed") is not False:
        errors.append("draft provider_execution_performed must be false")
    if plan.get("kind") != EXPECTED_PLAN_KIND:
        errors.append(f"replacement plan kind must be {EXPECTED_PLAN_KIND}")
    if plan.get("apply_mode") != EXPECTED_APPLY_MODE:
        errors.append("replacement plan apply_mode must be manual_review_only")
    if plan.get("provider_execution_performed") is not False:
        errors.append("replacement plan provider_execution_performed must be false")

    draft_operations = draft.get("operations")
    if not isinstance(draft_operations, list) or not draft_operations:
        errors.append("draft operations must be a non-empty list")

    plan_operations = plan.get("operations")
    if not isinstance(plan_operations, list) or not plan_operations:
        errors.append("replacement plan operations must be a non-empty list")

    if isinstance(draft_operations, list) and isinstance(plan_operations, list):
        draft_paths = {
            normalize_repo_path(op.get("path")) for op in draft_operations if isinstance(op, dict)
        }
        for index, operation in enumerate(plan_operations):
            if not isinstance(operation, dict):
                errors.append(f"plan operations[{index}] must be an object")
                continue
            path = normalize_repo_path(operation.get("path"))
            if path not in draft_paths:
                errors.append(f"plan operations[{index}] path is not present in draft: {path}")
            path_error = target_path_error(path, repo_root)
            if path_error:
                errors.append(f"plan operations[{index}] {path}: {path_error}")
            replacements = operation.get("replacements")
            if not isinstance(replacements, list) or not replacements:
                errors.append(f"plan operations[{index}] replacements must be a non-empty list")
            elif len(replacements) > 12:
                errors.append(
                    f"plan operations[{index}] has too many replacements; keep reviewed patches small"
                )
            else:
                for repl_index, replacement in enumerate(replacements):
                    repl_error = validate_replacement(replacement)
                    if repl_error:
                        errors.append(
                            f"plan operations[{index}].replacements[{repl_index}]: {repl_error}"
                        )

    for command in plan.get("validation_commands") or []:
        command_error = validation_command_error(command)
        if command_error:
            errors.append(command_error)

    return errors
