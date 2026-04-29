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

from Tools.ai_core.io_utils import write_json, write_text
from Tools.npu.implementation_draft_validation import validate_implementation_draft_with_adapter


def build_script() -> str:
    script = """
import bpy
import json
from pathlib import Path

BLENDER_KEYFRAMES_JSON = Path('output/track_analysis_blender_keyframes.json')
with BLENDER_KEYFRAMES_JSON.open('r', encoding='utf-8') as handle:
    keyframes = json.load(handle)
frames = keyframes.get('frames', [])

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()
mat = bpy.data.materials.new('BridgeSmokeMat')
mat.use_nodes = True
bpy.ops.mesh.primitive_uv_sphere_add(location=(0, 0, 0))
obj = bpy.context.object
obj.name = 'BridgeSmokeReactiveSphere'
obj.data.materials.append(mat)
for index, frame_data in enumerate(frames):
    frame = int(frame_data.get('frame', index + 1))
    amp = float(frame_data.get('low', frame_data.get('energy', 0.2)))
    obj.location.z = amp
    obj.scale = (1.0 + amp, 1.0 + amp, 1.0 + amp)
    obj.keyframe_insert(data_path='location', frame=frame)
    obj.keyframe_insert(data_path='scale', frame=frame)

camera_data = bpy.data.cameras.new('BridgeSmokeCamera')
camera = bpy.data.objects.new('BridgeSmokeCamera', camera_data)
bpy.context.collection.objects.link(camera)
camera.location = (0, -8, 4)
camera.rotation_euler = (1.1, 0, 0)
bpy.context.scene.camera = camera
light_data = bpy.data.lights.new('BridgeSmokeKeyLight', type='AREA')
light = bpy.data.objects.new('BridgeSmokeKeyLight', light_data)
bpy.context.collection.objects.link(light)
light.location = (0, -3, 6)
""".strip()
    if len(script) < 1800:
        script += "\n" + ("# bridge smoke filler for policy minimum length\n" * 24)
    return script


def build_valid_draft() -> dict[str, Any]:
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
            {"file": "indexAI/scene_scripts/bridge_smoke_scene_builder_candidate.py", "kind": "standalone_blender_scene_builder", "why": "bridge smoke test"}
        ],
        "implementation_plan": [
            {
                "reference_file": "Scripting/v61b/materials.py",
                "new_file": "indexAI/scene_scripts/bridge_smoke_scene_builder_candidate.py",
                "change": "validate standalone bridge draft",
                "why": "ensure legacy-compatible validator bridge works",
                "risk": "low",
                "manual_check": "run in Blender only on a disposable scene",
            }
        ],
        "new_files_allowed": ["indexAI/scene_scripts/...", "indexAI/patch_library/..."],
        "scene_script": build_script(),
        "support_files": [],
        "notes": ["bridge smoke-test draft"],
        "files_to_review_before_applying": ["Scripting/v61b/materials.py"],
        "expected_panel_or_operator": "Run as standalone Blender Text script on a new scene.",
    }


def build_markdown_report(report: dict[str, Any]) -> str:
    lines = [
        "# NPU Validation Bridge Smoke Test Report\n",
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
        "\n## Shareable files\n",
        "Share this Markdown file plus `npu_validation_bridge_smoke_report.json` for review.\n",
    ])
    return "".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description="Run smoke tests for the NPU validation bridge.")
    ap.add_argument("--output-dir", default="output/smoke_tests/npu_validation_bridge")
    ap.add_argument("--manifest", default="Tools/npu/npu_code_manifest.json")
    args = ap.parse_args()

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest = ROOT / args.manifest

    valid_draft = build_valid_draft()
    valid_report = validate_implementation_draft_with_adapter(valid_draft, manifest)

    invalid_draft = dict(valid_draft)
    invalid_draft["proposed_files"] = [{"file": "Scripting/v61b/materials.py"}]
    invalid_draft["scene_script"] = "import bpy\n# placeholder"
    invalid_report = validate_implementation_draft_with_adapter(invalid_draft, manifest)

    checks = {
        "valid_draft_acceptance": {"passed": bool(valid_report.get("passed")), "report": valid_report},
        "invalid_draft_rejection": {"passed": not bool(invalid_report.get("passed")), "report": invalid_report},
    }
    report = {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "repo_root": str(ROOT),
        "manifest": str(manifest),
        "runtime": {"python": sys.version, "platform": platform.platform()},
        "checks": checks,
        "passed": all(item.get("passed") for item in checks.values()),
    }
    json_path = write_json(out_dir / "npu_validation_bridge_smoke_report.json", report)
    md_path = write_text(out_dir / "npu_validation_bridge_smoke_report.md", build_markdown_report(report))
    print(json.dumps({"passed": report["passed"], "json_report": str(json_path), "markdown_report": str(md_path)}, indent=2))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
