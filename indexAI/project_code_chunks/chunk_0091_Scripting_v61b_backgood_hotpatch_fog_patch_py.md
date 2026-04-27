# Project Code Chunk 91/212

- File: `Scripting/v61b_backgood/hotpatch/fog_patch.py`
- Part: `1`
- Lines: `1-124`

## Symbol Map
- Imports: `bpy`, `from mathutils import Vector`, `from fog_dynamics import animate_fog_frame`, `from materials import build_atmosphere_volume_material`, `from common import cfg_value, clear_animation, store_base_vector`
- Functions: `find_or_create_fog_controller(cube)` line 10; `ensure_fog_cube()` line 24; `update_fog(frames)` line 46

## Content
```py
00001: import bpy
00002: from mathutils import Vector
00003: 
00004: from fog_dynamics import animate_fog_frame
00005: from materials import build_atmosphere_volume_material
00006: 
00007: from .common import cfg_value, clear_animation, store_base_vector
00008: 
00009: 
00010: def find_or_create_fog_controller(cube):
00011:     controller = bpy.data.objects.get("FogPulseController")
00012:     if controller is not None:
00013:         return controller
00014: 
00015:     bpy.ops.object.empty_add(type='PLAIN_AXES', location=cube.location.copy())
00016:     controller = bpy.context.active_object
00017:     controller.name = "FogPulseController"
00018:     controller.empty_display_size = 0.42
00019:     controller.hide_render = True
00020:     controller.hide_viewport = True
00021:     return controller
00022: 
00023: 
00024: def ensure_fog_cube():
00025:     cube = bpy.data.objects.get("AtmosphereCube")
00026:     if cube is None:
00027:         bpy.ops.mesh.primitive_cube_add(location=(0, 0, 3.0))
00028:         cube = bpy.context.active_object
00029:         cube.name = "AtmosphereCube"
00030:         size = cfg_value("ATMOSPHERE_CUBE_SIZE", 18.0) * 0.5
00031:         cube.scale = (size, size, size)
00032: 
00033:     cube["spaziotempo_volume_container"] = True
00034:     cube.hide_render = False
00035:     cube.hide_viewport = False
00036:     cube.display_type = 'WIRE'
00037: 
00038:     material, controls = build_atmosphere_volume_material()
00039:     cube.data.materials.clear()
00040:     cube.data.materials.append(material)
00041: 
00042:     controller = find_or_create_fog_controller(cube)
00043:     return cube, controller, material, controls
00044: 
00045: 
00046: def update_fog(frames):
00047:     cube, controller, material, controls = ensure_fog_cube()
00048:     clear_animation(cube)
00049:     clear_animation(controller)
00050:     clear_animation(material.node_tree)
00051: 
00052:     base_scale_raw = store_base_vector(cube, "_hot_base_scale", cube.scale)
00053:     base_loc_raw = store_base_vector(cube, "_hot_base_location", cube.location)
00054:     base_scale = Vector(base_scale_raw)
00055:     base_loc = Vector(base_loc_raw)
00056: 
00057:     fog_controller = {
00058:         "object": cube,
00059:         "material": material,
00060:         "controller": controller,
00061:         "base_location": base_loc,
00062:         "base_scale": base_scale,
00063:         "density_socket": controls.get("density_socket"),
00064:         "emission_socket": controls.get("emission_socket"),
00065:         "noise_scale_socket": controls.get("noise_scale_socket"),
00066:         "noise_detail_socket": controls.get("noise_detail_socket"),
00067:         "noise_roughness_socket": controls.get("noise_roughness_socket"),
00068:         "clump_noise_scale_socket": controls.get("clump_noise_scale_socket"),
00069:         "clump_noise_detail_socket": controls.get("clump_noise_detail_socket"),
00070:         "clump_noise_roughness_socket": controls.get("clump_noise_roughness_socket"),
00071:         "mapping_location_socket": controls.get("mapping_location_socket"),
00072:         "mapping_scale_socket": controls.get("mapping_scale_socket"),
00073:         "mapping_rotation_socket": controls.get("mapping_rotation_socket"),
00074:         "wave_scale_socket": controls.get("wave_scale_socket"),
00075:         "wave_distortion_socket": controls.get("wave_distortion_socket"),
00076:         "wave_phase_socket": controls.get("wave_phase_socket"),
00077:         "wave_weight_socket": controls.get("wave_weight_socket"),
00078:         "ramp_low_ctrl": controls.get("ramp_low_ctrl"),
00079:         "ramp_high_ctrl": controls.get("ramp_high_ctrl"),
00080:         "clump_ramp_low_ctrl": controls.get("clump_ramp_low_ctrl"),
00081:         "clump_ramp_high_ctrl": controls.get("clump_ramp_high_ctrl"),
00082:         "volume_color_socket": controls.get("volume_color_socket"),
00083:         "volume_anisotropy_socket": controls.get("volume_anisotropy_socket"),
00084:     }
00085: 
00086:     if not frames:
00087:         animate_fog_frame(
00088:             frame=1,
00089:             low=0.4,
00090:             mid=0.2,
00091:             high=0.2,
00092:             onset=0.0,
00093:             beat=0.0,
00094:             pulse=0.0,
00095:             fog_controller=fog_controller,
00096:             fog_obj=cube,
00097:             fog_control=controller,
00098:             fog_base_scale=base_scale,
00099:             fog_base_loc=base_loc,
00100:         )
00101:         return 1
00102: 
00103:     for frame, sample in enumerate(frames, start=1):
00104:         low = float(sample.get("low", 0.0))
00105:         mid = float(sample.get("mid", 0.0))
00106:         high = float(sample.get("high", 0.0))
00107:         onset = float(sample.get("onset", 0.0))
00108:         beat = float(sample.get("beat", 0.0))
00109:         animate_fog_frame(
00110:             frame=frame,
00111:             low=low,
00112:             mid=mid,
00113:             high=high,
00114:             onset=onset,
00115:             beat=beat,
00116:             pulse=max(onset, beat),
00117:             fog_controller=fog_controller,
00118:             fog_obj=cube,
00119:             fog_control=controller,
00120:             fog_base_scale=base_scale,
00121:             fog_base_loc=base_loc,
00122:         )
00123: 
00124:     return len(frames)
```
