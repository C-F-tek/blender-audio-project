bl_info = {
    "name": "Spaziotempo Scene Tuning Panel",
    "author": "Codex + Carmine",
    "version": (0, 1, 0),
    "blender": (5, 0, 0),
    "location": "View3D > Sidebar > Spaziotempo",
    "description": "Manual tuning controls for the Spaziotempo audio visual scene.",
    "category": "3D View",
}

import json
import sys
import traceback
from pathlib import Path

import bpy
from bpy.props import BoolProperty, FloatProperty, PointerProperty, StringProperty


def resolve_script_dir():
    candidates = []

    try:
        text = bpy.context.space_data.text
        if text is not None and text.filepath:
            candidates.append(Path(text.filepath).resolve().parent)
    except Exception:
        pass

    if "__file__" in globals():
        try:
            candidates.append(Path(__file__).resolve().parent)
        except Exception:
            pass

    candidates.append(Path.home() / "blender" / "blender-audio-project" / "Scripting" / "v61b")

    for candidate in candidates:
        if (candidate / "config.py").exists() and (candidate / "hot_update_scene_v61b.py").exists():
            return candidate

    return candidates[-1]


SCRIPT_DIR = resolve_script_dir()
PRESET_PATH = SCRIPT_DIR / "scene_tuning_preset.json"
GUIDE_PATH = SCRIPT_DIR / "SCENE_TUNING_GUIDE.md"
HOT_UPDATE_PATH = SCRIPT_DIR / "hot_update_scene_v61b.py"
ENCODE_SEQUENCE_PATH = SCRIPT_DIR / "encode_image_sequence_v61b.py"
ENCODE_FFMPEG_PATH = SCRIPT_DIR / "encode_ffmpeg_v61b.py"

if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))


def iter_action_fcurves(action):
    if action is None:
        return

    if hasattr(action, "fcurves"):
        try:
            for fcurve in action.fcurves:
                yield fcurve
            return
        except Exception:
            pass

    layers = getattr(action, "layers", None)
    if not layers:
        return

    for layer in layers:
        strips = getattr(layer, "strips", None)
        if not strips:
            continue
        for strip in strips:
            channelbags = getattr(strip, "channelbags", None)
            if not channelbags:
                continue
            for channelbag in channelbags:
                fcurves = getattr(channelbag, "fcurves", None)
                if not fcurves:
                    continue
                for fcurve in fcurves:
                    yield fcurve


def find_obj(name):
    return bpy.data.objects.get(name)


def objects_with_prefix(prefix):
    return [obj for obj in bpy.data.objects if obj.name.startswith(prefix)]


def particle_emitters():
    names = [
        "BeatPulseParticleEmitter",
        "OrbitDustParticleEmitter",
        "HighStreakParticleEmitter",
        "AlbumLetterParticleEmitter",
    ]
    return [obj for name in names if (obj := find_obj(name)) is not None]


def particle_source_objects():
    names = [
        "BeatSparkParticle",
        "OrbitDustParticle",
        "HighStreakParticle",
    ]
    sources = [obj for name in names if (obj := find_obj(name)) is not None]
    sources.extend(objects_with_prefix("AlbumLetterParticle_"))
    return sources


def store_base_vector(obj, key, value):
    if key not in obj:
        obj[key] = [float(value.x), float(value.y), float(value.z)]
    return obj[key]


def store_base_float(idblock, key, value):
    try:
        if key not in idblock:
            idblock[key] = float(value)
        return float(idblock[key])
    except Exception:
        return float(value)


def set_scale_from_base(obj, factor, key="_st_base_scale"):
    if obj is None:
        return

    base = store_base_vector(obj, key, obj.scale)
    obj.scale = (base[0] * factor, base[1] * factor, base[2] * factor)


def keyframe_if_possible(idblock, data_path, frame):
    try:
        idblock.keyframe_insert(data_path=data_path, frame=frame)
    except Exception:
        pass


def find_material(name):
    return bpy.data.materials.get(name)


def find_node(material_name, node_name):
    material = find_material(material_name)
    if material is None or not material.use_nodes:
        return None
    return material.node_tree.nodes.get(node_name)


def set_value_node(material_name, node_name, value):
    node = find_node(material_name, node_name)
    if node is None:
        return None
    try:
        node.outputs[0].default_value = value
        return node.outputs[0]
    except Exception:
        return None


