"""Repository file tools for the Ollama gateway."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .common import GatewayConfig, TEXT_EXTENSIONS, compact_text, is_under, path_policy_error, repo_rel, resolve_repo_path

def read_text_file(config: GatewayConfig, raw_path: str) -> dict[str, Any]:
    rel_input = raw_path.replace("\\", "/").strip()
    error = path_policy_error(rel_input, allow_output_read=config.allow_output_read)
    path = resolve_repo_path(config.repo_root, rel_input)
    if error:
        return {"passed": False, "path": rel_input, "error": error}
    if not is_under(path, config.repo_root):
        return {"passed": False, "path": rel_input, "error": "path escapes repo root"}
    if not path.is_file():
        return {
            "passed": False,
            "path": rel_input,
            "error": "file missing or not a file",
        }
    if path.suffix.lower() not in TEXT_EXTENSIONS:
        return {
            "passed": False,
            "path": repo_rel(path, config.repo_root),
            "error": "extension not allowed",
        }
    try:
        text = path.read_text(encoding="utf-8-sig", errors="replace")
    except OSError as exc:
        return {
            "passed": False,
            "path": repo_rel(path, config.repo_root),
            "error": f"{type(exc).__name__}: {exc}",
        }
    preview, truncated = compact_text(text, config.max_file_chars)
    return {
        "passed": True,
        "path": repo_rel(path, config.repo_root),
        "chars": len(text),
        "lines": len(text.splitlines()),
        "truncated": truncated,
        "content": preview,
    }

def iter_candidate_files(config: GatewayConfig, roots: list[str]) -> list[Path]:
    found: list[Path] = []
    seen: set[Path] = set()
    selected_roots = roots or [
        "docs",
        "ia_carmine",
        "Tools/validation",
        "Tools/workflow",
        "AGENTS.md",
        "README.md",
    ]
    for raw_root in selected_roots:
        root_rel = raw_root.replace("\\", "/").strip()
        if path_policy_error(root_rel, allow_output_read=config.allow_output_read):
            continue
        root = resolve_repo_path(config.repo_root, root_rel)
        if not is_under(root, config.repo_root) or not root.exists():
            continue
        candidates = [root] if root.is_file() else sorted(p for p in root.rglob("*") if p.is_file())
        for path in candidates:
            rel = repo_rel(path, config.repo_root)
            if path in seen:
                continue
            if path.suffix.lower() not in TEXT_EXTENSIONS:
                continue
            if path_policy_error(rel, allow_output_read=config.allow_output_read):
                continue
            seen.add(path)
            found.append(path)
    return found

def file_search(config: GatewayConfig, query: str, roots: list[str]) -> dict[str, Any]:
    terms = [item.lower() for item in query.split() if item.strip()]
    if not terms:
        return {"passed": False, "error": "query is required", "results": []}
    results: list[dict[str, Any]] = []
    for path in iter_candidate_files(config, roots):
        rel = repo_rel(path, config.repo_root)
        haystack = rel.lower()
        try:
            text = path.read_text(encoding="utf-8-sig", errors="replace")
        except OSError:
            continue
        body = text.lower()
        score = sum(3 for term in terms if term in haystack) + sum(
            1 for term in terms if term in body
        )
        if score <= 0:
            continue
        first_line = ""
        for line in text.splitlines():
            if any(term in line.lower() for term in terms):
                first_line = line.strip()[:240]
                break
        results.append(
            {
                "path": rel,
                "score": score,
                "lines": len(text.splitlines()),
                "match_preview": first_line,
            }
        )
    results.sort(key=lambda item: (-int(item["score"]), str(item["path"])))
    return {
        "passed": True,
        "query": query,
        "results": results[: config.max_search_results],
        "result_count": len(results),
    }
