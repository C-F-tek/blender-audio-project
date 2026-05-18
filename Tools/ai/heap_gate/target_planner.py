"""Runtime target planning for heap gate matrix/lab phases."""

from __future__ import annotations

import re
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

from Tools.ai.runtime_file_refs import RuntimeFileRefResolver
from Tools.ai.runtime_universe.models import RepoRuntimeUniverse

STOPWORDS = {
    "anche",
    "come",
    "cosa",
    "della",
    "degli",
    "delle",
    "deve",
    "devi",
    "file",
    "files",
    "from",
    "have",
    "into",
    "json",
    "nella",
    "nelle",
    "non",
    "output",
    "path",
    "report",
    "root",
    "sono",
    "source",
    "target",
    "task",
    "that",
    "this",
    "tool",
    "tutti",
    "with",
}


@dataclass(frozen=True)
class TargetPlanItem:
    path: str
    score: int
    reasons: tuple[str, ...]


def request_focus_text(text: str) -> str:
    """Keep current operator intent before appended historical revision context."""
    markers = (
        "EXTERNAL HEAP REVISION CONTEXT",
        "HEAP CHUNK/COMPOSER CONTRACT",
    )
    focused = str(text or "")
    for marker in markers:
        if marker in focused:
            focused = focused.split(marker, 1)[0]
    return focused


def tokenize(text: str) -> set[str]:
    return {
        item
        for item in re.split(r"[^a-z0-9]+", str(text or "").lower().replace("_", " "))
        if len(item) >= 4 and item not in STOPWORDS
    }


def path_tokens(path: str) -> set[str]:
    return tokenize(Path(path).stem) | tokenize(path.replace("/", " "))


class RuntimeTargetPlanner:
    """Select patchable source targets from the live repo universe."""

    def __init__(self, repo_root: str | Path, universe: RepoRuntimeUniverse):
        self.repo_root = Path(repo_root).resolve()
        self.universe = universe
        self.resolver = RuntimeFileRefResolver(self.repo_root)

    def _read_preview(self, rel_path: str, max_chars: int = 8000) -> str:
        try:
            return (self.repo_root / rel_path).read_text(encoding="utf-8-sig", errors="replace")[
                :max_chars
            ]
        except OSError:
            return ""

    def plan(
        self,
        *,
        request_text: str,
        explicit_candidates: Iterable[str] = (),
        limit: int = 32,
    ) -> list[TargetPlanItem]:
        terms = tokenize(request_focus_text(request_text))
        explicit = {str(item).replace("\\", "/") for item in explicit_candidates if item}
        scored: list[TargetPlanItem] = []
        for rel_path in self.universe.source_index:
            ref = self.resolver.resolve(rel_path)
            if not ref.patchable:
                continue
            score = 0
            reasons: list[str] = []
            token_hits = terms & path_tokens(rel_path)
            if token_hits:
                score += 14 * len(token_hits)
                reasons.append("path_terms:" + ",".join(sorted(token_hits)[:8]))
            preview = self._read_preview(rel_path).lower()
            content_hits = {term for term in terms if term in preview}
            if content_hits:
                score += min(18, 2 * len(content_hits))
                reasons.append("content_terms:" + ",".join(sorted(content_hits)[:8]))
            suffix = Path(rel_path).suffix.lower()
            if suffix in {".py", ".ps1"}:
                score += 6
                reasons.append("executable_source")
            elif suffix in {".json", ".toml", ".yml", ".yaml"}:
                score -= 6
                reasons.append("config_source_lower_priority")
            if rel_path in explicit and (token_hits or content_hits):
                score += 4
                reasons.append("explicit_current_context")
            if score > 0:
                scored.append(TargetPlanItem(rel_path, score, tuple(reasons)))
        scored.sort(key=lambda item: (-item.score, item.path))
        return scored[: max(1, int(limit))]
