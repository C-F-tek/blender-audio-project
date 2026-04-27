# Project Code Chunk 31/212

- File: `Scripting/v61b/fog_filaments.py`
- Part: `1`
- Lines: `1-159`

## Symbol Map
- Imports: `math`, `random`, `bpy`, `from mathutils import Euler, Vector`, `from config import FOG_FILAMENTS_ENABLED, FOG_FILAMENT_COUNT, FOG_FILAMENT_WIDTH_MIN, FOG_FILAMENT_WIDTH_MAX, FOG_FILAMENT_HEIGHT_MIN, FOG_FILAMENT_HEIGHT_MAX, FOG_FILAMENT_DEPTH_MIN, FOG_FILAMENT_DEPTH_MAX, FOG_FILAMENT_Z_MIN, FOG_FILAMENT_Z_MAX`, `from materials import build_fog_filament_material`, `from scene_utils import create_controller_empty`
- Functions: `_store_base_transform(obj, phase)` line 28; `_base_vector(obj, key, fallback)` line 36; `_base_euler(obj, key, fallback)` line 46; `_make_filament(index, material, parent)` line 56; `_collect_objects()` line 90; `ensure_fog_filaments(parent)` line 95
- Assignments: `ROOT_NAME`, `OBJECT_PREFIX`, `MATERIAL_NAME`

