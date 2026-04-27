# Project Code Chunk 89/212

- File: `Scripting/v61b_backgood/hotpatch/accent_patch.py`
- Part: `1`
- Lines: `1-125`

## Symbol Map
- Imports: `math`, `from materials import build_variant_material`, `from common import PALETTE_LIST, cfg_value, clear_animation, get_node, iter_objects_prefix, keyframe_if_possible, socket_by_name, store_base_vector`
- Functions: `drive_for_band(band, response, sample, frame, phase)` line 23; `ensure_accent_material(obj, index)` line 46; `update_physics_accents(frames)` line 67
- Assignments: `PHYSICS_ACCENT_EMISSION_MIN`, `PHYSICS_ACCENT_EMISSION_MAX`, `PHYSICS_ACCENT_MIX_MIN`, `PHYSICS_ACCENT_MIX_MAX`

## Content
```py
00001: import math
00002: 
00003: from materials import build_variant_material
00004: 
00005: from .common import (
00006:     PALETTE_LIST,
00007:     cfg_value,
00008:     clear_animation,
00009:     get_node,
00010:     iter_objects_prefix,
00011:     keyframe_if_possible,
00012:     socket_by_name,
00013:     store_base_vector,
00014: )
00015: 
00016: 
00017: PHYSICS_ACCENT_EMISSION_MIN = cfg_value("PHYSICS_ACCENT_EMISSION_MIN", 0.06)
00018: PHYSICS_ACCENT_EMISSION_MAX = cfg_value("PHYSICS_ACCENT_EMISSION_MAX", 0.72)
00019: PHYSICS_ACCENT_MIX_MIN = cfg_value("PHYSICS_ACCENT_MIX_MIN", 0.12)
00020: PHYSICS_ACCENT_MIX_MAX = cfg_value("PHYSICS_ACCENT_MIX_MAX", 0.42)
00021: 
00022: 
00023: def drive_for_band(band, response, sample, frame, phase):
00024:     low = float(sample.get("low", 0.0))
00025:     mid = float(sample.get("mid", 0.0))
00026:     high = float(sample.get("high", 0.0))
00027:     onset = float(sample.get("onset", 0.0))
00028:     beat = float(sample.get("beat", 0.0))
00029:     pulse = max(onset, beat)
00030:     local_pulse = max(0.0, math.sin(frame * (0.024 + response * 0.016) + phase)) * 0.20
00031: 
00032:     if band == "low":
00033:         drive = low * 0.74 + beat * 0.18 + local_pulse * 0.16
00034:     elif band == "mid":
00035:         drive = mid * 0.68 + low * 0.14 + local_pulse * 0.18
00036:     elif band == "beat":
00037:         drive = beat * 0.70 + low * 0.22 + local_pulse * 0.14
00038:     elif band == "onset":
00039:         drive = onset * 0.72 + high * 0.18 + local_pulse * 0.12
00040:     else:
00041:         drive = high * 0.68 + onset * 0.24 + pulse * 0.08 + local_pulse * 0.12
00042: 
00043:     return max(0.0, min(1.0, drive * response))
00044: 
00045: 
00046: def ensure_accent_material(obj, index):
00047:     mat = obj.active_material
00048:     if mat is None or not mat.use_nodes or get_node(mat, "VariantEmission") is None:
00049:         color = PALETTE_LIST[index % len(PALETTE_LIST)]
00050:         mat = build_variant_material(f"PhysicsAccentMat_hot_{index:02d}", color)
00051:         obj.data.materials.clear()
00052:         obj.data.materials.append(mat)
00053: 
00054:     emission = get_node(mat, "VariantEmission")
00055:     mix = get_node(mat, "VariantEmissionMix")
00056:     emit_socket = socket_by_name(emission, "Strength")
00057:     mix_socket = socket_by_name(mix, 0, is_output=True)
00058: 
00059:     if emit_socket is not None:
00060:         emit_socket.default_value = PHYSICS_ACCENT_EMISSION_MIN
00061:     if mix_socket is not None:
00062:         mix_socket.default_value = PHYSICS_ACCENT_MIX_MIN
00063: 
00064:     return mat, emit_socket, mix_socket
00065: 
00066: 
00067: def update_physics_accents(frames):
00068:     accents = sorted(iter_objects_prefix("PhysicsAccent_"), key=lambda obj: obj.name)
00069:     bands = ["low", "mid", "high", "beat", "onset"]
00070: 
00071:     controls = []
00072:     for idx, obj in enumerate(accents):
00073:         mat, emit_socket, mix_socket = ensure_accent_material(obj, idx)
00074:         clear_animation(obj)
00075:         if mat is not None and mat.use_nodes:
00076:             clear_animation(mat.node_tree)
00077: 
00078:         obj["hot_band"] = bands[idx % len(bands)]
00079:         obj["hot_response"] = float(obj.get("hot_response", 0.42 + (idx % 7) * 0.075))
00080:         obj["hot_phase"] = float(obj.get("hot_phase", idx * 0.61))
00081:         store_base_vector(obj, "_hot_base_rotation", obj.rotation_euler)
00082: 
00083:         controls.append({
00084:             "object": obj,
00085:             "material": mat,
00086:             "emission_socket": emit_socket,
00087:             "mix_socket": mix_socket,
00088:             "band": obj["hot_band"],
00089:             "response": obj["hot_response"],
00090:             "phase": obj["hot_phase"],
00091:             "base_rotation": obj["_hot_base_rotation"],
00092:         })
00093: 
00094:     if not controls:
00095:         return 0
00096: 
00097:     if not frames:
00098:         frames = [{"low": 0.3, "mid": 0.2, "high": 0.2, "onset": 0.0, "beat": 0.0}]
00099: 
00100:     for frame, sample in enumerate(frames, start=1):
00101:         for item in controls:
00102:             obj = item["object"]
00103:             response = item["response"]
00104:             phase = item["phase"]
00105:             drive = drive_for_band(item["band"], response, sample, frame, phase)
00106: 
00107:             rot = item["base_rotation"]
00108:             obj.rotation_euler.x = rot[0] + math.sin(frame * 0.017 + phase) * 0.10 * (0.35 + drive)
00109:             obj.rotation_euler.y = rot[1] + math.cos(frame * 0.015 + phase) * 0.08 * (0.35 + drive)
00110:             obj.rotation_euler.z = rot[2] + frame * (0.006 + drive * 0.006) + math.sin(frame * 0.011 + phase) * 0.04
00111:             obj.keyframe_insert(data_path="rotation_euler", frame=frame)
00112: 
00113:             if item["emission_socket"] is not None:
00114:                 item["emission_socket"].default_value = PHYSICS_ACCENT_EMISSION_MIN + drive * (
00115:                     PHYSICS_ACCENT_EMISSION_MAX - PHYSICS_ACCENT_EMISSION_MIN
00116:                 )
00117:                 keyframe_if_possible(item["emission_socket"], "default_value", frame)
00118: 
00119:             if item["mix_socket"] is not None:
00120:                 item["mix_socket"].default_value = PHYSICS_ACCENT_MIX_MIN + drive * (
00121:                     PHYSICS_ACCENT_MIX_MAX - PHYSICS_ACCENT_MIX_MIN
00122:                 )
00123:                 keyframe_if_possible(item["mix_socket"], "default_value", frame)
00124: 
00125:     return len(controls)
```
