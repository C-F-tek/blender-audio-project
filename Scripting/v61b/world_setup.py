import bpy
from pathlib import Path

from config import (
    PEACE_PALETTE,
    WORLD_STRENGTH,
    USE_HDRI_WORLD,
    HDRI_PATH,
    HDRI_STRENGTH,
    HDRI_ROT_Z,
    LIGHT_ENERGY_MIN,
    FLOOR_SIZE,
    FLOOR_RENDER_VISIBLE,
    FLOOR_VIEWPORT_VISIBLE,
    USE_SOFT_BACKDROP,
    BACKDROP_SIZE,
    BACKDROP_LOCATION,
    BACKDROP_ROT_X,
    USE_INVISIBLE_COLLISION_PLANE,
    INVISIBLE_COLLISION_PLANE_SIZE,
    INVISIBLE_COLLISION_PLANE_Z,
)
from materials import (
    build_reflective_floor_material,
    build_invisible_surface_material,
    build_soft_backdrop_material,
)
from scene_utils import create_controller_empty


def configure_world(scene):
    world = bpy.data.worlds.new("PeaceWorld") if scene.world is None else scene.world
    scene.world = world
    world.use_nodes = True

    nodes = world.node_tree.nodes
    links = world.node_tree.links

    for n in list(nodes):
        nodes.remove(n)

    out = nodes.new("ShaderNodeOutputWorld")
    out.location = (900, 0)

    if USE_HDRI_WORLD and Path(HDRI_PATH).exists():
        texcoord = nodes.new("ShaderNodeTexCoord")
        texcoord.location = (-1200, 0)

        mapping = nodes.new("ShaderNodeMapping")
        mapping.location = (-980, 0)
        mapping.inputs["Rotation"].default_value[2] = HDRI_ROT_Z

        env = nodes.new("ShaderNodeTexEnvironment")
        env.location = (-720, 0)
        env.image = bpy.data.images.load(str(HDRI_PATH), check_existing=True)

        bg_hdri = nodes.new("ShaderNodeBackground")
        bg_hdri.location = (-420, 80)
        bg_hdri.inputs["Strength"].default_value = HDRI_STRENGTH

        bg_black = nodes.new("ShaderNodeBackground")
        bg_black.location = (-420, -140)
        bg_black.inputs["Color"].default_value = (0.0, 0.0, 0.0, 1.0)
        bg_black.inputs["Strength"].default_value = 1.0

        light_path = nodes.new("ShaderNodeLightPath")
        light_path.location = (-720, -220)

        mix = nodes.new("ShaderNodeMixShader")
        mix.location = (-120, 0)

        links.new(texcoord.outputs["Generated"], mapping.inputs["Vector"])
        links.new(mapping.outputs["Vector"], env.inputs["Vector"])
        links.new(env.outputs["Color"], bg_hdri.inputs["Color"])

        links.new(light_path.outputs["Is Camera Ray"], mix.inputs[0])
        links.new(bg_hdri.outputs["Background"], mix.inputs[1])
        links.new(bg_black.outputs["Background"], mix.inputs[2])
        links.new(mix.outputs["Shader"], out.inputs["Surface"])
    else:
        bg = nodes.new("ShaderNodeBackground")
        bg.location = (260, 0)
        bg.inputs["Strength"].default_value = WORLD_STRENGTH
        bg.inputs["Color"].default_value = PEACE_PALETTE["twilight_blue"]
        links.new(bg.outputs["Background"], out.inputs["Surface"])

    return world


def create_floor_and_backdrop():
    floor_mat, floor_rough_output = build_reflective_floor_material()

    bpy.ops.mesh.primitive_plane_add(size=FLOOR_SIZE, location=(0, 0, 0))
    floor = bpy.context.active_object
    floor.name = "PeaceFloor"
    floor.data.materials.append(floor_mat)
    floor.hide_render = not FLOOR_RENDER_VISIBLE
    floor.hide_viewport = not FLOOR_VIEWPORT_VISIBLE

    invisible_plane = None
    if USE_INVISIBLE_COLLISION_PLANE:
        invisible_mat = build_invisible_surface_material("InvisibleParticleFloorMaterial")
        bpy.ops.mesh.primitive_plane_add(
            size=INVISIBLE_COLLISION_PLANE_SIZE,
            location=(0, 0, INVISIBLE_COLLISION_PLANE_Z),
        )
        invisible_plane = bpy.context.active_object
        invisible_plane.name = "InvisibleParticleFloor"
        invisible_plane.data.materials.append(invisible_mat)
        invisible_plane.hide_render = True
        invisible_plane.hide_viewport = True
        invisible_plane.hide_select = True

    backdrop = None
    backdrop_controls = {}
    backdrop_controller = None

    if USE_SOFT_BACKDROP:
        backdrop_mat, backdrop_controls = build_soft_backdrop_material()
        bpy.ops.mesh.primitive_plane_add(
            size=BACKDROP_SIZE,
            location=BACKDROP_LOCATION,
            rotation=(BACKDROP_ROT_X, 0.0, 0.0),
        )
        backdrop = bpy.context.active_object
        backdrop.name = "SoftRhythmBackdrop"
        backdrop.data.materials.append(backdrop_mat)
        backdrop.hide_select = True

        try:
            backdrop.visible_shadow = False
        except Exception:
            pass

        backdrop_controller = create_controller_empty(
            "BackdropPulseController",
            location=BACKDROP_LOCATION,
            display_size=0.35,
            hide_view=True,
        )

    return {
        "floor": floor,
        "floor_material": floor_mat,
        "floor_rough_socket": floor_rough_output,
        "invisible_particle_floor": invisible_plane,
        "backdrop": backdrop,
        "backdrop_controller": backdrop_controller,
        "backdrop_controls": backdrop_controls,
        "backdrop_base_scale": backdrop.scale.copy() if backdrop else None,
        "backdrop_base_location": backdrop.location.copy() if backdrop else None,
    }


def create_area_lights():
    lights = []

    positions = [
        (-6.0, -5.8, 5.8),
        (6.0, -5.8, 5.8),
        (0.0, 7.6, 4.8),
    ]
    colors = [
        PEACE_PALETTE["soft_teal"],
        PEACE_PALETTE["muted_gold"],
        PEACE_PALETTE["dust_rose"],
    ]

    for idx, (pos, col) in enumerate(zip(positions, colors)):
        bpy.ops.object.light_add(type='AREA', location=pos)
        light = bpy.context.active_object
        light.name = f"AreaLight_{idx:02d}"
        light.data.energy = LIGHT_ENERGY_MIN
        light.data.color = (col[0], col[1], col[2])
        light.scale = (4.5, 4.5, 4.5)
        lights.append(light)

    return lights
