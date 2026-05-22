"""Builder/report logic for agent-review patch bundles."""

from __future__ import annotations

import argparse
import zipfile
from pathlib import Path
from typing import Any

from .patch_bundle_common import (
    DEFAULT_BASENAME,
    collect_operations,
    load_patch_plan,
    now_iso,
    repo_rel,
    resolve_path,
    safe_json,
    stamp,
)
from .patch_bundle_sources import bundle_runner_source, readme_source, validation_script_source

def build_bundle(args: argparse.Namespace) -> dict[str, Any]:
    repo_root = Path(args.repo_root).resolve()
    patch_plan_path = resolve_path(repo_root, args.patch_plan)
    output_dir = resolve_path(repo_root, args.output_dir)
    errors: list[str] = []
    warnings: list[str] = []
    patch_plan, load_errors = load_patch_plan(patch_plan_path)
    errors.extend(f"patch_plan: {error}" for error in load_errors)

    operations: list[dict[str, Any]] = []
    skipped: list[dict[str, str]] = []
    if patch_plan:
        if patch_plan.get("kind") != "agent_review_patch_plan":
            warnings.append(f"unexpected patch plan kind: {patch_plan.get('kind')}")
        operations, skipped = collect_operations(patch_plan, repo_root)
    if not operations and not errors:
        errors.append("no supported Markdown operations were produced from the patch plan")

    bundle_stamp = args.stamp or stamp()
    bundle_name = f"{args.basename}_{bundle_stamp}"
    bundle_root = output_dir / bundle_name
    patches_dir = bundle_root / "patches"
    scripts_dir = bundle_root / "scripts"
    bundle_zip = output_dir / f"{bundle_name}.zip"

    if args.write_bundle and not errors:
        patches_dir.mkdir(parents=True, exist_ok=True)
        scripts_dir.mkdir(parents=True, exist_ok=True)
        manifest = {
            "schema_version": 1,
            "kind": "agent_review_patch_bundle_manifest",
            "generated_at": now_iso(),
            "repo_root": str(repo_root),
            "patch_plan": repo_rel(patch_plan_path, repo_root),
            "operation_count": len(operations),
            "skipped_candidate_count": len(skipped),
            "operations": operations,
            "skipped_candidates": skipped,
            "guardrails": {
                "dry_run_default": True,
                "explicit_apply_required": True,
                "markdown_managed_blocks_only": True,
                "provider_execution_performed": False,
                "patch_application_performed_by_builder": False,
                "sqlite_write_performed": False,
                "persistent_memory_write_performed": False,
            },
        }
        (patches_dir / "manifest.json").write_text(safe_json(manifest) + "\n", encoding="utf-8")
        (bundle_root / "run_patch_bundle.py").write_text(
            bundle_runner_source(), encoding="utf-8", newline="\n"
        )
        (scripts_dir / "validate_after_patch.ps1").write_text(
            validation_script_source(), encoding="utf-8", newline="\n"
        )
        (bundle_root / "README.md").write_text(
            readme_source(bundle_name, len(operations), len(skipped)),
            encoding="utf-8",
            newline="\n",
        )
        with zipfile.ZipFile(bundle_zip, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            for path in sorted(bundle_root.rglob("*")):
                if path.is_file():
                    zf.write(path, path.relative_to(bundle_root.parent).as_posix())

    report = {
        "schema_version": 1,
        "kind": "agent_review_patch_bundle_builder",
        "generated_at": now_iso(),
        "repo_root": str(repo_root),
        "passed": not errors,
        "errors": errors,
        "warnings": warnings,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "sqlite_write_performed": False,
        "persistent_memory_write_performed": False,
        "manual_review_required": True,
        "patch_plan": repo_rel(patch_plan_path, repo_root),
        "bundle_name": bundle_name,
        "bundle_dir": repo_rel(bundle_root, repo_root),
        "bundle_zip": repo_rel(bundle_zip, repo_root) if bundle_zip.exists() else "",
        "write_bundle": bool(args.write_bundle),
        "operation_count": len(operations),
        "skipped_candidate_count": len(skipped),
        "operations": [
            {key: value for key, value in operation.items() if key != "block"}
            for operation in operations
        ],
        "skipped_candidates": skipped,
        "guardrails": {
            "report_only_builder": True,
            "dry_run_default_bundle": True,
            "explicit_apply_required": True,
            "markdown_managed_blocks_only": True,
            "provider_execution_performed": False,
            "patch_application_performed": False,
            "sqlite_write_performed": False,
            "persistent_memory_write_performed": False,
        },
    }
    return report

def render_markdown(report: dict[str, Any]) -> str:
    lines = ["# Agent Review Patch Bundle Builder", ""]
    lines.append(f"- Passed: `{report['passed']}`")
    lines.append(f"- Bundle: `{report.get('bundle_name')}`")
    lines.append(f"- Bundle ZIP: `{report.get('bundle_zip')}`")
    lines.append(f"- Operation count: `{report['operation_count']}`")
    lines.append(f"- Skipped candidates: `{report['skipped_candidate_count']}`")
    lines.append(f"- Patch application performed: `{report['patch_application_performed']}`")
    lines.append(f"- SQLite write performed: `{report['sqlite_write_performed']}`")
    if report.get("errors"):
        lines.append("")
        lines.append("## Errors")
        lines.extend(f"- {error}" for error in report["errors"])
    if report.get("warnings"):
        lines.append("")
        lines.append("## Warnings")
        lines.extend(f"- {warning}" for warning in report["warnings"])
    lines.append("")
    lines.append("## Operations")
    if not report.get("operations"):
        lines.append("- none")
    for operation in report.get("operations", []):
        lines.append(f"- `{operation.get('id')}` -> `{operation.get('target')}`")
    if report.get("skipped_candidates"):
        lines.append("")
        lines.append("## Skipped candidates")
        for item in report["skipped_candidates"]:
            lines.append(f"- `{item.get('id')}` `{item.get('target', '')}`: {item.get('reason')}")
    return "\n".join(lines) + "\n"
