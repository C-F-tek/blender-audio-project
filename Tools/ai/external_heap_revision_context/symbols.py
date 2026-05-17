"""Block selection and symbol extraction helpers."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .applicability import candidate_applicability_flags_from_block, candidate_text_from_block
from .common import REJECTION_MARKER_PATTERNS, as_list

def proposal_blocks(pointer: dict[str, Any]) -> list[dict[str, Any]]:
    blocks = [
        block
        for block in as_list(pointer.get("blocks"))
        if isinstance(block, dict) and block.get("block_type") == "proposal_chunk"
    ]
    return sorted(blocks, key=lambda block: int(block.get("step_index") or 0))

def peer_blocks(pointer: dict[str, Any], role: str) -> list[dict[str, Any]]:
    blocks = [
        block
        for block in as_list(pointer.get("blocks"))
        if isinstance(block, dict) and block.get("role") == role
    ]
    return sorted(blocks, key=lambda block: int(block.get("step_index") or 0))

def latest_block(blocks: list[dict[str, Any]]) -> dict[str, Any]:
    return blocks[-1] if blocks else {}

def clean_import_line(line: str) -> str:
    stripped = line.strip()
    if stripped.startswith("import ") or stripped.startswith("from "):
        return stripped
    return ""

def extract_symbols(text: str) -> dict[str, list[str]]:
    imports: set[str] = set()
    defs: set[str] = set()
    classes: set[str] = set()
    assignments: set[str] = set()
    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        import_line = clean_import_line(line)
        if import_line:
            imports.add(import_line)
        def_match = re.match(r"^\s*def\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(", line)
        if def_match:
            defs.add(def_match.group(1))
        class_match = re.match(r"^\s*class\s+([A-Za-z_][A-Za-z0-9_]*)\s*[:(]", line)
        if class_match:
            classes.add(class_match.group(1))
        assignment_match = re.match(r"^\s*([A-Z][A-Z0-9_]{2,}|[a-z_][a-z0-9_]{3,})\s*=", line)
        if assignment_match and not stripped.startswith(("return ", "if ", "for ", "while ")):
            assignments.add(assignment_match.group(1))
    return {
        "imports": sorted(imports),
        "defs": sorted(defs),
        "classes": sorted(classes),
        "assignments": sorted(assignments)[:80],
    }

def rejection_reasons(composer: dict[str, Any], block: dict[str, Any]) -> list[str]:
    source_name = Path(str(block.get("source_path") or "")).name
    reasons: list[str] = []
    for item in as_list(composer.get("rejected_proposals")):
        if not isinstance(item, dict):
            continue
        if item.get("name") == source_name:
            reason = str(item.get("reason") or "").strip()
            if reason:
                reasons.append(reason)
    marker_text = candidate_text_from_block(block)
    for marker, pattern in REJECTION_MARKER_PATTERNS:
        if pattern.search(marker_text) and marker not in reasons:
            reasons.append(marker)
    for flag in candidate_applicability_flags_from_block(block):
        reason = f"candidate_applicability.{flag}"
        if reason not in reasons:
            reasons.append(reason)
    return reasons
