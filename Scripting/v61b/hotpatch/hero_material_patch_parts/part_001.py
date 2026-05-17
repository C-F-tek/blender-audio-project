import math

import bpy

from .common import cfg_value, clear_animation, keyframe_if_possible

HERO_MATERIAL_EMISSION_MIN = cfg_value("HERO_MATERIAL_EMISSION_MIN", 0.18)
HERO_MATERIAL_EMISSION_MAX = cfg_value("HERO_MATERIAL_EMISSION_MAX", 0.92)
HERO_MATERIAL_SELF_LIGHT_MIN = cfg_value("HERO_MATERIAL_SELF_LIGHT_MIN", 0.018)
HERO_MATERIAL_SELF_LIGHT_MAX = cfg_value("HERO_MATERIAL_SELF_LIGHT_MAX", 0.26)
HERO_MATERIAL_BUMP_MIN = cfg_value("HERO_MATERIAL_BUMP_MIN", 0.010)
HERO_MATERIAL_BUMP_MAX = cfg_value("HERO_MATERIAL_BUMP_MAX", 0.065)
HERO_MATERIAL_ROUGHNESS_MIN = cfg_value("HERO_MATERIAL_ROUGHNESS_MIN", 0.20)
HERO_MATERIAL_ROUGHNESS_MAX = cfg_value("HERO_MATERIAL_ROUGHNESS_MAX", 0.58)
HERO_MATERIAL_NOISE_SCALE_MIN = cfg_value("HERO_MATERIAL_NOISE_SCALE_MIN", 4.0)
HERO_MATERIAL_NOISE_SCALE_MAX = cfg_value("HERO_MATERIAL_NOISE_SCALE_MAX", 13.5)
HERO_MATERIAL_MAPPING_DRIFT = cfg_value("HERO_MATERIAL_MAPPING_DRIFT", 0.18)
PEACE_PALETTE = cfg_value(
    "PEACE_PALETTE",
    {
        "muted_gold": (0.720, 0.620, 0.340, 1.0),
        "warm_white": (0.940, 0.930, 0.900, 1.0),
    },
)


def find_principled_node(material):
    if material is None or not material.use_nodes:
        return None
    for node in material.node_tree.nodes:
        if node.type == "BSDF_PRINCIPLED":
            return node
    return None


def get_node_input(node, *names):
    if node is None:
        return None
    for name in names:
        if name in node.inputs:
            return node.inputs[name]
    return None


def link_node_sockets(links, output_socket, input_socket, replace_existing=False):
    if output_socket is None or input_socket is None:
        return False
    try:
        if replace_existing:
            for link in list(input_socket.links):
                links.remove(link)
        elif input_socket.is_linked:
            return False
        links.new(output_socket, input_socket)
        return True
    except Exception:
        return False


def get_or_create_node(nodes, node_type, name, location):
    node = nodes.get(name)
    if node is None:
        node = nodes.new(node_type)
        node.name = name
        node.location = location
    return node


def get_or_create_value(nodes, name, label, location, default):
    node = nodes.get(name)
    if node is None:
        node = nodes.new("ShaderNodeValue")
        node.name = name
        node.label = label
        node.location = location
    node.outputs[0].default_value = default
    return node


def find_material_output(material):
    fallback = None
    for node in material.node_tree.nodes:
        if node.type != "OUTPUT_MATERIAL":
            continue
        if fallback is None:
            fallback = node
        if getattr(node, "is_active_output", False):
            return node
    return fallback


def ensure_surface_light_layer(material, principled):
    nodes = material.node_tree.nodes
    links = material.node_tree.links
    output = find_material_output(material)
    if output is None or "Surface" not in output.inputs:
        return None

    self_light = get_or_create_value(
        nodes,
        "HeroMatSelfLightValue",
        "Material-preserving edge light",
        (-520, 445),
        HERO_MATERIAL_SELF_LIGHT_MIN,
    )

    layer = get_or_create_node(
        nodes,
        "ShaderNodeLayerWeight",
        "HeroMatSelfLightFacing",
        (-300, 470),
    )

    edge_ramp = get_or_create_node(
        nodes,
        "ShaderNodeValToRGB",
        "HeroMatSelfLightRamp",
        (-95, 450),
    )
    edge_ramp.color_ramp.elements[0].position = 0.18
    edge_ramp.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    edge_ramp.color_ramp.elements[1].position = 0.84
    edge_ramp.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)

    edge_mul = get_or_create_node(
        nodes,
        "ShaderNodeMath",
        "HeroMatSelfLightEdgeMultiply",
        (125, 445),
    )
    edge_mul.operation = "MULTIPLY"

    emission = get_or_create_node(
        nodes,
        "ShaderNodeEmission",
        "HeroMatSelfLightEmission",
        (350, 385),
    )
    emission.inputs["Color"].default_value = PEACE_PALETTE["muted_gold"]

    add_shader = get_or_create_node(
        nodes,
        "ShaderNodeAddShader",
        "HeroMatSelfLightAdd",
        (620, 120),
    )

    link_node_sockets(links, self_light.outputs[0], edge_mul.inputs[0], replace_existing=True)
    link_node_sockets(
        links, layer.outputs.get("Fresnel"), edge_ramp.inputs["Fac"], replace_existing=True
    )
    link_node_sockets(links, edge_ramp.outputs["Color"], edge_mul.inputs[1], replace_existing=True)
    link_node_sockets(
        links, edge_mul.outputs[0], emission.inputs["Strength"], replace_existing=True
    )
    link_node_sockets(
        links, emission.outputs["Emission"], add_shader.inputs[1], replace_existing=True
    )

    surface_input = output.inputs["Surface"]
    if surface_input.is_linked and surface_input.links[0].from_node == add_shader:
        return self_light.outputs[0]

    original_socket = None
    if surface_input.is_linked:
        original_socket = surface_input.links[0].from_socket
        for link in list(surface_input.links):
            links.remove(link)
    elif "BSDF" in principled.outputs:
        original_socket = principled.outputs["BSDF"]

    link_node_sockets(links, original_socket, add_shader.inputs[0], replace_existing=True)
    link_node_sockets(links, add_shader.outputs["Shader"], surface_input, replace_existing=True)
    return self_light.outputs[0]


