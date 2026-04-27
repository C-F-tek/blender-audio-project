# Project Code Chunk 32/212

- File: `Scripting/v61b/hot_update_scene_v61b.py`
- Part: `1`
- Lines: `1-63`

## Symbol Map
- Imports: `sys`, `from pathlib import Path`, `bpy`
- Functions: `resolve_script_dir()` line 7; `drop_hotpatch_cache()` line 38; `main()` line 53
- Assignments: `SCRIPT_DIR`

## Content
```py
00001: import sys
00002: from pathlib import Path
00003: 
00004: import bpy
00005: 
00006: 
00007: def resolve_script_dir():
00008:     candidates = []
00009: 
00010:     try:
00011:         text = bpy.context.space_data.text
00012:         if text is not None and text.filepath:
00013:             candidates.append(Path(text.filepath).resolve().parent)
00014:     except Exception:
00015:         pass
00016: 
00017:     if "__file__" in globals():
00018:         try:
00019:             candidates.append(Path(__file__).resolve().parent)
00020:         except Exception:
00021:             pass
00022: 
00023:     candidates.append(Path.home() / "blender" / "blender-audio-project" / "Scripting" / "v61b")
00024: 
00025:     for candidate in candidates:
00026:         if (candidate / "config.py").exists() and (candidate / "hotpatch").exists():
00027:             return candidate
00028: 
00029:     return candidates[-1]
00030: 
00031: 
00032: SCRIPT_DIR = resolve_script_dir()
00033: 
00034: if str(SCRIPT_DIR) not in sys.path:
00035:     sys.path.insert(0, str(SCRIPT_DIR))
00036: 
00037: 
00038: def drop_hotpatch_cache():
00039:     reload_prefixes = ("hotpatch", "spaziotempo")
00040:     reload_names = {
00041:         "config",
00042:         "materials",
00043:         "render_setup",
00044:         "fog_dynamics",
00045:         "fog_filaments",
00046:     }
00047: 
00048:     for mod_name in list(sys.modules):
00049:         if mod_name in reload_names or any(mod_name == prefix or mod_name.startswith(prefix + ".") for prefix in reload_prefixes):
00050:             sys.modules.pop(mod_name, None)
00051: 
00052: 
00053: def main():
00054:     drop_hotpatch_cache()
00055: 
00056:     from hotpatch.runner import run_hotpatch
00057: 
00058:     mode = globals().get("HOTPATCH_MODE", "ALL")
00059:     return run_hotpatch(mode)
00060: 
00061: 
00062: if __name__ == "__main__":
00063:     main()
```
