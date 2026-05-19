import math
import random

import bpy
from asset_setup import assign_material_to_hierarchy, duplicate_hierarchy
from fog_filaments import ensure_fog_filaments
from materials import (
    build_atmosphere_volume_material,
    build_aura_material,
    build_mist_particle_material,
    build_ribbon_material,
    build_ring_material,
    build_variant_material,
)
from scene_utils import create_controller_empty

from config import (
    ATMOSPHERE_CUBE_SIZE,
    AURA_DEFORM_DETAIL_MAX,
    AURA_DEFORM_DISPLACE_MAX,
    AURA_DEFORM_DISPLACE_MIN,
    AURA_DEFORM_FIELD_RADIUS,
    AURA_DEFORM_FIELD_STRENGTH_MAX,
    AURA_DEFORM_SUBDIV_RENDER,
    AURA_DEFORM_SUBDIV_VIEW,
    AURA_DEFORM_WAVE_HEIGHT_MAX,
    AURA_RADIUS,
    CREATE_VARIANTS,
    ENERGY_RING_COUNT,
    FOG_RAMP_HIGH_BASE,
    FOG_RAMP_LOW_BASE,
    FOG_VOLUME_ENABLED,
    FOG_VOLUME_VIEWPORT_VISIBLE,
    MIST_PARTICLE_COUNT,
    MIST_SCALE_MAX,
    MIST_SCALE_MIN,
    PALETTE_LIST,
    PEACE_PALETTE,
    PRIMARY_BASE_Z,
    RIBBON_COUNT,
    USE_HERO_AURA_MESH,
    USE_MIST_PARTICLES,
    VARIANT_COUNT,
    VARIANT_RING_RADIUS,
    VARIANT_SCALE_MAX,
    VARIANT_SCALE_MIN,
)

AURA_AUDIO_PROPS = [
    "low",
    "mid",
    "high",
    "onset",
    "beat",
    "pulse",
    "aura_deform",
    "detail",
    "phase",
]


def init_audio_props(obj):
    for prop in AURA_AUDIO_PROPS:
        obj[prop] = 0.0
        try:
            obj.id_properties_ui(prop).update(min=0.0, max=1.0)
        except Exception:
            pass


def add_prop_driver(idblock, data_path, expression, prop_targets):
    try:
        fcurve = idblock.driver_add(data_path)
    except Exception as exc:
        print(f"[WARN] Driver non creato per {data_path}: {exc}")
        return None

    driver = fcurve.driver
    driver.type = "SCRIPTED"
    driver.expression = expression

    while driver.variables:
        driver.variables.remove(driver.variables[0])

    for var_name, target_obj, prop_name in prop_targets:
        var = driver.variables.new()
        var.name = var_name
        target = var.targets[0]
        target.id_type = "OBJECT"
        target.id = target_obj
        target.data_path = f'["{prop_name}"]'

    return fcurve


def create_aura_deform_field(controller, aura_location, parent=None):
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=24,
        ring_count=12,
        radius=AURA_DEFORM_FIELD_RADIUS,
        location=aura_location,
    )
    field = bpy.context.active_object
    field.name = "AuraAudioDeformField"
    field.display_type = "WIRE"
    field.hide_render = True
    field.hide_viewport = True
    field.hide_select = True

    if parent is not None:
        field.parent = parent

    try:
        field.data.name = "AuraAudioDeformFieldMesh"
    except Exception:
        pass

    tex = bpy.data.textures.new("AuraAudioDeformFieldTexture", type="CLOUDS")
    for attr, value in [
        ("noise_scale", 0.92),
        ("noise_depth", 5),
        ("contrast", 3.2),
    ]:
        try:
            setattr(tex, attr, value)
        except Exception:
            pass

    mod = field.modifiers.new("AudioFieldInvisibleDisplace", "DISPLACE")
    mod.strength = 0.0
    mod.mid_level = 0.50
    mod.texture = tex

    add_prop_driver(
        mod,
        "strength",
        f"aura * {AURA_DEFORM_FIELD_STRENGTH_MAX:.6f}",
        [("aura", controller, "aura_deform")],
    )

    return field, mod, tex


