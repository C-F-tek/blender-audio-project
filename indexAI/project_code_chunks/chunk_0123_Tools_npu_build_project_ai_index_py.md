# Project Code Chunk 123/212

- File: `Tools/npu/build_project_ai_index.py`
- Part: `1`
- Lines: `1-300`

## Symbol Map
- Imports: `from __future__ import annotations`, `from datetime import datetime`, `from pathlib import Path`, `argparse`, `ast`, `hashlib`, `json`, `re`
- Functions: `sha256_text(text)` line 74; `sha256_file(path)` line 78; `rel_to_root(path)` line 86; `slugify(value, max_len)` line 90; `should_exclude(path)` line 95; `collect_project_files()` line 116; `target_name(target)` line 131; `extract_symbols(source)` line 139; `file_record(path)` line 182; `format_symbol_summary(record)` line 196; `numbered_lines(lines, start_line)` line 223; `split_source(source, max_chars)` line 227; `source_fingerprint(records)` line 249; `existing_cache_valid(fingerprint)` line 258; `write_readme()` line 272; `write_chunks(records, max_chunk_chars)` line 293; `write_index(records, chunks, created_at, fingerprint)` line 347; `build_project_ai_index(force, max_chunk_chars)` line 367; `main()` line 410
- Assignments: `ROOT`, `INDEX_DIR`, `PROJECT_INDEX_MD`, `PROJECT_MANIFEST_JSON`, `PROJECT_CHUNK_DIR`, `PATCH_LIBRARY_DIR`, `README_MD`, `DEFAULT_MAX_CHUNK_CHARS`, `TEXT_SUFFIXES`, `EXCLUDE_DIRS`, `EXCLUDE_PARTS`, `EXCLUDE_FILE_PREFIXES`, `MEDIA_SUFFIXES`

