# Project Code Chunk 36/212

- File: `Scripting/v61b/hotpatch/common.py`
- Part: `1`
- Lines: `1-91`

## Symbol Map
- Imports: `json`, `from pathlib import Path`, `bpy`, `config`
- Functions: `cfg_value(name, default)` line 9; `load_analysis()` line 32; `iter_objects_prefix(prefix)` line 42; `remove_objects_with_prefixes(prefixes)` line 46; `keyframe_if_possible(idblock, data_path, frame)` line 56; `clear_animation(idblock)` line 63; `get_node(material, node_name)` line 72; `socket_by_name(node, socket_name, is_output)` line 78; `store_base_vector(obj, key, value)` line 88
- Assignments: `ANALYSIS_JSON_PATH`, `OUTPUT_MP4`, `PALETTE_LIST`

## Content
```py
00001: import json
00002: from pathlib import Path
00003: 
00004: import bpy
00005: 
00006: import config as cfg
00007: 
00008: 
00009: def cfg_value(name, default):
00010:     return getattr(cfg, name, default)
00011: 
00012: 
00013: ANALYSIS_JSON_PATH = cfg_value(
00014:     "ANALYSIS_JSON_PATH",
00015:     Path.home() / "blender" / "blender-audio-project" / "output" / "Feel The Light-Luca Vera_Master_analysis.json",
00016: )
00017: OUTPUT_MP4 = cfg_value(
00018:     "OUTPUT_MP4",
00019:     Path.home() / "blender" / "renders" / "spaziotempo_asset_visual_v61b.mp4",
00020: )
00021: PALETTE_LIST = cfg_value(
00022:     "PALETTE_LIST",
00023:     [
00024:         (0.170, 0.460, 0.480, 1.0),
00025:         (0.720, 0.620, 0.340, 1.0),
00026:         (0.500, 0.300, 0.340, 1.0),
00027:         (0.940, 0.930, 0.900, 1.0),
00028:     ],
00029: )
00030: 
00031: 
00032: def load_analysis():
00033:     path = Path(ANALYSIS_JSON_PATH)
00034:     if not path.exists():
00035:         print(f"[WARN] Analysis JSON non trovato: {path}")
00036:         return None, []
00037: 
00038:     data = json.loads(path.read_text(encoding="utf-8"))
00039:     return data.get("meta", {}), data.get("frames", [])
00040: 
00041: 
00042: def iter_objects_prefix(prefix):
00043:     return [obj for obj in bpy.data.objects if obj.name.startswith(prefix)]
00044: 
00045: 
00046: def remove_objects_with_prefixes(prefixes):
00047:     removed = 0
00048:     for obj in list(bpy.data.objects):
00049:         if not any(obj.name.startswith(prefix) for prefix in prefixes):
00050:             continue
00051:         bpy.data.objects.remove(obj, do_unlink=True)
00052:         removed += 1
00053:     return removed
00054: 
00055: 
00056: def keyframe_if_possible(idblock, data_path, frame):
00057:     try:
00058:         idblock.keyframe_insert(data_path=data_path, frame=frame)
00059:     except Exception:
00060:         pass
00061: 
00062: 
00063: def clear_animation(idblock):
00064:     if idblock is None:
00065:         return
00066:     try:
00067:         idblock.animation_data_clear()
00068:     except Exception:
00069:         pass
00070: 
00071: 
00072: def get_node(material, node_name):
00073:     if material is None or not material.use_nodes:
00074:         return None
00075:     return material.node_tree.nodes.get(node_name)
00076: 
00077: 
00078: def socket_by_name(node, socket_name, is_output=False):
00079:     if node is None:
00080:         return None
00081:     sockets = node.outputs if is_output else node.inputs
00082:     try:
00083:         return sockets[socket_name]
00084:     except Exception:
00085:         return None
00086: 
00087: 
00088: def store_base_vector(obj, key, value):
00089:     if key not in obj:
00090:         obj[key] = [float(value.x), float(value.y), float(value.z)]
00091:     return obj[key]
```
