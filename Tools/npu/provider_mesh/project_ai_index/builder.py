"""Project AI index builder."""

from __future__ import annotations

import json
from datetime import datetime

from .chunks import write_chunks, write_index, write_readme
from .config import (
    DEFAULT_MAX_CHUNK_CHARS,
    EXCLUDE_DIRS,
    EXCLUDE_FILE_PREFIXES,
    EXCLUDE_PARTS,
    INDEX_DIR,
    PATCH_LIBRARY_DIR,
    PROJECT_CHUNK_DIR,
    PROJECT_INDEX_MD,
    PROJECT_MANIFEST_JSON,
    ROOT,
)
from .paths import collect_project_files
from .records import existing_cache_valid, file_record, source_fingerprint

def build_project_ai_index(
    force: bool = False, max_chunk_chars: int = DEFAULT_MAX_CHUNK_CHARS
) -> dict:
    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    PATCH_LIBRARY_DIR.mkdir(parents=True, exist_ok=True)
    write_readme()

    paths = collect_project_files()
    records = [file_record(path) for path in paths]
    fingerprint = source_fingerprint(records)
    created_at = datetime.now().isoformat(timespec="seconds")

    if not force and existing_cache_valid(fingerprint):
        manifest = json.loads(PROJECT_MANIFEST_JSON.read_text(encoding="utf-8"))
        manifest["cache_hit"] = True
        print(f"[OK] Reusing project AI index: {PROJECT_INDEX_MD}")
        return manifest

    chunks = write_chunks(records, max_chunk_chars=max_chunk_chars)
    write_index(records, chunks, created_at, fingerprint)
    manifest = {
        "created_at": created_at,
        "root": str(ROOT),
        "index_dir": str(INDEX_DIR),
        "primary_library": True,
        "source_fingerprint": fingerprint,
        "excluded_dirs": sorted(EXCLUDE_DIRS),
        "excluded_parts": sorted(EXCLUDE_PARTS),
        "excluded_file_prefixes": sorted(EXCLUDE_FILE_PREFIXES),
        "file_count": len(records),
        "chunk_count": len(chunks),
        "index_md": str(PROJECT_INDEX_MD),
        "chunk_dir": str(PROJECT_CHUNK_DIR),
        "patch_library_dir": str(PATCH_LIBRARY_DIR),
        "files": records,
        "chunks": chunks,
        "cache_hit": False,
    }
    PROJECT_MANIFEST_JSON.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"[OK] Wrote: {PROJECT_INDEX_MD}")
    print(f"[OK] Wrote: {PROJECT_MANIFEST_JSON}")
    print(f"[OK] Wrote chunks: {PROJECT_CHUNK_DIR} ({len(chunks)} files)")
    return manifest
