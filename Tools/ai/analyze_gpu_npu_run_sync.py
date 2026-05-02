#!/usr/bin/env python3
"""Analyze GPU/NPU timing skew from an orchestrator report.

Report-only utility. It reads a completed GPU/NPU orchestrator JSON and produces
sync diagnostics plus balanced-run parameter suggestions. It does not run
providers, apply patches, write source files, execute Blender, write SQLite
databases or change Git state.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def resolve_path(repo_root: Path, value: str) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = repo_root / path
    return path.resolve()


def repo_rel(repo_root: Path, path: Path) -> str:
    try:
        return path.resolve(strict=False).relative_to(repo_root.resolve(strict=False)).as_posix()
    except ValueError:
        return str(path)


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(value, dict):
        raise TypeError(f"JSON root must be object: {path}")
    return value


def nested_dict(data: dict[str, Any], key: str) -> dict[str, Any]:
    value = data.get(key)
    return value if isinstance(value, dict) else {}


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def safe_float(value: Any, default: float = 0.0) -> float:
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return float(value)
    if isinstance(value, str):
        try:
            return float(value)
        except ValueError:
            return default
    return default


def safe_int(value: Any, default: int = 0) -> int:
    if isinstance(value, int) and not isinstance(value, bool):
        return value
    if isinstance(value, float):
        return int(value)
    if isinstance(value, str) and value.isdigit():
        return int(value)
    return default


def first_int(default: int, *values: Any) -> int:
    for value in values:
        parsed = safe_int(value, default=-1)
        if parsed >= 0:
            return parsed
    return default


def audit_duration_seconds(audit: dict[str, Any]) -> float:
    started = audit.get("started_at")
    finished = audit.get("finished_at")
    if isinstance(started, str) and isinstance(finished, str):
        try:
            start_dt = datetime.fromisoformat(started)
            finish_dt = datetime.fromisoformat(finished)
            return max(0.0, (finish_dt - start_dt).total_seconds())
        except ValueError:
            pass
    return safe_float(audit.get("elapsed_seconds"))


def percentile(values: list[float], pct: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    index = min(len(ordered) - 1, max(0, round((pct / 100.0) * (len(ordered) - 1))))
    return ordered[index]


def build_suggestions(report: dict[str, Any], metrics: dict[str, Any]) -> dict[str, Any]:
    round_count = metrics["gpu_round_count"]
    audit_count = metrics["npu_audit_count"]
    coverage = metrics["npu_audit_round_coverage"]
    avg_gpu = metrics["avg_gpu_round_seconds"]
    avg_npu = metrics["avg_npu_audit_seconds"]
    skew = metrics["npu_to_gpu_avg_duration_ratio"]

    suggested_every = 4
    if avg_gpu > 0 and avg_npu > 0:
        suggested_every = max(2, min(8, round(avg_npu / avg_gpu)))

    suggestions = {
        "recommended_profile": "gpu_npu_balanced_advisory",
        "reasoning": [],
        "parameters": {
            "npu_auditor_every_rounds": suggested_every,
            "max_concurrent_npu_audits": 1,
            "npu_auditor_timeout_seconds": 420,
            "npu_max_context_chars": 8000,
            "npu_max_prompt_chars": 1200,
            "npu_max_new_tokens": 384,
            "npu_final_wait_seconds": 180,
            "gpu_max_new_tokens": 3600,
            "gpu_files_per_round": 8,
            "gpu_max_chars_per_file": 6000,
        },
        "guardrails": {
            "do_not_change_provider_model_settings_first": True,
            "keep_npu_auditor_non_blocking": True,
            "keep_max_concurrent_npu_audits": 1,
            "do_not_promote_npu_advisory": True,
            "do_not_make_openvino_gpu_primary": True,
        },
    }

    if audit_count == 0:
        suggestions["reasoning"].append("No NPU audits were observed; first verify provider availability before tuning cadence.")
    if coverage < 0.35 and round_count >= 12:
        suggestions["reasoning"].append("NPU audit coverage is low compared with GPU round count; keep checkpoint auditing sampled, not per-round.")
    if avg_gpu <= 0 and round_count > 0:
        suggestions["reasoning"].append("GPU per-round duration was unavailable in the orchestrator; using total GPU elapsed divided by round count as estimate.")
    if skew > 2.0:
        suggestions["reasoning"].append("Average NPU audit duration is much slower than one GPU round; reduce NPU prompt/context/tokens and audit every several rounds.")
    if metrics["npu_audit_success_count"] == audit_count and audit_count > 0:
        suggestions["reasoning"].append("NPU audits are usable; tune cadence rather than disabling the lane.")
    if report.get("gpu_empty_recommendations_reason") == "repair_attempt_failed" or report.get("empty_recommendations_reason") == "repair_attempt_failed":
        suggestions["reasoning"].append("GPU JSON contract hardening should be tested before increasing GPU token budget further.")
    return suggestions


def analyze(repo_root: Path, orchestrator_path: Path) -> dict[str, Any]:
    report = read_json(orchestrator_path)
    gpu_summary = nested_dict(report, "gpu_summary")
    rounds = report.get("rounds") if isinstance(report.get("rounds"), list) else []
    npu_audits = report.get("npu_audits") if isinstance(report.get("npu_audits"), list) else []
    gpu_round_durations = [safe_float(item.get("elapsed_seconds")) for item in rounds if isinstance(item, dict)]
    gpu_round_durations = [value for value in gpu_round_durations if value > 0]
    npu_durations = [audit_duration_seconds(item) for item in npu_audits if isinstance(item, dict)]
    npu_durations = [value for value in npu_durations if value > 0]
    round_count = first_int(len(rounds), report.get("round_count"), gpu_summary.get("round_count"))
    audit_count = first_int(len(npu_audits), report.get("npu_audit_count"))
    success_count = first_int(0, report.get("npu_audit_success_count"))
    gpu_elapsed = safe_float(report.get("gpu_elapsed_seconds")) or safe_float(gpu_summary.get("elapsed_seconds")) or safe_float(report.get("elapsed_seconds"))
    if not gpu_round_durations and round_count > 0 and gpu_elapsed > 0:
        gpu_round_durations = [gpu_elapsed / round_count]
    avg_gpu = sum(gpu_round_durations) / len(gpu_round_durations) if gpu_round_durations else 0.0
    avg_npu = sum(npu_durations) / len(npu_durations) if npu_durations else 0.0
    metrics = {
        "gpu_round_count": round_count,
        "npu_audit_count": audit_count,
        "npu_audit_success_count": success_count,
        "npu_audit_round_coverage": round(audit_count / round_count, 3) if round_count else 0.0,
        "avg_gpu_round_seconds": round(avg_gpu, 3),
        "p50_gpu_round_seconds": round(percentile(gpu_round_durations, 50), 3),
        "p90_gpu_round_seconds": round(percentile(gpu_round_durations, 90), 3),
        "avg_npu_audit_seconds": round(avg_npu, 3),
        "p50_npu_audit_seconds": round(percentile(npu_durations, 50), 3),
        "p90_npu_audit_seconds": round(percentile(npu_durations, 90), 3),
        "npu_to_gpu_avg_duration_ratio": round(avg_npu / avg_gpu, 3) if avg_gpu else 0.0,
        "gpu_elapsed_seconds": gpu_elapsed,
        "provider_execution_performed": bool(report.get("provider_execution_performed")),
        "patch_application_performed": bool(report.get("patch_application_performed")),
        "source_writes_performed": bool(report.get("source_writes_performed")),
        "gpu_metrics_source": "rounds" if report.get("rounds") else "gpu_summary_or_elapsed_estimate",
    }
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
        "suggestions": suggestions,
        "decision": {
            "npu_too_slow_for_per_round_lockstep": metrics["npu_to_gpu_avg_duration_ratio"] > 1.5,
            "recommended_next_layer": "run balanced profile and compare bundle evidence",
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
    lines.append("")
    lines.append("## Suggested balanced profile")
    lines.append("")
    for key, value in report["suggestions"]["parameters"].items():
        lines.append(f"- `{key}`: `{value}`")
    lines.append("")
    lines.append("## Reasoning")
    lines.append("")
    for item in report["suggestions"].get("reasoning", []):
        lines.append(f"- {item}")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--orchestrator", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--markdown-output", required=True)
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    report = analyze(repo_root, resolve_path(repo_root, args.orchestrator))
    output = resolve_path(repo_root, args.output)
    markdown_output = resolve_path(repo_root, args.markdown_output)
    write_json(output, report)
    markdown_output.parent.mkdir(parents=True, exist_ok=True)
    markdown_output.write_text(render_markdown(report) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "passed": report["passed"],
                "output": str(output),
                "markdown": str(markdown_output),
                "npu_to_gpu_avg_duration_ratio": report["metrics"]["npu_to_gpu_avg_duration_ratio"],
                "npu_too_slow_for_per_round_lockstep": report["decision"]["npu_too_slow_for_per_round_lockstep"],
                "patch_application_performed": report["patch_application_performed"],
                "source_writes_performed": report["source_writes_performed"],
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
