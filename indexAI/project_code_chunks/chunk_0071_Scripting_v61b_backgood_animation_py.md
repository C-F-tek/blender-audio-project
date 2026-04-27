# Project Code Chunk 71/212

- File: `Scripting/v61b_backgood/animation.py`
- Part: `1`
- Lines: `1-280`

## Symbol Map
- Imports: `math`, `from config import HERO_SCALE_MIN, HERO_SCALE_MAX, HERO_BOUNCE_Z, HERO_ROT_Z, HERO_ROT_X, HERO_ROT_Y, HERO_DRIFT_X, HERO_DRIFT_Y, HERO_ORBIT_X, HERO_ORBIT_Y, HERO_BEAT_TWIST_Z, HERO_ONSET_SHAKE, HERO_DEFORM_STRENGTH_MIN, HERO_DEFORM_STRENGTH_MAX, HERO_DEFORM_DETAIL_STRENGTH_MAX, HERO_DEFORM_WAVE_HEIGHT_MAX, HERO_DEFORM_TWIST_MAX, HERO_DEFORM_CONTROLLER_RADIUS, HERO_DEFORM_KEYFRAME_STEP, HERO_MATERIAL_EMISSION_MIN, HERO_MATERIAL_EMISSION_MAX, HERO_MATERIAL_SELF_LIGHT_MIN, HERO_MATERIAL_SELF_LIGHT_MAX, HERO_MATERIAL_BUMP_MIN, HERO_MATERIAL_BUMP_MAX, HERO_MATERIAL_ROUGHNESS_MIN, HERO_MATERIAL_ROUGHNESS_MAX, HERO_MATERIAL_NOISE_SCALE_MIN, HERO_MATERIAL_NOISE_SCALE_MAX, HERO_MATERIAL_MAPPING_DRIFT, AURA_DEFORM_KEYFRAME_STEP, AURA_DEFORM_FIELD_DRIFT, AURA_DEFORM_FIELD_SCALE, SECONDARY_SCALE_MIN, SECONDARY_SCALE_MAX, SECONDARY_BOUNCE_Z, SECONDARY_DRIFT_X, SECONDARY_DRIFT_Y, SECONDARY_ROT_Z, SECONDARY_ROT_X, CAMERA_BEAT_BUMP_Z, CAMERA_BEAT_BUMP_Y, CAMERA_ORBIT_AMOUNT, CAMERA_PUSH_AMOUNT, CAMERA_VERTICAL_SWAY, LIGHT_ENERGY_MIN, LIGHT_ENERGY_MAX, PHYSICS_ACCENT_EMISSION_MIN, PHYSICS_ACCENT_EMISSION_MAX, PHYSICS_ACCENT_MIX_MIN, PHYSICS_ACCENT_MIX_MAX, COMPOSITOR_GLARE_THRESHOLD_MIN, COMPOSITOR_GLARE_THRESHOLD_MAX, COMPOSITOR_LENS_DISTORT_MIN, COMPOSITOR_LENS_DISTORT_MAX, COMPOSITOR_LENS_DISPERSION_MIN, COMPOSITOR_LENS_DISPERSION_MAX, FIELD_STRENGTH_MIN, FIELD_STRENGTH_MAX, TURB_STRENGTH_MIN, TURB_STRENGTH_MAX, VORTEX_STRENGTH_MIN, VORTEX_STRENGTH_MAX, RHYTHM_PARTICLE_SIZE_MIN, RHYTHM_PARTICLE_SIZE_MAX, RHYTHM_PARTICLE_NORMAL_MIN, RHYTHM_PARTICLE_NORMAL_MAX, RHYTHM_PARTICLE_TANGENT_MIN, RHYTHM_PARTICLE_TANGENT_MAX, RHYTHM_PARTICLE_BROWNIAN_MIN, RHYTHM_PARTICLE_BROWNIAN_MAX, RHYTHM_PARTICLE_EMIT_MIN, RHYTHM_PARTICLE_EMIT_MAX, RHYTHM_PARTICLE_KEYFRAME_STEP, ALBUM_LETTER_PARTICLE_SIZE_MIN, ALBUM_LETTER_PARTICLE_SIZE_MAX, ALBUM_LETTER_ROOT_SCALE_MIN, ALBUM_LETTER_ROOT_SCALE_MAX, BACKDROP_EMISSION_MIN, BACKDROP_EMISSION_MAX, BACKDROP_BREATHE_SCALE, MIST_FLOAT_AMPLITUDE, MIST_BEAT_BOOST`, `from fog_dynamics import animate_fog_frame`, `from scene_utils import set_linear_interpolation_idblock`
- Functions: `keyframe_if_possible(idblock, data_path, frame)` line 92; `get_scene_compositor_tree(scene)` line 99; `rhythm_band_drive(band, response, low, mid, high, onset, beat, pulse, local_pulse)` line 107; `animate_scene(scene, frames, camera, target, hero_asset, secondary_asset, aura_data, fog_controller, scene_base, lights, physics_data, mist_particles, variants, energy_rings, energy_ribbons)` line 125

