#!/usr/bin/env python3
"""Smoke resilient RAG embedding ingest without Ollama."""

from __future__ import annotations

import argparse
import json
import tempfile
from argparse import Namespace
from contextlib import closing
from pathlib import Path
from typing import Any

from Tools.validation._shared.report_utils import resolve_output_path, write_json_report
from ia_carmine.context.agent_context.rag_context.chunking import ChunkPolicy, build_chunks
from ia_carmine.context.agent_context.rag_context.common import sha256_text
from ia_carmine.context.agent_context.rag_context.ingest_repo_cli import embed_pending_chunks
from ia_carmine.context.agent_context.rag_context.store import (
    connect,
    missing_embedding_chunks,
    upsert_document_chunks,
)


def _embedder_split_required(
    *,
    endpoint: str,
    model: str,
    texts: list[str],
    timeout_seconds: float,
    retries: int,
) -> tuple[list[list[float]], list[str]]:
    _ = (endpoint, model, timeout_seconds, retries)
    if len(texts) > 1:
        return [], ["simulated HTTPError: HTTP Error 500: Internal Server Error"]
    return [[1.0, 0.0, 0.0] for _text in texts], []


def _embedder_one_bad_chunk(
    *,
    endpoint: str,
    model: str,
    texts: list[str],
    timeout_seconds: float,
    retries: int,
) -> tuple[list[list[float]], list[str]]:
    _ = (endpoint, model, timeout_seconds, retries)
    if len(texts) > 1:
        return [], ["simulated batch failure"]
    if "bad" in texts[0]:
        return [], ["simulated singleton failure"]
    return [[1.0, 0.0, 0.0]], []


def _embedder_requires_source_prefix(
    *,
    endpoint: str,
    model: str,
    texts: list[str],
    timeout_seconds: float,
    retries: int,
) -> tuple[list[list[float]], list[str]]:
    _ = (endpoint, model, timeout_seconds, retries)
    if len(texts) > 1:
        return [], ["simulated batch failure"]
    if "prefix-only" in texts[0] and not texts[0].startswith("Source:"):
        return [], ["simulated singleton raw text failure"]
    return [[1.0, 0.0, 0.0]], []


def _transient_singleton_embedder() -> Any:
    attempts: dict[str, int] = {}

    def embedder(
        *,
        endpoint: str,
        model: str,
        texts: list[str],
        timeout_seconds: float,
        retries: int,
    ) -> tuple[list[list[float]], list[str]]:
        _ = (endpoint, model, timeout_seconds, retries)
        if len(texts) > 1:
            return [], ["simulated batch failure"]
        key = texts[0]
        attempts[key] = attempts.get(key, 0) + 1
        if "transient" in key and attempts[key] == 1:
            return [], ["simulated transient singleton failure"]
        return [[1.0, 0.0, 0.0]], []

    return embedder


def _prepare_pending(db_path: Path, text: str) -> list[dict[str, Any]]:
    policy = ChunkPolicy(min_chars=20, max_chars=60, overlap_chars=0)
    chunks = build_chunks(
        source_path="docs/sample.md",
        text=text,
        content_hash=sha256_text(text),
        policy=policy,
        metadata={"fixture": True},
    )
    with closing(connect(db_path)) as conn:
        upsert_document_chunks(
            conn,
            source_path="docs/sample.md",
            file_size=len(text),
            mtime_ns=1,
            suffix=".md",
            content_hash=sha256_text(text),
            chunks=chunks,
            metadata={"fixture": True},
        )
        pending = missing_embedding_chunks(conn, model="bge-m3", endpoint="mock://fixture")
        conn.commit()
    return pending


