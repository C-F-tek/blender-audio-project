from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import warnings
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INDEX_DIR = ROOT / "indexAI"
PROJECT_INDEX_MD = INDEX_DIR / "project_code_index.md"
PROJECT_MANIFEST_JSON = INDEX_DIR / "project_code_manifest.json"
PROJECT_CHUNK_DIR = INDEX_DIR / "project_code_chunks"
PATCH_LIBRARY_DIR = INDEX_DIR / "patch_library"
README_MD = INDEX_DIR / "README.md"

DEFAULT_MAX_CHUNK_CHARS = 12000
TEXT_SUFFIXES = {".py", ".ps1", ".md", ".json", ".txt", ".cfg", ".ini", ".toml", ".yaml", ".yml"}
EXCLUDE_DIRS = {
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "__pycache__",
    "cache",
    "indexAI",
    "node_modules",
    "output",
    "renders",
    "venv",
    "venvs",
    "old script legacy",
}
EXCLUDE_PARTS = {
    ".npucache",
    "npu_blender_manual_chunks",
    "npu_code_chunks",
    "npu_music_chunks",
}
EXCLUDE_FILE_PREFIXES = {
    ".aider",
    "npu_code_context",
    "npu_code_index",
    "npu_context_for_aider",
    "npu_music_context",
    "npu_music_context_for_aider",
    "npu_dual_ai_chunk_notes",
    "npu_dual_ai_technical_notes",
    "ollama_music_insights",
    "dual_ai_blender_agent_brief",
    "generated_implementation_notes",
}
MEDIA_SUFFIXES = {
    ".wav",
    ".mp3",
    ".flac",
    ".mp4",
    ".mov",
    ".avi",
    ".mkv",
    ".png",
    ".jpg",
    ".jpeg",
    ".exr",
    ".blend",
    ".blend1",
}


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def rel_to_root(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT.resolve())).replace("\\", "/")


def slugify(value: str, max_len: int = 80) -> str:
    slug = re.sub(r"[^A-Za-z0-9]+", "_", value).strip("_")
    return slug[:max_len] or "chunk"


def should_exclude(path: Path) -> bool:
    rel_parts = path.resolve().relative_to(ROOT.resolve()).parts
    if any(part in EXCLUDE_DIRS or part in EXCLUDE_PARTS for part in rel_parts[:-1]):
        return True

    suffix = path.suffix.lower()
    if suffix in MEDIA_SUFFIXES or suffix not in TEXT_SUFFIXES:
        return True

    stem = path.stem
    if any(stem.startswith(prefix) for prefix in EXCLUDE_FILE_PREFIXES):
        return True

    if path.name.endswith(".pyc") or path.name.endswith(".pyo"):
        return True
    if path.name.startswith("."):
        return True

    return False


def collect_project_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        try:
            path.resolve().relative_to(ROOT.resolve())
        except ValueError:
            continue
        if should_exclude(path):
            continue
        files.append(path.resolve())
    return sorted(files, key=lambda item: rel_to_root(item).lower())


def target_name(target: ast.expr) -> str | None:
    if isinstance(target, ast.Name):
        return target.id
    if isinstance(target, ast.Attribute):
        return target.attr
    return None


def format_syntax_warning(message: warnings.WarningMessage) -> str:
    """Return a compact warning string for manifest/index output."""
    return f"line {message.lineno}: {message.message}"


def extract_symbols(source: str, filename: str = "<unknown>") -> dict:
    symbols = {
        "imports": [],
        "functions": [],
        "classes": [],
        "assignments": [],
        "syntax_warnings": [],
    }
    try:
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always", SyntaxWarning)
            tree = ast.parse(source, filename=filename)
        symbols["syntax_warnings"] = [format_syntax_warning(item) for item in caught]
    except SyntaxError as exc:
        symbols["syntax_error"] = f"{filename}: {exc}"
        return symbols

    for node in tree.body:
        if isinstance(node, ast.Import):
            symbols["imports"].extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            names = ", ".join(alias.name for alias in node.names)
            symbols["imports"].append(f"from {module} import {names}")
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            symbols["functions"].append(
                {
                    "name": node.name,
                    "line": node.lineno,
                    "args": [arg.arg for arg in node.args.args],
                    "async": isinstance(node, ast.AsyncFunctionDef),
                }
            )
        elif isinstance(node, ast.ClassDef):
            methods = []
            for child in node.body:
                if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    methods.append({"name": child.name, "line": child.lineno})
            symbols["classes"].append({"name": node.name, "line": node.lineno, "methods": methods})
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                name = target_name(target)
                if name:
                    symbols["assignments"].append(name)
        elif isinstance(node, ast.AnnAssign):
            name = target_name(node.target)
            if name:
                symbols["assignments"].append(name)

    return symbols


