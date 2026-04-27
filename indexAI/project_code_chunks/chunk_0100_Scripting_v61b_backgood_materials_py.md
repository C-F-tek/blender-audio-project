# Project Code Chunk 100/212

- File: `Scripting/v61b_backgood/materials.py`
- Part: `2`
- Lines: `308-513`

## Symbol Map
- Imports: `bpy`, `from config import PEACE_PALETTE, FOG_DENSITY_MIN, FOG_EMISSION_MIN, FOG_NOISE_SCALE_MIN, FOG_CLUMP_SCALE_MIN, FOG_CLUMP_RAMP_LOW_BASE, FOG_CLUMP_RAMP_HIGH_BASE, FOG_WAVE_SCALE_MIN, FOG_WAVE_DISTORTION_MIN, FOG_WAVE_WEIGHT_MIN, AURA_EMIT_MIN, RING_EMIT_MIN, RIBBON_EMIT_MIN, BACKDROP_EMISSION_MIN`
- Functions: `build_reflective_floor_material()` line 21; `build_invisible_surface_material(name)` line 63; `build_soft_backdrop_material()` line 87; `build_aura_material()` line 136; `build_variant_material(name, color)` line 182; `build_ring_material(name, color)` line 222; `build_ribbon_material(name, color)` line 244; `build_atmosphere_volume_material()` line 266; `build_mist_particle_material(name, color)` line 474

