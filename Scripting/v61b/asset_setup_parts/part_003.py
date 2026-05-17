def _create_asset_from_dir(asset_dir, target_size, base_z, root_name, parent=None):
    asset_file = find_asset_file(asset_dir)
    imported_objects = import_asset_file(asset_file)

    asset_root = make_asset_root(root_name)
    parent_objects_keep_transform(imported_objects, asset_root)
    center_and_scale_asset(asset_root, imported_objects, target_size, base_z)

    if parent is not None:
        mw = asset_root.matrix_world.copy()
        asset_root.parent = parent
        asset_root.matrix_world = mw

    meshes = collect_meshes(imported_objects)
    soften_materials_to_peace(meshes)
    material_controls = add_hero_material_audio_nodes(meshes) if root_name == "HeroRoot" else []
    deform_data = (
        add_hero_mesh_deformers(asset_root, meshes)
        if root_name == "HeroRoot"
        else {
            "controller": None,
            "deformers": [],
        }
    )

    return {
        "asset_file": asset_file,
        "root": asset_root,
        "objects": imported_objects,
        "meshes": meshes,
        "deform_controller": deform_data["controller"],
        "deformers": deform_data["deformers"],
        "material_controls": material_controls,
        "base_scale": asset_root.scale.copy(),
        "base_location": asset_root.location.copy(),
        "base_rotation": asset_root.rotation_euler.copy(),
    }


def create_primary_asset(parent=None):
    return _create_asset_from_dir(
        asset_dir=PRIMARY_ASSET_DIR,
        target_size=PRIMARY_TARGET_SIZE,
        base_z=PRIMARY_BASE_Z,
        root_name="HeroRoot",
        parent=parent,
    )


def create_secondary_asset(parent=None):
    if not USE_SECONDARY_ASSET:
        return None

    if not SECONDARY_ASSET_DIR.exists():
        print(f"[WARN] Secondary asset dir non trovata: {SECONDARY_ASSET_DIR}")
        return None

    asset = _create_asset_from_dir(
        asset_dir=SECONDARY_ASSET_DIR,
        target_size=SECONDARY_TARGET_SIZE,
        base_z=SECONDARY_BASE_Z,
        root_name="SecondaryRoot",
        parent=parent,
    )

    root = asset["root"]
    root.location.x += SECONDARY_BASE_OFFSET_X
    root.location.y += SECONDARY_BASE_OFFSET_Y
    root.location.z += SECONDARY_BASE_OFFSET_Z

    bpy.context.view_layer.update()

    asset["base_scale"] = root.scale.copy()
    asset["base_location"] = root.location.copy()
    asset["base_rotation"] = root.rotation_euler.copy()

    return asset
