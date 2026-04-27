# Project Code Chunk 80/212

- File: `Scripting/v61b_backgood/atmosphere_setup.py`
- Part: `2`
- Lines: `349-543`

## Symbol Map
- Imports: `bpy`, `math`, `random`, `from config import PRIMARY_BASE_Z, AURA_RADIUS, USE_HERO_AURA_MESH, AURA_DEFORM_SUBDIV_VIEW, AURA_DEFORM_SUBDIV_RENDER, AURA_DEFORM_FIELD_RADIUS, AURA_DEFORM_DISPLACE_MIN, AURA_DEFORM_DISPLACE_MAX, AURA_DEFORM_DETAIL_MAX, AURA_DEFORM_WAVE_HEIGHT_MAX, AURA_DEFORM_FIELD_STRENGTH_MAX, ENERGY_RING_COUNT, RIBBON_COUNT, CREATE_VARIANTS, VARIANT_COUNT, VARIANT_RING_RADIUS, VARIANT_SCALE_MIN, VARIANT_SCALE_MAX, USE_MIST_PARTICLES, MIST_PARTICLE_COUNT, MIST_SCALE_MIN, MIST_SCALE_MAX, ATMOSPHERE_CUBE_SIZE, FOG_RAMP_LOW_BASE, FOG_RAMP_HIGH_BASE, PALETTE_LIST, PEACE_PALETTE`, `from materials import build_aura_material, build_ring_material, build_ribbon_material, build_variant_material, build_atmosphere_volume_material, build_mist_particle_material`, `from asset_setup import duplicate_hierarchy, assign_material_to_hierarchy`, `from scene_utils import create_controller_empty`
- Functions: `init_audio_props(obj)` line 59; `add_prop_driver(idblock, data_path, expression, prop_targets)` line 68; `create_aura_deform_field(controller, aura_location, parent)` line 93; `add_hero_aura_deformers(aura, controller, deform_field)` line 141; `create_hero_aura(parent)` line 246; `create_energy_rings(parent)` line 322; `create_energy_ribbons(parent)` line 358; `create_variants(hero_root, parent)` line 396; `create_atmosphere_cube()` line 430; `create_mist_particles(parent)` line 491
- Assignments: `AURA_AUDIO_PROPS`

