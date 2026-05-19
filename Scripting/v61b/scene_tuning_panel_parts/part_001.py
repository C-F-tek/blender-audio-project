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
