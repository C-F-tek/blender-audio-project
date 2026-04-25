import bpy
import math
import random

from config import (
    USE_PHYSICS_ACCENTS,
    PHYSICS_ACCENT_COUNT,
    PRIMARY_BASE_Z,
    TURB_STRENGTH_MIN,
    VORTEX_STRENGTH_MIN,
    PHYSICS_ORBIT_RADIUS_MIN,
    PHYSICS_ORBIT_RADIUS_MAX,
    PHYSICS_ATOM_ORBIT_SPEED_MIN,
    PHYSICS_ATOM_ORBIT_SPEED_MAX,
    PHYSICS_ATOM_MICRO_WOBBLE,
    HERO_GRAVITY_STRENGTH_MIN,
    TETHER_SPRING_STIFFNESS,
    TETHER_SPRING_DAMPING,
    USE_RHYTHM_PARTICLE_PHYSICS,
    RHYTHM_PARTICLE_COUNT,
    RHYTHM_DUST_PARTICLE_COUNT,
    RHYTHM_STREAK_PARTICLE_COUNT,
    RHYTHM_PARTICLE_LIFETIME,
    RHYTHM_DUST_LIFETIME,
    RHYTHM_PARTICLE_EMITTER_RADIUS,
    RHYTHM_PARTICLE_EMITTER_Z,
    PARTICLE_SOURCE_LOCATION,
    RHYTHM_PARTICLE_SOURCE_RADIUS,
    RHYTHM_PARTICLE_SIZE_MIN,
    RHYTHM_PARTICLE_NORMAL_MIN,
    RHYTHM_PARTICLE_TANGENT_MIN,
    RHYTHM_PARTICLE_BROWNIAN_MIN,
    USE_ALBUM_LETTER_PARTICLES,
    ALBUM_PARTICLE_TEXT,
    ALBUM_LETTER_PARTICLE_COUNT,
    ALBUM_LETTER_PARTICLE_LIFETIME,
    ALBUM_LETTER_SOURCE_SIZE,
    ALBUM_LETTER_EXTRUDE,
    ALBUM_LETTER_EMISSION_STRENGTH,
    ALBUM_LETTER_PARTICLE_SIZE_MIN,
    PHYSICS_ACCENT_EMISSION_MIN,
    PHYSICS_ACCENT_MIX_MIN,
    PALETTE_LIST,
    PEACE_PALETTE,
)
from materials import build_variant_material
from scene_utils import deselect_all, safe_active


def set_if_available(obj, attr, value):
    if not hasattr(obj, attr):
        return

    try:
        setattr(obj, attr, value)
    except Exception:
        pass


def build_particle_emission_material(name, color, strength):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    for node in list(nodes):
        nodes.remove(node)

    out = nodes.new("ShaderNodeOutputMaterial")
    out.location = (420, 0)

    emission = nodes.new("ShaderNodeEmission")
    emission.location = (140, 0)
    emission.inputs["Color"].default_value = color
    emission.inputs["Strength"].default_value = strength
    emission.name = f"{name}Emission"

    links.new(emission.outputs["Emission"], out.inputs["Surface"])
    return mat, emission.inputs["Strength"]


def build_invisible_emitter_material():
    mat = bpy.data.materials.new(name="InvisibleParticleEmitterMaterial")
    mat.use_nodes = True

    if hasattr(mat, "blend_method"):
        mat.blend_method = 'BLEND'
    if hasattr(mat, "shadow_method"):
        mat.shadow_method = 'NONE'

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    for node in list(nodes):
        nodes.remove(node)

    out = nodes.new("ShaderNodeOutputMaterial")
    out.location = (360, 0)

    transparent = nodes.new("ShaderNodeBsdfTransparent")
    transparent.location = (120, 0)

    links.new(transparent.outputs["BSDF"], out.inputs["Surface"])
    return mat


def get_material_node_socket(material, node_name, socket_name, is_output=False):
    if material is None or not material.use_nodes:
        return None

    node = material.node_tree.nodes.get(node_name)
    if node is None:
        return None

    sockets = node.outputs if is_output else node.inputs
    try:
        return sockets[socket_name]
    except Exception:
        return None


