# Project Code Chunk 15/212

- File: `Scripting/v61b/animation.py`
- Part: `4`
- Lines: `683-893`

## Symbol Map
- Imports: `math`, `from config import HERO_SCALE_MIN, HERO_SCALE_MAX, HERO_BOUNCE_Z, HERO_ROT_Z, HERO_ROT_X, HERO_ROT_Y, HERO_DRIFT_X, HERO_DRIFT_Y, HERO_ORBIT_X, HERO_ORBIT_Y, HERO_BEAT_TWIST_Z, HERO_ONSET_SHAKE, HERO_DEFORM_STRENGTH_MIN, HERO_DEFORM_STRENGTH_MAX, HERO_DEFORM_DETAIL_STRENGTH_MAX, HERO_DEFORM_WAVE_HEIGHT_MAX, HERO_DEFORM_TWIST_MAX, HERO_DEFORM_CONTROLLER_RADIUS, HERO_DEFORM_KEYFRAME_STEP, HERO_MATERIAL_EMISSION_MIN, HERO_MATERIAL_EMISSION_MAX, HERO_MATERIAL_SELF_LIGHT_MIN, HERO_MATERIAL_SELF_LIGHT_MAX, HERO_MATERIAL_BUMP_MIN, HERO_MATERIAL_BUMP_MAX, HERO_MATERIAL_ROUGHNESS_MIN, HERO_MATERIAL_ROUGHNESS_MAX, HERO_MATERIAL_NOISE_SCALE_MIN, HERO_MATERIAL_NOISE_SCALE_MAX, HERO_MATERIAL_MAPPING_DRIFT, AURA_DEFORM_KEYFRAME_STEP, AURA_DEFORM_FIELD_DRIFT, AURA_DEFORM_FIELD_SCALE, SECONDARY_SCALE_MIN, SECONDARY_SCALE_MAX, SECONDARY_BOUNCE_Z, SECONDARY_DRIFT_X, SECONDARY_DRIFT_Y, SECONDARY_ROT_Z, SECONDARY_ROT_X, CAMERA_BEAT_BUMP_Z, CAMERA_BEAT_BUMP_Y, CAMERA_ORBIT_AMOUNT, CAMERA_PUSH_AMOUNT, CAMERA_VERTICAL_SWAY, LIGHT_ENERGY_MIN, LIGHT_ENERGY_MAX, PHYSICS_ACCENT_EMISSION_MIN, PHYSICS_ACCENT_EMISSION_MAX, PHYSICS_ACCENT_MIX_MIN, PHYSICS_ACCENT_MIX_MAX, PHYSICS_ATOM_ORBIT_SPEED_MIN, PHYSICS_ATOM_ORBIT_AUDIO_SPEED, PHYSICS_ATOM_ORBIT_RADIUS_PULSE, PHYSICS_ATOM_ORBIT_HEIGHT_SWAY, PHYSICS_ATOM_MICRO_WOBBLE, COMPOSITOR_GLARE_THRESHOLD_MIN, COMPOSITOR_GLARE_THRESHOLD_MAX, COMPOSITOR_LENS_DISTORT_MIN, COMPOSITOR_LENS_DISTORT_MAX, COMPOSITOR_LENS_DISPERSION_MIN, COMPOSITOR_LENS_DISPERSION_MAX, FIELD_STRENGTH_MIN, FIELD_STRENGTH_MAX, HERO_GRAVITY_STRENGTH_MIN, HERO_GRAVITY_STRENGTH_MAX, TURB_STRENGTH_MIN, TURB_STRENGTH_MAX, VORTEX_STRENGTH_MIN, VORTEX_STRENGTH_MAX, RHYTHM_PARTICLE_SIZE_MIN, RHYTHM_PARTICLE_SIZE_MAX, RHYTHM_PARTICLE_NORMAL_MIN, RHYTHM_PARTICLE_NORMAL_MAX, RHYTHM_PARTICLE_TANGENT_MIN, RHYTHM_PARTICLE_TANGENT_MAX, RHYTHM_PARTICLE_BROWNIAN_MIN, RHYTHM_PARTICLE_BROWNIAN_MAX, RHYTHM_PARTICLE_EMIT_MIN, RHYTHM_PARTICLE_EMIT_MAX, RHYTHM_PARTICLE_KEYFRAME_STEP, ALBUM_LETTER_PARTICLE_SIZE_MIN, ALBUM_LETTER_PARTICLE_SIZE_MAX, ALBUM_LETTER_ROOT_SCALE_MIN, ALBUM_LETTER_ROOT_SCALE_MAX, BACKDROP_EMISSION_MIN, BACKDROP_EMISSION_MAX, BACKDROP_BREATHE_SCALE, MIST_FLOAT_AMPLITUDE, MIST_BEAT_BOOST`, `from fog_dynamics import animate_fog_frame`, `from scene_utils import set_linear_interpolation_idblock`
- Functions: `keyframe_if_possible(idblock, data_path, frame)` line 99; `get_scene_compositor_tree(scene)` line 106; `rhythm_band_drive(band, response, low, mid, high, onset, beat, pulse, local_pulse)` line 114; `animate_scene(scene, frames, camera, target, hero_asset, secondary_asset, aura_data, fog_controller, scene_base, lights, physics_data, mist_particles, variants, energy_rings, energy_ribbons)` line 132

