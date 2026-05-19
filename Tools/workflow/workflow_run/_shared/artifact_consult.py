from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .artifact_catalog import ArtifactEntry, collect_artifact_entries, human_bytes, open_external


@dataclass(frozen=True)
class ArtifactRecord:
    index: int
    key: str
    path: Path
    category: str
    exists: bool
    size: int


def collect_artifacts(session: Any, *, include_existing_only: bool = False) -> list[ArtifactRecord]:
    entries = collect_artifact_entries(
        session,
        include_existing_only=include_existing_only,
        include_render_siblings=True,
    )
    return [_record_from_entry(index, entry) for index, entry in enumerate(entries, start=1)]


def format_artifact_table(records: list[ArtifactRecord]) -> str:
    lines = [
        "=" * 96,
        "ARTEFATTI PRODOTTI",
        "=" * 96,
        f"Totale: {len(records)}",
        "",
        f"{'#':>3}  {'OK':<7} {'TYPE':<8} {'SIZE':>10}  {'KEY':<34} PATH",
        "-" * 96,
    ]
    for item in records:
        ok = "OK" if item.exists else "MISS"
        lines.append(
            f"{item.index:>3}  {ok:<7} {item.category:<8} {human_bytes(item.size):>10}  "
            f"{item.key[:34]:<34} {item.path}"
        )
    return "\n".join(lines)


def open_artifact(
    records: list[ArtifactRecord], index: int, *, folder: bool = False
) -> ArtifactRecord:
    for item in records:
        if item.index == index:
            target = item.path.parent if folder and not item.path.is_dir() else item.path
            open_external(target)
            return item
    raise ValueError(f"Indice artefatto non valido: {index}")


def _record_from_entry(index: int, entry: ArtifactEntry) -> ArtifactRecord:
    return ArtifactRecord(
        index=index,
        key=entry.key,
        path=entry.path,
        category=entry.category,
        exists=entry.exists,
        size=entry.size,
    )
