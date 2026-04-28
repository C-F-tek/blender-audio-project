"""Camera setup template."""

from __future__ import annotations

import math


def create_camera(bpy, controls=None):
    """Create a default camera for the package."""

    if bpy is None:
        raise RuntimeError("bpy is required inside Blender")

    bpy.ops.object.camera_add(location=(0, -7.5, 4.0), rotation=(math.radians(62), 0, 0))
    camera = bpy.context.object
    camera.name = "TemplateCamera"
    bpy.context.scene.camera = camera

    try:
        camera.data.lens = 32
        camera.data.dof.use_dof = True
        camera.data.dof.aperture_fstop = 5.6
    except Exception:
        pass

    return camera