## Content
```py
00001: from __future__ import annotations
00002: 
00003: from datetime import datetime
00004: from pathlib import Path
00005: import argparse
00006: import ast
00007: import hashlib
00008: import json
00009: import re
00010: 
00011: 
00012: ROOT = Path(__file__).resolve().parents[2]
00013: INDEX_DIR = ROOT / "indexAI"
00014: PROJECT_INDEX_MD = INDEX_DIR / "project_code_index.md"
00015: PROJECT_MANIFEST_JSON = INDEX_DIR / "project_code_manifest.json"
00016: PROJECT_CHUNK_DIR = INDEX_DIR / "project_code_chunks"
00017: PATCH_LIBRARY_DIR = INDEX_DIR / "patch_library"
00018: README_MD = INDEX_DIR / "README.md"
00019: 
00020: DEFAULT_MAX_CHUNK_CHARS = 12000
00021: TEXT_SUFFIXES = {".py", ".ps1", ".md", ".json", ".txt", ".cfg", ".ini", ".toml", ".yaml", ".yml"}
00022: EXCLUDE_DIRS = {
00023:     ".git",
00024:     ".mypy_cache",
00025:     ".pytest_cache",
00026:     ".ruff_cache",
00027:     ".venv",
00028:     "__pycache__",
00029:     "cache",
00030:     "indexAI",
00031:     "node_modules",
00032:     "output",
00033:     "renders",
00034:     "venv",
00035:     "venvs",
00036:     "old script legacy",
00037: }
00038: EXCLUDE_PARTS = {
00039:     ".npucache",
00040:     "npu_blender_manual_chunks",
00041:     "npu_code_chunks",
00042:     "npu_music_chunks",
00043: }
00044: EXCLUDE_FILE_PREFIXES = {
00045:     ".aider",
00046:     "npu_code_context",
00047:     "npu_code_index",
00048:     "npu_context_for_aider",
00049:     "npu_music_context",
00050:     "npu_music_context_for_aider",
00051:     "npu_dual_ai_chunk_notes",
00052:     "npu_dual_ai_technical_notes",
00053:     "ollama_music_insights",
00054:     "dual_ai_blender_agent_brief",
00055:     "generated_implementation_notes",
00056: }
00057: MEDIA_SUFFIXES = {
00058:     ".wav",
00059:     ".mp3",
00060:     ".flac",
00061:     ".mp4",
00062:     ".mov",
00063:     ".avi",
00064:     ".mkv",
00065:     ".png",
00066:     ".jpg",
00067:     ".jpeg",
00068:     ".exr",
00069:     ".blend",
00070:     ".blend1",
00071: }
00072: 
00073: 
00074: def sha256_text(text: str) -> str:
00075:     return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()
00076: 
00077: 
00078: def sha256_file(path: Path) -> str:
00079:     digest = hashlib.sha256()
00080:     with path.open("rb") as handle:
00081:         for block in iter(lambda: handle.read(1024 * 1024), b""):
00082:             digest.update(block)
00083:     return digest.hexdigest()
00084: 
00085: 
00086: def rel_to_root(path: Path) -> str:
00087:     return str(path.resolve().relative_to(ROOT.resolve())).replace("\\", "/")
00088: 
00089: 
00090: def slugify(value: str, max_len: int = 80) -> str:
00091:     slug = re.sub(r"[^A-Za-z0-9]+", "_", value).strip("_")
00092:     return slug[:max_len] or "chunk"
00093: 
00094: 
00095: def should_exclude(path: Path) -> bool:
00096:     rel_parts = path.resolve().relative_to(ROOT.resolve()).parts
00097:     if any(part in EXCLUDE_DIRS or part in EXCLUDE_PARTS for part in rel_parts[:-1]):
00098:         return True
00099: 
00100:     suffix = path.suffix.lower()
00101:     if suffix in MEDIA_SUFFIXES or suffix not in TEXT_SUFFIXES:
00102:         return True
00103: 
00104:     stem = path.stem
00105:     if any(stem.startswith(prefix) for prefix in EXCLUDE_FILE_PREFIXES):
00106:         return True
00107: 
00108:     if path.name.endswith(".pyc") or path.name.endswith(".pyo"):
00109:         return True
00110:     if path.name.startswith("."):
00111:         return True
00112: 
00113:     return False
00114: 
00115: 
00116: def collect_project_files() -> list[Path]:
00117:     files: list[Path] = []
00118:     for path in ROOT.rglob("*"):
00119:         if not path.is_file():
00120:             continue
00121:         try:
00122:             path.resolve().relative_to(ROOT.resolve())
00123:         except ValueError:
00124:             continue
00125:         if should_exclude(path):
00126:             continue
00127:         files.append(path.resolve())
00128:     return sorted(files, key=lambda item: rel_to_root(item).lower())
00129: 
00130: 
00131: def target_name(target: ast.expr) -> str | None:
00132:     if isinstance(target, ast.Name):
00133:         return target.id
00134:     if isinstance(target, ast.Attribute):
00135:         return target.attr
00136:     return None
00137: 
00138: 
00139: def extract_symbols(source: str) -> dict:
00140:     symbols = {"imports": [], "functions": [], "classes": [], "assignments": []}
00141:     try:
00142:         tree = ast.parse(source)
00143:     except SyntaxError as exc:
00144:         symbols["syntax_error"] = str(exc)
00145:         return symbols
00146: 
00147:     for node in tree.body:
00148:         if isinstance(node, ast.Import):
00149:             symbols["imports"].extend(alias.name for alias in node.names)
00150:         elif isinstance(node, ast.ImportFrom):
00151:             module = node.module or ""
00152:             names = ", ".join(alias.name for alias in node.names)
00153:             symbols["imports"].append(f"from {module} import {names}")
00154:         elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
00155:             symbols["functions"].append(
00156:                 {
00157:                     "name": node.name,
00158:                     "line": node.lineno,
00159:                     "args": [arg.arg for arg in node.args.args],
00160:                     "async": isinstance(node, ast.AsyncFunctionDef),
00161:                 }
00162:             )
00163:         elif isinstance(node, ast.ClassDef):
00164:             methods = []
00165:             for child in node.body:
00166:                 if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
00167:                     methods.append({"name": child.name, "line": child.lineno})
00168:             symbols["classes"].append({"name": node.name, "line": node.lineno, "methods": methods})
00169:         elif isinstance(node, ast.Assign):
00170:             for target in node.targets:
00171:                 name = target_name(target)
00172:                 if name:
00173:                     symbols["assignments"].append(name)
00174:         elif isinstance(node, ast.AnnAssign):
00175:             name = target_name(node.target)
00176:             if name:
00177:                 symbols["assignments"].append(name)
00178: 
00179:     return symbols
00180: 
00181: 
00182: def file_record(path: Path) -> dict:
00183:     source = path.read_text(encoding="utf-8", errors="replace")
00184:     record = {
00185:         "file": rel_to_root(path),
00186:         "suffix": path.suffix.lower(),
00187:         "lines": source.count("\n") + 1 if source else 0,
00188:         "chars": len(source),
00189:         "sha256": sha256_text(source),
00190:     }
00191:     if path.suffix.lower() == ".py":
00192:         record["symbols"] = extract_symbols(source)
00193:     return record
00194: 
00195: 
00196: def format_symbol_summary(record: dict) -> str:
00197:     symbols = record.get("symbols")
00198:     if not symbols:
00199:         return ""
00200:     lines: list[str] = []
00201:     if symbols.get("syntax_error"):
00202:         lines.append(f"- Syntax error: `{symbols['syntax_error']}`")
00203:     if symbols.get("imports"):
00204:         lines.append("- Imports: " + ", ".join(f"`{item}`" for item in symbols["imports"][:24]))
00205:     if symbols.get("classes"):
00206:         bits = []
00207:         for item in symbols["classes"][:20]:
00208:             methods = ", ".join(method["name"] for method in item.get("methods", [])[:10])
00209:             bits.append(f"`{item['name']}` line {item['line']}" + (f" methods: {methods}" if methods else ""))
00210:         lines.append("- Classes: " + "; ".join(bits))
00211:     if symbols.get("functions"):
00212:         bits = []
00213:         for item in symbols["functions"][:44]:
00214:             args = ", ".join(item["args"])
00215:             prefix = "async " if item.get("async") else ""
00216:             bits.append(f"`{prefix}{item['name']}({args})` line {item['line']}")
00217:         lines.append("- Functions: " + "; ".join(bits))
00218:     if symbols.get("assignments"):
00219:         lines.append("- Assignments: " + ", ".join(f"`{name}`" for name in symbols["assignments"][:80]))
00220:     return "\n".join(lines)
00221: 
00222: 
00223: def numbered_lines(lines: list[str], start_line: int) -> str:
00224:     return "\n".join(f"{line_no:05d}: {line}" for line_no, line in enumerate(lines, start_line))
00225: 
00226: 
00227: def split_source(source: str, max_chars: int) -> list[tuple[int, int, list[str]]]:
00228:     lines = source.splitlines()
00229:     if not lines:
00230:         return [(1, 1, [])]
00231:     chunks: list[tuple[int, int, list[str]]] = []
00232:     current: list[str] = []
00233:     current_len = 0
00234:     start_line = 1
00235:     for line_no, line in enumerate(lines, 1):
00236:         cost = len(line) + 9
00237:         if current and current_len + cost > max_chars:
00238:             chunks.append((start_line, line_no - 1, current))
00239:             current = []
00240:             current_len = 0
00241:             start_line = line_no
00242:         current.append(line)
00243:         current_len += cost
00244:     if current:
00245:         chunks.append((start_line, start_line + len(current) - 1, current))
00246:     return chunks
00247: 
00248: 
00249: def source_fingerprint(records: list[dict]) -> str:
00250:     payload = json.dumps(
00251:         [{"file": item["file"], "sha256": item["sha256"]} for item in records],
00252:         ensure_ascii=False,
00253:         sort_keys=True,
00254:     )
00255:     return sha256_text(payload)
00256: 
00257: 
00258: def existing_cache_valid(fingerprint: str) -> bool:
00259:     if not PROJECT_MANIFEST_JSON.exists() or not PROJECT_INDEX_MD.exists() or not PROJECT_CHUNK_DIR.exists():
00260:         return False
00261:     try:
00262:         manifest = json.loads(PROJECT_MANIFEST_JSON.read_text(encoding="utf-8"))
00263:     except Exception:
00264:         return False
00265:     if manifest.get("source_fingerprint") != fingerprint:
00266:         return False
00267:     expected = manifest.get("chunk_count", 0)
00268:     actual = len(list(PROJECT_CHUNK_DIR.glob("chunk_*.md")))
00269:     return expected == actual
00270: 
00271: 
00272: def write_readme() -> None:
00273:     README_MD.write_text(
00274:         "\n".join(
00275:             [
00276:                 "# indexAI",
00277:                 "",
00278:                 "Generated AI indexes and patch-library notes for the Spaziotempo Blender project.",
00279:                 "",
00280:                 "- `project_code_index.md` is the primary project structure library.",
00281:                 "- `project_code_manifest.json` contains hashes, symbols and chunk metadata.",
00282:                 "- `project_code_chunks/` contains line-numbered source chunks.",
00283:                 "- `patch_library/` is reserved for AI patch plans and drafts.",
00284:                 "",
00285:                 "This folder is excluded from source indexing to avoid recursive AI context loops.",
00286:                 "",
00287:             ]
00288:         ),
00289:         encoding="utf-8",
00290:     )
00291: 
00292: 
00293: def write_chunks(records: list[dict], max_chunk_chars: int) -> list[dict]:
00294:     PROJECT_CHUNK_DIR.mkdir(parents=True, exist_ok=True)
00295:     for old_chunk in PROJECT_CHUNK_DIR.glob("chunk_*.md"):
00296:         old_chunk.unlink()
00297: 
00298:     chunks: list[dict] = []
00299:     pending: list[dict] = []
00300:     for record in records:
```
