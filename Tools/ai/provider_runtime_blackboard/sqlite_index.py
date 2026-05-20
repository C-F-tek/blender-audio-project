"""SQLite sidecar index for the provider runtime heap."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

from .common import safe_dict, safe_int


def index_runtime_heap_event(db_path: Path, event: dict[str, Any]) -> None:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    try:
        _ensure_schema(conn)
        payload = safe_dict(event.get("payload"))
        payload_json = json.dumps(payload, ensure_ascii=False, sort_keys=True, default=str)
        cursor = conn.execute(
            """
            INSERT INTO events(
                stamp, created_at, source, target, round_id,
                event_type, correlation_id, payload_json
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                event.get("stamp"),
                event.get("created_at"),
                event.get("source"),
                event.get("target"),
                event.get("round"),
                event.get("event_type"),
                event.get("correlation_id") or "",
                payload_json,
            ),
        )
        event_id = int(cursor.lastrowid)
        _index_latest_event(conn, event, event_id, payload_json)
        _index_lane_status(conn, event, event_id)
        _index_pending_broker(conn, event, event_id, payload, payload_json)
        _index_provider_report(conn, event, event_id, payload, payload_json)
        _index_proposal_iteration(conn, event_id, payload, payload_json)
        _index_decision(conn, event, event_id, payload, payload_json)
        conn.commit()
    finally:
        conn.close()


