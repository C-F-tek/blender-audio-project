"""Shared helpers for selective execution plans."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

PLAN_KIND = "selective_execution_plan"
SCHEMA_VERSION = 1
DEFAULT_CONTEXT_EVIDENCE = (
    "docs/LOCAL_VALIDATION_EVIDENCE/project_self_improvement_context_pack_evidence.json"
)
DEFAULT_CONTEXT_EVIDENCE_MD = (
    "docs/LOCAL_VALIDATION_EVIDENCE/project_self_improvement_context_pack_evidence.md"
)
DEFAULT_DRY_RUN_EVIDENCE = "docs/LOCAL_VALIDATION_EVIDENCE/ai_pipeline_dry_run_matrix_evidence.json"
DEFAULT_PROVIDER_EVIDENCE = (
    "docs/LOCAL_VALIDATION_EVIDENCE/parallel_gpu_npu_multistep_real_npu_v2_evidence.json"
)
DEFAULT_VALIDATION_CONTRACT = "output/validation/validation_report_contract.json"
DEFAULT_TECH_DEBT = "docs/TECH_DEBT_TRACKER.md"
DEFAULT_EXECUTION_PLAN_DIR = "docs/EXECUTION_PLANS/active"

def repo_relative(path: Path, repo_root: Path) -> str:
    """Return a stable repo-relative POSIX path when possible."""
    resolved = path.resolve()
    try:
        return resolved.relative_to(repo_root).as_posix()
    except ValueError:
        return resolved.as_posix()

def resolve_repo_path(repo_root: Path, value: str) -> Path:
    """Resolve value under repo_root unless already absolute."""
    path = Path(value)
    if not path.is_absolute():
        path = repo_root / path
    return path.resolve()

def read_json_object(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    """Read a JSON object from path."""
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

def read_text_file(path: Path, max_chars: int = 12000) -> tuple[str | None, str | None, bool]:
    """Read a bounded text file."""
    try:
        text = path.read_text(encoding="utf-8-sig")
    except FileNotFoundError:
        return None, f"not found: {path}", False
    except OSError as exc:
        return None, f"read error: {exc}", False
    truncated = len(text) > max_chars
    return text[:max_chars], None, truncated
