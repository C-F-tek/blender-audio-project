#!/usr/bin/env python3
"""Temporary helper to split long repository files for API-only review.

This script belongs to the temporary PR109 refactor workspace branch only. It is
not part of the production AI lane and should not be mirrored into the official
PR unless intentionally promoted as a real tool.

It does not execute providers, run Blender, apply patches or modify source
files. It only reads one text file and writes bounded Markdown chunks under the
workspace directory.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Any

DEFAULT_OUTPUT_DIR = "docs/LOCAL_VALIDATION_EVIDENCE/tmp_refactor_pr109/chunks"
DEFAULT_MAX_CHARS = 12000


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()


def repo_rel(repo_root: Path, path: Path) -> str:
    try:
        return path.resolve(strict=False).relative_to(repo_root.resolve(strict=False)).as_posix()
    except ValueError:
        return path.as_posix()


def line_count(text: str) -> int:
    if not text:
        return 0
    return text.count("\n") + (0 if text.endswith("\n") else 1)


def split_text_by_lines(text: str, max_chars: int) -> list[str]:
    chunks: list[str] = []
    current: list[str] = []
    current_chars = 0
    for line in text.splitlines(keepends=True):
        if current and current_chars + len(line) > max_chars:
            chunks.append("".join(current))
            current = []
            current_chars = 0
        current.append(line)
        current_chars += len(line)
    if current:
        chunks.append("".join(current))
    return chunks


def chunk_filename(index: int, total: int, source_path: Path) -> str:
    stem = source_path.name.replace(".", "_").replace("/", "_").replace("\\", "_")
    width = max(3, len(str(total)))
    return f"{stem}.chunk_{index:0{width}d}_of_{total:0{width}d}.md"


def write_chunks(repo_root: Path, source: Path, output_dir: Path, max_chars: int) -> dict[str, Any]:
    text = source.read_text(encoding="utf-8-sig", errors="replace")
    chunks = split_text_by_lines(text, max_chars)
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest: dict[str, Any] = {
        "schema_version": 1,
        "kind": "temporary_api_review_file_chunks",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "source_file": repo_rel(repo_root, source),
        "source_sha256": sha256_text(text),
        "source_line_count": line_count(text),
        "source_chars": len(text),
        "max_chunk_chars": max_chars,
        "chunk_count": len(chunks),
        "chunks": [],
        "guardrails": {
            "temporary_workspace_only": True,
            "provider_execution_performed": False,
            "blender_runtime_execution_performed": False,
            "patch_application_performed": False,
            "source_writes_performed": False,
        },
    }
    for index, chunk in enumerate(chunks, start=1):
        name = chunk_filename(index, len(chunks), source)
        path = output_dir / name
        path.write_text(
            "\n".join(
                [
                    f"# Chunk {index} of {len(chunks)} — `{repo_rel(repo_root, source)}`",
                    "",
                    f"- Source SHA-256: `{manifest['source_sha256']}`",
                    f"- Chunk SHA-256: `{sha256_text(chunk)}`",
                    f"- Chunk chars: `{len(chunk)}`",
                    f"- Chunk lines: `{line_count(chunk)}`",
                    "",
                    "```python",
                    chunk.rstrip("\n"),
                    "```",
                    "",
                ]
            ),
            encoding="utf-8",
        )
        manifest["chunks"].append(
            {
                "index": index,
                "path": repo_rel(repo_root, path),
                "sha256": sha256_text(chunk),
                "chars": len(chunk),
                "line_count": line_count(chunk),
            }
        )
    manifest_path = output_dir / f"{source.name.replace('.', '_')}.chunks_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    manifest["manifest_path"] = repo_rel(repo_root, manifest_path)
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--source", required=True)
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--max-chars", type=int, default=DEFAULT_MAX_CHARS)
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    source = Path(args.source)
    source = source.resolve() if source.is_absolute() else (repo_root / source).resolve()
    output_dir = Path(args.output_dir)
    output_dir = output_dir.resolve() if output_dir.is_absolute() else (repo_root / output_dir).resolve()
    manifest = write_chunks(repo_root, source, output_dir, args.max_chars)
    print(json.dumps(manifest, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
