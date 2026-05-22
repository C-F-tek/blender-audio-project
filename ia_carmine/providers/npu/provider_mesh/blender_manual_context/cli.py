from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path

from ia_carmine.providers.npu.paths import find_repo_root

ROOT = find_repo_root(__file__)
MANUAL_ROOT = Path.home() / "blender" / "manual"
LEGACY_MANUAL_DIR = Path.home() / "blender" / "blender_manual_html"
MANUAL_README = MANUAL_ROOT / "README_MANUALI.md"
OUT_DIR = ROOT / "Tools" / "npu"
CHUNK_DIR = OUT_DIR / "npu_blender_manual_chunks"
OUT_INDEX = OUT_DIR / "npu_blender_manual_index.md"
OUT_MANIFEST = OUT_DIR / "npu_blender_manual_manifest.json"

MAX_CHARS = 11000
TEXT_EXTENSIONS = {".md", ".txt", ".rst", ".py"}
HTML_EXTENSIONS = {".html", ".htm"}
KEYWORDS = [
    "python",
    "scripting",
    "driver",
    "fcurve",
    "keyframe",
    "geometry nodes",
    "shader",
    "material",
    "compositor",
    "eevee",
    "cycles",
    "volume",
    "particle",
    "force field",
    "modifier",
    "animation",
    "sequencer",
]

README_TEXT = """# Manuali locali per NPU/Ollama

Metti qui i manuali offline che vuoi rendere disponibili alla pipeline IA.

Supportati automaticamente:
- cartelle HTML, per esempio manuali Blender esportati da browser o scaricati
- file `.html` / `.htm`
- file testo `.md`, `.txt`, `.rst`
- piccoli file `.py` usati come riferimento tecnico

Quando lanci la pipeline con `-IncludeManual`, lo script indicizza tutto quello che trova qui dentro e genera chunk in:

`C:\\Users\\carmi\\blender\\blender-audio-project\\Tools\\npu\\npu_blender_manual_chunks`

Non devi aggiungere i file manualmente ai prompt: NPU/Ollama useranno l'indice e i chunk prodotti.
"""


class TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []
        self.skip = False

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag in {"script", "style", "nav"}:
            self.skip = True
        if tag in {"h1", "h2", "h3", "p", "li", "dt", "dd", "pre", "code"}:
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style", "nav"}:
            self.skip = False
        if tag in {"h1", "h2", "h3", "p", "li", "dt", "dd", "pre"}:
            self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        if self.skip:
            return
        text = data.strip()
        if text:
            self.parts.append(text)
            self.parts.append(" ")

    def text(self) -> str:
        raw = "".join(self.parts)
        raw = re.sub(r"[ \t]+", " ", raw)
        raw = re.sub(r"\n\s*\n\s*\n+", "\n\n", raw)
        return raw.strip()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def slug(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "_", value).strip("_")[:90] or "manual"


def extract_text(path: Path) -> str:
    if path.suffix.lower() in TEXT_EXTENSIONS:
        return path.read_text(encoding="utf-8", errors="replace").strip()

    parser = TextExtractor()
    parser.feed(path.read_text(encoding="utf-8", errors="replace"))
    return parser.text()


def score_text(path: Path, text: str) -> int:
    haystack = str(path).lower() + "\n" + text[:20000].lower()
    return sum(haystack.count(keyword) for keyword in KEYWORDS)


def score_path(path: Path) -> int:
    haystack = str(path).lower().replace("\\", "/")
    score = sum(
        4 for keyword in KEYWORDS if keyword.replace(" ", "_") in haystack or keyword in haystack
    )
    extra_terms = [
        "python",
        "api",
        "drivers",
        "animation",
        "modifiers",
        "physics",
        "particles",
        "compositing",
        "render",
        "shader",
        "nodes",
    ]
    score += sum(2 for term in extra_terms if term in haystack)
    return score


def split_text(text: str, max_chars: int = MAX_CHARS) -> list[str]:
    if len(text) <= max_chars:
        return [text]

    chunks = []
    start = 0
    while start < len(text):
        end = min(start + max_chars, len(text))
        if end < len(text):
            split_at = max(text.rfind("\n", start, end), text.rfind(". ", start, end))
            if split_at > start + max_chars // 2:
                end = split_at + 1
        chunks.append(text[start:end].strip())
        start = end
    return [chunk for chunk in chunks if chunk]


def ensure_manual_root() -> None:
    MANUAL_ROOT.mkdir(parents=True, exist_ok=True)
    if not MANUAL_README.exists():
        MANUAL_README.write_text(README_TEXT, encoding="utf-8")


def source_group(path: Path) -> str:
    try:
        relative = path.relative_to(MANUAL_ROOT)
        return relative.parts[0] if relative.parts else MANUAL_ROOT.name
    except ValueError:
        return path.parent.name


def iter_manual_files(manual_root: Path) -> list[Path]:
    paths: list[Path] = []
    for extension in sorted(HTML_EXTENSIONS | TEXT_EXTENSIONS):
        paths.extend(manual_root.rglob(f"*{extension}"))

    if not paths and LEGACY_MANUAL_DIR.exists():
        for extension in sorted(HTML_EXTENSIONS | TEXT_EXTENSIONS):
            paths.extend(LEGACY_MANUAL_DIR.rglob(f"*{extension}"))

    ignored_dirs = {"_images", "_static", ".git", "__pycache__"}
    filtered = []
    for path in paths:
        if any(part in ignored_dirs for part in path.parts):
            continue
        if path.name == MANUAL_README.name:
            continue
        filtered.append(path)
    return filtered


