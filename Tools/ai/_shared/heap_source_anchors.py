#!/usr/bin/env python3
"""Verified source-anchor helpers for heap/provider proposal outputs."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

try:
    from Tools.ai.runtime_file_refs import RuntimeFileRefResolver
    from Tools.ai.runtime_universe import RepoRuntimeUniverseBuilder
except ImportError:  # pragma: no cover
    import sys

    repo_root_for_import = Path(__file__).resolve().parents[2]
    if str(repo_root_for_import) not in sys.path:
        sys.path.insert(0, str(repo_root_for_import))
    from Tools.ai.runtime_file_refs import RuntimeFileRefResolver  # type: ignore
    from Tools.ai.runtime_universe import RepoRuntimeUniverseBuilder  # type: ignore

FILE_REF_PATTERN = re.compile(
    r"`([^`]+\.(?:py|ps1|md|json|ya?ml|toml|txt|csv))`|"
    r"(?:File|file)\s+([A-Za-z0-9_./\\-]+\.(?:py|ps1|md|json|ya?ml|toml|txt|csv))"
)
BARE_FILE_REF_PATTERN = re.compile(
    r"(?<![A-Za-z0-9_./\\-])"
    r"((?:Tools|tools|docs|Scripting|scripts|patch_specs|CHATGPT|config|examples|assets|\.github)"
    r"[A-Za-z0-9_./\\-]*\.(?:py|ps1|md|json|ya?ml|toml|txt|csv))",
    re.IGNORECASE,
)

SOURCE_CODE_EXTENSIONS = {".py", ".ps1", ".md", ".yml", ".yaml", ".toml"}
PRIMARY_CODE_EXTENSIONS = {".py", ".ps1"}
OUTPUT_ARTIFACT_PREFIXES = (
    "output/",
    "renders/",
    "indexAI/",
    "docs/LOCAL_VALIDATION_EVIDENCE/",
)
SOURCE_CONTEXT_KEYS = {
    "path",
    "file",
    "source_file",
    "repo_path",
    "target_file",
    "target_path",
}
SOURCE_ANCHOR_SEARCH_ROOTS = (
    "tools",
    "Scripting",
    "patch_specs",
    "docs",
    "config",
    "examples",
    ".github",
)


def repo_rel(repo_root: Path, path: Path) -> str:
    try:
        return path.resolve(strict=False).relative_to(repo_root.resolve(strict=False)).as_posix()
    except ValueError:
        return str(path)


def normalize_ref_path(rel_path: str) -> str:
    return str(rel_path or "").strip().strip("`'\"").replace("\\", "/")


def repo_file_exists(repo_root: Path, rel_path: str) -> bool:
    normalized = normalize_ref_path(rel_path)
    if not normalized or normalized.startswith(("http:/", "https:/")):
        return False
    return (repo_root / normalized).is_file()


def is_output_artifact_ref(rel_path: str) -> bool:
    return normalize_ref_path(rel_path).startswith(OUTPUT_ARTIFACT_PREFIXES)


def is_source_candidate_ref(rel_path: str) -> bool:
    normalized = normalize_ref_path(rel_path)
    if not normalized or is_output_artifact_ref(normalized):
        return False
    return Path(normalized).suffix.lower() in SOURCE_CODE_EXTENSIONS


def repo_source_file_exists(repo_root: Path, rel_path: str) -> bool:
    ref = RuntimeFileRefResolver(repo_root).resolve(rel_path)
    return ref.patchable and is_source_candidate_ref(ref.repo_relative)


def extracted_file_refs(text: str) -> list[str]:
    refs: list[str] = []
    for match in FILE_REF_PATTERN.finditer(text or ""):
        value = next((group for group in match.groups() if group), "")
        normalized = normalize_ref_path(value)
        if normalized and normalized not in refs:
            refs.append(normalized)
    for match in BARE_FILE_REF_PATTERN.finditer(text or ""):
        normalized = normalize_ref_path(match.group(1))
        if normalized and normalized not in refs:
            refs.append(normalized)
    return refs


def proposal_declares_target_files(text: str) -> bool:
    lowered = (text or "").lower()
    return any(
        marker in lowered
        for marker in ("target_files", "target files", "target_file", "target file")
    )


def source_ref_alias_matches(
    repo_root: Path,
    rel_path: str,
    limit: int = 20,
    search_roots: tuple[str, ...] = SOURCE_ANCHOR_SEARCH_ROOTS,
) -> list[str]:
    normalized = normalize_ref_path(rel_path)
    if not normalized or is_output_artifact_ref(normalized):
        return []
    if Path(normalized).suffix.lower() not in SOURCE_CODE_EXTENSIONS:
        return []
    name = Path(normalized).name
    matches: list[str] = []
    for root in search_roots:
        base = repo_root / root
        if not base.exists():
            continue
        for path in sorted(base.rglob(name)):
            rel = repo_rel(repo_root, path)
            if repo_source_file_exists(repo_root, rel) and rel not in matches:
                matches.append(rel)
            if len(matches) >= limit:
                return matches
    return matches


def resolve_source_ref_alias(repo_root: Path, rel_path: str) -> str:
    normalized = normalize_ref_path(rel_path)
    if repo_source_file_exists(repo_root, normalized):
        return normalized
    matches = source_ref_alias_matches(repo_root, normalized, limit=25)
    if len(matches) == 1:
        return matches[0]
    return matches[0] if len(matches) == 1 else ""


def response_file_reference_quality(
    *,
    repo_root: Path,
    text: str,
    requires_existing: bool,
    implementation_required: bool,
) -> dict[str, Any]:
    refs = extracted_file_refs(text)
    output_refs = [ref for ref in refs if is_output_artifact_ref(ref)]
    source_refs = [ref for ref in refs if is_source_candidate_ref(ref)]
    existing_source: list[str] = []
    resolved_source: list[str] = []
    unverified_source: list[str] = []
    alias_refs: dict[str, str] = {}
    ambiguous_source: dict[str, list[str]] = {}
    for ref in source_refs:
        normalized = normalize_ref_path(ref)
        direct_exists = repo_source_file_exists(repo_root, normalized)
        resolved = normalized if direct_exists else resolve_source_ref_alias(repo_root, normalized)
        if resolved:
            if resolved not in existing_source:
                existing_source.append(resolved)
            if resolved not in resolved_source:
                resolved_source.append(resolved)
            if resolved != normalized:
                alias_refs[normalized] = resolved
            continue
        matches = source_ref_alias_matches(repo_root, normalized, limit=12)
        if matches:
            ambiguous_source[normalized] = matches
        unverified_source.append(normalized)
    declares_target_files = proposal_declares_target_files(text)
    requires_verified_sources = (
        requires_existing or declares_target_files or implementation_required
    )
    no_source_refs = requires_verified_sources and not existing_source
    passed = (not requires_verified_sources) or (
        not unverified_source and not ambiguous_source and not no_source_refs
    )
    return {
        "request_requires_existing_files": requires_existing,
        "declares_target_files": declares_target_files,
        "requires_verified_sources": requires_verified_sources,
        "file_refs": refs,
        "output_artifact_refs": output_refs,
        "source_file_refs": source_refs,
        "existing_file_refs": existing_source,
        "existing_source_file_refs": existing_source,
        "resolved_source_file_refs": resolved_source,
        "source_alias_refs": alias_refs,
        "ambiguous_source_file_refs": ambiguous_source,
        "unverified_file_refs": unverified_source,
        "unverified_source_file_refs": unverified_source,
        "no_source_file_refs": no_source_refs,
        "passed": passed,
    }


def collect_source_candidates_from_json(
    repo_root: Path, data: Any, out: list[str], max_count: int = 40
) -> None:
    if len(out) >= max_count:
        return
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, str) and key in SOURCE_CONTEXT_KEYS:
                ref = normalize_ref_path(value)
                if repo_source_file_exists(repo_root, ref) and ref not in out:
                    out.append(ref)
            else:
                collect_source_candidates_from_json(repo_root, value, out, max_count)
    elif isinstance(data, list):
        for item in data:
            collect_source_candidates_from_json(repo_root, item, out, max_count)


def read_json_file(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def request_source_file_candidates(repo_root: Path, texts: list[str], limit: int = 24) -> list[str]:
    candidates: list[str] = []
    for text in texts:
        for ref in extracted_file_refs(text):
            normalized = normalize_ref_path(ref)
            resolved = (
                normalized
                if repo_source_file_exists(repo_root, normalized)
                else resolve_source_ref_alias(repo_root, normalized)
            )
            if resolved and resolved not in candidates:
                candidates.append(resolved)
            if len(candidates) >= limit:
                return candidates
    return candidates


def implementation_request(texts: list[str]) -> bool:
    text = "\n".join(str(item or "") for item in texts).lower()
    hints = (
        "code product",
        "codice",
        "diff",
        "implement",
        "launcher",
        "patch",
        "proposte concrete",
        "refactor",
        "rifattoriz",
    )
    return any(hint in text for hint in hints)


def prioritize_source_candidates(candidates: list[str], texts: list[str], limit: int) -> list[str]:
    if not candidates:
        return []
    request_terms = {
        item
        for item in re.split(r"[^a-z0-9]+", "\n".join(texts).lower().replace("_", " "))
        if len(item) >= 4
    }
    implementation = implementation_request(texts)

    def score(path: str) -> tuple[int, str]:
        normalized = normalize_ref_path(path)
        suffix = Path(normalized).suffix.lower()
        path_text = normalized.lower().replace("_", " ")
        token_hits = sum(1 for term in request_terms if term in path_text)
        value = 10 * token_hits
        if suffix in PRIMARY_CODE_EXTENSIONS:
            value += 40
        elif implementation and suffix == ".md":
            value -= 30
        elif suffix in {".json", ".toml", ".yml", ".yaml"}:
            value -= 10
        return (-value, normalized)

    ordered = sorted(dict.fromkeys(candidates), key=score)
    return ordered[: max(1, int(limit))]


def real_source_file_candidates(
    *,
    repo_root: Path,
    request_texts: list[str],
    broker_output_refs: list[str],
    limit: int = 24,
) -> list[str]:
    candidates = request_source_file_candidates(repo_root, request_texts, limit=limit)
    for ref in broker_output_refs:
        if not str(ref).endswith(".json"):
            continue
        data = read_json_file(repo_root / ref)
        if data:
            collect_source_candidates_from_json(repo_root, data, candidates)
        if len(candidates) >= limit * 3:
            break
    universe = RepoRuntimeUniverseBuilder(repo_root).build()
    for rel in universe.source_index:
        if rel.endswith(".py") and rel not in candidates:
            candidates.append(rel)
    return prioritize_source_candidates(candidates, request_texts, limit)


def source_allowlist_contract(candidates: list[str]) -> dict[str, Any]:
    return {
        "allowed_source_paths": candidates,
        "allowed_source_path_count": len(candidates),
        "blocked_exit_decision": "NO_PATCHABLE_TARGET",
        "blocked_reason_field": "BLOCKED_NO_VERIFIED_TARGET_REASON",
        "forbid_unlisted_source_paths": True,
        "forbid_angle_bracket_placeholders": True,
    }


def render_source_allowlist_contract(candidates: list[str]) -> str:
    lines = [
        "SOURCE_PATH_ALLOWLIST_CONTRACT:",
        "- Every TARGET_FILES entry MUST be an exact repo-relative path from Allowed source paths below.",
        "- Every diff header path MUST match the same allowlist; do not cite basenames or invented directories.",
        "- Copy TARGET_FILES verbatim from Allowed source paths; do not cite non-allowlisted source paths anywhere in the proposal.",
        "- For refactor/OOB tasks, prefer existing allowed source paths; new files require an explicit operator request.",
        "- Do not invent files such as tools/data_processor/real_existing_file.py or any other non-allowlisted path.",
        "- Never use generated evidence/output prefixes as TARGET_FILES: output/, renders/, indexAI/, docs/LOCAL_VALIDATION_EVIDENCE/.",
        "- If no allowed source path is patchable from current evidence, emit EXIT_DECISION=NO_PATCHABLE_TARGET.",
        "- In that case include BLOCKED_NO_VERIFIED_TARGET_REASON and do not output a fake diff.",
        "- Never emit unresolved angle-bracket placeholders such as <id-or-empty>; use an empty value or a real block id.",
        "Allowed source paths:",
    ]
    lines.extend(f"- {item}" for item in candidates) if candidates else lines.append(
        "- none_available"
    )
    return "\n".join(lines)


def source_anchor_feedback(candidates: list[str], requested: list[Any] | None = None) -> str:
    if not candidates:
        return ""
    lines = [
        "SOURCE PATH ANCHORING REQUIRED:",
        "Use only exact repo-relative paths from this allowlist when citing source files.",
        "Copy TARGET_FILES verbatim from Allowed source paths; do not cite any non-allowlisted source path in prose, evidence or diff headers.",
        "Do not cite basenames unless the exact repo-relative path is also present.",
        "Every TARGET_FILES entry and every diff header path must be one of the allowed source paths below.",
        "Never use generated evidence/output prefixes as TARGET_FILES: output/, renders/, indexAI/, docs/LOCAL_VALIDATION_EVIDENCE/.",
        "If no allowed path fits the evidence, return EXIT_DECISION=NO_PATCHABLE_TARGET with BLOCKED_NO_VERIFIED_TARGET_REASON.",
        "Never output unresolved placeholders like <id-or-empty>; use empty values or real block ids.",
    ]
    rejected = [str(item) for item in (requested or []) if str(item).strip()]
    if rejected:
        lines.append(
            "Rejected/non-allowlisted refs from prior proposal (BLACKLIST; do not reuse): "
            + ", ".join(rejected[:12])
        )
        lines.append(
            "Do not copy candidate_response_preview TARGET_FILES, diff headers or PATCH_SKETCH entries that mention those refs."
        )
    lines.append("Allowed source paths:")
    lines.extend(f"- {item}" for item in candidates[:20])
    return "\n".join(lines)