def add_particle_collision(obj):
    if obj is None:
        return

    try:
        if not any(mod.type == 'COLLISION' for mod in obj.modifiers):
            obj.modifiers.new("ParticleFloorCollision", 'COLLISION')

        if hasattr(obj, "collision") and obj.collision is not None:
            obj.collision.damping_factor = 0.55
            obj.collision.damping = 0.30
            obj.collision.stickiness = 0.02
            obj.collision.use_particle_kill = False
    except Exception:
        pass


def add_passive_rigidbody(obj):
    deselect_all()
    safe_active(obj)
    bpy.ops.rigidbody.object_add()
    obj.rigid_body.type = 'PASSIVE'
    obj.rigid_body.friction = 0.6
    obj.rigid_body.restitution = 0.0


def add_active_rigidbody(obj, mass=0.15):
    deselect_all()
    safe_active(obj)
    bpy.ops.rigidbody.object_add()
    obj.rigid_body.type = 'ACTIVE'
    obj.rigid_body.mass = mass
    obj.rigid_body.linear_damping = 0.28
    obj.rigid_body.angular_damping = 0.45
    obj.rigid_body.collision_shape = 'SPHERE'
    obj.rigid_body.use_deactivation = False


def create_hidden_anchor(name, location):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.04, location=location)
    anchor = bpy.context.active_object
    anchor.name = name
    anchor.hide_render = True
    try:
        anchor.display_type = 'WIRE'
    except Exception:
        pass
    add_passive_rigidbody(anchor)
    return anchor


def create_spring_constraint(name, object1, object2, location):
    try:
        bpy.ops.object.empty_add(type='PLAIN_AXES', location=location)
        cobj = bpy.context.active_object
        cobj.name = name

        deselect_all()
        safe_active(cobj)
        bpy.ops.rigidbody.constraint_add(type='GENERIC_SPRING')

        rbc = cobj.rigid_body_constraint
        rbc.object1 = object1
        rbc.object2 = object2

        rbc.use_limit_lin_x = True
        rbc.use_limit_lin_y = True
        rbc.use_limit_lin_z = True

        rbc.limit_lin_x_lower = -0.45
        rbc.limit_lin_x_upper = 0.45
        rbc.limit_lin_y_lower = -0.45
        rbc.limit_lin_y_upper = 0.45
        rbc.limit_lin_z_lower = -0.45
        rbc.limit_lin_z_upper = 0.45

        rbc.use_spring_x = True
        rbc.use_spring_y = True
        rbc.use_spring_z = True

        rbc.spring_stiffness_x = TETHER_SPRING_STIFFNESS
        rbc.spring_stiffness_y = TETHER_SPRING_STIFFNESS
        rbc.spring_stiffness_z = TETHER_SPRING_STIFFNESS

        rbc.spring_damping_x = TETHER_SPRING_DAMPING
        rbc.spring_damping_y = TETHER_SPRING_DAMPING
        rbc.spring_damping_z = TETHER_SPRING_DAMPING

        cobj.hide_render = True
        return cobj
    except Exception:
        return None


def create_particle_instance(name, color, strength, shape="sphere"):
    if shape == "streak":
        bpy.ops.mesh.primitive_cone_add(
            vertices=7,
            radius1=RHYTHM_PARTICLE_SOURCE_RADIUS * 0.62,
            radius2=RHYTHM_PARTICLE_SOURCE_RADIUS * 0.08,
            depth=RHYTHM_PARTICLE_SOURCE_RADIUS * 4.2,
            location=PARTICLE_SOURCE_LOCATION,
        )
        obj = bpy.context.active_object
        obj.rotation_euler.x = math.radians(90.0)
    else:
        bpy.ops.mesh.primitive_ico_sphere_add(
            subdivisions=1,
            radius=RHYTHM_PARTICLE_SOURCE_RADIUS,
            location=PARTICLE_SOURCE_LOCATION,
        )
        obj = bpy.context.active_object

    obj.name = name
    mat, emit_socket = build_particle_emission_material(
        f"{name}Material",
        color,
        strength,
    )
    obj.data.materials.append(mat)

    deselect_all()
    safe_active(obj)
    try:
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    except Exception:
        pass

    # Kept off-stage so the source is not seen, but render-enabled for particle instancing.
    obj.hide_viewport = True
    obj.hide_render = False
    return obj, mat, emit_socket


