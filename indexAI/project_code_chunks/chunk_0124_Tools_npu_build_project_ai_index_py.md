# Project Code Chunk 124/212

- File: `Tools/npu/build_project_ai_index.py`
- Part: `2`
- Lines: `301-419`

## Symbol Map
- Imports: `from __future__ import annotations`, `from datetime import datetime`, `from pathlib import Path`, `argparse`, `ast`, `hashlib`, `json`, `re`
- Functions: `sha256_text(text)` line 74; `sha256_file(path)` line 78; `rel_to_root(path)` line 86; `slugify(value, max_len)` line 90; `should_exclude(path)` line 95; `collect_project_files()` line 116; `target_name(target)` line 131; `extract_symbols(source)` line 139; `file_record(path)` line 182; `format_symbol_summary(record)` line 196; `numbered_lines(lines, start_line)` line 223; `split_source(source, max_chars)` line 227; `source_fingerprint(records)` line 249; `existing_cache_valid(fingerprint)` line 258; `write_readme()` line 272; `write_chunks(records, max_chunk_chars)` line 293; `write_index(records, chunks, created_at, fingerprint)` line 347; `build_project_ai_index(force, max_chunk_chars)` line 367; `main()` line 410
- Assignments: `ROOT`, `INDEX_DIR`, `PROJECT_INDEX_MD`, `PROJECT_MANIFEST_JSON`, `PROJECT_CHUNK_DIR`, `PATCH_LIBRARY_DIR`, `README_MD`, `DEFAULT_MAX_CHUNK_CHARS`, `TEXT_SUFFIXES`, `EXCLUDE_DIRS`, `EXCLUDE_PARTS`, `EXCLUDE_FILE_PREFIXES`, `MEDIA_SUFFIXES`

