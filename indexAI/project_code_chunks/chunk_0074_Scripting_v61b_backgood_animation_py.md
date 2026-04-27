# Project Code Chunk 74/212

- File: `Scripting/v61b_backgood/animation.py`
- Part: `4`
- Lines: `683-882`

## Symbol Map
- Imports: `math`, `from config import HERO_SCALE_MIN, HERO_SCALE_MAX, HERO_BOUNCE_Z, HERO_ROT_Z, HERO_ROT_X, HERO_ROT_Y, HERO_DRIFT_X, HERO_DRIFT_Y, HERO_ORBIT_X, HERO_ORBIT_Y, HERO_BEAT_TWIST_Z, HERO_ONSET_SHAKE, HERO_DEFORM_STRENGTH_MIN, HERO_DEFORM_STRENGTH_MAX, HERO_DEFORM_DETAIL_STRENGTH_MAX, HERO_DEFORM_WAVE_HEIGHT_MAX, HERO_DEFORM_TWIST_MAX, HERO_DEFORM_CONTROLLER_RADIUS, HERO_DEFORM_KEYFRAME_STEP, HERO_MATERIAL_EMISSION_MIN, HERO_MATERIAL_EMISSION_MAX, HERO_MATERIAL_SELF_LIGHT_MIN, HERO_MATERIAL_SELF_LIGHT_MAX, HERO_MATERIAL_BUMP_MIN, HERO_MATERIAL_BUMP_MAX, HERO_MATERIAL_ROUGHNESS_MIN, HERO_MATERIAL_ROUGHNESS_MAX, HERO_MATERIAL_NOISE_SCALE_MIN, HERO_MATERIAL_NOISE_SCALE_MAX, HERO_MATERIAL_MAPPING_DRIFT, AURA_DEFORM_KEYFRAME_STEP, AURA_DEFORM_FIELD_DRIFT, AURA_DEFORM_FIELD_SCALE, SECONDARY_SCALE_MIN, SECONDARY_SCALE_MAX, SECONDARY_BOUNCE_Z, SECONDARY_DRIFT_X, SECONDARY_DRIFT_Y, SECONDARY_ROT_Z, SECONDARY_ROT_X, CAMERA_BEAT_BUMP_Z, CAMERA_BEAT_BUMP_Y, CAMERA_ORBIT_AMOUNT, CAMERA_PUSH_AMOUNT, CAMERA_VERTICAL_SWAY, LIGHT_ENERGY_MIN, LIGHT_ENERGY_MAX, PHYSICS_ACCENT_EMISSION_MIN, PHYSICS_ACCENT_EMISSION_MAX, PHYSICS_ACCENT_MIX_MIN, PHYSICS_ACCENT_MIX_MAX, COMPOSITOR_GLARE_THRESHOLD_MIN, COMPOSITOR_GLARE_THRESHOLD_MAX, COMPOSITOR_LENS_DISTORT_MIN, COMPOSITOR_LENS_DISTORT_MAX, COMPOSITOR_LENS_DISPERSION_MIN, COMPOSITOR_LENS_DISPERSION_MAX, FIELD_STRENGTH_MIN, FIELD_STRENGTH_MAX, TURB_STRENGTH_MIN, TURB_STRENGTH_MAX, VORTEX_STRENGTH_MIN, VORTEX_STRENGTH_MAX, RHYTHM_PARTICLE_SIZE_MIN, RHYTHM_PARTICLE_SIZE_MAX, RHYTHM_PARTICLE_NORMAL_MIN, RHYTHM_PARTICLE_NORMAL_MAX, RHYTHM_PARTICLE_TANGENT_MIN, RHYTHM_PARTICLE_TANGENT_MAX, RHYTHM_PARTICLE_BROWNIAN_MIN, RHYTHM_PARTICLE_BROWNIAN_MAX, RHYTHM_PARTICLE_EMIT_MIN, RHYTHM_PARTICLE_EMIT_MAX, RHYTHM_PARTICLE_KEYFRAME_STEP, ALBUM_LETTER_PARTICLE_SIZE_MIN, ALBUM_LETTER_PARTICLE_SIZE_MAX, ALBUM_LETTER_ROOT_SCALE_MIN, ALBUM_LETTER_ROOT_SCALE_MAX, BACKDROP_EMISSION_MIN, BACKDROP_EMISSION_MAX, BACKDROP_BREATHE_SCALE, MIST_FLOAT_AMPLITUDE, MIST_BEAT_BOOST`, `from fog_dynamics import animate_fog_frame`, `from scene_utils import set_linear_interpolation_idblock`
- Functions: `keyframe_if_possible(idblock, data_path, frame)` line 92; `get_scene_compositor_tree(scene)` line 99; `rhythm_band_drive(band, response, low, mid, high, onset, beat, pulse, local_pulse)` line 107; `animate_scene(scene, frames, camera, target, hero_asset, secondary_asset, aura_data, fog_controller, scene_base, lights, physics_data, mist_particles, variants, energy_rings, energy_ribbons)` line 125

