"""Explicit branch/push helpers for the patch suggestion final phase."""
from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any

from Tools.ai.patch_suggestion_bundle.common import current_branch, git_status_short


PROTECTED_BRANCHES = {"main", "master"}
INVALID_REF_CHARS = set(" ~^:?*[\\")


def validate_branch_name(branch: str, allowed_prefixes: list[str]) -> tuple[bool, str | None]:
    """Validate a branch name for explicit review-branch preparation."""
    if not branch:
        return False, "empty branch name"
    if branch in PROTECTED_BRANCHES:
        return False, "protected branch is not allowed"
    if not any(branch.startswith(prefix) for prefix in allowed_prefixes):
        return False, "branch does not match allowed prefix"
    if branch.startswith(("/", ".")) or branch.endswith(("/", ".", ".lock")):
        return False, "invalid branch edge characters"
    if ".." in branch or "@{" in branch or "//" in branch:
        return False, "invalid branch sequence"
    if any(char in INVALID_REF_CHARS for char in branch):
        return False, "invalid branch character"
    return True, None


def git_result(repo_root: Path, args: list[str]) -> dict[str, Any]:
    """Run git and return a compact command result."""
    result = subprocess.run(
        ["git", *args],
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
    )
    return {
        "command": ["git", *args],
        "returncode": result.returncode,
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
        "ok": result.returncode == 0,
    }


def local_branch_exists(repo_root: Path, branch: str) -> bool:
    """Return true when a local branch already exists."""
    result = git_result(repo_root, ["show-ref", "--verify", "--quiet", f"refs/heads/{branch}"])
    return bool(result["ok"])


def create_review_branch(
    repo_root: Path,
    branch: str,
    *,
    allowed_prefixes: list[str],
    allow_dirty: bool,
) -> dict[str, Any]:
    """Create and switch to an explicit review branch without committing."""
    status_before = git_status_short(repo_root)
    out: dict[str, Any] = {
        "requested": bool(branch),
        "branch": branch,
        "created": False,
        "switched": False,
        "errors": [],
        "warnings": [],
        "commands": [],
        "status_before": status_before,
        "status_after": status_before,
    }
    if not branch:
        return out
    ok, reason = validate_branch_name(branch, allowed_prefixes)
    if not ok:
        out["errors"].append(str(reason))
        return out
    if status_before and not allow_dirty:
        out["errors"].append("refusing branch creation with dirty tree; use --allow-dirty-branch")
        return out
    current = current_branch(repo_root)
    if current == branch:
        out["switched"] = True
        return out
    if local_branch_exists(repo_root, branch):
        out["errors"].append(f"local branch already exists: {branch}")
        return out
    result = git_result(repo_root, ["switch", "-c", branch])
    out["commands"].append(result)
    if result["ok"]:
        out["created"] = True
        out["switched"] = True
    else:
        out["errors"].append(result["stderr"] or "git switch -c failed")
    out["status_after"] = git_status_short(repo_root)
    return out


def push_review_branch(
    repo_root: Path,
    branch: str,
    *,
    remote: str,
    allowed_prefixes: list[str],
) -> dict[str, Any]:
    """Push the current branch head without committing or force-pushing."""
    target_branch = branch or current_branch(repo_root)
    status_before = git_status_short(repo_root)
    out: dict[str, Any] = {
        "requested": True,
        "remote": remote,
        "branch": target_branch,
        "pushed": False,
        "errors": [],
        "warnings": [],
        "commands": [],
        "status_before": status_before,
        "status_after": status_before,
        "uncommitted_changes_not_pushed": bool(status_before),
    }
    ok, reason = validate_branch_name(target_branch, allowed_prefixes)
    if not ok:
        out["errors"].append(str(reason))
        return out
    if not remote:
        out["errors"].append("empty remote is not allowed")
        return out
    if status_before:
        out["warnings"].append("working tree has uncommitted changes; push only publishes current HEAD")
    result = git_result(repo_root, ["push", "-u", remote, target_branch])
    out["commands"].append(result)
    if result["ok"]:
        out["pushed"] = True
    else:
        out["errors"].append(result["stderr"] or "git push failed")
    out["status_after"] = git_status_short(repo_root)
    return out
