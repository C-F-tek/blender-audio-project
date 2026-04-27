# Project Code Chunk 61/212

- File: `Scripting/v61b/scene_tuning_panel.py`
- Part: `5`
- Lines: `1038-1262`

## Symbol Map
- Imports: `json`, `sys`, `traceback`, `from pathlib import Path`, `bpy`, `from bpy.props import BoolProperty, FloatProperty, PointerProperty, StringProperty`
- Classes: `ST_TuningSettings` line 770; `ST_OT_apply_tuning` line 822 methods: execute; `ST_OT_keyframe_tuning` line 833 methods: execute; `ST_OT_scale_animation` line 844 methods: execute; `ST_OT_apply_runtime_profile` line 855 methods: execute; `ST_OT_hot_update_scene` line 871 methods: execute; `ST_OT_rebuild_restart_check` line 895 methods: execute; `ST_OT_optimizer_check` line 920 methods: execute; `ST_OT_load_image_sequence` line 943 methods: execute; `ST_OT_encode_ffmpeg` line 965 methods: execute; `ST_OT_encode_ffmpeg_shell` line 987 methods: execute; `ST_OT_save_preset` line 1016 methods: execute; `ST_OT_load_preset` line 1027 methods: execute; `ST_OT_open_guide_text` line 1043 methods: execute; `ST_OT_select_group` line 1062 methods: execute; `ST_PT_tuning_panel` line 1098 methods: draw
- Functions: `resolve_script_dir()` line 20; `iter_action_fcurves(action)` line 56; `find_obj(name)` line 88; `objects_with_prefix(prefix)` line 92; `particle_emitters()` line 96; `particle_source_objects()` line 106; `store_base_vector(obj, key, value)` line 117; `store_base_float(idblock, key, value)` line 123; `set_scale_from_base(obj, factor, key)` line 132; `keyframe_if_possible(idblock, data_path, frame)` line 140; `find_material(name)` line 147; `find_node(material_name, node_name)` line 151; `set_value_node(material_name, node_name, value)` line 158; `set_input_node(material_name, node_name, input_name, value)` line 169; `keyframe_socket(socket, frame)` line 180; `get_scene_compositor_tree(scene)` line 186; `clamp_value(value, min_value, max_value)` line 194; `normalize_runtime_profile(profile)` line 198; `runtime_profile_label(profile)` line 244; `apply_runtime_profile(context, profile)` line 257; `all_particle_settings()` line 442; `apply_tuning(context, insert_keyframes)` line 454; `scale_fcurve_values(idblock, predicate, factor)` line 669; `scale_full_animation(context)` line 685; `preset_data(settings)` line 721; `load_preset_data(settings, data)` line 764; `register()` line 1239; `unregister()` line 1254
- Assignments: `bl_info`, `SCRIPT_DIR`, `PRESET_PATH`, `GUIDE_PATH`, `HOT_UPDATE_PATH`, `ENCODE_SEQUENCE_PATH`, `ENCODE_FFMPEG_PATH`, `classes`

