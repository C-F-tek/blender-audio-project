"""Runtime heap and line-count summaries."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

from .common import repo_rel, resolve_output_path, safe_dict, safe_int, safe_list

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
        "parse_error_count": safe_int(
            telemetry.get("parse_error_count") or snapshot.get("parse_error_count")
        ),
        "direct_execution_violation_count": safe_int(
            telemetry.get("direct_execution_violation_count")
        ),
        "pending_broker_request_count": safe_int(
            telemetry.get("pending_broker_request_count")
            or snapshot.get("pending_broker_request_count")
        ),
        "events_by_lane": (
            telemetry.get("events_by_lane")
            if isinstance(telemetry.get("events_by_lane"), dict)
            else {}
        ),
        "events_by_type": (
            telemetry.get("events_by_type")
            if isinstance(telemetry.get("events_by_type"), dict)
            else {}
        ),
        "interaction_edges": (
            telemetry.get("interaction_edges")
            if isinstance(telemetry.get("interaction_edges"), dict)
            else {}
        ),
        "gpu1_to_gpu0_event_count": safe_int(telemetry.get("gpu1_to_gpu0_event_count")),
        "gpu0_to_gpu1_event_count": safe_int(telemetry.get("gpu0_to_gpu1_event_count")),
        "gpu1_gpu0_bidirectional": bool(telemetry.get("gpu1_gpu0_bidirectional")),
        "broker_result_count": safe_int(telemetry.get("broker_result_count")),
        "live_signals": live_signal_rows,
    }

def line_count_csv_summary(repo_root: Path, value: str) -> tuple[dict[str, Any], list[str]]:
    if not value:
        return {
            "seen": False,
            "path": "",
            "row_count": 0,
            "total_lines": 0,
            "top_files": [],
        }, []
    path = resolve_output_path(repo_root, value)
    path_rel = repo_rel(repo_root, path)
    if not path.exists():
        return {
            "seen": False,
            "path": path_rel,
            "row_count": 0,
            "total_lines": 0,
            "top_files": [],
        }, [f"line-count CSV missing: {path_rel}"]
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            rows = [dict(row) for row in csv.DictReader(handle)]
    except OSError as exc:
        return {
            "seen": False,
            "path": path_rel,
            "row_count": 0,
            "total_lines": 0,
            "top_files": [],
        }, [f"unable to read line-count CSV {path_rel}: {exc}"]
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
