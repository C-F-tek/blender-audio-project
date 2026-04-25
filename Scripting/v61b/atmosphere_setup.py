import bpy
import math
import random

from config import (
    PRIMARY_BASE_Z,
    AURA_RADIUS,
    USE_HERO_AURA_MESH,
    AURA_DEFORM_SUBDIV_VIEW,
    AURA_DEFORM_SUBDIV_RENDER,
    AURA_DEFORM_FIELD_RADIUS,
    AURA_DEFORM_DISPLACE_MIN,
    AURA_DEFORM_DISPLACE_MAX,
    AURA_DEFORM_DETAIL_MAX,
    AURA_DEFORM_WAVE_HEIGHT_MAX,
    AURA_DEFORM_FIELD_STRENGTH_MAX,
    ENERGY_RING_COUNT,
    RIBBON_COUNT,
    CREATE_VARIANTS,
    VARIANT_COUNT,
    VARIANT_RING_RADIUS,
    VARIANT_SCALE_MIN,
    VARIANT_SCALE_MAX,
    USE_MIST_PARTICLES,
    MIST_PARTICLE_COUNT,
    MIST_SCALE_MIN,
    MIST_SCALE_MAX,
    ATMOSPHERE_CUBE_SIZE,
    FOG_VOLUME_ENABLED,
    FOG_VOLUME_VIEWPORT_VISIBLE,
    FOG_RAMP_LOW_BASE,
    FOG_RAMP_HIGH_BASE,
    PALETTE_LIST,
    PEACE_PALETTE,
)
from materials import (
    build_aura_material,
    build_ring_material,
    build_ribbon_material,
    build_variant_material,
    build_atmosphere_volume_material,
    build_mist_particle_material,
)
from asset_setup import duplicate_hierarchy, assign_material_to_hierarchy
from scene_utils import create_controller_empty
from fog_filaments import ensure_fog_filaments


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
    driver.type = 'SCRIPTED'
    driver.expression = expression

    while driver.variables:
        driver.variables.remove(driver.variables[0])

    for var_name, target_obj, prop_name in prop_targets:
        var = driver.variables.new()
        var.name = var_name
        target = var.targets[0]
        target.id_type = 'OBJECT'
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
    field.display_type = 'WIRE'
    field.hide_render = True
    field.hide_viewport = True
    field.hide_select = True

    if parent is not None:
        field.parent = parent

    try:
        field.data.name = "AuraAudioDeformFieldMesh"
    except Exception:
        pass

    tex = bpy.data.textures.new("AuraAudioDeformFieldTexture", type='CLOUDS')
    for attr, value in [
        ("noise_scale", 0.92),
        ("noise_depth", 5),
        ("contrast", 3.2),
    ]:
        try:
            setattr(tex, attr, value)
        except Exception:
            pass

    mod = field.modifiers.new("AudioFieldInvisibleDisplace", 'DISPLACE')
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

    subdiv = aura.modifiers.new("AuraAudioSubdivision", 'SUBSURF')
    subdiv.levels = AURA_DEFORM_SUBDIV_VIEW
    subdiv.render_levels = AURA_DEFORM_SUBDIV_RENDER

    breath_tex = bpy.data.textures.new("AuraBreathDisplaceTexture", type='VORONOI')
    for attr, value in [
        ("noise_scale", 1.85),
        ("intensity", 0.42),
        ("contrast", 2.8),
    ]:
        try:
            setattr(breath_tex, attr, value)
        except Exception:
            pass

    breath = aura.modifiers.new("AuraAudioBreathDisplace", 'DISPLACE')
    breath.strength = AURA_DEFORM_DISPLACE_MIN
    breath.mid_level = 0.48
    breath.texture = breath_tex
    try:
        breath.direction = 'NORMAL'
        breath.texture_coords = 'OBJECT'
        breath.texture_coords_object = deform_field
    except Exception:
        pass

    add_prop_driver(
        breath,
        "strength",
        f"{AURA_DEFORM_DISPLACE_MIN:.6f} + aura * {(AURA_DEFORM_DISPLACE_MAX - AURA_DEFORM_DISPLACE_MIN):.6f}",
        [("aura", controller, "aura_deform")],
    )

    detail_tex = bpy.data.textures.new("AuraTransientDetailTexture", type='CLOUDS')
    for attr, value in [
        ("noise_scale", 0.54),
        ("noise_depth", 6),
        ("contrast", 4.0),
    ]:
        try:
            setattr(detail_tex, attr, value)
        except Exception:
            pass

    detail = aura.modifiers.new("AuraAudioTransientDetail", 'DISPLACE')
    detail.strength = 0.0
    detail.mid_level = 0.50
    detail.texture = detail_tex
    try:
        detail.direction = 'NORMAL'
        detail.texture_coords = 'OBJECT'
        detail.texture_coords_object = deform_field
    except Exception:
        pass

    add_prop_driver(
        detail,
        "strength",
        f"detail * {AURA_DEFORM_DETAIL_MAX:.6f}",
        [("detail", controller, "detail")],
    )

    wave = aura.modifiers.new("AuraAudioBeatWave", 'WAVE')
    try:
        wave.type = 'RINGS'
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

    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=AURA_RADIUS,
        location=aura_location
    )
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
            )
        )
        ring = bpy.context.active_object
        ring.name = f"EnergyRing_{i:02d}"

        color = PALETTE_LIST[(i + 1) % len(PALETTE_LIST)]
        mat, emit_socket = build_ring_material(f"EnergyRingMat_{i:02d}", color)
        ring.data.materials.append(mat)

        if parent is not None:
            ring.parent = parent

        rings.append({
            "object": ring,
            "emit_socket": emit_socket,
            "base_scale": ring.scale.copy(),
            "base_rot": ring.rotation_euler.copy(),
            "base_loc": ring.location.copy(),
            "phase": i * 0.9,
        })

    return rings


def create_energy_ribbons(parent=None):
    ribbons = []

    for i in range(RIBBON_COUNT):
        bpy.ops.curve.primitive_bezier_circle_add(
            location=(0, 0, PRIMARY_BASE_Z + 1.05 + i * 0.20)
        )
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

        ribbons.append({
            "object": ribbon,
            "emit_socket": emit_socket,
            "base_rot": ribbon.rotation_euler.copy(),
            "base_loc": ribbon.location.copy(),
            "base_scale": ribbon.scale.copy(),
            "phase": i * 1.15,
        })

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

        variants.append({
            "root": dup,
            "angle": ang,
            "base_location": dup.location.copy(),
            "base_scale": scale,
        })

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
    cube.display_type = 'WIRE'
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

    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
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
        mat, em_socket, mix_socket = build_mist_particle_material(
            f"MistParticleMat_{i:02d}",
            color
        )
        obj.data.materials.append(mat)

        particles.append({
            "object": obj,
            "material": mat,
            "emission_socket": em_socket,
            "mix_socket": mix_socket,
            "base_location": obj.location.copy(),
            "phase": random.uniform(0.0, math.tau),
            "base_scale": random.uniform(MIST_SCALE_MIN, MIST_SCALE_MAX),
        })

    return particles
