# Project Code Chunk 29/212

- File: `Scripting/v61b/fog_dynamics.py`
- Part: `1`
- Lines: `1-271`

## Symbol Map
- Imports: `math`, `from config import FOG_DENSITY_MIN, FOG_DENSITY_MAX, FOG_EMISSION_MIN, FOG_EMISSION_MAX, FOG_NOISE_SCALE_MIN, FOG_NOISE_SCALE_MAX, FOG_CLUMP_SCALE_MIN, FOG_CLUMP_SCALE_MAX, FOG_CLUMP_RAMP_LOW_BASE, FOG_CLUMP_RAMP_HIGH_BASE, FOG_CLUMP_WEIGHT_MIN, FOG_CLUMP_WEIGHT_MAX, FOG_RAMP_LOW_BASE, FOG_RAMP_HIGH_BASE, FOG_COMPACT_XY, FOG_EXPAND_Z, FOG_CONTROLLER_DRIFT, FOG_DRIFT_SPEED_X, FOG_DRIFT_SPEED_Y, FOG_DRIFT_SPEED_Z, FOG_WAVE_SCALE_MIN, FOG_WAVE_SCALE_MAX, FOG_WAVE_DISTORTION_MIN, FOG_WAVE_DISTORTION_MAX, FOG_WAVE_WEIGHT_MIN, FOG_WAVE_WEIGHT_MAX, FOG_WIND_SHEAR_X, FOG_WIND_SHEAR_Y, FOG_VOLUME_ENABLED, FOG_VOLUME_VIEWPORT_VISIBLE, FOG_FILAMENT_KEYFRAME_STEP, FOG_FILAMENT_ALPHA_MIN, FOG_FILAMENT_ALPHA_MAX, FOG_FILAMENT_EMISSION_MIN, FOG_FILAMENT_EMISSION_MAX, FOG_FILAMENT_WIND_DRIFT, FOG_FILAMENT_COMPACT_SCALE, FOG_FILAMENT_NOISE_SCALE_MIN, FOG_FILAMENT_NOISE_SCALE_MAX, FOG_FILAMENT_WAVE_SCALE_MIN, FOG_FILAMENT_WAVE_SCALE_MAX`
- Functions: `clamp(value, low, high)` line 48; `keyframe_if_possible(idblock, data_path, frame)` line 52; `set_socket_value(socket, value, frame)` line 59; `animate_vector_socket(socket, values, frame)` line 69; `should_keyframe_filaments(frame, beat, onset)` line 82; `animate_fog_filaments(frame, low, mid, high, onset, beat, pulse, filaments)` line 91; `animate_fog_frame(frame, low, mid, high, onset, beat, pulse, fog_controller, fog_obj, fog_control, fog_base_scale, fog_base_loc)` line 204

