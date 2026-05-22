"""Validators for generated patch-spec application."""

from __future__ import annotations

import shutil
import sys
from pathlib import Path
from typing import Any

from .apply_common import run

def touched_python_files(repo_root: Path, results: list[dict[str, Any]]) -> list[str]:
    return [
        item["path"]
        for item in results
        if item.get("changed")
        and str(item.get("path", "")).replace("\\", "/").endswith(".py")
        and (repo_root / str(item.get("path"))).exists()
    ]

def touched_powershell_files(repo_root: Path, results: list[dict[str, Any]]) -> list[str]:
    return [
        item["path"]
        for item in results
        if item.get("changed")
        and str(item.get("path", "")).replace("\\", "/").endswith(".ps1")
        and (repo_root / str(item.get("path"))).exists()
    ]

def run_validators(
    repo_root: Path, results: list[dict[str, Any]], require_all: bool
) -> tuple[list[dict[str, Any]], list[str], list[str]]:
    validator_results: list[dict[str, Any]] = []
    errors: list[str] = []
    warnings: list[str] = []

    py_files = touched_python_files(repo_root, results)
    if py_files:
        result = run([sys.executable, "-m", "py_compile", *py_files], repo_root)
        validator_results.append({"name": "py_compile", **result})
        if not result["ok"]:
            errors.append("py_compile failed for touched Python files")

    ps1_files = touched_powershell_files(repo_root, results)
    if ps1_files:
        powershell = shutil.which("powershell.exe") or shutil.which("pwsh")
        if powershell:
            for path in ps1_files:
                command = (
                    "$tokens=$null;$errors=$null;"
                    f"$null=[System.Management.Automation.Language.Parser]::ParseFile('{path}',[ref]$tokens,[ref]$errors);"
                    "if($errors.Count -gt 0){$errors | ForEach-Object { Write-Error $_.Message }; exit 1}"
                )
                result = run([powershell, "-NoProfile", "-Command", command], repo_root)
                validator_results.append({"name": "powershell_parser", "path": path, **result})
                if not result["ok"]:
                    errors.append(f"PowerShell parser failed for {path}")
        elif require_all:
            errors.append("PowerShell parser requested but powershell.exe/pwsh was not found")
        else:
            warnings.append("PowerShell parser skipped because powershell.exe/pwsh was not found")

    diff_check = run(["git", "diff", "--check"], repo_root)
    validator_results.append({"name": "git_diff_check", **diff_check})
    if not diff_check["ok"]:
        errors.append("git diff --check failed")

    return validator_results, errors, warnings
