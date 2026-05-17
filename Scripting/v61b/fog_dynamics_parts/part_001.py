import math

from config import (
    FOG_CLUMP_RAMP_HIGH_BASE,
    FOG_CLUMP_RAMP_LOW_BASE,
    FOG_CLUMP_SCALE_MAX,
    FOG_CLUMP_SCALE_MIN,
    FOG_CLUMP_WEIGHT_MAX,
    FOG_CLUMP_WEIGHT_MIN,
    FOG_COMPACT_XY,
    FOG_CONTROLLER_DRIFT,
    FOG_DENSITY_MAX,
    FOG_DENSITY_MIN,
    FOG_DRIFT_SPEED_X,
    FOG_DRIFT_SPEED_Y,
    FOG_DRIFT_SPEED_Z,
    FOG_EMISSION_MAX,
    FOG_EMISSION_MIN,
    FOG_EXPAND_Z,
    FOG_FILAMENT_ALPHA_MAX,
    FOG_FILAMENT_ALPHA_MIN,
    FOG_FILAMENT_COMPACT_SCALE,
    FOG_FILAMENT_EMISSION_MAX,
    FOG_FILAMENT_EMISSION_MIN,
    FOG_FILAMENT_KEYFRAME_STEP,
    FOG_FILAMENT_NOISE_SCALE_MAX,
    FOG_FILAMENT_NOISE_SCALE_MIN,
    FOG_FILAMENT_WAVE_SCALE_MAX,
    FOG_FILAMENT_WAVE_SCALE_MIN,
    FOG_FILAMENT_WIND_DRIFT,
    FOG_NOISE_SCALE_MAX,
    FOG_NOISE_SCALE_MIN,
    FOG_RAMP_HIGH_BASE,
    FOG_RAMP_LOW_BASE,
    FOG_VOLUME_ENABLED,
    FOG_VOLUME_VIEWPORT_VISIBLE,
    FOG_WAVE_DISTORTION_MAX,
    FOG_WAVE_DISTORTION_MIN,
    FOG_WAVE_SCALE_MAX,
    FOG_WAVE_SCALE_MIN,
    FOG_WAVE_WEIGHT_MAX,
    FOG_WAVE_WEIGHT_MIN,
    FOG_WIND_SHEAR_X,
    FOG_WIND_SHEAR_Y,
)


def clamp(value, low, high):
    return max(low, min(high, value))


def keyframe_if_possible(idblock, data_path, frame):
    try:
        idblock.keyframe_insert(data_path=data_path, frame=frame)
    except Exception:
        pass


def set_socket_value(socket, value, frame):
    if socket is None:
        return
    try:
        socket.default_value = value
        keyframe_if_possible(socket, "default_value", frame)
    except Exception:
        pass


def animate_vector_socket(socket, values, frame):
    if socket is None:
        return
    try:
        vec = socket.default_value
        for idx, value in enumerate(values):
            if idx < len(vec):
                vec[idx] = value
        keyframe_if_possible(socket, "default_value", frame)
    except Exception:
        pass


def should_keyframe_filaments(frame, beat, onset):
    return (
        frame == 1
        or frame % max(1, int(FOG_FILAMENT_KEYFRAME_STEP)) == 0
        or beat > 0.0
        or onset > 0.72
    )


