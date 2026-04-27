# Project Code Chunk 59/212

- File: `Scripting/v61b/scene_tuning_panel.py`
- Part: `3`
- Lines: `575-792`

## Symbol Map
- Imports: `json`, `sys`, `traceback`, `from pathlib import Path`, `bpy`, `from bpy.props import BoolProperty, FloatProperty, PointerProperty, StringProperty`
- Classes: `ST_TuningSettings` line 770; `ST_OT_apply_tuning` line 822 methods: execute; `ST_OT_keyframe_tuning` line 833 methods: execute; `ST_OT_scale_animation` line 844 methods: execute; `ST_OT_apply_runtime_profile` line 855 methods: execute; `ST_OT_hot_update_scene` line 871 methods: execute; `ST_OT_rebuild_restart_check` line 895 methods: execute; `ST_OT_optimizer_check` line 920 methods: execute; `ST_OT_load_image_sequence` line 943 methods: execute; `ST_OT_encode_ffmpeg` line 965 methods: execute; `ST_OT_encode_ffmpeg_shell` line 987 methods: execute; `ST_OT_save_preset` line 1016 methods: execute; `ST_OT_load_preset` line 1027 methods: execute; `ST_OT_open_guide_text` line 1043 methods: execute; `ST_OT_select_group` line 1062 methods: execute; `ST_PT_tuning_panel` line 1098 methods: draw
- Functions: `resolve_script_dir()` line 20; `iter_action_fcurves(action)` line 56; `find_obj(name)` line 88; `objects_with_prefix(prefix)` line 92; `particle_emitters()` line 96; `particle_source_objects()` line 106; `store_base_vector(obj, key, value)` line 117; `store_base_float(idblock, key, value)` line 123; `set_scale_from_base(obj, factor, key)` line 132; `keyframe_if_possible(idblock, data_path, frame)` line 140; `find_material(name)` line 147; `find_node(material_name, node_name)` line 151; `set_value_node(material_name, node_name, value)` line 158; `set_input_node(material_name, node_name, input_name, value)` line 169; `keyframe_socket(socket, frame)` line 180; `get_scene_compositor_tree(scene)` line 186; `clamp_value(value, min_value, max_value)` line 194; `normalize_runtime_profile(profile)` line 198; `runtime_profile_label(profile)` line 244; `apply_runtime_profile(context, profile)` line 257; `all_particle_settings()` line 442; `apply_tuning(context, insert_keyframes)` line 454; `scale_fcurve_values(idblock, predicate, factor)` line 669; `scale_full_animation(context)` line 685; `preset_data(settings)` line 721; `load_preset_data(settings, data)` line 764; `register()` line 1239; `unregister()` line 1254
- Assignments: `bl_info`, `SCRIPT_DIR`, `PRESET_PATH`, `GUIDE_PATH`, `HOT_UPDATE_PATH`, `ENCODE_SEQUENCE_PATH`, `ENCODE_FFMPEG_PATH`, `classes`

