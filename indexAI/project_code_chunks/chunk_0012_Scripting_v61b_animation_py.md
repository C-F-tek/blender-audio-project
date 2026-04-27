# Project Code Chunk 12/212

- File: `Scripting/v61b/animation.py`
- Part: `1`
- Lines: `1-280`

## Symbol Map
- Imports: `math`, `from config import HERO_SCALE_MIN, HERO_SCALE_MAX, HERO_BOUNCE_Z, HERO_ROT_Z, HERO_ROT_X, HERO_ROT_Y, HERO_DRIFT_X, HERO_DRIFT_Y, HERO_ORBIT_X, HERO_ORBIT_Y, HERO_BEAT_TWIST_Z, HERO_ONSET_SHAKE, HERO_DEFORM_STRENGTH_MIN, HERO_DEFORM_STRENGTH_MAX, HERO_DEFORM_DETAIL_STRENGTH_MAX, HERO_DEFORM_WAVE_HEIGHT_MAX, HERO_DEFORM_TWIST_MAX, HERO_DEFORM_CONTROLLER_RADIUS, HERO_DEFORM_KEYFRAME_STEP, HERO_MATERIAL_EMISSION_MIN, HERO_MATERIAL_EMISSION_MAX, HERO_MATERIAL_SELF_LIGHT_MIN, HERO_MATERIAL_SELF_LIGHT_MAX, HERO_MATERIAL_BUMP_MIN, HERO_MATERIAL_BUMP_MAX, HERO_MATERIAL_ROUGHNESS_MIN, HERO_MATERIAL_ROUGHNESS_MAX, HERO_MATERIAL_NOISE_SCALE_MIN, HERO_MATERIAL_NOISE_SCALE_MAX, HERO_MATERIAL_MAPPING_DRIFT, AURA_DEFORM_KEYFRAME_STEP, AURA_DEFORM_FIELD_DRIFT, AURA_DEFORM_FIELD_SCALE, SECONDARY_SCALE_MIN, SECONDARY_SCALE_MAX, SECONDARY_BOUNCE_Z, SECONDARY_DRIFT_X, SECONDARY_DRIFT_Y, SECONDARY_ROT_Z, SECONDARY_ROT_X, CAMERA_BEAT_BUMP_Z, CAMERA_BEAT_BUMP_Y, CAMERA_ORBIT_AMOUNT, CAMERA_PUSH_AMOUNT, CAMERA_VERTICAL_SWAY, LIGHT_ENERGY_MIN, LIGHT_ENERGY_MAX, PHYSICS_ACCENT_EMISSION_MIN, PHYSICS_ACCENT_EMISSION_MAX, PHYSICS_ACCENT_MIX_MIN, PHYSICS_ACCENT_MIX_MAX, PHYSICS_ATOM_ORBIT_SPEED_MIN, PHYSICS_ATOM_ORBIT_AUDIO_SPEED, PHYSICS_ATOM_ORBIT_RADIUS_PULSE, PHYSICS_ATOM_ORBIT_HEIGHT_SWAY, PHYSICS_ATOM_MICRO_WOBBLE, COMPOSITOR_GLARE_THRESHOLD_MIN, COMPOSITOR_GLARE_THRESHOLD_MAX, COMPOSITOR_LENS_DISTORT_MIN, COMPOSITOR_LENS_DISTORT_MAX, COMPOSITOR_LENS_DISPERSION_MIN, COMPOSITOR_LENS_DISPERSION_MAX, FIELD_STRENGTH_MIN, FIELD_STRENGTH_MAX, HERO_GRAVITY_STRENGTH_MIN, HERO_GRAVITY_STRENGTH_MAX, TURB_STRENGTH_MIN, TURB_STRENGTH_MAX, VORTEX_STRENGTH_MIN, VORTEX_STRENGTH_MAX, RHYTHM_PARTICLE_SIZE_MIN, RHYTHM_PARTICLE_SIZE_MAX, RHYTHM_PARTICLE_NORMAL_MIN, RHYTHM_PARTICLE_NORMAL_MAX, RHYTHM_PARTICLE_TANGENT_MIN, RHYTHM_PARTICLE_TANGENT_MAX, RHYTHM_PARTICLE_BROWNIAN_MIN, RHYTHM_PARTICLE_BROWNIAN_MAX, RHYTHM_PARTICLE_EMIT_MIN, RHYTHM_PARTICLE_EMIT_MAX, RHYTHM_PARTICLE_KEYFRAME_STEP, ALBUM_LETTER_PARTICLE_SIZE_MIN, ALBUM_LETTER_PARTICLE_SIZE_MAX, ALBUM_LETTER_ROOT_SCALE_MIN, ALBUM_LETTER_ROOT_SCALE_MAX, BACKDROP_EMISSION_MIN, BACKDROP_EMISSION_MAX, BACKDROP_BREATHE_SCALE, MIST_FLOAT_AMPLITUDE, MIST_BEAT_BOOST`, `from fog_dynamics import animate_fog_frame`, `from scene_utils import set_linear_interpolation_idblock`
- Functions: `keyframe_if_possible(idblock, data_path, frame)` line 99; `get_scene_compositor_tree(scene)` line 106; `rhythm_band_drive(band, response, low, mid, high, onset, beat, pulse, local_pulse)` line 114; `animate_scene(scene, frames, camera, target, hero_asset, secondary_asset, aura_data, fog_controller, scene_base, lights, physics_data, mist_particles, variants, energy_rings, energy_ribbons)` line 132

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
00055:     PHYSICS_ATOM_ORBIT_SPEED_MIN,
00056:     PHYSICS_ATOM_ORBIT_AUDIO_SPEED,
00057:     PHYSICS_ATOM_ORBIT_RADIUS_PULSE,
00058:     PHYSICS_ATOM_ORBIT_HEIGHT_SWAY,
00059:     PHYSICS_ATOM_MICRO_WOBBLE,
00060:     COMPOSITOR_GLARE_THRESHOLD_MIN,
00061:     COMPOSITOR_GLARE_THRESHOLD_MAX,
00062:     COMPOSITOR_LENS_DISTORT_MIN,
00063:     COMPOSITOR_LENS_DISTORT_MAX,
00064:     COMPOSITOR_LENS_DISPERSION_MIN,
00065:     COMPOSITOR_LENS_DISPERSION_MAX,
00066:     FIELD_STRENGTH_MIN,
00067:     FIELD_STRENGTH_MAX,
00068:     HERO_GRAVITY_STRENGTH_MIN,
00069:     HERO_GRAVITY_STRENGTH_MAX,
00070:     TURB_STRENGTH_MIN,
00071:     TURB_STRENGTH_MAX,
00072:     VORTEX_STRENGTH_MIN,
00073:     VORTEX_STRENGTH_MAX,
00074:     RHYTHM_PARTICLE_SIZE_MIN,
00075:     RHYTHM_PARTICLE_SIZE_MAX,
00076:     RHYTHM_PARTICLE_NORMAL_MIN,
00077:     RHYTHM_PARTICLE_NORMAL_MAX,
00078:     RHYTHM_PARTICLE_TANGENT_MIN,
00079:     RHYTHM_PARTICLE_TANGENT_MAX,
00080:     RHYTHM_PARTICLE_BROWNIAN_MIN,
00081:     RHYTHM_PARTICLE_BROWNIAN_MAX,
00082:     RHYTHM_PARTICLE_EMIT_MIN,
00083:     RHYTHM_PARTICLE_EMIT_MAX,
00084:     RHYTHM_PARTICLE_KEYFRAME_STEP,
00085:     ALBUM_LETTER_PARTICLE_SIZE_MIN,
00086:     ALBUM_LETTER_PARTICLE_SIZE_MAX,
00087:     ALBUM_LETTER_ROOT_SCALE_MIN,
00088:     ALBUM_LETTER_ROOT_SCALE_MAX,
00089:     BACKDROP_EMISSION_MIN,
00090:     BACKDROP_EMISSION_MAX,
00091:     BACKDROP_BREATHE_SCALE,
00092:     MIST_FLOAT_AMPLITUDE,
00093:     MIST_BEAT_BOOST,
00094: )
00095: from fog_dynamics import animate_fog_frame
00096: from scene_utils import set_linear_interpolation_idblock
00097: 
00098: 
00099: def keyframe_if_possible(idblock, data_path, frame):
00100:     try:
00101:         idblock.keyframe_insert(data_path=data_path, frame=frame)
00102:     except Exception:
00103:         pass
00104: 
00105: 
00106: def get_scene_compositor_tree(scene):
00107:     for attr in ("node_tree", "compositor_node_tree"):
00108:         tree = getattr(scene, attr, None)
00109:         if tree is not None:
00110:             return tree
00111:     return None
00112: 
00113: 
00114: def rhythm_band_drive(band, response, low, mid, high, onset, beat, pulse, local_pulse):
00115:     band = str(band)
00116:     response = float(response)
00117: 
00118:     if band == "low":
00119:         drive = low * 0.74 + beat * 0.18 + local_pulse * 0.16
00120:     elif band == "mid":
00121:         drive = mid * 0.68 + low * 0.14 + local_pulse * 0.18
00122:     elif band == "beat":
00123:         drive = beat * 0.70 + low * 0.22 + local_pulse * 0.14
00124:     elif band == "onset":
00125:         drive = onset * 0.72 + high * 0.18 + local_pulse * 0.12
00126:     else:
00127:         drive = high * 0.68 + onset * 0.24 + pulse * 0.08 + local_pulse * 0.12
00128: 
00129:     return min(1.0, max(0.0, drive * response))
00130: 
00131: 
00132: def animate_scene(
00133:     scene,
00134:     frames,
00135:     camera,
00136:     target,
00137:     hero_asset,
00138:     secondary_asset,
00139:     aura_data,
00140:     fog_controller,
00141:     scene_base,
00142:     lights,
00143:     physics_data,
00144:     mist_particles,
00145:     variants,
00146:     energy_rings,
00147:     energy_ribbons,
00148: ):
00149:     total_frames = len(frames)
00150: 
00151:     hero_root = hero_asset["root"]
00152:     hero_base_scale = hero_asset["base_scale"].copy()
00153:     hero_base_loc = hero_asset["base_location"].copy()
00154:     hero_base_rot = hero_asset["base_rotation"].copy()
00155:     hero_deform_controller = hero_asset.get("deform_controller")
00156:     hero_deformers = hero_asset.get("deformers", [])
00157:     hero_material_controls = hero_asset.get("material_controls", [])
00158:     hero_deform_base_loc = hero_deform_controller.location.copy() if hero_deform_controller else None
00159:     hero_deform_base_rot = hero_deform_controller.rotation_euler.copy() if hero_deform_controller else None
00160:     hero_deform_base_scale = hero_deform_controller.scale.copy() if hero_deform_controller else None
00161: 
00162:     secondary_root = None
00163:     secondary_base_scale = None
00164:     secondary_base_loc = None
00165:     secondary_base_rot = None
00166: 
00167:     if secondary_asset is not None:
00168:         secondary_root = secondary_asset["root"]
00169:         secondary_base_scale = secondary_asset["base_scale"].copy()
00170:         secondary_base_loc = secondary_asset["base_location"].copy()
00171:         secondary_base_rot = secondary_asset["base_rotation"].copy()
00172: 
00173:     aura_obj = aura_data["object"]
00174:     aura_base_loc = aura_obj.location.copy()
00175:     aura_audio_controller = aura_data.get("audio_controller")
00176:     aura_deform_field = aura_data.get("deform_field")
00177:     aura_audio_props = aura_data.get("audio_props", [])
00178:     aura_audio_base_loc = aura_audio_controller.location.copy() if aura_audio_controller else None
00179:     aura_audio_base_rot = aura_audio_controller.rotation_euler.copy() if aura_audio_controller else None
00180:     aura_audio_base_scale = aura_audio_controller.scale.copy() if aura_audio_controller else None
00181:     aura_field_base_loc = aura_deform_field.location.copy() if aura_deform_field else None
00182:     aura_field_base_rot = aura_deform_field.rotation_euler.copy() if aura_deform_field else None
00183:     aura_field_base_scale = aura_deform_field.scale.copy() if aura_deform_field else None
00184: 
00185:     fog_obj = fog_controller["object"] if fog_controller else None
00186:     fog_control = fog_controller.get("controller") if fog_controller else None
00187:     fog_base_loc = fog_controller.get("base_location") if fog_controller else None
00188:     fog_base_scale = fog_controller.get("base_scale") if fog_controller else None
00189: 
00190:     backdrop = scene_base.get("backdrop") if scene_base else None
00191:     backdrop_control = scene_base.get("backdrop_controller") if scene_base else None
00192:     backdrop_controls = scene_base.get("backdrop_controls", {}) if scene_base else {}
00193:     backdrop_base_loc = scene_base.get("backdrop_base_location") if scene_base else None
00194:     backdrop_base_scale = scene_base.get("backdrop_base_scale") if scene_base else None
00195: 
00196:     cam_base_loc = camera.location.copy()
00197:     target_base_loc = target.location.copy()
00198: 
00199:     compositor_glare = None
00200:     compositor_lens = None
00201:     compositor_tree = get_scene_compositor_tree(scene)
00202:     if compositor_tree is not None:
00203:         compositor_glare = compositor_tree.nodes.get("AudioSoftGlare")
00204:         compositor_lens = compositor_tree.nodes.get("AudioLensBreath")
00205: 
00206:     force_obj = physics_data["force_obj"]
00207:     turb_obj = physics_data["turb_obj"]
00208:     vortex_obj = physics_data["vortex_obj"]
00209:     wind_left = physics_data["wind_left"]
00210:     wind_right = physics_data["wind_right"]
00211:     accents = physics_data["accents"]
00212:     rhythm_particles = physics_data.get("rhythm_particles", [])
00213: 
00214:     for i, sample in enumerate(frames, start=1):
00215:         if i % 100 == 0:
00216:             print(f"[ANIMATE] frame {i}/{total_frames}")
00217: 
00218:         low = float(sample["low"])
00219:         mid = float(sample["mid"])
00220:         high = float(sample["high"])
00221:         onset = float(sample["onset"])
00222:         beat = float(sample["beat"])
00223: 
00224:         pulse = max(onset, beat)
00225:         bass_drive = min(1.0, low * 0.78 + beat * 0.35)
00226:         transient = min(1.0, onset * 0.68 + beat * 0.55)
00227: 
00228:         # HERO
00229:         s = HERO_SCALE_MIN + bass_drive * (HERO_SCALE_MAX - HERO_SCALE_MIN) + transient * 0.035
00230:         hero_root.scale = (
00231:             hero_base_scale.x * s,
00232:             hero_base_scale.y * s,
00233:             hero_base_scale.z * s,
00234:         )
00235: 
00236:         hero_root.location.x = (
00237:             hero_base_loc.x
00238:             + math.sin(i * 0.025) * HERO_DRIFT_X * (0.35 + mid * 0.65)
00239:             + math.sin(i * 0.071) * HERO_ORBIT_X * (0.25 + transient)
00240:         )
00241:         hero_root.location.y = (
00242:             hero_base_loc.y
00243:             + math.cos(i * 0.020) * HERO_DRIFT_Y * (0.25 + high * 0.75)
00244:             + math.cos(i * 0.063) * HERO_ORBIT_Y * (0.25 + pulse)
00245:         )
00246:         hero_root.location.z = (
00247:             hero_base_loc.z
00248:             + bass_drive * HERO_BOUNCE_Z
00249:             + transient * 0.16
00250:             + math.sin(i * 0.045) * 0.035
00251:         )
00252: 
00253:         onset_shake_x = math.sin(i * 0.43) * transient * HERO_ONSET_SHAKE
00254:         onset_shake_y = math.cos(i * 0.37) * transient * HERO_ONSET_SHAKE * 0.65
00255: 
00256:         hero_root.rotation_euler.x = (
00257:             hero_base_rot.x
00258:             + math.sin(i * 0.030) * HERO_ROT_X * (0.30 + mid * 0.70)
00259:             + onset_shake_x
00260:         )
00261:         hero_root.rotation_euler.y = (
00262:             hero_base_rot.y
00263:             + math.cos(i * 0.018) * HERO_ROT_Y * (0.20 + high * 0.80)
00264:             + onset_shake_y
00265:         )
00266:         hero_root.rotation_euler.z = (
00267:             hero_base_rot.z
00268:             + math.sin(i * 0.020) * HERO_ROT_Z * (0.35 + pulse * 0.65)
00269:             + beat * HERO_BEAT_TWIST_Z
00270:             + onset * math.sin(i * 0.19) * HERO_BEAT_TWIST_Z * 0.35
00271:         )
00272: 
00273:         hero_root.keyframe_insert(data_path="scale", frame=i)
00274:         hero_root.keyframe_insert(data_path="location", frame=i)
00275:         hero_root.keyframe_insert(data_path="rotation_euler", frame=i)
00276: 
00277:         # HERO MESH DEFORMATION
00278:         deform_keyframe = (
00279:             i == 1
00280:             or i == total_frames
```
