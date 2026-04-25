import math

import bpy

from materials import build_variant_material

from .common import (
    PALETTE_LIST,
    cfg_value,
    clear_animation,
    get_node,
    iter_objects_prefix,
    keyframe_if_possible,
    socket_by_name,
    store_base_vector,
)


PHYSICS_ACCENT_EMISSION_MIN = cfg_value("PHYSICS_ACCENT_EMISSION_MIN", 0.06)
PHYSICS_ACCENT_EMISSION_MAX = cfg_value("PHYSICS_ACCENT_EMISSION_MAX", 0.72)
PHYSICS_ACCENT_MIX_MIN = cfg_value("PHYSICS_ACCENT_MIX_MIN", 0.12)
PHYSICS_ACCENT_MIX_MAX = cfg_value("PHYSICS_ACCENT_MIX_MAX", 0.42)
PRIMARY_BASE_Z = cfg_value("PRIMARY_BASE_Z", 0.72)
PHYSICS_ORBIT_RADIUS_MIN = cfg_value("PHYSICS_ORBIT_RADIUS_MIN", 1.65)
PHYSICS_ORBIT_RADIUS_MAX = cfg_value("PHYSICS_ORBIT_RADIUS_MAX", 3.85)
PHYSICS_ATOM_ORBIT_SPEED_MIN = cfg_value("PHYSICS_ATOM_ORBIT_SPEED_MIN", 0.0048)
PHYSICS_ATOM_ORBIT_SPEED_MAX = cfg_value("PHYSICS_ATOM_ORBIT_SPEED_MAX", 0.0125)
PHYSICS_ATOM_ORBIT_AUDIO_SPEED = cfg_value("PHYSICS_ATOM_ORBIT_AUDIO_SPEED", 0.010)
PHYSICS_ATOM_ORBIT_RADIUS_PULSE = cfg_value("PHYSICS_ATOM_ORBIT_RADIUS_PULSE", 0.105)
PHYSICS_ATOM_ORBIT_HEIGHT_SWAY = cfg_value("PHYSICS_ATOM_ORBIT_HEIGHT_SWAY", 0.36)
PHYSICS_ATOM_MICRO_WOBBLE = cfg_value("PHYSICS_ATOM_MICRO_WOBBLE", 0.075)
HERO_GRAVITY_STRENGTH_MIN = cfg_value("HERO_GRAVITY_STRENGTH_MIN", 5.0)
HERO_GRAVITY_STRENGTH_MAX = cfg_value("HERO_GRAVITY_STRENGTH_MAX", 34.0)
TURB_STRENGTH_MIN = cfg_value("TURB_STRENGTH_MIN", 0.25)
TURB_STRENGTH_MAX = cfg_value("TURB_STRENGTH_MAX", 4.8)
VORTEX_STRENGTH_MIN = cfg_value("VORTEX_STRENGTH_MIN", 0.15)
VORTEX_STRENGTH_MAX = cfg_value("VORTEX_STRENGTH_MAX", 2.6)


def drive_for_band(band, response, sample, frame, phase):
    low = float(sample.get("low", 0.0))
    mid = float(sample.get("mid", 0.0))
    high = float(sample.get("high", 0.0))
    onset = float(sample.get("onset", 0.0))
    beat = float(sample.get("beat", 0.0))
    pulse = max(onset, beat)
    local_pulse = max(0.0, math.sin(frame * (0.024 + response * 0.016) + phase)) * 0.20

    if band == "low":
        drive = low * 0.74 + beat * 0.18 + local_pulse * 0.16
    elif band == "mid":
        drive = mid * 0.68 + low * 0.14 + local_pulse * 0.18
    elif band == "beat":
        drive = beat * 0.70 + low * 0.22 + local_pulse * 0.14
    elif band == "onset":
        drive = onset * 0.72 + high * 0.18 + local_pulse * 0.12
    else:
        drive = high * 0.68 + onset * 0.24 + pulse * 0.08 + local_pulse * 0.12

    return max(0.0, min(1.0, drive * response))


def ensure_accent_material(obj, index):
    mat = obj.active_material
    if mat is None or not mat.use_nodes or get_node(mat, "VariantEmission") is None:
        color = PALETTE_LIST[index % len(PALETTE_LIST)]
        mat = build_variant_material(f"PhysicsAccentMat_hot_{index:02d}", color)
        obj.data.materials.clear()
        obj.data.materials.append(mat)

    emission = get_node(mat, "VariantEmission")
    mix = get_node(mat, "VariantEmissionMix")
    emit_socket = socket_by_name(emission, "Strength")
    mix_socket = socket_by_name(mix, 0, is_output=True)

    if emit_socket is not None:
        emit_socket.default_value = PHYSICS_ACCENT_EMISSION_MIN
    if mix_socket is not None:
        mix_socket.default_value = PHYSICS_ACCENT_MIX_MIN

    return mat, emit_socket, mix_socket


def get_or_store_float(obj, key, default):
    if key not in obj:
        obj[key] = float(default)
    return float(obj[key])


