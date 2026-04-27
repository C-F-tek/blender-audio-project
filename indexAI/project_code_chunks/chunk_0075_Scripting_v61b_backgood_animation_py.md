# Project Code Chunk 75/212

- File: `Scripting/v61b_backgood/animation.py`
- Part: `5`
- Lines: `883-1019`

## Symbol Map
- Imports: `math`, `from config import HERO_SCALE_MIN, HERO_SCALE_MAX, HERO_BOUNCE_Z, HERO_ROT_Z, HERO_ROT_X, HERO_ROT_Y, HERO_DRIFT_X, HERO_DRIFT_Y, HERO_ORBIT_X, HERO_ORBIT_Y, HERO_BEAT_TWIST_Z, HERO_ONSET_SHAKE, HERO_DEFORM_STRENGTH_MIN, HERO_DEFORM_STRENGTH_MAX, HERO_DEFORM_DETAIL_STRENGTH_MAX, HERO_DEFORM_WAVE_HEIGHT_MAX, HERO_DEFORM_TWIST_MAX, HERO_DEFORM_CONTROLLER_RADIUS, HERO_DEFORM_KEYFRAME_STEP, HERO_MATERIAL_EMISSION_MIN, HERO_MATERIAL_EMISSION_MAX, HERO_MATERIAL_SELF_LIGHT_MIN, HERO_MATERIAL_SELF_LIGHT_MAX, HERO_MATERIAL_BUMP_MIN, HERO_MATERIAL_BUMP_MAX, HERO_MATERIAL_ROUGHNESS_MIN, HERO_MATERIAL_ROUGHNESS_MAX, HERO_MATERIAL_NOISE_SCALE_MIN, HERO_MATERIAL_NOISE_SCALE_MAX, HERO_MATERIAL_MAPPING_DRIFT, AURA_DEFORM_KEYFRAME_STEP, AURA_DEFORM_FIELD_DRIFT, AURA_DEFORM_FIELD_SCALE, SECONDARY_SCALE_MIN, SECONDARY_SCALE_MAX, SECONDARY_BOUNCE_Z, SECONDARY_DRIFT_X, SECONDARY_DRIFT_Y, SECONDARY_ROT_Z, SECONDARY_ROT_X, CAMERA_BEAT_BUMP_Z, CAMERA_BEAT_BUMP_Y, CAMERA_ORBIT_AMOUNT, CAMERA_PUSH_AMOUNT, CAMERA_VERTICAL_SWAY, LIGHT_ENERGY_MIN, LIGHT_ENERGY_MAX, PHYSICS_ACCENT_EMISSION_MIN, PHYSICS_ACCENT_EMISSION_MAX, PHYSICS_ACCENT_MIX_MIN, PHYSICS_ACCENT_MIX_MAX, COMPOSITOR_GLARE_THRESHOLD_MIN, COMPOSITOR_GLARE_THRESHOLD_MAX, COMPOSITOR_LENS_DISTORT_MIN, COMPOSITOR_LENS_DISTORT_MAX, COMPOSITOR_LENS_DISPERSION_MIN, COMPOSITOR_LENS_DISPERSION_MAX, FIELD_STRENGTH_MIN, FIELD_STRENGTH_MAX, TURB_STRENGTH_MIN, TURB_STRENGTH_MAX, VORTEX_STRENGTH_MIN, VORTEX_STRENGTH_MAX, RHYTHM_PARTICLE_SIZE_MIN, RHYTHM_PARTICLE_SIZE_MAX, RHYTHM_PARTICLE_NORMAL_MIN, RHYTHM_PARTICLE_NORMAL_MAX, RHYTHM_PARTICLE_TANGENT_MIN, RHYTHM_PARTICLE_TANGENT_MAX, RHYTHM_PARTICLE_BROWNIAN_MIN, RHYTHM_PARTICLE_BROWNIAN_MAX, RHYTHM_PARTICLE_EMIT_MIN, RHYTHM_PARTICLE_EMIT_MAX, RHYTHM_PARTICLE_KEYFRAME_STEP, ALBUM_LETTER_PARTICLE_SIZE_MIN, ALBUM_LETTER_PARTICLE_SIZE_MAX, ALBUM_LETTER_ROOT_SCALE_MIN, ALBUM_LETTER_ROOT_SCALE_MAX, BACKDROP_EMISSION_MIN, BACKDROP_EMISSION_MAX, BACKDROP_BREATHE_SCALE, MIST_FLOAT_AMPLITUDE, MIST_BEAT_BOOST`, `from fog_dynamics import animate_fog_frame`, `from scene_utils import set_linear_interpolation_idblock`
- Functions: `keyframe_if_possible(idblock, data_path, frame)` line 92; `get_scene_compositor_tree(scene)` line 99; `rhythm_band_drive(band, response, low, mid, high, onset, beat, pulse, local_pulse)` line 107; `animate_scene(scene, frames, camera, target, hero_asset, secondary_asset, aura_data, fog_controller, scene_base, lights, physics_data, mist_particles, variants, energy_rings, energy_ribbons)` line 125

