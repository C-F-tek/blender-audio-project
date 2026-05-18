"""Shared helpers for agent review patch-plan full validation."""

from __future__ import annotations

import json
import os
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any

def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def repo_path(repo_root: Path, value: str | Path) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = repo_root / path
    return path.resolve()


def rel(path: Path, repo_root: Path) -> str:
    try:
        return path.resolve(strict=False).relative_to(repo_root.resolve(strict=False)).as_posix()
    except ValueError:
        return str(path).replace("\\", "/")


def load_json(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:  # noqa: BLE001 - full validation report captures diagnostics.
        return None, f"{type(exc).__name__}: {exc}"
    if not isinstance(data, dict):
        return None, f"expected JSON object, got {type(data).__name__}"
    return data, None


def value_at(data: dict[str, Any], dotted: str) -> Any:
    current: Any = data
    for part in dotted.split("."):
        if not isinstance(current, dict):
            return None
        current = current.get(part)
    return current


def run_command(command: list[str], repo_root: Path, timeout_seconds: int) -> dict[str, Any]:
    started = datetime.now().isoformat(timespec="seconds")
    try:
        completed = subprocess.run(
            command,
            cwd=repo_root,
            text=True,
            capture_output=True,
            timeout=timeout_seconds,
            check=False,
            env={**os.environ, "PYTHONIOENCODING": "utf-8"},
        )
        return {
            "command": command,
            "started_at": started,
            "returncode": completed.returncode,
            "ok": completed.returncode == 0,
            "stdout_tail": (completed.stdout or "")[-12000:],
            "stderr_tail": (completed.stderr or "")[-12000:],
            "error": "",
        }
    except subprocess.TimeoutExpired as exc:
        return {
            "command": command,
            "started_at": started,
            "returncode": 124,
            "ok": False,
            "stdout_tail": exc.stdout or "",
            "stderr_tail": exc.stderr or "",
            "error": f"TimeoutExpired: {timeout_seconds}s",
        }
    except Exception as exc:  # noqa: BLE001
        return {
            "command": command,
            "started_at": started,
            "returncode": 1,
            "ok": False,
            "stdout_tail": "",
            "stderr_tail": "",
            "error": f"{type(exc).__name__}: {exc}",
        }


def bundle_paths(repo_root: Path, output_dir: str, basename: str) -> tuple[Path, Path]:
    directory = repo_path(repo_root, output_dir)
    return directory / f"{basename}.json", directory / f"{basename}.md"


def summarize_artifact(path: Path, repo_root: Path) -> dict[str, Any]:
    data, error = load_json(path) if path.exists() else (None, "missing")
    summary: dict[str, Any] = {
        "path": rel(path, repo_root),
        "exists": path.exists(),
        "json_ok": data is not None,
        "error": error or "",
    }
    if data:
        for key in (
            "schema_version",
            "kind",
            "passed",
            "provider_execution_performed",
            "patch_application_performed",
            "source_writes_performed",
            "apply_mode",
            "patch_plan_count",
            "fallback_used",
            "bundle_count",
        ):
            if key in data:
                summary[key] = data.get(key)
        decision = data.get("decision") if isinstance(data.get("decision"), dict) else {}
        if decision:
            summary["decision"] = {
                key: decision.get(key)
                for key in (
                    "ready_for_manual_review",
                    "patch_plan_count",
                    "fallback_used",
                    "gpu_recommendation_count",
                    "evidence_ready_for_manual_patch_count",
                    "manual_review_required",
                    "provider_execution_seen",
                    "selected_chunks_evidence_seen",
                )
                if key in decision
            }
    return summary
