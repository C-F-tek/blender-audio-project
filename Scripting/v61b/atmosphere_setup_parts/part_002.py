def create_energy_ribbons(parent=None):
    ribbons = []

    for i in range(RIBBON_COUNT):
        bpy.ops.curve.primitive_bezier_circle_add(location=(0, 0, PRIMARY_BASE_Z + 1.05 + i * 0.20))
        ribbon = bpy.context.active_object
        ribbon.name = f"EnergyRibbon_{i:02d}"
        ribbon.scale = (2.55 + i * 0.30, 1.35 + i * 0.14, 1.0)
        ribbon.rotation_euler = (
            math.radians(72 + i * 18),
            math.radians(18 + i * 10),
            math.radians(i * 30),
        )

        ribbon.data.bevel_depth = 0.020 + i * 0.004
        ribbon.data.resolution_u = 32

        color = PALETTE_LIST[(i + 2) % len(PALETTE_LIST)]
        mat, emit_socket = build_ribbon_material(f"EnergyRibbonMat_{i:02d}", color)
        ribbon.data.materials.append(mat)

        if parent is not None:
            ribbon.parent = parent

        ribbons.append(
            {
                "object": ribbon,
                "emit_socket": emit_socket,
                "base_rot": ribbon.rotation_euler.copy(),
                "base_loc": ribbon.location.copy(),
                "base_scale": ribbon.scale.copy(),
                "phase": i * 1.15,
            }
        )

    return ribbons


def create_variants(hero_root, parent=None):
    variants = []

    if not CREATE_VARIANTS:
        return variants

    for i in range(VARIANT_COUNT):
        ang = (math.tau / VARIANT_COUNT) * i
        x = math.cos(ang) * VARIANT_RING_RADIUS
        y = math.sin(ang) * VARIANT_RING_RADIUS

        dup = duplicate_hierarchy(hero_root, f"HeroVariantRoot_{i:02d}")
        if parent is not None:
            dup.parent = parent

        dup.location = (x, y, PRIMARY_BASE_Z + 0.25)
        scale = random.uniform(VARIANT_SCALE_MIN, VARIANT_SCALE_MAX)
        dup.scale = (scale, scale, scale)
        dup.rotation_euler = (0.0, 0.0, ang + random.uniform(-0.24, 0.24))

        color = PALETTE_LIST[i % len(PALETTE_LIST)]
        mat = build_variant_material(f"VariantPeaceMat_{i:02d}", color)
        assign_material_to_hierarchy(dup, mat)

        variants.append(
            {
                "root": dup,
                "angle": ang,
                "base_location": dup.location.copy(),
                "base_scale": scale,
            }
        )

    return variants


def create_atmosphere_cube(parent=None):
    mat, controls = build_atmosphere_volume_material()

    bpy.ops.mesh.primitive_cube_add(location=(0, 0, 3.0))
    cube = bpy.context.active_object
    cube.name = "AtmosphereCube"
    cube["spaziotempo_volume_container"] = True
    cube.scale = (
        ATMOSPHERE_CUBE_SIZE * 0.5,
        ATMOSPHERE_CUBE_SIZE * 0.5,
        ATMOSPHERE_CUBE_SIZE * 0.5,
    )
    cube.data.materials.append(mat)
    cube.display_type = "WIRE"
    cube.hide_select = True
    cube.hide_render = not FOG_VOLUME_ENABLED
    cube.hide_viewport = not FOG_VOLUME_VIEWPORT_VISIBLE

    if parent is not None:
        cube.parent = parent

    try:
        controls["ramp_low_ctrl"].position = FOG_RAMP_LOW_BASE
        controls["ramp_high_ctrl"].position = FOG_RAMP_HIGH_BASE
    except Exception:
        pass

    controller = create_controller_empty(
        "FogPulseController",
        location=cube.location.copy(),
        display_size=0.42,
        hide_view=True,
    )
    if parent is not None:
        controller.parent = parent

    filaments = ensure_fog_filaments(parent=parent)

    return {
        "object": cube,
        "material": mat,
        "controller": controller,
        "filaments": filaments,
        "base_location": cube.location.copy(),
        "base_scale": cube.scale.copy(),
        "density_socket": controls["density_socket"],
        "emission_socket": controls["emission_socket"],
        "noise_scale_socket": controls["noise_scale_socket"],
        "noise_detail_socket": controls.get("noise_detail_socket"),
        "noise_roughness_socket": controls.get("noise_roughness_socket"),
        "clump_noise_scale_socket": controls.get("clump_noise_scale_socket"),
        "clump_noise_detail_socket": controls.get("clump_noise_detail_socket"),
        "clump_noise_roughness_socket": controls.get("clump_noise_roughness_socket"),
        "mapping_location_socket": controls["mapping_location_socket"],
        "mapping_scale_socket": controls.get("mapping_scale_socket"),
        "mapping_rotation_socket": controls.get("mapping_rotation_socket"),
        "wave_scale_socket": controls.get("wave_scale_socket"),
        "wave_distortion_socket": controls.get("wave_distortion_socket"),
        "wave_phase_socket": controls.get("wave_phase_socket"),
        "wave_weight_socket": controls.get("wave_weight_socket"),
        "ramp_low_ctrl": controls["ramp_low_ctrl"],
        "ramp_high_ctrl": controls["ramp_high_ctrl"],
        "clump_ramp_low_ctrl": controls.get("clump_ramp_low_ctrl"),
        "clump_ramp_high_ctrl": controls.get("clump_ramp_high_ctrl"),
        "volume_color_socket": controls.get("volume_color_socket"),
        "volume_anisotropy_socket": controls.get("volume_anisotropy_socket"),
    }


def create_mist_particles(parent=None):
    particles = []
    if not USE_MIST_PARTICLES:
        return particles

    bpy.ops.object.empty_add(type="PLAIN_AXES", location=(0, 0, 0))
    root = bpy.context.active_object
    root.name = "MistParticlesRoot"

    if parent is not None:
        root.parent = parent

    color_choices = [
        PEACE_PALETTE["warm_white"],
        PEACE_PALETTE["soft_teal"],
        PEACE_PALETTE["muted_gold"],
    ]

    for i in range(MIST_PARTICLE_COUNT):
        radius = random.uniform(1.1, 4.4)
        angle = random.uniform(0.0, math.tau)
        z = random.uniform(0.55, 3.2)

        x = math.cos(angle) * radius
        y = math.sin(angle) * radius

        bpy.ops.mesh.primitive_ico_sphere_add(
            subdivisions=1,
            radius=random.uniform(0.03, 0.08),
            location=(x, y, z),
        )
        obj = bpy.context.active_object
        obj.name = f"MistParticle_{i:02d}"
        obj.parent = root

        color = random.choice(color_choices)
        mat, em_socket, mix_socket = build_mist_particle_material(f"MistParticleMat_{i:02d}", color)
        obj.data.materials.append(mat)

        particles.append(
            {
                "object": obj,
                "material": mat,
                "emission_socket": em_socket,
                "mix_socket": mix_socket,
                "base_location": obj.location.copy(),
                "phase": random.uniform(0.0, math.tau),
                "base_scale": random.uniform(MIST_SCALE_MIN, MIST_SCALE_MAX),
            }
        )

    return particles