def run_smoke() -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    with tempfile.TemporaryDirectory(prefix="rag-ingest-resilience-smoke-") as temp:
        db_ok = Path(temp) / "ok.sqlite"
        pending_ok = _prepare_pending(
            db_ok,
            ("alpha evidence chunk one. beta evidence chunk two. gamma evidence chunk three. " * 12),
        )
        with closing(connect(db_ok)) as conn:
            result_ok = embed_pending_chunks(
                conn,
                pending=pending_ok,
                args=Namespace(
                    batch_size=8,
                    embedding_endpoint="mock://fixture",
                    embedding_model="bge-m3",
                    final_singleton_retry_delays=[0.0, 0.0],
                ),
                embedder=_embedder_split_required,
            )
            remaining_ok = missing_embedding_chunks(
                conn, model="bge-m3", endpoint="mock://fixture"
            )
            conn.commit()
        checks.append(
            {
                "id": "split_batch_after_error_writes_all_embeddings",
                "passed": int(result_ok["written"]) == len(pending_ok)
                and not remaining_ok
                and bool(result_ok["retry_events"]),
                "evidence": {
                    "pending": len(pending_ok),
                    "written": result_ok["written"],
                    "remaining": len(remaining_ok),
                    "retry_events": result_ok["retry_events"],
                },
            }
        )
        db_transient = Path(temp) / "transient.sqlite"
        pending_transient = _prepare_pending(
            db_transient,
            ("transient evidence chunk. another stable evidence chunk. " * 12),
        )
        with closing(connect(db_transient)) as conn:
            result_transient = embed_pending_chunks(
                conn,
                pending=pending_transient,
                args=Namespace(
                    batch_size=8,
                    embedding_endpoint="mock://fixture",
                    embedding_model="bge-m3",
                    final_singleton_retry_delays=[0.0, 0.0],
                ),
                embedder=_transient_singleton_embedder(),
            )
            remaining_transient = missing_embedding_chunks(
                conn, model="bge-m3", endpoint="mock://fixture"
            )
            conn.commit()
        checks.append(
            {
                "id": "transient_singleton_failure_passes_after_final_retry",
                "passed": int(result_transient["written"]) == len(pending_transient)
                and not remaining_transient
                and any(
                    item.get("action") == "singleton_final_retry"
                    and item.get("passed") is True
                    for item in result_transient["retry_events"]
                ),
                "evidence": {
                    "pending": len(pending_transient),
                    "written": result_transient["written"],
                    "remaining": len(remaining_transient),
                    "retry_events": result_transient["retry_events"],
                },
            }
        )
        db_prefix = Path(temp) / "prefix.sqlite"
        pending_prefix = _prepare_pending(
            db_prefix,
            ("prefix-only evidence chunk. stable neighbor evidence chunk. " * 12),
        )
        with closing(connect(db_prefix)) as conn:
            result_prefix = embed_pending_chunks(
                conn,
                pending=pending_prefix,
                args=Namespace(
                    batch_size=8,
                    embedding_endpoint="mock://fixture",
                    embedding_model="bge-m3",
                    final_singleton_retry_delays=[0.0],
                ),
                embedder=_embedder_requires_source_prefix,
            )
            remaining_prefix = missing_embedding_chunks(
                conn, model="bge-m3", endpoint="mock://fixture"
            )
            conn.commit()
        checks.append(
            {
                "id": "pathological_singleton_passes_with_source_prefixed_retry",
                "passed": int(result_prefix["written"]) == len(pending_prefix)
                and not remaining_prefix
                and any(
                    item.get("action") == "singleton_source_prefixed_retry"
                    and item.get("passed") is True
                    for item in result_prefix["retry_events"]
                ),
                "evidence": {
                    "pending": len(pending_prefix),
                    "written": result_prefix["written"],
                    "remaining": len(remaining_prefix),
                    "retry_events": result_prefix["retry_events"],
                },
            }
        )
        db_bad = Path(temp) / "bad.sqlite"
        pending_bad = _prepare_pending(
            db_bad,
            ("good evidence chunk. bad evidence chunk. another good evidence chunk. " * 12),
        )
        with closing(connect(db_bad)) as conn:
            result_bad = embed_pending_chunks(
                conn,
                pending=pending_bad,
                args=Namespace(
                    batch_size=8,
                    embedding_endpoint="mock://fixture",
                    embedding_model="bge-m3",
                    final_singleton_retry_delays=[0.0, 0.0],
                ),
                embedder=_embedder_one_bad_chunk,
            )
            remaining_bad = missing_embedding_chunks(
                conn, model="bge-m3", endpoint="mock://fixture"
            )
            conn.commit()
        checks.append(
            {
                "id": "singleton_failure_remains_missing_for_hard_fail",
                "passed": int(result_bad["written"]) < len(pending_bad)
                and bool(remaining_bad)
                and bool(result_bad["failures"]),
                "evidence": {
                    "pending": len(pending_bad),
                    "written": result_bad["written"],
                    "remaining": len(remaining_bad),
                    "failures": result_bad["failures"],
                },
            }
        )
        checks.append(
            {
                "id": "permanent_singleton_failure_reports_rag_blocker",
                "passed": any(
                    item.get("blocker") == "rag_embedding_singleton_failed"
                    for item in result_bad["failures"]
                ),
                "evidence": result_bad["failures"],
            }
        )
    errors = [str(item["id"]) for item in checks if not item.get("passed")]
    return {
        "schema_version": 1,
        "kind": "rag_ingest_resilience_smoke",
        "passed": not errors,
        "checks": checks,
        "errors": errors,
        "warnings": [],
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output", default="output/validation/rag_ingest_resilience_smoke.json")
    args = parser.parse_args()
    repo_root = Path(args.repo_root).resolve()
    report = run_smoke()
    output = resolve_output_path(repo_root, args.output)
    write_json_report(report, output)
    print(json.dumps({"passed": report["passed"], "output": str(output)}, indent=2))
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
