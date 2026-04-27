# Project Code Chunk 98/212

- File: `Scripting/v61b_backgood/main_v61b.py`
- Part: `1`
- Lines: `1-181`

## Symbol Map
- Imports: `sys`, `time`, `from pathlib import Path`, `bpy`, `from config import ANALYSIS_JSON_PATH, AUDIO_PATH, OUTPUT_MP4, OUTPUT_IMAGE_SEQUENCE_DIR, OUTPUT_IMAGE_SEQUENCE_PREFIX, RENDER_OUTPUT_MODE, CLEAR_SCENE, CLEAR_SEQUENCER, FPS_OVERRIDE`, `from scene_utils import clear_scene`, `from io_utils import load_json, ensure_inputs_exist, add_audio_strip`, `from render_setup import configure_scene_physics, configure_render`, `from world_setup import configure_world, create_floor_and_backdrop, create_area_lights`, `from camera_setup import create_camera_rig`, `from asset_setup import create_scene_core, create_primary_asset, create_secondary_asset`, `from atmosphere_setup import create_hero_aura, create_energy_rings, create_energy_ribbons, create_variants, create_atmosphere_cube, create_mist_particles`, `from physics_setup import create_physics_accents`, `from animation import animate_scene`
- Functions: `print_summary(scene, analysis_file, hero_asset, secondary_asset, audio_file, fps, frame_count, elapsed)` line 65; `main()` line 90
- Assignments: `SCRIPT_DIR`

