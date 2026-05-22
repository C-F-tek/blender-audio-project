"""Optional bridge to NPU music-context helpers."""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .defaults import DEFAULT_OLLAMA_MODEL


@dataclass(frozen=True)
class MusicContextBridge:
    """Call optional NPU context builders without making them hard dependencies."""

    repo_root: Path

    @property
    def tools_dir(self) -> Path:
        return self.repo_root / "Tools" / "npu"

    def _ensure_tools_path(self) -> bool:
        tools_dir = self.tools_dir
        if not tools_dir.exists():
            return False
        tools_path = str(tools_dir)
        if tools_path not in sys.path:
            sys.path.insert(0, tools_path)
        return True

    def build_ai_memory_context(self, track_stem: str, output_dir: Path) -> dict[str, Any]:
        if not self._ensure_tools_path():
            return {}
        try:
            from ia_carmine.providers.npu.provider_mesh._shared.ai_memory_context import build_ai_memory_context

            result = build_ai_memory_context(track_stem=track_stem, output_dir=output_dir)
        except Exception:
            return {}
        return result if isinstance(result, dict) else {}

    def build_music_context(
        self,
        *,
        analysis_path: Path,
        track_summary_path: Path,
        compact_json_path: Path,
        analysis_ai_context_path: Path | None = None,
        blender_keyframes_path: Path | None = None,
        scene_files: list[Path] | None = None,
        run_ollama: bool = False,
        ollama_model: str = DEFAULT_OLLAMA_MODEL,
    ) -> dict[str, Any] | None:
        if not self._ensure_tools_path():
            return None
        try:
            from build_music_context import build_music_context

            kwargs: dict[str, Any] = {
                "analysis_path": analysis_path,
                "track_summary_path": track_summary_path,
                "compact_json_path": compact_json_path,
                "run_ollama": run_ollama,
                "ollama_model": ollama_model,
            }
            if analysis_ai_context_path is not None:
                kwargs["analysis_ai_context_path"] = analysis_ai_context_path
            if blender_keyframes_path is not None:
                kwargs["blender_keyframes_path"] = blender_keyframes_path
            if scene_files is not None:
                kwargs["scene_files"] = scene_files
            manifest = build_music_context(**kwargs)
        except Exception as exc:
            print(f"[WARN] NPU music context not updated: {exc}")
            return None
        if isinstance(manifest, dict) and manifest.get("context_md"):
            print(f"[OK] NPU music context updated: {manifest['context_md']}")
        return manifest if isinstance(manifest, dict) else None
