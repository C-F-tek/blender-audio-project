#!/usr/bin/env python3
"""Build a compact telemetry summary for full-toolbox decision-loop runs.

Report-only utility. It reads completed run reports and writes a compact JSON/MD
summary intended for docs/LOCAL_VALIDATION_EVIDENCE so GitHub/AI reviewers can
inspect run status, top recommendations, patch plans and performance telemetry
without committing output/**.
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path
from typing import Any

try:
    from Tools.ai.code_patch_plan_common import now_iso, read_json_object, repo_rel
    from Tools.validation.report_utils import resolve_output_path, write_json_report, write_text_report
except ImportError:
    repo_root_for_import = Path(__file__).resolve().parents[2]
    if str(repo_root_for_import) not in sys.path:
        sys.path.insert(0, str(repo_root_for_import))
    from Tools.ai.code_patch_plan_common import now_iso, read_json_object, repo_rel  # type: ignore
    from Tools.validation.report_utils import resolve_output_path, write_json_report, write_text_report  # type: ignore

DEFAULT_OUTPUT = "docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_run_telemetry_summary.json"
DEFAULT_MARKDOWN = "docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_run_telemetry_summary.md"


def read_optional_json(repo_root: Path, value: str) -> tuple[dict[str, Any], list[str], str]:
    if not value:
        return {}, [], ""
    path = resolve_output_path(repo_root, value)
    path_rel = repo_rel(repo_root, path)
    if not path.exists():
        return {}, [f"optional input missing: {path_rel}"], path_rel
    data, errors = read_json_object(path, missing_is_error=True)
    return data, errors, path_rel


def safe_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def safe_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def safe_int(value: Any, default: int = 0) -> int:
    if isinstance(value, bool):
        return default
    try:
        if value in (None, ""):
            return default
        return int(value)
    except (TypeError, ValueError):
        return default


def provider_evidence_summary(orchestrator: dict[str, Any], gpu_report: dict[str, Any]) -> dict[str, Any]:
    gpu_round_count = safe_int(gpu_report.get("round_count"))
    gpu_provider_performed = bool(
        gpu_report.get("provider_execution_performed")
        and gpu_round_count > 0
        and str(gpu_report.get("classification") or "") != "required_provider_artifact_missing"
        and not bool(gpu_report.get("provider_empty_response"))
    )
    npu_audit_count = safe_int(orchestrator.get("npu_audit_count"))
    npu_success_count = safe_int(orchestrator.get("npu_audit_success_count"))
    gpu0_peer_support_count = safe_int(orchestrator.get("gpu0_peer_support_count"))
    gpu0_peer_support_success_count = safe_int(orchestrator.get("gpu0_peer_support_success_count"))
    gpu0_peer_support_overlap_count = safe_int(orchestrator.get("gpu0_peer_support_overlap_count"))
    npu_micro_support_count = safe_int(orchestrator.get("npu_micro_support_count"))
    npu_micro_support_success_count = safe_int(orchestrator.get("npu_micro_support_success_count"))
    npu_micro_support_provider_success_count = safe_int(orchestrator.get("npu_micro_support_provider_success_count"))
    npu_micro_support_tool_success_count = safe_int(orchestrator.get("npu_micro_support_tool_success_count"))
    npu_micro_support_overlap_count = safe_int(orchestrator.get("npu_micro_support_overlap_count"))
    npu_micro_support_tool_request_count = safe_int(orchestrator.get("npu_micro_support_tool_request_count"))
    npu_micro_runtime_tool_execution_count = safe_int(orchestrator.get("npu_micro_runtime_tool_execution_count"))
    npu_lane = safe_dict(orchestrator.get("npu_lane"))
    legacy_npu_requested = bool(
        orchestrator.get("legacy_npu_auditor_provider_requested")
        or orchestrator.get("npu_auditor_provider_requested")
        or npu_lane.get("provider_requested")
    )
    gpu0_peer_support_performed = gpu0_peer_support_success_count > 0 or bool(orchestrator.get("gpu0_peer_support_provider_execution_performed"))
    npu_micro_provider_performed = npu_micro_support_provider_success_count > 0 or bool(orchestrator.get("npu_micro_support_provider_execution_performed"))
    npu_micro_tool_lane_performed = bool(
        orchestrator.get("npu_micro_support_tool_lane_performed")
        or npu_micro_support_tool_success_count > 0
        or npu_micro_runtime_tool_execution_count > 0
        or npu_micro_support_tool_request_count > 0
    )
    legacy_npu_provider_performed = npu_success_count > 0
    npu_provider_performed = bool(legacy_npu_provider_performed or npu_micro_provider_performed)
    degraded_reasons = []
    if isinstance(orchestrator.get("provider_degraded_reasons"), list):
        degraded_reasons.extend(str(item) for item in orchestrator.get("provider_degraded_reasons"))
    if not gpu_provider_performed and (orchestrator or gpu_report):
        degraded_reasons.append(
            "gpu_not_confirmed:"
            f"performed={gpu_report.get('provider_execution_performed')};"
            f"round_count={gpu_round_count};"
            f"classification={gpu_report.get('classification')};"
            f"passed={gpu_report.get('passed')}"
        )
    if legacy_npu_requested and orchestrator.get("npu_lane_mode") in {"skipped", "metadata_only", "degraded"} and npu_success_count == 0:
        degraded_reasons.append(
            "npu_auditor_not_confirmed:"
            f"audit_count={npu_audit_count};success_count={npu_success_count};"
            f"lane_mode={orchestrator.get('npu_lane_mode')}"
        )
    return {
        "provider_execution_requested": bool(orchestrator.get("provider_execution_performed") or gpu_report.get("provider_execution_requested")),
        "provider_execution_performed": bool(gpu_provider_performed or gpu0_peer_support_performed or npu_provider_performed),
        "gpu_provider_execution_performed": gpu_provider_performed,
        "gpu0_peer_support_provider_execution_performed": gpu0_peer_support_performed,
        "gpu0_peer_support_count": gpu0_peer_support_count,
        "gpu0_peer_support_success_count": gpu0_peer_support_success_count,
        "gpu0_peer_support_overlap_count": gpu0_peer_support_overlap_count,
        "gpu_round_count": gpu_round_count,
        "gpu_returncode": orchestrator.get("gpu_returncode"),
        "gpu_classification": gpu_report.get("classification"),
        "gpu_provider_empty_response": bool(gpu_report.get("provider_empty_response")),
        "legacy_npu_auditor_provider_requested": legacy_npu_requested,
        "npu_provider_execution_performed": npu_provider_performed,
        "legacy_npu_provider_execution_performed": legacy_npu_provider_performed,
        "npu_micro_provider_execution_performed": npu_micro_provider_performed,
        "npu_micro_tool_lane_performed": npu_micro_tool_lane_performed,
        "npu_micro_support_count": npu_micro_support_count,
        "npu_micro_support_success_count": npu_micro_support_success_count,
        "npu_micro_support_provider_success_count": npu_micro_support_provider_success_count,
        "npu_micro_support_tool_success_count": npu_micro_support_tool_success_count,
        "npu_micro_support_overlap_count": npu_micro_support_overlap_count,
        "npu_micro_support_tool_request_count": npu_micro_support_tool_request_count,
        "npu_micro_runtime_tool_execution_count": npu_micro_runtime_tool_execution_count,
        "npu_audit_count": npu_audit_count,
        "npu_audit_success_count": npu_success_count,
        "npu_lane_mode": orchestrator.get("npu_lane_mode"),
        "provider_degraded_reasons": degraded_reasons,
    }


def peer_exchange_summary(peer_exchange: dict[str, Any], peer_contract: dict[str, Any]) -> dict[str, Any]:
    response = peer_exchange.get("gpu0_response") if isinstance(peer_exchange.get("gpu0_response"), dict) else {}
    broker = peer_exchange.get("runtime_tool_broker") if isinstance(peer_exchange.get("runtime_tool_broker"), dict) else {}
    npu = peer_exchange.get("npu_micro_response") if isinstance(peer_exchange.get("npu_micro_response"), dict) else {}
    npu_broker = peer_exchange.get("npu_runtime_tool_broker") if isinstance(peer_exchange.get("npu_runtime_tool_broker"), dict) else {}
    return {
        "peer_exchange_seen": bool(peer_exchange),
        "peer_exchange_passed": peer_exchange.get("passed"),
        "peer_contract_passed": peer_contract.get("passed"),
        "gpu0_peer_provider_execution_performed": bool(response.get("provider_execution_performed")),
        "gpu0_peer_tool_request_count": safe_int(response.get("tool_request_count")),
        "gpu0_peer_tool_execution_count": safe_int(broker.get("tool_execution_count")),
        "npu_micro_non_blocking": bool(npu.get("non_blocking")),
        "npu_micro_provider_execution_performed": bool(npu.get("provider_execution_performed")),
        "npu_micro_tool_request_count": safe_int(npu.get("tool_request_count")),
        "npu_micro_tool_execution_count": safe_int(npu_broker.get("tool_execution_count")),
        "classifications": peer_exchange.get("classifications") or peer_contract.get("classifications") or [],
    }


def npu_final_review_summary(provider: dict[str, Any], peer: dict[str, Any]) -> dict[str, Any]:
    gpu1_review = bool(provider.get("gpu_provider_execution_performed"))
    gpu0_review = bool(
        provider.get("gpu0_peer_support_provider_execution_performed")
        or peer.get("gpu0_peer_provider_execution_performed")
        or peer.get("gpu0_peer_tool_execution_count")
    )
    npu_support_seen = bool(
        provider.get("npu_micro_tool_lane_performed")
        or provider.get("npu_provider_execution_performed")
        or peer.get("npu_micro_tool_execution_count")
        or peer.get("npu_micro_non_blocking")
    )
    if gpu1_review and gpu0_review:
        classification = "gpu1_gpu0_npu_final_review"
        reviewers = ["gpu1", "gpu0", "deterministic_validators"]
    elif gpu1_review:
        classification = "gpu1_npu_final_review"
        reviewers = ["gpu1", "deterministic_validators"]
    elif gpu0_review:
        classification = "gpu0_npu_final_review"
        reviewers = ["gpu0", "deterministic_validators"]
    else:
        classification = "npu_final_review_missing_gpu_peer"
        reviewers = ["deterministic_validators"]
    return {
        "classification": classification,
        "npu_support_seen": npu_support_seen,
        "npu_self_check_only": False,
        "npu_final_provider_close_path_required": False,
        "final_review_on_performant_lane": classification != "npu_final_review_missing_gpu_peer",
        "reviewers": reviewers,
        "deterministic_validator_acceptance_required": True,
        "product_blocker": not npu_support_seen,
    }


def runtime_heap_summary(
    telemetry: dict[str, Any],
    snapshot: dict[str, Any],
    live_signals: list[dict[str, Any]],
) -> dict[str, Any]:
    live_signal_rows: list[dict[str, Any]] = []
    for report in live_signals:
        heap = safe_dict(report.get("heap_snapshot"))
        live_signal_rows.append(
            {
                "mode": report.get("mode"),
                "passed": report.get("passed"),
                "event_count": safe_int(report.get("event_count")),
                "heap_event_count": safe_int(heap.get("event_count")),
                "pending_broker_request_count": safe_int(heap.get("pending_broker_request_count")),
            }
        )
    return {
        "telemetry_seen": bool(telemetry),
        "snapshot_seen": bool(snapshot),
        "live_signal_count": len(live_signal_rows),
        "event_count": safe_int(telemetry.get("event_count") or snapshot.get("event_count")),
        "parse_error_count": safe_int(telemetry.get("parse_error_count") or snapshot.get("parse_error_count")),
        "direct_execution_violation_count": safe_int(telemetry.get("direct_execution_violation_count")),
        "pending_broker_request_count": safe_int(telemetry.get("pending_broker_request_count") or snapshot.get("pending_broker_request_count")),
        "events_by_lane": telemetry.get("events_by_lane") if isinstance(telemetry.get("events_by_lane"), dict) else {},
        "events_by_type": telemetry.get("events_by_type") if isinstance(telemetry.get("events_by_type"), dict) else {},
        "interaction_edges": telemetry.get("interaction_edges") if isinstance(telemetry.get("interaction_edges"), dict) else {},
        "gpu1_to_gpu0_event_count": safe_int(telemetry.get("gpu1_to_gpu0_event_count")),
        "gpu0_to_gpu1_event_count": safe_int(telemetry.get("gpu0_to_gpu1_event_count")),
        "gpu1_gpu0_bidirectional": bool(telemetry.get("gpu1_gpu0_bidirectional")),
        "broker_result_count": safe_int(telemetry.get("broker_result_count")),
        "live_signals": live_signal_rows,
    }


def line_count_csv_summary(repo_root: Path, value: str) -> tuple[dict[str, Any], list[str]]:
    if not value:
        return {"seen": False, "path": "", "row_count": 0, "total_lines": 0, "top_files": []}, []
    path = resolve_output_path(repo_root, value)
    path_rel = repo_rel(repo_root, path)
    if not path.exists():
        return {"seen": False, "path": path_rel, "row_count": 0, "total_lines": 0, "top_files": []}, [f"line-count CSV missing: {path_rel}"]
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            rows = [dict(row) for row in csv.DictReader(handle)]
    except OSError as exc:
        return {"seen": False, "path": path_rel, "row_count": 0, "total_lines": 0, "top_files": []}, [f"unable to read line-count CSV {path_rel}: {exc}"]
    normalized: list[dict[str, Any]] = []
    for row in rows:
        file_value = str(row.get("File") or row.get("Path") or "")
        lines = safe_int(row.get("Lines") or row.get("lines"))
        if file_value:
            normalized.append({"file": file_value, "lines": lines})
    normalized.sort(key=lambda item: (-safe_int(item.get("lines")), str(item.get("file")).lower()))
    return {
        "seen": True,
        "path": path_rel,
        "row_count": len(normalized),
        "total_lines": sum(safe_int(item.get("lines")) for item in normalized),
        "top_files": normalized[:20],
    }, []


def compact_paths(values: Any, limit: int = 12) -> list[str]:
    out: list[str] = []
    for value in safe_list(values):
        text = str(value)
        if text and text not in out:
            out.append(text)
        if len(out) >= limit:
            break
    return out


def compact_recommendation(item: dict[str, Any]) -> dict[str, Any]:
    finding = safe_dict(item.get("repository_consistency_finding"))
    return {
        "id": item.get("id"),
        "area": item.get("area"),
        "risk": item.get("risk"),
        "status": item.get("status"),
        "target_files": compact_paths(item.get("target_files"), limit=6),
        "source": item.get("source"),
        "repository_consistency_kind": finding.get("kind"),
        "repository_consistency_severity": finding.get("severity"),
    }


def compact_patch_plan(item: dict[str, Any]) -> dict[str, Any]:
    source_evidence = safe_dict(item.get("source_evidence"))
    consistency = safe_dict(source_evidence.get("repository_consistency_finding"))
    return {
        "id": item.get("id"),
        "area": item.get("area"),
        "target_files": compact_paths(item.get("target_files"), limit=6),
        "manual_review_required": item.get("manual_review_required"),
        "cosmetic_patch_allowed": safe_dict(item.get("guardrails")).get("cosmetic_patch_allowed"),
        "repository_consistency_kind": consistency.get("kind"),
        "repository_consistency_severity": consistency.get("severity"),
    }


def compact_performance(data: dict[str, Any]) -> dict[str, Any]:
    performance = data.get("performance")
    return performance if isinstance(performance, dict) else {}


def build_summary(args: argparse.Namespace) -> dict[str, Any]:
    repo_root = Path(args.repo_root).resolve()
    warnings: list[str] = []
    errors: list[str] = []

    decision_loop, decision_errors, decision_path = read_optional_json(repo_root, args.decision_loop)
    recommendations, recommendation_errors, recommendations_path = read_optional_json(repo_root, args.recommendations)
    patch_plan, patch_plan_errors, patch_plan_path = read_optional_json(repo_root, args.patch_plan)
    repository_map, repository_errors, repository_path = read_optional_json(repo_root, args.repository_consistency)
    repository_smoke, repository_smoke_errors, repository_smoke_path = read_optional_json(repo_root, args.repository_consistency_smoke)
    gpu_npu_sync, gpu_npu_errors, gpu_npu_path = read_optional_json(repo_root, args.gpu_npu_sync)
    orchestrator, orchestrator_errors, orchestrator_path = read_optional_json(repo_root, args.orchestrator)
    gpu_report, gpu_errors, gpu_path = read_optional_json(repo_root, args.gpu_report)
    peer_exchange, peer_errors, peer_path = read_optional_json(repo_root, args.peer_exchange)
    peer_contract, peer_contract_errors, peer_contract_path = read_optional_json(repo_root, args.peer_contract)
    heap_telemetry, heap_telemetry_errors, heap_telemetry_path = read_optional_json(repo_root, args.provider_runtime_heap_telemetry)
    heap_snapshot, heap_snapshot_errors, heap_snapshot_path = read_optional_json(repo_root, args.provider_runtime_heap_snapshot)
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

    recommendation_items = [item for item in safe_list(recommendations.get("recommendations")) if isinstance(item, dict)]
    patch_plan_items = [item for item in safe_list(patch_plan.get("patch_plans")) if isinstance(item, dict)]
    workflow_like = {
        "passed": decision_loop.get("passed"),
        "recommendation_count": decision_loop.get("recommendation_count") or recommendations.get("recommendation_count") or len(recommendation_items),
        "patch_plan_count": decision_loop.get("patch_plan_count") or patch_plan.get("patch_plan_count") or len(patch_plan_items),
        "deterministic_synthesizer_used": decision_loop.get("deterministic_synthesizer_used"),
        "patch_plan_fallback_used": decision_loop.get("patch_plan_fallback_used") or patch_plan.get("fallback_used"),
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
        "recommendations_first20": [compact_recommendation(item) for item in recommendation_items[:20]],
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
            "gpu_provider_execution_performed": provider_evidence.get("gpu_provider_execution_performed"),
            "gpu0_peer_support_provider_execution_performed": provider_evidence.get("gpu0_peer_support_provider_execution_performed"),
            "npu_provider_execution_performed": provider_evidence.get("npu_provider_execution_performed"),
            "npu_micro_orchestrator_provider_execution_performed": provider_evidence.get("npu_micro_provider_execution_performed"),
            "npu_micro_orchestrator_tool_lane_performed": provider_evidence.get("npu_micro_tool_lane_performed"),
            "gpu0_peer_provider_execution_performed": peer_evidence.get("gpu0_peer_provider_execution_performed"),
            "npu_micro_provider_execution_performed": peer_evidence.get("npu_micro_provider_execution_performed"),
            "npu_micro_non_blocking": peer_evidence.get("npu_micro_non_blocking"),
            "npu_final_review_classification": npu_final_review.get("classification"),
            "npu_final_provider_close_path_required": npu_final_review.get("npu_final_provider_close_path_required"),
            "provider_runtime_heap_direct_execution_violation_count": heap_evidence.get("direct_execution_violation_count"),
            "patch_application_performed": False,
            "source_writes_performed": False,
            "sqlite_write_performed": False,
            "persistent_memory_write_performed": False,
        },
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = ["# Full Toolbox Run Telemetry Summary", ""]
    workflow = safe_dict(report.get("workflow_summary"))
    lines.append(f"- Passed: `{report.get('passed')}`")
    lines.append(f"- Stamp: `{report.get('stamp')}`")
    lines.append(f"- Recommendation count: `{workflow.get('recommendation_count')}`")
    lines.append(f"- Patch plan count: `{workflow.get('patch_plan_count')}`")
    lines.append(f"- Deterministic synthesizer used: `{workflow.get('deterministic_synthesizer_used')}`")
    lines.append(f"- Patch plan fallback used: `{workflow.get('patch_plan_fallback_used')}`")
    lines.append(f"- Provider execution performed: `{report.get('provider_execution_performed')}`")
    provider_evidence = safe_dict(report.get("provider_evidence"))
    lines.append(f"- GPU provider execution performed: `{provider_evidence.get('gpu_provider_execution_performed')}`")
    lines.append(f"- GPU round count: `{provider_evidence.get('gpu_round_count')}`")
    lines.append(f"- GPU0 startup peer support execution performed: `{provider_evidence.get('gpu0_peer_support_provider_execution_performed')}`")
    lines.append(f"- GPU0 startup peer support overlap count: `{provider_evidence.get('gpu0_peer_support_overlap_count')}`")
    lines.append(f"- Legacy NPU auditor requested: `{provider_evidence.get('legacy_npu_auditor_provider_requested')}`")
    lines.append(f"- Legacy NPU auditor execution performed: `{provider_evidence.get('legacy_npu_provider_execution_performed')}`")
    lines.append(f"- NPU audit success count: `{provider_evidence.get('npu_audit_success_count')}`")
    lines.append(f"- NPU orchestrator micro execution performed: `{provider_evidence.get('npu_micro_provider_execution_performed')}`")
    lines.append(f"- NPU orchestrator micro tool lane performed: `{provider_evidence.get('npu_micro_tool_lane_performed')}`")
    lines.append(f"- NPU orchestrator micro overlap count: `{provider_evidence.get('npu_micro_support_overlap_count')}`")
    lines.append(f"- NPU orchestrator micro runtime tool executions: `{provider_evidence.get('npu_micro_runtime_tool_execution_count')}`")
    if provider_evidence.get("provider_degraded_reasons"):
        lines.append(f"- Provider degraded reasons: `{provider_evidence.get('provider_degraded_reasons')}`")
    peer_evidence = safe_dict(safe_dict(report.get("gpu_npu")).get("peer_exchange"))
    lines.append(f"- AI peer exchange passed: `{peer_evidence.get('peer_exchange_passed')}`")
    lines.append(f"- GPU0 peer provider execution performed: `{peer_evidence.get('gpu0_peer_provider_execution_performed')}`")
    lines.append(f"- GPU0 peer broker tool executions: `{peer_evidence.get('gpu0_peer_tool_execution_count')}`")
    lines.append(f"- NPU micro non-blocking: `{peer_evidence.get('npu_micro_non_blocking')}`")
    lines.append(f"- NPU micro provider execution performed: `{peer_evidence.get('npu_micro_provider_execution_performed')}`")
    lines.append(f"- NPU micro broker tool executions: `{peer_evidence.get('npu_micro_tool_execution_count')}`")
    npu_final_review = safe_dict(safe_dict(report.get("gpu_npu")).get("npu_final_review"))
    lines.append(f"- NPU final review classification: `{npu_final_review.get('classification')}`")
    lines.append(f"- NPU final review on performant lane: `{npu_final_review.get('final_review_on_performant_lane')}`")
    lines.append(f"- NPU final close-path provider required: `{npu_final_review.get('npu_final_provider_close_path_required')}`")
    heap_evidence = safe_dict(report.get("provider_runtime_heap"))
    lines.append(f"- Runtime heap events: `{heap_evidence.get('event_count')}`")
    lines.append(f"- Runtime heap live signals: `{heap_evidence.get('live_signal_count')}`")
    lines.append(f"- Runtime heap direct execution violations: `{heap_evidence.get('direct_execution_violation_count')}`")
    line_csv = safe_dict(report.get("line_count_csv"))
    lines.append(f"- Line-count CSV rows: `{line_csv.get('row_count')}`")
    lines.append("")
    lines.append("## Provider runtime heap")
    lines.append("")
    lines.append(f"- Telemetry seen: `{heap_evidence.get('telemetry_seen')}`")
    lines.append(f"- Snapshot seen: `{heap_evidence.get('snapshot_seen')}`")
    lines.append(f"- Pending broker requests: `{heap_evidence.get('pending_broker_request_count')}`")
    lines.append(f"- Broker results: `{heap_evidence.get('broker_result_count')}`")
    for item in safe_list(heap_evidence.get("live_signals")):
        lines.append(f"- `{item.get('mode')}` passed=`{item.get('passed')}` event_count=`{item.get('event_count')}` heap_event_count=`{item.get('heap_event_count')}`")
    lines.append("")
    lines.append("## Line-count CSV")
    lines.append("")
    lines.append(f"- Seen: `{line_csv.get('seen')}`")
    lines.append(f"- Path: `{line_csv.get('path')}`")
    lines.append(f"- Total lines: `{line_csv.get('total_lines')}`")
    for item in safe_list(line_csv.get("top_files"))[:10]:
        lines.append(f"- `{item.get('file')}`: `{item.get('lines')}`")
    lines.append("")
    lines.append("## Repository consistency performance")
    lines.append("")
    performance = safe_dict(safe_dict(report.get("repository_consistency")).get("performance"))
    for key in (
        "total_build_report_seconds",
        "markdown_scan_seconds",
        "file_discovery_seconds",
        "python_inventory_seconds",
        "path_index_seconds",
        "findings_build_seconds",
    ):
        lines.append(f"- `{key}`: `{performance.get(key)}`")
    lines.append("")
    lines.append("## Top recommendations")
    lines.append("")
    for item in safe_list(report.get("recommendations_first20")):
        lines.append(f"- `{item.get('id')}` `{item.get('area')}` `{item.get('risk')}` -> `{item.get('target_files')}`")
    lines.append("")
    lines.append("## Top patch plans")
    lines.append("")
    for item in safe_list(report.get("patch_plans_first20")):
        lines.append(f"- `{item.get('id')}` `{item.get('area')}` review=`{item.get('manual_review_required')}` -> `{item.get('target_files')}`")
    gpu_npu = safe_dict(report.get("gpu_npu"))
    if gpu_npu.get("operational_opinions"):
        lines.append("")
        lines.append("## GPU/NPU operational opinions")
        lines.append("")
        for item in safe_list(gpu_npu.get("operational_opinions")):
            lines.append(f"- {item}")
    if report.get("errors"):
        lines.append("")
        lines.append("## Errors")
        for item in safe_list(report.get("errors")):
            lines.append(f"- {item}")
    if report.get("warnings"):
        lines.append("")
        lines.append("## Warnings")
        for item in safe_list(report.get("warnings"))[:30]:
            lines.append(f"- {item}")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--stamp", required=True)
    parser.add_argument("--decision-loop", required=True)
    parser.add_argument("--recommendations", required=True)
    parser.add_argument("--patch-plan", required=True)
    parser.add_argument("--repository-consistency", default="")
    parser.add_argument("--repository-consistency-smoke", default="")
    parser.add_argument("--gpu-npu-sync", default="")
    parser.add_argument("--orchestrator", default="")
    parser.add_argument("--gpu-report", default="")
    parser.add_argument("--peer-exchange", default="")
    parser.add_argument("--peer-contract", default="")
    parser.add_argument("--provider-runtime-heap-telemetry", default="")
    parser.add_argument("--provider-runtime-heap-snapshot", default="")
    parser.add_argument("--provider-runtime-heap-live-signal", action="append", default=[])
    parser.add_argument("--line-count-csv", default="")
    parser.add_argument("--evidence-to-commit", action="append", default=[])
    parser.add_argument("--bundle-validation-passed", action="store_true")
    parser.add_argument("--budget-minutes", type=int, default=0)
    parser.add_argument("--max-rounds", type=int, default=0)
    parser.add_argument("--files-per-round", type=int, default=0)
    parser.add_argument("--max-context-files", type=int, default=0)
    parser.add_argument("--max-chars-per-file", type=int, default=0)
    parser.add_argument("--max-new-tokens", type=int, default=0)
    parser.add_argument("--npu-auditor-every-rounds", type=int, default=0)
    parser.add_argument("--repository-consistency-map-workers", type=int, default=0)
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    parser.add_argument("--markdown-output", default=DEFAULT_MARKDOWN)
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    report = build_summary(args)
    output = resolve_output_path(repo_root, args.output)
    markdown_output = resolve_output_path(repo_root, args.markdown_output)
    print(write_json_report(report, output), end="")
    write_text_report(render_markdown(report) + "\n", markdown_output)
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
