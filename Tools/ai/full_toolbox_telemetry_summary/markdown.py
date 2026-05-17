"""Markdown rendering for full-toolbox telemetry summaries."""

from __future__ import annotations

from typing import Any

from .common import safe_dict, safe_list

def render_markdown(report: dict[str, Any]) -> str:
    lines = ["# Full Toolbox Run Telemetry Summary", ""]
    workflow = safe_dict(report.get("workflow_summary"))
    lines.append(f"- Passed: `{report.get('passed')}`")
    lines.append(f"- Stamp: `{report.get('stamp')}`")
    lines.append(f"- Recommendation count: `{workflow.get('recommendation_count')}`")
    lines.append(f"- Patch plan count: `{workflow.get('patch_plan_count')}`")
    lines.append(
        f"- Deterministic synthesizer used: `{workflow.get('deterministic_synthesizer_used')}`"
    )
    lines.append(f"- Patch plan fallback used: `{workflow.get('patch_plan_fallback_used')}`")
    lines.append(f"- Provider execution performed: `{report.get('provider_execution_performed')}`")
    provider_evidence = safe_dict(report.get("provider_evidence"))
    lines.append(
        f"- GPU provider execution performed: `{provider_evidence.get('gpu_provider_execution_performed')}`"
    )
    lines.append(f"- GPU round count: `{provider_evidence.get('gpu_round_count')}`")
    lines.append(
        f"- GPU0 startup peer support execution performed: `{provider_evidence.get('gpu0_peer_support_provider_execution_performed')}`"
    )
    lines.append(
        f"- GPU0 startup peer support overlap count: `{provider_evidence.get('gpu0_peer_support_overlap_count')}`"
    )
    lines.append(
        f"- Legacy NPU auditor requested: `{provider_evidence.get('legacy_npu_auditor_provider_requested')}`"
    )
    lines.append(
        f"- Legacy NPU auditor execution performed: `{provider_evidence.get('legacy_npu_provider_execution_performed')}`"
    )
    lines.append(f"- NPU audit success count: `{provider_evidence.get('npu_audit_success_count')}`")
    lines.append(
        f"- NPU orchestrator micro execution performed: `{provider_evidence.get('npu_micro_provider_execution_performed')}`"
    )
    lines.append(
        f"- NPU orchestrator micro tool lane performed: `{provider_evidence.get('npu_micro_tool_lane_performed')}`"
    )
    lines.append(
        f"- NPU orchestrator micro overlap count: `{provider_evidence.get('npu_micro_support_overlap_count')}`"
    )
    lines.append(
        f"- NPU orchestrator micro runtime tool executions: `{provider_evidence.get('npu_micro_runtime_tool_execution_count')}`"
    )
    if provider_evidence.get("provider_degraded_reasons"):
        lines.append(
            f"- Provider degraded reasons: `{provider_evidence.get('provider_degraded_reasons')}`"
        )
    peer_evidence = safe_dict(safe_dict(report.get("gpu_npu")).get("peer_exchange"))
    lines.append(f"- AI peer exchange passed: `{peer_evidence.get('peer_exchange_passed')}`")
    lines.append(
        f"- GPU0 peer provider execution performed: `{peer_evidence.get('gpu0_peer_provider_execution_performed')}`"
    )
    lines.append(
        f"- GPU0 peer broker tool executions: `{peer_evidence.get('gpu0_peer_tool_execution_count')}`"
    )
    lines.append(f"- NPU micro non-blocking: `{peer_evidence.get('npu_micro_non_blocking')}`")
    lines.append(
        f"- NPU micro provider execution performed: `{peer_evidence.get('npu_micro_provider_execution_performed')}`"
    )
    lines.append(
        f"- NPU micro broker tool executions: `{peer_evidence.get('npu_micro_tool_execution_count')}`"
    )
    npu_final_review = safe_dict(safe_dict(report.get("gpu_npu")).get("npu_final_review"))
    lines.append(f"- NPU final review classification: `{npu_final_review.get('classification')}`")
    lines.append(
        f"- NPU final review on performant lane: `{npu_final_review.get('final_review_on_performant_lane')}`"
    )
    lines.append(
        f"- NPU final close-path provider required: `{npu_final_review.get('npu_final_provider_close_path_required')}`"
    )
    heap_evidence = safe_dict(report.get("provider_runtime_heap"))
    lines.append(f"- Runtime heap events: `{heap_evidence.get('event_count')}`")
    lines.append(f"- Runtime heap live signals: `{heap_evidence.get('live_signal_count')}`")
    lines.append(
        f"- Runtime heap direct execution violations: `{heap_evidence.get('direct_execution_violation_count')}`"
    )
    line_csv = safe_dict(report.get("line_count_csv"))
    lines.append(f"- Line-count CSV rows: `{line_csv.get('row_count')}`")
    lines.append("")
    lines.append("## Provider runtime heap")
    lines.append("")
    lines.append(f"- Telemetry seen: `{heap_evidence.get('telemetry_seen')}`")
    lines.append(f"- Snapshot seen: `{heap_evidence.get('snapshot_seen')}`")
    lines.append(
        f"- Pending broker requests: `{heap_evidence.get('pending_broker_request_count')}`"
    )
    lines.append(f"- Broker results: `{heap_evidence.get('broker_result_count')}`")
    for item in safe_list(heap_evidence.get("live_signals")):
        lines.append(
            f"- `{item.get('mode')}` passed=`{item.get('passed')}` event_count=`{item.get('event_count')}` heap_event_count=`{item.get('heap_event_count')}`"
        )
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
        lines.append(
            f"- `{item.get('id')}` `{item.get('area')}` `{item.get('risk')}` -> `{item.get('target_files')}`"
        )
    lines.append("")
    lines.append("## Top patch plans")
    lines.append("")
    for item in safe_list(report.get("patch_plans_first20")):
        lines.append(
            f"- `{item.get('id')}` `{item.get('area')}` review=`{item.get('manual_review_required')}` -> `{item.get('target_files')}`"
        )
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
