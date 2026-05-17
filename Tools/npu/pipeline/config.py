from __future__ import annotations

import re
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

DEFAULT_TRACK_STEM = "Feel The Light-Luca Vera_Master"

DEFAULT_ALLOWED_ARTIFACT_PREFIXES = (
    "indexAI/scene_scripts/",
    "indexAI/patch_library/",
)

DEFAULT_PREFERRED_REFERENCE_FILES = (
    "Scripting/v61b/materials.py",
    "Scripting/v61b/fog_dynamics.py",
    "Scripting/v61b/physics_setup.py",
    "Scripting/v61b/scene_tuning_panel.py",
    "Scripting/v61b/config.py",
    "Scripting/v61b/render_setup.py",
    "Scripting/v61b/hot_update_scene_v61b.py",
)


def slugify_track_stem(value: str, max_len: int = 72) -> str:
    slug = re.sub(r"[^A-Za-z0-9]+", "_", value).strip("_").lower()
    return slug[:max_len] or "track"


@dataclass(frozen=True)
class DualPipelinePaths:
    """Resolved repository paths used by the dual AI pipeline.

    The object is intentionally data-only: it must not read files, load models,
    invoke Blender, or call external providers.
    """

    repo_root: Path
    track_stem: str = DEFAULT_TRACK_STEM
    analysis_ai_context: Path | None = None

    @property
    def tools_dir(self) -> Path:
        return self.repo_root / "Tools" / "npu"

    @property
    def output_dir(self) -> Path:
        return self.repo_root / "output"

    @property
    def music_ai_context(self) -> Path:
        if self.analysis_ai_context is not None:
            return self.analysis_ai_context
        return self.output_dir / f"{self.track_stem}_analysis_ai_context.json"

    @property
    def dual_plan_json(self) -> Path:
        return self.output_dir / f"{self.track_stem}_dual_ai_scene_plan.json"

    @property
    def ollama_insights_json(self) -> Path:
        return self.output_dir / f"{self.track_stem}_ollama_music_insights.json"

    @property
    def implementation_draft_json(self) -> Path:
        return self.output_dir / f"{self.track_stem}_ai_implementation_draft.json"

    @property
    def implementation_script(self) -> Path:
        slug = slugify_track_stem(self.track_stem)
        return self.repo_root / "indexAI" / "scene_scripts" / f"{slug}_scene_builder_candidate.py"

    @property
    def implementation_notes(self) -> Path:
        return self.tools_dir / "context_artifacts" / "generated_implementation_notes.md"


@dataclass(frozen=True)
class NpuPipelineConfig:
    """Pure configuration boundary for future NPU pipeline decomposition."""

    paths: DualPipelinePaths
    allowed_artifact_prefixes: tuple[str, ...] = DEFAULT_ALLOWED_ARTIFACT_PREFIXES
    preferred_reference_files: tuple[str, ...] = DEFAULT_PREFERRED_REFERENCE_FILES
    npu_chunk_tokens: int = 320
    npu_reduce_tokens: int = 512
    npu_final_tokens: int = 768
    include_manual_index: bool = False

    @classmethod
    def from_repo_root(
        cls,
        repo_root: str | Path,
        *,
        track_stem: str = DEFAULT_TRACK_STEM,
        analysis_ai_context: str | Path | None = None,
        allowed_artifact_prefixes: Iterable[str] = DEFAULT_ALLOWED_ARTIFACT_PREFIXES,
        preferred_reference_files: Iterable[str] = DEFAULT_PREFERRED_REFERENCE_FILES,
        include_manual_index: bool = False,
    ) -> NpuPipelineConfig:
        analysis_path = Path(analysis_ai_context) if analysis_ai_context else None
        paths = DualPipelinePaths(
            repo_root=Path(repo_root),
            track_stem=track_stem,
            analysis_ai_context=analysis_path,
        )
        return cls(
            paths=paths,
            allowed_artifact_prefixes=tuple(allowed_artifact_prefixes),
            preferred_reference_files=tuple(preferred_reference_files),
            include_manual_index=include_manual_index,
        )
