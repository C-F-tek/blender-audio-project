"""Current/stale checks for the internal RAG SQLite index."""

from __future__ import annotations

from contextlib import closing
from pathlib import Path
from typing import Any

from .chunking import ChunkPolicy
from .common import DEFAULT_MAX_FILE_SIZE, read_text, sha256_text
from .repo_files import list_repo_text_files
from .schema import integrity_check
from .store import connect, missing_embedding_chunks, status


def candidate_content_hashes(repo_root: Path, *, max_file_size: int) -> tuple[dict[str, str], list[str]]:
    files, _skipped, warnings = list_repo_text_files(
        repo_root, max_file_size=max(1, int(max_file_size))
    )
    hashes: dict[str, str] = {}
    for item in files:
        text, error = read_text(item.path)
        if error:
            warnings.append(f"{item.rel_path}: {error}")
        if text.strip():
            hashes[item.rel_path] = sha256_text(text)
    return hashes, warnings


def inspect_index(
    *,
    repo_root: Path,
    db_path: Path,
    embedding_model: str,
    embedding_endpoint: str,
    max_file_size: int = DEFAULT_MAX_FILE_SIZE,
    chunk_policy: ChunkPolicy | None = None,
) -> dict[str, Any]:
    policy = (chunk_policy or ChunkPolicy()).normalized()
    candidates, warnings = candidate_content_hashes(repo_root, max_file_size=max_file_size)
    report: dict[str, Any] = {
        "schema_version": 1,
        "kind": "rag_index_status",
        "db_path": str(db_path),
        "candidate_file_count": len(candidates),
        "candidate_policy": {
            "max_file_size": int(max_file_size),
            "chunk_policy_hash": policy.policy_hash(),
        },
        "embedding_model": embedding_model,
        "embedding_endpoint": embedding_endpoint,
        "warnings": warnings[:80],
        "errors": [],
        "reasons": [],
        "missing_document_paths": [],
        "changed_document_paths": [],
        "removed_document_paths": [],
        "missing_embedding_count": 0,
        "rag_index_ready": False,
        "action": "needs_ingest",
    }
    if not db_path.exists():
        report["reasons"].append("rag_db_missing")
        return report
    try:
        integrity = integrity_check(db_path)
    except Exception as exc:  # noqa: BLE001
        report["errors"].append(f"rag_db_integrity_unreadable: {type(exc).__name__}: {exc}")
        report["reasons"].append("rag_db_integrity_unreadable")
        report["action"] = "block"
        return report
    report["sqlite_integrity_check"] = integrity
    if integrity != "ok":
        report["errors"].append(f"rag_db_integrity_not_ok: {integrity}")
        report["reasons"].append("rag_db_integrity_not_ok")
        report["action"] = "block"
        return report
    with closing(connect(db_path)) as conn:
        rows = conn.execute(
            "SELECT source_path, content_hash FROM rag_documents WHERE status='active'"
        ).fetchall()
        active_docs = {str(row["source_path"]): str(row["content_hash"]) for row in rows}
        db_status = status(conn)
        missing_embeddings = missing_embedding_chunks(
            conn, model=embedding_model, endpoint=embedding_endpoint
        )
    candidate_paths = set(candidates)
    active_paths = set(active_docs)
    missing_paths = sorted(candidate_paths - active_paths)
    changed_paths = sorted(
        path for path in candidate_paths & active_paths if active_docs.get(path) != candidates[path]
    )
    removed_paths = sorted(active_paths - candidate_paths)
    report.update(
        {
            "db_status": db_status,
            "document_count": db_status.get("document_count", 0),
            "active_chunk_count": db_status.get("active_chunk_count", 0),
            "embedding_count": db_status.get("embedding_count", 0),
            "missing_document_paths": missing_paths[:80],
            "changed_document_paths": changed_paths[:80],
            "removed_document_paths": removed_paths[:80],
            "missing_embedding_count": len(missing_embeddings),
        }
    )
    if not db_status.get("document_count"):
        report["reasons"].append("rag_document_count_zero")
    if not db_status.get("active_chunk_count"):
        report["reasons"].append("rag_active_chunk_count_zero")
    if missing_paths:
        report["reasons"].append("rag_documents_missing")
    if changed_paths:
        report["reasons"].append("rag_documents_changed")
    if removed_paths:
        report["reasons"].append("rag_documents_removed")
    if missing_embeddings:
        report["reasons"].append("rag_embeddings_missing")
    report["rag_index_ready"] = not report["reasons"] and not report["errors"]
    report["action"] = "noop_current" if report["rag_index_ready"] else "needs_ingest"
    return report
