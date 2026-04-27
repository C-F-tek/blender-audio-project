# Project Code Chunk 19/212

- File: `Scripting/v61b/asset_setup.py`
- Part: `3`
- Lines: `581-725`

## Symbol Map
- Imports: `bpy`, `from mathutils import Vector`, `from pathlib import Path`, `from config import PRIMARY_ASSET_DIR, PRIMARY_TARGET_SIZE, PRIMARY_BASE_Z, SUPPORTED_ASSET_EXTENSIONS, USE_SECONDARY_ASSET, SECONDARY_ASSET_DIR, SECONDARY_TARGET_SIZE, SECONDARY_BASE_Z, SECONDARY_BASE_OFFSET_X, SECONDARY_BASE_OFFSET_Y, SECONDARY_BASE_OFFSET_Z, PEACE_PALETTE, USE_HERO_MESH_DEFORM, HERO_DEFORM_STRENGTH_MAX, HERO_DEFORM_STRENGTH_MIN, HERO_DEFORM_DETAIL_STRENGTH_MAX, HERO_DEFORM_WAVE_HEIGHT_MAX, HERO_DEFORM_MAIN_DIM_FACTOR, HERO_DEFORM_DETAIL_DIM_FACTOR, HERO_DEFORM_WAVE_DIM_FACTOR, HERO_DEFORM_TWIST_MAX, HERO_DEFORM_SUBDIV_VIEW, HERO_DEFORM_SUBDIV_RENDER, HERO_DEFORM_NOISE_SIZE, HERO_DEFORM_DETAIL_NOISE_SIZE, HERO_DEFORM_NOISE_CONTRAST, HERO_DEFORM_CONTROLLER_Z, USE_HERO_MATERIAL_AUDIO_NODES, HERO_MATERIAL_EMISSION_MIN, HERO_MATERIAL_SELF_LIGHT_MIN, HERO_MATERIAL_BUMP_MIN, HERO_MATERIAL_ROUGHNESS_MAX, HERO_MATERIAL_NOISE_SCALE_MIN`, `from scene_utils import create_controller_empty`
- Functions: `find_asset_file(asset_dir)` line 43; `import_asset_file(asset_file)` line 62; `get_world_bbox(objects)` line 94; `create_scene_core()` line 127; `make_asset_root(name)` line 134; `parent_objects_keep_transform(objects, parent)` line 141; `center_and_scale_asset(root, objects, target_size, base_z)` line 150; `collect_meshes(objects)` line 171; `soften_materials_to_peace(meshes)` line 175; `find_principled_node(material)` line 206; `get_node_input(node)` line 216; `link_node_sockets(links, output_socket, input_socket, replace_existing)` line 226; `get_or_create_node(nodes, node_type, name, location)` line 243; `find_material_output(material)` line 252; `ensure_hero_surface_light_layer(mat, principled)` line 266; `get_local_mesh_extent(obj)` line 346; `add_hero_material_audio_nodes(meshes)` line 360; `duplicate_hierarchy(root, name_prefix)` line 460; `assign_material_to_hierarchy(root, material)` line 488; `add_hero_mesh_deformers(asset_root, meshes)` line 498; `_create_asset_from_dir(asset_dir, target_size, base_z, root_name, parent)` line 653; `create_primary_asset(parent)` line 688; `create_secondary_asset(parent)` line 698

