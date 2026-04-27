# Project Code Chunk 153/212

- File: `Tools/npu/npu_code_manifest.json`
- Part: `6`
- Lines: `1634-1964`

## Content
```json
01634:               "color",
01635:               "strength"
01636:             ],
01637:             "async": false
01638:           },
01639:           {
01640:             "name": "build_invisible_emitter_material",
01641:             "line": 82,
01642:             "args": [],
01643:             "async": false
01644:           },
01645:           {
01646:             "name": "get_material_node_socket",
01647:             "line": 106,
01648:             "args": [
01649:               "material",
01650:               "node_name",
01651:               "socket_name",
01652:               "is_output"
01653:             ],
01654:             "async": false
01655:           },
01656:           {
01657:             "name": "add_particle_collision",
01658:             "line": 121,
01659:             "args": [
01660:               "obj"
01661:             ],
01662:             "async": false
01663:           },
01664:           {
01665:             "name": "add_passive_rigidbody",
01666:             "line": 138,
01667:             "args": [
01668:               "obj"
01669:             ],
01670:             "async": false
01671:           },
01672:           {
01673:             "name": "add_active_rigidbody",
01674:             "line": 147,
01675:             "args": [
01676:               "obj",
01677:               "mass"
01678:             ],
01679:             "async": false
01680:           },
01681:           {
01682:             "name": "create_hidden_anchor",
01683:             "line": 159,
01684:             "args": [
01685:               "name",
01686:               "location"
01687:             ],
01688:             "async": false
01689:           },
01690:           {
01691:             "name": "create_spring_constraint",
01692:             "line": 172,
01693:             "args": [
01694:               "name",
01695:               "object1",
01696:               "object2",
01697:               "location"
01698:             ],
01699:             "async": false
01700:           },
01701:           {
01702:             "name": "create_particle_instance",
01703:             "line": 215,
01704:             "args": [
01705:               "name",
01706:               "color",
01707:               "strength",
01708:               "shape"
01709:             ],
01710:             "async": false
01711:           },
01712:           {
01713:             "name": "create_album_letter_particle_collection",
01714:             "line": 255,
01715:             "args": [
01716:               "parent"
01717:             ],
01718:             "async": false
01719:           },
01720:           {
01721:             "name": "create_particle_emitter",
01722:             "line": 339,
01723:             "args": [
01724:               "name",
01725:               "kind",
01726:               "invisible_mat"
01727:             ],
01728:             "async": false
01729:           },
01730:           {
01731:             "name": "configure_particle_system",
01732:             "line": 367,
01733:             "args": [
01734:               "emitter",
01735:               "name",
01736:               "instance_obj",
01737:               "count",
01738:               "lifetime",
01739:               "particle_size",
01740:               "normal_factor",
01741:               "tangent_factor",
01742:               "brownian_factor",
01743:               "damping",
01744:               "child_count",
01745:               "child_percent",
01746:               "instance_collection"
01747:             ],
01748:             "async": false
01749:           },
01750:           {
01751:             "name": "create_rhythm_particle_physics",
01752:             "line": 445,
01753:             "args": [
01754:               "parent"
01755:             ],
01756:             "async": false
01757:           },
01758:           {
01759:             "name": "create_physics_accents",
01760:             "line": 606,
01761:             "args": [
01762:               "parent"
01763:             ],
01764:             "async": false
01765:           }
01766:         ],
01767:         "classes": [],
01768:         "assignments": []
01769:       }
01770:     },
01771:     {
01772:       "file": "Scripting/v61b/fog_dynamics.py",
01773:       "exists": true,
01774:       "suffix": ".py",
01775:       "lines": 393,
01776:       "chars": 15491,
01777:       "sha256": "21628c1c0e713ecbdf20bcae478983798b2354f4ed6bb8e700cc2adad4c59b58",
01778:       "symbols": {
01779:         "imports": [
01780:           "math",
01781:           "from config import FOG_DENSITY_MIN, FOG_DENSITY_MAX, FOG_EMISSION_MIN, FOG_EMISSION_MAX, FOG_NOISE_SCALE_MIN, FOG_NOISE_SCALE_MAX, FOG_CLUMP_SCALE_MIN, FOG_CLUMP_SCALE_MAX, FOG_CLUMP_RAMP_LOW_BASE, FOG_CLUMP_RAMP_HIGH_BASE, FOG_CLUMP_WEIGHT_MIN, FOG_CLUMP_WEIGHT_MAX, FOG_RAMP_LOW_BASE, FOG_RAMP_HIGH_BASE, FOG_COMPACT_XY, FOG_EXPAND_Z, FOG_CONTROLLER_DRIFT, FOG_DRIFT_SPEED_X, FOG_DRIFT_SPEED_Y, FOG_DRIFT_SPEED_Z, FOG_WAVE_SCALE_MIN, FOG_WAVE_SCALE_MAX, FOG_WAVE_DISTORTION_MIN, FOG_WAVE_DISTORTION_MAX, FOG_WAVE_WEIGHT_MIN, FOG_WAVE_WEIGHT_MAX, FOG_WIND_SHEAR_X, FOG_WIND_SHEAR_Y, FOG_VOLUME_ENABLED, FOG_VOLUME_VIEWPORT_VISIBLE, FOG_FILAMENT_KEYFRAME_STEP, FOG_FILAMENT_ALPHA_MIN, FOG_FILAMENT_ALPHA_MAX, FOG_FILAMENT_EMISSION_MIN, FOG_FILAMENT_EMISSION_MAX, FOG_FILAMENT_WIND_DRIFT, FOG_FILAMENT_COMPACT_SCALE, FOG_FILAMENT_NOISE_SCALE_MIN, FOG_FILAMENT_NOISE_SCALE_MAX, FOG_FILAMENT_WAVE_SCALE_MIN, FOG_FILAMENT_WAVE_SCALE_MAX"
01782:         ],
01783:         "functions": [
01784:           {
01785:             "name": "clamp",
01786:             "line": 48,
01787:             "args": [
01788:               "value",
01789:               "low",
01790:               "high"
01791:             ],
01792:             "async": false
01793:           },
01794:           {
01795:             "name": "keyframe_if_possible",
01796:             "line": 52,
01797:             "args": [
01798:               "idblock",
01799:               "data_path",
01800:               "frame"
01801:             ],
01802:             "async": false
01803:           },
01804:           {
01805:             "name": "set_socket_value",
01806:             "line": 59,
01807:             "args": [
01808:               "socket",
01809:               "value",
01810:               "frame"
01811:             ],
01812:             "async": false
01813:           },
01814:           {
01815:             "name": "animate_vector_socket",
01816:             "line": 69,
01817:             "args": [
01818:               "socket",
01819:               "values",
01820:               "frame"
01821:             ],
01822:             "async": false
01823:           },
01824:           {
01825:             "name": "should_keyframe_filaments",
01826:             "line": 82,
01827:             "args": [
01828:               "frame",
01829:               "beat",
01830:               "onset"
01831:             ],
01832:             "async": false
01833:           },
01834:           {
01835:             "name": "animate_fog_filaments",
01836:             "line": 91,
01837:             "args": [
01838:               "frame",
01839:               "low",
01840:               "mid",
01841:               "high",
01842:               "onset",
01843:               "beat",
01844:               "pulse",
01845:               "filaments"
01846:             ],
01847:             "async": false
01848:           },
01849:           {
01850:             "name": "animate_fog_frame",
01851:             "line": 204,
01852:             "args": [
01853:               "frame",
01854:               "low",
01855:               "mid",
01856:               "high",
01857:               "onset",
01858:               "beat",
01859:               "pulse",
01860:               "fog_controller",
01861:               "fog_obj",
01862:               "fog_control",
01863:               "fog_base_scale",
01864:               "fog_base_loc"
01865:             ],
01866:             "async": false
01867:           }
01868:         ],
01869:         "classes": [],
01870:         "assignments": []
01871:       }
01872:     },
01873:     {
01874:       "file": "Scripting/v61b/fog_filaments.py",
01875:       "exists": true,
01876:       "suffix": ".py",
01877:       "lines": 160,
01878:       "chars": 4634,
01879:       "sha256": "2b1d13a0b254084944ce0df40028222be32a6f8e96b7133e42044ee64d94d901",
01880:       "symbols": {
01881:         "imports": [
01882:           "math",
01883:           "random",
01884:           "bpy",
01885:           "from mathutils import Euler, Vector",
01886:           "from config import FOG_FILAMENTS_ENABLED, FOG_FILAMENT_COUNT, FOG_FILAMENT_WIDTH_MIN, FOG_FILAMENT_WIDTH_MAX, FOG_FILAMENT_HEIGHT_MIN, FOG_FILAMENT_HEIGHT_MAX, FOG_FILAMENT_DEPTH_MIN, FOG_FILAMENT_DEPTH_MAX, FOG_FILAMENT_Z_MIN, FOG_FILAMENT_Z_MAX",
01887:           "from materials import build_fog_filament_material",
01888:           "from scene_utils import create_controller_empty"
01889:         ],
01890:         "functions": [
01891:           {
01892:             "name": "_store_base_transform",
01893:             "line": 28,
01894:             "args": [
01895:               "obj",
01896:               "phase"
01897:             ],
01898:             "async": false
01899:           },
01900:           {
01901:             "name": "_base_vector",
01902:             "line": 36,
01903:             "args": [
01904:               "obj",
01905:               "key",
01906:               "fallback"
01907:             ],
01908:             "async": false
01909:           },
01910:           {
01911:             "name": "_base_euler",
01912:             "line": 46,
01913:             "args": [
01914:               "obj",
01915:               "key",
01916:               "fallback"
01917:             ],
01918:             "async": false
01919:           },
01920:           {
01921:             "name": "_make_filament",
01922:             "line": 56,
01923:             "args": [
01924:               "index",
01925:               "material",
01926:               "parent"
01927:             ],
01928:             "async": false
01929:           },
01930:           {
01931:             "name": "_collect_objects",
01932:             "line": 90,
01933:             "args": [],
01934:             "async": false
01935:           },
01936:           {
01937:             "name": "ensure_fog_filaments",
01938:             "line": 95,
01939:             "args": [
01940:               "parent"
01941:             ],
01942:             "async": false
01943:           }
01944:         ],
01945:         "classes": [],
01946:         "assignments": [
01947:           "ROOT_NAME",
01948:           "OBJECT_PREFIX",
01949:           "MATERIAL_NAME"
01950:         ]
01951:       }
01952:     },
01953:     {
01954:       "file": "Scripting/v61b/atmosphere_setup.py",
01955:       "exists": true,
01956:       "suffix": ".py",
01957:       "lines": 555,
01958:       "chars": 16075,
01959:       "sha256": "bb571c0bdf08feacdb1649491e01709e6bb54938b3805fdd8796944ec87cd874",
01960:       "symbols": {
01961:         "imports": [
01962:           "bpy",
01963:           "math",
01964:           "random",
```
