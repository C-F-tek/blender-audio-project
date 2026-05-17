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


def get_local_mesh_extent(obj):
    try:
        corners = [Vector(corner) for corner in obj.bound_box]
        min_v = Vector(
            (min(v.x for v in corners), min(v.y for v in corners), min(v.z for v in corners))
        )
        max_v = Vector(
            (max(v.x for v in corners), max(v.y for v in corners), max(v.z for v in corners))
        )
        size = max_v - min_v
        return max(size.x, size.y, size.z, 0.001)
    except Exception:
        try:
            return max(obj.dimensions.x, obj.dimensions.y, obj.dimensions.z, 0.001)
        except Exception:
            return 1.0


def add_hero_material_audio_nodes(meshes):
    if not USE_HERO_MATERIAL_AUDIO_NODES:
        return []

    controls = []
    seen_materials = set()

    for obj in meshes:
        for slot in obj.material_slots:
            mat = slot.material
            if mat is None or not mat.use_nodes:
                continue

            mat_key = mat.name
            if mat_key in seen_materials:
                continue
            seen_materials.add(mat_key)

            principled = find_principled_node(mat)
            if principled is None:
                continue

            nodes = mat.node_tree.nodes
            links = mat.node_tree.links

            rough_input = get_node_input(principled, "Roughness")
            emission_color_input = get_node_input(principled, "Emission Color", "Emission")
            emission_strength_input = get_node_input(principled, "Emission Strength")
            normal_input = get_node_input(principled, "Normal")

            emission_value = nodes.new("ShaderNodeValue")
            emission_value.name = "HeroMatEmissionValue"
            emission_value.label = "Audio Emission"
            emission_value.location = (-520, 280)
            emission_value.outputs[0].default_value = HERO_MATERIAL_EMISSION_MIN

            roughness_value = nodes.new("ShaderNodeValue")
            roughness_value.name = "HeroMatRoughnessValue"
            roughness_value.label = "Audio Roughness"
            roughness_value.location = (-520, 100)
            roughness_value.outputs[0].default_value = HERO_MATERIAL_ROUGHNESS_MAX

            bump_value = nodes.new("ShaderNodeValue")
            bump_value.name = "HeroMatBumpStrength"
            bump_value.label = "Audio Bump"
            bump_value.location = (-520, -110)
            bump_value.outputs[0].default_value = HERO_MATERIAL_BUMP_MIN

            texcoord = nodes.new("ShaderNodeTexCoord")
            texcoord.name = "HeroMatTextureCoords"
            texcoord.location = (-930, -220)

            mapping = nodes.new("ShaderNodeMapping")
            mapping.name = "HeroMatAudioMapping"
            mapping.location = (-720, -220)

            noise = nodes.new("ShaderNodeTexNoise")
            noise.name = "HeroMatAudioNoise"
            noise.location = (-500, -260)
            noise.inputs["Scale"].default_value = HERO_MATERIAL_NOISE_SCALE_MIN
            noise.inputs["Detail"].default_value = 12.0
            noise.inputs["Roughness"].default_value = 0.62

            bump = nodes.new("ShaderNodeBump")
            bump.name = "HeroMatAudioBump"
            bump.location = (-245, -215)
            bump.inputs["Strength"].default_value = HERO_MATERIAL_BUMP_MIN
            bump.inputs["Distance"].default_value = 0.28

            try:
                if emission_color_input is not None:
                    emission_color_input.default_value = PEACE_PALETTE["muted_gold"]
            except Exception:
                pass

            self_light_socket = ensure_hero_surface_light_layer(mat, principled)

            link_node_sockets(
                links, emission_value.outputs[0], emission_strength_input, replace_existing=True
            )
            link_node_sockets(links, roughness_value.outputs[0], rough_input, replace_existing=True)
            link_node_sockets(
                links, texcoord.outputs.get("Generated"), mapping.inputs.get("Vector")
            )
            link_node_sockets(links, mapping.outputs.get("Vector"), noise.inputs.get("Vector"))
            link_node_sockets(links, noise.outputs.get("Fac"), bump.inputs.get("Height"))
            link_node_sockets(
                links, bump_value.outputs[0], bump.inputs.get("Strength"), replace_existing=True
            )
            link_node_sockets(links, bump.outputs.get("Normal"), normal_input)

            controls.append(
                {
                    "material": mat,
                    "node_tree": mat.node_tree,
                    "emission_socket": emission_value.outputs[0],
                    "self_light_socket": self_light_socket,
                    "roughness_socket": roughness_value.outputs[0],
                    "bump_socket": bump_value.outputs[0],
                    "noise_scale_socket": noise.inputs["Scale"],
                    "mapping_location_socket": mapping.inputs["Location"],
                    "mapping_rotation_socket": mapping.inputs["Rotation"],
                }
            )

    return controls