def _ensure_schema(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS events(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            stamp TEXT NOT NULL,
            created_at TEXT,
            source TEXT,
            target TEXT,
            round_id INTEGER,
            event_type TEXT,
            correlation_id TEXT,
            payload_json TEXT NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_runtime_events_type ON events(event_type);
        CREATE INDEX IF NOT EXISTS idx_runtime_events_lane ON events(source, target);

        CREATE TABLE IF NOT EXISTS latest_event_by_type(
            event_type TEXT NOT NULL,
            source TEXT NOT NULL,
            event_id INTEGER NOT NULL,
            created_at TEXT,
            payload_json TEXT NOT NULL,
            PRIMARY KEY(event_type, source)
        );

        CREATE TABLE IF NOT EXISTS pending_broker_requests(
            request_id TEXT PRIMARY KEY,
            event_id INTEGER NOT NULL,
            created_at TEXT,
            source TEXT,
            target TEXT,
            requirement TEXT,
            tool TEXT,
            resolved INTEGER NOT NULL DEFAULT 0,
            payload_json TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS provider_reports(
            event_id INTEGER PRIMARY KEY,
            lane TEXT,
            requirement TEXT,
            operational_provider_activity INTEGER,
            diagnostic_only INTEGER,
            status TEXT,
            payload_json TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS lane_status_materialized(
            lane TEXT PRIMARY KEY,
            latest_event_id INTEGER NOT NULL,
            latest_event_type TEXT,
            latest_status TEXT,
            latest_at TEXT,
            event_count INTEGER NOT NULL DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS proposal_iterations(
            event_id INTEGER PRIMARY KEY,
            block_id TEXT,
            revision INTEGER,
            status TEXT,
            payload_json TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS decisions(
            event_id INTEGER PRIMARY KEY,
            decision_id TEXT,
            decision TEXT,
            reason TEXT,
            revision INTEGER,
            round_id INTEGER,
            payload_json TEXT NOT NULL
        );
        """
    )


def _index_latest_event(
    conn: sqlite3.Connection,
    event: dict[str, Any],
    event_id: int,
    payload_json: str,
) -> None:
    conn.execute(
        """
        INSERT INTO latest_event_by_type(event_type, source, event_id, created_at, payload_json)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(event_type, source) DO UPDATE SET
            event_id=excluded.event_id,
            created_at=excluded.created_at,
            payload_json=excluded.payload_json
        """,
        (
            event.get("event_type") or "",
            event.get("source") or "",
            event_id,
            event.get("created_at"),
            payload_json,
        ),
    )


def _index_lane_status(conn: sqlite3.Connection, event: dict[str, Any], event_id: int) -> None:
    payload = safe_dict(event.get("payload"))
    status = str(payload.get("status") or payload.get("state") or "")
    conn.execute(
        """
        INSERT INTO lane_status_materialized(
            lane, latest_event_id, latest_event_type, latest_status, latest_at, event_count
        )
        VALUES (?, ?, ?, ?, ?, 1)
        ON CONFLICT(lane) DO UPDATE SET
            latest_event_id=excluded.latest_event_id,
            latest_event_type=excluded.latest_event_type,
            latest_status=excluded.latest_status,
            latest_at=excluded.latest_at,
            event_count=lane_status_materialized.event_count + 1
        """,
        (
            event.get("source") or "",
            event_id,
            event.get("event_type") or "",
            status,
            event.get("created_at"),
        ),
    )


def _index_pending_broker(
    conn: sqlite3.Connection,
    event: dict[str, Any],
    event_id: int,
    payload: dict[str, Any],
    payload_json: str,
) -> None:
    event_type = str(event.get("event_type") or "")
    request_id = str(event.get("correlation_id") or payload.get("request_id") or payload.get("id") or "")
    if not request_id:
        return
    if event_type == "broker_request":
        conn.execute(
            """
            INSERT INTO pending_broker_requests(
                request_id, event_id, created_at, source, target,
                requirement, tool, resolved, payload_json
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, 0, ?)
            ON CONFLICT(request_id) DO UPDATE SET
                event_id=excluded.event_id,
                created_at=excluded.created_at,
                source=excluded.source,
                target=excluded.target,
                requirement=excluded.requirement,
                tool=excluded.tool,
                resolved=0,
                payload_json=excluded.payload_json
            """,
            (
                request_id,
                event_id,
                event.get("created_at"),
                event.get("source"),
                event.get("target"),
                payload.get("requirement") or "",
                payload.get("tool") or "",
                payload_json,
            ),
        )
    elif event_type == "broker_result":
        conn.execute(
            "UPDATE pending_broker_requests SET resolved=1 WHERE request_id=?",
            (request_id,),
        )


def _index_provider_report(
    conn: sqlite3.Connection,
    event: dict[str, Any],
    event_id: int,
    payload: dict[str, Any],
    payload_json: str,
) -> None:
    if str(event.get("event_type") or "") not in {"provider_state", "provider_peer_block"}:
        return
    lane = str(payload.get("lane") or event.get("source") or "")
    conn.execute(
        """
        INSERT OR REPLACE INTO provider_reports(
            event_id, lane, requirement, operational_provider_activity,
            diagnostic_only, status, payload_json
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            event_id,
            lane,
            payload.get("requirement") or "",
            _sqlite_bool(payload.get("operational_provider_activity")),
            _sqlite_bool(payload.get("diagnostic_only")),
            payload.get("status") or "",
            payload_json,
        ),
    )


def _index_proposal_iteration(
    conn: sqlite3.Connection,
    event_id: int,
    payload: dict[str, Any],
    payload_json: str,
) -> None:
    if str(payload.get("kind") or "") not in {
        "proposal_iteration",
        "heap_proposal_iteration",
    } and str(payload.get("block_type") or "") != "proposal_block":
        return
    conn.execute(
        """
        INSERT OR REPLACE INTO proposal_iterations(
            event_id, block_id, revision, status, payload_json
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            event_id,
            payload.get("block_id") or payload.get("proposal_block_id") or "",
            safe_int(payload.get("revision")),
            payload.get("status") or "",
            payload_json,
        ),
    )


def _index_decision(
    conn: sqlite3.Connection,
    event: dict[str, Any],
    event_id: int,
    payload: dict[str, Any],
    payload_json: str,
) -> None:
    if str(event.get("event_type") or "") != "decision" and not payload.get("decision"):
        return
    conn.execute(
        """
        INSERT OR REPLACE INTO decisions(
            event_id, decision_id, decision, reason, revision, round_id, payload_json
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            event_id,
            payload.get("id") or event.get("correlation_id") or f"event:{event_id}",
            payload.get("decision") or "",
            payload.get("reason") or "",
            safe_int(payload.get("revision")),
            safe_int(payload.get("round") if payload.get("round") is not None else event.get("round")),
            payload_json,
        ),
    )


def runtime_heap_index_summary(db_path: Path) -> dict[str, Any]:
    summary: dict[str, Any] = {
        "path": str(db_path),
        "exists": db_path.is_file(),
        "table_counts": {},
        "pending_unresolved_count": 0,
        "latest_event_type_count": 0,
    }
    if not db_path.is_file():
        return summary
    conn = sqlite3.connect(db_path)
    try:
        _ensure_schema(conn)
        table_counts = {
            table: _table_count(conn, table)
            for table in (
                "events",
                "latest_event_by_type",
                "pending_broker_requests",
                "provider_reports",
                "lane_status_materialized",
                "proposal_iterations",
                "decisions",
            )
        }
        unresolved = conn.execute(
            "SELECT COUNT(*) FROM pending_broker_requests WHERE resolved=0"
        ).fetchone()
        summary.update(
            {
                "table_counts": table_counts,
                "pending_unresolved_count": int(unresolved[0] or 0),
                "latest_event_type_count": table_counts.get("latest_event_by_type", 0),
            }
        )
    finally:
        conn.close()
    return summary


def _table_count(conn: sqlite3.Connection, table: str) -> int:
    row = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()
    return int(row[0] or 0)


def _sqlite_bool(value: Any) -> int | None:
    if value is True:
        return 1
    if value is False:
        return 0
    return None
