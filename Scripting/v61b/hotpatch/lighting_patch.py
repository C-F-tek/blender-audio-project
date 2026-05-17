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
WORLD_CAMERA_STRENGTH = cfg_value("WORLD_CAMERA_STRENGTH", 0.52)
WORLD_LIGHT_COLOR = cfg_value("WORLD_LIGHT_COLOR", (0.012, 0.052, 0.058, 1.0))
WORLD_CAMERA_COLOR = cfg_value("WORLD_CAMERA_COLOR", (0.045, 0.170, 0.185, 1.0))
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
    links = world.node_tree.links

    for node in list(nodes):
        nodes.remove(node)

    out = nodes.new("ShaderNodeOutputWorld")
    out.location = (520, 0)

    bg_camera = nodes.new("ShaderNodeBackground")
    bg_camera.name = "WorldCameraAzzurro"
    bg_camera.location = (-260, 80)
    bg_camera.inputs["Strength"].default_value = WORLD_CAMERA_STRENGTH
    bg_camera.inputs["Color"].default_value = WORLD_CAMERA_COLOR

    bg_light = nodes.new("ShaderNodeBackground")
    bg_light.name = "WorldSceneLight"
    bg_light.location = (-260, -130)
    bg_light.inputs["Strength"].default_value = WORLD_STRENGTH
    bg_light.inputs["Color"].default_value = WORLD_LIGHT_COLOR

    light_path = nodes.new("ShaderNodeLightPath")
    light_path.location = (-560, -70)

    mix = nodes.new("ShaderNodeMixShader")
    mix.location = (120, 0)

    links.new(light_path.outputs["Is Camera Ray"], mix.inputs[0])
    links.new(bg_light.outputs["Background"], mix.inputs[1])
    links.new(bg_camera.outputs["Background"], mix.inputs[2])
    links.new(mix.outputs["Shader"], out.inputs["Surface"])


def remove_legacy_rhythm_objects():
    return remove_objects_with_prefixes(["RhythmPulseLight", "RhythmEmitterOrb"])


def update_area_lights(frames):
    lights = [
        obj for obj in bpy.data.objects if obj.type == "LIGHT" and obj.name.startswith("AreaLight_")
    ]
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
            socket.default_value = (
                BACKDROP_EMISSION_MIN + (BACKDROP_EMISSION_MAX - BACKDROP_EMISSION_MIN) * 0.18
            )

        for node in material.node_tree.nodes:
            if node.type == "TEX_NOISE" and "Scale" in node.inputs:
                node.inputs["Scale"].default_value = 1.18
            if node.type == "VALTORGB":
                try:
                    node.color_ramp.elements[0].position = 0.14
                    node.color_ramp.elements[0].color = (0.012, 0.055, 0.064, 1.0)
                    node.color_ramp.elements[1].position = 1.00
                    node.color_ramp.elements[1].color = (0.085, 0.245, 0.255, 1.0)
                except Exception:
                    pass

    if backdrop is not None:
        clear_animation(backdrop)
        backdrop.hide_render = False
        backdrop.hide_viewport = False
        backdrop.location = BACKDROP_LOCATION
        backdrop.rotation_euler = (BACKDROP_ROT_X, 0.0, 0.0)
        resize_plane_local(backdrop, BACKDROP_SIZE)

    return backdrop is not None
