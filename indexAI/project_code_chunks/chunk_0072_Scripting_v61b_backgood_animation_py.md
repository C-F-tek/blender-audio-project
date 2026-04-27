# Project Code Chunk 72/212

- File: `Scripting/v61b_backgood/animation.py`
- Part: `2`
- Lines: `281-476`

## Symbol Map
- Imports: `math`, `from config import HERO_SCALE_MIN, HERO_SCALE_MAX, HERO_BOUNCE_Z, HERO_ROT_Z, HERO_ROT_X, HERO_ROT_Y, HERO_DRIFT_X, HERO_DRIFT_Y, HERO_ORBIT_X, HERO_ORBIT_Y, HERO_BEAT_TWIST_Z, HERO_ONSET_SHAKE, HERO_DEFORM_STRENGTH_MIN, HERO_DEFORM_STRENGTH_MAX, HERO_DEFORM_DETAIL_STRENGTH_MAX, HERO_DEFORM_WAVE_HEIGHT_MAX, HERO_DEFORM_TWIST_MAX, HERO_DEFORM_CONTROLLER_RADIUS, HERO_DEFORM_KEYFRAME_STEP, HERO_MATERIAL_EMISSION_MIN, HERO_MATERIAL_EMISSION_MAX, HERO_MATERIAL_SELF_LIGHT_MIN, HERO_MATERIAL_SELF_LIGHT_MAX, HERO_MATERIAL_BUMP_MIN, HERO_MATERIAL_BUMP_MAX, HERO_MATERIAL_ROUGHNESS_MIN, HERO_MATERIAL_ROUGHNESS_MAX, HERO_MATERIAL_NOISE_SCALE_MIN, HERO_MATERIAL_NOISE_SCALE_MAX, HERO_MATERIAL_MAPPING_DRIFT, AURA_DEFORM_KEYFRAME_STEP, AURA_DEFORM_FIELD_DRIFT, AURA_DEFORM_FIELD_SCALE, SECONDARY_SCALE_MIN, SECONDARY_SCALE_MAX, SECONDARY_BOUNCE_Z, SECONDARY_DRIFT_X, SECONDARY_DRIFT_Y, SECONDARY_ROT_Z, SECONDARY_ROT_X, CAMERA_BEAT_BUMP_Z, CAMERA_BEAT_BUMP_Y, CAMERA_ORBIT_AMOUNT, CAMERA_PUSH_AMOUNT, CAMERA_VERTICAL_SWAY, LIGHT_ENERGY_MIN, LIGHT_ENERGY_MAX, PHYSICS_ACCENT_EMISSION_MIN, PHYSICS_ACCENT_EMISSION_MAX, PHYSICS_ACCENT_MIX_MIN, PHYSICS_ACCENT_MIX_MAX, COMPOSITOR_GLARE_THRESHOLD_MIN, COMPOSITOR_GLARE_THRESHOLD_MAX, COMPOSITOR_LENS_DISTORT_MIN, COMPOSITOR_LENS_DISTORT_MAX, COMPOSITOR_LENS_DISPERSION_MIN, COMPOSITOR_LENS_DISPERSION_MAX, FIELD_STRENGTH_MIN, FIELD_STRENGTH_MAX, TURB_STRENGTH_MIN, TURB_STRENGTH_MAX, VORTEX_STRENGTH_MIN, VORTEX_STRENGTH_MAX, RHYTHM_PARTICLE_SIZE_MIN, RHYTHM_PARTICLE_SIZE_MAX, RHYTHM_PARTICLE_NORMAL_MIN, RHYTHM_PARTICLE_NORMAL_MAX, RHYTHM_PARTICLE_TANGENT_MIN, RHYTHM_PARTICLE_TANGENT_MAX, RHYTHM_PARTICLE_BROWNIAN_MIN, RHYTHM_PARTICLE_BROWNIAN_MAX, RHYTHM_PARTICLE_EMIT_MIN, RHYTHM_PARTICLE_EMIT_MAX, RHYTHM_PARTICLE_KEYFRAME_STEP, ALBUM_LETTER_PARTICLE_SIZE_MIN, ALBUM_LETTER_PARTICLE_SIZE_MAX, ALBUM_LETTER_ROOT_SCALE_MIN, ALBUM_LETTER_ROOT_SCALE_MAX, BACKDROP_EMISSION_MIN, BACKDROP_EMISSION_MAX, BACKDROP_BREATHE_SCALE, MIST_FLOAT_AMPLITUDE, MIST_BEAT_BOOST`, `from fog_dynamics import animate_fog_frame`, `from scene_utils import set_linear_interpolation_idblock`
- Functions: `keyframe_if_possible(idblock, data_path, frame)` line 92; `get_scene_compositor_tree(scene)` line 99; `rhythm_band_drive(band, response, low, mid, high, onset, beat, pulse, local_pulse)` line 107; `animate_scene(scene, frames, camera, target, hero_asset, secondary_asset, aura_data, fog_controller, scene_base, lights, physics_data, mist_particles, variants, energy_rings, energy_ribbons)` line 125

