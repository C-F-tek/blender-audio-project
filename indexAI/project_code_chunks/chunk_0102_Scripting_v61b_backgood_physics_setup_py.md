# Project Code Chunk 102/212

- File: `Scripting/v61b_backgood/physics_setup.py`
- Part: `2`
- Lines: `324-614`

## Symbol Map
- Imports: `bpy`, `math`, `random`, `from config import USE_PHYSICS_ACCENTS, PHYSICS_ACCENT_COUNT, PRIMARY_BASE_Z, TURB_STRENGTH_MIN, VORTEX_STRENGTH_MIN, PHYSICS_ORBIT_RADIUS_MIN, PHYSICS_ORBIT_RADIUS_MAX, TETHER_SPRING_STIFFNESS, TETHER_SPRING_DAMPING, USE_RHYTHM_PARTICLE_PHYSICS, RHYTHM_PARTICLE_COUNT, RHYTHM_DUST_PARTICLE_COUNT, RHYTHM_STREAK_PARTICLE_COUNT, RHYTHM_PARTICLE_LIFETIME, RHYTHM_DUST_LIFETIME, RHYTHM_PARTICLE_EMITTER_RADIUS, RHYTHM_PARTICLE_EMITTER_Z, PARTICLE_SOURCE_LOCATION, RHYTHM_PARTICLE_SOURCE_RADIUS, RHYTHM_PARTICLE_SIZE_MIN, RHYTHM_PARTICLE_NORMAL_MIN, RHYTHM_PARTICLE_TANGENT_MIN, RHYTHM_PARTICLE_BROWNIAN_MIN, USE_ALBUM_LETTER_PARTICLES, ALBUM_PARTICLE_TEXT, ALBUM_LETTER_PARTICLE_COUNT, ALBUM_LETTER_PARTICLE_LIFETIME, ALBUM_LETTER_SOURCE_SIZE, ALBUM_LETTER_EXTRUDE, ALBUM_LETTER_EMISSION_STRENGTH, ALBUM_LETTER_PARTICLE_SIZE_MIN, PHYSICS_ACCENT_EMISSION_MIN, PHYSICS_ACCENT_MIX_MIN, PALETTE_LIST, PEACE_PALETTE`, `from materials import build_variant_material`, `from scene_utils import deselect_all, safe_active`
- Functions: `set_if_available(obj, attr, value)` line 46; `build_particle_emission_material(name, color, strength)` line 56; `build_invisible_emitter_material()` line 78; `get_material_node_socket(material, node_name, socket_name, is_output)` line 102; `add_particle_collision(obj)` line 117; `add_passive_rigidbody(obj)` line 134; `add_active_rigidbody(obj, mass)` line 143; `create_hidden_anchor(name, location)` line 155; `create_spring_constraint(name, object1, object2, location)` line 168; `create_particle_instance(name, color, strength, shape)` line 211; `create_album_letter_particle_collection(parent)` line 251; `create_particle_emitter(name, kind, invisible_mat)` line 335; `configure_particle_system(emitter, name, instance_obj, count, lifetime, particle_size, normal_factor, tangent_factor, brownian_factor, damping, child_count, child_percent, instance_collection)` line 363; `create_rhythm_particle_physics(parent)` line 441; `create_physics_accents(parent)` line 602

