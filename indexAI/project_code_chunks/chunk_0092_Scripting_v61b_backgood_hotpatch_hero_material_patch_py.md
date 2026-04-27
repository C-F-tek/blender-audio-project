# Project Code Chunk 92/212

- File: `Scripting/v61b_backgood/hotpatch/hero_material_patch.py`
- Part: `1`
- Lines: `1-291`

## Symbol Map
- Imports: `math`, `bpy`, `from common import cfg_value, clear_animation, keyframe_if_possible`
- Functions: `find_principled_node(material)` line 28; `get_node_input(node)` line 37; `link_node_sockets(links, output_socket, input_socket, replace_existing)` line 46; `get_or_create_node(nodes, node_type, name, location)` line 61; `get_or_create_value(nodes, name, label, location, default)` line 70; `find_material_output(material)` line 81; `ensure_surface_light_layer(material, principled)` line 93; `hero_meshes()` line 172; `lift_principled_material(principled)` line 183; `ensure_hero_controls(material)` line 211; `collect_hero_controls()` line 300; `patch_hero_materials(frames)` line 317
- Assignments: `HERO_MATERIAL_EMISSION_MIN`, `HERO_MATERIAL_EMISSION_MAX`, `HERO_MATERIAL_SELF_LIGHT_MIN`, `HERO_MATERIAL_SELF_LIGHT_MAX`, `HERO_MATERIAL_BUMP_MIN`, `HERO_MATERIAL_BUMP_MAX`, `HERO_MATERIAL_ROUGHNESS_MIN`, `HERO_MATERIAL_ROUGHNESS_MAX`, `HERO_MATERIAL_NOISE_SCALE_MIN`, `HERO_MATERIAL_NOISE_SCALE_MAX`, `HERO_MATERIAL_MAPPING_DRIFT`, `PEACE_PALETTE`

