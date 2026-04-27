# Project Code Chunk 44/212

- File: `Scripting/v61b/hotpatch/runner.py`
- Part: `1`
- Lines: `1-103`

## Symbol Map
- Imports: `bpy`, `from accent_patch import update_physics_accents`, `from common import load_analysis`, `from fog_patch import update_fog`, `from hero_material_patch import patch_hero_materials`, `from lighting_patch import remove_legacy_rhythm_objects, update_area_lights, update_backdrop, update_world`, `from render_patch import configure_existing_render`, `from spaziotempo.core.collections import classify_scene_objects, compact_structure_summary`
- Functions: `print_result(title, result)` line 17; `run_hotpatch(mode)` line 41; `run_all()` line 102

## Content
```py
00001: import bpy
00002: 
00003: from .accent_patch import update_physics_accents
00004: from .common import load_analysis
00005: from .fog_patch import update_fog
00006: from .hero_material_patch import patch_hero_materials
00007: from .lighting_patch import (
00008:     remove_legacy_rhythm_objects,
00009:     update_area_lights,
00010:     update_backdrop,
00011:     update_world,
00012: )
00013: from .render_patch import configure_existing_render
00014: from spaziotempo.core.collections import classify_scene_objects, compact_structure_summary
00015: 
00016: 
00017: def print_result(title, result):
00018:     print("=" * 68)
00019:     print(title)
00020:     for label, key in [
00021:         ("FPS/render settings", "fps"),
00022:         ("Analysis frames", "analysis_frames"),
00023:         ("Legacy rhythm objs", "legacy_removed"),
00024:         ("Area lights updated", "area_lights"),
00025:         ("Backdrop updated", "backdrop"),
00026:         ("Hero materials", "hero_materials"),
00027:         ("Fog frames updated", "fog_frames"),
00028:         ("Accent objs updated", "accents"),
00029:         ("Scene structure", "structure"),
00030:     ]:
00031:         if key not in result:
00032:             continue
00033:         value = result[key]
00034:         if key == "legacy_removed":
00035:             value = f"removed {value}"
00036:         print(f"{label:20}: {value}")
00037:     print("No asset import, no scene clear, no Blender restart.")
00038:     print("=" * 68)
00039: 
00040: 
00041: def run_hotpatch(mode="ALL"):
00042:     scene = bpy.context.scene
00043:     meta, frames = load_analysis()
00044:     if meta is None:
00045:         meta = {}
00046: 
00047:     mode = str(mode or "ALL").upper().replace(" ", "_").replace("-", "_")
00048:     aliases = {
00049:         "RENDER_ONLY": "RENDER",
00050:         "RENDER": "RENDER",
00051:         "MATERIAL": "MATERIALS",
00052:         "MATERIALS": "MATERIALS",
00053:         "FOG": "FOG",
00054:         "PHYSIC": "PHYSICS",
00055:         "PHYSICS": "PHYSICS",
00056:         "ACCENTS": "PHYSICS",
00057:         "ALL": "ALL",
00058:     }
00059:     mode = aliases.get(mode, "ALL")
00060: 
00061:     result = {
00062:         "analysis_frames": len(frames),
00063:     }
00064: 
00065:     if mode in {"RENDER", "ALL"}:
00066:         result["fps"] = configure_existing_render(scene, meta)
00067: 
00068:     if mode == "ALL":
00069:         update_world(scene)
00070:         result["legacy_removed"] = remove_legacy_rhythm_objects()
00071:         result["area_lights"] = update_area_lights(frames)
00072:         result["backdrop"] = update_backdrop()
00073:     elif mode == "FOG":
00074:         update_world(scene)
00075:         result["backdrop"] = update_backdrop()
00076: 
00077:     if mode in {"MATERIALS", "ALL"}:
00078:         result["hero_materials"] = patch_hero_materials(frames)
00079: 
00080:     if mode in {"FOG", "ALL"}:
00081:         result["fog_frames"] = update_fog(frames)
00082: 
00083:     if mode in {"PHYSICS", "ALL"}:
00084:         result["accents"] = update_physics_accents(frames)
00085: 
00086:     if frames:
00087:         scene.frame_start = 1
00088:         scene.frame_end = len(frames)
00089:         scene.frame_set(1)
00090: 
00091:     try:
00092:         structure_report = classify_scene_objects(scene, include_reserved=True)
00093:         result["structure"] = compact_structure_summary(structure_report)
00094:     except Exception as exc:
00095:         result["structure"] = f"not classified: {exc}"
00096: 
00097:     print_result(f"SPAZIOTEMPO HOTPATCH {mode} COMPLETE", result)
00098: 
00099:     return result
00100: 
00101: 
00102: def run_all():
00103:     return run_hotpatch("ALL")
```
