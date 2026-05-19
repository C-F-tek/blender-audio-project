"""Shared helpers for agnostic context stack smoke."""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path
from typing import Any

DEFAULT_OUTPUT = "output/validation/agnostic_context_stack_smoke.json"
DEFAULT_MARKDOWN = "output/validation/agnostic_context_stack_smoke.md"
DEFAULT_WORK_DIR = "output/validation/agnostic_context_stack_smoke"


def repo_path(repo_root: Path, value: str) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = repo_root / path
    return path.resolve()


def rel(path: Path, repo_root: Path) -> str:
    try:
        return path.resolve(strict=False).relative_to(repo_root.resolve(strict=False)).as_posix()
    except ValueError:
        return str(path)


def load_json(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    try:
        return json.loads(path.read_text(encoding="utf-8-sig")), None
    except Exception as exc:  # noqa: BLE001
        return None, f"{type(exc).__name__}: {exc}"


def value_at(data: dict[str, Any], dotted: str) -> Any:
    current: Any = data
    for part in dotted.split("."):
        if not isinstance(current, dict) or part not in current:
            return None
        current = current[part]
    return current


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
    except Exception as exc:  # noqa: BLE001
        return 1, "", "", f"{type(exc).__name__}: {exc}"


def check_json_output(repo_root: Path, output: str, expected: dict[str, Any]) -> dict[str, Any]:
    path = repo_path(repo_root, output)
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
    data, error = load_json(path)
    if error or data is None:
        result["ok"] = False
        result["errors"].append(error or "invalid JSON")
        return result
    result["kind"] = data.get("kind")
    result["passed"] = data.get("passed")
    for required in ("schema_version", "kind", "passed"):
        if data.get(required) is None:
            result["ok"] = False
            result["errors"].append(f"missing required field: {required}")
    for key, expected_value in expected.items():
        actual = value_at(data, key)
        if actual != expected_value:
            result["ok"] = False
            result["errors"].append(
                f"unexpected {key}: expected {expected_value!r}, got {actual!r}"
            )
    return result


def run_step(
    repo_root: Path,
    name: str,
    command: list[str],
    outputs: dict[str, dict[str, Any]],
    timeout_seconds: int,
    dry_run: bool,
) -> dict[str, Any]:
    step: dict[str, Any] = {
        "name": name,
        "command": command,
        "returncode": None,
        "ok": True,
        "errors": [],
        "stdout_tail": "",
        "stderr_tail": "",
        "outputs": [],
    }
    if dry_run:
        step["warnings"] = ["dry-run: command not executed"]
        return step
    returncode, stdout, stderr, error = run_command(command, repo_root, timeout_seconds)
    step["returncode"] = returncode
    step["stdout_tail"] = stdout
    step["stderr_tail"] = stderr
    if error:
        step["errors"].append(error)
    if returncode != 0:
        step["errors"].append(f"command returned {returncode}")
    for output, expected in outputs.items():
        validation = (
            check_json_output(repo_root, output, expected)
            if output.endswith(".json")
            else {
                "path": output,
                "exists": repo_path(repo_root, output).exists(),
                "ok": repo_path(repo_root, output).exists(),
                "errors": [],
            }
        )
        step["outputs"].append(validation)
        if not validation["ok"]:
            step["errors"].extend(f"{validation['path']}: {err}" for err in validation["errors"])
    step["ok"] = not step["errors"]
    return step
