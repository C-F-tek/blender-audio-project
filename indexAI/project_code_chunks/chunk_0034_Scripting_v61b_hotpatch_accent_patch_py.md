# Project Code Chunk 34/212

- File: `Scripting/v61b/hotpatch/accent_patch.py`
- Part: `1`
- Lines: `1-244`

## Symbol Map
- Imports: `math`, `bpy`, `from materials import build_variant_material`, `from common import PALETTE_LIST, cfg_value, clear_animation, get_node, iter_objects_prefix, keyframe_if_possible, socket_by_name, store_base_vector`
- Functions: `drive_for_band(band, response, sample, frame, phase)` line 40; `ensure_accent_material(obj, index)` line 63; `get_or_store_float(obj, key, default)` line 84; `atom_center()` line 90; `find_or_create_force_object(name, effector_type, location)` line 100; `update_central_fields(frames, center)` line 121; `update_physics_accents(frames)` line 175
- Assignments: `PHYSICS_ACCENT_EMISSION_MIN`, `PHYSICS_ACCENT_EMISSION_MAX`, `PHYSICS_ACCENT_MIX_MIN`, `PHYSICS_ACCENT_MIX_MAX`, `PRIMARY_BASE_Z`, `PHYSICS_ORBIT_RADIUS_MIN`, `PHYSICS_ORBIT_RADIUS_MAX`, `PHYSICS_ATOM_ORBIT_SPEED_MIN`, `PHYSICS_ATOM_ORBIT_SPEED_MAX`, `PHYSICS_ATOM_ORBIT_AUDIO_SPEED`, `PHYSICS_ATOM_ORBIT_RADIUS_PULSE`, `PHYSICS_ATOM_ORBIT_HEIGHT_SWAY`, `PHYSICS_ATOM_MICRO_WOBBLE`, `HERO_GRAVITY_STRENGTH_MIN`, `HERO_GRAVITY_STRENGTH_MAX`, `TURB_STRENGTH_MIN`, `TURB_STRENGTH_MAX`, `VORTEX_STRENGTH_MIN`, `VORTEX_STRENGTH_MAX`

