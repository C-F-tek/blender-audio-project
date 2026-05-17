"""Typed runtime file reference models."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path


class RuntimeRefKind(str, Enum):
    SOURCE = "source"
    TEST = "test"
    VALIDATION_COMMAND_REF = "validation_command_ref"
    OUTPUT_ARTIFACT = "output_artifact"
    GENERATED_ARTIFACT = "generated_artifact"
    DOCS = "docs"
    CONFIG = "config"
    ASSET = "asset"
    UNKNOWN = "unknown"


class RuntimeRefStatus(str, Enum):
    VERIFIED = "verified"
    MISSING = "missing"
    AMBIGUOUS = "ambiguous"
    REJECTED_NON_ALLOWLISTED = "rejected_non_allowlisted"
    OUTPUT_ONLY = "output_only"
    VALIDATION_ONLY = "validation_only"
    UNSAFE = "unsafe"


class RuntimeRefProvenance(str, Enum):
    PROVIDER = "provider"
    STARTUP_CONTEXT = "startup_context"
    SEMANTIC_CHUNKS = "semantic_chunks"
    WORKTREE = "worktree"
    BROKER_RESULT = "broker_result"
    MATRIX_REPORT = "matrix_report"
    VALIDATION_REPORT = "validation_report"
    OPERATOR_REQUEST = "operator_request"
    STATIC_CONFIG = "static_config"
    TOOL_REQUEST = "tool_request"


class RuntimeConsumer(str, Enum):
    PROVIDER_CONTEXT = "provider_context"
    BROKER_TOOL = "broker_tool"
    MATRIX = "matrix"
    LAB = "lab"
    FINAL_ASSEMBLER = "final_assembler"


@dataclass(frozen=True)
class RuntimeFileRef:
    raw: str
    repo_relative: str
    absolute_path: str
    exists: bool
    is_file: bool
    kind: RuntimeRefKind
    provenance: RuntimeRefProvenance
    status: RuntimeRefStatus
    consumers: tuple[RuntimeConsumer, ...] = field(default_factory=tuple)
    reason: str = ""

    @property
    def patchable(self) -> bool:
        return self.status == RuntimeRefStatus.VERIFIED and self.kind not in {
            RuntimeRefKind.OUTPUT_ARTIFACT,
            RuntimeRefKind.GENERATED_ARTIFACT,
        }

    @property
    def validation_only(self) -> bool:
        return self.status == RuntimeRefStatus.VALIDATION_ONLY

    @property
    def output_only(self) -> bool:
        return self.status == RuntimeRefStatus.OUTPUT_ONLY

    def as_dict(self) -> dict[str, object]:
        return {
            "raw": self.raw,
            "repo_relative": self.repo_relative,
            "absolute_path": self.absolute_path,
            "exists": self.exists,
            "is_file": self.is_file,
            "kind": self.kind.value,
            "provenance": self.provenance.value,
            "status": self.status.value,
            "consumers": [item.value for item in self.consumers],
            "reason": self.reason,
            "patchable": self.patchable,
        }

    @classmethod
    def from_path(
        cls,
        *,
        raw: str,
        repo_root: Path,
        repo_relative: str,
        kind: RuntimeRefKind,
        provenance: RuntimeRefProvenance,
        status: RuntimeRefStatus,
        consumers: tuple[RuntimeConsumer, ...],
        reason: str = "",
    ) -> "RuntimeFileRef":
        path = repo_root / repo_relative if repo_relative else repo_root / raw
        return cls(
            raw=raw,
            repo_relative=repo_relative,
            absolute_path=str(path.resolve(strict=False)),
            exists=path.exists(),
            is_file=path.is_file(),
            kind=kind,
            provenance=provenance,
            status=status,
            consumers=consumers,
            reason=reason,
        )
