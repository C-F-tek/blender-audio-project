
#!/usr/bin/env python3
"""Apply concrete generated patch specs and emit a review-PR-compatible report.

The tool is a narrow bridge between generated patch specs and the existing
patch-suggestion/review-PR product path. It reuses
Tools.ai.patch_suggestion_bundle.operations.apply_operation for deterministic
writes and emits kind=patch_suggestion_bundle_apply so prepare_review_pr.py can
consume the report with --auto-include-from-apply-report.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from Tools.ai.patch_suggestion_bundle.common import (
    PatchOperation,
    current_branch,
    git_status_short,
    load_json,
    repo_relative,
    split_values,
    unique_in_order,
)
from Tools.ai.patch_suggestion_bundle.git_branch import create_review_branch
from Tools.ai.patch_suggestion_bundle.operations import apply_operation, normalize_operation
from Tools.validation.report_utils import resolve_output_path, write_json_report, write_text_report

CONCRETE_OPERATION_NAMES = {
    "replace_once",
    "append_once",
    "insert_after_once",
    "insert_before_once",
    "write_file",
}
MANUAL_OR_DRAFT_OPERATIONS = {
    "manual_patch_suggestion",
    "proposal_only",
    "manual_review_only",
}
DENIED_TARGET_PREFIXES = (
    "output/",
    "indexAI/code_chunks/",
    "indexAI/project_code_chunks/",
    "docs/LOCAL_VALIDATION_EVIDENCE/",
    "renders/",
)
DENIED_TARGET_SUFFIXES = (
    ".db",
    ".sqlite",
    ".sqlite3",
    ".sqlite-wal",
    ".sqlite-shm",
)

STAMP_RE = re.compile(r"\d{8}-\d{6}")


def run(command: list[str], cwd: Path, timeout: int = 120) -> dict[str, Any]:
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
        return {
            "command": command,
            "returncode": result.returncode,
            "stdout": result.stdout.strip()[:4000],
            "stderr": result.stderr.strip()[:4000],
            "ok": result.returncode == 0,
        }
    except subprocess.TimeoutExpired as exc:
        return {
            "command": command,
            "returncode": 124,
            "stdout": str(exc.stdout or "")[:4000],
            "stderr": str(exc.stderr or "")[:4000],
            "ok": False,
            "error": f"TimeoutExpired: {timeout}s",
        }


def normalize_repo_path(path: str) -> str:
    return str(path or "").strip().replace("\\", "/").lstrip("./")


def is_denied_target(path: str) -> str | None:
    normalized = normalize_repo_path(path)
    lower = normalized.lower()
    if not normalized:
        return "empty target path"
    if any(lower.startswith(prefix.lower()) for prefix in DENIED_TARGET_PREFIXES):
        return "target is generated/runtime/evidence path"
    if lower.endswith(DENIED_TARGET_SUFFIXES):
        return "target is a database/runtime artifact"
    return None


def read_json_object(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    data, error = load_json(path)
    if error:
        return None, error
    if not isinstance(data, dict):
        return None, "JSON root must be an object"
    return data, None


def discover_latest_manifest(repo_root: Path, roots: list[str], max_files: int, manifest_stamp: str = "") -> str:
    candidates: list[Path] = []
    for raw_root in roots:
        root = (repo_root / raw_root).resolve()
        if not root.exists():
            continue
        candidates.extend(path for path in root.rglob("*_manifest.json") if path.is_file())
    candidates = sorted(candidates, key=lambda item: item.stat().st_mtime, reverse=True)
    scanned = 0
    for path in candidates[:max_files]:
        scanned += 1
        relative = repo_relative(path, repo_root)
        if manifest_stamp and manifest_stamp not in relative:
            continue
        data, error = read_json_object(path)
        if error or not data:
            continue
        if data.get("kind") in {"proposal_patch_spec_manifest", "reviewed_patch_spec_manifest"}:
            return relative
    return ""


def infer_manifest_stamp(*values: str) -> str:
    for value in values:
        matches = STAMP_RE.findall(str(value or ""))
        if matches:
            return matches[-1]
    return ""


def manifest_spec_paths(data: dict[str, Any]) -> list[str]:
    paths: list[str] = []
    for item in data.get("specs") or []:
        if isinstance(item, dict) and isinstance(item.get("path"), str):
            paths.append(item["path"])
    for key in ("patch_specs", "reviewed_specs", "spec_paths"):
        value = data.get(key)
        if isinstance(value, list):
            paths.extend(str(item) for item in value if str(item).strip())
    return unique_in_order(paths)


def replacement_to_operation(path: str, replacement: dict[str, Any], source_id: str) -> PatchOperation | None:
    replacement_type = str(replacement.get("type") or "").strip().lower()
    if replacement_type == "exact":
        old = replacement.get("old")
        new = replacement.get("new")
        if isinstance(old, str) and isinstance(new, str):
            return PatchOperation(
                operation="replace_once",
                path=path,
                find=old,
                replace=new,
                source_id=source_id,
                family="generated_patch_spec",
                description="exact replacement from generated patch spec",
            )
    if replacement_type == "insert_after":
        anchor = replacement.get("anchor")
        insert = replacement.get("insert")
        if isinstance(anchor, str) and isinstance(insert, str):
            return PatchOperation(
                operation="insert_after_once",
                path=path,
                find=anchor,
                content=insert,
                source_id=source_id,
                family="generated_patch_spec",
                description="insert_after replacement from generated patch spec",
            )
    if replacement_type == "insert_before":
        anchor = replacement.get("anchor")
        insert = replacement.get("insert")
        if isinstance(anchor, str) and isinstance(insert, str):
            return PatchOperation(
                operation="insert_before_once",
                path=path,
                find=anchor,
                content=insert,
                source_id=source_id,
                family="generated_patch_spec",
                description="insert_before replacement from generated patch spec",
            )
    return None


def operations_from_spec(data: dict[str, Any], spec_path: str) -> tuple[list[PatchOperation], list[dict[str, Any]]]:
    operations: list[PatchOperation] = []
    manual: list[dict[str, Any]] = []
    raw_operations = data.get("operations")
    if not isinstance(raw_operations, list):
        manual.append({"id": spec_path, "reason": "spec operations is not a list", "target_files": []})
        return operations, manual

    for index, raw in enumerate(raw_operations):
        if not isinstance(raw, dict):
            manual.append({"id": f"{spec_path}#{index}", "reason": "operation is not an object", "target_files": []})
            continue

        source_id = str(raw.get("proposal_id") or raw.get("id") or f"{spec_path}#{index}")
        raw_operation = str(raw.get("operation") or raw.get("op") or raw.get("action") or "").strip().lower().replace("-", "_")
        raw_path = normalize_repo_path(str(raw.get("path") or raw.get("target_file") or raw.get("file") or ""))
        denied = is_denied_target(raw_path)
        if denied:
            manual.append({"id": source_id, "reason": denied, "target_files": [raw_path] if raw_path else []})
            continue

        if raw_operation in MANUAL_OR_DRAFT_OPERATIONS or raw.get("draft_status") == "needs_concrete_replacements":
            replacements = raw.get("replacements")
            if not replacements:
                manual.append({
                    "id": source_id,
                    "reason": "metadata-only draft operation has no concrete replacements",
                    "target_files": [raw_path] if raw_path else [],
                    "draft_status": raw.get("draft_status"),
                })
                continue

        normalized = normalize_operation(raw)
        if normalized and normalized.operation in CONCRETE_OPERATION_NAMES:
            operations.append(normalized)
            continue

        replacements = raw.get("replacements")
        if isinstance(replacements, list) and raw_path:
            converted = 0
            for repl_index, replacement in enumerate(replacements):
                if not isinstance(replacement, dict):
                    continue
                operation = replacement_to_operation(raw_path, replacement, f"{source_id}:{repl_index}")
                if operation:
                    operations.append(operation)
                    converted += 1
            if converted:
                continue

        manual.append({
            "id": source_id,
            "reason": "no allowlisted concrete deterministic operation found",
            "target_files": [raw_path] if raw_path else [],
            "operation": raw_operation,
        })

    return operations, manual


def touched_python_files(repo_root: Path, results: list[dict[str, Any]]) -> list[str]:
    return [
        item["path"]
        for item in results
        if item.get("changed") and str(item.get("path", "")).replace("\\", "/").endswith(".py")
        and (repo_root / str(item.get("path"))).exists()
    ]


def touched_powershell_files(repo_root: Path, results: list[dict[str, Any]]) -> list[str]:
    return [
        item["path"]
        for item in results
        if item.get("changed") and str(item.get("path", "")).replace("\\", "/").endswith(".ps1")
        and (repo_root / str(item.get("path"))).exists()
    ]


def run_validators(repo_root: Path, results: list[dict[str, Any]], require_all: bool) -> tuple[list[dict[str, Any]], list[str], list[str]]:
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


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Generated Patch Specs Review PR Apply",
        "",
        f"- Passed: `{report.get('passed')}`",
        f"- Apply requested: `{report.get('apply_requested')}`",
        f"- Patch application performed: `{report.get('patch_application_performed')}`",
        f"- Operation count: `{report.get('operation_count')}`",
        f"- Changed count: `{report.get('changed_count')}`",
        f"- Applied count: `{report.get('applied_count')}`",
        f"- Manual review required: `{report.get('manual_review_required')}`",
        "",
        "## Results",
        "",
    ]
    for item in report.get("results") or []:
        lines.append(f"- `{item.get('path')}` op=`{item.get('operation')}` changed=`{item.get('changed')}` applied=`{item.get('applied')}` ok=`{item.get('ok')}`")
    if report.get("manual_review_items"):
        lines.extend(["", "## Manual review items", ""])
        for item in report["manual_review_items"][:50]:
            lines.append(f"- `{item.get('id')}` {item.get('reason')} targets=`{item.get('target_files')}`")
    if report.get("errors"):
        lines.extend(["", "## Errors", ""])
        lines.extend(f"- {error}" for error in report["errors"])
    if report.get("warnings"):
        lines.extend(["", "## Warnings", ""])
        lines.extend(f"- {warning}" for warning in report["warnings"])
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--manifest", default="")
    parser.add_argument("--patch-spec", action="append", default=[])
    parser.add_argument("--discover-root", action="append", default=["output/patch_specs"])
    parser.add_argument("--discover-max-files", type=int, default=50)
    parser.add_argument("--manifest-stamp", default="")
    parser.add_argument("--output", default="output/validation/generated_patch_specs_review_pr_apply.json")
    parser.add_argument("--markdown-output", default="")
    parser.add_argument("--max-applied-patches", type=int, default=5)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--allow-dirty", action="store_true")
    parser.add_argument("--create-review-branch", default="")
    parser.add_argument("--allow-dirty-branch", action="store_true")
    parser.add_argument("--allowed-branch-prefix", action="append", default=["CARMINEai/", "codex/"])
    parser.add_argument("--require-all-validators", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    errors: list[str] = []
    warnings: list[str] = []
    loaded_specs: list[dict[str, Any]] = []

    branch_prepare = {
        "requested": bool(args.create_review_branch),
        "branch": args.create_review_branch,
        "created": False,
        "switched": False,
        "errors": [],
        "warnings": [],
    }
    if args.create_review_branch:
        branch_prepare = create_review_branch(
            repo_root,
            args.create_review_branch,
            allowed_prefixes=list(args.allowed_branch_prefix),
            allow_dirty=bool(args.allow_dirty_branch),
        )
        errors.extend(branch_prepare.get("errors") or [])
        warnings.extend(branch_prepare.get("warnings") or [])

    branch = current_branch(repo_root)
    status_before = git_status_short(repo_root)
    if args.apply and status_before and not args.allow_dirty:
        errors.append("refusing --apply with dirty working tree; use --allow-dirty only for reviewed incremental fixes")
    if args.apply and not any(branch.startswith(prefix) for prefix in args.allowed_branch_prefix):
        errors.append(f"refusing --apply on branch {branch!r}; expected allowed branch prefix")

    manifest_path = args.manifest.strip()
    discovered_manifest = ""
    manifest_stamp = infer_manifest_stamp(args.manifest_stamp, args.output, args.create_review_branch)
    if not manifest_path and not args.patch_spec:
        discovered_manifest = discover_latest_manifest(
            repo_root,
            split_values(args.discover_root),
            args.discover_max_files,
            manifest_stamp,
        )
        manifest_path = discovered_manifest

    spec_paths = split_values(args.patch_spec)
    manifest_info: dict[str, Any] = {
        "requested": bool(args.manifest),
        "path": manifest_path,
        "discovered": discovered_manifest,
        "discovery_filter_stamp": manifest_stamp,
    }
    if manifest_path:
        manifest_full = (repo_root / manifest_path).resolve()
        manifest_data, manifest_error = read_json_object(manifest_full)
        manifest_info.update({
            "exists": manifest_full.exists(),
            "json_ok": manifest_error is None,
            "error": manifest_error,
        })
        if manifest_error or not manifest_data:
            errors.append(f"{manifest_path}: {manifest_error}")
        else:
            manifest_info["kind"] = manifest_data.get("kind")
            spec_paths.extend(manifest_spec_paths(manifest_data))

    spec_paths = unique_in_order(spec_paths)
    if not spec_paths and not errors:
        errors.append("no generated patch specs supplied or discovered")

    operations: list[PatchOperation] = []
    manual_review_items: list[dict[str, Any]] = []
    if not errors:
        for raw_path in spec_paths:
            spec_full = (repo_root / raw_path).resolve()
            data, error = read_json_object(spec_full)
            loaded_specs.append({
                "path": normalize_repo_path(raw_path),
                "exists": spec_full.exists(),
                "json_ok": error is None,
                "kind": data.get("kind") if data else None,
                "error": error,
            })
            if error or not data:
                errors.append(f"{raw_path}: {error}")
                continue
            discovered_ops, manual = operations_from_spec(data, raw_path)
            operations.extend(discovered_ops)
            manual_review_items.extend(manual)

    operations = operations[: max(0, int(args.max_applied_patches))]
    results: list[dict[str, Any]] = []
    if not errors:
        for operation in operations:
            results.append(apply_operation(repo_root, operation, bool(args.apply)))

    failed = [item for item in results if not item.get("ok")]
    changed = [item for item in results if item.get("changed")]
    applied = [item for item in results if item.get("applied")]
    errors.extend(f"{item.get('path')}: {item.get('error')}" for item in failed)

    validator_results: list[dict[str, Any]] = []
    validator_errors: list[str] = []
    validator_warnings: list[str] = []
    if args.apply and changed and not failed:
        validator_results, validator_errors, validator_warnings = run_validators(
            repo_root,
            results,
            require_all=bool(args.require_all_validators),
        )
        errors.extend(validator_errors)
        warnings.extend(validator_warnings)

    report = {
        "schema_version": 1,
        "kind": "patch_suggestion_bundle_apply",
        "generated_by": "apply_generated_patch_specs_for_review_pr.py",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "repo_root": repo_root.as_posix(),
        "branch": branch,
        "apply_requested": bool(args.apply),
        "manifest": manifest_info,
        "loaded_specs": loaded_specs,
        "provider_execution_performed": False,
        "blender_execution_performed": False,
        "ffmpeg_execution_performed": False,
        "sqlite_writes_performed": False,
        "git_commit_performed": False,
        "git_push_performed": False,
        "git_review_branch_prepare": branch_prepare,
        "patch_application_performed": bool(applied),
        "source_writes_performed": bool(applied),
        "operation_count": len(operations),
        "changed_count": len(changed),
        "applied_count": len(applied),
        "failed_count": len(failed),
        "manual_review_required": bool(manual_review_items or failed),
        "manual_review_items": manual_review_items[:200],
        "results": results,
        "validators": validator_results,
        "git_status_before": status_before,
        "git_status_after": git_status_short(repo_root),
        "passed": not errors,
        "errors": errors,
        "warnings": warnings,
    }

    output = resolve_output_path(repo_root, args.output)
    print(write_json_report(report, output), end="")
    if args.markdown_output:
        markdown = resolve_output_path(repo_root, args.markdown_output)
        write_text_report(render_markdown(report), markdown)
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