## Content
```py
00001: import math
00002: 
00003: import bpy
00004: 
00005: from materials import build_variant_material
00006: 
00007: from .common import (
00008:     PALETTE_LIST,
00009:     cfg_value,
00010:     clear_animation,
00011:     get_node,
00012:     iter_objects_prefix,
00013:     keyframe_if_possible,
00014:     socket_by_name,
00015:     store_base_vector,
00016: )
00017: 
00018: 
00019: PHYSICS_ACCENT_EMISSION_MIN = cfg_value("PHYSICS_ACCENT_EMISSION_MIN", 0.06)
00020: PHYSICS_ACCENT_EMISSION_MAX = cfg_value("PHYSICS_ACCENT_EMISSION_MAX", 0.72)
00021: PHYSICS_ACCENT_MIX_MIN = cfg_value("PHYSICS_ACCENT_MIX_MIN", 0.12)
00022: PHYSICS_ACCENT_MIX_MAX = cfg_value("PHYSICS_ACCENT_MIX_MAX", 0.42)
00023: PRIMARY_BASE_Z = cfg_value("PRIMARY_BASE_Z", 0.72)
00024: PHYSICS_ORBIT_RADIUS_MIN = cfg_value("PHYSICS_ORBIT_RADIUS_MIN", 1.65)
00025: PHYSICS_ORBIT_RADIUS_MAX = cfg_value("PHYSICS_ORBIT_RADIUS_MAX", 3.85)
00026: PHYSICS_ATOM_ORBIT_SPEED_MIN = cfg_value("PHYSICS_ATOM_ORBIT_SPEED_MIN", 0.0048)
00027: PHYSICS_ATOM_ORBIT_SPEED_MAX = cfg_value("PHYSICS_ATOM_ORBIT_SPEED_MAX", 0.0125)
00028: PHYSICS_ATOM_ORBIT_AUDIO_SPEED = cfg_value("PHYSICS_ATOM_ORBIT_AUDIO_SPEED", 0.010)
00029: PHYSICS_ATOM_ORBIT_RADIUS_PULSE = cfg_value("PHYSICS_ATOM_ORBIT_RADIUS_PULSE", 0.105)
00030: PHYSICS_ATOM_ORBIT_HEIGHT_SWAY = cfg_value("PHYSICS_ATOM_ORBIT_HEIGHT_SWAY", 0.36)
00031: PHYSICS_ATOM_MICRO_WOBBLE = cfg_value("PHYSICS_ATOM_MICRO_WOBBLE", 0.075)
00032: HERO_GRAVITY_STRENGTH_MIN = cfg_value("HERO_GRAVITY_STRENGTH_MIN", 5.0)
00033: HERO_GRAVITY_STRENGTH_MAX = cfg_value("HERO_GRAVITY_STRENGTH_MAX", 34.0)
00034: TURB_STRENGTH_MIN = cfg_value("TURB_STRENGTH_MIN", 0.25)
00035: TURB_STRENGTH_MAX = cfg_value("TURB_STRENGTH_MAX", 4.8)
00036: VORTEX_STRENGTH_MIN = cfg_value("VORTEX_STRENGTH_MIN", 0.15)
00037: VORTEX_STRENGTH_MAX = cfg_value("VORTEX_STRENGTH_MAX", 2.6)
00038: 
00039: 
00040: def drive_for_band(band, response, sample, frame, phase):
00041:     low = float(sample.get("low", 0.0))
00042:     mid = float(sample.get("mid", 0.0))
00043:     high = float(sample.get("high", 0.0))
00044:     onset = float(sample.get("onset", 0.0))
00045:     beat = float(sample.get("beat", 0.0))
00046:     pulse = max(onset, beat)
00047:     local_pulse = max(0.0, math.sin(frame * (0.024 + response * 0.016) + phase)) * 0.20
00048: 
00049:     if band == "low":
00050:         drive = low * 0.74 + beat * 0.18 + local_pulse * 0.16
00051:     elif band == "mid":
00052:         drive = mid * 0.68 + low * 0.14 + local_pulse * 0.18
00053:     elif band == "beat":
00054:         drive = beat * 0.70 + low * 0.22 + local_pulse * 0.14
00055:     elif band == "onset":
00056:         drive = onset * 0.72 + high * 0.18 + local_pulse * 0.12
00057:     else:
00058:         drive = high * 0.68 + onset * 0.24 + pulse * 0.08 + local_pulse * 0.12
00059: 
00060:     return max(0.0, min(1.0, drive * response))
00061: 
00062: 
00063: def ensure_accent_material(obj, index):
00064:     mat = obj.active_material
00065:     if mat is None or not mat.use_nodes or get_node(mat, "VariantEmission") is None:
00066:         color = PALETTE_LIST[index % len(PALETTE_LIST)]
00067:         mat = build_variant_material(f"PhysicsAccentMat_hot_{index:02d}", color)
00068:         obj.data.materials.clear()
00069:         obj.data.materials.append(mat)
00070: 
00071:     emission = get_node(mat, "VariantEmission")
00072:     mix = get_node(mat, "VariantEmissionMix")
00073:     emit_socket = socket_by_name(emission, "Strength")
00074:     mix_socket = socket_by_name(mix, 0, is_output=True)
00075: 
00076:     if emit_socket is not None:
00077:         emit_socket.default_value = PHYSICS_ACCENT_EMISSION_MIN
00078:     if mix_socket is not None:
00079:         mix_socket.default_value = PHYSICS_ACCENT_MIX_MIN
00080: 
00081:     return mat, emit_socket, mix_socket
00082: 
00083: 
00084: def get_or_store_float(obj, key, default):
00085:     if key not in obj:
00086:         obj[key] = float(default)
00087:     return float(obj[key])
00088: 
00089: 
00090: def atom_center():
00091:     hero = bpy.data.objects.get("HeroRoot")
00092:     if hero is not None:
00093:         return hero.location.copy()
00094: 
00095:     from mathutils import Vector
00096: 
00097:     return Vector((0.0, 0.0, PRIMARY_BASE_Z + 1.02))
00098: 
00099: 
00100: def find_or_create_force_object(name, effector_type, location):
00101:     obj = bpy.data.objects.get(name)
00102:     if obj is not None:
00103:         return obj
00104: 
00105:     if name == "HeroGravityField":
00106:         old = bpy.data.objects.get("PulseForceField")
00107:         if old is not None:
00108:             old.name = "HeroGravityField"
00109:             return old
00110: 
00111:     try:
00112:         bpy.ops.object.effector_add(type=effector_type, location=location)
00113:         obj = bpy.context.active_object
00114:         obj.name = name
00115:         obj.hide_render = True
00116:         return obj
00117:     except Exception:
00118:         return None
00119: 
00120: 
00121: def update_central_fields(frames, center):
00122:     gravity = find_or_create_force_object("HeroGravityField", 'FORCE', center)
00123:     turbulence = find_or_create_force_object("AtmosphereTurbulence", 'TURBULENCE', center)
00124:     vortex = find_or_create_force_object("OrbitVortex", 'VORTEX', center)
00125: 
00126:     for obj in [gravity, turbulence, vortex]:
00127:         clear_animation(obj)
00128: 
00129:     if not frames:
00130:         frames = [{"low": 0.3, "mid": 0.2, "high": 0.2, "onset": 0.0, "beat": 0.0}]
00131: 
00132:     for frame, sample in enumerate(frames, start=1):
00133:         low = float(sample.get("low", 0.0))
00134:         mid = float(sample.get("mid", 0.0))
00135:         high = float(sample.get("high", 0.0))
00136:         onset = float(sample.get("onset", 0.0))
00137:         beat = float(sample.get("beat", 0.0))
00138:         pulse = max(onset, beat)
00139: 
00140:         if gravity is not None and getattr(gravity, "field", None) is not None:
00141:             gravity_drive = min(1.0, low * 0.44 + mid * 0.14 + pulse * 0.34 + beat * 0.16)
00142:             strength = HERO_GRAVITY_STRENGTH_MIN + gravity_drive * (
00143:                 HERO_GRAVITY_STRENGTH_MAX - HERO_GRAVITY_STRENGTH_MIN
00144:             )
00145:             gravity.field.strength = -strength
00146:             gravity.field.noise = 0.10
00147:             gravity.field.falloff_power = 1.55
00148:             gravity.location.x = center.x
00149:             gravity.location.y = center.y
00150:             gravity.location.z = center.z + 0.34 + math.sin(frame * 0.010) * 0.05
00151:             keyframe_if_possible(gravity, 'field.strength', frame)
00152:             gravity.keyframe_insert(data_path="location", frame=frame)
00153: 
00154:         if turbulence is not None and getattr(turbulence, "field", None) is not None:
00155:             turbulence.field.strength = TURB_STRENGTH_MIN + high * (TURB_STRENGTH_MAX - TURB_STRENGTH_MIN) * 0.64 + pulse * 0.42
00156:             turbulence.location.x = center.x
00157:             turbulence.location.y = center.y
00158:             turbulence.location.z = center.z + 0.74 + math.sin(frame * 0.012) * 0.08
00159:             keyframe_if_possible(turbulence, 'field.strength', frame)
00160:             turbulence.keyframe_insert(data_path="location", frame=frame)
00161: 
00162:         if vortex is not None and getattr(vortex, "field", None) is not None:
00163:             vortex.field.strength = VORTEX_STRENGTH_MIN + (mid * 0.62 + pulse * 0.18) * (
00164:                 VORTEX_STRENGTH_MAX - VORTEX_STRENGTH_MIN
00165:             )
00166:             vortex.location.x = center.x
00167:             vortex.location.y = center.y
00168:             vortex.location.z = center.z + 0.18
00169:             vortex.rotation_euler.z = frame * (0.004 + mid * 0.003 + beat * 0.002)
00170:             keyframe_if_possible(vortex, 'field.strength', frame)
00171:             vortex.keyframe_insert(data_path="location", frame=frame)
00172:             vortex.keyframe_insert(data_path="rotation_euler", frame=frame)
00173: 
00174: 
00175: def update_physics_accents(frames):
00176:     accents = sorted(iter_objects_prefix("PhysicsAccent_"), key=lambda obj: obj.name)
00177:     bands = ["low", "mid", "high", "beat", "onset"]
00178:     center = atom_center()
00179:     update_central_fields(frames, center)
00180: 
00181:     controls = []
00182:     for idx, obj in enumerate(accents):
00183:         anchor = bpy.data.objects.get(f"PhysicsAnchor_{idx:02d}")
00184:         mat, emit_socket, mix_socket = ensure_accent_material(obj, idx)
00185:         clear_animation(obj)
00186:         clear_animation(anchor)
00187:         if mat is not None and mat.use_nodes:
00188:             clear_animation(mat.node_tree)
00189:         try:
00190:             if obj.rigid_body is not None:
00191:                 obj.rigid_body.kinematic = True
00192:         except Exception:
00193:             pass
00194: 
00195:         obj["hot_band"] = bands[idx % len(bands)]
00196:         obj["hot_response"] = float(obj.get("hot_response", 0.42 + (idx % 7) * 0.075))
00197:         obj["hot_phase"] = float(obj.get("hot_phase", idx * 0.61))
00198:         store_base_vector(obj, "_hot_base_rotation", obj.rotation_euler)
00199: 
00200:         dx = float(obj.location.x - center.x)
00201:         dy = float(obj.location.y - center.y)
00202:         radius_span = max(0.01, PHYSICS_ORBIT_RADIUS_MAX - PHYSICS_ORBIT_RADIUS_MIN)
00203:         fallback_radius = PHYSICS_ORBIT_RADIUS_MIN + radius_span * ((idx % 6) / 5.0)
00204:         orbit_radius = get_or_store_float(obj, "_hot_orbit_radius", max(0.20, math.sqrt(dx * dx + dy * dy) or fallback_radius))
00205:         orbit_angle = get_or_store_float(obj, "_hot_orbit_angle", math.atan2(dy, dx) if dx or dy else idx * 0.55)
00206:         orbit_z_offset = get_or_store_float(obj, "_hot_orbit_z_offset", float(obj.location.z - center.z))
00207:         orbit_speed = get_or_store_float(
00208:             obj,
00209:             "_hot_orbit_speed",
00210:             PHYSICS_ATOM_ORBIT_SPEED_MIN + (idx % 7) / 6.0 * (PHYSICS_ATOM_ORBIT_SPEED_MAX - PHYSICS_ATOM_ORBIT_SPEED_MIN),
00211:         )
00212:         orbit_tilt = get_or_store_float(obj, "_hot_orbit_tilt", -0.35 + (idx % 5) * 0.175)
00213:         micro_radius = get_or_store_float(obj, "_hot_micro_radius", PHYSICS_ATOM_MICRO_WOBBLE * (0.55 + (idx % 4) * 0.18))
00214: 
00215:         controls.append({
00216:             "object": obj,
00217:             "anchor": anchor,
00218:             "material": mat,
00219:             "emission_socket": emit_socket,
00220:             "mix_socket": mix_socket,
00221:             "band": obj["hot_band"],
00222:             "response": obj["hot_response"],
00223:             "phase": obj["hot_phase"],
00224:             "base_rotation": obj["_hot_base_rotation"],
00225:             "orbit_radius": orbit_radius,
00226:             "orbit_angle": orbit_angle,
00227:             "orbit_z_offset": orbit_z_offset,
00228:             "orbit_speed": orbit_speed,
00229:             "orbit_tilt": orbit_tilt,
00230:             "micro_radius": micro_radius,
00231:         })
00232: 
00233:     if not controls:
00234:         return 0
00235: 
00236:     if not frames:
00237:         frames = [{"low": 0.3, "mid": 0.2, "high": 0.2, "onset": 0.0, "beat": 0.0}]
00238: 
00239:     for frame, sample in enumerate(frames, start=1):
00240:         for item in controls:
00241:             obj = item["object"]
00242:             anchor = item["anchor"]
00243:             response = item["response"]
00244:             phase = item["phase"]
```
