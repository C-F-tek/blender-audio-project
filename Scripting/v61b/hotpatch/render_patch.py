from render_setup import configure_render

from .common import OUTPUT_MP4, cfg_value


def normalize_runtime_profile(profile):
    profile = str(profile or "PREVIEW").upper().replace(" ", "_").replace("-", "_")
    aliases = {
        "FINAL": "YOUTUBE_1440P",
        "YOUTUBE": "YOUTUBE_1440P",
        "YOUTUBE_FINAL": "YOUTUBE_1440P",
        "YOUTUBE_FINAL_1440P": "YOUTUBE_1440P",
        "YOUTUBE_FAST": "YOUTUBE_FAST_1440P",
        "YOUTUBE_FAST_1440P": "YOUTUBE_FAST_1440P",
        "YT_FAST": "YOUTUBE_FAST_1440P",
        "YT_FAST_1440": "YOUTUBE_FAST_1440P",
        "YT_FAST_1440P": "YOUTUBE_FAST_1440P",
        "YT_FINAL": "YOUTUBE_1440P",
        "YT_1440": "YOUTUBE_1440P",
        "YT_1440P": "YOUTUBE_1440P",
        "1440": "YOUTUBE_1440P",
        "1440P": "YOUTUBE_1440P",
        "YT_4K": "YOUTUBE_4K",
        "YOUTUBE_FINAL_4K": "YOUTUBE_4K",
        "YOUTUBE_FAST_4K": "YOUTUBE_FAST_4K",
        "YT_FAST_4K": "YOUTUBE_FAST_4K",
        "4K": "YOUTUBE_4K",
        "YT_1080": "YOUTUBE_1080P",
        "YT_1080P": "YOUTUBE_1080P",
        "YOUTUBE_FINAL_1080P": "YOUTUBE_1080P",
        "YOUTUBE_FAST_1080P": "YOUTUBE_FAST_1080P",
        "YT_FAST_1080": "YOUTUBE_FAST_1080P",
        "YT_FAST_1080P": "YOUTUBE_FAST_1080P",
        "1080": "YOUTUBE_1080P",
        "1080P": "YOUTUBE_1080P",
    }
    valid = {
        "PREVIEW",
        "YOUTUBE_FAST_1080P",
        "YOUTUBE_FAST_1440P",
        "YOUTUBE_FAST_4K",
        "YOUTUBE_1080P",
        "YOUTUBE_1440P",
        "YOUTUBE_4K",
    }
    return aliases.get(profile, profile if profile in valid else "PREVIEW")


def get_scene_compositor_tree(scene):
    for attr in ("node_tree", "compositor_node_tree"):
        tree = getattr(scene, attr, None)
        if tree is not None:
            return tree
    return None


def current_runtime_profile(scene):
    if "spaziotempo_runtime_profile" in scene:
        return normalize_runtime_profile(scene["spaziotempo_runtime_profile"])

    tune = getattr(scene, "spaziotempo_tuning", None)
    if tune is not None:
        label = getattr(tune, "runtime_profile", "")
        if label:
            return normalize_runtime_profile(label)
        if getattr(tune, "youtube_final", False):
            return "YOUTUBE_1440P"

    return "PREVIEW"


def apply_runtime_profile_to_scene(scene, profile):
    profile = normalize_runtime_profile(profile)
    render = scene.render

    if profile == "YOUTUBE_FAST_4K":
        width, height = 3840, 2160
        video_bitrate, video_maxrate = 40000, 45000
        motion_blur = False
        fstop = 3.8
        taa_samples = 48
        volumetric_samples = 24
        bloom_intensity = 0.020
        compositor_threshold = 1.62
        lens_distort = 0.010
        lens_dispersion = 0.012
    elif profile == "YOUTUBE_FAST_1440P":
        width, height = 2560, 1440
        video_bitrate, video_maxrate = 24000, 30000
        motion_blur = False
        fstop = 3.8
        taa_samples = 48
        volumetric_samples = 24
        bloom_intensity = 0.020
        compositor_threshold = 1.62
        lens_distort = 0.010
        lens_dispersion = 0.012
    elif profile == "YOUTUBE_FAST_1080P":
        width, height = 1920, 1080
        video_bitrate, video_maxrate = 18000, 22000
        motion_blur = False
        fstop = 3.8
        taa_samples = 48
        volumetric_samples = 24
        bloom_intensity = 0.020
        compositor_threshold = 1.62
        lens_distort = 0.010
        lens_dispersion = 0.012
    elif profile == "YOUTUBE_4K":
        width, height = 3840, 2160
        video_bitrate, video_maxrate = 40000, 45000
        motion_blur = True
        fstop = 3.8
        taa_samples = 80
        volumetric_samples = 48
        bloom_intensity = 0.020
        compositor_threshold = 1.62
        lens_distort = 0.010
        lens_dispersion = 0.012
    elif profile == "YOUTUBE_1440P":
        width, height = 2560, 1440
        video_bitrate, video_maxrate = 24000, 30000
        motion_blur = True
        fstop = 3.8
        taa_samples = 80
        volumetric_samples = 48
        bloom_intensity = 0.020
        compositor_threshold = 1.62
        lens_distort = 0.010
        lens_dispersion = 0.012
    elif profile == "YOUTUBE_1080P":
        width, height = 1920, 1080
        video_bitrate, video_maxrate = 18000, 22000
        motion_blur = True
        fstop = 3.8
        taa_samples = 80
        volumetric_samples = 48
        bloom_intensity = 0.020
        compositor_threshold = 1.62
        lens_distort = 0.010
        lens_dispersion = 0.012
    else:
        width, height = 1920, 1080
        video_bitrate, video_maxrate = 12000, 16000
        motion_blur = False
        fstop = 6.5
        taa_samples = 48
        volumetric_samples = 32
        bloom_intensity = 0.018
        compositor_threshold = 1.48
        lens_distort = 0.0045
        lens_dispersion = 0.0052

    render.resolution_x = width
    render.resolution_y = height
    render.resolution_percentage = 100 if profile.startswith("YOUTUBE_") else 75
    render.use_motion_blur = motion_blur

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
            eevee.volumetric_tile_size = '8'
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

    scene["spaziotempo_runtime_profile"] = profile


def configure_existing_render(scene, meta):
    profile = current_runtime_profile(scene)
    fps = cfg_value("FPS_OVERRIDE", None) or meta.get("fps") or scene.render.fps or 30
    configure_render(scene, OUTPUT_MP4, fps)
    apply_runtime_profile_to_scene(scene, profile)
    return fps