def set_input_node(material_name, node_name, input_name, value):
    node = find_node(material_name, node_name)
    if node is None:
        return None
    try:
        node.inputs[input_name].default_value = value
        return node.inputs[input_name]
    except Exception:
        return None


def keyframe_socket(socket, frame):
    if socket is None:
        return
    keyframe_if_possible(socket, "default_value", frame)


def get_scene_compositor_tree(scene):
    for attr in ("node_tree", "compositor_node_tree"):
        tree = getattr(scene, attr, None)
        if tree is not None:
            return tree
    return None


def clamp_value(value, min_value, max_value):
    return max(min_value, min(max_value, value))


def normalize_runtime_profile(profile):
    if isinstance(profile, bool):
        return "YOUTUBE_4K" if profile else "PREVIEW"

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


def runtime_profile_label(profile):
    labels = {
        "PREVIEW": "Preview",
        "YOUTUBE_FAST_1080P": "YouTube Fast 1080p",
        "YOUTUBE_FAST_1440P": "YouTube Fast 1440p",
        "YOUTUBE_FAST_4K": "YouTube Fast 4K",
        "YOUTUBE_1080P": "YouTube Final 1080p",
        "YOUTUBE_1440P": "YouTube Final 1440p",
        "YOUTUBE_4K": "YouTube Final 4K",
    }
    return labels.get(normalize_runtime_profile(profile), "Preview")


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
            eevee.volumetric_tile_size = '8'
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
        for crf in ('PERC_LOSSLESS', 'HIGH'):
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
            if mod.type != 'PARTICLE_SYSTEM':
                continue
            ps = getattr(mod, "particle_system", None)
            if ps is not None and ps.settings is not None:
                settings.append(ps.settings)
    return settings


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
                base = store_base_float(obj, f"_st_base_{mod.name}_strength", getattr(mod, "strength", 0.0))
                mod.strength = base * tune.hero_deform
                if insert_keyframes:
                    keyframe_if_possible(mod, "strength", frame)
            elif mod.name == "HeroAudioFineDisplace":
                base = store_base_float(obj, f"_st_base_{mod.name}_strength", getattr(mod, "strength", 0.0))
                mod.strength = base * tune.hero_fine_deform
                if insert_keyframes:
                    keyframe_if_possible(mod, "strength", frame)
            elif mod.name == "HeroAudioSurfaceWave":
                try:
                    base = store_base_float(obj, f"_st_base_{mod.name}_height", getattr(mod, "height", 0.0))
                    mod.height = base * tune.hero_wave
                    if insert_keyframes:
                        keyframe_if_possible(mod, "height", frame)
                except Exception:
                    pass
            elif mod.name == "HeroAudioTwistDeform":
                try:
                    base = store_base_float(obj, f"_st_base_{mod.name}_angle", getattr(mod, "angle", 0.0))
                    mod.angle = base * tune.hero_twist
                    if insert_keyframes:
                        keyframe_if_possible(mod, "angle", frame)
                except Exception:
                    pass
            elif mod.name in {"AuraAudioBreathDisplace", "AuraAudioTransientDetail"}:
                base = store_base_float(obj, f"_st_base_{mod.name}_strength", getattr(mod, "strength", 0.0))
                mod.strength = base * tune.aura_deform
                if insert_keyframes:
                    keyframe_if_possible(mod, "strength", frame)

    for mat in bpy.data.materials:
        if mat is None or not mat.use_nodes:
            continue

        nodes = mat.node_tree.nodes
        for node_name, factor, key, min_value, max_value in [
            ("HeroMatEmissionValue", tune.hero_mat_emission, "_st_base_hero_mat_emission", 0.0, 3.0),
            ("HeroMatSelfLightValue", tune.hero_mat_emission, "_st_base_hero_mat_self_light", 0.0, 1.0),
            ("HeroMatBumpStrength", tune.hero_mat_bump, "_st_base_hero_mat_bump", 0.0, 0.25),
            ("HeroMatRoughnessValue", tune.hero_mat_roughness, "_st_base_hero_mat_roughness", 0.02, 1.0),
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
            base = store_base_float(noise, "_st_base_hero_mat_noise", noise.inputs["Scale"].default_value)
            noise.inputs["Scale"].default_value = clamp_value(base * tune.hero_mat_noise, 0.10, 80.0)
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
    fog_noise = set_input_node("AtmosphereVolumeMaterial", "Noise Texture", "Scale", tune.fog_noise_scale)
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
                base_emit = store_base_float(node, "_st_base_physics_accent_emit", socket.default_value)
                socket.default_value = max(0.0, base_emit * tune.rhythm_light_power)
                if insert_keyframes:
                    keyframe_socket(socket, frame)

            mix_node = mat.node_tree.nodes.get("VariantEmissionMix")
            if mix_node is not None:
                socket = mix_node.outputs[0]
                base_mix = store_base_float(mix_node, "_st_base_physics_accent_mix", socket.default_value)
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
        base_size = store_base_float(ps_settings, "_st_base_particle_size", ps_settings.particle_size)
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


class ST_TuningSettings(bpy.types.PropertyGroup):
    hero_scale: FloatProperty(name="Hero scale", default=1.0, min=0.20, max=3.0, precision=3)
    hero_deform: FloatProperty(name="Hero deform", default=1.0, min=0.0, max=4.0, precision=3)
    hero_fine_deform: FloatProperty(name="Hero fine", default=1.0, min=0.0, max=4.0, precision=3)
    hero_wave: FloatProperty(name="Hero wave", default=1.0, min=0.0, max=4.0, precision=3)
    hero_twist: FloatProperty(name="Hero twist", default=1.0, min=0.0, max=4.0, precision=3)
    hero_mat_emission: FloatProperty(name="Hero material light", default=1.0, min=0.0, max=4.0, precision=3)
    hero_mat_bump: FloatProperty(name="Hero material bump", default=1.0, min=0.0, max=4.0, precision=3)
    hero_mat_roughness: FloatProperty(name="Hero material rough", default=1.0, min=0.10, max=2.0, precision=3)
    hero_mat_noise: FloatProperty(name="Hero material noise", default=1.0, min=0.10, max=4.0, precision=3)

    aura_deform: FloatProperty(name="Aura deform", default=0.45, min=0.0, max=1.0, precision=3)
    aura_detail: FloatProperty(name="Aura detail", default=0.35, min=0.0, max=1.0, precision=3)
    aura_pulse: FloatProperty(name="Aura pulse", default=0.35, min=0.0, max=1.0, precision=3)

    fog_density: FloatProperty(name="Fog density", default=0.035, min=0.0, max=0.55, precision=4)
    fog_emission: FloatProperty(name="Fog emission", default=0.004, min=0.0, max=0.12, precision=4)
    fog_noise_scale: FloatProperty(name="Fog noise", default=0.9, min=0.10, max=12.0, precision=3)
    fog_scale_xy: FloatProperty(name="Fog XY", default=1.0, min=0.20, max=2.20, precision=3)
    fog_scale_z: FloatProperty(name="Fog Z", default=1.0, min=0.20, max=2.40, precision=3)

    backdrop_emission: FloatProperty(name="Backdrop light", default=0.075, min=0.0, max=0.60, precision=4)
    backdrop_noise_scale: FloatProperty(name="Backdrop noise", default=2.4, min=0.10, max=12.0, precision=3)
    backdrop_scale: FloatProperty(name="Backdrop scale", default=1.0, min=0.20, max=2.40, precision=3)
    floor_scale: FloatProperty(name="Floor scale", default=1.0, min=0.20, max=3.0, precision=3)

    camera_fstop: FloatProperty(name="Camera f-stop", default=6.5, min=1.0, max=16.0, precision=2)
    rhythm_light_power: FloatProperty(name="Accent emission", default=1.0, min=0.0, max=4.0, precision=3)
    compositor_glow: FloatProperty(name="Compositor glow", default=1.0, min=0.10, max=4.0, precision=3)
    compositor_lens: FloatProperty(name="Compositor lens", default=1.0, min=0.0, max=4.0, precision=3)

    particle_size: FloatProperty(name="Particle size", default=1.0, min=0.05, max=5.0, precision=3)
    particle_force: FloatProperty(name="Particle force", default=1.0, min=0.0, max=5.0, precision=3)
    letter_source_scale: FloatProperty(name="Letter source scale", default=1.0, min=0.10, max=3.0, precision=3)

    anim_hero_deform_factor: FloatProperty(name="Anim hero deform", default=1.0, min=0.0, max=4.0, precision=3)
    anim_aura_factor: FloatProperty(name="Anim aura", default=1.0, min=0.0, max=4.0, precision=3)
    anim_particle_size_factor: FloatProperty(name="Anim particle size", default=1.0, min=0.05, max=5.0, precision=3)
    anim_particle_force_factor: FloatProperty(name="Anim particle force", default=1.0, min=0.0, max=5.0, precision=3)

    show_fog_cube: BoolProperty(name="Show fog cube", default=False)
    show_backdrop: BoolProperty(name="Show backdrop", default=True)
    render_backdrop: BoolProperty(name="Render backdrop", default=True)
    show_floor: BoolProperty(name="Show floor", default=True)
    render_floor: BoolProperty(name="Render floor", default=False)
    show_emitters: BoolProperty(name="Show emitters", default=False)
    show_particle_sources: BoolProperty(name="Show source objects", default=False)
    motion_blur: BoolProperty(name="Motion blur", default=False)
    youtube_final: BoolProperty(name="YouTube final", default=False)
    runtime_profile: StringProperty(name="Runtime profile", default="Preview")


class ST_OT_apply_tuning(bpy.types.Operator):
    bl_idname = "spaziotempo.apply_tuning"
    bl_label = "Apply Live Values"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        apply_tuning(context, insert_keyframes=False)
        self.report({'INFO'}, "Spaziotempo tuning applied to current scene.")
        return {'FINISHED'}


class ST_OT_keyframe_tuning(bpy.types.Operator):
    bl_idname = "spaziotempo.keyframe_tuning"
    bl_label = "Apply + Keyframe"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        apply_tuning(context, insert_keyframes=True)
        self.report({'INFO'}, f"Spaziotempo values keyframed at frame {context.scene.frame_current}.")
        return {'FINISHED'}


class ST_OT_scale_animation(bpy.types.Operator):
    bl_idname = "spaziotempo.scale_animation"
    bl_label = "Scale Existing FCurves"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        changed = scale_full_animation(context)
        self.report({'INFO'}, f"Scaled {changed} keyframe values.")
        return {'FINISHED'}


class ST_OT_apply_runtime_profile(bpy.types.Operator):
    bl_idname = "spaziotempo.apply_runtime_profile"
    bl_label = "Apply Runtime Profile"
    bl_options = {'REGISTER', 'UNDO'}

    final_for_youtube: bpy.props.BoolProperty(default=False)
    profile: bpy.props.StringProperty(default="")

    def execute(self, context):
        profile = self.profile or ("YOUTUBE_4K" if self.final_for_youtube else "PREVIEW")
        apply_runtime_profile(context, profile)
        label = runtime_profile_label(profile)
        self.report({'INFO'}, f"{label} profile applied to current scene.")
        return {'FINISHED'}


class ST_OT_hot_update_scene(bpy.types.Operator):
    bl_idname = "spaziotempo.hot_update_scene"
    bl_label = "Hot Update Scene"
    bl_options = {'REGISTER', 'UNDO'}

    mode: bpy.props.StringProperty(default="ALL")

    def execute(self, context):
        if not HOT_UPDATE_PATH.exists():
            self.report({'WARNING'}, f"Hot update script not found: {HOT_UPDATE_PATH}")
            return {'CANCELLED'}

        try:
            code = compile(HOT_UPDATE_PATH.read_text(encoding="utf-8"), str(HOT_UPDATE_PATH), "exec")
            exec(code, {"__file__": str(HOT_UPDATE_PATH), "__name__": "__main__", "HOTPATCH_MODE": self.mode})
        except Exception as exc:
            traceback.print_exc()
            self.report({'ERROR'}, f"Hot update failed: {exc}")
            return {'CANCELLED'}

        self.report({'INFO'}, f"Hot update {self.mode} complete.")
        return {'FINISHED'}


class ST_OT_rebuild_restart_check(bpy.types.Operator):
    bl_idname = "spaziotempo.rebuild_restart_check"
    bl_label = "Rebuild / Restart Check"
    bl_options = {'REGISTER'}

    def execute(self, context):
        try:
            sys.modules.pop("hotpatch.diagnostics", None)
            from hotpatch.diagnostics import analyze_rebuild_need

            result = analyze_rebuild_need()
        except Exception as exc:
            traceback.print_exc()
            self.report({'ERROR'}, f"Check failed: {exc}")
            return {'CANCELLED'}

        if result["blocking"]:
            self.report({'WARNING'}, "Full rebuild needed. See SPAZIOTEMPO_REBUILD_CHECK.")
        elif result["restart"]:
            self.report({'WARNING'}, "Registration issue found. See SPAZIOTEMPO_REBUILD_CHECK.")
        else:
            self.report({'INFO'}, "Hotpatch should be enough. See SPAZIOTEMPO_REBUILD_CHECK.")
        return {'FINISHED'}


class ST_OT_optimizer_check(bpy.types.Operator):
    bl_idname = "spaziotempo.optimizer_check"
    bl_label = "Optimizer Check"
    bl_options = {'REGISTER'}

    def execute(self, context):
        try:
            sys.modules.pop("hotpatch.diagnostics", None)
            from hotpatch.diagnostics import analyze_optimizer

            result = analyze_optimizer()
        except Exception as exc:
            traceback.print_exc()
            self.report({'ERROR'}, f"Optimizer check failed: {exc}")
            return {'CANCELLED'}

        if result["warnings"]:
            self.report({'WARNING'}, "Cache/bake suggestions found. See SPAZIOTEMPO_OPTIMIZER_REPORT.")
        else:
            self.report({'INFO'}, "No required bake found. See SPAZIOTEMPO_OPTIMIZER_REPORT.")
        return {'FINISHED'}


class ST_OT_load_image_sequence(bpy.types.Operator):
    bl_idname = "spaziotempo.load_image_sequence"
    bl_label = "Load Image Sequence"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if not ENCODE_SEQUENCE_PATH.exists():
            self.report({'WARNING'}, f"Image sequence script not found: {ENCODE_SEQUENCE_PATH}")
            return {'CANCELLED'}

        try:
            code = compile(ENCODE_SEQUENCE_PATH.read_text(encoding="utf-8"), str(ENCODE_SEQUENCE_PATH), "exec")
            exec(code, {"__file__": str(ENCODE_SEQUENCE_PATH), "__name__": "__main__"})
        except Exception as exc:
            traceback.print_exc()
            self.report({'ERROR'}, f"Image sequence load failed: {exc}")
            return {'CANCELLED'}

        self.report({'INFO'}, "Image sequence + audio loaded in Video Sequencer.")
        return {'FINISHED'}


class ST_OT_encode_ffmpeg(bpy.types.Operator):
    bl_idname = "spaziotempo.encode_ffmpeg"
    bl_label = "Encode MP4 FFmpeg"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if not ENCODE_FFMPEG_PATH.exists():
            self.report({'WARNING'}, f"FFmpeg encode script not found: {ENCODE_FFMPEG_PATH}")
            return {'CANCELLED'}

        try:
            code = compile(ENCODE_FFMPEG_PATH.read_text(encoding="utf-8"), str(ENCODE_FFMPEG_PATH), "exec")
            exec(code, {"__file__": str(ENCODE_FFMPEG_PATH), "__name__": "__main__"})
        except Exception as exc:
            traceback.print_exc()
            self.report({'ERROR'}, f"FFmpeg encode failed: {exc}")
            return {'CANCELLED'}

        self.report({'INFO'}, "FFmpeg MP4 encoded from image sequence.")
        return {'FINISHED'}


class ST_OT_save_preset(bpy.types.Operator):
    bl_idname = "spaziotempo.save_tuning_preset"
    bl_label = "Save Preset"

    def execute(self, context):
        data = preset_data(context.scene.spaziotempo_tuning)
        PRESET_PATH.write_text(json.dumps(data, indent=2), encoding="utf-8")
        self.report({'INFO'}, f"Preset saved: {PRESET_PATH}")
        return {'FINISHED'}


class ST_OT_load_preset(bpy.types.Operator):
    bl_idname = "spaziotempo.load_tuning_preset"
    bl_label = "Load Preset"

    def execute(self, context):
        if not PRESET_PATH.exists():
            self.report({'WARNING'}, f"Preset not found: {PRESET_PATH}")
            return {'CANCELLED'}

        data = json.loads(PRESET_PATH.read_text(encoding="utf-8"))
        load_preset_data(context.scene.spaziotempo_tuning, data)
        apply_tuning(context, insert_keyframes=False)
        self.report({'INFO'}, "Preset loaded and applied.")
        return {'FINISHED'}


class ST_OT_open_guide_text(bpy.types.Operator):
    bl_idname = "spaziotempo.open_tuning_guide"
    bl_label = "Open Editable Guide"

    def execute(self, context):
        text_name = "SPAZIOTEMPO_TUNING_GUIDE"
        guide = bpy.data.texts.get(text_name) or bpy.data.texts.new(text_name)

        if GUIDE_PATH.exists():
            body = GUIDE_PATH.read_text(encoding="utf-8")
        else:
            body = "Spaziotempo tuning guide not found."

        guide.clear()
        guide.write(body)
        self.report({'INFO'}, f"Guide opened as Blender text block: {text_name}")
        return {'FINISHED'}


class ST_OT_select_group(bpy.types.Operator):
    bl_idname = "spaziotempo.select_group"
    bl_label = "Select Scene Group"

    group: bpy.props.StringProperty(default="hero")

    def execute(self, context):
        bpy.ops.object.select_all(action='DESELECT')

        names = []
        if self.group == "hero":
            names = ["HeroRoot", "HeroDeformController", "AuraAudioSampler"]
        elif self.group == "particles":
            names = [obj.name for obj in particle_emitters()]
        elif self.group == "fog":
            names = ["AtmosphereCube", "FogPulseController", "FogFilamentsRoot", "SoftRhythmBackdrop", "BackdropPulseController"]
            names.extend(obj.name for obj in objects_with_prefix("FogFilament_"))
        elif self.group == "letters":
            names = ["AlbumLetterParticleSources"]
            names.extend(obj.name for obj in objects_with_prefix("AlbumLetterParticle_"))

        selected = []
        for name in names:
            obj = find_obj(name)
            if obj is None:
                continue
            obj.hide_viewport = False
            obj.select_set(True)
            selected.append(obj)

        if selected:
            context.view_layer.objects.active = selected[0]
        self.report({'INFO'}, f"Selected {len(selected)} objects.")
        return {'FINISHED'}


class ST_PT_tuning_panel(bpy.types.Panel):
    bl_label = "Scene Tuner"
    bl_idname = "ST_PT_tuning_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Spaziotempo"

    def draw(self, context):
        layout = self.layout
        tune = context.scene.spaziotempo_tuning

        row = layout.row(align=True)
        row.operator("spaziotempo.apply_tuning", icon='CHECKMARK')
        row.operator("spaziotempo.keyframe_tuning", icon='KEY_HLT')

        box = layout.box()
        box.label(text="Hot Update")
        row = box.row(align=True)
        op = row.operator("spaziotempo.hot_update_scene", text="Render Only", icon='OUTPUT')
        op.mode = "RENDER"
        op = row.operator("spaziotempo.hot_update_scene", text="Materials", icon='MATERIAL')
        op.mode = "MATERIALS"
        row = box.row(align=True)
        op = row.operator("spaziotempo.hot_update_scene", text="Fog", icon='MOD_FLUIDSIM')
        op.mode = "FOG"
        op = row.operator("spaziotempo.hot_update_scene", text="Physics", icon='PHYSICS')
        op.mode = "PHYSICS"
        op = box.operator("spaziotempo.hot_update_scene", text="Hot Update All", icon='FILE_REFRESH')
        op.mode = "ALL"

        row = box.row(align=True)
        row.operator("spaziotempo.rebuild_restart_check", icon='VIEWZOOM')
        row.operator("spaziotempo.optimizer_check", icon='SETTINGS')

        row = layout.row(align=True)
        row.operator("spaziotempo.save_tuning_preset", icon='FILE_TICK')
        row.operator("spaziotempo.load_tuning_preset", icon='FILE_REFRESH')

        layout.operator("spaziotempo.open_tuning_guide", icon='TEXT')

        box = layout.box()
        box.label(text="Hero / Aura")
        box.prop(tune, "hero_scale")
        box.prop(tune, "hero_deform")
        box.prop(tune, "hero_fine_deform")
        box.prop(tune, "hero_wave")
        box.prop(tune, "hero_twist")
        box.prop(tune, "hero_mat_emission")
        box.prop(tune, "hero_mat_bump")
        box.prop(tune, "hero_mat_roughness")
        box.prop(tune, "hero_mat_noise")
        box.prop(tune, "aura_deform")
        box.prop(tune, "aura_detail")
        box.prop(tune, "aura_pulse")

        box = layout.box()
        box.label(text="Fog")
        box.prop(tune, "fog_density")
        box.prop(tune, "fog_emission")
        box.prop(tune, "fog_noise_scale")
        box.prop(tune, "fog_scale_xy")
        box.prop(tune, "fog_scale_z")
        box.prop(tune, "show_fog_cube")

        box = layout.box()
        box.label(text="Backdrop / Floor")
        box.prop(tune, "backdrop_emission")
        box.prop(tune, "backdrop_noise_scale")
        box.prop(tune, "backdrop_scale")
        box.prop(tune, "floor_scale")
        box.prop(tune, "show_backdrop")
        box.prop(tune, "render_backdrop")
        box.prop(tune, "show_floor")
        box.prop(tune, "render_floor")

        box = layout.box()
        box.label(text="Camera / Render")
        row = box.row(align=True)
        op = row.operator("spaziotempo.apply_runtime_profile", text="Preview")
        op.profile = "PREVIEW"
        op = row.operator("spaziotempo.apply_runtime_profile", text="YT Fast 1080p")
        op.profile = "YOUTUBE_FAST_1080P"
        row = box.row(align=True)
        op = row.operator("spaziotempo.apply_runtime_profile", text="YT Fast 1440p")
        op.profile = "YOUTUBE_FAST_1440P"
        op = row.operator("spaziotempo.apply_runtime_profile", text="YT Fast 4K")
        op.profile = "YOUTUBE_FAST_4K"
        row = box.row(align=True)
        op = row.operator("spaziotempo.apply_runtime_profile", text="YT Final 1080p")
        op.profile = "YOUTUBE_1080P"
        op = row.operator("spaziotempo.apply_runtime_profile", text="YT Final 1440p")
        op.profile = "YOUTUBE_1440P"
        row = box.row(align=True)
        op = row.operator("spaziotempo.apply_runtime_profile", text="YT Final 4K")
        op.profile = "YOUTUBE_4K"
        box.prop(tune, "runtime_profile")
        box.prop(tune, "youtube_final")
        box.prop(tune, "camera_fstop")
        box.prop(tune, "motion_blur")
        box.prop(tune, "rhythm_light_power")
        box.prop(tune, "compositor_glow")
        box.prop(tune, "compositor_lens")
        box.operator("spaziotempo.load_image_sequence", text="Load Frames + Audio", icon='FILE_MOVIE')
        box.operator("spaziotempo.encode_ffmpeg", text="Encode MP4 FFmpeg", icon='FILE_MOVIE')

        box = layout.box()
        box.label(text="Scale Existing Animation")
        box.prop(tune, "anim_hero_deform_factor")
        box.prop(tune, "anim_aura_factor")
        box.operator("spaziotempo.scale_animation", icon='GRAPH')

        box = layout.box()
        box.label(text="Select")
        row = box.row(align=True)
        op = row.operator("spaziotempo.select_group", text="Hero")
        op.group = "hero"
        op = row.operator("spaziotempo.select_group", text="Fog")
        op.group = "fog"


classes = (
    ST_TuningSettings,
    ST_OT_apply_tuning,
    ST_OT_keyframe_tuning,
    ST_OT_scale_animation,
    ST_OT_apply_runtime_profile,
    ST_OT_hot_update_scene,
    ST_OT_rebuild_restart_check,
    ST_OT_optimizer_check,
    ST_OT_load_image_sequence,
    ST_OT_encode_ffmpeg,
    ST_OT_save_preset,
    ST_OT_load_preset,
    ST_OT_open_guide_text,
    ST_OT_select_group,
    ST_PT_tuning_panel,
)


def register():
    if hasattr(bpy.types.Scene, "spaziotempo_tuning"):
        del bpy.types.Scene.spaziotempo_tuning

    for cls in reversed(classes):
        try:
            bpy.utils.unregister_class(cls)
        except Exception:
            pass

    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.spaziotempo_tuning = PointerProperty(type=ST_TuningSettings)


def unregister():
    if hasattr(bpy.types.Scene, "spaziotempo_tuning"):
        del bpy.types.Scene.spaziotempo_tuning
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
