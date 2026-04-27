# Project Code Chunk 21/212

- File: `Scripting/v61b/atmosphere_setup.py`
- Part: `2`
- Lines: `347-554`

## Symbol Map
- Imports: `bpy`, `math`, `random`, `from config import PRIMARY_BASE_Z, AURA_RADIUS, USE_HERO_AURA_MESH, AURA_DEFORM_SUBDIV_VIEW, AURA_DEFORM_SUBDIV_RENDER, AURA_DEFORM_FIELD_RADIUS, AURA_DEFORM_DISPLACE_MIN, AURA_DEFORM_DISPLACE_MAX, AURA_DEFORM_DETAIL_MAX, AURA_DEFORM_WAVE_HEIGHT_MAX, AURA_DEFORM_FIELD_STRENGTH_MAX, ENERGY_RING_COUNT, RIBBON_COUNT, CREATE_VARIANTS, VARIANT_COUNT, VARIANT_RING_RADIUS, VARIANT_SCALE_MIN, VARIANT_SCALE_MAX, USE_MIST_PARTICLES, MIST_PARTICLE_COUNT, MIST_SCALE_MIN, MIST_SCALE_MAX, ATMOSPHERE_CUBE_SIZE, FOG_VOLUME_ENABLED, FOG_VOLUME_VIEWPORT_VISIBLE, FOG_RAMP_LOW_BASE, FOG_RAMP_HIGH_BASE, PALETTE_LIST, PEACE_PALETTE`, `from materials import build_aura_material, build_ring_material, build_ribbon_material, build_variant_material, build_atmosphere_volume_material, build_mist_particle_material`, `from asset_setup import duplicate_hierarchy, assign_material_to_hierarchy`, `from scene_utils import create_controller_empty`, `from fog_filaments import ensure_fog_filaments`
- Functions: `init_audio_props(obj)` line 62; `add_prop_driver(idblock, data_path, expression, prop_targets)` line 71; `create_aura_deform_field(controller, aura_location, parent)` line 96; `add_hero_aura_deformers(aura, controller, deform_field)` line 144; `create_hero_aura(parent)` line 249; `create_energy_rings(parent)` line 325; `create_energy_ribbons(parent)` line 361; `create_variants(hero_root, parent)` line 399; `create_atmosphere_cube(parent)` line 433; `create_mist_particles(parent)` line 502
- Assignments: `AURA_AUDIO_PROPS`

