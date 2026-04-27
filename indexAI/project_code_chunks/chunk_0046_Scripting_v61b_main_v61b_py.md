# Project Code Chunk 46/212

- File: `Scripting/v61b/main_v61b.py`
- Part: `1`
- Lines: `1-219`

## Symbol Map
- Imports: `sys`, `time`, `from pathlib import Path`, `bpy`, `logging`, `from config import ANALYSIS_JSON_PATH, AUDIO_PATH, OUTPUT_MP4, OUTPUT_IMAGE_SEQUENCE_DIR, OUTPUT_IMAGE_SEQUENCE_PREFIX, RENDER_OUTPUT_MODE, CLEAR_SCENE, CLEAR_SEQUENCER, FPS_OVERRIDE`, `from scene_utils import clear_scene`, `from io_utils import load_json, ensure_inputs_exist, add_audio_strip`, `from render_setup import configure_scene_physics, configure_render`, `from world_setup import configure_world, create_floor_and_backdrop, create_area_lights`, `from camera_setup import create_camera_rig`, `from asset_setup import create_scene_core, create_primary_asset, create_secondary_asset`, `from atmosphere_setup import create_hero_aura, create_energy_rings, create_energy_ribbons, create_variants, create_atmosphere_cube, create_mist_particles`, `from physics_setup import create_physics_accents`, `from animation import animate_scene`, `from spaziotempo.core.collections import classify_scene_objects, compact_structure_summary`
- Functions: `register_tuning_panel()` line 79; `classify_project_structure(scene)` line 89; `print_summary(scene, analysis_file, hero_asset, secondary_asset, audio_file, fps, frame_count, elapsed)` line 100; `main()` line 125
- Assignments: `SCRIPT_DIR`, `reload_modules`, `reload_prefixes`

