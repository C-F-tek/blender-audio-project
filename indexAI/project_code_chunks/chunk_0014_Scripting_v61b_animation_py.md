# Project Code Chunk 14/212

- File: `Scripting/v61b/animation.py`
- Part: `3`
- Lines: `477-682`

## Symbol Map
- Imports: `math`, `from config import HERO_SCALE_MIN, HERO_SCALE_MAX, HERO_BOUNCE_Z, HERO_ROT_Z, HERO_ROT_X, HERO_ROT_Y, HERO_DRIFT_X, HERO_DRIFT_Y, HERO_ORBIT_X, HERO_ORBIT_Y, HERO_BEAT_TWIST_Z, HERO_ONSET_SHAKE, HERO_DEFORM_STRENGTH_MIN, HERO_DEFORM_STRENGTH_MAX, HERO_DEFORM_DETAIL_STRENGTH_MAX, HERO_DEFORM_WAVE_HEIGHT_MAX, HERO_DEFORM_TWIST_MAX, HERO_DEFORM_CONTROLLER_RADIUS, HERO_DEFORM_KEYFRAME_STEP, HERO_MATERIAL_EMISSION_MIN, HERO_MATERIAL_EMISSION_MAX, HERO_MATERIAL_SELF_LIGHT_MIN, HERO_MATERIAL_SELF_LIGHT_MAX, HERO_MATERIAL_BUMP_MIN, HERO_MATERIAL_BUMP_MAX, HERO_MATERIAL_ROUGHNESS_MIN, HERO_MATERIAL_ROUGHNESS_MAX, HERO_MATERIAL_NOISE_SCALE_MIN, HERO_MATERIAL_NOISE_SCALE_MAX, HERO_MATERIAL_MAPPING_DRIFT, AURA_DEFORM_KEYFRAME_STEP, AURA_DEFORM_FIELD_DRIFT, AURA_DEFORM_FIELD_SCALE, SECONDARY_SCALE_MIN, SECONDARY_SCALE_MAX, SECONDARY_BOUNCE_Z, SECONDARY_DRIFT_X, SECONDARY_DRIFT_Y, SECONDARY_ROT_Z, SECONDARY_ROT_X, CAMERA_BEAT_BUMP_Z, CAMERA_BEAT_BUMP_Y, CAMERA_ORBIT_AMOUNT, CAMERA_PUSH_AMOUNT, CAMERA_VERTICAL_SWAY, LIGHT_ENERGY_MIN, LIGHT_ENERGY_MAX, PHYSICS_ACCENT_EMISSION_MIN, PHYSICS_ACCENT_EMISSION_MAX, PHYSICS_ACCENT_MIX_MIN, PHYSICS_ACCENT_MIX_MAX, PHYSICS_ATOM_ORBIT_SPEED_MIN, PHYSICS_ATOM_ORBIT_AUDIO_SPEED, PHYSICS_ATOM_ORBIT_RADIUS_PULSE, PHYSICS_ATOM_ORBIT_HEIGHT_SWAY, PHYSICS_ATOM_MICRO_WOBBLE, COMPOSITOR_GLARE_THRESHOLD_MIN, COMPOSITOR_GLARE_THRESHOLD_MAX, COMPOSITOR_LENS_DISTORT_MIN, COMPOSITOR_LENS_DISTORT_MAX, COMPOSITOR_LENS_DISPERSION_MIN, COMPOSITOR_LENS_DISPERSION_MAX, FIELD_STRENGTH_MIN, FIELD_STRENGTH_MAX, HERO_GRAVITY_STRENGTH_MIN, HERO_GRAVITY_STRENGTH_MAX, TURB_STRENGTH_MIN, TURB_STRENGTH_MAX, VORTEX_STRENGTH_MIN, VORTEX_STRENGTH_MAX, RHYTHM_PARTICLE_SIZE_MIN, RHYTHM_PARTICLE_SIZE_MAX, RHYTHM_PARTICLE_NORMAL_MIN, RHYTHM_PARTICLE_NORMAL_MAX, RHYTHM_PARTICLE_TANGENT_MIN, RHYTHM_PARTICLE_TANGENT_MAX, RHYTHM_PARTICLE_BROWNIAN_MIN, RHYTHM_PARTICLE_BROWNIAN_MAX, RHYTHM_PARTICLE_EMIT_MIN, RHYTHM_PARTICLE_EMIT_MAX, RHYTHM_PARTICLE_KEYFRAME_STEP, ALBUM_LETTER_PARTICLE_SIZE_MIN, ALBUM_LETTER_PARTICLE_SIZE_MAX, ALBUM_LETTER_ROOT_SCALE_MIN, ALBUM_LETTER_ROOT_SCALE_MAX, BACKDROP_EMISSION_MIN, BACKDROP_EMISSION_MAX, BACKDROP_BREATHE_SCALE, MIST_FLOAT_AMPLITUDE, MIST_BEAT_BOOST`, `from fog_dynamics import animate_fog_frame`, `from scene_utils import set_linear_interpolation_idblock`
- Functions: `keyframe_if_possible(idblock, data_path, frame)` line 99; `get_scene_compositor_tree(scene)` line 106; `rhythm_band_drive(band, response, low, mid, high, onset, beat, pulse, local_pulse)` line 114; `animate_scene(scene, frames, camera, target, hero_asset, secondary_asset, aura_data, fog_controller, scene_base, lights, physics_data, mist_particles, variants, energy_rings, energy_ribbons)` line 132

