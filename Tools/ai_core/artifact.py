from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .io_utils import ensure_dir, write_json, write_text


@dataclass(slots=True)
class Artifact:
    name: str
    path: Path
    kind: str
    metadata: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "path": str(self.path).replace("\\", "/"),
            "kind": self.kind,
            "metadata": self.metadata,
        }


class ArtifactStore:
    """Writes pipeline run artifacts in a predictable per-run directory."""

    def __init__(self, base_dir: str | Path, *, run_id: str | None = None) -> None:
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        self.run_id = run_id or timestamp
        self.base_dir = ensure_dir(Path(base_dir) / self.run_id)
        self.artifacts: list[Artifact] = []

    def write_text(self, name: str, content: str, *, filename: str | None = None, metadata: dict[str, Any] | None = None) -> Artifact:
        target = write_text(self.base_dir / (filename or name), content)
        artifact = Artifact(name=name, path=target, kind="text", metadata=metadata or {})
        self.artifacts.append(artifact)
        return artifact

    def write_json(self, name: str, data: Any, *, filename: str | None = None, metadata: dict[str, Any] | None = None) -> Artifact:
        target = write_json(self.base_dir / (filename or name), data)
        artifact = Artifact(name=name, path=target, kind="json", metadata=metadata or {})
        self.artifacts.append(artifact)
        return artifact

    def manifest(self) -> dict[str, Any]:
        return {"run_id": self.run_id, "base_dir": str(self.base_dir), "artifacts": [item.to_dict() for item in self.artifacts]}

    def write_manifest(self) -> Path:
        return write_json(self.base_dir / "manifest.json", self.manifest())
