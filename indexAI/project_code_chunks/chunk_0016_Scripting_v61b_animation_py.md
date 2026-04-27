# Project Code Chunk 16/212

- File: `Scripting/v61b/animation.py`
- Part: `5`
- Lines: `894-1079`

## Symbol Map
- Imports: `math`, `from config import HERO_SCALE_MIN, HERO_SCALE_MAX, HERO_BOUNCE_Z, HERO_ROT_Z, HERO_ROT_X, HERO_ROT_Y, HERO_DRIFT_X, HERO_DRIFT_Y, HERO_ORBIT_X, HERO_ORBIT_Y, HERO_BEAT_TWIST_Z, HERO_ONSET_SHAKE, HERO_DEFORM_STRENGTH_MIN, HERO_DEFORM_STRENGTH_MAX, HERO_DEFORM_DETAIL_STRENGTH_MAX, HERO_DEFORM_WAVE_HEIGHT_MAX, HERO_DEFORM_TWIST_MAX, HERO_DEFORM_CONTROLLER_RADIUS, HERO_DEFORM_KEYFRAME_STEP, HERO_MATERIAL_EMISSION_MIN, HERO_MATERIAL_EMISSION_MAX, HERO_MATERIAL_SELF_LIGHT_MIN, HERO_MATERIAL_SELF_LIGHT_MAX, HERO_MATERIAL_BUMP_MIN, HERO_MATERIAL_BUMP_MAX, HERO_MATERIAL_ROUGHNESS_MIN, HERO_MATERIAL_ROUGHNESS_MAX, HERO_MATERIAL_NOISE_SCALE_MIN, HERO_MATERIAL_NOISE_SCALE_MAX, HERO_MATERIAL_MAPPING_DRIFT, AURA_DEFORM_KEYFRAME_STEP, AURA_DEFORM_FIELD_DRIFT, AURA_DEFORM_FIELD_SCALE, SECONDARY_SCALE_MIN, SECONDARY_SCALE_MAX, SECONDARY_BOUNCE_Z, SECONDARY_DRIFT_X, SECONDARY_DRIFT_Y, SECONDARY_ROT_Z, SECONDARY_ROT_X, CAMERA_BEAT_BUMP_Z, CAMERA_BEAT_BUMP_Y, CAMERA_ORBIT_AMOUNT, CAMERA_PUSH_AMOUNT, CAMERA_VERTICAL_SWAY, LIGHT_ENERGY_MIN, LIGHT_ENERGY_MAX, PHYSICS_ACCENT_EMISSION_MIN, PHYSICS_ACCENT_EMISSION_MAX, PHYSICS_ACCENT_MIX_MIN, PHYSICS_ACCENT_MIX_MAX, PHYSICS_ATOM_ORBIT_SPEED_MIN, PHYSICS_ATOM_ORBIT_AUDIO_SPEED, PHYSICS_ATOM_ORBIT_RADIUS_PULSE, PHYSICS_ATOM_ORBIT_HEIGHT_SWAY, PHYSICS_ATOM_MICRO_WOBBLE, COMPOSITOR_GLARE_THRESHOLD_MIN, COMPOSITOR_GLARE_THRESHOLD_MAX, COMPOSITOR_LENS_DISTORT_MIN, COMPOSITOR_LENS_DISTORT_MAX, COMPOSITOR_LENS_DISPERSION_MIN, COMPOSITOR_LENS_DISPERSION_MAX, FIELD_STRENGTH_MIN, FIELD_STRENGTH_MAX, HERO_GRAVITY_STRENGTH_MIN, HERO_GRAVITY_STRENGTH_MAX, TURB_STRENGTH_MIN, TURB_STRENGTH_MAX, VORTEX_STRENGTH_MIN, VORTEX_STRENGTH_MAX, RHYTHM_PARTICLE_SIZE_MIN, RHYTHM_PARTICLE_SIZE_MAX, RHYTHM_PARTICLE_NORMAL_MIN, RHYTHM_PARTICLE_NORMAL_MAX, RHYTHM_PARTICLE_TANGENT_MIN, RHYTHM_PARTICLE_TANGENT_MAX, RHYTHM_PARTICLE_BROWNIAN_MIN, RHYTHM_PARTICLE_BROWNIAN_MAX, RHYTHM_PARTICLE_EMIT_MIN, RHYTHM_PARTICLE_EMIT_MAX, RHYTHM_PARTICLE_KEYFRAME_STEP, ALBUM_LETTER_PARTICLE_SIZE_MIN, ALBUM_LETTER_PARTICLE_SIZE_MAX, ALBUM_LETTER_ROOT_SCALE_MIN, ALBUM_LETTER_ROOT_SCALE_MAX, BACKDROP_EMISSION_MIN, BACKDROP_EMISSION_MAX, BACKDROP_BREATHE_SCALE, MIST_FLOAT_AMPLITUDE, MIST_BEAT_BOOST`, `from fog_dynamics import animate_fog_frame`, `from scene_utils import set_linear_interpolation_idblock`
- Functions: `keyframe_if_possible(idblock, data_path, frame)` line 99; `get_scene_compositor_tree(scene)` line 106; `rhythm_band_drive(band, response, low, mid, high, onset, beat, pulse, local_pulse)` line 114; `animate_scene(scene, frames, camera, target, hero_asset, secondary_asset, aura_data, fog_controller, scene_base, lights, physics_data, mist_particles, variants, energy_rings, energy_ribbons)` line 132