## Content
```py
00347:             ring.parent = parent
00348: 
00349:         rings.append({
00350:             "object": ring,
00351:             "emit_socket": emit_socket,
00352:             "base_scale": ring.scale.copy(),
00353:             "base_rot": ring.rotation_euler.copy(),
00354:             "base_loc": ring.location.copy(),
00355:             "phase": i * 0.9,
00356:         })
00357: 
00358:     return rings
00359: 
00360: 
00361: def create_energy_ribbons(parent=None):
00362:     ribbons = []
00363: 
00364:     for i in range(RIBBON_COUNT):
00365:         bpy.ops.curve.primitive_bezier_circle_add(
00366:             location=(0, 0, PRIMARY_BASE_Z + 1.05 + i * 0.20)
00367:         )
00368:         ribbon = bpy.context.active_object
00369:         ribbon.name = f"EnergyRibbon_{i:02d}"
00370:         ribbon.scale = (2.55 + i * 0.30, 1.35 + i * 0.14, 1.0)
00371:         ribbon.rotation_euler = (
00372:             math.radians(72 + i * 18),
00373:             math.radians(18 + i * 10),
00374:             math.radians(i * 30),
00375:         )
00376: 
00377:         ribbon.data.bevel_depth = 0.020 + i * 0.004
00378:         ribbon.data.resolution_u = 32
00379: 
00380:         color = PALETTE_LIST[(i + 2) % len(PALETTE_LIST)]
00381:         mat, emit_socket = build_ribbon_material(f"EnergyRibbonMat_{i:02d}", color)
00382:         ribbon.data.materials.append(mat)
00383: 
00384:         if parent is not None:
00385:             ribbon.parent = parent
00386: 
00387:         ribbons.append({
00388:             "object": ribbon,
00389:             "emit_socket": emit_socket,
00390:             "base_rot": ribbon.rotation_euler.copy(),
00391:             "base_loc": ribbon.location.copy(),
00392:             "base_scale": ribbon.scale.copy(),
00393:             "phase": i * 1.15,
00394:         })
00395: 
00396:     return ribbons
00397: 
00398: 
00399: def create_variants(hero_root, parent=None):
00400:     variants = []
00401: 
00402:     if not CREATE_VARIANTS:
00403:         return variants
00404: 
00405:     for i in range(VARIANT_COUNT):
00406:         ang = (math.tau / VARIANT_COUNT) * i
00407:         x = math.cos(ang) * VARIANT_RING_RADIUS
00408:         y = math.sin(ang) * VARIANT_RING_RADIUS
00409: 
00410:         dup = duplicate_hierarchy(hero_root, f"HeroVariantRoot_{i:02d}")
00411:         if parent is not None:
00412:             dup.parent = parent
00413: 
00414:         dup.location = (x, y, PRIMARY_BASE_Z + 0.25)
00415:         scale = random.uniform(VARIANT_SCALE_MIN, VARIANT_SCALE_MAX)
00416:         dup.scale = (scale, scale, scale)
00417:         dup.rotation_euler = (0.0, 0.0, ang + random.uniform(-0.24, 0.24))
00418: 
00419:         color = PALETTE_LIST[i % len(PALETTE_LIST)]
00420:         mat = build_variant_material(f"VariantPeaceMat_{i:02d}", color)
00421:         assign_material_to_hierarchy(dup, mat)
00422: 
00423:         variants.append({
00424:             "root": dup,
00425:             "angle": ang,
00426:             "base_location": dup.location.copy(),
00427:             "base_scale": scale,
00428:         })
00429: 
00430:     return variants
00431: 
00432: 
00433: def create_atmosphere_cube(parent=None):
00434:     mat, controls = build_atmosphere_volume_material()
00435: 
00436:     bpy.ops.mesh.primitive_cube_add(location=(0, 0, 3.0))
00437:     cube = bpy.context.active_object
00438:     cube.name = "AtmosphereCube"
00439:     cube["spaziotempo_volume_container"] = True
00440:     cube.scale = (
00441:         ATMOSPHERE_CUBE_SIZE * 0.5,
00442:         ATMOSPHERE_CUBE_SIZE * 0.5,
00443:         ATMOSPHERE_CUBE_SIZE * 0.5,
00444:     )
00445:     cube.data.materials.append(mat)
00446:     cube.display_type = 'WIRE'
00447:     cube.hide_select = True
00448:     cube.hide_render = not FOG_VOLUME_ENABLED
00449:     cube.hide_viewport = not FOG_VOLUME_VIEWPORT_VISIBLE
00450: 
00451:     if parent is not None:
00452:         cube.parent = parent
00453: 
00454:     try:
00455:         controls["ramp_low_ctrl"].position = FOG_RAMP_LOW_BASE
00456:         controls["ramp_high_ctrl"].position = FOG_RAMP_HIGH_BASE
00457:     except Exception:
00458:         pass
00459: 
00460:     controller = create_controller_empty(
00461:         "FogPulseController",
00462:         location=cube.location.copy(),
00463:         display_size=0.42,
00464:         hide_view=True,
00465:     )
00466:     if parent is not None:
00467:         controller.parent = parent
00468: 
00469:     filaments = ensure_fog_filaments(parent=parent)
00470: 
00471:     return {
00472:         "object": cube,
00473:         "material": mat,
00474:         "controller": controller,
00475:         "filaments": filaments,
00476:         "base_location": cube.location.copy(),
00477:         "base_scale": cube.scale.copy(),
00478:         "density_socket": controls["density_socket"],
00479:         "emission_socket": controls["emission_socket"],
00480:         "noise_scale_socket": controls["noise_scale_socket"],
00481:         "noise_detail_socket": controls.get("noise_detail_socket"),
00482:         "noise_roughness_socket": controls.get("noise_roughness_socket"),
00483:         "clump_noise_scale_socket": controls.get("clump_noise_scale_socket"),
00484:         "clump_noise_detail_socket": controls.get("clump_noise_detail_socket"),
00485:         "clump_noise_roughness_socket": controls.get("clump_noise_roughness_socket"),
00486:         "mapping_location_socket": controls["mapping_location_socket"],
00487:         "mapping_scale_socket": controls.get("mapping_scale_socket"),
00488:         "mapping_rotation_socket": controls.get("mapping_rotation_socket"),
00489:         "wave_scale_socket": controls.get("wave_scale_socket"),
00490:         "wave_distortion_socket": controls.get("wave_distortion_socket"),
00491:         "wave_phase_socket": controls.get("wave_phase_socket"),
00492:         "wave_weight_socket": controls.get("wave_weight_socket"),
00493:         "ramp_low_ctrl": controls["ramp_low_ctrl"],
00494:         "ramp_high_ctrl": controls["ramp_high_ctrl"],
00495:         "clump_ramp_low_ctrl": controls.get("clump_ramp_low_ctrl"),
00496:         "clump_ramp_high_ctrl": controls.get("clump_ramp_high_ctrl"),
00497:         "volume_color_socket": controls.get("volume_color_socket"),
00498:         "volume_anisotropy_socket": controls.get("volume_anisotropy_socket"),
00499:     }
00500: 
00501: 
00502: def create_mist_particles(parent=None):
00503:     particles = []
00504:     if not USE_MIST_PARTICLES:
00505:         return particles
00506: 
00507:     bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
00508:     root = bpy.context.active_object
00509:     root.name = "MistParticlesRoot"
00510: 
00511:     if parent is not None:
00512:         root.parent = parent
00513: 
00514:     color_choices = [
00515:         PEACE_PALETTE["warm_white"],
00516:         PEACE_PALETTE["soft_teal"],
00517:         PEACE_PALETTE["muted_gold"],
00518:     ]
00519: 
00520:     for i in range(MIST_PARTICLE_COUNT):
00521:         radius = random.uniform(1.1, 4.4)
00522:         angle = random.uniform(0.0, math.tau)
00523:         z = random.uniform(0.55, 3.2)
00524: 
00525:         x = math.cos(angle) * radius
00526:         y = math.sin(angle) * radius
00527: 
00528:         bpy.ops.mesh.primitive_ico_sphere_add(
00529:             subdivisions=1,
00530:             radius=random.uniform(0.03, 0.08),
00531:             location=(x, y, z),
00532:         )
00533:         obj = bpy.context.active_object
00534:         obj.name = f"MistParticle_{i:02d}"
00535:         obj.parent = root
00536: 
00537:         color = random.choice(color_choices)
00538:         mat, em_socket, mix_socket = build_mist_particle_material(
00539:             f"MistParticleMat_{i:02d}",
00540:             color
00541:         )
00542:         obj.data.materials.append(mat)
00543: 
00544:         particles.append({
00545:             "object": obj,
00546:             "material": mat,
00547:             "emission_socket": em_socket,
00548:             "mix_socket": mix_socket,
00549:             "base_location": obj.location.copy(),
00550:             "phase": random.uniform(0.0, math.tau),
00551:             "base_scale": random.uniform(MIST_SCALE_MIN, MIST_SCALE_MAX),
00552:         })
00553: 
00554:     return particles
```
