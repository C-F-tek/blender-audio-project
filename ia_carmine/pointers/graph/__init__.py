"""IA-Carmine pointer graph for heap block navigation and anchoring."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class PointerNode:
    """A node in the pointer graph representing a heap block or proposal chunk."""
    
    block_id: str = ""
    previous_block_id: str = ""
    next_block_id: str = ""
    refines_block_id: str = ""
    resume_from_block_id: str = ""
    
    # Pointer action and decision metadata
    pointer_action: str = ""
    exit_decision: str = ""
    quality_passed: bool = False
    
    # Role and classification
    role: str = ""
    block_type: str = ""
    
    # Target files and evidence
    target_files: list[str] = field(default_factory=list)
    proposal_block_id: str = ""
    
    def get_previous(self) -> str:
        """Return the previous block ID for backward navigation."""
        return self.previous_block_id or ""
    
    def get_next(self) -> str:
        """Return the next block ID for forward continuation."""
        return self.next_block_id or ""
    
    def get_refines(self) -> str:
        """Return the refines block ID for back-refinement."""
        return self.refines_block_id or ""
    
    def get_resume_from(self) -> str:
        """Return the resume from block ID for continuation after rewrite."""
        return self.resume_from_block_id or self.block_id or ""


@dataclass
class PointerGraph:
    """A directed graph of pointer nodes representing heap execution history."""
    
    nodes: dict[str, PointerNode] = field(default_factory=dict)
    latest_block_id: str = ""
    proposal_block_id: str = ""
    
    def add_node(self, node: PointerNode) -> None:
        """Add a node to the pointer graph."""
        if node.block_id:
            self.nodes[node.block_id] = node
            self.latest_block_id = node.block_id
    
    def get_node(self, block_id: str) -> PointerNode | None:
        """Retrieve a node by its block ID."""
        return self.nodes.get(block_id)
    
    def has_previous(self, block_id: str) -> bool:
        """Check if the block has a previous block in the graph."""
        node = self.get_node(block_id)
        if not node:
            return False
        prev_id = node.get_previous()
        return bool(prev_id and (prev_id in self.nodes or prev_id == "previous_block_id"))
    
    def get_previous_node(self, block_id: str) -> PointerNode | None:
        """Get the previous node in the graph."""
        node = self.get_node(block_id)
        if not node:
            return None
        prev_id = node.get_previous()
        if not prev_id:
            return None
        return self.get_node(prev_id)
    
    def has_next(self, block_id: str) -> bool:
        """Check if the block has a next block in the graph."""
        node = self.get_node(block_id)
        if not node:
            return False
        next_id = node.get_next()
        return bool(next_id and (next_id in self.nodes or next_id == "next_block_id"))
    
    def get_next_node(self, block_id: str) -> PointerNode | None:
        """Get the next node in the graph."""
        node = self.get_node(block_id)
        if not node:
            return None
        next_id = node.get_next()
        if not next_id:
            return None
        return self.get_node(next_id)
    
    def has_refines(self, block_id: str) -> bool:
        """Check if the block has a refines target."""
        node = self.get_node(block_id)
        if not node:
            return False
        refines_id = node.get_refines()
        return bool(refines_id and (refines_id in self.nodes or refines_id == "refines_block_id"))
    
    def get_refines_node(self, block_id: str) -> PointerNode | None:
        """Get the node that this block refines."""
        node = self.get_node(block_id)
        if not node:
            return None
        refines_id = node.get_refines()
        if not refines_id:
            return None
        return self.get_node(refines_id)
    
    def get_resume_anchor(self, block_id: str) -> str:
        """Get the resume anchor block ID for continuation after rewrite."""
        node = self.get_node(block_id)
        if not node:
            return ""
        return node.get_resume_from()


def get_previous_block_id(node: PointerNode | dict[str, Any]) -> str:
    """Extract previous block ID from a pointer node or dictionary."""
    if isinstance(node, dict):
        return str(node.get("previous_block_id") or "")
    return node.get_previous() if hasattr(node, 'get_previous') else ""


def get_next_block_id(node: PointerNode | dict[str, Any]) -> str:
    """Extract next block ID from a pointer node or dictionary."""
    if isinstance(node, dict):
        return str(node.get("next_block_id") or "")
    return node.get_next() if hasattr(node, 'get_next') else ""


def get_refines_block_id(node: PointerNode | dict[str, Any]) -> str:
    """Extract refines block ID from a pointer node or dictionary."""
    if isinstance(node, dict):
        return str(node.get("refines_block_id") or "")
    return node.get_refines() if hasattr(node, 'get_refines') else ""


def get_resume_from_block_id(node: PointerNode | dict[str, Any]) -> str:
    """Extract resume from block ID from a pointer node or dictionary."""
    if isinstance(node, dict):
        return str(node.get("resume_from_block_id") or "")
    return node.get_resume_from() if hasattr(node, 'get_resume_from') else ""


def has_previous(block_id: str, graph: PointerGraph) -> bool:
    """Check if a block has a previous block in the pointer graph."""
    return graph.has_previous(block_id)


def has_next(block_id: str, graph: PointerGraph) -> bool:
    """Check if a block has a next block in the pointer graph."""
    return graph.has_next(block_id)


def has_refines(block_id: str, graph: PointerGraph) -> bool:
    """Check if a block has a refines target in the pointer graph."""
    return graph.has_refines(block_id)


__all__ = [
    "PointerNode",
    "PointerGraph",
    "get_previous_block_id",
    "get_next_block_id",
    "get_refines_block_id",
    "get_resume_from_block_id",
    "has_previous",
    "has_next",
    "has_refines",
]