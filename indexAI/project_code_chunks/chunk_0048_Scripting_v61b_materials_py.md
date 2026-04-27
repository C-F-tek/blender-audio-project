# Project Code Chunk 48/212

- File: `Scripting/v61b/materials.py`
- Part: `2`
- Lines: `309-562`

## Symbol Map
- Imports: `bpy`, `from config import PEACE_PALETTE, FOG_DENSITY_MIN, FOG_EMISSION_MIN, FOG_NOISE_SCALE_MIN, FOG_CLUMP_SCALE_MIN, FOG_CLUMP_RAMP_LOW_BASE, FOG_CLUMP_RAMP_HIGH_BASE, FOG_WAVE_SCALE_MIN, FOG_WAVE_DISTORTION_MIN, FOG_WAVE_WEIGHT_MIN, FOG_FILAMENT_ALPHA_MIN, FOG_FILAMENT_EMISSION_MIN, FOG_FILAMENT_NOISE_SCALE_MIN, FOG_FILAMENT_WAVE_SCALE_MIN, AURA_EMIT_MIN, RING_EMIT_MIN, RIBBON_EMIT_MIN, BACKDROP_EMISSION_MIN`
- Functions: `build_reflective_floor_material()` line 25; `build_invisible_surface_material(name)` line 67; `build_soft_backdrop_material()` line 91; `build_aura_material()` line 140; `build_variant_material(name, color)` line 186; `build_ring_material(name, color)` line 226; `build_ribbon_material(name, color)` line 248; `build_atmosphere_volume_material()` line 270; `build_fog_filament_material(name)` line 478; `build_mist_particle_material(name, color)` line 618

