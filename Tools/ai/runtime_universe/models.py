"""Models for the repository runtime universe."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class RepoRuntimeUniverse:
    repo_root: str
    file_index: list[str]
    source_index: list[str]
    docs_index: list[str]
    validation_index: list[str]
    output_artifact_index: list[str]
    asset_index: list[str] = field(default_factory=list)
    tool_catalog: list[dict[str, object]] = field(default_factory=list)
    tool_catalog_refs: list[str] = field(default_factory=list)
    memory_inventory_refs: list[str] = field(default_factory=list)
    context_chunk_refs: list[str] = field(default_factory=list)
    semantic_chunk_refs: list[str] = field(default_factory=list)
    startup_manifest_refs: list[str] = field(default_factory=list)

    def summary(self) -> dict[str, object]:
        return {
            "repo_root": self.repo_root,
            "file_count": len(self.file_index),
            "source_count": len(self.source_index),
            "docs_count": len(self.docs_index),
            "validation_count": len(self.validation_index),
            "asset_count": len(self.asset_index),
            "output_artifact_count": len(self.output_artifact_index),
            "tool_catalog_ref_count": len(self.tool_catalog_refs),
            "tool_catalog_count": len(self.tool_catalog),
            "memory_inventory_ref_count": len(self.memory_inventory_refs),
            "context_chunk_ref_count": len(self.context_chunk_refs),
            "semantic_chunk_ref_count": len(self.semantic_chunk_refs),
            "startup_manifest_ref_count": len(self.startup_manifest_refs),
            "startup_artifact_ref_count": self.startup_artifact_ref_count,
            "top_level_counts": self.top_level_counts(),
        }

    def top_level_counts(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for item in self.file_index:
            top = str(item).replace("\\", "/").split("/", 1)[0]
            counts[top] = counts.get(top, 0) + 1
        return dict(sorted(counts.items(), key=lambda pair: (-pair[1], pair[0])))

    @property
    def startup_artifact_ref_count(self) -> int:
        return (
            len(self.tool_catalog_refs)
            + len(self.memory_inventory_refs)
            + len(self.context_chunk_refs)
            + len(self.semantic_chunk_refs)
            + len(self.startup_manifest_refs)
        )

    def as_dict(self) -> dict[str, object]:
        return {
            "schema_version": 1,
            "kind": "repo_runtime_universe",
            **self.summary(),
            "file_index": self.file_index,
            "source_index": self.source_index,
            "docs_index": self.docs_index,
            "validation_index": self.validation_index,
            "asset_index": self.asset_index,
            "output_artifact_index": self.output_artifact_index,
            "tool_catalog": self.tool_catalog,
            "tool_catalog_refs": self.tool_catalog_refs,
            "memory_inventory_refs": self.memory_inventory_refs,
            "context_chunk_refs": self.context_chunk_refs,
            "semantic_chunk_refs": self.semantic_chunk_refs,
            "startup_manifest_refs": self.startup_manifest_refs,
        }
