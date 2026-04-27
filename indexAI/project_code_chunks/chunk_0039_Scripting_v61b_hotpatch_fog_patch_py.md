# Project Code Chunk 39/212

- File: `Scripting/v61b/hotpatch/fog_patch.py`
- Part: `1`
- Lines: `1-133`

## Symbol Map
- Imports: `bpy`, `from mathutils import Vector`, `from fog_dynamics import animate_fog_frame`, `from fog_filaments import ensure_fog_filaments`, `from materials import build_atmosphere_volume_material`, `from common import cfg_value, clear_animation, store_base_vector`
- Functions: `find_or_create_fog_controller(cube)` line 11; `ensure_fog_cube()` line 25; `update_fog(frames)` line 47

## Content
```py
00001: import bpy
00002: from mathutils import Vector
00003: 
00004: from fog_dynamics import animate_fog_frame
00005: from fog_filaments import ensure_fog_filaments
00006: from materials import build_atmosphere_volume_material
00007: 
00008: from .common import cfg_value, clear_animation, store_base_vector
00009: 
00010: 
00011: def find_or_create_fog_controller(cube):
00012:     controller = bpy.data.objects.get("FogPulseController")
00013:     if controller is not None:
00014:         return controller
00015: 
00016:     bpy.ops.object.empty_add(type='PLAIN_AXES', location=cube.location.copy())
00017:     controller = bpy.context.active_object
00018:     controller.name = "FogPulseController"
00019:     controller.empty_display_size = 0.42
00020:     controller.hide_render = True
00021:     controller.hide_viewport = True
00022:     return controller
00023: 
00024: 
00025: def ensure_fog_cube():
00026:     cube = bpy.data.objects.get("AtmosphereCube")
00027:     if cube is None:
00028:         bpy.ops.mesh.primitive_cube_add(location=(0, 0, 3.0))
00029:         cube = bpy.context.active_object
00030:         cube.name = "AtmosphereCube"
00031:         size = cfg_value("ATMOSPHERE_CUBE_SIZE", 18.0) * 0.5
00032:         cube.scale = (size, size, size)
00033: 
00034:     cube["spaziotempo_volume_container"] = True
00035:     cube.hide_render = not bool(cfg_value("FOG_VOLUME_ENABLED", False))
00036:     cube.hide_viewport = not bool(cfg_value("FOG_VOLUME_VIEWPORT_VISIBLE", False))
00037:     cube.display_type = 'WIRE'
00038: 
00039:     material, controls = build_atmosphere_volume_material()
00040:     cube.data.materials.clear()
00041:     cube.data.materials.append(material)
00042: 
00043:     controller = find_or_create_fog_controller(cube)
00044:     return cube, controller, material, controls
00045: 
00046: 
00047: def update_fog(frames):
00048:     cube, controller, material, controls = ensure_fog_cube()
00049:     filaments = ensure_fog_filaments()
00050:     clear_animation(cube)
00051:     clear_animation(controller)
00052:     clear_animation(material.node_tree)
00053:     if filaments.get("root") is not None:
00054:         clear_animation(filaments["root"])
00055:     if filaments.get("material") is not None and filaments["material"].use_nodes:
00056:         clear_animation(filaments["material"].node_tree)
00057:     for item in filaments.get("objects", []):
00058:         clear_animation(item["object"])
00059: 
00060:     base_scale_raw = store_base_vector(cube, "_hot_base_scale", cube.scale)
00061:     base_loc_raw = store_base_vector(cube, "_hot_base_location", cube.location)
00062:     base_scale = Vector(base_scale_raw)
00063:     base_loc = Vector(base_loc_raw)
00064: 
00065:     fog_controller = {
00066:         "object": cube,
00067:         "material": material,
00068:         "controller": controller,
00069:         "filaments": filaments,
00070:         "base_location": base_loc,
00071:         "base_scale": base_scale,
00072:         "density_socket": controls.get("density_socket"),
00073:         "emission_socket": controls.get("emission_socket"),
00074:         "noise_scale_socket": controls.get("noise_scale_socket"),
00075:         "noise_detail_socket": controls.get("noise_detail_socket"),
00076:         "noise_roughness_socket": controls.get("noise_roughness_socket"),
00077:         "clump_noise_scale_socket": controls.get("clump_noise_scale_socket"),
00078:         "clump_noise_detail_socket": controls.get("clump_noise_detail_socket"),
00079:         "clump_noise_roughness_socket": controls.get("clump_noise_roughness_socket"),
00080:         "mapping_location_socket": controls.get("mapping_location_socket"),
00081:         "mapping_scale_socket": controls.get("mapping_scale_socket"),
00082:         "mapping_rotation_socket": controls.get("mapping_rotation_socket"),
00083:         "wave_scale_socket": controls.get("wave_scale_socket"),
00084:         "wave_distortion_socket": controls.get("wave_distortion_socket"),
00085:         "wave_phase_socket": controls.get("wave_phase_socket"),
00086:         "wave_weight_socket": controls.get("wave_weight_socket"),
00087:         "ramp_low_ctrl": controls.get("ramp_low_ctrl"),
00088:         "ramp_high_ctrl": controls.get("ramp_high_ctrl"),
00089:         "clump_ramp_low_ctrl": controls.get("clump_ramp_low_ctrl"),
00090:         "clump_ramp_high_ctrl": controls.get("clump_ramp_high_ctrl"),
00091:         "volume_color_socket": controls.get("volume_color_socket"),
00092:         "volume_anisotropy_socket": controls.get("volume_anisotropy_socket"),
00093:     }
00094: 
00095:     if not frames:
00096:         animate_fog_frame(
00097:             frame=1,
00098:             low=0.4,
00099:             mid=0.2,
00100:             high=0.2,
00101:             onset=0.0,
00102:             beat=0.0,
00103:             pulse=0.0,
00104:             fog_controller=fog_controller,
00105:             fog_obj=cube,
00106:             fog_control=controller,
00107:             fog_base_scale=base_scale,
00108:             fog_base_loc=base_loc,
00109:         )
00110:         return 1
00111: 
00112:     for frame, sample in enumerate(frames, start=1):
00113:         low = float(sample.get("low", 0.0))
00114:         mid = float(sample.get("mid", 0.0))
00115:         high = float(sample.get("high", 0.0))
00116:         onset = float(sample.get("onset", 0.0))
00117:         beat = float(sample.get("beat", 0.0))
00118:         animate_fog_frame(
00119:             frame=frame,
00120:             low=low,
00121:             mid=mid,
00122:             high=high,
00123:             onset=onset,
00124:             beat=beat,
00125:             pulse=max(onset, beat),
00126:             fog_controller=fog_controller,
00127:             fog_obj=cube,
00128:             fog_control=controller,
00129:             fog_base_scale=base_scale,
00130:             fog_base_loc=base_loc,
00131:         )
00132: 
00133:     return len(frames)
```
