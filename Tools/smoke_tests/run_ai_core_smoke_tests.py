#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from Tools.ai_core import ArtifactStore, PipelineContext, PipelineResult, PipelineStage, SequentialPipeline, StaticModelClient, parse_model_json
from Tools.ai_core.io_utils import file_meta, write_json, write_text
from Tools.ai_adapters.blender import BlenderGeneratedScriptPolicy, BlenderImplementationDraftValidator


class AddValueStage:
    name = "add_value"

    def run(self, context: PipelineContext) -> PipelineContext:
        context.data["value"] = 42
        return context


class PersistValueStage:
    name = "persist_value"

    def run(self, context: PipelineContext) -> PipelineContext:
        if context.artifacts:
            context.artifacts.write_json("value.json", {"value": context.data.get("value")})
        return context


def smoke_parse_model_json() -> dict[str, Any]:
    samples = [
        "```json\n{\"ok\": true,}\n```",
        "prefix text {\"answer\": 7} suffix text",
        "[1, 2, 3,]",
    ]
    parsed = [parse_model_json(sample) for sample in samples]
    return {"passed": parsed == [{"ok": True}, {"answer": 7}, [1, 2, 3]], "parsed": parsed}


def smoke_static_model_client() -> dict[str, Any]:
    client = StaticModelClient('{"result": "ok"}', model="smoke-static")
    response = client.generate("hello")
    parsed = parse_model_json(response.text)
    return {"passed": parsed.get("result") == "ok" and response.model == "smoke-static", "response": response.__dict__, "parsed": parsed}


def smoke_pipeline(out_dir: Path) -> dict[str, Any]:
    store = ArtifactStore(out_dir, run_id="core_pipeline_smoke")
    context = PipelineContext(job={"name": "core_pipeline_smoke"}, artifacts=store)
    result: PipelineResult = SequentialPipeline([AddValueStage(), PersistValueStage()]).run(context)
    return {"passed": result.passed and context.data.get("value") == 42, "result": result.to_dict()}


def sample_valid_blender_draft() -> dict[str, Any]:
    script_body = """
import bpy
import json
from pathlib import Path

BLENDER_KEYFRAMES_JSON = Path('output/track_analysis_blender_keyframes.json')
with BLENDER_KEYFRAMES_JSON.open('r', encoding='utf-8') as handle:
    keyframes = json.load(handle)
frames = keyframes.get('frames', [])

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()
mat = bpy.data.materials.new('SmokeMat')
mat.use_nodes = True
mesh = bpy.ops.mesh.primitive_uv_sphere_add(location=(0, 0, 0))
obj = bpy.context.object
obj.name = 'SmokeReactiveSphere'
obj.data.materials.append(mat)
for index, frame_data in enumerate(frames):
    frame = int(frame_data.get('frame', index + 1))
    amp = float(frame_data.get('low', frame_data.get('energy', 0.2)))
    obj.location.z = amp
    obj.scale = (1.0 + amp, 1.0 + amp, 1.0 + amp)
    obj.keyframe_insert(data_path='location', frame=frame)
    obj.keyframe_insert(data_path='scale', frame=frame)

camera_data = bpy.data.cameras.new('SmokeCamera')
camera = bpy.data.objects.new('SmokeCamera', camera_data)
bpy.context.collection.objects.link(camera)
camera.location = (0, -8, 4)
camera.rotation_euler = (1.1, 0, 0)
bpy.context.scene.camera = camera
light_data = bpy.data.lights.new('SmokeKeyLight', type='AREA')
light = bpy.data.objects.new('SmokeKeyLight', light_data)
bpy.context.collection.objects.link(light)
light.location = (0, -3, 6)
""".strip()
    if len(script_body) < 1800:
        script_body += "\n" + ("# deterministic smoke-test filler for minimum script size\n" * 20)
    return {
        "implementation_kind": "new_blender_scene_script_from_json",
        "safety": {
            "does_not_modify_full_analysis_json": True,
            "does_not_modify_project_source_files": True,
            "requires_manual_review": True,
            "needs_blender_run": True,
        },
        "reference_files": [
            {"file": "Scripting/v61b/materials.py", "exists_in_project_index": True, "reason": "style/source reference only"}
        ],
        "proposed_files": [
            {"file": "indexAI/scene_scripts/smoke_scene_builder_candidate.py", "kind": "standalone_blender_scene_builder", "why": "smoke test"}
        ],
        "implementation_plan": [
            {
                "reference_file": "Scripting/v61b/materials.py",
                "new_file": "indexAI/scene_scripts/smoke_scene_builder_candidate.py",
                "change": "create standalone smoke scene builder",
                "why": "validate policy and generated script rules",
                "risk": "low",
                "manual_check": "run inside Blender on a disposable scene",
            }
        ],
        "new_files_allowed": ["indexAI/scene_scripts/...", "indexAI/patch_library/..."],
        "scene_script": script_body,
        "support_files": [],
        "notes": ["smoke-test draft"],
        "files_to_review_before_applying": ["Scripting/v61b/materials.py"],
        "expected_panel_or_operator": "Run as standalone Blender Text script on a new scene.",
    }


