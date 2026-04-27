# Project Code Chunk 161/212

- File: `Tools/npu/npu_code_manifest.json`
- Part: `14`
- Lines: `4489-4874`

## Content
```json
04489:             "line": 71,
04490:             "args": [
04491:               "values",
04492:               "ratio"
04493:             ],
04494:             "async": false
04495:           },
04496:           {
04497:             "name": "avg_top",
04498:             "line": 85,
04499:             "args": [
04500:               "values",
04501:               "ratio"
04502:             ],
04503:             "async": false
04504:           },
04505:           {
04506:             "name": "value_stats",
04507:             "line": 92,
04508:             "args": [
04509:               "values"
04510:             ],
04511:             "async": false
04512:           },
04513:           {
04514:             "name": "frame_values",
04515:             "line": 117,
04516:             "args": [
04517:               "frames",
04518:               "key"
04519:             ],
04520:             "async": false
04521:           },
04522:           {
04523:             "name": "energy_stats",
04524:             "line": 121,
04525:             "args": [
04526:               "frames"
04527:             ],
04528:             "async": false
04529:           },
04530:           {
04531:             "name": "dominant_band",
04532:             "line": 131,
04533:             "args": [
04534:               "stats"
04535:             ],
04536:             "async": false
04537:           },
04538:           {
04539:             "name": "intensity_label",
04540:             "line": 140,
04541:             "args": [
04542:               "score"
04543:             ],
04544:             "async": false
04545:           },
04546:           {
04547:             "name": "segment_score",
04548:             "line": 152,
04549:             "args": [
04550:               "stats"
04551:             ],
04552:             "async": false
04553:           },
04554:           {
04555:             "name": "control_suggestions",
04556:             "line": 162,
04557:             "args": [
04558:               "stats",
04559:               "beat_count"
04560:             ],
04561:             "async": false
04562:           },
04563:           {
04564:             "name": "split_segments",
04565:             "line": 176,
04566:             "args": [
04567:               "frames",
04568:               "segment_seconds",
04569:               "duration"
04570:             ],
04571:             "async": false
04572:           },
04573:           {
04574:             "name": "sampled_frames",
04575:             "line": 189,
04576:             "args": [
04577:               "frames",
04578:               "max_rows"
04579:             ],
04580:             "async": false
04581:           },
04582:           {
04583:             "name": "top_events",
04584:             "line": 210,
04585:             "args": [
04586:               "frames",
04587:               "limit"
04588:             ],
04589:             "async": false
04590:           },
04591:           {
04592:             "name": "beats_in_range",
04593:             "line": 235,
04594:             "args": [
04595:               "beats",
04596:               "start",
04597:               "end"
04598:             ],
04599:             "async": false
04600:           },
04601:           {
04602:             "name": "build_segments",
04603:             "line": 239,
04604:             "args": [
04605:               "analysis",
04606:               "segment_seconds"
04607:             ],
04608:             "async": false
04609:           },
04610:           {
04611:             "name": "summarize_analysis",
04612:             "line": 273,
04613:             "args": [
04614:               "analysis_path",
04615:               "segment_seconds"
04616:             ],
04617:             "async": false
04618:           },
04619:           {
04620:             "name": "scene_summary_from_json",
04621:             "line": 319,
04622:             "args": [
04623:               "path",
04624:               "data"
04625:             ],
04626:             "async": false
04627:           },
04628:           {
04629:             "name": "load_scene_records",
04630:             "line": 353,
04631:             "args": [
04632:               "scene_files"
04633:             ],
04634:             "async": false
04635:           },
04636:           {
04637:             "name": "markdown_table_rows",
04638:             "line": 387,
04639:             "args": [
04640:               "rows",
04641:               "keys"
04642:             ],
04643:             "async": false
04644:           },
04645:           {
04646:             "name": "write_chunk",
04647:             "line": 394,
04648:             "args": [
04649:               "path",
04650:               "title",
04651:               "body"
04652:             ],
04653:             "async": false
04654:           },
04655:           {
04656:             "name": "write_music_chunks",
04657:             "line": 404,
04658:             "args": [
04659:               "context",
04660:               "scene_records"
04661:             ],
04662:             "async": false
04663:           },
04664:           {
04665:             "name": "write_music_context_md",
04666:             "line": 481,
04667:             "args": [
04668:               "context",
04669:               "scene_records",
04670:               "chunks"
04671:             ],
04672:             "async": false
04673:           },
04674:           {
04675:             "name": "build_analysis_ai_context",
04676:             "line": 538,
04677:             "args": [
04678:               "context"
04679:             ],
04680:             "async": false
04681:           },
04682:           {
04683:             "name": "write_blender_keyframe_alias",
04684:             "line": 572,
04685:             "args": [
04686:               "analysis_path",
04687:               "blender_keyframes_path"
04688:             ],
04689:             "async": false
04690:           },
04691:           {
04692:             "name": "build_music_context",
04693:             "line": 579,
04694:             "args": [
04695:               "analysis_path",
04696:               "track_summary_path",
04697:               "scene_files",
04698:               "segment_seconds",
04699:               "compact_json_path",
04700:               "analysis_ai_context_path",
04701:               "blender_keyframes_path",
04702:               "run_ollama",
04703:               "ollama_model"
04704:             ],
04705:             "async": false
04706:           },
04707:           {
04708:             "name": "main",
04709:             "line": 676,
04710:             "args": [],
04711:             "async": false
04712:           }
04713:         ],
04714:         "classes": [],
04715:         "assignments": [
04716:           "ROOT",
04717:           "OUTPUT_DIR",
04718:           "OUT_DIR",
04719:           "CHUNK_DIR",
04720:           "DEFAULT_TRACK_STEM",
04721:           "DEFAULT_ANALYSIS",
04722:           "DEFAULT_TRACK_SUMMARY",
04723:           "DEFAULT_COMPACT_JSON",
04724:           "DEFAULT_ANALYSIS_AI_CONTEXT",
04725:           "DEFAULT_BLENDER_KEYFRAMES_JSON",
04726:           "OUT_MD",
04727:           "OUT_JSON",
04728:           "DEFAULT_SCENE_FILES",
04729:           "DEFAULT_SEGMENT_SECONDS",
04730:           "SAMPLE_ROWS_PER_SEGMENT",
04731:           "TOP_EVENTS_PER_SEGMENT"
04732:         ]
04733:       }
04734:     },
04735:     {
04736:       "file": "Tools/npu/build_npu_code_context.py",
04737:       "exists": true,
04738:       "suffix": ".py",
04739:       "lines": 390,
04740:       "chars": 12139,
04741:       "sha256": "45037f46cd073bdc0d191828f75224d1d8726bf519620bc3ba7f795b687922b0",
04742:       "symbols": {
04743:         "imports": [
04744:           "from __future__ import annotations",
04745:           "from pathlib import Path",
04746:           "ast",
04747:           "hashlib",
04748:           "json",
04749:           "re",
04750:           "from datetime import datetime"
04751:         ],
04752:         "functions": [
04753:           {
04754:             "name": "sha256_text",
04755:             "line": 56,
04756:             "args": [
04757:               "text"
04758:             ],
04759:             "async": false
04760:           },
04761:           {
04762:             "name": "rel_to_root",
04763:             "line": 60,
04764:             "args": [
04765:               "path"
04766:             ],
04767:             "async": false
04768:           },
04769:           {
04770:             "name": "slugify",
04771:             "line": 64,
04772:             "args": [
04773:               "value",
04774:               "max_len"
04775:             ],
04776:             "async": false
04777:           },
04778:           {
04779:             "name": "is_usable_text_file",
04780:             "line": 69,
04781:             "args": [
04782:               "path"
04783:             ],
04784:             "async": false
04785:           },
04786:           {
04787:             "name": "collect_files",
04788:             "line": 75,
04789:             "args": [],
04790:             "async": false
04791:           },
04792:           {
04793:             "name": "target_name",
04794:             "line": 99,
04795:             "args": [
04796:               "target"
04797:             ],
04798:             "async": false
04799:           },
04800:           {
04801:             "name": "extract_symbols",
04802:             "line": 107,
04803:             "args": [
04804:               "source"
04805:             ],
04806:             "async": false
04807:           },
04808:           {
04809:             "name": "file_record",
04810:             "line": 169,
04811:             "args": [
04812:               "path",
04813:               "source"
04814:             ],
04815:             "async": false
04816:           },
04817:           {
04818:             "name": "format_symbol_summary",
04819:             "line": 184,
04820:             "args": [
04821:               "record"
04822:             ],
04823:             "async": false
04824:           },
04825:           {
04826:             "name": "numbered_lines",
04827:             "line": 225,
04828:             "args": [
04829:               "lines",
04830:               "start_line"
04831:             ],
04832:             "async": false
04833:           },
04834:           {
04835:             "name": "split_source",
04836:             "line": 229,
04837:             "args": [
04838:               "source",
04839:               "max_chars"
04840:             ],
04841:             "async": false
04842:           },
04843:           {
04844:             "name": "write_context_chunks",
04845:             "line": 255,
04846:             "args": [
04847:               "files",
04848:               "sources"
04849:             ],
04850:             "async": false
04851:           },
04852:           {
04853:             "name": "write_index",
04854:             "line": 325,
04855:             "args": [
04856:               "files",
04857:               "chunks",
04858:               "created_at"
04859:             ],
04860:             "async": false
04861:           },
04862:           {
04863:             "name": "main",
04864:             "line": 348,
04865:             "args": [],
04866:             "async": false
04867:           }
04868:         ],
04869:         "classes": [],
04870:         "assignments": [
04871:           "ROOT",
04872:           "SCRIPT_DIR",
04873:           "OUT_DIR",
04874:           "OUT_MD",
```
