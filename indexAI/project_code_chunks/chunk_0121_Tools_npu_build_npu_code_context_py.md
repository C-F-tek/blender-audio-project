# Project Code Chunk 121/212

- File: `Tools/npu/build_npu_code_context.py`
- Part: `1`
- Lines: `1-306`

## Symbol Map
- Imports: `from __future__ import annotations`, `from pathlib import Path`, `ast`, `hashlib`, `json`, `re`, `from datetime import datetime`
- Functions: `sha256_text(text)` line 56; `rel_to_root(path)` line 60; `slugify(value, max_len)` line 64; `is_usable_text_file(path)` line 69; `collect_files()` line 75; `target_name(target)` line 99; `extract_symbols(source)` line 107; `file_record(path, source)` line 169; `format_symbol_summary(record)` line 184; `numbered_lines(lines, start_line)` line 225; `split_source(source, max_chars)` line 229; `write_context_chunks(files, sources)` line 255; `write_index(files, chunks, created_at)` line 325; `main()` line 348
- Assignments: `ROOT`, `SCRIPT_DIR`, `OUT_DIR`, `OUT_MD`, `OUT_INDEX_MD`, `OUT_JSON`, `CHUNK_DIR`, `MAX_CHUNK_CHARS`, `PRIORITY_FILES`, `DISCOVERY_GLOBS`, `EXCLUDE_PARTS`, `TEXT_SUFFIXES`

