# Project Code Chunk 111/212

- File: `Scripting/v61b_backgood/scene_utils.py`
- Part: `1`
- Lines: `1-97`

## Symbol Map
- Imports: `bpy`
- Functions: `clear_scene()` line 4; `deselect_all()` line 29; `safe_active(obj)` line 33; `create_controller_empty(name, location, parent, display_size, hide_view)` line 38; `iter_action_fcurves(action)` line 53; `set_linear_interpolation_idblock(idblock)` line 83

## Content
```py
00001: import bpy
00002: 
00003: 
00004: def clear_scene():
00005:     bpy.ops.object.select_all(action='SELECT')
00006:     bpy.ops.object.delete(use_global=False)
00007: 
00008:     datablocks = [
00009:         bpy.data.meshes,
00010:         bpy.data.materials,
00011:         bpy.data.lights,
00012:         bpy.data.cameras,
00013:         bpy.data.curves,
00014:         bpy.data.actions,
00015:         bpy.data.images,
00016:         bpy.data.worlds,
00017:         bpy.data.collections,
00018:     ]
00019: 
00020:     for collection in datablocks:
00021:         for block in list(collection):
00022:             try:
00023:                 if block.users == 0:
00024:                     collection.remove(block)
00025:             except Exception:
00026:                 pass
00027: 
00028: 
00029: def deselect_all():
00030:     bpy.ops.object.select_all(action='DESELECT')
00031: 
00032: 
00033: def safe_active(obj):
00034:     bpy.context.view_layer.objects.active = obj
00035:     obj.select_set(True)
00036: 
00037: 
00038: def create_controller_empty(name, location=(0, 0, 0), parent=None, display_size=0.25, hide_view=True):
00039:     bpy.ops.object.empty_add(type='PLAIN_AXES', location=location)
00040:     obj = bpy.context.active_object
00041:     obj.name = name
00042:     obj.empty_display_size = display_size
00043:     obj.hide_render = True
00044:     obj.hide_select = True
00045:     obj.hide_viewport = hide_view
00046: 
00047:     if parent is not None:
00048:         obj.parent = parent
00049: 
00050:     return obj
00051: 
00052: 
00053: def iter_action_fcurves(action):
00054:     if action is None:
00055:         return
00056: 
00057:     if hasattr(action, "fcurves"):
00058:         try:
00059:             for fc in action.fcurves:
00060:                 yield fc
00061:             return
00062:         except Exception:
00063:             pass
00064: 
00065:     layers = getattr(action, "layers", None)
00066:     if layers:
00067:         for layer in layers:
00068:             strips = getattr(layer, "strips", None)
00069:             if not strips:
00070:                 continue
00071:             for strip in strips:
00072:                 channelbags = getattr(strip, "channelbags", None)
00073:                 if not channelbags:
00074:                     continue
00075:                 for channelbag in channelbags:
00076:                     fcurves = getattr(channelbag, "fcurves", None)
00077:                     if not fcurves:
00078:                         continue
00079:                     for fc in fcurves:
00080:                         yield fc
00081: 
00082: 
00083: def set_linear_interpolation_idblock(idblock):
00084:     if idblock is None:
00085:         return
00086: 
00087:     anim = getattr(idblock, "animation_data", None)
00088:     if not anim:
00089:         return
00090: 
00091:     action = getattr(anim, "action", None)
00092:     if not action:
00093:         return
00094: 
00095:     for fcurve in iter_action_fcurves(action):
00096:         for kp in getattr(fcurve, "keyframe_points", []):
00097:             kp.interpolation = "LINEAR"
```
