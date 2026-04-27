# Project Code Chunk 57/212

- File: `Scripting/v61b/scene_tuning_panel.py`
- Part: `1`
- Lines: `1-323`

## Symbol Map
- Imports: `json`, `sys`, `traceback`, `from pathlib import Path`, `bpy`, `from bpy.props import BoolProperty, FloatProperty, PointerProperty, StringProperty`
- Classes: `ST_TuningSettings` line 770; `ST_OT_apply_tuning` line 822 methods: execute; `ST_OT_keyframe_tuning` line 833 methods: execute; `ST_OT_scale_animation` line 844 methods: execute; `ST_OT_apply_runtime_profile` line 855 methods: execute; `ST_OT_hot_update_scene` line 871 methods: execute; `ST_OT_rebuild_restart_check` line 895 methods: execute; `ST_OT_optimizer_check` line 920 methods: execute; `ST_OT_load_image_sequence` line 943 methods: execute; `ST_OT_encode_ffmpeg` line 965 methods: execute; `ST_OT_encode_ffmpeg_shell` line 987 methods: execute; `ST_OT_save_preset` line 1016 methods: execute; `ST_OT_load_preset` line 1027 methods: execute; `ST_OT_open_guide_text` line 1043 methods: execute; `ST_OT_select_group` line 1062 methods: execute; `ST_PT_tuning_panel` line 1098 methods: draw
- Functions: `resolve_script_dir()` line 20; `iter_action_fcurves(action)` line 56; `find_obj(name)` line 88; `objects_with_prefix(prefix)` line 92; `particle_emitters()` line 96; `particle_source_objects()` line 106; `store_base_vector(obj, key, value)` line 117; `store_base_float(idblock, key, value)` line 123; `set_scale_from_base(obj, factor, key)` line 132; `keyframe_if_possible(idblock, data_path, frame)` line 140; `find_material(name)` line 147; `find_node(material_name, node_name)` line 151; `set_value_node(material_name, node_name, value)` line 158; `set_input_node(material_name, node_name, input_name, value)` line 169; `keyframe_socket(socket, frame)` line 180; `get_scene_compositor_tree(scene)` line 186; `clamp_value(value, min_value, max_value)` line 194; `normalize_runtime_profile(profile)` line 198; `runtime_profile_label(profile)` line 244; `apply_runtime_profile(context, profile)` line 257; `all_particle_settings()` line 442; `apply_tuning(context, insert_keyframes)` line 454; `scale_fcurve_values(idblock, predicate, factor)` line 669; `scale_full_animation(context)` line 685; `preset_data(settings)` line 721; `load_preset_data(settings, data)` line 764; `register()` line 1239; `unregister()` line 1254
- Assignments: `bl_info`, `SCRIPT_DIR`, `PRESET_PATH`, `GUIDE_PATH`, `HOT_UPDATE_PATH`, `ENCODE_SEQUENCE_PATH`, `ENCODE_FFMPEG_PATH`, `classes`

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
00012: import sys
00013: import traceback
00014: from pathlib import Path
00015: 
00016: import bpy
00017: from bpy.props import BoolProperty, FloatProperty, PointerProperty, StringProperty
00018: 
00019: 
00020: def resolve_script_dir():
00021:     candidates = []
00022: 
00023:     try:
00024:         text = bpy.context.space_data.text
00025:         if text is not None and text.filepath:
00026:             candidates.append(Path(text.filepath).resolve().parent)
00027:     except Exception:
00028:         pass
00029: 
00030:     if "__file__" in globals():
00031:         try:
00032:             candidates.append(Path(__file__).resolve().parent)
00033:         except Exception:
00034:             pass
00035: 
00036:     candidates.append(Path.home() / "blender" / "blender-audio-project" / "Scripting" / "v61b")
00037: 
00038:     for candidate in candidates:
00039:         if (candidate / "config.py").exists() and (candidate / "hot_update_scene_v61b.py").exists():
00040:             return candidate
00041: 
00042:     return candidates[-1]
00043: 
00044: 
00045: SCRIPT_DIR = resolve_script_dir()
00046: PRESET_PATH = SCRIPT_DIR / "scene_tuning_preset.json"
00047: GUIDE_PATH = SCRIPT_DIR / "SCENE_TUNING_GUIDE.md"
00048: HOT_UPDATE_PATH = SCRIPT_DIR / "hot_update_scene_v61b.py"
00049: ENCODE_SEQUENCE_PATH = SCRIPT_DIR / "encode_image_sequence_v61b.py"
00050: ENCODE_FFMPEG_PATH = SCRIPT_DIR / "encode_ffmpeg_v61b.py"
00051: 
00052: if str(SCRIPT_DIR) not in sys.path:
00053:     sys.path.insert(0, str(SCRIPT_DIR))
00054: 
00055: 
00056: def iter_action_fcurves(action):
00057:     if action is None:
00058:         return
00059: 
00060:     if hasattr(action, "fcurves"):
00061:         try:
00062:             for fcurve in action.fcurves:
00063:                 yield fcurve
00064:             return
00065:         except Exception:
00066:             pass
00067: 
00068:     layers = getattr(action, "layers", None)
00069:     if not layers:
00070:         return
00071: 
00072:     for layer in layers:
00073:         strips = getattr(layer, "strips", None)
00074:         if not strips:
00075:             continue
00076:         for strip in strips:
00077:             channelbags = getattr(strip, "channelbags", None)
00078:             if not channelbags:
00079:                 continue
00080:             for channelbag in channelbags:
00081:                 fcurves = getattr(channelbag, "fcurves", None)
00082:                 if not fcurves:
00083:                     continue
00084:                 for fcurve in fcurves:
00085:                     yield fcurve
00086: 
00087: 
00088: def find_obj(name):
00089:     return bpy.data.objects.get(name)
00090: 
00091: 
00092: def objects_with_prefix(prefix):
00093:     return [obj for obj in bpy.data.objects if obj.name.startswith(prefix)]
00094: 
00095: 
00096: def particle_emitters():
00097:     names = [
00098:         "BeatPulseParticleEmitter",
00099:         "OrbitDustParticleEmitter",
00100:         "HighStreakParticleEmitter",
00101:         "AlbumLetterParticleEmitter",
00102:     ]
00103:     return [obj for name in names if (obj := find_obj(name)) is not None]
00104: 
00105: 
00106: def particle_source_objects():
00107:     names = [
00108:         "BeatSparkParticle",
00109:         "OrbitDustParticle",
00110:         "HighStreakParticle",
00111:     ]
00112:     sources = [obj for name in names if (obj := find_obj(name)) is not None]
00113:     sources.extend(objects_with_prefix("AlbumLetterParticle_"))
00114:     return sources
00115: 
00116: 
00117: def store_base_vector(obj, key, value):
00118:     if key not in obj:
00119:         obj[key] = [float(value.x), float(value.y), float(value.z)]
00120:     return obj[key]
00121: 
00122: 
00123: def store_base_float(idblock, key, value):
00124:     try:
00125:         if key not in idblock:
00126:             idblock[key] = float(value)
00127:         return float(idblock[key])
00128:     except Exception:
00129:         return float(value)
00130: 
00131: 
00132: def set_scale_from_base(obj, factor, key="_st_base_scale"):
00133:     if obj is None:
00134:         return
00135: 
00136:     base = store_base_vector(obj, key, obj.scale)
00137:     obj.scale = (base[0] * factor, base[1] * factor, base[2] * factor)
00138: 
00139: 
00140: def keyframe_if_possible(idblock, data_path, frame):
00141:     try:
00142:         idblock.keyframe_insert(data_path=data_path, frame=frame)
00143:     except Exception:
00144:         pass
00145: 
00146: 
00147: def find_material(name):
00148:     return bpy.data.materials.get(name)
00149: 
00150: 
00151: def find_node(material_name, node_name):
00152:     material = find_material(material_name)
00153:     if material is None or not material.use_nodes:
00154:         return None
00155:     return material.node_tree.nodes.get(node_name)
00156: 
00157: 
00158: def set_value_node(material_name, node_name, value):
00159:     node = find_node(material_name, node_name)
00160:     if node is None:
00161:         return None
00162:     try:
00163:         node.outputs[0].default_value = value
00164:         return node.outputs[0]
00165:     except Exception:
00166:         return None
00167: 
00168: 
00169: def set_input_node(material_name, node_name, input_name, value):
00170:     node = find_node(material_name, node_name)
00171:     if node is None:
00172:         return None
00173:     try:
00174:         node.inputs[input_name].default_value = value
00175:         return node.inputs[input_name]
00176:     except Exception:
00177:         return None
00178: 
00179: 
00180: def keyframe_socket(socket, frame):
00181:     if socket is None:
00182:         return
00183:     keyframe_if_possible(socket, "default_value", frame)
00184: 
00185: 
00186: def get_scene_compositor_tree(scene):
00187:     for attr in ("node_tree", "compositor_node_tree"):
00188:         tree = getattr(scene, attr, None)
00189:         if tree is not None:
00190:             return tree
00191:     return None
00192: 
00193: 
00194: def clamp_value(value, min_value, max_value):
00195:     return max(min_value, min(max_value, value))
00196: 
00197: 
00198: def normalize_runtime_profile(profile):
00199:     if isinstance(profile, bool):
00200:         return "YOUTUBE_4K" if profile else "PREVIEW"
00201: 
00202:     profile = str(profile or "PREVIEW").upper().replace(" ", "_").replace("-", "_")
00203:     aliases = {
00204:         "FINAL": "YOUTUBE_1440P",
00205:         "YOUTUBE": "YOUTUBE_1440P",
00206:         "YOUTUBE_FINAL": "YOUTUBE_1440P",
00207:         "YOUTUBE_FINAL_1440P": "YOUTUBE_1440P",
00208:         "YOUTUBE_FAST": "YOUTUBE_FAST_1440P",
00209:         "YOUTUBE_FAST_1440P": "YOUTUBE_FAST_1440P",
00210:         "YT_FAST": "YOUTUBE_FAST_1440P",
00211:         "YT_FAST_1440": "YOUTUBE_FAST_1440P",
00212:         "YT_FAST_1440P": "YOUTUBE_FAST_1440P",
00213:         "YT_FINAL": "YOUTUBE_1440P",
00214:         "YT_1440": "YOUTUBE_1440P",
00215:         "YT_1440P": "YOUTUBE_1440P",
00216:         "1440": "YOUTUBE_1440P",
00217:         "1440P": "YOUTUBE_1440P",
00218:         "YT_4K": "YOUTUBE_4K",
00219:         "YOUTUBE_FINAL_4K": "YOUTUBE_4K",
00220:         "YOUTUBE_FAST_4K": "YOUTUBE_FAST_4K",
00221:         "YT_FAST_4K": "YOUTUBE_FAST_4K",
00222:         "4K": "YOUTUBE_4K",
00223:         "YT_1080": "YOUTUBE_1080P",
00224:         "YT_1080P": "YOUTUBE_1080P",
00225:         "YOUTUBE_FINAL_1080P": "YOUTUBE_1080P",
00226:         "YOUTUBE_FAST_1080P": "YOUTUBE_FAST_1080P",
00227:         "YT_FAST_1080": "YOUTUBE_FAST_1080P",
00228:         "YT_FAST_1080P": "YOUTUBE_FAST_1080P",
00229:         "1080": "YOUTUBE_1080P",
00230:         "1080P": "YOUTUBE_1080P",
00231:     }
00232:     valid = {
00233:         "PREVIEW",
00234:         "YOUTUBE_FAST_1080P",
00235:         "YOUTUBE_FAST_1440P",
00236:         "YOUTUBE_FAST_4K",
00237:         "YOUTUBE_1080P",
00238:         "YOUTUBE_1440P",
00239:         "YOUTUBE_4K",
00240:     }
00241:     return aliases.get(profile, profile if profile in valid else "PREVIEW")
00242: 
00243: 
00244: def runtime_profile_label(profile):
00245:     labels = {
00246:         "PREVIEW": "Preview",
00247:         "YOUTUBE_FAST_1080P": "YouTube Fast 1080p",
00248:         "YOUTUBE_FAST_1440P": "YouTube Fast 1440p",
00249:         "YOUTUBE_FAST_4K": "YouTube Fast 4K",
00250:         "YOUTUBE_1080P": "YouTube Final 1080p",
00251:         "YOUTUBE_1440P": "YouTube Final 1440p",
00252:         "YOUTUBE_4K": "YouTube Final 4K",
00253:     }
00254:     return labels.get(normalize_runtime_profile(profile), "Preview")
00255: 
00256: 
00257: def apply_runtime_profile(context, profile):
00258:     scene = context.scene
00259:     render = scene.render
00260:     profile = normalize_runtime_profile(profile)
00261:     final_for_youtube = profile.startswith("YOUTUBE_")
00262: 
00263:     if profile == "YOUTUBE_FAST_4K":
00264:         render.resolution_x = 3840
00265:         render.resolution_y = 2160
00266:         render.resolution_percentage = 100
00267:         render.use_motion_blur = False
00268:         fstop = 3.8
00269:         taa_samples = 48
00270:         volumetric_samples = 12
00271:         video_bitrate = 40000
00272:         video_maxrate = 45000
00273:         bloom_intensity = 0.020
00274:         compositor_threshold = 1.62
00275:         compositor_lens = 1.0
00276:         lens_distort = 0.010
00277:         lens_dispersion = 0.012
00278:         rhythm_light_power = 1.0
00279:     elif profile == "YOUTUBE_FAST_1440P":
00280:         render.resolution_x = 2560
00281:         render.resolution_y = 1440
00282:         render.resolution_percentage = 100
00283:         render.use_motion_blur = False
00284:         fstop = 3.8
00285:         taa_samples = 48
00286:         volumetric_samples = 12
00287:         video_bitrate = 24000
00288:         video_maxrate = 30000
00289:         bloom_intensity = 0.020
00290:         compositor_threshold = 1.62
00291:         compositor_lens = 1.0
00292:         lens_distort = 0.010
00293:         lens_dispersion = 0.012
00294:         rhythm_light_power = 1.0
00295:     elif profile == "YOUTUBE_FAST_1080P":
00296:         render.resolution_x = 1920
00297:         render.resolution_y = 1080
00298:         render.resolution_percentage = 100
00299:         render.use_motion_blur = False
00300:         fstop = 3.8
00301:         taa_samples = 48
00302:         volumetric_samples = 12
00303:         video_bitrate = 18000
00304:         video_maxrate = 22000
00305:         bloom_intensity = 0.020
00306:         compositor_threshold = 1.62
00307:         compositor_lens = 1.0
00308:         lens_distort = 0.010
00309:         lens_dispersion = 0.012
00310:         rhythm_light_power = 1.0
00311:     elif profile == "YOUTUBE_4K":
00312:         render.resolution_x = 3840
00313:         render.resolution_y = 2160
00314:         render.resolution_percentage = 100
00315:         render.use_motion_blur = True
00316:         fstop = 3.8
00317:         taa_samples = 64
00318:         volumetric_samples = 24
00319:         video_bitrate = 40000
00320:         video_maxrate = 45000
00321:         bloom_intensity = 0.020
00322:         compositor_threshold = 1.62
00323:         compositor_lens = 1.0
```
