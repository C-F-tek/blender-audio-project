from __future__ import annotations

from .collection import (
    append_default_broker_report_if_present,
    collect_broker_pointer_entries,
    collect_explicit_broker_reports,
    collect_gpu_declared_requests,
    collect_npu_declared_requests,
    collect_npu_micro_support_broker_entries,
)
from .common import *  # noqa: F403
from .counters import (
    build_declared_runtime_tool_counter_entry,
    extract_declared_runtime_tool_counters,
    provider_evidence_summary,
    summarize_entries,
)

def build_report(args: argparse.Namespace) -> dict[str, Any]:
    repo_root = Path(args.repo_root).resolve()
    errors: list[str] = []
    warnings: list[str] = []
    orchestrator, orch_errors, orch_path = read_optional_json(repo_root, args.orchestrator)
    gpu_report, gpu_errors, gpu_path = read_optional_json(repo_root, args.gpu_report)
    gpu_npu_sync, sync_errors, sync_path = read_optional_json(repo_root, args.gpu_npu_sync)
    decision_loop, decision_errors, decision_path = read_optional_json(
        repo_root, args.decision_loop
    )
    warnings.extend(orch_errors + gpu_errors + sync_errors + decision_errors)

    entries: list[dict[str, Any]] = []
    entries.extend(
        collect_broker_pointer_entries(
            repo_root,
            orchestrator.get("runtime_tool_bootstrap_results"),
            "orchestrator",
            "orchestrator_bootstrap",
        )
    )
    entries.extend(
        collect_broker_pointer_entries(
            repo_root,
            orchestrator.get("runtime_tool_bootstrap_result"),
            "orchestrator",
            "orchestrator_bootstrap",
        )
    )
    broker_report_values = append_default_broker_report_if_present(
        repo_root, args.stamp, getattr(args, "broker_report", [])
    )
    explicit_broker_entries, explicit_broker_warnings, explicit_broker_paths = (
        collect_explicit_broker_reports(repo_root, broker_report_values)
    )
    entries.extend(explicit_broker_entries)
    warnings.extend(explicit_broker_warnings)
    entries.extend(
        collect_broker_pointer_entries(
            repo_root,
            orchestrator.get("gpu_runtime_tool_results"),
            "gpu",
            "gpu_runtime_tool_broker",
        )
    )
    entries.extend(
        collect_broker_pointer_entries(
            repo_root,
            orchestrator.get("npu_runtime_tool_results"),
            "npu",
            "npu_runtime_tool_broker",
        )
    )
    entries.extend(collect_npu_micro_support_broker_entries(repo_root, orchestrator))
    entries.extend(collect_gpu_declared_requests(gpu_report))
    entries.extend(collect_npu_declared_requests(orchestrator))
    declared_counters = extract_declared_runtime_tool_counters(gpu_report, gpu_npu_sync)
    if declared_counters["runtime_tool_request_count"] and not entries:
        entries.append(build_declared_runtime_tool_counter_entry(declared_counters))

    max_entries = max(1, int(args.max_entries))
    entries = [normalize_tool_entry(entry) for entry in entries]
    summary = summarize_entries(entries)
    summary["telemetry_quality"] = status_quality(entries)
    summary.update(declared_counters)
    provider_evidence = provider_evidence_summary(orchestrator, gpu_report)
    provider_broker_loop = (
        orchestrator.get("provider_broker_loop")
        if isinstance(orchestrator.get("provider_broker_loop"), dict)
        else {}
    )
    return {
        "schema_version": 1,
        "kind": "runtime_tool_usage_telemetry",
        "generated_at": now_iso(),
        "repo_root": str(repo_root),
        "stamp": args.stamp,
        "passed": not errors,
        "errors": errors,
        "warnings": warnings,
        "provider_execution_performed": provider_evidence["provider_execution_performed"],
        "provider_evidence": provider_evidence,
        "provider_broker_loop": provider_broker_loop,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "sqlite_write_performed": False,
        "persistent_memory_write_performed": False,
        "manual_review_required": True,
        "inputs": {
            "orchestrator": orch_path,
            "gpu_report": gpu_path,
            "gpu_npu_sync": sync_path,
            "decision_loop": decision_path,
            "broker_reports": explicit_broker_paths,
        },
        "decision_loop_summary": {
            "passed": decision_loop.get("passed"),
            "recommendation_count": decision_loop.get("recommendation_count"),
            "patch_plan_count": decision_loop.get("patch_plan_count"),
        },
        "gpu_npu_sync_metrics": gpu_npu_sync.get("metrics"),
        "summary": summary,
        "declared_runtime_tool_counters": declared_counters,
        "tool_calls": entries[:max_entries],
        "truncated_tool_call_count": max(0, len(entries) - max_entries),
        "guardrails": {
            "report_only": True,
            "committable_location": "docs/LOCAL_VALIDATION_EVIDENCE",
            "raw_output_commit_allowed": False,
            "provider_execution_performed": provider_evidence["provider_execution_performed"],
            "gpu_provider_execution_performed": provider_evidence[
                "gpu_provider_execution_performed"
            ],
            "npu_provider_execution_performed": provider_evidence[
                "npu_provider_execution_performed"
            ],
            "patch_application_performed": False,
            "source_writes_performed": False,
            "sqlite_write_performed": False,
            "persistent_memory_write_performed": False,
        },
    }

