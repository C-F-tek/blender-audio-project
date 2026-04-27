# Project Code Chunk 17/212

- File: `Scripting/v61b/asset_setup.py`
- Part: `1`
- Lines: `1-316`

## Symbol Map
- Imports: `bpy`, `from mathutils import Vector`, `from pathlib import Path`, `from config import PRIMARY_ASSET_DIR, PRIMARY_TARGET_SIZE, PRIMARY_BASE_Z, SUPPORTED_ASSET_EXTENSIONS, USE_SECONDARY_ASSET, SECONDARY_ASSET_DIR, SECONDARY_TARGET_SIZE, SECONDARY_BASE_Z, SECONDARY_BASE_OFFSET_X, SECONDARY_BASE_OFFSET_Y, SECONDARY_BASE_OFFSET_Z, PEACE_PALETTE, USE_HERO_MESH_DEFORM, HERO_DEFORM_STRENGTH_MAX, HERO_DEFORM_STRENGTH_MIN, HERO_DEFORM_DETAIL_STRENGTH_MAX, HERO_DEFORM_WAVE_HEIGHT_MAX, HERO_DEFORM_MAIN_DIM_FACTOR, HERO_DEFORM_DETAIL_DIM_FACTOR, HERO_DEFORM_WAVE_DIM_FACTOR, HERO_DEFORM_TWIST_MAX, HERO_DEFORM_SUBDIV_VIEW, HERO_DEFORM_SUBDIV_RENDER, HERO_DEFORM_NOISE_SIZE, HERO_DEFORM_DETAIL_NOISE_SIZE, HERO_DEFORM_NOISE_CONTRAST, HERO_DEFORM_CONTROLLER_Z, USE_HERO_MATERIAL_AUDIO_NODES, HERO_MATERIAL_EMISSION_MIN, HERO_MATERIAL_SELF_LIGHT_MIN, HERO_MATERIAL_BUMP_MIN, HERO_MATERIAL_ROUGHNESS_MAX, HERO_MATERIAL_NOISE_SCALE_MIN`, `from scene_utils import create_controller_empty`
- Functions: `find_asset_file(asset_dir)` line 43; `import_asset_file(asset_file)` line 62; `get_world_bbox(objects)` line 94; `create_scene_core()` line 127; `make_asset_root(name)` line 134; `parent_objects_keep_transform(objects, parent)` line 141; `center_and_scale_asset(root, objects, target_size, base_z)` line 150; `collect_meshes(objects)` line 171; `soften_materials_to_peace(meshes)` line 175; `find_principled_node(material)` line 206; `get_node_input(node)` line 216; `link_node_sockets(links, output_socket, input_socket, replace_existing)` line 226; `get_or_create_node(nodes, node_type, name, location)` line 243; `find_material_output(material)` line 252; `ensure_hero_surface_light_layer(mat, principled)` line 266; `get_local_mesh_extent(obj)` line 346; `add_hero_material_audio_nodes(meshes)` line 360; `duplicate_hierarchy(root, name_prefix)` line 460; `assign_material_to_hierarchy(root, material)` line 488; `add_hero_mesh_deformers(asset_root, meshes)` line 498; `_create_asset_from_dir(asset_dir, target_size, base_z, root_name, parent)` line 653; `create_primary_asset(parent)` line 688; `create_secondary_asset(parent)` line 698

