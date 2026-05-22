"""CLI for generated patch-spec application."""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path
from typing import Any

from .apply_common import (
    PatchOperation,
    apply_operation,
    create_review_branch,
    current_branch,
    git_status_short,
    resolve_output_path,
    split_values,
    unsafe_git_status_short,
    unique_in_order,
    write_json_report,
    write_text_report,
)
from .apply_discovery import (
    discover_latest_manifest,
    infer_manifest_stamp,
    manifest_spec_paths,
    normalize_repo_path,
    read_json_object,
)
from .apply_operations import operations_from_spec
from .apply_report import render_markdown
from .apply_validators import run_validators

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--manifest", default="")
    parser.add_argument("--patch-spec", action="append", default=[])
    parser.add_argument("--discover-root", action="append", default=["output/patch_specs"])
    parser.add_argument("--discover-max-files", type=int, default=50)
    parser.add_argument("--manifest-stamp", default="")
    parser.add_argument(
        "--output",
        default="output/validation/generated_patch_specs_review_pr_apply.json",
    )
    parser.add_argument("--markdown-output", default="")
    parser.add_argument("--max-applied-patches", type=int, default=5)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--allow-dirty", action="store_true")
    parser.add_argument("--create-review-branch", default="")
    parser.add_argument("--allow-dirty-branch", action="store_true")
    parser.add_argument(
        "--allowed-branch-prefix", action="append", default=["CARMINEai/", "codex/"]
    )
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
    unsafe_status_before = unsafe_git_status_short(repo_root)
    if args.apply and unsafe_status_before and not args.allow_dirty:
        errors.append(
            "refusing --apply with source/doc dirty working tree; use --allow-dirty only for reviewed incremental fixes"
        )
    if args.apply and not any(branch.startswith(prefix) for prefix in args.allowed_branch_prefix):
        errors.append(f"refusing --apply on branch {branch!r}; expected allowed branch prefix")

    manifest_path = args.manifest.strip()
    discovered_manifest = ""
    manifest_stamp = infer_manifest_stamp(
        args.manifest_stamp, args.output, args.create_review_branch
    )
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
        manifest_info.update(
            {
                "exists": manifest_full.exists(),
                "json_ok": manifest_error is None,
                "error": manifest_error,
            }
        )
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
            loaded_specs.append(
                {
                    "path": normalize_repo_path(raw_path),
                    "exists": spec_full.exists(),
                    "json_ok": error is None,
                    "kind": data.get("kind") if data else None,
                    "error": error,
                }
            )
            if error or not data:
                errors.append(f"{raw_path}: {error}")
                continue
            discovered_ops, manual = operations_from_spec(data, raw_path)
            operations.extend(discovered_ops)
            manual_review_items.extend(manual)

    operations = operations[: max(0, int(args.max_applied_patches))]
    if args.apply and not errors and not operations:
        reasons = sorted({str(item.get("reason") or "unknown") for item in manual_review_items})
        reason_text = (
            "; ".join(reasons)
            if reasons
            else "no generated patch specs contained allowlisted concrete deterministic operations"
        )
        errors.append(
            f"generated patch specs did not produce a concrete review product: {reason_text}"
        )
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
        "generated_by": "generated_patch_specs_apply.py",
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
        "git_unsafe_status_before": unsafe_status_before,
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
