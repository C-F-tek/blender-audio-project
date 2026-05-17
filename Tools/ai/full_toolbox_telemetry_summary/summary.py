"""Full-toolbox telemetry report assembly."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from .common import now_iso, read_optional_json, safe_list
from .provider import npu_final_review_summary, peer_exchange_summary, provider_evidence_summary
from .runtime import (
    compact_paths,
    compact_patch_plan,
    compact_performance,
    compact_recommendation,
    line_count_csv_summary,
    runtime_heap_summary,
)

def build_summary(args: argparse.Namespace) -> dict[str, Any]:
    repo_root = Path(args.repo_root).resolve()
    warnings: list[str] = []
    errors: list[str] = []

    decision_loop, decision_errors, decision_path = read_optional_json(
        repo_root, args.decision_loop
    )
    recommendations, recommendation_errors, recommendations_path = read_optional_json(
        repo_root, args.recommendations
    )
    patch_plan, patch_plan_errors, patch_plan_path = read_optional_json(repo_root, args.patch_plan)
    repository_map, repository_errors, repository_path = read_optional_json(
        repo_root, args.repository_consistency
    )
    repository_smoke, repository_smoke_errors, repository_smoke_path = read_optional_json(
        repo_root, args.repository_consistency_smoke
    )
    gpu_npu_sync, gpu_npu_errors, gpu_npu_path = read_optional_json(repo_root, args.gpu_npu_sync)
    orchestrator, orchestrator_errors, orchestrator_path = read_optional_json(
        repo_root, args.orchestrator
    )
    gpu_report, gpu_errors, gpu_path = read_optional_json(repo_root, args.gpu_report)
    peer_exchange, peer_errors, peer_path = read_optional_json(repo_root, args.peer_exchange)
    peer_contract, peer_contract_errors, peer_contract_path = read_optional_json(
        repo_root, args.peer_contract
    )
    heap_telemetry, heap_telemetry_errors, heap_telemetry_path = read_optional_json(
        repo_root, args.provider_runtime_heap_telemetry
    )
    heap_snapshot, heap_snapshot_errors, heap_snapshot_path = read_optional_json(
        repo_root, args.provider_runtime_heap_snapshot
    )
    heap_live_reports: list[dict[str, Any]] = []
    heap_live_paths: list[str] = []
    for raw_path in safe_list(args.provider_runtime_heap_live_signal):
        live_report, live_errors, live_path = read_optional_json(repo_root, str(raw_path))
        warnings.extend(live_errors)
        if live_path:
            heap_live_paths.append(live_path)
        if live_report:
            heap_live_reports.append(live_report)
    line_count_csv, line_count_csv_warnings = line_count_csv_summary(repo_root, args.line_count_csv)

    hard_inputs = {
        "decision_loop": decision_loop,
        "recommendations": recommendations,
        "patch_plan": patch_plan,
    }
    errors.extend(decision_errors)
    errors.extend(recommendation_errors)
    errors.extend(patch_plan_errors)
    warnings.extend(repository_errors)
    warnings.extend(repository_smoke_errors)
    warnings.extend(gpu_npu_errors)
    warnings.extend(orchestrator_errors)
    warnings.extend(gpu_errors)
    warnings.extend(peer_errors)
    warnings.extend(peer_contract_errors)
    warnings.extend(heap_telemetry_errors)
    warnings.extend(heap_snapshot_errors)
    warnings.extend(line_count_csv_warnings)

    for name, data in hard_inputs.items():
        if not data:
            errors.append(f"required telemetry input unavailable: {name}")

    recommendation_items = [
        item for item in safe_list(recommendations.get("recommendations")) if isinstance(item, dict)
    ]
    patch_plan_items = [
        item for item in safe_list(patch_plan.get("patch_plans")) if isinstance(item, dict)
    ]
    workflow_like = {
        "passed": decision_loop.get("passed"),
        "recommendation_count": decision_loop.get("recommendation_count")
        or recommendations.get("recommendation_count")
        or len(recommendation_items),
        "patch_plan_count": decision_loop.get("patch_plan_count")
        or patch_plan.get("patch_plan_count")
        or len(patch_plan_items),
        "deterministic_synthesizer_used": decision_loop.get("deterministic_synthesizer_used"),
        "patch_plan_fallback_used": decision_loop.get("patch_plan_fallback_used")
        or patch_plan.get("fallback_used"),
        "bundle_validation_passed": args.bundle_validation_passed,
        "evidence_to_commit": compact_paths(args.evidence_to_commit, limit=32),
    }

    provider_evidence = provider_evidence_summary(orchestrator, gpu_report)
    peer_evidence = peer_exchange_summary(peer_exchange, peer_contract)
    heap_evidence = runtime_heap_summary(heap_telemetry, heap_snapshot, heap_live_reports)
    npu_final_review = npu_final_review_summary(provider_evidence, peer_evidence)
    provider_evidence["npu_final_review"] = npu_final_review
    provider_execution = bool(provider_evidence["provider_execution_performed"])
    return {
        "schema_version": 1,
        "kind": "full_toolbox_run_telemetry_summary",
        "generated_at": now_iso(),
        "repo_root": str(repo_root),
        "stamp": args.stamp,
        "passed": not errors,
        "errors": errors,
        "warnings": warnings,
        "provider_execution_performed": provider_execution,
        "provider_evidence": provider_evidence,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "sqlite_write_performed": False,
        "persistent_memory_write_performed": False,
        "manual_review_required": True,
        "inputs": {
            "decision_loop": decision_path,
            "recommendations": recommendations_path,
            "patch_plan": patch_plan_path,
            "repository_consistency": repository_path,
            "repository_consistency_smoke": repository_smoke_path,
            "gpu_npu_sync": gpu_npu_path,
            "orchestrator": orchestrator_path,
            "gpu_report": gpu_path,
            "peer_exchange": peer_path,
            "peer_contract": peer_contract_path,
            "provider_runtime_heap_telemetry": heap_telemetry_path,
            "provider_runtime_heap_snapshot": heap_snapshot_path,
            "provider_runtime_heap_live_signals": heap_live_paths,
            "line_count_csv": line_count_csv.get("path"),
        },
        "run_parameters": {
            "budget_minutes": args.budget_minutes,
            "max_rounds": args.max_rounds,
            "files_per_round": args.files_per_round,
            "max_context_files": args.max_context_files,
            "max_chars_per_file": args.max_chars_per_file,
            "max_new_tokens": args.max_new_tokens,
            "npu_auditor_every_rounds": args.npu_auditor_every_rounds,
            "repository_consistency_map_workers": args.repository_consistency_map_workers,
        },
        "workflow_summary": workflow_like,
        "recommendations_first20": [
            compact_recommendation(item) for item in recommendation_items[:20]
        ],
        "patch_plans_first20": [compact_patch_plan(item) for item in patch_plan_items[:20]],
        "repository_consistency": {
            "finding_count": repository_map.get("finding_count"),
            "severity_counts": repository_map.get("severity_counts"),
            "finding_kind_counts": repository_map.get("finding_kind_counts"),
            "performance": compact_performance(repository_map),
            "smoke_passed": repository_smoke.get("passed"),
            "smoke_mapper_report_reused": repository_smoke.get("mapper_report_reused"),
            "smoke_elapsed_seconds": repository_smoke.get("elapsed_seconds"),
        },
        "gpu_npu": {
            "provider_evidence": provider_evidence,
            "peer_exchange": peer_evidence,
            "npu_final_review": npu_final_review,
            "provider_runtime_heap": heap_evidence,
            "sync_metrics": gpu_npu_sync.get("metrics"),
            "performance": compact_performance(gpu_npu_sync),
            "operational_opinions": gpu_npu_sync.get("operational_opinions"),
            "refactoring_suggestions": gpu_npu_sync.get("refactoring_suggestions"),
        },
        "provider_runtime_heap": heap_evidence,
        "line_count_csv": line_count_csv,
        "guardrails": {
            "report_only": True,
            "committable_location": "docs/LOCAL_VALIDATION_EVIDENCE",
            "raw_output_commit_allowed": False,
            "provider_execution_performed": provider_execution,
            "gpu_provider_execution_performed": provider_evidence.get(
                "gpu_provider_execution_performed"
            ),
            "gpu0_peer_support_provider_execution_performed": provider_evidence.get(
                "gpu0_peer_support_provider_execution_performed"
            ),
            "npu_provider_execution_performed": provider_evidence.get(
                "npu_provider_execution_performed"
            ),
            "npu_micro_orchestrator_provider_execution_performed": provider_evidence.get(
                "npu_micro_provider_execution_performed"
            ),
            "npu_micro_orchestrator_tool_lane_performed": provider_evidence.get(
                "npu_micro_tool_lane_performed"
            ),
            "gpu0_peer_provider_execution_performed": peer_evidence.get(
                "gpu0_peer_provider_execution_performed"
            ),
            "npu_micro_provider_execution_performed": peer_evidence.get(
                "npu_micro_provider_execution_performed"
            ),
            "npu_micro_non_blocking": peer_evidence.get("npu_micro_non_blocking"),
            "npu_final_review_classification": npu_final_review.get("classification"),
            "npu_final_provider_close_path_required": npu_final_review.get(
                "npu_final_provider_close_path_required"
            ),
            "provider_runtime_heap_direct_execution_violation_count": heap_evidence.get(
                "direct_execution_violation_count"
            ),
            "patch_application_performed": False,
            "source_writes_performed": False,
            "sqlite_write_performed": False,
            "persistent_memory_write_performed": False,
        },
    }