## Content
```py
00324:             pass
00325: 
00326:         letters.append({
00327:             "object": obj,
00328:             "base_scale": obj.scale.copy(),
00329:             "phase": idx * 0.37,
00330:         })
00331: 
00332:     return collection, root, letters
00333: 
00334: 
00335: def create_particle_emitter(name, kind, invisible_mat):
00336:     if kind == "sphere":
00337:         bpy.ops.mesh.primitive_uv_sphere_add(
00338:             segments=32,
00339:             ring_count=16,
00340:             radius=4.25,
00341:             location=(0, 0, PRIMARY_BASE_Z + 1.00),
00342:         )
00343:     else:
00344:         radius = RHYTHM_PARTICLE_EMITTER_RADIUS
00345:         if kind == "wide_ring":
00346:             radius *= 1.62
00347:         bpy.ops.mesh.primitive_torus_add(
00348:             major_radius=radius,
00349:             minor_radius=0.036 if kind == "ring" else 0.022,
00350:             major_segments=128,
00351:             minor_segments=8,
00352:             location=(0, 0, RHYTHM_PARTICLE_EMITTER_Z),
00353:         )
00354: 
00355:     emitter = bpy.context.active_object
00356:     emitter.name = name
00357:     emitter.data.materials.append(invisible_mat)
00358:     emitter.display_type = 'WIRE'
00359:     emitter.hide_select = True
00360:     return emitter
00361: 
00362: 
00363: def configure_particle_system(
00364:     emitter,
00365:     name,
00366:     instance_obj,
00367:     count,
00368:     lifetime,
00369:     particle_size,
00370:     normal_factor,
00371:     tangent_factor,
00372:     brownian_factor,
00373:     damping,
00374:     child_count,
00375:     child_percent,
00376:     instance_collection=None,
00377: ):
00378:     mod = emitter.modifiers.new(name=name, type='PARTICLE_SYSTEM')
00379:     ps = mod.particle_system
00380:     settings = ps.settings
00381:     settings.name = f"{name}Settings"
00382: 
00383:     frame_end = max(1, int(bpy.context.scene.frame_end))
00384: 
00385:     settings.type = 'EMITTER'
00386:     settings.physics_type = 'NEWTON'
00387:     if instance_collection is not None:
00388:         settings.render_type = 'COLLECTION'
00389:         set_if_available(settings, "instance_collection", instance_collection)
00390:         set_if_available(settings, "use_collection_pick_random", True)
00391:         set_if_available(settings, "use_whole_collection", False)
00392:         set_if_available(settings, "use_collection_count", False)
00393:     else:
00394:         settings.render_type = 'OBJECT'
00395:         settings.instance_object = instance_obj
00396:     settings.count = count
00397:     settings.frame_start = 1
00398:     settings.frame_end = frame_end
00399:     settings.lifetime = lifetime
00400:     settings.lifetime_random = 0.35
00401:     settings.particle_size = particle_size
00402:     settings.size_random = 0.72
00403:     settings.normal_factor = normal_factor
00404:     settings.tangent_factor = tangent_factor
00405:     settings.brownian_factor = brownian_factor
00406:     settings.damping = damping
00407:     settings.factor_random = 0.68
00408:     settings.show_unborn = False
00409:     settings.use_dead = False
00410:     settings.use_die_on_collision = False
00411: 
00412:     set_if_available(settings, "emit_from", 'FACE')
00413:     set_if_available(settings, "distribution", 'RAND')
00414:     set_if_available(settings, "use_emit_random", True)
00415:     set_if_available(settings, "use_modifier_stack", True)
00416:     set_if_available(settings, "use_rotations", True)
00417:     set_if_available(settings, "rotation_mode", 'VEL')
00418:     set_if_available(settings, "angular_velocity_mode", 'VELOCITY')
00419:     set_if_available(settings, "angular_velocity_factor", 0.72)
00420:     set_if_available(settings, "child_type", 'INTERPOLATED')
00421:     set_if_available(settings, "rendered_child_count", child_count)
00422:     set_if_available(settings, "child_percent", child_percent)
00423:     set_if_available(settings, "roughness_1_size", 0.65)
00424:     set_if_available(settings, "roughness_1", 0.018)
00425:     set_if_available(settings, "roughness_2_size", 0.34)
00426:     set_if_available(settings, "roughness_2", 0.010)
00427:     set_if_available(settings, "roughness_2_threshold", 0.42)
00428:     set_if_available(settings, "display_percentage", 45)
00429: 
00430:     try:
00431:         settings.effector_weights.gravity = 0.0
00432:         settings.effector_weights.turbulence = 1.0
00433:         settings.effector_weights.vortex = 1.0
00434:         settings.effector_weights.wind = 1.0
00435:     except Exception:
00436:         pass
00437: 
00438:     return ps, settings
00439: 
00440: 
00441: def create_rhythm_particle_physics(parent=None):
00442:     if not USE_RHYTHM_PARTICLE_PHYSICS:
00443:         return []
00444: 
00445:     bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
00446:     root = bpy.context.active_object
00447:     root.name = "RhythmParticlePhysicsRoot"
00448:     if parent is not None:
00449:         root.parent = parent
00450: 
00451:     invisible_mat = build_invisible_emitter_material()
00452: 
00453:     spark_obj, spark_mat, spark_emit = create_particle_instance(
00454:         "BeatSparkParticle",
00455:         PEACE_PALETTE["warm_white"],
00456:         0.40,
00457:     )
00458:     dust_obj, dust_mat, dust_emit = create_particle_instance(
00459:         "OrbitDustParticle",
00460:         PEACE_PALETTE["soft_teal"],
00461:         0.18,
00462:     )
00463:     streak_obj, streak_mat, streak_emit = create_particle_instance(
00464:         "HighStreakParticle",
00465:         PEACE_PALETTE["muted_gold"],
00466:         0.32,
00467:         shape="streak",
00468:     )
00469:     letter_collection, letter_root, letter_sources = create_album_letter_particle_collection(parent=root)
00470: 
00471:     for obj in [spark_obj, dust_obj, streak_obj]:
00472:         obj.parent = root
00473: 
00474:     pulse_emitter = create_particle_emitter("BeatPulseParticleEmitter", "ring", invisible_mat)
00475:     dust_emitter = create_particle_emitter("OrbitDustParticleEmitter", "sphere", invisible_mat)
00476:     streak_emitter = create_particle_emitter("HighStreakParticleEmitter", "wide_ring", invisible_mat)
00477:     letter_emitter = None
00478:     if letter_collection is not None and letter_sources:
00479:         letter_emitter = create_particle_emitter("AlbumLetterParticleEmitter", "wide_ring", invisible_mat)
00480: 
00481:     for emitter in [pulse_emitter, dust_emitter, streak_emitter, letter_emitter]:
00482:         if emitter is not None:
00483:             emitter.parent = root
00484: 
00485:     _, pulse_settings = configure_particle_system(
00486:         pulse_emitter,
00487:         "BeatPulseParticleSystem",
00488:         spark_obj,
00489:         RHYTHM_PARTICLE_COUNT,
00490:         RHYTHM_PARTICLE_LIFETIME,
00491:         RHYTHM_PARTICLE_SIZE_MIN,
00492:         RHYTHM_PARTICLE_NORMAL_MIN,
00493:         RHYTHM_PARTICLE_TANGENT_MIN,
00494:         RHYTHM_PARTICLE_BROWNIAN_MIN,
00495:         0.13,
00496:         3,
00497:         40,
00498:     )
00499:     _, dust_settings = configure_particle_system(
00500:         dust_emitter,
00501:         "OrbitDustParticleSystem",
00502:         dust_obj,
00503:         RHYTHM_DUST_PARTICLE_COUNT,
00504:         RHYTHM_DUST_LIFETIME,
00505:         RHYTHM_PARTICLE_SIZE_MIN * 0.72,
00506:         0.035,
00507:         0.12,
00508:         0.42,
00509:         0.24,
00510:         2,
00511:         25,
00512:     )
00513:     _, streak_settings = configure_particle_system(
00514:         streak_emitter,
00515:         "HighStreakParticleSystem",
00516:         streak_obj,
00517:         RHYTHM_STREAK_PARTICLE_COUNT,
00518:         max(42, int(RHYTHM_PARTICLE_LIFETIME * 0.70)),
00519:         RHYTHM_PARTICLE_SIZE_MIN * 0.95,
00520:         0.30,
00521:         0.55,
00522:         0.06,
00523:         0.08,
00524:         1,
00525:         12,
00526:     )
00527:     letter_settings = []
00528:     if letter_emitter is not None:
00529:         per_letter_count = max(8, int(ALBUM_LETTER_PARTICLE_COUNT / max(1, len(letter_sources))))
00530:         for idx, letter in enumerate(letter_sources):
00531:             _, settings = configure_particle_system(
00532:                 letter_emitter,
00533:                 f"AlbumLetterParticleSystem_{idx:02d}",
00534:                 letter["object"],
00535:                 per_letter_count,
00536:                 ALBUM_LETTER_PARTICLE_LIFETIME,
00537:                 ALBUM_LETTER_PARTICLE_SIZE_MIN,
00538:                 0.16,
00539:                 0.32,
00540:                 0.18,
00541:                 0.16,
00542:                 1,
00543:                 10,
00544:             )
00545:             letter_settings.append(settings)
00546: 
00547:     systems = [
00548:         {
00549:             "mode": "pulse",
00550:             "emitter": pulse_emitter,
00551:             "settings": pulse_settings,
00552:             "material": spark_mat,
00553:             "emission_socket": spark_emit,
00554:             "base_location": pulse_emitter.location.copy(),
00555:             "base_rotation": pulse_emitter.rotation_euler.copy(),
00556:             "base_scale": pulse_emitter.scale.copy(),
00557:             "phase": 0.0,
00558:         },
00559:         {
00560:             "mode": "dust",
00561:             "emitter": dust_emitter,
00562:             "settings": dust_settings,
00563:             "material": dust_mat,
00564:             "emission_socket": dust_emit,
00565:             "base_location": dust_emitter.location.copy(),
00566:             "base_rotation": dust_emitter.rotation_euler.copy(),
00567:             "base_scale": dust_emitter.scale.copy(),
00568:             "phase": 1.7,
00569:         },
00570:         {
00571:             "mode": "streak",
00572:             "emitter": streak_emitter,
00573:             "settings": streak_settings,
00574:             "material": streak_mat,
00575:             "emission_socket": streak_emit,
00576:             "base_location": streak_emitter.location.copy(),
00577:             "base_rotation": streak_emitter.rotation_euler.copy(),
00578:             "base_scale": streak_emitter.scale.copy(),
00579:             "phase": 3.1,
00580:         },
00581:     ]
00582: 
00583:     if letter_emitter is not None and letter_settings:
00584:         systems.append({
00585:             "mode": "letters",
00586:             "emitter": letter_emitter,
00587:             "settings": letter_settings[0],
00588:             "settings_list": letter_settings,
00589:             "material": None,
00590:             "emission_socket": None,
00591:             "base_location": letter_emitter.location.copy(),
00592:             "base_rotation": letter_emitter.rotation_euler.copy(),
00593:             "base_scale": letter_emitter.scale.copy(),
00594:             "phase": 4.4,
00595:             "letter_root": letter_root,
00596:             "letter_sources": letter_sources,
00597:         })
00598: 
00599:     return systems
00600: 
00601: 
00602: def create_physics_accents(parent=None):
00603:     floor = bpy.data.objects.get("PeaceFloor")
00604:     invisible_floor = bpy.data.objects.get("InvisibleParticleFloor")
00605:     add_particle_collision(floor)
00606:     add_particle_collision(invisible_floor)
00607:     rhythm_particles = create_rhythm_particle_physics(parent=parent)
00608: 
00609:     if not USE_PHYSICS_ACCENTS:
00610:         return {
00611:             "accents": [],
00612:             "force_obj": None,
00613:             "turb_obj": None,
00614:             "vortex_obj": None,
```
