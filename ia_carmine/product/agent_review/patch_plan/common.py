"""Shared helpers for agent review patch plans."""

from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    from ia_carmine._shared.code_patch_plan_common import read_json_object
except ImportError:
    repo_root_for_import = Path(__file__).resolve().parents[3]
    if str(repo_root_for_import) not in sys.path:
        sys.path.insert(0, str(repo_root_for_import))
    from ia_carmine._shared.code_patch_plan_common import read_json_object

DEFAULT_ORCHESTRATOR = "output/ai_pipeline/agent_gpu_npu_parallel_orchestrator_live.json"
DEFAULT_EVIDENCE = "output/ai_pipeline/agent_review_evidence_sufficiency.json"
DEFAULT_OUTPUT = "output/patch_specs/agent_review_patch_plan.json"
DEFAULT_MARKDOWN = "output/patch_specs/agent_review_patch_plan.md"

PLAN_KIND = "agent_review_patch_plan"
APPLY_MODE = "report_only_manual_review_patch_plan"

DEFAULT_VALIDATION_COMMANDS = [
    "python -m Tools.validation check_python_syntax --repo-root . --output output/validation/python_syntax.json",
    "python -m Tools.validation check_validation_report_contract --repo-root . --output output/validation/validation_report_contract.json",
    "git diff --check",
    "git status --short",
]

FORBIDDEN_TARGET_PREFIXES = (
    "output/",
    "renders/",
    ".git/",
    "indexAI/code_chunks/",
    "indexAI/project_code_chunks/",
)

FORBIDDEN_TARGET_FRAGMENTS = (
    "full_analysis",
    "analysis_full",
)

def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")

def resolve_path(repo_root: Path, value: str | Path) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = repo_root / path
    return path.resolve()

def repo_rel(path: Path, repo_root: Path) -> str:
    try:
        return path.resolve(strict=False).relative_to(repo_root.resolve(strict=False)).as_posix()
    except ValueError:
        return str(path)

def load_json_object(path: Path) -> dict[str, Any]:
    data, errors = read_json_object(path)
    if errors:
        raise ValueError(f"{path}: {'; '.join(errors)}")
    return data

def normalize_repo_path(value: Any) -> str:
    return str(value or "").strip().replace("\\", "/").strip("/")

def unique_strings(values: list[Any]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for value in values:
        text = normalize_repo_path(value)
        if text and text not in seen:
            seen.add(text)
            result.append(text)
    return result

def target_path_error(path_value: str, repo_root: Path) -> str | None:
    normalized = normalize_repo_path(path_value)
    if not normalized:
        return "empty target path"
    if Path(normalized).is_absolute():
        return "absolute target paths are not allowed"
    full = (repo_root / normalized).resolve()
    try:
        full.relative_to(repo_root.resolve())
    except ValueError:
        return "target path escapes repository root"
    if any(normalized.startswith(prefix) for prefix in FORBIDDEN_TARGET_PREFIXES):
        return f"forbidden generated/runtime target prefix: {normalized}"
    lower = normalized.lower()
    if any(fragment in lower for fragment in FORBIDDEN_TARGET_FRAGMENTS) and lower.endswith(
        ".json"
    ):
        return f"forbidden full-analysis JSON target: {normalized}"
    if "*" in normalized or normalized.endswith("/"):
        return "target is a glob or directory, not a concrete file"
    if not full.exists():
        return "target file does not exist"
    if not full.is_file():
        return "target is not a file"
    return None

def compact_evidence_files(item: dict[str, Any]) -> list[dict[str, Any]]:
    compact: list[dict[str, Any]] = []
    for evidence_file in (
        item.get("evidence_files", []) if isinstance(item.get("evidence_files"), list) else []
    ):
        if not isinstance(evidence_file, dict):
            continue
        compact.append(
            {
                "path": evidence_file.get("path"),
                "exists": evidence_file.get("exists"),
                "kind": evidence_file.get("kind"),
                "matched_terms": evidence_file.get("matched_terms", []),
            }
        )
    return compact


COSMETIC_PATCH_KEYWORDS = (
    "whitespace",
    "space-only",
    "spacing-only",
    "tag spacing",
    "tag-spacing",
    "formatting-only",
    "cosmetic",
)
