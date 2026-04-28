"""Lighting setup template."""

from __future__ import annotations


def create_lighting(bpy, controls=None):
    """Create default lights for the package."""

    if bpy is None:
        raise RuntimeError("bpy is required inside Blender")

    bpy.ops.object.light_add(type="AREA", location=(0, -3, 5))
    key = bpy.context.object
    key.name = "TemplateKeyLight"
    key.data.energy = 500
    key.data.size = 5

    bpy.ops.object.light_add(type="POINT", location=(3, 2, 3))
    accent = bpy.context.object
    accent.name = "TemplateAccentLight"
    accent.data.energy = 120

    return {"key": key, "accent": accent}
