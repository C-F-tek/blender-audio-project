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
from .context_builder import (
    ContextSlice,
    build_context_bundle,
    context_bundle_metrics,
    summarize_music_context,
)
from .io_utils import (
    read_json,
    read_json_object,
    read_optional_json,
    read_optional_json_object,
    read_text,
    write_json,
    write_json_object,
)
from .legacy_compat import (
    compare_json_readers,
    compare_optional_json_readers,
    compare_text_readers,
)
from .migration_readiness import (
    MigrationReadinessCheck,
    build_migration_readiness_report,
    default_runtime_wiring_readiness,
)
from .prompts import (
    build_creative_scene_prompt_payload,
    build_implementation_retry_payload,
    build_merge_prompt_payload,
    compact_segments_for_prompt,
)
from .providers import (
    ProviderRequest,
    ProviderResult,
    planned_provider_result,
    validate_provider_request,
)
from .reports import (
    build_helper_boundary_report,
    helper_boundary_passed,
)
from .runner import (
    PipelineStagePlan,
    build_default_stage_plan,
    stage_plan_report,
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
    "ContextSlice",
    "DualPipelinePaths",
    "MigrationReadinessCheck",
    "NpuPipelineConfig",
    "PipelineStagePlan",
    "PlannedArtifactWrite",
    "ProviderRequest",
    "ProviderResult",
    "REQUIRED_IMPLEMENTATION_DRAFT_KEYS",
    "build_context_bundle",
    "build_creative_scene_prompt_payload",
    "build_default_stage_plan",
    "build_helper_boundary_report",
    "build_implementation_retry_payload",
    "build_merge_prompt_payload",
    "build_migration_readiness_report",
    "compact_segments_for_prompt",
    "compare_json_readers",
    "compare_optional_json_readers",
    "compare_text_readers",
    "context_bundle_metrics",
    "default_runtime_wiring_readiness",
    "helper_boundary_passed",
    "is_allowed_generated_artifact_path",
    "normalize_repo_relative_path",
    "planned_provider_result",
    "read_json",
    "read_json_object",
    "read_optional_json",
    "read_optional_json_object",
    "read_text",
    "stage_plan_report",
    "summarize_music_context",
    "validate_generated_artifact_paths",
    "validate_implementation_draft_contract",
    "validate_json_object",
    "validate_planned_artifact_writes",
    "validate_provider_request",
    "validate_required_keys",
    "write_json",
    "write_json_object",
    "write_planned_artifact",
]
