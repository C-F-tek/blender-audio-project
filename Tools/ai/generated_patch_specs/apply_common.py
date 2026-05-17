"""Shared helpers for generated patch-spec application."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.ai.patch_suggestion_bundle.common import (
    PatchOperation,
    current_branch,
    git_status_short,
    load_json,
    repo_relative,
    split_values,
    unique_in_order,
    unsafe_git_status_short,
)
from tools.ai.patch_suggestion_bundle.git_branch import create_review_branch
from tools.ai.patch_suggestion_bundle.operations import apply_operation, normalize_operation
from tools.validation.report_utils import (
    resolve_output_path,
    write_json_report,
    write_text_report,
)

CONCRETE_OPERATION_NAMES = {
    "replace_once",
    "append_once",
    "insert_after_once",
    "insert_before_once",
    "write_file",
}
MANUAL_OR_DRAFT_OPERATIONS = {
    "manual_patch_suggestion",
    "proposal_only",
    "manual_review_only",
}
DENIED_TARGET_PREFIXES = (
    "output/",
    "indexAI/code_chunks/",
    "indexAI/project_code_chunks/",
    "docs/LOCAL_VALIDATION_EVIDENCE/",
    "renders/",
)
DENIED_TARGET_SUFFIXES = (
    ".db",
    ".sqlite",
    ".sqlite3",
    ".sqlite-wal",
    ".sqlite-shm",
)

STAMP_RE = re.compile(r"\d{8}-\d{6}")

def run(command: list[str], cwd: Path, timeout: int = 120) -> dict[str, Any]:
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
        return {
            "command": command,
            "returncode": result.returncode,
            "stdout": result.stdout.strip()[:4000],
            "stderr": result.stderr.strip()[:4000],
            "ok": result.returncode == 0,
        }
    except subprocess.TimeoutExpired as exc:
        return {
            "command": command,
            "returncode": 124,
            "stdout": str(exc.stdout or "")[:4000],
            "stderr": str(exc.stderr or "")[:4000],
            "ok": False,
            "error": f"TimeoutExpired: {timeout}s",
        }
