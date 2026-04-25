import json
from pathlib import Path

import bpy

import config as cfg


def cfg_value(name, default):
    return getattr(cfg, name, default)


ANALYSIS_JSON_PATH = cfg_value(
    "ANALYSIS_JSON_PATH",
    Path.home() / "blender" / "blender-audio-project" / "output" / "Feel The Light-Luca Vera_Master_analysis.json",
)
OUTPUT_MP4 = cfg_value(
    "OUTPUT_MP4",
    Path.home() / "blender" / "renders" / "spaziotempo_asset_visual_v61b.mp4",
)
PALETTE_LIST = cfg_value(
    "PALETTE_LIST",
    [
        (0.170, 0.460, 0.480, 1.0),
        (0.720, 0.620, 0.340, 1.0),
        (0.500, 0.300, 0.340, 1.0),
        (0.940, 0.930, 0.900, 1.0),
    ],
)


def load_analysis():
    path = Path(ANALYSIS_JSON_PATH)
    if not path.exists():
        print(f"[WARN] Analysis JSON non trovato: {path}")
        return None, []

    data = json.loads(path.read_text(encoding="utf-8"))
    return data.get("meta", {}), data.get("frames", [])


def iter_objects_prefix(prefix):
    return [obj for obj in bpy.data.objects if obj.name.startswith(prefix)]


def remove_objects_with_prefixes(prefixes):
    removed = 0
    for obj in list(bpy.data.objects):
        if not any(obj.name.startswith(prefix) for prefix in prefixes):
            continue
        bpy.data.objects.remove(obj, do_unlink=True)
        removed += 1
    return removed


def keyframe_if_possible(idblock, data_path, frame):
    try:
        idblock.keyframe_insert(data_path=data_path, frame=frame)
    except Exception:
        pass


def clear_animation(idblock):
    if idblock is None:
        return
    try:
        idblock.animation_data_clear()
    except Exception:
        pass


def get_node(material, node_name):
    if material is None or not material.use_nodes:
        return None
    return material.node_tree.nodes.get(node_name)


def socket_by_name(node, socket_name, is_output=False):
    if node is None:
        return None
    sockets = node.outputs if is_output else node.inputs
    try:
        return sockets[socket_name]
    except Exception:
        return None


def store_base_vector(obj, key, value):
    if key not in obj:
        obj[key] = [float(value.x), float(value.y), float(value.z)]
    return obj[key]
