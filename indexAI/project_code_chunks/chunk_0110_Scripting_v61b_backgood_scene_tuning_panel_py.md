# Project Code Chunk 110/212

- File: `Scripting/v61b_backgood/scene_tuning_panel.py`
- Part: `5`
- Lines: `1039-1097`

## Symbol Map
- Imports: `json`, `traceback`, `from pathlib import Path`, `bpy`, `from bpy.props import BoolProperty, FloatProperty, PointerProperty, StringProperty`
- Classes: `ST_TuningSettings` line 754; `ST_OT_apply_tuning` line 806 methods: execute; `ST_OT_keyframe_tuning` line 817 methods: execute; `ST_OT_scale_animation` line 828 methods: execute; `ST_OT_apply_runtime_profile` line 839 methods: execute; `ST_OT_hot_update_scene` line 855 methods: execute; `ST_OT_save_preset` line 877 methods: execute; `ST_OT_load_preset` line 888 methods: execute; `ST_OT_open_guide_text` line 904 methods: execute; `ST_OT_select_group` line 923 methods: execute; `ST_PT_tuning_panel` line 958 methods: draw
- Functions: `resolve_script_dir()` line 19; `iter_action_fcurves(action)` line 50; `find_obj(name)` line 82; `objects_with_prefix(prefix)` line 86; `particle_emitters()` line 90; `particle_source_objects()` line 100; `store_base_vector(obj, key, value)` line 111; `store_base_float(idblock, key, value)` line 117; `set_scale_from_base(obj, factor, key)` line 126; `keyframe_if_possible(idblock, data_path, frame)` line 134; `find_material(name)` line 141; `find_node(material_name, node_name)` line 145; `set_value_node(material_name, node_name, value)` line 152; `set_input_node(material_name, node_name, input_name, value)` line 163; `keyframe_socket(socket, frame)` line 174; `get_scene_compositor_tree(scene)` line 180; `clamp_value(value, min_value, max_value)` line 188; `normalize_runtime_profile(profile)` line 192; `runtime_profile_label(profile)` line 238; `apply_runtime_profile(context, profile)` line 251; `all_particle_settings()` line 426; `apply_tuning(context, insert_keyframes)` line 438; `scale_fcurve_values(idblock, predicate, factor)` line 653; `scale_full_animation(context)` line 669; `preset_data(settings)` line 705; `load_preset_data(settings, data)` line 748; `register()` line 1074; `unregister()` line 1089
- Assignments: `bl_info`, `SCRIPT_DIR`, `PRESET_PATH`, `GUIDE_PATH`, `HOT_UPDATE_PATH`, `classes`

## Content
```py
01039:         box.prop(tune, "motion_blur")
01040:         box.prop(tune, "rhythm_light_power")
01041:         box.prop(tune, "compositor_glow")
01042:         box.prop(tune, "compositor_lens")
01043: 
01044:         box = layout.box()
01045:         box.label(text="Scale Existing Animation")
01046:         box.prop(tune, "anim_hero_deform_factor")
01047:         box.prop(tune, "anim_aura_factor")
01048:         box.operator("spaziotempo.scale_animation", icon='GRAPH')
01049: 
01050:         box = layout.box()
01051:         box.label(text="Select")
01052:         row = box.row(align=True)
01053:         op = row.operator("spaziotempo.select_group", text="Hero")
01054:         op.group = "hero"
01055:         op = row.operator("spaziotempo.select_group", text="Fog")
01056:         op.group = "fog"
01057: 
01058: 
01059: classes = (
01060:     ST_TuningSettings,
01061:     ST_OT_apply_tuning,
01062:     ST_OT_keyframe_tuning,
01063:     ST_OT_scale_animation,
01064:     ST_OT_apply_runtime_profile,
01065:     ST_OT_hot_update_scene,
01066:     ST_OT_save_preset,
01067:     ST_OT_load_preset,
01068:     ST_OT_open_guide_text,
01069:     ST_OT_select_group,
01070:     ST_PT_tuning_panel,
01071: )
01072: 
01073: 
01074: def register():
01075:     if hasattr(bpy.types.Scene, "spaziotempo_tuning"):
01076:         del bpy.types.Scene.spaziotempo_tuning
01077: 
01078:     for cls in reversed(classes):
01079:         try:
01080:             bpy.utils.unregister_class(cls)
01081:         except Exception:
01082:             pass
01083: 
01084:     for cls in classes:
01085:         bpy.utils.register_class(cls)
01086:     bpy.types.Scene.spaziotempo_tuning = PointerProperty(type=ST_TuningSettings)
01087: 
01088: 
01089: def unregister():
01090:     if hasattr(bpy.types.Scene, "spaziotempo_tuning"):
01091:         del bpy.types.Scene.spaziotempo_tuning
01092:     for cls in reversed(classes):
01093:         bpy.utils.unregister_class(cls)
01094: 
01095: 
01096: if __name__ == "__main__":
01097:     register()
```