## Content
```py
00883:                         letter_root.keyframe_insert(data_path="rotation_euler", frame=i)
00884: 
00885:                     for letter in item.get("letter_sources", []):
00886:                         obj = letter["object"]
00887:                         lphase = letter["phase"]
00888:                         lscale = 1.0 + drive * 0.20 + math.sin(i * 0.030 + lphase) * 0.035
00889:                         obj.scale = (
00890:                             letter["base_scale"].x * lscale,
00891:                             letter["base_scale"].y * (1.0 + high * 0.14),
00892:                             letter["base_scale"].z * (1.0 + beat * 0.18),
00893:                         )
00894:                         obj.keyframe_insert(data_path="scale", frame=i)
00895: 
00896:                 emitter.scale = (
00897:                     base_scale.x * scale_boost,
00898:                     base_scale.y * scale_boost,
00899:                     base_scale.z * scale_boost,
00900:                 )
00901: 
00902:                 for extra_settings in settings_list[1:]:
00903:                     extra_settings.normal_factor = settings.normal_factor
00904:                     extra_settings.tangent_factor = settings.tangent_factor
00905:                     extra_settings.brownian_factor = settings.brownian_factor
00906:                     extra_settings.particle_size = settings.particle_size
00907: 
00908:                 for particle_settings in settings_list:
00909:                     keyframe_if_possible(particle_settings, "normal_factor", i)
00910:                     keyframe_if_possible(particle_settings, "tangent_factor", i)
00911:                     keyframe_if_possible(particle_settings, "brownian_factor", i)
00912:                     keyframe_if_possible(particle_settings, "particle_size", i)
00913:                 if item.get("emission_socket") is not None:
00914:                     keyframe_if_possible(item["emission_socket"], "default_value", i)
00915:                 emitter.keyframe_insert(data_path="location", frame=i)
00916:                 emitter.keyframe_insert(data_path="rotation_euler", frame=i)
00917:                 emitter.keyframe_insert(data_path="scale", frame=i)
00918: 
00919:         # CAMERA
00920:         camera.location.x = cam_base_loc.x + math.sin(i * 0.020) * CAMERA_ORBIT_AMOUNT
00921:         camera.location.y = cam_base_loc.y + low * CAMERA_PUSH_AMOUNT - beat * CAMERA_BEAT_BUMP_Y
00922:         camera.location.z = cam_base_loc.z + beat * CAMERA_BEAT_BUMP_Z + math.sin(i * 0.018) * CAMERA_VERTICAL_SWAY + high * 0.08
00923:         camera.keyframe_insert(data_path="location", frame=i)
00924: 
00925:         target.location.x = target_base_loc.x + (mid - 0.5) * 0.40
00926:         target.location.y = target_base_loc.y
00927:         target.location.z = target_base_loc.z + low * 0.25 + high * 0.08
00928:         target.keyframe_insert(data_path="location", frame=i)
00929: 
00930:     set_linear_interpolation_idblock(hero_root)
00931:     if hero_deform_controller is not None:
00932:         set_linear_interpolation_idblock(hero_deform_controller)
00933:     for item in hero_deformers:
00934:         set_linear_interpolation_idblock(item.get("mesh"))
00935:     for control in hero_material_controls:
00936:         set_linear_interpolation_idblock(control.get("node_tree"))
00937:     compositor_tree = get_scene_compositor_tree(scene)
00938:     if compositor_tree is not None:
00939:         set_linear_interpolation_idblock(compositor_tree)
00940:     if aura_audio_controller is not None:
00941:         set_linear_interpolation_idblock(aura_audio_controller)
00942:     if aura_deform_field is not None:
00943:         set_linear_interpolation_idblock(aura_deform_field)
00944:     if secondary_root is not None:
00945:         set_linear_interpolation_idblock(secondary_root)
00946:     set_linear_interpolation_idblock(aura_obj)
00947:     set_linear_interpolation_idblock(camera)
00948:     set_linear_interpolation_idblock(target)
00949: 
00950:     if lights:
00951:         for light in lights:
00952:             try:
00953:                 set_linear_interpolation_idblock(light.data)
00954:             except Exception:
00955:                 pass
00956: 
00957:     for item in mist_particles:
00958:         set_linear_interpolation_idblock(item["object"])
00959:         if item["material"]:
00960:             set_linear_interpolation_idblock(item["material"].node_tree)
00961: 
00962:     for item in variants:
00963:         set_linear_interpolation_idblock(item["root"])
00964: 
00965:     for item in accents:
00966:         set_linear_interpolation_idblock(item["anchor"])
00967: 
00968:     for item in rhythm_particles:
00969:         set_linear_interpolation_idblock(item.get("emitter"))
00970:         set_linear_interpolation_idblock(item.get("settings"))
00971:         for settings in item.get("settings_list", []):
00972:             set_linear_interpolation_idblock(settings)
00973:         set_linear_interpolation_idblock(item.get("letter_root"))
00974:         for letter in item.get("letter_sources", []):
00975:             set_linear_interpolation_idblock(letter.get("object"))
00976:         if item.get("material"):
00977:             set_linear_interpolation_idblock(item["material"].node_tree)
00978: 
00979:     for item in energy_rings:
00980:         set_linear_interpolation_idblock(item["object"])
00981:         if item["object"].active_material:
00982:             set_linear_interpolation_idblock(item["object"].active_material.node_tree)
00983: 
00984:     for item in energy_ribbons:
00985:         set_linear_interpolation_idblock(item["object"])
00986:         if item["object"].active_material:
00987:             set_linear_interpolation_idblock(item["object"].active_material.node_tree)
00988: 
00989:     aura_material = getattr(aura_obj, "active_material", None)
00990:     if aura_material:
00991:         set_linear_interpolation_idblock(aura_material.node_tree)
00992: 
00993:     floor = scene.objects.get("PeaceFloor")
00994:     if floor and floor.active_material:
00995:         set_linear_interpolation_idblock(floor.active_material.node_tree)
00996: 
00997:     if fog_controller and fog_controller["object"] and fog_controller["object"].active_material:
00998:         set_linear_interpolation_idblock(fog_controller["object"])
00999:         set_linear_interpolation_idblock(fog_controller["object"].active_material.node_tree)
01000:     if fog_control is not None:
01001:         set_linear_interpolation_idblock(fog_control)
01002: 
01003:     if backdrop is not None:
01004:         set_linear_interpolation_idblock(backdrop)
01005:         if backdrop.active_material:
01006:             set_linear_interpolation_idblock(backdrop.active_material.node_tree)
01007:     if backdrop_control is not None:
01008:         set_linear_interpolation_idblock(backdrop_control)
01009: 
01010:     if force_obj is not None:
01011:         set_linear_interpolation_idblock(force_obj)
01012:     if turb_obj is not None:
01013:         set_linear_interpolation_idblock(turb_obj)
01014:     if vortex_obj is not None:
01015:         set_linear_interpolation_idblock(vortex_obj)
01016:     if wind_left is not None:
01017:         set_linear_interpolation_idblock(wind_left)
01018:     if wind_right is not None:
01019:         set_linear_interpolation_idblock(wind_right)
```
