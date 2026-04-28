"""Render settings template."""

from __future__ import annotations


def apply_render_settings(bpy, cfg):
    """Apply basic render settings from config."""

    if bpy is None:
        raise RuntimeError("bpy is required inside Blender")

    scene = bpy.context.scene
    scene.frame_start = int(cfg.FRAME_START)

    if cfg.FRAME_END is not None:
        scene.frame_end = int(cfg.FRAME_END)

    scene.render.fps = int(cfg.FPS)
    scene.render.resolution_x = int(cfg.RESOLUTION_X)
    scene.render.resolution_y = int(cfg.RESOLUTION_Y)
    scene.render.resolution_percentage = int(cfg.RENDER_PERCENTAGE)

    cfg.OUTPUT_IMAGE_SEQUENCE_DIR.mkdir(parents=True, exist_ok=True)
    scene.render.filepath = str(cfg.OUTPUT_IMAGE_SEQUENCE_DIR / cfg.OUTPUT_IMAGE_SEQUENCE_PREFIX)

    return scene
