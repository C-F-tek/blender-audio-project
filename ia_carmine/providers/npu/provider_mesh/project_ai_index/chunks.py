"""Chunk writing for the project AI index."""

from __future__ import annotations

from .config import PROJECT_CHUNK_DIR, README_MD, ROOT
from .paths import rel_to_root, sha256_text, slugify
from .records import format_symbol_summary

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
