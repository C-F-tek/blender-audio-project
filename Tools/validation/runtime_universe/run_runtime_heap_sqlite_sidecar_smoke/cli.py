#!/usr/bin/env python3
"""Smoke the provider runtime heap SQLite sidecar index."""

from __future__ import annotations

import argparse
import sqlite3
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    from Tools.ai.provider_runtime_blackboard import ProviderRuntimeHeap
    from Tools.validation._shared.report_utils import resolve_output_path, write_json_report
except ImportError:
    repo_root_for_import = Path(__file__).resolve().parents[4]
    if str(repo_root_for_import) not in sys.path:
        sys.path.insert(0, str(repo_root_for_import))
    from Tools.ai.provider_runtime_blackboard import ProviderRuntimeHeap  # type: ignore
    from Tools.validation._shared.report_utils import (  # type: ignore
        resolve_output_path,
        write_json_report,
    )


REQUIRED_TABLES = (
    "events",
    "payload_blobs",
    "latest_event_by_type",
    "pending_broker_requests",
    "provider_reports",
    "lane_status_materialized",
    "proposal_iterations",
    "decisions",
)


def table_count(conn: sqlite3.Connection, table: str) -> int:
    row = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()
    return int(row[0] or 0)


def sidecar_checks(db_path: Path, snapshot: dict[str, Any]) -> dict[str, bool]:
    if not db_path.is_file():
        return {"sqlite_sidecar_created": False}
    conn = sqlite3.connect(db_path)
    try:
        table_names = {
            str(row[0])
            for row in conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            ).fetchall()
        }
        table_counts = {table: table_count(conn, table) for table in REQUIRED_TABLES}
        resolved_row = conn.execute(
            "SELECT resolved FROM pending_broker_requests WHERE request_id=?",
            ("smoke:req:1",),
        ).fetchone()
        decision_row = conn.execute(
            "SELECT decision, reason FROM decisions WHERE decision_id=?",
            ("provider_universe_blocked",),
        ).fetchone()
        payload_blob_row = conn.execute(
            """
            SELECT payload_chars, payload_json FROM payload_blobs
            WHERE payload_chars > 10000
            ORDER BY payload_chars DESC
            LIMIT 1
            """
        ).fetchone()
    finally:
        conn.close()
    snapshot_index = snapshot.get("sqlite_index") if isinstance(snapshot, dict) else {}
    snapshot_index = snapshot_index if isinstance(snapshot_index, dict) else {}
    snapshot_counts = snapshot_index.get("table_counts")
    snapshot_counts = snapshot_counts if isinstance(snapshot_counts, dict) else {}
    return {
        "sqlite_sidecar_created": True,
        "required_tables_present": set(REQUIRED_TABLES).issubset(table_names),
        "events_indexed": table_counts["events"] >= 5,
        "full_payload_blobs_indexed": table_counts["payload_blobs"] >= 6,
        "large_payload_not_truncated_in_sidecar": (
            payload_blob_row is not None
            and int(payload_blob_row[0] or 0) > 10000
            and "STATIC_CONTEXT_SENTINEL_END" in str(payload_blob_row[1] or "")
        ),
        "snapshot_exposes_full_payload_chars": int(
            snapshot_index.get("full_payload_chars") or 0
        ) > 10000,
        "latest_events_indexed": table_counts["latest_event_by_type"] >= 4,
        "pending_request_indexed": table_counts["pending_broker_requests"] == 1,
        "pending_request_resolved": resolved_row is not None and int(resolved_row[0]) == 1,
        "provider_reports_indexed": table_counts["provider_reports"] >= 1,
        "lane_status_indexed": table_counts["lane_status_materialized"] >= 3,
        "proposal_iteration_indexed": table_counts["proposal_iterations"] == 1,
        "decision_indexed": (
            decision_row is not None
            and decision_row[0] == "blocked_with_reason"
            and decision_row[1] == "gpu1_nonproductive_runtime_stall"
        ),
        "snapshot_exposes_sqlite_index": snapshot_index.get("exists") is True,
        "snapshot_exposes_decision_count": int(snapshot_counts.get("decisions") or 0) == 1,
    }


