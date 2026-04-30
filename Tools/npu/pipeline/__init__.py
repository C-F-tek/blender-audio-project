"""App-agnostic helpers for the local NPU/Ollama pipeline.

Phase 1 keeps this package additive. Existing CLI entrypoints continue to own
orchestration until a later validated migration wires these helpers in.
"""

from .config import (
    DEFAULT_ALLOWED_ARTIFACT_PREFIXES,
    DEFAULT_PREFERRED_REFERENCE_FILES,
    DualPipelinePaths,
    NpuPipelineConfig,
)
from .prompts import (
    build_creative_scene_prompt_payload,
    build_implementation_retry_payload,
    build_merge_prompt_payload,
    compact_segments_for_prompt,
)
from .artifact_paths import (
    is_allowed_generated_artifact_path,
    normalize_repo_relative_path,
    validate_generated_artifact_paths,
)

__all__ = [
    "DEFAULT_ALLOWED_ARTIFACT_PREFIXES",
    "DEFAULT_PREFERRED_REFERENCE_FILES",
    "DualPipelinePaths",
    "NpuPipelineConfig",
    "build_creative_scene_prompt_payload",
    "build_implementation_retry_payload",
    "build_merge_prompt_payload",
    "compact_segments_for_prompt",
    "is_allowed_generated_artifact_path",
    "normalize_repo_relative_path",
    "validate_generated_artifact_paths",
]