## Content
```py
00477:             aura_detail = min(1.0, high * 0.60 + onset * 0.55 + beat * 0.25)
00478:             phase = i * 0.011 + mid * 0.35 + onset * 0.18
00479:             audio_values = {
00480:                 "low": low,
00481:                 "mid": mid,
00482:                 "high": high,
00483:                 "onset": onset,
00484:                 "beat": beat,
00485:                 "pulse": pulse,
00486:                 "aura_deform": aura_deform,
00487:                 "detail": aura_detail,
00488:                 "phase": phase,
00489:             }
00490: 
00491:             for prop in aura_audio_props:
00492:                 if prop not in audio_values:
00493:                     continue
00494:                 aura_audio_controller[prop] = audio_values[prop]
00495:                 keyframe_if_possible(aura_audio_controller, f'["{prop}"]', i)
00496: 
00497:             aura_audio_controller.location.x = aura_audio_base_loc.x + math.sin(i * 0.018) * 0.18
00498:             aura_audio_controller.location.y = aura_audio_base_loc.y + math.cos(i * 0.016) * 0.14
00499:             aura_audio_controller.location.z = aura_audio_base_loc.z + aura_deform * 0.20
00500:             aura_audio_controller.rotation_euler.x = aura_audio_base_rot.x + i * 0.006 + high * 0.18
00501:             aura_audio_controller.rotation_euler.y = aura_audio_base_rot.y + math.sin(i * 0.021) * 0.14
00502:             aura_audio_controller.rotation_euler.z = aura_audio_base_rot.z + phase
00503:             aura_sampler_scale = 1.0 + aura_deform * 0.22
00504:             aura_audio_controller.scale = (
00505:                 aura_audio_base_scale.x * aura_sampler_scale,
00506:                 aura_audio_base_scale.y * (1.0 + aura_detail * 0.12),
00507:                 aura_audio_base_scale.z * (1.0 + low * 0.10),
00508:             )
00509:             aura_audio_controller.keyframe_insert(data_path="location", frame=i)
00510:             aura_audio_controller.keyframe_insert(data_path="rotation_euler", frame=i)
00511:             aura_audio_controller.keyframe_insert(data_path="scale", frame=i)
00512: 
00513:             if aura_deform_field is not None:
00514:                 aura_deform_field.location.x = aura_field_base_loc.x + math.sin(i * 0.025) * AURA_DEFORM_FIELD_DRIFT * (0.35 + mid)
00515:                 aura_deform_field.location.y = aura_field_base_loc.y + math.cos(i * 0.020) * AURA_DEFORM_FIELD_DRIFT * (0.25 + high)
00516:                 aura_deform_field.location.z = aura_field_base_loc.z + aura_deform * 0.16 + beat * 0.06
00517:                 aura_deform_field.rotation_euler.x = aura_field_base_rot.x + i * 0.009 + high * 0.22
00518:                 aura_deform_field.rotation_euler.y = aura_field_base_rot.y + math.sin(i * 0.031) * 0.20 + onset * 0.08
00519:                 aura_deform_field.rotation_euler.z = aura_field_base_rot.z + i * 0.013 + low * 0.12
00520: 
00521:                 compact = 1.0 - aura_deform * AURA_DEFORM_FIELD_SCALE * 0.45
00522:                 stretch = 1.0 + aura_deform * AURA_DEFORM_FIELD_SCALE
00523:                 aura_deform_field.scale = (
00524:                     aura_field_base_scale.x * compact,
00525:                     aura_field_base_scale.y * (1.0 + aura_detail * AURA_DEFORM_FIELD_SCALE * 0.45),
00526:                     aura_field_base_scale.z * stretch,
00527:                 )
00528:                 aura_deform_field.keyframe_insert(data_path="location", frame=i)
00529:                 aura_deform_field.keyframe_insert(data_path="rotation_euler", frame=i)
00530:                 aura_deform_field.keyframe_insert(data_path="scale", frame=i)
00531: 
00532:         # LIGHTS
00533:         if lights:
00534:             for light in lights:
00535:                 try:
00536:                     area_drive = min(1.0, high * 0.006 + mid * 0.006 + low * 0.005 + pulse * 0.004)
00537:                     light.data.energy = LIGHT_ENERGY_MIN + area_drive * (
00538:                         LIGHT_ENERGY_MAX - LIGHT_ENERGY_MIN
00539:                     )
00540:                     light.data.keyframe_insert(data_path="energy", frame=i)
00541:                 except Exception:
00542:                     pass
00543: 
00544:         # COMPOSITOR BREATH
00545:         if deform_keyframe:
00546:             comp_drive = min(1.0, high * 0.52 + onset * 0.34 + beat * 0.22)
00547: 
00548:             if compositor_glare is not None:
00549:                 try:
00550:                     compositor_glare.threshold = COMPOSITOR_GLARE_THRESHOLD_MAX - comp_drive * (
00551:                         COMPOSITOR_GLARE_THRESHOLD_MAX - COMPOSITOR_GLARE_THRESHOLD_MIN
00552:                     )
00553:                     keyframe_if_possible(compositor_glare, "threshold", i)
00554:                 except Exception:
00555:                     pass
00556: 
00557:             if compositor_lens is not None:
00558:                 try:
00559:                     if "Distort" in compositor_lens.inputs:
00560:                         compositor_lens.inputs["Distort"].default_value = COMPOSITOR_LENS_DISTORT_MIN + comp_drive * (
00561:                             COMPOSITOR_LENS_DISTORT_MAX - COMPOSITOR_LENS_DISTORT_MIN
00562:                         )
00563:                         keyframe_if_possible(compositor_lens.inputs["Distort"], "default_value", i)
00564:                     if "Dispersion" in compositor_lens.inputs:
00565:                         compositor_lens.inputs["Dispersion"].default_value = (
00566:                             COMPOSITOR_LENS_DISPERSION_MIN
00567:                             + comp_drive * (COMPOSITOR_LENS_DISPERSION_MAX - COMPOSITOR_LENS_DISPERSION_MIN)
00568:                         )
00569:                         keyframe_if_possible(compositor_lens.inputs["Dispersion"], "default_value", i)
00570:                 except Exception:
00571:                     pass
00572: 
00573:         # FOG
00574:         animate_fog_frame(
00575:             frame=i,
00576:             low=low,
00577:             mid=mid,
00578:             high=high,
00579:             onset=onset,
00580:             beat=beat,
00581:             pulse=pulse,
00582:             fog_controller=fog_controller,
00583:             fog_obj=fog_obj,
00584:             fog_control=fog_control,
00585:             fog_base_scale=fog_base_scale,
00586:             fog_base_loc=fog_base_loc,
00587:         )
00588: 
00589:         # BACKDROP
00590:         if backdrop is not None and backdrop_controls:
00591:             backdrop_drive = min(0.22, high * 0.035 + mid * 0.025 + pulse * 0.020)
00592:             if "emission_socket" in backdrop_controls:
00593:                 backdrop_controls["emission_socket"].default_value = BACKDROP_EMISSION_MIN + backdrop_drive * (
00594:                     BACKDROP_EMISSION_MAX - BACKDROP_EMISSION_MIN
00595:                 )
00596:                 backdrop_controls["emission_socket"].keyframe_insert(data_path="default_value", frame=i)
00597: 
00598:             if "mapping_location_socket" in backdrop_controls:
00599:                 bloc = backdrop_controls["mapping_location_socket"].default_value
00600:                 bloc[0] = i * 0.00018 + math.sin(i * 0.006) * 0.012
00601:                 bloc[1] = i * 0.00012 + backdrop_drive * 0.015
00602:                 bloc[2] = 0.0
00603:                 backdrop_controls["mapping_location_socket"].keyframe_insert(data_path="default_value", frame=i)
00604: 
00605:             if "noise_scale_socket" in backdrop_controls:
00606:                 backdrop_controls["noise_scale_socket"].default_value = 2.18 + backdrop_drive * 0.12
00607:                 backdrop_controls["noise_scale_socket"].keyframe_insert(data_path="default_value", frame=i)
00608: 
00609:             if backdrop_base_scale is not None and backdrop_base_loc is not None:
00610:                 bscale = 1.0 + backdrop_drive * BACKDROP_BREATHE_SCALE
00611:                 backdrop.scale = (
00612:                     backdrop_base_scale.x * bscale,
00613:                     backdrop_base_scale.y * (1.0 + backdrop_drive * BACKDROP_BREATHE_SCALE * 0.55),
00614:                     backdrop_base_scale.z,
00615:                 )
00616:                 backdrop.location.z = backdrop_base_loc.z + math.sin(i * 0.009) * 0.012
00617:                 backdrop.keyframe_insert(data_path="scale", frame=i)
00618:                 backdrop.keyframe_insert(data_path="location", frame=i)
00619: 
00620:             if backdrop_control is not None and backdrop_base_loc is not None:
00621:                 backdrop_control.location.x = backdrop_base_loc.x
00622:                 backdrop_control.location.y = backdrop_base_loc.y
00623:                 backdrop_control.location.z = backdrop_base_loc.z + backdrop_drive * 0.012
00624:                 backdrop_control.scale = (1.0 + backdrop_drive * 0.012, 1.0 + backdrop_drive * 0.012, 1.0)
00625:                 backdrop_control.keyframe_insert(data_path="location", frame=i)
00626:                 backdrop_control.keyframe_insert(data_path="scale", frame=i)
00627: 
00628:         # MIST
00629:         for item in mist_particles:
00630:             obj = item["object"]
00631:             phase = item["phase"]
00632:             base_loc = item["base_location"]
00633:             base_scale = item["base_scale"]
00634: 
00635:             obj.location.x = base_loc.x + math.sin(i * 0.012 + phase) * 0.16
00636:             obj.location.y = base_loc.y + math.cos(i * 0.010 + phase) * 0.14
00637:             obj.location.z = base_loc.z + math.sin(i * 0.015 + phase) * MIST_FLOAT_AMPLITUDE + beat * MIST_BEAT_BOOST
00638:             obj.keyframe_insert(data_path="location", frame=i)
00639: 
00640:             pscale = base_scale + high * 0.02 + pulse * 0.02
00641:             obj.scale = (pscale, pscale, pscale)
00642:             obj.keyframe_insert(data_path="scale", frame=i)
00643: 
00644:             em_val = 0.10 + high * 0.45 + pulse * 0.35
00645:             mix_val = 0.12 + pulse * 0.08
00646: 
00647:             item["emission_socket"].default_value = em_val
00648:             item["emission_socket"].keyframe_insert(data_path="default_value", frame=i)
00649: 
00650:             item["mix_socket"].default_value = mix_val
00651:             item["mix_socket"].keyframe_insert(data_path="default_value", frame=i)
00652: 
00653:         # VARIANTS
00654:         for idx, item in enumerate(variants):
00655:             obj = item["root"]
00656:             ang = item["angle"]
00657:             base_loc = item["base_location"]
00658:             base_scale = item["base_scale"]
00659:             phase = idx * 0.55
00660: 
00661:             obj.location.x = base_loc.x + math.sin(i * 0.016 + phase) * 0.20
00662:             obj.location.y = base_loc.y + math.cos(i * 0.014 + phase) * 0.18
00663:             obj.location.z = base_loc.z + high * 0.18 + math.sin(i * 0.018 + phase) * 0.04
00664: 
00665:             sc = base_scale + low * 0.07
00666:             obj.scale = (sc, sc, sc)
00667:             obj.rotation_euler.z = ang + math.sin(i * 0.012 + phase) * math.radians(14.0)
00668: 
00669:             obj.keyframe_insert(data_path="location", frame=i)
00670:             obj.keyframe_insert(data_path="scale", frame=i)
00671:             obj.keyframe_insert(data_path="rotation_euler", frame=i)
00672: 
00673:         # RINGS / RIBBONS
00674:         for item in energy_rings:
00675:             ring = item["object"]
00676:             phase = item["phase"]
00677:             base_scale = item["base_scale"]
00678:             base_rot = item["base_rot"]
00679:             base_loc = item["base_loc"]
00680: 
00681:             pulse_scale = 1.0 + low * 0.03 + pulse * 0.02
00682:             ring.scale = (
```
