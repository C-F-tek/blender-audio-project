def apply_tuning(context, insert_keyframes=False):
    scene = context.scene
    tune = scene.spaziotempo_tuning
    frame = scene.frame_current

    hero = find_obj("HeroRoot")
    if hero is not None:
        set_scale_from_base(hero, tune.hero_scale)
        if insert_keyframes:
            hero.keyframe_insert(data_path="scale", frame=frame)

    for obj in bpy.data.objects:
        for mod in obj.modifiers:
            if mod.name == "HeroAudioMeshDisplace":
                base = store_base_float(
                    obj, f"_st_base_{mod.name}_strength", getattr(mod, "strength", 0.0)
                )
                mod.strength = base * tune.hero_deform
                if insert_keyframes:
                    keyframe_if_possible(mod, "strength", frame)
            elif mod.name == "HeroAudioFineDisplace":
                base = store_base_float(
                    obj, f"_st_base_{mod.name}_strength", getattr(mod, "strength", 0.0)
                )
                mod.strength = base * tune.hero_fine_deform
                if insert_keyframes:
                    keyframe_if_possible(mod, "strength", frame)
            elif mod.name == "HeroAudioSurfaceWave":
                try:
                    base = store_base_float(
                        obj, f"_st_base_{mod.name}_height", getattr(mod, "height", 0.0)
                    )
                    mod.height = base * tune.hero_wave
                    if insert_keyframes:
                        keyframe_if_possible(mod, "height", frame)
                except Exception:
                    pass
            elif mod.name == "HeroAudioTwistDeform":
                try:
                    base = store_base_float(
                        obj, f"_st_base_{mod.name}_angle", getattr(mod, "angle", 0.0)
                    )
                    mod.angle = base * tune.hero_twist
                    if insert_keyframes:
                        keyframe_if_possible(mod, "angle", frame)
                except Exception:
                    pass
            elif mod.name in {"AuraAudioBreathDisplace", "AuraAudioTransientDetail"}:
                base = store_base_float(
                    obj, f"_st_base_{mod.name}_strength", getattr(mod, "strength", 0.0)
                )
                mod.strength = base * tune.aura_deform
                if insert_keyframes:
                    keyframe_if_possible(mod, "strength", frame)

    for mat in bpy.data.materials:
        if mat is None or not mat.use_nodes:
            continue

        nodes = mat.node_tree.nodes
        for node_name, factor, key, min_value, max_value in [
            (
                "HeroMatEmissionValue",
                tune.hero_mat_emission,
                "_st_base_hero_mat_emission",
                0.0,
                3.0,
            ),
            (
                "HeroMatSelfLightValue",
                tune.hero_mat_emission,
                "_st_base_hero_mat_self_light",
                0.0,
                1.0,
            ),
            ("HeroMatBumpStrength", tune.hero_mat_bump, "_st_base_hero_mat_bump", 0.0, 0.25),
            (
                "HeroMatRoughnessValue",
                tune.hero_mat_roughness,
                "_st_base_hero_mat_roughness",
                0.02,
                1.0,
            ),
        ]:
            node = nodes.get(node_name)
            if node is None:
                continue
            base = store_base_float(node, key, node.outputs[0].default_value)
            node.outputs[0].default_value = clamp_value(base * factor, min_value, max_value)
            if insert_keyframes:
                keyframe_socket(node.outputs[0], frame)

        noise = nodes.get("HeroMatAudioNoise")
        if noise is not None and "Scale" in noise.inputs:
            base = store_base_float(
                noise, "_st_base_hero_mat_noise", noise.inputs["Scale"].default_value
            )
            noise.inputs["Scale"].default_value = clamp_value(
                base * tune.hero_mat_noise, 0.10, 80.0
            )
            if insert_keyframes:
                keyframe_socket(noise.inputs["Scale"], frame)

    aura_sampler = find_obj("AuraAudioSampler")
    if aura_sampler is not None:
        for prop_name, value in [
            ("aura_deform", tune.aura_deform),
            ("detail", tune.aura_detail),
            ("pulse", tune.aura_pulse),
        ]:
            aura_sampler[prop_name] = value
            if insert_keyframes:
                keyframe_if_possible(aura_sampler, f'["{prop_name}"]', frame)

    fog = find_obj("AtmosphereCube")
    if fog is not None:
        base = store_base_vector(fog, "_st_base_fog_scale", fog.scale)
        fog.scale = (
            base[0] * tune.fog_scale_xy,
            base[1] * tune.fog_scale_xy,
            base[2] * tune.fog_scale_z,
        )
        fog.hide_viewport = not tune.show_fog_cube
        if insert_keyframes:
            fog.keyframe_insert(data_path="scale", frame=frame)

    fog_density = set_value_node("AtmosphereVolumeMaterial", "FogDensityValue", tune.fog_density)
    fog_emission = set_value_node("AtmosphereVolumeMaterial", "FogEmissionValue", tune.fog_emission)
    fog_noise = set_input_node(
        "AtmosphereVolumeMaterial", "Noise Texture", "Scale", tune.fog_noise_scale
    )
    if insert_keyframes:
        keyframe_socket(fog_density, frame)
        keyframe_socket(fog_emission, frame)
        keyframe_socket(fog_noise, frame)

    backdrop = find_obj("SoftRhythmBackdrop")
    if backdrop is not None:
        set_scale_from_base(backdrop, tune.backdrop_scale, "_st_base_backdrop_scale")
        backdrop.hide_viewport = not tune.show_backdrop
        backdrop.hide_render = not tune.render_backdrop
        if insert_keyframes:
            backdrop.keyframe_insert(data_path="scale", frame=frame)

    backdrop_emission = set_input_node(
        "SoftBackdropMaterial",
        "BackdropEmission",
        "Strength",
        tune.backdrop_emission,
    )
    backdrop_noise = set_input_node(
        "SoftBackdropMaterial",
        "Noise Texture",
        "Scale",
        tune.backdrop_noise_scale,
    )
    if insert_keyframes:
        keyframe_socket(backdrop_emission, frame)
        keyframe_socket(backdrop_noise, frame)

    floor = find_obj("PeaceFloor")
    if floor is not None:
        set_scale_from_base(floor, tune.floor_scale, "_st_base_floor_scale")
        floor.hide_viewport = not tune.show_floor
        floor.hide_render = not tune.render_floor
        if insert_keyframes:
            floor.keyframe_insert(data_path="scale", frame=frame)

    camera = scene.camera
    if camera is not None:
        try:
            camera.data.dof.aperture_fstop = tune.camera_fstop
            if insert_keyframes:
                keyframe_if_possible(camera.data.dof, "aperture_fstop", frame)
        except Exception:
            pass
    scene.render.use_motion_blur = tune.motion_blur

    for accent in objects_with_prefix("PhysicsAccent_"):
        mat = getattr(accent, "active_material", None)
        if mat is not None and mat.use_nodes:
            node = mat.node_tree.nodes.get("VariantEmission")
            if node is not None and "Strength" in node.inputs:
                socket = node.inputs["Strength"]
                base_emit = store_base_float(
                    node, "_st_base_physics_accent_emit", socket.default_value
                )
                socket.default_value = max(0.0, base_emit * tune.rhythm_light_power)
                if insert_keyframes:
                    keyframe_socket(socket, frame)

            mix_node = mat.node_tree.nodes.get("VariantEmissionMix")
            if mix_node is not None:
                socket = mix_node.outputs[0]
                base_mix = store_base_float(
                    mix_node, "_st_base_physics_accent_mix", socket.default_value
                )
                socket.default_value = max(0.0, min(1.0, base_mix * tune.rhythm_light_power))
                if insert_keyframes:
                    keyframe_socket(socket, frame)

    compositor_tree = get_scene_compositor_tree(scene)
    if compositor_tree is not None:
        glare = compositor_tree.nodes.get("AudioSoftGlare")
        if glare is not None and hasattr(glare, "threshold"):
            base = store_base_float(glare, "_st_base_glare_threshold", glare.threshold)
            glare.threshold = clamp_value(base / max(0.10, tune.compositor_glow), 0.20, 6.0)
            if insert_keyframes:
                keyframe_if_possible(glare, "threshold", frame)

        lens = compositor_tree.nodes.get("AudioLensBreath")
        if lens is not None:
            for input_name, key in [
                ("Distort", "_st_base_lens_distort"),
                ("Dispersion", "_st_base_lens_dispersion"),
            ]:
                if input_name not in lens.inputs:
                    continue
                socket = lens.inputs[input_name]
                base = store_base_float(lens, key, socket.default_value)
                socket.default_value = clamp_value(base * tune.compositor_lens, 0.0, 0.08)
                if insert_keyframes:
                    keyframe_socket(socket, frame)

    for emitter in particle_emitters():
        emitter.hide_viewport = not tune.show_emitters

    for source in particle_source_objects():
        source.hide_viewport = not tune.show_particle_sources

    for ps_settings in all_particle_settings():
        base_size = store_base_float(
            ps_settings, "_st_base_particle_size", ps_settings.particle_size
        )
        ps_settings.particle_size = base_size * tune.particle_size

        for attr in ["normal_factor", "tangent_factor", "brownian_factor"]:
            if not hasattr(ps_settings, attr):
                continue
            base = store_base_float(ps_settings, f"_st_base_{attr}", getattr(ps_settings, attr))
            setattr(ps_settings, attr, base * tune.particle_force)

        if insert_keyframes:
            keyframe_if_possible(ps_settings, "particle_size", frame)
            keyframe_if_possible(ps_settings, "normal_factor", frame)
            keyframe_if_possible(ps_settings, "tangent_factor", frame)
            keyframe_if_possible(ps_settings, "brownian_factor", frame)

    letter_root = find_obj("AlbumLetterParticleSources")
    if letter_root is not None:
        set_scale_from_base(letter_root, tune.letter_source_scale, "_st_base_letter_root_scale")
        if insert_keyframes:
            letter_root.keyframe_insert(data_path="scale", frame=frame)


