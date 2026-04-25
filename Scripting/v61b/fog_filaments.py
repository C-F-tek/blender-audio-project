import math
import random

import bpy
from mathutils import Euler, Vector

from config import (
    FOG_FILAMENTS_ENABLED,
    FOG_FILAMENT_COUNT,
    FOG_FILAMENT_WIDTH_MIN,
    FOG_FILAMENT_WIDTH_MAX,
    FOG_FILAMENT_HEIGHT_MIN,
    FOG_FILAMENT_HEIGHT_MAX,
    FOG_FILAMENT_DEPTH_MIN,
    FOG_FILAMENT_DEPTH_MAX,
    FOG_FILAMENT_Z_MIN,
    FOG_FILAMENT_Z_MAX,
)
from materials import build_fog_filament_material
from scene_utils import create_controller_empty


ROOT_NAME = "FogFilamentsRoot"
OBJECT_PREFIX = "FogFilament_"
MATERIAL_NAME = "FogFilamentMaterial"


def _store_base_transform(obj, phase):
    obj["st_fog_filament"] = True
    obj["st_phase"] = float(phase)
    obj["st_base_location"] = [float(v) for v in obj.location]
    obj["st_base_scale"] = [float(v) for v in obj.scale]
    obj["st_base_rotation"] = [float(v) for v in obj.rotation_euler]


def _base_vector(obj, key, fallback):
    raw = obj.get(key)
    if raw is None:
        return fallback.copy()
    try:
        return Vector((float(raw[0]), float(raw[1]), float(raw[2])))
    except Exception:
        return fallback.copy()


def _base_euler(obj, key, fallback):
    raw = obj.get(key)
    if raw is None:
        return fallback.copy()
    try:
        return Euler((float(raw[0]), float(raw[1]), float(raw[2])), fallback.order)
    except Exception:
        return fallback.copy()


def _make_filament(index, material, parent=None):
    rng = random.Random(6100 + index * 37)
    x = rng.uniform(-7.4, 7.4)
    y = rng.uniform(FOG_FILAMENT_DEPTH_MIN, FOG_FILAMENT_DEPTH_MAX)
    z = rng.uniform(FOG_FILAMENT_Z_MIN, FOG_FILAMENT_Z_MAX)
    width = rng.uniform(FOG_FILAMENT_WIDTH_MIN, FOG_FILAMENT_WIDTH_MAX)
    height = rng.uniform(FOG_FILAMENT_HEIGHT_MIN, FOG_FILAMENT_HEIGHT_MAX)

    bpy.ops.mesh.primitive_plane_add(
        size=1.0,
        location=(x, y, z),
        rotation=(
            math.radians(90.0 + rng.uniform(-4.0, 4.0)),
            math.radians(rng.uniform(-4.0, 4.0)),
            math.radians(rng.uniform(-8.0, 8.0)),
        ),
    )
    obj = bpy.context.active_object
    obj.name = f"{OBJECT_PREFIX}{index:02d}"
    obj.scale = (width, height, 1.0)
    obj.data.name = f"{OBJECT_PREFIX}{index:02d}_Mesh"
    obj.data.materials.append(material)
    obj.hide_render = False
    obj.hide_viewport = False
    try:
        obj.show_transparent = True
    except Exception:
        pass
    obj.parent = parent

    _store_base_transform(obj, rng.uniform(0.0, math.tau))
    return obj


def _collect_objects():
    objects = [obj for obj in bpy.data.objects if obj.name.startswith(OBJECT_PREFIX)]
    return sorted(objects, key=lambda obj: obj.name)


def ensure_fog_filaments(parent=None):
    material, controls = build_fog_filament_material(MATERIAL_NAME)

    root = bpy.data.objects.get(ROOT_NAME)
    if root is None:
        root = create_controller_empty(
            ROOT_NAME,
        location=(0, 4.8, 3.1),
        parent=parent,
        display_size=0.50,
        hide_view=False,
    )
    elif parent is not None and root.parent is None:
        root.parent = parent

    existing = _collect_objects()

    if not FOG_FILAMENTS_ENABLED:
        for obj in existing:
            obj.hide_render = True
            obj.hide_viewport = True
        return {
            "root": root,
            "objects": [],
            "material": material,
            "controls": controls,
        }

    for index in range(len(existing), FOG_FILAMENT_COUNT):
        existing.append(_make_filament(index, material, parent=root))

    active = []
    for index, obj in enumerate(existing):
        if index >= FOG_FILAMENT_COUNT:
            obj.hide_render = True
            obj.hide_viewport = True
            continue

        if not obj.data.materials:
            obj.data.materials.append(material)
        else:
            obj.data.materials[0] = material

        obj.hide_render = False
        obj.hide_viewport = False
        if "st_base_location" not in obj:
            _store_base_transform(obj, float(index) * 0.73)

        active.append({
            "object": obj,
            "phase": float(obj.get("st_phase", index * 0.73)),
            "base_location": _base_vector(obj, "st_base_location", obj.location),
            "base_scale": _base_vector(obj, "st_base_scale", obj.scale),
            "base_rotation": _base_euler(obj, "st_base_rotation", obj.rotation_euler),
        })

    return {
        "root": root,
        "objects": active,
        "material": material,
        "controls": controls,
    }