## Content
```py
00575:     )
00576:     if insert_keyframes:
00577:         keyframe_socket(backdrop_emission, frame)
00578:         keyframe_socket(backdrop_noise, frame)
00579: 
00580:     floor = find_obj("PeaceFloor")
00581:     if floor is not None:
00582:         set_scale_from_base(floor, tune.floor_scale, "_st_base_floor_scale")
00583:         floor.hide_viewport = not tune.show_floor
00584:         floor.hide_render = not tune.render_floor
00585:         if insert_keyframes:
00586:             floor.keyframe_insert(data_path="scale", frame=frame)
00587: 
00588:     camera = scene.camera
00589:     if camera is not None:
00590:         try:
00591:             camera.data.dof.aperture_fstop = tune.camera_fstop
00592:             if insert_keyframes:
00593:                 keyframe_if_possible(camera.data.dof, "aperture_fstop", frame)
00594:         except Exception:
00595:             pass
00596:     scene.render.use_motion_blur = tune.motion_blur
00597: 
00598:     for accent in objects_with_prefix("PhysicsAccent_"):
00599:         mat = getattr(accent, "active_material", None)
00600:         if mat is not None and mat.use_nodes:
00601:             node = mat.node_tree.nodes.get("VariantEmission")
00602:             if node is not None and "Strength" in node.inputs:
00603:                 socket = node.inputs["Strength"]
00604:                 base_emit = store_base_float(node, "_st_base_physics_accent_emit", socket.default_value)
00605:                 socket.default_value = max(0.0, base_emit * tune.rhythm_light_power)
00606:                 if insert_keyframes:
00607:                     keyframe_socket(socket, frame)
00608: 
00609:             mix_node = mat.node_tree.nodes.get("VariantEmissionMix")
00610:             if mix_node is not None:
00611:                 socket = mix_node.outputs[0]
00612:                 base_mix = store_base_float(mix_node, "_st_base_physics_accent_mix", socket.default_value)
00613:                 socket.default_value = max(0.0, min(1.0, base_mix * tune.rhythm_light_power))
00614:                 if insert_keyframes:
00615:                     keyframe_socket(socket, frame)
00616: 
00617:     compositor_tree = get_scene_compositor_tree(scene)
00618:     if compositor_tree is not None:
00619:         glare = compositor_tree.nodes.get("AudioSoftGlare")
00620:         if glare is not None and hasattr(glare, "threshold"):
00621:             base = store_base_float(glare, "_st_base_glare_threshold", glare.threshold)
00622:             glare.threshold = clamp_value(base / max(0.10, tune.compositor_glow), 0.20, 6.0)
00623:             if insert_keyframes:
00624:                 keyframe_if_possible(glare, "threshold", frame)
00625: 
00626:         lens = compositor_tree.nodes.get("AudioLensBreath")
00627:         if lens is not None:
00628:             for input_name, key in [
00629:                 ("Distort", "_st_base_lens_distort"),
00630:                 ("Dispersion", "_st_base_lens_dispersion"),
00631:             ]:
00632:                 if input_name not in lens.inputs:
00633:                     continue
00634:                 socket = lens.inputs[input_name]
00635:                 base = store_base_float(lens, key, socket.default_value)
00636:                 socket.default_value = clamp_value(base * tune.compositor_lens, 0.0, 0.08)
00637:                 if insert_keyframes:
00638:                     keyframe_socket(socket, frame)
00639: 
00640:     for emitter in particle_emitters():
00641:         emitter.hide_viewport = not tune.show_emitters
00642: 
00643:     for source in particle_source_objects():
00644:         source.hide_viewport = not tune.show_particle_sources
00645: 
00646:     for ps_settings in all_particle_settings():
00647:         base_size = store_base_float(ps_settings, "_st_base_particle_size", ps_settings.particle_size)
00648:         ps_settings.particle_size = base_size * tune.particle_size
00649: 
00650:         for attr in ["normal_factor", "tangent_factor", "brownian_factor"]:
00651:             if not hasattr(ps_settings, attr):
00652:                 continue
00653:             base = store_base_float(ps_settings, f"_st_base_{attr}", getattr(ps_settings, attr))
00654:             setattr(ps_settings, attr, base * tune.particle_force)
00655: 
00656:         if insert_keyframes:
00657:             keyframe_if_possible(ps_settings, "particle_size", frame)
00658:             keyframe_if_possible(ps_settings, "normal_factor", frame)
00659:             keyframe_if_possible(ps_settings, "tangent_factor", frame)
00660:             keyframe_if_possible(ps_settings, "brownian_factor", frame)
00661: 
00662:     letter_root = find_obj("AlbumLetterParticleSources")
00663:     if letter_root is not None:
00664:         set_scale_from_base(letter_root, tune.letter_source_scale, "_st_base_letter_root_scale")
00665:         if insert_keyframes:
00666:             letter_root.keyframe_insert(data_path="scale", frame=frame)
00667: 
00668: 
00669: def scale_fcurve_values(idblock, predicate, factor):
00670:     anim = getattr(idblock, "animation_data", None)
00671:     action = getattr(anim, "action", None) if anim else None
00672:     changed = 0
00673: 
00674:     for fcurve in iter_action_fcurves(action):
00675:         if not predicate(fcurve):
00676:             continue
00677:         for key in getattr(fcurve, "keyframe_points", []):
00678:             key.co.y *= factor
00679:             key.handle_left.y *= factor
00680:             key.handle_right.y *= factor
00681:             changed += 1
00682:     return changed
00683: 
00684: 
00685: def scale_full_animation(context):
00686:     tune = context.scene.spaziotempo_tuning
00687:     changed = 0
00688: 
00689:     for obj in bpy.data.objects:
00690:         changed += scale_fcurve_values(
00691:             obj,
00692:             lambda fc: (
00693:                 ("HeroAudioMeshDisplace" in fc.data_path and "strength" in fc.data_path)
00694:                 or ("HeroAudioFineDisplace" in fc.data_path and "strength" in fc.data_path)
00695:                 or ("HeroAudioSurfaceWave" in fc.data_path and "height" in fc.data_path)
00696:                 or ("HeroAudioTwistDeform" in fc.data_path and "angle" in fc.data_path)
00697:             ),
00698:             tune.anim_hero_deform_factor,
00699:         )
00700:         changed += scale_fcurve_values(
00701:             obj,
00702:             lambda fc: fc.data_path in {'["aura_deform"]', '["detail"]', '["pulse"]'},
00703:             tune.anim_aura_factor,
00704:         )
00705: 
00706:     for ps_settings in all_particle_settings():
00707:         changed += scale_fcurve_values(
00708:             ps_settings,
00709:             lambda fc: fc.data_path == "particle_size",
00710:             tune.anim_particle_size_factor,
00711:         )
00712:         changed += scale_fcurve_values(
00713:             ps_settings,
00714:             lambda fc: fc.data_path in {"normal_factor", "tangent_factor", "brownian_factor"},
00715:             tune.anim_particle_force_factor,
00716:         )
00717: 
00718:     return changed
00719: 
00720: 
00721: def preset_data(settings):
00722:     return {
00723:         "hero_scale": settings.hero_scale,
00724:         "hero_deform": settings.hero_deform,
00725:         "hero_fine_deform": settings.hero_fine_deform,
00726:         "hero_wave": settings.hero_wave,
00727:         "hero_twist": settings.hero_twist,
00728:         "hero_mat_emission": settings.hero_mat_emission,
00729:         "hero_mat_bump": settings.hero_mat_bump,
00730:         "hero_mat_roughness": settings.hero_mat_roughness,
00731:         "hero_mat_noise": settings.hero_mat_noise,
00732:         "aura_deform": settings.aura_deform,
00733:         "aura_detail": settings.aura_detail,
00734:         "aura_pulse": settings.aura_pulse,
00735:         "fog_density": settings.fog_density,
00736:         "fog_emission": settings.fog_emission,
00737:         "fog_noise_scale": settings.fog_noise_scale,
00738:         "fog_scale_xy": settings.fog_scale_xy,
00739:         "fog_scale_z": settings.fog_scale_z,
00740:         "backdrop_emission": settings.backdrop_emission,
00741:         "backdrop_noise_scale": settings.backdrop_noise_scale,
00742:         "backdrop_scale": settings.backdrop_scale,
00743:         "floor_scale": settings.floor_scale,
00744:         "camera_fstop": settings.camera_fstop,
00745:         "youtube_final": settings.youtube_final,
00746:         "runtime_profile": settings.runtime_profile,
00747:         "motion_blur": settings.motion_blur,
00748:         "rhythm_light_power": settings.rhythm_light_power,
00749:         "compositor_glow": settings.compositor_glow,
00750:         "compositor_lens": settings.compositor_lens,
00751:         "particle_size": settings.particle_size,
00752:         "particle_force": settings.particle_force,
00753:         "letter_source_scale": settings.letter_source_scale,
00754:         "show_fog_cube": settings.show_fog_cube,
00755:         "show_backdrop": settings.show_backdrop,
00756:         "render_backdrop": settings.render_backdrop,
00757:         "show_floor": settings.show_floor,
00758:         "render_floor": settings.render_floor,
00759:         "show_emitters": settings.show_emitters,
00760:         "show_particle_sources": settings.show_particle_sources,
00761:     }
00762: 
00763: 
00764: def load_preset_data(settings, data):
00765:     for key, value in data.items():
00766:         if hasattr(settings, key):
00767:             setattr(settings, key, value)
00768: 
00769: 
00770: class ST_TuningSettings(bpy.types.PropertyGroup):
00771:     hero_scale: FloatProperty(name="Hero scale", default=1.0, min=0.20, max=3.0, precision=3)
00772:     hero_deform: FloatProperty(name="Hero deform", default=1.0, min=0.0, max=4.0, precision=3)
00773:     hero_fine_deform: FloatProperty(name="Hero fine", default=1.0, min=0.0, max=4.0, precision=3)
00774:     hero_wave: FloatProperty(name="Hero wave", default=1.0, min=0.0, max=4.0, precision=3)
00775:     hero_twist: FloatProperty(name="Hero twist", default=1.0, min=0.0, max=4.0, precision=3)
00776:     hero_mat_emission: FloatProperty(name="Hero material light", default=1.0, min=0.0, max=4.0, precision=3)
00777:     hero_mat_bump: FloatProperty(name="Hero material bump", default=1.0, min=0.0, max=4.0, precision=3)
00778:     hero_mat_roughness: FloatProperty(name="Hero material rough", default=1.0, min=0.10, max=2.0, precision=3)
00779:     hero_mat_noise: FloatProperty(name="Hero material noise", default=1.0, min=0.10, max=4.0, precision=3)
00780: 
00781:     aura_deform: FloatProperty(name="Aura deform", default=0.45, min=0.0, max=1.0, precision=3)
00782:     aura_detail: FloatProperty(name="Aura detail", default=0.35, min=0.0, max=1.0, precision=3)
00783:     aura_pulse: FloatProperty(name="Aura pulse", default=0.35, min=0.0, max=1.0, precision=3)
00784: 
00785:     fog_density: FloatProperty(name="Fog density", default=0.035, min=0.0, max=0.55, precision=4)
00786:     fog_emission: FloatProperty(name="Fog emission", default=0.004, min=0.0, max=0.12, precision=4)
00787:     fog_noise_scale: FloatProperty(name="Fog noise", default=0.9, min=0.10, max=12.0, precision=3)
00788:     fog_scale_xy: FloatProperty(name="Fog XY", default=1.0, min=0.20, max=2.20, precision=3)
00789:     fog_scale_z: FloatProperty(name="Fog Z", default=1.0, min=0.20, max=2.40, precision=3)
00790: 
00791:     backdrop_emission: FloatProperty(name="Backdrop light", default=0.175, min=0.0, max=0.80, precision=4)
00792:     backdrop_noise_scale: FloatProperty(name="Backdrop noise", default=2.4, min=0.10, max=12.0, precision=3)
```