def file_record(path: Path) -> dict:
    source = path.read_text(encoding="utf-8", errors="replace")
    record = {
        "file": rel_to_root(path),
        "suffix": path.suffix.lower(),
        "lines": source.count("\n") + 1 if source else 0,
        "chars": len(source),
        "sha256": sha256_text(source),
    }
    if path.suffix.lower() == ".py":
        record["symbols"] = extract_symbols(source, filename=record["file"])
    return record


def format_symbol_summary(record: dict) -> str:
    symbols = record.get("symbols")
    if not symbols:
        return ""
    lines: list[str] = []
    if symbols.get("syntax_error"):
        lines.append(f"- Syntax error: `{symbols['syntax_error']}`")
    if symbols.get("syntax_warnings"):
        lines.append(
            "- Syntax warnings: "
            + "; ".join(f"`{item}`" for item in symbols["syntax_warnings"][:12])
        )
    if symbols.get("imports"):
        lines.append("- Imports: " + ", ".join(f"`{item}`" for item in symbols["imports"][:24]))
    if symbols.get("classes"):
        bits = []
        for item in symbols["classes"][:20]:
            methods = ", ".join(method["name"] for method in item.get("methods", [])[:10])
            bits.append(
                f"`{item['name']}` line {item['line']}"
                + (f" methods: {methods}" if methods else "")
            )
        lines.append("- Classes: " + "; ".join(bits))
    if symbols.get("functions"):
        bits = []
        for item in symbols["functions"][:44]:
            args = ", ".join(item["args"])
            prefix = "async " if item.get("async") else ""
            bits.append(f"`{prefix}{item['name']}({args})` line {item['line']}")
        lines.append("- Functions: " + "; ".join(bits))
    if symbols.get("assignments"):
        lines.append(
            "- Assignments: " + ", ".join(f"`{name}`" for name in symbols["assignments"][:80])
        )
    return "\n".join(lines)


def numbered_lines(lines: list[str], start_line: int) -> str:
    return "\n".join(f"{line_no:05d}: {line}" for line_no, line in enumerate(lines, start_line))


def split_source(source: str, max_chars: int) -> list[tuple[int, int, list[str]]]:
    lines = source.splitlines()
    if not lines:
        return [(1, 1, [])]
    chunks: list[tuple[int, int, list[str]]] = []
    current: list[str] = []
    current_len = 0
    start_line = 1
    for line_no, line in enumerate(lines, 1):
        cost = len(line) + 9
        if current and current_len + cost > max_chars:
            chunks.append((start_line, line_no - 1, current))
            current = []
            current_len = 0
            start_line = line_no
        current.append(line)
        current_len += cost
    if current:
        chunks.append((start_line, start_line + len(current) - 1, current))
    return chunks


def source_fingerprint(records: list[dict]) -> str:
    payload = json.dumps(
        [{"file": item["file"], "sha256": item["sha256"]} for item in records],
        ensure_ascii=False,
        sort_keys=True,
    )
    return sha256_text(payload)


def existing_cache_valid(fingerprint: str) -> bool:
    if (
        not PROJECT_MANIFEST_JSON.exists()
        or not PROJECT_INDEX_MD.exists()
        or not PROJECT_CHUNK_DIR.exists()
    ):
        return False
    try:
        manifest = json.loads(PROJECT_MANIFEST_JSON.read_text(encoding="utf-8"))
    except Exception:
        return False
    if manifest.get("source_fingerprint") != fingerprint:
        return False
    expected = manifest.get("chunk_count", 0)
    actual = len(list(PROJECT_CHUNK_DIR.glob("chunk_*.md")))
    return expected == actual


