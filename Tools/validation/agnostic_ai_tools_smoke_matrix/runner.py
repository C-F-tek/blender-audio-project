"""Step runner for agnostic AI tools smoke matrix."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .common import repo_path
from .models import SmokeStep
from .output_validation import expected_for_output, required_for_output, run_command, validate_output

def run_step(
    step: SmokeStep, repo_root: Path, timeout_seconds: int, *, dry_run: bool
) -> dict[str, Any]:
    result: dict[str, Any] = {
        "name": step.name,
        "command": step.command,
        "heavy": step.heavy,
        "provider_live": step.provider_live,
        "workflow": step.workflow,
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
        return result

    returncode, stdout, stderr, error = run_command(step.command, repo_root, timeout_seconds)
    result["returncode"] = returncode
    result["stdout_tail"] = stdout
    result["stderr_tail"] = stderr
    if error:
        result["errors"].append(error)
    if returncode != 0 and not step.allow_nonzero:
        result["errors"].append(f"command returned {returncode}")

    for output in step.expected_outputs:
        validation = validate_output(
            path=repo_path(repo_root, output),
            repo_root=repo_root,
            required_fields=required_for_output(step, output) if output.endswith(".json") else (),
            expected_values=expected_for_output(step, output) if output.endswith(".json") else {},
        )
        result["outputs"].append(validation)
        if not validation["ok"]:
            result["errors"].extend(f"{validation['path']}: {err}" for err in validation["errors"])

    result["ok"] = not result["errors"]
    return result
