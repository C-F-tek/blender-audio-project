"""Legacy runtime wiring checks for NPU pipeline module smoke."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path
from typing import Any

from .imports import (
    MigrationReadinessCheck,
    build_creative_scene_prompt_payload,
    build_implementation_retry_payload,
    build_merge_prompt_payload,
    build_migration_readiness_report,
    compare_json_readers,
    compare_optional_json_readers,
    default_runtime_wiring_readiness,
    read_json,
    read_optional_json,
    runtime_common,
    runtime_pipeline,
    runtime_writers,
    summarize_music_context,
    write_json,
)

def build_runtime_context(
    repo_root: Path, music_context: dict[str, Any], raw_preflight: dict[str, Any]
) -> dict[str, object]:
    migration_readiness = default_runtime_wiring_readiness(
        local_validation_passed=True,
        indexes_regenerated=True,
    )
    forced_migration_readiness = build_migration_readiness_report(
        target_file="Tools/npu/dual_ai_pipeline/cli.py",
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
                'frames = keyframes.get("frames", [])\n'
                "obj = bpy.data.objects.new('Smoke', None)\n"
                "obj.keyframe_insert(data_path='location')\n"
                "obj.modifiers.new('Smoke', 'BEVEL')\n"
                "bpy.data.materials.new('Smoke')\n" + "# smoke\n" * 500
            ),
        }
    )
    runtime_project_index = runtime_pipeline.read_text(runtime_pipeline.PROJECT_INDEX_MD)
    runtime_creative_expected_payload = build_creative_scene_prompt_payload(
        music_context,
        npu_notes="technical smoke notes",
        project_index="project smoke index",
    )
    runtime_creative_prompt = runtime_pipeline.build_creative_scene_prompt(
        music_context,
        "technical smoke notes",
        "project smoke index",
    )
    runtime_merge_expected_payload = build_merge_prompt_payload(
        music_context,
        npu_notes="technical smoke notes",
        project_index=runtime_project_index,
        creative={"ok": True},
        technical={"ok": True},
    )
    runtime_merge_prompt = runtime_pipeline.build_merge_prompt(
        music_context,
        "technical smoke notes",
        {"ok": True},
        {"ok": True},
    )
    runtime_manifest = (
        runtime_pipeline.read_json(runtime_pipeline.PROJECT_MANIFEST_JSON)
        if runtime_pipeline.PROJECT_MANIFEST_JSON.exists()
        else {}
    )
    runtime_indexed_files = sorted(
        item.get("file") for item in runtime_manifest.get("files", []) if item.get("file")
    )
    runtime_preferred_files = [
        file_name
        for file_name in runtime_indexed_files
        if file_name in runtime_pipeline.PREFERRED_IMPLEMENTATION_FILES
    ]
    runtime_retry_validation = {"issues": ["smoke"]}
    runtime_retry_expected_payload = build_implementation_retry_payload(
        {"plan": True},
        preferred_existing_files=runtime_preferred_files,
        allowed_new_prefixes=runtime_pipeline.ALLOWED_NEW_PREFIXES,
        validation=runtime_retry_validation,
    )
    runtime_retry_prompt = runtime_pipeline.build_implementation_retry_prompt(
        {"plan": True},
        {"ignored": True},
        runtime_retry_validation,
    )
    runtime_prompt_payload_report = {
        "creative": (
            json.dumps(runtime_creative_expected_payload, indent=2, ensure_ascii=False)
            in runtime_creative_prompt
        ),
        "merge": (
            json.dumps(runtime_merge_expected_payload, indent=2, ensure_ascii=False)
            in runtime_merge_prompt
        ),
        "retry": (
            json.dumps(runtime_retry_expected_payload, indent=2, ensure_ascii=False)
            in runtime_retry_prompt
        ),
    }
    runtime_context_notes = runtime_pipeline.deterministic_technical_notes(
        music_context,
        {"files": [{"file": "Scripting/v61b/materials.py"}]},
        "smoke_context",
    )
    runtime_context_report = {
        "segment_count": (
            f"- Segment count: `{summarize_music_context(music_context)['segment_count']}`."
            in runtime_context_notes
        ),
        "duration": "- Duration: `12.5` seconds." in runtime_context_notes,
        "priority_file": "`Scripting/v61b/materials.py`" in runtime_context_notes,
    }
    runtime_policy_report = runtime_pipeline.legacy_runtime_output_policy_report()
    runtime_preflight_report = runtime_pipeline.normalize_npu_preflight_report(
        raw_preflight,
        npu_python="C:/npu/python.exe",
        npu_model_dir="C:/npu/model",
    )
    old_runtime_paths = {
        "root": runtime_pipeline.ROOT,
        "tools_dir": runtime_pipeline.TOOLS_DIR,
        "output_dir": runtime_pipeline.OUTPUT_DIR,
        "track_stem": runtime_pipeline.TRACK_STEM,
        "implementation_draft_json": runtime_pipeline.IMPLEMENTATION_DRAFT_JSON,
        "implementation_script": runtime_pipeline.IMPLEMENTATION_SCRIPT,
        "implementation_notes": runtime_pipeline.IMPLEMENTATION_NOTES,
    }
    runtime_artifact_write_report = {
        "support_exists": False,
        "support_content": False,
        "draft_records_support": False,
    }
    try:
        with tempfile.TemporaryDirectory() as tmp:
            runtime_root = Path(tmp)
            runtime_modules = (runtime_pipeline, runtime_common, runtime_writers)
            runtime_paths = {
                "ROOT": runtime_root,
                "TOOLS_DIR": runtime_root / "Tools" / "npu",
                "OUTPUT_DIR": runtime_root / "output",
                "TRACK_STEM": "Smoke Track",
                "IMPLEMENTATION_DRAFT_JSON": runtime_root
                / "output"
                / "Smoke Track_ai_implementation_draft.json",
                "IMPLEMENTATION_SCRIPT": runtime_root
                / "indexAI"
                / "scene_scripts"
                / "smoke_track_scene_builder_candidate.py",
                "IMPLEMENTATION_NOTES": runtime_root
                / "Tools"
                / "npu"
                / "context_artifacts"
                / "generated_implementation_notes.md",
            }
            for module in runtime_modules:
                for name, value in runtime_paths.items():
                    setattr(module, name, value)
            runtime_pipeline.IMPLEMENTATION_SCRIPT.parent.mkdir(parents=True, exist_ok=True)
            runtime_pipeline.write_implementation_draft(
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
                        'frames = keyframes.get("frames", [])\n'
                        "obj = bpy.data.objects.new('Smoke', None)\n"
                        "obj.keyframe_insert(data_path='location')\n"
                        "obj.modifiers.new('Smoke', 'BEVEL')\n"
                        "bpy.data.materials.new('Smoke')\n" + "# smoke\n" * 500
                    ),
                    "support_files": [
                        {
                            "file": "indexAI/scene_scripts/smoke_bundle/README.md",
                            "kind": "notes",
                            "content": "support",
                        }
                    ],
                    "notes": ["smoke"],
                    "files_to_review_before_applying": [],
                }
            )
            support_path = runtime_root / "indexAI" / "scene_scripts" / "smoke_bundle" / "README.md"
            written_draft = runtime_pipeline.read_json(runtime_pipeline.IMPLEMENTATION_DRAFT_JSON)
            runtime_artifact_write_report = {
                "support_exists": support_path.exists(),
                "support_content": support_path.read_text(encoding="utf-8") == "support\n",
                "draft_records_support": str(support_path)
                in written_draft.get("written_support_files", []),
            }
    finally:
        for module in (runtime_pipeline, runtime_common, runtime_writers):
            module.ROOT = old_runtime_paths["root"]
            module.TOOLS_DIR = old_runtime_paths["tools_dir"]
            module.OUTPUT_DIR = old_runtime_paths["output_dir"]
            module.TRACK_STEM = old_runtime_paths["track_stem"]
            module.IMPLEMENTATION_DRAFT_JSON = old_runtime_paths["implementation_draft_json"]
            module.IMPLEMENTATION_SCRIPT = old_runtime_paths["implementation_script"]
            module.IMPLEMENTATION_NOTES = old_runtime_paths["implementation_notes"]
    return {
        "migration_readiness": migration_readiness,
        "forced_migration_readiness": forced_migration_readiness,
        "reader_alias_report": reader_alias_report,
        "runtime_reader_report": runtime_reader_report,
        "runtime_optional_report": runtime_optional_report,
        "runtime_draft_contract": runtime_draft_contract,
        "runtime_project_index": runtime_project_index,
        "runtime_creative_expected_payload": runtime_creative_expected_payload,
        "runtime_creative_prompt": runtime_creative_prompt,
        "runtime_merge_expected_payload": runtime_merge_expected_payload,
        "runtime_merge_prompt": runtime_merge_prompt,
        "runtime_manifest": runtime_manifest,
        "runtime_indexed_files": runtime_indexed_files,
        "runtime_preferred_files": runtime_preferred_files,
        "runtime_retry_validation": runtime_retry_validation,
        "runtime_retry_expected_payload": runtime_retry_expected_payload,
        "runtime_retry_prompt": runtime_retry_prompt,
        "runtime_prompt_payload_report": runtime_prompt_payload_report,
        "runtime_context_notes": runtime_context_notes,
        "runtime_context_report": runtime_context_report,
        "runtime_policy_report": runtime_policy_report,
        "runtime_preflight_report": runtime_preflight_report,
        "runtime_artifact_write_report": runtime_artifact_write_report,
    }
