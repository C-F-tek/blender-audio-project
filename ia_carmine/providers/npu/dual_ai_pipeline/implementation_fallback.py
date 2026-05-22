from __future__ import annotations

from .common import *  # noqa: F403
from .deterministic_scene import deterministic_scene_builder_script
from .implementation_parse import generated_scene_script_relpath, get_indexed_project_files

def deterministic_support_files(
    track_stem: str, scene_brief: dict[str, Any] | None = None
) -> list[dict[str, str]]:
    slug = packet_slugify(track_stem)
    bundle_dir = f"indexAI/scene_scripts/{slug}_scene_bundle"
    manifest = {
        "kind": "spaziotempo_generated_scene_bundle_manifest",
        "track_stem": track_stem,
        "main_script": f"indexAI/scene_scripts/{slug}_scene_builder_candidate.py",
        "npu_service_role": [
            "create split/module plan",
            "maintain manifest of generated files",
            "check naming consistency",
            "summarize previous script for next GPU revision",
            "avoid heavy code generation unless explicitly requested",
        ],
        "gpu_writer_role": [
            "generate Blender Python scene logic",
            "apply scene director changes",
            "keep full audio keyframes as the animation source",
        ],
        "generated_files": [
            f"{bundle_dir}/manifest.json",
            f"{bundle_dir}/director_brief_snapshot.json",
            f"{bundle_dir}/README.md",
        ],
    }
    readme = f"""# {track_stem} Scene Bundle

This folder is generated support context for the standalone Blender scene script.

- Main Blender script: `../{slug}_scene_builder_candidate.py`
- Existing project files are reference only.
- Full audio keyframe JSON remains the source for animation.
- NPU can safely maintain this manifest/split plan; GPU/Ollama should handle heavy Blender code generation.
"""
    return [
        {
            "file": f"{bundle_dir}/manifest.json",
            "kind": "manifest",
            "content": json.dumps(manifest, indent=2, ensure_ascii=False),
        },
        {
            "file": f"{bundle_dir}/director_brief_snapshot.json",
            "kind": "brief_snapshot",
            "content": json.dumps(scene_brief or {}, indent=2, ensure_ascii=False),
        },
        {
            "file": f"{bundle_dir}/README.md",
            "kind": "notes",
            "content": readme,
        },
    ]

def build_fallback_implementation_draft(
    reason: str,
    model: str | None = None,
    args: argparse.Namespace | None = None,
    scene_brief: dict[str, Any] | None = None,
    asset_inventory: dict[str, Any] | None = None,
) -> dict[str, Any]:
    indexed_files = get_indexed_project_files()
    selected_files = [path for path in PREFERRED_IMPLEMENTATION_FILES if path in indexed_files]
    new_file = generated_scene_script_relpath()
    scene_script = deterministic_scene_builder_script(
        track_stem=TRACK_STEM,
        analysis_json=str(Path(args.analysis)) if args else "",
        music_context_json=str(Path(args.compact_json)) if args else "",
        ai_context_json=str(Path(args.analysis_ai_context)) if args else "",
        blender_keyframes_json=str(Path(args.blender_keyframes_json)) if args else "",
        asset_inventory_json=str(Path(args.asset_inventory))
        if args and getattr(args, "asset_inventory", None)
        else "",
        scene_brief=scene_brief,
    )

    reference_files = [
        {
            "file": path,
            "exists_in_project_index": True,
            "reason": "Style/source reference only; not modified by this generated scene script.",
        }
        for path in selected_files
    ]

    implementation_plan = [
        {
            "reference_file": path,
            "new_file": new_file,
            "change": "Use this file as structure/style reference for the standalone scene builder.",
            "why": "The generated product is a new Blender scene script, not a patch to the existing project.",
            "risk": "medium",
            "manual_check": "Open the generated script in Blender Text Editor and run on an empty scene.",
        }
        for path in selected_files
    ]

    draft: dict[str, Any] = {
        "implementation_kind": "new_blender_scene_script_from_json",
        "safety": {
            "does_not_modify_full_analysis_json": True,
            "does_not_modify_project_source_files": True,
            "requires_manual_review": True,
            "needs_blender_run": True,
        },
        "reference_files": reference_files,
        "proposed_files": [
            {
                "file": new_file,
                "kind": "standalone_blender_scene_builder",
                "why": "Creates a new scene from JSON context while preserving the original project as reference only.",
            }
        ],
        "implementation_plan": implementation_plan,
        "new_files_allowed": [
            "indexAI/scene_scripts/...",
            "indexAI/patch_library/...",
        ],
        "scene_script": scene_script,
        "support_files": deterministic_support_files(TRACK_STEM, scene_brief),
        "notes": [
            f"Deterministic fallback generated because implementation draft was invalid: {reason}",
            "This is a standalone scene builder; it does not patch the existing project files.",
            "NPU service work is represented as manifest/split-plan support files.",
        ],
        "files_to_review_before_applying": [item["file"] for item in reference_files],
        "expected_panel_or_operator": "Run as standalone Blender Text script on a new/empty scene.",
    }

    if model:
        draft["model"] = model
    if asset_inventory:
        draft["asset_inventory_used"] = {
            "asset_count": asset_inventory.get("asset_count"),
            "primary_assets": [
                asset
                for asset in asset_inventory.get("assets", [])
                if asset.get("role")
                in {"primary_ball_asset", "animated_effect_asset", "blend_scene_reference"}
            ][:10],
        }

    return draft
