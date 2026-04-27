# Project Code Chunk 122/212

- File: `Tools/npu/build_npu_code_context.py`
- Part: `2`
- Lines: `307-389`

## Symbol Map
- Imports: `from __future__ import annotations`, `from pathlib import Path`, `ast`, `hashlib`, `json`, `re`, `from datetime import datetime`
- Functions: `sha256_text(text)` line 56; `rel_to_root(path)` line 60; `slugify(value, max_len)` line 64; `is_usable_text_file(path)` line 69; `collect_files()` line 75; `target_name(target)` line 99; `extract_symbols(source)` line 107; `file_record(path, source)` line 169; `format_symbol_summary(record)` line 184; `numbered_lines(lines, start_line)` line 225; `split_source(source, max_chars)` line 229; `write_context_chunks(files, sources)` line 255; `write_index(files, chunks, created_at)` line 325; `main()` line 348
- Assignments: `ROOT`, `SCRIPT_DIR`, `OUT_DIR`, `OUT_MD`, `OUT_INDEX_MD`, `OUT_JSON`, `CHUNK_DIR`, `MAX_CHUNK_CHARS`, `PRIORITY_FILES`, `DISCOVERY_GLOBS`, `EXCLUDE_PARTS`, `TEXT_SUFFIXES`

## Content
```py
00307:         chunk_path.write_text(chunk_text, encoding="utf-8")
00308: 
00309:         chunks.append(
00310:             {
00311:                 "index": index,
00312:                 "file": rel_file,
00313:                 "path": rel_to_root(chunk_path),
00314:                 "part": item["part"],
00315:                 "start_line": item["start_line"],
00316:                 "end_line": item["end_line"],
00317:                 "chars": len(chunk_text),
00318:                 "sha256": sha256_text(chunk_text),
00319:             }
00320:         )
00321: 
00322:     return chunks
00323: 
00324: 
00325: def write_index(files: list[dict], chunks: list[dict], created_at: str) -> None:
00326:     md: list[str] = []
00327:     md.append("# NPU Code Index\n\n")
00328:     md.append(f"Generated: `{created_at}`\n\n")
00329:     md.append("Purpose: long-context index for the local NPU musical/technical agent.\n")
00330:     md.append("Use `npu_code_chunks/chunk_*.md` for full file context.\n\n")
00331: 
00332:     md.append("## Files\n")
00333:     for record in files:
00334:         md.append(
00335:             f"- `{record['file']}`: {record['lines']} lines, {record['chars']} chars, sha256 `{record['sha256']}`\n"
00336:         )
00337: 
00338:     md.append("\n## Chunks\n")
00339:     for chunk in chunks:
00340:         md.append(
00341:             f"- `{chunk['path']}` -> `{chunk['file']}` lines {chunk['start_line']}-{chunk['end_line']}\n"
00342:         )
00343: 
00344:     OUT_INDEX_MD.write_text("".join(md), encoding="utf-8")
00345:     OUT_MD.write_text("".join(md), encoding="utf-8")
00346: 
00347: 
00348: def main() -> None:
00349:     OUT_DIR.mkdir(parents=True, exist_ok=True)
00350: 
00351:     created_at = datetime.now().isoformat(timespec="seconds")
00352:     paths = collect_files()
00353:     sources: dict[str, str] = {}
00354:     files: list[dict] = []
00355: 
00356:     for path in paths:
00357:         source = path.read_text(encoding="utf-8", errors="replace")
00358:         record = file_record(path, source)
00359:         sources[record["file"]] = source
00360:         files.append(record)
00361: 
00362:     chunks = write_context_chunks(files, sources)
00363:     write_index(files, chunks, created_at)
00364: 
00365:     manifest = {
00366:         "created_at": created_at,
00367:         "root": str(ROOT),
00368:         "script_dir": str(SCRIPT_DIR),
00369:         "long_context": {
00370:             "mode": "file_line_chunks",
00371:             "chunk_dir": rel_to_root(CHUNK_DIR),
00372:             "max_chunk_chars": MAX_CHUNK_CHARS,
00373:             "chunk_count": len(chunks),
00374:             "index": rel_to_root(OUT_INDEX_MD),
00375:         },
00376:         "files": files,
00377:         "chunks": chunks,
00378:     }
00379: 
00380:     OUT_JSON.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
00381: 
00382:     print(f"[OK] Wrote: {OUT_MD}")
00383:     print(f"[OK] Wrote: {OUT_INDEX_MD}")
00384:     print(f"[OK] Wrote: {OUT_JSON}")
00385:     print(f"[OK] Wrote chunks: {CHUNK_DIR} ({len(chunks)} files)")
00386: 
00387: 
00388: if __name__ == "__main__":
00389:     main()
```
