#!/usr/bin/env python3
"""Deterministic proposal gating helpers for heap final packaging."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

SOURCE_TARGET_EXTENSIONS = {".py", ".ps1", ".md", ".json", ".yml", ".yaml", ".toml"}
FORBIDDEN_TARGET_PREFIXES = (
    "output/",
    "renders/",
    "indexAI/",
    "docs/LOCAL_VALIDATION_EVIDENCE/",
)


def normalize_repo_path(value: Any) -> str:
    return str(value or "").strip().strip("`'\"").replace("\\", "/").lstrip("./")


def read_text(path: Path, limit: int | None = None) -> str:
    try:
        text = path.read_text(encoding="utf-8-sig", errors="replace")
    except Exception:
        return ""
    if limit is not None and len(text) > limit:
        return text[:limit] + "\n...[truncated]\n"
    return text


def load_allowlist(path: str, repo_root: Path) -> tuple[set[str], bool, str]:
    """Load an optional JSON source allowlist.

    Missing allowlist files do not reject proposals; existing empty allowlists
    deliberately reject all targets for safety.
    """
    if not path:
        return set(), False, ""
    allowlist_path = Path(path)
    if not allowlist_path.is_absolute():
        allowlist_path = repo_root / allowlist_path
    if not allowlist_path.exists():
        return set(), False, str(allowlist_path)
    try:
        data = json.loads(allowlist_path.read_text(encoding="utf-8-sig"))
    except Exception:
        return set(), True, str(allowlist_path)
    if not isinstance(data, list):
        return set(), True, str(allowlist_path)
    return (
        {normalize_repo_path(item) for item in data if str(item).strip()},
        True,
        str(allowlist_path),
    )


def is_source_allowed(source: str, allowlist: set[str]) -> bool:
    normalized = normalize_repo_path(source)
    return bool(normalized and normalized in allowlist)


def is_reviewable_target_path(path: str) -> bool:
    normalized = normalize_repo_path(path)
    if not normalized or normalized.startswith(FORBIDDEN_TARGET_PREFIXES):
        return False
    return Path(normalized).suffix.lower() in SOURCE_TARGET_EXTENSIONS


def has_forbidden_markers(text: str) -> bool:
    forbidden_patterns = [
        r"tools/.+real_existing_file\.py",
        r"Tools/data_processor/.+real_existing_file\.py",
        r"<id-or-empty>",
        r"placeholder",
        r"pass\s*/?\s*TODO\s*",
        r"\bFIXME\b",
    ]
    return any(re.search(pattern, text or "", re.IGNORECASE) for pattern in forbidden_patterns)


def proposal_similarity(p1: dict[str, Any], p2: dict[str, Any]) -> float:
    txt1 = str(p1.get("response_text") or "")
    txt2 = str(p2.get("response_text") or "")
    set1 = set(re.findall(r"\w+", txt1.lower()))
    set2 = set(re.findall(r"\w+", txt2.lower()))
    if not set1 and not set2:
        return 1.0
    if not set1 or not set2:
        return 0.0
    return len(set1 & set2) / len(set1 | set2)


def increment_reject(
    source: str,
    counters: dict[str, int],
    last: dict[str, dict[str, Any]],
    proposal: dict[str, Any],
    threshold: float,
) -> bool:
    previous = last.get(source)
    counters[source] = counters.get(source, 0) + 1
    last[source] = proposal
    return bool(previous and proposal_similarity(previous, proposal) >= threshold)


def proposal_gate_targets(proposal: dict[str, Any]) -> list[str]:
    targets: list[str] = []
    for value in [proposal.get("source")]:
        normalized = normalize_repo_path(value)
        if is_reviewable_target_path(normalized) and normalized not in targets:
            targets.append(normalized)
    preferred = proposal.get("verified_declared_target_files")
    if isinstance(preferred, list):
        for value in preferred:
            normalized = normalize_repo_path(value)
            if is_reviewable_target_path(normalized) and normalized not in targets:
                targets.append(normalized)
        return targets
    for key in ("target_files", "target_paths"):
        values = proposal.get(key)
        if not isinstance(values, list):
            continue
        for value in values:
            normalized = normalize_repo_path(value)
            if is_reviewable_target_path(normalized) and normalized not in targets:
                targets.append(normalized)
    return targets


def gate_proposals(
    *,
    proposals: list[dict[str, Any]],
    allowed_sources: set[str],
    allowlist_enforced: bool,
    similarity_threshold: float,
) -> list[dict[str, Any]]:
    gated: list[dict[str, Any]] = []
    reject_counters: dict[str, int] = {}
    last_rejected: dict[str, dict[str, Any]] = {}
    for proposal in proposals:
        item = dict(proposal)
        targets = proposal_gate_targets(item)
        gate_reasons: list[str] = []
        review_text = "\n".join(
            [
                str(item.get("source") or ""),
                str(item.get("response_text") or ""),
                read_text(item["markdown_path"], 12000)
                if isinstance(item.get("markdown_path"), Path)
                else "",
            ]
        )
        if has_forbidden_markers(review_text):
            gate_reasons.append("forbidden placeholder or fake-path marker detected")
        if allowlist_enforced:
            if not allowed_sources:
                gate_reasons.append("source allowlist exists but contains no allowed paths")
            elif not any(is_source_allowed(target, allowed_sources) for target in targets):
                gate_reasons.append("no proposal target is present in source allowlist")
        target_key = targets[0] if targets else normalize_repo_path(item.get("source"))
        if item.get("accepted") is not True and target_key:
            repeated = increment_reject(
                target_key,
                reject_counters,
                last_rejected,
                item,
                similarity_threshold,
            )
            if repeated:
                gate_reasons.append(
                    f"repeated rejected proposal for {target_key}: similarity>={similarity_threshold:.2f}"
                )
        if gate_reasons:
            item["accepted"] = False
            item["operator_gate_passed"] = False
            item["operator_gate_reasons"] = gate_reasons
            existing_reason = str(item.get("reject_reason") or "").strip()
            reason_text = "; ".join(gate_reasons)
            item["reject_reason"] = (
                f"{existing_reason}; {reason_text}" if existing_reason else reason_text
            )
        else:
            item["operator_gate_passed"] = True
            item["operator_gate_reasons"] = []
        item["operator_gate_targets"] = targets
        gated.append(item)
    return gated


def build_operator_decision(
    *,
    proposals: list[dict[str, Any]],
    allowlist_enforced: bool,
    allowlist_path: str,
) -> dict[str, Any]:
    accepted = [item for item in proposals if item.get("accepted")]
    rejected = [item for item in proposals if not item.get("accepted")]
    gate_reasons = [
        reason for proposal in proposals for reason in proposal.get("operator_gate_reasons", [])
    ]
    if not proposals:
        decision = "NO CONCRETE PATCHABLE PROPOSAL"
        reason = "No proposal iteration artifacts were found."
    elif accepted:
        decision = "ACCEPTED_PATCHABLE"
        reason = "At least one proposal passed the heap quality gate and operator gate."
    elif gate_reasons and all(
        any(
            marker in reason.lower()
            for marker in ("allowlist", "fake-path", "placeholder", "proposal target")
        )
        for reason in gate_reasons
    ):
        decision = "BLOCKED_NO_VERIFIED_TARGET"
        reason = "Proposal artifacts exist, but every candidate was blocked by target or placeholder gates."
    else:
        decision = "BLOCKED_PROVIDER_REVIEW"
        reason = "Provider proposal artifacts exist, but none passed as concrete patchable coding work."
    return {
        "decision": decision,
        "reason": reason,
        "accepted_count": len(accepted),
        "rejected_count": len(rejected),
        "proposal_count": len(proposals),
        "allowlist_enforced": allowlist_enforced,
        "allowlist_path": allowlist_path,
        "gate_reasons": gate_reasons,
        "targets_considered": sorted(
            {
                target
                for proposal in proposals
                for target in proposal.get("operator_gate_targets", [])
            }
        ),
    }


def record_operator_decision(
    doc_dir: Path,
    decision: dict[str, Any],
    targets: list[str],
) -> Path:
    doc_dir.mkdir(parents=True, exist_ok=True)
    lines = [
        f"Decision: {decision.get('decision')}",
        f"Reason: {decision.get('reason')}",
        f"Accepted proposals: {decision.get('accepted_count')}",
        f"Rejected proposals: {decision.get('rejected_count')}",
        f"Targets considered: {', '.join(targets) if targets else 'none'}",
        f"Allowlist enforced: {decision.get('allowlist_enforced')}",
        f"Allowlist path: {decision.get('allowlist_path') or 'none'}",
    ]
    gate_reasons = decision.get("gate_reasons")
    if gate_reasons:
        lines.append("Gate reasons:")
        lines.extend(f"- {reason}" for reason in gate_reasons)
    path = doc_dir / "OPERATOR_DECISION.txt"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path