def scale_fcurve_values(idblock, predicate, factor):
    anim = getattr(idblock, "animation_data", None)
    action = getattr(anim, "action", None) if anim else None
    changed = 0

    for fcurve in iter_action_fcurves(action):
        if not predicate(fcurve):
            continue
        for key in getattr(fcurve, "keyframe_points", []):
            key.co.y *= factor
            key.handle_left.y *= factor
            key.handle_right.y *= factor
            changed += 1
    return changed


def scale_full_animation(context):
    tune = context.scene.spaziotempo_tuning
    changed = 0

    for obj in bpy.data.objects:
        changed += scale_fcurve_values(
            obj,
            lambda fc: (
                ("HeroAudioMeshDisplace" in fc.data_path and "strength" in fc.data_path)
                or ("HeroAudioFineDisplace" in fc.data_path and "strength" in fc.data_path)
                or ("HeroAudioSurfaceWave" in fc.data_path and "height" in fc.data_path)
                or ("HeroAudioTwistDeform" in fc.data_path and "angle" in fc.data_path)
            ),
            tune.anim_hero_deform_factor,
        )
        changed += scale_fcurve_values(
            obj,
            lambda fc: fc.data_path in {'["aura_deform"]', '["detail"]', '["pulse"]'},
            tune.anim_aura_factor,
        )

    for ps_settings in all_particle_settings():
        changed += scale_fcurve_values(
            ps_settings,
            lambda fc: fc.data_path == "particle_size",
            tune.anim_particle_size_factor,
        )
        changed += scale_fcurve_values(
            ps_settings,
            lambda fc: fc.data_path in {"normal_factor", "tangent_factor", "brownian_factor"},
            tune.anim_particle_force_factor,
        )

    return changed


