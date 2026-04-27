# Project Code Chunk 106/212

- File: `Scripting/v61b_backgood/scene_tuning_panel.py`
- Part: `1`
- Lines: `1-323`

## Symbol Map
- Imports: `json`, `traceback`, `from pathlib import Path`, `bpy`, `from bpy.props import BoolProperty, FloatProperty, PointerProperty, StringProperty`
- Classes: `ST_TuningSettings` line 754; `ST_OT_apply_tuning` line 806 methods: execute; `ST_OT_keyframe_tuning` line 817 methods: execute; `ST_OT_scale_animation` line 828 methods: execute; `ST_OT_apply_runtime_profile` line 839 methods: execute; `ST_OT_hot_update_scene` line 855 methods: execute; `ST_OT_save_preset` line 877 methods: execute; `ST_OT_load_preset` line 888 methods: execute; `ST_OT_open_guide_text` line 904 methods: execute; `ST_OT_select_group` line 923 methods: execute; `ST_PT_tuning_panel` line 958 methods: draw
- Functions: `resolve_script_dir()` line 19; `iter_action_fcurves(action)` line 50; `find_obj(name)` line 82; `objects_with_prefix(prefix)` line 86; `particle_emitters()` line 90; `particle_source_objects()` line 100; `store_base_vector(obj, key, value)` line 111; `store_base_float(idblock, key, value)` line 117; `set_scale_from_base(obj, factor, key)` line 126; `keyframe_if_possible(idblock, data_path, frame)` line 134; `find_material(name)` line 141; `find_node(material_name, node_name)` line 145; `set_value_node(material_name, node_name, value)` line 152; `set_input_node(material_name, node_name, input_name, value)` line 163; `keyframe_socket(socket, frame)` line 174; `get_scene_compositor_tree(scene)` line 180; `clamp_value(value, min_value, max_value)` line 188; `normalize_runtime_profile(profile)` line 192; `runtime_profile_label(profile)` line 238; `apply_runtime_profile(context, profile)` line 251; `all_particle_settings()` line 426; `apply_tuning(context, insert_keyframes)` line 438; `scale_fcurve_values(idblock, predicate, factor)` line 653; `scale_full_animation(context)` line 669; `preset_data(settings)` line 705; `load_preset_data(settings, data)` line 748; `register()` line 1074; `unregister()` line 1089
- Assignments: `bl_info`, `SCRIPT_DIR`, `PRESET_PATH`, `GUIDE_PATH`, `HOT_UPDATE_PATH`, `classes`