def atom_center():
    hero = bpy.data.objects.get("HeroRoot")
    if hero is not None:
        return hero.location.copy()

    from mathutils import Vector

    return Vector((0.0, 0.0, PRIMARY_BASE_Z + 1.02))


def find_or_create_force_object(name, effector_type, location):
    obj = bpy.data.objects.get(name)
    if obj is not None:
        return obj

    if name == "HeroGravityField":
        old = bpy.data.objects.get("PulseForceField")
        if old is not None:
            old.name = "HeroGravityField"
            return old

    try:
        bpy.ops.object.effector_add(type=effector_type, location=location)
        obj = bpy.context.active_object
        obj.name = name
        obj.hide_render = True
        return obj
    except Exception:
        return None


def update_central_fields(frames, center):
    gravity = find_or_create_force_object("HeroGravityField", 'FORCE', center)
    turbulence = find_or_create_force_object("AtmosphereTurbulence", 'TURBULENCE', center)
    vortex = find_or_create_force_object("OrbitVortex", 'VORTEX', center)

    for obj in [gravity, turbulence, vortex]:
        clear_animation(obj)

    if not frames:
        frames = [{"low": 0.3, "mid": 0.2, "high": 0.2, "onset": 0.0, "beat": 0.0}]

    for frame, sample in enumerate(frames, start=1):
        low = float(sample.get("low", 0.0))
        mid = float(sample.get("mid", 0.0))
        high = float(sample.get("high", 0.0))
        onset = float(sample.get("onset", 0.0))
        beat = float(sample.get("beat", 0.0))
        pulse = max(onset, beat)

        if gravity is not None and getattr(gravity, "field", None) is not None:
            gravity_drive = min(1.0, low * 0.44 + mid * 0.14 + pulse * 0.34 + beat * 0.16)
            strength = HERO_GRAVITY_STRENGTH_MIN + gravity_drive * (
                HERO_GRAVITY_STRENGTH_MAX - HERO_GRAVITY_STRENGTH_MIN
            )
            gravity.field.strength = -strength
            gravity.field.noise = 0.10
            gravity.field.falloff_power = 1.55
            gravity.location.x = center.x
            gravity.location.y = center.y
            gravity.location.z = center.z + 0.34 + math.sin(frame * 0.010) * 0.05
            keyframe_if_possible(gravity, 'field.strength', frame)
            gravity.keyframe_insert(data_path="location", frame=frame)

        if turbulence is not None and getattr(turbulence, "field", None) is not None:
            turbulence.field.strength = TURB_STRENGTH_MIN + high * (TURB_STRENGTH_MAX - TURB_STRENGTH_MIN) * 0.64 + pulse * 0.42
            turbulence.location.x = center.x
            turbulence.location.y = center.y
            turbulence.location.z = center.z + 0.74 + math.sin(frame * 0.012) * 0.08
            keyframe_if_possible(turbulence, 'field.strength', frame)
            turbulence.keyframe_insert(data_path="location", frame=frame)

        if vortex is not None and getattr(vortex, "field", None) is not None:
            vortex.field.strength = VORTEX_STRENGTH_MIN + (mid * 0.62 + pulse * 0.18) * (
                VORTEX_STRENGTH_MAX - VORTEX_STRENGTH_MIN
            )
            vortex.location.x = center.x
            vortex.location.y = center.y
            vortex.location.z = center.z + 0.18
            vortex.rotation_euler.z = frame * (0.004 + mid * 0.003 + beat * 0.002)
            keyframe_if_possible(vortex, 'field.strength', frame)
            vortex.keyframe_insert(data_path="location", frame=frame)
            vortex.keyframe_insert(data_path="rotation_euler", frame=frame)


