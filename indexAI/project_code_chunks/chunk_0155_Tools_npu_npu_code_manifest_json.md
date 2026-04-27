# Project Code Chunk 155/212

- File: `Tools/npu/npu_code_manifest.json`
- Part: `8`
- Lines: `2283-2669`

## Content
```json
02283:               "value"
02284:             ],
02285:             "async": false
02286:           },
02287:           {
02288:             "name": "set_input_node",
02289:             "line": 169,
02290:             "args": [
02291:               "material_name",
02292:               "node_name",
02293:               "input_name",
02294:               "value"
02295:             ],
02296:             "async": false
02297:           },
02298:           {
02299:             "name": "keyframe_socket",
02300:             "line": 180,
02301:             "args": [
02302:               "socket",
02303:               "frame"
02304:             ],
02305:             "async": false
02306:           },
02307:           {
02308:             "name": "get_scene_compositor_tree",
02309:             "line": 186,
02310:             "args": [
02311:               "scene"
02312:             ],
02313:             "async": false
02314:           },
02315:           {
02316:             "name": "clamp_value",
02317:             "line": 194,
02318:             "args": [
02319:               "value",
02320:               "min_value",
02321:               "max_value"
02322:             ],
02323:             "async": false
02324:           },
02325:           {
02326:             "name": "normalize_runtime_profile",
02327:             "line": 198,
02328:             "args": [
02329:               "profile"
02330:             ],
02331:             "async": false
02332:           },
02333:           {
02334:             "name": "runtime_profile_label",
02335:             "line": 244,
02336:             "args": [
02337:               "profile"
02338:             ],
02339:             "async": false
02340:           },
02341:           {
02342:             "name": "apply_runtime_profile",
02343:             "line": 257,
02344:             "args": [
02345:               "context",
02346:               "profile"
02347:             ],
02348:             "async": false
02349:           },
02350:           {
02351:             "name": "all_particle_settings",
02352:             "line": 442,
02353:             "args": [],
02354:             "async": false
02355:           },
02356:           {
02357:             "name": "apply_tuning",
02358:             "line": 454,
02359:             "args": [
02360:               "context",
02361:               "insert_keyframes"
02362:             ],
02363:             "async": false
02364:           },
02365:           {
02366:             "name": "scale_fcurve_values",
02367:             "line": 669,
02368:             "args": [
02369:               "idblock",
02370:               "predicate",
02371:               "factor"
02372:             ],
02373:             "async": false
02374:           },
02375:           {
02376:             "name": "scale_full_animation",
02377:             "line": 685,
02378:             "args": [
02379:               "context"
02380:             ],
02381:             "async": false
02382:           },
02383:           {
02384:             "name": "preset_data",
02385:             "line": 721,
02386:             "args": [
02387:               "settings"
02388:             ],
02389:             "async": false
02390:           },
02391:           {
02392:             "name": "load_preset_data",
02393:             "line": 764,
02394:             "args": [
02395:               "settings",
02396:               "data"
02397:             ],
02398:             "async": false
02399:           },
02400:           {
02401:             "name": "register",
02402:             "line": 1239,
02403:             "args": [],
02404:             "async": false
02405:           },
02406:           {
02407:             "name": "unregister",
02408:             "line": 1254,
02409:             "args": [],
02410:             "async": false
02411:           }
02412:         ],
02413:         "classes": [
02414:           {
02415:             "name": "ST_TuningSettings",
02416:             "line": 770,
02417:             "methods": []
02418:           },
02419:           {
02420:             "name": "ST_OT_apply_tuning",
02421:             "line": 822,
02422:             "methods": [
02423:               {
02424:                 "name": "execute",
02425:                 "line": 827
02426:               }
02427:             ]
02428:           },
02429:           {
02430:             "name": "ST_OT_keyframe_tuning",
02431:             "line": 833,
02432:             "methods": [
02433:               {
02434:                 "name": "execute",
02435:                 "line": 838
02436:               }
02437:             ]
02438:           },
02439:           {
02440:             "name": "ST_OT_scale_animation",
02441:             "line": 844,
02442:             "methods": [
02443:               {
02444:                 "name": "execute",
02445:                 "line": 849
02446:               }
02447:             ]
02448:           },
02449:           {
02450:             "name": "ST_OT_apply_runtime_profile",
02451:             "line": 855,
02452:             "methods": [
02453:               {
02454:                 "name": "execute",
02455:                 "line": 863
02456:               }
02457:             ]
02458:           },
02459:           {
02460:             "name": "ST_OT_hot_update_scene",
02461:             "line": 871,
02462:             "methods": [
02463:               {
02464:                 "name": "execute",
02465:                 "line": 878
02466:               }
02467:             ]
02468:           },
02469:           {
02470:             "name": "ST_OT_rebuild_restart_check",
02471:             "line": 895,
02472:             "methods": [
02473:               {
02474:                 "name": "execute",
02475:                 "line": 900
02476:               }
02477:             ]
02478:           },
02479:           {
02480:             "name": "ST_OT_optimizer_check",
02481:             "line": 920,
02482:             "methods": [
02483:               {
02484:                 "name": "execute",
02485:                 "line": 925
02486:               }
02487:             ]
02488:           },
02489:           {
02490:             "name": "ST_OT_load_image_sequence",
02491:             "line": 943,
02492:             "methods": [
02493:               {
02494:                 "name": "execute",
02495:                 "line": 948
02496:               }
02497:             ]
02498:           },
02499:           {
02500:             "name": "ST_OT_encode_ffmpeg",
02501:             "line": 965,
02502:             "methods": [
02503:               {
02504:                 "name": "execute",
02505:                 "line": 970
02506:               }
02507:             ]
02508:           },
02509:           {
02510:             "name": "ST_OT_encode_ffmpeg_shell",
02511:             "line": 987,
02512:             "methods": [
02513:               {
02514:                 "name": "execute",
02515:                 "line": 992
02516:               }
02517:             ]
02518:           },
02519:           {
02520:             "name": "ST_OT_save_preset",
02521:             "line": 1016,
02522:             "methods": [
02523:               {
02524:                 "name": "execute",
02525:                 "line": 1020
02526:               }
02527:             ]
02528:           },
02529:           {
02530:             "name": "ST_OT_load_preset",
02531:             "line": 1027,
02532:             "methods": [
02533:               {
02534:                 "name": "execute",
02535:                 "line": 1031
02536:               }
02537:             ]
02538:           },
02539:           {
02540:             "name": "ST_OT_open_guide_text",
02541:             "line": 1043,
02542:             "methods": [
02543:               {
02544:                 "name": "execute",
02545:                 "line": 1047
02546:               }
02547:             ]
02548:           },
02549:           {
02550:             "name": "ST_OT_select_group",
02551:             "line": 1062,
02552:             "methods": [
02553:               {
02554:                 "name": "execute",
02555:                 "line": 1068
02556:               }
02557:             ]
02558:           },
02559:           {
02560:             "name": "ST_PT_tuning_panel",
02561:             "line": 1098,
02562:             "methods": [
02563:               {
02564:                 "name": "draw",
02565:                 "line": 1105
02566:               }
02567:             ]
02568:           }
02569:         ],
02570:         "assignments": [
02571:           "bl_info",
02572:           "SCRIPT_DIR",
02573:           "PRESET_PATH",
02574:           "GUIDE_PATH",
02575:           "HOT_UPDATE_PATH",
02576:           "ENCODE_SEQUENCE_PATH",
02577:           "ENCODE_FFMPEG_PATH",
02578:           "classes"
02579:         ]
02580:       }
02581:     },
02582:     {
02583:       "file": "Scripting/v61b/hot_update_scene_v61b.py",
02584:       "exists": true,
02585:       "suffix": ".py",
02586:       "lines": 64,
02587:       "chars": 1475,
02588:       "sha256": "e11a0f377365de65b0fb38a393fb6b3259e2a7afe398455cd8f47ca5d2ac5437",
02589:       "symbols": {
02590:         "imports": [
02591:           "sys",
02592:           "from pathlib import Path",
02593:           "bpy"
02594:         ],
02595:         "functions": [
02596:           {
02597:             "name": "resolve_script_dir",
02598:             "line": 7,
02599:             "args": [],
02600:             "async": false
02601:           },
02602:           {
02603:             "name": "drop_hotpatch_cache",
02604:             "line": 38,
02605:             "args": [],
02606:             "async": false
02607:           },
02608:           {
02609:             "name": "main",
02610:             "line": 53,
02611:             "args": [],
02612:             "async": false
02613:           }
02614:         ],
02615:         "classes": [],
02616:         "assignments": [
02617:           "SCRIPT_DIR"
02618:         ]
02619:       }
02620:     },
02621:     {
02622:       "file": "Scripting/v61b/encode_image_sequence_v61b.py",
02623:       "exists": true,
02624:       "suffix": ".py",
02625:       "lines": 396,
02626:       "chars": 11882,
02627:       "sha256": "f10f55d9f550c7124b46cf897dec2602b653ec62358d3c1f885a20ca149fe384",
02628:       "symbols": {
02629:         "imports": [
02630:           "re",
02631:           "sys",
02632:           "from pathlib import Path",
02633:           "bpy",
02634:           "config"
02635:         ],
02636:         "functions": [
02637:           {
02638:             "name": "resolve_script_dir",
02639:             "line": 8,
02640:             "args": [],
02641:             "async": false
02642:           },
02643:           {
02644:             "name": "extract_frame_number",
02645:             "line": 83,
02646:             "args": [
02647:               "path"
02648:             ],
02649:             "async": false
02650:           },
02651:           {
02652:             "name": "sorted_frame_files",
02653:             "line": 90,
02654:             "args": [],
02655:             "async": false
02656:           },
02657:           {
02658:             "name": "contiguous_frame_files",
02659:             "line": 116,
02660:             "args": [
02661:               "frame_files"
02662:             ],
02663:             "async": false
02664:           },
02665:           {
02666:             "name": "get_sequence_collection",
02667:             "line": 143,
02668:             "args": [
02669:               "editor"
```