## Content
```py
00683:             ring.keyframe_insert(data_path="scale", frame=i)
00684:             ring.keyframe_insert(data_path="location", frame=i)
00685:             ring.keyframe_insert(data_path="rotation_euler", frame=i)
00686: 
00687:             emit = 0.06 + (pulse * 0.40 + high * 0.60) * 0.70
00688:             item["emit_socket"].default_value = emit
00689:             item["emit_socket"].keyframe_insert(data_path="default_value", frame=i)
00690: 
00691:         for item in energy_ribbons:
00692:             ribbon = item["object"]
00693:             phase = item["phase"]
00694:             base_rot = item["base_rot"]
00695:             base_loc = item["base_loc"]
00696:             base_scale = item["base_scale"]
00697: 
00698:             ribbon.location.z = base_loc.z + math.sin(i * 0.008 + phase) * 0.12 + low * 0.03
00699:             ribbon.scale = (
00700:                 base_scale.x * (1.0 + mid * 0.05),
00701:                 base_scale.y * (1.0 + high * 0.04),
00702:                 base_scale.z,
00703:             )
00704:             ribbon.rotation_euler.z = base_rot.z + i * 0.007 + phase * 0.25
00705: 
00706:             ribbon.keyframe_insert(data_path="location", frame=i)
00707:             ribbon.keyframe_insert(data_path="scale", frame=i)
00708:             ribbon.keyframe_insert(data_path="rotation_euler", frame=i)
00709: 
00710:             emit = 0.08 + (mid * 0.55 + pulse * 0.45) * 0.82
00711:             item["emit_socket"].default_value = emit
00712:             item["emit_socket"].keyframe_insert(data_path="default_value", frame=i)
00713: 
00714:         # PHYSICS ACCENTS
00715:         for idx, item in enumerate(accents):
00716:             obj = item["object"]
00717:             anchor = item["anchor"]
00718:             base_loc = item["base_location"]
00719:             base_rot = item.get("base_rotation", obj.rotation_euler)
00720:             phase = item["phase"] + idx * 0.23
00721:             response = item.get("response", 0.65)
00722:             local_pulse = max(0.0, math.sin(i * (0.024 + response * 0.016) + phase)) * 0.20
00723:             accent_drive = rhythm_band_drive(
00724:                 item.get("band", "mid"),
00725:                 response,
00726:                 low,
00727:                 mid,
00728:                 high,
00729:                 onset,
00730:                 beat,
00731:                 pulse,
00732:                 local_pulse,
00733:             )
00734: 
00735:             anchor.location.x = base_loc.x + math.sin(i * 0.012 + phase) * 0.18
00736:             anchor.location.y = base_loc.y + math.cos(i * 0.010 + phase) * 0.18
00737:             anchor.location.z = base_loc.z + math.sin(i * 0.013 + phase) * 0.10 + low * 0.08
00738:             anchor.keyframe_insert(data_path="location", frame=i)
00739: 
00740:             obj.rotation_euler.x = base_rot.x + math.sin(i * 0.017 + phase) * 0.10 * (0.35 + accent_drive)
00741:             obj.rotation_euler.y = base_rot.y + math.cos(i * 0.015 + phase) * 0.08 * (0.35 + accent_drive)
00742:             obj.rotation_euler.z = base_rot.z + i * (0.006 + accent_drive * 0.006) + math.sin(i * 0.011 + phase) * 0.04
00743:             obj.keyframe_insert(data_path="rotation_euler", frame=i)
00744: 
00745:             emission_socket = item.get("emission_socket")
00746:             if emission_socket is not None:
00747:                 emission_socket.default_value = PHYSICS_ACCENT_EMISSION_MIN + accent_drive * (
00748:                     PHYSICS_ACCENT_EMISSION_MAX - PHYSICS_ACCENT_EMISSION_MIN
00749:                 )
00750:                 keyframe_if_possible(emission_socket, "default_value", i)
00751: 
00752:             mix_socket = item.get("mix_socket")
00753:             if mix_socket is not None:
00754:                 mix_socket.default_value = PHYSICS_ACCENT_MIX_MIN + accent_drive * (
00755:                     PHYSICS_ACCENT_MIX_MAX - PHYSICS_ACCENT_MIX_MIN
00756:                 )
00757:                 keyframe_if_possible(mix_socket, "default_value", i)
00758: 
00759:         # FORCE FIELDS
00760:         if force_obj is not None:
00761:             strength = FIELD_STRENGTH_MIN + pulse * (FIELD_STRENGTH_MAX - FIELD_STRENGTH_MIN)
00762:             force_obj.field.strength = strength
00763:             force_obj.location.x = math.sin(i * 0.010) * 0.35
00764:             force_obj.location.y = math.cos(i * 0.008) * 0.30
00765:             force_obj.keyframe_insert(data_path='field.strength', frame=i)
00766:             force_obj.keyframe_insert(data_path='location', frame=i)
00767: 
00768:         if turb_obj is not None:
00769:             turb_strength = TURB_STRENGTH_MIN + high * (TURB_STRENGTH_MAX - TURB_STRENGTH_MIN) + pulse * 0.75
00770:             turb_obj.field.strength = turb_strength
00771:             turb_obj.location.z = hero_base_loc.z + 1.5 + math.sin(i * 0.012) * 0.10
00772:             turb_obj.keyframe_insert(data_path='field.strength', frame=i)
00773:             turb_obj.keyframe_insert(data_path='location', frame=i)
00774: 
00775:         if vortex_obj is not None:
00776:             vortex_strength = VORTEX_STRENGTH_MIN + mid * (VORTEX_STRENGTH_MAX - VORTEX_STRENGTH_MIN)
00777:             vortex_obj.field.strength = vortex_strength
00778:             vortex_obj.rotation_euler.z = i * 0.004
00779:             vortex_obj.keyframe_insert(data_path='field.strength', frame=i)
00780:             vortex_obj.keyframe_insert(data_path='rotation_euler', frame=i)
00781: 
00782:         if wind_left is not None:
00783:             wl = onset * 6.0 + beat * 2.0
00784:             wind_left.field.strength = wl
00785:             wind_left.keyframe_insert(data_path='field.strength', frame=i)
00786: 
00787:         if wind_right is not None:
00788:             wr = high * 4.0 + beat * 1.8
00789:             wind_right.field.strength = wr
00790:             wind_right.keyframe_insert(data_path='field.strength', frame=i)
00791: 
00792:         # RHYTHM PARTICLE PHYSICS
00793:         particle_keyframe = (
00794:             i == 1
00795:             or i == total_frames
00796:             or i % RHYTHM_PARTICLE_KEYFRAME_STEP == 0
00797:             or beat > 0.0
00798:             or onset > 0.72
00799:         )
00800: 
00801:         if particle_keyframe:
00802:             for item in rhythm_particles:
00803:                 emitter = item["emitter"]
00804:                 settings = item["settings"]
00805:                 settings_list = item.get("settings_list", [settings])
00806:                 mode = item["mode"]
00807:                 phase = item["phase"]
00808:                 base_loc = item["base_location"]
00809:                 base_rot = item["base_rotation"]
00810:                 base_scale = item["base_scale"]
00811: 
00812:                 if mode == "pulse":
00813:                     drive = min(1.0, beat * 0.90 + onset * 0.62 + low * 0.28)
00814:                     settings.normal_factor = RHYTHM_PARTICLE_NORMAL_MIN + drive * (
00815:                         RHYTHM_PARTICLE_NORMAL_MAX - RHYTHM_PARTICLE_NORMAL_MIN
00816:                     )
00817:                     settings.tangent_factor = RHYTHM_PARTICLE_TANGENT_MIN + (mid * 0.55 + drive * 0.45) * (
00818:                         RHYTHM_PARTICLE_TANGENT_MAX - RHYTHM_PARTICLE_TANGENT_MIN
00819:                     )
00820:                     settings.brownian_factor = RHYTHM_PARTICLE_BROWNIAN_MIN + (high * 0.45 + drive * 0.55) * (
00821:                         RHYTHM_PARTICLE_BROWNIAN_MAX - RHYTHM_PARTICLE_BROWNIAN_MIN
00822:                     )
00823:                     settings.particle_size = RHYTHM_PARTICLE_SIZE_MIN + drive * (
00824:                         RHYTHM_PARTICLE_SIZE_MAX - RHYTHM_PARTICLE_SIZE_MIN
00825:                     )
00826:                     item["emission_socket"].default_value = RHYTHM_PARTICLE_EMIT_MIN + drive * (
00827:                         RHYTHM_PARTICLE_EMIT_MAX - RHYTHM_PARTICLE_EMIT_MIN
00828:                     )
00829: 
00830:                     emitter.location.z = base_loc.z + low * 0.10 + transient * 0.06
00831:                     scale_boost = 1.0 + drive * 0.12
00832:                     emitter.rotation_euler.z = base_rot.z + i * 0.010 + math.sin(i * 0.019 + phase) * 0.08
00833: 
00834:                 elif mode == "dust":
00835:                     drive = min(1.0, mid * 0.46 + low * 0.26 + pulse * 0.18)
00836:                     settings.normal_factor = 0.025 + drive * 0.35
00837:                     settings.tangent_factor = 0.08 + drive * 0.42
00838:                     settings.brownian_factor = 0.28 + (high * 0.55 + drive * 0.45) * 0.78
00839:                     settings.particle_size = RHYTHM_PARTICLE_SIZE_MIN * (0.58 + drive * 0.55)
00840:                     item["emission_socket"].default_value = 0.10 + (high * 0.36 + drive * 0.38) * 0.90
00841: 
00842:                     emitter.location.x = base_loc.x + math.sin(i * 0.008 + phase) * 0.18
00843:                     emitter.location.y = base_loc.y + math.cos(i * 0.007 + phase) * 0.16
00844:                     emitter.location.z = base_loc.z + math.sin(i * 0.010 + phase) * 0.08 + low * 0.05
00845:                     scale_boost = 1.0 + drive * 0.04
00846:                     emitter.rotation_euler.z = base_rot.z + i * 0.003 + phase
00847: 
00848:                 elif mode == "streak":
00849:                     drive = min(1.0, high * 0.85 + onset * 0.45 + beat * 0.20)
00850:                     settings.normal_factor = 0.18 + drive * 1.72
00851:                     settings.tangent_factor = 0.35 + drive * 1.10
00852:                     settings.brownian_factor = 0.04 + drive * 0.38
00853:                     settings.particle_size = RHYTHM_PARTICLE_SIZE_MIN * (0.70 + drive * 0.95)
00854:                     item["emission_socket"].default_value = 0.12 + drive * 1.70
00855: 
00856:                     emitter.location.z = base_loc.z + high * 0.22 + transient * 0.05
00857:                     scale_boost = 1.0 + drive * 0.08
00858:                     emitter.rotation_euler.z = base_rot.z - i * 0.014 + phase
00859: 
00860:                 else:
00861:                     drive = min(1.0, mid * 0.42 + onset * 0.44 + beat * 0.36 + high * 0.20)
00862:                     settings.normal_factor = 0.08 + drive * 0.92
00863:                     settings.tangent_factor = 0.24 + drive * 0.88
00864:                     settings.brownian_factor = 0.06 + drive * 0.54
00865:                     settings.particle_size = ALBUM_LETTER_PARTICLE_SIZE_MIN + drive * (
00866:                         ALBUM_LETTER_PARTICLE_SIZE_MAX - ALBUM_LETTER_PARTICLE_SIZE_MIN
00867:                     )
00868: 
00869:                     emitter.location.x = base_loc.x + math.sin(i * 0.011 + phase) * 0.24
00870:                     emitter.location.y = base_loc.y + math.cos(i * 0.009 + phase) * 0.20
00871:                     emitter.location.z = base_loc.z + mid * 0.18 + beat * 0.10
00872:                     scale_boost = 1.0 + drive * 0.10
00873:                     emitter.rotation_euler.z = base_rot.z + i * 0.006 + phase
00874: 
00875:                     letter_root = item.get("letter_root")
00876:                     if letter_root is not None:
00877:                         letter_scale = ALBUM_LETTER_ROOT_SCALE_MIN + drive * (
00878:                             ALBUM_LETTER_ROOT_SCALE_MAX - ALBUM_LETTER_ROOT_SCALE_MIN
00879:                         )
00880:                         letter_root.scale = (letter_scale, letter_scale, letter_scale)
00881:                         letter_root.rotation_euler.z = math.sin(i * 0.018 + phase) * 0.12
00882:                         letter_root.keyframe_insert(data_path="scale", frame=i)
```