## Content
```py
00001: import sys
00002: import time
00003: from pathlib import Path
00004: import bpy
00005: 
00006: SCRIPT_DIR = None
00007: 
00008: try:
00009:     text = bpy.context.space_data.text
00010:     if text is not None and text.filepath:
00011:         SCRIPT_DIR = Path(text.filepath).resolve().parent
00012: except Exception:
00013:     SCRIPT_DIR = None
00014: 
00015: if SCRIPT_DIR is None:
00016:     SCRIPT_DIR = Path.home() / "blender" / "blender-audio-project" / "Scripting" / "v61b"
00017: 
00018: if str(SCRIPT_DIR) not in sys.path:
00019:     sys.path.insert(0, str(SCRIPT_DIR))
00020: 
00021: for mod_name in [
00022:     "config",
00023:     "scene_utils",
00024:     "io_utils",
00025:     "render_setup",
00026:     "world_setup",
00027:     "camera_setup",
00028:     "asset_setup",
00029:     "atmosphere_setup",
00030:     "physics_setup",
00031:     "fog_dynamics",
00032:     "animation",
00033: ]:
00034:     sys.modules.pop(mod_name, None)
00035: 
00036: from config import (
00037:     ANALYSIS_JSON_PATH,
00038:     AUDIO_PATH,
00039:     OUTPUT_MP4,
00040:     OUTPUT_IMAGE_SEQUENCE_DIR,
00041:     OUTPUT_IMAGE_SEQUENCE_PREFIX,
00042:     RENDER_OUTPUT_MODE,
00043:     CLEAR_SCENE,
00044:     CLEAR_SEQUENCER,
00045:     FPS_OVERRIDE,
00046: )
00047: from scene_utils import clear_scene
00048: from io_utils import load_json, ensure_inputs_exist, add_audio_strip
00049: from render_setup import configure_scene_physics, configure_render
00050: from world_setup import configure_world, create_floor_and_backdrop, create_area_lights
00051: from camera_setup import create_camera_rig
00052: from asset_setup import create_scene_core, create_primary_asset, create_secondary_asset
00053: from atmosphere_setup import (
00054:     create_hero_aura,
00055:     create_energy_rings,
00056:     create_energy_ribbons,
00057:     create_variants,
00058:     create_atmosphere_cube,
00059:     create_mist_particles,
00060: )
00061: from physics_setup import create_physics_accents
00062: from animation import animate_scene
00063: 
00064: 
00065: def print_summary(scene, analysis_file, hero_asset, secondary_asset, audio_file, fps, frame_count, elapsed):
00066:     print("=" * 68)
00067:     print("SPAZIOTEMPOREC HERO + SECONDARY ASSET VISUAL READY")
00068:     print(f"Engine: {scene.render.engine}")
00069:     print(f"Resolution: {scene.render.resolution_x}x{scene.render.resolution_y} @ {scene.render.resolution_percentage}%")
00070:     print(f"FPS: {fps}")
00071:     print(f"Frames: {frame_count}")
00072:     print(f"Analysis JSON: {analysis_file}")
00073:     print(f"Hero asset:    {hero_asset['asset_file']}")
00074:     if secondary_asset is not None:
00075:         print(f"Secondary:     {secondary_asset['asset_file']}")
00076:     else:
00077:         print("Secondary:     NONE")
00078:     print(f"Audio:         {audio_file}")
00079:     if str(RENDER_OUTPUT_MODE).upper() == "IMAGE_SEQUENCE":
00080:         print(f"Frames:        {OUTPUT_IMAGE_SEQUENCE_DIR}")
00081:         print(f"Prefix:        {OUTPUT_IMAGE_SEQUENCE_PREFIX}")
00082:         print(f"Encode MP4:    run encode_image_sequence_v61b.py after Render Animation")
00083:     else:
00084:         print(f"MP4:           {scene.render.filepath}")
00085:     print(f"Elapsed:       {elapsed:.2f}s")
00086:     print("Use Render > Render Animation to export the configured output.")
00087:     print("=" * 68)
00088: 
00089: 
00090: def main():
00091:     t0 = time.time()
00092: 
00093:     print("[1/10] Verifica input...")
00094:     analysis_file, audio_file = ensure_inputs_exist(
00095:         ANALYSIS_JSON_PATH,
00096:         AUDIO_PATH,
00097:     )
00098: 
00099:     print("[2/10] Carico analysis JSON...")
00100:     analysis = load_json(analysis_file)
00101:     meta = analysis["meta"]
00102:     frames = analysis["frames"]
00103: 
00104:     fps = FPS_OVERRIDE if FPS_OVERRIDE else meta["fps"]
00105:     frame_count = len(frames)
00106: 
00107:     scene = bpy.context.scene
00108:     if CLEAR_SCENE:
00109:         print("[3/10] Pulisco scena...")
00110:         clear_scene()
00111: 
00112:     scene.frame_start = 1
00113:     scene.frame_end = frame_count
00114:     scene.frame_set(1)
00115: 
00116:     print("[4/10] Configuro render e world...")
00117:     configure_scene_physics(scene)
00118:     configure_render(scene, OUTPUT_MP4, fps)
00119:     configure_world(scene)
00120: 
00121:     print("[5/10] Aggiungo audio strip...")
00122:     add_audio_strip(scene, audio_file, clear_existing=CLEAR_SEQUENCER, sync_audio=True)
00123: 
00124:     if scene.rigidbody_world is not None and scene.rigidbody_world.point_cache is not None:
00125:         scene.rigidbody_world.point_cache.frame_start = 1
00126:         scene.rigidbody_world.point_cache.frame_end = frame_count
00127: 
00128:     print("[6/10] Creo camera...")
00129:     camera, target = create_camera_rig()
00130: 
00131:     print("[7/10] Creo base scena...")
00132:     scene_base = create_floor_and_backdrop()
00133:     lights = create_area_lights()
00134: 
00135:     print("[8/10] Importo hero + secondary asset...")
00136:     scene_core = create_scene_core()
00137:     hero_asset = create_primary_asset(parent=scene_core)
00138:     secondary_asset = create_secondary_asset(parent=scene_core)
00139: 
00140:     print(f"[INFO] Hero asset file: {hero_asset['asset_file']}")
00141:     if secondary_asset is not None:
00142:         print(f"[INFO] Secondary asset file: {secondary_asset['asset_file']}")
00143:     else:
00144:         print("[INFO] Secondary asset: NONE")
00145: 
00146:     print("[9/10] Creo atmosfera e fisica...")
00147:     aura_data = create_hero_aura(parent=scene_core)
00148:     energy_rings = create_energy_rings(parent=scene_core)
00149:     energy_ribbons = create_energy_ribbons(parent=scene_core)
00150:     variants = create_variants(hero_asset["root"], parent=scene_core)
00151: 
00152:     fog_controller = create_atmosphere_cube()
00153:     mist_particles = create_mist_particles(parent=scene_core)
00154: 
00155:     physics_data = create_physics_accents(parent=scene_core)
00156: 
00157:     print("[10/10] Animo scena...")
00158:     animate_scene(
00159:         scene=scene,
00160:         frames=frames,
00161:         camera=camera,
00162:         target=target,
00163:         hero_asset=hero_asset,
00164:         secondary_asset=secondary_asset,
00165:         aura_data=aura_data,
00166:         fog_controller=fog_controller,
00167:         scene_base=scene_base,
00168:         lights=lights,
00169:         physics_data=physics_data,
00170:         mist_particles=mist_particles,
00171:         variants=variants,
00172:         energy_rings=energy_rings,
00173:         energy_ribbons=energy_ribbons,
00174:     )
00175: 
00176:     elapsed = time.time() - t0
00177:     print_summary(scene, analysis_file, hero_asset, secondary_asset, audio_file, fps, frame_count, elapsed)
00178: 
00179: 
00180: if __name__ == "__main__":
00181:     main()
```
