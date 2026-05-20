"""Runtime target planning for heap gate matrix/lab phases."""

from __future__ import annotations

import re
import subprocess
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

from Tools.ai.runtime_tool.file_refs import RuntimeFileRefResolver
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

DOCUMENTATION_PREFIXES = ("docs/", "CHATGPT/")
VALIDATION_PREFIXES = ("Tools/validation/", "tools/validation/")
PRODUCT_RUNTIME_PREFIXES = (
    "Tools/ai/_shared/",
    "Tools/ai/agent_memory/",
    "Tools/ai/code_product/",
    "Tools/ai/external_heap/",
    "Tools/ai/heap_context_closure/",
    "Tools/ai/heap_gate/",
    "Tools/ai/heap_runtime/",
    "Tools/ai/operator_product_core/",
    "Tools/ai/patch_product/",
    "Tools/ai/provider_runtime_blackboard/",
    "Tools/ai/run/",
    "Tools/ai/runtime_sqlite_memory/",
    "Tools/ai/runtime_tool/",
    "Tools/workflow/",
)
PRODUCT_RUNTIME_PATHS = {
    "Tools/ai/run/cli.py",
    "Tools/ai/operator_product_core/runner.py",
    "Tools/ai/operator_product_core/controller.py",
}
DOC_INTENT_HINTS = (
    "aggiorna documentazione",
    "aggiorna docs",
    "edit readme",
    "modifica documentazione",
    "modifica docs",
    "scrivi markdown",
    "update docs",
    "update readme",
)
VALIDATION_INTENT_HINTS = (
    "correggi smoke",
    "fix smoke",
    "modifica validator",
    "smoke script",
    "test script",
    "tools/validation",
    "validation script",
    "validation/",
    "validator module",
)
PRODUCT_RUN_HINTS = (
    "broker",
    "code product",
    "code_product_full_patch",
    "heap",
    "lab",
    "matrix",
    "memoria",
    "memory",
    "pointer",
    "provider",
    "run unica",
    "runtime",
    "sqlite",
    "tool call",
    "universo",
)
IMPLEMENTATION_HINTS = (
    "codice",
    "diff",
    "implement",
    "patch",
    "proposte concrete",
    "target_files",
)
PACKAGE_FOCUS_HINTS = (
    (
        (
            "runtime_file_refs",
            "runtime file refs",
            "file reference",
            "file references",
            "target resolution",
            "source anchoring",
        ),
        (
            "Tools/ai/runtime_tool/file_refs/",
            "Tools/ai/_shared/heap_source_anchors.py",
        ),
    ),
)


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


def normalized_repo_path(path: str) -> str:
    return str(path or "").replace("\\", "/")


def has_any_hint(text: str, hints: tuple[str, ...]) -> bool:
    lowered = str(text or "").lower()
    return any(hint in lowered for hint in hints)


def has_product_run_intent(text: str) -> bool:
    return has_any_hint(text, PRODUCT_RUN_HINTS) or has_any_hint(text, IMPLEMENTATION_HINTS)


def has_documentation_intent(text: str) -> bool:
    return has_any_hint(text, DOC_INTENT_HINTS)


def has_validation_intent(text: str) -> bool:
    return has_any_hint(text, VALIDATION_INTENT_HINTS)


def is_documentation_path(path: str) -> bool:
    normalized = normalized_repo_path(path)
    return normalized.startswith(DOCUMENTATION_PREFIXES) or Path(normalized).suffix.lower() in {
        ".md",
        ".txt",
    }


def is_validation_path(path: str) -> bool:
    return normalized_repo_path(path).startswith(VALIDATION_PREFIXES)


def is_product_runtime_path(path: str) -> bool:
    normalized = normalized_repo_path(path)
    return normalized in PRODUCT_RUNTIME_PATHS or normalized.startswith(PRODUCT_RUNTIME_PREFIXES)


