#!/usr/bin/env python3
"""Unit tests for app-agnostic NPU pipeline helpers.

These tests intentionally avoid Blender, NPU, GPU, Ollama, FFmpeg and filesystem
writes outside a temporary directory.
"""
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import sys

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from Tools.npu.pipeline import (  # noqa: E402
    DEFAULT_ALLOWED_ARTIFACT_PREFIXES,
    DualPipelinePaths,
    NpuPipelineConfig,
    PlannedArtifactWrite,
    ProviderRequest,
    build_context_bundle,
    build_default_stage_plan,
    build_helper_boundary_report,
    compact_segments_for_prompt,
    context_bundle_metrics,
    helper_boundary_passed,
    is_allowed_generated_artifact_path,
    planned_provider_result,
    read_json_object,
    read_optional_json_object,
    read_text,
    stage_plan_report,
    summarize_music_context,
    validate_generated_artifact_paths,
    validate_implementation_draft_contract,
    validate_json_object,
    validate_planned_artifact_writes,
    validate_provider_request,
    write_json_object,
    write_planned_artifact,
)


class NpuPipelineHelperTests(unittest.TestCase):
    def sample_music_context(self) -> dict[str, object]:
        return {
            "analysis_summary": {"duration_sec": 60.0, "fps": 30},
            "track_summary": {"estimated_tempo_bpm": 120.0},
            "scene_summaries": [{"name": "intro"}],
            "segments": [
                {
                    "index": 1,
                    "start_sec": 0.0,
                    "end_sec": 8.0,
                    "dominant_band": "low",
                    "intensity": "medium",
                    "intensity_score": 0.55,
                    "controls": {"low": 0.7},
                    "top_events": list(range(20)),
                }
            ],
        }

    def test_config_paths_are_data_only(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = DualPipelinePaths(repo_root=root, track_stem="Track A")
            config = NpuPipelineConfig.from_repo_root(root, track_stem="Track A")
            self.assertEqual(paths.output_dir, root / "output")
            self.assertEqual(paths.tools_dir, root / "Tools" / "npu")
            self.assertEqual(config.paths.track_stem, "Track A")
            self.assertEqual(config.allowed_artifact_prefixes, DEFAULT_ALLOWED_ARTIFACT_PREFIXES)

    def test_io_helpers(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            json_path = root / "nested" / "data.json"
            write_json_object(json_path, {"ok": True})
            self.assertEqual(read_json_object(json_path), {"ok": True})
            self.assertIn('"ok"', read_text(json_path))
            self.assertEqual(read_optional_json_object(root / "missing.json"), {})
            bad_path = root / "bad.json"
            bad_path.write_text("not json", encoding="utf-8")
            self.assertEqual(read_optional_json_object(bad_path), {})

    def test_artifact_path_policy(self) -> None:
        self.assertTrue(is_allowed_generated_artifact_path("indexAI/scene_scripts/a.py"))
        self.assertTrue(is_allowed_generated_artifact_path("indexAI/patch_library/a.json"))
        self.assertFalse(is_allowed_generated_artifact_path("output/a.json"))
        self.assertFalse(is_allowed_generated_artifact_path("../outside.json"))
        report = validate_generated_artifact_paths(
            ["indexAI/scene_scripts/a.py", "output/a.json"],
            allowed_prefixes=DEFAULT_ALLOWED_ARTIFACT_PREFIXES,
        )
        self.assertFalse(report["ok"])
        self.assertEqual(report["invalid_paths"], ["output/a.json"])

    def test_artifact_writer_validates_destination(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            planned = PlannedArtifactWrite(
                repo_relative_path="indexAI/scene_scripts/generated.py",
                kind="script",
                content="print('ok')\n",
            )
            report = validate_planned_artifact_writes(
                [planned],
                allowed_prefixes=DEFAULT_ALLOWED_ARTIFACT_PREFIXES,
            )
            self.assertTrue(report["ok"])
            written = write_planned_artifact(root, planned, allowed_prefixes=DEFAULT_ALLOWED_ARTIFACT_PREFIXES)
            self.assertEqual(written.read_text(encoding="utf-8"), "print('ok')\n")

            with self.assertRaises(ValueError):
                write_planned_artifact(
                    root,
                    PlannedArtifactWrite("output/blocked.json", "json", {"blocked": True}),
                    allowed_prefixes=DEFAULT_ALLOWED_ARTIFACT_PREFIXES,
                )

    def test_context_and_prompt_payload_helpers(self) -> None:
        music_context = self.sample_music_context()
        compact = compact_segments_for_prompt(music_context)
        self.assertEqual(len(compact), 1)
        self.assertEqual(len(compact[0]["top_events"]), 6)
        summary = summarize_music_context(music_context)
        self.assertEqual(summary["segment_count"], 1)
        bundle = build_context_bundle(
            music_context=music_context,
            project_index="p" * 500,
            npu_notes="n" * 300,
            max_project_index_chars=50,
            max_npu_notes_chars=40,
        )
        metrics = context_bundle_metrics(bundle)
        self.assertEqual(metrics["slice_count"], 2)
        self.assertEqual(metrics["clipped_chars"], 90)

    def test_validator_contracts_are_permissive(self) -> None:
        object_report = validate_json_object({"future": True}, label="future")
        self.assertTrue(object_report["ok"])
        draft_report = validate_implementation_draft_contract(
            {
                "implementation_kind": "new_blender_scene_script_from_json",
                "safety": {"requires_manual_review": True},
                "reference_files": [],
                "proposed_files": [{"file": "indexAI/scene_scripts/generated.py"}],
                "implementation_plan": [],
                "future_field": {"kept": True},
            }
        )
        self.assertTrue(draft_report["ok"])
        missing_report = validate_implementation_draft_contract({})
        self.assertFalse(missing_report["ok"])
        self.assertTrue(missing_report["issues"])

    def test_provider_descriptors_are_planned_only(self) -> None:
        request = ProviderRequest(provider="ollama", model="model", prompt="hello", max_tokens=32)
        validation = validate_provider_request(request)
        result = planned_provider_result(request)
        self.assertTrue(validation["ok"])
        self.assertTrue(result.ok)
        self.assertFalse(result.metadata["executed"])
        self.assertEqual(result.text, "")

        invalid = planned_provider_result(ProviderRequest(provider="", model="", prompt="", max_tokens=0))
        self.assertFalse(invalid.ok)
        self.assertIn("provider is required", invalid.error or "")

    def test_runner_stage_plan_and_boundary_report(self) -> None:
        stages = build_default_stage_plan(include_provider_stages=False)
        report = stage_plan_report(stages)
        self.assertEqual(report["stage_count"], 5)
        self.assertEqual(report["enabled_stage_count"], 4)
        boundary = build_helper_boundary_report(
            package_name="Tools.npu.pipeline",
            modules=["config", "io_utils"],
            checks={"syntax": True, "imports": True},
        )
        self.assertTrue(helper_boundary_passed(boundary))
        failed = build_helper_boundary_report(
            package_name="Tools.npu.pipeline",
            modules=["config"],
            checks={"syntax": False},
        )
        self.assertFalse(helper_boundary_passed(failed))


if __name__ == "__main__":
    unittest.main(verbosity=2)
