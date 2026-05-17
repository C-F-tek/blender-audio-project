import bpy

from config import (
    AURA_EMIT_MIN,
    BACKDROP_EMISSION_MIN,
    FOG_CLUMP_RAMP_HIGH_BASE,
    FOG_CLUMP_RAMP_LOW_BASE,
    FOG_CLUMP_SCALE_MIN,
    FOG_DENSITY_MIN,
    FOG_EMISSION_MIN,
    FOG_FILAMENT_ALPHA_MIN,
    FOG_FILAMENT_EMISSION_MIN,
    FOG_FILAMENT_NOISE_SCALE_MIN,
    FOG_FILAMENT_WAVE_SCALE_MIN,
    FOG_NOISE_SCALE_MIN,
    FOG_WAVE_DISTORTION_MIN,
    FOG_WAVE_SCALE_MIN,
    FOG_WAVE_WEIGHT_MIN,
    PEACE_PALETTE,
    RIBBON_EMIT_MIN,
    RING_EMIT_MIN,
)


def build_reflective_floor_material():
    mat = bpy.data.materials.new(name="PeaceFloorMaterial")
    mat.use_nodes = True

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    bsdf = nodes.get("Principled BSDF")

    texcoord = nodes.new("ShaderNodeTexCoord")
    texcoord.location = (-900, -100)

    mapping = nodes.new("ShaderNodeMapping")
    mapping.location = (-700, -100)

    noise = nodes.new("ShaderNodeTexNoise")
    noise.location = (-470, -100)
    noise.inputs["Scale"].default_value = 7.0
    noise.inputs["Detail"].default_value = 9.0
    noise.inputs["Roughness"].default_value = 0.58

    bump = nodes.new("ShaderNodeBump")
    bump.location = (-220, -140)
    bump.inputs["Strength"].default_value = 0.035

    rough_val = nodes.new("ShaderNodeValue")
    rough_val.location = (-260, 110)
    rough_val.outputs[0].default_value = 0.22
    rough_val.name = "FloorRoughnessValue"

    bsdf.inputs["Base Color"].default_value = (0.055, 0.060, 0.070, 1.0)
    bsdf.inputs["Metallic"].default_value = 0.08
    bsdf.inputs["Roughness"].default_value = 0.22

    links.new(texcoord.outputs["Generated"], mapping.inputs["Vector"])
    links.new(mapping.outputs["Vector"], noise.inputs["Vector"])
    links.new(noise.outputs["Fac"], bump.inputs["Height"])
    links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])
    links.new(rough_val.outputs[0], bsdf.inputs["Roughness"])

    return mat, rough_val.outputs[0]


def build_invisible_surface_material(name="InvisibleSurfaceMaterial"):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True

    if hasattr(mat, "blend_method"):
        mat.blend_method = "BLEND"
    if hasattr(mat, "shadow_method"):
        mat.shadow_method = "NONE"

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    for node in list(nodes):
        nodes.remove(node)

    out = nodes.new("ShaderNodeOutputMaterial")
    out.location = (360, 0)

    transparent = nodes.new("ShaderNodeBsdfTransparent")
    transparent.location = (120, 0)

    links.new(transparent.outputs["BSDF"], out.inputs["Surface"])
    return mat


def build_soft_backdrop_material():
    mat = bpy.data.materials.new(name="SoftBackdropMaterial")
    mat.use_nodes = True

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    for node in list(nodes):
        nodes.remove(node)

    out = nodes.new("ShaderNodeOutputMaterial")
    out.location = (760, 0)

    texcoord = nodes.new("ShaderNodeTexCoord")
    texcoord.location = (-760, 0)

    mapping = nodes.new("ShaderNodeMapping")
    mapping.location = (-540, 0)

    noise = nodes.new("ShaderNodeTexNoise")
    noise.location = (-320, 0)
    noise.inputs["Scale"].default_value = 1.18
    noise.inputs["Detail"].default_value = 6.0
    noise.inputs["Roughness"].default_value = 0.46

    ramp = nodes.new("ShaderNodeValToRGB")
    ramp.location = (-80, 0)
    ramp.color_ramp.elements[0].position = 0.14
    ramp.color_ramp.elements[0].color = (0.012, 0.055, 0.064, 1.0)
    ramp.color_ramp.elements[1].position = 1.00
    ramp.color_ramp.elements[1].color = (0.085, 0.245, 0.255, 1.0)

    emission = nodes.new("ShaderNodeEmission")
    emission.location = (280, 0)
    emission.inputs["Strength"].default_value = BACKDROP_EMISSION_MIN
    emission.name = "BackdropEmission"

    links.new(texcoord.outputs["Generated"], mapping.inputs["Vector"])
    links.new(mapping.outputs["Vector"], noise.inputs["Vector"])
    links.new(noise.outputs["Fac"], ramp.inputs["Fac"])
    links.new(ramp.outputs["Color"], emission.inputs["Color"])
    links.new(emission.outputs["Emission"], out.inputs["Surface"])

    return mat, {
        "emission_socket": emission.inputs["Strength"],
        "mapping_location_socket": mapping.inputs["Location"],
        "noise_scale_socket": noise.inputs["Scale"],
    }


