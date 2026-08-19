"""IA-Carmine memory pointers for heap block navigation and anchoring."""

from __future__ import annotations

# Import from the main pointers module to avoid duplication
from ia_carmine.pointers.graph import (
    PointerGraph,
    PointerNode,
    get_previous_block_id,
    get_next_block_id,
    get_refines_block_id,
    get_resume_from_block_id,
    has_previous,
    has_next,
    has_refines,
)
from ia_carmine.pointers.resume import (
    ResumeContext,
    resume_anchor,
    can_resume_forward,
    build_resume_context,
)
from ia_carmine.pointers.revision_context import (
    RevisionPointer,
    build_revision_pointer,
    extract_pointer_fields,
    build_pointer_contract,
)

__all__ = [
    # From graph module
    "PointerGraph",
    "PointerNode",
    "get_previous_block_id",
    "get_next_block_id",
    "get_refines_block_id",
    "get_resume_from_block_id",
    "has_previous",
    "has_next",
    "has_refines",
    # From resume module
    "ResumeContext",
    "resume_anchor",
    "can_resume_forward",
    "build_resume_context",
    # From revision_context module
    "RevisionPointer",
    "build_revision_pointer",
    "extract_pointer_fields",
    "build_pointer_contract",
]