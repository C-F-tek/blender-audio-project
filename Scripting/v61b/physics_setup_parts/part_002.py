def create_particle_emitter(name, kind, invisible_mat):
    if kind == "sphere":
        bpy.ops.mesh.primitive_uv_sphere_add(
            segments=32,
            ring_count=16,
            radius=4.25,
            location=(0, 0, PRIMARY_BASE_Z + 1.00),
        )
    else:
        radius = RHYTHM_PARTICLE_EMITTER_RADIUS
        if kind == "wide_ring":
            radius *= 1.62
        bpy.ops.mesh.primitive_torus_add(
            major_radius=radius,
            minor_radius=0.036 if kind == "ring" else 0.022,
            major_segments=128,
            minor_segments=8,
            location=(0, 0, RHYTHM_PARTICLE_EMITTER_Z),
        )

    emitter = bpy.context.active_object
    emitter.name = name
    emitter.data.materials.append(invisible_mat)
    emitter.display_type = "WIRE"
    emitter.hide_select = True
    return emitter


def configure_particle_system(
    emitter,
    name,
    instance_obj,
    count,
    lifetime,
    particle_size,
    normal_factor,
    tangent_factor,
    brownian_factor,
    damping,
    child_count,
    child_percent,
    instance_collection=None,
):
    mod = emitter.modifiers.new(name=name, type="PARTICLE_SYSTEM")
    ps = mod.particle_system
    settings = ps.settings
    settings.name = f"{name}Settings"

    frame_end = max(1, int(bpy.context.scene.frame_end))

    settings.type = "EMITTER"
    settings.physics_type = "NEWTON"
    if instance_collection is not None:
        settings.render_type = "COLLECTION"
        set_if_available(settings, "instance_collection", instance_collection)
        set_if_available(settings, "use_collection_pick_random", True)
        set_if_available(settings, "use_whole_collection", False)
        set_if_available(settings, "use_collection_count", False)
    else:
        settings.render_type = "OBJECT"
        settings.instance_object = instance_obj
    settings.count = count
    settings.frame_start = 1
    settings.frame_end = frame_end
    settings.lifetime = lifetime
    settings.lifetime_random = 0.35
    settings.particle_size = particle_size
    settings.size_random = 0.72
    settings.normal_factor = normal_factor
    settings.tangent_factor = tangent_factor
    settings.brownian_factor = brownian_factor
    settings.damping = damping
    settings.factor_random = 0.68
    settings.show_unborn = False
    settings.use_dead = False
    settings.use_die_on_collision = False

    set_if_available(settings, "emit_from", "FACE")
    set_if_available(settings, "distribution", "RAND")
    set_if_available(settings, "use_emit_random", True)
    set_if_available(settings, "use_modifier_stack", True)
    set_if_available(settings, "use_rotations", True)
    set_if_available(settings, "rotation_mode", "VEL")
    set_if_available(settings, "angular_velocity_mode", "VELOCITY")
    set_if_available(settings, "angular_velocity_factor", 0.72)
    set_if_available(settings, "child_type", "INTERPOLATED")
    set_if_available(settings, "rendered_child_count", child_count)
    set_if_available(settings, "child_percent", child_percent)
    set_if_available(settings, "roughness_1_size", 0.65)
    set_if_available(settings, "roughness_1", 0.018)
    set_if_available(settings, "roughness_2_size", 0.34)
    set_if_available(settings, "roughness_2", 0.010)
    set_if_available(settings, "roughness_2_threshold", 0.42)
    set_if_available(settings, "display_percentage", 45)

    try:
        settings.effector_weights.gravity = 0.0
        settings.effector_weights.turbulence = 1.0
        settings.effector_weights.vortex = 1.0
        settings.effector_weights.wind = 1.0
    except Exception:
        pass

    return ps, settings


