"""Candidate applicability and terminal-target classification."""

from __future__ import annotations

import json
import re
from typing import Any

from .common import CANDIDATE_APPLICABILITY_PATTERNS, as_list

def candidate_applicability_flags(text: str) -> list[str]:
    flags: list[str] = []
    for flag, pattern in CANDIDATE_APPLICABILITY_PATTERNS:
        if pattern.search(text or "") and flag not in flags:
            flags.append(flag)
    return flags

def no_patchable_target_text(text: str) -> bool:
    candidate = str(text or "")
    return (
        "EXIT_DECISION=NO_PATCHABLE_TARGET" in candidate
        and re.search(r"(?im)^\s*-\s*none_verified\s*$", candidate) is not None
        and "PATCH_SKETCH:" in candidate
    )

def block_is_terminal_no_patchable_target(block: dict[str, Any]) -> bool:
    for key in (
        "candidate_response_preview",
        "source_preview",
        "preview",
        "response_text",
    ):
        if no_patchable_target_text(str(block.get(key) or "")):
            return True

    evidence_text = candidate_text_from_block(block)
    lowered = evidence_text.lower()
    flags = candidate_applicability_flags(evidence_text)
    for flag in as_list(block.get("candidate_applicability_flags")):
        flag_text = str(flag).strip()
        if flag_text and flag_text not in flags:
            flags.append(flag_text)

    no_verified_target_signals = (
        "no verified source file references",
        "source refs non verificati",
        "target_files must come from source allowlist only",
        "invented_source_path veto",
        "decision=reject_until_concrete_code_and_full_repo_relative_paths",
        "no verified/allowlisted repo-relative patch target",
        "none_verified",
    )

    has_no_verified_target_signal = any(signal in lowered for signal in no_verified_target_signals)
    has_terminal_blocker = any(
        flag in flags
        for flag in (
            "invented_source_path",
            "unresolved_pointer_placeholder",
            "unresolved_angle_bracket_token",
        )
    )

    return has_terminal_blocker and has_no_verified_target_signal

def terminal_no_patchable_target_summary(
    proposals: list[dict[str, Any]],
) -> dict[str, Any]:
    terminal_ids = [
        str(block.get("block_id") or "")
        for block in proposals
        if block_is_terminal_no_patchable_target(block)
    ]
    all_terminal = bool(proposals) and len(terminal_ids) == len(proposals)
    return {
        "count": len(terminal_ids),
        "block_ids": terminal_ids,
        "all_proposals_terminal_no_patchable_target": all_terminal,
    }

def candidate_text_from_block(block: dict[str, Any]) -> str:
    """Return the full evidence text used to classify candidate applicability.

    The old implementation looked mainly at candidate_response_preview. That was
    insufficient once the deterministic lanes reported placeholder/stub markers
    only in diagnostic previews or composer rejection reasons. This function
    deliberately combines candidate response, source preview, diagnostic preview,
    rejection snippets and existing block quality metadata.
    """
    parts: list[str] = []
    for key in (
        "candidate_response_preview",
        "source_preview",
        "preview",
        "diagnostic_preview",
        "response_text",
    ):
        value = block.get(key)
        if value:
            parts.append(str(value))
    for key in (
        "rejection_reasons",
        "errors",
        "warnings",
        "candidate_applicability_flags",
    ):
        for value in as_list(block.get(key)):
            parts.append(str(value))
    for key in ("implementation_quality", "proposal_progress", "cross_lane_veto"):
        value = block.get(key)
        if isinstance(value, dict):
            parts.append(json.dumps(value, ensure_ascii=False, sort_keys=True))
    return "\n".join(parts)

def candidate_symbol_text_from_block(block: dict[str, Any]) -> str:
    """Return candidate-only text used for symbol propagation.

    Diagnostic previews, rejection reasons and quality metadata are intentionally
    excluded here. They are valid evidence for applicability blockers, but they
    must not introduce synthetic imports, defs, classes or assignments into the
    back-propagation lane.
    """
    parts: list[str] = []
    for key in (
        "candidate_response_preview",
        "source_preview",
        "preview",
        "response_text",
    ):
        value = block.get(key)
        if value:
            parts.append(str(value))
    return "\n".join(parts)

def candidate_applicability_flags_from_block(block: dict[str, Any]) -> list[str]:
    if block_is_terminal_no_patchable_target(block):
        return []
    flags = candidate_applicability_flags(candidate_text_from_block(block))
    for flag in as_list(block.get("candidate_applicability_flags")):
        text = str(flag).strip()
        if text and text not in flags:
            flags.append(text)
    return flags

def candidate_concrete_enough(text: str) -> bool:
    return not candidate_applicability_flags(text)

def candidate_block_concrete_enough(block: dict[str, Any]) -> bool:
    return not candidate_applicability_flags_from_block(block)

def sanitize_revision_context_text(text: str) -> str:
    """Remove rejected generated refs from next-run operational context."""
    cleaned = str(text or "")
    cleaned = re.sub(
        r"`?(?:[A-Za-z0-9_.-]+[/\\])+[A-Za-z0-9_.-]+\.(?:py|ps1|md|json|ya?ml|toml|txt)`?",
        "`[REJECTED_NON_ALLOWLISTED_SOURCE_PATH]`",
        cleaned,
    )
    cleaned = re.sub(
        r"`?[A-Za-z0-9_.-]+\.(?:py|ps1)`?",
        "`[REJECTED_SOURCE_BASENAME]`",
        cleaned,
    )
    cleaned = re.sub(r"<id-or-empty>", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"<[^>\n]*placeholder[^>\n]*>", "", cleaned, flags=re.IGNORECASE)
    return cleaned
