# Project Code Chunk 152/212

- File: `Tools/npu/npu_code_manifest.json`
- Part: `5`
- Lines: `1382-1633`

## Content
```json
01382:           "from atmosphere_setup import create_hero_aura, create_energy_rings, create_energy_ribbons, create_variants, create_atmosphere_cube, create_mist_particles",
01383:           "from physics_setup import create_physics_accents",
01384:           "from animation import animate_scene",
01385:           "from spaziotempo.core.collections import classify_scene_objects, compact_structure_summary"
01386:         ],
01387:         "functions": [
01388:           {
01389:             "name": "register_tuning_panel",
01390:             "line": 79,
01391:             "args": [],
01392:             "async": false
01393:           },
01394:           {
01395:             "name": "classify_project_structure",
01396:             "line": 89,
01397:             "args": [
01398:               "scene"
01399:             ],
01400:             "async": false
01401:           },
01402:           {
01403:             "name": "print_summary",
01404:             "line": 100,
01405:             "args": [
01406:               "scene",
01407:               "analysis_file",
01408:               "hero_asset",
01409:               "secondary_asset",
01410:               "audio_file",
01411:               "fps",
01412:               "frame_count",
01413:               "elapsed"
01414:             ],
01415:             "async": false
01416:           },
01417:           {
01418:             "name": "main",
01419:             "line": 125,
01420:             "args": [],
01421:             "async": false
01422:           }
01423:         ],
01424:         "classes": [],
01425:         "assignments": [
01426:           "SCRIPT_DIR",
01427:           "reload_modules",
01428:           "reload_prefixes"
01429:         ]
01430:       }
01431:     },
01432:     {
01433:       "file": "Scripting/v61b/animation.py",
01434:       "exists": true,
01435:       "suffix": ".py",
01436:       "lines": 1080,
01437:       "chars": 50253,
01438:       "sha256": "8e08e656c5fdf65cf95d2d6c4c24df4b5d2e5b17ea47f7ab7b12034f970461ce",
01439:       "symbols": {
01440:         "imports": [
01441:           "math",
01442:           "from config import HERO_SCALE_MIN, HERO_SCALE_MAX, HERO_BOUNCE_Z, HERO_ROT_Z, HERO_ROT_X, HERO_ROT_Y, HERO_DRIFT_X, HERO_DRIFT_Y, HERO_ORBIT_X, HERO_ORBIT_Y, HERO_BEAT_TWIST_Z, HERO_ONSET_SHAKE, HERO_DEFORM_STRENGTH_MIN, HERO_DEFORM_STRENGTH_MAX, HERO_DEFORM_DETAIL_STRENGTH_MAX, HERO_DEFORM_WAVE_HEIGHT_MAX, HERO_DEFORM_TWIST_MAX, HERO_DEFORM_CONTROLLER_RADIUS, HERO_DEFORM_KEYFRAME_STEP, HERO_MATERIAL_EMISSION_MIN, HERO_MATERIAL_EMISSION_MAX, HERO_MATERIAL_SELF_LIGHT_MIN, HERO_MATERIAL_SELF_LIGHT_MAX, HERO_MATERIAL_BUMP_MIN, HERO_MATERIAL_BUMP_MAX, HERO_MATERIAL_ROUGHNESS_MIN, HERO_MATERIAL_ROUGHNESS_MAX, HERO_MATERIAL_NOISE_SCALE_MIN, HERO_MATERIAL_NOISE_SCALE_MAX, HERO_MATERIAL_MAPPING_DRIFT, AURA_DEFORM_KEYFRAME_STEP, AURA_DEFORM_FIELD_DRIFT, AURA_DEFORM_FIELD_SCALE, SECONDARY_SCALE_MIN, SECONDARY_SCALE_MAX, SECONDARY_BOUNCE_Z, SECONDARY_DRIFT_X, SECONDARY_DRIFT_Y, SECONDARY_ROT_Z, SECONDARY_ROT_X, CAMERA_BEAT_BUMP_Z, CAMERA_BEAT_BUMP_Y, CAMERA_ORBIT_AMOUNT, CAMERA_PUSH_AMOUNT, CAMERA_VERTICAL_SWAY, LIGHT_ENERGY_MIN, LIGHT_ENERGY_MAX, PHYSICS_ACCENT_EMISSION_MIN, PHYSICS_ACCENT_EMISSION_MAX, PHYSICS_ACCENT_MIX_MIN, PHYSICS_ACCENT_MIX_MAX, PHYSICS_ATOM_ORBIT_SPEED_MIN, PHYSICS_ATOM_ORBIT_AUDIO_SPEED, PHYSICS_ATOM_ORBIT_RADIUS_PULSE, PHYSICS_ATOM_ORBIT_HEIGHT_SWAY, PHYSICS_ATOM_MICRO_WOBBLE, COMPOSITOR_GLARE_THRESHOLD_MIN, COMPOSITOR_GLARE_THRESHOLD_MAX, COMPOSITOR_LENS_DISTORT_MIN, COMPOSITOR_LENS_DISTORT_MAX, COMPOSITOR_LENS_DISPERSION_MIN, COMPOSITOR_LENS_DISPERSION_MAX, FIELD_STRENGTH_MIN, FIELD_STRENGTH_MAX, HERO_GRAVITY_STRENGTH_MIN, HERO_GRAVITY_STRENGTH_MAX, TURB_STRENGTH_MIN, TURB_STRENGTH_MAX, VORTEX_STRENGTH_MIN, VORTEX_STRENGTH_MAX, RHYTHM_PARTICLE_SIZE_MIN, RHYTHM_PARTICLE_SIZE_MAX, RHYTHM_PARTICLE_NORMAL_MIN, RHYTHM_PARTICLE_NORMAL_MAX, RHYTHM_PARTICLE_TANGENT_MIN, RHYTHM_PARTICLE_TANGENT_MAX, RHYTHM_PARTICLE_BROWNIAN_MIN, RHYTHM_PARTICLE_BROWNIAN_MAX, RHYTHM_PARTICLE_EMIT_MIN, RHYTHM_PARTICLE_EMIT_MAX, RHYTHM_PARTICLE_KEYFRAME_STEP, ALBUM_LETTER_PARTICLE_SIZE_MIN, ALBUM_LETTER_PARTICLE_SIZE_MAX, ALBUM_LETTER_ROOT_SCALE_MIN, ALBUM_LETTER_ROOT_SCALE_MAX, BACKDROP_EMISSION_MIN, BACKDROP_EMISSION_MAX, BACKDROP_BREATHE_SCALE, MIST_FLOAT_AMPLITUDE, MIST_BEAT_BOOST",
01443:           "from fog_dynamics import animate_fog_frame",
01444:           "from scene_utils import set_linear_interpolation_idblock"
01445:         ],
01446:         "functions": [
01447:           {
01448:             "name": "keyframe_if_possible",
01449:             "line": 99,
01450:             "args": [
01451:               "idblock",
01452:               "data_path",
01453:               "frame"
01454:             ],
01455:             "async": false
01456:           },
01457:           {
01458:             "name": "get_scene_compositor_tree",
01459:             "line": 106,
01460:             "args": [
01461:               "scene"
01462:             ],
01463:             "async": false
01464:           },
01465:           {
01466:             "name": "rhythm_band_drive",
01467:             "line": 114,
01468:             "args": [
01469:               "band",
01470:               "response",
01471:               "low",
01472:               "mid",
01473:               "high",
01474:               "onset",
01475:               "beat",
01476:               "pulse",
01477:               "local_pulse"
01478:             ],
01479:             "async": false
01480:           },
01481:           {
01482:             "name": "animate_scene",
01483:             "line": 132,
01484:             "args": [
01485:               "scene",
01486:               "frames",
01487:               "camera",
01488:               "target",
01489:               "hero_asset",
01490:               "secondary_asset",
01491:               "aura_data",
01492:               "fog_controller",
01493:               "scene_base",
01494:               "lights",
01495:               "physics_data",
01496:               "mist_particles",
01497:               "variants",
01498:               "energy_rings",
01499:               "energy_ribbons"
01500:             ],
01501:             "async": false
01502:           }
01503:         ],
01504:         "classes": [],
01505:         "assignments": []
01506:       }
01507:     },
01508:     {
01509:       "file": "Scripting/v61b/materials.py",
01510:       "exists": true,
01511:       "suffix": ".py",
01512:       "lines": 658,
01513:       "chars": 23180,
01514:       "sha256": "073e38f04df3414be8fe87cc0a568ce396592e19553f991815cfb94c7b749577",
01515:       "symbols": {
01516:         "imports": [
01517:           "bpy",
01518:           "from config import PEACE_PALETTE, FOG_DENSITY_MIN, FOG_EMISSION_MIN, FOG_NOISE_SCALE_MIN, FOG_CLUMP_SCALE_MIN, FOG_CLUMP_RAMP_LOW_BASE, FOG_CLUMP_RAMP_HIGH_BASE, FOG_WAVE_SCALE_MIN, FOG_WAVE_DISTORTION_MIN, FOG_WAVE_WEIGHT_MIN, FOG_FILAMENT_ALPHA_MIN, FOG_FILAMENT_EMISSION_MIN, FOG_FILAMENT_NOISE_SCALE_MIN, FOG_FILAMENT_WAVE_SCALE_MIN, AURA_EMIT_MIN, RING_EMIT_MIN, RIBBON_EMIT_MIN, BACKDROP_EMISSION_MIN"
01519:         ],
01520:         "functions": [
01521:           {
01522:             "name": "build_reflective_floor_material",
01523:             "line": 25,
01524:             "args": [],
01525:             "async": false
01526:           },
01527:           {
01528:             "name": "build_invisible_surface_material",
01529:             "line": 67,
01530:             "args": [
01531:               "name"
01532:             ],
01533:             "async": false
01534:           },
01535:           {
01536:             "name": "build_soft_backdrop_material",
01537:             "line": 91,
01538:             "args": [],
01539:             "async": false
01540:           },
01541:           {
01542:             "name": "build_aura_material",
01543:             "line": 140,
01544:             "args": [],
01545:             "async": false
01546:           },
01547:           {
01548:             "name": "build_variant_material",
01549:             "line": 186,
01550:             "args": [
01551:               "name",
01552:               "color"
01553:             ],
01554:             "async": false
01555:           },
01556:           {
01557:             "name": "build_ring_material",
01558:             "line": 226,
01559:             "args": [
01560:               "name",
01561:               "color"
01562:             ],
01563:             "async": false
01564:           },
01565:           {
01566:             "name": "build_ribbon_material",
01567:             "line": 248,
01568:             "args": [
01569:               "name",
01570:               "color"
01571:             ],
01572:             "async": false
01573:           },
01574:           {
01575:             "name": "build_atmosphere_volume_material",
01576:             "line": 270,
01577:             "args": [],
01578:             "async": false
01579:           },
01580:           {
01581:             "name": "build_fog_filament_material",
01582:             "line": 478,
01583:             "args": [
01584:               "name"
01585:             ],
01586:             "async": false
01587:           },
01588:           {
01589:             "name": "build_mist_particle_material",
01590:             "line": 618,
01591:             "args": [
01592:               "name",
01593:               "color"
01594:             ],
01595:             "async": false
01596:           }
01597:         ],
01598:         "classes": [],
01599:         "assignments": []
01600:       }
01601:     },
01602:     {
01603:       "file": "Scripting/v61b/physics_setup.py",
01604:       "exists": true,
01605:       "suffix": ".py",
01606:       "lines": 738,
01607:       "chars": 23685,
01608:       "sha256": "15ccd171bf927564a01d46238dca9f9149d70198caf5cd7eb451733a5cbf2edf",
01609:       "symbols": {
01610:         "imports": [
01611:           "bpy",
01612:           "math",
01613:           "random",
01614:           "from config import USE_PHYSICS_ACCENTS, PHYSICS_ACCENT_COUNT, PRIMARY_BASE_Z, TURB_STRENGTH_MIN, VORTEX_STRENGTH_MIN, PHYSICS_ORBIT_RADIUS_MIN, PHYSICS_ORBIT_RADIUS_MAX, PHYSICS_ATOM_ORBIT_SPEED_MIN, PHYSICS_ATOM_ORBIT_SPEED_MAX, PHYSICS_ATOM_MICRO_WOBBLE, HERO_GRAVITY_STRENGTH_MIN, TETHER_SPRING_STIFFNESS, TETHER_SPRING_DAMPING, USE_RHYTHM_PARTICLE_PHYSICS, RHYTHM_PARTICLE_COUNT, RHYTHM_DUST_PARTICLE_COUNT, RHYTHM_STREAK_PARTICLE_COUNT, RHYTHM_PARTICLE_LIFETIME, RHYTHM_DUST_LIFETIME, RHYTHM_PARTICLE_EMITTER_RADIUS, RHYTHM_PARTICLE_EMITTER_Z, PARTICLE_SOURCE_LOCATION, RHYTHM_PARTICLE_SOURCE_RADIUS, RHYTHM_PARTICLE_SIZE_MIN, RHYTHM_PARTICLE_NORMAL_MIN, RHYTHM_PARTICLE_TANGENT_MIN, RHYTHM_PARTICLE_BROWNIAN_MIN, USE_ALBUM_LETTER_PARTICLES, ALBUM_PARTICLE_TEXT, ALBUM_LETTER_PARTICLE_COUNT, ALBUM_LETTER_PARTICLE_LIFETIME, ALBUM_LETTER_SOURCE_SIZE, ALBUM_LETTER_EXTRUDE, ALBUM_LETTER_EMISSION_STRENGTH, ALBUM_LETTER_PARTICLE_SIZE_MIN, PHYSICS_ACCENT_EMISSION_MIN, PHYSICS_ACCENT_MIX_MIN, PALETTE_LIST, PEACE_PALETTE",
01615:           "from materials import build_variant_material",
01616:           "from scene_utils import deselect_all, safe_active"
01617:         ],
01618:         "functions": [
01619:           {
01620:             "name": "set_if_available",
01621:             "line": 50,
01622:             "args": [
01623:               "obj",
01624:               "attr",
01625:               "value"
01626:             ],
01627:             "async": false
01628:           },
01629:           {
01630:             "name": "build_particle_emission_material",
01631:             "line": 60,
01632:             "args": [
01633:               "name",
```