## Content
```py
00349:             "base_scale": ring.scale.copy(),
00350:             "base_rot": ring.rotation_euler.copy(),
00351:             "base_loc": ring.location.copy(),
00352:             "phase": i * 0.9,
00353:         })
00354: 
00355:     return rings
00356: 
00357: 
00358: def create_energy_ribbons(parent=None):
00359:     ribbons = []
00360: 
00361:     for i in range(RIBBON_COUNT):
00362:         bpy.ops.curve.primitive_bezier_circle_add(
00363:             location=(0, 0, PRIMARY_BASE_Z + 1.05 + i * 0.20)
00364:         )
00365:         ribbon = bpy.context.active_object
00366:         ribbon.name = f"EnergyRibbon_{i:02d}"
00367:         ribbon.scale = (2.55 + i * 0.30, 1.35 + i * 0.14, 1.0)
00368:         ribbon.rotation_euler = (
00369:             math.radians(72 + i * 18),
00370:             math.radians(18 + i * 10),
00371:             math.radians(i * 30),
00372:         )
00373: 
00374:         ribbon.data.bevel_depth = 0.020 + i * 0.004
00375:         ribbon.data.resolution_u = 32
00376: 
00377:         color = PALETTE_LIST[(i + 2) % len(PALETTE_LIST)]
00378:         mat, emit_socket = build_ribbon_material(f"EnergyRibbonMat_{i:02d}", color)
00379:         ribbon.data.materials.append(mat)
00380: 
00381:         if parent is not None:
00382:             ribbon.parent = parent
00383: 
00384:         ribbons.append({
00385:             "object": ribbon,
00386:             "emit_socket": emit_socket,
00387:             "base_rot": ribbon.rotation_euler.copy(),
00388:             "base_loc": ribbon.location.copy(),
00389:             "base_scale": ribbon.scale.copy(),
00390:             "phase": i * 1.15,
00391:         })
00392: 
00393:     return ribbons
00394: 
00395: 
00396: def create_variants(hero_root, parent=None):
00397:     variants = []
00398: 
00399:     if not CREATE_VARIANTS:
00400:         return variants
00401: 
00402:     for i in range(VARIANT_COUNT):
00403:         ang = (math.tau / VARIANT_COUNT) * i
00404:         x = math.cos(ang) * VARIANT_RING_RADIUS
00405:         y = math.sin(ang) * VARIANT_RING_RADIUS
00406: 
00407:         dup = duplicate_hierarchy(hero_root, f"HeroVariantRoot_{i:02d}")
00408:         if parent is not None:
00409:             dup.parent = parent
00410: 
00411:         dup.location = (x, y, PRIMARY_BASE_Z + 0.25)
00412:         scale = random.uniform(VARIANT_SCALE_MIN, VARIANT_SCALE_MAX)
00413:         dup.scale = (scale, scale, scale)
00414:         dup.rotation_euler = (0.0, 0.0, ang + random.uniform(-0.24, 0.24))
00415: 
00416:         color = PALETTE_LIST[i % len(PALETTE_LIST)]
00417:         mat = build_variant_material(f"VariantPeaceMat_{i:02d}", color)
00418:         assign_material_to_hierarchy(dup, mat)
00419: 
00420:         variants.append({
00421:             "root": dup,
00422:             "angle": ang,
00423:             "base_location": dup.location.copy(),
00424:             "base_scale": scale,
00425:         })
00426: 
00427:     return variants
00428: 
00429: 
00430: def create_atmosphere_cube():
00431:     mat, controls = build_atmosphere_volume_material()
00432: 
00433:     bpy.ops.mesh.primitive_cube_add(location=(0, 0, 3.0))
00434:     cube = bpy.context.active_object
00435:     cube.name = "AtmosphereCube"
00436:     cube["spaziotempo_volume_container"] = True
00437:     cube.scale = (
00438:         ATMOSPHERE_CUBE_SIZE * 0.5,
00439:         ATMOSPHERE_CUBE_SIZE * 0.5,
00440:         ATMOSPHERE_CUBE_SIZE * 0.5,
00441:     )
00442:     cube.data.materials.append(mat)
00443:     cube.display_type = 'WIRE'
00444:     cube.hide_select = True
00445:     cube.hide_render = False
00446:     cube.hide_viewport = False
00447: 
00448:     try:
00449:         controls["ramp_low_ctrl"].position = FOG_RAMP_LOW_BASE
00450:         controls["ramp_high_ctrl"].position = FOG_RAMP_HIGH_BASE
00451:     except Exception:
00452:         pass
00453: 
00454:     controller = create_controller_empty(
00455:         "FogPulseController",
00456:         location=cube.location.copy(),
00457:         display_size=0.42,
00458:         hide_view=True,
00459:     )
00460: 
00461:     return {
00462:         "object": cube,
00463:         "material": mat,
00464:         "controller": controller,
00465:         "base_location": cube.location.copy(),
00466:         "base_scale": cube.scale.copy(),
00467:         "density_socket": controls["density_socket"],
00468:         "emission_socket": controls["emission_socket"],
00469:         "noise_scale_socket": controls["noise_scale_socket"],
00470:         "noise_detail_socket": controls.get("noise_detail_socket"),
00471:         "noise_roughness_socket": controls.get("noise_roughness_socket"),
00472:         "clump_noise_scale_socket": controls.get("clump_noise_scale_socket"),
00473:         "clump_noise_detail_socket": controls.get("clump_noise_detail_socket"),
00474:         "clump_noise_roughness_socket": controls.get("clump_noise_roughness_socket"),
00475:         "mapping_location_socket": controls["mapping_location_socket"],
00476:         "mapping_scale_socket": controls.get("mapping_scale_socket"),
00477:         "mapping_rotation_socket": controls.get("mapping_rotation_socket"),
00478:         "wave_scale_socket": controls.get("wave_scale_socket"),
00479:         "wave_distortion_socket": controls.get("wave_distortion_socket"),
00480:         "wave_phase_socket": controls.get("wave_phase_socket"),
00481:         "wave_weight_socket": controls.get("wave_weight_socket"),
00482:         "ramp_low_ctrl": controls["ramp_low_ctrl"],
00483:         "ramp_high_ctrl": controls["ramp_high_ctrl"],
00484:         "clump_ramp_low_ctrl": controls.get("clump_ramp_low_ctrl"),
00485:         "clump_ramp_high_ctrl": controls.get("clump_ramp_high_ctrl"),
00486:         "volume_color_socket": controls.get("volume_color_socket"),
00487:         "volume_anisotropy_socket": controls.get("volume_anisotropy_socket"),
00488:     }
00489: 
00490: 
00491: def create_mist_particles(parent=None):
00492:     particles = []
00493:     if not USE_MIST_PARTICLES:
00494:         return particles
00495: 
00496:     bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
00497:     root = bpy.context.active_object
00498:     root.name = "MistParticlesRoot"
00499: 
00500:     if parent is not None:
00501:         root.parent = parent
00502: 
00503:     color_choices = [
00504:         PEACE_PALETTE["warm_white"],
00505:         PEACE_PALETTE["soft_teal"],
00506:         PEACE_PALETTE["muted_gold"],
00507:     ]
00508: 
00509:     for i in range(MIST_PARTICLE_COUNT):
00510:         radius = random.uniform(1.1, 4.4)
00511:         angle = random.uniform(0.0, math.tau)
00512:         z = random.uniform(0.55, 3.2)
00513: 
00514:         x = math.cos(angle) * radius
00515:         y = math.sin(angle) * radius
00516: 
00517:         bpy.ops.mesh.primitive_ico_sphere_add(
00518:             subdivisions=1,
00519:             radius=random.uniform(0.03, 0.08),
00520:             location=(x, y, z),
00521:         )
00522:         obj = bpy.context.active_object
00523:         obj.name = f"MistParticle_{i:02d}"
00524:         obj.parent = root
00525: 
00526:         color = random.choice(color_choices)
00527:         mat, em_socket, mix_socket = build_mist_particle_material(
00528:             f"MistParticleMat_{i:02d}",
00529:             color
00530:         )
00531:         obj.data.materials.append(mat)
00532: 
00533:         particles.append({
00534:             "object": obj,
00535:             "material": mat,
00536:             "emission_socket": em_socket,
00537:             "mix_socket": mix_socket,
00538:             "base_location": obj.location.copy(),
00539:             "phase": random.uniform(0.0, math.tau),
00540:             "base_scale": random.uniform(MIST_SCALE_MIN, MIST_SCALE_MAX),
00541:         })
00542: 
00543:     return particles
```
