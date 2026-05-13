from __future__ import annotations

import re
import sqlite3
from collections import Counter
from pathlib import Path
from typing import Any

from tools.ai.patch_plan_quality_product.io_utils import (
    flatten_json,
    read_text,
    repo_rel,
)

TOKEN_RE = re.compile(r"[A-Za-z0-9_./:-]{4,}")
BANNED = {
    "true",
    "false",
    "none",
    "null",
    "output",
    "validation",
    "report",
    "json",
    "markdown",
    "patch",
    "plan",
    "tools",
    "python",
    "manual",
    "review",
    "schema",
    "version",
    "passed",
    "errors",
    "warnings",
}


def safe_tokens(text: str, *, max_terms: int = 20) -> list[str]:
    counts = Counter(token.lower().strip("_-.") for token in TOKEN_RE.findall(text))
    out = []
    for token, _ in counts.most_common(120):
        if len(token) < 4 or token in BANNED:
            continue
        if token not in out:
            out.append(token)
        if len(out) >= max_terms:
            break
    return out


def ensure_fts(conn: sqlite3.Connection) -> bool:
    try:
        conn.execute(
            "CREATE VIRTUAL TABLE IF NOT EXISTS evidence_fts USING fts5(source, kind, content)"
        )
        return True
    except sqlite3.OperationalError:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS evidence_fts_fallback (rowid INTEGER PRIMARY KEY AUTOINCREMENT, source TEXT NOT NULL, kind TEXT NOT NULL, content TEXT NOT NULL)"
        )
        return False


def index_doc(
    conn: sqlite3.Connection, fts_enabled: bool, source: str, kind: str, content: str
) -> None:
    if not content.strip():
        return
    if fts_enabled:
        conn.execute(
            "INSERT INTO evidence_fts(source, kind, content) VALUES (?, ?, ?)",
            (source, kind, content),
        )
    else:
        conn.execute(
            "INSERT INTO evidence_fts_fallback(source, kind, content) VALUES (?, ?, ?)",
            (source, kind, content),
        )


def search_docs(
    conn: sqlite3.Connection, fts_enabled: bool, query: str, limit: int
) -> list[dict[str, Any]]:
    tokens = safe_tokens(query, max_terms=8)
    if not tokens:
        return []
    if fts_enabled:
        fts_query = " OR ".join(
            f'"{token.replace(chr(34), chr(34) + chr(34))}"' for token in tokens
        )
        rows = conn.execute(
            "SELECT source, kind, snippet(evidence_fts, 2, '[', ']', '…', 12) FROM evidence_fts WHERE evidence_fts MATCH ? LIMIT ?",
            (fts_query, limit),
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT source, kind, substr(content, 1, 320) FROM evidence_fts_fallback WHERE content LIKE ? LIMIT ?",
            ("%" + "%".join(tokens[:3]) + "%", limit),
        ).fetchall()
    return [{"source": row[0], "kind": row[1], "snippet": row[2]} for row in rows]


def build_search_index(
    conn: sqlite3.Connection,
    repo_root: Path,
    input_paths: dict[str, Path],
    loaded: dict[str, dict[str, Any]],
    request: str,
    extra_context: list[str],
) -> tuple[bool, int]:
    fts_enabled = ensure_fts(conn)
    conn.execute(
        "DELETE FROM evidence_fts"
        if fts_enabled
        else "DELETE FROM evidence_fts_fallback"
    )
    indexed = 0
    for key, path in input_paths.items():
        content = flatten_json(loaded.get(key, {}))
        if content and content != "{}":
            index_doc(conn, fts_enabled, repo_rel(path, repo_root), key, content)
            indexed += 1
    if request:
        index_doc(conn, fts_enabled, "inline_request", "request", request)
        indexed += 1
    for extra in extra_context:
        extra_path = (repo_root / extra).resolve()
        content = read_text(extra_path)
        if content:
            index_doc(
                conn,
                fts_enabled,
                repo_rel(extra_path, repo_root),
                "extra_context",
                content,
            )
            indexed += 1
    conn.commit()
    return fts_enabled, indexed
