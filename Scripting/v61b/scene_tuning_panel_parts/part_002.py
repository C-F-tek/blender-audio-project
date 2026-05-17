def apply_runtime_profile(context, profile):
    scene = context.scene
    render = scene.render
    profile = normalize_runtime_profile(profile)
    final_for_youtube = profile.startswith("YOUTUBE_")

    if profile == "YOUTUBE_FAST_4K":
        render.resolution_x = 3840
        render.resolution_y = 2160
        render.resolution_percentage = 100
        render.use_motion_blur = False
        fstop = 3.8
        taa_samples = 48
        volumetric_samples = 12
        video_bitrate = 40000
        video_maxrate = 45000
        bloom_intensity = 0.020
        compositor_threshold = 1.62
        compositor_lens = 1.0
        lens_distort = 0.010
        lens_dispersion = 0.012
        rhythm_light_power = 1.0
    elif profile == "YOUTUBE_FAST_1440P":
        render.resolution_x = 2560
        render.resolution_y = 1440
        render.resolution_percentage = 100
        render.use_motion_blur = False
        fstop = 3.8
        taa_samples = 48
        volumetric_samples = 12
        video_bitrate = 24000
        video_maxrate = 30000
        bloom_intensity = 0.020
        compositor_threshold = 1.62
        compositor_lens = 1.0
        lens_distort = 0.010
        lens_dispersion = 0.012
        rhythm_light_power = 1.0
    elif profile == "YOUTUBE_FAST_1080P":
        render.resolution_x = 1920
        render.resolution_y = 1080
        render.resolution_percentage = 100
        render.use_motion_blur = False
        fstop = 3.8
        taa_samples = 48
        volumetric_samples = 12
        video_bitrate = 18000
        video_maxrate = 22000
        bloom_intensity = 0.020
        compositor_threshold = 1.62
        compositor_lens = 1.0
        lens_distort = 0.010
        lens_dispersion = 0.012
        rhythm_light_power = 1.0
    elif profile == "YOUTUBE_4K":
        render.resolution_x = 3840
        render.resolution_y = 2160
        render.resolution_percentage = 100
        render.use_motion_blur = True
        fstop = 3.8
        taa_samples = 64
        volumetric_samples = 24
        video_bitrate = 40000
        video_maxrate = 45000
        bloom_intensity = 0.020
        compositor_threshold = 1.62
        compositor_lens = 1.0
        lens_distort = 0.010
        lens_dispersion = 0.012
        rhythm_light_power = 1.0
    elif profile == "YOUTUBE_1440P":
        render.resolution_x = 2560
        render.resolution_y = 1440
        render.resolution_percentage = 100
        render.use_motion_blur = True
        fstop = 3.8
        taa_samples = 64
        volumetric_samples = 24
        video_bitrate = 24000
        video_maxrate = 30000
        bloom_intensity = 0.020
        compositor_threshold = 1.62
        compositor_lens = 1.0
        lens_distort = 0.010
        lens_dispersion = 0.012
        rhythm_light_power = 1.0
    elif profile == "YOUTUBE_1080P":
        render.resolution_x = 1920
        render.resolution_y = 1080
        render.resolution_percentage = 100
        render.use_motion_blur = True
        fstop = 3.8
        taa_samples = 64
        volumetric_samples = 24
        video_bitrate = 18000
        video_maxrate = 22000
        bloom_intensity = 0.020
        compositor_threshold = 1.62
        compositor_lens = 1.0
        lens_distort = 0.010
        lens_dispersion = 0.012
        rhythm_light_power = 1.0
    else:
        render.resolution_x = 1920
        render.resolution_y = 1080
        render.resolution_percentage = 75
        render.use_motion_blur = False
        fstop = 6.5
        taa_samples = 40
        volumetric_samples = 12
        video_bitrate = 12000
        video_maxrate = 16000
        bloom_intensity = 0.018
        compositor_threshold = 1.48
        compositor_lens = 0.75
        lens_distort = 0.0045
        lens_dispersion = 0.0052
        rhythm_light_power = 0.85

    try:
        scene.camera.data.dof.aperture_fstop = fstop
    except Exception:
        pass

    eevee = getattr(scene, "eevee", None)
    if eevee is not None:
        if hasattr(eevee, "taa_render_samples"):
            eevee.taa_render_samples = taa_samples
        if hasattr(eevee, "volumetric_samples"):
            eevee.volumetric_samples = volumetric_samples
        if hasattr(eevee, "volumetric_tile_size"):
            eevee.volumetric_tile_size = "8"
        if hasattr(eevee, "use_volumetric_lights"):
            eevee.use_volumetric_lights = False
        if hasattr(eevee, "use_volumetric_shadows"):
            eevee.use_volumetric_shadows = False
        if hasattr(eevee, "use_bloom"):
            eevee.use_bloom = True
        if hasattr(eevee, "bloom_intensity"):
            eevee.bloom_intensity = bloom_intensity

    try:
        render.ffmpeg.video_bitrate = video_bitrate
        render.ffmpeg.maxrate = video_maxrate
        render.ffmpeg.minrate = 0
        render.ffmpeg.buffersize = 1792
        render.ffmpeg.audio_bitrate = 320
        for crf in ("PERC_LOSSLESS", "HIGH"):
            try:
                render.ffmpeg.constant_rate_factor = crf
                break
            except Exception:
                pass
    except Exception:
        pass

    try:
        scene.view_settings.exposure = -0.06
        scene.view_settings.gamma = 1.0
    except Exception:
        pass

    compositor_tree = get_scene_compositor_tree(scene)
    if compositor_tree is not None:
        glare = compositor_tree.nodes.get("AudioSoftGlare")
        if glare is not None and hasattr(glare, "threshold"):
            glare.threshold = compositor_threshold
        lens = compositor_tree.nodes.get("AudioLensBreath")
        if lens is not None:
            if "Distort" in lens.inputs:
                lens.inputs["Distort"].default_value = lens_distort
            if "Dispersion" in lens.inputs:
                lens.inputs["Dispersion"].default_value = lens_dispersion

    tune = scene.spaziotempo_tuning
    tune.youtube_final = final_for_youtube
    tune.runtime_profile = runtime_profile_label(profile)
    scene["spaziotempo_runtime_profile"] = profile
    tune.motion_blur = render.use_motion_blur
    tune.camera_fstop = fstop
    tune.rhythm_light_power = rhythm_light_power
    tune.compositor_glow = 1.0
    tune.compositor_lens = compositor_lens


def all_particle_settings():
    settings = []
    for emitter in particle_emitters():
        for mod in emitter.modifiers:
            if mod.type != "PARTICLE_SYSTEM":
                continue
            ps = getattr(mod, "particle_system", None)
            if ps is not None and ps.settings is not None:
                settings.append(ps.settings)
    return settings
