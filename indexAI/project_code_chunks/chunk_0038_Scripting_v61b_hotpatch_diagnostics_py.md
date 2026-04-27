# Project Code Chunk 38/212

- File: `Scripting/v61b/hotpatch/diagnostics.py`
- Part: `2`
- Lines: `277-286`

## Symbol Map
- Imports: `bpy`, `from common import ANALYSIS_JSON_PATH, cfg_value, load_analysis`, `from spaziotempo.core.registry import LAYER_ORDER, LAYER_SPECS, PROJECT_ROOT_COLLECTION`
- Functions: `text_report(name, lines)` line 17; `has_object(name)` line 24; `count_objects(prefix)` line 28; `collection_exists(name)` line 32; `layer_collection_counts()` line 36; `scene_frame_count(scene)` line 45; `material_node_exists(node_name)` line 49; `modifier_exists(mod_name)` line 56; `point_cache_state(cache)` line 64; `particle_cache_state(ps)` line 72; `analyze_rebuild_need()` line 83; `analyze_optimizer()` line 169
- Assignments: `STRUCTURAL_OBJECTS`

## Content
```py
00277:         lines.append("")
00278:     lines.append("Checked OK:")
00279:     lines.extend(f"- {item}" for item in ok)
00280: 
00281:     text_report("SPAZIOTEMPO_OPTIMIZER_REPORT", lines)
00282:     return {
00283:         "warnings": warnings,
00284:         "suggestions": suggestions,
00285:         "report": "\n".join(lines),
00286:     }
```
