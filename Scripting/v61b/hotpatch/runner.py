import bpy
from spaziotempo.core.collections import classify_scene_objects, compact_structure_summary

from .accent_patch import update_physics_accents
from .common import load_analysis
from .fog_patch import update_fog
from .hero_material_patch import patch_hero_materials
from .lighting_patch import (
    remove_legacy_rhythm_objects,
    update_area_lights,
    update_backdrop,
    update_world,
)
from .render_patch import configure_existing_render


def print_result(title, result):
    print("=" * 68)
    print(title)
    for label, key in [
        ("FPS/render settings", "fps"),
        ("Analysis frames", "analysis_frames"),
        ("Legacy rhythm objs", "legacy_removed"),
        ("Area lights updated", "area_lights"),
        ("Backdrop updated", "backdrop"),
        ("Hero materials", "hero_materials"),
        ("Fog frames updated", "fog_frames"),
        ("Accent objs updated", "accents"),
        ("Scene structure", "structure"),
    ]:
        if key not in result:
            continue
        value = result[key]
        if key == "legacy_removed":
            value = f"removed {value}"
        print(f"{label:20}: {value}")
    print("No asset import, no scene clear, no Blender restart.")
    print("=" * 68)


def run_hotpatch(mode="ALL"):
    scene = bpy.context.scene
    meta, frames = load_analysis()
    if meta is None:
        meta = {}

    mode = str(mode or "ALL").upper().replace(" ", "_").replace("-", "_")
    aliases = {
        "RENDER_ONLY": "RENDER",
        "RENDER": "RENDER",
        "MATERIAL": "MATERIALS",
        "MATERIALS": "MATERIALS",
        "FOG": "FOG",
        "PHYSIC": "PHYSICS",
        "PHYSICS": "PHYSICS",
        "ACCENTS": "PHYSICS",
        "ALL": "ALL",
    }
    mode = aliases.get(mode, "ALL")

    result = {
        "analysis_frames": len(frames),
    }

    if mode in {"RENDER", "ALL"}:
        result["fps"] = configure_existing_render(scene, meta)

    if mode == "ALL":
        update_world(scene)
        result["legacy_removed"] = remove_legacy_rhythm_objects()
        result["area_lights"] = update_area_lights(frames)
        result["backdrop"] = update_backdrop()
    elif mode == "FOG":
        update_world(scene)
        result["backdrop"] = update_backdrop()

    if mode in {"MATERIALS", "ALL"}:
        result["hero_materials"] = patch_hero_materials(frames)

    if mode in {"FOG", "ALL"}:
        result["fog_frames"] = update_fog(frames)

    if mode in {"PHYSICS", "ALL"}:
        result["accents"] = update_physics_accents(frames)

    if frames:
        scene.frame_start = 1
        scene.frame_end = len(frames)
        scene.frame_set(1)

    try:
        structure_report = classify_scene_objects(scene, include_reserved=True)
        result["structure"] = compact_structure_summary(structure_report)
    except Exception as exc:
        result["structure"] = f"not classified: {exc}"

    print_result(f"SPAZIOTEMPO HOTPATCH {mode} COMPLETE", result)

    return result


def run_all():
    return run_hotpatch("ALL")