def preset_data(settings):
    return {
        "hero_scale": settings.hero_scale,
        "hero_deform": settings.hero_deform,
        "hero_fine_deform": settings.hero_fine_deform,
        "hero_wave": settings.hero_wave,
        "hero_twist": settings.hero_twist,
        "hero_mat_emission": settings.hero_mat_emission,
        "hero_mat_bump": settings.hero_mat_bump,
        "hero_mat_roughness": settings.hero_mat_roughness,
        "hero_mat_noise": settings.hero_mat_noise,
        "aura_deform": settings.aura_deform,
        "aura_detail": settings.aura_detail,
        "aura_pulse": settings.aura_pulse,
        "fog_density": settings.fog_density,
        "fog_emission": settings.fog_emission,
        "fog_noise_scale": settings.fog_noise_scale,
        "fog_scale_xy": settings.fog_scale_xy,
        "fog_scale_z": settings.fog_scale_z,
        "backdrop_emission": settings.backdrop_emission,
        "backdrop_noise_scale": settings.backdrop_noise_scale,
        "backdrop_scale": settings.backdrop_scale,
        "floor_scale": settings.floor_scale,
        "camera_fstop": settings.camera_fstop,
        "youtube_final": settings.youtube_final,
        "runtime_profile": settings.runtime_profile,
        "motion_blur": settings.motion_blur,
        "rhythm_light_power": settings.rhythm_light_power,
        "compositor_glow": settings.compositor_glow,
        "compositor_lens": settings.compositor_lens,
        "particle_size": settings.particle_size,
        "particle_force": settings.particle_force,
        "letter_source_scale": settings.letter_source_scale,
        "show_fog_cube": settings.show_fog_cube,
        "show_backdrop": settings.show_backdrop,
        "render_backdrop": settings.render_backdrop,
        "show_floor": settings.show_floor,
        "render_floor": settings.render_floor,
        "show_emitters": settings.show_emitters,
        "show_particle_sources": settings.show_particle_sources,
    }


def load_preset_data(settings, data):
    for key, value in data.items():
        if hasattr(settings, key):
            setattr(settings, key, value)
