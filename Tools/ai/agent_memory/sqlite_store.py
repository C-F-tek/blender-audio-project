"""Runtime SQLite memory storage operations."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

from .common import safe_identifier, utc_now_iso


def now_iso() -> str:
    return utc_now_iso()


def safe_id(value: str) -> str:
    return safe_identifier(value, "runtime_memory")

def ensure_operational_db(db_path: Path) -> None:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("""
            CREATE TABLE IF NOT EXISTS operational_memory_records (
                record_id TEXT PRIMARY KEY,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                kind TEXT NOT NULL,
                scope TEXT NOT NULL,
                role TEXT NOT NULL,
                summary TEXT NOT NULL,
                content TEXT NOT NULL,
                tags_json TEXT NOT NULL,
                metadata_json TEXT NOT NULL
            )
            """)
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_operational_memory_kind ON operational_memory_records(kind)"
        )
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_operational_memory_scope ON operational_memory_records(scope)"
        )
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_operational_memory_role ON operational_memory_records(role)"
        )
        conn.execute("""
            CREATE TABLE IF NOT EXISTS operational_memory_meta (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
            """)
        conn.execute(
            "INSERT OR REPLACE INTO operational_memory_meta(key, value) VALUES('schema_version', '1')"
        )
        conn.execute(
            "INSERT OR REPLACE INTO operational_memory_meta(key, value) VALUES('memory_class', 'operational_context')"
        )

def operational_status(db_path: Path) -> dict[str, Any]:
    ensure_operational_db(db_path)
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        row_count = conn.execute("SELECT count(*) FROM operational_memory_records").fetchone()[0]
        kind_rows = conn.execute(
            "SELECT kind, count(*) AS count FROM operational_memory_records GROUP BY kind ORDER BY count DESC, kind"
        ).fetchall()
        role_rows = conn.execute(
            "SELECT role, count(*) AS count FROM operational_memory_records GROUP BY role ORDER BY count DESC, role"
        ).fetchall()
    return {
        "record_count": row_count,
        "kind_counts": {str(row["kind"]): int(row["count"]) for row in kind_rows},
        "role_counts": {str(row["role"]): int(row["count"]) for row in role_rows},
    }

def persistent_status(db_path: Path) -> dict[str, Any]:
    if not db_path.exists():
        return {
            "exists": False,
            "opened_read_only": False,
            "record_count": 0,
            "tables": [],
        }
    tables: list[dict[str, Any]] = []
    record_count = 0
    uri = f"file:{db_path.as_posix()}?mode=ro"
    with sqlite3.connect(uri, uri=True) as conn:
        conn.row_factory = sqlite3.Row
        table_rows = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        ).fetchall()
        for row in table_rows:
            table_name = str(row["name"])
            try:
                count = conn.execute(
                    f'SELECT count(*) FROM "{table_name.replace(chr(34), chr(34) + chr(34))}"'
                ).fetchone()[0]
            except Exception:
                count = None
            tables.append({"name": table_name, "row_count": count})
        if any(item["name"] == "memory_records" for item in tables):
            record_count = conn.execute("SELECT count(*) FROM memory_records").fetchone()[0]
    return {
        "exists": True,
        "opened_read_only": True,
        "record_count": record_count,
        "tables": tables,
    }

def ensure_persistent_db(db_path: Path) -> None:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("""
            CREATE TABLE IF NOT EXISTS memory_records (
                record_id TEXT PRIMARY KEY,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                kind TEXT NOT NULL,
                scope TEXT NOT NULL,
                source TEXT NOT NULL,
                summary TEXT NOT NULL,
                content TEXT NOT NULL,
                tags_json TEXT NOT NULL,
                metadata_json TEXT NOT NULL
            )
            """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_memory_records_kind ON memory_records(kind)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_memory_records_scope ON memory_records(scope)")
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_memory_records_source ON memory_records(source)"
        )

def remember_operational(
    db_path: Path,
    *,
    summary: str,
    content: str,
    role: str,
    tags: list[str],
    metadata: dict[str, Any],
) -> dict[str, Any]:
    ensure_operational_db(db_path)
    timestamp = now_iso()
    identity = f"{timestamp}:{role}:{summary}:{content}"
    record_id = safe_id(identity)[:48]
    if not content.strip():
        raise ValueError("content is required for operational remember")
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            INSERT OR REPLACE INTO operational_memory_records (
                record_id, created_at, updated_at, kind, scope, role,
                summary, content, tags_json, metadata_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                record_id,
                timestamp,
                timestamp,
                "operational_context",
                "runtime",
                role,
                summary or content[:180],
                content,
                json.dumps(tags, ensure_ascii=False),
                json.dumps(metadata, ensure_ascii=False),
            ),
        )
    return {"record_id": record_id, "created_at": timestamp}

def remember_persistent(
    db_path: Path,
    *,
    summary: str,
    content: str,
    source: str,
    tags: list[str],
    metadata: dict[str, Any],
) -> dict[str, Any]:
    ensure_persistent_db(db_path)
    timestamp = now_iso()
    identity = f"{timestamp}:{source}:{summary}:{content}"
    record_id = safe_id(identity)[:64]
    if not content.strip():
        raise ValueError("content is required for persistent remember")
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            INSERT OR REPLACE INTO memory_records (
                record_id, created_at, updated_at, kind, scope, source,
                summary, content, tags_json, metadata_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                record_id,
                timestamp,
                timestamp,
                "project_operating_rule",
                "persistent",
                source,
                summary or content[:180],
                content,
                json.dumps(tags, ensure_ascii=False),
                json.dumps(metadata, ensure_ascii=False),
            ),
        )
    return {
        "record_id": record_id,
        "created_at": timestamp,
        "persistent_database_written": True,
    }

def search_operational(db_path: Path, query: str, limit: int) -> list[dict[str, Any]]:
    ensure_operational_db(db_path)
    pattern = f"%{query}%"
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        if query:
            rows = conn.execute(
                """
                SELECT record_id, created_at, updated_at, kind, scope, role, summary, content, tags_json, metadata_json
                FROM operational_memory_records
                WHERE summary LIKE ? OR content LIKE ? OR tags_json LIKE ? OR role LIKE ?
                ORDER BY updated_at DESC
                LIMIT ?
                """,
                (pattern, pattern, pattern, pattern, int(limit)),
            ).fetchall()
        else:
            rows = conn.execute(
                """
                SELECT record_id, created_at, updated_at, kind, scope, role, summary, content, tags_json, metadata_json
                FROM operational_memory_records
                ORDER BY updated_at DESC
                LIMIT ?
                """,
                (int(limit),),
            ).fetchall()
    return [row_to_dict(row) for row in rows]

def search_persistent(db_path: Path, query: str, limit: int) -> list[dict[str, Any]]:
    if not db_path.exists():
        return []
    pattern = f"%{query}%"
    uri = f"file:{db_path.as_posix()}?mode=ro"
    with sqlite3.connect(uri, uri=True) as conn:
        conn.row_factory = sqlite3.Row
        has_memory_records = conn.execute(
            "SELECT count(*) FROM sqlite_master WHERE type='table' AND name='memory_records'"
        ).fetchone()[0]
        if not has_memory_records:
            return []
        if query:
            rows = conn.execute(
                """
                SELECT record_id, created_at, updated_at, kind, scope, source, summary, content, tags_json, metadata_json
                FROM memory_records
                WHERE summary LIKE ? OR content LIKE ? OR tags_json LIKE ? OR source LIKE ?
                ORDER BY COALESCE(updated_at, created_at) DESC
                LIMIT ?
                """,
                (pattern, pattern, pattern, pattern, int(limit)),
            ).fetchall()
        else:
            rows = conn.execute(
                """
                SELECT record_id, created_at, updated_at, kind, scope, source, summary, content, tags_json, metadata_json
                FROM memory_records
                ORDER BY COALESCE(updated_at, created_at) DESC
                LIMIT ?
                """,
                (int(limit),),
            ).fetchall()
    return [persistent_row_to_dict(row) for row in rows]

def row_to_dict(row: sqlite3.Row) -> dict[str, Any]:
    return {
        "record_id": row["record_id"],
        "created_at": row["created_at"],
        "updated_at": row["updated_at"],
        "kind": row["kind"],
        "scope": row["scope"],
        "role": row["role"],
        "summary": row["summary"],
        "content_preview": str(row["content"])[:1000],
        "tags": json.loads(row["tags_json"] or "[]"),
        "metadata": json.loads(row["metadata_json"] or "{}"),
    }

def persistent_row_to_dict(row: sqlite3.Row) -> dict[str, Any]:
    return {
        "record_id": row["record_id"],
        "created_at": row["created_at"],
        "updated_at": row["updated_at"],
        "kind": row["kind"],
        "scope": row["scope"],
        "source": row["source"],
        "summary": row["summary"],
        "content_preview": str(row["content"])[:1000],
        "tags": json.loads(row["tags_json"] or "[]"),
        "metadata": json.loads(row["metadata_json"] or "{}"),
    }

def clear_operational(db_path: Path, confirm: str) -> dict[str, Any]:
    ensure_operational_db(db_path)
    if confirm != "clear_operational":
        raise ValueError("clear_operational requires --confirm clear_operational")
    before = operational_status(db_path)["record_count"]
    with sqlite3.connect(db_path) as conn:
        conn.execute("DELETE FROM operational_memory_records")
    return {"cleared": before, "remaining": operational_status(db_path)["record_count"]}
