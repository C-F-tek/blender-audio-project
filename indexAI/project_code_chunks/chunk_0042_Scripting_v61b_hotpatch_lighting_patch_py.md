# Project Code Chunk 42/212

- File: `Scripting/v61b/hotpatch/lighting_patch.py`
- Part: `1`
- Lines: `1-150`

## Symbol Map
- Imports: `bpy`, `from common import cfg_value, clear_animation, get_node, keyframe_if_possible, remove_objects_with_prefixes, socket_by_name`
- Functions: `resize_plane_local(obj, target_size)` line 28; `update_world(scene)` line 44; `remove_legacy_rhythm_objects()` line 84; `update_area_lights(frames)` line 88; `update_backdrop()` line 114
- Assignments: `LIGHT_ENERGY_MIN`, `LIGHT_ENERGY_MAX`, `WORLD_STRENGTH`, `WORLD_CAMERA_STRENGTH`, `WORLD_LIGHT_COLOR`, `WORLD_CAMERA_COLOR`, `BACKDROP_EMISSION_MIN`, `BACKDROP_EMISSION_MAX`, `BACKDROP_SIZE`, `BACKDROP_LOCATION`, `BACKDROP_ROT_X`, `FLOOR_RENDER_VISIBLE`, `FLOOR_VIEWPORT_VISIBLE`

