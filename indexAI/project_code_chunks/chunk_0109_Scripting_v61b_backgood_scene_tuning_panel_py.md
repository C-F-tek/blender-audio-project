# Project Code Chunk 109/212

- File: `Scripting/v61b_backgood/scene_tuning_panel.py`
- Part: `4`
- Lines: `786-1038`

## Symbol Map
- Imports: `json`, `traceback`, `from pathlib import Path`, `bpy`, `from bpy.props import BoolProperty, FloatProperty, PointerProperty, StringProperty`
- Classes: `ST_TuningSettings` line 754; `ST_OT_apply_tuning` line 806 methods: execute; `ST_OT_keyframe_tuning` line 817 methods: execute; `ST_OT_scale_animation` line 828 methods: execute; `ST_OT_apply_runtime_profile` line 839 methods: execute; `ST_OT_hot_update_scene` line 855 methods: execute; `ST_OT_save_preset` line 877 methods: execute; `ST_OT_load_preset` line 888 methods: execute; `ST_OT_open_guide_text` line 904 methods: execute; `ST_OT_select_group` line 923 methods: execute; `ST_PT_tuning_panel` line 958 methods: draw
- Functions: `resolve_script_dir()` line 19; `iter_action_fcurves(action)` line 50; `find_obj(name)` line 82; `objects_with_prefix(prefix)` line 86; `particle_emitters()` line 90; `particle_source_objects()` line 100; `store_base_vector(obj, key, value)` line 111; `store_base_float(idblock, key, value)` line 117; `set_scale_from_base(obj, factor, key)` line 126; `keyframe_if_possible(idblock, data_path, frame)` line 134; `find_material(name)` line 141; `find_node(material_name, node_name)` line 145; `set_value_node(material_name, node_name, value)` line 152; `set_input_node(material_name, node_name, input_name, value)` line 163; `keyframe_socket(socket, frame)` line 174; `get_scene_compositor_tree(scene)` line 180; `clamp_value(value, min_value, max_value)` line 188; `normalize_runtime_profile(profile)` line 192; `runtime_profile_label(profile)` line 238; `apply_runtime_profile(context, profile)` line 251; `all_particle_settings()` line 426; `apply_tuning(context, insert_keyframes)` line 438; `scale_fcurve_values(idblock, predicate, factor)` line 653; `scale_full_animation(context)` line 669; `preset_data(settings)` line 705; `load_preset_data(settings, data)` line 748; `register()` line 1074; `unregister()` line 1089
- Assignments: `bl_info`, `SCRIPT_DIR`, `PRESET_PATH`, `GUIDE_PATH`, `HOT_UPDATE_PATH`, `classes`

