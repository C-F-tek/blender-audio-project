"""Artifact builders for heap startup reload."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from Tools.ai.heap_context_memory_reload.common import (
    read_text,
    repo_rel,
    sha256_text,
    write_json,
    write_markdown,
)
from Tools.ai.heap_context_memory_reload.scanner import repo_scan_semantic_candidates

STARTUP_SEMANTIC_PREVIEW_CHUNK_LIMIT = 80
STARTUP_SEMANTIC_PREVIEW_CHARS = 1600
STARTUP_SEMANTIC_MARKDOWN_ROW_LIMIT = 240
STARTUP_SEMANTIC_MARKDOWN_PREVIEW_BLOCKS = 16
STARTUP_DOCS_MAP_PREVIEW_LIMIT = 80
STARTUP_DOCS_MAP_PREVIEW_CHARS = 1200
STARTUP_DOCS_MAP_MARKDOWN_ROW_LIMIT = 240
STARTUP_DOCS_MAP_MARKDOWN_PREVIEW_BLOCKS = 16


def build_repo_docs_map(
    repo_root: Path, context_files: list[str], output_dir: Path
) -> dict[str, str]:
    docs = []
    for index, rel_path in enumerate(context_files):
        full = repo_root / rel_path
        preview_included = index < STARTUP_DOCS_MAP_PREVIEW_LIMIT
        text = read_text(full, max_chars=STARTUP_DOCS_MAP_PREVIEW_CHARS) if preview_included else ""
        docs.append(
            {
                "path": rel_path,
                "size_bytes": full.stat().st_size if full.exists() else 0,
                "preview_included": preview_included,
                "preview_chars": len(text),
                "sha256_scope": "preview" if text else "",
                "sha256": sha256_text(text),
                "preview": text,
            }
        )
    data = {
        "schema_version": 1,
        "kind": "heap_startup_repo_docs_map",
        "passed": True,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "document_count": len(docs),
        "live_artifact_policy": "all_context_paths_indexed; bounded previews only",
        "preview_document_limit": STARTUP_DOCS_MAP_PREVIEW_LIMIT,
        "stored_preview_chars": STARTUP_DOCS_MAP_PREVIEW_CHARS,
        "detail_retrieval_tool": "runtime_file_refs",
        "documents": docs,
    }
    json_path = output_dir / "startup_repo_docs_map.json"
    md_path = output_dir / "startup_repo_docs_map.md"
    write_json(json_path, data)
    lines = [
        "# Heap Startup Repo Docs Map",
        "",
        f"- Document count: `{len(docs)}`",
        f"- Preview document limit: `{STARTUP_DOCS_MAP_PREVIEW_LIMIT}`",
        f"- Stored preview chars: `{STARTUP_DOCS_MAP_PREVIEW_CHARS}`",
        "- Detail retrieval tool: `runtime_file_refs`",
        "- Live artifact policy: `all_context_paths_indexed; bounded previews only`",
        "",
        "## Indexed document refs",
        "",
    ]
    for item in docs[:STARTUP_DOCS_MAP_MARKDOWN_ROW_LIMIT]:
        lines.append(
            f"- `{item['path']}` size=`{item['size_bytes']}` "
            f"preview=`{item['preview_chars']}`"
        )
    if len(docs) > STARTUP_DOCS_MAP_MARKDOWN_ROW_LIMIT:
        remaining = len(docs) - STARTUP_DOCS_MAP_MARKDOWN_ROW_LIMIT
        lines.append(f"- ... `{remaining}` additional refs in `startup_repo_docs_map.json`")
    lines.extend(["", "## Bounded preview samples", ""])
    for item in [doc for doc in docs if doc.get("preview")][
        :STARTUP_DOCS_MAP_MARKDOWN_PREVIEW_BLOCKS
    ]:
        lines.extend(
            [
                f"### `{item['path']}`",
                "",
                f"- Size bytes: `{item['size_bytes']}`",
                "",
                "```text",
                item["preview"],
                "```",
                "",
            ]
        )
    write_markdown(md_path, "\n".join(lines) + "\n")
    return {
        "repo_docs_map_json": repo_rel(repo_root, json_path),
        "repo_docs_map_markdown": repo_rel(repo_root, md_path),
    }


def collect_semantic_code_chunks(
    repo_root: Path,
    output_dir: Path,
    request: str,
    limit: int = 48,
    preview_chars: int = 1800,
) -> dict[str, str]:
    keywords = [
        part.lower()
        for part in request.replace("_", " ").replace("-", " ").split()
        if len(part) >= 4
    ]
    candidates = repo_scan_semantic_candidates(repo_root, max_files=max(1000, limit * 80))
    ranked = sorted(
        ((_semantic_score(repo_root, path, keywords), path) for path in candidates),
        key=lambda item: (-item[0], repo_rel(repo_root, item[1])),
    )
    chunks = []
    stored_preview_chars = max(1, min(preview_chars, STARTUP_SEMANTIC_PREVIEW_CHARS))
    for index, (score, path) in enumerate(ranked[:limit]):
        rel = repo_rel(repo_root, path)
        preview_included = index < STARTUP_SEMANTIC_PREVIEW_CHUNK_LIMIT
        text = read_text(path, max_chars=stored_preview_chars) if preview_included else ""
        chunks.append(
            {
                "path": rel,
                "score": score,
                "size_bytes": path.stat().st_size if path.exists() else 0,
                "preview": text,
                "preview_included": preview_included,
                "preview_chars": len(text),
                "sha256": sha256_text(text) if text else "",
            }
        )
    data = {
        "schema_version": 1,
        "kind": "heap_startup_semantic_code_chunks",
        "passed": True,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "chunk_count": len(chunks),
        "selection_policy": "deterministic_path_keyword_ranker",
        "live_artifact_policy": "all_selected_paths_indexed; bounded previews only",
        "requested_preview_chars": preview_chars,
        "stored_preview_chars": stored_preview_chars,
        "preview_chunk_limit": STARTUP_SEMANTIC_PREVIEW_CHUNK_LIMIT,
        "detail_retrieval_tool": "select_semantic_code_chunks",
        "chunks": chunks,
    }
    json_path = output_dir / "startup_semantic_code_chunks.json"
    md_path = output_dir / "startup_semantic_code_chunks.md"
    write_json(json_path, data)
    lines = [
        "# Heap Startup Semantic Code Chunks",
        "",
        f"- Chunk count: `{len(chunks)}`",
        f"- Preview chunk limit: `{STARTUP_SEMANTIC_PREVIEW_CHUNK_LIMIT}`",
        f"- Stored preview chars: `{stored_preview_chars}`",
        "- Detail retrieval tool: `select_semantic_code_chunks`",
        "- Live artifact policy: `all_selected_paths_indexed; bounded previews only`",
        "",
        "## Indexed chunk refs",
        "",
    ]
    for item in chunks[:STARTUP_SEMANTIC_MARKDOWN_ROW_LIMIT]:
        lines.append(
            f"- `{item['path']}` score=`{item['score']}` size=`{item['size_bytes']}` "
            f"preview=`{item['preview_chars']}`"
        )
    if len(chunks) > STARTUP_SEMANTIC_MARKDOWN_ROW_LIMIT:
        remaining = len(chunks) - STARTUP_SEMANTIC_MARKDOWN_ROW_LIMIT
        lines.append(f"- ... `{remaining}` additional refs in `startup_semantic_code_chunks.json`")
    lines.extend(["", "## Bounded preview samples", ""])
    for item in [chunk for chunk in chunks if chunk.get("preview")][
        :STARTUP_SEMANTIC_MARKDOWN_PREVIEW_BLOCKS
    ]:
        lines.extend(
            [
                f"## `{item['path']}`",
                "",
                f"- Score: `{item['score']}`",
                f"- Size bytes: `{item['size_bytes']}`",
                "",
                "```text",
                item["preview"],
                "```",
                "",
            ]
        )
    write_markdown(md_path, "\n".join(lines))
    return {
        "semantic_code_chunks_json": repo_rel(repo_root, json_path),
        "semantic_code_chunks_markdown": repo_rel(repo_root, md_path),
    }


def write_semantic_evidence(
    commands: list[dict[str, Any]], repo_root: Path, output_dir: Path
) -> dict[str, str]:
    evidence_items = [
        {
            "name": command.get("name"),
            "requirement": command.get("requirement"),
            "passed": command.get("passed"),
            "effective_passed": command.get("effective_passed"),
            "degraded": command.get("degraded"),
            "hard_failed": command.get("hard_failed"),
            "useful_artifact_paths": command.get("useful_artifact_paths", []),
        }
        for command in commands
    ]
    data = {
        "schema_version": 1,
        "kind": "heap_startup_semantic_evidence_chunks",
        "passed": all(
            bool(item.get("effective_passed")) for item in commands if item.get("required")
        ),
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "evidence_count": len(evidence_items),
        "evidence": evidence_items,
    }
    json_path = output_dir / "startup_semantic_evidence_chunks.json"
    md_path = output_dir / "startup_semantic_evidence_chunks.md"
    write_json(json_path, data)
    lines = ["# Heap Startup Semantic Evidence Chunks", ""]
    for item in evidence_items:
        lines.append(
            f"- `{item['requirement']}` name=`{item['name']}` passed=`{item['passed']}` "
            f"effective=`{item['effective_passed']}` degraded=`{item['degraded']}`"
        )
    write_markdown(md_path, "\n".join(lines) + "\n")
    return {
        "semantic_evidence_chunks_json": repo_rel(repo_root, json_path),
        "semantic_evidence_chunks_markdown": repo_rel(repo_root, md_path),
    }


def _semantic_score(repo_root: Path, path: Path, keywords: list[str]) -> int:
    rel_lower = repo_rel(repo_root, path).lower()
    score = sum(3 for key in keywords if key in rel_lower)
    if any(
        token in rel_lower
        for token in ("heap", "context", "memory", "provider", "gpu", "npu", "composer")
    ):
        score += 8
    normalized_rel = rel_lower.replace("\\", "/")
    high_value_paths = {
        "tools/ai/heap_context_closure/cli.py",
        "tools/ai/heap_context_memory_reload/cli.py",
        "tools/ai/heap_final_proposals/cli.py",
        "tools/ai/heap_runtime/completeness_gate/cli.py",
        "tools/ai/agent_context/ai_context_pack/cli.py",
        "tools/ai/agent_memory/sqlite_cli.py",
    }
    if normalized_rel in high_value_paths:
        score += 20
    return score
