"""File records and source fingerprints for the project AI index."""

from __future__ import annotations

import json
from pathlib import Path

from .config import PROJECT_CHUNK_DIR, PROJECT_INDEX_MD, PROJECT_MANIFEST_JSON, ROOT
from .paths import rel_to_root, sha256_text
from .symbols import extract_symbols

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
