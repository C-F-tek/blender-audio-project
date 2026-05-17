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


def build_atmosphere_volume_material():
    mat = bpy.data.materials.new(name="AtmosphereVolumeMaterial")
    mat.use_nodes = True
    mat["spaziotempo_volume_fog"] = True

    try:
        mat.blend_method = "BLEND"
    except Exception:
        pass
    try:
        mat.use_screen_refraction = False
    except Exception:
        pass

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    for n in list(nodes):
        nodes.remove(n)

    out = nodes.new("ShaderNodeOutputMaterial")
    out.location = (980, 0)

    texcoord = nodes.new("ShaderNodeTexCoord")
    texcoord.location = (-1000, 80)

    mapping = nodes.new("ShaderNodeMapping")
    mapping.location = (-760, 80)

    noise = nodes.new("ShaderNodeTexNoise")
    noise.location = (-520, 80)
    noise.inputs["Scale"].default_value = FOG_NOISE_SCALE_MIN
    noise.inputs["Detail"].default_value = 6.0
    noise.inputs["Roughness"].default_value = 0.64

    ramp = nodes.new("ShaderNodeValToRGB")
    ramp.location = (-280, 80)
    ramp.color_ramp.elements[0].position = 0.28
    ramp.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    ramp.color_ramp.elements[1].position = 0.54
    ramp.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)

    clump_noise = nodes.new("ShaderNodeTexNoise")
    clump_noise.location = (-520, -90)
    clump_noise.name = "FogClumpNoise"
    clump_noise.inputs["Scale"].default_value = FOG_CLUMP_SCALE_MIN
    clump_noise.inputs["Detail"].default_value = 10.0
    clump_noise.inputs["Roughness"].default_value = 0.70

    clump_ramp = nodes.new("ShaderNodeValToRGB")
    clump_ramp.location = (-280, -90)
    clump_ramp.name = "FogClumpRamp"
    clump_ramp.color_ramp.elements[0].position = FOG_CLUMP_RAMP_LOW_BASE
    clump_ramp.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    clump_ramp.color_ramp.elements[1].position = FOG_CLUMP_RAMP_HIGH_BASE
    clump_ramp.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)

    wave = nodes.new("ShaderNodeTexWave")
    wave.location = (-520, -270)
    wave.name = "FogWindWave"
    try:
        wave.wave_type = "RINGS"
    except Exception:
        pass
    try:
        wave.bands_direction = "Z"
    except Exception:
        pass
    if "Scale" in wave.inputs:
        wave.inputs["Scale"].default_value = FOG_WAVE_SCALE_MIN
    if "Distortion" in wave.inputs:
        wave.inputs["Distortion"].default_value = FOG_WAVE_DISTORTION_MIN

    wave_weight = nodes.new("ShaderNodeMath")
    wave_weight.location = (-270, -275)
    wave_weight.name = "FogWindWaveWeight"
    wave_weight.operation = "MULTIPLY"
    wave_weight.inputs[1].default_value = FOG_WAVE_WEIGHT_MIN

    clump_mask = nodes.new("ShaderNodeMath")
    clump_mask.location = (-20, 15)
    clump_mask.name = "FogClumpMask"
    clump_mask.operation = "MULTIPLY"
    try:
        clump_mask.use_clamp = True
    except Exception:
        pass

    wave_inside_clumps = nodes.new("ShaderNodeMath")
    wave_inside_clumps.location = (-20, -175)
    wave_inside_clumps.name = "FogWaveInsideClumps"
    wave_inside_clumps.operation = "MULTIPLY"
    try:
        wave_inside_clumps.use_clamp = True
    except Exception:
        pass

    smoke_mix = nodes.new("ShaderNodeMath")
    smoke_mix.location = (190, 30)
    smoke_mix.name = "FogSmokeShapeMix"
    smoke_mix.operation = "ADD"
    try:
        smoke_mix.use_clamp = True
    except Exception:
        pass

    density_val = nodes.new("ShaderNodeValue")
    density_val.location = (-20, -90)
    density_val.outputs[0].default_value = FOG_DENSITY_MIN
    density_val.name = "FogDensityValue"

    emission_val = nodes.new("ShaderNodeValue")
    emission_val.location = (-20, -240)
    emission_val.outputs[0].default_value = FOG_EMISSION_MIN
    emission_val.name = "FogEmissionValue"

    density_mul = nodes.new("ShaderNodeMath")
    density_mul.location = (410, 40)
    density_mul.operation = "MULTIPLY"

    links.new(texcoord.outputs["Generated"], mapping.inputs["Vector"])
    links.new(mapping.outputs["Vector"], noise.inputs["Vector"])
    links.new(mapping.outputs["Vector"], clump_noise.inputs["Vector"])
    links.new(mapping.outputs["Vector"], wave.inputs["Vector"])
    links.new(noise.outputs["Fac"], ramp.inputs["Fac"])
    links.new(clump_noise.outputs["Fac"], clump_ramp.inputs["Fac"])
    links.new(wave.outputs["Color"], wave_weight.inputs[0])
    links.new(ramp.outputs["Color"], clump_mask.inputs[0])
    links.new(clump_ramp.outputs["Color"], clump_mask.inputs[1])
    links.new(wave_weight.outputs[0], wave_inside_clumps.inputs[0])
    links.new(clump_mask.outputs[0], wave_inside_clumps.inputs[1])
    links.new(clump_mask.outputs[0], smoke_mix.inputs[0])
    links.new(wave_inside_clumps.outputs[0], smoke_mix.inputs[1])
    links.new(smoke_mix.outputs[0], density_mul.inputs[0])
    links.new(density_val.outputs[0], density_mul.inputs[1])

    controls = {
        "density_socket": density_val.outputs[0],
        "emission_socket": emission_val.outputs[0],
        "noise_scale_socket": noise.inputs["Scale"],
        "noise_detail_socket": noise.inputs["Detail"],
        "noise_roughness_socket": noise.inputs["Roughness"],
        "clump_noise_scale_socket": clump_noise.inputs["Scale"],
        "clump_noise_detail_socket": clump_noise.inputs["Detail"],
        "clump_noise_roughness_socket": clump_noise.inputs["Roughness"],
        "mapping_location_socket": mapping.inputs["Location"],
        "mapping_scale_socket": mapping.inputs["Scale"],
        "mapping_rotation_socket": mapping.inputs["Rotation"],
        "wave_scale_socket": wave.inputs.get("Scale"),
        "wave_distortion_socket": wave.inputs.get("Distortion"),
        "wave_phase_socket": wave.inputs.get("Phase Offset"),
        "wave_weight_socket": wave_weight.inputs[1],
        "ramp_low_ctrl": ramp.color_ramp.elements[0],
        "ramp_high_ctrl": ramp.color_ramp.elements[1],
        "clump_ramp_low_ctrl": clump_ramp.color_ramp.elements[0],
        "clump_ramp_high_ctrl": clump_ramp.color_ramp.elements[1],
    }

    try:
        volume = nodes.new("ShaderNodeVolumePrincipled")
        volume.name = "AtmospherePrincipledVolume"
        volume.location = (500, 0)
        if "Color" in volume.inputs:
            volume.inputs["Color"].default_value = (0.82, 0.89, 0.91, 1.0)
        if "Emission Color" in volume.inputs:
            volume.inputs["Emission Color"].default_value = PEACE_PALETTE["soft_teal"]
        links.new(density_mul.outputs[0], volume.inputs["Density"])
        if "Emission Strength" in volume.inputs:
            links.new(emission_val.outputs[0], volume.inputs["Emission Strength"])
        links.new(volume.outputs["Volume"], out.inputs["Volume"])

        for input_name, control_name in [
            ("Color", "volume_color_socket"),
            ("Anisotropy", "volume_anisotropy_socket"),
        ]:
            if input_name in volume.inputs:
                controls[control_name] = volume.inputs[input_name]
    except Exception:
        scatter = nodes.new("ShaderNodeVolumeScatter")
        scatter.name = "AtmosphereVolumeScatter"
        scatter.location = (500, 90)
        if "Color" in scatter.inputs:
            scatter.inputs["Color"].default_value = (0.82, 0.89, 0.91, 1.0)
        if "Density" in scatter.inputs:
            links.new(density_mul.outputs[0], scatter.inputs["Density"])

        absorption = nodes.new("ShaderNodeVolumeAbsorption")
        absorption.name = "AtmosphereVolumeAbsorption"
        absorption.location = (500, -105)
        if "Color" in absorption.inputs:
            absorption.inputs["Color"].default_value = (0.72, 0.86, 0.88, 1.0)
        if "Density" in absorption.inputs:
            links.new(density_mul.outputs[0], absorption.inputs["Density"])

        add_volume = nodes.new("ShaderNodeAddShader")
        add_volume.name = "AtmosphereVolumeAdd"
        add_volume.location = (760, 0)
        links.new(scatter.outputs["Volume"], add_volume.inputs[0])
        links.new(absorption.outputs["Volume"], add_volume.inputs[1])
        links.new(add_volume.outputs["Shader"], out.inputs["Volume"])

        if "Color" in scatter.inputs:
            controls["volume_color_socket"] = scatter.inputs["Color"]
        if "Anisotropy" in scatter.inputs:
            controls["volume_anisotropy_socket"] = scatter.inputs["Anisotropy"]

    return mat, controls


