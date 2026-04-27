# Project Code Chunk 18/212

- File: `Scripting/v61b/asset_setup.py`
- Part: `2`
- Lines: `317-580`

## Symbol Map
- Imports: `bpy`, `from mathutils import Vector`, `from pathlib import Path`, `from config import PRIMARY_ASSET_DIR, PRIMARY_TARGET_SIZE, PRIMARY_BASE_Z, SUPPORTED_ASSET_EXTENSIONS, USE_SECONDARY_ASSET, SECONDARY_ASSET_DIR, SECONDARY_TARGET_SIZE, SECONDARY_BASE_Z, SECONDARY_BASE_OFFSET_X, SECONDARY_BASE_OFFSET_Y, SECONDARY_BASE_OFFSET_Z, PEACE_PALETTE, USE_HERO_MESH_DEFORM, HERO_DEFORM_STRENGTH_MAX, HERO_DEFORM_STRENGTH_MIN, HERO_DEFORM_DETAIL_STRENGTH_MAX, HERO_DEFORM_WAVE_HEIGHT_MAX, HERO_DEFORM_MAIN_DIM_FACTOR, HERO_DEFORM_DETAIL_DIM_FACTOR, HERO_DEFORM_WAVE_DIM_FACTOR, HERO_DEFORM_TWIST_MAX, HERO_DEFORM_SUBDIV_VIEW, HERO_DEFORM_SUBDIV_RENDER, HERO_DEFORM_NOISE_SIZE, HERO_DEFORM_DETAIL_NOISE_SIZE, HERO_DEFORM_NOISE_CONTRAST, HERO_DEFORM_CONTROLLER_Z, USE_HERO_MATERIAL_AUDIO_NODES, HERO_MATERIAL_EMISSION_MIN, HERO_MATERIAL_SELF_LIGHT_MIN, HERO_MATERIAL_BUMP_MIN, HERO_MATERIAL_ROUGHNESS_MAX, HERO_MATERIAL_NOISE_SCALE_MIN`, `from scene_utils import create_controller_empty`
- Functions: `find_asset_file(asset_dir)` line 43; `import_asset_file(asset_file)` line 62; `get_world_bbox(objects)` line 94; `create_scene_core()` line 127; `make_asset_root(name)` line 134; `parent_objects_keep_transform(objects, parent)` line 141; `center_and_scale_asset(root, objects, target_size, base_z)` line 150; `collect_meshes(objects)` line 171; `soften_materials_to_peace(meshes)` line 175; `find_principled_node(material)` line 206; `get_node_input(node)` line 216; `link_node_sockets(links, output_socket, input_socket, replace_existing)` line 226; `get_or_create_node(nodes, node_type, name, location)` line 243; `find_material_output(material)` line 252; `ensure_hero_surface_light_layer(mat, principled)` line 266; `get_local_mesh_extent(obj)` line 346; `add_hero_material_audio_nodes(meshes)` line 360; `duplicate_hierarchy(root, name_prefix)` line 460; `assign_material_to_hierarchy(root, material)` line 488; `add_hero_mesh_deformers(asset_root, meshes)` line 498; `_create_asset_from_dir(asset_dir, target_size, base_z, root_name, parent)` line 653; `create_primary_asset(parent)` line 688; `create_secondary_asset(parent)` line 698

