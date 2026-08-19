"""IA-Carmine proposal chunks management with dynamic reconstruction capabilities."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ProposalChunk:
    """A proposal chunk with navigation and concatenation support."""
    
    chunk_id: str = ""
    name: str = ""
    kind: str = "proposal_chunk"
    
    # Block identifiers for pointer graph integration
    block_id: str = ""
    proposal_block_id: str = ""
    previous_block_id: str = ""
    refines_block_id: str = ""
    resume_from_block_id: str = ""
    
    # Content and status
    quality_passed: bool = False
    exit_decision: str = ""
    pointer_action: str = ""
    
    # Target files
    target_files: list[str] = field(default_factory=list)
    
    # Metadata
    summary_short: str = ""
    content_preview: str = ""
    
    def get_previous_proposal_chunk_id(self) -> str:
        """Return the previous proposal chunk ID for sequential reconstruction."""
        return self.previous_block_id or f"{self.chunk_id}:prev"
    
    def get_next_proposal_chunk_id(self) -> str:
        """Return the next proposal chunk ID for sequential reconstruction."""
        return self.resume_from_block_id or f"{self.chunk_id}:next"
    
    def can_concat_with(self, other: 'ProposalChunk') -> bool:
        """Check if this chunk can be concatenated with another proposal chunk."""
        # Proposal chunks from same revision or related blocks can be concatenated
        if self.proposal_block_id and self.proposal_block_id == other.proposal_block_id:
            return True
        return False


def build_proposal_chunk_sequence(
    proposals: list[dict[str, Any] | ProposalChunk],
) -> list[ProposalChunk]:
    """Build a sequence of proposal chunks from dictionary data."""
    result = []
    for item in proposals:
        if isinstance(item, dict):
            chunk = ProposalChunk(
                chunk_id=item.get("chunk_id", ""),
                name=item.get("name", ""),
                kind=item.get("kind", "proposal_chunk"),
                block_id=str(item.get("block_id", "")),
                proposal_block_id=str(item.get("proposal_block_id", "")),
                previous_block_id=str(item.get("previous_block_id", "")),
                refines_block_id=str(item.get("refines_block_id", "")),
                resume_from_block_id=str(item.get("resume_from_block_id", "")),
                quality_passed=bool(item.get("quality_passed", False)),
                exit_decision=str(item.get("exit_decision", "")),
                pointer_action=str(item.get("pointer_action", "")),
                target_files=item.get("target_files", []),
                summary_short=str(item.get("summary_short", "")),
                content_preview=str(item.get("content_preview", "")),
            )
        else:
            chunk = item
        result.append(chunk)
    return result


def concat_proposal_chunks(chunks: list[ProposalChunk | dict[str, Any]]) -> str:
    """Concatenate proposal chunks to form complete proposal text (chunk + chunk = testo completo)."""
    sorted_chunks = sorted(
        [c if isinstance(c, ProposalChunk) else ProposalChunk(**c) for c in chunks],
        key=lambda c: (c.proposal_block_id or "", c.name or ""),
    )
    
    # Build concatenated proposal summary
    lines = ["# Heap Final Proposals", ""]
    
    for chunk in sorted_chunks:
        status = "accepted" if chunk.quality_passed else "rejected"
        lines.append(f"## Proposal: `{chunk.name or chunk.proposal_block_id}`")
        lines.append(f"- Status: `{status}`")
        lines.append(f"- Exit decision: `{chunk.exit_decision}`")
        lines.append(f"- Pointer action: `{chunk.pointer_action}`")
        
        if chunk.target_files:
            lines.append("- Target files:")
            for tf in chunk.target_files:
                lines.append(f"  - `{tf}`")
        
        if chunk.content_preview:
            lines.extend(["", "```text", chunk.content_preview, "```"])
        
        lines.append("")
    
    return "\n".join(lines) + "\n"


def merge_proposal_chunks(chunks: list[ProposalChunk | dict[str, Any]]) -> ProposalChunk:
    """Merge multiple proposal chunks into a single unified proposal representation."""
    if not chunks:
        return ProposalChunk()
    
    # Aggregate metadata
    all_block_ids = set(str(c.block_id or c.proposal_block_id) for c in chunks if getattr(c, 'block_id', None) or (isinstance(c, dict) and c.get('block_id')))
    
    merged = ProposalChunk(
        chunk_id=f"merged_proposal_chunks:{len(chunks)}_chunks",
        name="unified_proposal_summary",
        kind="merged_semantic_proposal_chunks",
        proposal_block_id=list(all_block_ids)[0] if all_block_ids else "",
        quality_passed=all(getattr(c, 'quality_passed', False) for c in chunks),
        exit_decision="PATCHABLE_TARGET" if any(getattr(c, 'exit_decision', '') == "PATCHABLE_TARGET" for c in chunks) else "BLOCKED",
        pointer_action="RESUME_FORWARD",
        target_files=[str(c.target_files[0]) if getattr(c, 'target_files', None) and c.target_files else "" for c in chunks if getattr(c, 'target_files', None)],
    )
    
    return merged