import math
import random

import bpy
from materials import build_variant_material
from scene_utils import deselect_all, safe_active

from config import (
    ALBUM_LETTER_EMISSION_STRENGTH,
    ALBUM_LETTER_EXTRUDE,
    ALBUM_LETTER_PARTICLE_COUNT,
    ALBUM_LETTER_PARTICLE_LIFETIME,
    ALBUM_LETTER_PARTICLE_SIZE_MIN,
    ALBUM_LETTER_SOURCE_SIZE,
    ALBUM_PARTICLE_TEXT,
    HERO_GRAVITY_STRENGTH_MIN,
    PALETTE_LIST,
    PARTICLE_SOURCE_LOCATION,
    PEACE_PALETTE,
    PHYSICS_ACCENT_COUNT,
    PHYSICS_ACCENT_EMISSION_MIN,
    PHYSICS_ACCENT_MIX_MIN,
    PHYSICS_ATOM_MICRO_WOBBLE,
    PHYSICS_ATOM_ORBIT_SPEED_MAX,
    PHYSICS_ATOM_ORBIT_SPEED_MIN,
    PHYSICS_ORBIT_RADIUS_MAX,
    PHYSICS_ORBIT_RADIUS_MIN,
    PRIMARY_BASE_Z,
    RHYTHM_DUST_LIFETIME,
    RHYTHM_DUST_PARTICLE_COUNT,
    RHYTHM_PARTICLE_BROWNIAN_MIN,
    RHYTHM_PARTICLE_COUNT,
    RHYTHM_PARTICLE_EMITTER_RADIUS,
    RHYTHM_PARTICLE_EMITTER_Z,
    RHYTHM_PARTICLE_LIFETIME,
    RHYTHM_PARTICLE_NORMAL_MIN,
    RHYTHM_PARTICLE_SIZE_MIN,
    RHYTHM_PARTICLE_SOURCE_RADIUS,
    RHYTHM_PARTICLE_TANGENT_MIN,
    RHYTHM_STREAK_PARTICLE_COUNT,
    TETHER_SPRING_DAMPING,
    TETHER_SPRING_STIFFNESS,
    TURB_STRENGTH_MIN,
    USE_ALBUM_LETTER_PARTICLES,
    USE_PHYSICS_ACCENTS,
    USE_RHYTHM_PARTICLE_PHYSICS,
    VORTEX_STRENGTH_MIN,
)


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
        mat.blend_method = "BLEND"
    if hasattr(mat, "shadow_method"):
        mat.shadow_method = "NONE"

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
        if not any(mod.type == "COLLISION" for mod in obj.modifiers):
            obj.modifiers.new("ParticleFloorCollision", "COLLISION")

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
    obj.rigid_body.type = "PASSIVE"
    obj.rigid_body.friction = 0.6
    obj.rigid_body.restitution = 0.0


def add_active_rigidbody(obj, mass=0.15):
    deselect_all()
    safe_active(obj)
    bpy.ops.rigidbody.object_add()
    obj.rigid_body.type = "ACTIVE"
    obj.rigid_body.mass = mass
    obj.rigid_body.linear_damping = 0.28
    obj.rigid_body.angular_damping = 0.45
    obj.rigid_body.collision_shape = "SPHERE"
    obj.rigid_body.use_deactivation = False


def create_hidden_anchor(name, location):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.04, location=location)
    anchor = bpy.context.active_object
    anchor.name = name
    anchor.hide_render = True
    try:
        anchor.display_type = "WIRE"
    except Exception:
        pass
    add_passive_rigidbody(anchor)
    return anchor


def create_spring_constraint(name, object1, object2, location):
    try:
        bpy.ops.object.empty_add(type="PLAIN_AXES", location=location)
        cobj = bpy.context.active_object
        cobj.name = name

        deselect_all()
        safe_active(cobj)
        bpy.ops.rigidbody.constraint_add(type="GENERIC_SPRING")

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

    bpy.ops.object.empty_add(type="PLAIN_AXES", location=PARTICLE_SOURCE_LOCATION)
    root = bpy.context.active_object
    root.name = "AlbumLetterParticleSources"
    root.hide_viewport = False
    root.hide_render = False
    root.display_type = "WIRE"
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
        obj.data.align_x = "CENTER"
        obj.data.align_y = "CENTER"
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
            bpy.ops.object.convert(target="MESH")
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

        letters.append(
            {
                "object": obj,
                "base_scale": obj.scale.copy(),
                "phase": idx * 0.37,
            }
        )

    return collection, root, letters
