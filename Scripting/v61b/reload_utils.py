from __future__ import annotations

import importlib
import sys
from types import ModuleType

MODULES_TO_RELOAD = [
    "config",
    "scene_utils",
    "io_utils",
    "render_setup",
    "world_setup",
    "camera_setup",
    "asset_setup",
    "atmosphere_setup",
    "physics_setup",
    "fog_dynamics",
    "fog_filaments",
    "animation",
    "scene_tuning_panel",
]

PACKAGE_PREFIXES_TO_RELOAD = ("spaziotempo",)


def should_reload_module(module_name: str) -> bool:
    if module_name in MODULES_TO_RELOAD:
        return True
    return any(
        module_name == prefix or module_name.startswith(prefix + ".")
        for prefix in PACKAGE_PREFIXES_TO_RELOAD
    )


def reload_known_modules() -> list[ModuleType]:
    """Reload already-imported v61b modules without deleting unrelated sys.modules entries."""
    reloaded: list[ModuleType] = []
    for module_name in list(sys.modules):
        if not should_reload_module(module_name):
            continue
        module = sys.modules.get(module_name)
        if module is None:
            continue
        try:
            reloaded.append(importlib.reload(module))
        except Exception:
            # Preserve Blender-session resilience: callers can still import modules normally.
            sys.modules.pop(module_name, None)
    return reloaded
