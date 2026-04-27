# Project Code Chunk 107/212

- File: `Scripting/v61b_backgood/scene_tuning_panel.py`
- Part: `2`
- Lines: `324-575`

## Symbol Map
- Imports: `json`, `traceback`, `from pathlib import Path`, `bpy`, `from bpy.props import BoolProperty, FloatProperty, PointerProperty, StringProperty`
- Classes: `ST_TuningSettings` line 754; `ST_OT_apply_tuning` line 806 methods: execute; `ST_OT_keyframe_tuning` line 817 methods: execute; `ST_OT_scale_animation` line 828 methods: execute; `ST_OT_apply_runtime_profile` line 839 methods: execute; `ST_OT_hot_update_scene` line 855 methods: execute; `ST_OT_save_preset` line 877 methods: execute; `ST_OT_load_preset` line 888 methods: execute; `ST_OT_open_guide_text` line 904 methods: execute; `ST_OT_select_group` line 923 methods: execute; `ST_PT_tuning_panel` line 958 methods: draw
- Functions: `resolve_script_dir()` line 19; `iter_action_fcurves(action)` line 50; `find_obj(name)` line 82; `objects_with_prefix(prefix)` line 86; `particle_emitters()` line 90; `particle_source_objects()` line 100; `store_base_vector(obj, key, value)` line 111; `store_base_float(idblock, key, value)` line 117; `set_scale_from_base(obj, factor, key)` line 126; `keyframe_if_possible(idblock, data_path, frame)` line 134; `find_material(name)` line 141; `find_node(material_name, node_name)` line 145; `set_value_node(material_name, node_name, value)` line 152; `set_input_node(material_name, node_name, input_name, value)` line 163; `keyframe_socket(socket, frame)` line 174; `get_scene_compositor_tree(scene)` line 180; `clamp_value(value, min_value, max_value)` line 188; `normalize_runtime_profile(profile)` line 192; `runtime_profile_label(profile)` line 238; `apply_runtime_profile(context, profile)` line 251; `all_particle_settings()` line 426; `apply_tuning(context, insert_keyframes)` line 438; `scale_fcurve_values(idblock, predicate, factor)` line 653; `scale_full_animation(context)` line 669; `preset_data(settings)` line 705; `load_preset_data(settings, data)` line 748; `register()` line 1074; `unregister()` line 1089
- Assignments: `bl_info`, `SCRIPT_DIR`, `PRESET_PATH`, `GUIDE_PATH`, `HOT_UPDATE_PATH`, `classes`