## Content
```py
00894:                     settings.tangent_factor = 0.08 + drive * 0.42
00895:                     settings.brownian_factor = 0.28 + (high * 0.55 + drive * 0.45) * 0.78
00896:                     settings.particle_size = RHYTHM_PARTICLE_SIZE_MIN * (0.58 + drive * 0.55)
00897:                     item["emission_socket"].default_value = 0.10 + (high * 0.36 + drive * 0.38) * 0.90
00898: 
00899:                     emitter.location.x = base_loc.x + math.sin(i * 0.008 + phase) * 0.18
00900:                     emitter.location.y = base_loc.y + math.cos(i * 0.007 + phase) * 0.16
00901:                     emitter.location.z = base_loc.z + math.sin(i * 0.010 + phase) * 0.08 + low * 0.05
00902:                     scale_boost = 1.0 + drive * 0.04
00903:                     emitter.rotation_euler.z = base_rot.z + i * 0.003 + phase
00904: 
00905:                 elif mode == "streak":
00906:                     drive = min(1.0, high * 0.85 + onset * 0.45 + beat * 0.20)
00907:                     settings.normal_factor = 0.18 + drive * 1.72
00908:                     settings.tangent_factor = 0.35 + drive * 1.10
00909:                     settings.brownian_factor = 0.04 + drive * 0.38
00910:                     settings.particle_size = RHYTHM_PARTICLE_SIZE_MIN * (0.70 + drive * 0.95)
00911:                     item["emission_socket"].default_value = 0.12 + drive * 1.70
00912: 
00913:                     emitter.location.z = base_loc.z + high * 0.22 + transient * 0.05
00914:                     scale_boost = 1.0 + drive * 0.08
00915:                     emitter.rotation_euler.z = base_rot.z - i * 0.014 + phase
00916: 
00917:                 else:
00918:                     drive = min(1.0, mid * 0.42 + onset * 0.44 + beat * 0.36 + high * 0.20)
00919:                     settings.normal_factor = 0.08 + drive * 0.92
00920:                     settings.tangent_factor = 0.24 + drive * 0.88
00921:                     settings.brownian_factor = 0.06 + drive * 0.54
00922:                     settings.particle_size = ALBUM_LETTER_PARTICLE_SIZE_MIN + drive * (
00923:                         ALBUM_LETTER_PARTICLE_SIZE_MAX - ALBUM_LETTER_PARTICLE_SIZE_MIN
00924:                     )
00925: 
00926:                     emitter.location.x = base_loc.x + math.sin(i * 0.011 + phase) * 0.24
00927:                     emitter.location.y = base_loc.y + math.cos(i * 0.009 + phase) * 0.20
00928:                     emitter.location.z = base_loc.z + mid * 0.18 + beat * 0.10
00929:                     scale_boost = 1.0 + drive * 0.10
00930:                     emitter.rotation_euler.z = base_rot.z + i * 0.006 + phase
00931: 
00932:                     letter_root = item.get("letter_root")
00933:                     if letter_root is not None:
00934:                         letter_scale = ALBUM_LETTER_ROOT_SCALE_MIN + drive * (
00935:                             ALBUM_LETTER_ROOT_SCALE_MAX - ALBUM_LETTER_ROOT_SCALE_MIN
00936:                         )
00937:                         letter_root.scale = (letter_scale, letter_scale, letter_scale)
00938:                         letter_root.rotation_euler.z = math.sin(i * 0.018 + phase) * 0.12
00939:                         letter_root.keyframe_insert(data_path="scale", frame=i)
00940:                         letter_root.keyframe_insert(data_path="rotation_euler", frame=i)
00941: 
00942:                     for letter in item.get("letter_sources", []):
00943:                         obj = letter["object"]
00944:                         lphase = letter["phase"]
00945:                         lscale = 1.0 + drive * 0.20 + math.sin(i * 0.030 + lphase) * 0.035
00946:                         obj.scale = (
00947:                             letter["base_scale"].x * lscale,
00948:                             letter["base_scale"].y * (1.0 + high * 0.14),
00949:                             letter["base_scale"].z * (1.0 + beat * 0.18),
00950:                         )
00951:                         obj.keyframe_insert(data_path="scale", frame=i)
00952: 
00953:                 emitter.scale = (
00954:                     base_scale.x * scale_boost,
00955:                     base_scale.y * scale_boost,
00956:                     base_scale.z * scale_boost,
00957:                 )
00958: 
00959:                 for extra_settings in settings_list[1:]:
00960:                     extra_settings.normal_factor = settings.normal_factor
00961:                     extra_settings.tangent_factor = settings.tangent_factor
00962:                     extra_settings.brownian_factor = settings.brownian_factor
00963:                     extra_settings.particle_size = settings.particle_size
00964: 
00965:                 for particle_settings in settings_list:
00966:                     keyframe_if_possible(particle_settings, "normal_factor", i)
00967:                     keyframe_if_possible(particle_settings, "tangent_factor", i)
00968:                     keyframe_if_possible(particle_settings, "brownian_factor", i)
00969:                     keyframe_if_possible(particle_settings, "particle_size", i)
00970:                 if item.get("emission_socket") is not None:
00971:                     keyframe_if_possible(item["emission_socket"], "default_value", i)
00972:                 emitter.keyframe_insert(data_path="location", frame=i)
00973:                 emitter.keyframe_insert(data_path="rotation_euler", frame=i)
00974:                 emitter.keyframe_insert(data_path="scale", frame=i)
00975: 
00976:         # CAMERA
00977:         camera.location.x = cam_base_loc.x + math.sin(i * 0.020) * CAMERA_ORBIT_AMOUNT
00978:         camera.location.y = cam_base_loc.y + low * CAMERA_PUSH_AMOUNT - beat * CAMERA_BEAT_BUMP_Y
00979:         camera.location.z = cam_base_loc.z + beat * CAMERA_BEAT_BUMP_Z + math.sin(i * 0.018) * CAMERA_VERTICAL_SWAY + high * 0.08
00980:         camera.keyframe_insert(data_path="location", frame=i)
00981: 
00982:         target.location.x = target_base_loc.x + (mid - 0.5) * 0.40
00983:         target.location.y = target_base_loc.y
00984:         target.location.z = target_base_loc.z + low * 0.25 + high * 0.08
00985:         target.keyframe_insert(data_path="location", frame=i)
00986: 
00987:     set_linear_interpolation_idblock(hero_root)
00988:     if hero_deform_controller is not None:
00989:         set_linear_interpolation_idblock(hero_deform_controller)
00990:     for item in hero_deformers:
00991:         set_linear_interpolation_idblock(item.get("mesh"))
00992:     for control in hero_material_controls:
00993:         set_linear_interpolation_idblock(control.get("node_tree"))
00994:     compositor_tree = get_scene_compositor_tree(scene)
00995:     if compositor_tree is not None:
00996:         set_linear_interpolation_idblock(compositor_tree)
00997:     if aura_audio_controller is not None:
00998:         set_linear_interpolation_idblock(aura_audio_controller)
00999:     if aura_deform_field is not None:
01000:         set_linear_interpolation_idblock(aura_deform_field)
01001:     if secondary_root is not None:
01002:         set_linear_interpolation_idblock(secondary_root)
01003:     set_linear_interpolation_idblock(aura_obj)
01004:     set_linear_interpolation_idblock(camera)
01005:     set_linear_interpolation_idblock(target)
01006: 
01007:     if lights:
01008:         for light in lights:
01009:             try:
01010:                 set_linear_interpolation_idblock(light.data)
01011:             except Exception:
01012:                 pass
01013: 
01014:     for item in mist_particles:
01015:         set_linear_interpolation_idblock(item["object"])
01016:         if item["material"]:
01017:             set_linear_interpolation_idblock(item["material"].node_tree)
01018: 
01019:     for item in variants:
01020:         set_linear_interpolation_idblock(item["root"])
01021: 
01022:     for item in accents:
01023:         set_linear_interpolation_idblock(item["anchor"])
01024:         set_linear_interpolation_idblock(item["object"])
01025:         if item.get("material"):
01026:             set_linear_interpolation_idblock(item["material"].node_tree)
01027: 
01028:     for item in rhythm_particles:
01029:         set_linear_interpolation_idblock(item.get("emitter"))
01030:         set_linear_interpolation_idblock(item.get("settings"))
01031:         for settings in item.get("settings_list", []):
01032:             set_linear_interpolation_idblock(settings)
01033:         set_linear_interpolation_idblock(item.get("letter_root"))
01034:         for letter in item.get("letter_sources", []):
01035:             set_linear_interpolation_idblock(letter.get("object"))
01036:         if item.get("material"):
01037:             set_linear_interpolation_idblock(item["material"].node_tree)
01038: 
01039:     for item in energy_rings:
01040:         set_linear_interpolation_idblock(item["object"])
01041:         if item["object"].active_material:
01042:             set_linear_interpolation_idblock(item["object"].active_material.node_tree)
01043: 
01044:     for item in energy_ribbons:
01045:         set_linear_interpolation_idblock(item["object"])
01046:         if item["object"].active_material:
01047:             set_linear_interpolation_idblock(item["object"].active_material.node_tree)
01048: 
01049:     aura_material = getattr(aura_obj, "active_material", None)
01050:     if aura_material:
01051:         set_linear_interpolation_idblock(aura_material.node_tree)
01052: 
01053:     floor = scene.objects.get("PeaceFloor")
01054:     if floor and floor.active_material:
01055:         set_linear_interpolation_idblock(floor.active_material.node_tree)
01056: 
01057:     if fog_controller and fog_controller["object"] and fog_controller["object"].active_material:
01058:         set_linear_interpolation_idblock(fog_controller["object"])
01059:         set_linear_interpolation_idblock(fog_controller["object"].active_material.node_tree)
01060:     if fog_control is not None:
01061:         set_linear_interpolation_idblock(fog_control)
01062: 
01063:     if backdrop is not None:
01064:         set_linear_interpolation_idblock(backdrop)
01065:         if backdrop.active_material:
01066:             set_linear_interpolation_idblock(backdrop.active_material.node_tree)
01067:     if backdrop_control is not None:
01068:         set_linear_interpolation_idblock(backdrop_control)
01069: 
01070:     if force_obj is not None:
01071:         set_linear_interpolation_idblock(force_obj)
01072:     if turb_obj is not None:
01073:         set_linear_interpolation_idblock(turb_obj)
01074:     if vortex_obj is not None:
01075:         set_linear_interpolation_idblock(vortex_obj)
01076:     if wind_left is not None:
01077:         set_linear_interpolation_idblock(wind_left)
01078:     if wind_right is not None:
01079:         set_linear_interpolation_idblock(wind_right)
```
