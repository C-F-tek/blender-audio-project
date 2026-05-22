from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


DENIED_GIT_PATH_PREFIXES = (
    "output/",
    "renders/",
    "indexAI/code_chunks/",
    "indexAI/project_code_chunks/",
)

DENIED_GIT_SUFFIXES = (
    ".db",
    ".sqlite",
    ".sqlite-wal",
    ".sqlite-shm",
)

DESTRUCTIVE_PATTERNS = (
    r"\bgit\s+add\s+(\.|-A|--all)\b",
    r"\bgit\s+add\s+(\.\\)?output\b",
    r"\bgit\s+reset\s+--hard\b",
    r"\bgit\s+clean\b",
    r"\bgit\s+push\b.*\s--force(?:-with-lease)?\b",
    r"\bgit\s+merge\b.*\b(master|main)\b",
    r"\brm\s+-rf\b",
    r"\bRemove-Item\b.*\b-Recurse\b.*\b-Force\b",
    r"\bdel\s+/s\b",
    r"\bterraform\s+(apply|destroy)\b",
)

SAFE_VALIDATION_HINTS = (
    "git status --short",
    "git diff --check",
    "python -m Tools.validation check_python_syntax",
    "python .\\Tools\\validation\\check_python_syntax.py",
    "python .\\Tools\\validation\\check_validation_report_contract.py",
)


def read_hook_input() -> dict[str, Any]:
    try:
        raw = sys.stdin.read()
        return json.loads(raw) if raw.strip() else {}
    except Exception:
        return {}


def repo_root(event: dict[str, Any] | None = None) -> Path:
    event = event or {}
    cwd = Path(str(event.get("cwd") or os.getcwd())).resolve()
    try:
        completed = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=cwd,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=10,
            check=False,
        )
        if completed.returncode == 0 and completed.stdout.strip():
            return Path(completed.stdout.strip()).resolve()
    except Exception:
        pass
    return cwd


def run_git(root: Path, *args: str, timeout: int = 10) -> str:
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=root,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
            check=False,
        )
        if completed.returncode == 0:
            return completed.stdout.strip()
        return (completed.stdout + "\n" + completed.stderr).strip()
    except Exception as exc:
        return f"{type(exc).__name__}: {exc}"


def git_status_paths(root: Path) -> list[str]:
    status = run_git(root, "status", "--short")
    paths: list[str] = []
    for line in status.splitlines():
        if not line.strip():
            continue
        text = line[3:].strip() if len(line) > 3 else line.strip()
        if " -> " in text:
            text = text.split(" -> ", 1)[1].strip()
        paths.append(normalize_repo_path(text))
    return paths


def normalize_repo_path(path: str) -> str:
    return str(path or "").strip().strip('"').replace("\\", "/")


def is_denied_git_path(path: str) -> bool:
    normalized = normalize_repo_path(path)
    lower = normalized.lower()
    if any(lower.startswith(prefix.lower()) for prefix in DENIED_GIT_PATH_PREFIXES):
        return True
    return any(lower.endswith(suffix) for suffix in DENIED_GIT_SUFFIXES)


def command_text(event: dict[str, Any]) -> str:
    tool_input = event.get("tool_input")
    if isinstance(tool_input, dict):
        command = tool_input.get("command")
        if isinstance(command, str):
            return command
        return json.dumps(tool_input, ensure_ascii=False, sort_keys=True)
    return "" if tool_input is None else str(tool_input)


def tool_name(event: dict[str, Any]) -> str:
    return str(event.get("tool_name") or "")


def first_existing(root: Path, candidates: list[str]) -> list[str]:
    found: list[str] = []
    for item in candidates:
        if (root / item).exists():
            found.append(item)
    return found


def latest_files(root: Path, pattern: str, limit: int = 5) -> list[str]:
    files = [path for path in root.glob(pattern) if path.is_file()]
    files.sort(key=lambda path: path.stat().st_mtime, reverse=True)
    return [path.relative_to(root).as_posix() for path in files[:limit]]


def excerpt_file(root: Path, rel_path: str, max_chars: int = 1800) -> str:
    path = root / rel_path
    if not path.exists() or not path.is_file():
        return ""
    try:
        text = path.read_text(encoding="utf-8-sig", errors="replace")
    except Exception as exc:
        return f"[read_error] {type(exc).__name__}: {exc}"
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + "\n...[truncated]"


def compact_list(items: list[str], empty: str = "none") -> str:
    return ", ".join(items) if items else empty


def json_stdout(payload: dict[str, Any]) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def additional_context(event_name: str, text: str, *, system_message: str | None = None) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "hookSpecificOutput": {
            "hookEventName": event_name,
            "additionalContext": text,
        }
    }
    if system_message:
        payload["systemMessage"] = system_message
    return payload


def pretool_deny(reason: str) -> dict[str, Any]:
    return {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    }


def posttool_block(reason: str, context: str) -> dict[str, Any]:
    return {
        "continue": False,
        "stopReason": reason,
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": context,
        },
    }


def stop_continue(context: str) -> dict[str, Any]:
    return {
        "continue": False,
        "stopReason": "IA-Carmine completion gate requires more work before closing.",
        "systemMessage": "IA-Carmine completion gate found missing validation or unsafe working-tree state.",
        "hookSpecificOutput": {
            "hookEventName": "Stop",
            "additionalContext": context,
        },
    }


def command_matches_any(command: str, patterns: tuple[str, ...]) -> str:
    for pattern in patterns:
        if re.search(pattern, command, flags=re.IGNORECASE | re.MULTILINE):
            return pattern
    return ""


def summarize_git(root: Path) -> list[str]:
    branch = run_git(root, "branch", "--show-current") or "unknown"
    head = run_git(root, "log", "--oneline", "-1") or "unknown"
    status = run_git(root, "status", "--short")
    dirty = "yes" if status.strip() else "no"
    return [
        f"repo_root={root}",
        f"branch={branch}",
        f"head={head}",
        f"dirty={dirty}",
    ]
