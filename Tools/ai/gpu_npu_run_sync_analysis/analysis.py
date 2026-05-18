"""Report assembly for GPU/NPU run sync analysis."""

from __future__ import annotations

import time
from pathlib import Path
from typing import Any

from Tools.ai._shared.code_patch_plan_common import read_json_object

from .common import (
    audit_duration_seconds,
    extract_gpu_round_durations,
    first_int,
    list_of_dicts,
    nested_dict,
    now_iso,
    percentile,
    repo_rel,
    safe_float,
    safe_int,
)
from .suggestions import build_operational_opinions, build_refactoring_suggestions, build_suggestions
from .timing import build_performance_summary

def analyze(repo_root: Path, orchestrator_path: Path) -> dict[str, Any]:
    analyzer_started = time.perf_counter()
    report, read_errors = read_json_object(orchestrator_path)
    if read_errors:
        raise ValueError("; ".join(read_errors))

    gpu_summary = nested_dict(report, "gpu_summary")
    rounds = list_of_dicts(report.get("rounds"))
    legacy_npu_audits = list_of_dicts(report.get("npu_audits"))
    npu_micro_supports = list_of_dicts(report.get("npu_micro_supports"))
    npu_audits = legacy_npu_audits + npu_micro_supports
    round_count = first_int(len(rounds), report.get("round_count"), gpu_summary.get("round_count"))
    audit_count = (
        len(npu_audits)
        if npu_audits
        else safe_int(report.get("npu_audit_count"))
        + safe_int(report.get("npu_micro_support_count"))
    )
    success_count = safe_int(report.get("npu_audit_success_count")) + safe_int(
        report.get("npu_micro_support_success_count")
    )
    gpu_elapsed = (
        safe_float(report.get("gpu_elapsed_seconds"))
        or safe_float(gpu_summary.get("elapsed_seconds"))
        or safe_float(report.get("elapsed_seconds"))
    )
    gpu_round_durations, gpu_metrics_source = extract_gpu_round_durations(
        report, rounds, round_count, gpu_elapsed
    )
    npu_durations = [audit_duration_seconds(item) for item in npu_audits]
    npu_durations = [value for value in npu_durations if value > 0]
    avg_gpu = sum(gpu_round_durations) / len(gpu_round_durations) if gpu_round_durations else 0.0
    avg_npu = sum(npu_durations) / len(npu_durations) if npu_durations else 0.0

    metrics = {
        "gpu_round_count": round_count,
        "npu_audit_count": audit_count,
        "legacy_npu_audit_count": len(legacy_npu_audits),
        "npu_micro_support_count": len(npu_micro_supports),
        "npu_micro_support_overlap_count": safe_int(report.get("npu_micro_support_overlap_count")),
        "gpu0_peer_support_count": safe_int(report.get("gpu0_peer_support_count")),
        "gpu0_peer_support_overlap_count": safe_int(report.get("gpu0_peer_support_overlap_count")),
        "npu_audit_success_count": success_count,
        "npu_audit_round_coverage": (round(audit_count / round_count, 3) if round_count else 0.0),
        "avg_gpu_round_seconds": round(avg_gpu, 3),
        "p50_gpu_round_seconds": round(percentile(gpu_round_durations, 50), 3),
        "p90_gpu_round_seconds": round(percentile(gpu_round_durations, 90), 3),
        "avg_npu_audit_seconds": round(avg_npu, 3),
        "p50_npu_audit_seconds": round(percentile(npu_durations, 50), 3),
        "p90_npu_audit_seconds": round(percentile(npu_durations, 90), 3),
        "npu_to_gpu_avg_duration_ratio": (round(avg_npu / avg_gpu, 3) if avg_gpu else 0.0),
        "gpu_elapsed_seconds": round(gpu_elapsed, 3),
        "provider_execution_performed": bool(report.get("provider_execution_performed")),
        "patch_application_performed": bool(report.get("patch_application_performed")),
        "source_writes_performed": bool(report.get("source_writes_performed")),
        "gpu_metrics_source": gpu_metrics_source,
    }
    performance = build_performance_summary(
        analyzer_started=analyzer_started,
        report=report,
        gpu_summary=gpu_summary,
        rounds=rounds,
        npu_audits=npu_audits,
        metrics=metrics,
    )
    suggestions = build_suggestions(report, metrics)
    return {
        "schema_version": 1,
        "kind": "gpu_npu_run_sync_analysis",
        "generated_at": now_iso(),
        "repo_root": str(repo_root),
        "passed": True,
        "errors": [],
        "warnings": [],
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "blender_runtime_execution_performed": False,
        "sqlite_write_performed": False,
        "manual_review_required": True,
        "inputs": {"orchestrator": repo_rel(repo_root, orchestrator_path)},
        "metrics": metrics,
        "performance": performance,
        "suggestions": suggestions,
        "operational_opinions": build_operational_opinions(metrics, performance),
        "refactoring_suggestions": build_refactoring_suggestions(metrics, performance),
        "decision": {
            "npu_too_slow_for_per_round_lockstep": metrics["npu_to_gpu_avg_duration_ratio"] > 1.5,
            "recommended_next_layer": "feed timing-backed GPU/NPU suggestions into decision-loop patch planning",
            "manual_review_required": True,
        },
    }

def render_markdown(report: dict[str, Any]) -> str:
    lines = ["# GPU/NPU Run Sync Analysis", ""]
    lines.append(f"- Passed: `{report['passed']}`")
    lines.append(f"- Provider execution performed: `{report['provider_execution_performed']}`")
    lines.append(f"- Patch application performed: `{report['patch_application_performed']}`")
    lines.append(f"- Source writes performed: `{report['source_writes_performed']}`")
    lines.append("")
    lines.append("## Metrics")
    lines.append("")
    for key, value in report["metrics"].items():
        lines.append(f"- `{key}`: `{value}`")

    gpu = nested_dict(report["performance"], "gpu")
    npu = nested_dict(report["performance"], "npu")
    lines.extend(
        [
            "",
            "## Performance",
            "",
            f"- Analyzer elapsed seconds: `{report['performance'].get('analyzer_elapsed_seconds')}`",
            f"- GPU elapsed seconds: `{gpu.get('elapsed_seconds')}`",
            f"- GPU average round seconds: `{gpu.get('avg_round_seconds')}`",
            f"- GPU timing source: `{gpu.get('round_duration_source')}`",
            f"- GPU timing sample count: `{gpu.get('round_duration_sample_count')}`",
            f"- GPU round durations total seconds: `{gpu.get('round_durations_total_seconds')}`",
            f"- NPU average audit seconds: `{npu.get('avg_audit_seconds')}`",
            f"- NPU duration sample count: `{npu.get('duration_sample_count')}`",
            "",
            "## Operational opinions",
            "",
        ]
    )
    for item in report.get("operational_opinions", []):
        lines.append(f"- {item}")

    lines.extend(["", "## Refactoring suggestions", ""])
    for item in report.get("refactoring_suggestions", []):
        lines.append(
            f"- `{item.get('priority')}` `{item.get('area')}`: {item.get('recommendation')} Evidence: {item.get('evidence')}"
        )

    lines.extend(["", "## Suggested balanced profile", ""])
    for key, value in report["suggestions"]["parameters"].items():
        lines.append(f"- `{key}`: `{value}`")

    lines.extend(["", "## Reasoning", ""])
    for item in report["suggestions"].get("reasoning", []):
        lines.append(f"- {item}")
    lines.append("")
    return "\n".join(lines)
