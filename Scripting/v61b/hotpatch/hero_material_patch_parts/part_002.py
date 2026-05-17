def patch_hero_materials(frames):
    controls = collect_hero_controls()
    for control in controls:
        clear_animation(control.get("node_tree"))

    if not controls:
        return 0

    if not frames:
        frames = [{"low": 0.25, "mid": 0.25, "high": 0.25, "onset": 0.0, "beat": 0.0}]

    for frame, sample in enumerate(frames, start=1):
        high = float(sample.get("high", 0.0))
        mid = float(sample.get("mid", 0.0))
        low = float(sample.get("low", 0.0))
        onset = float(sample.get("onset", 0.0))
        beat = float(sample.get("beat", 0.0))
        pulse = max(onset, beat)
        material_drive = min(1.0, 0.18 + high * 0.48 + mid * 0.20 + pulse * 0.34)
        surface_drive = min(1.0, low * 0.24 + mid * 0.28 + high * 0.34 + onset * 0.26)

        for idx, control in enumerate(controls):
            phase = idx * 0.47
            shimmer = max(0.0, math.sin(frame * 0.017 + phase)) * 0.08

            emission_socket = control.get("emission_socket")
            if emission_socket is not None:
                emission_socket.default_value = HERO_MATERIAL_EMISSION_MIN + min(
                    1.0, material_drive + shimmer
                ) * (HERO_MATERIAL_EMISSION_MAX - HERO_MATERIAL_EMISSION_MIN)
                keyframe_if_possible(emission_socket, "default_value", frame)

            self_light_socket = control.get("self_light_socket")
            if self_light_socket is not None:
                edge_drive = min(
                    1.0, material_drive * 0.74 + surface_drive * 0.18 + pulse * 0.16 + shimmer
                )
                self_light_socket.default_value = HERO_MATERIAL_SELF_LIGHT_MIN + edge_drive * (
                    HERO_MATERIAL_SELF_LIGHT_MAX - HERO_MATERIAL_SELF_LIGHT_MIN
                )
                keyframe_if_possible(self_light_socket, "default_value", frame)

            roughness_socket = control.get("roughness_socket")
            if roughness_socket is not None:
                roughness_socket.default_value = HERO_MATERIAL_ROUGHNESS_MAX - material_drive * (
                    HERO_MATERIAL_ROUGHNESS_MAX - HERO_MATERIAL_ROUGHNESS_MIN
                )
                keyframe_if_possible(roughness_socket, "default_value", frame)

            bump_socket = control.get("bump_socket")
            if bump_socket is not None:
                bump_socket.default_value = HERO_MATERIAL_BUMP_MIN + surface_drive * (
                    HERO_MATERIAL_BUMP_MAX - HERO_MATERIAL_BUMP_MIN
                )
                keyframe_if_possible(bump_socket, "default_value", frame)

            noise_scale_socket = control.get("noise_scale_socket")
            if noise_scale_socket is not None:
                noise_scale_socket.default_value = HERO_MATERIAL_NOISE_SCALE_MIN + surface_drive * (
                    HERO_MATERIAL_NOISE_SCALE_MAX - HERO_MATERIAL_NOISE_SCALE_MIN
                )
                keyframe_if_possible(noise_scale_socket, "default_value", frame)

            mapping_location_socket = control.get("mapping_location_socket")
            if mapping_location_socket is not None:
                drift = HERO_MATERIAL_MAPPING_DRIFT
                loc = mapping_location_socket.default_value
                loc[0] = math.sin(frame * 0.012 + phase) * drift + mid * drift * 0.45
                loc[1] = math.cos(frame * 0.010 + phase) * drift + high * drift * 0.35
                loc[2] = frame * 0.0018 + pulse * drift * 0.20
                keyframe_if_possible(mapping_location_socket, "default_value", frame)

            mapping_rotation_socket = control.get("mapping_rotation_socket")
            if mapping_rotation_socket is not None:
                rot = mapping_rotation_socket.default_value
                rot[0] = math.sin(frame * 0.006 + phase) * 0.08 * (0.35 + surface_drive)
                rot[1] = math.cos(frame * 0.005 + phase) * 0.06 * (0.30 + material_drive)
                rot[2] = frame * 0.0025 + pulse * 0.09
                keyframe_if_possible(mapping_rotation_socket, "default_value", frame)

    return len(controls)
