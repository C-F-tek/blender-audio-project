# Project Code Chunk 73/212

- File: `Scripting/v61b_backgood/animation.py`
- Part: `3`
- Lines: `477-682`

## Symbol Map
- Imports: `math`, `from config import HERO_SCALE_MIN, HERO_SCALE_MAX, HERO_BOUNCE_Z, HERO_ROT_Z, HERO_ROT_X, HERO_ROT_Y, HERO_DRIFT_X, HERO_DRIFT_Y, HERO_ORBIT_X, HERO_ORBIT_Y, HERO_BEAT_TWIST_Z, HERO_ONSET_SHAKE, HERO_DEFORM_STRENGTH_MIN, HERO_DEFORM_STRENGTH_MAX, HERO_DEFORM_DETAIL_STRENGTH_MAX, HERO_DEFORM_WAVE_HEIGHT_MAX, HERO_DEFORM_TWIST_MAX, HERO_DEFORM_CONTROLLER_RADIUS, HERO_DEFORM_KEYFRAME_STEP, HERO_MATERIAL_EMISSION_MIN, HERO_MATERIAL_EMISSION_MAX, HERO_MATERIAL_SELF_LIGHT_MIN, HERO_MATERIAL_SELF_LIGHT_MAX, HERO_MATERIAL_BUMP_MIN, HERO_MATERIAL_BUMP_MAX, HERO_MATERIAL_ROUGHNESS_MIN, HERO_MATERIAL_ROUGHNESS_MAX, HERO_MATERIAL_NOISE_SCALE_MIN, HERO_MATERIAL_NOISE_SCALE_MAX, HERO_MATERIAL_MAPPING_DRIFT, AURA_DEFORM_KEYFRAME_STEP, AURA_DEFORM_FIELD_DRIFT, AURA_DEFORM_FIELD_SCALE, SECONDARY_SCALE_MIN, SECONDARY_SCALE_MAX, SECONDARY_BOUNCE_Z, SECONDARY_DRIFT_X, SECONDARY_DRIFT_Y, SECONDARY_ROT_Z, SECONDARY_ROT_X, CAMERA_BEAT_BUMP_Z, CAMERA_BEAT_BUMP_Y, CAMERA_ORBIT_AMOUNT, CAMERA_PUSH_AMOUNT, CAMERA_VERTICAL_SWAY, LIGHT_ENERGY_MIN, LIGHT_ENERGY_MAX, PHYSICS_ACCENT_EMISSION_MIN, PHYSICS_ACCENT_EMISSION_MAX, PHYSICS_ACCENT_MIX_MIN, PHYSICS_ACCENT_MIX_MAX, COMPOSITOR_GLARE_THRESHOLD_MIN, COMPOSITOR_GLARE_THRESHOLD_MAX, COMPOSITOR_LENS_DISTORT_MIN, COMPOSITOR_LENS_DISTORT_MAX, COMPOSITOR_LENS_DISPERSION_MIN, COMPOSITOR_LENS_DISPERSION_MAX, FIELD_STRENGTH_MIN, FIELD_STRENGTH_MAX, TURB_STRENGTH_MIN, TURB_STRENGTH_MAX, VORTEX_STRENGTH_MIN, VORTEX_STRENGTH_MAX, RHYTHM_PARTICLE_SIZE_MIN, RHYTHM_PARTICLE_SIZE_MAX, RHYTHM_PARTICLE_NORMAL_MIN, RHYTHM_PARTICLE_NORMAL_MAX, RHYTHM_PARTICLE_TANGENT_MIN, RHYTHM_PARTICLE_TANGENT_MAX, RHYTHM_PARTICLE_BROWNIAN_MIN, RHYTHM_PARTICLE_BROWNIAN_MAX, RHYTHM_PARTICLE_EMIT_MIN, RHYTHM_PARTICLE_EMIT_MAX, RHYTHM_PARTICLE_KEYFRAME_STEP, ALBUM_LETTER_PARTICLE_SIZE_MIN, ALBUM_LETTER_PARTICLE_SIZE_MAX, ALBUM_LETTER_ROOT_SCALE_MIN, ALBUM_LETTER_ROOT_SCALE_MAX, BACKDROP_EMISSION_MIN, BACKDROP_EMISSION_MAX, BACKDROP_BREATHE_SCALE, MIST_FLOAT_AMPLITUDE, MIST_BEAT_BOOST`, `from fog_dynamics import animate_fog_frame`, `from scene_utils import set_linear_interpolation_idblock`
- Functions: `keyframe_if_possible(idblock, data_path, frame)` line 92; `get_scene_compositor_tree(scene)` line 99; `rhythm_band_drive(band, response, low, mid, high, onset, beat, pulse, local_pulse)` line 107; `animate_scene(scene, frames, camera, target, hero_asset, secondary_asset, aura_data, fog_controller, scene_base, lights, physics_data, mist_particles, variants, energy_rings, energy_ribbons)` line 125

