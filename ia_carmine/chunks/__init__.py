"""IA-Carmine chunk system for dynamic reconstruction and concatenation."""

from __future__ import annotations

# Import from subdirectories to avoid circular imports with .py files
from .code_chunks import (
    CodeChunk,
    build_code_chunk_sequence,
    concat_code_chunks,
)
from .evidence_chunks import (
    EvidenceChunk,
    build_evidence_chunk_sequence,
    concat_evidence_chunks,
)
from .proposal_chunks import (
    ProposalChunk,
    build_proposal_chunk_sequence,
    concat_proposal_chunks,
)

__all__ = [
    # From code_chunks module
    "CodeChunk",
    "build_code_chunk_sequence",
    "concat_code_chunks",
    # From evidence_chunks module
    "EvidenceChunk",
    "build_evidence_chunk_sequence",
    "concat_evidence_chunks",
    # From proposal_chunks module
    "ProposalChunk",
    "build_proposal_chunk_sequence",
    "concat_proposal_chunks",
]