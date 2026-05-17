from __future__ import annotations

from pathlib import Path
from typing import Any

from .capsules import json_capsules, text_capsules
from .core import read_json, read_text, rel


def discover(repo: Path, track: str, explicit: list[str]) -> list[Path]:
    paths: list[Path] = []
    for item in explicit:
        p = Path(item)
        if not p.is_absolute():
            p = repo / p
        if p.exists() and p.is_file():
            paths.append(p)
    paths.extend(_track_outputs(repo, track))
    paths.extend(_static_context_files(repo))
    return _unique_paths(paths)


def _track_outputs(repo: Path, track: str) -> list[Path]:
    out = repo / "output"
    names = [
        f"{track}_scene_brief.json",
        f"{track}_music_context.json",
        f"{track}_analysis_ai_context.json",
        f"{track}_analysis_blender_keyframes.json",
        f"{track}_dual_ai_scene_plan.json",
        f"{track}_ai_implementation_draft.json",
        "spaziotempo_asset_inventory.json",
    ]
    return [out / name for name in names if (out / name).exists()]


def _static_context_files(repo: Path) -> list[Path]:
    candidates = [
        repo / "docs" / "LOCAL_WORKSTATION_TARGET.md",
        repo / "indexAI" / "project_code_index.md",
        repo / "indexAI" / "project_code_manifest.json",
        repo / "indexAI" / "task_capsules" / "blender_51_compat.json",
        repo / "indexAI" / "task_capsules" / "resource_budget.json",
        repo / "Tools" / "npu" / "context_artifacts" / "npu_music_context.md",
        repo / "Tools" / "npu" / "context_artifacts" / "npu_code_index.md",
    ]
    return [path for path in candidates if path.exists()]


def _unique_paths(paths: list[Path]) -> list[Path]:
    seen: set[str] = set()
    unique: list[Path] = []
    for path in paths:
        key = str(path.resolve(strict=False)).lower()
        if key not in seen:
            seen.add(key)
            unique.append(path)
    return unique


def build_capsules(
    repo: Path, track: str, explicit: list[str], max_chars: int
) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for path in discover(repo, track, explicit):
        relative = rel(path, repo)
        source = path.stem
        if path.suffix.lower() == ".json":
            data = read_json(path)
            if data is not None:
                out.extend(json_capsules(source, relative, data, max_chars))
        elif path.suffix.lower() in {".md", ".txt", ".py"}:
            out.extend(text_capsules(source, relative, read_text(path), max_chars))
    return out