## Content
```py
00001: import math
00002: 
00003: from config import (
00004:     FOG_DENSITY_MIN,
00005:     FOG_DENSITY_MAX,
00006:     FOG_EMISSION_MIN,
00007:     FOG_EMISSION_MAX,
00008:     FOG_NOISE_SCALE_MIN,
00009:     FOG_NOISE_SCALE_MAX,
00010:     FOG_CLUMP_SCALE_MIN,
00011:     FOG_CLUMP_SCALE_MAX,
00012:     FOG_CLUMP_RAMP_LOW_BASE,
00013:     FOG_CLUMP_RAMP_HIGH_BASE,
00014:     FOG_CLUMP_WEIGHT_MIN,
00015:     FOG_CLUMP_WEIGHT_MAX,
00016:     FOG_RAMP_LOW_BASE,
00017:     FOG_RAMP_HIGH_BASE,
00018:     FOG_COMPACT_XY,
00019:     FOG_EXPAND_Z,
00020:     FOG_CONTROLLER_DRIFT,
00021:     FOG_DRIFT_SPEED_X,
00022:     FOG_DRIFT_SPEED_Y,
00023:     FOG_DRIFT_SPEED_Z,
00024:     FOG_WAVE_SCALE_MIN,
00025:     FOG_WAVE_SCALE_MAX,
00026:     FOG_WAVE_DISTORTION_MIN,
00027:     FOG_WAVE_DISTORTION_MAX,
00028:     FOG_WAVE_WEIGHT_MIN,
00029:     FOG_WAVE_WEIGHT_MAX,
00030:     FOG_WIND_SHEAR_X,
00031:     FOG_WIND_SHEAR_Y,
00032:     FOG_VOLUME_ENABLED,
00033:     FOG_VOLUME_VIEWPORT_VISIBLE,
00034:     FOG_FILAMENT_KEYFRAME_STEP,
00035:     FOG_FILAMENT_ALPHA_MIN,
00036:     FOG_FILAMENT_ALPHA_MAX,
00037:     FOG_FILAMENT_EMISSION_MIN,
00038:     FOG_FILAMENT_EMISSION_MAX,
00039:     FOG_FILAMENT_WIND_DRIFT,
00040:     FOG_FILAMENT_COMPACT_SCALE,
00041:     FOG_FILAMENT_NOISE_SCALE_MIN,
00042:     FOG_FILAMENT_NOISE_SCALE_MAX,
00043:     FOG_FILAMENT_WAVE_SCALE_MIN,
00044:     FOG_FILAMENT_WAVE_SCALE_MAX,
00045: )
00046: 
00047: 
00048: def clamp(value, low, high):
00049:     return max(low, min(high, value))
00050: 
00051: 
00052: def keyframe_if_possible(idblock, data_path, frame):
00053:     try:
00054:         idblock.keyframe_insert(data_path=data_path, frame=frame)
00055:     except Exception:
00056:         pass
00057: 
00058: 
00059: def set_socket_value(socket, value, frame):
00060:     if socket is None:
00061:         return
00062:     try:
00063:         socket.default_value = value
00064:         keyframe_if_possible(socket, "default_value", frame)
00065:     except Exception:
00066:         pass
00067: 
00068: 
00069: def animate_vector_socket(socket, values, frame):
00070:     if socket is None:
00071:         return
00072:     try:
00073:         vec = socket.default_value
00074:         for idx, value in enumerate(values):
00075:             if idx < len(vec):
00076:                 vec[idx] = value
00077:         keyframe_if_possible(socket, "default_value", frame)
00078:     except Exception:
00079:         pass
00080: 
00081: 
00082: def should_keyframe_filaments(frame, beat, onset):
00083:     return (
00084:         frame == 1
00085:         or frame % max(1, int(FOG_FILAMENT_KEYFRAME_STEP)) == 0
00086:         or beat > 0.0
00087:         or onset > 0.72
00088:     )
00089: 
00090: 
00091: def animate_fog_filaments(frame, low, mid, high, onset, beat, pulse, filaments):
00092:     if not filaments:
00093:         return
00094: 
00095:     objects = filaments.get("objects") or []
00096:     controls = filaments.get("controls") or {}
00097:     root = filaments.get("root")
00098:     if not objects and root is None:
00099:         return
00100: 
00101:     wind = clamp(mid * 0.32 + high * 0.28 + onset * 0.28 + beat * 0.12, 0.0, 1.0)
00102:     compact = clamp(low * 0.36 + mid * 0.20 + pulse * 0.28, 0.0, 1.0)
00103:     disperse = 1.0 - compact
00104:     keyframe = should_keyframe_filaments(frame, beat, onset)
00105:     if not keyframe:
00106:         return
00107: 
00108:     alpha_drive = clamp(0.16 + compact * 0.34 + pulse * 0.28 + mid * 0.16, 0.0, 1.0)
00109:     alpha = FOG_FILAMENT_ALPHA_MIN + alpha_drive * (FOG_FILAMENT_ALPHA_MAX - FOG_FILAMENT_ALPHA_MIN)
00110:     set_socket_value(controls.get("alpha_socket"), alpha, frame)
00111: 
00112:     emission_drive = clamp(0.12 + high * 0.28 + onset * 0.22 + beat * 0.18, 0.0, 1.0)
00113:     emission = FOG_FILAMENT_EMISSION_MIN + emission_drive * (
00114:         FOG_FILAMENT_EMISSION_MAX - FOG_FILAMENT_EMISSION_MIN
00115:     )
00116:     set_socket_value(controls.get("emission_socket"), emission, frame)
00117: 
00118:     noise_scale = FOG_FILAMENT_NOISE_SCALE_MIN + clamp(disperse * 0.32 + wind * 0.38, 0.0, 1.0) * (
00119:         FOG_FILAMENT_NOISE_SCALE_MAX - FOG_FILAMENT_NOISE_SCALE_MIN
00120:     )
00121:     set_socket_value(controls.get("noise_scale_socket"), noise_scale, frame)
00122:     set_socket_value(controls.get("noise_detail_socket"), 10.0 + high * 4.0 + onset * 1.8, frame)
00123:     set_socket_value(controls.get("noise_roughness_socket"), clamp(0.54 + compact * 0.12, 0.48, 0.82), frame)
00124: 
00125:     wave_scale = FOG_FILAMENT_WAVE_SCALE_MIN + clamp(wind * 0.56 + disperse * 0.22, 0.0, 1.0) * (
00126:         FOG_FILAMENT_WAVE_SCALE_MAX - FOG_FILAMENT_WAVE_SCALE_MIN
00127:     )
00128:     set_socket_value(controls.get("wave_scale_socket"), wave_scale, frame)
00129:     set_socket_value(controls.get("wave_distortion_socket"), 4.0 + wind * 10.0 + onset * 3.0, frame)
00130:     set_socket_value(controls.get("wave_weight_socket"), 0.12 + compact * 0.26 + wind * 0.18, frame)
00131:     set_socket_value(controls.get("wave_phase_socket"), frame * 0.018 + onset * 0.50, frame)
00132: 
00133:     animate_vector_socket(
00134:         controls.get("mapping_location_socket"),
00135:         (
00136:             frame * 0.006 + math.sin(frame * 0.008) * wind * 0.18,
00137:             frame * 0.003 + math.cos(frame * 0.006) * wind * 0.16,
00138:             frame * 0.002 + compact * 0.32,
00139:         ),
00140:         frame,
00141:     )
00142:     animate_vector_socket(
00143:         controls.get("mapping_scale_socket"),
00144:         (
00145:             1.0 + compact * 0.32,
00146:             0.74 + disperse * 0.22,
00147:             1.0 + low * 0.18,
00148:         ),
00149:         frame,
00150:     )
00151: 
00152:     if "ramp_low_ctrl" in controls and controls["ramp_low_ctrl"] is not None:
00153:         ramp_low = clamp(0.32 + compact * 0.08 - wind * 0.04, 0.20, 0.60)
00154:         ramp_high = clamp(0.76 - compact * 0.12 + disperse * 0.04, ramp_low + 0.12, 0.92)
00155:         controls["ramp_low_ctrl"].position = ramp_low
00156:         controls["ramp_high_ctrl"].position = ramp_high
00157:         keyframe_if_possible(controls["ramp_low_ctrl"], "position", frame)
00158:         keyframe_if_possible(controls["ramp_high_ctrl"], "position", frame)
00159: 
00160:     if root is not None:
00161:         root.location.x = math.sin(frame * 0.006) * FOG_FILAMENT_WIND_DRIFT * (0.20 + wind)
00162:         root.location.y = 4.8 + math.cos(frame * 0.004) * FOG_FILAMENT_WIND_DRIFT * 0.24
00163:         root.location.z = 3.1 + compact * 0.12 + beat * 0.08
00164:         root.scale = (
00165:             1.0 - compact * 0.10,
00166:             1.0 + wind * 0.10,
00167:             1.0 + low * 0.08,
00168:         )
00169:         root.keyframe_insert(data_path="location", frame=frame)
00170:         root.keyframe_insert(data_path="scale", frame=frame)
00171: 
00172:     for index, item in enumerate(objects):
00173:         obj = item["object"]
00174:         phase = item["phase"]
00175:         base_loc = item["base_location"]
00176:         base_scale = item["base_scale"]
00177:         base_rot = item["base_rotation"]
00178: 
00179:         side = math.sin(frame * 0.010 + phase)
00180:         lift = math.cos(frame * 0.008 + phase * 0.7)
00181:         swirl = math.sin(frame * 0.006 + phase * 1.3)
00182: 
00183:         obj.location.x = base_loc.x + side * FOG_FILAMENT_WIND_DRIFT * (0.22 + wind * 0.72)
00184:         obj.location.y = base_loc.y + swirl * FOG_FILAMENT_WIND_DRIFT * (0.12 + mid * 0.28)
00185:         obj.location.z = base_loc.z + lift * 0.12 + beat * 0.06 + compact * 0.08
00186: 
00187:         width_scale = 1.0 - compact * FOG_FILAMENT_COMPACT_SCALE + wind * 0.08
00188:         height_scale = 1.0 + compact * 0.22 + high * 0.08
00189:         obj.scale = (
00190:             base_scale.x * width_scale,
00191:             base_scale.y * height_scale,
00192:             base_scale.z,
00193:         )
00194: 
00195:         obj.rotation_euler.x = base_rot.x + math.sin(frame * 0.005 + phase) * 0.035
00196:         obj.rotation_euler.y = base_rot.y + math.cos(frame * 0.004 + phase) * 0.025
00197:         obj.rotation_euler.z = base_rot.z + side * 0.045 + wind * 0.025 + index * 0.001
00198: 
00199:         obj.keyframe_insert(data_path="location", frame=frame)
00200:         obj.keyframe_insert(data_path="scale", frame=frame)
00201:         obj.keyframe_insert(data_path="rotation_euler", frame=frame)
00202: 
00203: 
00204: def animate_fog_frame(
00205:     frame,
00206:     low,
00207:     mid,
00208:     high,
00209:     onset,
00210:     beat,
00211:     pulse,
00212:     fog_controller,
00213:     fog_obj,
00214:     fog_control,
00215:     fog_base_scale,
00216:     fog_base_loc,
00217: ):
00218:     if not fog_controller:
00219:         return
00220: 
00221:     smoke_push = clamp(onset * 0.34 + beat * 0.26 + high * 0.22 + mid * 0.18, 0.0, 1.0)
00222:     fog_compact = clamp(low * 0.36 + mid * 0.22 + pulse * 0.28, 0.0, 1.0)
00223:     fog_disperse = 1.0 - fog_compact
00224:     wind = clamp(mid * 0.30 + high * 0.28 + onset * 0.34 + beat * 0.12, 0.0, 1.0)
00225: 
00226:     animate_fog_filaments(
00227:         frame=frame,
00228:         low=low,
00229:         mid=mid,
00230:         high=high,
00231:         onset=onset,
00232:         beat=beat,
00233:         pulse=pulse,
00234:         filaments=fog_controller.get("filaments"),
00235:     )
00236: 
00237:     if not FOG_VOLUME_ENABLED:
00238:         if fog_obj is not None:
00239:             fog_obj.hide_render = True
00240:             fog_obj.hide_viewport = not FOG_VOLUME_VIEWPORT_VISIBLE
00241:         return
00242: 
00243:     density_drive = clamp(0.24 + low * 0.22 + fog_compact * 0.58 + mid * 0.15, 0.0, 1.0)
00244:     density = FOG_DENSITY_MIN + density_drive * (FOG_DENSITY_MAX - FOG_DENSITY_MIN)
00245:     set_socket_value(fog_controller.get("density_socket"), density, frame)
00246: 
00247:     emission_drive = clamp(0.10 + high * 0.18 + onset * 0.11 + beat * 0.07, 0.0, 1.0)
00248:     emission = FOG_EMISSION_MIN + emission_drive * (FOG_EMISSION_MAX - FOG_EMISSION_MIN)
00249:     set_socket_value(fog_controller.get("emission_socket"), emission, frame)
00250: 
00251:     noise_drive = clamp(fog_disperse * 0.28 + high * 0.18 + wind * 0.18 + mid * 0.10, 0.0, 1.0)
00252:     noise_scale = FOG_NOISE_SCALE_MIN + noise_drive * (FOG_NOISE_SCALE_MAX - FOG_NOISE_SCALE_MIN)
00253:     set_socket_value(fog_controller.get("noise_scale_socket"), noise_scale, frame)
00254:     set_socket_value(fog_controller.get("noise_detail_socket"), 8.0 + high * 4.0 + onset * 1.2, frame)
00255:     set_socket_value(
00256:         fog_controller.get("noise_roughness_socket"),
00257:         clamp(0.66 + mid * 0.10 + high * 0.08 - fog_compact * 0.04, 0.52, 0.90),
00258:         frame,
00259:     )
00260: 
00261:     clump_scale_drive = clamp(fog_disperse * 0.42 + wind * 0.22 + high * 0.18 - fog_compact * 0.12, 0.0, 1.0)
00262:     clump_scale = FOG_CLUMP_SCALE_MIN + clump_scale_drive * (FOG_CLUMP_SCALE_MAX - FOG_CLUMP_SCALE_MIN)
00263:     set_socket_value(fog_controller.get("clump_noise_scale_socket"), clump_scale, frame)
00264:     set_socket_value(fog_controller.get("clump_noise_detail_socket"), 9.0 + high * 3.5 + onset * 1.0, frame)
00265:     set_socket_value(
00266:         fog_controller.get("clump_noise_roughness_socket"),
00267:         clamp(0.70 + fog_compact * 0.08 + wind * 0.05, 0.58, 0.92),
00268:         frame,
00269:     )
00270: 
00271:     wave_scale = FOG_WAVE_SCALE_MIN + clamp(0.22 + wind * 0.48 + fog_disperse * 0.22, 0.0, 1.0) * (
```
