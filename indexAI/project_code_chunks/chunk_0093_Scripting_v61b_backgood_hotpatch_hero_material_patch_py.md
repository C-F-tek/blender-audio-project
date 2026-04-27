# Project Code Chunk 93/212

- File: `Scripting/v61b_backgood/hotpatch/hero_material_patch.py`
- Part: `2`
- Lines: `292-395`

## Symbol Map
- Imports: `math`, `bpy`, `from common import cfg_value, clear_animation, keyframe_if_possible`
- Functions: `find_principled_node(material)` line 28; `get_node_input(node)` line 37; `link_node_sockets(links, output_socket, input_socket, replace_existing)` line 46; `get_or_create_node(nodes, node_type, name, location)` line 61; `get_or_create_value(nodes, name, label, location, default)` line 70; `find_material_output(material)` line 81; `ensure_surface_light_layer(material, principled)` line 93; `hero_meshes()` line 172; `lift_principled_material(principled)` line 183; `ensure_hero_controls(material)` line 211; `collect_hero_controls()` line 300; `patch_hero_materials(frames)` line 317
- Assignments: `HERO_MATERIAL_EMISSION_MIN`, `HERO_MATERIAL_EMISSION_MAX`, `HERO_MATERIAL_SELF_LIGHT_MIN`, `HERO_MATERIAL_SELF_LIGHT_MAX`, `HERO_MATERIAL_BUMP_MIN`, `HERO_MATERIAL_BUMP_MAX`, `HERO_MATERIAL_ROUGHNESS_MIN`, `HERO_MATERIAL_ROUGHNESS_MAX`, `HERO_MATERIAL_NOISE_SCALE_MIN`, `HERO_MATERIAL_NOISE_SCALE_MAX`, `HERO_MATERIAL_MAPPING_DRIFT`, `PEACE_PALETTE`

## Content
```py
00292:         "roughness_socket": roughness_value.outputs[0],
00293:         "bump_socket": bump_value.outputs[0],
00294:         "noise_scale_socket": noise.inputs["Scale"],
00295:         "mapping_location_socket": mapping.inputs["Location"],
00296:         "mapping_rotation_socket": mapping.inputs["Rotation"],
00297:     }
00298: 
00299: 
00300: def collect_hero_controls():
00301:     controls = []
00302:     seen = set()
00303: 
00304:     for obj in hero_meshes():
00305:         for slot in obj.material_slots:
00306:             mat = slot.material
00307:             if mat is None or mat.name in seen:
00308:                 continue
00309:             seen.add(mat.name)
00310:             control = ensure_hero_controls(mat)
00311:             if control is not None:
00312:                 controls.append(control)
00313: 
00314:     return controls
00315: 
00316: 
00317: def patch_hero_materials(frames):
00318:     controls = collect_hero_controls()
00319:     for control in controls:
00320:         clear_animation(control.get("node_tree"))
00321: 
00322:     if not controls:
00323:         return 0
00324: 
00325:     if not frames:
00326:         frames = [{"low": 0.25, "mid": 0.25, "high": 0.25, "onset": 0.0, "beat": 0.0}]
00327: 
00328:     for frame, sample in enumerate(frames, start=1):
00329:         high = float(sample.get("high", 0.0))
00330:         mid = float(sample.get("mid", 0.0))
00331:         low = float(sample.get("low", 0.0))
00332:         onset = float(sample.get("onset", 0.0))
00333:         beat = float(sample.get("beat", 0.0))
00334:         pulse = max(onset, beat)
00335:         material_drive = min(1.0, 0.18 + high * 0.48 + mid * 0.20 + pulse * 0.34)
00336:         surface_drive = min(1.0, low * 0.24 + mid * 0.28 + high * 0.34 + onset * 0.26)
00337: 
00338:         for idx, control in enumerate(controls):
00339:             phase = idx * 0.47
00340:             shimmer = max(0.0, math.sin(frame * 0.017 + phase)) * 0.08
00341: 
00342:             emission_socket = control.get("emission_socket")
00343:             if emission_socket is not None:
00344:                 emission_socket.default_value = HERO_MATERIAL_EMISSION_MIN + min(1.0, material_drive + shimmer) * (
00345:                     HERO_MATERIAL_EMISSION_MAX - HERO_MATERIAL_EMISSION_MIN
00346:                 )
00347:                 keyframe_if_possible(emission_socket, "default_value", frame)
00348: 
00349:             self_light_socket = control.get("self_light_socket")
00350:             if self_light_socket is not None:
00351:                 edge_drive = min(1.0, material_drive * 0.74 + surface_drive * 0.18 + pulse * 0.16 + shimmer)
00352:                 self_light_socket.default_value = HERO_MATERIAL_SELF_LIGHT_MIN + edge_drive * (
00353:                     HERO_MATERIAL_SELF_LIGHT_MAX - HERO_MATERIAL_SELF_LIGHT_MIN
00354:                 )
00355:                 keyframe_if_possible(self_light_socket, "default_value", frame)
00356: 
00357:             roughness_socket = control.get("roughness_socket")
00358:             if roughness_socket is not None:
00359:                 roughness_socket.default_value = HERO_MATERIAL_ROUGHNESS_MAX - material_drive * (
00360:                     HERO_MATERIAL_ROUGHNESS_MAX - HERO_MATERIAL_ROUGHNESS_MIN
00361:                 )
00362:                 keyframe_if_possible(roughness_socket, "default_value", frame)
00363: 
00364:             bump_socket = control.get("bump_socket")
00365:             if bump_socket is not None:
00366:                 bump_socket.default_value = HERO_MATERIAL_BUMP_MIN + surface_drive * (
00367:                     HERO_MATERIAL_BUMP_MAX - HERO_MATERIAL_BUMP_MIN
00368:                 )
00369:                 keyframe_if_possible(bump_socket, "default_value", frame)
00370: 
00371:             noise_scale_socket = control.get("noise_scale_socket")
00372:             if noise_scale_socket is not None:
00373:                 noise_scale_socket.default_value = HERO_MATERIAL_NOISE_SCALE_MIN + surface_drive * (
00374:                     HERO_MATERIAL_NOISE_SCALE_MAX - HERO_MATERIAL_NOISE_SCALE_MIN
00375:                 )
00376:                 keyframe_if_possible(noise_scale_socket, "default_value", frame)
00377: 
00378:             mapping_location_socket = control.get("mapping_location_socket")
00379:             if mapping_location_socket is not None:
00380:                 drift = HERO_MATERIAL_MAPPING_DRIFT
00381:                 loc = mapping_location_socket.default_value
00382:                 loc[0] = math.sin(frame * 0.012 + phase) * drift + mid * drift * 0.45
00383:                 loc[1] = math.cos(frame * 0.010 + phase) * drift + high * drift * 0.35
00384:                 loc[2] = frame * 0.0018 + pulse * drift * 0.20
00385:                 keyframe_if_possible(mapping_location_socket, "default_value", frame)
00386: 
00387:             mapping_rotation_socket = control.get("mapping_rotation_socket")
00388:             if mapping_rotation_socket is not None:
00389:                 rot = mapping_rotation_socket.default_value
00390:                 rot[0] = math.sin(frame * 0.006 + phase) * 0.08 * (0.35 + surface_drive)
00391:                 rot[1] = math.cos(frame * 0.005 + phase) * 0.06 * (0.30 + material_drive)
00392:                 rot[2] = frame * 0.0025 + pulse * 0.09
00393:                 keyframe_if_possible(mapping_rotation_socket, "default_value", frame)
00394: 
00395:     return len(controls)
```
