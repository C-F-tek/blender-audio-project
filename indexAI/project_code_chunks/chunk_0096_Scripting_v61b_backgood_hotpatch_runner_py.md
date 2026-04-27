# Project Code Chunk 96/212

- File: `Scripting/v61b_backgood/hotpatch/runner.py`
- Part: `1`
- Lines: `1-60`

## Symbol Map
- Imports: `bpy`, `from accent_patch import update_physics_accents`, `from common import load_analysis`, `from fog_patch import update_fog`, `from hero_material_patch import patch_hero_materials`, `from lighting_patch import remove_legacy_rhythm_objects, update_area_lights, update_backdrop, update_world`, `from render_patch import configure_existing_render`
- Functions: `run_all()` line 16

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
00014: 
00015: 
00016: def run_all():
00017:     scene = bpy.context.scene
00018:     meta, frames = load_analysis()
00019:     if meta is None:
00020:         meta = {}
00021: 
00022:     fps = configure_existing_render(scene, meta)
00023:     update_world(scene)
00024:     removed = remove_legacy_rhythm_objects()
00025:     lights = update_area_lights(frames)
00026:     backdrop = update_backdrop()
00027:     hero_materials = patch_hero_materials(frames)
00028:     fog_frames = update_fog(frames)
00029:     accents = update_physics_accents(frames)
00030: 
00031:     if frames:
00032:         scene.frame_start = 1
00033:         scene.frame_end = len(frames)
00034:         scene.frame_set(1)
00035: 
00036:     result = {
00037:         "fps": fps,
00038:         "analysis_frames": len(frames),
00039:         "legacy_removed": removed,
00040:         "area_lights": lights,
00041:         "backdrop": backdrop,
00042:         "hero_materials": hero_materials,
00043:         "fog_frames": fog_frames,
00044:         "accents": accents,
00045:     }
00046: 
00047:     print("=" * 68)
00048:     print("SPAZIOTEMPO HOTPATCH COMPLETE")
00049:     print(f"FPS/render settings: {fps}")
00050:     print(f"Analysis frames:     {len(frames)}")
00051:     print(f"Legacy rhythm objs:  removed {removed}")
00052:     print(f"Area lights updated: {lights}")
00053:     print(f"Backdrop updated:    {backdrop}")
00054:     print(f"Hero materials:      {hero_materials}")
00055:     print(f"Fog frames updated:  {fog_frames}")
00056:     print(f"Accent objs updated: {accents}")
00057:     print("No asset import, no scene clear, no Blender restart.")
00058:     print("=" * 68)
00059: 
00060:     return result
```