def build_aura_material():
    mat = bpy.data.materials.new(name="HeroAuraMaterial")
    mat.use_nodes = True

    if hasattr(mat, "blend_method"):
        mat.blend_method = "BLEND"
    if hasattr(mat, "shadow_method"):
        mat.shadow_method = "NONE"

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    for n in list(nodes):
        nodes.remove(n)

    out = nodes.new("ShaderNodeOutputMaterial")
    out.location = (900, 0)

    mix = nodes.new("ShaderNodeMixShader")
    mix.location = (650, 0)

    transparent = nodes.new("ShaderNodeBsdfTransparent")
    transparent.location = (380, -120)

    emission = nodes.new("ShaderNodeEmission")
    emission.location = (380, 120)
    emission.inputs["Color"].default_value = PEACE_PALETTE["soft_teal"]
    emission.inputs["Strength"].default_value = AURA_EMIT_MIN
    emission.name = "AuraEmission"

    fresnel = nodes.new("ShaderNodeLayerWeight")
    fresnel.location = (120, -260)

    ramp = nodes.new("ShaderNodeValToRGB")
    ramp.location = (380, -300)
    ramp.color_ramp.elements[0].position = 0.18
    ramp.color_ramp.elements[1].position = 0.92

    links.new(fresnel.outputs["Facing"], ramp.inputs["Fac"])
    links.new(ramp.outputs["Color"], mix.inputs[0])
    links.new(emission.outputs["Emission"], mix.inputs[1])
    links.new(transparent.outputs["BSDF"], mix.inputs[2])
    links.new(mix.outputs["Shader"], out.inputs["Surface"])

    return mat, emission.inputs["Strength"], ramp.color_ramp.elements[0]


def build_variant_material(name, color):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    for n in list(nodes):
        nodes.remove(n)

    out = nodes.new("ShaderNodeOutputMaterial")
    out.location = (700, 0)

    mix = nodes.new("ShaderNodeMixShader")
    mix.location = (420, 0)

    principled = nodes.new("ShaderNodeBsdfPrincipled")
    principled.location = (120, -120)
    principled.inputs["Base Color"].default_value = color
    principled.inputs["Metallic"].default_value = 0.18
    principled.inputs["Roughness"].default_value = 0.32

    emission = nodes.new("ShaderNodeEmission")
    emission.location = (120, 120)
    emission.name = "VariantEmission"
    emission.inputs["Color"].default_value = color
    emission.inputs["Strength"].default_value = 0.32

    fac = nodes.new("ShaderNodeValue")
    fac.location = (120, -300)
    fac.name = "VariantEmissionMix"
    fac.outputs[0].default_value = 0.20

    links.new(fac.outputs[0], mix.inputs[0])
    links.new(principled.outputs["BSDF"], mix.inputs[1])
    links.new(emission.outputs["Emission"], mix.inputs[2])
    links.new(mix.outputs["Shader"], out.inputs["Surface"])

    return mat


def build_ring_material(name, color):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    for n in list(nodes):
        nodes.remove(n)

    out = nodes.new("ShaderNodeOutputMaterial")
    out.location = (520, 0)

    emission = nodes.new("ShaderNodeEmission")
    emission.location = (240, 0)
    emission.inputs["Color"].default_value = color
    emission.inputs["Strength"].default_value = RING_EMIT_MIN
    emission.name = "RingEmission"

    links.new(emission.outputs["Emission"], out.inputs["Surface"])
    return mat, emission.inputs["Strength"]


def build_ribbon_material(name, color):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    for n in list(nodes):
        nodes.remove(n)

    out = nodes.new("ShaderNodeOutputMaterial")
    out.location = (520, 0)

    emission = nodes.new("ShaderNodeEmission")
    emission.location = (240, 0)
    emission.inputs["Color"].default_value = color
    emission.inputs["Strength"].default_value = RIBBON_EMIT_MIN
    emission.name = "RibbonEmission"

    links.new(emission.outputs["Emission"], out.inputs["Surface"])
    return mat, emission.inputs["Strength"]
