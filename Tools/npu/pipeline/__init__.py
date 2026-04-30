"""App-agnostic helpers for the local NPU/Ollama pipeline.

Existing CLI entrypoints continue to own orchestration until validated migration
phases wire these helpers in one group at a time.
"""

from .artifact_paths import (
    is_allowed_generated_artifact_path,
    normalize_repo_relative_path,
    validate_generated_artifact_paths,
)
from .artifact_writer import (
    PlannedArtifactWrite,
    validate_planned_artifact_writes,
    write_planned_artifact,
)
from .config import (
    DEFAULT_ALLOWED_ARTIFACT_PREFIXES,
    DEFAULT_PREFERRED_REFERENCE_FILES,
    DualPipelinePaths,
    NpuPipelineConfig,
)
from .io_utils import (
    read_json_object,
    read_optional_json_object,
    read_text,
    write_json_object,
)
from .prompts import (
    build_creative_scene_prompt_payload,
    build_implementation_retry_payload,
    build_merge_prompt_payload,
    compact_segments_for_prompt,
)
from .validators import (
    REQUIRED_IMPLEMENTATION_DRAFT_KEYS,
    validate_implementation_draft_contract,
    validate_json_object,
    validate_required_keys,
)

__all__ = [
    "DEFAULT_ALLOWED_ARTIFACT_PREFIXES",
    "DEFAULT_PREFERRED_REFERENCE_FILES",
    "DualPipelinePaths",
    "NpuPipelineConfig",
    "PlannedArtifactWrite",
    "REQUIRED_IMPLEMENTATION_DRAFT_KEYS",
    "build_creative_scene_prompt_payload",
    "build_implementation_retry_payload",
    "build_merge_prompt_payload",
    "compact_segments_for_prompt",
    "is_allowed_generated_artifact_path",
    "normalize_repo_relative_path",
    "read_json_object",
    "read_optional_json_object",
    "read_text",
    "validate_generated_artifact_paths",
    "validate_implementation_draft_contract",
    "validate_json_object",
    "validate_planned_artifact_writes",
    "validate_required_keys",
    "write_json_object",
    "write_planned_artifact",
]
