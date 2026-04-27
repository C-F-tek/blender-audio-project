# Project Code Chunk 159/212

- File: `Tools/npu/npu_code_manifest.json`
- Part: `12`
- Lines: `3760-4111`

## Content
```json
03760:             "name": "get_or_create_node",
03761:             "line": 61,
03762:             "args": [
03763:               "nodes",
03764:               "node_type",
03765:               "name",
03766:               "location"
03767:             ],
03768:             "async": false
03769:           },
03770:           {
03771:             "name": "get_or_create_value",
03772:             "line": 70,
03773:             "args": [
03774:               "nodes",
03775:               "name",
03776:               "label",
03777:               "location",
03778:               "default"
03779:             ],
03780:             "async": false
03781:           },
03782:           {
03783:             "name": "find_material_output",
03784:             "line": 81,
03785:             "args": [
03786:               "material"
03787:             ],
03788:             "async": false
03789:           },
03790:           {
03791:             "name": "ensure_surface_light_layer",
03792:             "line": 93,
03793:             "args": [
03794:               "material",
03795:               "principled"
03796:             ],
03797:             "async": false
03798:           },
03799:           {
03800:             "name": "hero_meshes",
03801:             "line": 172,
03802:             "args": [],
03803:             "async": false
03804:           },
03805:           {
03806:             "name": "lift_principled_material",
03807:             "line": 183,
03808:             "args": [
03809:               "principled"
03810:             ],
03811:             "async": false
03812:           },
03813:           {
03814:             "name": "ensure_hero_controls",
03815:             "line": 211,
03816:             "args": [
03817:               "material"
03818:             ],
03819:             "async": false
03820:           },
03821:           {
03822:             "name": "collect_hero_controls",
03823:             "line": 300,
03824:             "args": [],
03825:             "async": false
03826:           },
03827:           {
03828:             "name": "patch_hero_materials",
03829:             "line": 317,
03830:             "args": [
03831:               "frames"
03832:             ],
03833:             "async": false
03834:           }
03835:         ],
03836:         "classes": [],
03837:         "assignments": [
03838:           "HERO_MATERIAL_EMISSION_MIN",
03839:           "HERO_MATERIAL_EMISSION_MAX",
03840:           "HERO_MATERIAL_SELF_LIGHT_MIN",
03841:           "HERO_MATERIAL_SELF_LIGHT_MAX",
03842:           "HERO_MATERIAL_BUMP_MIN",
03843:           "HERO_MATERIAL_BUMP_MAX",
03844:           "HERO_MATERIAL_ROUGHNESS_MIN",
03845:           "HERO_MATERIAL_ROUGHNESS_MAX",
03846:           "HERO_MATERIAL_NOISE_SCALE_MIN",
03847:           "HERO_MATERIAL_NOISE_SCALE_MAX",
03848:           "HERO_MATERIAL_MAPPING_DRIFT",
03849:           "PEACE_PALETTE"
03850:         ]
03851:       }
03852:     },
03853:     {
03854:       "file": "Scripting/v61b/hotpatch/lighting_patch.py",
03855:       "exists": true,
03856:       "suffix": ".py",
03857:       "lines": 151,
03858:       "chars": 5444,
03859:       "sha256": "132d9dc0fbbfe26fb6ff8909d3307d6503c50aede3577911dea73cfd18770956",
03860:       "symbols": {
03861:         "imports": [
03862:           "bpy",
03863:           "from common import cfg_value, clear_animation, get_node, keyframe_if_possible, remove_objects_with_prefixes, socket_by_name"
03864:         ],
03865:         "functions": [
03866:           {
03867:             "name": "resize_plane_local",
03868:             "line": 28,
03869:             "args": [
03870:               "obj",
03871:               "target_size"
03872:             ],
03873:             "async": false
03874:           },
03875:           {
03876:             "name": "update_world",
03877:             "line": 44,
03878:             "args": [
03879:               "scene"
03880:             ],
03881:             "async": false
03882:           },
03883:           {
03884:             "name": "remove_legacy_rhythm_objects",
03885:             "line": 84,
03886:             "args": [],
03887:             "async": false
03888:           },
03889:           {
03890:             "name": "update_area_lights",
03891:             "line": 88,
03892:             "args": [
03893:               "frames"
03894:             ],
03895:             "async": false
03896:           },
03897:           {
03898:             "name": "update_backdrop",
03899:             "line": 114,
03900:             "args": [],
03901:             "async": false
03902:           }
03903:         ],
03904:         "classes": [],
03905:         "assignments": [
03906:           "LIGHT_ENERGY_MIN",
03907:           "LIGHT_ENERGY_MAX",
03908:           "WORLD_STRENGTH",
03909:           "WORLD_CAMERA_STRENGTH",
03910:           "WORLD_LIGHT_COLOR",
03911:           "WORLD_CAMERA_COLOR",
03912:           "BACKDROP_EMISSION_MIN",
03913:           "BACKDROP_EMISSION_MAX",
03914:           "BACKDROP_SIZE",
03915:           "BACKDROP_LOCATION",
03916:           "BACKDROP_ROT_X",
03917:           "FLOOR_RENDER_VISIBLE",
03918:           "FLOOR_VIEWPORT_VISIBLE"
03919:         ]
03920:       }
03921:     },
03922:     {
03923:       "file": "Scripting/v61b/hotpatch/render_patch.py",
03924:       "exists": true,
03925:       "suffix": ".py",
03926:       "lines": 207,
03927:       "chars": 6904,
03928:       "sha256": "916caf8f5ad9d9010a3dcf0b50897b0118c208306b11495c7bbd603d02bd907f",
03929:       "symbols": {
03930:         "imports": [
03931:           "from render_setup import configure_render",
03932:           "from common import OUTPUT_MP4, cfg_value"
03933:         ],
03934:         "functions": [
03935:           {
03936:             "name": "normalize_runtime_profile",
03937:             "line": 6,
03938:             "args": [
03939:               "profile"
03940:             ],
03941:             "async": false
03942:           },
03943:           {
03944:             "name": "get_scene_compositor_tree",
03945:             "line": 49,
03946:             "args": [
03947:               "scene"
03948:             ],
03949:             "async": false
03950:           },
03951:           {
03952:             "name": "current_runtime_profile",
03953:             "line": 57,
03954:             "args": [
03955:               "scene"
03956:             ],
03957:             "async": false
03958:           },
03959:           {
03960:             "name": "apply_runtime_profile_to_scene",
03961:             "line": 72,
03962:             "args": [
03963:               "scene",
03964:               "profile"
03965:             ],
03966:             "async": false
03967:           },
03968:           {
03969:             "name": "configure_existing_render",
03970:             "line": 201,
03971:             "args": [
03972:               "scene",
03973:               "meta"
03974:             ],
03975:             "async": false
03976:           }
03977:         ],
03978:         "classes": [],
03979:         "assignments": []
03980:       }
03981:     },
03982:     {
03983:       "file": "Scripting/v61b/hotpatch/runner.py",
03984:       "exists": true,
03985:       "suffix": ".py",
03986:       "lines": 104,
03987:       "chars": 3026,
03988:       "sha256": "938c367a2ea774376d12815124f8c755672d67578d5ae8c1bfb6c69e9379b074",
03989:       "symbols": {
03990:         "imports": [
03991:           "bpy",
03992:           "from accent_patch import update_physics_accents",
03993:           "from common import load_analysis",
03994:           "from fog_patch import update_fog",
03995:           "from hero_material_patch import patch_hero_materials",
03996:           "from lighting_patch import remove_legacy_rhythm_objects, update_area_lights, update_backdrop, update_world",
03997:           "from render_patch import configure_existing_render",
03998:           "from spaziotempo.core.collections import classify_scene_objects, compact_structure_summary"
03999:         ],
04000:         "functions": [
04001:           {
04002:             "name": "print_result",
04003:             "line": 17,
04004:             "args": [
04005:               "title",
04006:               "result"
04007:             ],
04008:             "async": false
04009:           },
04010:           {
04011:             "name": "run_hotpatch",
04012:             "line": 41,
04013:             "args": [
04014:               "mode"
04015:             ],
04016:             "async": false
04017:           },
04018:           {
04019:             "name": "run_all",
04020:             "line": 102,
04021:             "args": [],
04022:             "async": false
04023:           }
04024:         ],
04025:         "classes": [],
04026:         "assignments": []
04027:       }
04028:     },
04029:     {
04030:       "file": "Scripting/v61b/spaziotempo/__init__.py",
04031:       "exists": true,
04032:       "suffix": ".py",
04033:       "lines": 5,
04034:       "chars": 128,
04035:       "sha256": "b4c134fb5b10b26b42246d0fb626a393396d9ce775a0a7183c8754fd5b85387c",
04036:       "symbols": {
04037:         "imports": [],
04038:         "functions": [],
04039:         "classes": [],
04040:         "assignments": [
04041:           "PROJECT_SLUG",
04042:           "PROJECT_VERSION"
04043:         ]
04044:       }
04045:     },
04046:     {
04047:       "file": "Scripting/v61b/spaziotempo/core/__init__.py",
04048:       "exists": true,
04049:       "suffix": ".py",
04050:       "lines": 2,
04051:       "chars": 41,
04052:       "sha256": "3d9532a93d330048ac9408aa2c49adbfb3263e6e950b10fe579a330b5e8f4925",
04053:       "symbols": {
04054:         "imports": [],
04055:         "functions": [],
04056:         "classes": [],
04057:         "assignments": []
04058:       }
04059:     },
04060:     {
04061:       "file": "Scripting/v61b/spaziotempo/core/collections.py",
04062:       "exists": true,
04063:       "suffix": ".py",
04064:       "lines": 133,
04065:       "chars": 3958,
04066:       "sha256": "2cf178afbdd5d808c520edd44d2e4c80eaa671480e65b571adb9b798f9df808b",
04067:       "symbols": {
04068:         "imports": [
04069:           "bpy",
04070:           "from registry import EXACT_OBJECT_LAYERS, LAYER_ORDER, LAYER_SPECS, PARENT_LAYER_HINTS, PREFIX_OBJECT_LAYERS, PROJECT_ROOT_COLLECTION, STRUCTURE_VERSION, TYPE_FALLBACK_LAYERS"
04071:         ],
04072:         "functions": [
04073:           {
04074:             "name": "_children_by_name",
04075:             "line": 17,
04076:             "args": [
04077:               "collection"
04078:             ],
04079:             "async": false
04080:           },
04081:           {
04082:             "name": "_objects_by_name",
04083:             "line": 21,
04084:             "args": [
04085:               "collection"
04086:             ],
04087:             "async": false
04088:           },
04089:           {
04090:             "name": "ensure_child_collection",
04091:             "line": 25,
04092:             "args": [
04093:               "parent",
04094:               "name"
04095:             ],
04096:             "async": false
04097:           },
04098:           {
04099:             "name": "ensure_project_collections",
04100:             "line": 33,
04101:             "args": [
04102:               "scene",
04103:               "include_reserved"
04104:             ],
04105:             "async": false
04106:           },
04107:           {
04108:             "name": "_parent_hint",
04109:             "line": 54,
04110:             "args": [
04111:               "obj"
```