def render_markdown(report: dict[str, Any]) -> str:
    lines = ["# Runtime Tool Usage Telemetry", ""]
    lines.append(f"- Passed: `{report.get('passed')}`")
    lines.append(f"- Stamp: `{report.get('stamp')}`")
    provider_evidence = safe_dict(report.get("provider_evidence"))
    lines.append(f"- Provider execution performed: `{report.get('provider_execution_performed')}`")
    lines.append(
        f"- GPU provider execution performed: `{provider_evidence.get('gpu_provider_execution_performed')}`"
    )
    lines.append(
        f"- NPU provider execution performed: `{provider_evidence.get('npu_provider_execution_performed')}`"
    )
    if provider_evidence.get("provider_degraded_reasons"):
        lines.append(
            f"- Provider degraded reasons: `{provider_evidence.get('provider_degraded_reasons')}`"
        )
    summary = safe_dict(report.get("summary"))
    lines.append(f"- Tool call entries: `{summary.get('tool_call_entry_count')}`")
    lines.append(f"- Executed count: `{summary.get('executed_count')}`")
    lines.append(f"- Failed count: `{summary.get('failed_count')}`")
    lines.append(f"- Blocked count: `{summary.get('blocked_count')}`")
    lines.append(
        f"- Total reported tool elapsed seconds: `{summary.get('total_reported_tool_elapsed_seconds')}`"
    )
    telemetry_quality = safe_dict(summary.get("telemetry_quality"))
    if telemetry_quality:
        lines.append(f"- Status normalized: `{telemetry_quality.get('status_normalized')}`")
        lines.append(f"- Status missing count: `{telemetry_quality.get('status_missing_count')}`")
        lines.append(
            f"- Executed elapsed missing count: `{telemetry_quality.get('executed_elapsed_missing_count')}`"
        )
    lines.append(f"- Declared runtime tool requests: `{summary.get('runtime_tool_request_count')}`")
    lines.append(
        f"- Declared runtime tool executions: `{summary.get('runtime_tool_execution_count')}`"
    )
    lines.append(f"- Broker runtime tool executions: `{summary.get('broker_executed_count')}`")
    lines.append(f"- Declared not executed count: `{summary.get('declared_not_executed_count')}`")
    provider_broker_loop = safe_dict(report.get("provider_broker_loop"))
    if provider_broker_loop:
        lines.append(f"- Provider-broker loop active: `{provider_broker_loop.get('active')}`")
        lines.append(
            f"- Provider-broker loop executor: `{provider_broker_loop.get('controlled_executor')}`"
        )
        lines.append(
            f"- Provider-broker loop broker executions: `{provider_broker_loop.get('broker_tool_execution_count')}`"
        )
        lines.append(
            f"- Provider-broker loop GPU0 executions: `{provider_broker_loop.get('gpu0_broker_tool_execution_count')}`"
        )
        lines.append(
            f"- Provider-broker loop NPU executions: `{provider_broker_loop.get('npu_broker_tool_execution_count')}`"
        )
        lines.append(
            f"- Provider-broker loop NPU non-blocking: `{provider_broker_loop.get('npu_non_blocking')}`"
        )
    lines.append("")
    lines.append("## By caller AI")
    lines.append("")
    for caller, item in safe_dict(summary.get("by_caller_ai")).items():
        lines.append(
            f"- `{caller}`: count=`{item.get('count')}` executed=`{item.get('executed')}` failed=`{item.get('failed')}` elapsed=`{item.get('elapsed_seconds')}`"
        )
    lines.append("")
    lines.append("## By phase")
    lines.append("")
    for phase, item in safe_dict(summary.get("by_phase")).items():
        lines.append(
            f"- `{phase}`: count=`{item.get('count')}` executed=`{item.get('executed')}` failed=`{item.get('failed')}` elapsed=`{item.get('elapsed_seconds')}`"
        )
    lines.append("")
    lines.append("## By tool")
    lines.append("")
    for tool, item in safe_dict(summary.get("by_tool")).items():
        lines.append(
            f"- `{tool}`: count=`{item.get('count')}` executed=`{item.get('executed')}` failed=`{item.get('failed')}` elapsed=`{item.get('elapsed_seconds')}`"
        )
    lines.append("")
    lines.append("## First tool call entries")
    lines.append("")
    for entry in safe_list(report.get("tool_calls"))[:25]:
        lines.append(
            f"- `{entry.get('caller_ai')}` `{entry.get('phase')}` round=`{entry.get('round')}` tool=`{entry.get('tool')}` status=`{entry.get('status')}` elapsed=`{entry.get('elapsed_seconds')}`"
        )
    if report.get("warnings"):
        lines.append("")
        lines.append("## Warnings")
        lines.append("")
        for warning in safe_list(report.get("warnings"))[:30]:
            lines.append(f"- {warning}")
    lines.append("")
    return "\n".join(lines) + "\n"