## Content
```py
00001: import sys
00002: import time
00003: from pathlib import Path
00004: import bpy
00005: import logging
00006: 
00007: # Configurazione del logging
00008: logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
00009: 
00010: SCRIPT_DIR = None
00011: 
00012: try:
00013:     text = bpy.context.space_data.text
00014:     if text is not None and text.filepath:
00015:         SCRIPT_DIR = Path(text.filepath).resolve().parent
00016: except Exception as e:
00017:     logging.warning(f"Impossibile determinare la directory dello script: {e}")
00018:     SCRIPT_DIR = None
00019: 
00020: if SCRIPT_DIR is None:
00021:     SCRIPT_DIR = Path.home() / "blender" / "blender-audio-project" / "Scripting" / "v61b"
00022: 
00023: if str(SCRIPT_DIR) not in sys.path:
00024:     sys.path.insert(0, str(SCRIPT_DIR))
00025: 
00026: reload_modules = {
00027:     "config",
00028:     "scene_utils",
00029:     "io_utils",
00030:     "render_setup",
00031:     "world_setup",
00032:     "camera_setup",
00033:     "asset_setup",
00034:     "atmosphere_setup",
00035:     "physics_setup",
00036:     "fog_dynamics",
00037:     "fog_filaments",
00038:     "animation",
00039:     "scene_tuning_panel",
00040: }
00041: reload_prefixes = ("spaziotempo",)
00042: 
00043: for mod_name in list(sys.modules):
00044:     if mod_name in reload_modules or any(
00045:         mod_name == prefix or mod_name.startswith(prefix + ".") for prefix in reload_prefixes
00046:     ):
00047:         sys.modules.pop(mod_name, None)
00048: 
00049: from config import (
00050:     ANALYSIS_JSON_PATH,
00051:     AUDIO_PATH,
00052:     OUTPUT_MP4,
00053:     OUTPUT_IMAGE_SEQUENCE_DIR,
00054:     OUTPUT_IMAGE_SEQUENCE_PREFIX,
00055:     RENDER_OUTPUT_MODE,
00056:     CLEAR_SCENE,
00057:     CLEAR_SEQUENCER,
00058:     FPS_OVERRIDE,
00059: )
00060: from scene_utils import clear_scene
00061: from io_utils import load_json, ensure_inputs_exist, add_audio_strip
00062: from render_setup import configure_scene_physics, configure_render
00063: from world_setup import configure_world, create_floor_and_backdrop, create_area_lights
00064: from camera_setup import create_camera_rig
00065: from asset_setup import create_scene_core, create_primary_asset, create_secondary_asset
00066: from atmosphere_setup import (
00067:     create_hero_aura,
00068:     create_energy_rings,
00069:     create_energy_ribbons,
00070:     create_variants,
00071:     create_atmosphere_cube,
00072:     create_mist_particles,
00073: )
00074: from physics_setup import create_physics_accents
00075: from animation import animate_scene
00076: from spaziotempo.core.collections import classify_scene_objects, compact_structure_summary
00077: 
00078: 
00079: def register_tuning_panel():
00080:     try:
00081:         import scene_tuning_panel
00082: 
00083:         scene_tuning_panel.register()
00084:         logging.info("Pannello di tuning Spaziotempo registrato. Aprire il pannello laterale con N > Spaziotempo.")
00085:     except Exception as exc:
00086:         logging.warning(f"Impossibile registrare il pannello di tuning: {exc}")
00087: 
00088: 
00089: def classify_project_structure(scene):
00090:     try:
00091:         report = classify_scene_objects(scene, include_reserved=True)
00092:         summary = compact_structure_summary(report)
00093:         logging.info(f"Struttura della scena classificata: {summary}")
00094:         return report
00095:     except Exception as exc:
00096:         logging.warning(f"Impossibile classificare la struttura della scena: {exc}")
00097:         return None
00098: 
00099: 
00100: def print_summary(scene, analysis_file, hero_asset, secondary_asset, audio_file, fps, frame_count, elapsed):
00101:     logging.info("=" * 68)
00102:     logging.info("SPAZIOTEMPOREC HERO + SECONDARY ASSET VISUAL READY")
00103:     logging.info(f"Engine: {scene.render.engine}")
00104:     logging.info(f"Resolution: {scene.render.resolution_x}x{scene.render.resolution_y} @ {scene.render.resolution_percentage}%")
00105:     logging.info(f"FPS: {fps}")
00106:     logging.info(f"Frames: {frame_count}")
00107:     logging.info(f"Analysis JSON: {analysis_file}")
00108:     logging.info(f"Hero asset:    {hero_asset['asset_file']}")
00109:     if secondary_asset is not None:
00110:         logging.info(f"Secondary:     {secondary_asset['asset_file']}")
00111:     else:
00112:         logging.info("Secondary:     NONE")
00113:     logging.info(f"Audio:         {audio_file}")
00114:     if str(RENDER_OUTPUT_MODE).upper() == "IMAGE_SEQUENCE":
00115:         logging.info(f"Frames:        {OUTPUT_IMAGE_SEQUENCE_DIR}")
00116:         logging.info(f"Prefix:        {OUTPUT_IMAGE_SEQUENCE_PREFIX}")
00117:         logging.info(f"Encode MP4:    eseguire encode_image_sequence_v61b.py dopo il Render Animation")
00118:     else:
00119:         logging.info(f"MP4:           {scene.render.filepath}")
00120:     logging.info(f"Elapsed:       {elapsed:.2f}s")
00121:     logging.info("Utilizzare Render > Render Animation per esportare l'output configurato.")
00122:     logging.info("=" * 68)
00123: 
00124: 
00125: def main():
00126:     t0 = time.time()
00127: 
00128:     logging.info("[1/10] Verifica input...")
00129:     analysis_file, audio_file = ensure_inputs_exist(
00130:         ANALYSIS_JSON_PATH,
00131:         AUDIO_PATH,
00132:     )
00133: 
00134:     logging.info("[2/10] Carico analysis JSON...")
00135:     analysis = load_json(analysis_file)
00136:     meta = analysis["meta"]
00137:     frames = analysis["frames"]
00138: 
00139:     fps = FPS_OVERRIDE if FPS_OVERRIDE else meta["fps"]
00140:     frame_count = len(frames)
00141: 
00142:     scene = bpy.context.scene
00143:     if CLEAR_SCENE:
00144:         logging.info("[3/10] Pulisco scena...")
00145:         clear_scene()
00146: 
00147:     scene.frame_start = 1
00148:     scene.frame_end = frame_count
00149:     scene.frame_set(1)
00150: 
00151:     logging.info("[4/10] Configuro render e world...")
00152:     configure_scene_physics(scene)
00153:     configure_render(scene, OUTPUT_MP4, fps)
00154:     configure_world(scene)
00155: 
00156:     logging.info("[5/10] Aggiungo audio strip...")
00157:     add_audio_strip(scene, audio_file, clear_existing=CLEAR_SEQUENCER, sync_audio=True)
00158: 
00159:     if scene.rigidbody_world is not None and scene.rigidbody_world.point_cache is not None:
00160:         scene.rigidbody_world.point_cache.frame_start = 1
00161:         scene.rigidbody_world.point_cache.frame_end = frame_count
00162: 
00163:     logging.info("[6/10] Creo camera...")
00164:     camera, target = create_camera_rig()
00165: 
00166:     logging.info("[7/10] Creo base scena...")
00167:     scene_base = create_floor_and_backdrop()
00168:     lights = create_area_lights()
00169: 
00170:     logging.info("[8/10] Importo hero + secondary asset...")
00171:     scene_core = create_scene_core()
00172:     hero_asset = create_primary_asset(parent=scene_core)
00173:     secondary_asset = create_secondary_asset(parent=scene_core)
00174: 
00175:     logging.info(f"[INFO] Hero asset file: {hero_asset['asset_file']}")
00176:     if secondary_asset is not None:
00177:         logging.info(f"[INFO] Secondary asset file: {secondary_asset['asset_file']}")
00178:     else:
00179:         logging.info("[INFO] Secondary asset: NONE")
00180: 
00181:     logging.info("[9/10] Creo atmosfera e fisica...")
00182:     aura_data = create_hero_aura(parent=scene_core)
00183:     energy_rings = create_energy_rings(parent=scene_core)
00184:     energy_ribbons = create_energy_ribbons(parent=scene_core)
00185:     variants = create_variants(hero_asset["root"], parent=scene_core)
00186: 
00187:     fog_controller = create_atmosphere_cube(parent=scene_core)
00188:     mist_particles = create_mist_particles(parent=scene_core)
00189: 
00190:     physics_data = create_physics_accents(parent=scene_core)
00191: 
00192:     logging.info("[10/10] Animo scena...")
00193:     animate_scene(
00194:         scene=scene,
00195:         frames=frames,
00196:         camera=camera,
00197:         target=target,
00198:         hero_asset=hero_asset,
00199:         secondary_asset=secondary_asset,
00200:         aura_data=aura_data,
00201:         fog_controller=fog_controller,
00202:         scene_base=scene_base,
00203:         lights=lights,
00204:         physics_data=physics_data,
00205:         mist_particles=mist_particles,
00206:         variants=variants,
00207:         energy_rings=energy_rings,
00208:         energy_ribbons=energy_ribbons,
00209:     )
00210: 
00211:     classify_project_structure(scene)
00212: 
00213:     elapsed = time.time() - t0
00214:     register_tuning_panel()
00215:     print_summary(scene, analysis_file, hero_asset, secondary_asset, audio_file, fps, frame_count, elapsed)
00216: 
00217: 
00218: if __name__ == "__main__":
00219:     main()
```
