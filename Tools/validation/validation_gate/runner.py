"""Execution helpers for the unified validation gate."""

from __future__ import annotations

import os
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any

from .models import GateStep


def repo_path(repo_root: Path, value: str) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = repo_root / path
    return path.resolve()


def rel(path: Path, repo_root: Path) -> str:
    try:
        return path.resolve(strict=False).relative_to(repo_root.resolve(strict=False)).as_posix()
    except ValueError:
        return str(path).replace("\\", "/")


def run_command(step: GateStep, repo_root: Path, *, dry_run: bool) -> dict[str, Any]:
    result: dict[str, Any] = {
        "name": step.name,
        "command": step.command,
        "suites": list(step.suites),
        "tags": list(step.tags),
        "heavy": step.heavy,
        "provider_live": step.provider_live,
        "timeout_seconds": step.timeout_seconds,
        "returncode": None,
        "ok": True,
        "errors": [],
        "warnings": [],
        "stdout_tail": "",
        "stderr_tail": "",
        "outputs": [],
    }
    if dry_run:
        result["warnings"].append("dry-run: command not executed")
    else:
        try:
            completed = subprocess.run(
                step.command,
                cwd=repo_root,
                text=True,
                capture_output=True,
                timeout=step.timeout_seconds,
                check=False,
                env={**os.environ, "PYTHONIOENCODING": "utf-8"},
            )
            result["returncode"] = completed.returncode
            result["stdout_tail"] = (completed.stdout or "")[-12000:]
            result["stderr_tail"] = (completed.stderr or "")[-12000:]
            if completed.returncode != 0 and not step.allow_nonzero:
                result["errors"].append(f"command returned {completed.returncode}")
        except subprocess.TimeoutExpired as exc:
            result["returncode"] = 124
            result["stdout_tail"] = exc.stdout or ""
            result["stderr_tail"] = exc.stderr or ""
            result["errors"].append(f"TimeoutExpired: {step.timeout_seconds}s")
        except Exception as exc:  # noqa: BLE001 - gate report captures diagnostics.
            result["returncode"] = 1
            result["errors"].append(f"{type(exc).__name__}: {exc}")

    for output in step.outputs:
        output_path = repo_path(repo_root, output)
        result["outputs"].append(
            {
                "path": rel(output_path, repo_root),
                "exists": output_path.exists(),
                "size_bytes": output_path.stat().st_size if output_path.exists() else 0,
            }
        )
        if not dry_run and not output_path.exists():
            result["errors"].append(f"missing output: {output}")

    result["ok"] = not result["errors"]
    return result


def run_gate(repo_root: Path, steps: list[GateStep], *, dry_run: bool) -> dict[str, Any]:
    results = [run_command(step, repo_root, dry_run=dry_run) for step in steps]
    errors = [f"{step['name']}: {error}" for step in results for error in step["errors"]]
    warnings = [
        f"{step['name']}: {warning}" for step in results for warning in step["warnings"]
    ]
    return {
        "schema_version": 1,
        "kind": "validation_gate",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "repo_root": str(repo_root),
        "passed": not errors,
        "errors": errors,
        "warnings": warnings,
        "dry_run": dry_run,
        "step_count": len(results),
        "steps": results,
        "provider_execution_performed": any(step["provider_live"] for step in results)
        and not dry_run,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "guardrails": {
            "single_validation_entrypoint": True,
            "provider_live_default_off": True,
            "heavy_default_off": True,
            "patch_application_performed": False,
            "source_writes_performed": False,
        },
    }
