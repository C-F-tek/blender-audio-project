"""Shared normalization helpers for evidence-derived plan builders."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from ia_carmine._shared.code_patch_plan_common import normalize_repo_path

TargetPathError = Callable[[str, Path], str | None]


@dataclass(frozen=True)
class DocCodeEvidenceItem:
    doc: str
    reference: str
    existing_candidate: str
    candidates: list[str]


@dataclass(frozen=True)
class DocDocEvidenceItem:
    path: str
    missing_terms: list[str]
    terms_text: str


def iter_sufficient_area_items(evidence: dict[str, Any], area_name: str):
    areas = evidence.get("areas") if isinstance(evidence.get("areas"), dict) else {}
    area = areas.get(area_name) if isinstance(areas.get(area_name), dict) else {}
    items = area.get("items", []) if isinstance(area.get("items"), list) else []
    for index, item in enumerate(items, start=1):
        if isinstance(item, dict) and item.get("evidence_sufficient") is True:
            yield index, item


def unique_repo_paths(values: Any) -> list[str]:
    if not isinstance(values, list):
        return []
    result: list[str] = []
    seen: set[str] = set()
    for value in values:
        text = normalize_repo_path(value)
        if text and text not in seen:
            seen.add(text)
            result.append(text)
    return result


def doc_code_item_or_skip(
    *,
    item: dict[str, Any],
    index: int,
    repo_root: Path,
    id_prefix: str,
    target_path_error: TargetPathError,
    missing_reason: str,
) -> tuple[DocCodeEvidenceItem | None, dict[str, str] | None]:
    doc = normalize_repo_path(item.get("doc"))
    if not doc:
        return None, {"id": f"{id_prefix}_{index:03d}", "reason": missing_reason}
    error = target_path_error(doc, repo_root)
    if error:
        return None, {"id": f"{id_prefix}_{index:03d}", "reason": f"{doc}: {error}"}
    return (
        DocCodeEvidenceItem(
            doc=doc,
            reference=normalize_repo_path(item.get("reference")),
            existing_candidate=normalize_repo_path(item.get("existing_candidate")),
            candidates=unique_repo_paths(item.get("candidate_references")),
        ),
        None,
    )


def doc_code_strategy_parts(
    *,
    reference: str,
    doc: str,
    existing_candidate: str,
    candidates: list[str],
    opening: str,
    inspect_template: str,
    existing_template: str,
    candidate_limit: int,
) -> list[str]:
    parts = [opening, inspect_template.format(reference=reference, doc=doc)]
    if existing_candidate:
        parts.append(existing_template.format(existing_candidate=existing_candidate))
    if candidates:
        rendered = ", ".join(f"`{candidate}`" for candidate in candidates[:candidate_limit])
        parts.append(f"Candidate references observed: {rendered}.")
    return parts


def doc_doc_item_or_skip(
    *,
    item: dict[str, Any],
    index: int,
    repo_root: Path,
    id_prefix: str,
    target_path_error: TargetPathError,
    missing_reason: str,
    term_limit: int,
    terms_fallback: str,
) -> tuple[DocDocEvidenceItem | None, dict[str, str] | None]:
    path = normalize_repo_path(item.get("path"))
    if not path:
        return None, {"id": f"{id_prefix}_{index:03d}", "reason": missing_reason}
    error = target_path_error(path, repo_root)
    if error:
        return None, {"id": f"{id_prefix}_{index:03d}", "reason": f"{path}: {error}"}
    missing_terms = (
        [str(term) for term in item.get("missing_terms", []) if str(term).strip()]
        if isinstance(item.get("missing_terms"), list)
        else []
    )
    terms_text = ", ".join(f"`{term}`" for term in missing_terms[:term_limit]) or terms_fallback
    return DocDocEvidenceItem(path=path, missing_terms=missing_terms, terms_text=terms_text), None


def doc_doc_strategy_text(terms_text: str, *, lead: str) -> str:
    return (
        f"{lead} {terms_text}. "
        "Link or summarize the canonical source instead of duplicating large contract sections."
    )