## Content
```py
00001: bl_info = {
00002:     "name": "Spaziotempo Scene Tuning Panel",
00003:     "author": "Codex + Carmine",
00004:     "version": (0, 1, 0),
00005:     "blender": (5, 0, 0),
00006:     "location": "View3D > Sidebar > Spaziotempo",
00007:     "description": "Manual tuning controls for the Spaziotempo audio visual scene.",
00008:     "category": "3D View",
00009: }
00010: 
00011: import json
00012: import traceback
00013: from pathlib import Path
00014: 
00015: import bpy
00016: from bpy.props import BoolProperty, FloatProperty, PointerProperty, StringProperty
00017: 
00018: 
00019: def resolve_script_dir():
00020:     candidates = []
00021: 
00022:     try:
00023:         text = bpy.context.space_data.text
00024:         if text is not None and text.filepath:
00025:             candidates.append(Path(text.filepath).resolve().parent)
00026:     except Exception:
00027:         pass
00028: 
00029:     if "__file__" in globals():
00030:         try:
00031:             candidates.append(Path(__file__).resolve().parent)
00032:         except Exception:
00033:             pass
00034: 
00035:     candidates.append(Path.home() / "blender" / "blender-audio-project" / "Scripting" / "v61b")
00036: 
00037:     for candidate in candidates:
00038:         if (candidate / "config.py").exists() and (candidate / "hot_update_scene_v61b.py").exists():
00039:             return candidate
00040: 
00041:     return candidates[-1]
00042: 
00043: 
00044: SCRIPT_DIR = resolve_script_dir()
00045: PRESET_PATH = SCRIPT_DIR / "scene_tuning_preset.json"
00046: GUIDE_PATH = SCRIPT_DIR / "SCENE_TUNING_GUIDE.md"
00047: HOT_UPDATE_PATH = SCRIPT_DIR / "hot_update_scene_v61b.py"
00048: 
00049: 
00050: def iter_action_fcurves(action):
00051:     if action is None:
00052:         return
00053: 
00054:     if hasattr(action, "fcurves"):
00055:         try:
00056:             for fcurve in action.fcurves:
00057:                 yield fcurve
00058:             return
00059:         except Exception:
00060:             pass
00061: 
00062:     layers = getattr(action, "layers", None)
00063:     if not layers:
00064:         return
00065: 
00066:     for layer in layers:
00067:         strips = getattr(layer, "strips", None)
00068:         if not strips:
00069:             continue
00070:         for strip in strips:
00071:             channelbags = getattr(strip, "channelbags", None)
00072:             if not channelbags:
00073:                 continue
00074:             for channelbag in channelbags:
00075:                 fcurves = getattr(channelbag, "fcurves", None)
00076:                 if not fcurves:
00077:                     continue
00078:                 for fcurve in fcurves:
00079:                     yield fcurve
00080: 
00081: 
00082: def find_obj(name):
00083:     return bpy.data.objects.get(name)
00084: 
00085: 
00086: def objects_with_prefix(prefix):
00087:     return [obj for obj in bpy.data.objects if obj.name.startswith(prefix)]
00088: 
00089: 
00090: def particle_emitters():
00091:     names = [
00092:         "BeatPulseParticleEmitter",
00093:         "OrbitDustParticleEmitter",
00094:         "HighStreakParticleEmitter",
00095:         "AlbumLetterParticleEmitter",
00096:     ]
00097:     return [obj for name in names if (obj := find_obj(name)) is not None]
00098: 
00099: 
00100: def particle_source_objects():
00101:     names = [
00102:         "BeatSparkParticle",
00103:         "OrbitDustParticle",
00104:         "HighStreakParticle",
00105:     ]
00106:     sources = [obj for name in names if (obj := find_obj(name)) is not None]
00107:     sources.extend(objects_with_prefix("AlbumLetterParticle_"))
00108:     return sources
00109: 
00110: 
00111: def store_base_vector(obj, key, value):
00112:     if key not in obj:
00113:         obj[key] = [float(value.x), float(value.y), float(value.z)]
00114:     return obj[key]
00115: 
00116: 
00117: def store_base_float(idblock, key, value):
00118:     try:
00119:         if key not in idblock:
00120:             idblock[key] = float(value)
00121:         return float(idblock[key])
00122:     except Exception:
00123:         return float(value)
00124: 
00125: 
00126: def set_scale_from_base(obj, factor, key="_st_base_scale"):
00127:     if obj is None:
00128:         return
00129: 
00130:     base = store_base_vector(obj, key, obj.scale)
00131:     obj.scale = (base[0] * factor, base[1] * factor, base[2] * factor)
00132: 
00133: 
00134: def keyframe_if_possible(idblock, data_path, frame):
00135:     try:
00136:         idblock.keyframe_insert(data_path=data_path, frame=frame)
00137:     except Exception:
00138:         pass
00139: 
00140: 
00141: def find_material(name):
00142:     return bpy.data.materials.get(name)
00143: 
00144: 
00145: def find_node(material_name, node_name):
00146:     material = find_material(material_name)
00147:     if material is None or not material.use_nodes:
00148:         return None
00149:     return material.node_tree.nodes.get(node_name)
00150: 
00151: 
00152: def set_value_node(material_name, node_name, value):
00153:     node = find_node(material_name, node_name)
00154:     if node is None:
00155:         return None
00156:     try:
00157:         node.outputs[0].default_value = value
00158:         return node.outputs[0]
00159:     except Exception:
00160:         return None
00161: 
00162: 
00163: def set_input_node(material_name, node_name, input_name, value):
00164:     node = find_node(material_name, node_name)
00165:     if node is None:
00166:         return None
00167:     try:
00168:         node.inputs[input_name].default_value = value
00169:         return node.inputs[input_name]
00170:     except Exception:
00171:         return None
00172: 
00173: 
00174: def keyframe_socket(socket, frame):
00175:     if socket is None:
00176:         return
00177:     keyframe_if_possible(socket, "default_value", frame)
00178: 
00179: 
00180: def get_scene_compositor_tree(scene):
00181:     for attr in ("node_tree", "compositor_node_tree"):
00182:         tree = getattr(scene, attr, None)
00183:         if tree is not None:
00184:             return tree
00185:     return None
00186: 
00187: 
00188: def clamp_value(value, min_value, max_value):
00189:     return max(min_value, min(max_value, value))
00190: 
00191: 
00192: def normalize_runtime_profile(profile):
00193:     if isinstance(profile, bool):
00194:         return "YOUTUBE_4K" if profile else "PREVIEW"
00195: 
00196:     profile = str(profile or "PREVIEW").upper().replace(" ", "_").replace("-", "_")
00197:     aliases = {
00198:         "FINAL": "YOUTUBE_1440P",
00199:         "YOUTUBE": "YOUTUBE_1440P",
00200:         "YOUTUBE_FINAL": "YOUTUBE_1440P",
00201:         "YOUTUBE_FINAL_1440P": "YOUTUBE_1440P",
00202:         "YOUTUBE_FAST": "YOUTUBE_FAST_1440P",
00203:         "YOUTUBE_FAST_1440P": "YOUTUBE_FAST_1440P",
00204:         "YT_FAST": "YOUTUBE_FAST_1440P",
00205:         "YT_FAST_1440": "YOUTUBE_FAST_1440P",
00206:         "YT_FAST_1440P": "YOUTUBE_FAST_1440P",
00207:         "YT_FINAL": "YOUTUBE_1440P",
00208:         "YT_1440": "YOUTUBE_1440P",
00209:         "YT_1440P": "YOUTUBE_1440P",
00210:         "1440": "YOUTUBE_1440P",
00211:         "1440P": "YOUTUBE_1440P",
00212:         "YT_4K": "YOUTUBE_4K",
00213:         "YOUTUBE_FINAL_4K": "YOUTUBE_4K",
00214:         "YOUTUBE_FAST_4K": "YOUTUBE_FAST_4K",
00215:         "YT_FAST_4K": "YOUTUBE_FAST_4K",
00216:         "4K": "YOUTUBE_4K",
00217:         "YT_1080": "YOUTUBE_1080P",
00218:         "YT_1080P": "YOUTUBE_1080P",
00219:         "YOUTUBE_FINAL_1080P": "YOUTUBE_1080P",
00220:         "YOUTUBE_FAST_1080P": "YOUTUBE_FAST_1080P",
00221:         "YT_FAST_1080": "YOUTUBE_FAST_1080P",
00222:         "YT_FAST_1080P": "YOUTUBE_FAST_1080P",
00223:         "1080": "YOUTUBE_1080P",
00224:         "1080P": "YOUTUBE_1080P",
00225:     }
00226:     valid = {
00227:         "PREVIEW",
00228:         "YOUTUBE_FAST_1080P",
00229:         "YOUTUBE_FAST_1440P",
00230:         "YOUTUBE_FAST_4K",
00231:         "YOUTUBE_1080P",
00232:         "YOUTUBE_1440P",
00233:         "YOUTUBE_4K",
00234:     }
00235:     return aliases.get(profile, profile if profile in valid else "PREVIEW")
00236: 
00237: 
00238: def runtime_profile_label(profile):
00239:     labels = {
00240:         "PREVIEW": "Preview",
00241:         "YOUTUBE_FAST_1080P": "YouTube Fast 1080p",
00242:         "YOUTUBE_FAST_1440P": "YouTube Fast 1440p",
00243:         "YOUTUBE_FAST_4K": "YouTube Fast 4K",
00244:         "YOUTUBE_1080P": "YouTube Final 1080p",
00245:         "YOUTUBE_1440P": "YouTube Final 1440p",
00246:         "YOUTUBE_4K": "YouTube Final 4K",
00247:     }
00248:     return labels.get(normalize_runtime_profile(profile), "Preview")
00249: 
00250: 
00251: def apply_runtime_profile(context, profile):
00252:     scene = context.scene
00253:     render = scene.render
00254:     profile = normalize_runtime_profile(profile)
00255:     final_for_youtube = profile.startswith("YOUTUBE_")
00256: 
00257:     if profile == "YOUTUBE_FAST_4K":
00258:         render.resolution_x = 3840
00259:         render.resolution_y = 2160
00260:         render.resolution_percentage = 100
00261:         render.use_motion_blur = False
00262:         fstop = 3.8
00263:         taa_samples = 64
00264:         volumetric_samples = 32
00265:         video_bitrate = 40000
00266:         video_maxrate = 45000
00267:         bloom_intensity = 0.020
00268:         compositor_threshold = 1.62
00269:         compositor_lens = 1.0
00270:         lens_distort = 0.010
00271:         lens_dispersion = 0.012
00272:         rhythm_light_power = 1.0
00273:     elif profile == "YOUTUBE_FAST_1440P":
00274:         render.resolution_x = 2560
00275:         render.resolution_y = 1440
00276:         render.resolution_percentage = 100
00277:         render.use_motion_blur = False
00278:         fstop = 3.8
00279:         taa_samples = 64
00280:         volumetric_samples = 32
00281:         video_bitrate = 24000
00282:         video_maxrate = 30000
00283:         bloom_intensity = 0.020
00284:         compositor_threshold = 1.62
00285:         compositor_lens = 1.0
00286:         lens_distort = 0.010
00287:         lens_dispersion = 0.012
00288:         rhythm_light_power = 1.0
00289:     elif profile == "YOUTUBE_FAST_1080P":
00290:         render.resolution_x = 1920
00291:         render.resolution_y = 1080
00292:         render.resolution_percentage = 100
00293:         render.use_motion_blur = False
00294:         fstop = 3.8
00295:         taa_samples = 64
00296:         volumetric_samples = 32
00297:         video_bitrate = 18000
00298:         video_maxrate = 22000
00299:         bloom_intensity = 0.020
00300:         compositor_threshold = 1.62
00301:         compositor_lens = 1.0
00302:         lens_distort = 0.010
00303:         lens_dispersion = 0.012
00304:         rhythm_light_power = 1.0
00305:     elif profile == "YOUTUBE_4K":
00306:         render.resolution_x = 3840
00307:         render.resolution_y = 2160
00308:         render.resolution_percentage = 100
00309:         render.use_motion_blur = True
00310:         fstop = 3.8
00311:         taa_samples = 96
00312:         volumetric_samples = 64
00313:         video_bitrate = 40000
00314:         video_maxrate = 45000
00315:         bloom_intensity = 0.020
00316:         compositor_threshold = 1.62
00317:         compositor_lens = 1.0
00318:         lens_distort = 0.010
00319:         lens_dispersion = 0.012
00320:         rhythm_light_power = 1.0
00321:     elif profile == "YOUTUBE_1440P":
00322:         render.resolution_x = 2560
00323:         render.resolution_y = 1440
```
