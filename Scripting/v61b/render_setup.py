import bpy
from pathlib import Path

from config import (
    RENDER_RESOLUTION_X,
    RENDER_RESOLUTION_Y,
    USE_4K,
    RENDER_PERCENT,
    USE_MOTION_BLUR,
    EEVEE_TAA_RENDER_SAMPLES,
    USE_BLOOM,
    BLOOM_THRESHOLD,
    BLOOM_INTENSITY,
    VIEW_EXPOSURE,
    VIEW_GAMMA,
    VIDEO_BITRATE,
    VIDEO_MAXRATE,
    VIDEO_MINRATE,
    VIDEO_BUFFERSIZE,
    AUDIO_BITRATE,
    RENDER_OUTPUT_MODE,
    OUTPUT_IMAGE_SEQUENCE_DIR,
    OUTPUT_IMAGE_SEQUENCE_PREFIX,
    IMAGE_SEQUENCE_FORMAT,
    IMAGE_SEQUENCE_COLOR_DEPTH,
    IMAGE_SEQUENCE_COMPRESSION,
    VOLUMETRIC_SAMPLES,
    VOLUMETRIC_TILE_SIZE,
    FOG_VOLUME_ENABLED,
    USE_COMPOSITING,
    COMPOSITOR_GLARE_THRESHOLD_MAX,
    COMPOSITOR_GLARE_MIX,
    COMPOSITOR_GLARE_SIZE,
    COMPOSITOR_LENS_DISTORT_MIN,
    COMPOSITOR_LENS_DISPERSION_MIN,
)


def configure_scene_physics(scene):
    try:
        scene.use_gravity = False
    except Exception:
        pass

    if scene.rigidbody_world is None:
        bpy.ops.rigidbody.world_add()

    rbw = scene.rigidbody_world
    rbw.enabled = True

    if hasattr(rbw, "time_scale"):
        rbw.time_scale = 1.0

    if hasattr(rbw, "steps_per_second"):
        rbw.steps_per_second = 120
    elif hasattr(rbw, "substeps_per_frame"):
        rbw.substeps_per_frame = 10

    if hasattr(rbw, "solver_iterations"):
        rbw.solver_iterations = 25

    if hasattr(rbw, "point_cache") and rbw.point_cache is not None:
        rbw.point_cache.frame_start = 1
        rbw.point_cache.frame_end = scene.frame_end


def get_scene_compositor_tree(scene):
    for attr in ("node_tree", "compositor_node_tree"):
        tree = getattr(scene, attr, None)
        if tree is not None:
            return tree
    return None


def configure_compositor(scene):
    if not USE_COMPOSITING:
        return

    tree = get_scene_compositor_tree(scene)
    if tree is None:
        print("[WARN] Compositor saltato: questa build non espone un node tree compositor compatibile.")
        return

    nodes = tree.nodes
    links = tree.links

    for node in list(nodes):
        nodes.remove(node)

    render_layers = nodes.new("CompositorNodeRLayers")
    render_layers.location = (-820, 0)

    glare = nodes.new("CompositorNodeGlare")
    glare.name = "AudioSoftGlare"
    glare.label = "Audio Soft Glare"
    glare.location = (-520, 0)
    try:
        glare.glare_type = 'FOG_GLOW'
    except Exception:
        pass
    try:
        glare.quality = 'MEDIUM'
    except Exception:
        pass
    try:
        glare.threshold = COMPOSITOR_GLARE_THRESHOLD_MAX
    except Exception:
        pass
    try:
        glare.mix = COMPOSITOR_GLARE_MIX
    except Exception:
        pass
    try:
        glare.size = COMPOSITOR_GLARE_SIZE
    except Exception:
        pass

    lens = nodes.new("CompositorNodeLensdist")
    lens.name = "AudioLensBreath"
    lens.label = "Audio Lens Breath"
    lens.location = (-220, 0)
    if "Distort" in lens.inputs:
        lens.inputs["Distort"].default_value = COMPOSITOR_LENS_DISTORT_MIN
    if "Dispersion" in lens.inputs:
        lens.inputs["Dispersion"].default_value = COMPOSITOR_LENS_DISPERSION_MIN

    color_balance = nodes.new("CompositorNodeColorBalance")
    color_balance.name = "AudioColorBalance"
    color_balance.label = "Audio Color Balance"
    color_balance.location = (80, 0)
    try:
        color_balance.lift = (0.985, 0.990, 1.010)
        color_balance.gamma = (0.985, 1.000, 1.020)
        color_balance.gain = (1.035, 1.020, 0.985)
    except Exception:
        pass

    composite = nodes.new("CompositorNodeComposite")
    composite.location = (410, 70)

    viewer = nodes.new("CompositorNodeViewer")
    viewer.location = (410, -110)

    try:
        links.new(render_layers.outputs["Image"], glare.inputs["Image"])
        links.new(glare.outputs["Image"], lens.inputs["Image"])
        links.new(lens.outputs["Image"], color_balance.inputs["Image"])
        links.new(color_balance.outputs["Image"], composite.inputs["Image"])
        links.new(color_balance.outputs["Image"], viewer.inputs["Image"])
    except Exception:
        try:
            links.new(render_layers.outputs["Image"], composite.inputs["Image"])
        except Exception:
            pass