def hero_meshes():
    root = bpy.data.objects.get("HeroRoot")
    if root is None:
        return []

    meshes = [obj for obj in root.children_recursive if obj.type == "MESH"]
    if root.type == "MESH":
        meshes.append(root)
    return meshes


def lift_principled_material(principled):
    base_input = get_node_input(principled, "Base Color")
    if base_input is not None:
        try:
            base = base_input.default_value
            base[0] = min(1.0, max(0.20, base[0] * 0.82 + 0.14))
            base[1] = min(1.0, max(0.22, base[1] * 0.86 + 0.11))
            base[2] = min(1.0, max(0.22, base[2] * 0.90 + 0.09))
            if len(base) > 3:
                base[3] = 1.0
        except Exception:
            pass

    metallic = get_node_input(principled, "Metallic")
    if metallic is not None:
        try:
            metallic.default_value = min(metallic.default_value, 0.22)
        except Exception:
            pass

    emission_color = get_node_input(principled, "Emission Color", "Emission")
    if emission_color is not None:
        try:
            emission_color.default_value = PEACE_PALETTE["muted_gold"]
        except Exception:
            pass


def ensure_hero_controls(material):
    material.use_nodes = True
    material["spaziotempo_self_lit"] = True

    principled = find_principled_node(material)
    if principled is None:
        return None

    lift_principled_material(principled)

    nodes = material.node_tree.nodes
    links = material.node_tree.links
    emission_input = get_node_input(principled, "Emission Strength")
    roughness_input = get_node_input(principled, "Roughness")
    normal_input = get_node_input(principled, "Normal")

    emission_value = get_or_create_value(
        nodes,
        "HeroMatEmissionValue",
        "Audio Emission",
        (-520, 280),
        HERO_MATERIAL_EMISSION_MIN,
    )
    roughness_value = get_or_create_value(
        nodes,
        "HeroMatRoughnessValue",
        "Audio Roughness",
        (-520, 100),
        HERO_MATERIAL_ROUGHNESS_MAX,
    )
    bump_value = get_or_create_value(
        nodes,
        "HeroMatBumpStrength",
        "Audio Bump",
        (-520, -110),
        HERO_MATERIAL_BUMP_MIN,
    )

    mapping = nodes.get("HeroMatAudioMapping")
    if mapping is None:
        mapping = nodes.new("ShaderNodeMapping")
        mapping.name = "HeroMatAudioMapping"
        mapping.location = (-720, -220)

    texcoord = nodes.get("HeroMatTextureCoords")
    if texcoord is None:
        texcoord = nodes.new("ShaderNodeTexCoord")
        texcoord.name = "HeroMatTextureCoords"
        texcoord.location = (-930, -220)

    noise = nodes.get("HeroMatAudioNoise")
    if noise is None:
        noise = nodes.new("ShaderNodeTexNoise")
        noise.name = "HeroMatAudioNoise"
        noise.location = (-500, -260)
        noise.inputs["Detail"].default_value = 12.0
        noise.inputs["Roughness"].default_value = 0.62
    noise.inputs["Scale"].default_value = HERO_MATERIAL_NOISE_SCALE_MIN

    bump = nodes.get("HeroMatAudioBump")
    if bump is None:
        bump = nodes.new("ShaderNodeBump")
        bump.name = "HeroMatAudioBump"
        bump.location = (-245, -215)
        bump.inputs["Distance"].default_value = 0.28

    link_node_sockets(links, emission_value.outputs[0], emission_input, replace_existing=True)
    link_node_sockets(links, roughness_value.outputs[0], roughness_input, replace_existing=True)
    link_node_sockets(links, texcoord.outputs.get("Generated"), mapping.inputs.get("Vector"))
    link_node_sockets(links, mapping.outputs.get("Vector"), noise.inputs.get("Vector"))
    link_node_sockets(links, noise.outputs.get("Fac"), bump.inputs.get("Height"))
    link_node_sockets(
        links, bump_value.outputs[0], bump.inputs.get("Strength"), replace_existing=True
    )
    link_node_sockets(links, bump.outputs.get("Normal"), normal_input)

    self_light_socket = ensure_surface_light_layer(material, principled)

    return {
        "material": material,
        "node_tree": material.node_tree,
        "emission_socket": emission_value.outputs[0],
        "self_light_socket": self_light_socket,
        "roughness_socket": roughness_value.outputs[0],
        "bump_socket": bump_value.outputs[0],
        "noise_scale_socket": noise.inputs["Scale"],
        "mapping_location_socket": mapping.inputs["Location"],
        "mapping_rotation_socket": mapping.inputs["Rotation"],
    }


def collect_hero_controls():
    controls = []
    seen = set()

    for obj in hero_meshes():
        for slot in obj.material_slots:
            mat = slot.material
            if mat is None or mat.name in seen:
                continue
            seen.add(mat.name)
            control = ensure_hero_controls(mat)
            if control is not None:
                controls.append(control)

    return controls
