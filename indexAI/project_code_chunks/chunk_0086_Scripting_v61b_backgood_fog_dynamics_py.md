# Project Code Chunk 86/212

- File: `Scripting/v61b_backgood/fog_dynamics.py`
- Part: `1`
- Lines: `1-240`

## Symbol Map
- Imports: `math`, `from config import FOG_DENSITY_MIN, FOG_DENSITY_MAX, FOG_EMISSION_MIN, FOG_EMISSION_MAX, FOG_NOISE_SCALE_MIN, FOG_NOISE_SCALE_MAX, FOG_CLUMP_SCALE_MIN, FOG_CLUMP_SCALE_MAX, FOG_CLUMP_RAMP_LOW_BASE, FOG_CLUMP_RAMP_HIGH_BASE, FOG_CLUMP_WEIGHT_MIN, FOG_CLUMP_WEIGHT_MAX, FOG_RAMP_LOW_BASE, FOG_RAMP_HIGH_BASE, FOG_COMPACT_XY, FOG_EXPAND_Z, FOG_CONTROLLER_DRIFT, FOG_DRIFT_SPEED_X, FOG_DRIFT_SPEED_Y, FOG_DRIFT_SPEED_Z, FOG_WAVE_SCALE_MIN, FOG_WAVE_SCALE_MAX, FOG_WAVE_DISTORTION_MIN, FOG_WAVE_DISTORTION_MAX, FOG_WAVE_WEIGHT_MIN, FOG_WAVE_WEIGHT_MAX, FOG_WIND_SHEAR_X, FOG_WIND_SHEAR_Y`
- Functions: `clamp(value, low, high)` line 35; `keyframe_if_possible(idblock, data_path, frame)` line 39; `set_socket_value(socket, value, frame)` line 46; `animate_vector_socket(socket, values, frame)` line 56; `animate_fog_frame(frame, low, mid, high, onset, beat, pulse, fog_controller, fog_obj, fog_control, fog_base_scale, fog_base_loc)` line 69

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
00032: )
00033: 
00034: 
00035: def clamp(value, low, high):
00036:     return max(low, min(high, value))
00037: 
00038: 
00039: def keyframe_if_possible(idblock, data_path, frame):
00040:     try:
00041:         idblock.keyframe_insert(data_path=data_path, frame=frame)
00042:     except Exception:
00043:         pass
00044: 
00045: 
00046: def set_socket_value(socket, value, frame):
00047:     if socket is None:
00048:         return
00049:     try:
00050:         socket.default_value = value
00051:         keyframe_if_possible(socket, "default_value", frame)
00052:     except Exception:
00053:         pass
00054: 
00055: 
00056: def animate_vector_socket(socket, values, frame):
00057:     if socket is None:
00058:         return
00059:     try:
00060:         vec = socket.default_value
00061:         for idx, value in enumerate(values):
00062:             if idx < len(vec):
00063:                 vec[idx] = value
00064:         keyframe_if_possible(socket, "default_value", frame)
00065:     except Exception:
00066:         pass
00067: 
00068: 
00069: def animate_fog_frame(
00070:     frame,
00071:     low,
00072:     mid,
00073:     high,
00074:     onset,
00075:     beat,
00076:     pulse,
00077:     fog_controller,
00078:     fog_obj,
00079:     fog_control,
00080:     fog_base_scale,
00081:     fog_base_loc,
00082: ):
00083:     if not fog_controller:
00084:         return
00085: 
00086:     smoke_push = clamp(onset * 0.34 + beat * 0.26 + high * 0.22 + mid * 0.18, 0.0, 1.0)
00087:     fog_compact = clamp(low * 0.36 + mid * 0.22 + pulse * 0.28, 0.0, 1.0)
00088:     fog_disperse = 1.0 - fog_compact
00089:     wind = clamp(mid * 0.30 + high * 0.28 + onset * 0.34 + beat * 0.12, 0.0, 1.0)
00090: 
00091:     density_drive = clamp(0.24 + low * 0.22 + fog_compact * 0.58 + mid * 0.15, 0.0, 1.0)
00092:     density = FOG_DENSITY_MIN + density_drive * (FOG_DENSITY_MAX - FOG_DENSITY_MIN)
00093:     set_socket_value(fog_controller.get("density_socket"), density, frame)
00094: 
00095:     emission_drive = clamp(0.10 + high * 0.18 + onset * 0.11 + beat * 0.07, 0.0, 1.0)
00096:     emission = FOG_EMISSION_MIN + emission_drive * (FOG_EMISSION_MAX - FOG_EMISSION_MIN)
00097:     set_socket_value(fog_controller.get("emission_socket"), emission, frame)
00098: 
00099:     noise_drive = clamp(fog_disperse * 0.28 + high * 0.18 + wind * 0.18 + mid * 0.10, 0.0, 1.0)
00100:     noise_scale = FOG_NOISE_SCALE_MIN + noise_drive * (FOG_NOISE_SCALE_MAX - FOG_NOISE_SCALE_MIN)
00101:     set_socket_value(fog_controller.get("noise_scale_socket"), noise_scale, frame)
00102:     set_socket_value(fog_controller.get("noise_detail_socket"), 8.0 + high * 4.0 + onset * 1.2, frame)
00103:     set_socket_value(
00104:         fog_controller.get("noise_roughness_socket"),
00105:         clamp(0.66 + mid * 0.10 + high * 0.08 - fog_compact * 0.04, 0.52, 0.90),
00106:         frame,
00107:     )
00108: 
00109:     clump_scale_drive = clamp(fog_disperse * 0.42 + wind * 0.22 + high * 0.18 - fog_compact * 0.12, 0.0, 1.0)
00110:     clump_scale = FOG_CLUMP_SCALE_MIN + clump_scale_drive * (FOG_CLUMP_SCALE_MAX - FOG_CLUMP_SCALE_MIN)
00111:     set_socket_value(fog_controller.get("clump_noise_scale_socket"), clump_scale, frame)
00112:     set_socket_value(fog_controller.get("clump_noise_detail_socket"), 9.0 + high * 3.5 + onset * 1.0, frame)
00113:     set_socket_value(
00114:         fog_controller.get("clump_noise_roughness_socket"),
00115:         clamp(0.70 + fog_compact * 0.08 + wind * 0.05, 0.58, 0.92),
00116:         frame,
00117:     )
00118: 
00119:     wave_scale = FOG_WAVE_SCALE_MIN + clamp(0.22 + wind * 0.48 + fog_disperse * 0.22, 0.0, 1.0) * (
00120:         FOG_WAVE_SCALE_MAX - FOG_WAVE_SCALE_MIN
00121:     )
00122:     set_socket_value(fog_controller.get("wave_scale_socket"), wave_scale, frame)
00123: 
00124:     wave_distortion = FOG_WAVE_DISTORTION_MIN + clamp(wind * 0.62 + onset * 0.26 + mid * 0.12, 0.0, 1.0) * (
00125:         FOG_WAVE_DISTORTION_MAX - FOG_WAVE_DISTORTION_MIN
00126:     )
00127:     set_socket_value(fog_controller.get("wave_distortion_socket"), wave_distortion, frame)
00128:     set_socket_value(
00129:         fog_controller.get("wave_weight_socket"),
00130:         FOG_WAVE_WEIGHT_MIN + clamp(fog_compact * 0.28 + wind * 0.30 + beat * 0.12, 0.0, 1.0) * (
00131:             FOG_WAVE_WEIGHT_MAX - FOG_WAVE_WEIGHT_MIN
00132:         ),
00133:         frame,
00134:     )
00135:     set_socket_value(fog_controller.get("wave_phase_socket"), frame * 0.018 + smoke_push * 0.45, frame)
00136: 
00137:     animate_vector_socket(
00138:         fog_controller.get("mapping_location_socket"),
00139:         (
00140:             frame * FOG_DRIFT_SPEED_X + math.sin(frame * 0.010) * FOG_WIND_SHEAR_X * wind,
00141:             frame * FOG_DRIFT_SPEED_Y + math.cos(frame * 0.008) * FOG_WIND_SHEAR_Y * (0.35 + wind),
00142:             frame * FOG_DRIFT_SPEED_Z + fog_compact * 0.26 + smoke_push * 0.12,
00143:         ),
00144:         frame,
00145:     )
00146: 
00147:     animate_vector_socket(
00148:         fog_controller.get("mapping_scale_socket"),
00149:         (
00150:             0.64 + fog_compact * 1.10 + high * 0.06,
00151:             0.70 + fog_compact * 0.88 + mid * 0.06,
00152:             1.82 - fog_compact * 0.46 + low * 0.25,
00153:         ),
00154:         frame,
00155:     )
00156: 
00157:     animate_vector_socket(
00158:         fog_controller.get("mapping_rotation_socket"),
00159:         (
00160:             math.sin(frame * 0.005) * 0.20 + wind * 0.11,
00161:             math.cos(frame * 0.004) * 0.16 + high * 0.07,
00162:             frame * 0.0032 + fog_compact * 0.16 + onset * 0.05,
00163:         ),
00164:         frame,
00165:     )
00166: 
00167:     set_socket_value(
00168:         fog_controller.get("volume_anisotropy_socket"),
00169:         clamp(0.08 + fog_compact * 0.22 + wind * 0.12, 0.02, 0.48),
00170:         frame,
00171:     )
00172: 
00173:     color_socket = fog_controller.get("volume_color_socket")
00174:     if color_socket is not None:
00175:         try:
00176:             col = color_socket.default_value
00177:             col[0] = clamp(0.76 + low * 0.055 + beat * 0.020, 0.0, 1.0)
00178:             col[1] = clamp(0.84 + mid * 0.055, 0.0, 1.0)
00179:             col[2] = clamp(0.88 + high * 0.040, 0.0, 1.0)
00180:             if len(col) > 3:
00181:                 col[3] = 1.0
00182:             keyframe_if_possible(color_socket, "default_value", frame)
00183:         except Exception:
00184:             pass
00185: 
00186:     if "ramp_low_ctrl" in fog_controller and "ramp_high_ctrl" in fog_controller:
00187:         ramp_low = clamp(FOG_RAMP_LOW_BASE + fog_compact * 0.090 - wind * 0.026, 0.16, 0.58)
00188:         ramp_high = clamp(FOG_RAMP_HIGH_BASE - fog_compact * 0.145 + low * 0.030, ramp_low + 0.070, 0.82)
00189:         fog_controller["ramp_low_ctrl"].position = ramp_low
00190:         fog_controller["ramp_high_ctrl"].position = ramp_high
00191:         keyframe_if_possible(fog_controller["ramp_low_ctrl"], "position", frame)
00192:         keyframe_if_possible(fog_controller["ramp_high_ctrl"], "position", frame)
00193: 
00194:     if "clump_ramp_low_ctrl" in fog_controller and "clump_ramp_high_ctrl" in fog_controller:
00195:         clump_weight = clamp(
00196:             FOG_CLUMP_WEIGHT_MIN + fog_compact * (FOG_CLUMP_WEIGHT_MAX - FOG_CLUMP_WEIGHT_MIN),
00197:             FOG_CLUMP_WEIGHT_MIN,
00198:             FOG_CLUMP_WEIGHT_MAX,
00199:         )
00200:         clump_low = clamp(FOG_CLUMP_RAMP_LOW_BASE + fog_compact * 0.095 - wind * 0.035, 0.22, 0.68)
00201:         clump_high = clamp(
00202:             FOG_CLUMP_RAMP_HIGH_BASE - fog_compact * 0.135 + fog_disperse * 0.045 + high * 0.025,
00203:             clump_low + 0.040,
00204:             0.86,
00205:         )
00206:         fog_controller["clump_ramp_low_ctrl"].position = clump_low
00207:         fog_controller["clump_ramp_high_ctrl"].position = clump_high
00208:         keyframe_if_possible(fog_controller["clump_ramp_low_ctrl"], "position", frame)
00209:         keyframe_if_possible(fog_controller["clump_ramp_high_ctrl"], "position", frame)
00210: 
00211:         boosted_density = density * clump_weight
00212:         set_socket_value(fog_controller.get("density_socket"), boosted_density, frame)
00213: 
00214:     if fog_obj is not None and fog_base_scale is not None and fog_base_loc is not None:
00215:         compact_xy = 1.0 - fog_compact * FOG_COMPACT_XY
00216:         expand_z = 1.0 + (low * 0.50 + beat * 0.36 + wind * 0.14) * FOG_EXPAND_Z
00217:         fog_obj.scale = (
00218:             fog_base_scale.x * compact_xy,
00219:             fog_base_scale.y * (compact_xy + wind * 0.035),
00220:             fog_base_scale.z * expand_z,
00221:         )
00222:         fog_obj.location.x = fog_base_loc.x + math.sin(frame * 0.007) * FOG_CONTROLLER_DRIFT * (0.18 + wind * 0.32)
00223:         fog_obj.location.y = fog_base_loc.y + math.cos(frame * 0.006) * FOG_CONTROLLER_DRIFT * (0.12 + wind * 0.26)
00224:         fog_obj.location.z = fog_base_loc.z + (low - high) * 0.10 + beat * 0.06
00225:         fog_obj.keyframe_insert(data_path="scale", frame=frame)
00226:         fog_obj.keyframe_insert(data_path="location", frame=frame)
00227: 
00228:     if fog_control is not None and fog_base_loc is not None:
00229:         fog_control.location.x = fog_base_loc.x + math.sin(frame * 0.010) * FOG_CONTROLLER_DRIFT * (0.40 + wind)
00230:         fog_control.location.y = fog_base_loc.y + math.cos(frame * 0.009) * FOG_CONTROLLER_DRIFT * (0.26 + mid)
00231:         fog_control.location.z = fog_base_loc.z + fog_compact * 0.22 + smoke_push * 0.10
00232:         fog_control.rotation_euler.z = frame * 0.008 + fog_compact * 0.28 + wind * 0.12
00233:         fog_control.scale = (
00234:             1.0 + fog_compact * 0.26,
00235:             1.0 + wind * 0.18,
00236:             1.0 + low * 0.20,
00237:         )
00238:         fog_control.keyframe_insert(data_path="location", frame=frame)
00239:         fog_control.keyframe_insert(data_path="rotation_euler", frame=frame)
00240:         fog_control.keyframe_insert(data_path="scale", frame=frame)
```
