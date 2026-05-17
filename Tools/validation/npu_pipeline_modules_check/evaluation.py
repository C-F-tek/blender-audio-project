"""Final report evaluation for NPU pipeline module smoke."""

from __future__ import annotations

from .imports import (
    DEFAULT_ALLOWED_ARTIFACT_PREFIXES,
    helper_boundary_passed,
    is_allowed_generated_artifact_path,
    is_allowed_legacy_runtime_output_path,
    runtime_output_manifest_passed,
    summarize_music_context,
    validation_report_has_common_keys,
)

def build_report_from_context(context: dict[str, object]) -> dict[str, object]:
    repo_root = context["repo_root"]
    music_context = context["music_context"]
    compact_segments = context["compact_segments"]
    music_summary = context["music_summary"]
    context_bundle = context["context_bundle"]
    context_metrics = context["context_metrics"]
    stage_plan = context["stage_plan"]
    stage_report = context["stage_report"]
    common_validation_report = context["common_validation_report"]
    provider_request = context["provider_request"]
    provider_validation = context["provider_validation"]
    provider_result = context["provider_result"]
    invalid_provider_result = context["invalid_provider_result"]
    raw_preflight = context["raw_preflight"]
    provider_preflight = context["provider_preflight"]
    creative_payload = context["creative_payload"]
    merge_payload = context["merge_payload"]
    retry_payload = context["retry_payload"]
    config = context["config"]
    paths = context["paths"]
    planned_write = context["planned_write"]
    path_report = context["path_report"]
    legacy_runtime_paths = context["legacy_runtime_paths"]
    legacy_runtime_path_report = context["legacy_runtime_path_report"]
    runtime_output_manifest = context["runtime_output_manifest"]
    runtime_output_manifest_allowed = context["runtime_output_manifest_allowed"]
    planned_write_report = context["planned_write_report"]
    draft_report = context["draft_report"]
    json_object_report = context["json_object_report"]
    missing_optional = context["missing_optional"]
    optional_alias_report = context["optional_alias_report"]
    migration_readiness = context["migration_readiness"]
    forced_migration_readiness = context["forced_migration_readiness"]
    reader_alias_report = context["reader_alias_report"]
    runtime_reader_report = context["runtime_reader_report"]
    runtime_optional_report = context["runtime_optional_report"]
    runtime_draft_contract = context["runtime_draft_contract"]
    runtime_project_index = context["runtime_project_index"]
    runtime_creative_expected_payload = context["runtime_creative_expected_payload"]
    runtime_creative_prompt = context["runtime_creative_prompt"]
    runtime_merge_expected_payload = context["runtime_merge_expected_payload"]
    runtime_merge_prompt = context["runtime_merge_prompt"]
    runtime_manifest = context["runtime_manifest"]
    runtime_indexed_files = context["runtime_indexed_files"]
    runtime_preferred_files = context["runtime_preferred_files"]
    runtime_retry_validation = context["runtime_retry_validation"]
    runtime_retry_expected_payload = context["runtime_retry_expected_payload"]
    runtime_retry_prompt = context["runtime_retry_prompt"]
    runtime_prompt_payload_report = context["runtime_prompt_payload_report"]
    runtime_context_notes = context["runtime_context_notes"]
    runtime_context_report = context["runtime_context_report"]
    runtime_policy_report = context["runtime_policy_report"]
    runtime_preflight_report = context["runtime_preflight_report"]
    runtime_artifact_write_report = context["runtime_artifact_write_report"]
    boundary_report = context["boundary_report"]
    errors: list[str] = []
    if len(compact_segments) != 1:
        errors.append("compact segment helper did not preserve one valid segment")
    if len(compact_segments[0].get("top_events", [])) != 6:
        errors.append("compact segment helper did not cap top_events to six entries")
    if music_summary.get("segment_count") != 1:
        errors.append("music summary did not preserve segment count")
    if context_metrics.get("slice_count") != 2:
        errors.append("context bundle metrics should report two slices")
    if context_metrics.get("clipped_chars") != 210:
        errors.append("context bundle did not apply deterministic clipping limits")
    if validation_report_has_common_keys(common_validation_report) is not True:
        errors.append("common validation report should expose the standard NPU report keys")
    if stage_report.get("stage_count") != 5:
        errors.append("default stage plan should include five stages")
    if stage_report.get("enabled_stage_count") != 4:
        errors.append("provider stage should be disabled by default in smoke plan")
    if provider_validation.get("ok") is not True:
        errors.append("valid provider request should pass validation")
    if provider_result.ok is not True or provider_result.metadata.get("executed") is not False:
        errors.append("planned provider result should be ok and non-executed")
    if invalid_provider_result.ok is not False or not invalid_provider_result.error:
        errors.append("invalid provider request should produce failed planned result")
    if provider_preflight.get("provider") != "openvino_npu":
        errors.append("provider preflight normalization did not preserve provider")
    if provider_preflight.get("provider_execution_performed") is not False:
        errors.append("provider preflight normalization must not claim provider execution")
    if provider_preflight.get("runtime", {}).get("recommended_workers") != 4:
        errors.append("provider preflight normalization did not preserve recommended workers")
    if creative_payload.get("npu_technical_notes") != "technical smoke notes":
        errors.append("creative payload did not preserve NPU notes")
    if merge_payload.get("ollama_creative") != {"ok": True}:
        errors.append("merge payload did not preserve creative payload")
    if retry_payload.get("previous_response_was_invalid") is not True:
        errors.append("retry payload did not mark invalid previous response")
    if paths.output_dir != repo_root / "output":
        errors.append("DualPipelinePaths output_dir mismatch")
    if config.paths.track_stem != "Smoke Track":
        errors.append("NpuPipelineConfig did not preserve track stem")
    if not is_allowed_generated_artifact_path("indexAI/scene_scripts/smoke.py"):
        errors.append("allowed artifact path was rejected")
    if is_allowed_generated_artifact_path("output/smoke.json"):
        errors.append("disallowed artifact path was accepted")
    if "Tools/npu/npu_preflight_report.json" not in legacy_runtime_paths:
        errors.append("legacy runtime output policy should include the NPU preflight report")
    if not is_allowed_legacy_runtime_output_path(
        repo_root / "Tools" / "npu" / "npu_preflight_report.json",
        repo_root=repo_root,
        track_stem="Smoke Track",
    ):
        errors.append("legacy runtime output policy rejected a known exact output")
    if legacy_runtime_path_report.get("ok") is not False:
        errors.append("legacy runtime output policy should reject unknown Tools/npu outputs")
    if runtime_output_manifest_passed(runtime_output_manifest_allowed) is not True:
        errors.append("runtime output manifest should pass when all entries are allowed")
    if runtime_output_manifest.get("blocked_count") != 1:
        errors.append("runtime output manifest should count blocked entries")
    if runtime_output_manifest.get("provider_execution_performed") is not False:
        errors.append(
            "runtime output manifest must not claim provider execution in smoke validation"
        )
    if path_report.get("ok") is not False:
        errors.append("mixed path report should fail when one path is outside allowed prefixes")
    if planned_write_report.get("ok") is not True:
        errors.append("planned write report should pass for allowed generated path")
    if draft_report.get("ok") is not True:
        errors.append(f"implementation draft contract should pass: {draft_report.get('issues')}")
    if json_object_report.get("ok") is not True:
        errors.append("JSON object validator rejected an object")
    if missing_optional != {}:
        errors.append("missing optional JSON should return empty object")
    if optional_alias_report.get("ok") is not True or reader_alias_report.get("ok") is not True:
        errors.append("legacy compatibility alias checks should pass")
    if runtime_reader_report.get("ok") is not True or runtime_optional_report.get("ok") is not True:
        errors.append("runtime IO helper wiring should preserve helper behavior")
    if runtime_draft_contract.get("contract_validation", {}).get("ok") is not True:
        errors.append(
            "runtime implementation draft validation should include passing helper contract validation"
        )
    if not all(runtime_prompt_payload_report.values()):
        errors.append("runtime prompt builders should embed helper-built payloads")
    if not all(runtime_context_report.values()):
        errors.append(
            "runtime deterministic notes should use helper-compatible context summary fields"
        )
    if not all(runtime_artifact_write_report.values()):
        errors.append(
            "runtime support-file writes should use planned artifact writes under allowed prefixes"
        )
    if runtime_policy_report.get("ok") is not True:
        errors.append("runtime legacy output policy should pass for known dual-AI outputs")
    if runtime_preflight_report.get("kind") != "provider_preflight":
        errors.append("runtime NPU preflight report should use provider preflight normalization")
    if migration_readiness.get("ready") is not False:
        errors.append("default migration readiness should block runtime wiring")
    if forced_migration_readiness.get("ready") is not True:
        errors.append("explicit positive migration readiness should pass")
    if boundary_report.get("module_count") != 12:
        errors.append("helper boundary report should list twelve modules")
    if helper_boundary_passed(boundary_report) is not True:
        errors.append("helper boundary report should pass all boolean checks")

    return {
        "schema_version": 1,
        "kind": "npu_pipeline_modules",
        "repo_root": str(repo_root),
        "passed": not errors,
        "errors": errors,
        "warnings": [],
        "checks": {
            "compact_segment_count": len(compact_segments),
            "music_summary": music_summary,
            "context_metrics": context_metrics,
            "stage_report": stage_report,
            "common_validation_report": common_validation_report,
            "provider_validation": provider_validation,
            "provider_result": provider_result.to_dict(),
            "invalid_provider_result": invalid_provider_result.to_dict(),
            "provider_preflight": provider_preflight,
            "legacy_runtime_path_report": legacy_runtime_path_report,
            "runtime_output_manifest": runtime_output_manifest,
            "runtime_output_manifest_allowed": runtime_output_manifest_allowed,
            "optional_alias_report": optional_alias_report,
            "reader_alias_report": reader_alias_report,
            "runtime_reader_report": runtime_reader_report,
            "runtime_optional_report": runtime_optional_report,
            "runtime_draft_contract": runtime_draft_contract.get("contract_validation"),
            "runtime_prompt_payload_report": runtime_prompt_payload_report,
            "runtime_context_report": runtime_context_report,
            "runtime_artifact_write_report": runtime_artifact_write_report,
            "runtime_policy_report": runtime_policy_report,
            "runtime_preflight_report": runtime_preflight_report,
            "migration_readiness": migration_readiness,
            "forced_migration_readiness": forced_migration_readiness,
            "boundary_report": boundary_report,
            "creative_payload_keys": sorted(creative_payload.keys()),
            "merge_payload_keys": sorted(merge_payload.keys()),
            "retry_payload_keys": sorted(retry_payload.keys()),
            "allowed_prefixes": list(DEFAULT_ALLOWED_ARTIFACT_PREFIXES),
            "path_report": path_report,
            "planned_write_report": planned_write_report,
            "draft_report": draft_report,
            "json_object_report": json_object_report,
        },
    }
