from __future__ import annotations

from pathlib import Path
import ast
import hashlib
import json
import re
from datetime import datetime


ROOT = Path(__file__).resolve().parents[2]
SCRIPT_DIR = ROOT / "Scripting" / "v61b"
OUT_DIR = ROOT / "Tools" / "npu"
OUT_MD = OUT_DIR / "npu_code_context.md"
OUT_INDEX_MD = OUT_DIR / "npu_code_index.md"
OUT_JSON = OUT_DIR / "npu_code_manifest.json"
CHUNK_DIR = OUT_DIR / "npu_code_chunks"

MAX_CHUNK_CHARS = 10500

PRIORITY_FILES = [
    ROOT / "analyze_wav.py",
    ROOT / "build_track_summary.py",
    ROOT / "normalize_scene_spec.py",
    OUT_DIR / "npu_runtime.py",
    OUT_DIR / "ollama_runtime.py",
    OUT_DIR / "build_blender_manual_context.py",
    OUT_DIR / "run_dual_ai_pipeline.py",
    SCRIPT_DIR / "config.py",
    SCRIPT_DIR / "main_v61b.py",
    SCRIPT_DIR / "animation.py",
    SCRIPT_DIR / "materials.py",
    SCRIPT_DIR / "physics_setup.py",
    SCRIPT_DIR / "fog_dynamics.py",
    SCRIPT_DIR / "fog_filaments.py",
    SCRIPT_DIR / "atmosphere_setup.py",
    SCRIPT_DIR / "world_setup.py",
    SCRIPT_DIR / "render_setup.py",
    SCRIPT_DIR / "scene_tuning_panel.py",
    SCRIPT_DIR / "hot_update_scene_v61b.py",
    SCRIPT_DIR / "encode_image_sequence_v61b.py",
    SCRIPT_DIR / "encode_ffmpeg_v61b.py",
    SCRIPT_DIR / "PROJECT_STRUCTURE.md",
    SCRIPT_DIR / "SCENE_TUNING_GUIDE.md",
]

DISCOVERY_GLOBS = [
    (SCRIPT_DIR, ["*.py", "*.md", "hotpatch/*.py", "spaziotempo/**/*.py"]),
    (OUT_DIR, ["*.py", "*.ps1"]),
]

EXCLUDE_PARTS = {"__pycache__", ".npucache", "npu_code_chunks"}
TEXT_SUFFIXES = {".py", ".md", ".ps1", ".json", ".txt"}


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()