## Content
```py
00309:     ramp.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
00310: 
00311:     clump_noise = nodes.new("ShaderNodeTexNoise")
00312:     clump_noise.location = (-520, -90)
00313:     clump_noise.name = "FogClumpNoise"
00314:     clump_noise.inputs["Scale"].default_value = FOG_CLUMP_SCALE_MIN
00315:     clump_noise.inputs["Detail"].default_value = 10.0
00316:     clump_noise.inputs["Roughness"].default_value = 0.70
00317: 
00318:     clump_ramp = nodes.new("ShaderNodeValToRGB")
00319:     clump_ramp.location = (-280, -90)
00320:     clump_ramp.name = "FogClumpRamp"
00321:     clump_ramp.color_ramp.elements[0].position = FOG_CLUMP_RAMP_LOW_BASE
00322:     clump_ramp.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
00323:     clump_ramp.color_ramp.elements[1].position = FOG_CLUMP_RAMP_HIGH_BASE
00324:     clump_ramp.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
00325: 
00326:     wave = nodes.new("ShaderNodeTexWave")
00327:     wave.location = (-520, -270)
00328:     wave.name = "FogWindWave"
00329:     try:
00330:         wave.wave_type = 'RINGS'
00331:     except Exception:
00332:         pass
00333:     try:
00334:         wave.bands_direction = 'Z'
00335:     except Exception:
00336:         pass
00337:     if "Scale" in wave.inputs:
00338:         wave.inputs["Scale"].default_value = FOG_WAVE_SCALE_MIN
00339:     if "Distortion" in wave.inputs:
00340:         wave.inputs["Distortion"].default_value = FOG_WAVE_DISTORTION_MIN
00341: 
00342:     wave_weight = nodes.new("ShaderNodeMath")
00343:     wave_weight.location = (-270, -275)
00344:     wave_weight.name = "FogWindWaveWeight"
00345:     wave_weight.operation = 'MULTIPLY'
00346:     wave_weight.inputs[1].default_value = FOG_WAVE_WEIGHT_MIN
00347: 
00348:     clump_mask = nodes.new("ShaderNodeMath")
00349:     clump_mask.location = (-20, 15)
00350:     clump_mask.name = "FogClumpMask"
00351:     clump_mask.operation = 'MULTIPLY'
00352:     try:
00353:         clump_mask.use_clamp = True
00354:     except Exception:
00355:         pass
00356: 
00357:     wave_inside_clumps = nodes.new("ShaderNodeMath")
00358:     wave_inside_clumps.location = (-20, -175)
00359:     wave_inside_clumps.name = "FogWaveInsideClumps"
00360:     wave_inside_clumps.operation = 'MULTIPLY'
00361:     try:
00362:         wave_inside_clumps.use_clamp = True
00363:     except Exception:
00364:         pass
00365: 
00366:     smoke_mix = nodes.new("ShaderNodeMath")
00367:     smoke_mix.location = (190, 30)
00368:     smoke_mix.name = "FogSmokeShapeMix"
00369:     smoke_mix.operation = 'ADD'
00370:     try:
00371:         smoke_mix.use_clamp = True
00372:     except Exception:
00373:         pass
00374: 
00375:     density_val = nodes.new("ShaderNodeValue")
00376:     density_val.location = (-20, -90)
00377:     density_val.outputs[0].default_value = FOG_DENSITY_MIN
00378:     density_val.name = "FogDensityValue"
00379: 
00380:     emission_val = nodes.new("ShaderNodeValue")
00381:     emission_val.location = (-20, -240)
00382:     emission_val.outputs[0].default_value = FOG_EMISSION_MIN
00383:     emission_val.name = "FogEmissionValue"
00384: 
00385:     density_mul = nodes.new("ShaderNodeMath")
00386:     density_mul.location = (410, 40)
00387:     density_mul.operation = 'MULTIPLY'
00388: 
00389:     links.new(texcoord.outputs["Generated"], mapping.inputs["Vector"])
00390:     links.new(mapping.outputs["Vector"], noise.inputs["Vector"])
00391:     links.new(mapping.outputs["Vector"], clump_noise.inputs["Vector"])
00392:     links.new(mapping.outputs["Vector"], wave.inputs["Vector"])
00393:     links.new(noise.outputs["Fac"], ramp.inputs["Fac"])
00394:     links.new(clump_noise.outputs["Fac"], clump_ramp.inputs["Fac"])
00395:     links.new(wave.outputs["Color"], wave_weight.inputs[0])
00396:     links.new(ramp.outputs["Color"], clump_mask.inputs[0])
00397:     links.new(clump_ramp.outputs["Color"], clump_mask.inputs[1])
00398:     links.new(wave_weight.outputs[0], wave_inside_clumps.inputs[0])
00399:     links.new(clump_mask.outputs[0], wave_inside_clumps.inputs[1])
00400:     links.new(clump_mask.outputs[0], smoke_mix.inputs[0])
00401:     links.new(wave_inside_clumps.outputs[0], smoke_mix.inputs[1])
00402:     links.new(smoke_mix.outputs[0], density_mul.inputs[0])
00403:     links.new(density_val.outputs[0], density_mul.inputs[1])
00404: 
00405:     controls = {
00406:         "density_socket": density_val.outputs[0],
00407:         "emission_socket": emission_val.outputs[0],
00408:         "noise_scale_socket": noise.inputs["Scale"],
00409:         "noise_detail_socket": noise.inputs["Detail"],
00410:         "noise_roughness_socket": noise.inputs["Roughness"],
00411:         "clump_noise_scale_socket": clump_noise.inputs["Scale"],
00412:         "clump_noise_detail_socket": clump_noise.inputs["Detail"],
00413:         "clump_noise_roughness_socket": clump_noise.inputs["Roughness"],
00414:         "mapping_location_socket": mapping.inputs["Location"],
00415:         "mapping_scale_socket": mapping.inputs["Scale"],
00416:         "mapping_rotation_socket": mapping.inputs["Rotation"],
00417:         "wave_scale_socket": wave.inputs.get("Scale"),
00418:         "wave_distortion_socket": wave.inputs.get("Distortion"),
00419:         "wave_phase_socket": wave.inputs.get("Phase Offset"),
00420:         "wave_weight_socket": wave_weight.inputs[1],
00421:         "ramp_low_ctrl": ramp.color_ramp.elements[0],
00422:         "ramp_high_ctrl": ramp.color_ramp.elements[1],
00423:         "clump_ramp_low_ctrl": clump_ramp.color_ramp.elements[0],
00424:         "clump_ramp_high_ctrl": clump_ramp.color_ramp.elements[1],
00425:     }
00426: 
00427:     try:
00428:         volume = nodes.new("ShaderNodeVolumePrincipled")
00429:         volume.name = "AtmospherePrincipledVolume"
00430:         volume.location = (500, 0)
00431:         if "Color" in volume.inputs:
00432:             volume.inputs["Color"].default_value = (0.82, 0.89, 0.91, 1.0)
00433:         if "Emission Color" in volume.inputs:
00434:             volume.inputs["Emission Color"].default_value = PEACE_PALETTE["soft_teal"]
00435:         links.new(density_mul.outputs[0], volume.inputs["Density"])
00436:         if "Emission Strength" in volume.inputs:
00437:             links.new(emission_val.outputs[0], volume.inputs["Emission Strength"])
00438:         links.new(volume.outputs["Volume"], out.inputs["Volume"])
00439: 
00440:         for input_name, control_name in [
00441:             ("Color", "volume_color_socket"),
00442:             ("Anisotropy", "volume_anisotropy_socket"),
00443:         ]:
00444:             if input_name in volume.inputs:
00445:                 controls[control_name] = volume.inputs[input_name]
00446:     except Exception:
00447:         scatter = nodes.new("ShaderNodeVolumeScatter")
00448:         scatter.name = "AtmosphereVolumeScatter"
00449:         scatter.location = (500, 90)
00450:         if "Color" in scatter.inputs:
00451:             scatter.inputs["Color"].default_value = (0.82, 0.89, 0.91, 1.0)
00452:         if "Density" in scatter.inputs:
00453:             links.new(density_mul.outputs[0], scatter.inputs["Density"])
00454: 
00455:         absorption = nodes.new("ShaderNodeVolumeAbsorption")
00456:         absorption.name = "AtmosphereVolumeAbsorption"
00457:         absorption.location = (500, -105)
00458:         if "Color" in absorption.inputs:
00459:             absorption.inputs["Color"].default_value = (0.72, 0.86, 0.88, 1.0)
00460:         if "Density" in absorption.inputs:
00461:             links.new(density_mul.outputs[0], absorption.inputs["Density"])
00462: 
00463:         add_volume = nodes.new("ShaderNodeAddShader")
00464:         add_volume.name = "AtmosphereVolumeAdd"
00465:         add_volume.location = (760, 0)
00466:         links.new(scatter.outputs["Volume"], add_volume.inputs[0])
00467:         links.new(absorption.outputs["Volume"], add_volume.inputs[1])
00468:         links.new(add_volume.outputs["Shader"], out.inputs["Volume"])
00469: 
00470:         if "Color" in scatter.inputs:
00471:             controls["volume_color_socket"] = scatter.inputs["Color"]
00472:         if "Anisotropy" in scatter.inputs:
00473:             controls["volume_anisotropy_socket"] = scatter.inputs["Anisotropy"]
00474: 
00475:     return mat, controls
00476: 
00477: 
00478: def build_fog_filament_material(name="FogFilamentMaterial"):
00479:     mat = bpy.data.materials.get(name) or bpy.data.materials.new(name=name)
00480:     mat.use_nodes = True
00481: 
00482:     for attr, value in [
00483:         ("blend_method", 'BLEND'),
00484:         ("shadow_method", 'NONE'),
00485:         ("use_screen_refraction", False),
00486:         ("show_transparent_back", True),
00487:     ]:
00488:         try:
00489:             setattr(mat, attr, value)
00490:         except Exception:
00491:             pass
00492: 
00493:     nodes = mat.node_tree.nodes
00494:     links = mat.node_tree.links
00495:     for n in list(nodes):
00496:         nodes.remove(n)
00497: 
00498:     out = nodes.new("ShaderNodeOutputMaterial")
00499:     out.location = (720, 0)
00500: 
00501:     transparent = nodes.new("ShaderNodeBsdfTransparent")
00502:     transparent.location = (420, 120)
00503: 
00504:     emission_shader = nodes.new("ShaderNodeEmission")
00505:     emission_shader.location = (420, -60)
00506:     emission_shader.inputs["Color"].default_value = (0.58, 0.86, 0.86, 1.0)
00507:     emission_shader.inputs["Strength"].default_value = FOG_FILAMENT_EMISSION_MIN
00508: 
00509:     mix_shader = nodes.new("ShaderNodeMixShader")
00510:     mix_shader.location = (650, 20)
00511: 
00512:     texcoord = nodes.new("ShaderNodeTexCoord")
00513:     texcoord.location = (-900, 120)
00514: 
00515:     mapping = nodes.new("ShaderNodeMapping")
00516:     mapping.name = "FogFilamentMapping"
00517:     mapping.location = (-690, 120)
00518: 
00519:     noise = nodes.new("ShaderNodeTexNoise")
00520:     noise.name = "FogFilamentNoise"
00521:     noise.location = (-460, 135)
00522:     noise.inputs["Scale"].default_value = FOG_FILAMENT_NOISE_SCALE_MIN
00523:     noise.inputs["Detail"].default_value = 13.0
00524:     noise.inputs["Roughness"].default_value = 0.58
00525: 
00526:     ramp = nodes.new("ShaderNodeValToRGB")
00527:     ramp.name = "FogFilamentRamp"
00528:     ramp.location = (-230, 135)
00529:     ramp.color_ramp.elements[0].position = 0.34
00530:     ramp.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
00531:     ramp.color_ramp.elements[1].position = 0.74
00532:     ramp.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
00533: 
00534:     wave = nodes.new("ShaderNodeTexWave")
00535:     wave.name = "FogFilamentWave"
00536:     wave.location = (-460, -60)
00537:     try:
00538:         wave.wave_type = 'RINGS'
00539:     except Exception:
00540:         pass
00541:     try:
00542:         wave.bands_direction = 'Z'
00543:     except Exception:
00544:         pass
00545:     if "Scale" in wave.inputs:
00546:         wave.inputs["Scale"].default_value = FOG_FILAMENT_WAVE_SCALE_MIN
00547:     if "Distortion" in wave.inputs:
00548:         wave.inputs["Distortion"].default_value = 6.0
00549: 
00550:     wave_weight = nodes.new("ShaderNodeMath")
00551:     wave_weight.name = "FogFilamentWaveWeight"
00552:     wave_weight.location = (-230, -60)
00553:     wave_weight.operation = 'MULTIPLY'
00554:     wave_weight.inputs[1].default_value = 0.20
00555: 
00556:     alpha_mix = nodes.new("ShaderNodeMath")
00557:     alpha_mix.name = "FogFilamentAlphaMask"
00558:     alpha_mix.location = (10, 55)
00559:     alpha_mix.operation = 'ADD'
00560:     try:
00561:         alpha_mix.use_clamp = True
00562:     except Exception:
```
