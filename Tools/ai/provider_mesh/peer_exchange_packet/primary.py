"""Primary advisory and deterministic source summaries."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .common import compact_list, now_iso, read_json, repo_rel, resolve_output_path, safe_int

def primary_advisory(
    repo_root: Path, stamp: str, gpu_report_path: Path, gpu_markdown_path: Path
) -> dict[str, Any]:
    gpu_report = read_json(gpu_report_path)
    round_count = safe_int(gpu_report.get("round_count"))
    provider_performed = bool(gpu_report.get("provider_execution_performed"))
    empty = bool(gpu_report.get("provider_empty_response"))
    classification = str(gpu_report.get("classification") or "")
    proven = bool(
        provider_performed
        and round_count > 0
        and not empty
        and classification != "required_provider_artifact_missing"
    )
    classifications: list[str] = []
    if not proven:
        classifications.append("gpu1_primary_advisory_not_proven")
    if empty:
        classifications.append("gpu1_primary_advisory_empty_response")
    if classification:
        classifications.append(f"gpu1_primary_classification:{classification}")
    return {
        "schema_version": 1,
        "kind": "gpu1_primary_advisory",
        "generated_at": now_iso(),
        "stamp": stamp,
        "role": "gpu1_master_planner_worker",
        "lane": "GPU1/Ollama/RTX5080",
        "passed": proven,
        "provider_execution_performed": provider_performed,
        "gpu_report": repo_rel(repo_root, gpu_report_path),
        "gpu_markdown": (
            repo_rel(repo_root, gpu_markdown_path) if gpu_markdown_path.exists() else ""
        ),
        "gpu_report_exists": gpu_report_path.exists(),
        "round_count": round_count,
        "recommendation_count": safe_int(gpu_report.get("recommendation_count")),
        "runtime_tool_request_count": safe_int(gpu_report.get("runtime_tool_request_count")),
        "runtime_tool_execution_count": safe_int(gpu_report.get("runtime_tool_execution_count")),
        "provider_empty_response": empty,
        "classification": classification,
        "classifications": classifications,
        "errors": (
            []
            if proven
            else ["GPU1/Ollama primary advisory execution was not proven by the GPU report."]
        ),
        "warnings": [],
        "recommendations_preview": compact_list(gpu_report.get("recommendations")),
        "decision": (
            gpu_report.get("decision") if isinstance(gpu_report.get("decision"), dict) else {}
        ),
        "guardrails": {
            "report_only": True,
            "gpu1_reserved_for_primary_ollama": True,
            "openvino_gpu1_workload_allowed": False,
            "patch_application_performed": False,
            "source_writes_performed": False,
        },
    }

def source_summaries(repo_root: Path, paths: list[str]) -> list[dict[str, Any]]:
    summaries: list[dict[str, Any]] = []
    for raw in paths:
        path = resolve_output_path(repo_root, raw)
        data = read_json(path)
        summaries.append(
            {
                "path": repo_rel(repo_root, path),
                "exists": path.exists(),
                "kind": data.get("kind"),
                "passed": data.get("passed"),
                "classifications": (
                    data.get("classifications", [])
                    if isinstance(data.get("classifications"), list)
                    else []
                ),
                "errors": compact_list(data.get("errors"), 5),
                "warnings": compact_list(data.get("warnings"), 5),
            }
        )
    return summaries
