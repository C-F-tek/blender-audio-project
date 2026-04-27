# Project Code Chunk 108/212

- File: `Scripting/v61b_backgood/scene_tuning_panel.py`
- Part: `3`
- Lines: `576-785`

## Symbol Map
- Imports: `json`, `traceback`, `from pathlib import Path`, `bpy`, `from bpy.props import BoolProperty, FloatProperty, PointerProperty, StringProperty`
- Classes: `ST_TuningSettings` line 754; `ST_OT_apply_tuning` line 806 methods: execute; `ST_OT_keyframe_tuning` line 817 methods: execute; `ST_OT_scale_animation` line 828 methods: execute; `ST_OT_apply_runtime_profile` line 839 methods: execute; `ST_OT_hot_update_scene` line 855 methods: execute; `ST_OT_save_preset` line 877 methods: execute; `ST_OT_load_preset` line 888 methods: execute; `ST_OT_open_guide_text` line 904 methods: execute; `ST_OT_select_group` line 923 methods: execute; `ST_PT_tuning_panel` line 958 methods: draw
- Functions: `resolve_script_dir()` line 19; `iter_action_fcurves(action)` line 50; `find_obj(name)` line 82; `objects_with_prefix(prefix)` line 86; `particle_emitters()` line 90; `particle_source_objects()` line 100; `store_base_vector(obj, key, value)` line 111; `store_base_float(idblock, key, value)` line 117; `set_scale_from_base(obj, factor, key)` line 126; `keyframe_if_possible(idblock, data_path, frame)` line 134; `find_material(name)` line 141; `find_node(material_name, node_name)` line 145; `set_value_node(material_name, node_name, value)` line 152; `set_input_node(material_name, node_name, input_name, value)` line 163; `keyframe_socket(socket, frame)` line 174; `get_scene_compositor_tree(scene)` line 180; `clamp_value(value, min_value, max_value)` line 188; `normalize_runtime_profile(profile)` line 192; `runtime_profile_label(profile)` line 238; `apply_runtime_profile(context, profile)` line 251; `all_particle_settings()` line 426; `apply_tuning(context, insert_keyframes)` line 438; `scale_fcurve_values(idblock, predicate, factor)` line 653; `scale_full_animation(context)` line 669; `preset_data(settings)` line 705; `load_preset_data(settings, data)` line 748; `register()` line 1074; `unregister()` line 1089
- Assignments: `bl_info`, `SCRIPT_DIR`, `PRESET_PATH`, `GUIDE_PATH`, `HOT_UPDATE_PATH`, `classes`

