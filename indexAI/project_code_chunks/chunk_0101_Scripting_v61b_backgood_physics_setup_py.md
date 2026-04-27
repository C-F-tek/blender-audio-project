# Project Code Chunk 101/212

- File: `Scripting/v61b_backgood/physics_setup.py`
- Part: `1`
- Lines: `1-323`

## Symbol Map
- Imports: `bpy`, `math`, `random`, `from config import USE_PHYSICS_ACCENTS, PHYSICS_ACCENT_COUNT, PRIMARY_BASE_Z, TURB_STRENGTH_MIN, VORTEX_STRENGTH_MIN, PHYSICS_ORBIT_RADIUS_MIN, PHYSICS_ORBIT_RADIUS_MAX, TETHER_SPRING_STIFFNESS, TETHER_SPRING_DAMPING, USE_RHYTHM_PARTICLE_PHYSICS, RHYTHM_PARTICLE_COUNT, RHYTHM_DUST_PARTICLE_COUNT, RHYTHM_STREAK_PARTICLE_COUNT, RHYTHM_PARTICLE_LIFETIME, RHYTHM_DUST_LIFETIME, RHYTHM_PARTICLE_EMITTER_RADIUS, RHYTHM_PARTICLE_EMITTER_Z, PARTICLE_SOURCE_LOCATION, RHYTHM_PARTICLE_SOURCE_RADIUS, RHYTHM_PARTICLE_SIZE_MIN, RHYTHM_PARTICLE_NORMAL_MIN, RHYTHM_PARTICLE_TANGENT_MIN, RHYTHM_PARTICLE_BROWNIAN_MIN, USE_ALBUM_LETTER_PARTICLES, ALBUM_PARTICLE_TEXT, ALBUM_LETTER_PARTICLE_COUNT, ALBUM_LETTER_PARTICLE_LIFETIME, ALBUM_LETTER_SOURCE_SIZE, ALBUM_LETTER_EXTRUDE, ALBUM_LETTER_EMISSION_STRENGTH, ALBUM_LETTER_PARTICLE_SIZE_MIN, PHYSICS_ACCENT_EMISSION_MIN, PHYSICS_ACCENT_MIX_MIN, PALETTE_LIST, PEACE_PALETTE`, `from materials import build_variant_material`, `from scene_utils import deselect_all, safe_active`
- Functions: `set_if_available(obj, attr, value)` line 46; `build_particle_emission_material(name, color, strength)` line 56; `build_invisible_emitter_material()` line 78; `get_material_node_socket(material, node_name, socket_name, is_output)` line 102; `add_particle_collision(obj)` line 117; `add_passive_rigidbody(obj)` line 134; `add_active_rigidbody(obj, mass)` line 143; `create_hidden_anchor(name, location)` line 155; `create_spring_constraint(name, object1, object2, location)` line 168; `create_particle_instance(name, color, strength, shape)` line 211; `create_album_letter_particle_collection(parent)` line 251; `create_particle_emitter(name, kind, invisible_mat)` line 335; `configure_particle_system(emitter, name, instance_obj, count, lifetime, particle_size, normal_factor, tangent_factor, brownian_factor, damping, child_count, child_percent, instance_collection)` line 363; `create_rhythm_particle_physics(parent)` line 441; `create_physics_accents(parent)` line 602

