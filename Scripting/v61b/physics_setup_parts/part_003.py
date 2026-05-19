def create_physics_accents(parent=None):
    floor = bpy.data.objects.get("PeaceFloor")
    invisible_floor = bpy.data.objects.get("InvisibleParticleFloor")
    add_particle_collision(floor)
    add_particle_collision(invisible_floor)
    rhythm_particles = create_rhythm_particle_physics(parent=parent)

    if not USE_PHYSICS_ACCENTS:
        return {
            "accents": [],
            "force_obj": None,
            "turb_obj": None,
            "vortex_obj": None,
            "wind_left": None,
            "wind_right": None,
            "rhythm_particles": rhythm_particles,
        }

    accents = []

    if floor:
        add_passive_rigidbody(floor)

    bpy.ops.object.effector_add(type="FORCE", location=(0, 0, PRIMARY_BASE_Z + 1.20))
    force_obj = bpy.context.active_object
    force_obj.name = "HeroGravityField"
    force_obj.field.strength = -HERO_GRAVITY_STRENGTH_MIN
    force_obj.field.flow = 1.0
    force_obj.field.noise = 0.10
    force_obj.field.falloff_power = 1.55

    bpy.ops.object.effector_add(type="TURBULENCE", location=(0, 0, PRIMARY_BASE_Z + 1.50))
    turb_obj = bpy.context.active_object
    turb_obj.name = "AtmosphereTurbulence"
    turb_obj.field.strength = TURB_STRENGTH_MIN
    turb_obj.field.size = 2.0
    turb_obj.field.flow = 0.45

    bpy.ops.object.effector_add(type="VORTEX", location=(0, 0, PRIMARY_BASE_Z + 1.00))
    vortex_obj = bpy.context.active_object
    vortex_obj.name = "OrbitVortex"
    vortex_obj.rotation_euler.x = math.radians(90.0)
    vortex_obj.field.strength = VORTEX_STRENGTH_MIN

    bpy.ops.object.effector_add(type="WIND", location=(-3.0, -1.2, PRIMARY_BASE_Z + 1.8))
    wind_left = bpy.context.active_object
    wind_left.name = "WindLeft"
    wind_left.rotation_euler = (math.radians(90), 0, math.radians(20))
    wind_left.field.strength = 0.0
    wind_left.field.flow = 1.0

    bpy.ops.object.effector_add(type="WIND", location=(3.0, -1.2, PRIMARY_BASE_Z + 1.8))
    wind_right = bpy.context.active_object
    wind_right.name = "WindRight"
    wind_right.rotation_euler = (math.radians(90), 0, math.radians(-20))
    wind_right.field.strength = 0.0
    wind_right.field.flow = 1.0

    radius_span = max(0.01, PHYSICS_ORBIT_RADIUS_MAX - PHYSICS_ORBIT_RADIUS_MIN)
    for i in range(PHYSICS_ACCENT_COUNT):
        shell_t = (i % 6) / 5.0
        radius = PHYSICS_ORBIT_RADIUS_MIN + radius_span * shell_t + random.uniform(-0.08, 0.10)
        angle = (i / max(1, PHYSICS_ACCENT_COUNT)) * math.tau + random.uniform(-0.18, 0.18)
        z_offset = random.uniform(-0.52, 0.88)
        z = PRIMARY_BASE_Z + 1.02 + z_offset

        x = math.cos(angle) * radius
        y = math.sin(angle) * radius
        loc = (x, y, z)

        color = PALETTE_LIST[i % len(PALETTE_LIST)]

        anchor = create_hidden_anchor(f"PhysicsAnchor_{i:02d}", loc)

        bpy.ops.mesh.primitive_uv_sphere_add(
            radius=random.uniform(0.07, 0.12),
            location=loc,
        )
        obj = bpy.context.active_object
        obj.name = f"PhysicsAccent_{i:02d}"

        mat = build_variant_material(f"PhysicsAccentMat_{i:02d}", color)
        emit_socket = get_material_node_socket(mat, "VariantEmission", "Strength")
        mix_socket = get_material_node_socket(mat, "VariantEmissionMix", 0, is_output=True)
        if emit_socket is not None:
            emit_socket.default_value = PHYSICS_ACCENT_EMISSION_MIN
        if mix_socket is not None:
            mix_socket.default_value = PHYSICS_ACCENT_MIX_MIN
        obj.data.materials.append(mat)

        add_active_rigidbody(obj, mass=0.14)
        try:
            obj.rigid_body.kinematic = True
        except Exception:
            pass

        constraint = create_spring_constraint(
            f"PhysicsSpring_{i:02d}",
            anchor,
            obj,
            loc,
        )

        accents.append(
            {
                "object": obj,
                "anchor": anchor,
                "constraint": constraint,
                "base_location": obj.location.copy(),
                "base_rotation": obj.rotation_euler.copy(),
                "phase": random.uniform(0.0, math.tau),
                "orbit_radius": radius,
                "orbit_angle": angle,
                "orbit_z_offset": z_offset,
                "orbit_speed": random.uniform(
                    PHYSICS_ATOM_ORBIT_SPEED_MIN, PHYSICS_ATOM_ORBIT_SPEED_MAX
                ),
                "orbit_tilt": random.uniform(-0.42, 0.42),
                "micro_radius": random.uniform(
                    PHYSICS_ATOM_MICRO_WOBBLE * 0.45, PHYSICS_ATOM_MICRO_WOBBLE * 1.25
                ),
                "band": ["low", "mid", "high", "beat", "onset"][i % 5],
                "response": random.uniform(0.42, 1.0),
                "emission_socket": emit_socket,
                "mix_socket": mix_socket,
                "material": mat,
            }
        )

    return {
        "accents": accents,
        "force_obj": force_obj,
        "turb_obj": turb_obj,
        "vortex_obj": vortex_obj,
        "wind_left": wind_left,
        "wind_right": wind_right,
        "rhythm_particles": rhythm_particles,
    }