## Content
```py
00576:             if insert_keyframes:
00577:                 keyframe_if_possible(camera.data.dof, "aperture_fstop", frame)
00578:         except Exception:
00579:             pass
00580:     scene.render.use_motion_blur = tune.motion_blur
00581: 
00582:     for accent in objects_with_prefix("PhysicsAccent_"):
00583:         mat = getattr(accent, "active_material", None)
00584:         if mat is not None and mat.use_nodes:
00585:             node = mat.node_tree.nodes.get("VariantEmission")
00586:             if node is not None and "Strength" in node.inputs:
00587:                 socket = node.inputs["Strength"]
00588:                 base_emit = store_base_float(node, "_st_base_physics_accent_emit", socket.default_value)
00589:                 socket.default_value = max(0.0, base_emit * tune.rhythm_light_power)
00590:                 if insert_keyframes:
00591:                     keyframe_socket(socket, frame)
00592: 
00593:             mix_node = mat.node_tree.nodes.get("VariantEmissionMix")
00594:             if mix_node is not None:
00595:                 socket = mix_node.outputs[0]
00596:                 base_mix = store_base_float(mix_node, "_st_base_physics_accent_mix", socket.default_value)
00597:                 socket.default_value = max(0.0, min(1.0, base_mix * tune.rhythm_light_power))
00598:                 if insert_keyframes:
00599:                     keyframe_socket(socket, frame)
00600: 
00601:     compositor_tree = get_scene_compositor_tree(scene)
00602:     if compositor_tree is not None:
00603:         glare = compositor_tree.nodes.get("AudioSoftGlare")
00604:         if glare is not None and hasattr(glare, "threshold"):
00605:             base = store_base_float(glare, "_st_base_glare_threshold", glare.threshold)
00606:             glare.threshold = clamp_value(base / max(0.10, tune.compositor_glow), 0.20, 6.0)
00607:             if insert_keyframes:
00608:                 keyframe_if_possible(glare, "threshold", frame)
00609: 
00610:         lens = compositor_tree.nodes.get("AudioLensBreath")
00611:         if lens is not None:
00612:             for input_name, key in [
00613:                 ("Distort", "_st_base_lens_distort"),
00614:                 ("Dispersion", "_st_base_lens_dispersion"),
00615:             ]:
00616:                 if input_name not in lens.inputs:
00617:                     continue
00618:                 socket = lens.inputs[input_name]
00619:                 base = store_base_float(lens, key, socket.default_value)
00620:                 socket.default_value = clamp_value(base * tune.compositor_lens, 0.0, 0.08)
00621:                 if insert_keyframes:
00622:                     keyframe_socket(socket, frame)
00623: 
00624:     for emitter in particle_emitters():
00625:         emitter.hide_viewport = not tune.show_emitters
00626: 
00627:     for source in particle_source_objects():
00628:         source.hide_viewport = not tune.show_particle_sources
00629: 
00630:     for ps_settings in all_particle_settings():
00631:         base_size = store_base_float(ps_settings, "_st_base_particle_size", ps_settings.particle_size)
00632:         ps_settings.particle_size = base_size * tune.particle_size
00633: 
00634:         for attr in ["normal_factor", "tangent_factor", "brownian_factor"]:
00635:             if not hasattr(ps_settings, attr):
00636:                 continue
00637:             base = store_base_float(ps_settings, f"_st_base_{attr}", getattr(ps_settings, attr))
00638:             setattr(ps_settings, attr, base * tune.particle_force)
00639: 
00640:         if insert_keyframes:
00641:             keyframe_if_possible(ps_settings, "particle_size", frame)
00642:             keyframe_if_possible(ps_settings, "normal_factor", frame)
00643:             keyframe_if_possible(ps_settings, "tangent_factor", frame)
00644:             keyframe_if_possible(ps_settings, "brownian_factor", frame)
00645: 
00646:     letter_root = find_obj("AlbumLetterParticleSources")
00647:     if letter_root is not None:
00648:         set_scale_from_base(letter_root, tune.letter_source_scale, "_st_base_letter_root_scale")
00649:         if insert_keyframes:
00650:             letter_root.keyframe_insert(data_path="scale", frame=frame)
00651: 
00652: 
00653: def scale_fcurve_values(idblock, predicate, factor):
00654:     anim = getattr(idblock, "animation_data", None)
00655:     action = getattr(anim, "action", None) if anim else None
00656:     changed = 0
00657: 
00658:     for fcurve in iter_action_fcurves(action):
00659:         if not predicate(fcurve):
00660:             continue
00661:         for key in getattr(fcurve, "keyframe_points", []):
00662:             key.co.y *= factor
00663:             key.handle_left.y *= factor
00664:             key.handle_right.y *= factor
00665:             changed += 1
00666:     return changed
00667: 
00668: 
00669: def scale_full_animation(context):
00670:     tune = context.scene.spaziotempo_tuning
00671:     changed = 0
00672: 
00673:     for obj in bpy.data.objects:
00674:         changed += scale_fcurve_values(
00675:             obj,
00676:             lambda fc: (
00677:                 ("HeroAudioMeshDisplace" in fc.data_path and "strength" in fc.data_path)
00678:                 or ("HeroAudioFineDisplace" in fc.data_path and "strength" in fc.data_path)
00679:                 or ("HeroAudioSurfaceWave" in fc.data_path and "height" in fc.data_path)
00680:                 or ("HeroAudioTwistDeform" in fc.data_path and "angle" in fc.data_path)
00681:             ),
00682:             tune.anim_hero_deform_factor,
00683:         )
00684:         changed += scale_fcurve_values(
00685:             obj,
00686:             lambda fc: fc.data_path in {'["aura_deform"]', '["detail"]', '["pulse"]'},
00687:             tune.anim_aura_factor,
00688:         )
00689: 
00690:     for ps_settings in all_particle_settings():
00691:         changed += scale_fcurve_values(
00692:             ps_settings,
00693:             lambda fc: fc.data_path == "particle_size",
00694:             tune.anim_particle_size_factor,
00695:         )
00696:         changed += scale_fcurve_values(
00697:             ps_settings,
00698:             lambda fc: fc.data_path in {"normal_factor", "tangent_factor", "brownian_factor"},
00699:             tune.anim_particle_force_factor,
00700:         )
00701: 
00702:     return changed
00703: 
00704: 
00705: def preset_data(settings):
00706:     return {
00707:         "hero_scale": settings.hero_scale,
00708:         "hero_deform": settings.hero_deform,
00709:         "hero_fine_deform": settings.hero_fine_deform,
00710:         "hero_wave": settings.hero_wave,
00711:         "hero_twist": settings.hero_twist,
00712:         "hero_mat_emission": settings.hero_mat_emission,
00713:         "hero_mat_bump": settings.hero_mat_bump,
00714:         "hero_mat_roughness": settings.hero_mat_roughness,
00715:         "hero_mat_noise": settings.hero_mat_noise,
00716:         "aura_deform": settings.aura_deform,
00717:         "aura_detail": settings.aura_detail,
00718:         "aura_pulse": settings.aura_pulse,
00719:         "fog_density": settings.fog_density,
00720:         "fog_emission": settings.fog_emission,
00721:         "fog_noise_scale": settings.fog_noise_scale,
00722:         "fog_scale_xy": settings.fog_scale_xy,
00723:         "fog_scale_z": settings.fog_scale_z,
00724:         "backdrop_emission": settings.backdrop_emission,
00725:         "backdrop_noise_scale": settings.backdrop_noise_scale,
00726:         "backdrop_scale": settings.backdrop_scale,
00727:         "floor_scale": settings.floor_scale,
00728:         "camera_fstop": settings.camera_fstop,
00729:         "youtube_final": settings.youtube_final,
00730:         "runtime_profile": settings.runtime_profile,
00731:         "motion_blur": settings.motion_blur,
00732:         "rhythm_light_power": settings.rhythm_light_power,
00733:         "compositor_glow": settings.compositor_glow,
00734:         "compositor_lens": settings.compositor_lens,
00735:         "particle_size": settings.particle_size,
00736:         "particle_force": settings.particle_force,
00737:         "letter_source_scale": settings.letter_source_scale,
00738:         "show_fog_cube": settings.show_fog_cube,
00739:         "show_backdrop": settings.show_backdrop,
00740:         "render_backdrop": settings.render_backdrop,
00741:         "show_floor": settings.show_floor,
00742:         "render_floor": settings.render_floor,
00743:         "show_emitters": settings.show_emitters,
00744:         "show_particle_sources": settings.show_particle_sources,
00745:     }
00746: 
00747: 
00748: def load_preset_data(settings, data):
00749:     for key, value in data.items():
00750:         if hasattr(settings, key):
00751:             setattr(settings, key, value)
00752: 
00753: 
00754: class ST_TuningSettings(bpy.types.PropertyGroup):
00755:     hero_scale: FloatProperty(name="Hero scale", default=1.0, min=0.20, max=3.0, precision=3)
00756:     hero_deform: FloatProperty(name="Hero deform", default=1.0, min=0.0, max=4.0, precision=3)
00757:     hero_fine_deform: FloatProperty(name="Hero fine", default=1.0, min=0.0, max=4.0, precision=3)
00758:     hero_wave: FloatProperty(name="Hero wave", default=1.0, min=0.0, max=4.0, precision=3)
00759:     hero_twist: FloatProperty(name="Hero twist", default=1.0, min=0.0, max=4.0, precision=3)
00760:     hero_mat_emission: FloatProperty(name="Hero material light", default=1.0, min=0.0, max=4.0, precision=3)
00761:     hero_mat_bump: FloatProperty(name="Hero material bump", default=1.0, min=0.0, max=4.0, precision=3)
00762:     hero_mat_roughness: FloatProperty(name="Hero material rough", default=1.0, min=0.10, max=2.0, precision=3)
00763:     hero_mat_noise: FloatProperty(name="Hero material noise", default=1.0, min=0.10, max=4.0, precision=3)
00764: 
00765:     aura_deform: FloatProperty(name="Aura deform", default=0.45, min=0.0, max=1.0, precision=3)
00766:     aura_detail: FloatProperty(name="Aura detail", default=0.35, min=0.0, max=1.0, precision=3)
00767:     aura_pulse: FloatProperty(name="Aura pulse", default=0.35, min=0.0, max=1.0, precision=3)
00768: 
00769:     fog_density: FloatProperty(name="Fog density", default=0.180, min=0.0, max=0.55, precision=4)
00770:     fog_emission: FloatProperty(name="Fog emission", default=0.012, min=0.0, max=0.12, precision=4)
00771:     fog_noise_scale: FloatProperty(name="Fog noise", default=0.9, min=0.10, max=12.0, precision=3)
00772:     fog_scale_xy: FloatProperty(name="Fog XY", default=1.0, min=0.20, max=2.20, precision=3)
00773:     fog_scale_z: FloatProperty(name="Fog Z", default=1.0, min=0.20, max=2.40, precision=3)
00774: 
00775:     backdrop_emission: FloatProperty(name="Backdrop light", default=0.075, min=0.0, max=0.60, precision=4)
00776:     backdrop_noise_scale: FloatProperty(name="Backdrop noise", default=2.4, min=0.10, max=12.0, precision=3)
00777:     backdrop_scale: FloatProperty(name="Backdrop scale", default=1.0, min=0.20, max=2.40, precision=3)
00778:     floor_scale: FloatProperty(name="Floor scale", default=1.0, min=0.20, max=3.0, precision=3)
00779: 
00780:     camera_fstop: FloatProperty(name="Camera f-stop", default=6.5, min=1.0, max=16.0, precision=2)
00781:     rhythm_light_power: FloatProperty(name="Accent emission", default=1.0, min=0.0, max=4.0, precision=3)
00782:     compositor_glow: FloatProperty(name="Compositor glow", default=1.0, min=0.10, max=4.0, precision=3)
00783:     compositor_lens: FloatProperty(name="Compositor lens", default=1.0, min=0.0, max=4.0, precision=3)
00784: 
00785:     particle_size: FloatProperty(name="Particle size", default=1.0, min=0.05, max=5.0, precision=3)
```
