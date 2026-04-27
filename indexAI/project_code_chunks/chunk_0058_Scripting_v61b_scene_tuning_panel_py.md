# Project Code Chunk 58/212

- File: `Scripting/v61b/scene_tuning_panel.py`
- Part: `2`
- Lines: `324-574`

## Symbol Map
- Imports: `json`, `sys`, `traceback`, `from pathlib import Path`, `bpy`, `from bpy.props import BoolProperty, FloatProperty, PointerProperty, StringProperty`
- Classes: `ST_TuningSettings` line 770; `ST_OT_apply_tuning` line 822 methods: execute; `ST_OT_keyframe_tuning` line 833 methods: execute; `ST_OT_scale_animation` line 844 methods: execute; `ST_OT_apply_runtime_profile` line 855 methods: execute; `ST_OT_hot_update_scene` line 871 methods: execute; `ST_OT_rebuild_restart_check` line 895 methods: execute; `ST_OT_optimizer_check` line 920 methods: execute; `ST_OT_load_image_sequence` line 943 methods: execute; `ST_OT_encode_ffmpeg` line 965 methods: execute; `ST_OT_encode_ffmpeg_shell` line 987 methods: execute; `ST_OT_save_preset` line 1016 methods: execute; `ST_OT_load_preset` line 1027 methods: execute; `ST_OT_open_guide_text` line 1043 methods: execute; `ST_OT_select_group` line 1062 methods: execute; `ST_PT_tuning_panel` line 1098 methods: draw
- Functions: `resolve_script_dir()` line 20; `iter_action_fcurves(action)` line 56; `find_obj(name)` line 88; `objects_with_prefix(prefix)` line 92; `particle_emitters()` line 96; `particle_source_objects()` line 106; `store_base_vector(obj, key, value)` line 117; `store_base_float(idblock, key, value)` line 123; `set_scale_from_base(obj, factor, key)` line 132; `keyframe_if_possible(idblock, data_path, frame)` line 140; `find_material(name)` line 147; `find_node(material_name, node_name)` line 151; `set_value_node(material_name, node_name, value)` line 158; `set_input_node(material_name, node_name, input_name, value)` line 169; `keyframe_socket(socket, frame)` line 180; `get_scene_compositor_tree(scene)` line 186; `clamp_value(value, min_value, max_value)` line 194; `normalize_runtime_profile(profile)` line 198; `runtime_profile_label(profile)` line 244; `apply_runtime_profile(context, profile)` line 257; `all_particle_settings()` line 442; `apply_tuning(context, insert_keyframes)` line 454; `scale_fcurve_values(idblock, predicate, factor)` line 669; `scale_full_animation(context)` line 685; `preset_data(settings)` line 721; `load_preset_data(settings, data)` line 764; `register()` line 1239; `unregister()` line 1254
- Assignments: `bl_info`, `SCRIPT_DIR`, `PRESET_PATH`, `GUIDE_PATH`, `HOT_UPDATE_PATH`, `ENCODE_SEQUENCE_PATH`, `ENCODE_FFMPEG_PATH`, `classes`

