"""Quality-gated advisory context routing."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .common import TRACKED_WORKLOAD_CONTEXT_FILES, WORKLOAD_QUALITY_REPORT, _ensure_repo_imports

def tracked_workload_context_decision(path: str, reason: str, error: str = "") -> dict[str, Any]:
    lane = (
        "npu"
        if path.endswith("npu_real_workload_report.md")
        else "ollama"
        if path.endswith("ollama_gpu_real_workload_report.md")
        else ""
    )
    return {
        "path": path,
        "lane": lane,
        "trusted": False,
        "reason": reason,
        "classification": "quality_unknown",
        "error": error,
    }

def build_advisory_context_routing(
    repo_root: Path, requested_context_files: list[str]
) -> dict[str, Any]:
    """Filter candidate context files before reading generated workload content."""

    _ensure_repo_imports(repo_root)
    try:
        from Tools.ai._shared.workload_quality import (  # noqa: PLC0415
            load_workload_quality_report,
            route_context_files_by_quality,
        )

        quality_report = load_workload_quality_report(repo_root, WORKLOAD_QUALITY_REPORT)
        routing = route_context_files_by_quality(requested_context_files, quality_report)
        routing["enforced"] = True
        routing["policy"] = "quality-approved-workload-context-only"
        routing["provider_execution_performed"] = False
        return routing
    except Exception as exc:  # noqa: BLE001 - keep non-workload docs open, workload reports closed.
        error = f"{type(exc).__name__}: {exc}"
        trusted = []
        excluded = []
        for path in requested_context_files:
            if any(
                path.replace("\\", "/").endswith(suffix)
                for suffix in TRACKED_WORKLOAD_CONTEXT_FILES
            ):
                excluded.append(
                    tracked_workload_context_decision(
                        path, "routing_unavailable_fail_closed", error
                    )
                )
            else:
                trusted.append(
                    {
                        "path": path,
                        "lane": "",
                        "trusted": True,
                        "reason": "routing_unavailable_non_workload_context",
                        "classification": "",
                    }
                )
        return {
            "quality_report_present": False,
            "advisory_lanes": [],
            "excluded_advisory_lanes": sorted(
                {item["lane"] for item in excluded if item.get("lane")}
            ),
            "trusted_context_files": trusted,
            "excluded_context_files": excluded,
            "decisions": trusted + excluded,
            "enforced": False,
            "policy": "routing_unavailable_fail_closed_for_tracked_workload_reports",
            "provider_execution_performed": False,
            "error": error,
        }
