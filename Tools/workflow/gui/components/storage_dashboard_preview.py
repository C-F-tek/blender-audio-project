from __future__ import annotations

import json
from pathlib import Path

from components.storage_dashboard_model import (
    PathStats,
    human_bytes,
    immediate_children_stats,
)


def build_overview_text(
    root_dir: Path,
    project_dir: Path,
    root_stats: PathStats,
    project_stats: PathStats,
    outside_stats: list[PathStats],
) -> str:
    lines = [
        "STORAGE OVERVIEW",
        "=" * 80,
        f"Blender root: {root_dir}",
        f"Project dir:  {project_dir}",
        "",
        f"Root totale:     {human_bytes(root_stats.bytes)} | files={root_stats.files} dirs={root_stats.dirs}",
        f"Project totale:  {human_bytes(project_stats.bytes)} | files={project_stats.files} dirs={project_stats.dirs}",
        "",
        "Elementi dentro blender ma fuori da blender-audio-project:",
    ]
    if not outside_stats:
        lines.append("  Nessun elemento rilevato fuori dal progetto.")
    for item in outside_stats[:60]:
        lines.append(
            f"  - {item.path.name}: {human_bytes(item.bytes)} | files={item.files} dirs={item.dirs} | {item.path}"
        )
    if len(outside_stats) > 60:
        lines.append(f"  ... altri {len(outside_stats) - 60} elementi")
    lines.extend(
        [
            "",
            "Clicca sulle intestazioni Nome/Tipo/Dimensione/File/Dir/Percorso per ordinare.",
            "Doppio click su una riga per aprire file/cartella.",
            "Usa Open folder per aprire la cartella che contiene il file selezionato.",
        ]
    )
    return "\n".join(lines)


def build_directory_preview(path: Path) -> str:
    children = immediate_children_stats(path)
    lines = [f"Cartella: {path}", f"Elementi diretti: {len(children)}", ""]
    for child in children[:120]:
        lines.append(
            f"{child.path.name:<42} {human_bytes(child.bytes):>10} files={child.files:<6} dirs={child.dirs:<6}"
        )
    if len(children) > 120:
        lines.append(f"... altri {len(children) - 120} elementi")
    return "\n".join(lines)


def build_file_preview(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in {".json", ".md", ".txt", ".py", ".log", ".jsonl", ".csv"}:
        try:
            raw = path.read_text(encoding="utf-8", errors="replace")
            if suffix == ".json":
                try:
                    raw = json.dumps(json.loads(raw), indent=2, ensure_ascii=False)
                except Exception:
                    pass
            return raw[:100000] + ("\n\n<preview troncata>" if len(raw) > 100000 else "")
        except Exception as exc:
            return f"Errore lettura file:\n{path}\n\n{exc}"
    return (
        f"File: {path}\nDimensione: {human_bytes(path.stat().st_size)}"
        "\n\nDoppio click/Open per aprire esternamente."
    )
