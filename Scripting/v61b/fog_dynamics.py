import math

from config import (
    FOG_DENSITY_MIN,
    FOG_DENSITY_MAX,
    FOG_EMISSION_MIN,
    FOG_EMISSION_MAX,
    FOG_NOISE_SCALE_MIN,
    FOG_NOISE_SCALE_MAX,
    FOG_CLUMP_SCALE_MIN,
    FOG_CLUMP_SCALE_MAX,
    FOG_CLUMP_RAMP_LOW_BASE,
    FOG_CLUMP_RAMP_HIGH_BASE,
    FOG_CLUMP_WEIGHT_MIN,
    FOG_CLUMP_WEIGHT_MAX,
    FOG_RAMP_LOW_BASE,
    FOG_RAMP_HIGH_BASE,
    FOG_COMPACT_XY,
    FOG_EXPAND_Z,
    FOG_CONTROLLER_DRIFT,
    FOG_DRIFT_SPEED_X,
    FOG_DRIFT_SPEED_Y,
    FOG_DRIFT_SPEED_Z,
    FOG_WAVE_SCALE_MIN,
    FOG_WAVE_SCALE_MAX,
    FOG_WAVE_DISTORTION_MIN,
    FOG_WAVE_DISTORTION_MAX,
    FOG_WAVE_WEIGHT_MIN,
    FOG_WAVE_WEIGHT_MAX,
    FOG_WIND_SHEAR_X,
    FOG_WIND_SHEAR_Y,
    FOG_VOLUME_ENABLED,
    FOG_VOLUME_VIEWPORT_VISIBLE,
    FOG_FILAMENT_KEYFRAME_STEP,
    FOG_FILAMENT_ALPHA_MIN,
    FOG_FILAMENT_ALPHA_MAX,
    FOG_FILAMENT_EMISSION_MIN,
    FOG_FILAMENT_EMISSION_MAX,
    FOG_FILAMENT_WIND_DRIFT,
    FOG_FILAMENT_COMPACT_SCALE,
    FOG_FILAMENT_NOISE_SCALE_MIN,
    FOG_FILAMENT_NOISE_SCALE_MAX,
    FOG_FILAMENT_WAVE_SCALE_MIN,
    FOG_FILAMENT_WAVE_SCALE_MAX,
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
    set_socket_value(controls.get("noise_roughness_socket"), clamp(0.54 + compact * 0.12, 0.48, 0.82), frame)

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


def animate_fog_frame(
    frame,
    low,
    mid,
    high,
    onset,
    beat,
    pulse,
    fog_controller,
    fog_obj,
    fog_control,
    fog_base_scale,
    fog_base_loc,
):
    if not fog_controller:
        return

    smoke_push = clamp(onset * 0.34 + beat * 0.26 + high * 0.22 + mid * 0.18, 0.0, 1.0)
    fog_compact = clamp(low * 0.36 + mid * 0.22 + pulse * 0.28, 0.0, 1.0)
    fog_disperse = 1.0 - fog_compact
    wind = clamp(mid * 0.30 + high * 0.28 + onset * 0.34 + beat * 0.12, 0.0, 1.0)

    animate_fog_filaments(
        frame=frame,
        low=low,
        mid=mid,
        high=high,
        onset=onset,
        beat=beat,
        pulse=pulse,
        filaments=fog_controller.get("filaments"),
    )

    if not FOG_VOLUME_ENABLED:
        if fog_obj is not None:
            fog_obj.hide_render = True
            fog_obj.hide_viewport = not FOG_VOLUME_VIEWPORT_VISIBLE
        return

    density_drive = clamp(0.24 + low * 0.22 + fog_compact * 0.58 + mid * 0.15, 0.0, 1.0)
    density = FOG_DENSITY_MIN + density_drive * (FOG_DENSITY_MAX - FOG_DENSITY_MIN)
    set_socket_value(fog_controller.get("density_socket"), density, frame)

    emission_drive = clamp(0.10 + high * 0.18 + onset * 0.11 + beat * 0.07, 0.0, 1.0)
    emission = FOG_EMISSION_MIN + emission_drive * (FOG_EMISSION_MAX - FOG_EMISSION_MIN)
    set_socket_value(fog_controller.get("emission_socket"), emission, frame)

    noise_drive = clamp(fog_disperse * 0.28 + high * 0.18 + wind * 0.18 + mid * 0.10, 0.0, 1.0)
    noise_scale = FOG_NOISE_SCALE_MIN + noise_drive * (FOG_NOISE_SCALE_MAX - FOG_NOISE_SCALE_MIN)
    set_socket_value(fog_controller.get("noise_scale_socket"), noise_scale, frame)
    set_socket_value(fog_controller.get("noise_detail_socket"), 8.0 + high * 4.0 + onset * 1.2, frame)
    set_socket_value(
        fog_controller.get("noise_roughness_socket"),
        clamp(0.66 + mid * 0.10 + high * 0.08 - fog_compact * 0.04, 0.52, 0.90),
        frame,
    )

    clump_scale_drive = clamp(fog_disperse * 0.42 + wind * 0.22 + high * 0.18 - fog_compact * 0.12, 0.0, 1.0)
    clump_scale = FOG_CLUMP_SCALE_MIN + clump_scale_drive * (FOG_CLUMP_SCALE_MAX - FOG_CLUMP_SCALE_MIN)
    set_socket_value(fog_controller.get("clump_noise_scale_socket"), clump_scale, frame)
    set_socket_value(fog_controller.get("clump_noise_detail_socket"), 9.0 + high * 3.5 + onset * 1.0, frame)
    set_socket_value(
        fog_controller.get("clump_noise_roughness_socket"),
        clamp(0.70 + fog_compact * 0.08 + wind * 0.05, 0.58, 0.92),
        frame,
    )

    wave_scale = FOG_WAVE_SCALE_MIN + clamp(0.22 + wind * 0.48 + fog_disperse * 0.22, 0.0, 1.0) * (
        FOG_WAVE_SCALE_MAX - FOG_WAVE_SCALE_MIN
    )
    set_socket_value(fog_controller.get("wave_scale_socket"), wave_scale, frame)

    wave_distortion = FOG_WAVE_DISTORTION_MIN + clamp(wind * 0.62 + onset * 0.26 + mid * 0.12, 0.0, 1.0) * (
        FOG_WAVE_DISTORTION_MAX - FOG_WAVE_DISTORTION_MIN
    )
    set_socket_value(fog_controller.get("wave_distortion_socket"), wave_distortion, frame)
    set_socket_value(
        fog_controller.get("wave_weight_socket"),
        FOG_WAVE_WEIGHT_MIN + clamp(fog_compact * 0.28 + wind * 0.30 + beat * 0.12, 0.0, 1.0) * (
            FOG_WAVE_WEIGHT_MAX - FOG_WAVE_WEIGHT_MIN
        ),
        frame,
    )
    set_socket_value(fog_controller.get("wave_phase_socket"), frame * 0.018 + smoke_push * 0.45, frame)

    animate_vector_socket(
        fog_controller.get("mapping_location_socket"),
        (
            frame * FOG_DRIFT_SPEED_X + math.sin(frame * 0.010) * FOG_WIND_SHEAR_X * wind,
            frame * FOG_DRIFT_SPEED_Y + math.cos(frame * 0.008) * FOG_WIND_SHEAR_Y * (0.35 + wind),
            frame * FOG_DRIFT_SPEED_Z + fog_compact * 0.26 + smoke_push * 0.12,
        ),
        frame,
    )

    animate_vector_socket(
        fog_controller.get("mapping_scale_socket"),
        (
            0.64 + fog_compact * 1.10 + high * 0.06,
            0.70 + fog_compact * 0.88 + mid * 0.06,
            1.82 - fog_compact * 0.46 + low * 0.25,
        ),
        frame,
    )

    animate_vector_socket(
        fog_controller.get("mapping_rotation_socket"),
        (
            math.sin(frame * 0.005) * 0.20 + wind * 0.11,
            math.cos(frame * 0.004) * 0.16 + high * 0.07,
            frame * 0.0032 + fog_compact * 0.16 + onset * 0.05,
        ),
        frame,
    )

    set_socket_value(
        fog_controller.get("volume_anisotropy_socket"),
        clamp(0.08 + fog_compact * 0.22 + wind * 0.12, 0.02, 0.48),
        frame,
    )

    color_socket = fog_controller.get("volume_color_socket")
    if color_socket is not None:
        try:
            col = color_socket.default_value
            col[0] = clamp(0.76 + low * 0.055 + beat * 0.020, 0.0, 1.0)
            col[1] = clamp(0.84 + mid * 0.055, 0.0, 1.0)
            col[2] = clamp(0.88 + high * 0.040, 0.0, 1.0)
            if len(col) > 3:
                col[3] = 1.0
            keyframe_if_possible(color_socket, "default_value", frame)
        except Exception:
            pass

    if "ramp_low_ctrl" in fog_controller and "ramp_high_ctrl" in fog_controller:
        ramp_low = clamp(FOG_RAMP_LOW_BASE + fog_compact * 0.090 - wind * 0.026, 0.16, 0.58)
        ramp_high = clamp(FOG_RAMP_HIGH_BASE - fog_compact * 0.145 + low * 0.030, ramp_low + 0.070, 0.82)
        fog_controller["ramp_low_ctrl"].position = ramp_low
        fog_controller["ramp_high_ctrl"].position = ramp_high
        keyframe_if_possible(fog_controller["ramp_low_ctrl"], "position", frame)
        keyframe_if_possible(fog_controller["ramp_high_ctrl"], "position", frame)

    if "clump_ramp_low_ctrl" in fog_controller and "clump_ramp_high_ctrl" in fog_controller:
        clump_weight = clamp(
            FOG_CLUMP_WEIGHT_MIN + fog_compact * (FOG_CLUMP_WEIGHT_MAX - FOG_CLUMP_WEIGHT_MIN),
            FOG_CLUMP_WEIGHT_MIN,
            FOG_CLUMP_WEIGHT_MAX,
        )
        clump_low = clamp(FOG_CLUMP_RAMP_LOW_BASE + fog_compact * 0.095 - wind * 0.035, 0.22, 0.68)
        clump_high = clamp(
            FOG_CLUMP_RAMP_HIGH_BASE - fog_compact * 0.135 + fog_disperse * 0.045 + high * 0.025,
            clump_low + 0.040,
            0.86,
        )
        fog_controller["clump_ramp_low_ctrl"].position = clump_low
        fog_controller["clump_ramp_high_ctrl"].position = clump_high
        keyframe_if_possible(fog_controller["clump_ramp_low_ctrl"], "position", frame)
        keyframe_if_possible(fog_controller["clump_ramp_high_ctrl"], "position", frame)

        boosted_density = density * clump_weight
        set_socket_value(fog_controller.get("density_socket"), boosted_density, frame)

    if fog_obj is not None and fog_base_scale is not None and fog_base_loc is not None:
        compact_xy = 1.0 - fog_compact * FOG_COMPACT_XY
        expand_z = 1.0 + (low * 0.50 + beat * 0.36 + wind * 0.14) * FOG_EXPAND_Z
        fog_obj.scale = (
            fog_base_scale.x * compact_xy,
            fog_base_scale.y * (compact_xy + wind * 0.035),
            fog_base_scale.z * expand_z,
        )
        fog_obj.location.x = fog_base_loc.x + math.sin(frame * 0.007) * FOG_CONTROLLER_DRIFT * (0.18 + wind * 0.32)
        fog_obj.location.y = fog_base_loc.y + math.cos(frame * 0.006) * FOG_CONTROLLER_DRIFT * (0.12 + wind * 0.26)
        fog_obj.location.z = fog_base_loc.z + (low - high) * 0.10 + beat * 0.06
        fog_obj.keyframe_insert(data_path="scale", frame=frame)
        fog_obj.keyframe_insert(data_path="location", frame=frame)

    if fog_control is not None and fog_base_loc is not None:
        fog_control.location.x = fog_base_loc.x + math.sin(frame * 0.010) * FOG_CONTROLLER_DRIFT * (0.40 + wind)
        fog_control.location.y = fog_base_loc.y + math.cos(frame * 0.009) * FOG_CONTROLLER_DRIFT * (0.26 + mid)
        fog_control.location.z = fog_base_loc.z + fog_compact * 0.22 + smoke_push * 0.10
        fog_control.rotation_euler.z = frame * 0.008 + fog_compact * 0.28 + wind * 0.12
        fog_control.scale = (
            1.0 + fog_compact * 0.26,
            1.0 + wind * 0.18,
            1.0 + low * 0.20,
        )
        fog_control.keyframe_insert(data_path="location", frame=frame)
        fog_control.keyframe_insert(data_path="rotation_euler", frame=frame)
        fog_control.keyframe_insert(data_path="scale", frame=frame)
