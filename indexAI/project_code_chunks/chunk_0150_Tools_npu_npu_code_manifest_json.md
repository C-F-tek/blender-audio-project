# Project Code Chunk 150/212

- File: `Tools/npu/npu_code_manifest.json`
- Part: `3`
- Lines: `753-1106`

## Content
```json
00753:           },
00754:           {
00755:             "name": "read_json",
00756:             "line": 57,
00757:             "args": [
00758:               "path"
00759:             ],
00760:             "async": false
00761:           },
00762:           {
00763:             "name": "write_json",
00764:             "line": 63,
00765:             "args": [
00766:               "path",
00767:               "data"
00768:             ],
00769:             "async": false
00770:           },
00771:           {
00772:             "name": "read_optional_json",
00773:             "line": 68,
00774:             "args": [
00775:               "path"
00776:             ],
00777:             "async": false
00778:           },
00779:           {
00780:             "name": "update_track_paths",
00781:             "line": 81,
00782:             "args": [
00783:               "track_stem",
00784:               "analysis_ai_context"
00785:             ],
00786:             "async": false
00787:           },
00788:           {
00789:             "name": "apply_default_input_paths",
00790:             "line": 93,
00791:             "args": [
00792:               "args"
00793:             ],
00794:             "async": false
00795:           },
00796:           {
00797:             "name": "validate_input_files",
00798:             "line": 106,
00799:             "args": [
00800:               "args"
00801:             ],
00802:             "async": false
00803:           },
00804:           {
00805:             "name": "looks_degraded_text",
00806:             "line": 126,
00807:             "args": [
00808:               "text"
00809:             ],
00810:             "async": false
00811:           },
00812:           {
00813:             "name": "deterministic_technical_notes",
00814:             "line": 142,
00815:             "args": [
00816:               "music_context",
00817:               "project_manifest",
00818:               "reason"
00819:             ],
00820:             "async": false
00821:           },
00822:           {
00823:             "name": "run_npu_technical_pass",
00824:             "line": 191,
00825:             "args": [
00826:               "args"
00827:             ],
00828:             "async": false
00829:           },
00830:           {
00831:             "name": "build_creative_scene_prompt",
00832:             "line": 235,
00833:             "args": [
00834:               "music_context",
00835:               "npu_notes",
00836:               "project_index"
00837:             ],
00838:             "async": false
00839:           },
00840:           {
00841:             "name": "build_merge_prompt",
00842:             "line": 317,
00843:             "args": [
00844:               "music_context",
00845:               "npu_notes",
00846:               "creative",
00847:               "technical"
00848:             ],
00849:             "async": false
00850:           },
00851:           {
00852:             "name": "build_implementation_prompt",
00853:             "line": 379,
00854:             "args": [
00855:               "plan",
00856:               "npu_notes",
00857:               "include_manual",
00858:               "gpu_packet",
00859:               "scene_brief",
00860:               "asset_inventory"
00861:             ],
00862:             "async": false
00863:           },
00864:           {
00865:             "name": "build_implementation_retry_prompt",
00866:             "line": 491,
00867:             "args": [
00868:               "plan",
00869:               "invalid_draft",
00870:               "validation"
00871:             ],
00872:             "async": false
00873:           },
00874:           {
00875:             "name": "safe_parse_json",
00876:             "line": 580,
00877:             "args": [
00878:               "text",
00879:               "fallback_key"
00880:             ],
00881:             "async": false
00882:           },
00883:           {
00884:             "name": "extract_python_script",
00885:             "line": 588,
00886:             "args": [
00887:               "text"
00888:             ],
00889:             "async": false
00890:           },
00891:           {
00892:             "name": "draft_from_raw_python_script",
00893:             "line": 608,
00894:             "args": [
00895:               "text",
00896:               "model",
00897:               "reason"
00898:             ],
00899:             "async": false
00900:           },
00901:           {
00902:             "name": "get_indexed_project_files",
00903:             "line": 659,
00904:             "args": [],
00905:             "async": false
00906:           },
00907:           {
00908:             "name": "validate_implementation_draft",
00909:             "line": 664,
00910:             "args": [
00911:               "draft"
00912:             ],
00913:             "async": false
00914:           },
00915:           {
00916:             "name": "generated_scene_script_relpath",
00917:             "line": 761,
00918:             "args": [],
00919:             "async": false
00920:           },
00921:           {
00922:             "name": "generated_scene_script_abspath",
00923:             "line": 765,
00924:             "args": [],
00925:             "async": false
00926:           },
00927:           {
00928:             "name": "deterministic_scene_builder_script",
00929:             "line": 769,
00930:             "args": [
00931:               "track_stem",
00932:               "analysis_json",
00933:               "music_context_json",
00934:               "ai_context_json",
00935:               "blender_keyframes_json",
00936:               "asset_inventory_json",
00937:               "scene_brief"
00938:             ],
00939:             "async": false
00940:           },
00941:           {
00942:             "name": "deterministic_support_files",
00943:             "line": 1152,
00944:             "args": [
00945:               "track_stem",
00946:               "scene_brief"
00947:             ],
00948:             "async": false
00949:           },
00950:           {
00951:             "name": "build_fallback_implementation_draft",
00952:             "line": 1205,
00953:             "args": [
00954:               "reason",
00955:               "model",
00956:               "args",
00957:               "scene_brief",
00958:               "asset_inventory"
00959:             ],
00960:             "async": false
00961:           },
00962:           {
00963:             "name": "normalize_implementation_draft",
00964:             "line": 1292,
00965:             "args": [
00966:               "draft",
00967:               "model",
00968:               "args",
00969:               "scene_brief",
00970:               "asset_inventory"
00971:             ],
00972:             "async": false
00973:           },
00974:           {
00975:             "name": "generate_implementation_draft_with_retry",
00976:             "line": 1313,
00977:             "args": [
00978:               "manager",
00979:               "model_name",
00980:               "implementation_prompt",
00981:               "plan",
00982:               "max_new_tokens",
00983:               "args",
00984:               "scene_brief",
00985:               "asset_inventory"
00986:             ],
00987:             "async": false
00988:           },
00989:           {
00990:             "name": "write_brief",
00991:             "line": 1376,
00992:             "args": [
00993:               "plan",
00994:               "creative",
00995:               "technical",
00996:               "npu_notes"
00997:             ],
00998:             "async": false
00999:           },
01000:           {
01001:             "name": "write_implementation_draft",
01002:             "line": 1399,
01003:             "args": [
01004:               "draft"
01005:             ],
01006:             "async": false
01007:           },
01008:           {
01009:             "name": "main",
01010:             "line": 1453,
01011:             "args": [],
01012:             "async": false
01013:           }
01014:         ],
01015:         "classes": [],
01016:         "assignments": [
01017:           "ROOT",
01018:           "TOOLS_DIR",
01019:           "OUTPUT_DIR",
01020:           "DEFAULT_TRACK_STEM",
01021:           "TRACK_STEM",
01022:           "MUSIC_AI_CONTEXT",
01023:           "DUAL_PLAN_JSON",
01024:           "DUAL_BRIEF_MD",
01025:           "OLLAMA_INSIGHTS_JSON",
01026:           "OLLAMA_INSIGHTS_MD",
01027:           "NPU_TECH_MD",
01028:           "NPU_PREFLIGHT_JSON",
01029:           "IMPLEMENTATION_DRAFT_JSON",
01030:           "IMPLEMENTATION_SCRIPT",
01031:           "IMPLEMENTATION_NOTES",
01032:           "NPU_IMPLEMENTATION_NOTES",
01033:           "ALLOWED_NEW_PREFIXES",
01034:           "PREFERRED_IMPLEMENTATION_FILES"
01035:         ]
01036:       }
01037:     },
01038:     {
01039:       "file": "Scripting/v61b/config.py",
01040:       "exists": true,
01041:       "suffix": ".py",
01042:       "lines": 439,
01043:       "chars": 15317,
01044:       "sha256": "a01b8504529dd7bd8d25d54a6612e17f834097d74f448034c6a945d8f523913e",
01045:       "symbols": {
01046:         "imports": [
01047:           "from pathlib import Path",
01048:           "json",
01049:           "math"
01050:         ],
01051:         "functions": [],
01052:         "classes": [],
01053:         "assignments": [
01054:           "ROOT",
01055:           "PROJECT_DIR",
01056:           "OUTPUT_DIR",
01057:           "ASSETS_DIR",
01058:           "AUDIO_DIR",
01059:           "RENDERS_DIR",
01060:           "SCRIPTING_DIR",
01061:           "ANALYSIS_JSON_PATH",
01062:           "AUDIO_PATH",
01063:           "OUTPUT_MP4",
01064:           "OUTPUT_IMAGE_SEQUENCE_DIR",
01065:           "OUTPUT_IMAGE_SEQUENCE_PREFIX",
01066:           "WORKFLOW_SESSION_PATH",
01067:           "WORKFLOW_SESSION_ACTIVE",
01068:           "WORKFLOW_SESSION_ARTIFACTS",
01069:           "FINAL_FOR_YOUTUBE",
01070:           "YOUTUBE_FINAL_RESOLUTION",
01071:           "CLEAR_SCENE",
01072:           "CLEAR_SEQUENCER",
01073:           "FPS_OVERRIDE",
01074:           "RENDER_OUTPUT_MODE",
01075:           "YOUTUBE_FINAL_RESOLUTION",
01076:           "USE_4K",
01077:           "RENDER_PERCENT",
01078:           "USE_MOTION_BLUR",
01079:           "EEVEE_TAA_RENDER_SAMPLES",
01080:           "VOLUMETRIC_SAMPLES",
01081:           "VOLUMETRIC_TILE_SIZE",
01082:           "USE_COMPOSITING",
01083:           "COMPOSITOR_GLARE_THRESHOLD_MIN",
01084:           "COMPOSITOR_GLARE_THRESHOLD_MAX",
01085:           "COMPOSITOR_GLARE_MIX",
01086:           "COMPOSITOR_GLARE_SIZE",
01087:           "COMPOSITOR_LENS_DISTORT_MIN",
01088:           "COMPOSITOR_LENS_DISTORT_MAX",
01089:           "COMPOSITOR_LENS_DISPERSION_MIN",
01090:           "COMPOSITOR_LENS_DISPERSION_MAX",
01091:           "VIDEO_BITRATE",
01092:           "VIDEO_MAXRATE",
01093:           "VIDEO_MINRATE",
01094:           "VIDEO_BUFFERSIZE",
01095:           "AUDIO_BITRATE",
01096:           "IMAGE_SEQUENCE_FORMAT",
01097:           "IMAGE_SEQUENCE_COLOR_DEPTH",
01098:           "IMAGE_SEQUENCE_COMPRESSION",
01099:           "ENCODE_SEQUENCE_AUTO_RENDER",
01100:           "ENCODE_SEQUENCE_SYNC_AUDIO_TO_FRAME_NUMBER",
01101:           "ENCODE_SEQUENCE_AUDIO_ZERO_FRAME",
01102:           "ENCODE_SEQUENCE_SKIP_PLACEHOLDERS",
01103:           "ENCODE_SEQUENCE_SWITCH_TO_SEQUENCER",
01104:           "ENCODE_USE_EXTERNAL_FFMPEG",
01105:           "FFMPEG_EXE_PATH",
01106:           "FFMPEG_OUTPUT_SUFFIX",
```