def create_album_letter_particle_collection(parent=None):
    if not USE_ALBUM_LETTER_PARTICLES:
        return None, None, []

    collection = bpy.data.collections.new("AlbumLetterParticleCollection")
    bpy.context.scene.collection.children.link(collection)

    bpy.ops.object.empty_add(type='PLAIN_AXES', location=PARTICLE_SOURCE_LOCATION)
    root = bpy.context.active_object
    root.name = "AlbumLetterParticleSources"
    root.hide_viewport = False
    root.hide_render = False
    root.display_type = 'WIRE'
    if parent is not None:
        root.parent = parent

    letters = []
    chars = [char for char in ALBUM_PARTICLE_TEXT if not char.isspace()]
    if not chars:
        return collection, root, letters

    palette = [
        PEACE_PALETTE["warm_white"],
        PEACE_PALETTE["soft_teal"],
        PEACE_PALETTE["muted_gold"],
        PEACE_PALETTE["dust_rose"],
    ]

    for idx, char in enumerate(chars):
        x = (idx - len(chars) * 0.5) * 0.18
        bpy.ops.object.text_add(
            location=(
                PARTICLE_SOURCE_LOCATION[0] + x,
                PARTICLE_SOURCE_LOCATION[1],
                PARTICLE_SOURCE_LOCATION[2],
            ),
            rotation=(math.radians(90.0), 0, 0),
        )
        obj = bpy.context.active_object
        obj.name = f"AlbumLetterParticle_{idx:02d}_{char}"
        obj.data.body = char
        obj.data.align_x = 'CENTER'
        obj.data.align_y = 'CENTER'
        obj.data.size = ALBUM_LETTER_SOURCE_SIZE
        obj.data.extrude = ALBUM_LETTER_EXTRUDE
        obj.data.resolution_u = 8

        mat, _ = build_particle_emission_material(
            f"AlbumLetterParticleMat_{idx:02d}",
            palette[idx % len(palette)],
            ALBUM_LETTER_EMISSION_STRENGTH,
        )
        obj.data.materials.append(mat)

        deselect_all()
        safe_active(obj)
        try:
            bpy.ops.object.convert(target='MESH')
            obj = bpy.context.active_object
            obj.name = f"AlbumLetterParticle_{idx:02d}_{char}"
        except Exception:
            pass

        obj.parent = root
        obj.hide_viewport = False
        obj.hide_render = False

        try:
            for coll in list(obj.users_collection):
                if coll != collection:
                    coll.objects.unlink(obj)
            collection.objects.link(obj)
        except Exception:
            pass

        letters.append({
            "object": obj,
            "base_scale": obj.scale.copy(),
            "phase": idx * 0.37,
        })

    return collection, root, letters


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
    emitter.display_type = 'WIRE'
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
    mod = emitter.modifiers.new(name=name, type='PARTICLE_SYSTEM')
    ps = mod.particle_system
    settings = ps.settings
    settings.name = f"{name}Settings"

    frame_end = max(1, int(bpy.context.scene.frame_end))

    settings.type = 'EMITTER'
    settings.physics_type = 'NEWTON'
    if instance_collection is not None:
        settings.render_type = 'COLLECTION'
        set_if_available(settings, "instance_collection", instance_collection)
        set_if_available(settings, "use_collection_pick_random", True)
        set_if_available(settings, "use_whole_collection", False)
        set_if_available(settings, "use_collection_count", False)
    else:
        settings.render_type = 'OBJECT'
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

    set_if_available(settings, "emit_from", 'FACE')
    set_if_available(settings, "distribution", 'RAND')
    set_if_available(settings, "use_emit_random", True)
    set_if_available(settings, "use_modifier_stack", True)
    set_if_available(settings, "use_rotations", True)
    set_if_available(settings, "rotation_mode", 'VEL')
    set_if_available(settings, "angular_velocity_mode", 'VELOCITY')
    set_if_available(settings, "angular_velocity_factor", 0.72)
    set_if_available(settings, "child_type", 'INTERPOLATED')
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

    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
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
    letter_collection, letter_root, letter_sources = create_album_letter_particle_collection(parent=root)

    for obj in [spark_obj, dust_obj, streak_obj]:
        obj.parent = root

    pulse_emitter = create_particle_emitter("BeatPulseParticleEmitter", "ring", invisible_mat)
    dust_emitter = create_particle_emitter("OrbitDustParticleEmitter", "sphere", invisible_mat)
    streak_emitter = create_particle_emitter("HighStreakParticleEmitter", "wide_ring", invisible_mat)
    letter_emitter = None
    if letter_collection is not None and letter_sources:
        letter_emitter = create_particle_emitter("AlbumLetterParticleEmitter", "wide_ring", invisible_mat)

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
        systems.append({
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
        })

    return systems


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

    bpy.ops.object.effector_add(type='FORCE', location=(0, 0, PRIMARY_BASE_Z + 1.20))
    force_obj = bpy.context.active_object
    force_obj.name = "HeroGravityField"
    force_obj.field.strength = -HERO_GRAVITY_STRENGTH_MIN
    force_obj.field.flow = 1.0
    force_obj.field.noise = 0.10
    force_obj.field.falloff_power = 1.55

    bpy.ops.object.effector_add(type='TURBULENCE', location=(0, 0, PRIMARY_BASE_Z + 1.50))
    turb_obj = bpy.context.active_object
    turb_obj.name = "AtmosphereTurbulence"
    turb_obj.field.strength = TURB_STRENGTH_MIN
    turb_obj.field.size = 2.0
    turb_obj.field.flow = 0.45

    bpy.ops.object.effector_add(type='VORTEX', location=(0, 0, PRIMARY_BASE_Z + 1.00))
    vortex_obj = bpy.context.active_object
    vortex_obj.name = "OrbitVortex"
    vortex_obj.rotation_euler.x = math.radians(90.0)
    vortex_obj.field.strength = VORTEX_STRENGTH_MIN

    bpy.ops.object.effector_add(type='WIND', location=(-3.0, -1.2, PRIMARY_BASE_Z + 1.8))
    wind_left = bpy.context.active_object
    wind_left.name = "WindLeft"
    wind_left.rotation_euler = (math.radians(90), 0, math.radians(20))
    wind_left.field.strength = 0.0
    wind_left.field.flow = 1.0

    bpy.ops.object.effector_add(type='WIND', location=(3.0, -1.2, PRIMARY_BASE_Z + 1.8))
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

        accents.append({
            "object": obj,
            "anchor": anchor,
            "constraint": constraint,
            "base_location": obj.location.copy(),
            "base_rotation": obj.rotation_euler.copy(),
            "phase": random.uniform(0.0, math.tau),
            "orbit_radius": radius,
            "orbit_angle": angle,
            "orbit_z_offset": z_offset,
            "orbit_speed": random.uniform(PHYSICS_ATOM_ORBIT_SPEED_MIN, PHYSICS_ATOM_ORBIT_SPEED_MAX),
            "orbit_tilt": random.uniform(-0.42, 0.42),
            "micro_radius": random.uniform(PHYSICS_ATOM_MICRO_WOBBLE * 0.45, PHYSICS_ATOM_MICRO_WOBBLE * 1.25),
            "band": ["low", "mid", "high", "beat", "onset"][i % 5],
            "response": random.uniform(0.42, 1.0),
            "emission_socket": emit_socket,
            "mix_socket": mix_socket,
            "material": mat,
        })

    return {
        "accents": accents,
        "force_obj": force_obj,
        "turb_obj": turb_obj,
        "vortex_obj": vortex_obj,
        "wind_left": wind_left,
        "wind_right": wind_right,
        "rhythm_particles": rhythm_particles,
    }
