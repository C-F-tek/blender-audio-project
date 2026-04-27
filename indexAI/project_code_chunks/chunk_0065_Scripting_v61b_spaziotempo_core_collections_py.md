# Project Code Chunk 65/212

- File: `Scripting/v61b/spaziotempo/core/collections.py`
- Part: `1`
- Lines: `1-132`

## Symbol Map
- Imports: `bpy`, `from registry import EXACT_OBJECT_LAYERS, LAYER_ORDER, LAYER_SPECS, PARENT_LAYER_HINTS, PREFIX_OBJECT_LAYERS, PROJECT_ROOT_COLLECTION, STRUCTURE_VERSION, TYPE_FALLBACK_LAYERS`
- Functions: `_children_by_name(collection)` line 17; `_objects_by_name(collection)` line 21; `ensure_child_collection(parent, name)` line 25; `ensure_project_collections(scene, include_reserved)` line 33; `_parent_hint(obj)` line 54; `classify_object(obj)` line 64; `link_object_to_layer(obj, collection)` line 86; `apply_object_metadata(obj, spec)` line 91; `classify_scene_objects(scene, include_reserved)` line 99; `compact_structure_summary(report)` line 126

## Content
```py
00001: """Scene collection and object classification helpers."""
00002: 
00003: import bpy
00004: 
00005: from .registry import (
00006:     EXACT_OBJECT_LAYERS,
00007:     LAYER_ORDER,
00008:     LAYER_SPECS,
00009:     PARENT_LAYER_HINTS,
00010:     PREFIX_OBJECT_LAYERS,
00011:     PROJECT_ROOT_COLLECTION,
00012:     STRUCTURE_VERSION,
00013:     TYPE_FALLBACK_LAYERS,
00014: )
00015: 
00016: 
00017: def _children_by_name(collection):
00018:     return {child.name: child for child in collection.children}
00019: 
00020: 
00021: def _objects_by_name(collection):
00022:     return {obj.name: obj for obj in collection.objects}
00023: 
00024: 
00025: def ensure_child_collection(parent, name):
00026:     existing = bpy.data.collections.get(name)
00027:     collection = existing or bpy.data.collections.new(name)
00028:     if name not in _children_by_name(parent):
00029:         parent.children.link(collection)
00030:     return collection
00031: 
00032: 
00033: def ensure_project_collections(scene=None, include_reserved=True):
00034:     scene = scene or bpy.context.scene
00035:     project = ensure_child_collection(scene.collection, PROJECT_ROOT_COLLECTION)
00036:     project["st_structure_version"] = STRUCTURE_VERSION
00037: 
00038:     collections = {}
00039:     for key in LAYER_ORDER:
00040:         spec = LAYER_SPECS[key]
00041:         if spec.reserved and not include_reserved:
00042:             continue
00043:         collection = ensure_child_collection(project, spec.collection)
00044:         collection["st_key"] = spec.key
00045:         collection["st_family"] = spec.family
00046:         collection["st_layer"] = spec.layer
00047:         collection["st_feature"] = spec.feature
00048:         collection["st_reserved"] = bool(spec.reserved)
00049:         collections[key] = collection
00050: 
00051:     return collections
00052: 
00053: 
00054: def _parent_hint(obj):
00055:     parent = getattr(obj, "parent", None)
00056:     while parent is not None:
00057:         hint = PARENT_LAYER_HINTS.get(parent.name)
00058:         if hint is not None:
00059:             return hint
00060:         parent = getattr(parent, "parent", None)
00061:     return None
00062: 
00063: 
00064: def classify_object(obj):
00065:     name = obj.name
00066: 
00067:     exact = EXACT_OBJECT_LAYERS.get(name)
00068:     if exact is not None:
00069:         return exact
00070: 
00071:     for prefix, layer_key in PREFIX_OBJECT_LAYERS:
00072:         if name.startswith(prefix):
00073:             return layer_key
00074: 
00075:     hint = _parent_hint(obj)
00076:     if hint is not None:
00077:         return hint
00078: 
00079:     type_hint = TYPE_FALLBACK_LAYERS.get(getattr(obj, "type", ""))
00080:     if type_hint is not None:
00081:         return type_hint
00082: 
00083:     return "technical"
00084: 
00085: 
00086: def link_object_to_layer(obj, collection):
00087:     if obj.name not in _objects_by_name(collection):
00088:         collection.objects.link(obj)
00089: 
00090: 
00091: def apply_object_metadata(obj, spec):
00092:     obj["st_family"] = spec.family
00093:     obj["st_layer"] = spec.layer
00094:     obj["st_feature"] = spec.feature
00095:     obj["st_collection"] = spec.collection
00096:     obj["st_structure_version"] = STRUCTURE_VERSION
00097: 
00098: 
00099: def classify_scene_objects(scene=None, include_reserved=True):
00100:     scene = scene or bpy.context.scene
00101:     collections = ensure_project_collections(scene, include_reserved=include_reserved)
00102:     counts = {key: 0 for key in LAYER_ORDER if key in collections}
00103:     objects_classified = 0
00104: 
00105:     for obj in scene.objects:
00106:         layer_key = classify_object(obj)
00107:         if layer_key not in collections:
00108:             collections[layer_key] = ensure_project_collections(scene, include_reserved=True)[layer_key]
00109:             counts.setdefault(layer_key, 0)
00110: 
00111:         spec = LAYER_SPECS[layer_key]
00112:         link_object_to_layer(obj, collections[layer_key])
00113:         apply_object_metadata(obj, spec)
00114:         counts[layer_key] = counts.get(layer_key, 0) + 1
00115:         objects_classified += 1
00116: 
00117:     return {
00118:         "root_collection": PROJECT_ROOT_COLLECTION,
00119:         "structure_version": STRUCTURE_VERSION,
00120:         "objects_classified": objects_classified,
00121:         "counts": counts,
00122:         "collections": {key: coll.name for key, coll in collections.items()},
00123:     }
00124: 
00125: 
00126: def compact_structure_summary(report):
00127:     parts = []
00128:     for key in LAYER_ORDER:
00129:         count = report.get("counts", {}).get(key, 0)
00130:         if count:
00131:             parts.append(f"{LAYER_SPECS[key].collection}={count}")
00132:     return ", ".join(parts) if parts else "no classified objects"
```