def duplicate_hierarchy(root, name_prefix):
    before = set(bpy.data.objects)

    for obj in bpy.data.objects:
        obj.select_set(False)

    root.select_set(True)
    for child in root.children_recursive:
        child.select_set(True)

    bpy.context.view_layer.objects.active = root
    bpy.ops.object.duplicate(linked=False)

    created = [obj for obj in bpy.data.objects if obj not in before]
    created_root = None

    for obj in created:
        if obj.type == "EMPTY":
            created_root = obj
            break

    if created_root is None:
        raise RuntimeError("Impossibile duplicare la gerarchia dell'asset.")

    created_root.name = name_prefix
    return created_root


def assign_material_to_hierarchy(root, material):
    meshes = [obj for obj in root.children_recursive if obj.type == "MESH"]
    if root.type == "MESH":
        meshes.append(root)

    for obj in meshes:
        obj.data.materials.clear()
        obj.data.materials.append(material)


def add_hero_mesh_deformers(asset_root, meshes):
    if not USE_HERO_MESH_DEFORM:
        return {
            "controller": None,
            "deformers": [],
        }

    controller = create_controller_empty(
        "HeroDeformController",
        location=(0, 0, HERO_DEFORM_CONTROLLER_Z),
        parent=asset_root,
        display_size=0.32,
        hide_view=True,
    )

    deformers = []
    for idx, obj in enumerate(meshes):
        local_extent = get_local_mesh_extent(obj)
        main_strength_max = max(
            HERO_DEFORM_STRENGTH_MAX, local_extent * HERO_DEFORM_MAIN_DIM_FACTOR
        )
        detail_strength_max = max(
            HERO_DEFORM_DETAIL_STRENGTH_MAX, local_extent * HERO_DEFORM_DETAIL_DIM_FACTOR
        )
        wave_height_max = max(
            HERO_DEFORM_WAVE_HEIGHT_MAX, local_extent * HERO_DEFORM_WAVE_DIM_FACTOR
        )

        try:
            subdiv = obj.modifiers.new("HeroAudioSubdivision", "SUBSURF")
            subdiv.levels = HERO_DEFORM_SUBDIV_VIEW
            subdiv.render_levels = HERO_DEFORM_SUBDIV_RENDER
        except Exception:
            subdiv = None

        try:
            tex = bpy.data.textures.new(f"HeroAudioDisplaceTexture_{idx:02d}", type="VORONOI")
        except Exception:
            try:
                tex = bpy.data.textures.new(f"HeroAudioDisplaceTexture_{idx:02d}", type="CLOUDS")
            except Exception:
                continue

        for attr, value in [
            ("noise_scale", HERO_DEFORM_NOISE_SIZE),
            ("intensity", 0.48),
            ("contrast", HERO_DEFORM_NOISE_CONTRAST),
        ]:
            try:
                setattr(tex, attr, value)
            except Exception:
                pass

        mod = obj.modifiers.new("HeroAudioMeshDisplace", "DISPLACE")
        mod.strength = HERO_DEFORM_STRENGTH_MIN
        mod.mid_level = 0.50
        mod.texture = tex

        try:
            mod.direction = "NORMAL"
        except Exception:
            pass

        try:
            mod.texture_coords = "OBJECT"
            mod.texture_coords_object = controller
        except Exception:
            pass

        try:
            mod.show_render = True
            mod.show_viewport = True
        except Exception:
            pass

        deformers.append(
            {
                "mesh": obj,
                "subdivision": subdiv,
                "modifier": mod,
                "texture": tex,
                "detail_modifier": None,
                "detail_texture": None,
                "wave_modifier": None,
                "twist_modifier": None,
                "phase": idx * 0.61,
                "main_strength_max": main_strength_max,
                "detail_strength_max": detail_strength_max,
                "wave_height_max": wave_height_max,
                "twist_angle_max": HERO_DEFORM_TWIST_MAX,
            }
        )

        try:
            detail_tex = bpy.data.textures.new(f"HeroAudioDetailTexture_{idx:02d}", type="CLOUDS")
            for attr, value in [
                ("noise_scale", HERO_DEFORM_DETAIL_NOISE_SIZE),
                ("noise_depth", 6),
                ("contrast", HERO_DEFORM_NOISE_CONTRAST),
            ]:
                try:
                    setattr(detail_tex, attr, value)
                except Exception:
                    pass

            detail = obj.modifiers.new("HeroAudioFineDisplace", "DISPLACE")
            detail.strength = HERO_DEFORM_STRENGTH_MIN
            detail.mid_level = 0.50
            detail.texture = detail_tex
            try:
                detail.direction = "NORMAL"
                detail.texture_coords = "OBJECT"
                detail.texture_coords_object = controller
            except Exception:
                pass

            deformers[-1]["detail_modifier"] = detail
            deformers[-1]["detail_texture"] = detail_tex
        except Exception:
            pass

        try:
            wave = obj.modifiers.new("HeroAudioSurfaceWave", "WAVE")
            wave.height = 0.0
            wave.width = 1.20
            wave.narrowness = 1.75
            wave.speed = 0.16
            try:
                wave.type = "RINGS"
                wave.use_x = True
                wave.use_y = True
                wave.use_normal = True
                wave.start_position_object = controller
            except Exception:
                pass

            deformers[-1]["wave_modifier"] = wave
        except Exception:
            pass

        try:
            twist = obj.modifiers.new("HeroAudioTwistDeform", "SIMPLE_DEFORM")
            twist.deform_method = "TWIST"
            twist.angle = 0.0
            try:
                twist.deform_axis = "Z"
            except Exception:
                pass
            try:
                twist.origin = controller
            except Exception:
                pass

            deformers[-1]["twist_modifier"] = twist
        except Exception:
            pass

    return {
        "controller": controller,
        "deformers": deformers,
    }