def write_readme() -> None:
    README_MD.write_text(
        "\n".join(
            [
                "# indexAI",
                "",
                "Generated AI indexes and patch-library notes for the Spaziotempo Blender project.",
                "",
                "- `project_code_index.md` is the primary project structure library.",
                "- `project_code_manifest.json` contains hashes, symbols and chunk metadata.",
                "- `project_code_chunks/` contains line-numbered source chunks.",
                "- `patch_library/` is reserved for AI patch plans and drafts.",
                "",
                "This folder is excluded from source indexing to avoid recursive AI context loops.",
                "",
            ]
        ),
        encoding="utf-8",
    )


def write_chunks(records: list[dict], max_chunk_chars: int) -> list[dict]:
    PROJECT_CHUNK_DIR.mkdir(parents=True, exist_ok=True)
    for old_chunk in PROJECT_CHUNK_DIR.glob("chunk_*.md"):
        old_chunk.unlink()

    chunks: list[dict] = []
    pending: list[dict] = []
    for record in records:
        path = ROOT / record["file"]
        source = path.read_text(encoding="utf-8", errors="replace")
        for part, (start_line, end_line, lines) in enumerate(
            split_source(source, max_chunk_chars), 1
        ):
            pending.append(
                {
                    "file": record["file"],
                    "suffix": record["suffix"],
                    "part": part,
                    "start_line": start_line,
                    "end_line": end_line,
                    "symbols": format_symbol_summary(record),
                    "text": numbered_lines(lines, start_line),
                }
            )

    total = len(pending)
    for index, item in enumerate(pending, 1):
        chunk_name = f"chunk_{index:04d}_{slugify(item['file'])}.md"
        chunk_path = PROJECT_CHUNK_DIR / chunk_name
        fence = item["suffix"].lstrip(".") or "text"
        body = [
            f"# Project Code Chunk {index}/{total}\n\n",
            f"- File: `{item['file']}`\n",
            f"- Part: `{item['part']}`\n",
            f"- Lines: `{item['start_line']}-{item['end_line']}`\n\n",
        ]
        if item["symbols"]:
            body.extend(["## Symbol Map\n", item["symbols"], "\n\n"])
        body.extend(["## Content\n", f"```{fence}\n", item["text"], "\n```\n"])
        chunk_text = "".join(body)
        chunk_path.write_text(chunk_text, encoding="utf-8")
        chunks.append(
            {
                "index": index,
                "file": item["file"],
                "path": rel_to_root(chunk_path),
                "part": item["part"],
                "start_line": item["start_line"],
                "end_line": item["end_line"],
                "chars": len(chunk_text),
                "sha256": sha256_text(chunk_text),
            }
        )
    return chunks


def write_index(records: list[dict], chunks: list[dict], created_at: str, fingerprint: str) -> None:
    lines: list[str] = []
    lines.append("# Spaziotempo Primary Project Code Index\n\n")
    lines.append(f"Generated: `{created_at}`\n\n")
    lines.append(f"Source fingerprint: `{fingerprint}`\n\n")
    lines.append(
        "Priority: this is the primary library for project structure. AI patches must respect these files before Blender manuals.\n\n"
    )
    lines.append("## Rules For AI Implementers\n")
    lines.append("- Prefer existing files, functions and panel patterns.\n")
    lines.append(
        "- Do not generate monolithic replacement scripts when a targeted patch is possible.\n"
    )
    lines.append(
        "- Full frame-by-frame keyframe JSON files are data inputs and must not be compacted or rewritten.\n"
    )
    lines.append("- `indexAI` is generated context and must not be re-indexed as source.\n\n")
    lines.append("## Files\n")
    for record in records:
        lines.append(
            f"- `{record['file']}`: {record['lines']} lines, {record['chars']} chars, sha256 `{record['sha256']}`\n"
        )
    lines.append("\n## Chunks\n")
    for chunk in chunks:
        lines.append(
            f"- `{chunk['path']}` -> `{chunk['file']}` lines {chunk['start_line']}-{chunk['end_line']}\n"
        )
    PROJECT_INDEX_MD.write_text("".join(lines), encoding="utf-8")


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


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build primary project code index for AI patch planning."
    )
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--max-chunk-chars", type=int, default=DEFAULT_MAX_CHUNK_CHARS)
    args = parser.parse_args()
    build_project_ai_index(force=args.force, max_chunk_chars=args.max_chunk_chars)


if __name__ == "__main__":
    main()