## Content
```py
00001: from __future__ import annotations
00002: 
00003: from pathlib import Path
00004: import ast
00005: import hashlib
00006: import json
00007: import re
00008: from datetime import datetime
00009: 
00010: 
00011: ROOT = Path(__file__).resolve().parents[2]
00012: SCRIPT_DIR = ROOT / "Scripting" / "v61b"
00013: OUT_DIR = ROOT / "Tools" / "npu"
00014: OUT_MD = OUT_DIR / "npu_code_context.md"
00015: OUT_INDEX_MD = OUT_DIR / "npu_code_index.md"
00016: OUT_JSON = OUT_DIR / "npu_code_manifest.json"
00017: CHUNK_DIR = OUT_DIR / "npu_code_chunks"
00018: 
00019: MAX_CHUNK_CHARS = 10500
00020: 
00021: PRIORITY_FILES = [
00022:     ROOT / "analyze_wav.py",
00023:     ROOT / "build_track_summary.py",
00024:     ROOT / "normalize_scene_spec.py",
00025:     OUT_DIR / "npu_runtime.py",
00026:     OUT_DIR / "ollama_runtime.py",
00027:     OUT_DIR / "build_blender_manual_context.py",
00028:     OUT_DIR / "run_dual_ai_pipeline.py",
00029:     SCRIPT_DIR / "config.py",
00030:     SCRIPT_DIR / "main_v61b.py",
00031:     SCRIPT_DIR / "animation.py",
00032:     SCRIPT_DIR / "materials.py",
00033:     SCRIPT_DIR / "physics_setup.py",
00034:     SCRIPT_DIR / "fog_dynamics.py",
00035:     SCRIPT_DIR / "fog_filaments.py",
00036:     SCRIPT_DIR / "atmosphere_setup.py",
00037:     SCRIPT_DIR / "world_setup.py",
00038:     SCRIPT_DIR / "render_setup.py",
00039:     SCRIPT_DIR / "scene_tuning_panel.py",
00040:     SCRIPT_DIR / "hot_update_scene_v61b.py",
00041:     SCRIPT_DIR / "encode_image_sequence_v61b.py",
00042:     SCRIPT_DIR / "encode_ffmpeg_v61b.py",
00043:     SCRIPT_DIR / "PROJECT_STRUCTURE.md",
00044:     SCRIPT_DIR / "SCENE_TUNING_GUIDE.md",
00045: ]
00046: 
00047: DISCOVERY_GLOBS = [
00048:     (SCRIPT_DIR, ["*.py", "*.md", "hotpatch/*.py", "spaziotempo/**/*.py"]),
00049:     (OUT_DIR, ["*.py", "*.ps1"]),
00050: ]
00051: 
00052: EXCLUDE_PARTS = {"__pycache__", ".npucache", "npu_code_chunks"}
00053: TEXT_SUFFIXES = {".py", ".md", ".ps1", ".json", ".txt"}
00054: 
00055: 
00056: def sha256_text(text: str) -> str:
00057:     return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()
00058: 
00059: 
00060: def rel_to_root(path: Path) -> str:
00061:     return str(path.relative_to(ROOT)).replace("\\", "/")
00062: 
00063: 
00064: def slugify(value: str, max_len: int = 64) -> str:
00065:     slug = re.sub(r"[^A-Za-z0-9]+", "_", value).strip("_")
00066:     return slug[:max_len] or "chunk"
00067: 
00068: 
00069: def is_usable_text_file(path: Path) -> bool:
00070:     if path.suffix.lower() not in TEXT_SUFFIXES:
00071:         return False
00072:     return not any(part in EXCLUDE_PARTS for part in path.parts)
00073: 
00074: 
00075: def collect_files() -> list[Path]:
00076:     seen: set[Path] = set()
00077:     ordered: list[Path] = []
00078: 
00079:     def add(path: Path) -> None:
00080:         resolved = path.resolve()
00081:         if resolved in seen or not resolved.exists() or not resolved.is_file():
00082:             return
00083:         if not is_usable_text_file(resolved):
00084:             return
00085:         seen.add(resolved)
00086:         ordered.append(resolved)
00087: 
00088:     for path in PRIORITY_FILES:
00089:         add(path)
00090: 
00091:     for base, patterns in DISCOVERY_GLOBS:
00092:         for pattern in patterns:
00093:             for path in sorted(base.glob(pattern), key=lambda item: rel_to_root(item.resolve()).lower()):
00094:                 add(path)
00095: 
00096:     return ordered
00097: 
00098: 
00099: def target_name(target: ast.expr) -> str | None:
00100:     if isinstance(target, ast.Name):
00101:         return target.id
00102:     if isinstance(target, ast.Attribute):
00103:         return target.attr
00104:     return None
00105: 
00106: 
00107: def extract_symbols(source: str) -> dict:
00108:     symbols = {
00109:         "imports": [],
00110:         "functions": [],
00111:         "classes": [],
00112:         "assignments": [],
00113:     }
00114: 
00115:     try:
00116:         tree = ast.parse(source)
00117:     except SyntaxError as exc:
00118:         symbols["syntax_error"] = str(exc)
00119:         return symbols
00120: 
00121:     for node in tree.body:
00122:         if isinstance(node, ast.Import):
00123:             for alias in node.names:
00124:                 symbols["imports"].append(alias.name)
00125: 
00126:         elif isinstance(node, ast.ImportFrom):
00127:             module = node.module or ""
00128:             names = ", ".join(alias.name for alias in node.names)
00129:             symbols["imports"].append(f"from {module} import {names}")
00130: 
00131:         elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
00132:             args = [arg.arg for arg in node.args.args]
00133:             symbols["functions"].append(
00134:                 {
00135:                     "name": node.name,
00136:                     "line": node.lineno,
00137:                     "args": args,
00138:                     "async": isinstance(node, ast.AsyncFunctionDef),
00139:                 }
00140:             )
00141: 
00142:         elif isinstance(node, ast.ClassDef):
00143:             methods = []
00144:             for child in node.body:
00145:                 if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
00146:                     methods.append({"name": child.name, "line": child.lineno})
00147:             symbols["classes"].append(
00148:                 {
00149:                     "name": node.name,
00150:                     "line": node.lineno,
00151:                     "methods": methods,
00152:                 }
00153:             )
00154: 
00155:         elif isinstance(node, ast.Assign):
00156:             for target in node.targets:
00157:                 name = target_name(target)
00158:                 if name:
00159:                     symbols["assignments"].append(name)
00160: 
00161:         elif isinstance(node, ast.AnnAssign):
00162:             name = target_name(node.target)
00163:             if name:
00164:                 symbols["assignments"].append(name)
00165: 
00166:     return symbols
00167: 
00168: 
00169: def file_record(path: Path, source: str) -> dict:
00170:     suffix = path.suffix.lower()
00171:     record = {
00172:         "file": rel_to_root(path),
00173:         "exists": True,
00174:         "suffix": suffix,
00175:         "lines": source.count("\n") + 1 if source else 0,
00176:         "chars": len(source),
00177:         "sha256": sha256_text(source),
00178:     }
00179:     if suffix == ".py":
00180:         record["symbols"] = extract_symbols(source)
00181:     return record
00182: 
00183: 
00184: def format_symbol_summary(record: dict) -> str:
00185:     symbols = record.get("symbols")
00186:     if not symbols:
00187:         return ""
00188: 
00189:     lines: list[str] = []
00190: 
00191:     if symbols.get("syntax_error"):
00192:         lines.append(f"- Syntax error: `{symbols['syntax_error']}`")
00193: 
00194:     imports = symbols.get("imports", [])
00195:     if imports:
00196:         lines.append("- Imports: " + ", ".join(f"`{item}`" for item in imports[:24]))
00197: 
00198:     classes = symbols.get("classes", [])
00199:     if classes:
00200:         class_bits = []
00201:         for item in classes[:20]:
00202:             method_names = ", ".join(method["name"] for method in item.get("methods", [])[:10])
00203:             if method_names:
00204:                 class_bits.append(f"`{item['name']}` line {item['line']} methods: {method_names}")
00205:             else:
00206:                 class_bits.append(f"`{item['name']}` line {item['line']}")
00207:         lines.append("- Classes: " + "; ".join(class_bits))
00208: 
00209:     functions = symbols.get("functions", [])
00210:     if functions:
00211:         function_bits = []
00212:         for item in functions[:36]:
00213:             args = ", ".join(item["args"])
00214:             prefix = "async " if item.get("async") else ""
00215:             function_bits.append(f"`{prefix}{item['name']}({args})` line {item['line']}")
00216:         lines.append("- Functions: " + "; ".join(function_bits))
00217: 
00218:     assignments = symbols.get("assignments", [])
00219:     if assignments:
00220:         lines.append("- Assignments: " + ", ".join(f"`{name}`" for name in assignments[:80]))
00221: 
00222:     return "\n".join(lines)
00223: 
00224: 
00225: def numbered_lines(lines: list[str], start_line: int) -> str:
00226:     return "\n".join(f"{line_no:05d}: {line}" for line_no, line in enumerate(lines, start_line))
00227: 
00228: 
00229: def split_source(source: str, max_chars: int) -> list[tuple[int, int, list[str]]]:
00230:     source_lines = source.splitlines()
00231:     if not source_lines:
00232:         return [(1, 1, [])]
00233: 
00234:     chunks: list[tuple[int, int, list[str]]] = []
00235:     current: list[str] = []
00236:     current_len = 0
00237:     start_line = 1
00238: 
00239:     for line_no, line in enumerate(source_lines, 1):
00240:         cost = len(line) + 9
00241:         if current and current_len + cost > max_chars:
00242:             chunks.append((start_line, line_no - 1, current))
00243:             current = []
00244:             current_len = 0
00245:             start_line = line_no
00246:         current.append(line)
00247:         current_len += cost
00248: 
00249:     if current:
00250:         chunks.append((start_line, start_line + len(current) - 1, current))
00251: 
00252:     return chunks
00253: 
00254: 
00255: def write_context_chunks(files: list[dict], sources: dict[str, str]) -> list[dict]:
00256:     CHUNK_DIR.mkdir(parents=True, exist_ok=True)
00257: 
00258:     for old_chunk in CHUNK_DIR.glob("chunk_*.md"):
00259:         old_chunk.unlink()
00260: 
00261:     pending: list[dict] = []
00262: 
00263:     for record in files:
00264:         rel_file = record["file"]
00265:         source = sources[rel_file]
00266:         for part_index, (start_line, end_line, lines) in enumerate(split_source(source, MAX_CHUNK_CHARS), 1):
00267:             pending.append(
00268:                 {
00269:                     "file": rel_file,
00270:                     "part": part_index,
00271:                     "start_line": start_line,
00272:                     "end_line": end_line,
00273:                     "text": numbered_lines(lines, start_line),
00274:                     "symbols": format_symbol_summary(record),
00275:                     "suffix": record.get("suffix", ""),
00276:                 }
00277:             )
00278: 
00279:     total = len(pending)
00280:     chunks: list[dict] = []
00281: 
00282:     for index, item in enumerate(pending, 1):
00283:         rel_file = item["file"]
00284:         path_slug = slugify(rel_file)
00285:         chunk_name = f"chunk_{index:03d}_{path_slug}.md"
00286:         chunk_path = CHUNK_DIR / chunk_name
00287:         fence = item["suffix"].lstrip(".") or "text"
00288: 
00289:         body = [
00290:             f"# NPU Long Context Chunk {index}/{total}\n\n",
00291:             f"- File: `{rel_file}`\n",
00292:             f"- Part: `{item['part']}`\n",
00293:             f"- Lines: `{item['start_line']}-{item['end_line']}`\n\n",
00294:         ]
00295: 
00296:         if item["symbols"]:
00297:             body.append("## Symbol Map\n")
00298:             body.append(item["symbols"])
00299:             body.append("\n\n")
00300: 
00301:         body.append("## Content\n")
00302:         body.append(f"```{fence}\n")
00303:         body.append(item["text"])
00304:         body.append("\n```\n")
00305: 
00306:         chunk_text = "".join(body)
```