def build_fog_filament_material(name="FogFilamentMaterial"):
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name=name)
    mat.use_nodes = True

    for attr, value in [
        ("blend_method", "BLEND"),
        ("shadow_method", "NONE"),
        ("use_screen_refraction", False),
        ("show_transparent_back", True),
    ]:
        try:
            setattr(mat, attr, value)
        except Exception:
            pass

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    for n in list(nodes):
        nodes.remove(n)

    out = nodes.new("ShaderNodeOutputMaterial")
    out.location = (720, 0)

    transparent = nodes.new("ShaderNodeBsdfTransparent")
    transparent.location = (420, 120)

    emission_shader = nodes.new("ShaderNodeEmission")
    emission_shader.location = (420, -60)
    emission_shader.inputs["Color"].default_value = (0.58, 0.86, 0.86, 1.0)
    emission_shader.inputs["Strength"].default_value = FOG_FILAMENT_EMISSION_MIN

    mix_shader = nodes.new("ShaderNodeMixShader")
    mix_shader.location = (650, 20)

    texcoord = nodes.new("ShaderNodeTexCoord")
    texcoord.location = (-900, 120)

    mapping = nodes.new("ShaderNodeMapping")
    mapping.name = "FogFilamentMapping"
    mapping.location = (-690, 120)

    noise = nodes.new("ShaderNodeTexNoise")
    noise.name = "FogFilamentNoise"
    noise.location = (-460, 135)
    noise.inputs["Scale"].default_value = FOG_FILAMENT_NOISE_SCALE_MIN
    noise.inputs["Detail"].default_value = 13.0
    noise.inputs["Roughness"].default_value = 0.58

    ramp = nodes.new("ShaderNodeValToRGB")
    ramp.name = "FogFilamentRamp"
    ramp.location = (-230, 135)
    ramp.color_ramp.elements[0].position = 0.34
    ramp.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    ramp.color_ramp.elements[1].position = 0.74
    ramp.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)

    wave = nodes.new("ShaderNodeTexWave")
    wave.name = "FogFilamentWave"
    wave.location = (-460, -60)
    try:
        wave.wave_type = "RINGS"
    except Exception:
        pass
    try:
        wave.bands_direction = "Z"
    except Exception:
        pass
    if "Scale" in wave.inputs:
        wave.inputs["Scale"].default_value = FOG_FILAMENT_WAVE_SCALE_MIN
    if "Distortion" in wave.inputs:
        wave.inputs["Distortion"].default_value = 6.0

    wave_weight = nodes.new("ShaderNodeMath")
    wave_weight.name = "FogFilamentWaveWeight"
    wave_weight.location = (-230, -60)
    wave_weight.operation = "MULTIPLY"
    wave_weight.inputs[1].default_value = 0.20

    alpha_mix = nodes.new("ShaderNodeMath")
    alpha_mix.name = "FogFilamentAlphaMask"
    alpha_mix.location = (10, 55)
    alpha_mix.operation = "ADD"
    try:
        alpha_mix.use_clamp = True
    except Exception:
        pass

    alpha_value = nodes.new("ShaderNodeValue")
    alpha_value.name = "FogFilamentAlphaValue"
    alpha_value.location = (10, -120)
    alpha_value.outputs[0].default_value = FOG_FILAMENT_ALPHA_MIN

    alpha_mul = nodes.new("ShaderNodeMath")
    alpha_mul.name = "FogFilamentAlphaMultiply"
    alpha_mul.location = (240, 20)
    alpha_mul.operation = "MULTIPLY"

    emission_value = nodes.new("ShaderNodeValue")
    emission_value.name = "FogFilamentEmissionValue"
    emission_value.location = (240, -155)
    emission_value.outputs[0].default_value = FOG_FILAMENT_EMISSION_MIN

    links.new(texcoord.outputs["Generated"], mapping.inputs["Vector"])
    links.new(mapping.outputs["Vector"], noise.inputs["Vector"])
    links.new(mapping.outputs["Vector"], wave.inputs["Vector"])
    links.new(noise.outputs["Fac"], ramp.inputs["Fac"])
    wave_output = wave.outputs.get("Color") or wave.outputs.get("Fac")
    if wave_output is not None:
        links.new(wave_output, wave_weight.inputs[0])
    links.new(ramp.outputs["Color"], alpha_mix.inputs[0])
    links.new(wave_weight.outputs[0], alpha_mix.inputs[1])
    links.new(alpha_mix.outputs[0], alpha_mul.inputs[0])
    links.new(alpha_value.outputs[0], alpha_mul.inputs[1])

    links.new(alpha_mul.outputs[0], mix_shader.inputs[0])
    links.new(transparent.outputs["BSDF"], mix_shader.inputs[1])
    links.new(emission_shader.outputs["Emission"], mix_shader.inputs[2])
    links.new(emission_value.outputs[0], emission_shader.inputs["Strength"])
    links.new(mix_shader.outputs["Shader"], out.inputs["Surface"])

    controls = {
        "alpha_socket": alpha_value.outputs[0],
        "emission_socket": emission_value.outputs[0],
        "noise_scale_socket": noise.inputs["Scale"],
        "noise_detail_socket": noise.inputs["Detail"],
        "noise_roughness_socket": noise.inputs["Roughness"],
        "mapping_location_socket": mapping.inputs["Location"],
        "mapping_scale_socket": mapping.inputs["Scale"],
        "mapping_rotation_socket": mapping.inputs["Rotation"],
        "wave_scale_socket": wave.inputs.get("Scale"),
        "wave_distortion_socket": wave.inputs.get("Distortion"),
        "wave_phase_socket": wave.inputs.get("Phase Offset"),
        "wave_weight_socket": wave_weight.inputs[1],
        "ramp_low_ctrl": ramp.color_ramp.elements[0],
        "ramp_high_ctrl": ramp.color_ramp.elements[1],
    }

    return mat, controls


def build_mist_particle_material(name, color):
    mat = bpy.data.materials.new(name=name)
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
    out.location = (700, 0)

    mix = nodes.new("ShaderNodeMixShader")
    mix.location = (420, 0)

    transparent = nodes.new("ShaderNodeBsdfTransparent")
    transparent.location = (140, -100)

    emission = nodes.new("ShaderNodeEmission")
    emission.location = (140, 120)
    emission.inputs["Color"].default_value = color
    emission.inputs["Strength"].default_value = 0.14
    emission.name = "MistEmission"

    fac = nodes.new("ShaderNodeValue")
    fac.location = (140, -280)
    fac.outputs[0].default_value = 0.12
    fac.name = "MistMix"

    links.new(fac.outputs[0], mix.inputs[0])
    links.new(transparent.outputs["BSDF"], mix.inputs[1])
    links.new(emission.outputs["Emission"], mix.inputs[2])
    links.new(mix.outputs["Shader"], out.inputs["Surface"])

    return mat, emission.inputs["Strength"], fac.outputs[0]
