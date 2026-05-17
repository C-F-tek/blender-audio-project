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