## Content
```py
00324:         lens_distort = 0.010
00325:         lens_dispersion = 0.012
00326:         rhythm_light_power = 1.0
00327:     elif profile == "YOUTUBE_1440P":
00328:         render.resolution_x = 2560
00329:         render.resolution_y = 1440
00330:         render.resolution_percentage = 100
00331:         render.use_motion_blur = True
00332:         fstop = 3.8
00333:         taa_samples = 64
00334:         volumetric_samples = 24
00335:         video_bitrate = 24000
00336:         video_maxrate = 30000
00337:         bloom_intensity = 0.020
00338:         compositor_threshold = 1.62
00339:         compositor_lens = 1.0
00340:         lens_distort = 0.010
00341:         lens_dispersion = 0.012
00342:         rhythm_light_power = 1.0
00343:     elif profile == "YOUTUBE_1080P":
00344:         render.resolution_x = 1920
00345:         render.resolution_y = 1080
00346:         render.resolution_percentage = 100
00347:         render.use_motion_blur = True
00348:         fstop = 3.8
00349:         taa_samples = 64
00350:         volumetric_samples = 24
00351:         video_bitrate = 18000
00352:         video_maxrate = 22000
00353:         bloom_intensity = 0.020
00354:         compositor_threshold = 1.62
00355:         compositor_lens = 1.0
00356:         lens_distort = 0.010
00357:         lens_dispersion = 0.012
00358:         rhythm_light_power = 1.0
00359:     else:
00360:         render.resolution_x = 1920
00361:         render.resolution_y = 1080
00362:         render.resolution_percentage = 75
00363:         render.use_motion_blur = False
00364:         fstop = 6.5
00365:         taa_samples = 40
00366:         volumetric_samples = 12
00367:         video_bitrate = 12000
00368:         video_maxrate = 16000
00369:         bloom_intensity = 0.018
00370:         compositor_threshold = 1.48
00371:         compositor_lens = 0.75
00372:         lens_distort = 0.0045
00373:         lens_dispersion = 0.0052
00374:         rhythm_light_power = 0.85
00375: 
00376:     try:
00377:         scene.camera.data.dof.aperture_fstop = fstop
00378:     except Exception:
00379:         pass
00380: 
00381:     eevee = getattr(scene, "eevee", None)
00382:     if eevee is not None:
00383:         if hasattr(eevee, "taa_render_samples"):
00384:             eevee.taa_render_samples = taa_samples
00385:         if hasattr(eevee, "volumetric_samples"):
00386:             eevee.volumetric_samples = volumetric_samples
00387:         if hasattr(eevee, "volumetric_tile_size"):
00388:             eevee.volumetric_tile_size = '8'
00389:         if hasattr(eevee, "use_volumetric_lights"):
00390:             eevee.use_volumetric_lights = False
00391:         if hasattr(eevee, "use_volumetric_shadows"):
00392:             eevee.use_volumetric_shadows = False
00393:         if hasattr(eevee, "use_bloom"):
00394:             eevee.use_bloom = True
00395:         if hasattr(eevee, "bloom_intensity"):
00396:             eevee.bloom_intensity = bloom_intensity
00397: 
00398:     try:
00399:         render.ffmpeg.video_bitrate = video_bitrate
00400:         render.ffmpeg.maxrate = video_maxrate
00401:         render.ffmpeg.minrate = 0
00402:         render.ffmpeg.buffersize = 1792
00403:         render.ffmpeg.audio_bitrate = 320
00404:         for crf in ('PERC_LOSSLESS', 'HIGH'):
00405:             try:
00406:                 render.ffmpeg.constant_rate_factor = crf
00407:                 break
00408:             except Exception:
00409:                 pass
00410:     except Exception:
00411:         pass
00412: 
00413:     try:
00414:         scene.view_settings.exposure = -0.06
00415:         scene.view_settings.gamma = 1.0
00416:     except Exception:
00417:         pass
00418: 
00419:     compositor_tree = get_scene_compositor_tree(scene)
00420:     if compositor_tree is not None:
00421:         glare = compositor_tree.nodes.get("AudioSoftGlare")
00422:         if glare is not None and hasattr(glare, "threshold"):
00423:             glare.threshold = compositor_threshold
00424:         lens = compositor_tree.nodes.get("AudioLensBreath")
00425:         if lens is not None:
00426:             if "Distort" in lens.inputs:
00427:                 lens.inputs["Distort"].default_value = lens_distort
00428:             if "Dispersion" in lens.inputs:
00429:                 lens.inputs["Dispersion"].default_value = lens_dispersion
00430: 
00431:     tune = scene.spaziotempo_tuning
00432:     tune.youtube_final = final_for_youtube
00433:     tune.runtime_profile = runtime_profile_label(profile)
00434:     scene["spaziotempo_runtime_profile"] = profile
00435:     tune.motion_blur = render.use_motion_blur
00436:     tune.camera_fstop = fstop
00437:     tune.rhythm_light_power = rhythm_light_power
00438:     tune.compositor_glow = 1.0
00439:     tune.compositor_lens = compositor_lens
00440: 
00441: 
00442: def all_particle_settings():
00443:     settings = []
00444:     for emitter in particle_emitters():
00445:         for mod in emitter.modifiers:
00446:             if mod.type != 'PARTICLE_SYSTEM':
00447:                 continue
00448:             ps = getattr(mod, "particle_system", None)
00449:             if ps is not None and ps.settings is not None:
00450:                 settings.append(ps.settings)
00451:     return settings
00452: 
00453: 
00454: def apply_tuning(context, insert_keyframes=False):
00455:     scene = context.scene
00456:     tune = scene.spaziotempo_tuning
00457:     frame = scene.frame_current
00458: 
00459:     hero = find_obj("HeroRoot")
00460:     if hero is not None:
00461:         set_scale_from_base(hero, tune.hero_scale)
00462:         if insert_keyframes:
00463:             hero.keyframe_insert(data_path="scale", frame=frame)
00464: 
00465:     for obj in bpy.data.objects:
00466:         for mod in obj.modifiers:
00467:             if mod.name == "HeroAudioMeshDisplace":
00468:                 base = store_base_float(obj, f"_st_base_{mod.name}_strength", getattr(mod, "strength", 0.0))
00469:                 mod.strength = base * tune.hero_deform
00470:                 if insert_keyframes:
00471:                     keyframe_if_possible(mod, "strength", frame)
00472:             elif mod.name == "HeroAudioFineDisplace":
00473:                 base = store_base_float(obj, f"_st_base_{mod.name}_strength", getattr(mod, "strength", 0.0))
00474:                 mod.strength = base * tune.hero_fine_deform
00475:                 if insert_keyframes:
00476:                     keyframe_if_possible(mod, "strength", frame)
00477:             elif mod.name == "HeroAudioSurfaceWave":
00478:                 try:
00479:                     base = store_base_float(obj, f"_st_base_{mod.name}_height", getattr(mod, "height", 0.0))
00480:                     mod.height = base * tune.hero_wave
00481:                     if insert_keyframes:
00482:                         keyframe_if_possible(mod, "height", frame)
00483:                 except Exception:
00484:                     pass
00485:             elif mod.name == "HeroAudioTwistDeform":
00486:                 try:
00487:                     base = store_base_float(obj, f"_st_base_{mod.name}_angle", getattr(mod, "angle", 0.0))
00488:                     mod.angle = base * tune.hero_twist
00489:                     if insert_keyframes:
00490:                         keyframe_if_possible(mod, "angle", frame)
00491:                 except Exception:
00492:                     pass
00493:             elif mod.name in {"AuraAudioBreathDisplace", "AuraAudioTransientDetail"}:
00494:                 base = store_base_float(obj, f"_st_base_{mod.name}_strength", getattr(mod, "strength", 0.0))
00495:                 mod.strength = base * tune.aura_deform
00496:                 if insert_keyframes:
00497:                     keyframe_if_possible(mod, "strength", frame)
00498: 
00499:     for mat in bpy.data.materials:
00500:         if mat is None or not mat.use_nodes:
00501:             continue
00502: 
00503:         nodes = mat.node_tree.nodes
00504:         for node_name, factor, key, min_value, max_value in [
00505:             ("HeroMatEmissionValue", tune.hero_mat_emission, "_st_base_hero_mat_emission", 0.0, 3.0),
00506:             ("HeroMatSelfLightValue", tune.hero_mat_emission, "_st_base_hero_mat_self_light", 0.0, 1.0),
00507:             ("HeroMatBumpStrength", tune.hero_mat_bump, "_st_base_hero_mat_bump", 0.0, 0.25),
00508:             ("HeroMatRoughnessValue", tune.hero_mat_roughness, "_st_base_hero_mat_roughness", 0.02, 1.0),
00509:         ]:
00510:             node = nodes.get(node_name)
00511:             if node is None:
00512:                 continue
00513:             base = store_base_float(node, key, node.outputs[0].default_value)
00514:             node.outputs[0].default_value = clamp_value(base * factor, min_value, max_value)
00515:             if insert_keyframes:
00516:                 keyframe_socket(node.outputs[0], frame)
00517: 
00518:         noise = nodes.get("HeroMatAudioNoise")
00519:         if noise is not None and "Scale" in noise.inputs:
00520:             base = store_base_float(noise, "_st_base_hero_mat_noise", noise.inputs["Scale"].default_value)
00521:             noise.inputs["Scale"].default_value = clamp_value(base * tune.hero_mat_noise, 0.10, 80.0)
00522:             if insert_keyframes:
00523:                 keyframe_socket(noise.inputs["Scale"], frame)
00524: 
00525:     aura_sampler = find_obj("AuraAudioSampler")
00526:     if aura_sampler is not None:
00527:         for prop_name, value in [
00528:             ("aura_deform", tune.aura_deform),
00529:             ("detail", tune.aura_detail),
00530:             ("pulse", tune.aura_pulse),
00531:         ]:
00532:             aura_sampler[prop_name] = value
00533:             if insert_keyframes:
00534:                 keyframe_if_possible(aura_sampler, f'["{prop_name}"]', frame)
00535: 
00536:     fog = find_obj("AtmosphereCube")
00537:     if fog is not None:
00538:         base = store_base_vector(fog, "_st_base_fog_scale", fog.scale)
00539:         fog.scale = (
00540:             base[0] * tune.fog_scale_xy,
00541:             base[1] * tune.fog_scale_xy,
00542:             base[2] * tune.fog_scale_z,
00543:         )
00544:         fog.hide_viewport = not tune.show_fog_cube
00545:         if insert_keyframes:
00546:             fog.keyframe_insert(data_path="scale", frame=frame)
00547: 
00548:     fog_density = set_value_node("AtmosphereVolumeMaterial", "FogDensityValue", tune.fog_density)
00549:     fog_emission = set_value_node("AtmosphereVolumeMaterial", "FogEmissionValue", tune.fog_emission)
00550:     fog_noise = set_input_node("AtmosphereVolumeMaterial", "Noise Texture", "Scale", tune.fog_noise_scale)
00551:     if insert_keyframes:
00552:         keyframe_socket(fog_density, frame)
00553:         keyframe_socket(fog_emission, frame)
00554:         keyframe_socket(fog_noise, frame)
00555: 
00556:     backdrop = find_obj("SoftRhythmBackdrop")
00557:     if backdrop is not None:
00558:         set_scale_from_base(backdrop, tune.backdrop_scale, "_st_base_backdrop_scale")
00559:         backdrop.hide_viewport = not tune.show_backdrop
00560:         backdrop.hide_render = not tune.render_backdrop
00561:         if insert_keyframes:
00562:             backdrop.keyframe_insert(data_path="scale", frame=frame)
00563: 
00564:     backdrop_emission = set_input_node(
00565:         "SoftBackdropMaterial",
00566:         "BackdropEmission",
00567:         "Strength",
00568:         tune.backdrop_emission,
00569:     )
00570:     backdrop_noise = set_input_node(
00571:         "SoftBackdropMaterial",
00572:         "Noise Texture",
00573:         "Scale",
00574:         tune.backdrop_noise_scale,
```