def configure_render(scene, output_mp4, fps):
    scene.render.fps = int(round(fps))
    scene.render.use_file_extension = True
    scene.render.engine = 'BLENDER_EEVEE'

    scene.render.resolution_x = RENDER_RESOLUTION_X
    scene.render.resolution_y = RENDER_RESOLUTION_Y

    scene.render.resolution_percentage = RENDER_PERCENT

    output_mode = str(RENDER_OUTPUT_MODE).upper()
    if output_mode == "IMAGE_SEQUENCE":
        frame_dir = Path(OUTPUT_IMAGE_SEQUENCE_DIR)
        frame_dir.mkdir(parents=True, exist_ok=True)
        scene.render.filepath = str(frame_dir / OUTPUT_IMAGE_SEQUENCE_PREFIX)
        scene.render.use_overwrite = False
        try:
            scene.render.use_placeholder = True
        except Exception:
            pass
        scene.render.use_sequencer = False

        try:
            scene.render.image_settings.media_type = 'IMAGE'
        except Exception:
            pass
        try:
            scene.render.image_settings.file_format = IMAGE_SEQUENCE_FORMAT
            scene.render.image_settings.color_mode = 'RGB'
            scene.render.image_settings.color_depth = IMAGE_SEQUENCE_COLOR_DEPTH
            scene.render.image_settings.compression = IMAGE_SEQUENCE_COMPRESSION
        except Exception:
            pass
    else:
        Path(output_mp4).parent.mkdir(parents=True, exist_ok=True)
        scene.render.filepath = str(output_mp4)
        scene.render.use_overwrite = True
        scene.render.use_sequencer = True

        try:
            scene.render.image_settings.media_type = 'VIDEO'
        except Exception:
            pass

        try:
            scene.render.image_settings.file_format = 'FFMPEG'
            scene.render.image_settings.color_mode = 'RGB'
        except Exception:
            pass

        scene.render.ffmpeg.format = 'MPEG4'
        scene.render.ffmpeg.codec = 'H264'
        scene.render.ffmpeg.audio_codec = 'AAC'
        scene.render.ffmpeg.audio_bitrate = AUDIO_BITRATE

        for crf in ('PERC_LOSSLESS', 'HIGH'):
            try:
                scene.render.ffmpeg.constant_rate_factor = crf
                break
            except Exception:
                pass

        try:
            scene.render.ffmpeg.ffmpeg_preset = 'GOOD'
        except Exception:
            pass

        try:
            scene.render.ffmpeg.video_bitrate = VIDEO_BITRATE
            scene.render.ffmpeg.maxrate = VIDEO_MAXRATE
            scene.render.ffmpeg.minrate = VIDEO_MINRATE
            scene.render.ffmpeg.buffersize = VIDEO_BUFFERSIZE
        except Exception:
            pass

    scene.render.use_motion_blur = USE_MOTION_BLUR

    eevee = scene.eevee

    if hasattr(eevee, "taa_render_samples"):
        eevee.taa_render_samples = EEVEE_TAA_RENDER_SAMPLES

    if hasattr(eevee, "use_bloom"):
        eevee.use_bloom = USE_BLOOM
        if hasattr(eevee, "bloom_threshold"):
            eevee.bloom_threshold = BLOOM_THRESHOLD
        if hasattr(eevee, "bloom_intensity"):
            eevee.bloom_intensity = BLOOM_INTENSITY

    if hasattr(eevee, "use_gtao"):
        eevee.use_gtao = True
    if hasattr(eevee, "gtao_quality"):
        eevee.gtao_quality = 0.25

    if hasattr(eevee, "use_volumetric_lights"):
        eevee.use_volumetric_lights = bool(FOG_VOLUME_ENABLED)
    if hasattr(eevee, "use_volumetric_shadows"):
        eevee.use_volumetric_shadows = False
    if hasattr(eevee, "volumetric_samples"):
        eevee.volumetric_samples = VOLUMETRIC_SAMPLES
    if hasattr(eevee, "volumetric_tile_size"):
        eevee.volumetric_tile_size = VOLUMETRIC_TILE_SIZE

    try:
        scene.view_settings.exposure = VIEW_EXPOSURE
    except Exception:
        pass

    try:
        scene.view_settings.gamma = VIEW_GAMMA
    except Exception:
        pass

    configure_compositor(scene)
