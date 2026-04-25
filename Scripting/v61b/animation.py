import math

from config import (
    HERO_SCALE_MIN,
    HERO_SCALE_MAX,
    HERO_BOUNCE_Z,
    HERO_ROT_Z,
    HERO_ROT_X,
    HERO_ROT_Y,
    HERO_DRIFT_X,
    HERO_DRIFT_Y,
    HERO_ORBIT_X,
    HERO_ORBIT_Y,
    HERO_BEAT_TWIST_Z,
    HERO_ONSET_SHAKE,
    HERO_DEFORM_STRENGTH_MIN,
    HERO_DEFORM_STRENGTH_MAX,
    HERO_DEFORM_DETAIL_STRENGTH_MAX,
    HERO_DEFORM_WAVE_HEIGHT_MAX,
    HERO_DEFORM_TWIST_MAX,
    HERO_DEFORM_CONTROLLER_RADIUS,
    HERO_DEFORM_KEYFRAME_STEP,
    HERO_MATERIAL_EMISSION_MIN,
    HERO_MATERIAL_EMISSION_MAX,
    HERO_MATERIAL_SELF_LIGHT_MIN,
    HERO_MATERIAL_SELF_LIGHT_MAX,
    HERO_MATERIAL_BUMP_MIN,
    HERO_MATERIAL_BUMP_MAX,
    HERO_MATERIAL_ROUGHNESS_MIN,
    HERO_MATERIAL_ROUGHNESS_MAX,
    HERO_MATERIAL_NOISE_SCALE_MIN,
    HERO_MATERIAL_NOISE_SCALE_MAX,
    HERO_MATERIAL_MAPPING_DRIFT,
    AURA_DEFORM_KEYFRAME_STEP,
    AURA_DEFORM_FIELD_DRIFT,
    AURA_DEFORM_FIELD_SCALE,
    SECONDARY_SCALE_MIN,
    SECONDARY_SCALE_MAX,
    SECONDARY_BOUNCE_Z,
    SECONDARY_DRIFT_X,
    SECONDARY_DRIFT_Y,
    SECONDARY_ROT_Z,
    SECONDARY_ROT_X,
    CAMERA_BEAT_BUMP_Z,
    CAMERA_BEAT_BUMP_Y,
    CAMERA_ORBIT_AMOUNT,
    CAMERA_PUSH_AMOUNT,
    CAMERA_VERTICAL_SWAY,
    LIGHT_ENERGY_MIN,
    LIGHT_ENERGY_MAX,
    PHYSICS_ACCENT_EMISSION_MIN,
    PHYSICS_ACCENT_EMISSION_MAX,
    PHYSICS_ACCENT_MIX_MIN,
    PHYSICS_ACCENT_MIX_MAX,
    PHYSICS_ATOM_ORBIT_SPEED_MIN,
    PHYSICS_ATOM_ORBIT_AUDIO_SPEED,
    PHYSICS_ATOM_ORBIT_RADIUS_PULSE,
    PHYSICS_ATOM_ORBIT_HEIGHT_SWAY,
    PHYSICS_ATOM_MICRO_WOBBLE,
    COMPOSITOR_GLARE_THRESHOLD_MIN,
    COMPOSITOR_GLARE_THRESHOLD_MAX,
    COMPOSITOR_LENS_DISTORT_MIN,
    COMPOSITOR_LENS_DISTORT_MAX,
    COMPOSITOR_LENS_DISPERSION_MIN,
    COMPOSITOR_LENS_DISPERSION_MAX,
    FIELD_STRENGTH_MIN,
    FIELD_STRENGTH_MAX,
    HERO_GRAVITY_STRENGTH_MIN,
    HERO_GRAVITY_STRENGTH_MAX,
    TURB_STRENGTH_MIN,
    TURB_STRENGTH_MAX,
    VORTEX_STRENGTH_MIN,
    VORTEX_STRENGTH_MAX,
    RHYTHM_PARTICLE_SIZE_MIN,
    RHYTHM_PARTICLE_SIZE_MAX,
    RHYTHM_PARTICLE_NORMAL_MIN,
    RHYTHM_PARTICLE_NORMAL_MAX,
    RHYTHM_PARTICLE_TANGENT_MIN,
    RHYTHM_PARTICLE_TANGENT_MAX,
    RHYTHM_PARTICLE_BROWNIAN_MIN,
    RHYTHM_PARTICLE_BROWNIAN_MAX,
    RHYTHM_PARTICLE_EMIT_MIN,
    RHYTHM_PARTICLE_EMIT_MAX,
    RHYTHM_PARTICLE_KEYFRAME_STEP,
    ALBUM_LETTER_PARTICLE_SIZE_MIN,
    ALBUM_LETTER_PARTICLE_SIZE_MAX,
    ALBUM_LETTER_ROOT_SCALE_MIN,
    ALBUM_LETTER_ROOT_SCALE_MAX,
    BACKDROP_EMISSION_MIN,
    BACKDROP_EMISSION_MAX,
    BACKDROP_BREATHE_SCALE,
    MIST_FLOAT_AMPLITUDE,
    MIST_BEAT_BOOST,
)
from fog_dynamics import animate_fog_frame
from scene_utils import set_linear_interpolation_idblock


def keyframe_if_possible(idblock, data_path, frame):
    try:
        idblock.keyframe_insert(data_path=data_path, frame=frame)
    except Exception:
        pass


def get_scene_compositor_tree(scene):
    for attr in ("node_tree", "compositor_node_tree"):
        tree = getattr(scene, attr, None)
        if tree is not None:
            return tree
    return None


def rhythm_band_drive(band, response, low, mid, high, onset, beat, pulse, local_pulse):
    band = str(band)
    response = float(response)

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

    return min(1.0, max(0.0, drive * response))


