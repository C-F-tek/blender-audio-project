"""Context source loaders for NPU knowledge broker packets."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .candidates import add_candidate
from .common import normalize_path, read_json, repo_relative, resolve_repo_path

def add_selected_chunks(
    candidates: dict[str, dict[str, Any]],
    repo_root: Path,
    selected_chunks: str,
    objective_terms: set[str],
) -> list[str]:
    selected_path = resolve_repo_path(repo_root, selected_chunks)
    data = read_json(selected_path)
    source_paths: list[str] = []
    if not data:
        return source_paths
    add_candidate(
        candidates,
        repo_relative(selected_path, repo_root),
        "selected_chunks_bundle",
        objective_terms,
        "selected chunks bundle",
        20,
    )
    markdown_path = selected_path.with_suffix(".md")
    if markdown_path.exists():
        add_candidate(
            candidates,
            repo_relative(markdown_path, repo_root),
            "selected_chunks_markdown",
            objective_terms,
            "selected chunks markdown summary",
            18,
        )
    chunks = data.get("selected_chunks")
    if isinstance(chunks, list):
        for chunk in chunks:
            if not isinstance(chunk, dict):
                continue
            path = normalize_path(chunk.get("path"))
            if not path:
                continue
            source_paths.append(path)
            add_candidate(
                candidates,
                path,
                "selected_chunk_source",
                objective_terms,
                "source file referenced by selected chunk",
                int(chunk.get("score") or 0),
            )
    return source_paths


def add_adapter_manifest(
    candidates: dict[str, dict[str, Any]], repo_root: Path, manifest: str, objective_terms: set[str]
) -> list[str]:
    manifest_path = resolve_repo_path(repo_root, manifest)
    data = read_json(manifest_path)
    refs: list[str] = []
    if not data:
        return refs
    add_candidate(
        candidates,
        repo_relative(manifest_path, repo_root),
        "adapter_manifest",
        objective_terms,
        "local AI adapter manifest",
        18,
    )
    for key in ("context_files",):
        values = data.get(key)
        if isinstance(values, list):
            for item in values:
                path = normalize_path(item)
                refs.append(path)
                add_candidate(
                    candidates,
                    path,
                    "adapter_manifest_context",
                    objective_terms,
                    "context file recorded by adapter manifest",
                    10,
                )
    enrichment_outputs = data.get("enrichment_outputs")
    if isinstance(enrichment_outputs, dict):
        for key, item in enrichment_outputs.items():
            path = normalize_path(item)
            if path:
                refs.append(path)
                add_candidate(
                    candidates,
                    path,
                    f"adapter_manifest_output:{key}",
                    objective_terms,
                    "enrichment output recorded by adapter manifest",
                    8,
                )
    return refs


def add_context_pack(
    candidates: dict[str, dict[str, Any]],
    repo_root: Path,
    context_pack: str,
    objective_terms: set[str],
) -> list[str]:
    pack_path = resolve_repo_path(repo_root, context_pack)
    data = read_json(pack_path)
    refs: list[str] = []
    if not data:
        return refs
    add_candidate(
        candidates,
        repo_relative(pack_path, repo_root),
        "context_pack",
        objective_terms,
        "bounded context pack",
        16,
    )
    md_path = pack_path.with_suffix(".md")
    if md_path.exists():
        add_candidate(
            candidates,
            repo_relative(md_path, repo_root),
            "context_pack_markdown",
            objective_terms,
            "bounded context pack markdown",
            14,
        )
    for key in ("included_files", "files", "context_files"):
        values = data.get(key)
        if isinstance(values, list):
            for item in values:
                if isinstance(item, dict):
                    path = normalize_path(item.get("path"))
                else:
                    path = normalize_path(item)
                if path:
                    refs.append(path)
                    add_candidate(
                        candidates,
                        path,
                        f"context_pack:{key}",
                        objective_terms,
                        "file referenced by context pack",
                        7,
                    )
    return refs