def rel_to_root(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def slugify(value: str, max_len: int = 64) -> str:
    slug = re.sub(r"[^A-Za-z0-9]+", "_", value).strip("_")
    return slug[:max_len] or "chunk"


def is_usable_text_file(path: Path) -> bool:
    if path.suffix.lower() not in TEXT_SUFFIXES:
        return False
    return not any(part in EXCLUDE_PARTS for part in path.parts)


def collect_files() -> list[Path]:
    seen: set[Path] = set()
    ordered: list[Path] = []

    def add(path: Path) -> None:
        resolved = path.resolve()
        if resolved in seen or not resolved.exists() or not resolved.is_file():
            return
        if not is_usable_text_file(resolved):
            return
        seen.add(resolved)
        ordered.append(resolved)

    for path in PRIORITY_FILES:
        add(path)

    for base, patterns in DISCOVERY_GLOBS:
        for pattern in patterns:
            for path in sorted(base.glob(pattern), key=lambda item: rel_to_root(item.resolve()).lower()):
                add(path)

    return ordered


def target_name(target: ast.expr) -> str | None:
    if isinstance(target, ast.Name):
        return target.id
    if isinstance(target, ast.Attribute):
        return target.attr
    return None


def extract_symbols(source: str) -> dict:
    symbols = {
        "imports": [],
        "functions": [],
        "classes": [],
        "assignments": [],
    }

    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        symbols["syntax_error"] = str(exc)
        return symbols

    for node in tree.body:
        if isinstance(node, ast.Import):
            for alias in node.names:
                symbols["imports"].append(alias.name)

        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            names = ", ".join(alias.name for alias in node.names)
            symbols["imports"].append(f"from {module} import {names}")

        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            args = [arg.arg for arg in node.args.args]
            symbols["functions"].append(
                {
                    "name": node.name,
                    "line": node.lineno,
                    "args": args,
                    "async": isinstance(node, ast.AsyncFunctionDef),
                }
            )

        elif isinstance(node, ast.ClassDef):
            methods = []
            for child in node.body:
                if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    methods.append({"name": child.name, "line": child.lineno})
            symbols["classes"].append(
                {
                    "name": node.name,
                    "line": node.lineno,
                    "methods": methods,
                }
            )

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


def file_record(path: Path, source: str) -> dict:
    suffix = path.suffix.lower()
    record = {
        "file": rel_to_root(path),
        "exists": True,
        "suffix": suffix,
        "lines": source.count("\n") + 1 if source else 0,
        "chars": len(source),
        "sha256": sha256_text(source),
    }
    if suffix == ".py":
        record["symbols"] = extract_symbols(source)
    return record


def format_symbol_summary(record: dict) -> str:
    symbols = record.get("symbols")
    if not symbols:
        return ""

    lines: list[str] = []

    if symbols.get("syntax_error"):
        lines.append(f"- Syntax error: `{symbols['syntax_error']}`")

    imports = symbols.get("imports", [])
    if imports:
        lines.append("- Imports: " + ", ".join(f"`{item}`" for item in imports[:24]))

    classes = symbols.get("classes", [])
    if classes:
        class_bits = []
        for item in classes[:20]:
            method_names = ", ".join(method["name"] for method in item.get("methods", [])[:10])
            if method_names:
                class_bits.append(f"`{item['name']}` line {item['line']} methods: {method_names}")
            else:
                class_bits.append(f"`{item['name']}` line {item['line']}")
        lines.append("- Classes: " + "; ".join(class_bits))

    functions = symbols.get("functions", [])
    if functions:
        function_bits = []
        for item in functions[:36]:
            args = ", ".join(item["args"])
            prefix = "async " if item.get("async") else ""
            function_bits.append(f"`{prefix}{item['name']}({args})` line {item['line']}")
        lines.append("- Functions: " + "; ".join(function_bits))

    assignments = symbols.get("assignments", [])
    if assignments:
        lines.append("- Assignments: " + ", ".join(f"`{name}`" for name in assignments[:80]))

    return "\n".join(lines)


def numbered_lines(lines: list[str], start_line: int) -> str:
    return "\n".join(f"{line_no:05d}: {line}" for line_no, line in enumerate(lines, start_line))


def split_source(source: str, max_chars: int) -> list[tuple[int, int, list[str]]]:
    source_lines = source.splitlines()
    if not source_lines:
        return [(1, 1, [])]

    chunks: list[tuple[int, int, list[str]]] = []
    current: list[str] = []
    current_len = 0
    start_line = 1

    for line_no, line in enumerate(source_lines, 1):
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


def write_context_chunks(files: list[dict], sources: dict[str, str]) -> list[dict]:
    CHUNK_DIR.mkdir(parents=True, exist_ok=True)

    for old_chunk in CHUNK_DIR.glob("chunk_*.md"):
        old_chunk.unlink()

    pending: list[dict] = []

    for record in files:
        rel_file = record["file"]
        source = sources[rel_file]
        for part_index, (start_line, end_line, lines) in enumerate(split_source(source, MAX_CHUNK_CHARS), 1):
            pending.append(
                {
                    "file": rel_file,
                    "part": part_index,
                    "start_line": start_line,
                    "end_line": end_line,
                    "text": numbered_lines(lines, start_line),
                    "symbols": format_symbol_summary(record),
                    "suffix": record.get("suffix", ""),
                }
            )

    total = len(pending)
    chunks: list[dict] = []

    for index, item in enumerate(pending, 1):
        rel_file = item["file"]
        path_slug = slugify(rel_file)
        chunk_name = f"chunk_{index:03d}_{path_slug}.md"
        chunk_path = CHUNK_DIR / chunk_name
        fence = item["suffix"].lstrip(".") or "text"

        body = [
            f"# NPU Long Context Chunk {index}/{total}\n\n",
            f"- File: `{rel_file}`\n",
            f"- Part: `{item['part']}`\n",
            f"- Lines: `{item['start_line']}-{item['end_line']}`\n\n",
        ]

        if item["symbols"]:
            body.append("## Symbol Map\n")
            body.append(item["symbols"])
            body.append("\n\n")

        body.append("## Content\n")
        body.append(f"```{fence}\n")
        body.append(item["text"])
        body.append("\n```\n")

        chunk_text = "".join(body)
        chunk_path.write_text(chunk_text, encoding="utf-8")

        chunks.append(
            {
                "index": index,
                "file": rel_file,
                "path": rel_to_root(chunk_path),
                "part": item["part"],
                "start_line": item["start_line"],
                "end_line": item["end_line"],
                "chars": len(chunk_text),
                "sha256": sha256_text(chunk_text),
            }
        )

    return chunks


def write_index(files: list[dict], chunks: list[dict], created_at: str) -> None:
    md: list[str] = []
    md.append("# NPU Code Index\n\n")
    md.append(f"Generated: `{created_at}`\n\n")
    md.append("Purpose: long-context index for the local NPU musical/technical agent.\n")
    md.append("Use `npu_code_chunks/chunk_*.md` for full file context.\n\n")

    md.append("## Files\n")
    for record in files:
        md.append(
            f"- `{record['file']}`: {record['lines']} lines, {record['chars']} chars, sha256 `{record['sha256']}`\n"
        )

    md.append("\n## Chunks\n")
    for chunk in chunks:
        md.append(
            f"- `{chunk['path']}` -> `{chunk['file']}` lines {chunk['start_line']}-{chunk['end_line']}\n"
        )

    OUT_INDEX_MD.write_text("".join(md), encoding="utf-8")
    OUT_MD.write_text("".join(md), encoding="utf-8")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    created_at = datetime.now().isoformat(timespec="seconds")
    paths = collect_files()
    sources: dict[str, str] = {}
    files: list[dict] = []

    for path in paths:
        source = path.read_text(encoding="utf-8", errors="replace")
        record = file_record(path, source)
        sources[record["file"]] = source
        files.append(record)

    chunks = write_context_chunks(files, sources)
    write_index(files, chunks, created_at)

    manifest = {
        "created_at": created_at,
        "root": str(ROOT),
        "script_dir": str(SCRIPT_DIR),
        "long_context": {
            "mode": "file_line_chunks",
            "chunk_dir": rel_to_root(CHUNK_DIR),
            "max_chunk_chars": MAX_CHUNK_CHARS,
            "chunk_count": len(chunks),
            "index": rel_to_root(OUT_INDEX_MD),
        },
        "files": files,
        "chunks": chunks,
    }

    OUT_JSON.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"[OK] Wrote: {OUT_MD}")
    print(f"[OK] Wrote: {OUT_INDEX_MD}")
    print(f"[OK] Wrote: {OUT_JSON}")
    print(f"[OK] Wrote chunks: {CHUNK_DIR} ({len(chunks)} files)")


if __name__ == "__main__":
    main()