## Content
```py
00477:                 "beat": beat,
00478:                 "pulse": pulse,
00479:                 "aura_deform": aura_deform,
00480:                 "detail": aura_detail,
00481:                 "phase": phase,
00482:             }
00483: 
00484:             for prop in aura_audio_props:
00485:                 if prop not in audio_values:
00486:                     continue
00487:                 aura_audio_controller[prop] = audio_values[prop]
00488:                 keyframe_if_possible(aura_audio_controller, f'["{prop}"]', i)
00489: 
00490:             aura_audio_controller.location.x = aura_audio_base_loc.x + math.sin(i * 0.018) * 0.18
00491:             aura_audio_controller.location.y = aura_audio_base_loc.y + math.cos(i * 0.016) * 0.14
00492:             aura_audio_controller.location.z = aura_audio_base_loc.z + aura_deform * 0.20
00493:             aura_audio_controller.rotation_euler.x = aura_audio_base_rot.x + i * 0.006 + high * 0.18
00494:             aura_audio_controller.rotation_euler.y = aura_audio_base_rot.y + math.sin(i * 0.021) * 0.14
00495:             aura_audio_controller.rotation_euler.z = aura_audio_base_rot.z + phase
00496:             aura_sampler_scale = 1.0 + aura_deform * 0.22
00497:             aura_audio_controller.scale = (
00498:                 aura_audio_base_scale.x * aura_sampler_scale,
00499:                 aura_audio_base_scale.y * (1.0 + aura_detail * 0.12),
00500:                 aura_audio_base_scale.z * (1.0 + low * 0.10),
00501:             )
00502:             aura_audio_controller.keyframe_insert(data_path="location", frame=i)
00503:             aura_audio_controller.keyframe_insert(data_path="rotation_euler", frame=i)
00504:             aura_audio_controller.keyframe_insert(data_path="scale", frame=i)
00505: 
00506:             if aura_deform_field is not None:
00507:                 aura_deform_field.location.x = aura_field_base_loc.x + math.sin(i * 0.025) * AURA_DEFORM_FIELD_DRIFT * (0.35 + mid)
00508:                 aura_deform_field.location.y = aura_field_base_loc.y + math.cos(i * 0.020) * AURA_DEFORM_FIELD_DRIFT * (0.25 + high)
00509:                 aura_deform_field.location.z = aura_field_base_loc.z + aura_deform * 0.16 + beat * 0.06
00510:                 aura_deform_field.rotation_euler.x = aura_field_base_rot.x + i * 0.009 + high * 0.22
00511:                 aura_deform_field.rotation_euler.y = aura_field_base_rot.y + math.sin(i * 0.031) * 0.20 + onset * 0.08
00512:                 aura_deform_field.rotation_euler.z = aura_field_base_rot.z + i * 0.013 + low * 0.12
00513: 
00514:                 compact = 1.0 - aura_deform * AURA_DEFORM_FIELD_SCALE * 0.45
00515:                 stretch = 1.0 + aura_deform * AURA_DEFORM_FIELD_SCALE
00516:                 aura_deform_field.scale = (
00517:                     aura_field_base_scale.x * compact,
00518:                     aura_field_base_scale.y * (1.0 + aura_detail * AURA_DEFORM_FIELD_SCALE * 0.45),
00519:                     aura_field_base_scale.z * stretch,
00520:                 )
00521:                 aura_deform_field.keyframe_insert(data_path="location", frame=i)
00522:                 aura_deform_field.keyframe_insert(data_path="rotation_euler", frame=i)
00523:                 aura_deform_field.keyframe_insert(data_path="scale", frame=i)
00524: 
00525:         # LIGHTS
00526:         if lights:
00527:             for light in lights:
00528:                 try:
00529:                     area_drive = min(1.0, high * 0.006 + mid * 0.006 + low * 0.005 + pulse * 0.004)
00530:                     light.data.energy = LIGHT_ENERGY_MIN + area_drive * (
00531:                         LIGHT_ENERGY_MAX - LIGHT_ENERGY_MIN
00532:                     )
00533:                     light.data.keyframe_insert(data_path="energy", frame=i)
00534:                 except Exception:
00535:                     pass
00536: 
00537:         # COMPOSITOR BREATH
00538:         if deform_keyframe:
00539:             comp_drive = min(1.0, high * 0.52 + onset * 0.34 + beat * 0.22)
00540: 
00541:             if compositor_glare is not None:
00542:                 try:
00543:                     compositor_glare.threshold = COMPOSITOR_GLARE_THRESHOLD_MAX - comp_drive * (
00544:                         COMPOSITOR_GLARE_THRESHOLD_MAX - COMPOSITOR_GLARE_THRESHOLD_MIN
00545:                     )
00546:                     keyframe_if_possible(compositor_glare, "threshold", i)
00547:                 except Exception:
00548:                     pass
00549: 
00550:             if compositor_lens is not None:
00551:                 try:
00552:                     if "Distort" in compositor_lens.inputs:
00553:                         compositor_lens.inputs["Distort"].default_value = COMPOSITOR_LENS_DISTORT_MIN + comp_drive * (
00554:                             COMPOSITOR_LENS_DISTORT_MAX - COMPOSITOR_LENS_DISTORT_MIN
00555:                         )
00556:                         keyframe_if_possible(compositor_lens.inputs["Distort"], "default_value", i)
00557:                     if "Dispersion" in compositor_lens.inputs:
00558:                         compositor_lens.inputs["Dispersion"].default_value = (
00559:                             COMPOSITOR_LENS_DISPERSION_MIN
00560:                             + comp_drive * (COMPOSITOR_LENS_DISPERSION_MAX - COMPOSITOR_LENS_DISPERSION_MIN)
00561:                         )
00562:                         keyframe_if_possible(compositor_lens.inputs["Dispersion"], "default_value", i)
00563:                 except Exception:
00564:                     pass
00565: 
00566:         # FOG
00567:         animate_fog_frame(
00568:             frame=i,
00569:             low=low,
00570:             mid=mid,
00571:             high=high,
00572:             onset=onset,
00573:             beat=beat,
00574:             pulse=pulse,
00575:             fog_controller=fog_controller,
00576:             fog_obj=fog_obj,
00577:             fog_control=fog_control,
00578:             fog_base_scale=fog_base_scale,
00579:             fog_base_loc=fog_base_loc,
00580:         )
00581: 
00582:         # BACKDROP
00583:         if backdrop is not None and backdrop_controls:
00584:             backdrop_drive = min(0.22, high * 0.035 + mid * 0.025 + pulse * 0.020)
00585:             if "emission_socket" in backdrop_controls:
00586:                 backdrop_controls["emission_socket"].default_value = BACKDROP_EMISSION_MIN + backdrop_drive * (
00587:                     BACKDROP_EMISSION_MAX - BACKDROP_EMISSION_MIN
00588:                 )
00589:                 backdrop_controls["emission_socket"].keyframe_insert(data_path="default_value", frame=i)
00590: 
00591:             if "mapping_location_socket" in backdrop_controls:
00592:                 bloc = backdrop_controls["mapping_location_socket"].default_value
00593:                 bloc[0] = i * 0.00018 + math.sin(i * 0.006) * 0.012
00594:                 bloc[1] = i * 0.00012 + backdrop_drive * 0.015
00595:                 bloc[2] = 0.0
00596:                 backdrop_controls["mapping_location_socket"].keyframe_insert(data_path="default_value", frame=i)
00597: 
00598:             if "noise_scale_socket" in backdrop_controls:
00599:                 backdrop_controls["noise_scale_socket"].default_value = 2.18 + backdrop_drive * 0.12
00600:                 backdrop_controls["noise_scale_socket"].keyframe_insert(data_path="default_value", frame=i)
00601: 
00602:             if backdrop_base_scale is not None and backdrop_base_loc is not None:
00603:                 bscale = 1.0 + backdrop_drive * BACKDROP_BREATHE_SCALE
00604:                 backdrop.scale = (
00605:                     backdrop_base_scale.x * bscale,
00606:                     backdrop_base_scale.y * (1.0 + backdrop_drive * BACKDROP_BREATHE_SCALE * 0.55),
00607:                     backdrop_base_scale.z,
00608:                 )
00609:                 backdrop.location.z = backdrop_base_loc.z + math.sin(i * 0.009) * 0.012
00610:                 backdrop.keyframe_insert(data_path="scale", frame=i)
00611:                 backdrop.keyframe_insert(data_path="location", frame=i)
00612: 
00613:             if backdrop_control is not None and backdrop_base_loc is not None:
00614:                 backdrop_control.location.x = backdrop_base_loc.x
00615:                 backdrop_control.location.y = backdrop_base_loc.y
00616:                 backdrop_control.location.z = backdrop_base_loc.z + backdrop_drive * 0.012
00617:                 backdrop_control.scale = (1.0 + backdrop_drive * 0.012, 1.0 + backdrop_drive * 0.012, 1.0)
00618:                 backdrop_control.keyframe_insert(data_path="location", frame=i)
00619:                 backdrop_control.keyframe_insert(data_path="scale", frame=i)
00620: 
00621:         # MIST
00622:         for item in mist_particles:
00623:             obj = item["object"]
00624:             phase = item["phase"]
00625:             base_loc = item["base_location"]
00626:             base_scale = item["base_scale"]
00627: 
00628:             obj.location.x = base_loc.x + math.sin(i * 0.012 + phase) * 0.16
00629:             obj.location.y = base_loc.y + math.cos(i * 0.010 + phase) * 0.14
00630:             obj.location.z = base_loc.z + math.sin(i * 0.015 + phase) * MIST_FLOAT_AMPLITUDE + beat * MIST_BEAT_BOOST
00631:             obj.keyframe_insert(data_path="location", frame=i)
00632: 
00633:             pscale = base_scale + high * 0.02 + pulse * 0.02
00634:             obj.scale = (pscale, pscale, pscale)
00635:             obj.keyframe_insert(data_path="scale", frame=i)
00636: 
00637:             em_val = 0.10 + high * 0.45 + pulse * 0.35
00638:             mix_val = 0.12 + pulse * 0.08
00639: 
00640:             item["emission_socket"].default_value = em_val
00641:             item["emission_socket"].keyframe_insert(data_path="default_value", frame=i)
00642: 
00643:             item["mix_socket"].default_value = mix_val
00644:             item["mix_socket"].keyframe_insert(data_path="default_value", frame=i)
00645: 
00646:         # VARIANTS
00647:         for idx, item in enumerate(variants):
00648:             obj = item["root"]
00649:             ang = item["angle"]
00650:             base_loc = item["base_location"]
00651:             base_scale = item["base_scale"]
00652:             phase = idx * 0.55
00653: 
00654:             obj.location.x = base_loc.x + math.sin(i * 0.016 + phase) * 0.20
00655:             obj.location.y = base_loc.y + math.cos(i * 0.014 + phase) * 0.18
00656:             obj.location.z = base_loc.z + high * 0.18 + math.sin(i * 0.018 + phase) * 0.04
00657: 
00658:             sc = base_scale + low * 0.07
00659:             obj.scale = (sc, sc, sc)
00660:             obj.rotation_euler.z = ang + math.sin(i * 0.012 + phase) * math.radians(14.0)
00661: 
00662:             obj.keyframe_insert(data_path="location", frame=i)
00663:             obj.keyframe_insert(data_path="scale", frame=i)
00664:             obj.keyframe_insert(data_path="rotation_euler", frame=i)
00665: 
00666:         # RINGS / RIBBONS
00667:         for item in energy_rings:
00668:             ring = item["object"]
00669:             phase = item["phase"]
00670:             base_scale = item["base_scale"]
00671:             base_rot = item["base_rot"]
00672:             base_loc = item["base_loc"]
00673: 
00674:             pulse_scale = 1.0 + low * 0.03 + pulse * 0.02
00675:             ring.scale = (
00676:                 base_scale.x * pulse_scale,
00677:                 base_scale.y * pulse_scale,
00678:                 base_scale.z * pulse_scale,
00679:             )
00680:             ring.location.z = base_loc.z + math.sin(i * 0.009 + phase) * 0.05
00681:             ring.rotation_euler.z = base_rot.z + i * 0.006 + phase
00682: 
```