def build_smoke_heap(repo_root: Path) -> tuple[ProviderRuntimeHeap, dict[str, Any]]:
    heap = ProviderRuntimeHeap.from_args(
        repo_root=repo_root,
        stamp="sqlite_sidecar_smoke",
        events_path="output/validation/runtime_heap_sqlite_sidecar_smoke/events.jsonl",
        snapshot_path="output/validation/runtime_heap_sqlite_sidecar_smoke/snapshot.json",
        markdown_path="output/validation/runtime_heap_sqlite_sidecar_smoke/snapshot.md",
    )
    for path in (
        heap.paths.events,
        heap.paths.snapshot,
        heap.paths.markdown,
        heap.sqlite_index_path(),
    ):
        if path.exists():
            path.unlink()
    heap.append_event(
        source="gpu1",
        target="broker",
        event_type="broker_request",
        correlation_id="smoke:req:1",
        round_id=1,
        payload={
            "request_id": "smoke:req:1",
            "requirement": "semantic_code_chunks",
            "tool": "select_semantic_code_chunks",
        },
    )
    heap.append_event(
        source="broker",
        target="gpu1",
        event_type="broker_result",
        correlation_id="smoke:req:1",
        round_id=1,
        payload={"request_id": "smoke:req:1", "passed": True},
    )
    heap.append_event(
        source="gpu0",
        target="orchestrator",
        event_type="provider_state",
        round_id=1,
        payload={
            "lane": "gpu0_peer",
            "requirement": "gpu0_provider_peer",
            "status": "non_operational",
            "operational_provider_activity": False,
            "diagnostic_only": True,
        },
    )
    heap.append_event(
        source="gpu1",
        target="orchestrator",
        event_type="provider_peer_block",
        round_id=1,
        payload={
            "lane": "gpu1_planner",
            "provider_block_id": "smoke:gpu1:000",
            "operational_provider_activity": True,
            "diagnostic_only": False,
        },
    )
    heap.append_event(
        source="orchestrator",
        target="deterministic",
        event_type="recommendation",
        round_id=1,
        payload={
            "kind": "proposal_iteration",
            "block_id": "smoke:proposal:000",
            "revision": 0,
            "status": "blocked",
        },
    )
    heap.append_event(
        source="deterministic",
        target="orchestrator",
        event_type="decision",
        correlation_id="smoke:decision:1",
        round_id=1,
        payload={
            "id": "provider_universe_blocked",
            "decision": "blocked_with_reason",
            "reason": "gpu1_nonproductive_runtime_stall",
            "revision": 0,
            "round": 1,
        },
    )
    heap.append_event(
        source="context_memory",
        target="orchestrator",
        event_type="fact",
        correlation_id="smoke:large-static-context",
        round_id=1,
        payload={
            "kind": "large_static_context_ref",
            "source": "startup_semantic_code_chunks.md",
            "full_context": "STATIC_CONTEXT_SENTINEL_START\n"
            + ("0123456789abcdef" * 900)
            + "\nSTATIC_CONTEXT_SENTINEL_END",
        },
    )
    return heap, heap.write_snapshot()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument(
        "--output",
        default="output/validation/runtime_heap_sqlite_sidecar_smoke.json",
    )
    args = parser.parse_args()
    repo_root = Path(args.repo_root).resolve()
    heap, snapshot = build_smoke_heap(repo_root)
    checks = sidecar_checks(heap.sqlite_index_path(), snapshot)
    errors = [
        f"runtime heap SQLite sidecar check failed: {name}"
        for name, ok in checks.items()
        if not ok
    ]
    report = {
        "schema_version": 1,
        "kind": "runtime_heap_sqlite_sidecar_smoke",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "repo_root": str(repo_root),
        "passed": not errors,
        "checks": checks,
        "sqlite_index": snapshot.get("sqlite_index"),
        "snapshot": str(heap.paths.snapshot),
        "markdown": str(heap.paths.markdown),
        "errors": errors,
        "source_writes_performed": False,
        "patch_application_performed": False,
    }
    output = resolve_output_path(repo_root, args.output)
    print(write_json_report(report, output), end="")
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
