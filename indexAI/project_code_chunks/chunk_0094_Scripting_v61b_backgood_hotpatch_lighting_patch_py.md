# Project Code Chunk 94/212

- File: `Scripting/v61b_backgood/hotpatch/lighting_patch.py`
- Part: `1`
- Lines: `1-85`

## Symbol Map
- Imports: `bpy`, `from common import cfg_value, clear_animation, get_node, keyframe_if_possible, remove_objects_with_prefixes, socket_by_name`
- Functions: `update_world(scene)` line 20; `remove_legacy_rhythm_objects()` line 35; `update_area_lights(frames)` line 39; `update_backdrop()` line 65
- Assignments: `LIGHT_ENERGY_MIN`, `LIGHT_ENERGY_MAX`, `WORLD_STRENGTH`, `BACKDROP_EMISSION_MIN`, `BACKDROP_EMISSION_MAX`

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
00016: BACKDROP_EMISSION_MIN = cfg_value("BACKDROP_EMISSION_MIN", 0.025)
00017: BACKDROP_EMISSION_MAX = cfg_value("BACKDROP_EMISSION_MAX", 0.027)
00018: 
00019: 
00020: def update_world(scene):
00021:     world = scene.world
00022:     if world is None:
00023:         world = bpy.data.worlds.new("PeaceWorld")
00024:         scene.world = world
00025: 
00026:     world.use_nodes = True
00027:     nodes = world.node_tree.nodes
00028:     bg = nodes.get("Background")
00029:     if bg is None:
00030:         bg = nodes.new("ShaderNodeBackground")
00031:     if "Strength" in bg.inputs:
00032:         bg.inputs["Strength"].default_value = WORLD_STRENGTH
00033: 
00034: 
00035: def remove_legacy_rhythm_objects():
00036:     return remove_objects_with_prefixes(["RhythmPulseLight", "RhythmEmitterOrb"])
00037: 
00038: 
00039: def update_area_lights(frames):
00040:     lights = [obj for obj in bpy.data.objects if obj.type == 'LIGHT' and obj.name.startswith("AreaLight_")]
00041:     for light in lights:
00042:         clear_animation(light.data)
00043: 
00044:     if not frames:
00045:         for light in lights:
00046:             light.data.energy = LIGHT_ENERGY_MIN
00047:         return len(lights)
00048: 
00049:     for frame, sample in enumerate(frames, start=1):
00050:         high = float(sample.get("high", 0.0))
00051:         mid = float(sample.get("mid", 0.0))
00052:         low = float(sample.get("low", 0.0))
00053:         onset = float(sample.get("onset", 0.0))
00054:         beat = float(sample.get("beat", 0.0))
00055:         pulse = max(onset, beat)
00056:         drive = min(1.0, high * 0.006 + mid * 0.006 + low * 0.005 + pulse * 0.004)
00057:         energy = LIGHT_ENERGY_MIN + drive * (LIGHT_ENERGY_MAX - LIGHT_ENERGY_MIN)
00058:         for light in lights:
00059:             light.data.energy = energy
00060:             keyframe_if_possible(light.data, "energy", frame)
00061: 
00062:     return len(lights)
00063: 
00064: 
00065: def update_backdrop():
00066:     backdrop = bpy.data.objects.get("SoftRhythmBackdrop")
00067:     material = bpy.data.materials.get("SoftBackdropMaterial")
00068: 
00069:     if material is not None and material.use_nodes:
00070:         clear_animation(material.node_tree)
00071:         emission = get_node(material, "BackdropEmission")
00072:         socket = socket_by_name(emission, "Strength")
00073:         if socket is not None:
00074:             socket.default_value = BACKDROP_EMISSION_MIN + (BACKDROP_EMISSION_MAX - BACKDROP_EMISSION_MIN) * 0.06
00075: 
00076:         for node in material.node_tree.nodes:
00077:             if node.type == "TEX_NOISE" and "Scale" in node.inputs:
00078:                 node.inputs["Scale"].default_value = 2.18
00079: 
00080:     if backdrop is not None:
00081:         clear_animation(backdrop)
00082:         backdrop.hide_render = False
00083:         backdrop.hide_viewport = False
00084: 
00085:     return backdrop is not None
```
