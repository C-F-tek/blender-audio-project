# Project Code Chunk 51/212

- File: `Scripting/v61b/physics_setup.py`
- Part: `2`
- Lines: `324-614`

## Symbol Map
- Imports: `bpy`, `math`, `random`, `from config import USE_PHYSICS_ACCENTS, PHYSICS_ACCENT_COUNT, PRIMARY_BASE_Z, TURB_STRENGTH_MIN, VORTEX_STRENGTH_MIN, PHYSICS_ORBIT_RADIUS_MIN, PHYSICS_ORBIT_RADIUS_MAX, PHYSICS_ATOM_ORBIT_SPEED_MIN, PHYSICS_ATOM_ORBIT_SPEED_MAX, PHYSICS_ATOM_MICRO_WOBBLE, HERO_GRAVITY_STRENGTH_MIN, TETHER_SPRING_STIFFNESS, TETHER_SPRING_DAMPING, USE_RHYTHM_PARTICLE_PHYSICS, RHYTHM_PARTICLE_COUNT, RHYTHM_DUST_PARTICLE_COUNT, RHYTHM_STREAK_PARTICLE_COUNT, RHYTHM_PARTICLE_LIFETIME, RHYTHM_DUST_LIFETIME, RHYTHM_PARTICLE_EMITTER_RADIUS, RHYTHM_PARTICLE_EMITTER_Z, PARTICLE_SOURCE_LOCATION, RHYTHM_PARTICLE_SOURCE_RADIUS, RHYTHM_PARTICLE_SIZE_MIN, RHYTHM_PARTICLE_NORMAL_MIN, RHYTHM_PARTICLE_TANGENT_MIN, RHYTHM_PARTICLE_BROWNIAN_MIN, USE_ALBUM_LETTER_PARTICLES, ALBUM_PARTICLE_TEXT, ALBUM_LETTER_PARTICLE_COUNT, ALBUM_LETTER_PARTICLE_LIFETIME, ALBUM_LETTER_SOURCE_SIZE, ALBUM_LETTER_EXTRUDE, ALBUM_LETTER_EMISSION_STRENGTH, ALBUM_LETTER_PARTICLE_SIZE_MIN, PHYSICS_ACCENT_EMISSION_MIN, PHYSICS_ACCENT_MIX_MIN, PALETTE_LIST, PEACE_PALETTE`, `from materials import build_variant_material`, `from scene_utils import deselect_all, safe_active`
- Functions: `set_if_available(obj, attr, value)` line 50; `build_particle_emission_material(name, color, strength)` line 60; `build_invisible_emitter_material()` line 82; `get_material_node_socket(material, node_name, socket_name, is_output)` line 106; `add_particle_collision(obj)` line 121; `add_passive_rigidbody(obj)` line 138; `add_active_rigidbody(obj, mass)` line 147; `create_hidden_anchor(name, location)` line 159; `create_spring_constraint(name, object1, object2, location)` line 172; `create_particle_instance(name, color, strength, shape)` line 215; `create_album_letter_particle_collection(parent)` line 255; `create_particle_emitter(name, kind, invisible_mat)` line 339; `configure_particle_system(emitter, name, instance_obj, count, lifetime, particle_size, normal_factor, tangent_factor, brownian_factor, damping, child_count, child_percent, instance_collection)` line 367; `create_rhythm_particle_physics(parent)` line 445; `create_physics_accents(parent)` line 606