def _create_asset_from_dir(asset_dir, target_size, base_z, root_name, parent=None):
    asset_file = find_asset_file(asset_dir)
    imported_objects = import_asset_file(asset_file)

    asset_root = make_asset_root(root_name)
    parent_objects_keep_transform(imported_objects, asset_root)
    center_and_scale_asset(asset_root, imported_objects, target_size, base_z)

    if parent is not None:
        mw = asset_root.matrix_world.copy()
        asset_root.parent = parent
        asset_root.matrix_world = mw

    meshes = collect_meshes(imported_objects)
    soften_materials_to_peace(meshes)
    material_controls = add_hero_material_audio_nodes(meshes) if root_name == "HeroRoot" else []
    deform_data = (
        add_hero_mesh_deformers(asset_root, meshes)
        if root_name == "HeroRoot"
        else {
            "controller": None,
            "deformers": [],
        }
    )

    return {
        "asset_file": asset_file,
        "root": asset_root,
        "objects": imported_objects,
        "meshes": meshes,
        "deform_controller": deform_data["controller"],
        "deformers": deform_data["deformers"],
        "material_controls": material_controls,
        "base_scale": asset_root.scale.copy(),
        "base_location": asset_root.location.copy(),
        "base_rotation": asset_root.rotation_euler.copy(),
    }


def create_primary_asset(parent=None):
    return _create_asset_from_dir(
        asset_dir=PRIMARY_ASSET_DIR,
        target_size=PRIMARY_TARGET_SIZE,
        base_z=PRIMARY_BASE_Z,
        root_name="HeroRoot",
        parent=parent,
    )


def create_secondary_asset(parent=None):
    if not USE_SECONDARY_ASSET:
        return None

    if not SECONDARY_ASSET_DIR.exists():
        print(f"[WARN] Secondary asset dir non trovata: {SECONDARY_ASSET_DIR}")
        return None

    asset = _create_asset_from_dir(
        asset_dir=SECONDARY_ASSET_DIR,
        target_size=SECONDARY_TARGET_SIZE,
        base_z=SECONDARY_BASE_Z,
        root_name="SecondaryRoot",
        parent=parent,
    )

    root = asset["root"]
    root.location.x += SECONDARY_BASE_OFFSET_X
    root.location.y += SECONDARY_BASE_OFFSET_Y
    root.location.z += SECONDARY_BASE_OFFSET_Z

    bpy.context.view_layer.update()

    asset["base_scale"] = root.scale.copy()
    asset["base_location"] = root.location.copy()
    asset["base_rotation"] = root.rotation_euler.copy()

    return asset
