import bpy
from fog_dynamics import animate_fog_frame
from fog_filaments import ensure_fog_filaments
from materials import build_atmosphere_volume_material
from mathutils import Vector

from .common import cfg_value, clear_animation, store_base_vector


def find_or_create_fog_controller(cube):
    controller = bpy.data.objects.get("FogPulseController")
    if controller is not None:
        return controller

    bpy.ops.object.empty_add(type="PLAIN_AXES", location=cube.location.copy())
    controller = bpy.context.active_object
    controller.name = "FogPulseController"
    controller.empty_display_size = 0.42
    controller.hide_render = True
    controller.hide_viewport = True
    return controller


def ensure_fog_cube():
    cube = bpy.data.objects.get("AtmosphereCube")
    if cube is None:
        bpy.ops.mesh.primitive_cube_add(location=(0, 0, 3.0))
        cube = bpy.context.active_object
        cube.name = "AtmosphereCube"
        size = cfg_value("ATMOSPHERE_CUBE_SIZE", 18.0) * 0.5
        cube.scale = (size, size, size)

    cube["spaziotempo_volume_container"] = True
    cube.hide_render = not bool(cfg_value("FOG_VOLUME_ENABLED", False))
    cube.hide_viewport = not bool(cfg_value("FOG_VOLUME_VIEWPORT_VISIBLE", False))
    cube.display_type = "WIRE"

    material, controls = build_atmosphere_volume_material()
    cube.data.materials.clear()
    cube.data.materials.append(material)

    controller = find_or_create_fog_controller(cube)
    return cube, controller, material, controls


def update_fog(frames):
    cube, controller, material, controls = ensure_fog_cube()
    filaments = ensure_fog_filaments()
    clear_animation(cube)
    clear_animation(controller)
    clear_animation(material.node_tree)
    if filaments.get("root") is not None:
        clear_animation(filaments["root"])
    if filaments.get("material") is not None and filaments["material"].use_nodes:
        clear_animation(filaments["material"].node_tree)
    for item in filaments.get("objects", []):
        clear_animation(item["object"])

    base_scale_raw = store_base_vector(cube, "_hot_base_scale", cube.scale)
    base_loc_raw = store_base_vector(cube, "_hot_base_location", cube.location)
    base_scale = Vector(base_scale_raw)
    base_loc = Vector(base_loc_raw)

    fog_controller = {
        "object": cube,
        "material": material,
        "controller": controller,
        "filaments": filaments,
        "base_location": base_loc,
        "base_scale": base_scale,
        "density_socket": controls.get("density_socket"),
        "emission_socket": controls.get("emission_socket"),
        "noise_scale_socket": controls.get("noise_scale_socket"),
        "noise_detail_socket": controls.get("noise_detail_socket"),
        "noise_roughness_socket": controls.get("noise_roughness_socket"),
        "clump_noise_scale_socket": controls.get("clump_noise_scale_socket"),
        "clump_noise_detail_socket": controls.get("clump_noise_detail_socket"),
        "clump_noise_roughness_socket": controls.get("clump_noise_roughness_socket"),
        "mapping_location_socket": controls.get("mapping_location_socket"),
        "mapping_scale_socket": controls.get("mapping_scale_socket"),
        "mapping_rotation_socket": controls.get("mapping_rotation_socket"),
        "wave_scale_socket": controls.get("wave_scale_socket"),
        "wave_distortion_socket": controls.get("wave_distortion_socket"),
        "wave_phase_socket": controls.get("wave_phase_socket"),
        "wave_weight_socket": controls.get("wave_weight_socket"),
        "ramp_low_ctrl": controls.get("ramp_low_ctrl"),
        "ramp_high_ctrl": controls.get("ramp_high_ctrl"),
        "clump_ramp_low_ctrl": controls.get("clump_ramp_low_ctrl"),
        "clump_ramp_high_ctrl": controls.get("clump_ramp_high_ctrl"),
        "volume_color_socket": controls.get("volume_color_socket"),
        "volume_anisotropy_socket": controls.get("volume_anisotropy_socket"),
    }

    if not frames:
        animate_fog_frame(
            frame=1,
            low=0.4,
            mid=0.2,
            high=0.2,
            onset=0.0,
            beat=0.0,
            pulse=0.0,
            fog_controller=fog_controller,
            fog_obj=cube,
            fog_control=controller,
            fog_base_scale=base_scale,
            fog_base_loc=base_loc,
        )
        return 1

    for frame, sample in enumerate(frames, start=1):
        low = float(sample.get("low", 0.0))
        mid = float(sample.get("mid", 0.0))
        high = float(sample.get("high", 0.0))
        onset = float(sample.get("onset", 0.0))
        beat = float(sample.get("beat", 0.0))
        animate_fog_frame(
            frame=frame,
            low=low,
            mid=mid,
            high=high,
            onset=onset,
            beat=beat,
            pulse=max(onset, beat),
            fog_controller=fog_controller,
            fog_obj=cube,
            fog_control=controller,
            fog_base_scale=base_scale,
            fog_base_loc=base_loc,
        )

    return len(frames)
