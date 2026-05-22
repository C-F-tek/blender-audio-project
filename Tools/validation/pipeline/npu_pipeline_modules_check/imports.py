"""Imports for NPU pipeline module smoke checks."""

from __future__ import annotations

import sys
from pathlib import Path

def _repo_root() -> Path:
    for candidate in Path(__file__).resolve().parents:
        if (candidate / ".git").exists() or (candidate / "Tools").is_dir():
            return candidate
    return Path(__file__).resolve().parents[4]


REPO_ROOT = _repo_root()
TOOLS_NPU = REPO_ROOT / "Tools" / "npu"
for path in (REPO_ROOT, TOOLS_NPU):
    text = str(path)
    if text not in sys.path:
        sys.path.insert(0, text)

import ia_carmine.providers.npu.dual_ai_pipeline as runtime_pipeline  # noqa: E402
from ia_carmine.providers.npu.dual_ai_pipeline import common as runtime_common  # noqa: E402
from ia_carmine.providers.npu.dual_ai_pipeline import writers as runtime_writers  # noqa: E402

from ia_carmine.providers.npu.pipeline import (  # noqa: E402
    DEFAULT_ALLOWED_ARTIFACT_PREFIXES,
    DualPipelinePaths,
    MigrationReadinessCheck,
    NpuPipelineConfig,
    PlannedArtifactWrite,
    ProviderRequest,
    RuntimeOutputManifestEntry,
    build_context_bundle,
    build_creative_scene_prompt_payload,
    build_default_stage_plan,
    build_helper_boundary_report,
    build_implementation_retry_payload,
    build_merge_prompt_payload,
    build_migration_readiness_report,
    build_runtime_output_manifest,
    build_validation_report,
    compact_segments_for_prompt,
    compare_json_readers,
    compare_optional_json_readers,
    context_bundle_metrics,
    default_runtime_wiring_readiness,
    dual_ai_legacy_runtime_output_paths,
    helper_boundary_passed,
    is_allowed_generated_artifact_path,
    is_allowed_legacy_runtime_output_path,
    normalize_provider_preflight_report,
    planned_provider_result,
    read_json,
    read_optional_json,
    read_optional_json_object,
    runtime_output_manifest_passed,
    stage_plan_report,
    summarize_music_context,
    validate_generated_artifact_paths,
    validate_implementation_draft_contract,
    validate_json_object,
    validate_legacy_runtime_output_paths,
    validate_planned_artifact_writes,
    validate_provider_request,
    validation_report_has_common_keys,
    write_json,
)
