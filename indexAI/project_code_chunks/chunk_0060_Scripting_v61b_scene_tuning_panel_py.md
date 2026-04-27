# Project Code Chunk 60/212

- File: `Scripting/v61b/scene_tuning_panel.py`
- Part: `4`
- Lines: `793-1037`

## Symbol Map
- Imports: `json`, `sys`, `traceback`, `from pathlib import Path`, `bpy`, `from bpy.props import BoolProperty, FloatProperty, PointerProperty, StringProperty`
- Classes: `ST_TuningSettings` line 770; `ST_OT_apply_tuning` line 822 methods: execute; `ST_OT_keyframe_tuning` line 833 methods: execute; `ST_OT_scale_animation` line 844 methods: execute; `ST_OT_apply_runtime_profile` line 855 methods: execute; `ST_OT_hot_update_scene` line 871 methods: execute; `ST_OT_rebuild_restart_check` line 895 methods: execute; `ST_OT_optimizer_check` line 920 methods: execute; `ST_OT_load_image_sequence` line 943 methods: execute; `ST_OT_encode_ffmpeg` line 965 methods: execute; `ST_OT_encode_ffmpeg_shell` line 987 methods: execute; `ST_OT_save_preset` line 1016 methods: execute; `ST_OT_load_preset` line 1027 methods: execute; `ST_OT_open_guide_text` line 1043 methods: execute; `ST_OT_select_group` line 1062 methods: execute; `ST_PT_tuning_panel` line 1098 methods: draw
- Functions: `resolve_script_dir()` line 20; `iter_action_fcurves(action)` line 56; `find_obj(name)` line 88; `objects_with_prefix(prefix)` line 92; `particle_emitters()` line 96; `particle_source_objects()` line 106; `store_base_vector(obj, key, value)` line 117; `store_base_float(idblock, key, value)` line 123; `set_scale_from_base(obj, factor, key)` line 132; `keyframe_if_possible(idblock, data_path, frame)` line 140; `find_material(name)` line 147; `find_node(material_name, node_name)` line 151; `set_value_node(material_name, node_name, value)` line 158; `set_input_node(material_name, node_name, input_name, value)` line 169; `keyframe_socket(socket, frame)` line 180; `get_scene_compositor_tree(scene)` line 186; `clamp_value(value, min_value, max_value)` line 194; `normalize_runtime_profile(profile)` line 198; `runtime_profile_label(profile)` line 244; `apply_runtime_profile(context, profile)` line 257; `all_particle_settings()` line 442; `apply_tuning(context, insert_keyframes)` line 454; `scale_fcurve_values(idblock, predicate, factor)` line 669; `scale_full_animation(context)` line 685; `preset_data(settings)` line 721; `load_preset_data(settings, data)` line 764; `register()` line 1239; `unregister()` line 1254
- Assignments: `bl_info`, `SCRIPT_DIR`, `PRESET_PATH`, `GUIDE_PATH`, `HOT_UPDATE_PATH`, `ENCODE_SEQUENCE_PATH`, `ENCODE_FFMPEG_PATH`, `classes`

