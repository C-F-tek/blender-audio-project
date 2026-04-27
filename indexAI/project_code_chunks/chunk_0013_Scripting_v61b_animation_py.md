# Project Code Chunk 13/212

- File: `Scripting/v61b/animation.py`
- Part: `2`
- Lines: `281-476`

## Symbol Map
- Imports: `math`, `from config import HERO_SCALE_MIN, HERO_SCALE_MAX, HERO_BOUNCE_Z, HERO_ROT_Z, HERO_ROT_X, HERO_ROT_Y, HERO_DRIFT_X, HERO_DRIFT_Y, HERO_ORBIT_X, HERO_ORBIT_Y, HERO_BEAT_TWIST_Z, HERO_ONSET_SHAKE, HERO_DEFORM_STRENGTH_MIN, HERO_DEFORM_STRENGTH_MAX, HERO_DEFORM_DETAIL_STRENGTH_MAX, HERO_DEFORM_WAVE_HEIGHT_MAX, HERO_DEFORM_TWIST_MAX, HERO_DEFORM_CONTROLLER_RADIUS, HERO_DEFORM_KEYFRAME_STEP, HERO_MATERIAL_EMISSION_MIN, HERO_MATERIAL_EMISSION_MAX, HERO_MATERIAL_SELF_LIGHT_MIN, HERO_MATERIAL_SELF_LIGHT_MAX, HERO_MATERIAL_BUMP_MIN, HERO_MATERIAL_BUMP_MAX, HERO_MATERIAL_ROUGHNESS_MIN, HERO_MATERIAL_ROUGHNESS_MAX, HERO_MATERIAL_NOISE_SCALE_MIN, HERO_MATERIAL_NOISE_SCALE_MAX, HERO_MATERIAL_MAPPING_DRIFT, AURA_DEFORM_KEYFRAME_STEP, AURA_DEFORM_FIELD_DRIFT, AURA_DEFORM_FIELD_SCALE, SECONDARY_SCALE_MIN, SECONDARY_SCALE_MAX, SECONDARY_BOUNCE_Z, SECONDARY_DRIFT_X, SECONDARY_DRIFT_Y, SECONDARY_ROT_Z, SECONDARY_ROT_X, CAMERA_BEAT_BUMP_Z, CAMERA_BEAT_BUMP_Y, CAMERA_ORBIT_AMOUNT, CAMERA_PUSH_AMOUNT, CAMERA_VERTICAL_SWAY, LIGHT_ENERGY_MIN, LIGHT_ENERGY_MAX, PHYSICS_ACCENT_EMISSION_MIN, PHYSICS_ACCENT_EMISSION_MAX, PHYSICS_ACCENT_MIX_MIN, PHYSICS_ACCENT_MIX_MAX, PHYSICS_ATOM_ORBIT_SPEED_MIN, PHYSICS_ATOM_ORBIT_AUDIO_SPEED, PHYSICS_ATOM_ORBIT_RADIUS_PULSE, PHYSICS_ATOM_ORBIT_HEIGHT_SWAY, PHYSICS_ATOM_MICRO_WOBBLE, COMPOSITOR_GLARE_THRESHOLD_MIN, COMPOSITOR_GLARE_THRESHOLD_MAX, COMPOSITOR_LENS_DISTORT_MIN, COMPOSITOR_LENS_DISTORT_MAX, COMPOSITOR_LENS_DISPERSION_MIN, COMPOSITOR_LENS_DISPERSION_MAX, FIELD_STRENGTH_MIN, FIELD_STRENGTH_MAX, HERO_GRAVITY_STRENGTH_MIN, HERO_GRAVITY_STRENGTH_MAX, TURB_STRENGTH_MIN, TURB_STRENGTH_MAX, VORTEX_STRENGTH_MIN, VORTEX_STRENGTH_MAX, RHYTHM_PARTICLE_SIZE_MIN, RHYTHM_PARTICLE_SIZE_MAX, RHYTHM_PARTICLE_NORMAL_MIN, RHYTHM_PARTICLE_NORMAL_MAX, RHYTHM_PARTICLE_TANGENT_MIN, RHYTHM_PARTICLE_TANGENT_MAX, RHYTHM_PARTICLE_BROWNIAN_MIN, RHYTHM_PARTICLE_BROWNIAN_MAX, RHYTHM_PARTICLE_EMIT_MIN, RHYTHM_PARTICLE_EMIT_MAX, RHYTHM_PARTICLE_KEYFRAME_STEP, ALBUM_LETTER_PARTICLE_SIZE_MIN, ALBUM_LETTER_PARTICLE_SIZE_MAX, ALBUM_LETTER_ROOT_SCALE_MIN, ALBUM_LETTER_ROOT_SCALE_MAX, BACKDROP_EMISSION_MIN, BACKDROP_EMISSION_MAX, BACKDROP_BREATHE_SCALE, MIST_FLOAT_AMPLITUDE, MIST_BEAT_BOOST`, `from fog_dynamics import animate_fog_frame`, `from scene_utils import set_linear_interpolation_idblock`
- Functions: `keyframe_if_possible(idblock, data_path, frame)` line 99; `get_scene_compositor_tree(scene)` line 106; `rhythm_band_drive(band, response, low, mid, high, onset, beat, pulse, local_pulse)` line 114; `animate_scene(scene, frames, camera, target, hero_asset, secondary_asset, aura_data, fog_controller, scene_base, lights, physics_data, mist_particles, variants, energy_rings, energy_ribbons)` line 132

