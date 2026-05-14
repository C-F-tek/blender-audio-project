#!/usr/bin/env python3
"""Safe apply helpers for CODE_PRODUCT_FULL_PATCH intake."""

from __future__ import annotations

import re
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any

FENCE_RE = re.compile(r"```diff\n(.*?)\n```", re.DOTALL)
INTEGRATED_STATUSES = {
    "already_integrated",
    "already_integrated_with_context_drift",
    "already_integrated_truncated_dump",
}


def normalize_target(raw: str) -> str:
    return str(raw or "").strip().strip("`").replace("\\", "/")


def repo_rel(repo_root: Path, value: str | Path) -> str:
    path = Path(value)
    if not path.is_absolute():
        path = repo_root / path
    try:
        return path.resolve(strict=False).relative_to(repo_root.resolve(strict=False)).as_posix()
    except ValueError:
        return str(value).replace("\\", "/")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def code_block(body: str) -> str:
    match = FENCE_RE.search(body)
    return match.group(1).strip("\n") if match else ""


def new_file_payload_content(payload: str) -> str:
    return payload.split("\n\n", 1)[1] if "\n\n" in payload else ""


def safe_apply_sections(
    repo_root: Path,
    output_dir: Path,
    raw_sections: list[dict[str, str]],
    analyzed: list[dict[str, Any]],
) -> dict[str, Any]:
    allowed = {*INTEGRATED_STATUSES, "forward_applicable", "forward_applicable_new_file"}
    report: dict[str, Any] = {
        "performed": False,
        "applied_count": 0,
        "already_integrated_count": 0,
        "results": [],
        "errors": [],
        "warnings": [],
        "backup_dir": "",
    }
    if [item for item in analyzed if item.get("status") not in allowed]:
        report["errors"].append("safe apply blocked: at least one section is not safe")
        return report
    raw_by_target = {normalize_target(item["target"]): item for item in raw_sections}
    eligible = [
        item
        for item in analyzed
        if item.get("status") in {"forward_applicable", "forward_applicable_new_file"}
    ]
    report["already_integrated_count"] = sum(
        1 for item in analyzed if item.get("status") in INTEGRATED_STATUSES
    )
    if not eligible:
        report["warnings"].append("nothing to apply; all sections are already integrated")
        return report
    backup_root = output_dir / "safe_apply_backups" / datetime.now().strftime("%Y%m%d-%H%M%S")
    apply_dir = output_dir / "safe_apply_patches"
    apply_dir.mkdir(parents=True, exist_ok=True)
    report["backup_dir"] = repo_rel(repo_root, backup_root)
    for item in eligible:
        target = str(item.get("target_file") or "")
        payload = code_block(raw_by_target.get(target, {}).get("body", ""))
        target_path = repo_root / target
        result: dict[str, Any] = {"target_file": target, "applied": False}
        if item.get("status") == "forward_applicable":
            if target_path.exists():
                backup_path = backup_root / target
                backup_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(target_path, backup_path)
                result["backup"] = repo_rel(repo_root, backup_path)
            patch_name = re.sub(r"[^A-Za-z0-9_.-]+", "_", target).strip("_") or "patch"
            patch_path = apply_dir / f"{patch_name}.diff"
            write_text(patch_path, payload)
            completed = subprocess.run(
                ["git", "apply", "--whitespace=nowarn", str(patch_path)],
                cwd=repo_root,
                text=True,
                capture_output=True,
                check=False,
                timeout=120,
            )
            result.update(
                {
                    "returncode": completed.returncode,
                    "stderr_tail": (completed.stderr or "")[-2000:],
                    "patch_file": repo_rel(repo_root, patch_path),
                }
            )
            result["applied"] = completed.returncode == 0
        else:
            if target_path.exists():
                result.update(returncode=2, stderr_tail="target appeared before new-file write")
            else:
                write_text(target_path, new_file_payload_content(payload))
                result.update(returncode=0, applied=True)
        report["applied_count"] += 1 if result["applied"] else 0
        report["performed"] = bool(report["applied_count"])
        if not result["applied"]:
            report["errors"].append(f"{target}: safe apply failed")
        report["results"].append(result)
    return report
