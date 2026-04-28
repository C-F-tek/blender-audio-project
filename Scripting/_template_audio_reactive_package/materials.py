"""Material setup template."""

from __future__ import annotations


def create_materials(bpy, controls=None):
    """Create package materials.

    Replace this placeholder material with package-specific shader logic.
    """

    if bpy is None:
        raise RuntimeError("bpy is required inside Blender")

    material = bpy.data.materials.new("TemplateReactiveMaterial")
    material.use_nodes = True

    nodes = material.node_tree.nodes
    principled = nodes.get("Principled BSDF")
    if principled is not None:
        if "Base Color" in principled.inputs:
            principled.inputs["Base Color"].default_value = (0.1, 0.25, 0.8, 1.0)
        if "Emission Strength" in principled.inputs:
            principled.inputs["Emission Strength"].default_value = 0.15

    return {"hero_material": material}


def assign_materials(objects, materials):
    """Assign generated materials to generated objects."""

    hero = objects.get("hero") if objects else None
    material = materials.get("hero_material") if materials else None
    if hero is not None and material is not None:
        hero.data.materials.append(material)