## Content
```py
00581:         })
00582: 
00583:         try:
00584:             detail_tex = bpy.data.textures.new(f"HeroAudioDetailTexture_{idx:02d}", type='CLOUDS')
00585:             for attr, value in [
00586:                 ("noise_scale", HERO_DEFORM_DETAIL_NOISE_SIZE),
00587:                 ("noise_depth", 6),
00588:                 ("contrast", HERO_DEFORM_NOISE_CONTRAST),
00589:             ]:
00590:                 try:
00591:                     setattr(detail_tex, attr, value)
00592:                 except Exception:
00593:                     pass
00594: 
00595:             detail = obj.modifiers.new("HeroAudioFineDisplace", 'DISPLACE')
00596:             detail.strength = HERO_DEFORM_STRENGTH_MIN
00597:             detail.mid_level = 0.50
00598:             detail.texture = detail_tex
00599:             try:
00600:                 detail.direction = 'NORMAL'
00601:                 detail.texture_coords = 'OBJECT'
00602:                 detail.texture_coords_object = controller
00603:             except Exception:
00604:                 pass
00605: 
00606:             deformers[-1]["detail_modifier"] = detail
00607:             deformers[-1]["detail_texture"] = detail_tex
00608:         except Exception:
00609:             pass
00610: 
00611:         try:
00612:             wave = obj.modifiers.new("HeroAudioSurfaceWave", 'WAVE')
00613:             wave.height = 0.0
00614:             wave.width = 1.20
00615:             wave.narrowness = 1.75
00616:             wave.speed = 0.16
00617:             try:
00618:                 wave.type = 'RINGS'
00619:                 wave.use_x = True
00620:                 wave.use_y = True
00621:                 wave.use_normal = True
00622:                 wave.start_position_object = controller
00623:             except Exception:
00624:                 pass
00625: 
00626:             deformers[-1]["wave_modifier"] = wave
00627:         except Exception:
00628:             pass
00629: 
00630:         try:
00631:             twist = obj.modifiers.new("HeroAudioTwistDeform", 'SIMPLE_DEFORM')
00632:             twist.deform_method = 'TWIST'
00633:             twist.angle = 0.0
00634:             try:
00635:                 twist.deform_axis = 'Z'
00636:             except Exception:
00637:                 pass
00638:             try:
00639:                 twist.origin = controller
00640:             except Exception:
00641:                 pass
00642: 
00643:             deformers[-1]["twist_modifier"] = twist
00644:         except Exception:
00645:             pass
00646: 
00647:     return {
00648:         "controller": controller,
00649:         "deformers": deformers,
00650:     }
00651: 
00652: 
00653: def _create_asset_from_dir(asset_dir, target_size, base_z, root_name, parent=None):
00654:     asset_file = find_asset_file(asset_dir)
00655:     imported_objects = import_asset_file(asset_file)
00656: 
00657:     asset_root = make_asset_root(root_name)
00658:     parent_objects_keep_transform(imported_objects, asset_root)
00659:     center_and_scale_asset(asset_root, imported_objects, target_size, base_z)
00660: 
00661:     if parent is not None:
00662:         mw = asset_root.matrix_world.copy()
00663:         asset_root.parent = parent
00664:         asset_root.matrix_world = mw
00665: 
00666:     meshes = collect_meshes(imported_objects)
00667:     soften_materials_to_peace(meshes)
00668:     material_controls = add_hero_material_audio_nodes(meshes) if root_name == "HeroRoot" else []
00669:     deform_data = add_hero_mesh_deformers(asset_root, meshes) if root_name == "HeroRoot" else {
00670:         "controller": None,
00671:         "deformers": [],
00672:     }
00673: 
00674:     return {
00675:         "asset_file": asset_file,
00676:         "root": asset_root,
00677:         "objects": imported_objects,
00678:         "meshes": meshes,
00679:         "deform_controller": deform_data["controller"],
00680:         "deformers": deform_data["deformers"],
00681:         "material_controls": material_controls,
00682:         "base_scale": asset_root.scale.copy(),
00683:         "base_location": asset_root.location.copy(),
00684:         "base_rotation": asset_root.rotation_euler.copy(),
00685:     }
00686: 
00687: 
00688: def create_primary_asset(parent=None):
00689:     return _create_asset_from_dir(
00690:         asset_dir=PRIMARY_ASSET_DIR,
00691:         target_size=PRIMARY_TARGET_SIZE,
00692:         base_z=PRIMARY_BASE_Z,
00693:         root_name="HeroRoot",
00694:         parent=parent,
00695:     )
00696: 
00697: 
00698: def create_secondary_asset(parent=None):
00699:     if not USE_SECONDARY_ASSET:
00700:         return None
00701: 
00702:     if not SECONDARY_ASSET_DIR.exists():
00703:         print(f"[WARN] Secondary asset dir non trovata: {SECONDARY_ASSET_DIR}")
00704:         return None
00705: 
00706:     asset = _create_asset_from_dir(
00707:         asset_dir=SECONDARY_ASSET_DIR,
00708:         target_size=SECONDARY_TARGET_SIZE,
00709:         base_z=SECONDARY_BASE_Z,
00710:         root_name="SecondaryRoot",
00711:         parent=parent,
00712:     )
00713: 
00714:     root = asset["root"]
00715:     root.location.x += SECONDARY_BASE_OFFSET_X
00716:     root.location.y += SECONDARY_BASE_OFFSET_Y
00717:     root.location.z += SECONDARY_BASE_OFFSET_Z
00718: 
00719:     bpy.context.view_layer.update()
00720: 
00721:     asset["base_scale"] = root.scale.copy()
00722:     asset["base_location"] = root.location.copy()
00723:     asset["base_rotation"] = root.rotation_euler.copy()
00724: 
00725:     return asset
```