## Content
```py
00001: import bpy
00002: 
00003: from .common import (
00004:     cfg_value,
00005:     clear_animation,
00006:     get_node,
00007:     keyframe_if_possible,
00008:     remove_objects_with_prefixes,
00009:     socket_by_name,
00010: )
00011: 
00012: 
00013: LIGHT_ENERGY_MIN = cfg_value("LIGHT_ENERGY_MIN", 105.0)
00014: LIGHT_ENERGY_MAX = cfg_value("LIGHT_ENERGY_MAX", 128.0)
00015: WORLD_STRENGTH = cfg_value("WORLD_STRENGTH", 0.115)
00016: WORLD_CAMERA_STRENGTH = cfg_value("WORLD_CAMERA_STRENGTH", 0.52)
00017: WORLD_LIGHT_COLOR = cfg_value("WORLD_LIGHT_COLOR", (0.012, 0.052, 0.058, 1.0))
00018: WORLD_CAMERA_COLOR = cfg_value("WORLD_CAMERA_COLOR", (0.045, 0.170, 0.185, 1.0))
00019: BACKDROP_EMISSION_MIN = cfg_value("BACKDROP_EMISSION_MIN", 0.025)
00020: BACKDROP_EMISSION_MAX = cfg_value("BACKDROP_EMISSION_MAX", 0.027)
00021: BACKDROP_SIZE = cfg_value("BACKDROP_SIZE", 92.0)
00022: BACKDROP_LOCATION = cfg_value("BACKDROP_LOCATION", (0.0, 12.0, 5.2))
00023: BACKDROP_ROT_X = cfg_value("BACKDROP_ROT_X", 1.57079632679)
00024: FLOOR_RENDER_VISIBLE = cfg_value("FLOOR_RENDER_VISIBLE", False)
00025: FLOOR_VIEWPORT_VISIBLE = cfg_value("FLOOR_VIEWPORT_VISIBLE", True)
00026: 
00027: 
00028: def resize_plane_local(obj, target_size):
00029:     mesh = getattr(obj, "data", None)
00030:     vertices = getattr(mesh, "vertices", None)
00031:     if not vertices:
00032:         return
00033: 
00034:     xs = [v.co.x for v in vertices]
00035:     ys = [v.co.y for v in vertices]
00036:     width = max(xs) - min(xs)
00037:     height = max(ys) - min(ys)
00038:     if width > 0.0001:
00039:         obj.scale.x = float(target_size) / width
00040:     if height > 0.0001:
00041:         obj.scale.y = float(target_size) / height
00042: 
00043: 
00044: def update_world(scene):
00045:     world = scene.world
00046:     if world is None:
00047:         world = bpy.data.worlds.new("PeaceWorld")
00048:         scene.world = world
00049: 
00050:     world.use_nodes = True
00051:     nodes = world.node_tree.nodes
00052:     links = world.node_tree.links
00053: 
00054:     for node in list(nodes):
00055:         nodes.remove(node)
00056: 
00057:     out = nodes.new("ShaderNodeOutputWorld")
00058:     out.location = (520, 0)
00059: 
00060:     bg_camera = nodes.new("ShaderNodeBackground")
00061:     bg_camera.name = "WorldCameraAzzurro"
00062:     bg_camera.location = (-260, 80)
00063:     bg_camera.inputs["Strength"].default_value = WORLD_CAMERA_STRENGTH
00064:     bg_camera.inputs["Color"].default_value = WORLD_CAMERA_COLOR
00065: 
00066:     bg_light = nodes.new("ShaderNodeBackground")
00067:     bg_light.name = "WorldSceneLight"
00068:     bg_light.location = (-260, -130)
00069:     bg_light.inputs["Strength"].default_value = WORLD_STRENGTH
00070:     bg_light.inputs["Color"].default_value = WORLD_LIGHT_COLOR
00071: 
00072:     light_path = nodes.new("ShaderNodeLightPath")
00073:     light_path.location = (-560, -70)
00074: 
00075:     mix = nodes.new("ShaderNodeMixShader")
00076:     mix.location = (120, 0)
00077: 
00078:     links.new(light_path.outputs["Is Camera Ray"], mix.inputs[0])
00079:     links.new(bg_light.outputs["Background"], mix.inputs[1])
00080:     links.new(bg_camera.outputs["Background"], mix.inputs[2])
00081:     links.new(mix.outputs["Shader"], out.inputs["Surface"])
00082: 
00083: 
00084: def remove_legacy_rhythm_objects():
00085:     return remove_objects_with_prefixes(["RhythmPulseLight", "RhythmEmitterOrb"])
00086: 
00087: 
00088: def update_area_lights(frames):
00089:     lights = [obj for obj in bpy.data.objects if obj.type == 'LIGHT' and obj.name.startswith("AreaLight_")]
00090:     for light in lights:
00091:         clear_animation(light.data)
00092: 
00093:     if not frames:
00094:         for light in lights:
00095:             light.data.energy = LIGHT_ENERGY_MIN
00096:         return len(lights)
00097: 
00098:     for frame, sample in enumerate(frames, start=1):
00099:         high = float(sample.get("high", 0.0))
00100:         mid = float(sample.get("mid", 0.0))
00101:         low = float(sample.get("low", 0.0))
00102:         onset = float(sample.get("onset", 0.0))
00103:         beat = float(sample.get("beat", 0.0))
00104:         pulse = max(onset, beat)
00105:         drive = min(1.0, high * 0.006 + mid * 0.006 + low * 0.005 + pulse * 0.004)
00106:         energy = LIGHT_ENERGY_MIN + drive * (LIGHT_ENERGY_MAX - LIGHT_ENERGY_MIN)
00107:         for light in lights:
00108:             light.data.energy = energy
00109:             keyframe_if_possible(light.data, "energy", frame)
00110: 
00111:     return len(lights)
00112: 
00113: 
00114: def update_backdrop():
00115:     backdrop = bpy.data.objects.get("SoftRhythmBackdrop")
00116:     material = bpy.data.materials.get("SoftBackdropMaterial")
00117:     floor = bpy.data.objects.get("PeaceFloor")
00118: 
00119:     if floor is not None:
00120:         floor.hide_render = not bool(FLOOR_RENDER_VISIBLE)
00121:         floor.hide_viewport = not bool(FLOOR_VIEWPORT_VISIBLE)
00122: 
00123:     if material is not None and material.use_nodes:
00124:         clear_animation(material.node_tree)
00125:         emission = get_node(material, "BackdropEmission")
00126:         socket = socket_by_name(emission, "Strength")
00127:         if socket is not None:
00128:             socket.default_value = BACKDROP_EMISSION_MIN + (BACKDROP_EMISSION_MAX - BACKDROP_EMISSION_MIN) * 0.18
00129: 
00130:         for node in material.node_tree.nodes:
00131:             if node.type == "TEX_NOISE" and "Scale" in node.inputs:
00132:                 node.inputs["Scale"].default_value = 1.18
00133:             if node.type == "VALTORGB":
00134:                 try:
00135:                     node.color_ramp.elements[0].position = 0.14
00136:                     node.color_ramp.elements[0].color = (0.012, 0.055, 0.064, 1.0)
00137:                     node.color_ramp.elements[1].position = 1.00
00138:                     node.color_ramp.elements[1].color = (0.085, 0.245, 0.255, 1.0)
00139:                 except Exception:
00140:                     pass
00141: 
00142:     if backdrop is not None:
00143:         clear_animation(backdrop)
00144:         backdrop.hide_render = False
00145:         backdrop.hide_viewport = False
00146:         backdrop.location = BACKDROP_LOCATION
00147:         backdrop.rotation_euler = (BACKDROP_ROT_X, 0.0, 0.0)
00148:         resize_plane_local(backdrop, BACKDROP_SIZE)
00149: 
00150:     return backdrop is not None
```