## Content
```py
00281:             or i % HERO_DEFORM_KEYFRAME_STEP == 0
00282:             or beat > 0.0
00283:             or onset > 0.72
00284:         )
00285: 
00286:         if hero_deformers and deform_keyframe:
00287:             deform_drive = min(1.0, low * 0.58 + mid * 0.20 + transient * 0.52)
00288:             if hero_deform_controller is not None:
00289:                 hero_deform_controller.location.x = (
00290:                     hero_deform_base_loc.x
00291:                     + math.sin(i * 0.036) * HERO_DEFORM_CONTROLLER_RADIUS * (0.45 + deform_drive)
00292:                 )
00293:                 hero_deform_controller.location.y = (
00294:                     hero_deform_base_loc.y
00295:                     + math.cos(i * 0.031) * HERO_DEFORM_CONTROLLER_RADIUS * (0.35 + pulse)
00296:                 )
00297:                 hero_deform_controller.location.z = (
00298:                     hero_deform_base_loc.z
00299:                     + math.sin(i * 0.027) * HERO_DEFORM_CONTROLLER_RADIUS * 0.28
00300:                     + beat * 0.08
00301:                 )
00302:                 hero_deform_controller.rotation_euler.x = hero_deform_base_rot.x + i * 0.006 + high * 0.14
00303:                 hero_deform_controller.rotation_euler.y = hero_deform_base_rot.y + math.sin(i * 0.022) * 0.18
00304:                 hero_deform_controller.rotation_euler.z = hero_deform_base_rot.z + i * 0.010 + onset * 0.24
00305: 
00306:                 deform_scale = 1.0 + deform_drive * 0.18
00307:                 hero_deform_controller.scale = (
00308:                     hero_deform_base_scale.x * deform_scale,
00309:                     hero_deform_base_scale.y * (1.0 + high * 0.12),
00310:                     hero_deform_base_scale.z * (1.0 + low * 0.10),
00311:                 )
00312: 
00313:                 hero_deform_controller.keyframe_insert(data_path="location", frame=i)
00314:                 hero_deform_controller.keyframe_insert(data_path="rotation_euler", frame=i)
00315:                 hero_deform_controller.keyframe_insert(data_path="scale", frame=i)
00316: 
00317:             for item in hero_deformers:
00318:                 phase = item["phase"]
00319:                 modifier = item["modifier"]
00320:                 ripple = 0.5 + 0.5 * math.sin(i * 0.045 + phase)
00321:                 main_strength_max = item.get("main_strength_max", HERO_DEFORM_STRENGTH_MAX)
00322:                 strength = HERO_DEFORM_STRENGTH_MIN + deform_drive * (
00323:                     main_strength_max - HERO_DEFORM_STRENGTH_MIN
00324:                 )
00325:                 modifier.strength = strength * (0.74 + ripple * 0.26)
00326:                 keyframe_if_possible(modifier, "strength", i)
00327: 
00328:                 detail_modifier = item.get("detail_modifier")
00329:                 if detail_modifier is not None:
00330:                     detail_drive = min(1.0, high * 0.56 + onset * 0.46 + deform_drive * 0.30)
00331:                     detail_modifier.strength = detail_drive * item.get(
00332:                         "detail_strength_max",
00333:                         HERO_DEFORM_DETAIL_STRENGTH_MAX,
00334:                     )
00335:                     keyframe_if_possible(detail_modifier, "strength", i)
00336: 
00337:                 wave_modifier = item.get("wave_modifier")
00338:                 if wave_modifier is not None:
00339:                     wave_drive = min(1.0, beat * 0.72 + onset * 0.36 + low * 0.20)
00340:                     try:
00341:                         wave_modifier.height = wave_drive * item.get(
00342:                             "wave_height_max",
00343:                             HERO_DEFORM_WAVE_HEIGHT_MAX,
00344:                         )
00345:                         keyframe_if_possible(wave_modifier, "height", i)
00346:                     except Exception:
00347:                         pass
00348:                     try:
00349:                         wave_modifier.time_offset = -i * 0.018 - phase
00350:                         keyframe_if_possible(wave_modifier, "time_offset", i)
00351:                     except Exception:
00352:                         pass
00353: 
00354:                 twist_modifier = item.get("twist_modifier")
00355:                 if twist_modifier is not None:
00356:                     twist_drive = min(1.0, mid * 0.42 + beat * 0.42 + onset * 0.34 + high * 0.18)
00357:                     twist_angle_max = item.get("twist_angle_max", HERO_DEFORM_TWIST_MAX)
00358:                     try:
00359:                         twist_modifier.angle = math.sin(i * 0.030 + phase) * twist_drive * twist_angle_max
00360:                         keyframe_if_possible(twist_modifier, "angle", i)
00361:                     except Exception:
00362:                         pass
00363: 
00364:         if hero_material_controls and deform_keyframe:
00365:             material_drive = min(1.0, high * 0.54 + mid * 0.22 + pulse * 0.38)
00366:             surface_drive = min(1.0, low * 0.24 + mid * 0.28 + high * 0.34 + onset * 0.26)
00367: 
00368:             for control in hero_material_controls:
00369:                 emission_socket = control.get("emission_socket")
00370:                 if emission_socket is not None:
00371:                     emission_socket.default_value = HERO_MATERIAL_EMISSION_MIN + material_drive * (
00372:                         HERO_MATERIAL_EMISSION_MAX - HERO_MATERIAL_EMISSION_MIN
00373:                     )
00374:                     keyframe_if_possible(emission_socket, "default_value", i)
00375: 
00376:                 self_light_socket = control.get("self_light_socket")
00377:                 if self_light_socket is not None:
00378:                     edge_drive = min(1.0, material_drive * 0.74 + surface_drive * 0.18 + pulse * 0.16)
00379:                     self_light_socket.default_value = HERO_MATERIAL_SELF_LIGHT_MIN + edge_drive * (
00380:                         HERO_MATERIAL_SELF_LIGHT_MAX - HERO_MATERIAL_SELF_LIGHT_MIN
00381:                     )
00382:                     keyframe_if_possible(self_light_socket, "default_value", i)
00383: 
00384:                 roughness_socket = control.get("roughness_socket")
00385:                 if roughness_socket is not None:
00386:                     roughness_socket.default_value = HERO_MATERIAL_ROUGHNESS_MAX - material_drive * (
00387:                         HERO_MATERIAL_ROUGHNESS_MAX - HERO_MATERIAL_ROUGHNESS_MIN
00388:                     )
00389:                     keyframe_if_possible(roughness_socket, "default_value", i)
00390: 
00391:                 bump_socket = control.get("bump_socket")
00392:                 if bump_socket is not None:
00393:                     bump_socket.default_value = HERO_MATERIAL_BUMP_MIN + surface_drive * (
00394:                         HERO_MATERIAL_BUMP_MAX - HERO_MATERIAL_BUMP_MIN
00395:                     )
00396:                     keyframe_if_possible(bump_socket, "default_value", i)
00397: 
00398:                 noise_scale_socket = control.get("noise_scale_socket")
00399:                 if noise_scale_socket is not None:
00400:                     noise_scale_socket.default_value = HERO_MATERIAL_NOISE_SCALE_MIN + surface_drive * (
00401:                         HERO_MATERIAL_NOISE_SCALE_MAX - HERO_MATERIAL_NOISE_SCALE_MIN
00402:                     )
00403:                     keyframe_if_possible(noise_scale_socket, "default_value", i)
00404: 
00405:                 mapping_location_socket = control.get("mapping_location_socket")
00406:                 if mapping_location_socket is not None:
00407:                     drift = HERO_MATERIAL_MAPPING_DRIFT
00408:                     loc = mapping_location_socket.default_value
00409:                     loc[0] = math.sin(i * 0.012) * drift + mid * drift * 0.45
00410:                     loc[1] = math.cos(i * 0.010) * drift + high * drift * 0.35
00411:                     loc[2] = i * 0.0018 + pulse * drift * 0.20
00412:                     keyframe_if_possible(mapping_location_socket, "default_value", i)
00413: 
00414:                 mapping_rotation_socket = control.get("mapping_rotation_socket")
00415:                 if mapping_rotation_socket is not None:
00416:                     rot = mapping_rotation_socket.default_value
00417:                     rot[0] = math.sin(i * 0.006) * 0.08 * (0.35 + surface_drive)
00418:                     rot[1] = math.cos(i * 0.005) * 0.06 * (0.30 + material_drive)
00419:                     rot[2] = i * 0.0025 + pulse * 0.09
00420:                     keyframe_if_possible(mapping_rotation_socket, "default_value", i)
00421: 
00422:         # SECONDARY ASSET
00423:         if secondary_root is not None:
00424:             ss = SECONDARY_SCALE_MIN + low * (SECONDARY_SCALE_MAX - SECONDARY_SCALE_MIN)
00425:             secondary_root.scale = (
00426:                 secondary_base_scale.x * ss,
00427:                 secondary_base_scale.y * ss,
00428:                 secondary_base_scale.z * ss,
00429:             )
00430: 
00431:             secondary_root.location.x = secondary_base_loc.x + math.sin(i * 0.018) * SECONDARY_DRIFT_X * (0.35 + mid * 0.65)
00432:             secondary_root.location.y = secondary_base_loc.y + math.cos(i * 0.022) * SECONDARY_DRIFT_Y * (0.30 + high * 0.70)
00433:             secondary_root.location.z = secondary_base_loc.z + low * SECONDARY_BOUNCE_Z + pulse * 0.06
00434: 
00435:             secondary_root.rotation_euler.x = secondary_base_rot.x + math.sin(i * 0.024) * SECONDARY_ROT_X * (0.35 + high * 0.65)
00436:             secondary_root.rotation_euler.y = secondary_base_rot.y + math.cos(i * 0.016) * math.radians(3.0) * (0.25 + mid * 0.75)
00437:             secondary_root.rotation_euler.z = secondary_base_rot.z + math.sin(i * 0.014) * SECONDARY_ROT_Z * (0.35 + pulse * 0.65)
00438: 
00439:             secondary_root.keyframe_insert(data_path="scale", frame=i)
00440:             secondary_root.keyframe_insert(data_path="location", frame=i)
00441:             secondary_root.keyframe_insert(data_path="rotation_euler", frame=i)
00442: 
00443:         # AURA
00444:         aura_obj.location.z = aura_base_loc.z + low * 0.08 + pulse * 0.04
00445:         aura_obj.scale = (
00446:             1.0 + low * 0.06,
00447:             1.0 + low * 0.06,
00448:             1.0 + low * 0.06,
00449:         )
00450:         aura_obj.keyframe_insert(data_path="location", frame=i)
00451:         aura_obj.keyframe_insert(data_path="scale", frame=i)
00452: 
00453:         aura_strength = 0.10 + (pulse * 0.55 + high * 0.45) * 1.25
00454:         if aura_data.get("strength_socket") is not None:
00455:             aura_data["strength_socket"].default_value = aura_strength
00456:             aura_data["strength_socket"].keyframe_insert(data_path="default_value", frame=i)
00457: 
00458:         try:
00459:             aura_edge = max(0.05, min(0.42, 0.18 - high * 0.05 + pulse * 0.10))
00460:             if aura_data.get("edge_ctrl") is not None:
00461:                 aura_data["edge_ctrl"].position = aura_edge
00462:                 aura_data["edge_ctrl"].keyframe_insert(data_path="position", frame=i)
00463:         except Exception:
00464:             pass
00465: 
00466:         # AURA AUDIO SAMPLER / INVISIBLE DEFORM FIELD
00467:         aura_sample_keyframe = (
00468:             i == 1
00469:             or i == total_frames
00470:             or i % AURA_DEFORM_KEYFRAME_STEP == 0
00471:             or beat > 0.0
00472:             or onset > 0.72
00473:         )
00474: 
00475:         if aura_audio_controller is not None and aura_sample_keyframe:
00476:             aura_deform = min(1.0, low * 0.44 + mid * 0.24 + transient * 0.58)
```
