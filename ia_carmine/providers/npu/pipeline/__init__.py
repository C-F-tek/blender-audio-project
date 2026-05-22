"""App-agnostic helpers for the local NPU/Ollama pipeline.

Existing CLI entrypoints own orchestration while validated migration phases wire
selected helpers in one group at a time.
"""

from .artifact_paths import (
    dual_ai_legacy_runtime_output_paths,
    is_allowed_generated_artifact_path,
    is_allowed_legacy_runtime_output_path,
    normalize_repo_relative_path,
    repo_relative_path,
    validate_generated_artifact_paths,
    validate_legacy_runtime_output_paths,
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
from .fixtures import (
    sample_implementation_draft_fixture,
    sample_music_context_fixture,
    sample_provider_request_fixture,
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
    ProviderParsedResult,
    ProviderRequest,
    ProviderResult,
    build_provider_result_report,
    normalize_provider_preflight_report,
    parse_provider_result,
    planned_provider_result,
    validate_provider_request,
)
from .reports import (
    COMMON_VALIDATION_REPORT_KEYS,
    RuntimeOutputManifestEntry,
    build_helper_boundary_report,
    build_runtime_output_manifest,
    build_validation_report,
    helper_boundary_passed,
    runtime_output_manifest_passed,
    validation_report_has_common_keys,
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
    "COMMON_VALIDATION_REPORT_KEYS",
    "DEFAULT_ALLOWED_ARTIFACT_PREFIXES",
    "DEFAULT_PREFERRED_REFERENCE_FILES",
    "ContextSlice",
    "DualPipelinePaths",
    "MigrationReadinessCheck",
    "NpuPipelineConfig",
    "PipelineStagePlan",
    "PlannedArtifactWrite",
    "ProviderParsedResult",
    "ProviderRequest",
    "ProviderResult",
    "REQUIRED_IMPLEMENTATION_DRAFT_KEYS",
    "RuntimeOutputManifestEntry",
    "build_context_bundle",
    "build_creative_scene_prompt_payload",
    "build_default_stage_plan",
    "build_helper_boundary_report",
    "build_implementation_retry_payload",
    "build_merge_prompt_payload",
    "build_migration_readiness_report",
    "build_provider_result_report",
    "build_runtime_output_manifest",
    "build_validation_report",
    "compact_segments_for_prompt",
    "compare_json_readers",
    "compare_optional_json_readers",
    "compare_text_readers",
    "context_bundle_metrics",
    "default_runtime_wiring_readiness",
    "dual_ai_legacy_runtime_output_paths",
    "helper_boundary_passed",
    "is_allowed_legacy_runtime_output_path",
    "is_allowed_generated_artifact_path",
    "normalize_provider_preflight_report",
    "normalize_repo_relative_path",
    "parse_provider_result",
    "planned_provider_result",
    "read_json",
    "read_json_object",
    "read_optional_json",
    "read_optional_json_object",
    "read_text",
    "repo_relative_path",
    "runtime_output_manifest_passed",
    "sample_implementation_draft_fixture",
    "sample_music_context_fixture",
    "sample_provider_request_fixture",
    "stage_plan_report",
    "summarize_music_context",
    "validate_generated_artifact_paths",
    "validate_implementation_draft_contract",
    "validate_json_object",
    "validate_legacy_runtime_output_paths",
    "validate_planned_artifact_writes",
    "validate_provider_request",
    "validate_required_keys",
    "validation_report_has_common_keys",
    "write_json",
    "write_json_object",
    "write_planned_artifact",
]