## Content
```py
00308:     clump_noise.location = (-520, -90)
00309:     clump_noise.name = "FogClumpNoise"
00310:     clump_noise.inputs["Scale"].default_value = FOG_CLUMP_SCALE_MIN
00311:     clump_noise.inputs["Detail"].default_value = 10.0
00312:     clump_noise.inputs["Roughness"].default_value = 0.70
00313: 
00314:     clump_ramp = nodes.new("ShaderNodeValToRGB")
00315:     clump_ramp.location = (-280, -90)
00316:     clump_ramp.name = "FogClumpRamp"
00317:     clump_ramp.color_ramp.elements[0].position = FOG_CLUMP_RAMP_LOW_BASE
00318:     clump_ramp.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
00319:     clump_ramp.color_ramp.elements[1].position = FOG_CLUMP_RAMP_HIGH_BASE
00320:     clump_ramp.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
00321: 
00322:     wave = nodes.new("ShaderNodeTexWave")
00323:     wave.location = (-520, -270)
00324:     wave.name = "FogWindWave"
00325:     try:
00326:         wave.wave_type = 'RINGS'
00327:     except Exception:
00328:         pass
00329:     try:
00330:         wave.bands_direction = 'Z'
00331:     except Exception:
00332:         pass
00333:     if "Scale" in wave.inputs:
00334:         wave.inputs["Scale"].default_value = FOG_WAVE_SCALE_MIN
00335:     if "Distortion" in wave.inputs:
00336:         wave.inputs["Distortion"].default_value = FOG_WAVE_DISTORTION_MIN
00337: 
00338:     wave_weight = nodes.new("ShaderNodeMath")
00339:     wave_weight.location = (-270, -275)
00340:     wave_weight.name = "FogWindWaveWeight"
00341:     wave_weight.operation = 'MULTIPLY'
00342:     wave_weight.inputs[1].default_value = FOG_WAVE_WEIGHT_MIN
00343: 
00344:     clump_mask = nodes.new("ShaderNodeMath")
00345:     clump_mask.location = (-20, 15)
00346:     clump_mask.name = "FogClumpMask"
00347:     clump_mask.operation = 'MULTIPLY'
00348:     try:
00349:         clump_mask.use_clamp = True
00350:     except Exception:
00351:         pass
00352: 
00353:     wave_inside_clumps = nodes.new("ShaderNodeMath")
00354:     wave_inside_clumps.location = (-20, -175)
00355:     wave_inside_clumps.name = "FogWaveInsideClumps"
00356:     wave_inside_clumps.operation = 'MULTIPLY'
00357:     try:
00358:         wave_inside_clumps.use_clamp = True
00359:     except Exception:
00360:         pass
00361: 
00362:     smoke_mix = nodes.new("ShaderNodeMath")
00363:     smoke_mix.location = (190, 30)
00364:     smoke_mix.name = "FogSmokeShapeMix"
00365:     smoke_mix.operation = 'ADD'
00366:     try:
00367:         smoke_mix.use_clamp = True
00368:     except Exception:
00369:         pass
00370: 
00371:     density_val = nodes.new("ShaderNodeValue")
00372:     density_val.location = (-20, -90)
00373:     density_val.outputs[0].default_value = FOG_DENSITY_MIN
00374:     density_val.name = "FogDensityValue"
00375: 
00376:     emission_val = nodes.new("ShaderNodeValue")
00377:     emission_val.location = (-20, -240)
00378:     emission_val.outputs[0].default_value = FOG_EMISSION_MIN
00379:     emission_val.name = "FogEmissionValue"
00380: 
00381:     density_mul = nodes.new("ShaderNodeMath")
00382:     density_mul.location = (410, 40)
00383:     density_mul.operation = 'MULTIPLY'
00384: 
00385:     links.new(texcoord.outputs["Generated"], mapping.inputs["Vector"])
00386:     links.new(mapping.outputs["Vector"], noise.inputs["Vector"])
00387:     links.new(mapping.outputs["Vector"], clump_noise.inputs["Vector"])
00388:     links.new(mapping.outputs["Vector"], wave.inputs["Vector"])
00389:     links.new(noise.outputs["Fac"], ramp.inputs["Fac"])
00390:     links.new(clump_noise.outputs["Fac"], clump_ramp.inputs["Fac"])
00391:     links.new(wave.outputs["Color"], wave_weight.inputs[0])
00392:     links.new(ramp.outputs["Color"], clump_mask.inputs[0])
00393:     links.new(clump_ramp.outputs["Color"], clump_mask.inputs[1])
00394:     links.new(wave_weight.outputs[0], wave_inside_clumps.inputs[0])
00395:     links.new(clump_mask.outputs[0], wave_inside_clumps.inputs[1])
00396:     links.new(clump_mask.outputs[0], smoke_mix.inputs[0])
00397:     links.new(wave_inside_clumps.outputs[0], smoke_mix.inputs[1])
00398:     links.new(smoke_mix.outputs[0], density_mul.inputs[0])
00399:     links.new(density_val.outputs[0], density_mul.inputs[1])
00400: 
00401:     controls = {
00402:         "density_socket": density_val.outputs[0],
00403:         "emission_socket": emission_val.outputs[0],
00404:         "noise_scale_socket": noise.inputs["Scale"],
00405:         "noise_detail_socket": noise.inputs["Detail"],
00406:         "noise_roughness_socket": noise.inputs["Roughness"],
00407:         "clump_noise_scale_socket": clump_noise.inputs["Scale"],
00408:         "clump_noise_detail_socket": clump_noise.inputs["Detail"],
00409:         "clump_noise_roughness_socket": clump_noise.inputs["Roughness"],
00410:         "mapping_location_socket": mapping.inputs["Location"],
00411:         "mapping_scale_socket": mapping.inputs["Scale"],
00412:         "mapping_rotation_socket": mapping.inputs["Rotation"],
00413:         "wave_scale_socket": wave.inputs.get("Scale"),
00414:         "wave_distortion_socket": wave.inputs.get("Distortion"),
00415:         "wave_phase_socket": wave.inputs.get("Phase Offset"),
00416:         "wave_weight_socket": wave_weight.inputs[1],
00417:         "ramp_low_ctrl": ramp.color_ramp.elements[0],
00418:         "ramp_high_ctrl": ramp.color_ramp.elements[1],
00419:         "clump_ramp_low_ctrl": clump_ramp.color_ramp.elements[0],
00420:         "clump_ramp_high_ctrl": clump_ramp.color_ramp.elements[1],
00421:     }
00422: 
00423:     try:
00424:         volume = nodes.new("ShaderNodeVolumePrincipled")
00425:         volume.name = "AtmospherePrincipledVolume"
00426:         volume.location = (500, 0)
00427:         if "Color" in volume.inputs:
00428:             volume.inputs["Color"].default_value = (0.82, 0.89, 0.91, 1.0)
00429:         if "Emission Color" in volume.inputs:
00430:             volume.inputs["Emission Color"].default_value = PEACE_PALETTE["soft_teal"]
00431:         links.new(density_mul.outputs[0], volume.inputs["Density"])
00432:         if "Emission Strength" in volume.inputs:
00433:             links.new(emission_val.outputs[0], volume.inputs["Emission Strength"])
00434:         links.new(volume.outputs["Volume"], out.inputs["Volume"])
00435: 
00436:         for input_name, control_name in [
00437:             ("Color", "volume_color_socket"),
00438:             ("Anisotropy", "volume_anisotropy_socket"),
00439:         ]:
00440:             if input_name in volume.inputs:
00441:                 controls[control_name] = volume.inputs[input_name]
00442:     except Exception:
00443:         scatter = nodes.new("ShaderNodeVolumeScatter")
00444:         scatter.name = "AtmosphereVolumeScatter"
00445:         scatter.location = (500, 90)
00446:         if "Color" in scatter.inputs:
00447:             scatter.inputs["Color"].default_value = (0.82, 0.89, 0.91, 1.0)
00448:         if "Density" in scatter.inputs:
00449:             links.new(density_mul.outputs[0], scatter.inputs["Density"])
00450: 
00451:         absorption = nodes.new("ShaderNodeVolumeAbsorption")
00452:         absorption.name = "AtmosphereVolumeAbsorption"
00453:         absorption.location = (500, -105)
00454:         if "Color" in absorption.inputs:
00455:             absorption.inputs["Color"].default_value = (0.72, 0.86, 0.88, 1.0)
00456:         if "Density" in absorption.inputs:
00457:             links.new(density_mul.outputs[0], absorption.inputs["Density"])
00458: 
00459:         add_volume = nodes.new("ShaderNodeAddShader")
00460:         add_volume.name = "AtmosphereVolumeAdd"
00461:         add_volume.location = (760, 0)
00462:         links.new(scatter.outputs["Volume"], add_volume.inputs[0])
00463:         links.new(absorption.outputs["Volume"], add_volume.inputs[1])
00464:         links.new(add_volume.outputs["Shader"], out.inputs["Volume"])
00465: 
00466:         if "Color" in scatter.inputs:
00467:             controls["volume_color_socket"] = scatter.inputs["Color"]
00468:         if "Anisotropy" in scatter.inputs:
00469:             controls["volume_anisotropy_socket"] = scatter.inputs["Anisotropy"]
00470: 
00471:     return mat, controls
00472: 
00473: 
00474: def build_mist_particle_material(name, color):
00475:     mat = bpy.data.materials.new(name=name)
00476:     mat.use_nodes = True
00477: 
00478:     if hasattr(mat, "blend_method"):
00479:         mat.blend_method = 'BLEND'
00480:     if hasattr(mat, "shadow_method"):
00481:         mat.shadow_method = 'NONE'
00482: 
00483:     nodes = mat.node_tree.nodes
00484:     links = mat.node_tree.links
00485:     for n in list(nodes):
00486:         nodes.remove(n)
00487: 
00488:     out = nodes.new("ShaderNodeOutputMaterial")
00489:     out.location = (700, 0)
00490: 
00491:     mix = nodes.new("ShaderNodeMixShader")
00492:     mix.location = (420, 0)
00493: 
00494:     transparent = nodes.new("ShaderNodeBsdfTransparent")
00495:     transparent.location = (140, -100)
00496: 
00497:     emission = nodes.new("ShaderNodeEmission")
00498:     emission.location = (140, 120)
00499:     emission.inputs["Color"].default_value = color
00500:     emission.inputs["Strength"].default_value = 0.14
00501:     emission.name = "MistEmission"
00502: 
00503:     fac = nodes.new("ShaderNodeValue")
00504:     fac.location = (140, -280)
00505:     fac.outputs[0].default_value = 0.12
00506:     fac.name = "MistMix"
00507: 
00508:     links.new(fac.outputs[0], mix.inputs[0])
00509:     links.new(transparent.outputs["BSDF"], mix.inputs[1])
00510:     links.new(emission.outputs["Emission"], mix.inputs[2])
00511:     links.new(mix.outputs["Shader"], out.inputs["Surface"])
00512: 
00513:     return mat, emission.inputs["Strength"], fac.outputs[0]
```