## Content
```py
00001: import math
00002: 
00003: from config import (
00004:     HERO_SCALE_MIN,
00005:     HERO_SCALE_MAX,
00006:     HERO_BOUNCE_Z,
00007:     HERO_ROT_Z,
00008:     HERO_ROT_X,
00009:     HERO_ROT_Y,
00010:     HERO_DRIFT_X,
00011:     HERO_DRIFT_Y,
00012:     HERO_ORBIT_X,
00013:     HERO_ORBIT_Y,
00014:     HERO_BEAT_TWIST_Z,
00015:     HERO_ONSET_SHAKE,
00016:     HERO_DEFORM_STRENGTH_MIN,
00017:     HERO_DEFORM_STRENGTH_MAX,
00018:     HERO_DEFORM_DETAIL_STRENGTH_MAX,
00019:     HERO_DEFORM_WAVE_HEIGHT_MAX,
00020:     HERO_DEFORM_TWIST_MAX,
00021:     HERO_DEFORM_CONTROLLER_RADIUS,
00022:     HERO_DEFORM_KEYFRAME_STEP,
00023:     HERO_MATERIAL_EMISSION_MIN,
00024:     HERO_MATERIAL_EMISSION_MAX,
00025:     HERO_MATERIAL_SELF_LIGHT_MIN,
00026:     HERO_MATERIAL_SELF_LIGHT_MAX,
00027:     HERO_MATERIAL_BUMP_MIN,
00028:     HERO_MATERIAL_BUMP_MAX,
00029:     HERO_MATERIAL_ROUGHNESS_MIN,
00030:     HERO_MATERIAL_ROUGHNESS_MAX,
00031:     HERO_MATERIAL_NOISE_SCALE_MIN,
00032:     HERO_MATERIAL_NOISE_SCALE_MAX,
00033:     HERO_MATERIAL_MAPPING_DRIFT,
00034:     AURA_DEFORM_KEYFRAME_STEP,
00035:     AURA_DEFORM_FIELD_DRIFT,
00036:     AURA_DEFORM_FIELD_SCALE,
00037:     SECONDARY_SCALE_MIN,
00038:     SECONDARY_SCALE_MAX,
00039:     SECONDARY_BOUNCE_Z,
00040:     SECONDARY_DRIFT_X,
00041:     SECONDARY_DRIFT_Y,
00042:     SECONDARY_ROT_Z,
00043:     SECONDARY_ROT_X,
00044:     CAMERA_BEAT_BUMP_Z,
00045:     CAMERA_BEAT_BUMP_Y,
00046:     CAMERA_ORBIT_AMOUNT,
00047:     CAMERA_PUSH_AMOUNT,
00048:     CAMERA_VERTICAL_SWAY,
00049:     LIGHT_ENERGY_MIN,
00050:     LIGHT_ENERGY_MAX,
00051:     PHYSICS_ACCENT_EMISSION_MIN,
00052:     PHYSICS_ACCENT_EMISSION_MAX,
00053:     PHYSICS_ACCENT_MIX_MIN,
00054:     PHYSICS_ACCENT_MIX_MAX,
00055:     COMPOSITOR_GLARE_THRESHOLD_MIN,
00056:     COMPOSITOR_GLARE_THRESHOLD_MAX,
00057:     COMPOSITOR_LENS_DISTORT_MIN,
00058:     COMPOSITOR_LENS_DISTORT_MAX,
00059:     COMPOSITOR_LENS_DISPERSION_MIN,
00060:     COMPOSITOR_LENS_DISPERSION_MAX,
00061:     FIELD_STRENGTH_MIN,
00062:     FIELD_STRENGTH_MAX,
00063:     TURB_STRENGTH_MIN,
00064:     TURB_STRENGTH_MAX,
00065:     VORTEX_STRENGTH_MIN,
00066:     VORTEX_STRENGTH_MAX,
00067:     RHYTHM_PARTICLE_SIZE_MIN,
00068:     RHYTHM_PARTICLE_SIZE_MAX,
00069:     RHYTHM_PARTICLE_NORMAL_MIN,
00070:     RHYTHM_PARTICLE_NORMAL_MAX,
00071:     RHYTHM_PARTICLE_TANGENT_MIN,
00072:     RHYTHM_PARTICLE_TANGENT_MAX,
00073:     RHYTHM_PARTICLE_BROWNIAN_MIN,
00074:     RHYTHM_PARTICLE_BROWNIAN_MAX,
00075:     RHYTHM_PARTICLE_EMIT_MIN,
00076:     RHYTHM_PARTICLE_EMIT_MAX,
00077:     RHYTHM_PARTICLE_KEYFRAME_STEP,
00078:     ALBUM_LETTER_PARTICLE_SIZE_MIN,
00079:     ALBUM_LETTER_PARTICLE_SIZE_MAX,
00080:     ALBUM_LETTER_ROOT_SCALE_MIN,
00081:     ALBUM_LETTER_ROOT_SCALE_MAX,
00082:     BACKDROP_EMISSION_MIN,
00083:     BACKDROP_EMISSION_MAX,
00084:     BACKDROP_BREATHE_SCALE,
00085:     MIST_FLOAT_AMPLITUDE,
00086:     MIST_BEAT_BOOST,
00087: )
00088: from fog_dynamics import animate_fog_frame
00089: from scene_utils import set_linear_interpolation_idblock
00090: 
00091: 
00092: def keyframe_if_possible(idblock, data_path, frame):
00093:     try:
00094:         idblock.keyframe_insert(data_path=data_path, frame=frame)
00095:     except Exception:
00096:         pass
00097: 
00098: 
00099: def get_scene_compositor_tree(scene):
00100:     for attr in ("node_tree", "compositor_node_tree"):
00101:         tree = getattr(scene, attr, None)
00102:         if tree is not None:
00103:             return tree
00104:     return None
00105: 
00106: 
00107: def rhythm_band_drive(band, response, low, mid, high, onset, beat, pulse, local_pulse):
00108:     band = str(band)
00109:     response = float(response)
00110: 
00111:     if band == "low":
00112:         drive = low * 0.74 + beat * 0.18 + local_pulse * 0.16
00113:     elif band == "mid":
00114:         drive = mid * 0.68 + low * 0.14 + local_pulse * 0.18
00115:     elif band == "beat":
00116:         drive = beat * 0.70 + low * 0.22 + local_pulse * 0.14
00117:     elif band == "onset":
00118:         drive = onset * 0.72 + high * 0.18 + local_pulse * 0.12
00119:     else:
00120:         drive = high * 0.68 + onset * 0.24 + pulse * 0.08 + local_pulse * 0.12
00121: 
00122:     return min(1.0, max(0.0, drive * response))
00123: 
00124: 
00125: def animate_scene(
00126:     scene,
00127:     frames,
00128:     camera,
00129:     target,
00130:     hero_asset,
00131:     secondary_asset,
00132:     aura_data,
00133:     fog_controller,
00134:     scene_base,
00135:     lights,
00136:     physics_data,
00137:     mist_particles,
00138:     variants,
00139:     energy_rings,
00140:     energy_ribbons,
00141: ):
00142:     total_frames = len(frames)
00143: 
00144:     hero_root = hero_asset["root"]
00145:     hero_base_scale = hero_asset["base_scale"].copy()
00146:     hero_base_loc = hero_asset["base_location"].copy()
00147:     hero_base_rot = hero_asset["base_rotation"].copy()
00148:     hero_deform_controller = hero_asset.get("deform_controller")
00149:     hero_deformers = hero_asset.get("deformers", [])
00150:     hero_material_controls = hero_asset.get("material_controls", [])
00151:     hero_deform_base_loc = hero_deform_controller.location.copy() if hero_deform_controller else None
00152:     hero_deform_base_rot = hero_deform_controller.rotation_euler.copy() if hero_deform_controller else None
00153:     hero_deform_base_scale = hero_deform_controller.scale.copy() if hero_deform_controller else None
00154: 
00155:     secondary_root = None
00156:     secondary_base_scale = None
00157:     secondary_base_loc = None
00158:     secondary_base_rot = None
00159: 
00160:     if secondary_asset is not None:
00161:         secondary_root = secondary_asset["root"]
00162:         secondary_base_scale = secondary_asset["base_scale"].copy()
00163:         secondary_base_loc = secondary_asset["base_location"].copy()
00164:         secondary_base_rot = secondary_asset["base_rotation"].copy()
00165: 
00166:     aura_obj = aura_data["object"]
00167:     aura_base_loc = aura_obj.location.copy()
00168:     aura_audio_controller = aura_data.get("audio_controller")
00169:     aura_deform_field = aura_data.get("deform_field")
00170:     aura_audio_props = aura_data.get("audio_props", [])
00171:     aura_audio_base_loc = aura_audio_controller.location.copy() if aura_audio_controller else None
00172:     aura_audio_base_rot = aura_audio_controller.rotation_euler.copy() if aura_audio_controller else None
00173:     aura_audio_base_scale = aura_audio_controller.scale.copy() if aura_audio_controller else None
00174:     aura_field_base_loc = aura_deform_field.location.copy() if aura_deform_field else None
00175:     aura_field_base_rot = aura_deform_field.rotation_euler.copy() if aura_deform_field else None
00176:     aura_field_base_scale = aura_deform_field.scale.copy() if aura_deform_field else None
00177: 
00178:     fog_obj = fog_controller["object"] if fog_controller else None
00179:     fog_control = fog_controller.get("controller") if fog_controller else None
00180:     fog_base_loc = fog_controller.get("base_location") if fog_controller else None
00181:     fog_base_scale = fog_controller.get("base_scale") if fog_controller else None
00182: 
00183:     backdrop = scene_base.get("backdrop") if scene_base else None
00184:     backdrop_control = scene_base.get("backdrop_controller") if scene_base else None
00185:     backdrop_controls = scene_base.get("backdrop_controls", {}) if scene_base else {}
00186:     backdrop_base_loc = scene_base.get("backdrop_base_location") if scene_base else None
00187:     backdrop_base_scale = scene_base.get("backdrop_base_scale") if scene_base else None
00188: 
00189:     cam_base_loc = camera.location.copy()
00190:     target_base_loc = target.location.copy()
00191: 
00192:     compositor_glare = None
00193:     compositor_lens = None
00194:     compositor_tree = get_scene_compositor_tree(scene)
00195:     if compositor_tree is not None:
00196:         compositor_glare = compositor_tree.nodes.get("AudioSoftGlare")
00197:         compositor_lens = compositor_tree.nodes.get("AudioLensBreath")
00198: 
00199:     force_obj = physics_data["force_obj"]
00200:     turb_obj = physics_data["turb_obj"]
00201:     vortex_obj = physics_data["vortex_obj"]
00202:     wind_left = physics_data["wind_left"]
00203:     wind_right = physics_data["wind_right"]
00204:     accents = physics_data["accents"]
00205:     rhythm_particles = physics_data.get("rhythm_particles", [])
00206: 
00207:     for i, sample in enumerate(frames, start=1):
00208:         if i % 100 == 0:
00209:             print(f"[ANIMATE] frame {i}/{total_frames}")
00210: 
00211:         low = float(sample["low"])
00212:         mid = float(sample["mid"])
00213:         high = float(sample["high"])
00214:         onset = float(sample["onset"])
00215:         beat = float(sample["beat"])
00216: 
00217:         pulse = max(onset, beat)
00218:         bass_drive = min(1.0, low * 0.78 + beat * 0.35)
00219:         transient = min(1.0, onset * 0.68 + beat * 0.55)
00220: 
00221:         # HERO
00222:         s = HERO_SCALE_MIN + bass_drive * (HERO_SCALE_MAX - HERO_SCALE_MIN) + transient * 0.035
00223:         hero_root.scale = (
00224:             hero_base_scale.x * s,
00225:             hero_base_scale.y * s,
00226:             hero_base_scale.z * s,
00227:         )
00228: 
00229:         hero_root.location.x = (
00230:             hero_base_loc.x
00231:             + math.sin(i * 0.025) * HERO_DRIFT_X * (0.35 + mid * 0.65)
00232:             + math.sin(i * 0.071) * HERO_ORBIT_X * (0.25 + transient)
00233:         )
00234:         hero_root.location.y = (
00235:             hero_base_loc.y
00236:             + math.cos(i * 0.020) * HERO_DRIFT_Y * (0.25 + high * 0.75)
00237:             + math.cos(i * 0.063) * HERO_ORBIT_Y * (0.25 + pulse)
00238:         )
00239:         hero_root.location.z = (
00240:             hero_base_loc.z
00241:             + bass_drive * HERO_BOUNCE_Z
00242:             + transient * 0.16
00243:             + math.sin(i * 0.045) * 0.035
00244:         )
00245: 
00246:         onset_shake_x = math.sin(i * 0.43) * transient * HERO_ONSET_SHAKE
00247:         onset_shake_y = math.cos(i * 0.37) * transient * HERO_ONSET_SHAKE * 0.65
00248: 
00249:         hero_root.rotation_euler.x = (
00250:             hero_base_rot.x
00251:             + math.sin(i * 0.030) * HERO_ROT_X * (0.30 + mid * 0.70)
00252:             + onset_shake_x
00253:         )
00254:         hero_root.rotation_euler.y = (
00255:             hero_base_rot.y
00256:             + math.cos(i * 0.018) * HERO_ROT_Y * (0.20 + high * 0.80)
00257:             + onset_shake_y
00258:         )
00259:         hero_root.rotation_euler.z = (
00260:             hero_base_rot.z
00261:             + math.sin(i * 0.020) * HERO_ROT_Z * (0.35 + pulse * 0.65)
00262:             + beat * HERO_BEAT_TWIST_Z
00263:             + onset * math.sin(i * 0.19) * HERO_BEAT_TWIST_Z * 0.35
00264:         )
00265: 
00266:         hero_root.keyframe_insert(data_path="scale", frame=i)
00267:         hero_root.keyframe_insert(data_path="location", frame=i)
00268:         hero_root.keyframe_insert(data_path="rotation_euler", frame=i)
00269: 
00270:         # HERO MESH DEFORMATION
00271:         deform_keyframe = (
00272:             i == 1
00273:             or i == total_frames
00274:             or i % HERO_DEFORM_KEYFRAME_STEP == 0
00275:             or beat > 0.0
00276:             or onset > 0.72
00277:         )
00278: 
00279:         if hero_deformers and deform_keyframe:
00280:             deform_drive = min(1.0, low * 0.58 + mid * 0.20 + transient * 0.52)
```