def update_physics_accents(frames):
    accents = sorted(iter_objects_prefix("PhysicsAccent_"), key=lambda obj: obj.name)
    bands = ["low", "mid", "high", "beat", "onset"]
    center = atom_center()
    update_central_fields(frames, center)

    controls = []
    for idx, obj in enumerate(accents):
        anchor = bpy.data.objects.get(f"PhysicsAnchor_{idx:02d}")
        mat, emit_socket, mix_socket = ensure_accent_material(obj, idx)
        clear_animation(obj)
        clear_animation(anchor)
        if mat is not None and mat.use_nodes:
            clear_animation(mat.node_tree)
        try:
            if obj.rigid_body is not None:
                obj.rigid_body.kinematic = True
        except Exception:
            pass

        obj["hot_band"] = bands[idx % len(bands)]
        obj["hot_response"] = float(obj.get("hot_response", 0.42 + (idx % 7) * 0.075))
        obj["hot_phase"] = float(obj.get("hot_phase", idx * 0.61))
        store_base_vector(obj, "_hot_base_rotation", obj.rotation_euler)

        dx = float(obj.location.x - center.x)
        dy = float(obj.location.y - center.y)
        radius_span = max(0.01, PHYSICS_ORBIT_RADIUS_MAX - PHYSICS_ORBIT_RADIUS_MIN)
        fallback_radius = PHYSICS_ORBIT_RADIUS_MIN + radius_span * ((idx % 6) / 5.0)
        orbit_radius = get_or_store_float(obj, "_hot_orbit_radius", max(0.20, math.sqrt(dx * dx + dy * dy) or fallback_radius))
        orbit_angle = get_or_store_float(obj, "_hot_orbit_angle", math.atan2(dy, dx) if dx or dy else idx * 0.55)
        orbit_z_offset = get_or_store_float(obj, "_hot_orbit_z_offset", float(obj.location.z - center.z))
        orbit_speed = get_or_store_float(
            obj,
            "_hot_orbit_speed",
            PHYSICS_ATOM_ORBIT_SPEED_MIN + (idx % 7) / 6.0 * (PHYSICS_ATOM_ORBIT_SPEED_MAX - PHYSICS_ATOM_ORBIT_SPEED_MIN),
        )
        orbit_tilt = get_or_store_float(obj, "_hot_orbit_tilt", -0.35 + (idx % 5) * 0.175)
        micro_radius = get_or_store_float(obj, "_hot_micro_radius", PHYSICS_ATOM_MICRO_WOBBLE * (0.55 + (idx % 4) * 0.18))

        controls.append({
            "object": obj,
            "anchor": anchor,
            "material": mat,
            "emission_socket": emit_socket,
            "mix_socket": mix_socket,
            "band": obj["hot_band"],
            "response": obj["hot_response"],
            "phase": obj["hot_phase"],
            "base_rotation": obj["_hot_base_rotation"],
            "orbit_radius": orbit_radius,
            "orbit_angle": orbit_angle,
            "orbit_z_offset": orbit_z_offset,
            "orbit_speed": orbit_speed,
            "orbit_tilt": orbit_tilt,
            "micro_radius": micro_radius,
        })

    if not controls:
        return 0

    if not frames:
        frames = [{"low": 0.3, "mid": 0.2, "high": 0.2, "onset": 0.0, "beat": 0.0}]

    for frame, sample in enumerate(frames, start=1):
        for item in controls:
            obj = item["object"]
            anchor = item["anchor"]
            response = item["response"]
            phase = item["phase"]
            drive = drive_for_band(item["band"], response, sample, frame, phase)
            low = float(sample.get("low", 0.0))
            high = float(sample.get("high", 0.0))
            beat = float(sample.get("beat", 0.0))

            speed = item["orbit_speed"] + drive * PHYSICS_ATOM_ORBIT_AUDIO_SPEED + beat * 0.004
            angle = item["orbit_angle"] + frame * speed + math.sin(frame * 0.012 + phase) * 0.055
            radius = item["orbit_radius"] * (
                1.0
                + drive * PHYSICS_ATOM_ORBIT_RADIUS_PULSE
                + low * 0.035
                - high * 0.012
            )
            y_radius = radius * (0.82 + math.cos(item["orbit_tilt"]) * 0.10)

            anchor_x = center.x + math.cos(angle) * radius
            anchor_y = center.y + math.sin(angle) * y_radius
            anchor_z = (
                center.z
                + item["orbit_z_offset"]
                + math.sin(angle * 1.31 + item["orbit_tilt"]) * PHYSICS_ATOM_ORBIT_HEIGHT_SWAY * (0.35 + drive)
                + low * 0.10
                + beat * 0.045
            )

            if anchor is not None:
                anchor.location.x = anchor_x
                anchor.location.y = anchor_y
                anchor.location.z = anchor_z
                anchor.keyframe_insert(data_path="location", frame=frame)

            micro_angle = angle * 2.70 + frame * (0.010 + drive * 0.010) + phase
            micro_drive = item["micro_radius"] * (0.55 + drive * 0.85)
            obj.location.x = anchor_x + math.cos(micro_angle) * micro_drive
            obj.location.y = anchor_y + math.sin(micro_angle) * micro_drive * 0.72
            obj.location.z = anchor_z + math.sin(micro_angle * 1.17) * micro_drive * 0.54
            obj.keyframe_insert(data_path="location", frame=frame)

            rot = item["base_rotation"]
            obj.rotation_euler.x = rot[0] + math.sin(frame * 0.017 + phase) * 0.10 * (0.35 + drive)
            obj.rotation_euler.y = rot[1] + math.cos(frame * 0.015 + phase) * 0.08 * (0.35 + drive)
            obj.rotation_euler.z = rot[2] + angle + frame * (0.006 + drive * 0.006) + math.sin(frame * 0.011 + phase) * 0.04
            obj.keyframe_insert(data_path="rotation_euler", frame=frame)

            if item["emission_socket"] is not None:
                item["emission_socket"].default_value = PHYSICS_ACCENT_EMISSION_MIN + drive * (
                    PHYSICS_ACCENT_EMISSION_MAX - PHYSICS_ACCENT_EMISSION_MIN
                )
                keyframe_if_possible(item["emission_socket"], "default_value", frame)

            if item["mix_socket"] is not None:
                item["mix_socket"].default_value = PHYSICS_ACCENT_MIX_MIN + drive * (
                    PHYSICS_ACCENT_MIX_MAX - PHYSICS_ACCENT_MIX_MIN
                )
                keyframe_if_possible(item["mix_socket"], "default_value", frame)

    return len(controls)
