"""FTS and hybrid-ready search for Full0To10 SQLite memory."""
from __future__ import annotations

import sqlite3
from typing import Any

from .schema import init_schema


def memory_search(
    conn: sqlite3.Connection,
    namespace: str,
    query: str,
    limit: int = 10,
    mode: str = "hybrid",
) -> dict[str, Any]:
    init_schema(conn)
    rows = conn.execute(
        """
        SELECT chunk_id, namespace, heading_path, text, bm25(memory_chunks_fts) AS rank
        FROM memory_chunks_fts
        WHERE memory_chunks_fts MATCH ? AND namespace = ?
        ORDER BY rank
        LIMIT ?
        """,
        (query, namespace, limit),
    ).fetchall()
    results = []
    for row in rows:
        raw_rank = float(row["rank"])
        fts_score = 1.0 / (1.0 + abs(raw_rank))
        results.append(
            {
                "chunk_id": row["chunk_id"],
                "namespace": row["namespace"],
                "heading_path": row["heading_path"],
                "fts_score": fts_score,
                "vector_score": None,
                "hybrid_score": fts_score,
                "text_preview": row["text"][:500],
            }
        )
    return {
        "kind": "memory_search",
        "passed": True,
        "namespace": namespace,
        "query": query,
        "mode": mode,
        "result_count": len(results),
        "embedding_cache_used": False,
        "results": results,
    }
