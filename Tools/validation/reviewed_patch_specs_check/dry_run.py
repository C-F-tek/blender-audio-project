"""Mandatory dry-run execution for reviewed patch specs."""

from __future__ import annotations

import copy
import importlib
import sys
from pathlib import Path
from typing import Any

from .common import repo_relative

def load_patch_runner(repo_root: Path) -> tuple[Any, Any]:
    sys.path.insert(0, str(repo_root))
    module = importlib.import_module("Tools.repo_patch_runner.apply_repo_mods")
    return module.apply_spec, module.PatchError

def dry_run_spec(repo_root: Path, spec: dict[str, Any]) -> tuple[bool, list[dict[str, Any]], str]:
    apply_spec, patch_error = load_patch_runner(repo_root)
    try:
        reports = apply_spec(repo_root, copy.deepcopy(spec), write=False, no_backup=True)
    except patch_error as exc:
        return False, [], str(exc)
    return (
        True,
        [
            {
                "path": repo_relative(report.path, repo_root),
                "changed": report.changed,
                "before_lines": report.before_lines,
                "after_lines": report.after_lines,
                "replacements_applied": report.replacements_applied,
                "bom_removed": report.bom_removed,
            }
            for report in reports
        ],
        "",
    )
