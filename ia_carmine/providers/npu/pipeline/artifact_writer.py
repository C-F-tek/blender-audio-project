from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .artifact_paths import validate_generated_artifact_paths
from .io_utils import write_json_object


@dataclass(frozen=True)
class PlannedArtifactWrite:
    """A generated artifact write request that can be validated before writing."""

    repo_relative_path: str
    kind: str
    content: str | dict[str, Any]


def validate_planned_artifact_writes(
    planned_writes: list[PlannedArtifactWrite],
    *,
    allowed_prefixes: tuple[str, ...],
) -> dict[str, object]:
    """Validate artifact write destinations without touching the filesystem."""

    return validate_generated_artifact_paths(
        [write.repo_relative_path for write in planned_writes],
        allowed_prefixes=allowed_prefixes,
    )


def write_planned_artifact(
    repo_root: str | Path,
    planned_write: PlannedArtifactWrite,
    *,
    allowed_prefixes: tuple[str, ...],
) -> Path:
    """Write one validated generated artifact under the repository root."""

    validation = validate_planned_artifact_writes(
        [planned_write],
        allowed_prefixes=allowed_prefixes,
    )
    if not validation["ok"]:
        raise ValueError(f"Refusing to write artifact outside allowed prefixes: {validation}")

    output_path = Path(repo_root) / planned_write.repo_relative_path
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if isinstance(planned_write.content, dict):
        write_json_object(output_path, planned_write.content)
    else:
        output_path.write_text(str(planned_write.content), encoding="utf-8")

    return output_path