def build_manual_context(limit_files: int = 80, manual_root: Path | str = MANUAL_ROOT) -> dict:
    global MANUAL_ROOT, MANUAL_README

    MANUAL_ROOT = Path(manual_root)
    MANUAL_README = MANUAL_ROOT / "README_MANUALI.md"
    ensure_manual_root()

    CHUNK_DIR.mkdir(parents=True, exist_ok=True)
    for old in CHUNK_DIR.glob("chunk_*.md"):
        old.unlink()

    manual_files = iter_manual_files(MANUAL_ROOT)
    ranked_paths = sorted(
        ((score_path(path), path) for path in manual_files),
        key=lambda item: item[0],
        reverse=True,
    )
    candidate_paths = [path for score, path in ranked_paths if score > 0]
    if not candidate_paths:
        candidate_paths = [path for _, path in ranked_paths]
    candidate_paths = candidate_paths[: max(limit_files * 6, limit_files)]
    records = []

    for path in candidate_paths:
        try:
            text = extract_text(path)
        except Exception:
            continue
        score = score_path(path) + score_text(path, text)
        if score <= 0:
            continue
        records.append({"path": path, "score": score, "text": text})

    records.sort(key=lambda item: item["score"], reverse=True)
    records = records[:limit_files]

    chunks = []
    chunk_index = 1
    for record in records:
        path = record["path"]
        for part, text in enumerate(split_text(record["text"]), 1):
            group = source_group(path)
            chunk_path = CHUNK_DIR / f"chunk_{chunk_index:03d}_{slug(group)}_{slug(path.stem)}.md"
            body = (
                f"# Blender Manual Chunk {chunk_index}\n\n"
                f"- Source: `{path}`\n"
                f"- Manual group: `{group}`\n"
                f"- Score: `{record['score']}`\n"
                f"- Part: `{part}`\n\n"
                "## Content\n\n"
                f"{text}\n"
            )
            chunk_path.write_text(body, encoding="utf-8")
            chunks.append(
                {
                    "index": chunk_index,
                    "source": str(path),
                    "manual_group": group,
                    "path": rel(chunk_path),
                    "score": record["score"],
                    "part": part,
                    "chars": len(body),
                    "sha256": sha256_text(body),
                }
            )
            chunk_index += 1

    created_at = datetime.now().isoformat(timespec="seconds")
    manifest = {
        "created_at": created_at,
        "manual_root": str(MANUAL_ROOT),
        "manual_readme": str(MANUAL_README),
        "legacy_fallback_dir": str(LEGACY_MANUAL_DIR),
        "keywords": KEYWORDS,
        "supported_extensions": sorted(HTML_EXTENSIONS | TEXT_EXTENSIONS),
        "discovered_file_count": len(manual_files),
        "source_file_count": len(records),
        "chunk_count": len(chunks),
        "chunk_dir": rel(CHUNK_DIR),
        "chunks": chunks,
    }

    md = [
        "# Blender Manual Context Index\n\n",
        f"Generated: `{created_at}`\n\n",
        "Purpose: offline local manual chunks for NPU/Ollama implementation drafts.\n\n",
        f"Manual root: `{MANUAL_ROOT}`\n\n",
        f"Discovered files: `{len(manual_files)}` | Indexed sources: `{len(records)}` | Chunks: `{len(chunks)}`\n\n",
        "## Sources\n",
    ]
    for record in records[:40]:
        md.append(f"- `{record['path']}` score `{record['score']}`\n")
    md.append("\n## Chunks\n")
    for chunk in chunks:
        md.append(f"- `{chunk['path']}` from `{chunk['source']}`\n")

    OUT_MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    OUT_INDEX.write_text("".join(md), encoding="utf-8")
    return manifest


def main() -> None:
    global MANUAL_ROOT, MANUAL_README

    parser = argparse.ArgumentParser()
    parser.add_argument("--limit-files", type=int, default=80)
    parser.add_argument("--manual-root", default=str(MANUAL_ROOT))
    parser.add_argument(
        "--ensure-only",
        action="store_true",
        help="Create the local manual folder and README without scanning/indexing manuals.",
    )
    args = parser.parse_args()

    if args.ensure_only:
        MANUAL_ROOT = Path(args.manual_root)
        MANUAL_README = MANUAL_ROOT / "README_MANUALI.md"
        ensure_manual_root()
        print(f"[OK] Manual root ready: {MANUAL_ROOT}")
        print(f"[OK] Manual README: {MANUAL_README}")
        return

    manifest = build_manual_context(limit_files=args.limit_files, manual_root=args.manual_root)
    print(f"[OK] Manual root: {manifest['manual_root']}")
    print(f"[OK] Manual README: {manifest['manual_readme']}")
    print(f"[OK] Wrote: {OUT_INDEX}")
    print(f"[OK] Wrote: {OUT_MANIFEST}")
    print(f"[OK] Wrote chunks: {CHUNK_DIR} ({manifest['chunk_count']} files)")


if __name__ == "__main__":
    main()
