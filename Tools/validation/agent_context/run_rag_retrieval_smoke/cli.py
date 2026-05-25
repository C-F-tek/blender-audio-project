#!/usr/bin/env python3
"""Fixture-only smoke for internal RAG retrieval."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from Tools.validation._shared.report_utils import resolve_output_path, write_json_report
from ia_carmine.context.agent_context.rag_context.chunking import ChunkPolicy, build_chunks
from ia_carmine.context.agent_context.rag_context.context_pack import build_context_pack
from ia_carmine.context.agent_context.rag_context.embedding import validate_vector
from ia_carmine.context.agent_context.rag_context.retrieval import hybrid_search
from ia_carmine.context.agent_context.rag_context.schema import integrity_check
from ia_carmine.context.agent_context.rag_context.store import (
    connect,
    insert_embedding,
    upsert_document_chunks,
)
from ia_carmine.context.agent_context.rag_context.common import sha256_text


def render_markdown(report: dict) -> str:
    lines = [
        "# RAG Retrieval Smoke",
        "",
        f"- Passed: `{report.get('passed')}`",
        f"- Retrieved count: `{report.get('retrieved_count')}`",
        f"- Vector hit source: `{report.get('vector_hit_source')}`",
        f"- Context pack output: `{report.get('context_pack_output')}`",
    ]
    if report.get("errors"):
        lines.extend(["", "## Errors", ""])
        lines.extend(f"- {item}" for item in report["errors"])
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output", default="output/validation/rag_retrieval_smoke.json")
    parser.add_argument("--markdown-output", default="output/validation/rag_retrieval_smoke.md")
    args = parser.parse_args()
    repo_root = Path(args.repo_root).resolve()
    work_dir = repo_root / "output" / "validation" / "rag_retrieval_smoke_fixture"
    db_path = work_dir / "rag.sqlite"
    pack_json = work_dir / "context_pack.json"
    work_dir.mkdir(parents=True, exist_ok=True)
    if db_path.exists():
        db_path.unlink()

    policy = ChunkPolicy(min_chars=80, max_chars=240, overlap_chars=20)
    fixtures = {
        "docs/LOCAL_AI_TASKS/rag_fixture.md": "GPU1 primary evidence uses generic_write evidence and heap context.",
        "ia_carmine/runtime/heap_gate/generic_write_followup.py": "GPU0 and NPU peer evidence requires later GPU1 consumption.",
    }
    with connect(db_path) as conn:
        for source, text in fixtures.items():
            chunks = build_chunks(
                source_path=source,
                text=text,
                content_hash=sha256_text(text),
                policy=policy,
            )
            upsert_document_chunks(
                conn,
                source_path=source,
                file_size=len(text),
                mtime_ns=1,
                suffix=Path(source).suffix,
                content_hash=sha256_text(text),
                chunks=chunks,
                metadata={"fixture": True},
            )
        rows = conn.execute("SELECT chunk_id, source_path FROM rag_chunks ORDER BY source_path").fetchall()
        for row in rows:
            vector = [1.0, 0.0, 0.0] if "LOCAL_AI_TASKS" in row["source_path"] else [0.1, 0.9, 0.0]
            values, norm, error = validate_vector(vector)
            if error:
                raise RuntimeError(error)
            insert_embedding(
                conn,
                chunk_id=row["chunk_id"],
                model="bge-m3",
                endpoint="mock://fixture",
                vector=values,
                norm=norm,
                metadata={"mock": True},
            )
        selected = hybrid_search(
            conn,
            query="generic_write evidence",
            query_vector=[1.0, 0.0, 0.0],
            query_norm=1.0,
            model="bge-m3",
            endpoint="mock://fixture",
            top_k=4,
            char_budget=4000,
        )
    pack = build_context_pack(
        repo_root=repo_root,
        db_path=db_path,
        rag_profile="runtime_code_context",
        query="generic_write evidence",
        embedding_endpoint="mock://fixture",
        embedding_model="bge-m3",
        query_embedding=False,
    )
    write_json_report(pack, pack_json)
    errors: list[str] = []
    if not selected:
        errors.append("hybrid_search returned no rows")
    if not pack.get("chunks"):
        errors.append("context pack returned no chunks")
    if pack.get("source_writes_performed") is not False:
        errors.append("context pack must not report source writes")
    report = {
        "schema_version": 1,
        "kind": "rag_retrieval_smoke",
        "passed": not errors,
        "errors": errors,
        "warnings": [],
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "retrieved_count": len(selected),
        "vector_hit_source": selected[0].get("source_path") if selected else "",
        "sqlite_integrity_check": integrity_check(db_path),
        "context_pack_output": str(pack_json),
    }
    output = resolve_output_path(repo_root, args.output)
    markdown = resolve_output_path(repo_root, args.markdown_output)
    write_json_report(report, output)
    markdown.parent.mkdir(parents=True, exist_ok=True)
    markdown.write_text(render_markdown(report), encoding="utf-8")
    print(json.dumps({"passed": report["passed"], "output": str(output)}, indent=2))
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
