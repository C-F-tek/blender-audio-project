# Project Code Chunk 49/212

- File: `Scripting/v61b/materials.py`
- Part: `3`
- Lines: `563-657`

## Symbol Map
- Imports: `bpy`, `from config import PEACE_PALETTE, FOG_DENSITY_MIN, FOG_EMISSION_MIN, FOG_NOISE_SCALE_MIN, FOG_CLUMP_SCALE_MIN, FOG_CLUMP_RAMP_LOW_BASE, FOG_CLUMP_RAMP_HIGH_BASE, FOG_WAVE_SCALE_MIN, FOG_WAVE_DISTORTION_MIN, FOG_WAVE_WEIGHT_MIN, FOG_FILAMENT_ALPHA_MIN, FOG_FILAMENT_EMISSION_MIN, FOG_FILAMENT_NOISE_SCALE_MIN, FOG_FILAMENT_WAVE_SCALE_MIN, AURA_EMIT_MIN, RING_EMIT_MIN, RIBBON_EMIT_MIN, BACKDROP_EMISSION_MIN`
- Functions: `build_reflective_floor_material()` line 25; `build_invisible_surface_material(name)` line 67; `build_soft_backdrop_material()` line 91; `build_aura_material()` line 140; `build_variant_material(name, color)` line 186; `build_ring_material(name, color)` line 226; `build_ribbon_material(name, color)` line 248; `build_atmosphere_volume_material()` line 270; `build_fog_filament_material(name)` line 478; `build_mist_particle_material(name, color)` line 618

## Content
```py
00563:         pass
00564: 
00565:     alpha_value = nodes.new("ShaderNodeValue")
00566:     alpha_value.name = "FogFilamentAlphaValue"
00567:     alpha_value.location = (10, -120)
00568:     alpha_value.outputs[0].default_value = FOG_FILAMENT_ALPHA_MIN
00569: 
00570:     alpha_mul = nodes.new("ShaderNodeMath")
00571:     alpha_mul.name = "FogFilamentAlphaMultiply"
00572:     alpha_mul.location = (240, 20)
00573:     alpha_mul.operation = 'MULTIPLY'
00574: 
00575:     emission_value = nodes.new("ShaderNodeValue")
00576:     emission_value.name = "FogFilamentEmissionValue"
00577:     emission_value.location = (240, -155)
00578:     emission_value.outputs[0].default_value = FOG_FILAMENT_EMISSION_MIN
00579: 
00580:     links.new(texcoord.outputs["Generated"], mapping.inputs["Vector"])
00581:     links.new(mapping.outputs["Vector"], noise.inputs["Vector"])
00582:     links.new(mapping.outputs["Vector"], wave.inputs["Vector"])
00583:     links.new(noise.outputs["Fac"], ramp.inputs["Fac"])
00584:     wave_output = wave.outputs.get("Color") or wave.outputs.get("Fac")
00585:     if wave_output is not None:
00586:         links.new(wave_output, wave_weight.inputs[0])
00587:     links.new(ramp.outputs["Color"], alpha_mix.inputs[0])
00588:     links.new(wave_weight.outputs[0], alpha_mix.inputs[1])
00589:     links.new(alpha_mix.outputs[0], alpha_mul.inputs[0])
00590:     links.new(alpha_value.outputs[0], alpha_mul.inputs[1])
00591: 
00592:     links.new(alpha_mul.outputs[0], mix_shader.inputs[0])
00593:     links.new(transparent.outputs["BSDF"], mix_shader.inputs[1])
00594:     links.new(emission_shader.outputs["Emission"], mix_shader.inputs[2])
00595:     links.new(emission_value.outputs[0], emission_shader.inputs["Strength"])
00596:     links.new(mix_shader.outputs["Shader"], out.inputs["Surface"])
00597: 
00598:     controls = {
00599:         "alpha_socket": alpha_value.outputs[0],
00600:         "emission_socket": emission_value.outputs[0],
00601:         "noise_scale_socket": noise.inputs["Scale"],
00602:         "noise_detail_socket": noise.inputs["Detail"],
00603:         "noise_roughness_socket": noise.inputs["Roughness"],
00604:         "mapping_location_socket": mapping.inputs["Location"],
00605:         "mapping_scale_socket": mapping.inputs["Scale"],
00606:         "mapping_rotation_socket": mapping.inputs["Rotation"],
00607:         "wave_scale_socket": wave.inputs.get("Scale"),
00608:         "wave_distortion_socket": wave.inputs.get("Distortion"),
00609:         "wave_phase_socket": wave.inputs.get("Phase Offset"),
00610:         "wave_weight_socket": wave_weight.inputs[1],
00611:         "ramp_low_ctrl": ramp.color_ramp.elements[0],
00612:         "ramp_high_ctrl": ramp.color_ramp.elements[1],
00613:     }
00614: 
00615:     return mat, controls
00616: 
00617: 
00618: def build_mist_particle_material(name, color):
00619:     mat = bpy.data.materials.new(name=name)
00620:     mat.use_nodes = True
00621: 
00622:     if hasattr(mat, "blend_method"):
00623:         mat.blend_method = 'BLEND'
00624:     if hasattr(mat, "shadow_method"):
00625:         mat.shadow_method = 'NONE'
00626: 
00627:     nodes = mat.node_tree.nodes
00628:     links = mat.node_tree.links
00629:     for n in list(nodes):
00630:         nodes.remove(n)
00631: 
00632:     out = nodes.new("ShaderNodeOutputMaterial")
00633:     out.location = (700, 0)
00634: 
00635:     mix = nodes.new("ShaderNodeMixShader")
00636:     mix.location = (420, 0)
00637: 
00638:     transparent = nodes.new("ShaderNodeBsdfTransparent")
00639:     transparent.location = (140, -100)
00640: 
00641:     emission = nodes.new("ShaderNodeEmission")
00642:     emission.location = (140, 120)
00643:     emission.inputs["Color"].default_value = color
00644:     emission.inputs["Strength"].default_value = 0.14
00645:     emission.name = "MistEmission"
00646: 
00647:     fac = nodes.new("ShaderNodeValue")
00648:     fac.location = (140, -280)
00649:     fac.outputs[0].default_value = 0.12
00650:     fac.name = "MistMix"
00651: 
00652:     links.new(fac.outputs[0], mix.inputs[0])
00653:     links.new(transparent.outputs["BSDF"], mix.inputs[1])
00654:     links.new(emission.outputs["Emission"], mix.inputs[2])
00655:     links.new(mix.outputs["Shader"], out.inputs["Surface"])
00656: 
00657:     return mat, emission.inputs["Strength"], fac.outputs[0]
```
