"""IA-Carmine evidence chunks management with dynamic reconstruction capabilities."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class EvidenceChunk:
    """An evidence chunk with navigation and concatenation support."""
    
    chunk_id: str = ""
    name: str = ""
    requirement: str = ""
    kind: str = "semantic_evidence_chunk"
    
    # Status flags
    passed: bool = False
    effective_passed: bool = False
    degraded: bool = False
    hard_failed: bool = False
    
    # Artifact paths
    useful_artifact_paths: list[str] = field(default_factory=list)
    
    # Metadata
    summary_short: str = ""
    content_preview: str = ""
    
    def get_previous_evidence_chunk_id(self) -> str:
        """Return the previous evidence chunk ID for sequential reconstruction."""
        return f"{self.chunk_id}:prev" if self.requirement else ""
    
    def get_next_evidence_chunk_id(self) -> str:
        """Return the next evidence chunk ID for sequential reconstruction."""
        return f"{self.chunk_id}:next" if self.effective_passed else ""
    
    def can_concat_with(self, other: 'EvidenceChunk') -> bool:
        """Check if this chunk can be concatenated with another evidence chunk."""
        # Evidence chunks from same requirement or related tools can be concatenated
        return True


def build_evidence_chunk_sequence(
    commands: list[dict[str, Any] | EvidenceChunk],
) -> list[EvidenceChunk]:
    """Build a sequence of evidence chunks from command data."""
    result = []
    for item in commands:
        if isinstance(item, dict):
            chunk = EvidenceChunk(
                chunk_id=f"evidence:{item.get('name', '')}:{item.get('requirement', '')}",
                name=item.get("name", ""),
                requirement=item.get("requirement", ""),
                kind="semantic_evidence_chunk",
                passed=bool(item.get("passed", False)),
                effective_passed=bool(item.get("effective_passed", False)),
                degraded=bool(item.get("degraded", False)),
                hard_failed=bool(item.get("hard_failed", False)),
                useful_artifact_paths=item.get("useful_artifact_paths", []),
            )
        else:
            chunk = item
        result.append(chunk)
    return result


def concat_evidence_chunks(chunks: list[EvidenceChunk | dict[str, Any]]) -> str:
    """Concatenate evidence chunks to form complete evidence summary (chunk + chunk = testo completo)."""
    sorted_chunks = sorted(
        [c if isinstance(c, EvidenceChunk) else EvidenceChunk(**c) for c in chunks],
        key=lambda c: (c.requirement or "", c.name or ""),
    )
    
    # Build concatenated evidence summary
    lines = ["# Heap Startup Semantic Evidence Chunks", ""]
    passed_count = 0
    failed_count = 0
    
    for chunk in sorted_chunks:
        status = "passed" if chunk.effective_passed else ("degraded" if chunk.degraded else ("failed" if chunk.hard_failed else "unknown"))
        lines.append(
            f"- `{chunk.requirement}` name=`{chunk.name}` passed=`{chunk.passed}` "
            f"effective=`{chunk.effective_passed}` degraded=`{chunk.degraded}` status=`{status}`"
        )
        if chunk.effective_passed:
            passed_count += 1
        else:
            failed_count += 1
    
    lines.append("")
    lines.append(f"## Summary")
    lines.append(f"- Total evidence chunks: `{len(sorted_chunks)}`")
    lines.append(f"- Passed: `{passed_count}`")
    lines.append(f"- Failed/Degraded: `{failed_count}`")
    
    return "\n".join(lines) + "\n"


def merge_evidence_chunks(chunks: list[EvidenceChunk | dict[str, Any]]) -> EvidenceChunk:
    """Merge multiple evidence chunks into a single unified evidence representation."""
    if not chunks:
        return EvidenceChunk()
    
    # Aggregate status
    all_passed = all(getattr(c, 'effective_passed', True) if isinstance(c, EvidenceChunk) else c.get('effective_passed', False) for c in chunks)
    any_degraded = any(getattr(c, 'degraded', False) if isinstance(c, EvidenceChunk) else c.get('degraded', False) for c in chunks)
    
    merged = EvidenceChunk(
        chunk_id=f"merged_evidence_chunks:{len(chunks)}_chunks",
        name="unified_evidence_summary",
        requirement="startup_semantic_evidence_chunks",
        kind="merged_semantic_evidence_chunks",
        passed=all_passed,
        effective_passed=all_passed and not any_degraded,
        degraded=any_degraded,
        hard_failed=not all_passed,
        useful_artifact_paths=[
            str(getattr(c, 'useful_artifact_paths', []) if isinstance(c, EvidenceChunk) else c.get('useful_artifact_paths', []))
            for c in chunks
        ],
    )
    
    return merged