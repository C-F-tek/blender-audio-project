from pathlib import Path

import bpy
from mathutils import Vector
from scene_utils import create_controller_empty

from config import (
    HERO_DEFORM_CONTROLLER_Z,
    HERO_DEFORM_DETAIL_DIM_FACTOR,
    HERO_DEFORM_DETAIL_NOISE_SIZE,
    HERO_DEFORM_DETAIL_STRENGTH_MAX,
    HERO_DEFORM_MAIN_DIM_FACTOR,
    HERO_DEFORM_NOISE_CONTRAST,
    HERO_DEFORM_NOISE_SIZE,
    HERO_DEFORM_STRENGTH_MAX,
    HERO_DEFORM_STRENGTH_MIN,
    HERO_DEFORM_SUBDIV_RENDER,
    HERO_DEFORM_SUBDIV_VIEW,
    HERO_DEFORM_TWIST_MAX,
    HERO_DEFORM_WAVE_DIM_FACTOR,
    HERO_DEFORM_WAVE_HEIGHT_MAX,
    HERO_MATERIAL_BUMP_MIN,
    HERO_MATERIAL_EMISSION_MIN,
    HERO_MATERIAL_NOISE_SCALE_MIN,
    HERO_MATERIAL_ROUGHNESS_MAX,
    HERO_MATERIAL_SELF_LIGHT_MIN,
    PEACE_PALETTE,
    PRIMARY_ASSET_DIR,
    PRIMARY_BASE_Z,
    PRIMARY_TARGET_SIZE,
    SECONDARY_ASSET_DIR,
    SECONDARY_BASE_OFFSET_X,
    SECONDARY_BASE_OFFSET_Y,
    SECONDARY_BASE_OFFSET_Z,
    SECONDARY_BASE_Z,
    SECONDARY_TARGET_SIZE,
    SUPPORTED_ASSET_EXTENSIONS,
    USE_HERO_MATERIAL_AUDIO_NODES,
    USE_HERO_MESH_DEFORM,
    USE_SECONDARY_ASSET,
)


def find_asset_file(asset_dir: Path) -> Path:
    if not asset_dir.exists():
        raise FileNotFoundError(f"Cartella asset non trovata: {asset_dir}")

    files = []
    for ext in SUPPORTED_ASSET_EXTENSIONS:
        files.extend(asset_dir.rglob(f"*{ext}"))

    if not files:
        raise FileNotFoundError(
            f"Nessun asset supportato trovato in: {asset_dir}\n"
            f"Estensioni cercate: {SUPPORTED_ASSET_EXTENSIONS}"
        )

    priority = {".fbx": 0, ".glb": 1, ".gltf": 2, ".obj": 3, ".blend": 4}
    files.sort(key=lambda p: (priority.get(p.suffix.lower(), 99), str(p)))
    return files[0]


def import_asset_file(asset_file: Path):
    ext = asset_file.suffix.lower()
    before = set(obj.name for obj in bpy.data.objects)

    if ext == ".fbx":
        bpy.ops.import_scene.fbx(filepath=str(asset_file))
    elif ext in {".glb", ".gltf"}:
        bpy.ops.import_scene.gltf(filepath=str(asset_file))
    elif ext == ".obj":
        try:
            bpy.ops.wm.obj_import(filepath=str(asset_file))
        except Exception:
            bpy.ops.import_scene.obj(filepath=str(asset_file))
    elif ext == ".blend":
        with bpy.data.libraries.load(str(asset_file), link=False) as (data_from, data_to):
            data_to.objects = data_from.objects
        for obj in data_to.objects:
            if obj is not None:
                bpy.context.collection.objects.link(obj)
    else:
        raise RuntimeError(f"Formato non supportato: {ext}")

    after = set(obj.name for obj in bpy.data.objects)
    new_names = after - before
    imported = [bpy.data.objects[name] for name in new_names if name in bpy.data.objects]

    if not imported:
        raise RuntimeError(f"Import completato ma nessun oggetto rilevato: {asset_file}")

    return imported