## Content
```py
00793:     backdrop_scale: FloatProperty(name="Backdrop scale", default=1.0, min=0.20, max=2.40, precision=3)
00794:     floor_scale: FloatProperty(name="Floor scale", default=1.0, min=0.20, max=3.0, precision=3)
00795: 
00796:     camera_fstop: FloatProperty(name="Camera f-stop", default=6.5, min=1.0, max=16.0, precision=2)
00797:     rhythm_light_power: FloatProperty(name="Accent emission", default=1.0, min=0.0, max=4.0, precision=3)
00798:     compositor_glow: FloatProperty(name="Compositor glow", default=1.0, min=0.10, max=4.0, precision=3)
00799:     compositor_lens: FloatProperty(name="Compositor lens", default=1.0, min=0.0, max=4.0, precision=3)
00800: 
00801:     particle_size: FloatProperty(name="Particle size", default=1.0, min=0.05, max=5.0, precision=3)
00802:     particle_force: FloatProperty(name="Particle force", default=1.0, min=0.0, max=5.0, precision=3)
00803:     letter_source_scale: FloatProperty(name="Letter source scale", default=1.0, min=0.10, max=3.0, precision=3)
00804: 
00805:     anim_hero_deform_factor: FloatProperty(name="Anim hero deform", default=1.0, min=0.0, max=4.0, precision=3)
00806:     anim_aura_factor: FloatProperty(name="Anim aura", default=1.0, min=0.0, max=4.0, precision=3)
00807:     anim_particle_size_factor: FloatProperty(name="Anim particle size", default=1.0, min=0.05, max=5.0, precision=3)
00808:     anim_particle_force_factor: FloatProperty(name="Anim particle force", default=1.0, min=0.0, max=5.0, precision=3)
00809: 
00810:     show_fog_cube: BoolProperty(name="Show fog cube", default=False)
00811:     show_backdrop: BoolProperty(name="Show backdrop", default=True)
00812:     render_backdrop: BoolProperty(name="Render backdrop", default=True)
00813:     show_floor: BoolProperty(name="Show floor", default=True)
00814:     render_floor: BoolProperty(name="Render floor", default=False)
00815:     show_emitters: BoolProperty(name="Show emitters", default=False)
00816:     show_particle_sources: BoolProperty(name="Show source objects", default=False)
00817:     motion_blur: BoolProperty(name="Motion blur", default=False)
00818:     youtube_final: BoolProperty(name="YouTube final", default=False)
00819:     runtime_profile: StringProperty(name="Runtime profile", default="Preview")
00820: 
00821: 
00822: class ST_OT_apply_tuning(bpy.types.Operator):
00823:     bl_idname = "spaziotempo.apply_tuning"
00824:     bl_label = "Apply Live Values"
00825:     bl_options = {'REGISTER', 'UNDO'}
00826: 
00827:     def execute(self, context):
00828:         apply_tuning(context, insert_keyframes=False)
00829:         self.report({'INFO'}, "Spaziotempo tuning applied to current scene.")
00830:         return {'FINISHED'}
00831: 
00832: 
00833: class ST_OT_keyframe_tuning(bpy.types.Operator):
00834:     bl_idname = "spaziotempo.keyframe_tuning"
00835:     bl_label = "Apply + Keyframe"
00836:     bl_options = {'REGISTER', 'UNDO'}
00837: 
00838:     def execute(self, context):
00839:         apply_tuning(context, insert_keyframes=True)
00840:         self.report({'INFO'}, f"Spaziotempo values keyframed at frame {context.scene.frame_current}.")
00841:         return {'FINISHED'}
00842: 
00843: 
00844: class ST_OT_scale_animation(bpy.types.Operator):
00845:     bl_idname = "spaziotempo.scale_animation"
00846:     bl_label = "Scale Existing FCurves"
00847:     bl_options = {'REGISTER', 'UNDO'}
00848: 
00849:     def execute(self, context):
00850:         changed = scale_full_animation(context)
00851:         self.report({'INFO'}, f"Scaled {changed} keyframe values.")
00852:         return {'FINISHED'}
00853: 
00854: 
00855: class ST_OT_apply_runtime_profile(bpy.types.Operator):
00856:     bl_idname = "spaziotempo.apply_runtime_profile"
00857:     bl_label = "Apply Runtime Profile"
00858:     bl_options = {'REGISTER', 'UNDO'}
00859: 
00860:     final_for_youtube: bpy.props.BoolProperty(default=False)
00861:     profile: bpy.props.StringProperty(default="")
00862: 
00863:     def execute(self, context):
00864:         profile = self.profile or ("YOUTUBE_4K" if self.final_for_youtube else "PREVIEW")
00865:         apply_runtime_profile(context, profile)
00866:         label = runtime_profile_label(profile)
00867:         self.report({'INFO'}, f"{label} profile applied to current scene.")
00868:         return {'FINISHED'}
00869: 
00870: 
00871: class ST_OT_hot_update_scene(bpy.types.Operator):
00872:     bl_idname = "spaziotempo.hot_update_scene"
00873:     bl_label = "Hot Update Scene"
00874:     bl_options = {'REGISTER', 'UNDO'}
00875: 
00876:     mode: bpy.props.StringProperty(default="ALL")
00877: 
00878:     def execute(self, context):
00879:         if not HOT_UPDATE_PATH.exists():
00880:             self.report({'WARNING'}, f"Hot update script not found: {HOT_UPDATE_PATH}")
00881:             return {'CANCELLED'}
00882: 
00883:         try:
00884:             code = compile(HOT_UPDATE_PATH.read_text(encoding="utf-8"), str(HOT_UPDATE_PATH), "exec")
00885:             exec(code, {"__file__": str(HOT_UPDATE_PATH), "__name__": "__main__", "HOTPATCH_MODE": self.mode})
00886:         except Exception as exc:
00887:             traceback.print_exc()
00888:             self.report({'ERROR'}, f"Hot update failed: {exc}")
00889:             return {'CANCELLED'}
00890: 
00891:         self.report({'INFO'}, f"Hot update {self.mode} complete.")
00892:         return {'FINISHED'}
00893: 
00894: 
00895: class ST_OT_rebuild_restart_check(bpy.types.Operator):
00896:     bl_idname = "spaziotempo.rebuild_restart_check"
00897:     bl_label = "Rebuild / Restart Check"
00898:     bl_options = {'REGISTER'}
00899: 
00900:     def execute(self, context):
00901:         try:
00902:             sys.modules.pop("hotpatch.diagnostics", None)
00903:             from hotpatch.diagnostics import analyze_rebuild_need
00904: 
00905:             result = analyze_rebuild_need()
00906:         except Exception as exc:
00907:             traceback.print_exc()
00908:             self.report({'ERROR'}, f"Check failed: {exc}")
00909:             return {'CANCELLED'}
00910: 
00911:         if result["blocking"]:
00912:             self.report({'WARNING'}, "Full rebuild needed. See SPAZIOTEMPO_REBUILD_CHECK.")
00913:         elif result["restart"]:
00914:             self.report({'WARNING'}, "Registration issue found. See SPAZIOTEMPO_REBUILD_CHECK.")
00915:         else:
00916:             self.report({'INFO'}, "Hotpatch should be enough. See SPAZIOTEMPO_REBUILD_CHECK.")
00917:         return {'FINISHED'}
00918: 
00919: 
00920: class ST_OT_optimizer_check(bpy.types.Operator):
00921:     bl_idname = "spaziotempo.optimizer_check"
00922:     bl_label = "Optimizer Check"
00923:     bl_options = {'REGISTER'}
00924: 
00925:     def execute(self, context):
00926:         try:
00927:             sys.modules.pop("hotpatch.diagnostics", None)
00928:             from hotpatch.diagnostics import analyze_optimizer
00929: 
00930:             result = analyze_optimizer()
00931:         except Exception as exc:
00932:             traceback.print_exc()
00933:             self.report({'ERROR'}, f"Optimizer check failed: {exc}")
00934:             return {'CANCELLED'}
00935: 
00936:         if result["warnings"]:
00937:             self.report({'WARNING'}, "Cache/bake suggestions found. See SPAZIOTEMPO_OPTIMIZER_REPORT.")
00938:         else:
00939:             self.report({'INFO'}, "No required bake found. See SPAZIOTEMPO_OPTIMIZER_REPORT.")
00940:         return {'FINISHED'}
00941: 
00942: 
00943: class ST_OT_load_image_sequence(bpy.types.Operator):
00944:     bl_idname = "spaziotempo.load_image_sequence"
00945:     bl_label = "Load Image Sequence"
00946:     bl_options = {'REGISTER', 'UNDO'}
00947: 
00948:     def execute(self, context):
00949:         if not ENCODE_SEQUENCE_PATH.exists():
00950:             self.report({'WARNING'}, f"Image sequence script not found: {ENCODE_SEQUENCE_PATH}")
00951:             return {'CANCELLED'}
00952: 
00953:         try:
00954:             code = compile(ENCODE_SEQUENCE_PATH.read_text(encoding="utf-8"), str(ENCODE_SEQUENCE_PATH), "exec")
00955:             exec(code, {"__file__": str(ENCODE_SEQUENCE_PATH), "__name__": "__main__"})
00956:         except Exception as exc:
00957:             traceback.print_exc()
00958:             self.report({'ERROR'}, f"Image sequence load failed: {exc}")
00959:             return {'CANCELLED'}
00960: 
00961:         self.report({'INFO'}, "Image sequence + audio loaded in Video Sequencer.")
00962:         return {'FINISHED'}
00963: 
00964: 
00965: class ST_OT_encode_ffmpeg(bpy.types.Operator):
00966:     bl_idname = "spaziotempo.encode_ffmpeg"
00967:     bl_label = "Encode MP4 FFmpeg"
00968:     bl_options = {'REGISTER', 'UNDO'}
00969: 
00970:     def execute(self, context):
00971:         if not ENCODE_FFMPEG_PATH.exists():
00972:             self.report({'WARNING'}, f"FFmpeg encode script not found: {ENCODE_FFMPEG_PATH}")
00973:             return {'CANCELLED'}
00974: 
00975:         try:
00976:             code = compile(ENCODE_FFMPEG_PATH.read_text(encoding="utf-8"), str(ENCODE_FFMPEG_PATH), "exec")
00977:             exec(code, {"__file__": str(ENCODE_FFMPEG_PATH), "__name__": "__main__"})
00978:         except Exception as exc:
00979:             traceback.print_exc()
00980:             self.report({'ERROR'}, f"FFmpeg encode failed: {exc}")
00981:             return {'CANCELLED'}
00982: 
00983:         self.report({'INFO'}, "FFmpeg MP4 encoded from image sequence.")
00984:         return {'FINISHED'}
00985: 
00986: 
00987: class ST_OT_encode_ffmpeg_shell(bpy.types.Operator):
00988:     bl_idname = "spaziotempo.encode_ffmpeg_shell"
00989:     bl_label = "Encode MP4 FFmpeg Shell"
00990:     bl_options = {'REGISTER'}
00991: 
00992:     def execute(self, context):
00993:         if not ENCODE_FFMPEG_PATH.exists():
00994:             self.report({'WARNING'}, f"FFmpeg encode script not found: {ENCODE_FFMPEG_PATH}")
00995:             return {'CANCELLED'}
00996: 
00997:         try:
00998:             code = compile(ENCODE_FFMPEG_PATH.read_text(encoding="utf-8"), str(ENCODE_FFMPEG_PATH), "exec")
00999:             exec(
01000:                 code,
01001:                 {
01002:                     "__file__": str(ENCODE_FFMPEG_PATH),
01003:                     "__name__": "__main__",
01004:                     "FFMPEG_LAUNCH_VISIBLE_SHELL": True,
01005:                 },
01006:             )
01007:         except Exception as exc:
01008:             traceback.print_exc()
01009:             self.report({'ERROR'}, f"FFmpeg shell encode failed: {exc}")
01010:             return {'CANCELLED'}
01011: 
01012:         self.report({'INFO'}, "FFmpeg encode launched in external shell.")
01013:         return {'FINISHED'}
01014: 
01015: 
01016: class ST_OT_save_preset(bpy.types.Operator):
01017:     bl_idname = "spaziotempo.save_tuning_preset"
01018:     bl_label = "Save Preset"
01019: 
01020:     def execute(self, context):
01021:         data = preset_data(context.scene.spaziotempo_tuning)
01022:         PRESET_PATH.write_text(json.dumps(data, indent=2), encoding="utf-8")
01023:         self.report({'INFO'}, f"Preset saved: {PRESET_PATH}")
01024:         return {'FINISHED'}
01025: 
01026: 
01027: class ST_OT_load_preset(bpy.types.Operator):
01028:     bl_idname = "spaziotempo.load_tuning_preset"
01029:     bl_label = "Load Preset"
01030: 
01031:     def execute(self, context):
01032:         if not PRESET_PATH.exists():
01033:             self.report({'WARNING'}, f"Preset not found: {PRESET_PATH}")
01034:             return {'CANCELLED'}
01035: 
01036:         data = json.loads(PRESET_PATH.read_text(encoding="utf-8"))
01037:         load_preset_data(context.scene.spaziotempo_tuning, data)
```
