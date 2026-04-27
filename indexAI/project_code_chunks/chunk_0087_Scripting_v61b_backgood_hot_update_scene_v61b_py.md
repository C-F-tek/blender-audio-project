# Project Code Chunk 87/212

- File: `Scripting/v61b_backgood/hot_update_scene_v61b.py`
- Part: `1`
- Lines: `1-61`

## Symbol Map
- Imports: `sys`, `from pathlib import Path`, `bpy`
- Functions: `resolve_script_dir()` line 7; `drop_hotpatch_cache()` line 38; `main()` line 52
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
00039:     reload_prefixes = ("hotpatch",)
00040:     reload_names = {
00041:         "config",
00042:         "materials",
00043:         "render_setup",
00044:         "fog_dynamics",
00045:     }
00046: 
00047:     for mod_name in list(sys.modules):
00048:         if mod_name in reload_names or any(mod_name == prefix or mod_name.startswith(prefix + ".") for prefix in reload_prefixes):
00049:             sys.modules.pop(mod_name, None)
00050: 
00051: 
00052: def main():
00053:     drop_hotpatch_cache()
00054: 
00055:     from hotpatch.runner import run_all
00056: 
00057:     return run_all()
00058: 
00059: 
00060: if __name__ == "__main__":
00061:     main()
```