## Content
```py
00786:     particle_force: FloatProperty(name="Particle force", default=1.0, min=0.0, max=5.0, precision=3)
00787:     letter_source_scale: FloatProperty(name="Letter source scale", default=1.0, min=0.10, max=3.0, precision=3)
00788: 
00789:     anim_hero_deform_factor: FloatProperty(name="Anim hero deform", default=1.0, min=0.0, max=4.0, precision=3)
00790:     anim_aura_factor: FloatProperty(name="Anim aura", default=1.0, min=0.0, max=4.0, precision=3)
00791:     anim_particle_size_factor: FloatProperty(name="Anim particle size", default=1.0, min=0.05, max=5.0, precision=3)
00792:     anim_particle_force_factor: FloatProperty(name="Anim particle force", default=1.0, min=0.0, max=5.0, precision=3)
00793: 
00794:     show_fog_cube: BoolProperty(name="Show fog cube", default=False)
00795:     show_backdrop: BoolProperty(name="Show backdrop", default=True)
00796:     render_backdrop: BoolProperty(name="Render backdrop", default=True)
00797:     show_floor: BoolProperty(name="Show floor", default=True)
00798:     render_floor: BoolProperty(name="Render floor", default=True)
00799:     show_emitters: BoolProperty(name="Show emitters", default=False)
00800:     show_particle_sources: BoolProperty(name="Show source objects", default=False)
00801:     motion_blur: BoolProperty(name="Motion blur", default=False)
00802:     youtube_final: BoolProperty(name="YouTube final", default=False)
00803:     runtime_profile: StringProperty(name="Runtime profile", default="Preview")
00804: 
00805: 
00806: class ST_OT_apply_tuning(bpy.types.Operator):
00807:     bl_idname = "spaziotempo.apply_tuning"
00808:     bl_label = "Apply Live Values"
00809:     bl_options = {'REGISTER', 'UNDO'}
00810: 
00811:     def execute(self, context):
00812:         apply_tuning(context, insert_keyframes=False)
00813:         self.report({'INFO'}, "Spaziotempo tuning applied to current scene.")
00814:         return {'FINISHED'}
00815: 
00816: 
00817: class ST_OT_keyframe_tuning(bpy.types.Operator):
00818:     bl_idname = "spaziotempo.keyframe_tuning"
00819:     bl_label = "Apply + Keyframe"
00820:     bl_options = {'REGISTER', 'UNDO'}
00821: 
00822:     def execute(self, context):
00823:         apply_tuning(context, insert_keyframes=True)
00824:         self.report({'INFO'}, f"Spaziotempo values keyframed at frame {context.scene.frame_current}.")
00825:         return {'FINISHED'}
00826: 
00827: 
00828: class ST_OT_scale_animation(bpy.types.Operator):
00829:     bl_idname = "spaziotempo.scale_animation"
00830:     bl_label = "Scale Existing FCurves"
00831:     bl_options = {'REGISTER', 'UNDO'}
00832: 
00833:     def execute(self, context):
00834:         changed = scale_full_animation(context)
00835:         self.report({'INFO'}, f"Scaled {changed} keyframe values.")
00836:         return {'FINISHED'}
00837: 
00838: 
00839: class ST_OT_apply_runtime_profile(bpy.types.Operator):
00840:     bl_idname = "spaziotempo.apply_runtime_profile"
00841:     bl_label = "Apply Runtime Profile"
00842:     bl_options = {'REGISTER', 'UNDO'}
00843: 
00844:     final_for_youtube: bpy.props.BoolProperty(default=False)
00845:     profile: bpy.props.StringProperty(default="")
00846: 
00847:     def execute(self, context):
00848:         profile = self.profile or ("YOUTUBE_4K" if self.final_for_youtube else "PREVIEW")
00849:         apply_runtime_profile(context, profile)
00850:         label = runtime_profile_label(profile)
00851:         self.report({'INFO'}, f"{label} profile applied to current scene.")
00852:         return {'FINISHED'}
00853: 
00854: 
00855: class ST_OT_hot_update_scene(bpy.types.Operator):
00856:     bl_idname = "spaziotempo.hot_update_scene"
00857:     bl_label = "Hot Update Scene"
00858:     bl_options = {'REGISTER', 'UNDO'}
00859: 
00860:     def execute(self, context):
00861:         if not HOT_UPDATE_PATH.exists():
00862:             self.report({'WARNING'}, f"Hot update script not found: {HOT_UPDATE_PATH}")
00863:             return {'CANCELLED'}
00864: 
00865:         try:
00866:             code = compile(HOT_UPDATE_PATH.read_text(encoding="utf-8"), str(HOT_UPDATE_PATH), "exec")
00867:             exec(code, {"__file__": str(HOT_UPDATE_PATH), "__name__": "__main__"})
00868:         except Exception as exc:
00869:             traceback.print_exc()
00870:             self.report({'ERROR'}, f"Hot update failed: {exc}")
00871:             return {'CANCELLED'}
00872: 
00873:         self.report({'INFO'}, "Hot update complete: fog/material/lights/accent refreshed.")
00874:         return {'FINISHED'}
00875: 
00876: 
00877: class ST_OT_save_preset(bpy.types.Operator):
00878:     bl_idname = "spaziotempo.save_tuning_preset"
00879:     bl_label = "Save Preset"
00880: 
00881:     def execute(self, context):
00882:         data = preset_data(context.scene.spaziotempo_tuning)
00883:         PRESET_PATH.write_text(json.dumps(data, indent=2), encoding="utf-8")
00884:         self.report({'INFO'}, f"Preset saved: {PRESET_PATH}")
00885:         return {'FINISHED'}
00886: 
00887: 
00888: class ST_OT_load_preset(bpy.types.Operator):
00889:     bl_idname = "spaziotempo.load_tuning_preset"
00890:     bl_label = "Load Preset"
00891: 
00892:     def execute(self, context):
00893:         if not PRESET_PATH.exists():
00894:             self.report({'WARNING'}, f"Preset not found: {PRESET_PATH}")
00895:             return {'CANCELLED'}
00896: 
00897:         data = json.loads(PRESET_PATH.read_text(encoding="utf-8"))
00898:         load_preset_data(context.scene.spaziotempo_tuning, data)
00899:         apply_tuning(context, insert_keyframes=False)
00900:         self.report({'INFO'}, "Preset loaded and applied.")
00901:         return {'FINISHED'}
00902: 
00903: 
00904: class ST_OT_open_guide_text(bpy.types.Operator):
00905:     bl_idname = "spaziotempo.open_tuning_guide"
00906:     bl_label = "Open Editable Guide"
00907: 
00908:     def execute(self, context):
00909:         text_name = "SPAZIOTEMPO_TUNING_GUIDE"
00910:         guide = bpy.data.texts.get(text_name) or bpy.data.texts.new(text_name)
00911: 
00912:         if GUIDE_PATH.exists():
00913:             body = GUIDE_PATH.read_text(encoding="utf-8")
00914:         else:
00915:             body = "Spaziotempo tuning guide not found."
00916: 
00917:         guide.clear()
00918:         guide.write(body)
00919:         self.report({'INFO'}, f"Guide opened as Blender text block: {text_name}")
00920:         return {'FINISHED'}
00921: 
00922: 
00923: class ST_OT_select_group(bpy.types.Operator):
00924:     bl_idname = "spaziotempo.select_group"
00925:     bl_label = "Select Scene Group"
00926: 
00927:     group: bpy.props.StringProperty(default="hero")
00928: 
00929:     def execute(self, context):
00930:         bpy.ops.object.select_all(action='DESELECT')
00931: 
00932:         names = []
00933:         if self.group == "hero":
00934:             names = ["HeroRoot", "HeroDeformController", "AuraAudioSampler"]
00935:         elif self.group == "particles":
00936:             names = [obj.name for obj in particle_emitters()]
00937:         elif self.group == "fog":
00938:             names = ["AtmosphereCube", "FogPulseController", "SoftRhythmBackdrop", "BackdropPulseController"]
00939:         elif self.group == "letters":
00940:             names = ["AlbumLetterParticleSources"]
00941:             names.extend(obj.name for obj in objects_with_prefix("AlbumLetterParticle_"))
00942: 
00943:         selected = []
00944:         for name in names:
00945:             obj = find_obj(name)
00946:             if obj is None:
00947:                 continue
00948:             obj.hide_viewport = False
00949:             obj.select_set(True)
00950:             selected.append(obj)
00951: 
00952:         if selected:
00953:             context.view_layer.objects.active = selected[0]
00954:         self.report({'INFO'}, f"Selected {len(selected)} objects.")
00955:         return {'FINISHED'}
00956: 
00957: 
00958: class ST_PT_tuning_panel(bpy.types.Panel):
00959:     bl_label = "Scene Tuner"
00960:     bl_idname = "ST_PT_tuning_panel"
00961:     bl_space_type = 'VIEW_3D'
00962:     bl_region_type = 'UI'
00963:     bl_category = "Spaziotempo"
00964: 
00965:     def draw(self, context):
00966:         layout = self.layout
00967:         tune = context.scene.spaziotempo_tuning
00968: 
00969:         row = layout.row(align=True)
00970:         row.operator("spaziotempo.apply_tuning", icon='CHECKMARK')
00971:         row.operator("spaziotempo.keyframe_tuning", icon='KEY_HLT')
00972: 
00973:         layout.operator("spaziotempo.hot_update_scene", icon='FILE_REFRESH')
00974: 
00975:         row = layout.row(align=True)
00976:         row.operator("spaziotempo.save_tuning_preset", icon='FILE_TICK')
00977:         row.operator("spaziotempo.load_tuning_preset", icon='FILE_REFRESH')
00978: 
00979:         layout.operator("spaziotempo.open_tuning_guide", icon='TEXT')
00980: 
00981:         box = layout.box()
00982:         box.label(text="Hero / Aura")
00983:         box.prop(tune, "hero_scale")
00984:         box.prop(tune, "hero_deform")
00985:         box.prop(tune, "hero_fine_deform")
00986:         box.prop(tune, "hero_wave")
00987:         box.prop(tune, "hero_twist")
00988:         box.prop(tune, "hero_mat_emission")
00989:         box.prop(tune, "hero_mat_bump")
00990:         box.prop(tune, "hero_mat_roughness")
00991:         box.prop(tune, "hero_mat_noise")
00992:         box.prop(tune, "aura_deform")
00993:         box.prop(tune, "aura_detail")
00994:         box.prop(tune, "aura_pulse")
00995: 
00996:         box = layout.box()
00997:         box.label(text="Fog")
00998:         box.prop(tune, "fog_density")
00999:         box.prop(tune, "fog_emission")
01000:         box.prop(tune, "fog_noise_scale")
01001:         box.prop(tune, "fog_scale_xy")
01002:         box.prop(tune, "fog_scale_z")
01003:         box.prop(tune, "show_fog_cube")
01004: 
01005:         box = layout.box()
01006:         box.label(text="Backdrop / Floor")
01007:         box.prop(tune, "backdrop_emission")
01008:         box.prop(tune, "backdrop_noise_scale")
01009:         box.prop(tune, "backdrop_scale")
01010:         box.prop(tune, "floor_scale")
01011:         box.prop(tune, "show_backdrop")
01012:         box.prop(tune, "render_backdrop")
01013:         box.prop(tune, "show_floor")
01014:         box.prop(tune, "render_floor")
01015: 
01016:         box = layout.box()
01017:         box.label(text="Camera / Render")
01018:         row = box.row(align=True)
01019:         op = row.operator("spaziotempo.apply_runtime_profile", text="Preview")
01020:         op.profile = "PREVIEW"
01021:         op = row.operator("spaziotempo.apply_runtime_profile", text="YT Fast 1080p")
01022:         op.profile = "YOUTUBE_FAST_1080P"
01023:         row = box.row(align=True)
01024:         op = row.operator("spaziotempo.apply_runtime_profile", text="YT Fast 1440p")
01025:         op.profile = "YOUTUBE_FAST_1440P"
01026:         op = row.operator("spaziotempo.apply_runtime_profile", text="YT Fast 4K")
01027:         op.profile = "YOUTUBE_FAST_4K"
01028:         row = box.row(align=True)
01029:         op = row.operator("spaziotempo.apply_runtime_profile", text="YT Final 1080p")
01030:         op.profile = "YOUTUBE_1080P"
01031:         op = row.operator("spaziotempo.apply_runtime_profile", text="YT Final 1440p")
01032:         op.profile = "YOUTUBE_1440P"
01033:         row = box.row(align=True)
01034:         op = row.operator("spaziotempo.apply_runtime_profile", text="YT Final 4K")
01035:         op.profile = "YOUTUBE_4K"
01036:         box.prop(tune, "runtime_profile")
01037:         box.prop(tune, "youtube_final")
01038:         box.prop(tune, "camera_fstop")
```
