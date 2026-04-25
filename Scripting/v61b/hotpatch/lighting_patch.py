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

    if material is not None and material.use_nodes:
        clear_animation(material.node_tree)
        emission = get_node(material, "BackdropEmission")
        socket = socket_by_name(emission, "Strength")
        if socket is not None:
            socket.default_value = BACKDROP_EMISSION_MIN + (BACKDROP_EMISSION_MAX - BACKDROP_EMISSION_MIN) * 0.06

        for node in material.node_tree.nodes:
            if node.type == "TEX_NOISE" and "Scale" in node.inputs:
                node.inputs["Scale"].default_value = 2.18

    if backdrop is not None:
        clear_animation(backdrop)
        backdrop.hide_render = False
        backdrop.hide_viewport = False

    return backdrop is not None
