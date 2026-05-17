#!/usr/bin/env python3
"""Build argv for the final unified chain contract gate.

PowerShell remains the Windows wrapper. This helper owns the contract-gate
argument construction so the unified run product chain can be tested without
editing a giant ps1 block for every rule change.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any


def as_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return value != 0
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "y", "on"}
    return False


def repo_path(repo_root: Path, raw: str) -> Path:
    path = Path(str(raw))
    return path if path.is_absolute() else repo_root / path


def existing_or_blank(repo_root: Path, raw: Any) -> str:
    if raw is None:
        return ""
    value = str(raw).strip()
    if not value:
        return ""
    path = repo_path(repo_root, value)
    return value if path.exists() else ""


def discover_first(repo_root: Path, patterns: list[str]) -> str:
    for pattern in patterns:
        matches = sorted(
            repo_root.glob(pattern),
            key=lambda item: item.stat().st_mtime if item.exists() else 0,
            reverse=True,
        )
        if matches:
            try:
                return matches[0].resolve().relative_to(repo_root.resolve()).as_posix()
            except ValueError:
                return matches[0].as_posix()
    return ""


def add_pair(argv: list[str], flag: str, value: str) -> None:
    if value:
        argv.extend([flag, value])


def build_args(context: dict[str, Any]) -> dict[str, Any]:
    repo_root = Path(str(context.get("repo_root") or ".")).resolve()
    stamp = str(context.get("stamp") or "").strip()
    mode_name = str(context.get("mode_name") or "").strip()
    manifest = str(context.get("manifest") or "").strip()
    output_report = str(context.get("output_report") or "").strip()
    markdown_report = str(context.get("markdown_report") or "").strip()

    errors: list[str] = []
    warnings: list[str] = []

    if not stamp:
        errors.append("stamp is required")
    if not mode_name:
        errors.append("mode_name is required")
    if not manifest:
        errors.append("manifest is required")
    if not output_report:
        errors.append("output_report is required")

    apply_report = existing_or_blank(repo_root, context.get("apply_report"))
    product_separation_report = existing_or_blank(
        repo_root, context.get("product_separation_report")
    )
    review_pr_report = existing_or_blank(repo_root, context.get("review_pr_report"))
    tool_capability_manifest = existing_or_blank(repo_root, context.get("tool_capability_manifest"))
    tool_usage_telemetry = existing_or_blank(repo_root, context.get("tool_usage_telemetry"))
    if not tool_capability_manifest:
        tool_capability_manifest = discover_first(
            repo_root,
            [
                f"output/**/runtime_tool_capability_manifest*{stamp}*.json",
                f"docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_capability_manifest*{stamp}*.json",
                f"output/**/tool_capability_manifest*{stamp}*.json",
            ],
        )
    if not tool_usage_telemetry:
        tool_usage_telemetry = discover_first(
            repo_root,
            [
                f"output/**/full_toolbox_run_telemetry_summary*{stamp}*.json",
                f"docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_run_telemetry_summary*{stamp}*.json",
                f"output/**/tool_usage*{stamp}*.json",
                f"output/**/runtime_tool_usage*{stamp}*.json",
            ],
        )
    heap_peer_runtime = existing_or_blank(repo_root, context.get("heap_peer_runtime"))
    if not heap_peer_runtime:
        heap_peer_runtime = discover_first(
            repo_root,
            [
                f"output/**/heap_peer_runtime*{stamp}*.json",
                f"output/**/runtime_tool_capability_manifest*{stamp}*.json",
                f"docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_capability_manifest*{stamp}*.json",
                f"output/**/full_toolbox_run_telemetry_summary*{stamp}*.json",
                f"docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_run_telemetry_summary*{stamp}*.json",
            ],
        )
    shared_memory_evidence = existing_or_blank(repo_root, context.get("shared_memory_evidence"))
    if not shared_memory_evidence:
        shared_memory_evidence = discover_first(
            repo_root,
            [
                f"output/**/shared_toolbox_ai_to_ai_bundle*{stamp}*.json",
                f"docs/LOCAL_VALIDATION_EVIDENCE/shared_toolbox_ai_to_ai_bundle*{stamp}*.json",
                f"output/**/full_memory_tool_regeneration_bundle*{stamp}*.json",
                f"docs/LOCAL_VALIDATION_EVIDENCE/full_memory_tool_regeneration_bundle*{stamp}*.json",
                f"output/**/heap_exchange*{stamp}*.json",
            ],
        )
    closure_audit_report = existing_or_blank(repo_root, context.get("closure_audit_report"))
    if not closure_audit_report:
        closure_audit_report = discover_first(
            repo_root,
            [
                f"output/**/heap_exchange_closure_audit*{stamp}*.json",
                f"docs/LOCAL_VALIDATION_EVIDENCE/heap_exchange_closure_audit*{stamp}*.json",
            ],
        )

    requested_apply_report = str(context.get("apply_report") or "").strip()
    requested_product_report = str(context.get("product_separation_report") or "").strip()
    requested_review_report = str(context.get("review_pr_report") or "").strip()

    if requested_apply_report and not apply_report:
        warnings.append(f"apply_report not found, omitted: {requested_apply_report}")
    if requested_product_report and not product_separation_report:
        warnings.append(f"product_separation_report not found, omitted: {requested_product_report}")
    if requested_review_report and not review_pr_report:
        warnings.append(f"review_pr_report not found, omitted: {requested_review_report}")

    require_ai_exchange = any(
        as_bool(context.get(key))
        for key in (
            "use_primary_advisory_provider",
            "run_multistep_provider_workflow",
            "use_ollama_advisory",
            "run_ollama_probe",
            "open_extended_observer_consoles",
        )
    )
    require_provider_tool_evidence = (
        as_bool(context.get("require_provider_tool_evidence")) or require_ai_exchange
    )
    require_heap_peer_runtime = (
        as_bool(context.get("require_heap_peer_runtime")) or require_ai_exchange
    )
    require_shared_memory_evidence = (
        as_bool(context.get("require_shared_memory_evidence")) or require_ai_exchange
    )
    require_heap_closure_audit = (
        as_bool(context.get("require_heap_closure_audit")) or require_ai_exchange
    )
    require_concrete_patch_specs = as_bool(context.get("review_pr_from_generated_patch_specs"))
    require_review_pr_product = as_bool(context.get("prepare_review_pr")) and (
        as_bool(context.get("review_pr_from_generated_patch_specs"))
        or as_bool(context.get("review_pr_apply_deterministic_suggestions"))
    )

    argv = [
        "Tools/validation/check_unified_chain_contract.py",
        "--repo-root",
        ".",
        "--stamp",
        stamp,
        "--mode-name",
        mode_name,
        "--manifest",
        manifest,
        "--output",
        output_report,
    ]
    if markdown_report:
        argv.extend(["--markdown-output", markdown_report])

    add_pair(argv, "--apply-report", apply_report)
    add_pair(argv, "--product-separation-report", product_separation_report)
    add_pair(argv, "--review-pr-report", review_pr_report)
    add_pair(argv, "--tool-capability-manifest", tool_capability_manifest)
    add_pair(argv, "--tool-usage-telemetry", tool_usage_telemetry)
    add_pair(argv, "--heap-peer-runtime", heap_peer_runtime)
    add_pair(argv, "--shared-memory-evidence", shared_memory_evidence)
    add_pair(argv, "--closure-audit-report", closure_audit_report)

    if require_ai_exchange:
        argv.append("--require-ai-exchange")
    if require_provider_tool_evidence:
        argv.append("--require-provider-tool-evidence")
    if require_heap_peer_runtime:
        argv.append("--require-heap-peer-runtime")
    if require_shared_memory_evidence:
        argv.append("--require-shared-memory-evidence")
    if require_heap_closure_audit:
        argv.append("--require-heap-closure-audit")
    if require_concrete_patch_specs:
        argv.append("--require-concrete-patch-specs")
    if require_review_pr_product:
        argv.append("--require-review-pr-product")

    return {
        "schema_version": 1,
        "kind": "unified_chain_contract_args",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "repo_root": repo_root.as_posix(),
        "passed": not errors,
        "argv": argv,
        "derived": {
            "require_ai_exchange": require_ai_exchange,
            "require_provider_tool_evidence": require_provider_tool_evidence,
            "require_heap_peer_runtime": require_heap_peer_runtime,
            "require_shared_memory_evidence": require_shared_memory_evidence,
            "require_heap_closure_audit": require_heap_closure_audit,
            "require_concrete_patch_specs": require_concrete_patch_specs,
            "require_review_pr_product": require_review_pr_product,
        },
        "inputs": {
            "stamp": stamp,
            "mode_name": mode_name,
            "manifest": manifest,
            "apply_report": apply_report,
            "product_separation_report": product_separation_report,
            "review_pr_report": review_pr_report,
            "tool_capability_manifest": tool_capability_manifest,
            "tool_usage_telemetry": tool_usage_telemetry,
            "heap_peer_runtime": heap_peer_runtime,
            "shared_memory_evidence": shared_memory_evidence,
            "closure_audit_report": closure_audit_report,
            "output_report": output_report,
            "markdown_report": markdown_report,
        },
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "errors": errors,
        "warnings": warnings,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--context", required=True)
    parser.add_argument("--output", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    context_path = Path(args.context)
    output_path = Path(args.output)
    context = json.loads(context_path.read_text(encoding="utf-8-sig"))
    if not isinstance(context, dict):
        raise SystemExit("context JSON root must be an object")

    report = build_args(context)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