## Content
```py
00324:         render.resolution_percentage = 100
00325:         render.use_motion_blur = True
00326:         fstop = 3.8
00327:         taa_samples = 96
00328:         volumetric_samples = 64
00329:         video_bitrate = 24000
00330:         video_maxrate = 30000
00331:         bloom_intensity = 0.020
00332:         compositor_threshold = 1.62
00333:         compositor_lens = 1.0
00334:         lens_distort = 0.010
00335:         lens_dispersion = 0.012
00336:         rhythm_light_power = 1.0
00337:     elif profile == "YOUTUBE_1080P":
00338:         render.resolution_x = 1920
00339:         render.resolution_y = 1080
00340:         render.resolution_percentage = 100
00341:         render.use_motion_blur = True
00342:         fstop = 3.8
00343:         taa_samples = 96
00344:         volumetric_samples = 64
00345:         video_bitrate = 18000
00346:         video_maxrate = 22000
00347:         bloom_intensity = 0.020
00348:         compositor_threshold = 1.62
00349:         compositor_lens = 1.0
00350:         lens_distort = 0.010
00351:         lens_dispersion = 0.012
00352:         rhythm_light_power = 1.0
00353:     else:
00354:         render.resolution_x = 1920
00355:         render.resolution_y = 1080
00356:         render.resolution_percentage = 75
00357:         render.use_motion_blur = False
00358:         fstop = 6.5
00359:         taa_samples = 48
00360:         volumetric_samples = 32
00361:         video_bitrate = 12000
00362:         video_maxrate = 16000
00363:         bloom_intensity = 0.018
00364:         compositor_threshold = 1.48
00365:         compositor_lens = 0.75
00366:         lens_distort = 0.0045
00367:         lens_dispersion = 0.0052
00368:         rhythm_light_power = 0.85
00369: 
00370:     try:
00371:         scene.camera.data.dof.aperture_fstop = fstop
00372:     except Exception:
00373:         pass
00374: 
00375:     eevee = getattr(scene, "eevee", None)
00376:     if eevee is not None:
00377:         if hasattr(eevee, "taa_render_samples"):
00378:             eevee.taa_render_samples = taa_samples
00379:         if hasattr(eevee, "volumetric_samples"):
00380:             eevee.volumetric_samples = volumetric_samples
00381:         if hasattr(eevee, "volumetric_tile_size"):
00382:             eevee.volumetric_tile_size = '8'
00383:         if hasattr(eevee, "use_bloom"):
00384:             eevee.use_bloom = True
00385:         if hasattr(eevee, "bloom_intensity"):
00386:             eevee.bloom_intensity = bloom_intensity
00387: 
00388:     try:
00389:         render.ffmpeg.video_bitrate = video_bitrate
00390:         render.ffmpeg.maxrate = video_maxrate
00391:         render.ffmpeg.minrate = 0
00392:         render.ffmpeg.buffersize = 1792
00393:         render.ffmpeg.audio_bitrate = 320
00394:     except Exception:
00395:         pass
00396: 
00397:     try:
00398:         scene.view_settings.exposure = -0.06
00399:         scene.view_settings.gamma = 1.0
00400:     except Exception:
00401:         pass
00402: 
00403:     compositor_tree = get_scene_compositor_tree(scene)
00404:     if compositor_tree is not None:
00405:         glare = compositor_tree.nodes.get("AudioSoftGlare")
00406:         if glare is not None and hasattr(glare, "threshold"):
00407:             glare.threshold = compositor_threshold
00408:         lens = compositor_tree.nodes.get("AudioLensBreath")
00409:         if lens is not None:
00410:             if "Distort" in lens.inputs:
00411:                 lens.inputs["Distort"].default_value = lens_distort
00412:             if "Dispersion" in lens.inputs:
00413:                 lens.inputs["Dispersion"].default_value = lens_dispersion
00414: 
00415:     tune = scene.spaziotempo_tuning
00416:     tune.youtube_final = final_for_youtube
00417:     tune.runtime_profile = runtime_profile_label(profile)
00418:     scene["spaziotempo_runtime_profile"] = profile
00419:     tune.motion_blur = render.use_motion_blur
00420:     tune.camera_fstop = fstop
00421:     tune.rhythm_light_power = rhythm_light_power
00422:     tune.compositor_glow = 1.0
00423:     tune.compositor_lens = compositor_lens
00424: 
00425: 
00426: def all_particle_settings():
00427:     settings = []
00428:     for emitter in particle_emitters():
00429:         for mod in emitter.modifiers:
00430:             if mod.type != 'PARTICLE_SYSTEM':
00431:                 continue
00432:             ps = getattr(mod, "particle_system", None)
00433:             if ps is not None and ps.settings is not None:
00434:                 settings.append(ps.settings)
00435:     return settings
00436: 
00437: 
00438: def apply_tuning(context, insert_keyframes=False):
00439:     scene = context.scene
00440:     tune = scene.spaziotempo_tuning
00441:     frame = scene.frame_current
00442: 
00443:     hero = find_obj("HeroRoot")
00444:     if hero is not None:
00445:         set_scale_from_base(hero, tune.hero_scale)
00446:         if insert_keyframes:
00447:             hero.keyframe_insert(data_path="scale", frame=frame)
00448: 
00449:     for obj in bpy.data.objects:
00450:         for mod in obj.modifiers:
00451:             if mod.name == "HeroAudioMeshDisplace":
00452:                 base = store_base_float(obj, f"_st_base_{mod.name}_strength", getattr(mod, "strength", 0.0))
00453:                 mod.strength = base * tune.hero_deform
00454:                 if insert_keyframes:
00455:                     keyframe_if_possible(mod, "strength", frame)
00456:             elif mod.name == "HeroAudioFineDisplace":
00457:                 base = store_base_float(obj, f"_st_base_{mod.name}_strength", getattr(mod, "strength", 0.0))
00458:                 mod.strength = base * tune.hero_fine_deform
00459:                 if insert_keyframes:
00460:                     keyframe_if_possible(mod, "strength", frame)
00461:             elif mod.name == "HeroAudioSurfaceWave":
00462:                 try:
00463:                     base = store_base_float(obj, f"_st_base_{mod.name}_height", getattr(mod, "height", 0.0))
00464:                     mod.height = base * tune.hero_wave
00465:                     if insert_keyframes:
00466:                         keyframe_if_possible(mod, "height", frame)
00467:                 except Exception:
00468:                     pass
00469:             elif mod.name == "HeroAudioTwistDeform":
00470:                 try:
00471:                     base = store_base_float(obj, f"_st_base_{mod.name}_angle", getattr(mod, "angle", 0.0))
00472:                     mod.angle = base * tune.hero_twist
00473:                     if insert_keyframes:
00474:                         keyframe_if_possible(mod, "angle", frame)
00475:                 except Exception:
00476:                     pass
00477:             elif mod.name in {"AuraAudioBreathDisplace", "AuraAudioTransientDetail"}:
00478:                 base = store_base_float(obj, f"_st_base_{mod.name}_strength", getattr(mod, "strength", 0.0))
00479:                 mod.strength = base * tune.aura_deform
00480:                 if insert_keyframes:
00481:                     keyframe_if_possible(mod, "strength", frame)
00482: 
00483:     for mat in bpy.data.materials:
00484:         if mat is None or not mat.use_nodes:
00485:             continue
00486: 
00487:         nodes = mat.node_tree.nodes
00488:         for node_name, factor, key, min_value, max_value in [
00489:             ("HeroMatEmissionValue", tune.hero_mat_emission, "_st_base_hero_mat_emission", 0.0, 3.0),
00490:             ("HeroMatSelfLightValue", tune.hero_mat_emission, "_st_base_hero_mat_self_light", 0.0, 1.0),
00491:             ("HeroMatBumpStrength", tune.hero_mat_bump, "_st_base_hero_mat_bump", 0.0, 0.25),
00492:             ("HeroMatRoughnessValue", tune.hero_mat_roughness, "_st_base_hero_mat_roughness", 0.02, 1.0),
00493:         ]:
00494:             node = nodes.get(node_name)
00495:             if node is None:
00496:                 continue
00497:             base = store_base_float(node, key, node.outputs[0].default_value)
00498:             node.outputs[0].default_value = clamp_value(base * factor, min_value, max_value)
00499:             if insert_keyframes:
00500:                 keyframe_socket(node.outputs[0], frame)
00501: 
00502:         noise = nodes.get("HeroMatAudioNoise")
00503:         if noise is not None and "Scale" in noise.inputs:
00504:             base = store_base_float(noise, "_st_base_hero_mat_noise", noise.inputs["Scale"].default_value)
00505:             noise.inputs["Scale"].default_value = clamp_value(base * tune.hero_mat_noise, 0.10, 80.0)
00506:             if insert_keyframes:
00507:                 keyframe_socket(noise.inputs["Scale"], frame)
00508: 
00509:     aura_sampler = find_obj("AuraAudioSampler")
00510:     if aura_sampler is not None:
00511:         for prop_name, value in [
00512:             ("aura_deform", tune.aura_deform),
00513:             ("detail", tune.aura_detail),
00514:             ("pulse", tune.aura_pulse),
00515:         ]:
00516:             aura_sampler[prop_name] = value
00517:             if insert_keyframes:
00518:                 keyframe_if_possible(aura_sampler, f'["{prop_name}"]', frame)
00519: 
00520:     fog = find_obj("AtmosphereCube")
00521:     if fog is not None:
00522:         base = store_base_vector(fog, "_st_base_fog_scale", fog.scale)
00523:         fog.scale = (
00524:             base[0] * tune.fog_scale_xy,
00525:             base[1] * tune.fog_scale_xy,
00526:             base[2] * tune.fog_scale_z,
00527:         )
00528:         fog.hide_viewport = not tune.show_fog_cube
00529:         if insert_keyframes:
00530:             fog.keyframe_insert(data_path="scale", frame=frame)
00531: 
00532:     fog_density = set_value_node("AtmosphereVolumeMaterial", "FogDensityValue", tune.fog_density)
00533:     fog_emission = set_value_node("AtmosphereVolumeMaterial", "FogEmissionValue", tune.fog_emission)
00534:     fog_noise = set_input_node("AtmosphereVolumeMaterial", "Noise Texture", "Scale", tune.fog_noise_scale)
00535:     if insert_keyframes:
00536:         keyframe_socket(fog_density, frame)
00537:         keyframe_socket(fog_emission, frame)
00538:         keyframe_socket(fog_noise, frame)
00539: 
00540:     backdrop = find_obj("SoftRhythmBackdrop")
00541:     if backdrop is not None:
00542:         set_scale_from_base(backdrop, tune.backdrop_scale, "_st_base_backdrop_scale")
00543:         backdrop.hide_viewport = not tune.show_backdrop
00544:         backdrop.hide_render = not tune.render_backdrop
00545:         if insert_keyframes:
00546:             backdrop.keyframe_insert(data_path="scale", frame=frame)
00547: 
00548:     backdrop_emission = set_input_node(
00549:         "SoftBackdropMaterial",
00550:         "BackdropEmission",
00551:         "Strength",
00552:         tune.backdrop_emission,
00553:     )
00554:     backdrop_noise = set_input_node(
00555:         "SoftBackdropMaterial",
00556:         "Noise Texture",
00557:         "Scale",
00558:         tune.backdrop_noise_scale,
00559:     )
00560:     if insert_keyframes:
00561:         keyframe_socket(backdrop_emission, frame)
00562:         keyframe_socket(backdrop_noise, frame)
00563: 
00564:     floor = find_obj("PeaceFloor")
00565:     if floor is not None:
00566:         set_scale_from_base(floor, tune.floor_scale, "_st_base_floor_scale")
00567:         floor.hide_viewport = not tune.show_floor
00568:         floor.hide_render = not tune.render_floor
00569:         if insert_keyframes:
00570:             floor.keyframe_insert(data_path="scale", frame=frame)
00571: 
00572:     camera = scene.camera
00573:     if camera is not None:
00574:         try:
00575:             camera.data.dof.aperture_fstop = tune.camera_fstop
```
