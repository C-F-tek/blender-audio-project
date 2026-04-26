import bpy

from .common import (
    cfg_value,
    clear_animation,
    get_node,
    keyframe_if_possible,
    remove_objects_with_prefixes,
    socket_by_name,
)


LIGHT_ENERGY_MIN = cfg_value("LIGHT_ENERGY_MIN", 105.0)
LIGHT_ENERGY_MAX = cfg_value("LIGHT_ENERGY_MAX", 128.0)
WORLD_STRENGTH = cfg_value("WORLD_STRENGTH", 0.115)
BACKDROP_EMISSION_MIN = cfg_value("BACKDROP_EMISSION_MIN", 0.025)
BACKDROP_EMISSION_MAX = cfg_value("BACKDROP_EMISSION_MAX", 0.027)
BACKDROP_SIZE = cfg_value("BACKDROP_SIZE", 92.0)
BACKDROP_LOCATION = cfg_value("BACKDROP_LOCATION", (0.0, 12.0, 5.2))
BACKDROP_ROT_X = cfg_value("BACKDROP_ROT_X", 1.57079632679)
FLOOR_RENDER_VISIBLE = cfg_value("FLOOR_RENDER_VISIBLE", False)
FLOOR_VIEWPORT_VISIBLE = cfg_value("FLOOR_VIEWPORT_VISIBLE", True)


def resize_plane_local(obj, target_size):
    mesh = getattr(obj, "data", None)
    vertices = getattr(mesh, "vertices", None)
    if not vertices:
        return

    xs = [v.co.x for v in vertices]
    ys = [v.co.y for v in vertices]
    width = max(xs) - min(xs)
    height = max(ys) - min(ys)
    if width > 0.0001:
        obj.scale.x = float(target_size) / width
    if height > 0.0001:
        obj.scale.y = float(target_size) / height


def update_world(scene):
    world = scene.world
    if world is None:
        world = bpy.data.worlds.new("PeaceWorld")
        scene.world = world

    world.use_nodes = True
    nodes = world.node_tree.nodes
    bg = nodes.get("Background")
    if bg is None:
        bg = nodes.new("ShaderNodeBackground")
    if "Strength" in bg.inputs:
        bg.inputs["Strength"].default_value = WORLD_STRENGTH
    if "Color" in bg.inputs:
        bg.inputs["Color"].default_value = (0.004, 0.012, 0.014, 1.0)


def remove_legacy_rhythm_objects():
    return remove_objects_with_prefixes(["RhythmPulseLight", "RhythmEmitterOrb"])


def update_area_lights(frames):
    lights = [obj for obj in bpy.data.objects if obj.type == 'LIGHT' and obj.name.startswith("AreaLight_")]
    for light in lights:
        clear_animation(light.data)

    if not frames:
        for light in lights:
            light.data.energy = LIGHT_ENERGY_MIN
        return len(lights)

    for frame, sample in enumerate(frames, start=1):
        high = float(sample.get("high", 0.0))
        mid = float(sample.get("mid", 0.0))
        low = float(sample.get("low", 0.0))
        onset = float(sample.get("onset", 0.0))
        beat = float(sample.get("beat", 0.0))
        pulse = max(onset, beat)
        drive = min(1.0, high * 0.006 + mid * 0.006 + low * 0.005 + pulse * 0.004)
        energy = LIGHT_ENERGY_MIN + drive * (LIGHT_ENERGY_MAX - LIGHT_ENERGY_MIN)
        for light in lights:
            light.data.energy = energy
            keyframe_if_possible(light.data, "energy", frame)

    return len(lights)


def update_backdrop():
    backdrop = bpy.data.objects.get("SoftRhythmBackdrop")
    material = bpy.data.materials.get("SoftBackdropMaterial")
    floor = bpy.data.objects.get("PeaceFloor")

    if floor is not None:
        floor.hide_render = not bool(FLOOR_RENDER_VISIBLE)
        floor.hide_viewport = not bool(FLOOR_VIEWPORT_VISIBLE)

    if material is not None and material.use_nodes:
        clear_animation(material.node_tree)
        emission = get_node(material, "BackdropEmission")
        socket = socket_by_name(emission, "Strength")
        if socket is not None:
            socket.default_value = BACKDROP_EMISSION_MIN + (BACKDROP_EMISSION_MAX - BACKDROP_EMISSION_MIN) * 0.18

        for node in material.node_tree.nodes:
            if node.type == "TEX_NOISE" and "Scale" in node.inputs:
                node.inputs["Scale"].default_value = 1.35

    if backdrop is not None:
        clear_animation(backdrop)
        backdrop.hide_render = False
        backdrop.hide_viewport = False
        backdrop.location = BACKDROP_LOCATION
        backdrop.rotation_euler = (BACKDROP_ROT_X, 0.0, 0.0)
        resize_plane_local(backdrop, BACKDROP_SIZE)

    return backdrop is not None
