# Project Code Chunk 30/212

- File: `Scripting/v61b/fog_dynamics.py`
- Part: `2`
- Lines: `272-392`

## Symbol Map
- Imports: `math`, `from config import FOG_DENSITY_MIN, FOG_DENSITY_MAX, FOG_EMISSION_MIN, FOG_EMISSION_MAX, FOG_NOISE_SCALE_MIN, FOG_NOISE_SCALE_MAX, FOG_CLUMP_SCALE_MIN, FOG_CLUMP_SCALE_MAX, FOG_CLUMP_RAMP_LOW_BASE, FOG_CLUMP_RAMP_HIGH_BASE, FOG_CLUMP_WEIGHT_MIN, FOG_CLUMP_WEIGHT_MAX, FOG_RAMP_LOW_BASE, FOG_RAMP_HIGH_BASE, FOG_COMPACT_XY, FOG_EXPAND_Z, FOG_CONTROLLER_DRIFT, FOG_DRIFT_SPEED_X, FOG_DRIFT_SPEED_Y, FOG_DRIFT_SPEED_Z, FOG_WAVE_SCALE_MIN, FOG_WAVE_SCALE_MAX, FOG_WAVE_DISTORTION_MIN, FOG_WAVE_DISTORTION_MAX, FOG_WAVE_WEIGHT_MIN, FOG_WAVE_WEIGHT_MAX, FOG_WIND_SHEAR_X, FOG_WIND_SHEAR_Y, FOG_VOLUME_ENABLED, FOG_VOLUME_VIEWPORT_VISIBLE, FOG_FILAMENT_KEYFRAME_STEP, FOG_FILAMENT_ALPHA_MIN, FOG_FILAMENT_ALPHA_MAX, FOG_FILAMENT_EMISSION_MIN, FOG_FILAMENT_EMISSION_MAX, FOG_FILAMENT_WIND_DRIFT, FOG_FILAMENT_COMPACT_SCALE, FOG_FILAMENT_NOISE_SCALE_MIN, FOG_FILAMENT_NOISE_SCALE_MAX, FOG_FILAMENT_WAVE_SCALE_MIN, FOG_FILAMENT_WAVE_SCALE_MAX`
- Functions: `clamp(value, low, high)` line 48; `keyframe_if_possible(idblock, data_path, frame)` line 52; `set_socket_value(socket, value, frame)` line 59; `animate_vector_socket(socket, values, frame)` line 69; `should_keyframe_filaments(frame, beat, onset)` line 82; `animate_fog_filaments(frame, low, mid, high, onset, beat, pulse, filaments)` line 91; `animate_fog_frame(frame, low, mid, high, onset, beat, pulse, fog_controller, fog_obj, fog_control, fog_base_scale, fog_base_loc)` line 204

