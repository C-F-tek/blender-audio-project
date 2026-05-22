"""Boundary report builder for NPU pipeline module smoke."""

from __future__ import annotations

from .imports import (
    build_helper_boundary_report,
    helper_boundary_passed,
    runtime_output_manifest_passed,
    validation_report_has_common_keys,
)

def build_boundary_context(context: dict[str, object]) -> dict[str, object]:
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
    repo_root = context["repo_root"]
    boundary_report = build_helper_boundary_report(
        package_name="ia_carmine.providers.npu.pipeline",
        modules=[
            "artifact_paths",
            "artifact_writer",
            "config",
            "context_builder",
            "io_utils",
            "legacy_compat",
            "migration_readiness",
            "prompts",
            "providers",
            "reports",
            "runner",
            "validators",
        ],
        checks={
            "paths": path_report.get("ok") is False,
            "planned_write": planned_write_report.get("ok") is True,
            "draft_contract": draft_report.get("ok") is True,
            "provider_boundary": provider_result.ok is True,
            "provider_preflight_normalization": provider_preflight.get("kind")
            == "provider_preflight",
            "legacy_runtime_output_policy": legacy_runtime_path_report.get("invalid_paths")
            == ["Tools/npu/not_a_runtime_output.md"],
            "common_validation_report": validation_report_has_common_keys(common_validation_report),
            "runtime_output_manifest_allowed": runtime_output_manifest_passed(
                runtime_output_manifest_allowed
            ),
            "runtime_output_manifest_blocks_unknown": runtime_output_manifest.get("blocked_count")
            == 1,
            "legacy_compat": optional_alias_report.get("ok") is True
            and reader_alias_report.get("ok") is True,
            "runtime_io_wiring": runtime_reader_report.get("ok") is True
            and runtime_optional_report.get("ok") is True,
            "runtime_contract_wiring": runtime_draft_contract.get("contract_validation", {}).get(
                "ok"
            )
            is True,
            "runtime_prompt_payload_wiring": all(runtime_prompt_payload_report.values()),
            "runtime_context_summary_wiring": all(runtime_context_report.values()),
            "runtime_artifact_write_planning": all(runtime_artifact_write_report.values()),
            "runtime_legacy_output_policy": runtime_policy_report.get("ok") is True,
            "runtime_provider_preflight_normalization": runtime_preflight_report.get("provider")
            == "openvino_npu",
            "migration_gate_blocks_runtime": migration_readiness.get("ready") is False,
        },
    )
    return {"boundary_report": boundary_report}
