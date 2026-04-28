#!/usr/bin/env python3
"""
Generate AI-friendly semantic code chunks.

Safe behavior:
- reads Python source files;
- writes generated JSON under indexAI/code_chunks/;
- never modifies Scripting/ or raw analysis files.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

EXCLUDE_DIRS = {".git", "__pycache__", ".venv", "venv", "indexAI", "output", "outputs", "renders"}
DOMAIN_RULES = {
    "audio": ("audio", "wav", "beat", "bpm", "onset", "spectrum"),
    "materials": ("material", "shader", "node", "texture", "color"),
    "lighting": ("light", "emission", "glow"),
    "camera": ("camera", "lens", "dof"),
    "render": ("render", "ffmpeg", "codec", "frame", "cycles", "eevee"),
    "physics": ("physics", "rigid", "gravity", "orbit", "collision"),
    "fog": ("fog", "volume", "atmosphere"),
    "config": ("config", "path", "setting", "profile"),
    "ai_context": ("ai", "npu", "gpu", "chunk", "context", "prompt"),
    "validation": ("validate", "schema", "quality", "check", "lint"),
}
BLOCKED = {"ShaderNodeTexMusgrave": "Blender 5.x compatibility risk: use Noise/Voronoi/ColorRamp alternatives."}
RISK_PATTERNS = {
    "ShaderNodeTexMusgrave": "blocked_blender_node",
    "shutil.rmtree": "recursive_delete",
    "os.remove": "file_delete",
    "bpy.ops.object.delete": "scene_delete",
    "subprocess.": "external_process",
    "C:\\\\Users\\\\": "hardcoded_windows_user_path",
    "nodes.new": "shader_node_creation",
    "bpy.ops": "operator_side_effect",
}


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", "replace")).hexdigest()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def is_excluded(path: Path, repo_root: Path) -> bool:
    try:
        parts = set(path.relative_to(repo_root).parts)
    except ValueError:
        return True
    return bool(parts & EXCLUDE_DIRS)


def iter_python_files(repo_root: Path, source_dirs: list[str]) -> list[Path]:
    files: list[Path] = []
    for item in source_dirs:
        start = (repo_root / item).resolve()
        if not start.exists():
            continue
        candidates = [start] if start.is_file() else list(start.rglob("*.py"))
        for path in candidates:
            if path.suffix == ".py" and not is_excluded(path, repo_root):
                files.append(path)
    return sorted(set(files))


def line_end(node: ast.AST) -> int:
    return int(getattr(node, "end_lineno", getattr(node, "lineno", 1)))


def segment(lines: list[str], start: int, end: int) -> str:
    return "\n".join(lines[max(start - 1, 0): min(end, len(lines))])


def imports(tree: ast.AST) -> list[str]:
    found: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            found.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            found.add(node.module.split(".")[0])
    return sorted(found)


def dependencies(node: ast.AST) -> list[str]:
    found: set[str] = set()
    for child in ast.walk(node):
        if isinstance(child, ast.Name):
            found.add(child.id)
        elif isinstance(child, ast.Attribute):
            found.add(child.attr)
    return sorted(name for name in found if not name.startswith("__"))[:80]


def domains(path: str, symbol: str, code: str) -> list[str]:
    haystack = f"{path} {symbol} {code[:4000]}".lower()
    result = [name for name, tokens in DOMAIN_RULES.items() if any(token in haystack for token in tokens)]
    return result or ["general"]


def blender_api(code: str) -> list[str]:
    found = set(re.findall(r"\bbpy(?:\.[A-Za-z_][A-Za-z0-9_]*){1,4}", code))
    found.update(re.findall(r"ShaderNode[A-Za-z0-9_]+", code))
    if "nodes.new" in code:
        found.add("nodes.new")
    if "keyframe_insert" in code:
        found.add("keyframe_insert")
    return sorted(found)[:60]


def risk(code: str) -> tuple[str, list[str]]:
    signals = sorted({label for pattern, label in RISK_PATTERNS.items() if pattern in code})
    if {"blocked_blender_node", "recursive_delete", "file_delete"} & set(signals):
        return "high", signals
    if {"operator_side_effect", "shader_node_creation", "external_process", "scene_delete"} & set(signals):
        return "medium", signals
    return "low", signals


def compatibility(code: str) -> list[str]:
    return [note for pattern, note in BLOCKED.items() if pattern in code]


def summarize(node: ast.AST, fallback: str) -> tuple[str, str]:
    doc = ast.get_docstring(node) if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)) else None
    text = " ".join(doc.split()) if doc else fallback
    return text[:180], text[:700]


def chunks_for_file(path: Path, repo_root: Path) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    text = read_text(path)
    rel = path.relative_to(repo_root).as_posix()
    lines = text.splitlines()
    try:
        tree = ast.parse(text)
    except SyntaxError as exc:
        return [], {"path": rel, "status": "syntax_error", "error": f"{exc.msg} at line {exc.lineno}"}

    module_imports = imports(tree)
    nodes = [n for n in ast.iter_child_nodes(tree) if isinstance(n, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef))]
    if not nodes:
        nodes = [tree]

    chunks = []
    for node in nodes:
        symbol = getattr(node, "name", "<module>")
        kind = "class" if isinstance(node, ast.ClassDef) else "function" if hasattr(node, "name") else "module"
        start = int(getattr(node, "lineno", 1))
        end = line_end(node)
        code = segment(lines, start, end) if kind != "module" else text
        risk_level, risk_signals = risk(code)
        summary_short, summary_for_ai = summarize(node, f"{kind} {symbol} in {rel}")
        chunks.append({
            "chunk_id": f"{rel}::{symbol}",
            "path": rel,
            "symbol": symbol,
            "kind": kind,
            "line_start": start,
            "line_end": end if kind != "module" else max(len(lines), 1),
            "domain": domains(rel, symbol, code),
            "blender_api": blender_api(code),
            "risk": risk_level,
            "risk_signals": risk_signals,
            "compatibility_notes": compatibility(code),
            "dependencies": dependencies(node),
            "imports": module_imports,
            "sha256": sha256_text(code),
            "summary_short": summary_short,
            "summary_for_ai": summary_for_ai,
            "do_not_change": rel.startswith("Scripting/v61b/"),
        })

    return chunks, {"path": rel, "status": "ok", "chunks": len(chunks), "lines": len(lines), "sha256": sha256_text(text)}


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--source-dir", action="append", default=[])
    parser.add_argument("--output", default="indexAI/code_chunks/semantic_code_chunks.json")
    parser.add_argument("--manifest", default="indexAI/code_chunks/semantic_code_chunks_manifest.json")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    source_dirs = args.source_dir or ["Scripting", "Tools", "."]
    chunks: list[dict[str, Any]] = []
    files: list[dict[str, Any]] = []

    for path in iter_python_files(repo_root, source_dirs):
        file_chunks, file_info = chunks_for_file(path, repo_root)
        chunks.extend(file_chunks)
        files.append(file_info)

    now = datetime.now(timezone.utc).isoformat()
    payload = {"schema_version": 1, "generated_at": now, "chunk_count": len(chunks), "chunks": chunks}
    manifest = {
        "schema_version": 1,
        "generated_at": now,
        "source_dirs": source_dirs,
        "files_scanned": len(files),
        "chunk_count": len(chunks),
        "files": files,
    }

    if not args.dry_run:
        write_json(repo_root / args.output, payload)
        write_json(repo_root / args.manifest, manifest)
    print(json.dumps(manifest, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