## Content
```py
00001: import bpy
00002: from mathutils import Vector
00003: from pathlib import Path
00004: 
00005: from config import (
00006:     PRIMARY_ASSET_DIR,
00007:     PRIMARY_TARGET_SIZE,
00008:     PRIMARY_BASE_Z,
00009:     SUPPORTED_ASSET_EXTENSIONS,
00010:     USE_SECONDARY_ASSET,
00011:     SECONDARY_ASSET_DIR,
00012:     SECONDARY_TARGET_SIZE,
00013:     SECONDARY_BASE_Z,
00014:     SECONDARY_BASE_OFFSET_X,
00015:     SECONDARY_BASE_OFFSET_Y,
00016:     SECONDARY_BASE_OFFSET_Z,
00017:     PEACE_PALETTE,
00018:     USE_HERO_MESH_DEFORM,
00019:     HERO_DEFORM_STRENGTH_MAX,
00020:     HERO_DEFORM_STRENGTH_MIN,
00021:     HERO_DEFORM_DETAIL_STRENGTH_MAX,
00022:     HERO_DEFORM_WAVE_HEIGHT_MAX,
00023:     HERO_DEFORM_MAIN_DIM_FACTOR,
00024:     HERO_DEFORM_DETAIL_DIM_FACTOR,
00025:     HERO_DEFORM_WAVE_DIM_FACTOR,
00026:     HERO_DEFORM_TWIST_MAX,
00027:     HERO_DEFORM_SUBDIV_VIEW,
00028:     HERO_DEFORM_SUBDIV_RENDER,
00029:     HERO_DEFORM_NOISE_SIZE,
00030:     HERO_DEFORM_DETAIL_NOISE_SIZE,
00031:     HERO_DEFORM_NOISE_CONTRAST,
00032:     HERO_DEFORM_CONTROLLER_Z,
00033:     USE_HERO_MATERIAL_AUDIO_NODES,
00034:     HERO_MATERIAL_EMISSION_MIN,
00035:     HERO_MATERIAL_SELF_LIGHT_MIN,
00036:     HERO_MATERIAL_BUMP_MIN,
00037:     HERO_MATERIAL_ROUGHNESS_MAX,
00038:     HERO_MATERIAL_NOISE_SCALE_MIN,
00039: )
00040: from scene_utils import create_controller_empty
00041: 
00042: 
00043: def find_asset_file(asset_dir: Path) -> Path:
00044:     if not asset_dir.exists():
00045:         raise FileNotFoundError(f"Cartella asset non trovata: {asset_dir}")
00046: 
00047:     files = []
00048:     for ext in SUPPORTED_ASSET_EXTENSIONS:
00049:         files.extend(asset_dir.rglob(f"*{ext}"))
00050: 
00051:     if not files:
00052:         raise FileNotFoundError(
00053:             f"Nessun asset supportato trovato in: {asset_dir}\n"
00054:             f"Estensioni cercate: {SUPPORTED_ASSET_EXTENSIONS}"
00055:         )
00056: 
00057:     priority = {".fbx": 0, ".glb": 1, ".gltf": 2, ".obj": 3, ".blend": 4}
00058:     files.sort(key=lambda p: (priority.get(p.suffix.lower(), 99), str(p)))
00059:     return files[0]
00060: 
00061: 
00062: def import_asset_file(asset_file: Path):
00063:     ext = asset_file.suffix.lower()
00064:     before = set(obj.name for obj in bpy.data.objects)
00065: 
00066:     if ext == ".fbx":
00067:         bpy.ops.import_scene.fbx(filepath=str(asset_file))
00068:     elif ext in {".glb", ".gltf"}:
00069:         bpy.ops.import_scene.gltf(filepath=str(asset_file))
00070:     elif ext == ".obj":
00071:         try:
00072:             bpy.ops.wm.obj_import(filepath=str(asset_file))
00073:         except Exception:
00074:             bpy.ops.import_scene.obj(filepath=str(asset_file))
00075:     elif ext == ".blend":
00076:         with bpy.data.libraries.load(str(asset_file), link=False) as (data_from, data_to):
00077:             data_to.objects = data_from.objects
00078:         for obj in data_to.objects:
00079:             if obj is not None:
00080:                 bpy.context.collection.objects.link(obj)
00081:     else:
00082:         raise RuntimeError(f"Formato non supportato: {ext}")
00083: 
00084:     after = set(obj.name for obj in bpy.data.objects)
00085:     new_names = after - before
00086:     imported = [bpy.data.objects[name] for name in new_names if name in bpy.data.objects]
00087: 
00088:     if not imported:
00089:         raise RuntimeError(f"Import completato ma nessun oggetto rilevato: {asset_file}")
00090: 
00091:     return imported
00092: 
00093: 
00094: def get_world_bbox(objects):
00095:     coords = []
00096:     depsgraph = bpy.context.evaluated_depsgraph_get()
00097: 
00098:     for obj in objects:
00099:         if obj.type not in {"MESH", "CURVE", "SURFACE", "META", "FONT", "EMPTY", "ARMATURE"}:
00100:             continue
00101: 
00102:         if obj.type == "EMPTY":
00103:             coords.append(obj.matrix_world.translation.copy())
00104:             continue
00105: 
00106:         try:
00107:             obj_eval = obj.evaluated_get(depsgraph)
00108:             bbox = [obj_eval.matrix_world @ Vector(corner) for corner in obj_eval.bound_box]
00109:             coords.extend(bbox)
00110:         except Exception:
00111:             try:
00112:                 bbox = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
00113:                 coords.extend(bbox)
00114:             except Exception:
00115:                 coords.append(obj.matrix_world.translation.copy())
00116: 
00117:     if not coords:
00118:         return Vector((0, 0, 0)), Vector((1, 1, 1)), Vector((0, 0, 0)), Vector((0, 0, 0))
00119: 
00120:     min_v = Vector((min(v.x for v in coords), min(v.y for v in coords), min(v.z for v in coords)))
00121:     max_v = Vector((max(v.x for v in coords), max(v.y for v in coords), max(v.z for v in coords)))
00122:     center = (min_v + max_v) * 0.5
00123:     size = max_v - min_v
00124:     return center, size, min_v, max_v
00125: 
00126: 
00127: def create_scene_core():
00128:     bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
00129:     root = bpy.context.active_object
00130:     root.name = "SceneCore"
00131:     return root
00132: 
00133: 
00134: def make_asset_root(name):
00135:     bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
00136:     root = bpy.context.active_object
00137:     root.name = name
00138:     return root
00139: 
00140: 
00141: def parent_objects_keep_transform(objects, parent):
00142:     for obj in objects:
00143:         if obj == parent:
00144:             continue
00145:         mw = obj.matrix_world.copy()
00146:         obj.parent = parent
00147:         obj.matrix_world = mw
00148: 
00149: 
00150: def center_and_scale_asset(root, objects, target_size, base_z):
00151:     bpy.context.view_layer.update()
00152: 
00153:     center, size, min_v, _ = get_world_bbox(objects)
00154:     max_dim = max(size.x, size.y, size.z)
00155:     if max_dim <= 0.0001:
00156:         max_dim = 1.0
00157: 
00158:     scale_factor = target_size / max_dim
00159:     root.scale = (scale_factor, scale_factor, scale_factor)
00160: 
00161:     bpy.context.view_layer.update()
00162: 
00163:     center, _, min_v, _ = get_world_bbox(objects)
00164:     root.location.x += -center.x
00165:     root.location.y += -center.y
00166:     root.location.z += (base_z - min_v.z)
00167: 
00168:     bpy.context.view_layer.update()
00169: 
00170: 
00171: def collect_meshes(objects):
00172:     return [obj for obj in objects if obj.type == "MESH"]
00173: 
00174: 
00175: def soften_materials_to_peace(meshes):
00176:     for obj in meshes:
00177:         for slot in obj.material_slots:
00178:             mat = slot.material
00179:             if mat is None or not mat.use_nodes:
00180:                 continue
00181: 
00182:             principled = None
00183:             for node in mat.node_tree.nodes:
00184:                 if node.type == "BSDF_PRINCIPLED":
00185:                     principled = node
00186:                     break
00187: 
00188:             if principled is None:
00189:                 continue
00190: 
00191:             try:
00192:                 base = principled.inputs["Base Color"].default_value
00193:                 base[0] = min(1.0, max(0.18, base[0] * 0.84 + 0.12))
00194:                 base[1] = min(1.0, max(0.20, base[1] * 0.88 + 0.10))
00195:                 base[2] = min(1.0, max(0.20, base[2] * 0.92 + 0.08))
00196:                 metallic = get_node_input(principled, "Metallic")
00197:                 if metallic is not None:
00198:                     metallic.default_value = min(metallic.default_value, 0.22)
00199:                 principled.inputs["Roughness"].default_value = min(
00200:                     1.0, max(0.18, principled.inputs["Roughness"].default_value)
00201:                 )
00202:             except Exception:
00203:                 pass
00204: 
00205: 
00206: def find_principled_node(material):
00207:     if material is None or not material.use_nodes:
00208:         return None
00209: 
00210:     for node in material.node_tree.nodes:
00211:         if node.type == "BSDF_PRINCIPLED":
00212:             return node
00213:     return None
00214: 
00215: 
00216: def get_node_input(node, *names):
00217:     if node is None:
00218:         return None
00219: 
00220:     for name in names:
00221:         if name in node.inputs:
00222:             return node.inputs[name]
00223:     return None
00224: 
00225: 
00226: def link_node_sockets(links, output_socket, input_socket, replace_existing=False):
00227:     if output_socket is None or input_socket is None:
00228:         return False
00229: 
00230:     try:
00231:         if replace_existing:
00232:             for link in list(input_socket.links):
00233:                 links.remove(link)
00234:         elif input_socket.is_linked:
00235:             return False
00236: 
00237:         links.new(output_socket, input_socket)
00238:         return True
00239:     except Exception:
00240:         return False
00241: 
00242: 
00243: def get_or_create_node(nodes, node_type, name, location):
00244:     node = nodes.get(name)
00245:     if node is None:
00246:         node = nodes.new(node_type)
00247:         node.name = name
00248:         node.location = location
00249:     return node
00250: 
00251: 
00252: def find_material_output(material):
00253:     if material is None or not material.use_nodes:
00254:         return None
00255:     fallback = None
00256:     for node in material.node_tree.nodes:
00257:         if node.type != "OUTPUT_MATERIAL":
00258:             continue
00259:         if fallback is None:
00260:             fallback = node
00261:         if getattr(node, "is_active_output", False):
00262:             return node
00263:     return fallback
00264: 
00265: 
00266: def ensure_hero_surface_light_layer(mat, principled):
00267:     nodes = mat.node_tree.nodes
00268:     links = mat.node_tree.links
00269:     output = find_material_output(mat)
00270:     if output is None or "Surface" not in output.inputs:
00271:         return None
00272: 
00273:     self_light = get_or_create_node(
00274:         nodes,
00275:         "ShaderNodeValue",
00276:         "HeroMatSelfLightValue",
00277:         (-520, 445),
00278:     )
00279:     self_light.label = "Material-preserving edge light"
00280:     self_light.outputs[0].default_value = HERO_MATERIAL_SELF_LIGHT_MIN
00281: 
00282:     layer = get_or_create_node(
00283:         nodes,
00284:         "ShaderNodeLayerWeight",
00285:         "HeroMatSelfLightFacing",
00286:         (-300, 470),
00287:     )
00288: 
00289:     edge_ramp = get_or_create_node(
00290:         nodes,
00291:         "ShaderNodeValToRGB",
00292:         "HeroMatSelfLightRamp",
00293:         (-95, 450),
00294:     )
00295:     edge_ramp.color_ramp.elements[0].position = 0.18
00296:     edge_ramp.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
00297:     edge_ramp.color_ramp.elements[1].position = 0.84
00298:     edge_ramp.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
00299: 
00300:     edge_mul = get_or_create_node(
00301:         nodes,
00302:         "ShaderNodeMath",
00303:         "HeroMatSelfLightEdgeMultiply",
00304:         (125, 445),
00305:     )
00306:     edge_mul.operation = 'MULTIPLY'
00307: 
00308:     emission = get_or_create_node(
00309:         nodes,
00310:         "ShaderNodeEmission",
00311:         "HeroMatSelfLightEmission",
00312:         (350, 385),
00313:     )
00314:     emission.inputs["Color"].default_value = PEACE_PALETTE["muted_gold"]
00315: 
00316:     add_shader = get_or_create_node(
```