def add_hero_aura_deformers(aura, controller, deform_field):
    try:
        bpy.ops.object.shade_smooth()
    except Exception:
        pass

    subdiv = aura.modifiers.new("AuraAudioSubdivision", "SUBSURF")
    subdiv.levels = AURA_DEFORM_SUBDIV_VIEW
    subdiv.render_levels = AURA_DEFORM_SUBDIV_RENDER

    breath_tex = bpy.data.textures.new("AuraBreathDisplaceTexture", type="VORONOI")
    for attr, value in [
        ("noise_scale", 1.85),
        ("intensity", 0.42),
        ("contrast", 2.8),
    ]:
        try:
            setattr(breath_tex, attr, value)
        except Exception:
            pass

    breath = aura.modifiers.new("AuraAudioBreathDisplace", "DISPLACE")
    breath.strength = AURA_DEFORM_DISPLACE_MIN
    breath.mid_level = 0.48
    breath.texture = breath_tex
    try:
        breath.direction = "NORMAL"
        breath.texture_coords = "OBJECT"
        breath.texture_coords_object = deform_field
    except Exception:
        pass

    add_prop_driver(
        breath,
        "strength",
        f"{AURA_DEFORM_DISPLACE_MIN:.6f} + aura * {(AURA_DEFORM_DISPLACE_MAX - AURA_DEFORM_DISPLACE_MIN):.6f}",
        [("aura", controller, "aura_deform")],
    )

    detail_tex = bpy.data.textures.new("AuraTransientDetailTexture", type="CLOUDS")
    for attr, value in [
        ("noise_scale", 0.54),
        ("noise_depth", 6),
        ("contrast", 4.0),
    ]:
        try:
            setattr(detail_tex, attr, value)
        except Exception:
            pass

    detail = aura.modifiers.new("AuraAudioTransientDetail", "DISPLACE")
    detail.strength = 0.0
    detail.mid_level = 0.50
    detail.texture = detail_tex
    try:
        detail.direction = "NORMAL"
        detail.texture_coords = "OBJECT"
        detail.texture_coords_object = deform_field
    except Exception:
        pass

    add_prop_driver(
        detail,
        "strength",
        f"detail * {AURA_DEFORM_DETAIL_MAX:.6f}",
        [("detail", controller, "detail")],
    )

    wave = aura.modifiers.new("AuraAudioBeatWave", "WAVE")
    try:
        wave.type = "RINGS"
        wave.use_x = True
        wave.use_y = True
        wave.use_normal = True
        wave.width = 1.10
        wave.narrowness = 1.85
        wave.speed = 0.28
        wave.height = 0.0
        wave.start_position_object = deform_field
    except Exception:
        pass

    add_prop_driver(
        wave,
        "height",
        f"pulse * {AURA_DEFORM_WAVE_HEIGHT_MAX:.6f}",
        [("pulse", controller, "pulse")],
    )
    add_prop_driver(
        wave,
        "time_offset",
        "-phase * 3.0",
        [("phase", controller, "phase")],
    )

    return {
        "subdivision": subdiv,
        "breath_modifier": breath,
        "breath_texture": breath_tex,
        "detail_modifier": detail,
        "detail_texture": detail_tex,
        "wave_modifier": wave,
    }


def create_hero_aura(parent=None):
    aura_location = (0, 0, PRIMARY_BASE_Z + 0.95)

    if not USE_HERO_AURA_MESH:
        proxy = create_controller_empty(
            "HeroAuraProxy",
            location=aura_location,
            parent=parent,
            display_size=0.30,
            hide_view=True,
        )
        audio_controller = create_controller_empty(
            "AuraAudioSampler",
            location=aura_location,
            parent=parent,
            display_size=0.38,
            hide_view=True,
        )
        init_audio_props(audio_controller)

        return {
            "object": proxy,
            "material": None,
            "strength_socket": None,
            "edge_ctrl": None,
            "audio_controller": audio_controller,
            "deform_field": None,
            "field_modifier": None,
            "field_texture": None,
            "deformers": {},
            "audio_props": AURA_AUDIO_PROPS,
        }

    mat, aura_strength_socket, aura_edge_ctrl = build_aura_material()

    bpy.ops.mesh.primitive_uv_sphere_add(radius=AURA_RADIUS, location=aura_location)
    aura = bpy.context.active_object
    aura.name = "HeroAura"
    aura.data.materials.append(mat)

    if parent is not None:
        aura.parent = parent

    audio_controller = create_controller_empty(
        "AuraAudioSampler",
        location=aura_location,
        parent=parent,
        display_size=0.38,
        hide_view=True,
    )
    init_audio_props(audio_controller)

    deform_field, field_modifier, field_texture = create_aura_deform_field(
        audio_controller,
        aura_location,
        parent=parent,
    )
    deformers = add_hero_aura_deformers(aura, audio_controller, deform_field)

    return {
        "object": aura,
        "material": mat,
        "strength_socket": aura_strength_socket,
        "edge_ctrl": aura_edge_ctrl,
        "audio_controller": audio_controller,
        "deform_field": deform_field,
        "field_modifier": field_modifier,
        "field_texture": field_texture,
        "deformers": deformers,
        "audio_props": AURA_AUDIO_PROPS,
    }


def create_energy_rings(parent=None):
    rings = []

    for i in range(ENERGY_RING_COUNT):
        bpy.ops.mesh.primitive_torus_add(
            major_radius=2.90 + i * 0.70,
            minor_radius=0.014 + i * 0.006,
            location=(0, 0, PRIMARY_BASE_Z + 1.10 + i * 0.16),
            rotation=(
                math.radians(82 + i * 8),
                math.radians(10 + i * 10),
                math.radians(i * 20),
            ),
        )
        ring = bpy.context.active_object
        ring.name = f"EnergyRing_{i:02d}"

        color = PALETTE_LIST[(i + 1) % len(PALETTE_LIST)]
        mat, emit_socket = build_ring_material(f"EnergyRingMat_{i:02d}", color)
        ring.data.materials.append(mat)

        if parent is not None:
            ring.parent = parent

        rings.append(
            {
                "object": ring,
                "emit_socket": emit_socket,
                "base_scale": ring.scale.copy(),
                "base_rot": ring.rotation_euler.copy(),
                "base_loc": ring.location.copy(),
                "phase": i * 0.9,
            }
        )

    return rings
