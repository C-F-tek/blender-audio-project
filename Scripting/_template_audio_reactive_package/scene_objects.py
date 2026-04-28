"""Scene object creation template."""

from __future__ import annotations


def create_scene_objects(bpy, controls=None):
    """Create or prepare scene objects.

    This template creates a minimal placeholder object. Replace this with
    package-specific geometry using the v61b style as quality reference.
    """

    if bpy is None:
        raise RuntimeError("bpy is required inside Blender")

    bpy.ops.mesh.primitive_uv_sphere_add(location=(0, 0, 1.5))
    hero = bpy.context.object
    hero.name = "TemplateHeroObject"
    hero.scale = (1.5, 1.5, 1.5)

    return {"hero": hero}
