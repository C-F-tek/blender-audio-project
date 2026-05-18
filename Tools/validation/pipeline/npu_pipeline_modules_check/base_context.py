"""Base pure-helper context for NPU pipeline module smoke."""

from __future__ import annotations

from pathlib import Path

from .imports import (
    DEFAULT_ALLOWED_ARTIFACT_PREFIXES,
    DualPipelinePaths,
    NpuPipelineConfig,
    PlannedArtifactWrite,
    ProviderRequest,
    RuntimeOutputManifestEntry,
    build_context_bundle,
    build_creative_scene_prompt_payload,
    build_default_stage_plan,
    build_implementation_retry_payload,
    build_merge_prompt_payload,
    build_runtime_output_manifest,
    build_validation_report,
    compact_segments_for_prompt,
    compare_optional_json_readers,
    context_bundle_metrics,
    dual_ai_legacy_runtime_output_paths,
    is_allowed_generated_artifact_path,
    is_allowed_legacy_runtime_output_path,
    normalize_provider_preflight_report,
    planned_provider_result,
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
)

def build_base_context(repo_root: Path) -> dict[str, object]:
    music_context = {
        "analysis_summary": {"duration_sec": 12.5, "fps": 30},
        "track_summary": {"estimated_tempo_bpm": 120},
        "scene_summaries": [{"name": "smoke"}],
        "segments": [
            {
                "index": 1,
                "start_sec": 0.0,
                "end_sec": 4.0,
                "dominant_band": "low",
                "intensity": "medium",
                "intensity_score": 0.5,
                "controls": {"low": 0.5},
                "top_events": list(range(10)),
            }
        ],
    }
    compact_segments = compact_segments_for_prompt(music_context)
    music_summary = summarize_music_context(music_context)
    context_bundle = build_context_bundle(
        music_context=music_context,
        project_index="project smoke index" * 100,
        npu_notes="technical smoke notes" * 100,
        max_project_index_chars=120,
        max_npu_notes_chars=90,
    )
    context_metrics = context_bundle_metrics(context_bundle)
    stage_plan = build_default_stage_plan(include_provider_stages=False)
    stage_report = stage_plan_report(stage_plan)
    common_validation_report = build_validation_report(
        kind="npu_pipeline_modules",
        repo_root=repo_root,
        passed=True,
        checks={"sample": True},
    )
    provider_request = ProviderRequest(
        provider="ollama",
        model="smoke-model",
        prompt="smoke prompt",
        max_tokens=128,
        metadata={"dry_run": True},
    )
    provider_validation = validate_provider_request(provider_request)
    provider_result = planned_provider_result(provider_request)
    invalid_provider_result = planned_provider_result(
        ProviderRequest(provider="", model="", prompt="", max_tokens=0)
    )
    raw_preflight = {
        "schema_version": 2,
        "ready": True,
        "mode": "npu_ready",
        "python_exe": "C:/npu/python.exe",
        "model_dir": "C:/npu/model",
        "python_exists": True,
        "model_dir_exists": True,
        "python_starts": True,
        "python_version": "3.13.0",
        "openvino_import": True,
        "openvino_genai_import": True,
        "openvino_available_devices": ["CPU", "NPU"],
        "npu_device_available": True,
        "recommended_workers": 4,
        "errors": [],
        "warnings": ["smoke"],
    }
    provider_preflight = normalize_provider_preflight_report(
        raw_preflight,
        provider="openvino_npu",
        model="smoke-model",
        executable="C:/npu/python.exe",
        model_dir="C:/npu/model",
    )
    creative_payload = build_creative_scene_prompt_payload(
        music_context,
        npu_notes="technical smoke notes",
        project_index="project smoke index",
    )
    merge_payload = build_merge_prompt_payload(
        music_context,
        npu_notes="technical smoke notes",
        project_index="project smoke index",
        creative={"ok": True},
        technical={"ok": True},
    )
    retry_payload = build_implementation_retry_payload(
        {"plan": True},
        preferred_existing_files=["Scripting/v61b/materials.py"],
        allowed_new_prefixes=DEFAULT_ALLOWED_ARTIFACT_PREFIXES,
        validation={"issues": ["smoke"]},
    )

    config = NpuPipelineConfig.from_repo_root(repo_root, track_stem="Smoke Track")
    paths = DualPipelinePaths(repo_root=repo_root, track_stem="Smoke Track")

    planned_write = PlannedArtifactWrite(
        repo_relative_path="indexAI/scene_scripts/smoke_candidate.py",
        kind="smoke",
        content="print('smoke')\n",
    )
    path_report = validate_generated_artifact_paths(
        [planned_write.repo_relative_path, "output/not_allowed.json"],
        allowed_prefixes=DEFAULT_ALLOWED_ARTIFACT_PREFIXES,
    )
    legacy_runtime_paths = dual_ai_legacy_runtime_output_paths("Smoke Track")
    legacy_runtime_path_report = validate_legacy_runtime_output_paths(
        [
            repo_root / "output" / "Smoke Track_dual_ai_scene_plan.json",
            "Tools/npu/npu_preflight_report.json",
            "Tools/npu/not_a_runtime_output.md",
        ],
        repo_root=repo_root,
        track_stem="Smoke Track",
    )
    runtime_output_manifest = build_runtime_output_manifest(
        repo_root=repo_root,
        entries=[
            RuntimeOutputManifestEntry(
                path="Tools/npu/npu_preflight_report.json",
                kind="provider_preflight_report",
                policy_source="legacy_runtime_output_policy",
                allowed=True,
                legacy=True,
                provider_execution_performed=False,
            ),
            RuntimeOutputManifestEntry(
                path="Tools/npu/not_a_runtime_output.md",
                kind="unknown",
                policy_source="legacy_runtime_output_policy",
                allowed=False,
                reason="not in exact legacy output allowlist",
            ),
        ],
        provider_execution_performed=False,
    )
    runtime_output_manifest_allowed = build_runtime_output_manifest(
        repo_root=repo_root,
        entries=[
            RuntimeOutputManifestEntry(
                path="Tools/npu/npu_preflight_report.json",
                kind="provider_preflight_report",
                policy_source="legacy_runtime_output_policy",
                allowed=True,
                legacy=True,
                provider_execution_performed=False,
            )
        ],
        provider_execution_performed=False,
    )
    planned_write_report = validate_planned_artifact_writes(
        [planned_write],
        allowed_prefixes=DEFAULT_ALLOWED_ARTIFACT_PREFIXES,
    )
    draft_report = validate_implementation_draft_contract(
        {
            "implementation_kind": "new_blender_scene_script_from_json",
            "safety": {"requires_manual_review": True},
            "reference_files": [],
            "proposed_files": [{"file": "indexAI/scene_scripts/smoke_candidate.py"}],
            "implementation_plan": [],
        }
    )
    json_object_report = validate_json_object({"ok": True}, label="smoke_object")
    missing_optional = read_optional_json_object(repo_root / "not_existing_optional_smoke.json")
    optional_alias_report = compare_optional_json_readers(
        repo_root / "not_existing_optional_smoke.json",
        read_optional_json_object,
        read_optional_json,
    )
    return {
        "music_context": music_context,
        "compact_segments": compact_segments,
        "music_summary": music_summary,
        "context_bundle": context_bundle,
        "context_metrics": context_metrics,
        "stage_plan": stage_plan,
        "stage_report": stage_report,
        "common_validation_report": common_validation_report,
        "provider_request": provider_request,
        "provider_validation": provider_validation,
        "provider_result": provider_result,
        "invalid_provider_result": invalid_provider_result,
        "raw_preflight": raw_preflight,
        "provider_preflight": provider_preflight,
        "creative_payload": creative_payload,
        "merge_payload": merge_payload,
        "retry_payload": retry_payload,
        "config": config,
        "paths": paths,
        "planned_write": planned_write,
        "path_report": path_report,
        "legacy_runtime_paths": legacy_runtime_paths,
        "legacy_runtime_path_report": legacy_runtime_path_report,
        "runtime_output_manifest": runtime_output_manifest,
        "runtime_output_manifest_allowed": runtime_output_manifest_allowed,
        "planned_write_report": planned_write_report,
        "draft_report": draft_report,
        "json_object_report": json_object_report,
        "missing_optional": missing_optional,
        "optional_alias_report": optional_alias_report,
    }
