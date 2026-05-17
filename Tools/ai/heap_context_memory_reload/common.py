"""Common IO and tool execution helpers for heap startup reload."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

CANONICAL_CONTEXT_FILES = (
    "AGENTS.md",
    "README.md",
    "WORKFLOW.md",
    "docs/README.md",
    "docs/LOCAL_AI_TASKS/read-first-reuse-first-small-files-rule-2026-05-07.md",
    "docs/LOCAL_AI_TASKS/single-owner-scripts-and-flow-boundaries-2026-05-07.md",
    "docs/LOCAL_AI_TASKS/project-tool-registry.md",
    "docs/LOCAL_AI_TASKS/documentation-panorama-and-staleness-map-2026-05-09.md",
    "docs/LOCAL_AI_TASKS/ai-orientation-map-2026-05-09.md",
    "Tools/ai/README.md",
    "Tools/workflow/README.md",
)
SEMANTIC_CHUNK_ROOTS = (
    "Tools/ai",
    "Tools/validation",
    "Tools/workflow",
    "docs/LOCAL_AI_TASKS",
)
REPO_SCAN_EXCLUDED_DIRS = {
    ".git",
    ".venv",
    "venv",
    ".venv314",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "node_modules",
    "renders",
    "output",
    "indexAI/code_chunks",
}
REPO_SCAN_TEXT_SUFFIXES = {
    ".py",
    ".ps1",
    ".md",
    ".txt",
    ".json",
    ".yml",
    ".yaml",
    ".toml",
    ".ini",
    ".cfg",
    ".csv",
    ".bat",
    ".sh",
}


def now_stamp() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def read_request_file(repo_root: Path, value: str) -> str:
    path = Path(value)
    if not path.is_absolute():
        path = repo_root / path
    return path.read_text(encoding="utf-8-sig", errors="replace")


def repo_rel(repo_root: Path, path: Path) -> str:
    try:
        return path.resolve(strict=False).relative_to(repo_root.resolve(strict=False)).as_posix()
    except ValueError:
        return str(path)


def read_text(path: Path, max_chars: int = 6000) -> str:
    try:
        text = path.read_text(encoding="utf-8-sig", errors="replace")
    except Exception:
        return ""
    if len(text) > max_chars:
        return text[:max_chars] + "\n...[truncated]\n"
    return text


def read_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_markdown(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def resolve_project_python(repo_root: Path, explicit: str = "") -> str:
    if explicit:
        return str(Path(explicit).resolve())
    for candidate in (
        repo_root / ".venv" / "Scripts" / "python.exe",
        repo_root / "venv" / "Scripts" / "python.exe",
        repo_root / ".venv314" / "Scripts" / "python.exe",
    ):
        if candidate.exists():
            return str(candidate.resolve())
    return sys.executable


def summarize_artifact(path: Path, repo_root: Path) -> dict[str, Any]:
    item: dict[str, Any] = {
        "path": repo_rel(repo_root, path),
        "exists": path.exists(),
        "size_bytes": None,
        "suffix": path.suffix.lower(),
        "json_ok": False,
        "json_passed": None,
        "kind": "",
        "useful": False,
    }
    if not path.exists() or not path.is_file():
        return item
    try:
        size = path.stat().st_size
    except OSError:
        size = 0
    item["size_bytes"] = size
    item["useful"] = size > 0
    if path.suffix.lower() == ".json" and size > 0:
        data = read_json(path)
        item["json_ok"] = bool(data)
        item["json_passed"] = data.get("passed") if data else None
        item["kind"] = str(data.get("kind") or data.get("report_kind") or "")
        if data:
            item["summary_fields"] = {
                key: data.get(key)
                for key in (
                    "passed",
                    "profile",
                    "included_file_count",
                    "truncated_file_count",
                    "provider_execution_performed",
                    "patch_application_performed",
                    "source_writes_performed",
                )
                if key in data
            }
    return item


def run_tool(
    command: list[str],
    repo_root: Path,
    *,
    name: str,
    requirement: str,
    required: bool,
    artifact_paths: list[Path] | None = None,
) -> dict[str, Any]:
    completed = subprocess.run(
        command,
        cwd=repo_root,
        text=True,
        capture_output=True,
        check=False,
    )
    artifacts = [summarize_artifact(path, repo_root) for path in (artifact_paths or [])]
    existing_artifacts = [item["path"] for item in artifacts if item.get("exists")]
    useful_artifacts = [item["path"] for item in artifacts if item.get("useful")]
    passed = completed.returncode == 0
    artifact_useful = bool(useful_artifacts)
    return {
        "name": name,
        "requirement": requirement,
        "required": required,
        "command": command,
        "returncode": completed.returncode,
        "passed": passed,
        "effective_passed": passed or artifact_useful,
        "degraded": (not passed) and artifact_useful,
        "hard_failed": (not passed) and (not artifact_useful),
        "artifact_useful": artifact_useful,
        "artifact_paths": [item["path"] for item in artifacts],
        "existing_artifact_paths": existing_artifacts,
        "useful_artifact_paths": useful_artifacts,
        "artifact_summaries": artifacts,
        "stdout_tail": (completed.stdout or "")[-3000:],
        "stderr_tail": (completed.stderr or "")[-3000:],
    }


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest() if text else ""