def package_focus_score(path: str, request_text: str) -> int:
    focused = request_focus_text(request_text).lower()
    normalized = normalized_repo_path(path)
    score = 0
    for hints, package_paths in PACKAGE_FOCUS_HINTS:
        if not any(hint in focused for hint in hints):
            continue
        if any(
            normalized == package_path.rstrip("/")
            or normalized.startswith(package_path)
            for package_path in package_paths
        ):
            score += 180
    return score


def source_target_allowed_for_request(path: str, request_text: str) -> bool:
    """Keep product runs on product source, not docs/static validation artifacts."""
    focused = request_focus_text(request_text)
    if not has_product_run_intent(focused):
        return True
    if is_documentation_path(path) and not has_documentation_intent(focused):
        return False
    if is_validation_path(path) and not has_validation_intent(focused):
        return False
    return True


def filter_source_candidates_for_request(
    candidates: Iterable[str],
    request_text: str,
    *,
    limit: int,
) -> list[str]:
    focused = request_focus_text(request_text)
    product_intent = has_product_run_intent(focused)
    ordered: list[tuple[int, int, str]] = []
    seen: set[str] = set()
    for index, item in enumerate(candidates):
        rel_path = normalized_repo_path(item)
        if not rel_path or rel_path in seen:
            continue
        if not source_target_allowed_for_request(rel_path, focused):
            continue
        seen.add(rel_path)
        score = 0
        if product_intent and is_product_runtime_path(rel_path):
            score += 80
        score += package_focus_score(rel_path, focused)
        if Path(rel_path).suffix.lower() in {".py", ".ps1"}:
            score += 20
        ordered.append((-score, index, rel_path))
    ordered.sort()
    return [item[2] for item in ordered[: max(1, int(limit))]]


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

    def changed_source_candidates(self) -> set[str]:
        completed = subprocess.run(
            ["git", "status", "--short"],
            cwd=self.repo_root,
            text=True,
            capture_output=True,
            check=False,
        )
        candidates: set[str] = set()
        for line in (completed.stdout or "").splitlines():
            raw = line[3:].strip()
            if " -> " in raw:
                raw = raw.rsplit(" -> ", 1)[-1]
            ref = self.resolver.resolve(raw.replace("\\", "/"))
            if ref.patchable:
                candidates.add(ref.repo_relative)
        return candidates

    def plan(
        self,
        *,
        request_text: str,
        explicit_candidates: Iterable[str] = (),
        limit: int = 32,
    ) -> list[TargetPlanItem]:
        focused_request = request_focus_text(request_text)
        terms = tokenize(focused_request)
        product_intent = has_product_run_intent(focused_request)
        docs_intent = has_documentation_intent(focused_request)
        validation_intent = has_validation_intent(focused_request)
        explicit = {str(item).replace("\\", "/") for item in explicit_candidates if item}
        changed = self.changed_source_candidates()
        scored: list[TargetPlanItem] = []
        for rel_path in self.universe.source_index:
            ref = self.resolver.resolve(rel_path)
            if not ref.patchable:
                continue
            if not source_target_allowed_for_request(rel_path, focused_request):
                continue
            score = 0
            reasons: list[str] = []
            if product_intent and is_product_runtime_path(rel_path):
                score += 80
                reasons.append("canonical_product_runtime")
            focus_score = package_focus_score(rel_path, focused_request)
            if focus_score:
                score += focus_score
                reasons.append("package_focus")
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
            if product_intent and is_documentation_path(rel_path) and not docs_intent:
                score -= 80
                reasons.append("documentation_evidence_not_product_target")
            if product_intent and is_validation_path(rel_path) and not validation_intent:
                score -= 70
                reasons.append("validation_path_not_product_target")
            if rel_path in explicit and (token_hits or content_hits):
                score += 4
                reasons.append("explicit_current_context")
            if rel_path in changed:
                changed_boost = 24
                if token_hits or content_hits:
                    changed_boost = 96 if is_product_runtime_path(rel_path) else 36
                score += changed_boost
                reasons.append("changed_worktree_source")
            if score > 0:
                scored.append(TargetPlanItem(rel_path, score, tuple(reasons)))
        scored.sort(key=lambda item: (-item.score, item.path))
        return scored[: max(1, int(limit))]
