"""IA-Carmine code chunks management with dynamic reconstruction capabilities."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class CodeChunk:
    """A semantic code chunk with navigation and concatenation support."""
    
    chunk_id: str = ""
    path: str = ""
    symbol: str = ""
    kind: str = "semantic_code_chunk"
    
    # Line range for reconstruction
    line_start: int = 1
    line_end: int = -1
    
    # Domain and metadata
    domain: list[str] = field(default_factory=lambda: ["code_chunks"])
    risk: str = "low"
    risk_signals: list[str] = field(default_factory=list)
    
    # Compatibility and dependencies
    compatibility_notes: list[str] = field(default_factory=list)
    dependencies: list[str] = field(default_factory=list)
    blender_api: list[str] = field(default_factory=list)
    
    # Content and summary
    summary_short: str = ""
    content_preview: str = ""
    do_not_change: bool = False
    
    # Hash and scoring
    sha256: str = ""
    score: int = 0
    matched_terms: list[str] = field(default_factory=list)
    
    def get_previous_chunk_id(self) -> str:
        """Return the previous chunk ID for sequential reconstruction."""
        return f"{self.chunk_id}:prev" if self.line_start > 1 else ""
    
    def get_next_chunk_id(self) -> str:
        """Return the next chunk ID for sequential reconstruction."""
        return f"{self.chunk_id}:next" if self.line_end < -1 or self.line_end > 0 else ""
    
    def can_concat_with(self, other: 'CodeChunk') -> bool:
        """Check if this chunk can be concatenated with another code chunk."""
        if self.path != other.path:
            return False
        # Check line continuity
        if other.line_start == self.line_end + 1 or other.line_start == self.line_end:
            return True
        return False


def build_code_chunk_sequence(
    chunks: list[dict[str, Any] | CodeChunk],
) -> list[CodeChunk]:
    """Build a sequence of code chunks from dictionary data."""
    result = []
    for item in chunks:
        if isinstance(item, dict):
            chunk = CodeChunk(
                chunk_id=item.get("chunk_id", ""),
                path=item.get("path", ""),
                symbol=item.get("symbol", ""),
                kind=item.get("kind", "semantic_code_chunk"),
                line_start=int(item.get("line_start", 1)),
                line_end=int(item.get("line_end", -1)),
                domain=item.get("domain", ["code_chunks"]),
                risk=str(item.get("risk", "low")),
                risk_signals=item.get("risk_signals", []),
                compatibility_notes=item.get("compatibility_notes", []),
                dependencies=item.get("dependencies", []),
                blender_api=item.get("blender_api", []),
                summary_short=str(item.get("summary_short", "")),
                content_preview=str(item.get("content_preview", "")),
                do_not_change=bool(item.get("do_not_change", False)),
                sha256=str(item.get("sha256", "")),
                score=int(item.get("score", 0)),
                matched_terms=item.get("matched_terms", []),
            )
        else:
            chunk = item
        result.append(chunk)
    return result


def concat_code_chunks(chunks: list[CodeChunk | dict[str, Any]]) -> str:
    """Concatenate code chunks to form complete text (chunk + chunk = testo completo)."""
    sorted_chunks = sorted(
        [c if isinstance(c, CodeChunk) else CodeChunk(**c) for c in chunks],
        key=lambda c: (c.path, c.line_start),
    )
    
    # Group by path and sort by line range
    by_path: dict[str, list[CodeChunk]] = {}
    for chunk in sorted_chunks:
        if chunk.path not in by_path:
            by_path[chunk.path] = []
        by_path[chunk.path].append(chunk)
    
    # Concatenate chunks for each path
    full_text_parts: dict[str, str] = {}
    for path, path_chunks in by_path.items():
        path_chunks.sort(key=lambda c: c.line_start if c.line_start > 0 else 999999)
        
        # Reconstruct complete text from chunks
        reconstructed_lines: list[str] = []
        for chunk in path_chunks:
            preview = str(chunk.content_preview or "")
            if preview:
                lines = preview.splitlines()
                reconstructed_lines.extend(lines)
        
        full_text_parts[path] = "\n".join(reconstructed_lines)
    
    # Return concatenated result
    return "\n\n--- SEPARATED BY PATH ---\n\n".join(
        [f"## {path}\n{text}" for path, text in full_text_parts.items()]
    )


def merge_code_chunks(chunks: list[CodeChunk | dict[str, Any]]) -> CodeChunk:
    """Merge multiple code chunks into a single unified chunk representation."""
    if not chunks:
        return CodeChunk()
    
    # Get first chunk as base
    base = chunks[0] if isinstance(chunks[0], CodeChunk) else CodeChunk(**chunks[0])
    
    # Aggregate metadata
    all_paths = set(str(c.path if isinstance(c, CodeChunk) else c.get("path", "")) for c in chunks)
    all_symbols = set(str(c.symbol if isinstance(c, CodeChunk) else c.get("symbol", "")) for c in chunks if getattr(c, 'symbol', None) or (isinstance(c, dict) and c.get('symbol')))
    
    merged = CodeChunk(
        chunk_id=f"merged_code_chunks:{len(chunks)}_chunks",
        path="/".join(list(all_paths)[:3]) if len(all_paths) <= 3 else f"{list(all_paths)[0]}+...",
        symbol=", ".join(list(all_symbols)[:3]) if all_symbols else "",
        kind="merged_semantic_code_chunks",
        line_start=min(getattr(c, 'line_start', 1) if isinstance(c, CodeChunk) else c.get('line_start', 1) for c in chunks),
        line_end=max(getattr(c, 'line_end', -1) if isinstance(c, CodeChunk) else c.get('line_end', -1) for c in chunks),
        domain=["merged_code_chunks"],
        risk="medium",
        compatibility_notes=["merged from multiple semantic code chunks"],
    )
    
    return merged