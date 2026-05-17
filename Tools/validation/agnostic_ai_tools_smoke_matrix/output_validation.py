"""Output validators for agnostic AI tools smoke matrix."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path
from typing import Any

from .common import load_json, rel, value_at
from .models import SmokeStep

def expected_for_output(step: SmokeStep, output: str) -> dict[str, Any]:
    """Return expected values for a specific output artifact."""
    return step.expected_values_by_output.get(output, step.expected_values)


def required_for_output(step: SmokeStep, output: str) -> tuple[str, ...]:
    """Return required fields for a specific output artifact."""
    return step.required_fields_by_output.get(output, step.required_fields)


def run_command(
    command: list[str], repo_root: Path, timeout_seconds: int
) -> tuple[int, str, str, str | None]:
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
        return completed.returncode, completed.stdout[-12000:], completed.stderr[-12000:], None
    except subprocess.TimeoutExpired as exc:
        return 124, exc.stdout or "", exc.stderr or "", f"TimeoutExpired: {timeout_seconds}s"
    except Exception as exc:  # noqa: BLE001 - matrix smoke runner.
        return 1, "", "", f"{type(exc).__name__}: {exc}"


def validate_output(
    *,
    path: Path,
    repo_root: Path,
    required_fields: tuple[str, ...],
    expected_values: dict[str, Any],
) -> dict[str, Any]:
    result: dict[str, Any] = {
        "path": rel(path, repo_root),
        "exists": path.exists(),
        "ok": True,
        "errors": [],
        "kind": None,
        "passed": None,
    }
    if not path.exists():
        result["ok"] = False
        result["errors"].append("missing output")
        return result
    if path.suffix.lower() != ".json":
        return result
    data, error = load_json(path)
    if error or data is None:
        result["ok"] = False
        result["errors"].append(error or "invalid JSON")
        return result
    result["kind"] = data.get("kind")
    result["passed"] = data.get("passed")
    for field_name in required_fields:
        if value_at(data, field_name) is None:
            result["ok"] = False
            result["errors"].append(f"missing required field: {field_name}")
    for field_name, expected in expected_values.items():
        actual = value_at(data, field_name)
        if actual != expected:
            result["ok"] = False
            result["errors"].append(
                f"unexpected {field_name}: expected {expected!r}, got {actual!r}"
            )
    return result
