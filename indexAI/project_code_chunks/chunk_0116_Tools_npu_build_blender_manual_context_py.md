# Project Code Chunk 116/212

- File: `Tools/npu/build_blender_manual_context.py`
- Part: `1`
- Lines: `1-301`

## Symbol Map
- Imports: `from __future__ import annotations`, `from pathlib import Path`, `from html.parser import HTMLParser`, `argparse`, `hashlib`, `json`, `re`, `from datetime import datetime`
- Classes: `TextExtractor` line 62 methods: __init__, handle_starttag, handle_endtag, handle_data, text
- Functions: `sha256_text(text)` line 95; `rel(path)` line 99; `slug(value)` line 106; `extract_text(path)` line 110; `score_text(path, text)` line 119; `score_path(path)` line 124; `split_text(text, max_chars)` line 144; `ensure_manual_root()` line 161; `source_group(path)` line 167; `iter_manual_files(manual_root)` line 175; `build_manual_context(limit_files, manual_root)` line 195; `main()` line 296
- Assignments: `ROOT`, `MANUAL_ROOT`, `LEGACY_MANUAL_DIR`, `MANUAL_README`, `OUT_DIR`, `CHUNK_DIR`, `OUT_INDEX`, `OUT_MANIFEST`, `MAX_CHARS`, `TEXT_EXTENSIONS`, `HTML_EXTENSIONS`, `KEYWORDS`, `README_TEXT`

