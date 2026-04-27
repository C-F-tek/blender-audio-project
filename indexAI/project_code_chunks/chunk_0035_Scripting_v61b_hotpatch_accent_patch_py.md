# Project Code Chunk 35/212

- File: `Scripting/v61b/hotpatch/accent_patch.py`
- Part: `2`
- Lines: `245-301`

## Symbol Map
- Imports: `math`, `bpy`, `from materials import build_variant_material`, `from common import PALETTE_LIST, cfg_value, clear_animation, get_node, iter_objects_prefix, keyframe_if_possible, socket_by_name, store_base_vector`
- Functions: `drive_for_band(band, response, sample, frame, phase)` line 40; `ensure_accent_material(obj, index)` line 63; `get_or_store_float(obj, key, default)` line 84; `atom_center()` line 90; `find_or_create_force_object(name, effector_type, location)` line 100; `update_central_fields(frames, center)` line 121; `update_physics_accents(frames)` line 175
- Assignments: `PHYSICS_ACCENT_EMISSION_MIN`, `PHYSICS_ACCENT_EMISSION_MAX`, `PHYSICS_ACCENT_MIX_MIN`, `PHYSICS_ACCENT_MIX_MAX`, `PRIMARY_BASE_Z`, `PHYSICS_ORBIT_RADIUS_MIN`, `PHYSICS_ORBIT_RADIUS_MAX`, `PHYSICS_ATOM_ORBIT_SPEED_MIN`, `PHYSICS_ATOM_ORBIT_SPEED_MAX`, `PHYSICS_ATOM_ORBIT_AUDIO_SPEED`, `PHYSICS_ATOM_ORBIT_RADIUS_PULSE`, `PHYSICS_ATOM_ORBIT_HEIGHT_SWAY`, `PHYSICS_ATOM_MICRO_WOBBLE`, `HERO_GRAVITY_STRENGTH_MIN`, `HERO_GRAVITY_STRENGTH_MAX`, `TURB_STRENGTH_MIN`, `TURB_STRENGTH_MAX`, `VORTEX_STRENGTH_MIN`, `VORTEX_STRENGTH_MAX`

## Content
```py
00245:             drive = drive_for_band(item["band"], response, sample, frame, phase)
00246:             low = float(sample.get("low", 0.0))
00247:             high = float(sample.get("high", 0.0))
00248:             beat = float(sample.get("beat", 0.0))
00249: 
00250:             speed = item["orbit_speed"] + drive * PHYSICS_ATOM_ORBIT_AUDIO_SPEED + beat * 0.004
00251:             angle = item["orbit_angle"] + frame * speed + math.sin(frame * 0.012 + phase) * 0.055
00252:             radius = item["orbit_radius"] * (
00253:                 1.0
00254:                 + drive * PHYSICS_ATOM_ORBIT_RADIUS_PULSE
00255:                 + low * 0.035
00256:                 - high * 0.012
00257:             )
00258:             y_radius = radius * (0.82 + math.cos(item["orbit_tilt"]) * 0.10)
00259: 
00260:             anchor_x = center.x + math.cos(angle) * radius
00261:             anchor_y = center.y + math.sin(angle) * y_radius
00262:             anchor_z = (
00263:                 center.z
00264:                 + item["orbit_z_offset"]
00265:                 + math.sin(angle * 1.31 + item["orbit_tilt"]) * PHYSICS_ATOM_ORBIT_HEIGHT_SWAY * (0.35 + drive)
00266:                 + low * 0.10
00267:                 + beat * 0.045
00268:             )
00269: 
00270:             if anchor is not None:
00271:                 anchor.location.x = anchor_x
00272:                 anchor.location.y = anchor_y
00273:                 anchor.location.z = anchor_z
00274:                 anchor.keyframe_insert(data_path="location", frame=frame)
00275: 
00276:             micro_angle = angle * 2.70 + frame * (0.010 + drive * 0.010) + phase
00277:             micro_drive = item["micro_radius"] * (0.55 + drive * 0.85)
00278:             obj.location.x = anchor_x + math.cos(micro_angle) * micro_drive
00279:             obj.location.y = anchor_y + math.sin(micro_angle) * micro_drive * 0.72
00280:             obj.location.z = anchor_z + math.sin(micro_angle * 1.17) * micro_drive * 0.54
00281:             obj.keyframe_insert(data_path="location", frame=frame)
00282: 
00283:             rot = item["base_rotation"]
00284:             obj.rotation_euler.x = rot[0] + math.sin(frame * 0.017 + phase) * 0.10 * (0.35 + drive)
00285:             obj.rotation_euler.y = rot[1] + math.cos(frame * 0.015 + phase) * 0.08 * (0.35 + drive)
00286:             obj.rotation_euler.z = rot[2] + angle + frame * (0.006 + drive * 0.006) + math.sin(frame * 0.011 + phase) * 0.04
00287:             obj.keyframe_insert(data_path="rotation_euler", frame=frame)
00288: 
00289:             if item["emission_socket"] is not None:
00290:                 item["emission_socket"].default_value = PHYSICS_ACCENT_EMISSION_MIN + drive * (
00291:                     PHYSICS_ACCENT_EMISSION_MAX - PHYSICS_ACCENT_EMISSION_MIN
00292:                 )
00293:                 keyframe_if_possible(item["emission_socket"], "default_value", frame)
00294: 
00295:             if item["mix_socket"] is not None:
00296:                 item["mix_socket"].default_value = PHYSICS_ACCENT_MIX_MIN + drive * (
00297:                     PHYSICS_ACCENT_MIX_MAX - PHYSICS_ACCENT_MIX_MIN
00298:                 )
00299:                 keyframe_if_possible(item["mix_socket"], "default_value", frame)
00300: 
00301:     return len(controls)
```