def animate_fog_filaments(frame, low, mid, high, onset, beat, pulse, filaments):
    if not filaments:
        return

    objects = filaments.get("objects") or []
    controls = filaments.get("controls") or {}
    root = filaments.get("root")
    if not objects and root is None:
        return

    wind = clamp(mid * 0.32 + high * 0.28 + onset * 0.28 + beat * 0.12, 0.0, 1.0)
    compact = clamp(low * 0.36 + mid * 0.20 + pulse * 0.28, 0.0, 1.0)
    disperse = 1.0 - compact
    keyframe = should_keyframe_filaments(frame, beat, onset)
    if not keyframe:
        return

    alpha_drive = clamp(0.16 + compact * 0.34 + pulse * 0.28 + mid * 0.16, 0.0, 1.0)
    alpha = FOG_FILAMENT_ALPHA_MIN + alpha_drive * (FOG_FILAMENT_ALPHA_MAX - FOG_FILAMENT_ALPHA_MIN)
    set_socket_value(controls.get("alpha_socket"), alpha, frame)

    emission_drive = clamp(0.12 + high * 0.28 + onset * 0.22 + beat * 0.18, 0.0, 1.0)
    emission = FOG_FILAMENT_EMISSION_MIN + emission_drive * (
        FOG_FILAMENT_EMISSION_MAX - FOG_FILAMENT_EMISSION_MIN
    )
    set_socket_value(controls.get("emission_socket"), emission, frame)

    noise_scale = FOG_FILAMENT_NOISE_SCALE_MIN + clamp(disperse * 0.32 + wind * 0.38, 0.0, 1.0) * (
        FOG_FILAMENT_NOISE_SCALE_MAX - FOG_FILAMENT_NOISE_SCALE_MIN
    )
    set_socket_value(controls.get("noise_scale_socket"), noise_scale, frame)
    set_socket_value(controls.get("noise_detail_socket"), 10.0 + high * 4.0 + onset * 1.8, frame)
    set_socket_value(
        controls.get("noise_roughness_socket"), clamp(0.54 + compact * 0.12, 0.48, 0.82), frame
    )

    wave_scale = FOG_FILAMENT_WAVE_SCALE_MIN + clamp(wind * 0.56 + disperse * 0.22, 0.0, 1.0) * (
        FOG_FILAMENT_WAVE_SCALE_MAX - FOG_FILAMENT_WAVE_SCALE_MIN
    )
    set_socket_value(controls.get("wave_scale_socket"), wave_scale, frame)
    set_socket_value(controls.get("wave_distortion_socket"), 4.0 + wind * 10.0 + onset * 3.0, frame)
    set_socket_value(controls.get("wave_weight_socket"), 0.12 + compact * 0.26 + wind * 0.18, frame)
    set_socket_value(controls.get("wave_phase_socket"), frame * 0.018 + onset * 0.50, frame)

    animate_vector_socket(
        controls.get("mapping_location_socket"),
        (
            frame * 0.006 + math.sin(frame * 0.008) * wind * 0.18,
            frame * 0.003 + math.cos(frame * 0.006) * wind * 0.16,
            frame * 0.002 + compact * 0.32,
        ),
        frame,
    )
    animate_vector_socket(
        controls.get("mapping_scale_socket"),
        (
            1.0 + compact * 0.32,
            0.74 + disperse * 0.22,
            1.0 + low * 0.18,
        ),
        frame,
    )

    if "ramp_low_ctrl" in controls and controls["ramp_low_ctrl"] is not None:
        ramp_low = clamp(0.32 + compact * 0.08 - wind * 0.04, 0.20, 0.60)
        ramp_high = clamp(0.76 - compact * 0.12 + disperse * 0.04, ramp_low + 0.12, 0.92)
        controls["ramp_low_ctrl"].position = ramp_low
        controls["ramp_high_ctrl"].position = ramp_high
        keyframe_if_possible(controls["ramp_low_ctrl"], "position", frame)
        keyframe_if_possible(controls["ramp_high_ctrl"], "position", frame)

    if root is not None:
        root.location.x = math.sin(frame * 0.006) * FOG_FILAMENT_WIND_DRIFT * (0.20 + wind)
        root.location.y = 4.8 + math.cos(frame * 0.004) * FOG_FILAMENT_WIND_DRIFT * 0.24
        root.location.z = 3.1 + compact * 0.12 + beat * 0.08
        root.scale = (
            1.0 - compact * 0.10,
            1.0 + wind * 0.10,
            1.0 + low * 0.08,
        )
        root.keyframe_insert(data_path="location", frame=frame)
        root.keyframe_insert(data_path="scale", frame=frame)

    for index, item in enumerate(objects):
        obj = item["object"]
        phase = item["phase"]
        base_loc = item["base_location"]
        base_scale = item["base_scale"]
        base_rot = item["base_rotation"]

        side = math.sin(frame * 0.010 + phase)
        lift = math.cos(frame * 0.008 + phase * 0.7)
        swirl = math.sin(frame * 0.006 + phase * 1.3)

        obj.location.x = base_loc.x + side * FOG_FILAMENT_WIND_DRIFT * (0.22 + wind * 0.72)
        obj.location.y = base_loc.y + swirl * FOG_FILAMENT_WIND_DRIFT * (0.12 + mid * 0.28)
        obj.location.z = base_loc.z + lift * 0.12 + beat * 0.06 + compact * 0.08

        width_scale = 1.0 - compact * FOG_FILAMENT_COMPACT_SCALE + wind * 0.08
        height_scale = 1.0 + compact * 0.22 + high * 0.08
        obj.scale = (
            base_scale.x * width_scale,
            base_scale.y * height_scale,
            base_scale.z,
        )

        obj.rotation_euler.x = base_rot.x + math.sin(frame * 0.005 + phase) * 0.035
        obj.rotation_euler.y = base_rot.y + math.cos(frame * 0.004 + phase) * 0.025
        obj.rotation_euler.z = base_rot.z + side * 0.045 + wind * 0.025 + index * 0.001

        obj.keyframe_insert(data_path="location", frame=frame)
        obj.keyframe_insert(data_path="scale", frame=frame)
        obj.keyframe_insert(data_path="rotation_euler", frame=frame)