## Content
```py
00001: import bpy
00002: import math
00003: import random
00004: 
00005: from config import (
00006:     USE_PHYSICS_ACCENTS,
00007:     PHYSICS_ACCENT_COUNT,
00008:     PRIMARY_BASE_Z,
00009:     TURB_STRENGTH_MIN,
00010:     VORTEX_STRENGTH_MIN,
00011:     PHYSICS_ORBIT_RADIUS_MIN,
00012:     PHYSICS_ORBIT_RADIUS_MAX,
00013:     TETHER_SPRING_STIFFNESS,
00014:     TETHER_SPRING_DAMPING,
00015:     USE_RHYTHM_PARTICLE_PHYSICS,
00016:     RHYTHM_PARTICLE_COUNT,
00017:     RHYTHM_DUST_PARTICLE_COUNT,
00018:     RHYTHM_STREAK_PARTICLE_COUNT,
00019:     RHYTHM_PARTICLE_LIFETIME,
00020:     RHYTHM_DUST_LIFETIME,
00021:     RHYTHM_PARTICLE_EMITTER_RADIUS,
00022:     RHYTHM_PARTICLE_EMITTER_Z,
00023:     PARTICLE_SOURCE_LOCATION,
00024:     RHYTHM_PARTICLE_SOURCE_RADIUS,
00025:     RHYTHM_PARTICLE_SIZE_MIN,
00026:     RHYTHM_PARTICLE_NORMAL_MIN,
00027:     RHYTHM_PARTICLE_TANGENT_MIN,
00028:     RHYTHM_PARTICLE_BROWNIAN_MIN,
00029:     USE_ALBUM_LETTER_PARTICLES,
00030:     ALBUM_PARTICLE_TEXT,
00031:     ALBUM_LETTER_PARTICLE_COUNT,
00032:     ALBUM_LETTER_PARTICLE_LIFETIME,
00033:     ALBUM_LETTER_SOURCE_SIZE,
00034:     ALBUM_LETTER_EXTRUDE,
00035:     ALBUM_LETTER_EMISSION_STRENGTH,
00036:     ALBUM_LETTER_PARTICLE_SIZE_MIN,
00037:     PHYSICS_ACCENT_EMISSION_MIN,
00038:     PHYSICS_ACCENT_MIX_MIN,
00039:     PALETTE_LIST,
00040:     PEACE_PALETTE,
00041: )
00042: from materials import build_variant_material
00043: from scene_utils import deselect_all, safe_active
00044: 
00045: 
00046: def set_if_available(obj, attr, value):
00047:     if not hasattr(obj, attr):
00048:         return
00049: 
00050:     try:
00051:         setattr(obj, attr, value)
00052:     except Exception:
00053:         pass
00054: 
00055: 
00056: def build_particle_emission_material(name, color, strength):
00057:     mat = bpy.data.materials.new(name=name)
00058:     mat.use_nodes = True
00059: 
00060:     nodes = mat.node_tree.nodes
00061:     links = mat.node_tree.links
00062:     for node in list(nodes):
00063:         nodes.remove(node)
00064: 
00065:     out = nodes.new("ShaderNodeOutputMaterial")
00066:     out.location = (420, 0)
00067: 
00068:     emission = nodes.new("ShaderNodeEmission")
00069:     emission.location = (140, 0)
00070:     emission.inputs["Color"].default_value = color
00071:     emission.inputs["Strength"].default_value = strength
00072:     emission.name = f"{name}Emission"
00073: 
00074:     links.new(emission.outputs["Emission"], out.inputs["Surface"])
00075:     return mat, emission.inputs["Strength"]
00076: 
00077: 
00078: def build_invisible_emitter_material():
00079:     mat = bpy.data.materials.new(name="InvisibleParticleEmitterMaterial")
00080:     mat.use_nodes = True
00081: 
00082:     if hasattr(mat, "blend_method"):
00083:         mat.blend_method = 'BLEND'
00084:     if hasattr(mat, "shadow_method"):
00085:         mat.shadow_method = 'NONE'
00086: 
00087:     nodes = mat.node_tree.nodes
00088:     links = mat.node_tree.links
00089:     for node in list(nodes):
00090:         nodes.remove(node)
00091: 
00092:     out = nodes.new("ShaderNodeOutputMaterial")
00093:     out.location = (360, 0)
00094: 
00095:     transparent = nodes.new("ShaderNodeBsdfTransparent")
00096:     transparent.location = (120, 0)
00097: 
00098:     links.new(transparent.outputs["BSDF"], out.inputs["Surface"])
00099:     return mat
00100: 
00101: 
00102: def get_material_node_socket(material, node_name, socket_name, is_output=False):
00103:     if material is None or not material.use_nodes:
00104:         return None
00105: 
00106:     node = material.node_tree.nodes.get(node_name)
00107:     if node is None:
00108:         return None
00109: 
00110:     sockets = node.outputs if is_output else node.inputs
00111:     try:
00112:         return sockets[socket_name]
00113:     except Exception:
00114:         return None
00115: 
00116: 
00117: def add_particle_collision(obj):
00118:     if obj is None:
00119:         return
00120: 
00121:     try:
00122:         if not any(mod.type == 'COLLISION' for mod in obj.modifiers):
00123:             obj.modifiers.new("ParticleFloorCollision", 'COLLISION')
00124: 
00125:         if hasattr(obj, "collision") and obj.collision is not None:
00126:             obj.collision.damping_factor = 0.55
00127:             obj.collision.damping = 0.30
00128:             obj.collision.stickiness = 0.02
00129:             obj.collision.use_particle_kill = False
00130:     except Exception:
00131:         pass
00132: 
00133: 
00134: def add_passive_rigidbody(obj):
00135:     deselect_all()
00136:     safe_active(obj)
00137:     bpy.ops.rigidbody.object_add()
00138:     obj.rigid_body.type = 'PASSIVE'
00139:     obj.rigid_body.friction = 0.6
00140:     obj.rigid_body.restitution = 0.0
00141: 
00142: 
00143: def add_active_rigidbody(obj, mass=0.15):
00144:     deselect_all()
00145:     safe_active(obj)
00146:     bpy.ops.rigidbody.object_add()
00147:     obj.rigid_body.type = 'ACTIVE'
00148:     obj.rigid_body.mass = mass
00149:     obj.rigid_body.linear_damping = 0.28
00150:     obj.rigid_body.angular_damping = 0.45
00151:     obj.rigid_body.collision_shape = 'SPHERE'
00152:     obj.rigid_body.use_deactivation = False
00153: 
00154: 
00155: def create_hidden_anchor(name, location):
00156:     bpy.ops.mesh.primitive_uv_sphere_add(radius=0.04, location=location)
00157:     anchor = bpy.context.active_object
00158:     anchor.name = name
00159:     anchor.hide_render = True
00160:     try:
00161:         anchor.display_type = 'WIRE'
00162:     except Exception:
00163:         pass
00164:     add_passive_rigidbody(anchor)
00165:     return anchor
00166: 
00167: 
00168: def create_spring_constraint(name, object1, object2, location):
00169:     try:
00170:         bpy.ops.object.empty_add(type='PLAIN_AXES', location=location)
00171:         cobj = bpy.context.active_object
00172:         cobj.name = name
00173: 
00174:         deselect_all()
00175:         safe_active(cobj)
00176:         bpy.ops.rigidbody.constraint_add(type='GENERIC_SPRING')
00177: 
00178:         rbc = cobj.rigid_body_constraint
00179:         rbc.object1 = object1
00180:         rbc.object2 = object2
00181: 
00182:         rbc.use_limit_lin_x = True
00183:         rbc.use_limit_lin_y = True
00184:         rbc.use_limit_lin_z = True
00185: 
00186:         rbc.limit_lin_x_lower = -0.45
00187:         rbc.limit_lin_x_upper = 0.45
00188:         rbc.limit_lin_y_lower = -0.45
00189:         rbc.limit_lin_y_upper = 0.45
00190:         rbc.limit_lin_z_lower = -0.45
00191:         rbc.limit_lin_z_upper = 0.45
00192: 
00193:         rbc.use_spring_x = True
00194:         rbc.use_spring_y = True
00195:         rbc.use_spring_z = True
00196: 
00197:         rbc.spring_stiffness_x = TETHER_SPRING_STIFFNESS
00198:         rbc.spring_stiffness_y = TETHER_SPRING_STIFFNESS
00199:         rbc.spring_stiffness_z = TETHER_SPRING_STIFFNESS
00200: 
00201:         rbc.spring_damping_x = TETHER_SPRING_DAMPING
00202:         rbc.spring_damping_y = TETHER_SPRING_DAMPING
00203:         rbc.spring_damping_z = TETHER_SPRING_DAMPING
00204: 
00205:         cobj.hide_render = True
00206:         return cobj
00207:     except Exception:
00208:         return None
00209: 
00210: 
00211: def create_particle_instance(name, color, strength, shape="sphere"):
00212:     if shape == "streak":
00213:         bpy.ops.mesh.primitive_cone_add(
00214:             vertices=7,
00215:             radius1=RHYTHM_PARTICLE_SOURCE_RADIUS * 0.62,
00216:             radius2=RHYTHM_PARTICLE_SOURCE_RADIUS * 0.08,
00217:             depth=RHYTHM_PARTICLE_SOURCE_RADIUS * 4.2,
00218:             location=PARTICLE_SOURCE_LOCATION,
00219:         )
00220:         obj = bpy.context.active_object
00221:         obj.rotation_euler.x = math.radians(90.0)
00222:     else:
00223:         bpy.ops.mesh.primitive_ico_sphere_add(
00224:             subdivisions=1,
00225:             radius=RHYTHM_PARTICLE_SOURCE_RADIUS,
00226:             location=PARTICLE_SOURCE_LOCATION,
00227:         )
00228:         obj = bpy.context.active_object
00229: 
00230:     obj.name = name
00231:     mat, emit_socket = build_particle_emission_material(
00232:         f"{name}Material",
00233:         color,
00234:         strength,
00235:     )
00236:     obj.data.materials.append(mat)
00237: 
00238:     deselect_all()
00239:     safe_active(obj)
00240:     try:
00241:         bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
00242:     except Exception:
00243:         pass
00244: 
00245:     # Kept off-stage so the source is not seen, but render-enabled for particle instancing.
00246:     obj.hide_viewport = True
00247:     obj.hide_render = False
00248:     return obj, mat, emit_socket
00249: 
00250: 
00251: def create_album_letter_particle_collection(parent=None):
00252:     if not USE_ALBUM_LETTER_PARTICLES:
00253:         return None, None, []
00254: 
00255:     collection = bpy.data.collections.new("AlbumLetterParticleCollection")
00256:     bpy.context.scene.collection.children.link(collection)
00257: 
00258:     bpy.ops.object.empty_add(type='PLAIN_AXES', location=PARTICLE_SOURCE_LOCATION)
00259:     root = bpy.context.active_object
00260:     root.name = "AlbumLetterParticleSources"
00261:     root.hide_viewport = False
00262:     root.hide_render = False
00263:     root.display_type = 'WIRE'
00264:     if parent is not None:
00265:         root.parent = parent
00266: 
00267:     letters = []
00268:     chars = [char for char in ALBUM_PARTICLE_TEXT if not char.isspace()]
00269:     if not chars:
00270:         return collection, root, letters
00271: 
00272:     palette = [
00273:         PEACE_PALETTE["warm_white"],
00274:         PEACE_PALETTE["soft_teal"],
00275:         PEACE_PALETTE["muted_gold"],
00276:         PEACE_PALETTE["dust_rose"],
00277:     ]
00278: 
00279:     for idx, char in enumerate(chars):
00280:         x = (idx - len(chars) * 0.5) * 0.18
00281:         bpy.ops.object.text_add(
00282:             location=(
00283:                 PARTICLE_SOURCE_LOCATION[0] + x,
00284:                 PARTICLE_SOURCE_LOCATION[1],
00285:                 PARTICLE_SOURCE_LOCATION[2],
00286:             ),
00287:             rotation=(math.radians(90.0), 0, 0),
00288:         )
00289:         obj = bpy.context.active_object
00290:         obj.name = f"AlbumLetterParticle_{idx:02d}_{char}"
00291:         obj.data.body = char
00292:         obj.data.align_x = 'CENTER'
00293:         obj.data.align_y = 'CENTER'
00294:         obj.data.size = ALBUM_LETTER_SOURCE_SIZE
00295:         obj.data.extrude = ALBUM_LETTER_EXTRUDE
00296:         obj.data.resolution_u = 8
00297: 
00298:         mat, _ = build_particle_emission_material(
00299:             f"AlbumLetterParticleMat_{idx:02d}",
00300:             palette[idx % len(palette)],
00301:             ALBUM_LETTER_EMISSION_STRENGTH,
00302:         )
00303:         obj.data.materials.append(mat)
00304: 
00305:         deselect_all()
00306:         safe_active(obj)
00307:         try:
00308:             bpy.ops.object.convert(target='MESH')
00309:             obj = bpy.context.active_object
00310:             obj.name = f"AlbumLetterParticle_{idx:02d}_{char}"
00311:         except Exception:
00312:             pass
00313: 
00314:         obj.parent = root
00315:         obj.hide_viewport = False
00316:         obj.hide_render = False
00317: 
00318:         try:
00319:             for coll in list(obj.users_collection):
00320:                 if coll != collection:
00321:                     coll.objects.unlink(obj)
00322:             collection.objects.link(obj)
00323:         except Exception:
```