def animate_scene(
    scene,
    frames,
    camera,
    target,
    hero_asset,
    secondary_asset,
    aura_data,
    fog_controller,
    scene_base,
    lights,
    physics_data,
    mist_particles,
    variants,
    energy_rings,
    energy_ribbons,
):
    total_frames = len(frames)

    hero_root = hero_asset["root"]
    hero_base_scale = hero_asset["base_scale"].copy()
    hero_base_loc = hero_asset["base_location"].copy()
    hero_base_rot = hero_asset["base_rotation"].copy()
    hero_deform_controller = hero_asset.get("deform_controller")
    hero_deformers = hero_asset.get("deformers", [])
    hero_material_controls = hero_asset.get("material_controls", [])
    hero_deform_base_loc = hero_deform_controller.location.copy() if hero_deform_controller else None
    hero_deform_base_rot = hero_deform_controller.rotation_euler.copy() if hero_deform_controller else None
    hero_deform_base_scale = hero_deform_controller.scale.copy() if hero_deform_controller else None

    secondary_root = None
    secondary_base_scale = None
    secondary_base_loc = None
    secondary_base_rot = None

    if secondary_asset is not None:
        secondary_root = secondary_asset["root"]
        secondary_base_scale = secondary_asset["base_scale"].copy()
        secondary_base_loc = secondary_asset["base_location"].copy()
        secondary_base_rot = secondary_asset["base_rotation"].copy()

    aura_obj = aura_data["object"]
    aura_base_loc = aura_obj.location.copy()
    aura_audio_controller = aura_data.get("audio_controller")
    aura_deform_field = aura_data.get("deform_field")
    aura_audio_props = aura_data.get("audio_props", [])
    aura_audio_base_loc = aura_audio_controller.location.copy() if aura_audio_controller else None
    aura_audio_base_rot = aura_audio_controller.rotation_euler.copy() if aura_audio_controller else None
    aura_audio_base_scale = aura_audio_controller.scale.copy() if aura_audio_controller else None
    aura_field_base_loc = aura_deform_field.location.copy() if aura_deform_field else None
    aura_field_base_rot = aura_deform_field.rotation_euler.copy() if aura_deform_field else None
    aura_field_base_scale = aura_deform_field.scale.copy() if aura_deform_field else None

    fog_obj = fog_controller["object"] if fog_controller else None
    fog_control = fog_controller.get("controller") if fog_controller else None
    fog_base_loc = fog_controller.get("base_location") if fog_controller else None
    fog_base_scale = fog_controller.get("base_scale") if fog_controller else None

    backdrop = scene_base.get("backdrop") if scene_base else None
    backdrop_control = scene_base.get("backdrop_controller") if scene_base else None
    backdrop_controls = scene_base.get("backdrop_controls", {}) if scene_base else {}
    backdrop_base_loc = scene_base.get("backdrop_base_location") if scene_base else None
    backdrop_base_scale = scene_base.get("backdrop_base_scale") if scene_base else None

    cam_base_loc = camera.location.copy()
    target_base_loc = target.location.copy()

    compositor_glare = None
    compositor_lens = None
    compositor_tree = get_scene_compositor_tree(scene)
    if compositor_tree is not None:
        compositor_glare = compositor_tree.nodes.get("AudioSoftGlare")
        compositor_lens = compositor_tree.nodes.get("AudioLensBreath")

    force_obj = physics_data["force_obj"]
    turb_obj = physics_data["turb_obj"]
    vortex_obj = physics_data["vortex_obj"]
    wind_left = physics_data["wind_left"]
    wind_right = physics_data["wind_right"]
    accents = physics_data["accents"]
    rhythm_particles = physics_data.get("rhythm_particles", [])

    for i, sample in enumerate(frames, start=1):
        if i % 100 == 0:
            print(f"[ANIMATE] frame {i}/{total_frames}")

        low = float(sample["low"])
        mid = float(sample["mid"])
        high = float(sample["high"])
        onset = float(sample["onset"])
        beat = float(sample["beat"])

        pulse = max(onset, beat)
        bass_drive = min(1.0, low * 0.78 + beat * 0.35)
        transient = min(1.0, onset * 0.68 + beat * 0.55)

        # HERO
        s = HERO_SCALE_MIN + bass_drive * (HERO_SCALE_MAX - HERO_SCALE_MIN) + transient * 0.035
        hero_root.scale = (
            hero_base_scale.x * s,
            hero_base_scale.y * s,
            hero_base_scale.z * s,
        )

        hero_root.location.x = (
            hero_base_loc.x
            + math.sin(i * 0.025) * HERO_DRIFT_X * (0.35 + mid * 0.65)
            + math.sin(i * 0.071) * HERO_ORBIT_X * (0.25 + transient)
        )
        hero_root.location.y = (
            hero_base_loc.y
            + math.cos(i * 0.020) * HERO_DRIFT_Y * (0.25 + high * 0.75)
            + math.cos(i * 0.063) * HERO_ORBIT_Y * (0.25 + pulse)
        )
        hero_root.location.z = (
            hero_base_loc.z
            + bass_drive * HERO_BOUNCE_Z
            + transient * 0.16
            + math.sin(i * 0.045) * 0.035
        )

        onset_shake_x = math.sin(i * 0.43) * transient * HERO_ONSET_SHAKE
        onset_shake_y = math.cos(i * 0.37) * transient * HERO_ONSET_SHAKE * 0.65

        hero_root.rotation_euler.x = (
            hero_base_rot.x
            + math.sin(i * 0.030) * HERO_ROT_X * (0.30 + mid * 0.70)
            + onset_shake_x
        )
        hero_root.rotation_euler.y = (
            hero_base_rot.y
            + math.cos(i * 0.018) * HERO_ROT_Y * (0.20 + high * 0.80)
            + onset_shake_y
        )
        hero_root.rotation_euler.z = (
            hero_base_rot.z
            + math.sin(i * 0.020) * HERO_ROT_Z * (0.35 + pulse * 0.65)
            + beat * HERO_BEAT_TWIST_Z
            + onset * math.sin(i * 0.19) * HERO_BEAT_TWIST_Z * 0.35
        )

        hero_root.keyframe_insert(data_path="scale", frame=i)
        hero_root.keyframe_insert(data_path="location", frame=i)
        hero_root.keyframe_insert(data_path="rotation_euler", frame=i)

        # HERO MESH DEFORMATION
        deform_keyframe = (
            i == 1
            or i == total_frames
            or i % HERO_DEFORM_KEYFRAME_STEP == 0
            or beat > 0.0
            or onset > 0.72
        )

        if hero_deformers and deform_keyframe:
            deform_drive = min(1.0, low * 0.58 + mid * 0.20 + transient * 0.52)
            if hero_deform_controller is not None:
                hero_deform_controller.location.x = (
                    hero_deform_base_loc.x
                    + math.sin(i * 0.036) * HERO_DEFORM_CONTROLLER_RADIUS * (0.45 + deform_drive)
                )
                hero_deform_controller.location.y = (
                    hero_deform_base_loc.y
                    + math.cos(i * 0.031) * HERO_DEFORM_CONTROLLER_RADIUS * (0.35 + pulse)
                )
                hero_deform_controller.location.z = (
                    hero_deform_base_loc.z
                    + math.sin(i * 0.027) * HERO_DEFORM_CONTROLLER_RADIUS * 0.28
                    + beat * 0.08
                )
                hero_deform_controller.rotation_euler.x = hero_deform_base_rot.x + i * 0.006 + high * 0.14
                hero_deform_controller.rotation_euler.y = hero_deform_base_rot.y + math.sin(i * 0.022) * 0.18
                hero_deform_controller.rotation_euler.z = hero_deform_base_rot.z + i * 0.010 + onset * 0.24

                deform_scale = 1.0 + deform_drive * 0.18
                hero_deform_controller.scale = (
                    hero_deform_base_scale.x * deform_scale,
                    hero_deform_base_scale.y * (1.0 + high * 0.12),
                    hero_deform_base_scale.z * (1.0 + low * 0.10),
                )

                hero_deform_controller.keyframe_insert(data_path="location", frame=i)
                hero_deform_controller.keyframe_insert(data_path="rotation_euler", frame=i)
                hero_deform_controller.keyframe_insert(data_path="scale", frame=i)

            for item in hero_deformers:
                phase = item["phase"]
                modifier = item["modifier"]
                ripple = 0.5 + 0.5 * math.sin(i * 0.045 + phase)
                main_strength_max = item.get("main_strength_max", HERO_DEFORM_STRENGTH_MAX)
                strength = HERO_DEFORM_STRENGTH_MIN + deform_drive * (
                    main_strength_max - HERO_DEFORM_STRENGTH_MIN
                )
                modifier.strength = strength * (0.74 + ripple * 0.26)
                keyframe_if_possible(modifier, "strength", i)

                detail_modifier = item.get("detail_modifier")
                if detail_modifier is not None:
                    detail_drive = min(1.0, high * 0.56 + onset * 0.46 + deform_drive * 0.30)
                    detail_modifier.strength = detail_drive * item.get(
                        "detail_strength_max",
                        HERO_DEFORM_DETAIL_STRENGTH_MAX,
                    )
                    keyframe_if_possible(detail_modifier, "strength", i)

                wave_modifier = item.get("wave_modifier")
                if wave_modifier is not None:
                    wave_drive = min(1.0, beat * 0.72 + onset * 0.36 + low * 0.20)
                    try:
                        wave_modifier.height = wave_drive * item.get(
                            "wave_height_max",
                            HERO_DEFORM_WAVE_HEIGHT_MAX,
                        )
                        keyframe_if_possible(wave_modifier, "height", i)
                    except Exception:
                        pass
                    try:
                        wave_modifier.time_offset = -i * 0.018 - phase
                        keyframe_if_possible(wave_modifier, "time_offset", i)
                    except Exception:
                        pass

                twist_modifier = item.get("twist_modifier")
                if twist_modifier is not None:
                    twist_drive = min(1.0, mid * 0.42 + beat * 0.42 + onset * 0.34 + high * 0.18)
                    twist_angle_max = item.get("twist_angle_max", HERO_DEFORM_TWIST_MAX)
                    try:
                        twist_modifier.angle = math.sin(i * 0.030 + phase) * twist_drive * twist_angle_max
                        keyframe_if_possible(twist_modifier, "angle", i)
                    except Exception:
                        pass

        if hero_material_controls and deform_keyframe:
            material_drive = min(1.0, high * 0.54 + mid * 0.22 + pulse * 0.38)
            surface_drive = min(1.0, low * 0.24 + mid * 0.28 + high * 0.34 + onset * 0.26)

            for control in hero_material_controls:
                emission_socket = control.get("emission_socket")
                if emission_socket is not None:
                    emission_socket.default_value = HERO_MATERIAL_EMISSION_MIN + material_drive * (
                        HERO_MATERIAL_EMISSION_MAX - HERO_MATERIAL_EMISSION_MIN
                    )
                    keyframe_if_possible(emission_socket, "default_value", i)

                self_light_socket = control.get("self_light_socket")
                if self_light_socket is not None:
                    edge_drive = min(1.0, material_drive * 0.74 + surface_drive * 0.18 + pulse * 0.16)
                    self_light_socket.default_value = HERO_MATERIAL_SELF_LIGHT_MIN + edge_drive * (
                        HERO_MATERIAL_SELF_LIGHT_MAX - HERO_MATERIAL_SELF_LIGHT_MIN
                    )
                    keyframe_if_possible(self_light_socket, "default_value", i)

                roughness_socket = control.get("roughness_socket")
                if roughness_socket is not None:
                    roughness_socket.default_value = HERO_MATERIAL_ROUGHNESS_MAX - material_drive * (
                        HERO_MATERIAL_ROUGHNESS_MAX - HERO_MATERIAL_ROUGHNESS_MIN
                    )
                    keyframe_if_possible(roughness_socket, "default_value", i)

                bump_socket = control.get("bump_socket")
                if bump_socket is not None:
                    bump_socket.default_value = HERO_MATERIAL_BUMP_MIN + surface_drive * (
                        HERO_MATERIAL_BUMP_MAX - HERO_MATERIAL_BUMP_MIN
                    )
                    keyframe_if_possible(bump_socket, "default_value", i)

                noise_scale_socket = control.get("noise_scale_socket")
                if noise_scale_socket is not None:
                    noise_scale_socket.default_value = HERO_MATERIAL_NOISE_SCALE_MIN + surface_drive * (
                        HERO_MATERIAL_NOISE_SCALE_MAX - HERO_MATERIAL_NOISE_SCALE_MIN
                    )
                    keyframe_if_possible(noise_scale_socket, "default_value", i)

                mapping_location_socket = control.get("mapping_location_socket")
                if mapping_location_socket is not None:
                    drift = HERO_MATERIAL_MAPPING_DRIFT
                    loc = mapping_location_socket.default_value
                    loc[0] = math.sin(i * 0.012) * drift + mid * drift * 0.45
                    loc[1] = math.cos(i * 0.010) * drift + high * drift * 0.35
                    loc[2] = i * 0.0018 + pulse * drift * 0.20
                    keyframe_if_possible(mapping_location_socket, "default_value", i)

                mapping_rotation_socket = control.get("mapping_rotation_socket")
                if mapping_rotation_socket is not None:
                    rot = mapping_rotation_socket.default_value
                    rot[0] = math.sin(i * 0.006) * 0.08 * (0.35 + surface_drive)
                    rot[1] = math.cos(i * 0.005) * 0.06 * (0.30 + material_drive)
                    rot[2] = i * 0.0025 + pulse * 0.09
                    keyframe_if_possible(mapping_rotation_socket, "default_value", i)

        # SECONDARY ASSET
        if secondary_root is not None:
            ss = SECONDARY_SCALE_MIN + low * (SECONDARY_SCALE_MAX - SECONDARY_SCALE_MIN)
            secondary_root.scale = (
                secondary_base_scale.x * ss,
                secondary_base_scale.y * ss,
                secondary_base_scale.z * ss,
            )

            secondary_root.location.x = secondary_base_loc.x + math.sin(i * 0.018) * SECONDARY_DRIFT_X * (0.35 + mid * 0.65)
            secondary_root.location.y = secondary_base_loc.y + math.cos(i * 0.022) * SECONDARY_DRIFT_Y * (0.30 + high * 0.70)
            secondary_root.location.z = secondary_base_loc.z + low * SECONDARY_BOUNCE_Z + pulse * 0.06

            secondary_root.rotation_euler.x = secondary_base_rot.x + math.sin(i * 0.024) * SECONDARY_ROT_X * (0.35 + high * 0.65)
            secondary_root.rotation_euler.y = secondary_base_rot.y + math.cos(i * 0.016) * math.radians(3.0) * (0.25 + mid * 0.75)
            secondary_root.rotation_euler.z = secondary_base_rot.z + math.sin(i * 0.014) * SECONDARY_ROT_Z * (0.35 + pulse * 0.65)

            secondary_root.keyframe_insert(data_path="scale", frame=i)
            secondary_root.keyframe_insert(data_path="location", frame=i)
            secondary_root.keyframe_insert(data_path="rotation_euler", frame=i)

        # AURA
        aura_obj.location.z = aura_base_loc.z + low * 0.08 + pulse * 0.04
        aura_obj.scale = (
            1.0 + low * 0.06,
            1.0 + low * 0.06,
            1.0 + low * 0.06,
        )
        aura_obj.keyframe_insert(data_path="location", frame=i)
        aura_obj.keyframe_insert(data_path="scale", frame=i)

        aura_strength = 0.10 + (pulse * 0.55 + high * 0.45) * 1.25
        if aura_data.get("strength_socket") is not None:
            aura_data["strength_socket"].default_value = aura_strength
            aura_data["strength_socket"].keyframe_insert(data_path="default_value", frame=i)

        try:
            aura_edge = max(0.05, min(0.42, 0.18 - high * 0.05 + pulse * 0.10))
            if aura_data.get("edge_ctrl") is not None:
                aura_data["edge_ctrl"].position = aura_edge
                aura_data["edge_ctrl"].keyframe_insert(data_path="position", frame=i)
        except Exception:
            pass

        # AURA AUDIO SAMPLER / INVISIBLE DEFORM FIELD
        aura_sample_keyframe = (
            i == 1
            or i == total_frames
            or i % AURA_DEFORM_KEYFRAME_STEP == 0
            or beat > 0.0
            or onset > 0.72
        )

        if aura_audio_controller is not None and aura_sample_keyframe:
            aura_deform = min(1.0, low * 0.44 + mid * 0.24 + transient * 0.58)
            aura_detail = min(1.0, high * 0.60 + onset * 0.55 + beat * 0.25)
            phase = i * 0.011 + mid * 0.35 + onset * 0.18
            audio_values = {
                "low": low,
                "mid": mid,
                "high": high,
                "onset": onset,
                "beat": beat,
                "pulse": pulse,
                "aura_deform": aura_deform,
                "detail": aura_detail,
                "phase": phase,
            }

            for prop in aura_audio_props:
                if prop not in audio_values:
                    continue
                aura_audio_controller[prop] = audio_values[prop]
                keyframe_if_possible(aura_audio_controller, f'["{prop}"]', i)

            aura_audio_controller.location.x = aura_audio_base_loc.x + math.sin(i * 0.018) * 0.18
            aura_audio_controller.location.y = aura_audio_base_loc.y + math.cos(i * 0.016) * 0.14
            aura_audio_controller.location.z = aura_audio_base_loc.z + aura_deform * 0.20
            aura_audio_controller.rotation_euler.x = aura_audio_base_rot.x + i * 0.006 + high * 0.18
            aura_audio_controller.rotation_euler.y = aura_audio_base_rot.y + math.sin(i * 0.021) * 0.14
            aura_audio_controller.rotation_euler.z = aura_audio_base_rot.z + phase
            aura_sampler_scale = 1.0 + aura_deform * 0.22
            aura_audio_controller.scale = (
                aura_audio_base_scale.x * aura_sampler_scale,
                aura_audio_base_scale.y * (1.0 + aura_detail * 0.12),
                aura_audio_base_scale.z * (1.0 + low * 0.10),
            )
            aura_audio_controller.keyframe_insert(data_path="location", frame=i)
            aura_audio_controller.keyframe_insert(data_path="rotation_euler", frame=i)
            aura_audio_controller.keyframe_insert(data_path="scale", frame=i)

            if aura_deform_field is not None:
                aura_deform_field.location.x = aura_field_base_loc.x + math.sin(i * 0.025) * AURA_DEFORM_FIELD_DRIFT * (0.35 + mid)
                aura_deform_field.location.y = aura_field_base_loc.y + math.cos(i * 0.020) * AURA_DEFORM_FIELD_DRIFT * (0.25 + high)
                aura_deform_field.location.z = aura_field_base_loc.z + aura_deform * 0.16 + beat * 0.06
                aura_deform_field.rotation_euler.x = aura_field_base_rot.x + i * 0.009 + high * 0.22
                aura_deform_field.rotation_euler.y = aura_field_base_rot.y + math.sin(i * 0.031) * 0.20 + onset * 0.08
                aura_deform_field.rotation_euler.z = aura_field_base_rot.z + i * 0.013 + low * 0.12

                compact = 1.0 - aura_deform * AURA_DEFORM_FIELD_SCALE * 0.45
                stretch = 1.0 + aura_deform * AURA_DEFORM_FIELD_SCALE
                aura_deform_field.scale = (
                    aura_field_base_scale.x * compact,
                    aura_field_base_scale.y * (1.0 + aura_detail * AURA_DEFORM_FIELD_SCALE * 0.45),
                    aura_field_base_scale.z * stretch,
                )
                aura_deform_field.keyframe_insert(data_path="location", frame=i)
                aura_deform_field.keyframe_insert(data_path="rotation_euler", frame=i)
                aura_deform_field.keyframe_insert(data_path="scale", frame=i)

        # LIGHTS
        if lights:
            for light in lights:
                try:
                    area_drive = min(1.0, high * 0.006 + mid * 0.006 + low * 0.005 + pulse * 0.004)
                    light.data.energy = LIGHT_ENERGY_MIN + area_drive * (
                        LIGHT_ENERGY_MAX - LIGHT_ENERGY_MIN
                    )
                    light.data.keyframe_insert(data_path="energy", frame=i)
                except Exception:
                    pass

        # COMPOSITOR BREATH
        if deform_keyframe:
            comp_drive = min(1.0, high * 0.52 + onset * 0.34 + beat * 0.22)

            if compositor_glare is not None:
                try:
                    compositor_glare.threshold = COMPOSITOR_GLARE_THRESHOLD_MAX - comp_drive * (
                        COMPOSITOR_GLARE_THRESHOLD_MAX - COMPOSITOR_GLARE_THRESHOLD_MIN
                    )
                    keyframe_if_possible(compositor_glare, "threshold", i)
                except Exception:
                    pass

            if compositor_lens is not None:
                try:
                    if "Distort" in compositor_lens.inputs:
                        compositor_lens.inputs["Distort"].default_value = COMPOSITOR_LENS_DISTORT_MIN + comp_drive * (
                            COMPOSITOR_LENS_DISTORT_MAX - COMPOSITOR_LENS_DISTORT_MIN
                        )
                        keyframe_if_possible(compositor_lens.inputs["Distort"], "default_value", i)
                    if "Dispersion" in compositor_lens.inputs:
                        compositor_lens.inputs["Dispersion"].default_value = (
                            COMPOSITOR_LENS_DISPERSION_MIN
                            + comp_drive * (COMPOSITOR_LENS_DISPERSION_MAX - COMPOSITOR_LENS_DISPERSION_MIN)
                        )
                        keyframe_if_possible(compositor_lens.inputs["Dispersion"], "default_value", i)
                except Exception:
                    pass

        # FOG
        animate_fog_frame(
            frame=i,
            low=low,
            mid=mid,
            high=high,
            onset=onset,
            beat=beat,
            pulse=pulse,
            fog_controller=fog_controller,
            fog_obj=fog_obj,
            fog_control=fog_control,
            fog_base_scale=fog_base_scale,
            fog_base_loc=fog_base_loc,
        )

        # BACKDROP
        if backdrop is not None and backdrop_controls:
            backdrop_drive = min(0.22, high * 0.035 + mid * 0.025 + pulse * 0.020)
            if "emission_socket" in backdrop_controls:
                backdrop_controls["emission_socket"].default_value = BACKDROP_EMISSION_MIN + backdrop_drive * (
                    BACKDROP_EMISSION_MAX - BACKDROP_EMISSION_MIN
                )
                backdrop_controls["emission_socket"].keyframe_insert(data_path="default_value", frame=i)

            if "mapping_location_socket" in backdrop_controls:
                bloc = backdrop_controls["mapping_location_socket"].default_value
                bloc[0] = i * 0.00018 + math.sin(i * 0.006) * 0.012
                bloc[1] = i * 0.00012 + backdrop_drive * 0.015
                bloc[2] = 0.0
                backdrop_controls["mapping_location_socket"].keyframe_insert(data_path="default_value", frame=i)

            if "noise_scale_socket" in backdrop_controls:
                backdrop_controls["noise_scale_socket"].default_value = 2.18 + backdrop_drive * 0.12
                backdrop_controls["noise_scale_socket"].keyframe_insert(data_path="default_value", frame=i)

            if backdrop_base_scale is not None and backdrop_base_loc is not None:
                bscale = 1.0 + backdrop_drive * BACKDROP_BREATHE_SCALE
                backdrop.scale = (
                    backdrop_base_scale.x * bscale,
                    backdrop_base_scale.y * (1.0 + backdrop_drive * BACKDROP_BREATHE_SCALE * 0.55),
                    backdrop_base_scale.z,
                )
                backdrop.location.z = backdrop_base_loc.z + math.sin(i * 0.009) * 0.012
                backdrop.keyframe_insert(data_path="scale", frame=i)
                backdrop.keyframe_insert(data_path="location", frame=i)

            if backdrop_control is not None and backdrop_base_loc is not None:
                backdrop_control.location.x = backdrop_base_loc.x
                backdrop_control.location.y = backdrop_base_loc.y
                backdrop_control.location.z = backdrop_base_loc.z + backdrop_drive * 0.012
                backdrop_control.scale = (1.0 + backdrop_drive * 0.012, 1.0 + backdrop_drive * 0.012, 1.0)
                backdrop_control.keyframe_insert(data_path="location", frame=i)
                backdrop_control.keyframe_insert(data_path="scale", frame=i)

        # MIST
        for item in mist_particles:
            obj = item["object"]
            phase = item["phase"]
            base_loc = item["base_location"]
            base_scale = item["base_scale"]

            obj.location.x = base_loc.x + math.sin(i * 0.012 + phase) * 0.16
            obj.location.y = base_loc.y + math.cos(i * 0.010 + phase) * 0.14
            obj.location.z = base_loc.z + math.sin(i * 0.015 + phase) * MIST_FLOAT_AMPLITUDE + beat * MIST_BEAT_BOOST
            obj.keyframe_insert(data_path="location", frame=i)

            pscale = base_scale + high * 0.02 + pulse * 0.02
            obj.scale = (pscale, pscale, pscale)
            obj.keyframe_insert(data_path="scale", frame=i)

            em_val = 0.10 + high * 0.45 + pulse * 0.35
            mix_val = 0.12 + pulse * 0.08

            item["emission_socket"].default_value = em_val
            item["emission_socket"].keyframe_insert(data_path="default_value", frame=i)

            item["mix_socket"].default_value = mix_val
            item["mix_socket"].keyframe_insert(data_path="default_value", frame=i)

        # VARIANTS
        for idx, item in enumerate(variants):
            obj = item["root"]
            ang = item["angle"]
            base_loc = item["base_location"]
            base_scale = item["base_scale"]
            phase = idx * 0.55

            obj.location.x = base_loc.x + math.sin(i * 0.016 + phase) * 0.20
            obj.location.y = base_loc.y + math.cos(i * 0.014 + phase) * 0.18
            obj.location.z = base_loc.z + high * 0.18 + math.sin(i * 0.018 + phase) * 0.04

            sc = base_scale + low * 0.07
            obj.scale = (sc, sc, sc)
            obj.rotation_euler.z = ang + math.sin(i * 0.012 + phase) * math.radians(14.0)

            obj.keyframe_insert(data_path="location", frame=i)
            obj.keyframe_insert(data_path="scale", frame=i)
            obj.keyframe_insert(data_path="rotation_euler", frame=i)

        # RINGS / RIBBONS
        for item in energy_rings:
            ring = item["object"]
            phase = item["phase"]
            base_scale = item["base_scale"]
            base_rot = item["base_rot"]
            base_loc = item["base_loc"]

            pulse_scale = 1.0 + low * 0.03 + pulse * 0.02
            ring.scale = (
                base_scale.x * pulse_scale,
                base_scale.y * pulse_scale,
                base_scale.z * pulse_scale,
            )
            ring.location.z = base_loc.z + math.sin(i * 0.009 + phase) * 0.05
            ring.rotation_euler.z = base_rot.z + i * 0.006 + phase

            ring.keyframe_insert(data_path="scale", frame=i)
            ring.keyframe_insert(data_path="location", frame=i)
            ring.keyframe_insert(data_path="rotation_euler", frame=i)

            emit = 0.06 + (pulse * 0.40 + high * 0.60) * 0.70
            item["emit_socket"].default_value = emit
            item["emit_socket"].keyframe_insert(data_path="default_value", frame=i)

        for item in energy_ribbons:
            ribbon = item["object"]
            phase = item["phase"]
            base_rot = item["base_rot"]
            base_loc = item["base_loc"]
            base_scale = item["base_scale"]

            ribbon.location.z = base_loc.z + math.sin(i * 0.008 + phase) * 0.12 + low * 0.03
            ribbon.scale = (
                base_scale.x * (1.0 + mid * 0.05),
                base_scale.y * (1.0 + high * 0.04),
                base_scale.z,
            )
            ribbon.rotation_euler.z = base_rot.z + i * 0.007 + phase * 0.25

            ribbon.keyframe_insert(data_path="location", frame=i)
            ribbon.keyframe_insert(data_path="scale", frame=i)
            ribbon.keyframe_insert(data_path="rotation_euler", frame=i)

            emit = 0.08 + (mid * 0.55 + pulse * 0.45) * 0.82
            item["emit_socket"].default_value = emit
            item["emit_socket"].keyframe_insert(data_path="default_value", frame=i)

        # PHYSICS ACCENTS
        for idx, item in enumerate(accents):
            obj = item["object"]
            anchor = item["anchor"]
            base_loc = item["base_location"]
            base_rot = item.get("base_rotation", obj.rotation_euler)
            phase = item["phase"] + idx * 0.23
            response = item.get("response", 0.65)
            local_pulse = max(0.0, math.sin(i * (0.024 + response * 0.016) + phase)) * 0.20
            accent_drive = rhythm_band_drive(
                item.get("band", "mid"),
                response,
                low,
                mid,
                high,
                onset,
                beat,
                pulse,
                local_pulse,
            )

            orbit_radius = item.get("orbit_radius")
            if orbit_radius is None:
                orbit_radius = max(0.20, math.sqrt(base_loc.x * base_loc.x + base_loc.y * base_loc.y))
            orbit_angle = item.get("orbit_angle", math.atan2(base_loc.y, base_loc.x))
            orbit_speed = item.get("orbit_speed", PHYSICS_ATOM_ORBIT_SPEED_MIN + response * 0.004)
            orbit_tilt = item.get("orbit_tilt", 0.0)
            orbit_z_offset = item.get("orbit_z_offset", base_loc.z - hero_base_loc.z)
            micro_radius = item.get("micro_radius", PHYSICS_ATOM_MICRO_WOBBLE)

            speed = orbit_speed + accent_drive * PHYSICS_ATOM_ORBIT_AUDIO_SPEED + beat * 0.004
            angle = orbit_angle + i * speed + math.sin(i * 0.012 + phase) * 0.055
            radius = orbit_radius * (
                1.0
                + accent_drive * PHYSICS_ATOM_ORBIT_RADIUS_PULSE
                + low * 0.035
                - high * 0.012
            )
            y_radius = radius * (0.82 + math.cos(orbit_tilt) * 0.10)
            atom_center = hero_root.location

            anchor.location.x = atom_center.x + math.cos(angle) * radius
            anchor.location.y = atom_center.y + math.sin(angle) * y_radius
            anchor.location.z = (
                atom_center.z
                + orbit_z_offset
                + math.sin(angle * 1.31 + orbit_tilt) * PHYSICS_ATOM_ORBIT_HEIGHT_SWAY * (0.35 + accent_drive)
                + low * 0.10
                + beat * 0.045
            )
            anchor.keyframe_insert(data_path="location", frame=i)

            micro_angle = angle * 2.70 + i * (0.010 + accent_drive * 0.010) + phase
            micro_drive = micro_radius * (0.55 + accent_drive * 0.85)
            obj.location.x = anchor.location.x + math.cos(micro_angle) * micro_drive
            obj.location.y = anchor.location.y + math.sin(micro_angle) * micro_drive * 0.72
            obj.location.z = anchor.location.z + math.sin(micro_angle * 1.17) * micro_drive * 0.54
            obj.keyframe_insert(data_path="location", frame=i)

            obj.rotation_euler.x = base_rot.x + math.sin(i * 0.017 + phase) * 0.10 * (0.35 + accent_drive)
            obj.rotation_euler.y = base_rot.y + math.cos(i * 0.015 + phase) * 0.08 * (0.35 + accent_drive)
            obj.rotation_euler.z = (
                base_rot.z
                + angle
                + i * (0.006 + accent_drive * 0.006)
                + math.sin(i * 0.011 + phase) * 0.04
            )
            obj.keyframe_insert(data_path="rotation_euler", frame=i)

            emission_socket = item.get("emission_socket")
            if emission_socket is not None:
                emission_socket.default_value = PHYSICS_ACCENT_EMISSION_MIN + accent_drive * (
                    PHYSICS_ACCENT_EMISSION_MAX - PHYSICS_ACCENT_EMISSION_MIN
                )
                keyframe_if_possible(emission_socket, "default_value", i)

            mix_socket = item.get("mix_socket")
            if mix_socket is not None:
                mix_socket.default_value = PHYSICS_ACCENT_MIX_MIN + accent_drive * (
                    PHYSICS_ACCENT_MIX_MAX - PHYSICS_ACCENT_MIX_MIN
                )
                keyframe_if_possible(mix_socket, "default_value", i)

        # FORCE FIELDS
        if force_obj is not None:
            gravity_drive = min(1.0, low * 0.44 + mid * 0.14 + pulse * 0.34 + beat * 0.16)
            strength = HERO_GRAVITY_STRENGTH_MIN + gravity_drive * (
                HERO_GRAVITY_STRENGTH_MAX - HERO_GRAVITY_STRENGTH_MIN
            )
            force_obj.field.strength = -strength
            force_obj.location.x = hero_root.location.x
            force_obj.location.y = hero_root.location.y
            force_obj.location.z = hero_root.location.z + 0.34 + math.sin(i * 0.010) * 0.05
            force_obj.keyframe_insert(data_path='field.strength', frame=i)
            force_obj.keyframe_insert(data_path='location', frame=i)

        if turb_obj is not None:
            turb_strength = TURB_STRENGTH_MIN + high * (TURB_STRENGTH_MAX - TURB_STRENGTH_MIN) * 0.64 + pulse * 0.42
            turb_obj.field.strength = turb_strength
            turb_obj.location.x = hero_root.location.x
            turb_obj.location.y = hero_root.location.y
            turb_obj.location.z = hero_root.location.z + 0.74 + math.sin(i * 0.012) * 0.08
            turb_obj.keyframe_insert(data_path='field.strength', frame=i)
            turb_obj.keyframe_insert(data_path='location', frame=i)

        if vortex_obj is not None:
            vortex_strength = VORTEX_STRENGTH_MIN + (mid * 0.62 + pulse * 0.18) * (
                VORTEX_STRENGTH_MAX - VORTEX_STRENGTH_MIN
            )
            vortex_obj.field.strength = vortex_strength
            vortex_obj.location.x = hero_root.location.x
            vortex_obj.location.y = hero_root.location.y
            vortex_obj.location.z = hero_root.location.z + 0.18
            vortex_obj.rotation_euler.z = i * (0.004 + mid * 0.003 + beat * 0.002)
            vortex_obj.keyframe_insert(data_path='field.strength', frame=i)
            vortex_obj.keyframe_insert(data_path='location', frame=i)
            vortex_obj.keyframe_insert(data_path='rotation_euler', frame=i)

        if wind_left is not None:
            wl = onset * 6.0 + beat * 2.0
            wind_left.field.strength = wl
            wind_left.keyframe_insert(data_path='field.strength', frame=i)

        if wind_right is not None:
            wr = high * 4.0 + beat * 1.8
            wind_right.field.strength = wr
            wind_right.keyframe_insert(data_path='field.strength', frame=i)

        # RHYTHM PARTICLE PHYSICS
        particle_keyframe = (
            i == 1
            or i == total_frames
            or i % RHYTHM_PARTICLE_KEYFRAME_STEP == 0
            or beat > 0.0
            or onset > 0.72
        )

        if particle_keyframe:
            for item in rhythm_particles:
                emitter = item["emitter"]
                settings = item["settings"]
                settings_list = item.get("settings_list", [settings])
                mode = item["mode"]
                phase = item["phase"]
                base_loc = item["base_location"]
                base_rot = item["base_rotation"]
                base_scale = item["base_scale"]

                if mode == "pulse":
                    drive = min(1.0, beat * 0.90 + onset * 0.62 + low * 0.28)
                    settings.normal_factor = RHYTHM_PARTICLE_NORMAL_MIN + drive * (
                        RHYTHM_PARTICLE_NORMAL_MAX - RHYTHM_PARTICLE_NORMAL_MIN
                    )
                    settings.tangent_factor = RHYTHM_PARTICLE_TANGENT_MIN + (mid * 0.55 + drive * 0.45) * (
                        RHYTHM_PARTICLE_TANGENT_MAX - RHYTHM_PARTICLE_TANGENT_MIN
                    )
                    settings.brownian_factor = RHYTHM_PARTICLE_BROWNIAN_MIN + (high * 0.45 + drive * 0.55) * (
                        RHYTHM_PARTICLE_BROWNIAN_MAX - RHYTHM_PARTICLE_BROWNIAN_MIN
                    )
                    settings.particle_size = RHYTHM_PARTICLE_SIZE_MIN + drive * (
                        RHYTHM_PARTICLE_SIZE_MAX - RHYTHM_PARTICLE_SIZE_MIN
                    )
                    item["emission_socket"].default_value = RHYTHM_PARTICLE_EMIT_MIN + drive * (
                        RHYTHM_PARTICLE_EMIT_MAX - RHYTHM_PARTICLE_EMIT_MIN
                    )

                    emitter.location.z = base_loc.z + low * 0.10 + transient * 0.06
                    scale_boost = 1.0 + drive * 0.12
                    emitter.rotation_euler.z = base_rot.z + i * 0.010 + math.sin(i * 0.019 + phase) * 0.08

                elif mode == "dust":
                    drive = min(1.0, mid * 0.46 + low * 0.26 + pulse * 0.18)
                    settings.normal_factor = 0.025 + drive * 0.35
                    settings.tangent_factor = 0.08 + drive * 0.42
                    settings.brownian_factor = 0.28 + (high * 0.55 + drive * 0.45) * 0.78
                    settings.particle_size = RHYTHM_PARTICLE_SIZE_MIN * (0.58 + drive * 0.55)
                    item["emission_socket"].default_value = 0.10 + (high * 0.36 + drive * 0.38) * 0.90

                    emitter.location.x = base_loc.x + math.sin(i * 0.008 + phase) * 0.18
                    emitter.location.y = base_loc.y + math.cos(i * 0.007 + phase) * 0.16
                    emitter.location.z = base_loc.z + math.sin(i * 0.010 + phase) * 0.08 + low * 0.05
                    scale_boost = 1.0 + drive * 0.04
                    emitter.rotation_euler.z = base_rot.z + i * 0.003 + phase

                elif mode == "streak":
                    drive = min(1.0, high * 0.85 + onset * 0.45 + beat * 0.20)
                    settings.normal_factor = 0.18 + drive * 1.72
                    settings.tangent_factor = 0.35 + drive * 1.10
                    settings.brownian_factor = 0.04 + drive * 0.38
                    settings.particle_size = RHYTHM_PARTICLE_SIZE_MIN * (0.70 + drive * 0.95)
                    item["emission_socket"].default_value = 0.12 + drive * 1.70

                    emitter.location.z = base_loc.z + high * 0.22 + transient * 0.05
                    scale_boost = 1.0 + drive * 0.08
                    emitter.rotation_euler.z = base_rot.z - i * 0.014 + phase

                else:
                    drive = min(1.0, mid * 0.42 + onset * 0.44 + beat * 0.36 + high * 0.20)
                    settings.normal_factor = 0.08 + drive * 0.92
                    settings.tangent_factor = 0.24 + drive * 0.88
                    settings.brownian_factor = 0.06 + drive * 0.54
                    settings.particle_size = ALBUM_LETTER_PARTICLE_SIZE_MIN + drive * (
                        ALBUM_LETTER_PARTICLE_SIZE_MAX - ALBUM_LETTER_PARTICLE_SIZE_MIN
                    )

                    emitter.location.x = base_loc.x + math.sin(i * 0.011 + phase) * 0.24
                    emitter.location.y = base_loc.y + math.cos(i * 0.009 + phase) * 0.20
                    emitter.location.z = base_loc.z + mid * 0.18 + beat * 0.10
                    scale_boost = 1.0 + drive * 0.10
                    emitter.rotation_euler.z = base_rot.z + i * 0.006 + phase

                    letter_root = item.get("letter_root")
                    if letter_root is not None:
                        letter_scale = ALBUM_LETTER_ROOT_SCALE_MIN + drive * (
                            ALBUM_LETTER_ROOT_SCALE_MAX - ALBUM_LETTER_ROOT_SCALE_MIN
                        )
                        letter_root.scale = (letter_scale, letter_scale, letter_scale)
                        letter_root.rotation_euler.z = math.sin(i * 0.018 + phase) * 0.12
                        letter_root.keyframe_insert(data_path="scale", frame=i)
                        letter_root.keyframe_insert(data_path="rotation_euler", frame=i)

                    for letter in item.get("letter_sources", []):
                        obj = letter["object"]
                        lphase = letter["phase"]
                        lscale = 1.0 + drive * 0.20 + math.sin(i * 0.030 + lphase) * 0.035
                        obj.scale = (
                            letter["base_scale"].x * lscale,
                            letter["base_scale"].y * (1.0 + high * 0.14),
                            letter["base_scale"].z * (1.0 + beat * 0.18),
                        )
                        obj.keyframe_insert(data_path="scale", frame=i)

                emitter.scale = (
                    base_scale.x * scale_boost,
                    base_scale.y * scale_boost,
                    base_scale.z * scale_boost,
                )

                for extra_settings in settings_list[1:]:
                    extra_settings.normal_factor = settings.normal_factor
                    extra_settings.tangent_factor = settings.tangent_factor
                    extra_settings.brownian_factor = settings.brownian_factor
                    extra_settings.particle_size = settings.particle_size

                for particle_settings in settings_list:
                    keyframe_if_possible(particle_settings, "normal_factor", i)
                    keyframe_if_possible(particle_settings, "tangent_factor", i)
                    keyframe_if_possible(particle_settings, "brownian_factor", i)
                    keyframe_if_possible(particle_settings, "particle_size", i)
                if item.get("emission_socket") is not None:
                    keyframe_if_possible(item["emission_socket"], "default_value", i)
                emitter.keyframe_insert(data_path="location", frame=i)
                emitter.keyframe_insert(data_path="rotation_euler", frame=i)
                emitter.keyframe_insert(data_path="scale", frame=i)

        # CAMERA
        camera.location.x = cam_base_loc.x + math.sin(i * 0.020) * CAMERA_ORBIT_AMOUNT
        camera.location.y = cam_base_loc.y + low * CAMERA_PUSH_AMOUNT - beat * CAMERA_BEAT_BUMP_Y
        camera.location.z = cam_base_loc.z + beat * CAMERA_BEAT_BUMP_Z + math.sin(i * 0.018) * CAMERA_VERTICAL_SWAY + high * 0.08
        camera.keyframe_insert(data_path="location", frame=i)

        target.location.x = target_base_loc.x + (mid - 0.5) * 0.40
        target.location.y = target_base_loc.y
        target.location.z = target_base_loc.z + low * 0.25 + high * 0.08
        target.keyframe_insert(data_path="location", frame=i)

    set_linear_interpolation_idblock(hero_root)
    if hero_deform_controller is not None:
        set_linear_interpolation_idblock(hero_deform_controller)
    for item in hero_deformers:
        set_linear_interpolation_idblock(item.get("mesh"))
    for control in hero_material_controls:
        set_linear_interpolation_idblock(control.get("node_tree"))
    compositor_tree = get_scene_compositor_tree(scene)
    if compositor_tree is not None:
        set_linear_interpolation_idblock(compositor_tree)
    if aura_audio_controller is not None:
        set_linear_interpolation_idblock(aura_audio_controller)
    if aura_deform_field is not None:
        set_linear_interpolation_idblock(aura_deform_field)
    if secondary_root is not None:
        set_linear_interpolation_idblock(secondary_root)
    set_linear_interpolation_idblock(aura_obj)
    set_linear_interpolation_idblock(camera)
    set_linear_interpolation_idblock(target)

    if lights:
        for light in lights:
            try:
                set_linear_interpolation_idblock(light.data)
            except Exception:
                pass

    for item in mist_particles:
        set_linear_interpolation_idblock(item["object"])
        if item["material"]:
            set_linear_interpolation_idblock(item["material"].node_tree)

    for item in variants:
        set_linear_interpolation_idblock(item["root"])

    for item in accents:
        set_linear_interpolation_idblock(item["anchor"])
        set_linear_interpolation_idblock(item["object"])
        if item.get("material"):
            set_linear_interpolation_idblock(item["material"].node_tree)

    for item in rhythm_particles:
        set_linear_interpolation_idblock(item.get("emitter"))
        set_linear_interpolation_idblock(item.get("settings"))
        for settings in item.get("settings_list", []):
            set_linear_interpolation_idblock(settings)
        set_linear_interpolation_idblock(item.get("letter_root"))
        for letter in item.get("letter_sources", []):
            set_linear_interpolation_idblock(letter.get("object"))
        if item.get("material"):
            set_linear_interpolation_idblock(item["material"].node_tree)

    for item in energy_rings:
        set_linear_interpolation_idblock(item["object"])
        if item["object"].active_material:
            set_linear_interpolation_idblock(item["object"].active_material.node_tree)

    for item in energy_ribbons:
        set_linear_interpolation_idblock(item["object"])
        if item["object"].active_material:
            set_linear_interpolation_idblock(item["object"].active_material.node_tree)

    aura_material = getattr(aura_obj, "active_material", None)
    if aura_material:
        set_linear_interpolation_idblock(aura_material.node_tree)

    floor = scene.objects.get("PeaceFloor")
    if floor and floor.active_material:
        set_linear_interpolation_idblock(floor.active_material.node_tree)

    if fog_controller and fog_controller["object"] and fog_controller["object"].active_material:
        set_linear_interpolation_idblock(fog_controller["object"])
        set_linear_interpolation_idblock(fog_controller["object"].active_material.node_tree)
    if fog_control is not None:
        set_linear_interpolation_idblock(fog_control)

    if backdrop is not None:
        set_linear_interpolation_idblock(backdrop)
        if backdrop.active_material:
            set_linear_interpolation_idblock(backdrop.active_material.node_tree)
    if backdrop_control is not None:
        set_linear_interpolation_idblock(backdrop_control)

    if force_obj is not None:
        set_linear_interpolation_idblock(force_obj)
    if turb_obj is not None:
        set_linear_interpolation_idblock(turb_obj)
    if vortex_obj is not None:
        set_linear_interpolation_idblock(vortex_obj)
    if wind_left is not None:
        set_linear_interpolation_idblock(wind_left)
    if wind_right is not None:
        set_linear_interpolation_idblock(wind_right)
