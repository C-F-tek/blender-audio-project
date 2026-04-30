#!/usr/bin/env python3
"""Smoke-check app-agnostic NPU pipeline helper modules.

This validator imports the `Tools.npu.pipeline` package and exercises only pure
helpers. It does not run Blender, NPU, GPU, Ollama, FFmpeg or provider calls.
"""
from __future__ import annotations

import argparse
import sys
import tempfile
from pathlib import Path

from report_utils import resolve_output_path, write_json_report


def check_npu_pipeline_modules(repo_root: Path) -> dict[str, object]:
    root_text = str(repo_root)
    if root_text not in sys.path:
        sys.path.insert(0, root_text)
    npu_tools_text = str(repo_root / "Tools" / "npu")
    if npu_tools_text not in sys.path:
        sys.path.insert(0, npu_tools_text)

    from Tools.npu.pipeline import (  # noqa: PLC0415
        DEFAULT_ALLOWED_ARTIFACT_PREFIXES,
        DualPipelinePaths,
        MigrationReadinessCheck,
        NpuPipelineConfig,
        PlannedArtifactWrite,
        ProviderRequest,
        build_context_bundle,
        build_creative_scene_prompt_payload,
        build_default_stage_plan,
        build_helper_boundary_report,
        build_implementation_retry_payload,
        build_merge_prompt_payload,
        build_migration_readiness_report,
        compact_segments_for_prompt,
        compare_json_readers,
        compare_optional_json_readers,
        context_bundle_metrics,
        default_runtime_wiring_readiness,
        helper_boundary_passed,
        is_allowed_generated_artifact_path,
        planned_provider_result,
        read_json,
        read_optional_json,
        read_optional_json_object,
        stage_plan_report,
        summarize_music_context,
        validate_generated_artifact_paths,
        validate_implementation_draft_contract,
        validate_json_object,
        validate_planned_artifact_writes,
        validate_provider_request,
        write_json,
    )
    import run_dual_ai_pipeline as runtime_pipeline  # noqa: PLC0415

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
    migration_readiness = default_runtime_wiring_readiness(
        local_validation_passed=True,
        indexes_regenerated=True,
    )
    forced_migration_readiness = build_migration_readiness_report(
        target_file="Tools/npu/run_dual_ai_pipeline.py",
        checks=[MigrationReadinessCheck("smoke", True, "smoke check")],
        allowed_to_modify_runtime=True,
    )
    reader_alias_report = compare_json_readers(
        repo_root / "not_existing_required_smoke.json",
        lambda _path: {},
        lambda _path: {},
    )
    with tempfile.TemporaryDirectory() as tmp:
        runtime_smoke_path = Path(tmp) / "runtime_smoke.json"
        write_json(runtime_smoke_path, {"runtime": True})
        runtime_reader_report = compare_json_readers(
            runtime_smoke_path,
            runtime_pipeline.read_json,
            read_json,
        )
        runtime_optional_report = compare_optional_json_readers(
            Path(tmp) / "missing_optional.json",
            runtime_pipeline.read_optional_json,
            read_optional_json,
        )
    runtime_draft_contract = runtime_pipeline.validate_implementation_draft(
        {
            "implementation_kind": "new_blender_scene_script_from_json",
            "safety": {"requires_manual_review": True},
            "reference_files": [{"file": "Scripting/v61b/materials.py"}],
            "proposed_files": [{"file": "indexAI/scene_scripts/smoke_candidate.py"}],
            "implementation_plan": [{"change": "smoke"}],
            "scene_script": (
                "import bpy\n"
                "import json\n"
                "def load_json(path): return {}\n"
                "keyframes = {'frames': []}\n"
                "frames = keyframes.get(\"frames\", [])\n"
                "obj = bpy.data.objects.new('Smoke', None)\n"
                "obj.keyframe_insert(data_path='location')\n"
                "obj.modifiers.new('Smoke', 'BEVEL')\n"
                "bpy.data.materials.new('Smoke')\n"
                + "# smoke\n" * 500
            ),
        }
    )
    boundary_report = build_helper_boundary_report(
        package_name="Tools.npu.pipeline",
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
            "legacy_compat": optional_alias_report.get("ok") is True and reader_alias_report.get("ok") is True,
            "runtime_io_wiring": runtime_reader_report.get("ok") is True and runtime_optional_report.get("ok") is True,
            "runtime_contract_wiring": runtime_draft_contract.get("contract_validation", {}).get("ok") is True,
            "migration_gate_blocks_runtime": migration_readiness.get("ready") is False,
        },
    )

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
        errors.append("runtime implementation draft validation should include passing helper contract validation")
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
            "provider_validation": provider_validation,
            "provider_result": provider_result.to_dict(),
            "invalid_provider_result": invalid_provider_result.to_dict(),
            "optional_alias_report": optional_alias_report,
            "reader_alias_report": reader_alias_report,
            "runtime_reader_report": runtime_reader_report,
            "runtime_optional_report": runtime_optional_report,
            "runtime_draft_contract": runtime_draft_contract.get("contract_validation"),
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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output", help="Optional JSON report path.")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    report = check_npu_pipeline_modules(repo_root)
    output = resolve_output_path(repo_root, args.output) if args.output else None
    text = write_json_report(report, output)
    print(text, end="")
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
