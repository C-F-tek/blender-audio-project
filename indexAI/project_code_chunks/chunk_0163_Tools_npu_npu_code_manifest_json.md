# Project Code Chunk 163/212

- File: `Tools/npu/npu_code_manifest.json`
- Part: `16`
- Lines: `5245-5607`

## Content
```json
05245:           "DUAL_BRIEF_MD",
05246:           "OLLAMA_INSIGHTS_JSON",
05247:           "OLLAMA_INSIGHTS_MD",
05248:           "NPU_TECH_MD",
05249:           "NPU_PREFLIGHT_JSON",
05250:           "IMPLEMENTATION_DRAFT_JSON",
05251:           "IMPLEMENTATION_SCRIPT",
05252:           "IMPLEMENTATION_NOTES",
05253:           "NPU_IMPLEMENTATION_NOTES"
05254:         ]
05255:       }
05256:     },
05257:     {
05258:       "file": "Tools/npu/run_npu_review.py",
05259:       "exists": true,
05260:       "suffix": ".py",
05261:       "lines": 566,
05262:       "chars": 18230,
05263:       "sha256": "d13f94b1d0c5c586cc63177f44f022f33f3e19a926fc675a1540e4d24cc524ed",
05264:       "symbols": {
05265:         "imports": [
05266:           "from __future__ import annotations",
05267:           "from pathlib import Path",
05268:           "argparse",
05269:           "from datetime import datetime"
05270:         ],
05271:         "functions": [
05272:           {
05273:             "name": "read_text",
05274:             "line": 21,
05275:             "args": [
05276:               "path"
05277:             ],
05278:             "async": false
05279:           },
05280:           {
05281:             "name": "read_text_limited",
05282:             "line": 25,
05283:             "args": [
05284:               "path",
05285:               "max_chars"
05286:             ],
05287:             "async": false
05288:           },
05289:           {
05290:             "name": "split_text",
05291:             "line": 34,
05292:             "args": [
05293:               "text",
05294:               "max_chars",
05295:               "overlap_chars"
05296:             ],
05297:             "async": false
05298:           },
05299:           {
05300:             "name": "load_context_chunks",
05301:             "line": 52,
05302:             "args": [
05303:               "context_path",
05304:               "chunk_dir",
05305:               "chunk_chars",
05306:               "overlap_chars",
05307:               "max_chunks"
05308:             ],
05309:             "async": false
05310:           },
05311:           {
05312:             "name": "fit_prompt",
05313:             "line": 78,
05314:             "args": [
05315:               "prefix",
05316:               "context",
05317:               "suffix",
05318:               "max_prompt_chars"
05319:             ],
05320:             "async": false
05321:           },
05322:           {
05323:             "name": "build_onepass_prompt",
05324:             "line": 92,
05325:             "args": [
05326:               "context",
05327:               "max_prompt_chars",
05328:               "domain"
05329:             ],
05330:             "async": false
05331:           },
05332:           {
05333:             "name": "build_chunk_prompt",
05334:             "line": 163,
05335:             "args": [
05336:               "title",
05337:               "index",
05338:               "total",
05339:               "context",
05340:               "max_prompt_chars",
05341:               "domain"
05342:             ],
05343:             "async": false
05344:           },
05345:           {
05346:             "name": "build_batch_reduce_prompt",
05347:             "line": 235,
05348:             "args": [
05349:               "batch_title",
05350:               "notes",
05351:               "max_prompt_chars",
05352:               "domain"
05353:             ],
05354:             "async": false
05355:           },
05356:           {
05357:             "name": "build_final_prompt",
05358:             "line": 274,
05359:             "args": [
05360:               "notes",
05361:               "max_prompt_chars",
05362:               "domain"
05363:             ],
05364:             "async": false
05365:           },
05366:           {
05367:             "name": "create_pipeline",
05368:             "line": 346,
05369:             "args": [
05370:               "model_dir",
05371:               "device",
05372:               "max_prompt_len",
05373:               "min_response_len"
05374:             ],
05375:             "async": false
05376:           },
05377:           {
05378:             "name": "create_ollama_pipeline",
05379:             "line": 358,
05380:             "args": [
05381:               "args"
05382:             ],
05383:             "async": false
05384:           },
05385:           {
05386:             "name": "generate_text",
05387:             "line": 373,
05388:             "args": [
05389:               "pipe",
05390:               "prompt",
05391:               "max_new_tokens"
05392:             ],
05393:             "async": false
05394:           },
05395:           {
05396:             "name": "write_notes",
05397:             "line": 378,
05398:             "args": [
05399:               "notes_out",
05400:               "notes"
05401:             ],
05402:             "async": false
05403:           },
05404:           {
05405:             "name": "pack_batches",
05406:             "line": 393,
05407:             "args": [
05408:               "items",
05409:               "max_chars"
05410:             ],
05411:             "async": false
05412:           },
05413:           {
05414:             "name": "reduce_notes",
05415:             "line": 413,
05416:             "args": [
05417:               "pipe",
05418:               "notes",
05419:               "args"
05420:             ],
05421:             "async": false
05422:           },
05423:           {
05424:             "name": "run_onepass",
05425:             "line": 435,
05426:             "args": [
05427:               "pipe",
05428:               "context_path",
05429:               "args"
05430:             ],
05431:             "async": false
05432:           },
05433:           {
05434:             "name": "run_chunked",
05435:             "line": 441,
05436:             "args": [
05437:               "pipe",
05438:               "context_path",
05439:               "chunk_dir",
05440:               "notes_out",
05441:               "args"
05442:             ],
05443:             "async": false
05444:           },
05445:           {
05446:             "name": "main",
05447:             "line": 477,
05448:             "args": [],
05449:             "async": false
05450:           }
05451:         ],
05452:         "classes": [],
05453:         "assignments": [
05454:           "ROOT",
05455:           "DEFAULT_MODEL_DIR",
05456:           "DEFAULT_CONTEXT",
05457:           "DEFAULT_CHUNK_DIR",
05458:           "DEFAULT_OUT",
05459:           "DEFAULT_NOTES_OUT",
05460:           "DEFAULT_MUSIC_CONTEXT",
05461:           "DEFAULT_MUSIC_CHUNK_DIR",
05462:           "DEFAULT_MUSIC_OUT",
05463:           "DEFAULT_MUSIC_NOTES_OUT"
05464:         ]
05465:       }
05466:     },
05467:     {
05468:       "file": "Tools/npu/run_ollama_music_agent.py",
05469:       "exists": true,
05470:       "suffix": ".py",
05471:       "lines": 239,
05472:       "chars": 8218,
05473:       "sha256": "e5c78a8bdd345b4b4a638f9b0482a039fe7b990c31465c780b2359009bb1157c",
05474:       "symbols": {
05475:         "imports": [
05476:           "from __future__ import annotations",
05477:           "from pathlib import Path",
05478:           "argparse",
05479:           "json",
05480:           "from datetime import datetime",
05481:           "from ollama_runtime import OllamaSession, parse_json_response"
05482:         ],
05483:         "functions": [
05484:           {
05485:             "name": "read_json",
05486:             "line": 22,
05487:             "args": [
05488:               "path"
05489:             ],
05490:             "async": false
05491:           },
05492:           {
05493:             "name": "compact_context_for_prompt",
05494:             "line": 27,
05495:             "args": [
05496:               "context"
05497:             ],
05498:             "async": false
05499:           },
05500:           {
05501:             "name": "build_prompt",
05502:             "line": 56,
05503:             "args": [
05504:               "context"
05505:             ],
05506:             "async": false
05507:           },
05508:           {
05509:             "name": "markdown_from_insights",
05510:             "line": 111,
05511:             "args": [
05512:               "data",
05513:               "model"
05514:             ],
05515:             "async": false
05516:           },
05517:           {
05518:             "name": "run_ollama_music_agent",
05519:             "line": 141,
05520:             "args": [
05521:               "context_json",
05522:               "fallback_context_json",
05523:               "out_json",
05524:               "out_md",
05525:               "model",
05526:               "base_url",
05527:               "keep_alive",
05528:               "max_new_tokens",
05529:               "temperature",
05530:               "keep_server",
05531:               "keep_model"
05532:             ],
05533:             "async": false
05534:           },
05535:           {
05536:             "name": "main",
05537:             "line": 207,
05538:             "args": [],
05539:             "async": false
05540:           }
05541:         ],
05542:         "classes": [],
05543:         "assignments": [
05544:           "ROOT",
05545:           "OUTPUT_DIR",
05546:           "TOOLS_DIR",
05547:           "DEFAULT_TRACK_STEM",
05548:           "DEFAULT_CONTEXT_JSON",
05549:           "DEFAULT_MUSIC_CONTEXT_JSON",
05550:           "DEFAULT_OUT_JSON",
05551:           "DEFAULT_OUT_MD"
05552:         ]
05553:       }
05554:     },
05555:     {
05556:       "file": "Tools/npu/run_npu_context.ps1",
05557:       "exists": true,
05558:       "suffix": ".ps1",
05559:       "lines": 239,
05560:       "chars": 7213,
05561:       "sha256": "2eecccc5fb54474ebaf957686aff5de3e875f3822e6ec16dc26efe8bb525154d"
05562:     }
05563:   ],
05564:   "chunks": [
05565:     {
05566:       "index": 1,
05567:       "file": "analyze_wav.py",
05568:       "path": "Tools/npu/npu_code_chunks/chunk_001_analyze_wav_py.md",
05569:       "part": 1,
05570:       "start_line": 1,
05571:       "end_line": 213,
05572:       "chars": 10943,
05573:       "sha256": "95bf0c688760f38bbf4fb2647d233f28408ee34e3d69dea2ded7d89020425a4d"
05574:     },
05575:     {
05576:       "index": 2,
05577:       "file": "analyze_wav.py",
05578:       "path": "Tools/npu/npu_code_chunks/chunk_002_analyze_wav_py.md",
05579:       "part": 2,
05580:       "start_line": 214,
05581:       "end_line": 257,
05582:       "chars": 2521,
05583:       "sha256": "7be941249f940bd1233e248c35d21b0111541c9c6f6d6be8dc4b282eafb5b555"
05584:     },
05585:     {
05586:       "index": 3,
05587:       "file": "build_track_summary.py",
05588:       "path": "Tools/npu/npu_code_chunks/chunk_003_build_track_summary_py.md",
05589:       "part": 1,
05590:       "start_line": 1,
05591:       "end_line": 113,
05592:       "chars": 5325,
05593:       "sha256": "a942e518cbe07ec14e90551a11e59535449dfa318d73fdc35f2c4e32674c8e02"
05594:     },
05595:     {
05596:       "index": 4,
05597:       "file": "normalize_scene_spec.py",
05598:       "path": "Tools/npu/npu_code_chunks/chunk_004_normalize_scene_spec_py.md",
05599:       "part": 1,
05600:       "start_line": 1,
05601:       "end_line": 275,
05602:       "chars": 11108,
05603:       "sha256": "8bd34ef7c8392166a482a7515607e105ae1aaaebe41f8b0330c1581f853e8139"
05604:     },
05605:     {
05606:       "index": 5,
05607:       "file": "normalize_scene_spec.py",
```
