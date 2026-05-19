"""Entry point template for a Blender audio-reactive package.

Copy this package folder before using it for a real project.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    import bpy
except Exception:  # Allows static inspection outside Blender.
    bpy = None

PACKAGE_DIR = Path(__file__).resolve().parent
if str(PACKAGE_DIR) not in sys.path:
    sys.path.insert(0, str(PACKAGE_DIR))

from audio_mapping import controls_from_summary  # noqa: E402
from camera import create_camera  # noqa: E402
from lighting import create_lighting  # noqa: E402
from materials import assign_materials, create_materials  # noqa: E402
from render_settings import apply_render_settings  # noqa: E402
from scene_objects import create_scene_objects  # noqa: E402

import config as cfg  # noqa: E402


def load_json_if_exists(path):
    """Load a JSON file if it exists, otherwise return None."""

    if path is None:
        return None

    path = Path(path)
    if not path.exists():
        return None

    return json.loads(path.read_text(encoding="utf-8"))


def clear_scene():
    """Clear the current Blender scene when explicitly allowed by config."""

    if bpy is None:
        raise RuntimeError("bpy is required inside Blender")

    if not cfg.ALLOW_DESTRUCTIVE_SCENE_CLEAR:
        return

    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()


def main():
    """Build the template scene."""

    if bpy is None:
        raise RuntimeError("This script must be run inside Blender")

    summary = load_json_if_exists(cfg.TRACK_SUMMARY_JSON)
    controls = controls_from_summary(summary)

    clear_scene()
    apply_render_settings(bpy, cfg)

    objects = create_scene_objects(bpy, controls=controls)
    materials = create_materials(bpy, controls=controls)
    assign_materials(objects, materials)
    create_camera(bpy, controls=controls)
    create_lighting(bpy, controls=controls)

    print(f"[INFO] Package template executed: {cfg.PACKAGE_NAME}")
    print("[INFO] Replace placeholder logic with project-specific scene generation.")


if __name__ == "__main__":
    main()