## Content
```py
00683:                 base_scale.x * pulse_scale,
00684:                 base_scale.y * pulse_scale,
00685:                 base_scale.z * pulse_scale,
00686:             )
00687:             ring.location.z = base_loc.z + math.sin(i * 0.009 + phase) * 0.05
00688:             ring.rotation_euler.z = base_rot.z + i * 0.006 + phase
00689: 
00690:             ring.keyframe_insert(data_path="scale", frame=i)
00691:             ring.keyframe_insert(data_path="location", frame=i)
00692:             ring.keyframe_insert(data_path="rotation_euler", frame=i)
00693: 
00694:             emit = 0.06 + (pulse * 0.40 + high * 0.60) * 0.70
00695:             item["emit_socket"].default_value = emit
00696:             item["emit_socket"].keyframe_insert(data_path="default_value", frame=i)
00697: 
00698:         for item in energy_ribbons:
00699:             ribbon = item["object"]
00700:             phase = item["phase"]
00701:             base_rot = item["base_rot"]
00702:             base_loc = item["base_loc"]
00703:             base_scale = item["base_scale"]
00704: 
00705:             ribbon.location.z = base_loc.z + math.sin(i * 0.008 + phase) * 0.12 + low * 0.03
00706:             ribbon.scale = (
00707:                 base_scale.x * (1.0 + mid * 0.05),
00708:                 base_scale.y * (1.0 + high * 0.04),
00709:                 base_scale.z,
00710:             )
00711:             ribbon.rotation_euler.z = base_rot.z + i * 0.007 + phase * 0.25
00712: 
00713:             ribbon.keyframe_insert(data_path="location", frame=i)
00714:             ribbon.keyframe_insert(data_path="scale", frame=i)
00715:             ribbon.keyframe_insert(data_path="rotation_euler", frame=i)
00716: 
00717:             emit = 0.08 + (mid * 0.55 + pulse * 0.45) * 0.82
00718:             item["emit_socket"].default_value = emit
00719:             item["emit_socket"].keyframe_insert(data_path="default_value", frame=i)
00720: 
00721:         # PHYSICS ACCENTS
00722:         for idx, item in enumerate(accents):
00723:             obj = item["object"]
00724:             anchor = item["anchor"]
00725:             base_loc = item["base_location"]
00726:             base_rot = item.get("base_rotation", obj.rotation_euler)
00727:             phase = item["phase"] + idx * 0.23
00728:             response = item.get("response", 0.65)
00729:             local_pulse = max(0.0, math.sin(i * (0.024 + response * 0.016) + phase)) * 0.20
00730:             accent_drive = rhythm_band_drive(
00731:                 item.get("band", "mid"),
00732:                 response,
00733:                 low,
00734:                 mid,
00735:                 high,
00736:                 onset,
00737:                 beat,
00738:                 pulse,
00739:                 local_pulse,
00740:             )
00741: 
00742:             orbit_radius = item.get("orbit_radius")
00743:             if orbit_radius is None:
00744:                 orbit_radius = max(0.20, math.sqrt(base_loc.x * base_loc.x + base_loc.y * base_loc.y))
00745:             orbit_angle = item.get("orbit_angle", math.atan2(base_loc.y, base_loc.x))
00746:             orbit_speed = item.get("orbit_speed", PHYSICS_ATOM_ORBIT_SPEED_MIN + response * 0.004)
00747:             orbit_tilt = item.get("orbit_tilt", 0.0)
00748:             orbit_z_offset = item.get("orbit_z_offset", base_loc.z - hero_base_loc.z)
00749:             micro_radius = item.get("micro_radius", PHYSICS_ATOM_MICRO_WOBBLE)
00750: 
00751:             speed = orbit_speed + accent_drive * PHYSICS_ATOM_ORBIT_AUDIO_SPEED + beat * 0.004
00752:             angle = orbit_angle + i * speed + math.sin(i * 0.012 + phase) * 0.055
00753:             radius = orbit_radius * (
00754:                 1.0
00755:                 + accent_drive * PHYSICS_ATOM_ORBIT_RADIUS_PULSE
00756:                 + low * 0.035
00757:                 - high * 0.012
00758:             )
00759:             y_radius = radius * (0.82 + math.cos(orbit_tilt) * 0.10)
00760:             atom_center = hero_root.location
00761: 
00762:             anchor.location.x = atom_center.x + math.cos(angle) * radius
00763:             anchor.location.y = atom_center.y + math.sin(angle) * y_radius
00764:             anchor.location.z = (
00765:                 atom_center.z
00766:                 + orbit_z_offset
00767:                 + math.sin(angle * 1.31 + orbit_tilt) * PHYSICS_ATOM_ORBIT_HEIGHT_SWAY * (0.35 + accent_drive)
00768:                 + low * 0.10
00769:                 + beat * 0.045
00770:             )
00771:             anchor.keyframe_insert(data_path="location", frame=i)
00772: 
00773:             micro_angle = angle * 2.70 + i * (0.010 + accent_drive * 0.010) + phase
00774:             micro_drive = micro_radius * (0.55 + accent_drive * 0.85)
00775:             obj.location.x = anchor.location.x + math.cos(micro_angle) * micro_drive
00776:             obj.location.y = anchor.location.y + math.sin(micro_angle) * micro_drive * 0.72
00777:             obj.location.z = anchor.location.z + math.sin(micro_angle * 1.17) * micro_drive * 0.54
00778:             obj.keyframe_insert(data_path="location", frame=i)
00779: 
00780:             obj.rotation_euler.x = base_rot.x + math.sin(i * 0.017 + phase) * 0.10 * (0.35 + accent_drive)
00781:             obj.rotation_euler.y = base_rot.y + math.cos(i * 0.015 + phase) * 0.08 * (0.35 + accent_drive)
00782:             obj.rotation_euler.z = (
00783:                 base_rot.z
00784:                 + angle
00785:                 + i * (0.006 + accent_drive * 0.006)
00786:                 + math.sin(i * 0.011 + phase) * 0.04
00787:             )
00788:             obj.keyframe_insert(data_path="rotation_euler", frame=i)
00789: 
00790:             emission_socket = item.get("emission_socket")
00791:             if emission_socket is not None:
00792:                 emission_socket.default_value = PHYSICS_ACCENT_EMISSION_MIN + accent_drive * (
00793:                     PHYSICS_ACCENT_EMISSION_MAX - PHYSICS_ACCENT_EMISSION_MIN
00794:                 )
00795:                 keyframe_if_possible(emission_socket, "default_value", i)
00796: 
00797:             mix_socket = item.get("mix_socket")
00798:             if mix_socket is not None:
00799:                 mix_socket.default_value = PHYSICS_ACCENT_MIX_MIN + accent_drive * (
00800:                     PHYSICS_ACCENT_MIX_MAX - PHYSICS_ACCENT_MIX_MIN
00801:                 )
00802:                 keyframe_if_possible(mix_socket, "default_value", i)
00803: 
00804:         # FORCE FIELDS
00805:         if force_obj is not None:
00806:             gravity_drive = min(1.0, low * 0.44 + mid * 0.14 + pulse * 0.34 + beat * 0.16)
00807:             strength = HERO_GRAVITY_STRENGTH_MIN + gravity_drive * (
00808:                 HERO_GRAVITY_STRENGTH_MAX - HERO_GRAVITY_STRENGTH_MIN
00809:             )
00810:             force_obj.field.strength = -strength
00811:             force_obj.location.x = hero_root.location.x
00812:             force_obj.location.y = hero_root.location.y
00813:             force_obj.location.z = hero_root.location.z + 0.34 + math.sin(i * 0.010) * 0.05
00814:             force_obj.keyframe_insert(data_path='field.strength', frame=i)
00815:             force_obj.keyframe_insert(data_path='location', frame=i)
00816: 
00817:         if turb_obj is not None:
00818:             turb_strength = TURB_STRENGTH_MIN + high * (TURB_STRENGTH_MAX - TURB_STRENGTH_MIN) * 0.64 + pulse * 0.42
00819:             turb_obj.field.strength = turb_strength
00820:             turb_obj.location.x = hero_root.location.x
00821:             turb_obj.location.y = hero_root.location.y
00822:             turb_obj.location.z = hero_root.location.z + 0.74 + math.sin(i * 0.012) * 0.08
00823:             turb_obj.keyframe_insert(data_path='field.strength', frame=i)
00824:             turb_obj.keyframe_insert(data_path='location', frame=i)
00825: 
00826:         if vortex_obj is not None:
00827:             vortex_strength = VORTEX_STRENGTH_MIN + (mid * 0.62 + pulse * 0.18) * (
00828:                 VORTEX_STRENGTH_MAX - VORTEX_STRENGTH_MIN
00829:             )
00830:             vortex_obj.field.strength = vortex_strength
00831:             vortex_obj.location.x = hero_root.location.x
00832:             vortex_obj.location.y = hero_root.location.y
00833:             vortex_obj.location.z = hero_root.location.z + 0.18
00834:             vortex_obj.rotation_euler.z = i * (0.004 + mid * 0.003 + beat * 0.002)
00835:             vortex_obj.keyframe_insert(data_path='field.strength', frame=i)
00836:             vortex_obj.keyframe_insert(data_path='location', frame=i)
00837:             vortex_obj.keyframe_insert(data_path='rotation_euler', frame=i)
00838: 
00839:         if wind_left is not None:
00840:             wl = onset * 6.0 + beat * 2.0
00841:             wind_left.field.strength = wl
00842:             wind_left.keyframe_insert(data_path='field.strength', frame=i)
00843: 
00844:         if wind_right is not None:
00845:             wr = high * 4.0 + beat * 1.8
00846:             wind_right.field.strength = wr
00847:             wind_right.keyframe_insert(data_path='field.strength', frame=i)
00848: 
00849:         # RHYTHM PARTICLE PHYSICS
00850:         particle_keyframe = (
00851:             i == 1
00852:             or i == total_frames
00853:             or i % RHYTHM_PARTICLE_KEYFRAME_STEP == 0
00854:             or beat > 0.0
00855:             or onset > 0.72
00856:         )
00857: 
00858:         if particle_keyframe:
00859:             for item in rhythm_particles:
00860:                 emitter = item["emitter"]
00861:                 settings = item["settings"]
00862:                 settings_list = item.get("settings_list", [settings])
00863:                 mode = item["mode"]
00864:                 phase = item["phase"]
00865:                 base_loc = item["base_location"]
00866:                 base_rot = item["base_rotation"]
00867:                 base_scale = item["base_scale"]
00868: 
00869:                 if mode == "pulse":
00870:                     drive = min(1.0, beat * 0.90 + onset * 0.62 + low * 0.28)
00871:                     settings.normal_factor = RHYTHM_PARTICLE_NORMAL_MIN + drive * (
00872:                         RHYTHM_PARTICLE_NORMAL_MAX - RHYTHM_PARTICLE_NORMAL_MIN
00873:                     )
00874:                     settings.tangent_factor = RHYTHM_PARTICLE_TANGENT_MIN + (mid * 0.55 + drive * 0.45) * (
00875:                         RHYTHM_PARTICLE_TANGENT_MAX - RHYTHM_PARTICLE_TANGENT_MIN
00876:                     )
00877:                     settings.brownian_factor = RHYTHM_PARTICLE_BROWNIAN_MIN + (high * 0.45 + drive * 0.55) * (
00878:                         RHYTHM_PARTICLE_BROWNIAN_MAX - RHYTHM_PARTICLE_BROWNIAN_MIN
00879:                     )
00880:                     settings.particle_size = RHYTHM_PARTICLE_SIZE_MIN + drive * (
00881:                         RHYTHM_PARTICLE_SIZE_MAX - RHYTHM_PARTICLE_SIZE_MIN
00882:                     )
00883:                     item["emission_socket"].default_value = RHYTHM_PARTICLE_EMIT_MIN + drive * (
00884:                         RHYTHM_PARTICLE_EMIT_MAX - RHYTHM_PARTICLE_EMIT_MIN
00885:                     )
00886: 
00887:                     emitter.location.z = base_loc.z + low * 0.10 + transient * 0.06
00888:                     scale_boost = 1.0 + drive * 0.12
00889:                     emitter.rotation_euler.z = base_rot.z + i * 0.010 + math.sin(i * 0.019 + phase) * 0.08
00890: 
00891:                 elif mode == "dust":
00892:                     drive = min(1.0, mid * 0.46 + low * 0.26 + pulse * 0.18)
00893:                     settings.normal_factor = 0.025 + drive * 0.35
```
