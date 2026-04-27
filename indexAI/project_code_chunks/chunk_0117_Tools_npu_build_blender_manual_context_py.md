# Project Code Chunk 117/212

- File: `Tools/npu/build_blender_manual_context.py`
- Part: `2`
- Lines: `302-326`

## Symbol Map
- Imports: `from __future__ import annotations`, `from pathlib import Path`, `from html.parser import HTMLParser`, `argparse`, `hashlib`, `json`, `re`, `from datetime import datetime`
- Classes: `TextExtractor` line 62 methods: __init__, handle_starttag, handle_endtag, handle_data, text
- Functions: `sha256_text(text)` line 95; `rel(path)` line 99; `slug(value)` line 106; `extract_text(path)` line 110; `score_text(path, text)` line 119; `score_path(path)` line 124; `split_text(text, max_chars)` line 144; `ensure_manual_root()` line 161; `source_group(path)` line 167; `iter_manual_files(manual_root)` line 175; `build_manual_context(limit_files, manual_root)` line 195; `main()` line 296
- Assignments: `ROOT`, `MANUAL_ROOT`, `LEGACY_MANUAL_DIR`, `MANUAL_README`, `OUT_DIR`, `CHUNK_DIR`, `OUT_INDEX`, `OUT_MANIFEST`, `MAX_CHARS`, `TEXT_EXTENSIONS`, `HTML_EXTENSIONS`, `KEYWORDS`, `README_TEXT`

## Content
```py
00302:     parser.add_argument(
00303:         "--ensure-only",
00304:         action="store_true",
00305:         help="Create the local manual folder and README without scanning/indexing manuals.",
00306:     )
00307:     args = parser.parse_args()
00308: 
00309:     if args.ensure_only:
00310:         MANUAL_ROOT = Path(args.manual_root)
00311:         MANUAL_README = MANUAL_ROOT / "README_MANUALI.md"
00312:         ensure_manual_root()
00313:         print(f"[OK] Manual root ready: {MANUAL_ROOT}")
00314:         print(f"[OK] Manual README: {MANUAL_README}")
00315:         return
00316: 
00317:     manifest = build_manual_context(limit_files=args.limit_files, manual_root=args.manual_root)
00318:     print(f"[OK] Manual root: {manifest['manual_root']}")
00319:     print(f"[OK] Manual README: {manifest['manual_readme']}")
00320:     print(f"[OK] Wrote: {OUT_INDEX}")
00321:     print(f"[OK] Wrote: {OUT_MANIFEST}")
00322:     print(f"[OK] Wrote chunks: {CHUNK_DIR} ({manifest['chunk_count']} files)")
00323: 
00324: 
00325: if __name__ == "__main__":
00326:     main()
```
