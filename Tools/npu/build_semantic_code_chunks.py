#!/usr/bin/env python3
"""Generate semantic code chunks for AI context without modifying source files."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

EXCLUDE = {".git", "__pycache__", ".venv", "venv", "indexAI", "output", "outputs", "renders"}
RISK = {
    "ShaderNodeTexMusgrave": "blocked_blender_node",
    "shutil.rmtree": "recursive_delete",
    "os.remove": "file_delete",
    "bpy.ops.object.delete": "scene_delete",
    "subprocess.": "external_process",
    "nodes.new": "shader_node_creation",
    "bpy.ops": "operator_side_effect",
}
DOMAINS = {
    "audio": ("audio", "wav", "beat", "bpm", "onset"),
    "materials": ("material", "shader", "node", "texture"),
    "lighting": ("light", "emission"),
    "camera": ("camera", "lens"),
    "render": ("render", "ffmpeg", "codec", "frame", "cycles", "eevee"),
    "physics": ("physics", "rigid", "gravity", "orbit"),
    "fog": ("fog", "volume", "atmosphere"),
    "config": ("config", "path", "setting"),
    "ai_context": ("ai", "npu", "gpu", "chunk", "context"),
    "validation": ("validate", "schema", "quality", "check"),
}


def sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", "replace")).hexdigest()


def excluded(path: Path, root: Path) -> bool:
    return bool(set(path.relative_to(root).parts) & EXCLUDE)


def py_files(root: Path, sources: list[str]):
    out = []
    for item in sources:
        start = (root / item).resolve()
        if not start.exists():
            continue
        candidates = [start] if start.is_file() else list(start.rglob("*.py"))
        out += [p for p in candidates if p.suffix == ".py" and not excluded(p, root)]
    return sorted(set(out))


def deps(node):
    found = set()
    for child in ast.walk(node):
        if isinstance(child, ast.Name):
            found.add(child.id)
        elif isinstance(child, ast.Attribute):
            found.add(child.attr)
    return sorted(x for x in found if not x.startswith("__"))[:80]


def domain_tags(path: str, symbol: str, code: str):
    hay = f"{path} {symbol} {code[:3000]}".lower()
    tags = [name for name, toks in DOMAINS.items() if any(t in hay for t in toks)]
    return tags or ["general"]


def api_refs(code: str):
    refs = set(re.findall(r"\bbpy(?:\.[A-Za-z_][A-Za-z0-9_]*){1,4}", code))
    refs.update(re.findall(r"ShaderNode[A-Za-z0-9_]+", code))
    if "nodes.new" in code:
        refs.add("nodes.new")
    if "keyframe_insert" in code:
        refs.add("keyframe_insert")
    return sorted(refs)[:60]


def risk(code: str):
    signals = sorted({v for k, v in RISK.items() if k in code})
    if {"blocked_blender_node", "recursive_delete", "file_delete"} & set(signals):
        return "high", signals
    if signals:
        return "medium", signals
    return "low", signals


def chunks(path: Path, root: Path):
    text = path.read_text(encoding="utf-8", errors="replace")
    rel = path.relative_to(root).as_posix()
    lines = text.splitlines()
    try:
        tree = ast.parse(text)
    except SyntaxError as exc:
        return [], {"path": rel, "status": "syntax_error", "error": str(exc)}
    nodes = [
        n
        for n in ast.iter_child_nodes(tree)
        if isinstance(n, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef))
    ] or [tree]
    result = []
    for node in nodes:
        symbol = getattr(node, "name", "<module>")
        kind = (
            "class"
            if isinstance(node, ast.ClassDef)
            else "function"
            if hasattr(node, "name")
            else "module"
        )
        start = int(getattr(node, "lineno", 1))
        end = int(getattr(node, "end_lineno", len(lines)))
        code = "\n".join(lines[start - 1 : end]) if kind != "module" else text
        r, sig = risk(code)
        doc = (
            ast.get_docstring(node)
            if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef))
            else None
        )
        result.append(
            {
                "chunk_id": f"{rel}::{symbol}",
                "path": rel,
                "symbol": symbol,
                "kind": kind,
                "line_start": start,
                "line_end": end if kind != "module" else len(lines),
                "domain": domain_tags(rel, symbol, code),
                "blender_api": api_refs(code),
                "risk": r,
                "risk_signals": sig,
                "compatibility_notes": ["Blender 5.x: ShaderNodeTexMusgrave is blocked"]
                if "ShaderNodeTexMusgrave" in code
                else [],
                "dependencies": deps(node),
                "sha256": sha(code),
                "summary_short": (
                    " ".join(doc.split())[:180] if doc else f"{kind} {symbol} in {rel}"
                ),
                "do_not_change": rel.startswith("Scripting/v61b/"),
            }
        )
    return result, {
        "path": rel,
        "status": "ok",
        "chunks": len(result),
        "lines": len(lines),
        "sha256": sha(text),
    }


def write(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("--source-dir", action="append", default=[])
    ap.add_argument("--output", default="indexAI/code_chunks/semantic_code_chunks.json")
    ap.add_argument("--manifest", default="indexAI/code_chunks/semantic_code_chunks_manifest.json")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    root = Path(args.repo_root).resolve()
    sources = args.source_dir or ["Scripting", "Tools", "."]
    all_chunks, files = [], []
    for path in py_files(root, sources):
        c, info = chunks(path, root)
        all_chunks += c
        files.append(info)
    now = datetime.now(timezone.utc).isoformat()
    payload = {
        "schema_version": 1,
        "generated_at": now,
        "chunk_count": len(all_chunks),
        "chunks": all_chunks,
    }
    manifest = {
        "schema_version": 1,
        "generated_at": now,
        "source_dirs": sources,
        "files_scanned": len(files),
        "chunk_count": len(all_chunks),
        "files": files,
    }
    if not args.dry_run:
        write(root / args.output, payload)
        write(root / args.manifest, manifest)
    print(json.dumps(manifest, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
