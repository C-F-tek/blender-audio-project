# Project Code Chunk 156/212

- File: `Tools/npu/npu_code_manifest.json`
- Part: `9`
- Lines: `2670-3010`

## Content
```json
02670:             ],
02671:             "async": false
02672:           },
02673:           {
02674:             "name": "all_editor_strips",
02675:             "line": 151,
02676:             "args": [
02677:               "editor"
02678:             ],
02679:             "async": false
02680:           },
02681:           {
02682:             "name": "remove_editor_strip",
02683:             "line": 163,
02684:             "args": [
02685:               "editor",
02686:               "strip"
02687:             ],
02688:             "async": false
02689:           },
02690:           {
02691:             "name": "force_visible_sequencer",
02692:             "line": 176,
02693:             "args": [
02694:               "scene",
02695:               "editor"
02696:             ],
02697:             "async": false
02698:           },
02699:           {
02700:             "name": "clear_sequence_editor",
02701:             "line": 224,
02702:             "args": [
02703:               "scene"
02704:             ],
02705:             "async": false
02706:           },
02707:           {
02708:             "name": "add_image_sequence",
02709:             "line": 235,
02710:             "args": [
02711:               "editor",
02712:               "frame_files"
02713:             ],
02714:             "async": false
02715:           },
02716:           {
02717:             "name": "add_synced_audio",
02718:             "line": 258,
02719:             "args": [
02720:               "editor",
02721:               "first_frame"
02722:             ],
02723:             "async": false
02724:           },
02725:           {
02726:             "name": "configure_video_output",
02727:             "line": 285,
02728:             "args": [
02729:               "scene",
02730:               "frame_count"
02731:             ],
02732:             "async": false
02733:           },
02734:           {
02735:             "name": "print_strip_report",
02736:             "line": 327,
02737:             "args": [
02738:               "scene",
02739:               "editor"
02740:             ],
02741:             "async": false
02742:           },
02743:           {
02744:             "name": "main",
02745:             "line": 342,
02746:             "args": [],
02747:             "async": false
02748:           }
02749:         ],
02750:         "classes": [],
02751:         "assignments": [
02752:           "SCRIPT_DIR",
02753:           "ROOT",
02754:           "RENDERS_DIR",
02755:           "AUDIO_PATH",
02756:           "OUTPUT_MP4",
02757:           "OUTPUT_IMAGE_SEQUENCE_DIR",
02758:           "OUTPUT_IMAGE_SEQUENCE_PREFIX",
02759:           "IMAGE_SEQUENCE_FORMAT",
02760:           "VIDEO_BITRATE",
02761:           "VIDEO_MAXRATE",
02762:           "VIDEO_MINRATE",
02763:           "VIDEO_BUFFERSIZE",
02764:           "AUDIO_BITRATE",
02765:           "ENCODE_SEQUENCE_AUTO_RENDER",
02766:           "ENCODE_SEQUENCE_SYNC_AUDIO_TO_FRAME_NUMBER",
02767:           "ENCODE_SEQUENCE_AUDIO_ZERO_FRAME",
02768:           "ENCODE_SEQUENCE_SKIP_PLACEHOLDERS",
02769:           "ENCODE_SEQUENCE_SWITCH_TO_SEQUENCER"
02770:         ]
02771:       }
02772:     },
02773:     {
02774:       "file": "Scripting/v61b/encode_ffmpeg_v61b.py",
02775:       "exists": true,
02776:       "suffix": ".py",
02777:       "lines": 399,
02778:       "chars": 12329,
02779:       "sha256": "c8c7a5a772e173407ffedf0b8abf7b1908634ea91543946f5f71c361d2076034",
02780:       "symbols": {
02781:         "imports": [
02782:           "json",
02783:           "os",
02784:           "re",
02785:           "shutil",
02786:           "subprocess",
02787:           "sys",
02788:           "from pathlib import Path",
02789:           "config"
02790:         ],
02791:         "functions": [
02792:           {
02793:             "name": "resolve_script_dir",
02794:             "line": 15,
02795:             "args": [],
02796:             "async": false
02797:           },
02798:           {
02799:             "name": "extract_frame_number",
02800:             "line": 82,
02801:             "args": [
02802:               "path"
02803:             ],
02804:             "async": false
02805:           },
02806:           {
02807:             "name": "sorted_frame_files",
02808:             "line": 89,
02809:             "args": [],
02810:             "async": false
02811:           },
02812:           {
02813:             "name": "contiguous_frame_files",
02814:             "line": 109,
02815:             "args": [
02816:               "frame_files"
02817:             ],
02818:             "async": false
02819:           },
02820:           {
02821:             "name": "get_fps",
02822:             "line": 133,
02823:             "args": [],
02824:             "async": false
02825:           },
02826:           {
02827:             "name": "candidate_path_values",
02828:             "line": 155,
02829:             "args": [],
02830:             "async": false
02831:           },
02832:           {
02833:             "name": "find_ffmpeg",
02834:             "line": 175,
02835:             "args": [],
02836:             "async": false
02837:           },
02838:           {
02839:             "name": "build_image_pattern",
02840:             "line": 203,
02841:             "args": [
02842:               "first_file",
02843:               "first_frame"
02844:             ],
02845:             "async": false
02846:           },
02847:           {
02848:             "name": "source_frame_to_audio_offset",
02849:             "line": 216,
02850:             "args": [
02851:               "first_frame",
02852:               "fps"
02853:             ],
02854:             "async": false
02855:           },
02856:           {
02857:             "name": "build_command",
02858:             "line": 222,
02859:             "args": [
02860:               "ffmpeg",
02861:               "pattern",
02862:               "first_frame",
02863:               "frame_count",
02864:               "fps",
02865:               "audio_offset"
02866:             ],
02867:             "async": false
02868:           },
02869:           {
02870:             "name": "write_visible_shell_launcher",
02871:             "line": 328,
02872:             "args": [
02873:               "command",
02874:               "output",
02875:               "first_frame",
02876:               "frame_count",
02877:               "fps",
02878:               "audio_offset"
02879:             ],
02880:             "async": false
02881:           },
02882:           {
02883:             "name": "launch_visible_shell",
02884:             "line": 355,
02885:             "args": [
02886:               "command",
02887:               "output",
02888:               "first_frame",
02889:               "frame_count",
02890:               "fps",
02891:               "audio_offset"
02892:             ],
02893:             "async": false
02894:           },
02895:           {
02896:             "name": "main",
02897:             "line": 362,
02898:             "args": [],
02899:             "async": false
02900:           }
02901:         ],
02902:         "classes": [],
02903:         "assignments": [
02904:           "SCRIPT_DIR",
02905:           "AUDIO_PATH",
02906:           "ANALYSIS_JSON_PATH",
02907:           "OUTPUT_IMAGE_SEQUENCE_DIR",
02908:           "OUTPUT_IMAGE_SEQUENCE_PREFIX",
02909:           "IMAGE_SEQUENCE_FORMAT",
02910:           "OUTPUT_MP4",
02911:           "FFMPEG_EXE_PATH",
02912:           "FFMPEG_CRF",
02913:           "FFMPEG_PRESET",
02914:           "FFMPEG_TUNE",
02915:           "FFMPEG_AUDIO_BITRATE",
02916:           "FFMPEG_PROFILE",
02917:           "FFMPEG_GPU_INDEX",
02918:           "FFMPEG_NVENC_PRESET",
02919:           "FFMPEG_NVENC_TUNE",
02920:           "FFMPEG_NVENC_CQ",
02921:           "FFMPEG_SVTAV1_PRESET",
02922:           "FFMPEG_SVTAV1_CRF",
02923:           "FFMPEG_THREADS",
02924:           "FFMPEG_VIDEO_FILTER",
02925:           "FFMPEG_AUDIO_SAMPLE_RATE",
02926:           "SYNC_AUDIO",
02927:           "AUDIO_ZERO_FRAME",
02928:           "SKIP_PLACEHOLDERS",
02929:           "LAUNCH_VISIBLE_SHELL"
02930:         ]
02931:       }
02932:     },
02933:     {
02934:       "file": "Scripting/v61b/PROJECT_STRUCTURE.md",
02935:       "exists": true,
02936:       "suffix": ".md",
02937:       "lines": 44,
02938:       "chars": 2497,
02939:       "sha256": "a1dc036f5e6a993dd1197de70a96338f76de597950e5164def3f1dc17eb188e4"
02940:     },
02941:     {
02942:       "file": "Scripting/v61b/SCENE_TUNING_GUIDE.md",
02943:       "exists": true,
02944:       "suffix": ".md",
02945:       "lines": 305,
02946:       "chars": 13330,
02947:       "sha256": "edd8ed0ef33670b4bbd79078b76fa9943be23a39ccf8c40c731eb0e7b7feeaac"
02948:     },
02949:     {
02950:       "file": "Scripting/v61b/__init__.py",
02951:       "exists": true,
02952:       "suffix": ".py",
02953:       "lines": 1,
02954:       "chars": 16,
02955:       "sha256": "c0bbbb5b6d776bd569a8ce1dde718a322055ae62b1c3b48f26826d6e8acdb651",
02956:       "symbols": {
02957:         "imports": [],
02958:         "functions": [],
02959:         "classes": [],
02960:         "assignments": []
02961:       }
02962:     },
02963:     {
02964:       "file": "Scripting/v61b/asset_setup.py",
02965:       "exists": true,
02966:       "suffix": ".py",
02967:       "lines": 726,
02968:       "chars": 23898,
02969:       "sha256": "91343beb43af7ff1a9a022e03ce20e1d104057e497a74a8da19b07658605689e",
02970:       "symbols": {
02971:         "imports": [
02972:           "bpy",
02973:           "from mathutils import Vector",
02974:           "from pathlib import Path",
02975:           "from config import PRIMARY_ASSET_DIR, PRIMARY_TARGET_SIZE, PRIMARY_BASE_Z, SUPPORTED_ASSET_EXTENSIONS, USE_SECONDARY_ASSET, SECONDARY_ASSET_DIR, SECONDARY_TARGET_SIZE, SECONDARY_BASE_Z, SECONDARY_BASE_OFFSET_X, SECONDARY_BASE_OFFSET_Y, SECONDARY_BASE_OFFSET_Z, PEACE_PALETTE, USE_HERO_MESH_DEFORM, HERO_DEFORM_STRENGTH_MAX, HERO_DEFORM_STRENGTH_MIN, HERO_DEFORM_DETAIL_STRENGTH_MAX, HERO_DEFORM_WAVE_HEIGHT_MAX, HERO_DEFORM_MAIN_DIM_FACTOR, HERO_DEFORM_DETAIL_DIM_FACTOR, HERO_DEFORM_WAVE_DIM_FACTOR, HERO_DEFORM_TWIST_MAX, HERO_DEFORM_SUBDIV_VIEW, HERO_DEFORM_SUBDIV_RENDER, HERO_DEFORM_NOISE_SIZE, HERO_DEFORM_DETAIL_NOISE_SIZE, HERO_DEFORM_NOISE_CONTRAST, HERO_DEFORM_CONTROLLER_Z, USE_HERO_MATERIAL_AUDIO_NODES, HERO_MATERIAL_EMISSION_MIN, HERO_MATERIAL_SELF_LIGHT_MIN, HERO_MATERIAL_BUMP_MIN, HERO_MATERIAL_ROUGHNESS_MAX, HERO_MATERIAL_NOISE_SCALE_MIN",
02976:           "from scene_utils import create_controller_empty"
02977:         ],
02978:         "functions": [
02979:           {
02980:             "name": "find_asset_file",
02981:             "line": 43,
02982:             "args": [
02983:               "asset_dir"
02984:             ],
02985:             "async": false
02986:           },
02987:           {
02988:             "name": "import_asset_file",
02989:             "line": 62,
02990:             "args": [
02991:               "asset_file"
02992:             ],
02993:             "async": false
02994:           },
02995:           {
02996:             "name": "get_world_bbox",
02997:             "line": 94,
02998:             "args": [
02999:               "objects"
03000:             ],
03001:             "async": false
03002:           },
03003:           {
03004:             "name": "create_scene_core",
03005:             "line": 127,
03006:             "args": [],
03007:             "async": false
03008:           },
03009:           {
03010:             "name": "make_asset_root",
```
