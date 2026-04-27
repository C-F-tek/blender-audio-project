# Project Code Chunk 37/212

- File: `Scripting/v61b/hotpatch/diagnostics.py`
- Part: `1`
- Lines: `1-276`

## Symbol Map
- Imports: `bpy`, `from common import ANALYSIS_JSON_PATH, cfg_value, load_analysis`, `from spaziotempo.core.registry import LAYER_ORDER, LAYER_SPECS, PROJECT_ROOT_COLLECTION`
- Functions: `text_report(name, lines)` line 17; `has_object(name)` line 24; `count_objects(prefix)` line 28; `collection_exists(name)` line 32; `layer_collection_counts()` line 36; `scene_frame_count(scene)` line 45; `material_node_exists(node_name)` line 49; `modifier_exists(mod_name)` line 56; `point_cache_state(cache)` line 64; `particle_cache_state(ps)` line 72; `analyze_rebuild_need()` line 83; `analyze_optimizer()` line 169
- Assignments: `STRUCTURAL_OBJECTS`

## Content
```py
00001: import bpy
00002: 
00003: from .common import ANALYSIS_JSON_PATH, cfg_value, load_analysis
00004: from spaziotempo.core.registry import LAYER_ORDER, LAYER_SPECS, PROJECT_ROOT_COLLECTION
00005: 
00006: 
00007: STRUCTURAL_OBJECTS = [
00008:     "HeroRoot",
00009:     "MainCamera",
00010:     "CameraTarget",
00011:     "AtmosphereCube",
00012:     "FogPulseController",
00013:     "SoftRhythmBackdrop",
00014: ]
00015: 
00016: 
00017: def text_report(name, lines):
00018:     text = bpy.data.texts.get(name) or bpy.data.texts.new(name)
00019:     text.clear()
00020:     text.write("\n".join(lines))
00021:     return text
00022: 
00023: 
00024: def has_object(name):
00025:     return bpy.data.objects.get(name) is not None
00026: 
00027: 
00028: def count_objects(prefix):
00029:     return sum(1 for obj in bpy.data.objects if obj.name.startswith(prefix))
00030: 
00031: 
00032: def collection_exists(name):
00033:     return bpy.data.collections.get(name) is not None
00034: 
00035: 
00036: def layer_collection_counts():
00037:     counts = {}
00038:     for key in LAYER_ORDER:
00039:         spec = LAYER_SPECS[key]
00040:         collection = bpy.data.collections.get(spec.collection)
00041:         counts[key] = len(collection.objects) if collection is not None else 0
00042:     return counts
00043: 
00044: 
00045: def scene_frame_count(scene):
00046:     return max(0, int(scene.frame_end) - int(scene.frame_start) + 1)
00047: 
00048: 
00049: def material_node_exists(node_name):
00050:     for mat in bpy.data.materials:
00051:         if mat is not None and mat.use_nodes and mat.node_tree.nodes.get(node_name) is not None:
00052:             return True
00053:     return False
00054: 
00055: 
00056: def modifier_exists(mod_name):
00057:     for obj in bpy.data.objects:
00058:         for mod in obj.modifiers:
00059:             if mod.name == mod_name:
00060:                 return True
00061:     return False
00062: 
00063: 
00064: def point_cache_state(cache):
00065:     if cache is None:
00066:         return "no-cache"
00067:     if getattr(cache, "is_baked", False):
00068:         return "baked"
00069:     return "not-baked"
00070: 
00071: 
00072: def particle_cache_state(ps):
00073:     cache = getattr(ps, "point_cache", None)
00074:     if cache is None:
00075:         return "no-cache"
00076:     if getattr(cache, "is_baked", False):
00077:         return "baked"
00078:     if getattr(cache, "use_disk_cache", False):
00079:         return "disk-cache-on"
00080:     return "not-baked"
00081: 
00082: 
00083: def analyze_rebuild_need():
00084:     scene = bpy.context.scene
00085:     _, frames = load_analysis()
00086:     expected_frames = len(frames)
00087:     current_frames = scene_frame_count(scene)
00088: 
00089:     blocking = []
00090:     warnings = []
00091:     ok = []
00092: 
00093:     for name in STRUCTURAL_OBJECTS:
00094:         if has_object(name):
00095:             ok.append(f"OK object: {name}")
00096:         else:
00097:             blocking.append(f"Missing structural object `{name}`: run `main_v61b.py`.")
00098: 
00099:     if count_objects("PhysicsAccent_") == 0:
00100:         warnings.append("No `PhysicsAccent_*` objects found: Physics hotpatch has nothing to update.")
00101:     else:
00102:         ok.append(f"OK PhysicsAccent objects: {count_objects('PhysicsAccent_')}")
00103: 
00104:     if not modifier_exists("HeroAudioMeshDisplace"):
00105:         warnings.append("Hero mesh deform modifier missing: run full rebuild if you expect mesh deformation.")
00106:     else:
00107:         ok.append("OK hero mesh deform modifier")
00108: 
00109:     if not material_node_exists("HeroMatEmissionValue"):
00110:         warnings.append("Hero audio material nodes missing: use Hot Update Materials or full rebuild.")
00111:     else:
00112:         ok.append("OK hero material nodes")
00113: 
00114:     if expected_frames and current_frames != expected_frames:
00115:         blocking.append(
00116:             f"Frame count mismatch: scene has {current_frames}, analysis has {expected_frames}. Run `main_v61b.py`."
00117:         )
00118:     elif expected_frames:
00119:         ok.append(f"OK frame count: {current_frames}")
00120:     else:
00121:         warnings.append(f"Analysis file not loaded/found: {ANALYSIS_JSON_PATH}")
00122: 
00123:     if not has_object("HeroGravityField") and has_object("PulseForceField"):
00124:         warnings.append("Old `PulseForceField` found: Hot Update Physics can rename/update it.")
00125:     elif not has_object("HeroGravityField"):
00126:         warnings.append("No `HeroGravityField`: Hot Update Physics can create it, full rebuild creates it cleanly.")
00127:     else:
00128:         ok.append("OK HeroGravityField")
00129: 
00130:     if collection_exists(PROJECT_ROOT_COLLECTION):
00131:         ok.append(f"OK layer root collection: {PROJECT_ROOT_COLLECTION}")
00132:     else:
00133:         warnings.append("Layer collections missing: use Hot Update All or rebuild with updated `main_v61b.py`.")
00134: 
00135:     restart = []
00136:     if not hasattr(bpy.types.Scene, "spaziotempo_tuning"):
00137:         restart.append("Panel properties not registered: run `scene_tuning_panel.py` or rebuild with updated `main_v61b.py`.")
00138: 
00139:     lines = [
00140:         "SPAZIOTEMPO REBUILD / RESTART CHECK",
00141:         "=" * 52,
00142:         f"Result: {'FULL REBUILD NEEDED' if blocking else 'HOTPATCH SHOULD BE ENOUGH'}",
00143:         "",
00144:     ]
00145:     if blocking:
00146:         lines.append("Full rebuild triggers:")
00147:         lines.extend(f"- {item}" for item in blocking)
00148:         lines.append("")
00149:     if warnings:
00150:         lines.append("Warnings:")
00151:         lines.extend(f"- {item}" for item in warnings)
00152:         lines.append("")
00153:     if restart:
00154:         lines.append("Registration/restart notes:")
00155:         lines.extend(f"- {item}" for item in restart)
00156:         lines.append("")
00157:     lines.append("Checked OK:")
00158:     lines.extend(f"- {item}" for item in ok)
00159: 
00160:     text_report("SPAZIOTEMPO_REBUILD_CHECK", lines)
00161:     return {
00162:         "blocking": blocking,
00163:         "warnings": warnings,
00164:         "restart": restart,
00165:         "report": "\n".join(lines),
00166:     }
00167: 
00168: 
00169: def analyze_optimizer():
00170:     scene = bpy.context.scene
00171:     warnings = []
00172:     suggestions = []
00173:     ok = []
00174: 
00175:     particle_systems = []
00176:     for obj in bpy.data.objects:
00177:         for mod in obj.modifiers:
00178:             if mod.type == 'PARTICLE_SYSTEM':
00179:                 ps = getattr(mod, "particle_system", None)
00180:                 if ps is not None:
00181:                     particle_systems.append((obj, ps, mod))
00182: 
00183:     if particle_systems:
00184:         unbaked = []
00185:         for obj, ps, _ in particle_systems:
00186:             state = particle_cache_state(ps)
00187:             settings = getattr(ps, "settings", None)
00188:             physics_type = getattr(settings, "physics_type", "")
00189:             if state != "baked" and physics_type not in {"NO", "NONE", ""}:
00190:                 unbaked.append(f"{obj.name} / {ps.name}: {state}, physics={physics_type}")
00191:         if unbaked:
00192:             warnings.append("Particle systems with simulation are not baked/cache-confirmed.")
00193:             suggestions.extend(f"Bake or disk-cache particle system: {item}" for item in unbaked)
00194:         else:
00195:             ok.append(f"Particle systems checked: {len(particle_systems)}")
00196:     else:
00197:         ok.append("No particle systems active")
00198: 
00199:     rb_world = getattr(scene, "rigidbody_world", None)
00200:     active_rigid = [
00201:         obj for obj in bpy.data.objects
00202:         if getattr(obj, "rigid_body", None) is not None
00203:         and obj.rigid_body.type == 'ACTIVE'
00204:         and not getattr(obj.rigid_body, "kinematic", False)
00205:     ]
00206:     if active_rigid:
00207:         state = point_cache_state(getattr(rb_world, "point_cache", None) if rb_world else None)
00208:         if state != "baked":
00209:             warnings.append(f"{len(active_rigid)} active rigid bodies are dynamic and rigid body cache is {state}.")
00210:             suggestions.append("Bake rigid body cache before final render or make those bodies kinematic/keyframed.")
00211:         else:
00212:             ok.append("Rigid body cache baked")
00213:     else:
00214:         ok.append("No unbaked dynamic rigid bodies detected")
00215: 
00216:     sim_mods = []
00217:     for obj in bpy.data.objects:
00218:         for mod in obj.modifiers:
00219:             if mod.type in {"CLOTH", "FLUID", "SOFT_BODY", "DYNAMIC_PAINT"}:
00220:                 sim_mods.append(f"{obj.name} / {mod.name} ({mod.type})")
00221:     if sim_mods:
00222:         warnings.append("Simulation modifiers found.")
00223:         suggestions.extend(f"Check/bake cache: {item}" for item in sim_mods)
00224:     else:
00225:         ok.append("No cloth/fluid/soft-body simulation modifiers")
00226: 
00227:     output_mode = str(cfg_value("RENDER_OUTPUT_MODE", "")).upper()
00228:     if output_mode == "IMAGE_SEQUENCE":
00229:         ok.append("Image sequence output active: good for long renders and resume workflow")
00230:     else:
00231:         suggestions.append("For long final renders, IMAGE_SEQUENCE is safer than direct MP4.")
00232: 
00233:     if bool(cfg_value("FOG_VOLUME_ENABLED", False)):
00234:         suggestions.append("Volumetric fog is enabled: use fog filaments for faster renders and fewer square artifacts.")
00235:     else:
00236:         ok.append("Volumetric fog disabled: fog filaments should avoid Eevee grid artifacts")
00237: 
00238:     if bool(cfg_value("ENCODE_USE_EXTERNAL_FFMPEG", False)):
00239:         ok.append("External ffmpeg encode enabled: better MP4 quality for fog/gradients")
00240: 
00241:     counts = layer_collection_counts()
00242:     if any(counts.values()):
00243:         visible_counts = [
00244:             f"{LAYER_SPECS[key].collection}={count}"
00245:             for key, count in counts.items()
00246:             if count
00247:         ]
00248:         ok.append("Layer classification: " + ", ".join(visible_counts))
00249:     else:
00250:         suggestions.append("Run Hot Update All once to populate ST_* layer collections and object metadata.")
00251: 
00252:     render = scene.render
00253:     if getattr(render, "use_motion_blur", False):
00254:         suggestions.append("Motion blur is on: highest visual cost after volumetrics. Use YT Fast profiles for tests.")
00255: 
00256:     eevee = getattr(scene, "eevee", None)
00257:     if eevee is not None and hasattr(eevee, "volumetric_samples"):
00258:         samples = int(eevee.volumetric_samples)
00259:         if samples > 48:
00260:             suggestions.append(f"Volumetric samples are {samples}: consider 48 final / 24 fast.")
00261:         else:
00262:             ok.append(f"Volumetric samples: {samples}")
00263: 
00264:     lines = [
00265:         "SPAZIOTEMPO OPTIMIZER CHECK",
00266:         "=" * 52,
00267:         f"Result: {'CHECK CACHE / BAKE' if warnings else 'NO REQUIRED BAKE FOUND'}",
00268:         "",
00269:     ]
00270:     if warnings:
00271:         lines.append("Warnings:")
00272:         lines.extend(f"- {item}" for item in warnings)
00273:         lines.append("")
00274:     if suggestions:
00275:         lines.append("Suggestions:")
00276:         lines.extend(f"- {item}" for item in suggestions)
```