## Content
```py
00317:         nodes,
00318:         "ShaderNodeAddShader",
00319:         "HeroMatSelfLightAdd",
00320:         (620, 120),
00321:     )
00322: 
00323:     link_node_sockets(links, self_light.outputs[0], edge_mul.inputs[0], replace_existing=True)
00324:     link_node_sockets(links, layer.outputs.get("Fresnel"), edge_ramp.inputs["Fac"], replace_existing=True)
00325:     link_node_sockets(links, edge_ramp.outputs["Color"], edge_mul.inputs[1], replace_existing=True)
00326:     link_node_sockets(links, edge_mul.outputs[0], emission.inputs["Strength"], replace_existing=True)
00327:     link_node_sockets(links, emission.outputs["Emission"], add_shader.inputs[1], replace_existing=True)
00328: 
00329:     surface_input = output.inputs["Surface"]
00330:     if surface_input.is_linked and surface_input.links[0].from_node == add_shader:
00331:         return self_light.outputs[0]
00332: 
00333:     original_socket = None
00334:     if surface_input.is_linked:
00335:         original_socket = surface_input.links[0].from_socket
00336:         for link in list(surface_input.links):
00337:             links.remove(link)
00338:     elif "BSDF" in principled.outputs:
00339:         original_socket = principled.outputs["BSDF"]
00340: 
00341:     link_node_sockets(links, original_socket, add_shader.inputs[0], replace_existing=True)
00342:     link_node_sockets(links, add_shader.outputs["Shader"], surface_input, replace_existing=True)
00343:     return self_light.outputs[0]
00344: 
00345: 
00346: def get_local_mesh_extent(obj):
00347:     try:
00348:         corners = [Vector(corner) for corner in obj.bound_box]
00349:         min_v = Vector((min(v.x for v in corners), min(v.y for v in corners), min(v.z for v in corners)))
00350:         max_v = Vector((max(v.x for v in corners), max(v.y for v in corners), max(v.z for v in corners)))
00351:         size = max_v - min_v
00352:         return max(size.x, size.y, size.z, 0.001)
00353:     except Exception:
00354:         try:
00355:             return max(obj.dimensions.x, obj.dimensions.y, obj.dimensions.z, 0.001)
00356:         except Exception:
00357:             return 1.0
00358: 
00359: 
00360: def add_hero_material_audio_nodes(meshes):
00361:     if not USE_HERO_MATERIAL_AUDIO_NODES:
00362:         return []
00363: 
00364:     controls = []
00365:     seen_materials = set()
00366: 
00367:     for obj in meshes:
00368:         for slot in obj.material_slots:
00369:             mat = slot.material
00370:             if mat is None or not mat.use_nodes:
00371:                 continue
00372: 
00373:             mat_key = mat.name
00374:             if mat_key in seen_materials:
00375:                 continue
00376:             seen_materials.add(mat_key)
00377: 
00378:             principled = find_principled_node(mat)
00379:             if principled is None:
00380:                 continue
00381: 
00382:             nodes = mat.node_tree.nodes
00383:             links = mat.node_tree.links
00384: 
00385:             rough_input = get_node_input(principled, "Roughness")
00386:             emission_color_input = get_node_input(principled, "Emission Color", "Emission")
00387:             emission_strength_input = get_node_input(principled, "Emission Strength")
00388:             normal_input = get_node_input(principled, "Normal")
00389: 
00390:             emission_value = nodes.new("ShaderNodeValue")
00391:             emission_value.name = "HeroMatEmissionValue"
00392:             emission_value.label = "Audio Emission"
00393:             emission_value.location = (-520, 280)
00394:             emission_value.outputs[0].default_value = HERO_MATERIAL_EMISSION_MIN
00395: 
00396:             roughness_value = nodes.new("ShaderNodeValue")
00397:             roughness_value.name = "HeroMatRoughnessValue"
00398:             roughness_value.label = "Audio Roughness"
00399:             roughness_value.location = (-520, 100)
00400:             roughness_value.outputs[0].default_value = HERO_MATERIAL_ROUGHNESS_MAX
00401: 
00402:             bump_value = nodes.new("ShaderNodeValue")
00403:             bump_value.name = "HeroMatBumpStrength"
00404:             bump_value.label = "Audio Bump"
00405:             bump_value.location = (-520, -110)
00406:             bump_value.outputs[0].default_value = HERO_MATERIAL_BUMP_MIN
00407: 
00408:             texcoord = nodes.new("ShaderNodeTexCoord")
00409:             texcoord.name = "HeroMatTextureCoords"
00410:             texcoord.location = (-930, -220)
00411: 
00412:             mapping = nodes.new("ShaderNodeMapping")
00413:             mapping.name = "HeroMatAudioMapping"
00414:             mapping.location = (-720, -220)
00415: 
00416:             noise = nodes.new("ShaderNodeTexNoise")
00417:             noise.name = "HeroMatAudioNoise"
00418:             noise.location = (-500, -260)
00419:             noise.inputs["Scale"].default_value = HERO_MATERIAL_NOISE_SCALE_MIN
00420:             noise.inputs["Detail"].default_value = 12.0
00421:             noise.inputs["Roughness"].default_value = 0.62
00422: 
00423:             bump = nodes.new("ShaderNodeBump")
00424:             bump.name = "HeroMatAudioBump"
00425:             bump.location = (-245, -215)
00426:             bump.inputs["Strength"].default_value = HERO_MATERIAL_BUMP_MIN
00427:             bump.inputs["Distance"].default_value = 0.28
00428: 
00429:             try:
00430:                 if emission_color_input is not None:
00431:                     emission_color_input.default_value = PEACE_PALETTE["muted_gold"]
00432:             except Exception:
00433:                 pass
00434: 
00435:             self_light_socket = ensure_hero_surface_light_layer(mat, principled)
00436: 
00437:             link_node_sockets(links, emission_value.outputs[0], emission_strength_input, replace_existing=True)
00438:             link_node_sockets(links, roughness_value.outputs[0], rough_input, replace_existing=True)
00439:             link_node_sockets(links, texcoord.outputs.get("Generated"), mapping.inputs.get("Vector"))
00440:             link_node_sockets(links, mapping.outputs.get("Vector"), noise.inputs.get("Vector"))
00441:             link_node_sockets(links, noise.outputs.get("Fac"), bump.inputs.get("Height"))
00442:             link_node_sockets(links, bump_value.outputs[0], bump.inputs.get("Strength"), replace_existing=True)
00443:             link_node_sockets(links, bump.outputs.get("Normal"), normal_input)
00444: 
00445:             controls.append({
00446:                 "material": mat,
00447:                 "node_tree": mat.node_tree,
00448:                 "emission_socket": emission_value.outputs[0],
00449:                 "self_light_socket": self_light_socket,
00450:                 "roughness_socket": roughness_value.outputs[0],
00451:                 "bump_socket": bump_value.outputs[0],
00452:                 "noise_scale_socket": noise.inputs["Scale"],
00453:                 "mapping_location_socket": mapping.inputs["Location"],
00454:                 "mapping_rotation_socket": mapping.inputs["Rotation"],
00455:             })
00456: 
00457:     return controls
00458: 
00459: 
00460: def duplicate_hierarchy(root, name_prefix):
00461:     before = set(bpy.data.objects)
00462: 
00463:     for obj in bpy.data.objects:
00464:         obj.select_set(False)
00465: 
00466:     root.select_set(True)
00467:     for child in root.children_recursive:
00468:         child.select_set(True)
00469: 
00470:     bpy.context.view_layer.objects.active = root
00471:     bpy.ops.object.duplicate(linked=False)
00472: 
00473:     created = [obj for obj in bpy.data.objects if obj not in before]
00474:     created_root = None
00475: 
00476:     for obj in created:
00477:         if obj.type == 'EMPTY':
00478:             created_root = obj
00479:             break
00480: 
00481:     if created_root is None:
00482:         raise RuntimeError("Impossibile duplicare la gerarchia dell'asset.")
00483: 
00484:     created_root.name = name_prefix
00485:     return created_root
00486: 
00487: 
00488: def assign_material_to_hierarchy(root, material):
00489:     meshes = [obj for obj in root.children_recursive if obj.type == 'MESH']
00490:     if root.type == 'MESH':
00491:         meshes.append(root)
00492: 
00493:     for obj in meshes:
00494:         obj.data.materials.clear()
00495:         obj.data.materials.append(material)
00496: 
00497: 
00498: def add_hero_mesh_deformers(asset_root, meshes):
00499:     if not USE_HERO_MESH_DEFORM:
00500:         return {
00501:             "controller": None,
00502:             "deformers": [],
00503:         }
00504: 
00505:     controller = create_controller_empty(
00506:         "HeroDeformController",
00507:         location=(0, 0, HERO_DEFORM_CONTROLLER_Z),
00508:         parent=asset_root,
00509:         display_size=0.32,
00510:         hide_view=True,
00511:     )
00512: 
00513:     deformers = []
00514:     for idx, obj in enumerate(meshes):
00515:         local_extent = get_local_mesh_extent(obj)
00516:         main_strength_max = max(HERO_DEFORM_STRENGTH_MAX, local_extent * HERO_DEFORM_MAIN_DIM_FACTOR)
00517:         detail_strength_max = max(HERO_DEFORM_DETAIL_STRENGTH_MAX, local_extent * HERO_DEFORM_DETAIL_DIM_FACTOR)
00518:         wave_height_max = max(HERO_DEFORM_WAVE_HEIGHT_MAX, local_extent * HERO_DEFORM_WAVE_DIM_FACTOR)
00519: 
00520:         try:
00521:             subdiv = obj.modifiers.new("HeroAudioSubdivision", 'SUBSURF')
00522:             subdiv.levels = HERO_DEFORM_SUBDIV_VIEW
00523:             subdiv.render_levels = HERO_DEFORM_SUBDIV_RENDER
00524:         except Exception:
00525:             subdiv = None
00526: 
00527:         try:
00528:             tex = bpy.data.textures.new(f"HeroAudioDisplaceTexture_{idx:02d}", type='VORONOI')
00529:         except Exception:
00530:             try:
00531:                 tex = bpy.data.textures.new(f"HeroAudioDisplaceTexture_{idx:02d}", type='CLOUDS')
00532:             except Exception:
00533:                 continue
00534: 
00535:         for attr, value in [
00536:             ("noise_scale", HERO_DEFORM_NOISE_SIZE),
00537:             ("intensity", 0.48),
00538:             ("contrast", HERO_DEFORM_NOISE_CONTRAST),
00539:         ]:
00540:             try:
00541:                 setattr(tex, attr, value)
00542:             except Exception:
00543:                 pass
00544: 
00545:         mod = obj.modifiers.new("HeroAudioMeshDisplace", 'DISPLACE')
00546:         mod.strength = HERO_DEFORM_STRENGTH_MIN
00547:         mod.mid_level = 0.50
00548:         mod.texture = tex
00549: 
00550:         try:
00551:             mod.direction = 'NORMAL'
00552:         except Exception:
00553:             pass
00554: 
00555:         try:
00556:             mod.texture_coords = 'OBJECT'
00557:             mod.texture_coords_object = controller
00558:         except Exception:
00559:             pass
00560: 
00561:         try:
00562:             mod.show_render = True
00563:             mod.show_viewport = True
00564:         except Exception:
00565:             pass
00566: 
00567:         deformers.append({
00568:             "mesh": obj,
00569:             "subdivision": subdiv,
00570:             "modifier": mod,
00571:             "texture": tex,
00572:             "detail_modifier": None,
00573:             "detail_texture": None,
00574:             "wave_modifier": None,
00575:             "twist_modifier": None,
00576:             "phase": idx * 0.61,
00577:             "main_strength_max": main_strength_max,
00578:             "detail_strength_max": detail_strength_max,
00579:             "wave_height_max": wave_height_max,
00580:             "twist_angle_max": HERO_DEFORM_TWIST_MAX,
```
