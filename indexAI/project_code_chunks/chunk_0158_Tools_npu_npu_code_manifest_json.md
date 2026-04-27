# Project Code Chunk 158/212

- File: `Tools/npu/npu_code_manifest.json`
- Part: `11`
- Lines: `3390-3759`

## Content
```json
03390:             "async": false
03391:           },
03392:           {
03393:             "name": "get_or_store_float",
03394:             "line": 84,
03395:             "args": [
03396:               "obj",
03397:               "key",
03398:               "default"
03399:             ],
03400:             "async": false
03401:           },
03402:           {
03403:             "name": "atom_center",
03404:             "line": 90,
03405:             "args": [],
03406:             "async": false
03407:           },
03408:           {
03409:             "name": "find_or_create_force_object",
03410:             "line": 100,
03411:             "args": [
03412:               "name",
03413:               "effector_type",
03414:               "location"
03415:             ],
03416:             "async": false
03417:           },
03418:           {
03419:             "name": "update_central_fields",
03420:             "line": 121,
03421:             "args": [
03422:               "frames",
03423:               "center"
03424:             ],
03425:             "async": false
03426:           },
03427:           {
03428:             "name": "update_physics_accents",
03429:             "line": 175,
03430:             "args": [
03431:               "frames"
03432:             ],
03433:             "async": false
03434:           }
03435:         ],
03436:         "classes": [],
03437:         "assignments": [
03438:           "PHYSICS_ACCENT_EMISSION_MIN",
03439:           "PHYSICS_ACCENT_EMISSION_MAX",
03440:           "PHYSICS_ACCENT_MIX_MIN",
03441:           "PHYSICS_ACCENT_MIX_MAX",
03442:           "PRIMARY_BASE_Z",
03443:           "PHYSICS_ORBIT_RADIUS_MIN",
03444:           "PHYSICS_ORBIT_RADIUS_MAX",
03445:           "PHYSICS_ATOM_ORBIT_SPEED_MIN",
03446:           "PHYSICS_ATOM_ORBIT_SPEED_MAX",
03447:           "PHYSICS_ATOM_ORBIT_AUDIO_SPEED",
03448:           "PHYSICS_ATOM_ORBIT_RADIUS_PULSE",
03449:           "PHYSICS_ATOM_ORBIT_HEIGHT_SWAY",
03450:           "PHYSICS_ATOM_MICRO_WOBBLE",
03451:           "HERO_GRAVITY_STRENGTH_MIN",
03452:           "HERO_GRAVITY_STRENGTH_MAX",
03453:           "TURB_STRENGTH_MIN",
03454:           "TURB_STRENGTH_MAX",
03455:           "VORTEX_STRENGTH_MIN",
03456:           "VORTEX_STRENGTH_MAX"
03457:         ]
03458:       }
03459:     },
03460:     {
03461:       "file": "Scripting/v61b/hotpatch/common.py",
03462:       "exists": true,
03463:       "suffix": ".py",
03464:       "lines": 92,
03465:       "chars": 2201,
03466:       "sha256": "81758e52dae24735b45e08524292be5d1a6d0f820c15526514518e1e2e5c6662",
03467:       "symbols": {
03468:         "imports": [
03469:           "json",
03470:           "from pathlib import Path",
03471:           "bpy",
03472:           "config"
03473:         ],
03474:         "functions": [
03475:           {
03476:             "name": "cfg_value",
03477:             "line": 9,
03478:             "args": [
03479:               "name",
03480:               "default"
03481:             ],
03482:             "async": false
03483:           },
03484:           {
03485:             "name": "load_analysis",
03486:             "line": 32,
03487:             "args": [],
03488:             "async": false
03489:           },
03490:           {
03491:             "name": "iter_objects_prefix",
03492:             "line": 42,
03493:             "args": [
03494:               "prefix"
03495:             ],
03496:             "async": false
03497:           },
03498:           {
03499:             "name": "remove_objects_with_prefixes",
03500:             "line": 46,
03501:             "args": [
03502:               "prefixes"
03503:             ],
03504:             "async": false
03505:           },
03506:           {
03507:             "name": "keyframe_if_possible",
03508:             "line": 56,
03509:             "args": [
03510:               "idblock",
03511:               "data_path",
03512:               "frame"
03513:             ],
03514:             "async": false
03515:           },
03516:           {
03517:             "name": "clear_animation",
03518:             "line": 63,
03519:             "args": [
03520:               "idblock"
03521:             ],
03522:             "async": false
03523:           },
03524:           {
03525:             "name": "get_node",
03526:             "line": 72,
03527:             "args": [
03528:               "material",
03529:               "node_name"
03530:             ],
03531:             "async": false
03532:           },
03533:           {
03534:             "name": "socket_by_name",
03535:             "line": 78,
03536:             "args": [
03537:               "node",
03538:               "socket_name",
03539:               "is_output"
03540:             ],
03541:             "async": false
03542:           },
03543:           {
03544:             "name": "store_base_vector",
03545:             "line": 88,
03546:             "args": [
03547:               "obj",
03548:               "key",
03549:               "value"
03550:             ],
03551:             "async": false
03552:           }
03553:         ],
03554:         "classes": [],
03555:         "assignments": [
03556:           "ANALYSIS_JSON_PATH",
03557:           "OUTPUT_MP4",
03558:           "PALETTE_LIST"
03559:         ]
03560:       }
03561:     },
03562:     {
03563:       "file": "Scripting/v61b/hotpatch/diagnostics.py",
03564:       "exists": true,
03565:       "suffix": ".py",
03566:       "lines": 287,
03567:       "chars": 10043,
03568:       "sha256": "0c67d184cf13c5fb66ea91e3bcaa77312ecec4022985d7dd810a2d238f966092",
03569:       "symbols": {
03570:         "imports": [
03571:           "bpy",
03572:           "from common import ANALYSIS_JSON_PATH, cfg_value, load_analysis",
03573:           "from spaziotempo.core.registry import LAYER_ORDER, LAYER_SPECS, PROJECT_ROOT_COLLECTION"
03574:         ],
03575:         "functions": [
03576:           {
03577:             "name": "text_report",
03578:             "line": 17,
03579:             "args": [
03580:               "name",
03581:               "lines"
03582:             ],
03583:             "async": false
03584:           },
03585:           {
03586:             "name": "has_object",
03587:             "line": 24,
03588:             "args": [
03589:               "name"
03590:             ],
03591:             "async": false
03592:           },
03593:           {
03594:             "name": "count_objects",
03595:             "line": 28,
03596:             "args": [
03597:               "prefix"
03598:             ],
03599:             "async": false
03600:           },
03601:           {
03602:             "name": "collection_exists",
03603:             "line": 32,
03604:             "args": [
03605:               "name"
03606:             ],
03607:             "async": false
03608:           },
03609:           {
03610:             "name": "layer_collection_counts",
03611:             "line": 36,
03612:             "args": [],
03613:             "async": false
03614:           },
03615:           {
03616:             "name": "scene_frame_count",
03617:             "line": 45,
03618:             "args": [
03619:               "scene"
03620:             ],
03621:             "async": false
03622:           },
03623:           {
03624:             "name": "material_node_exists",
03625:             "line": 49,
03626:             "args": [
03627:               "node_name"
03628:             ],
03629:             "async": false
03630:           },
03631:           {
03632:             "name": "modifier_exists",
03633:             "line": 56,
03634:             "args": [
03635:               "mod_name"
03636:             ],
03637:             "async": false
03638:           },
03639:           {
03640:             "name": "point_cache_state",
03641:             "line": 64,
03642:             "args": [
03643:               "cache"
03644:             ],
03645:             "async": false
03646:           },
03647:           {
03648:             "name": "particle_cache_state",
03649:             "line": 72,
03650:             "args": [
03651:               "ps"
03652:             ],
03653:             "async": false
03654:           },
03655:           {
03656:             "name": "analyze_rebuild_need",
03657:             "line": 83,
03658:             "args": [],
03659:             "async": false
03660:           },
03661:           {
03662:             "name": "analyze_optimizer",
03663:             "line": 169,
03664:             "args": [],
03665:             "async": false
03666:           }
03667:         ],
03668:         "classes": [],
03669:         "assignments": [
03670:           "STRUCTURAL_OBJECTS"
03671:         ]
03672:       }
03673:     },
03674:     {
03675:       "file": "Scripting/v61b/hotpatch/fog_patch.py",
03676:       "exists": true,
03677:       "suffix": ".py",
03678:       "lines": 134,
03679:       "chars": 5066,
03680:       "sha256": "728d3daf653f3a0551843b26040422d0f14826005a8a0e7abb0cc5b7414d3df4",
03681:       "symbols": {
03682:         "imports": [
03683:           "bpy",
03684:           "from mathutils import Vector",
03685:           "from fog_dynamics import animate_fog_frame",
03686:           "from fog_filaments import ensure_fog_filaments",
03687:           "from materials import build_atmosphere_volume_material",
03688:           "from common import cfg_value, clear_animation, store_base_vector"
03689:         ],
03690:         "functions": [
03691:           {
03692:             "name": "find_or_create_fog_controller",
03693:             "line": 11,
03694:             "args": [
03695:               "cube"
03696:             ],
03697:             "async": false
03698:           },
03699:           {
03700:             "name": "ensure_fog_cube",
03701:             "line": 25,
03702:             "args": [],
03703:             "async": false
03704:           },
03705:           {
03706:             "name": "update_fog",
03707:             "line": 47,
03708:             "args": [
03709:               "frames"
03710:             ],
03711:             "async": false
03712:           }
03713:         ],
03714:         "classes": [],
03715:         "assignments": []
03716:       }
03717:     },
03718:     {
03719:       "file": "Scripting/v61b/hotpatch/hero_material_patch.py",
03720:       "exists": true,
03721:       "suffix": ".py",
03722:       "lines": 396,
03723:       "chars": 14403,
03724:       "sha256": "94be76940e0b8ef01d1dfd973d767f0cfdb1a398621a512c8810429940d4cfe7",
03725:       "symbols": {
03726:         "imports": [
03727:           "math",
03728:           "bpy",
03729:           "from common import cfg_value, clear_animation, keyframe_if_possible"
03730:         ],
03731:         "functions": [
03732:           {
03733:             "name": "find_principled_node",
03734:             "line": 28,
03735:             "args": [
03736:               "material"
03737:             ],
03738:             "async": false
03739:           },
03740:           {
03741:             "name": "get_node_input",
03742:             "line": 37,
03743:             "args": [
03744:               "node"
03745:             ],
03746:             "async": false
03747:           },
03748:           {
03749:             "name": "link_node_sockets",
03750:             "line": 46,
03751:             "args": [
03752:               "links",
03753:               "output_socket",
03754:               "input_socket",
03755:               "replace_existing"
03756:             ],
03757:             "async": false
03758:           },
03759:           {
```