## Content
```py
00001: from __future__ import annotations
00002: 
00003: from pathlib import Path
00004: from html.parser import HTMLParser
00005: import argparse
00006: import hashlib
00007: import json
00008: import re
00009: from datetime import datetime
00010: 
00011: 
00012: ROOT = Path(__file__).resolve().parents[2]
00013: MANUAL_ROOT = Path.home() / "blender" / "manual"
00014: LEGACY_MANUAL_DIR = Path.home() / "blender" / "blender_manual_html"
00015: MANUAL_README = MANUAL_ROOT / "README_MANUALI.md"
00016: OUT_DIR = ROOT / "Tools" / "npu"
00017: CHUNK_DIR = OUT_DIR / "npu_blender_manual_chunks"
00018: OUT_INDEX = OUT_DIR / "npu_blender_manual_index.md"
00019: OUT_MANIFEST = OUT_DIR / "npu_blender_manual_manifest.json"
00020: 
00021: MAX_CHARS = 11000
00022: TEXT_EXTENSIONS = {".md", ".txt", ".rst", ".py"}
00023: HTML_EXTENSIONS = {".html", ".htm"}
00024: KEYWORDS = [
00025:     "python",
00026:     "scripting",
00027:     "driver",
00028:     "fcurve",
00029:     "keyframe",
00030:     "geometry nodes",
00031:     "shader",
00032:     "material",
00033:     "compositor",
00034:     "eevee",
00035:     "cycles",
00036:     "volume",
00037:     "particle",
00038:     "force field",
00039:     "modifier",
00040:     "animation",
00041:     "sequencer",
00042: ]
00043: 
00044: README_TEXT = """# Manuali locali per NPU/Ollama
00045: 
00046: Metti qui i manuali offline che vuoi rendere disponibili alla pipeline IA.
00047: 
00048: Supportati automaticamente:
00049: - cartelle HTML, per esempio manuali Blender esportati da browser o scaricati
00050: - file `.html` / `.htm`
00051: - file testo `.md`, `.txt`, `.rst`
00052: - piccoli file `.py` usati come riferimento tecnico
00053: 
00054: Quando lanci la pipeline con `-IncludeManual`, lo script indicizza tutto quello che trova qui dentro e genera chunk in:
00055: 
00056: `C:\\Users\\carmi\\blender\\blender-audio-project\\Tools\\npu\\npu_blender_manual_chunks`
00057: 
00058: Non devi aggiungere i file manualmente ai prompt: NPU/Ollama useranno l'indice e i chunk prodotti.
00059: """
00060: 
00061: 
00062: class TextExtractor(HTMLParser):
00063:     def __init__(self) -> None:
00064:         super().__init__()
00065:         self.parts: list[str] = []
00066:         self.skip = False
00067: 
00068:     def handle_starttag(self, tag: str, attrs) -> None:
00069:         if tag in {"script", "style", "nav"}:
00070:             self.skip = True
00071:         if tag in {"h1", "h2", "h3", "p", "li", "dt", "dd", "pre", "code"}:
00072:             self.parts.append("\n")
00073: 
00074:     def handle_endtag(self, tag: str) -> None:
00075:         if tag in {"script", "style", "nav"}:
00076:             self.skip = False
00077:         if tag in {"h1", "h2", "h3", "p", "li", "dt", "dd", "pre"}:
00078:             self.parts.append("\n")
00079: 
00080:     def handle_data(self, data: str) -> None:
00081:         if self.skip:
00082:             return
00083:         text = data.strip()
00084:         if text:
00085:             self.parts.append(text)
00086:             self.parts.append(" ")
00087: 
00088:     def text(self) -> str:
00089:         raw = "".join(self.parts)
00090:         raw = re.sub(r"[ \t]+", " ", raw)
00091:         raw = re.sub(r"\n\s*\n\s*\n+", "\n\n", raw)
00092:         return raw.strip()
00093: 
00094: 
00095: def sha256_text(text: str) -> str:
00096:     return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()
00097: 
00098: 
00099: def rel(path: Path) -> str:
00100:     try:
00101:         return str(path.relative_to(ROOT)).replace("\\", "/")
00102:     except ValueError:
00103:         return str(path)
00104: 
00105: 
00106: def slug(value: str) -> str:
00107:     return re.sub(r"[^A-Za-z0-9]+", "_", value).strip("_")[:90] or "manual"
00108: 
00109: 
00110: def extract_text(path: Path) -> str:
00111:     if path.suffix.lower() in TEXT_EXTENSIONS:
00112:         return path.read_text(encoding="utf-8", errors="replace").strip()
00113: 
00114:     parser = TextExtractor()
00115:     parser.feed(path.read_text(encoding="utf-8", errors="replace"))
00116:     return parser.text()
00117: 
00118: 
00119: def score_text(path: Path, text: str) -> int:
00120:     haystack = (str(path).lower() + "\n" + text[:20000].lower())
00121:     return sum(haystack.count(keyword) for keyword in KEYWORDS)
00122: 
00123: 
00124: def score_path(path: Path) -> int:
00125:     haystack = str(path).lower().replace("\\", "/")
00126:     score = sum(4 for keyword in KEYWORDS if keyword.replace(" ", "_") in haystack or keyword in haystack)
00127:     extra_terms = [
00128:         "python",
00129:         "api",
00130:         "drivers",
00131:         "animation",
00132:         "modifiers",
00133:         "physics",
00134:         "particles",
00135:         "compositing",
00136:         "render",
00137:         "shader",
00138:         "nodes",
00139:     ]
00140:     score += sum(2 for term in extra_terms if term in haystack)
00141:     return score
00142: 
00143: 
00144: def split_text(text: str, max_chars: int = MAX_CHARS) -> list[str]:
00145:     if len(text) <= max_chars:
00146:         return [text]
00147: 
00148:     chunks = []
00149:     start = 0
00150:     while start < len(text):
00151:         end = min(start + max_chars, len(text))
00152:         if end < len(text):
00153:             split_at = max(text.rfind("\n", start, end), text.rfind(". ", start, end))
00154:             if split_at > start + max_chars // 2:
00155:                 end = split_at + 1
00156:         chunks.append(text[start:end].strip())
00157:         start = end
00158:     return [chunk for chunk in chunks if chunk]
00159: 
00160: 
00161: def ensure_manual_root() -> None:
00162:     MANUAL_ROOT.mkdir(parents=True, exist_ok=True)
00163:     if not MANUAL_README.exists():
00164:         MANUAL_README.write_text(README_TEXT, encoding="utf-8")
00165: 
00166: 
00167: def source_group(path: Path) -> str:
00168:     try:
00169:         relative = path.relative_to(MANUAL_ROOT)
00170:         return relative.parts[0] if relative.parts else MANUAL_ROOT.name
00171:     except ValueError:
00172:         return path.parent.name
00173: 
00174: 
00175: def iter_manual_files(manual_root: Path) -> list[Path]:
00176:     paths: list[Path] = []
00177:     for extension in sorted(HTML_EXTENSIONS | TEXT_EXTENSIONS):
00178:         paths.extend(manual_root.rglob(f"*{extension}"))
00179: 
00180:     if not paths and LEGACY_MANUAL_DIR.exists():
00181:         for extension in sorted(HTML_EXTENSIONS | TEXT_EXTENSIONS):
00182:             paths.extend(LEGACY_MANUAL_DIR.rglob(f"*{extension}"))
00183: 
00184:     ignored_dirs = {"_images", "_static", ".git", "__pycache__"}
00185:     filtered = []
00186:     for path in paths:
00187:         if any(part in ignored_dirs for part in path.parts):
00188:             continue
00189:         if path.name == MANUAL_README.name:
00190:             continue
00191:         filtered.append(path)
00192:     return filtered
00193: 
00194: 
00195: def build_manual_context(limit_files: int = 80, manual_root: Path | str = MANUAL_ROOT) -> dict:
00196:     global MANUAL_ROOT, MANUAL_README
00197: 
00198:     MANUAL_ROOT = Path(manual_root)
00199:     MANUAL_README = MANUAL_ROOT / "README_MANUALI.md"
00200:     ensure_manual_root()
00201: 
00202:     CHUNK_DIR.mkdir(parents=True, exist_ok=True)
00203:     for old in CHUNK_DIR.glob("chunk_*.md"):
00204:         old.unlink()
00205: 
00206:     manual_files = iter_manual_files(MANUAL_ROOT)
00207:     ranked_paths = sorted(
00208:         ((score_path(path), path) for path in manual_files),
00209:         key=lambda item: item[0],
00210:         reverse=True,
00211:     )
00212:     candidate_paths = [path for score, path in ranked_paths if score > 0]
00213:     if not candidate_paths:
00214:         candidate_paths = [path for _, path in ranked_paths]
00215:     candidate_paths = candidate_paths[: max(limit_files * 6, limit_files)]
00216:     records = []
00217: 
00218:     for path in candidate_paths:
00219:         try:
00220:             text = extract_text(path)
00221:         except Exception:
00222:             continue
00223:         score = score_path(path) + score_text(path, text)
00224:         if score <= 0:
00225:             continue
00226:         records.append({"path": path, "score": score, "text": text})
00227: 
00228:     records.sort(key=lambda item: item["score"], reverse=True)
00229:     records = records[:limit_files]
00230: 
00231:     chunks = []
00232:     chunk_index = 1
00233:     for record in records:
00234:         path = record["path"]
00235:         for part, text in enumerate(split_text(record["text"]), 1):
00236:             group = source_group(path)
00237:             chunk_path = CHUNK_DIR / f"chunk_{chunk_index:03d}_{slug(group)}_{slug(path.stem)}.md"
00238:             body = (
00239:                 f"# Blender Manual Chunk {chunk_index}\n\n"
00240:                 f"- Source: `{path}`\n"
00241:                 f"- Manual group: `{group}`\n"
00242:                 f"- Score: `{record['score']}`\n"
00243:                 f"- Part: `{part}`\n\n"
00244:                 "## Content\n\n"
00245:                 f"{text}\n"
00246:             )
00247:             chunk_path.write_text(body, encoding="utf-8")
00248:             chunks.append(
00249:                 {
00250:                     "index": chunk_index,
00251:                     "source": str(path),
00252:                     "manual_group": group,
00253:                     "path": rel(chunk_path),
00254:                     "score": record["score"],
00255:                     "part": part,
00256:                     "chars": len(body),
00257:                     "sha256": sha256_text(body),
00258:                 }
00259:             )
00260:             chunk_index += 1
00261: 
00262:     created_at = datetime.now().isoformat(timespec="seconds")
00263:     manifest = {
00264:         "created_at": created_at,
00265:         "manual_root": str(MANUAL_ROOT),
00266:         "manual_readme": str(MANUAL_README),
00267:         "legacy_fallback_dir": str(LEGACY_MANUAL_DIR),
00268:         "keywords": KEYWORDS,
00269:         "supported_extensions": sorted(HTML_EXTENSIONS | TEXT_EXTENSIONS),
00270:         "discovered_file_count": len(manual_files),
00271:         "source_file_count": len(records),
00272:         "chunk_count": len(chunks),
00273:         "chunk_dir": rel(CHUNK_DIR),
00274:         "chunks": chunks,
00275:     }
00276: 
00277:     md = [
00278:         "# Blender Manual Context Index\n\n",
00279:         f"Generated: `{created_at}`\n\n",
00280:         "Purpose: offline local manual chunks for NPU/Ollama implementation drafts.\n\n",
00281:         f"Manual root: `{MANUAL_ROOT}`\n\n",
00282:         f"Discovered files: `{len(manual_files)}` | Indexed sources: `{len(records)}` | Chunks: `{len(chunks)}`\n\n",
00283:         "## Sources\n",
00284:     ]
00285:     for record in records[:40]:
00286:         md.append(f"- `{record['path']}` score `{record['score']}`\n")
00287:     md.append("\n## Chunks\n")
00288:     for chunk in chunks:
00289:         md.append(f"- `{chunk['path']}` from `{chunk['source']}`\n")
00290: 
00291:     OUT_MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
00292:     OUT_INDEX.write_text("".join(md), encoding="utf-8")
00293:     return manifest
00294: 
00295: 
00296: def main() -> None:
00297:     global MANUAL_ROOT, MANUAL_README
00298: 
00299:     parser = argparse.ArgumentParser()
00300:     parser.add_argument("--limit-files", type=int, default=80)
00301:     parser.add_argument("--manual-root", default=str(MANUAL_ROOT))
```