## Content
```py
00324:                 if coll != collection:
00325:                     coll.objects.unlink(obj)
00326:             collection.objects.link(obj)
00327:         except Exception:
00328:             pass
00329: 
00330:         letters.append({
00331:             "object": obj,
00332:             "base_scale": obj.scale.copy(),
00333:             "phase": idx * 0.37,
00334:         })
00335: 
00336:     return collection, root, letters
00337: 
00338: 
00339: def create_particle_emitter(name, kind, invisible_mat):
00340:     if kind == "sphere":
00341:         bpy.ops.mesh.primitive_uv_sphere_add(
00342:             segments=32,
00343:             ring_count=16,
00344:             radius=4.25,
00345:             location=(0, 0, PRIMARY_BASE_Z + 1.00),
00346:         )
00347:     else:
00348:         radius = RHYTHM_PARTICLE_EMITTER_RADIUS
00349:         if kind == "wide_ring":
00350:             radius *= 1.62
00351:         bpy.ops.mesh.primitive_torus_add(
00352:             major_radius=radius,
00353:             minor_radius=0.036 if kind == "ring" else 0.022,
00354:             major_segments=128,
00355:             minor_segments=8,
00356:             location=(0, 0, RHYTHM_PARTICLE_EMITTER_Z),
00357:         )
00358: 
00359:     emitter = bpy.context.active_object
00360:     emitter.name = name
00361:     emitter.data.materials.append(invisible_mat)
00362:     emitter.display_type = 'WIRE'
00363:     emitter.hide_select = True
00364:     return emitter
00365: 
00366: 
00367: def configure_particle_system(
00368:     emitter,
00369:     name,
00370:     instance_obj,
00371:     count,
00372:     lifetime,
00373:     particle_size,
00374:     normal_factor,
00375:     tangent_factor,
00376:     brownian_factor,
00377:     damping,
00378:     child_count,
00379:     child_percent,
00380:     instance_collection=None,
00381: ):
00382:     mod = emitter.modifiers.new(name=name, type='PARTICLE_SYSTEM')
00383:     ps = mod.particle_system
00384:     settings = ps.settings
00385:     settings.name = f"{name}Settings"
00386: 
00387:     frame_end = max(1, int(bpy.context.scene.frame_end))
00388: 
00389:     settings.type = 'EMITTER'
00390:     settings.physics_type = 'NEWTON'
00391:     if instance_collection is not None:
00392:         settings.render_type = 'COLLECTION'
00393:         set_if_available(settings, "instance_collection", instance_collection)
00394:         set_if_available(settings, "use_collection_pick_random", True)
00395:         set_if_available(settings, "use_whole_collection", False)
00396:         set_if_available(settings, "use_collection_count", False)
00397:     else:
00398:         settings.render_type = 'OBJECT'
00399:         settings.instance_object = instance_obj
00400:     settings.count = count
00401:     settings.frame_start = 1
00402:     settings.frame_end = frame_end
00403:     settings.lifetime = lifetime
00404:     settings.lifetime_random = 0.35
00405:     settings.particle_size = particle_size
00406:     settings.size_random = 0.72
00407:     settings.normal_factor = normal_factor
00408:     settings.tangent_factor = tangent_factor
00409:     settings.brownian_factor = brownian_factor
00410:     settings.damping = damping
00411:     settings.factor_random = 0.68
00412:     settings.show_unborn = False
00413:     settings.use_dead = False
00414:     settings.use_die_on_collision = False
00415: 
00416:     set_if_available(settings, "emit_from", 'FACE')
00417:     set_if_available(settings, "distribution", 'RAND')
00418:     set_if_available(settings, "use_emit_random", True)
00419:     set_if_available(settings, "use_modifier_stack", True)
00420:     set_if_available(settings, "use_rotations", True)
00421:     set_if_available(settings, "rotation_mode", 'VEL')
00422:     set_if_available(settings, "angular_velocity_mode", 'VELOCITY')
00423:     set_if_available(settings, "angular_velocity_factor", 0.72)
00424:     set_if_available(settings, "child_type", 'INTERPOLATED')
00425:     set_if_available(settings, "rendered_child_count", child_count)
00426:     set_if_available(settings, "child_percent", child_percent)
00427:     set_if_available(settings, "roughness_1_size", 0.65)
00428:     set_if_available(settings, "roughness_1", 0.018)
00429:     set_if_available(settings, "roughness_2_size", 0.34)
00430:     set_if_available(settings, "roughness_2", 0.010)
00431:     set_if_available(settings, "roughness_2_threshold", 0.42)
00432:     set_if_available(settings, "display_percentage", 45)
00433: 
00434:     try:
00435:         settings.effector_weights.gravity = 0.0
00436:         settings.effector_weights.turbulence = 1.0
00437:         settings.effector_weights.vortex = 1.0
00438:         settings.effector_weights.wind = 1.0
00439:     except Exception:
00440:         pass
00441: 
00442:     return ps, settings
00443: 
00444: 
00445: def create_rhythm_particle_physics(parent=None):
00446:     if not USE_RHYTHM_PARTICLE_PHYSICS:
00447:         return []
00448: 
00449:     bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
00450:     root = bpy.context.active_object
00451:     root.name = "RhythmParticlePhysicsRoot"
00452:     if parent is not None:
00453:         root.parent = parent
00454: 
00455:     invisible_mat = build_invisible_emitter_material()
00456: 
00457:     spark_obj, spark_mat, spark_emit = create_particle_instance(
00458:         "BeatSparkParticle",
00459:         PEACE_PALETTE["warm_white"],
00460:         0.40,
00461:     )
00462:     dust_obj, dust_mat, dust_emit = create_particle_instance(
00463:         "OrbitDustParticle",
00464:         PEACE_PALETTE["soft_teal"],
00465:         0.18,
00466:     )
00467:     streak_obj, streak_mat, streak_emit = create_particle_instance(
00468:         "HighStreakParticle",
00469:         PEACE_PALETTE["muted_gold"],
00470:         0.32,
00471:         shape="streak",
00472:     )
00473:     letter_collection, letter_root, letter_sources = create_album_letter_particle_collection(parent=root)
00474: 
00475:     for obj in [spark_obj, dust_obj, streak_obj]:
00476:         obj.parent = root
00477: 
00478:     pulse_emitter = create_particle_emitter("BeatPulseParticleEmitter", "ring", invisible_mat)
00479:     dust_emitter = create_particle_emitter("OrbitDustParticleEmitter", "sphere", invisible_mat)
00480:     streak_emitter = create_particle_emitter("HighStreakParticleEmitter", "wide_ring", invisible_mat)
00481:     letter_emitter = None
00482:     if letter_collection is not None and letter_sources:
00483:         letter_emitter = create_particle_emitter("AlbumLetterParticleEmitter", "wide_ring", invisible_mat)
00484: 
00485:     for emitter in [pulse_emitter, dust_emitter, streak_emitter, letter_emitter]:
00486:         if emitter is not None:
00487:             emitter.parent = root
00488: 
00489:     _, pulse_settings = configure_particle_system(
00490:         pulse_emitter,
00491:         "BeatPulseParticleSystem",
00492:         spark_obj,
00493:         RHYTHM_PARTICLE_COUNT,
00494:         RHYTHM_PARTICLE_LIFETIME,
00495:         RHYTHM_PARTICLE_SIZE_MIN,
00496:         RHYTHM_PARTICLE_NORMAL_MIN,
00497:         RHYTHM_PARTICLE_TANGENT_MIN,
00498:         RHYTHM_PARTICLE_BROWNIAN_MIN,
00499:         0.13,
00500:         3,
00501:         40,
00502:     )
00503:     _, dust_settings = configure_particle_system(
00504:         dust_emitter,
00505:         "OrbitDustParticleSystem",
00506:         dust_obj,
00507:         RHYTHM_DUST_PARTICLE_COUNT,
00508:         RHYTHM_DUST_LIFETIME,
00509:         RHYTHM_PARTICLE_SIZE_MIN * 0.72,
00510:         0.035,
00511:         0.12,
00512:         0.42,
00513:         0.24,
00514:         2,
00515:         25,
00516:     )
00517:     _, streak_settings = configure_particle_system(
00518:         streak_emitter,
00519:         "HighStreakParticleSystem",
00520:         streak_obj,
00521:         RHYTHM_STREAK_PARTICLE_COUNT,
00522:         max(42, int(RHYTHM_PARTICLE_LIFETIME * 0.70)),
00523:         RHYTHM_PARTICLE_SIZE_MIN * 0.95,
00524:         0.30,
00525:         0.55,
00526:         0.06,
00527:         0.08,
00528:         1,
00529:         12,
00530:     )
00531:     letter_settings = []
00532:     if letter_emitter is not None:
00533:         per_letter_count = max(8, int(ALBUM_LETTER_PARTICLE_COUNT / max(1, len(letter_sources))))
00534:         for idx, letter in enumerate(letter_sources):
00535:             _, settings = configure_particle_system(
00536:                 letter_emitter,
00537:                 f"AlbumLetterParticleSystem_{idx:02d}",
00538:                 letter["object"],
00539:                 per_letter_count,
00540:                 ALBUM_LETTER_PARTICLE_LIFETIME,
00541:                 ALBUM_LETTER_PARTICLE_SIZE_MIN,
00542:                 0.16,
00543:                 0.32,
00544:                 0.18,
00545:                 0.16,
00546:                 1,
00547:                 10,
00548:             )
00549:             letter_settings.append(settings)
00550: 
00551:     systems = [
00552:         {
00553:             "mode": "pulse",
00554:             "emitter": pulse_emitter,
00555:             "settings": pulse_settings,
00556:             "material": spark_mat,
00557:             "emission_socket": spark_emit,
00558:             "base_location": pulse_emitter.location.copy(),
00559:             "base_rotation": pulse_emitter.rotation_euler.copy(),
00560:             "base_scale": pulse_emitter.scale.copy(),
00561:             "phase": 0.0,
00562:         },
00563:         {
00564:             "mode": "dust",
00565:             "emitter": dust_emitter,
00566:             "settings": dust_settings,
00567:             "material": dust_mat,
00568:             "emission_socket": dust_emit,
00569:             "base_location": dust_emitter.location.copy(),
00570:             "base_rotation": dust_emitter.rotation_euler.copy(),
00571:             "base_scale": dust_emitter.scale.copy(),
00572:             "phase": 1.7,
00573:         },
00574:         {
00575:             "mode": "streak",
00576:             "emitter": streak_emitter,
00577:             "settings": streak_settings,
00578:             "material": streak_mat,
00579:             "emission_socket": streak_emit,
00580:             "base_location": streak_emitter.location.copy(),
00581:             "base_rotation": streak_emitter.rotation_euler.copy(),
00582:             "base_scale": streak_emitter.scale.copy(),
00583:             "phase": 3.1,
00584:         },
00585:     ]
00586: 
00587:     if letter_emitter is not None and letter_settings:
00588:         systems.append({
00589:             "mode": "letters",
00590:             "emitter": letter_emitter,
00591:             "settings": letter_settings[0],
00592:             "settings_list": letter_settings,
00593:             "material": None,
00594:             "emission_socket": None,
00595:             "base_location": letter_emitter.location.copy(),
00596:             "base_rotation": letter_emitter.rotation_euler.copy(),
00597:             "base_scale": letter_emitter.scale.copy(),
00598:             "phase": 4.4,
00599:             "letter_root": letter_root,
00600:             "letter_sources": letter_sources,
00601:         })
00602: 
00603:     return systems
00604: 
00605: 
00606: def create_physics_accents(parent=None):
00607:     floor = bpy.data.objects.get("PeaceFloor")
00608:     invisible_floor = bpy.data.objects.get("InvisibleParticleFloor")
00609:     add_particle_collision(floor)
00610:     add_particle_collision(invisible_floor)
00611:     rhythm_particles = create_rhythm_particle_physics(parent=parent)
00612: 
00613:     if not USE_PHYSICS_ACCENTS:
00614:         return {
```