## Content
```py
00272:         FOG_WAVE_SCALE_MAX - FOG_WAVE_SCALE_MIN
00273:     )
00274:     set_socket_value(fog_controller.get("wave_scale_socket"), wave_scale, frame)
00275: 
00276:     wave_distortion = FOG_WAVE_DISTORTION_MIN + clamp(wind * 0.62 + onset * 0.26 + mid * 0.12, 0.0, 1.0) * (
00277:         FOG_WAVE_DISTORTION_MAX - FOG_WAVE_DISTORTION_MIN
00278:     )
00279:     set_socket_value(fog_controller.get("wave_distortion_socket"), wave_distortion, frame)
00280:     set_socket_value(
00281:         fog_controller.get("wave_weight_socket"),
00282:         FOG_WAVE_WEIGHT_MIN + clamp(fog_compact * 0.28 + wind * 0.30 + beat * 0.12, 0.0, 1.0) * (
00283:             FOG_WAVE_WEIGHT_MAX - FOG_WAVE_WEIGHT_MIN
00284:         ),
00285:         frame,
00286:     )
00287:     set_socket_value(fog_controller.get("wave_phase_socket"), frame * 0.018 + smoke_push * 0.45, frame)
00288: 
00289:     animate_vector_socket(
00290:         fog_controller.get("mapping_location_socket"),
00291:         (
00292:             frame * FOG_DRIFT_SPEED_X + math.sin(frame * 0.010) * FOG_WIND_SHEAR_X * wind,
00293:             frame * FOG_DRIFT_SPEED_Y + math.cos(frame * 0.008) * FOG_WIND_SHEAR_Y * (0.35 + wind),
00294:             frame * FOG_DRIFT_SPEED_Z + fog_compact * 0.26 + smoke_push * 0.12,
00295:         ),
00296:         frame,
00297:     )
00298: 
00299:     animate_vector_socket(
00300:         fog_controller.get("mapping_scale_socket"),
00301:         (
00302:             0.64 + fog_compact * 1.10 + high * 0.06,
00303:             0.70 + fog_compact * 0.88 + mid * 0.06,
00304:             1.82 - fog_compact * 0.46 + low * 0.25,
00305:         ),
00306:         frame,
00307:     )
00308: 
00309:     animate_vector_socket(
00310:         fog_controller.get("mapping_rotation_socket"),
00311:         (
00312:             math.sin(frame * 0.005) * 0.20 + wind * 0.11,
00313:             math.cos(frame * 0.004) * 0.16 + high * 0.07,
00314:             frame * 0.0032 + fog_compact * 0.16 + onset * 0.05,
00315:         ),
00316:         frame,
00317:     )
00318: 
00319:     set_socket_value(
00320:         fog_controller.get("volume_anisotropy_socket"),
00321:         clamp(0.08 + fog_compact * 0.22 + wind * 0.12, 0.02, 0.48),
00322:         frame,
00323:     )
00324: 
00325:     color_socket = fog_controller.get("volume_color_socket")
00326:     if color_socket is not None:
00327:         try:
00328:             col = color_socket.default_value
00329:             col[0] = clamp(0.76 + low * 0.055 + beat * 0.020, 0.0, 1.0)
00330:             col[1] = clamp(0.84 + mid * 0.055, 0.0, 1.0)
00331:             col[2] = clamp(0.88 + high * 0.040, 0.0, 1.0)
00332:             if len(col) > 3:
00333:                 col[3] = 1.0
00334:             keyframe_if_possible(color_socket, "default_value", frame)
00335:         except Exception:
00336:             pass
00337: 
00338:     if "ramp_low_ctrl" in fog_controller and "ramp_high_ctrl" in fog_controller:
00339:         ramp_low = clamp(FOG_RAMP_LOW_BASE + fog_compact * 0.090 - wind * 0.026, 0.16, 0.58)
00340:         ramp_high = clamp(FOG_RAMP_HIGH_BASE - fog_compact * 0.145 + low * 0.030, ramp_low + 0.070, 0.82)
00341:         fog_controller["ramp_low_ctrl"].position = ramp_low
00342:         fog_controller["ramp_high_ctrl"].position = ramp_high
00343:         keyframe_if_possible(fog_controller["ramp_low_ctrl"], "position", frame)
00344:         keyframe_if_possible(fog_controller["ramp_high_ctrl"], "position", frame)
00345: 
00346:     if "clump_ramp_low_ctrl" in fog_controller and "clump_ramp_high_ctrl" in fog_controller:
00347:         clump_weight = clamp(
00348:             FOG_CLUMP_WEIGHT_MIN + fog_compact * (FOG_CLUMP_WEIGHT_MAX - FOG_CLUMP_WEIGHT_MIN),
00349:             FOG_CLUMP_WEIGHT_MIN,
00350:             FOG_CLUMP_WEIGHT_MAX,
00351:         )
00352:         clump_low = clamp(FOG_CLUMP_RAMP_LOW_BASE + fog_compact * 0.095 - wind * 0.035, 0.22, 0.68)
00353:         clump_high = clamp(
00354:             FOG_CLUMP_RAMP_HIGH_BASE - fog_compact * 0.135 + fog_disperse * 0.045 + high * 0.025,
00355:             clump_low + 0.040,
00356:             0.86,
00357:         )
00358:         fog_controller["clump_ramp_low_ctrl"].position = clump_low
00359:         fog_controller["clump_ramp_high_ctrl"].position = clump_high
00360:         keyframe_if_possible(fog_controller["clump_ramp_low_ctrl"], "position", frame)
00361:         keyframe_if_possible(fog_controller["clump_ramp_high_ctrl"], "position", frame)
00362: 
00363:         boosted_density = density * clump_weight
00364:         set_socket_value(fog_controller.get("density_socket"), boosted_density, frame)
00365: 
00366:     if fog_obj is not None and fog_base_scale is not None and fog_base_loc is not None:
00367:         compact_xy = 1.0 - fog_compact * FOG_COMPACT_XY
00368:         expand_z = 1.0 + (low * 0.50 + beat * 0.36 + wind * 0.14) * FOG_EXPAND_Z
00369:         fog_obj.scale = (
00370:             fog_base_scale.x * compact_xy,
00371:             fog_base_scale.y * (compact_xy + wind * 0.035),
00372:             fog_base_scale.z * expand_z,
00373:         )
00374:         fog_obj.location.x = fog_base_loc.x + math.sin(frame * 0.007) * FOG_CONTROLLER_DRIFT * (0.18 + wind * 0.32)
00375:         fog_obj.location.y = fog_base_loc.y + math.cos(frame * 0.006) * FOG_CONTROLLER_DRIFT * (0.12 + wind * 0.26)
00376:         fog_obj.location.z = fog_base_loc.z + (low - high) * 0.10 + beat * 0.06
00377:         fog_obj.keyframe_insert(data_path="scale", frame=frame)
00378:         fog_obj.keyframe_insert(data_path="location", frame=frame)
00379: 
00380:     if fog_control is not None and fog_base_loc is not None:
00381:         fog_control.location.x = fog_base_loc.x + math.sin(frame * 0.010) * FOG_CONTROLLER_DRIFT * (0.40 + wind)
00382:         fog_control.location.y = fog_base_loc.y + math.cos(frame * 0.009) * FOG_CONTROLLER_DRIFT * (0.26 + mid)
00383:         fog_control.location.z = fog_base_loc.z + fog_compact * 0.22 + smoke_push * 0.10
00384:         fog_control.rotation_euler.z = frame * 0.008 + fog_compact * 0.28 + wind * 0.12
00385:         fog_control.scale = (
00386:             1.0 + fog_compact * 0.26,
00387:             1.0 + wind * 0.18,
00388:             1.0 + low * 0.20,
00389:         )
00390:         fog_control.keyframe_insert(data_path="location", frame=frame)
00391:         fog_control.keyframe_insert(data_path="rotation_euler", frame=frame)
00392:         fog_control.keyframe_insert(data_path="scale", frame=frame)
```
