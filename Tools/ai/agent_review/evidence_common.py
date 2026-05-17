"""Shared helpers for agent-review evidence sufficiency."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from tools.ai.code_patch_plan_common import read_json_object

DEFAULT_REFINED_REVIEW = "output/ai_pipeline/local_ai_core_tool_activation_megalithic_refined_review.json"
DEFAULT_REFINED_PROPOSALS = "output/ai_pipeline/local_ai_core_tool_activation_megalithic_refined_proposals.json"
DEFAULT_OUTPUT = "output/ai_pipeline/agent_review_evidence_sufficiency.json"
DEFAULT_MARKDOWN = "output/ai_pipeline/agent_review_evidence_sufficiency.md"
MAX_SNIPPET_CHARS = 1600

class EvidenceFile:
    """A repository file inspected as evidence."""

    path: str
    exists: bool
    kind: str
    chars: int = 0
    lines: int = 0
    matched_terms: tuple[str, ...] = ()
    snippet: str = ""

def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")

def resolve_path(repo_root: Path, value: str) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = repo_root / path
    return path.resolve()

def repo_rel(path: Path, repo_root: Path) -> str:
    try:
        return path.resolve(strict=False).relative_to(repo_root.resolve(strict=False)).as_posix()
    except ValueError:
        return str(path)

def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")

def load_json_object(path: Path) -> dict[str, Any]:
    data, errors = read_json_object(path)
    if errors:
        raise ValueError(f"{path}: {'; '.join(errors)}")
    return data

def compact_snippet(text: str, terms: list[str], *, max_chars: int = MAX_SNIPPET_CHARS) -> str:
    """Return a compact snippet around the first matching term."""
    if not text:
        return ""
    lower = text.lower()
    positions = [
        lower.find(term.lower()) for term in terms if term and lower.find(term.lower()) >= 0
    ]
    if positions:
        start = max(0, min(positions) - max_chars / 3)
    else:
        start = 0
    snippet = text[start : start + max_chars]
    return snippet.replace("\r\n", "\n")

def inspect_file(
    repo_root: Path,
    value: str,
    *,
    terms: list[str] | None = None,
    kind: str = "evidence",
) -> EvidenceFile:
    terms = terms or []
    path = resolve_path(repo_root, value)
    if not path.exists() or not path.is_file():
        return EvidenceFile(path=repo_rel(path, repo_root), exists=False, kind=kind)
    text = read_text(path)
    matched = tuple(term for term in terms if term and term.lower() in text.lower())
    return EvidenceFile(
        path=repo_rel(path, repo_root),
        exists=True,
        kind=kind,
        chars=len(text),
        lines=len(text.splitlines()),
        matched_terms=matched,
        snippet=compact_snippet(text, list(matched or terms)),
    )

def evidence_to_dict(item: EvidenceFile) -> dict[str, Any]:
    return {
        "path": item.path,
        "exists": item.exists,
        "kind": item.kind,
        "chars": item.chars,
        "lines": item.lines,
        "matched_terms": list(item.matched_terms),
        "snippet": item.snippet,
    }

def load_optional_report(repo_root: Path, value: str) -> dict[str, Any]:
    path = resolve_path(repo_root, value)
    out: dict[str, Any] = {
        "path": repo_rel(path, repo_root),
        "exists": path.exists(),
        "kind": None,
        "passed": None,
        "error": "",
    }
    if not path.exists():
        out["error"] = "missing"
        return out
    data, errors = read_json_object(path)
    if errors:
        out["error"] = "; ".join(errors)
        return out
    out["kind"] = data.get("kind")
    out["passed"] = data.get("passed")
    out["summary"] = data.get("summary") if isinstance(data.get("summary"), dict) else {}
    return out
