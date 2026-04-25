import sys
from pathlib import Path

import bpy


def resolve_script_dir():
    candidates = []

    try:
        text = bpy.context.space_data.text
        if text is not None and text.filepath:
            candidates.append(Path(text.filepath).resolve().parent)
    except Exception:
        pass

    if "__file__" in globals():
        try:
            candidates.append(Path(__file__).resolve().parent)
        except Exception:
            pass

    candidates.append(Path.home() / "blender" / "blender-audio-project" / "Scripting" / "v61b")

    for candidate in candidates:
        if (candidate / "config.py").exists() and (candidate / "hotpatch").exists():
            return candidate

    return candidates[-1]


SCRIPT_DIR = resolve_script_dir()

if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))


def drop_hotpatch_cache():
    reload_prefixes = ("hotpatch", "spaziotempo")
    reload_names = {
        "config",
        "materials",
        "render_setup",
        "fog_dynamics",
        "fog_filaments",
    }

    for mod_name in list(sys.modules):
        if mod_name in reload_names or any(mod_name == prefix or mod_name.startswith(prefix + ".") for prefix in reload_prefixes):
            sys.modules.pop(mod_name, None)


def main():
    drop_hotpatch_cache()

    from hotpatch.runner import run_hotpatch

    mode = globals().get("HOTPATCH_MODE", "ALL")
    return run_hotpatch(mode)


if __name__ == "__main__":
    main()