## Content
```py
01038:         apply_tuning(context, insert_keyframes=False)
01039:         self.report({'INFO'}, "Preset loaded and applied.")
01040:         return {'FINISHED'}
01041: 
01042: 
01043: class ST_OT_open_guide_text(bpy.types.Operator):
01044:     bl_idname = "spaziotempo.open_tuning_guide"
01045:     bl_label = "Open Editable Guide"
01046: 
01047:     def execute(self, context):
01048:         text_name = "SPAZIOTEMPO_TUNING_GUIDE"
01049:         guide = bpy.data.texts.get(text_name) or bpy.data.texts.new(text_name)
01050: 
01051:         if GUIDE_PATH.exists():
01052:             body = GUIDE_PATH.read_text(encoding="utf-8")
01053:         else:
01054:             body = "Spaziotempo tuning guide not found."
01055: 
01056:         guide.clear()
01057:         guide.write(body)
01058:         self.report({'INFO'}, f"Guide opened as Blender text block: {text_name}")
01059:         return {'FINISHED'}
01060: 
01061: 
01062: class ST_OT_select_group(bpy.types.Operator):
01063:     bl_idname = "spaziotempo.select_group"
01064:     bl_label = "Select Scene Group"
01065: 
01066:     group: bpy.props.StringProperty(default="hero")
01067: 
01068:     def execute(self, context):
01069:         bpy.ops.object.select_all(action='DESELECT')
01070: 
01071:         names = []
01072:         if self.group == "hero":
01073:             names = ["HeroRoot", "HeroDeformController", "AuraAudioSampler"]
01074:         elif self.group == "particles":
01075:             names = [obj.name for obj in particle_emitters()]
01076:         elif self.group == "fog":
01077:             names = ["AtmosphereCube", "FogPulseController", "FogFilamentsRoot", "SoftRhythmBackdrop", "BackdropPulseController"]
01078:             names.extend(obj.name for obj in objects_with_prefix("FogFilament_"))
01079:         elif self.group == "letters":
01080:             names = ["AlbumLetterParticleSources"]
01081:             names.extend(obj.name for obj in objects_with_prefix("AlbumLetterParticle_"))
01082: 
01083:         selected = []
01084:         for name in names:
01085:             obj = find_obj(name)
01086:             if obj is None:
01087:                 continue
01088:             obj.hide_viewport = False
01089:             obj.select_set(True)
01090:             selected.append(obj)
01091: 
01092:         if selected:
01093:             context.view_layer.objects.active = selected[0]
01094:         self.report({'INFO'}, f"Selected {len(selected)} objects.")
01095:         return {'FINISHED'}
01096: 
01097: 
01098: class ST_PT_tuning_panel(bpy.types.Panel):
01099:     bl_label = "Scene Tuner"
01100:     bl_idname = "ST_PT_tuning_panel"
01101:     bl_space_type = 'VIEW_3D'
01102:     bl_region_type = 'UI'
01103:     bl_category = "Spaziotempo"
01104: 
01105:     def draw(self, context):
01106:         layout = self.layout
01107:         tune = context.scene.spaziotempo_tuning
01108: 
01109:         row = layout.row(align=True)
01110:         row.operator("spaziotempo.apply_tuning", icon='CHECKMARK')
01111:         row.operator("spaziotempo.keyframe_tuning", icon='KEY_HLT')
01112: 
01113:         box = layout.box()
01114:         box.label(text="Hot Update")
01115:         row = box.row(align=True)
01116:         op = row.operator("spaziotempo.hot_update_scene", text="Render Only", icon='OUTPUT')
01117:         op.mode = "RENDER"
01118:         op = row.operator("spaziotempo.hot_update_scene", text="Materials", icon='MATERIAL')
01119:         op.mode = "MATERIALS"
01120:         row = box.row(align=True)
01121:         op = row.operator("spaziotempo.hot_update_scene", text="Fog", icon='MOD_FLUIDSIM')
01122:         op.mode = "FOG"
01123:         op = row.operator("spaziotempo.hot_update_scene", text="Physics", icon='PHYSICS')
01124:         op.mode = "PHYSICS"
01125:         op = box.operator("spaziotempo.hot_update_scene", text="Hot Update All", icon='FILE_REFRESH')
01126:         op.mode = "ALL"
01127: 
01128:         row = box.row(align=True)
01129:         row.operator("spaziotempo.rebuild_restart_check", icon='VIEWZOOM')
01130:         row.operator("spaziotempo.optimizer_check", icon='SETTINGS')
01131: 
01132:         row = layout.row(align=True)
01133:         row.operator("spaziotempo.save_tuning_preset", icon='FILE_TICK')
01134:         row.operator("spaziotempo.load_tuning_preset", icon='FILE_REFRESH')
01135: 
01136:         layout.operator("spaziotempo.open_tuning_guide", icon='TEXT')
01137: 
01138:         box = layout.box()
01139:         box.label(text="Hero / Aura")
01140:         box.prop(tune, "hero_scale")
01141:         box.prop(tune, "hero_deform")
01142:         box.prop(tune, "hero_fine_deform")
01143:         box.prop(tune, "hero_wave")
01144:         box.prop(tune, "hero_twist")
01145:         box.prop(tune, "hero_mat_emission")
01146:         box.prop(tune, "hero_mat_bump")
01147:         box.prop(tune, "hero_mat_roughness")
01148:         box.prop(tune, "hero_mat_noise")
01149:         box.prop(tune, "aura_deform")
01150:         box.prop(tune, "aura_detail")
01151:         box.prop(tune, "aura_pulse")
01152: 
01153:         box = layout.box()
01154:         box.label(text="Fog")
01155:         box.prop(tune, "fog_density")
01156:         box.prop(tune, "fog_emission")
01157:         box.prop(tune, "fog_noise_scale")
01158:         box.prop(tune, "fog_scale_xy")
01159:         box.prop(tune, "fog_scale_z")
01160:         box.prop(tune, "show_fog_cube")
01161: 
01162:         box = layout.box()
01163:         box.label(text="Backdrop / Floor")
01164:         box.prop(tune, "backdrop_emission")
01165:         box.prop(tune, "backdrop_noise_scale")
01166:         box.prop(tune, "backdrop_scale")
01167:         box.prop(tune, "floor_scale")
01168:         box.prop(tune, "show_backdrop")
01169:         box.prop(tune, "render_backdrop")
01170:         box.prop(tune, "show_floor")
01171:         box.prop(tune, "render_floor")
01172: 
01173:         box = layout.box()
01174:         box.label(text="Camera / Render")
01175:         row = box.row(align=True)
01176:         op = row.operator("spaziotempo.apply_runtime_profile", text="Preview")
01177:         op.profile = "PREVIEW"
01178:         op = row.operator("spaziotempo.apply_runtime_profile", text="YT Fast 1080p")
01179:         op.profile = "YOUTUBE_FAST_1080P"
01180:         row = box.row(align=True)
01181:         op = row.operator("spaziotempo.apply_runtime_profile", text="YT Fast 1440p")
01182:         op.profile = "YOUTUBE_FAST_1440P"
01183:         op = row.operator("spaziotempo.apply_runtime_profile", text="YT Fast 4K")
01184:         op.profile = "YOUTUBE_FAST_4K"
01185:         row = box.row(align=True)
01186:         op = row.operator("spaziotempo.apply_runtime_profile", text="YT Final 1080p")
01187:         op.profile = "YOUTUBE_1080P"
01188:         op = row.operator("spaziotempo.apply_runtime_profile", text="YT Final 1440p")
01189:         op.profile = "YOUTUBE_1440P"
01190:         row = box.row(align=True)
01191:         op = row.operator("spaziotempo.apply_runtime_profile", text="YT Final 4K")
01192:         op.profile = "YOUTUBE_4K"
01193:         box.prop(tune, "runtime_profile")
01194:         box.prop(tune, "youtube_final")
01195:         box.prop(tune, "camera_fstop")
01196:         box.prop(tune, "motion_blur")
01197:         box.prop(tune, "rhythm_light_power")
01198:         box.prop(tune, "compositor_glow")
01199:         box.prop(tune, "compositor_lens")
01200:         box.operator("spaziotempo.load_image_sequence", text="Load Frames + Audio", icon='FILE_MOVIE')
01201:         box.operator("spaziotempo.encode_ffmpeg", text="Encode MP4 FFmpeg", icon='FILE_MOVIE')
01202:         box.operator("spaziotempo.encode_ffmpeg_shell", text="Encode FFmpeg Shell", icon='CONSOLE')
01203: 
01204:         box = layout.box()
01205:         box.label(text="Scale Existing Animation")
01206:         box.prop(tune, "anim_hero_deform_factor")
01207:         box.prop(tune, "anim_aura_factor")
01208:         box.operator("spaziotempo.scale_animation", icon='GRAPH')
01209: 
01210:         box = layout.box()
01211:         box.label(text="Select")
01212:         row = box.row(align=True)
01213:         op = row.operator("spaziotempo.select_group", text="Hero")
01214:         op.group = "hero"
01215:         op = row.operator("spaziotempo.select_group", text="Fog")
01216:         op.group = "fog"
01217: 
01218: 
01219: classes = (
01220:     ST_TuningSettings,
01221:     ST_OT_apply_tuning,
01222:     ST_OT_keyframe_tuning,
01223:     ST_OT_scale_animation,
01224:     ST_OT_apply_runtime_profile,
01225:     ST_OT_hot_update_scene,
01226:     ST_OT_rebuild_restart_check,
01227:     ST_OT_optimizer_check,
01228:     ST_OT_load_image_sequence,
01229:     ST_OT_encode_ffmpeg,
01230:     ST_OT_encode_ffmpeg_shell,
01231:     ST_OT_save_preset,
01232:     ST_OT_load_preset,
01233:     ST_OT_open_guide_text,
01234:     ST_OT_select_group,
01235:     ST_PT_tuning_panel,
01236: )
01237: 
01238: 
01239: def register():
01240:     if hasattr(bpy.types.Scene, "spaziotempo_tuning"):
01241:         del bpy.types.Scene.spaziotempo_tuning
01242: 
01243:     for cls in reversed(classes):
01244:         try:
01245:             bpy.utils.unregister_class(cls)
01246:         except Exception:
01247:             pass
01248: 
01249:     for cls in classes:
01250:         bpy.utils.register_class(cls)
01251:     bpy.types.Scene.spaziotempo_tuning = PointerProperty(type=ST_TuningSettings)
01252: 
01253: 
01254: def unregister():
01255:     if hasattr(bpy.types.Scene, "spaziotempo_tuning"):
01256:         del bpy.types.Scene.spaziotempo_tuning
01257:     for cls in reversed(classes):
01258:         bpy.utils.unregister_class(cls)
01259: 
01260: 
01261: if __name__ == "__main__":
01262:     register()
```