## Content
```py
00001: import math
00002: 
00003: import bpy
00004: 
00005: from .common import cfg_value, clear_animation, keyframe_if_possible
00006: 
00007: 
00008: HERO_MATERIAL_EMISSION_MIN = cfg_value("HERO_MATERIAL_EMISSION_MIN", 0.18)
00009: HERO_MATERIAL_EMISSION_MAX = cfg_value("HERO_MATERIAL_EMISSION_MAX", 0.92)
00010: HERO_MATERIAL_SELF_LIGHT_MIN = cfg_value("HERO_MATERIAL_SELF_LIGHT_MIN", 0.018)
00011: HERO_MATERIAL_SELF_LIGHT_MAX = cfg_value("HERO_MATERIAL_SELF_LIGHT_MAX", 0.26)
00012: HERO_MATERIAL_BUMP_MIN = cfg_value("HERO_MATERIAL_BUMP_MIN", 0.010)
00013: HERO_MATERIAL_BUMP_MAX = cfg_value("HERO_MATERIAL_BUMP_MAX", 0.065)
00014: HERO_MATERIAL_ROUGHNESS_MIN = cfg_value("HERO_MATERIAL_ROUGHNESS_MIN", 0.20)
00015: HERO_MATERIAL_ROUGHNESS_MAX = cfg_value("HERO_MATERIAL_ROUGHNESS_MAX", 0.58)
00016: HERO_MATERIAL_NOISE_SCALE_MIN = cfg_value("HERO_MATERIAL_NOISE_SCALE_MIN", 4.0)
00017: HERO_MATERIAL_NOISE_SCALE_MAX = cfg_value("HERO_MATERIAL_NOISE_SCALE_MAX", 13.5)
00018: HERO_MATERIAL_MAPPING_DRIFT = cfg_value("HERO_MATERIAL_MAPPING_DRIFT", 0.18)
00019: PEACE_PALETTE = cfg_value(
00020:     "PEACE_PALETTE",
00021:     {
00022:         "muted_gold": (0.720, 0.620, 0.340, 1.0),
00023:         "warm_white": (0.940, 0.930, 0.900, 1.0),
00024:     },
00025: )
00026: 
00027: 
00028: def find_principled_node(material):
00029:     if material is None or not material.use_nodes:
00030:         return None
00031:     for node in material.node_tree.nodes:
00032:         if node.type == "BSDF_PRINCIPLED":
00033:             return node
00034:     return None
00035: 
00036: 
00037: def get_node_input(node, *names):
00038:     if node is None:
00039:         return None
00040:     for name in names:
00041:         if name in node.inputs:
00042:             return node.inputs[name]
00043:     return None
00044: 
00045: 
00046: def link_node_sockets(links, output_socket, input_socket, replace_existing=False):
00047:     if output_socket is None or input_socket is None:
00048:         return False
00049:     try:
00050:         if replace_existing:
00051:             for link in list(input_socket.links):
00052:                 links.remove(link)
00053:         elif input_socket.is_linked:
00054:             return False
00055:         links.new(output_socket, input_socket)
00056:         return True
00057:     except Exception:
00058:         return False
00059: 
00060: 
00061: def get_or_create_node(nodes, node_type, name, location):
00062:     node = nodes.get(name)
00063:     if node is None:
00064:         node = nodes.new(node_type)
00065:         node.name = name
00066:         node.location = location
00067:     return node
00068: 
00069: 
00070: def get_or_create_value(nodes, name, label, location, default):
00071:     node = nodes.get(name)
00072:     if node is None:
00073:         node = nodes.new("ShaderNodeValue")
00074:         node.name = name
00075:         node.label = label
00076:         node.location = location
00077:     node.outputs[0].default_value = default
00078:     return node
00079: 
00080: 
00081: def find_material_output(material):
00082:     fallback = None
00083:     for node in material.node_tree.nodes:
00084:         if node.type != "OUTPUT_MATERIAL":
00085:             continue
00086:         if fallback is None:
00087:             fallback = node
00088:         if getattr(node, "is_active_output", False):
00089:             return node
00090:     return fallback
00091: 
00092: 
00093: def ensure_surface_light_layer(material, principled):
00094:     nodes = material.node_tree.nodes
00095:     links = material.node_tree.links
00096:     output = find_material_output(material)
00097:     if output is None or "Surface" not in output.inputs:
00098:         return None
00099: 
00100:     self_light = get_or_create_value(
00101:         nodes,
00102:         "HeroMatSelfLightValue",
00103:         "Material-preserving edge light",
00104:         (-520, 445),
00105:         HERO_MATERIAL_SELF_LIGHT_MIN,
00106:     )
00107: 
00108:     layer = get_or_create_node(
00109:         nodes,
00110:         "ShaderNodeLayerWeight",
00111:         "HeroMatSelfLightFacing",
00112:         (-300, 470),
00113:     )
00114: 
00115:     edge_ramp = get_or_create_node(
00116:         nodes,
00117:         "ShaderNodeValToRGB",
00118:         "HeroMatSelfLightRamp",
00119:         (-95, 450),
00120:     )
00121:     edge_ramp.color_ramp.elements[0].position = 0.18
00122:     edge_ramp.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
00123:     edge_ramp.color_ramp.elements[1].position = 0.84
00124:     edge_ramp.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
00125: 
00126:     edge_mul = get_or_create_node(
00127:         nodes,
00128:         "ShaderNodeMath",
00129:         "HeroMatSelfLightEdgeMultiply",
00130:         (125, 445),
00131:     )
00132:     edge_mul.operation = 'MULTIPLY'
00133: 
00134:     emission = get_or_create_node(
00135:         nodes,
00136:         "ShaderNodeEmission",
00137:         "HeroMatSelfLightEmission",
00138:         (350, 385),
00139:     )
00140:     emission.inputs["Color"].default_value = PEACE_PALETTE["muted_gold"]
00141: 
00142:     add_shader = get_or_create_node(
00143:         nodes,
00144:         "ShaderNodeAddShader",
00145:         "HeroMatSelfLightAdd",
00146:         (620, 120),
00147:     )
00148: 
00149:     link_node_sockets(links, self_light.outputs[0], edge_mul.inputs[0], replace_existing=True)
00150:     link_node_sockets(links, layer.outputs.get("Fresnel"), edge_ramp.inputs["Fac"], replace_existing=True)
00151:     link_node_sockets(links, edge_ramp.outputs["Color"], edge_mul.inputs[1], replace_existing=True)
00152:     link_node_sockets(links, edge_mul.outputs[0], emission.inputs["Strength"], replace_existing=True)
00153:     link_node_sockets(links, emission.outputs["Emission"], add_shader.inputs[1], replace_existing=True)
00154: 
00155:     surface_input = output.inputs["Surface"]
00156:     if surface_input.is_linked and surface_input.links[0].from_node == add_shader:
00157:         return self_light.outputs[0]
00158: 
00159:     original_socket = None
00160:     if surface_input.is_linked:
00161:         original_socket = surface_input.links[0].from_socket
00162:         for link in list(surface_input.links):
00163:             links.remove(link)
00164:     elif "BSDF" in principled.outputs:
00165:         original_socket = principled.outputs["BSDF"]
00166: 
00167:     link_node_sockets(links, original_socket, add_shader.inputs[0], replace_existing=True)
00168:     link_node_sockets(links, add_shader.outputs["Shader"], surface_input, replace_existing=True)
00169:     return self_light.outputs[0]
00170: 
00171: 
00172: def hero_meshes():
00173:     root = bpy.data.objects.get("HeroRoot")
00174:     if root is None:
00175:         return []
00176: 
00177:     meshes = [obj for obj in root.children_recursive if obj.type == 'MESH']
00178:     if root.type == 'MESH':
00179:         meshes.append(root)
00180:     return meshes
00181: 
00182: 
00183: def lift_principled_material(principled):
00184:     base_input = get_node_input(principled, "Base Color")
00185:     if base_input is not None:
00186:         try:
00187:             base = base_input.default_value
00188:             base[0] = min(1.0, max(0.20, base[0] * 0.82 + 0.14))
00189:             base[1] = min(1.0, max(0.22, base[1] * 0.86 + 0.11))
00190:             base[2] = min(1.0, max(0.22, base[2] * 0.90 + 0.09))
00191:             if len(base) > 3:
00192:                 base[3] = 1.0
00193:         except Exception:
00194:             pass
00195: 
00196:     metallic = get_node_input(principled, "Metallic")
00197:     if metallic is not None:
00198:         try:
00199:             metallic.default_value = min(metallic.default_value, 0.22)
00200:         except Exception:
00201:             pass
00202: 
00203:     emission_color = get_node_input(principled, "Emission Color", "Emission")
00204:     if emission_color is not None:
00205:         try:
00206:             emission_color.default_value = PEACE_PALETTE["muted_gold"]
00207:         except Exception:
00208:             pass
00209: 
00210: 
00211: def ensure_hero_controls(material):
00212:     material.use_nodes = True
00213:     material["spaziotempo_self_lit"] = True
00214: 
00215:     principled = find_principled_node(material)
00216:     if principled is None:
00217:         return None
00218: 
00219:     lift_principled_material(principled)
00220: 
00221:     nodes = material.node_tree.nodes
00222:     links = material.node_tree.links
00223:     emission_input = get_node_input(principled, "Emission Strength")
00224:     roughness_input = get_node_input(principled, "Roughness")
00225:     normal_input = get_node_input(principled, "Normal")
00226: 
00227:     emission_value = get_or_create_value(
00228:         nodes,
00229:         "HeroMatEmissionValue",
00230:         "Audio Emission",
00231:         (-520, 280),
00232:         HERO_MATERIAL_EMISSION_MIN,
00233:     )
00234:     roughness_value = get_or_create_value(
00235:         nodes,
00236:         "HeroMatRoughnessValue",
00237:         "Audio Roughness",
00238:         (-520, 100),
00239:         HERO_MATERIAL_ROUGHNESS_MAX,
00240:     )
00241:     bump_value = get_or_create_value(
00242:         nodes,
00243:         "HeroMatBumpStrength",
00244:         "Audio Bump",
00245:         (-520, -110),
00246:         HERO_MATERIAL_BUMP_MIN,
00247:     )
00248: 
00249:     mapping = nodes.get("HeroMatAudioMapping")
00250:     if mapping is None:
00251:         mapping = nodes.new("ShaderNodeMapping")
00252:         mapping.name = "HeroMatAudioMapping"
00253:         mapping.location = (-720, -220)
00254: 
00255:     texcoord = nodes.get("HeroMatTextureCoords")
00256:     if texcoord is None:
00257:         texcoord = nodes.new("ShaderNodeTexCoord")
00258:         texcoord.name = "HeroMatTextureCoords"
00259:         texcoord.location = (-930, -220)
00260: 
00261:     noise = nodes.get("HeroMatAudioNoise")
00262:     if noise is None:
00263:         noise = nodes.new("ShaderNodeTexNoise")
00264:         noise.name = "HeroMatAudioNoise"
00265:         noise.location = (-500, -260)
00266:         noise.inputs["Detail"].default_value = 12.0
00267:         noise.inputs["Roughness"].default_value = 0.62
00268:     noise.inputs["Scale"].default_value = HERO_MATERIAL_NOISE_SCALE_MIN
00269: 
00270:     bump = nodes.get("HeroMatAudioBump")
00271:     if bump is None:
00272:         bump = nodes.new("ShaderNodeBump")
00273:         bump.name = "HeroMatAudioBump"
00274:         bump.location = (-245, -215)
00275:         bump.inputs["Distance"].default_value = 0.28
00276: 
00277:     link_node_sockets(links, emission_value.outputs[0], emission_input, replace_existing=True)
00278:     link_node_sockets(links, roughness_value.outputs[0], roughness_input, replace_existing=True)
00279:     link_node_sockets(links, texcoord.outputs.get("Generated"), mapping.inputs.get("Vector"))
00280:     link_node_sockets(links, mapping.outputs.get("Vector"), noise.inputs.get("Vector"))
00281:     link_node_sockets(links, noise.outputs.get("Fac"), bump.inputs.get("Height"))
00282:     link_node_sockets(links, bump_value.outputs[0], bump.inputs.get("Strength"), replace_existing=True)
00283:     link_node_sockets(links, bump.outputs.get("Normal"), normal_input)
00284: 
00285:     self_light_socket = ensure_surface_light_layer(material, principled)
00286: 
00287:     return {
00288:         "material": material,
00289:         "node_tree": material.node_tree,
00290:         "emission_socket": emission_value.outputs[0],
00291:         "self_light_socket": self_light_socket,
```
