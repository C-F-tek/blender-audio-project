# Project Code Chunk 50/212

- File: `Scripting/v61b/physics_setup.py`
- Part: `1`
- Lines: `1-323`

## Symbol Map
- Imports: `bpy`, `math`, `random`, `from config import USE_PHYSICS_ACCENTS, PHYSICS_ACCENT_COUNT, PRIMARY_BASE_Z, TURB_STRENGTH_MIN, VORTEX_STRENGTH_MIN, PHYSICS_ORBIT_RADIUS_MIN, PHYSICS_ORBIT_RADIUS_MAX, PHYSICS_ATOM_ORBIT_SPEED_MIN, PHYSICS_ATOM_ORBIT_SPEED_MAX, PHYSICS_ATOM_MICRO_WOBBLE, HERO_GRAVITY_STRENGTH_MIN, TETHER_SPRING_STIFFNESS, TETHER_SPRING_DAMPING, USE_RHYTHM_PARTICLE_PHYSICS, RHYTHM_PARTICLE_COUNT, RHYTHM_DUST_PARTICLE_COUNT, RHYTHM_STREAK_PARTICLE_COUNT, RHYTHM_PARTICLE_LIFETIME, RHYTHM_DUST_LIFETIME, RHYTHM_PARTICLE_EMITTER_RADIUS, RHYTHM_PARTICLE_EMITTER_Z, PARTICLE_SOURCE_LOCATION, RHYTHM_PARTICLE_SOURCE_RADIUS, RHYTHM_PARTICLE_SIZE_MIN, RHYTHM_PARTICLE_NORMAL_MIN, RHYTHM_PARTICLE_TANGENT_MIN, RHYTHM_PARTICLE_BROWNIAN_MIN, USE_ALBUM_LETTER_PARTICLES, ALBUM_PARTICLE_TEXT, ALBUM_LETTER_PARTICLE_COUNT, ALBUM_LETTER_PARTICLE_LIFETIME, ALBUM_LETTER_SOURCE_SIZE, ALBUM_LETTER_EXTRUDE, ALBUM_LETTER_EMISSION_STRENGTH, ALBUM_LETTER_PARTICLE_SIZE_MIN, PHYSICS_ACCENT_EMISSION_MIN, PHYSICS_ACCENT_MIX_MIN, PALETTE_LIST, PEACE_PALETTE`, `from materials import build_variant_material`, `from scene_utils import deselect_all, safe_active`
- Functions: `set_if_available(obj, attr, value)` line 50; `build_particle_emission_material(name, color, strength)` line 60; `build_invisible_emitter_material()` line 82; `get_material_node_socket(material, node_name, socket_name, is_output)` line 106; `add_particle_collision(obj)` line 121; `add_passive_rigidbody(obj)` line 138; `add_active_rigidbody(obj, mass)` line 147; `create_hidden_anchor(name, location)` line 159; `create_spring_constraint(name, object1, object2, location)` line 172; `create_particle_instance(name, color, strength, shape)` line 215; `create_album_letter_particle_collection(parent)` line 255; `create_particle_emitter(name, kind, invisible_mat)` line 339; `configure_particle_system(emitter, name, instance_obj, count, lifetime, particle_size, normal_factor, tangent_factor, brownian_factor, damping, child_count, child_percent, instance_collection)` line 367; `create_rhythm_particle_physics(parent)` line 445; `create_physics_accents(parent)` line 606

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
00013:     PHYSICS_ATOM_ORBIT_SPEED_MIN,
00014:     PHYSICS_ATOM_ORBIT_SPEED_MAX,
00015:     PHYSICS_ATOM_MICRO_WOBBLE,
00016:     HERO_GRAVITY_STRENGTH_MIN,
00017:     TETHER_SPRING_STIFFNESS,
00018:     TETHER_SPRING_DAMPING,
00019:     USE_RHYTHM_PARTICLE_PHYSICS,
00020:     RHYTHM_PARTICLE_COUNT,
00021:     RHYTHM_DUST_PARTICLE_COUNT,
00022:     RHYTHM_STREAK_PARTICLE_COUNT,
00023:     RHYTHM_PARTICLE_LIFETIME,
00024:     RHYTHM_DUST_LIFETIME,
00025:     RHYTHM_PARTICLE_EMITTER_RADIUS,
00026:     RHYTHM_PARTICLE_EMITTER_Z,
00027:     PARTICLE_SOURCE_LOCATION,
00028:     RHYTHM_PARTICLE_SOURCE_RADIUS,
00029:     RHYTHM_PARTICLE_SIZE_MIN,
00030:     RHYTHM_PARTICLE_NORMAL_MIN,
00031:     RHYTHM_PARTICLE_TANGENT_MIN,
00032:     RHYTHM_PARTICLE_BROWNIAN_MIN,
00033:     USE_ALBUM_LETTER_PARTICLES,
00034:     ALBUM_PARTICLE_TEXT,
00035:     ALBUM_LETTER_PARTICLE_COUNT,
00036:     ALBUM_LETTER_PARTICLE_LIFETIME,
00037:     ALBUM_LETTER_SOURCE_SIZE,
00038:     ALBUM_LETTER_EXTRUDE,
00039:     ALBUM_LETTER_EMISSION_STRENGTH,
00040:     ALBUM_LETTER_PARTICLE_SIZE_MIN,
00041:     PHYSICS_ACCENT_EMISSION_MIN,
00042:     PHYSICS_ACCENT_MIX_MIN,
00043:     PALETTE_LIST,
00044:     PEACE_PALETTE,
00045: )
00046: from materials import build_variant_material
00047: from scene_utils import deselect_all, safe_active
00048: 
00049: 
00050: def set_if_available(obj, attr, value):
00051:     if not hasattr(obj, attr):
00052:         return
00053: 
00054:     try:
00055:         setattr(obj, attr, value)
00056:     except Exception:
00057:         pass
00058: 
00059: 
00060: def build_particle_emission_material(name, color, strength):
00061:     mat = bpy.data.materials.new(name=name)
00062:     mat.use_nodes = True
00063: 
00064:     nodes = mat.node_tree.nodes
00065:     links = mat.node_tree.links
00066:     for node in list(nodes):
00067:         nodes.remove(node)
00068: 
00069:     out = nodes.new("ShaderNodeOutputMaterial")
00070:     out.location = (420, 0)
00071: 
00072:     emission = nodes.new("ShaderNodeEmission")
00073:     emission.location = (140, 0)
00074:     emission.inputs["Color"].default_value = color
00075:     emission.inputs["Strength"].default_value = strength
00076:     emission.name = f"{name}Emission"
00077: 
00078:     links.new(emission.outputs["Emission"], out.inputs["Surface"])
00079:     return mat, emission.inputs["Strength"]
00080: 
00081: 
00082: def build_invisible_emitter_material():
00083:     mat = bpy.data.materials.new(name="InvisibleParticleEmitterMaterial")
00084:     mat.use_nodes = True
00085: 
00086:     if hasattr(mat, "blend_method"):
00087:         mat.blend_method = 'BLEND'
00088:     if hasattr(mat, "shadow_method"):
00089:         mat.shadow_method = 'NONE'
00090: 
00091:     nodes = mat.node_tree.nodes
00092:     links = mat.node_tree.links
00093:     for node in list(nodes):
00094:         nodes.remove(node)
00095: 
00096:     out = nodes.new("ShaderNodeOutputMaterial")
00097:     out.location = (360, 0)
00098: 
00099:     transparent = nodes.new("ShaderNodeBsdfTransparent")
00100:     transparent.location = (120, 0)
00101: 
00102:     links.new(transparent.outputs["BSDF"], out.inputs["Surface"])
00103:     return mat
00104: 
00105: 
00106: def get_material_node_socket(material, node_name, socket_name, is_output=False):
00107:     if material is None or not material.use_nodes:
00108:         return None
00109: 
00110:     node = material.node_tree.nodes.get(node_name)
00111:     if node is None:
00112:         return None
00113: 
00114:     sockets = node.outputs if is_output else node.inputs
00115:     try:
00116:         return sockets[socket_name]
00117:     except Exception:
00118:         return None
00119: 
00120: 
00121: def add_particle_collision(obj):
00122:     if obj is None:
00123:         return
00124: 
00125:     try:
00126:         if not any(mod.type == 'COLLISION' for mod in obj.modifiers):
00127:             obj.modifiers.new("ParticleFloorCollision", 'COLLISION')
00128: 
00129:         if hasattr(obj, "collision") and obj.collision is not None:
00130:             obj.collision.damping_factor = 0.55
00131:             obj.collision.damping = 0.30
00132:             obj.collision.stickiness = 0.02
00133:             obj.collision.use_particle_kill = False
00134:     except Exception:
00135:         pass
00136: 
00137: 
00138: def add_passive_rigidbody(obj):
00139:     deselect_all()
00140:     safe_active(obj)
00141:     bpy.ops.rigidbody.object_add()
00142:     obj.rigid_body.type = 'PASSIVE'
00143:     obj.rigid_body.friction = 0.6
00144:     obj.rigid_body.restitution = 0.0
00145: 
00146: 
00147: def add_active_rigidbody(obj, mass=0.15):
00148:     deselect_all()
00149:     safe_active(obj)
00150:     bpy.ops.rigidbody.object_add()
00151:     obj.rigid_body.type = 'ACTIVE'
00152:     obj.rigid_body.mass = mass
00153:     obj.rigid_body.linear_damping = 0.28
00154:     obj.rigid_body.angular_damping = 0.45
00155:     obj.rigid_body.collision_shape = 'SPHERE'
00156:     obj.rigid_body.use_deactivation = False
00157: 
00158: 
00159: def create_hidden_anchor(name, location):
00160:     bpy.ops.mesh.primitive_uv_sphere_add(radius=0.04, location=location)
00161:     anchor = bpy.context.active_object
00162:     anchor.name = name
00163:     anchor.hide_render = True
00164:     try:
00165:         anchor.display_type = 'WIRE'
00166:     except Exception:
00167:         pass
00168:     add_passive_rigidbody(anchor)
00169:     return anchor
00170: 
00171: 
00172: def create_spring_constraint(name, object1, object2, location):
00173:     try:
00174:         bpy.ops.object.empty_add(type='PLAIN_AXES', location=location)
00175:         cobj = bpy.context.active_object
00176:         cobj.name = name
00177: 
00178:         deselect_all()
00179:         safe_active(cobj)
00180:         bpy.ops.rigidbody.constraint_add(type='GENERIC_SPRING')
00181: 
00182:         rbc = cobj.rigid_body_constraint
00183:         rbc.object1 = object1
00184:         rbc.object2 = object2
00185: 
00186:         rbc.use_limit_lin_x = True
00187:         rbc.use_limit_lin_y = True
00188:         rbc.use_limit_lin_z = True
00189: 
00190:         rbc.limit_lin_x_lower = -0.45
00191:         rbc.limit_lin_x_upper = 0.45
00192:         rbc.limit_lin_y_lower = -0.45
00193:         rbc.limit_lin_y_upper = 0.45
00194:         rbc.limit_lin_z_lower = -0.45
00195:         rbc.limit_lin_z_upper = 0.45
00196: 
00197:         rbc.use_spring_x = True
00198:         rbc.use_spring_y = True
00199:         rbc.use_spring_z = True
00200: 
00201:         rbc.spring_stiffness_x = TETHER_SPRING_STIFFNESS
00202:         rbc.spring_stiffness_y = TETHER_SPRING_STIFFNESS
00203:         rbc.spring_stiffness_z = TETHER_SPRING_STIFFNESS
00204: 
00205:         rbc.spring_damping_x = TETHER_SPRING_DAMPING
00206:         rbc.spring_damping_y = TETHER_SPRING_DAMPING
00207:         rbc.spring_damping_z = TETHER_SPRING_DAMPING
00208: 
00209:         cobj.hide_render = True
00210:         return cobj
00211:     except Exception:
00212:         return None
00213: 
00214: 
00215: def create_particle_instance(name, color, strength, shape="sphere"):
00216:     if shape == "streak":
00217:         bpy.ops.mesh.primitive_cone_add(
00218:             vertices=7,
00219:             radius1=RHYTHM_PARTICLE_SOURCE_RADIUS * 0.62,
00220:             radius2=RHYTHM_PARTICLE_SOURCE_RADIUS * 0.08,
00221:             depth=RHYTHM_PARTICLE_SOURCE_RADIUS * 4.2,
00222:             location=PARTICLE_SOURCE_LOCATION,
00223:         )
00224:         obj = bpy.context.active_object
00225:         obj.rotation_euler.x = math.radians(90.0)
00226:     else:
00227:         bpy.ops.mesh.primitive_ico_sphere_add(
00228:             subdivisions=1,
00229:             radius=RHYTHM_PARTICLE_SOURCE_RADIUS,
00230:             location=PARTICLE_SOURCE_LOCATION,
00231:         )
00232:         obj = bpy.context.active_object
00233: 
00234:     obj.name = name
00235:     mat, emit_socket = build_particle_emission_material(
00236:         f"{name}Material",
00237:         color,
00238:         strength,
00239:     )
00240:     obj.data.materials.append(mat)
00241: 
00242:     deselect_all()
00243:     safe_active(obj)
00244:     try:
00245:         bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
00246:     except Exception:
00247:         pass
00248: 
00249:     # Kept off-stage so the source is not seen, but render-enabled for particle instancing.
00250:     obj.hide_viewport = True
00251:     obj.hide_render = False
00252:     return obj, mat, emit_socket
00253: 
00254: 
00255: def create_album_letter_particle_collection(parent=None):
00256:     if not USE_ALBUM_LETTER_PARTICLES:
00257:         return None, None, []
00258: 
00259:     collection = bpy.data.collections.new("AlbumLetterParticleCollection")
00260:     bpy.context.scene.collection.children.link(collection)
00261: 
00262:     bpy.ops.object.empty_add(type='PLAIN_AXES', location=PARTICLE_SOURCE_LOCATION)
00263:     root = bpy.context.active_object
00264:     root.name = "AlbumLetterParticleSources"
00265:     root.hide_viewport = False
00266:     root.hide_render = False
00267:     root.display_type = 'WIRE'
00268:     if parent is not None:
00269:         root.parent = parent
00270: 
00271:     letters = []
00272:     chars = [char for char in ALBUM_PARTICLE_TEXT if not char.isspace()]
00273:     if not chars:
00274:         return collection, root, letters
00275: 
00276:     palette = [
00277:         PEACE_PALETTE["warm_white"],
00278:         PEACE_PALETTE["soft_teal"],
00279:         PEACE_PALETTE["muted_gold"],
00280:         PEACE_PALETTE["dust_rose"],
00281:     ]
00282: 
00283:     for idx, char in enumerate(chars):
00284:         x = (idx - len(chars) * 0.5) * 0.18
00285:         bpy.ops.object.text_add(
00286:             location=(
00287:                 PARTICLE_SOURCE_LOCATION[0] + x,
00288:                 PARTICLE_SOURCE_LOCATION[1],
00289:                 PARTICLE_SOURCE_LOCATION[2],
00290:             ),
00291:             rotation=(math.radians(90.0), 0, 0),
00292:         )
00293:         obj = bpy.context.active_object
00294:         obj.name = f"AlbumLetterParticle_{idx:02d}_{char}"
00295:         obj.data.body = char
00296:         obj.data.align_x = 'CENTER'
00297:         obj.data.align_y = 'CENTER'
00298:         obj.data.size = ALBUM_LETTER_SOURCE_SIZE
00299:         obj.data.extrude = ALBUM_LETTER_EXTRUDE
00300:         obj.data.resolution_u = 8
00301: 
00302:         mat, _ = build_particle_emission_material(
00303:             f"AlbumLetterParticleMat_{idx:02d}",
00304:             palette[idx % len(palette)],
00305:             ALBUM_LETTER_EMISSION_STRENGTH,
00306:         )
00307:         obj.data.materials.append(mat)
00308: 
00309:         deselect_all()
00310:         safe_active(obj)
00311:         try:
00312:             bpy.ops.object.convert(target='MESH')
00313:             obj = bpy.context.active_object
00314:             obj.name = f"AlbumLetterParticle_{idx:02d}_{char}"
00315:         except Exception:
00316:             pass
00317: 
00318:         obj.parent = root
00319:         obj.hide_viewport = False
00320:         obj.hide_render = False
00321: 
00322:         try:
00323:             for coll in list(obj.users_collection):
```
