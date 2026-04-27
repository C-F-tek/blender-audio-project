# Project Code Chunk 149/212

- File: `Tools/npu/npu_code_manifest.json`
- Part: `2`
- Lines: `384-752`

## Content
```json
00384:           "from __future__ import annotations",
00385:           "from pathlib import Path",
00386:           "json",
00387:           "os",
00388:           "shutil",
00389:           "subprocess",
00390:           "time",
00391:           "urllib.error",
00392:           "urllib.request"
00393:         ],
00394:         "functions": [
00395:           {
00396:             "name": "normalize_base_url",
00397:             "line": 13,
00398:             "args": [
00399:               "value"
00400:             ],
00401:             "async": false
00402:           },
00403:           {
00404:             "name": "ollama_home",
00405:             "line": 24,
00406:             "args": [],
00407:             "async": false
00408:           },
00409:           {
00410:             "name": "manifest_root",
00411:             "line": 31,
00412:             "args": [],
00413:             "async": false
00414:           },
00415:           {
00416:             "name": "find_ollama_exe",
00417:             "line": 36,
00418:             "args": [],
00419:             "async": false
00420:           },
00421:           {
00422:             "name": "_json_request",
00423:             "line": 74,
00424:             "args": [
00425:               "base_url",
00426:               "path",
00427:               "payload",
00428:               "timeout"
00429:             ],
00430:             "async": false
00431:           },
00432:           {
00433:             "name": "is_server_ready",
00434:             "line": 91,
00435:             "args": [
00436:               "base_url",
00437:               "timeout"
00438:             ],
00439:             "async": false
00440:           },
00441:           {
00442:             "name": "list_models",
00443:             "line": 99,
00444:             "args": [
00445:               "base_url"
00446:             ],
00447:             "async": false
00448:           },
00449:           {
00450:             "name": "list_models_from_disk",
00451:             "line": 110,
00452:             "args": [],
00453:             "async": false
00454:           },
00455:           {
00456:             "name": "start_server",
00457:             "line": 139,
00458:             "args": [
00459:               "ollama_exe",
00460:               "base_url",
00461:               "startup_timeout"
00462:             ],
00463:             "async": false
00464:           },
00465:           {
00466:             "name": "choose_model",
00467:             "line": 160,
00468:             "args": [
00469:               "preferred_model",
00470:               "available_models"
00471:             ],
00472:             "async": false
00473:           },
00474:           {
00475:             "name": "strip_json_fence",
00476:             "line": 175,
00477:             "args": [
00478:               "text"
00479:             ],
00480:             "async": false
00481:           },
00482:           {
00483:             "name": "parse_json_response",
00484:             "line": 187,
00485:             "args": [
00486:               "text"
00487:             ],
00488:             "async": false
00489:           }
00490:         ],
00491:         "classes": [
00492:           {
00493:             "name": "OllamaModelManager",
00494:             "line": 199,
00495:             "methods": [
00496:               {
00497:                 "name": "__init__",
00498:                 "line": 200
00499:               },
00500:               {
00501:                 "name": "generate",
00502:                 "line": 214
00503:               },
00504:               {
00505:                 "name": "close",
00506:                 "line": 240
00507:               },
00508:               {
00509:                 "name": "__enter__",
00510:                 "line": 246
00511:               },
00512:               {
00513:                 "name": "__exit__",
00514:                 "line": 249
00515:               }
00516:             ]
00517:           },
00518:           {
00519:             "name": "OllamaSession",
00520:             "line": 253,
00521:             "methods": [
00522:               {
00523:                 "name": "__init__",
00524:                 "line": 254
00525:               },
00526:               {
00527:                 "name": "start",
00528:                 "line": 275
00529:               },
00530:               {
00531:                 "name": "generate",
00532:                 "line": 291
00533:               },
00534:               {
00535:                 "name": "unload_model",
00536:                 "line": 308
00537:               },
00538:               {
00539:                 "name": "close",
00540:                 "line": 336
00541:               },
00542:               {
00543:                 "name": "__enter__",
00544:                 "line": 347
00545:               },
00546:               {
00547:                 "name": "__exit__",
00548:                 "line": 350
00549:               }
00550:             ]
00551:           }
00552:         ],
00553:         "assignments": [
00554:           "DEFAULT_BASE_URL",
00555:           "DEFAULT_MODELS"
00556:         ]
00557:       }
00558:     },
00559:     {
00560:       "file": "Tools/npu/build_blender_manual_context.py",
00561:       "exists": true,
00562:       "suffix": ".py",
00563:       "lines": 327,
00564:       "chars": 10493,
00565:       "sha256": "5516f84a1f112607a51f93aa7dbe52631a7e834353a0b98c71706e33b152719c",
00566:       "symbols": {
00567:         "imports": [
00568:           "from __future__ import annotations",
00569:           "from pathlib import Path",
00570:           "from html.parser import HTMLParser",
00571:           "argparse",
00572:           "hashlib",
00573:           "json",
00574:           "re",
00575:           "from datetime import datetime"
00576:         ],
00577:         "functions": [
00578:           {
00579:             "name": "sha256_text",
00580:             "line": 95,
00581:             "args": [
00582:               "text"
00583:             ],
00584:             "async": false
00585:           },
00586:           {
00587:             "name": "rel",
00588:             "line": 99,
00589:             "args": [
00590:               "path"
00591:             ],
00592:             "async": false
00593:           },
00594:           {
00595:             "name": "slug",
00596:             "line": 106,
00597:             "args": [
00598:               "value"
00599:             ],
00600:             "async": false
00601:           },
00602:           {
00603:             "name": "extract_text",
00604:             "line": 110,
00605:             "args": [
00606:               "path"
00607:             ],
00608:             "async": false
00609:           },
00610:           {
00611:             "name": "score_text",
00612:             "line": 119,
00613:             "args": [
00614:               "path",
00615:               "text"
00616:             ],
00617:             "async": false
00618:           },
00619:           {
00620:             "name": "score_path",
00621:             "line": 124,
00622:             "args": [
00623:               "path"
00624:             ],
00625:             "async": false
00626:           },
00627:           {
00628:             "name": "split_text",
00629:             "line": 144,
00630:             "args": [
00631:               "text",
00632:               "max_chars"
00633:             ],
00634:             "async": false
00635:           },
00636:           {
00637:             "name": "ensure_manual_root",
00638:             "line": 161,
00639:             "args": [],
00640:             "async": false
00641:           },
00642:           {
00643:             "name": "source_group",
00644:             "line": 167,
00645:             "args": [
00646:               "path"
00647:             ],
00648:             "async": false
00649:           },
00650:           {
00651:             "name": "iter_manual_files",
00652:             "line": 175,
00653:             "args": [
00654:               "manual_root"
00655:             ],
00656:             "async": false
00657:           },
00658:           {
00659:             "name": "build_manual_context",
00660:             "line": 195,
00661:             "args": [
00662:               "limit_files",
00663:               "manual_root"
00664:             ],
00665:             "async": false
00666:           },
00667:           {
00668:             "name": "main",
00669:             "line": 296,
00670:             "args": [],
00671:             "async": false
00672:           }
00673:         ],
00674:         "classes": [
00675:           {
00676:             "name": "TextExtractor",
00677:             "line": 62,
00678:             "methods": [
00679:               {
00680:                 "name": "__init__",
00681:                 "line": 63
00682:               },
00683:               {
00684:                 "name": "handle_starttag",
00685:                 "line": 68
00686:               },
00687:               {
00688:                 "name": "handle_endtag",
00689:                 "line": 74
00690:               },
00691:               {
00692:                 "name": "handle_data",
00693:                 "line": 80
00694:               },
00695:               {
00696:                 "name": "text",
00697:                 "line": 88
00698:               }
00699:             ]
00700:           }
00701:         ],
00702:         "assignments": [
00703:           "ROOT",
00704:           "MANUAL_ROOT",
00705:           "LEGACY_MANUAL_DIR",
00706:           "MANUAL_README",
00707:           "OUT_DIR",
00708:           "CHUNK_DIR",
00709:           "OUT_INDEX",
00710:           "OUT_MANIFEST",
00711:           "MAX_CHARS",
00712:           "TEXT_EXTENSIONS",
00713:           "HTML_EXTENSIONS",
00714:           "KEYWORDS",
00715:           "README_TEXT"
00716:         ]
00717:       }
00718:     },
00719:     {
00720:       "file": "Tools/npu/run_dual_ai_pipeline.py",
00721:       "exists": true,
00722:       "suffix": ".py",
00723:       "lines": 1705,
00724:       "chars": 72162,
00725:       "sha256": "a6a3d187992b5d66d4d8edb064e2a04cc303c5f685b05b0a698efd953f636bbb",
00726:       "symbols": {
00727:         "imports": [
00728:           "from __future__ import annotations",
00729:           "from pathlib import Path",
00730:           "argparse",
00731:           "json",
00732:           "subprocess",
00733:           "from datetime import datetime",
00734:           "from typing import Any",
00735:           "from build_music_context import build_music_context",
00736:           "from build_npu_code_context import main",
00737:           "from build_blender_manual_context import build_manual_context",
00738:           "from build_ai_service_packet import build_ai_service_packet, slugify",
00739:           "from build_project_ai_index import PROJECT_INDEX_MD, PROJECT_MANIFEST_JSON, build_project_ai_index",
00740:           "from npu_runtime import DEFAULT_MODEL_DIR, DEFAULT_NPU_PYTHON, npu_preflight, write_npu_preflight_report",
00741:           "from ollama_runtime import OllamaModelManager, parse_json_response",
00742:           "from run_ollama_music_agent import build_prompt",
00743:           "from run_ollama_music_agent import markdown_from_insights"
00744:         ],
00745:         "functions": [
00746:           {
00747:             "name": "read_text",
00748:             "line": 53,
00749:             "args": [
00750:               "path"
00751:             ],
00752:             "async": false
```
