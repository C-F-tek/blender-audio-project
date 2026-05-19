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