def create_rhythm_particle_physics(parent=None):
    if not USE_RHYTHM_PARTICLE_PHYSICS:
        return []

    bpy.ops.object.empty_add(type="PLAIN_AXES", location=(0, 0, 0))
    root = bpy.context.active_object
    root.name = "RhythmParticlePhysicsRoot"
    if parent is not None:
        root.parent = parent

    invisible_mat = build_invisible_emitter_material()

    spark_obj, spark_mat, spark_emit = create_particle_instance(
        "BeatSparkParticle",
        PEACE_PALETTE["warm_white"],
        0.40,
    )
    dust_obj, dust_mat, dust_emit = create_particle_instance(
        "OrbitDustParticle",
        PEACE_PALETTE["soft_teal"],
        0.18,
    )
    streak_obj, streak_mat, streak_emit = create_particle_instance(
        "HighStreakParticle",
        PEACE_PALETTE["muted_gold"],
        0.32,
        shape="streak",
    )
    letter_collection, letter_root, letter_sources = create_album_letter_particle_collection(
        parent=root
    )

    for obj in [spark_obj, dust_obj, streak_obj]:
        obj.parent = root

    pulse_emitter = create_particle_emitter("BeatPulseParticleEmitter", "ring", invisible_mat)
    dust_emitter = create_particle_emitter("OrbitDustParticleEmitter", "sphere", invisible_mat)
    streak_emitter = create_particle_emitter(
        "HighStreakParticleEmitter", "wide_ring", invisible_mat
    )
    letter_emitter = None
    if letter_collection is not None and letter_sources:
        letter_emitter = create_particle_emitter(
            "AlbumLetterParticleEmitter", "wide_ring", invisible_mat
        )

    for emitter in [pulse_emitter, dust_emitter, streak_emitter, letter_emitter]:
        if emitter is not None:
            emitter.parent = root

    _, pulse_settings = configure_particle_system(
        pulse_emitter,
        "BeatPulseParticleSystem",
        spark_obj,
        RHYTHM_PARTICLE_COUNT,
        RHYTHM_PARTICLE_LIFETIME,
        RHYTHM_PARTICLE_SIZE_MIN,
        RHYTHM_PARTICLE_NORMAL_MIN,
        RHYTHM_PARTICLE_TANGENT_MIN,
        RHYTHM_PARTICLE_BROWNIAN_MIN,
        0.13,
        3,
        40,
    )
    _, dust_settings = configure_particle_system(
        dust_emitter,
        "OrbitDustParticleSystem",
        dust_obj,
        RHYTHM_DUST_PARTICLE_COUNT,
        RHYTHM_DUST_LIFETIME,
        RHYTHM_PARTICLE_SIZE_MIN * 0.72,
        0.035,
        0.12,
        0.42,
        0.24,
        2,
        25,
    )
    _, streak_settings = configure_particle_system(
        streak_emitter,
        "HighStreakParticleSystem",
        streak_obj,
        RHYTHM_STREAK_PARTICLE_COUNT,
        max(42, int(RHYTHM_PARTICLE_LIFETIME * 0.70)),
        RHYTHM_PARTICLE_SIZE_MIN * 0.95,
        0.30,
        0.55,
        0.06,
        0.08,
        1,
        12,
    )
    letter_settings = []
    if letter_emitter is not None:
        per_letter_count = max(8, int(ALBUM_LETTER_PARTICLE_COUNT / max(1, len(letter_sources))))
        for idx, letter in enumerate(letter_sources):
            _, settings = configure_particle_system(
                letter_emitter,
                f"AlbumLetterParticleSystem_{idx:02d}",
                letter["object"],
                per_letter_count,
                ALBUM_LETTER_PARTICLE_LIFETIME,
                ALBUM_LETTER_PARTICLE_SIZE_MIN,
                0.16,
                0.32,
                0.18,
                0.16,
                1,
                10,
            )
            letter_settings.append(settings)

    systems = [
        {
            "mode": "pulse",
            "emitter": pulse_emitter,
            "settings": pulse_settings,
            "material": spark_mat,
            "emission_socket": spark_emit,
            "base_location": pulse_emitter.location.copy(),
            "base_rotation": pulse_emitter.rotation_euler.copy(),
            "base_scale": pulse_emitter.scale.copy(),
            "phase": 0.0,
        },
        {
            "mode": "dust",
            "emitter": dust_emitter,
            "settings": dust_settings,
            "material": dust_mat,
            "emission_socket": dust_emit,
            "base_location": dust_emitter.location.copy(),
            "base_rotation": dust_emitter.rotation_euler.copy(),
            "base_scale": dust_emitter.scale.copy(),
            "phase": 1.7,
        },
        {
            "mode": "streak",
            "emitter": streak_emitter,
            "settings": streak_settings,
            "material": streak_mat,
            "emission_socket": streak_emit,
            "base_location": streak_emitter.location.copy(),
            "base_rotation": streak_emitter.rotation_euler.copy(),
            "base_scale": streak_emitter.scale.copy(),
            "phase": 3.1,
        },
    ]

    if letter_emitter is not None and letter_settings:
        systems.append(
            {
                "mode": "letters",
                "emitter": letter_emitter,
                "settings": letter_settings[0],
                "settings_list": letter_settings,
                "material": None,
                "emission_socket": None,
                "base_location": letter_emitter.location.copy(),
                "base_rotation": letter_emitter.rotation_euler.copy(),
                "base_scale": letter_emitter.scale.copy(),
                "phase": 4.4,
                "letter_root": letter_root,
                "letter_sources": letter_sources,
            }
        )

    return systems
