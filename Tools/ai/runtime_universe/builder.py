"""Build the local repository runtime universe from real files and artifacts."""

from __future__ import annotations

from pathlib import Path

from .models import RepoRuntimeUniverse
from .tool_catalog import broker_tool_catalog

DENY_DIR_PARTS = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    ".ruff_cache",
    "indexAI",
    "output",
    "renders",
}
HIDDEN_ALLOW_DIRS = {".github"}
SOURCE_SUFFIXES = {".py", ".ps1", ".json", ".yml", ".yaml", ".toml"}
DOC_SUFFIXES = {".md", ".txt", ".rst"}
ASSET_SUFFIXES = {
    ".blend",
    ".bmp",
    ".csv",
    ".exr",
    ".flac",
    ".gif",
    ".hdr",
    ".jpeg",
    ".jpg",
    ".lnk",
    ".mov",
    ".mp3",
    ".mp4",
    ".png",
    ".svg",
    ".tsv",
    ".wav",
    ".webp",
}
INDEXABLE_SUFFIXES = SOURCE_SUFFIXES | DOC_SUFFIXES | ASSET_SUFFIXES | {".patch", ".diff"}


def rel(repo_root: Path, path: Path) -> str:
    try:
        return path.resolve(strict=False).relative_to(repo_root.resolve(strict=False)).as_posix()
    except ValueError:
        return str(path)


def has_denied_part(path: Path) -> bool:
    return any(part in DENY_DIR_PARTS for part in path.parts)


def is_indexable_file(path: Path) -> bool:
    if path.suffix.lower() in INDEXABLE_SUFFIXES:
        return True
    return False


class RepoRuntimeUniverseBuilder:
    """Filesystem-first universe builder used before provider and matrix phases."""

    def __init__(self, repo_root: str | Path, run_dir: str | Path | None = None):
        self.repo_root = Path(repo_root).resolve()
        self.run_dir = Path(run_dir).resolve() if run_dir else None

    def _tracked_files(self) -> list[str]:
        out: list[str] = []
        for base in sorted(self.repo_root.iterdir(), key=lambda item: item.name.lower()):
            if base.is_dir():
                if base.name.startswith(".") and base.name not in HIDDEN_ALLOW_DIRS:
                    continue
                if has_denied_part(base):
                    continue
                for path in base.rglob("*"):
                    relative = rel(self.repo_root, path)
                    if (
                        path.is_file()
                        and not has_denied_part(path)
                        and is_indexable_file(path)
                    ):
                        out.append(relative)
            elif base.is_file() and is_indexable_file(base):
                out.append(rel(self.repo_root, base))
        return sorted(dict.fromkeys(out))

    def _output_artifacts(self) -> list[str]:
        artifacts: list[str] = []
        roots = []
        if self.run_dir and self.run_dir.exists():
            roots.append(self.run_dir)
        output_validation = self.repo_root / "output" / "validation"
        if output_validation.exists():
            roots.append(output_validation)
        for root in roots:
            for path in root.rglob("*"):
                if path.is_file() and path.suffix.lower() in {".json", ".md", ".txt", ".diff"}:
                    artifacts.append(rel(self.repo_root, path))
        return sorted(dict.fromkeys(artifacts))[:1000]

    def _startup_refs(self, artifacts: list[str], names: tuple[str, ...]) -> list[str]:
        lowered_names = tuple(item.lower() for item in names)
        return [item for item in artifacts if any(name in item.lower() for name in lowered_names)]

    def build(self) -> RepoRuntimeUniverse:
        files = self._tracked_files()
        artifacts = self._output_artifacts()
        sources = [
            item
            for item in files
            if Path(item).suffix.lower() in SOURCE_SUFFIXES
            and not item.startswith("docs/LOCAL_VALIDATION_EVIDENCE/")
        ]
        docs = [item for item in files if Path(item).suffix.lower() in DOC_SUFFIXES]
        validation = [item for item in files if item.startswith("Tools/validation/") and item.endswith(".py")]
        assets = [item for item in files if Path(item).suffix.lower() in ASSET_SUFFIXES]
        return RepoRuntimeUniverse(
            repo_root=str(self.repo_root),
            file_index=files,
            source_index=sources,
            docs_index=docs,
            validation_index=validation,
            output_artifact_index=artifacts,
            asset_index=assets,
            tool_catalog=broker_tool_catalog(),
            tool_catalog_refs=self._startup_refs(artifacts, ("tool_catalog", "tool_inventory")),
            memory_inventory_refs=self._startup_refs(artifacts, ("memory", "sqlite")),
            context_chunk_refs=self._startup_refs(artifacts, ("context", "ai_context_pack")),
            semantic_chunk_refs=self._startup_refs(artifacts, ("semantic", "chunk")),
            startup_manifest_refs=self._startup_refs(artifacts, ("startup", "manifest")),
        )
