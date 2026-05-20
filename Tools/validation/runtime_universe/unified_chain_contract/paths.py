"""Artifact path discovery for unified chain contract validation."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .common import discover_apply_report, discover_first, discover_observer_dir, repo_path


def discover_contract_paths(
    repo_root: Path, args: Any, stamp: str, mode_name: str
) -> dict[str, Path | None]:
    manifest_path = (
        repo_path(repo_root, args.manifest)
        if args.manifest
        else discover_first(
            repo_root,
            [f"output/local_ai_runs/*{stamp}*/pipeline/unified_local_ai_refactor_manifest.json"],
        )
    )
    official_path = (
        repo_path(repo_root, args.official_report)
        if args.official_report
        else repo_root / f"output/validation/{stamp}_phase_official.json"
    )
    gpu0_path = (
        repo_path(repo_root, args.gpu0_report)
        if args.gpu0_report
        else repo_root / f"output/validation/openvino_gpu0_workload_{stamp}.json"
    )
    apply_path = (
        repo_path(repo_root, args.apply_report)
        if args.apply_report
        else discover_apply_report(repo_root, stamp, mode_name)
    )
    product_path = (
        repo_path(repo_root, args.product_separation_report)
        if args.product_separation_report
        else repo_root
        / f"output/validation/patch_suggestion_product_separation_{mode_name}_{stamp}.json"
    )
    review_pr_path = (
        repo_path(repo_root, args.review_pr_report)
        if args.review_pr_report
        else repo_root / f"output/validation/review_pr_prepare_{mode_name}_{stamp}.json"
    )
    observer_dir = (
        repo_path(repo_root, args.observer_dir)
        if args.observer_dir
        else discover_observer_dir(repo_root, stamp)
    )
    ai_events_path = (
        repo_path(repo_root, args.ai_public_events)
        if args.ai_public_events
        else ((observer_dir / "ai_public_events.jsonl") if observer_dir else None)
    )
    tool_capability_path = (
        repo_path(repo_root, args.tool_capability_manifest)
        if args.tool_capability_manifest
        else discover_first(
            repo_root,
            [
                f"output/**/runtime_tool_capability_manifest*{stamp}*.json",
                f"docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_capability_manifest*{stamp}*.json",
                f"output/**/tool_capability_manifest*{stamp}*.json",
            ],
        )
    )
    heap_peer_path = (
        repo_path(repo_root, args.heap_peer_runtime)
        if args.heap_peer_runtime
        else discover_first(
            repo_root,
            [
                f"output/**/heap_peer_runtime*{stamp}*.json",
                f"output/**/runtime_tool_capability_manifest*{stamp}*.json",
                f"docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_capability_manifest*{stamp}*.json",
            ],
        )
    )
    shared_memory_path = (
        repo_path(repo_root, args.shared_memory_evidence)
        if args.shared_memory_evidence
        else discover_first(
            repo_root,
            [
                f"output/**/shared_toolbox_ai_to_ai_bundle*{stamp}*.json",
                f"docs/LOCAL_VALIDATION_EVIDENCE/shared_toolbox_ai_to_ai_bundle*{stamp}*.json",
                f"output/**/full_memory_tool_regeneration_bundle*{stamp}*.json",
                f"docs/LOCAL_VALIDATION_EVIDENCE/full_memory_tool_regeneration_bundle*{stamp}*.json",
                f"output/**/heap_exchange*{stamp}*.json",
            ],
        )
    )
    closure_audit_path = (
        repo_path(repo_root, args.closure_audit_report)
        if args.closure_audit_report
        else discover_first(
            repo_root,
            [
                f"output/**/heap_exchange_closure_audit*{stamp}*.json",
                f"docs/LOCAL_VALIDATION_EVIDENCE/heap_exchange_closure_audit*{stamp}*.json",
            ],
        )
    )
    return {
        "manifest": manifest_path,
        "official": official_path,
        "gpu0": gpu0_path,
        "apply": apply_path,
        "product": product_path,
        "review_pr": review_pr_path,
        "observer_dir": observer_dir,
        "ai_events": ai_events_path,
        "tool_capability": tool_capability_path,
        "heap_peer": heap_peer_path,
        "shared_memory": shared_memory_path,
        "closure_audit": closure_audit_path,
    }