## Content
```py
00281:             if hero_deform_controller is not None:
00282:                 hero_deform_controller.location.x = (
00283:                     hero_deform_base_loc.x
00284:                     + math.sin(i * 0.036) * HERO_DEFORM_CONTROLLER_RADIUS * (0.45 + deform_drive)
00285:                 )
00286:                 hero_deform_controller.location.y = (
00287:                     hero_deform_base_loc.y
00288:                     + math.cos(i * 0.031) * HERO_DEFORM_CONTROLLER_RADIUS * (0.35 + pulse)
00289:                 )
00290:                 hero_deform_controller.location.z = (
00291:                     hero_deform_base_loc.z
00292:                     + math.sin(i * 0.027) * HERO_DEFORM_CONTROLLER_RADIUS * 0.28
00293:                     + beat * 0.08
00294:                 )
00295:                 hero_deform_controller.rotation_euler.x = hero_deform_base_rot.x + i * 0.006 + high * 0.14
00296:                 hero_deform_controller.rotation_euler.y = hero_deform_base_rot.y + math.sin(i * 0.022) * 0.18
00297:                 hero_deform_controller.rotation_euler.z = hero_deform_base_rot.z + i * 0.010 + onset * 0.24
00298: 
00299:                 deform_scale = 1.0 + deform_drive * 0.18
00300:                 hero_deform_controller.scale = (
00301:                     hero_deform_base_scale.x * deform_scale,
00302:                     hero_deform_base_scale.y * (1.0 + high * 0.12),
00303:                     hero_deform_base_scale.z * (1.0 + low * 0.10),
00304:                 )
00305: 
00306:                 hero_deform_controller.keyframe_insert(data_path="location", frame=i)
00307:                 hero_deform_controller.keyframe_insert(data_path="rotation_euler", frame=i)
00308:                 hero_deform_controller.keyframe_insert(data_path="scale", frame=i)
00309: 
00310:             for item in hero_deformers:
00311:                 phase = item["phase"]
00312:                 modifier = item["modifier"]
00313:                 ripple = 0.5 + 0.5 * math.sin(i * 0.045 + phase)
00314:                 main_strength_max = item.get("main_strength_max", HERO_DEFORM_STRENGTH_MAX)
00315:                 strength = HERO_DEFORM_STRENGTH_MIN + deform_drive * (
00316:                     main_strength_max - HERO_DEFORM_STRENGTH_MIN
00317:                 )
00318:                 modifier.strength = strength * (0.74 + ripple * 0.26)
00319:                 keyframe_if_possible(modifier, "strength", i)
00320: 
00321:                 detail_modifier = item.get("detail_modifier")
00322:                 if detail_modifier is not None:
00323:                     detail_drive = min(1.0, high * 0.56 + onset * 0.46 + deform_drive * 0.30)
00324:                     detail_modifier.strength = detail_drive * item.get(
00325:                         "detail_strength_max",
00326:                         HERO_DEFORM_DETAIL_STRENGTH_MAX,
00327:                     )
00328:                     keyframe_if_possible(detail_modifier, "strength", i)
00329: 
00330:                 wave_modifier = item.get("wave_modifier")
00331:                 if wave_modifier is not None:
00332:                     wave_drive = min(1.0, beat * 0.72 + onset * 0.36 + low * 0.20)
00333:                     try:
00334:                         wave_modifier.height = wave_drive * item.get(
00335:                             "wave_height_max",
00336:                             HERO_DEFORM_WAVE_HEIGHT_MAX,
00337:                         )
00338:                         keyframe_if_possible(wave_modifier, "height", i)
00339:                     except Exception:
00340:                         pass
00341:                     try:
00342:                         wave_modifier.time_offset = -i * 0.018 - phase
00343:                         keyframe_if_possible(wave_modifier, "time_offset", i)
00344:                     except Exception:
00345:                         pass
00346: 
00347:                 twist_modifier = item.get("twist_modifier")
00348:                 if twist_modifier is not None:
00349:                     twist_drive = min(1.0, mid * 0.42 + beat * 0.42 + onset * 0.34 + high * 0.18)
00350:                     twist_angle_max = item.get("twist_angle_max", HERO_DEFORM_TWIST_MAX)
00351:                     try:
00352:                         twist_modifier.angle = math.sin(i * 0.030 + phase) * twist_drive * twist_angle_max
00353:                         keyframe_if_possible(twist_modifier, "angle", i)
00354:                     except Exception:
00355:                         pass
00356: 
00357:         if hero_material_controls and deform_keyframe:
00358:             material_drive = min(1.0, high * 0.54 + mid * 0.22 + pulse * 0.38)
00359:             surface_drive = min(1.0, low * 0.24 + mid * 0.28 + high * 0.34 + onset * 0.26)
00360: 
00361:             for control in hero_material_controls:
00362:                 emission_socket = control.get("emission_socket")
00363:                 if emission_socket is not None:
00364:                     emission_socket.default_value = HERO_MATERIAL_EMISSION_MIN + material_drive * (
00365:                         HERO_MATERIAL_EMISSION_MAX - HERO_MATERIAL_EMISSION_MIN
00366:                     )
00367:                     keyframe_if_possible(emission_socket, "default_value", i)
00368: 
00369:                 self_light_socket = control.get("self_light_socket")
00370:                 if self_light_socket is not None:
00371:                     edge_drive = min(1.0, material_drive * 0.74 + surface_drive * 0.18 + pulse * 0.16)
00372:                     self_light_socket.default_value = HERO_MATERIAL_SELF_LIGHT_MIN + edge_drive * (
00373:                         HERO_MATERIAL_SELF_LIGHT_MAX - HERO_MATERIAL_SELF_LIGHT_MIN
00374:                     )
00375:                     keyframe_if_possible(self_light_socket, "default_value", i)
00376: 
00377:                 roughness_socket = control.get("roughness_socket")
00378:                 if roughness_socket is not None:
00379:                     roughness_socket.default_value = HERO_MATERIAL_ROUGHNESS_MAX - material_drive * (
00380:                         HERO_MATERIAL_ROUGHNESS_MAX - HERO_MATERIAL_ROUGHNESS_MIN
00381:                     )
00382:                     keyframe_if_possible(roughness_socket, "default_value", i)
00383: 
00384:                 bump_socket = control.get("bump_socket")
00385:                 if bump_socket is not None:
00386:                     bump_socket.default_value = HERO_MATERIAL_BUMP_MIN + surface_drive * (
00387:                         HERO_MATERIAL_BUMP_MAX - HERO_MATERIAL_BUMP_MIN
00388:                     )
00389:                     keyframe_if_possible(bump_socket, "default_value", i)
00390: 
00391:                 noise_scale_socket = control.get("noise_scale_socket")
00392:                 if noise_scale_socket is not None:
00393:                     noise_scale_socket.default_value = HERO_MATERIAL_NOISE_SCALE_MIN + surface_drive * (
00394:                         HERO_MATERIAL_NOISE_SCALE_MAX - HERO_MATERIAL_NOISE_SCALE_MIN
00395:                     )
00396:                     keyframe_if_possible(noise_scale_socket, "default_value", i)
00397: 
00398:                 mapping_location_socket = control.get("mapping_location_socket")
00399:                 if mapping_location_socket is not None:
00400:                     drift = HERO_MATERIAL_MAPPING_DRIFT
00401:                     loc = mapping_location_socket.default_value
00402:                     loc[0] = math.sin(i * 0.012) * drift + mid * drift * 0.45
00403:                     loc[1] = math.cos(i * 0.010) * drift + high * drift * 0.35
00404:                     loc[2] = i * 0.0018 + pulse * drift * 0.20
00405:                     keyframe_if_possible(mapping_location_socket, "default_value", i)
00406: 
00407:                 mapping_rotation_socket = control.get("mapping_rotation_socket")
00408:                 if mapping_rotation_socket is not None:
00409:                     rot = mapping_rotation_socket.default_value
00410:                     rot[0] = math.sin(i * 0.006) * 0.08 * (0.35 + surface_drive)
00411:                     rot[1] = math.cos(i * 0.005) * 0.06 * (0.30 + material_drive)
00412:                     rot[2] = i * 0.0025 + pulse * 0.09
00413:                     keyframe_if_possible(mapping_rotation_socket, "default_value", i)
00414: 
00415:         # SECONDARY ASSET
00416:         if secondary_root is not None:
00417:             ss = SECONDARY_SCALE_MIN + low * (SECONDARY_SCALE_MAX - SECONDARY_SCALE_MIN)
00418:             secondary_root.scale = (
00419:                 secondary_base_scale.x * ss,
00420:                 secondary_base_scale.y * ss,
00421:                 secondary_base_scale.z * ss,
00422:             )
00423: 
00424:             secondary_root.location.x = secondary_base_loc.x + math.sin(i * 0.018) * SECONDARY_DRIFT_X * (0.35 + mid * 0.65)
00425:             secondary_root.location.y = secondary_base_loc.y + math.cos(i * 0.022) * SECONDARY_DRIFT_Y * (0.30 + high * 0.70)
00426:             secondary_root.location.z = secondary_base_loc.z + low * SECONDARY_BOUNCE_Z + pulse * 0.06
00427: 
00428:             secondary_root.rotation_euler.x = secondary_base_rot.x + math.sin(i * 0.024) * SECONDARY_ROT_X * (0.35 + high * 0.65)
00429:             secondary_root.rotation_euler.y = secondary_base_rot.y + math.cos(i * 0.016) * math.radians(3.0) * (0.25 + mid * 0.75)
00430:             secondary_root.rotation_euler.z = secondary_base_rot.z + math.sin(i * 0.014) * SECONDARY_ROT_Z * (0.35 + pulse * 0.65)
00431: 
00432:             secondary_root.keyframe_insert(data_path="scale", frame=i)
00433:             secondary_root.keyframe_insert(data_path="location", frame=i)
00434:             secondary_root.keyframe_insert(data_path="rotation_euler", frame=i)
00435: 
00436:         # AURA
00437:         aura_obj.location.z = aura_base_loc.z + low * 0.08 + pulse * 0.04
00438:         aura_obj.scale = (
00439:             1.0 + low * 0.06,
00440:             1.0 + low * 0.06,
00441:             1.0 + low * 0.06,
00442:         )
00443:         aura_obj.keyframe_insert(data_path="location", frame=i)
00444:         aura_obj.keyframe_insert(data_path="scale", frame=i)
00445: 
00446:         aura_strength = 0.10 + (pulse * 0.55 + high * 0.45) * 1.25
00447:         if aura_data.get("strength_socket") is not None:
00448:             aura_data["strength_socket"].default_value = aura_strength
00449:             aura_data["strength_socket"].keyframe_insert(data_path="default_value", frame=i)
00450: 
00451:         try:
00452:             aura_edge = max(0.05, min(0.42, 0.18 - high * 0.05 + pulse * 0.10))
00453:             if aura_data.get("edge_ctrl") is not None:
00454:                 aura_data["edge_ctrl"].position = aura_edge
00455:                 aura_data["edge_ctrl"].keyframe_insert(data_path="position", frame=i)
00456:         except Exception:
00457:             pass
00458: 
00459:         # AURA AUDIO SAMPLER / INVISIBLE DEFORM FIELD
00460:         aura_sample_keyframe = (
00461:             i == 1
00462:             or i == total_frames
00463:             or i % AURA_DEFORM_KEYFRAME_STEP == 0
00464:             or beat > 0.0
00465:             or onset > 0.72
00466:         )
00467: 
00468:         if aura_audio_controller is not None and aura_sample_keyframe:
00469:             aura_deform = min(1.0, low * 0.44 + mid * 0.24 + transient * 0.58)
00470:             aura_detail = min(1.0, high * 0.60 + onset * 0.55 + beat * 0.25)
00471:             phase = i * 0.011 + mid * 0.35 + onset * 0.18
00472:             audio_values = {
00473:                 "low": low,
00474:                 "mid": mid,
00475:                 "high": high,
00476:                 "onset": onset,
```