## Content
```py
00301:         path = ROOT / record["file"]
00302:         source = path.read_text(encoding="utf-8", errors="replace")
00303:         for part, (start_line, end_line, lines) in enumerate(split_source(source, max_chunk_chars), 1):
00304:             pending.append(
00305:                 {
00306:                     "file": record["file"],
00307:                     "suffix": record["suffix"],
00308:                     "part": part,
00309:                     "start_line": start_line,
00310:                     "end_line": end_line,
00311:                     "symbols": format_symbol_summary(record),
00312:                     "text": numbered_lines(lines, start_line),
00313:                 }
00314:             )
00315: 
00316:     total = len(pending)
00317:     for index, item in enumerate(pending, 1):
00318:         chunk_name = f"chunk_{index:04d}_{slugify(item['file'])}.md"
00319:         chunk_path = PROJECT_CHUNK_DIR / chunk_name
00320:         fence = item["suffix"].lstrip(".") or "text"
00321:         body = [
00322:             f"# Project Code Chunk {index}/{total}\n\n",
00323:             f"- File: `{item['file']}`\n",
00324:             f"- Part: `{item['part']}`\n",
00325:             f"- Lines: `{item['start_line']}-{item['end_line']}`\n\n",
00326:         ]
00327:         if item["symbols"]:
00328:             body.extend(["## Symbol Map\n", item["symbols"], "\n\n"])
00329:         body.extend(["## Content\n", f"```{fence}\n", item["text"], "\n```\n"])
00330:         chunk_text = "".join(body)
00331:         chunk_path.write_text(chunk_text, encoding="utf-8")
00332:         chunks.append(
00333:             {
00334:                 "index": index,
00335:                 "file": item["file"],
00336:                 "path": rel_to_root(chunk_path),
00337:                 "part": item["part"],
00338:                 "start_line": item["start_line"],
00339:                 "end_line": item["end_line"],
00340:                 "chars": len(chunk_text),
00341:                 "sha256": sha256_text(chunk_text),
00342:             }
00343:         )
00344:     return chunks
00345: 
00346: 
00347: def write_index(records: list[dict], chunks: list[dict], created_at: str, fingerprint: str) -> None:
00348:     lines: list[str] = []
00349:     lines.append("# Spaziotempo Primary Project Code Index\n\n")
00350:     lines.append(f"Generated: `{created_at}`\n\n")
00351:     lines.append(f"Source fingerprint: `{fingerprint}`\n\n")
00352:     lines.append("Priority: this is the primary library for project structure. AI patches must respect these files before Blender manuals.\n\n")
00353:     lines.append("## Rules For AI Implementers\n")
00354:     lines.append("- Prefer existing files, functions and panel patterns.\n")
00355:     lines.append("- Do not generate monolithic replacement scripts when a targeted patch is possible.\n")
00356:     lines.append("- Full frame-by-frame keyframe JSON files are data inputs and must not be compacted or rewritten.\n")
00357:     lines.append("- `indexAI` is generated context and must not be re-indexed as source.\n\n")
00358:     lines.append("## Files\n")
00359:     for record in records:
00360:         lines.append(f"- `{record['file']}`: {record['lines']} lines, {record['chars']} chars, sha256 `{record['sha256']}`\n")
00361:     lines.append("\n## Chunks\n")
00362:     for chunk in chunks:
00363:         lines.append(f"- `{chunk['path']}` -> `{chunk['file']}` lines {chunk['start_line']}-{chunk['end_line']}\n")
00364:     PROJECT_INDEX_MD.write_text("".join(lines), encoding="utf-8")
00365: 
00366: 
00367: def build_project_ai_index(force: bool = False, max_chunk_chars: int = DEFAULT_MAX_CHUNK_CHARS) -> dict:
00368:     INDEX_DIR.mkdir(parents=True, exist_ok=True)
00369:     PATCH_LIBRARY_DIR.mkdir(parents=True, exist_ok=True)
00370:     write_readme()
00371: 
00372:     paths = collect_project_files()
00373:     records = [file_record(path) for path in paths]
00374:     fingerprint = source_fingerprint(records)
00375:     created_at = datetime.now().isoformat(timespec="seconds")
00376: 
00377:     if not force and existing_cache_valid(fingerprint):
00378:         manifest = json.loads(PROJECT_MANIFEST_JSON.read_text(encoding="utf-8"))
00379:         manifest["cache_hit"] = True
00380:         print(f"[OK] Reusing project AI index: {PROJECT_INDEX_MD}")
00381:         return manifest
00382: 
00383:     chunks = write_chunks(records, max_chunk_chars=max_chunk_chars)
00384:     write_index(records, chunks, created_at, fingerprint)
00385:     manifest = {
00386:         "created_at": created_at,
00387:         "root": str(ROOT),
00388:         "index_dir": str(INDEX_DIR),
00389:         "primary_library": True,
00390:         "source_fingerprint": fingerprint,
00391:         "excluded_dirs": sorted(EXCLUDE_DIRS),
00392:         "excluded_parts": sorted(EXCLUDE_PARTS),
00393:         "excluded_file_prefixes": sorted(EXCLUDE_FILE_PREFIXES),
00394:         "file_count": len(records),
00395:         "chunk_count": len(chunks),
00396:         "index_md": str(PROJECT_INDEX_MD),
00397:         "chunk_dir": str(PROJECT_CHUNK_DIR),
00398:         "patch_library_dir": str(PATCH_LIBRARY_DIR),
00399:         "files": records,
00400:         "chunks": chunks,
00401:         "cache_hit": False,
00402:     }
00403:     PROJECT_MANIFEST_JSON.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
00404:     print(f"[OK] Wrote: {PROJECT_INDEX_MD}")
00405:     print(f"[OK] Wrote: {PROJECT_MANIFEST_JSON}")
00406:     print(f"[OK] Wrote chunks: {PROJECT_CHUNK_DIR} ({len(chunks)} files)")
00407:     return manifest
00408: 
00409: 
00410: def main() -> None:
00411:     parser = argparse.ArgumentParser(description="Build primary project code index for AI patch planning.")
00412:     parser.add_argument("--force", action="store_true")
00413:     parser.add_argument("--max-chunk-chars", type=int, default=DEFAULT_MAX_CHUNK_CHARS)
00414:     args = parser.parse_args()
00415:     build_project_ai_index(force=args.force, max_chunk_chars=args.max_chunk_chars)
00416: 
00417: 
00418: if __name__ == "__main__":
00419:     main()
```