def smoke_blender_validator() -> dict[str, Any]:
    indexed = {"Scripting/v61b/materials.py", "Scripting/v61b/config.py"}
    policy = BlenderGeneratedScriptPolicy(min_script_chars=1200)
    validator = BlenderImplementationDraftValidator(policy=policy, indexed_files=indexed)
    valid_draft = sample_valid_blender_draft()
    valid_report = validator.validate(valid_draft)

    invalid_draft = dict(valid_draft)
    invalid_draft["proposed_files"] = [{"file": "Scripting/v61b/materials.py"}]
    invalid_draft["scene_script"] = "import bpy\n# placeholder"
    invalid_report = validator.validate(invalid_draft)

    return {
        "passed": valid_report.passed and not invalid_report.passed,
        "policy": policy.to_dict(),
        "valid_report": valid_report.to_dict(),
        "invalid_report": invalid_report.to_dict(),
    }


def build_markdown_report(report: dict[str, Any]) -> str:
    lines = [
        "# AI Core Smoke Test Report\n",
        f"- Generated at: `{report['generated_at']}`\n",
        f"- Repository root: `{report['repo_root']}`\n",
        f"- Python: `{report['runtime']['python']}`\n",
        f"- Platform: `{report['runtime']['platform']}`\n",
        f"- Overall passed: `{report['passed']}`\n\n",
        "## Checks\n",
    ]
    for name, item in report["checks"].items():
        lines.append(f"- `{name}`: `{item.get('passed')}`\n")
    lines.extend([
        "\n## Files to share\n",
        "Share this Markdown file plus `ai_core_smoke_report.json` when asking for review.\n",
    ])
    return "".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description="Run shareable smoke tests for the reusable AI core.")
    ap.add_argument("--output-dir", default="output/smoke_tests/ai_core")
    args = ap.parse_args()

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    checks = {
        "parse_model_json": smoke_parse_model_json(),
        "static_model_client": smoke_static_model_client(),
        "sequential_pipeline": smoke_pipeline(out_dir),
        "blender_validator": smoke_blender_validator(),
    }
    report = {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "repo_root": str(ROOT),
        "runtime": {"python": sys.version, "platform": platform.platform()},
        "inputs": {
            "ai_core": file_meta(ROOT / "Tools" / "ai_core", root=ROOT),
            "blender_adapter": file_meta(ROOT / "Tools" / "ai_adapters" / "blender", root=ROOT),
        },
        "checks": checks,
        "passed": all(item.get("passed") for item in checks.values()),
    }

    json_path = write_json(out_dir / "ai_core_smoke_report.json", report)
    md_path = write_text(out_dir / "ai_core_smoke_report.md", build_markdown_report(report))
    print(json.dumps({"passed": report["passed"], "json_report": str(json_path), "markdown_report": str(md_path)}, indent=2))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