def get_world_bbox(objects):
    coords = []
    depsgraph = bpy.context.evaluated_depsgraph_get()

    for obj in objects:
        if obj.type not in {"MESH", "CURVE", "SURFACE", "META", "FONT", "EMPTY", "ARMATURE"}:
            continue

        if obj.type == "EMPTY":
            coords.append(obj.matrix_world.translation.copy())
            continue

        try:
            obj_eval = obj.evaluated_get(depsgraph)
            bbox = [obj_eval.matrix_world @ Vector(corner) for corner in obj_eval.bound_box]
            coords.extend(bbox)
        except Exception:
            try:
                bbox = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
                coords.extend(bbox)
            except Exception:
                coords.append(obj.matrix_world.translation.copy())

    if not coords:
        return Vector((0, 0, 0)), Vector((1, 1, 1)), Vector((0, 0, 0)), Vector((0, 0, 0))

    min_v = Vector((min(v.x for v in coords), min(v.y for v in coords), min(v.z for v in coords)))
    max_v = Vector((max(v.x for v in coords), max(v.y for v in coords), max(v.z for v in coords)))
    center = (min_v + max_v) * 0.5
    size = max_v - min_v
    return center, size, min_v, max_v


def create_scene_core():
    bpy.ops.object.empty_add(type="PLAIN_AXES", location=(0, 0, 0))
    root = bpy.context.active_object
    root.name = "SceneCore"
    return root


def make_asset_root(name):
    bpy.ops.object.empty_add(type="PLAIN_AXES", location=(0, 0, 0))
    root = bpy.context.active_object
    root.name = name
    return root


def parent_objects_keep_transform(objects, parent):
    for obj in objects:
        if obj == parent:
            continue
        mw = obj.matrix_world.copy()
        obj.parent = parent
        obj.matrix_world = mw


def center_and_scale_asset(root, objects, target_size, base_z):
    bpy.context.view_layer.update()

    center, size, min_v, _ = get_world_bbox(objects)
    max_dim = max(size.x, size.y, size.z)
    if max_dim <= 0.0001:
        max_dim = 1.0

    scale_factor = target_size / max_dim
    root.scale = (scale_factor, scale_factor, scale_factor)

    bpy.context.view_layer.update()

    center, _, min_v, _ = get_world_bbox(objects)
    root.location.x += -center.x
    root.location.y += -center.y
    root.location.z += base_z - min_v.z

    bpy.context.view_layer.update()


def collect_meshes(objects):
    return [obj for obj in objects if obj.type == "MESH"]


def soften_materials_to_peace(meshes):
    for obj in meshes:
        for slot in obj.material_slots:
            mat = slot.material
            if mat is None or not mat.use_nodes:
                continue

            principled = None
            for node in mat.node_tree.nodes:
                if node.type == "BSDF_PRINCIPLED":
                    principled = node
                    break

            if principled is None:
                continue

            try:
                base = principled.inputs["Base Color"].default_value
                base[0] = min(1.0, max(0.18, base[0] * 0.84 + 0.12))
                base[1] = min(1.0, max(0.20, base[1] * 0.88 + 0.10))
                base[2] = min(1.0, max(0.20, base[2] * 0.92 + 0.08))
                metallic = get_node_input(principled, "Metallic")
                if metallic is not None:
                    metallic.default_value = min(metallic.default_value, 0.22)
                principled.inputs["Roughness"].default_value = min(
                    1.0, max(0.18, principled.inputs["Roughness"].default_value)
                )
            except Exception:
                pass


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


def find_material_output(material):
    if material is None or not material.use_nodes:
        return None
    fallback = None
    for node in material.node_tree.nodes:
        if node.type != "OUTPUT_MATERIAL":
            continue
        if fallback is None:
            fallback = node
        if getattr(node, "is_active_output", False):
            return node
    return fallback


def ensure_hero_surface_light_layer(mat, principled):
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    output = find_material_output(mat)
    if output is None or "Surface" not in output.inputs:
        return None

    self_light = get_or_create_node(
        nodes,
        "ShaderNodeValue",
        "HeroMatSelfLightValue",
        (-520, 445),
    )
    self_light.label = "Material-preserving edge light"
    self_light.outputs[0].default_value = HERO_MATERIAL_SELF_LIGHT_MIN

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
