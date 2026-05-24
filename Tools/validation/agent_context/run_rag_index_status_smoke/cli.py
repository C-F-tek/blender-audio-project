#!/usr/bin/env python3
"""Smoke current/stale decisions for the internal RAG index without Ollama."""

from __future__ import annotations

import argparse
import json
import tempfile
from contextlib import closing
from pathlib import Path
from typing import Any

from Tools.validation._shared.report_utils import resolve_output_path, write_json_report
from ia_carmine.context.agent_context.rag_context.chunking import ChunkPolicy, build_chunks
from ia_carmine.context.agent_context.rag_context.common import sha256_text
from ia_carmine.context.agent_context.rag_context.index_status import inspect_index
from ia_carmine.context.agent_context.rag_context.schema import ensure_schema
from ia_carmine.context.agent_context.rag_context.store import (
    connect,
    insert_embedding,
    mark_absent_documents_inactive,
    upsert_document_chunks,
)


def _write_fixture(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _index_file(db: Path, repo: Path, rel_path: str, *, embed: bool) -> None:
    source = repo / rel_path
    text = source.read_text(encoding="utf-8")
    content_hash = sha256_text(text)
    policy = ChunkPolicy(min_chars=20, max_chars=80, overlap_chars=5).normalized()
    chunks = build_chunks(
        source_path=rel_path,
        text=text,
        content_hash=content_hash,
        policy=policy,
        metadata={"fixture": True},
    )
    with closing(connect(db)) as conn:
        upsert_document_chunks(
            conn,
            source_path=rel_path,
            file_size=source.stat().st_size,
            mtime_ns=source.stat().st_mtime_ns,
            suffix=source.suffix,
            content_hash=content_hash,
            chunks=chunks,
            metadata={"fixture": True},
        )
        if embed:
            for chunk in chunks:
                insert_embedding(
                    conn,
                    chunk_id=str(chunk["chunk_id"]),
                    model="mock-embed",
                    endpoint="mock://local",
                    vector=[1.0, 0.0, 0.0],
                    norm=1.0,
                )
        conn.commit()


def _status(db: Path, repo: Path) -> dict[str, Any]:
    return inspect_index(
        repo_root=repo,
        db_path=db,
        embedding_model="mock-embed",
        embedding_endpoint="mock://local",
        max_file_size=10000,
        chunk_policy=ChunkPolicy(min_chars=20, max_chars=80, overlap_chars=5),
    )


def run_smoke() -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    with tempfile.TemporaryDirectory(prefix="rag-index-status-smoke-") as tmp:
        repo = Path(tmp) / "repo"
        db = Path(tmp) / "rag.sqlite"
        source = repo / "docs" / "sample.md"
        _write_fixture(source, "GPU1 generic_write must stay anchored to real source files.")
        missing = _status(db, repo)
        checks.append(
            {
                "id": "db_missing_needs_ingest",
                "passed": missing.get("action") == "needs_ingest"
                and "rag_db_missing" in (missing.get("reasons") or []),
                "evidence": missing,
            }
        )
        ensure_schema(db)
        _index_file(db, repo, "docs/sample.md", embed=True)
        current = _status(db, repo)
        checks.append(
            {
                "id": "current_index_noop",
                "passed": current.get("action") == "noop_current"
                and current.get("rag_index_ready") is True,
                "evidence": current,
            }
        )
        _write_fixture(source, "GPU1 generic_write changed; RAG must detect the delta.")
        changed = _status(db, repo)
        checks.append(
            {
                "id": "changed_file_needs_ingest",
                "passed": "rag_documents_changed" in (changed.get("reasons") or []),
                "evidence": changed,
            }
        )
        _write_fixture(source, "GPU1 generic_write must stay anchored to real source files.")
        source.unlink()
        removed = _status(db, repo)
        checks.append(
            {
                "id": "removed_file_needs_ingest",
                "passed": "rag_documents_removed" in (removed.get("reasons") or []),
                "evidence": removed,
            }
        )
        _write_fixture(source, "GPU1 generic_write must stay anchored to real source files.")
        db_missing_embed = Path(tmp) / "missing_embed.sqlite"
        ensure_schema(db_missing_embed)
        _index_file(db_missing_embed, repo, "docs/sample.md", embed=False)
        missing_embed = _status(db_missing_embed, repo)
        checks.append(
            {
                "id": "missing_embeddings_needs_ingest",
                "passed": "rag_embeddings_missing" in (missing_embed.get("reasons") or []),
                "evidence": missing_embed,
            }
        )
        with closing(connect(db)) as conn:
            removed_count = mark_absent_documents_inactive(conn, set())
            conn.commit()
        checks.append(
            {
                "id": "mark_absent_documents_inactive",
                "passed": removed_count >= 1,
                "evidence": {"removed_count": removed_count},
            }
        )
    errors = [item["id"] for item in checks if not item["passed"]]
    return {
        "schema_version": 1,
        "kind": "rag_index_status_smoke",
        "passed": not errors,
        "checks": checks,
        "errors": errors,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output", default="output/validation/rag_index_status_smoke.json")
    args = parser.parse_args()
    repo_root = Path(args.repo_root).resolve()
    report = run_smoke()
    report["repo_root"] = repo_root.as_posix()
    report.setdefault("warnings", [])
    output = resolve_output_path(repo_root, args.output)
    write_json_report(report, output)
    print(json.dumps({"passed": report["passed"], "output": str(output)}, indent=2))
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