## Content
```py
00001: import math
00002: import random
00003: 
00004: import bpy
00005: from mathutils import Euler, Vector
00006: 
00007: from config import (
00008:     FOG_FILAMENTS_ENABLED,
00009:     FOG_FILAMENT_COUNT,
00010:     FOG_FILAMENT_WIDTH_MIN,
00011:     FOG_FILAMENT_WIDTH_MAX,
00012:     FOG_FILAMENT_HEIGHT_MIN,
00013:     FOG_FILAMENT_HEIGHT_MAX,
00014:     FOG_FILAMENT_DEPTH_MIN,
00015:     FOG_FILAMENT_DEPTH_MAX,
00016:     FOG_FILAMENT_Z_MIN,
00017:     FOG_FILAMENT_Z_MAX,
00018: )
00019: from materials import build_fog_filament_material
00020: from scene_utils import create_controller_empty
00021: 
00022: 
00023: ROOT_NAME = "FogFilamentsRoot"
00024: OBJECT_PREFIX = "FogFilament_"
00025: MATERIAL_NAME = "FogFilamentMaterial"
00026: 
00027: 
00028: def _store_base_transform(obj, phase):
00029:     obj["st_fog_filament"] = True
00030:     obj["st_phase"] = float(phase)
00031:     obj["st_base_location"] = [float(v) for v in obj.location]
00032:     obj["st_base_scale"] = [float(v) for v in obj.scale]
00033:     obj["st_base_rotation"] = [float(v) for v in obj.rotation_euler]
00034: 
00035: 
00036: def _base_vector(obj, key, fallback):
00037:     raw = obj.get(key)
00038:     if raw is None:
00039:         return fallback.copy()
00040:     try:
00041:         return Vector((float(raw[0]), float(raw[1]), float(raw[2])))
00042:     except Exception:
00043:         return fallback.copy()
00044: 
00045: 
00046: def _base_euler(obj, key, fallback):
00047:     raw = obj.get(key)
00048:     if raw is None:
00049:         return fallback.copy()
00050:     try:
00051:         return Euler((float(raw[0]), float(raw[1]), float(raw[2])), fallback.order)
00052:     except Exception:
00053:         return fallback.copy()
00054: 
00055: 
00056: def _make_filament(index, material, parent=None):
00057:     rng = random.Random(6100 + index * 37)
00058:     x = rng.uniform(-7.4, 7.4)
00059:     y = rng.uniform(FOG_FILAMENT_DEPTH_MIN, FOG_FILAMENT_DEPTH_MAX)
00060:     z = rng.uniform(FOG_FILAMENT_Z_MIN, FOG_FILAMENT_Z_MAX)
00061:     width = rng.uniform(FOG_FILAMENT_WIDTH_MIN, FOG_FILAMENT_WIDTH_MAX)
00062:     height = rng.uniform(FOG_FILAMENT_HEIGHT_MIN, FOG_FILAMENT_HEIGHT_MAX)
00063: 
00064:     bpy.ops.mesh.primitive_plane_add(
00065:         size=1.0,
00066:         location=(x, y, z),
00067:         rotation=(
00068:             math.radians(90.0 + rng.uniform(-4.0, 4.0)),
00069:             math.radians(rng.uniform(-4.0, 4.0)),
00070:             math.radians(rng.uniform(-8.0, 8.0)),
00071:         ),
00072:     )
00073:     obj = bpy.context.active_object
00074:     obj.name = f"{OBJECT_PREFIX}{index:02d}"
00075:     obj.scale = (width, height, 1.0)
00076:     obj.data.name = f"{OBJECT_PREFIX}{index:02d}_Mesh"
00077:     obj.data.materials.append(material)
00078:     obj.hide_render = False
00079:     obj.hide_viewport = False
00080:     try:
00081:         obj.show_transparent = True
00082:     except Exception:
00083:         pass
00084:     obj.parent = parent
00085: 
00086:     _store_base_transform(obj, rng.uniform(0.0, math.tau))
00087:     return obj
00088: 
00089: 
00090: def _collect_objects():
00091:     objects = [obj for obj in bpy.data.objects if obj.name.startswith(OBJECT_PREFIX)]
00092:     return sorted(objects, key=lambda obj: obj.name)
00093: 
00094: 
00095: def ensure_fog_filaments(parent=None):
00096:     material, controls = build_fog_filament_material(MATERIAL_NAME)
00097: 
00098:     root = bpy.data.objects.get(ROOT_NAME)
00099:     if root is None:
00100:         root = create_controller_empty(
00101:             ROOT_NAME,
00102:         location=(0, 4.8, 3.1),
00103:         parent=parent,
00104:         display_size=0.50,
00105:         hide_view=False,
00106:     )
00107:     elif parent is not None and root.parent is None:
00108:         root.parent = parent
00109:     root.hide_render = True
00110:     root.hide_viewport = False
00111:     root.hide_select = True
00112: 
00113:     existing = _collect_objects()
00114: 
00115:     if not FOG_FILAMENTS_ENABLED:
00116:         for obj in existing:
00117:             obj.hide_render = True
00118:             obj.hide_viewport = True
00119:         return {
00120:             "root": root,
00121:             "objects": [],
00122:             "material": material,
00123:             "controls": controls,
00124:         }
00125: 
00126:     for index in range(len(existing), FOG_FILAMENT_COUNT):
00127:         existing.append(_make_filament(index, material, parent=root))
00128: 
00129:     active = []
00130:     for index, obj in enumerate(existing):
00131:         if index >= FOG_FILAMENT_COUNT:
00132:             obj.hide_render = True
00133:             obj.hide_viewport = True
00134:             continue
00135: 
00136:         if not obj.data.materials:
00137:             obj.data.materials.append(material)
00138:         else:
00139:             obj.data.materials[0] = material
00140: 
00141:         obj.hide_render = False
00142:         obj.hide_viewport = False
00143:         if "st_base_location" not in obj:
00144:             _store_base_transform(obj, float(index) * 0.73)
00145: 
00146:         active.append({
00147:             "object": obj,
00148:             "phase": float(obj.get("st_phase", index * 0.73)),
00149:             "base_location": _base_vector(obj, "st_base_location", obj.location),
00150:             "base_scale": _base_vector(obj, "st_base_scale", obj.scale),
00151:             "base_rotation": _base_euler(obj, "st_base_rotation", obj.rotation_euler),
00152:         })
00153: 
00154:     return {
00155:         "root": root,
00156:         "objects": active,
00157:         "material": material,
00158:         "controls": controls,
00159:     }
```
