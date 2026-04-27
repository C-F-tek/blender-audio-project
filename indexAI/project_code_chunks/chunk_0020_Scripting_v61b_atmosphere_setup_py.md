# Project Code Chunk 20/212

- File: `Scripting/v61b/atmosphere_setup.py`
- Part: `1`
- Lines: `1-346`

## Symbol Map
- Imports: `bpy`, `math`, `random`, `from config import PRIMARY_BASE_Z, AURA_RADIUS, USE_HERO_AURA_MESH, AURA_DEFORM_SUBDIV_VIEW, AURA_DEFORM_SUBDIV_RENDER, AURA_DEFORM_FIELD_RADIUS, AURA_DEFORM_DISPLACE_MIN, AURA_DEFORM_DISPLACE_MAX, AURA_DEFORM_DETAIL_MAX, AURA_DEFORM_WAVE_HEIGHT_MAX, AURA_DEFORM_FIELD_STRENGTH_MAX, ENERGY_RING_COUNT, RIBBON_COUNT, CREATE_VARIANTS, VARIANT_COUNT, VARIANT_RING_RADIUS, VARIANT_SCALE_MIN, VARIANT_SCALE_MAX, USE_MIST_PARTICLES, MIST_PARTICLE_COUNT, MIST_SCALE_MIN, MIST_SCALE_MAX, ATMOSPHERE_CUBE_SIZE, FOG_VOLUME_ENABLED, FOG_VOLUME_VIEWPORT_VISIBLE, FOG_RAMP_LOW_BASE, FOG_RAMP_HIGH_BASE, PALETTE_LIST, PEACE_PALETTE`, `from materials import build_aura_material, build_ring_material, build_ribbon_material, build_variant_material, build_atmosphere_volume_material, build_mist_particle_material`, `from asset_setup import duplicate_hierarchy, assign_material_to_hierarchy`, `from scene_utils import create_controller_empty`, `from fog_filaments import ensure_fog_filaments`
- Functions: `init_audio_props(obj)` line 62; `add_prop_driver(idblock, data_path, expression, prop_targets)` line 71; `create_aura_deform_field(controller, aura_location, parent)` line 96; `add_hero_aura_deformers(aura, controller, deform_field)` line 144; `create_hero_aura(parent)` line 249; `create_energy_rings(parent)` line 325; `create_energy_ribbons(parent)` line 361; `create_variants(hero_root, parent)` line 399; `create_atmosphere_cube(parent)` line 433; `create_mist_particles(parent)` line 502
- Assignments: `AURA_AUDIO_PROPS`

## Content
```py
00001: import bpy
00002: import math
00003: import random
00004: 
00005: from config import (
00006:     PRIMARY_BASE_Z,
00007:     AURA_RADIUS,
00008:     USE_HERO_AURA_MESH,
00009:     AURA_DEFORM_SUBDIV_VIEW,
00010:     AURA_DEFORM_SUBDIV_RENDER,
00011:     AURA_DEFORM_FIELD_RADIUS,
00012:     AURA_DEFORM_DISPLACE_MIN,
00013:     AURA_DEFORM_DISPLACE_MAX,
00014:     AURA_DEFORM_DETAIL_MAX,
00015:     AURA_DEFORM_WAVE_HEIGHT_MAX,
00016:     AURA_DEFORM_FIELD_STRENGTH_MAX,
00017:     ENERGY_RING_COUNT,
00018:     RIBBON_COUNT,
00019:     CREATE_VARIANTS,
00020:     VARIANT_COUNT,
00021:     VARIANT_RING_RADIUS,
00022:     VARIANT_SCALE_MIN,
00023:     VARIANT_SCALE_MAX,
00024:     USE_MIST_PARTICLES,
00025:     MIST_PARTICLE_COUNT,
00026:     MIST_SCALE_MIN,
00027:     MIST_SCALE_MAX,
00028:     ATMOSPHERE_CUBE_SIZE,
00029:     FOG_VOLUME_ENABLED,
00030:     FOG_VOLUME_VIEWPORT_VISIBLE,
00031:     FOG_RAMP_LOW_BASE,
00032:     FOG_RAMP_HIGH_BASE,
00033:     PALETTE_LIST,
00034:     PEACE_PALETTE,
00035: )
00036: from materials import (
00037:     build_aura_material,
00038:     build_ring_material,
00039:     build_ribbon_material,
00040:     build_variant_material,
00041:     build_atmosphere_volume_material,
00042:     build_mist_particle_material,
00043: )
00044: from asset_setup import duplicate_hierarchy, assign_material_to_hierarchy
00045: from scene_utils import create_controller_empty
00046: from fog_filaments import ensure_fog_filaments
00047: 
00048: 
00049: AURA_AUDIO_PROPS = [
00050:     "low",
00051:     "mid",
00052:     "high",
00053:     "onset",
00054:     "beat",
00055:     "pulse",
00056:     "aura_deform",
00057:     "detail",
00058:     "phase",
00059: ]
00060: 
00061: 
00062: def init_audio_props(obj):
00063:     for prop in AURA_AUDIO_PROPS:
00064:         obj[prop] = 0.0
00065:         try:
00066:             obj.id_properties_ui(prop).update(min=0.0, max=1.0)
00067:         except Exception:
00068:             pass
00069: 
00070: 
00071: def add_prop_driver(idblock, data_path, expression, prop_targets):
00072:     try:
00073:         fcurve = idblock.driver_add(data_path)
00074:     except Exception as exc:
00075:         print(f"[WARN] Driver non creato per {data_path}: {exc}")
00076:         return None
00077: 
00078:     driver = fcurve.driver
00079:     driver.type = 'SCRIPTED'
00080:     driver.expression = expression
00081: 
00082:     while driver.variables:
00083:         driver.variables.remove(driver.variables[0])
00084: 
00085:     for var_name, target_obj, prop_name in prop_targets:
00086:         var = driver.variables.new()
00087:         var.name = var_name
00088:         target = var.targets[0]
00089:         target.id_type = 'OBJECT'
00090:         target.id = target_obj
00091:         target.data_path = f'["{prop_name}"]'
00092: 
00093:     return fcurve
00094: 
00095: 
00096: def create_aura_deform_field(controller, aura_location, parent=None):
00097:     bpy.ops.mesh.primitive_uv_sphere_add(
00098:         segments=24,
00099:         ring_count=12,
00100:         radius=AURA_DEFORM_FIELD_RADIUS,
00101:         location=aura_location,
00102:     )
00103:     field = bpy.context.active_object
00104:     field.name = "AuraAudioDeformField"
00105:     field.display_type = 'WIRE'
00106:     field.hide_render = True
00107:     field.hide_viewport = True
00108:     field.hide_select = True
00109: 
00110:     if parent is not None:
00111:         field.parent = parent
00112: 
00113:     try:
00114:         field.data.name = "AuraAudioDeformFieldMesh"
00115:     except Exception:
00116:         pass
00117: 
00118:     tex = bpy.data.textures.new("AuraAudioDeformFieldTexture", type='CLOUDS')
00119:     for attr, value in [
00120:         ("noise_scale", 0.92),
00121:         ("noise_depth", 5),
00122:         ("contrast", 3.2),
00123:     ]:
00124:         try:
00125:             setattr(tex, attr, value)
00126:         except Exception:
00127:             pass
00128: 
00129:     mod = field.modifiers.new("AudioFieldInvisibleDisplace", 'DISPLACE')
00130:     mod.strength = 0.0
00131:     mod.mid_level = 0.50
00132:     mod.texture = tex
00133: 
00134:     add_prop_driver(
00135:         mod,
00136:         "strength",
00137:         f"aura * {AURA_DEFORM_FIELD_STRENGTH_MAX:.6f}",
00138:         [("aura", controller, "aura_deform")],
00139:     )
00140: 
00141:     return field, mod, tex
00142: 
00143: 
00144: def add_hero_aura_deformers(aura, controller, deform_field):
00145:     try:
00146:         bpy.ops.object.shade_smooth()
00147:     except Exception:
00148:         pass
00149: 
00150:     subdiv = aura.modifiers.new("AuraAudioSubdivision", 'SUBSURF')
00151:     subdiv.levels = AURA_DEFORM_SUBDIV_VIEW
00152:     subdiv.render_levels = AURA_DEFORM_SUBDIV_RENDER
00153: 
00154:     breath_tex = bpy.data.textures.new("AuraBreathDisplaceTexture", type='VORONOI')
00155:     for attr, value in [
00156:         ("noise_scale", 1.85),
00157:         ("intensity", 0.42),
00158:         ("contrast", 2.8),
00159:     ]:
00160:         try:
00161:             setattr(breath_tex, attr, value)
00162:         except Exception:
00163:             pass
00164: 
00165:     breath = aura.modifiers.new("AuraAudioBreathDisplace", 'DISPLACE')
00166:     breath.strength = AURA_DEFORM_DISPLACE_MIN
00167:     breath.mid_level = 0.48
00168:     breath.texture = breath_tex
00169:     try:
00170:         breath.direction = 'NORMAL'
00171:         breath.texture_coords = 'OBJECT'
00172:         breath.texture_coords_object = deform_field
00173:     except Exception:
00174:         pass
00175: 
00176:     add_prop_driver(
00177:         breath,
00178:         "strength",
00179:         f"{AURA_DEFORM_DISPLACE_MIN:.6f} + aura * {(AURA_DEFORM_DISPLACE_MAX - AURA_DEFORM_DISPLACE_MIN):.6f}",
00180:         [("aura", controller, "aura_deform")],
00181:     )
00182: 
00183:     detail_tex = bpy.data.textures.new("AuraTransientDetailTexture", type='CLOUDS')
00184:     for attr, value in [
00185:         ("noise_scale", 0.54),
00186:         ("noise_depth", 6),
00187:         ("contrast", 4.0),
00188:     ]:
00189:         try:
00190:             setattr(detail_tex, attr, value)
00191:         except Exception:
00192:             pass
00193: 
00194:     detail = aura.modifiers.new("AuraAudioTransientDetail", 'DISPLACE')
00195:     detail.strength = 0.0
00196:     detail.mid_level = 0.50
00197:     detail.texture = detail_tex
00198:     try:
00199:         detail.direction = 'NORMAL'
00200:         detail.texture_coords = 'OBJECT'
00201:         detail.texture_coords_object = deform_field
00202:     except Exception:
00203:         pass
00204: 
00205:     add_prop_driver(
00206:         detail,
00207:         "strength",
00208:         f"detail * {AURA_DEFORM_DETAIL_MAX:.6f}",
00209:         [("detail", controller, "detail")],
00210:     )
00211: 
00212:     wave = aura.modifiers.new("AuraAudioBeatWave", 'WAVE')
00213:     try:
00214:         wave.type = 'RINGS'
00215:         wave.use_x = True
00216:         wave.use_y = True
00217:         wave.use_normal = True
00218:         wave.width = 1.10
00219:         wave.narrowness = 1.85
00220:         wave.speed = 0.28
00221:         wave.height = 0.0
00222:         wave.start_position_object = deform_field
00223:     except Exception:
00224:         pass
00225: 
00226:     add_prop_driver(
00227:         wave,
00228:         "height",
00229:         f"pulse * {AURA_DEFORM_WAVE_HEIGHT_MAX:.6f}",
00230:         [("pulse", controller, "pulse")],
00231:     )
00232:     add_prop_driver(
00233:         wave,
00234:         "time_offset",
00235:         "-phase * 3.0",
00236:         [("phase", controller, "phase")],
00237:     )
00238: 
00239:     return {
00240:         "subdivision": subdiv,
00241:         "breath_modifier": breath,
00242:         "breath_texture": breath_tex,
00243:         "detail_modifier": detail,
00244:         "detail_texture": detail_tex,
00245:         "wave_modifier": wave,
00246:     }
00247: 
00248: 
00249: def create_hero_aura(parent=None):
00250:     aura_location = (0, 0, PRIMARY_BASE_Z + 0.95)
00251: 
00252:     if not USE_HERO_AURA_MESH:
00253:         proxy = create_controller_empty(
00254:             "HeroAuraProxy",
00255:             location=aura_location,
00256:             parent=parent,
00257:             display_size=0.30,
00258:             hide_view=True,
00259:         )
00260:         audio_controller = create_controller_empty(
00261:             "AuraAudioSampler",
00262:             location=aura_location,
00263:             parent=parent,
00264:             display_size=0.38,
00265:             hide_view=True,
00266:         )
00267:         init_audio_props(audio_controller)
00268: 
00269:         return {
00270:             "object": proxy,
00271:             "material": None,
00272:             "strength_socket": None,
00273:             "edge_ctrl": None,
00274:             "audio_controller": audio_controller,
00275:             "deform_field": None,
00276:             "field_modifier": None,
00277:             "field_texture": None,
00278:             "deformers": {},
00279:             "audio_props": AURA_AUDIO_PROPS,
00280:         }
00281: 
00282:     mat, aura_strength_socket, aura_edge_ctrl = build_aura_material()
00283: 
00284:     bpy.ops.mesh.primitive_uv_sphere_add(
00285:         radius=AURA_RADIUS,
00286:         location=aura_location
00287:     )
00288:     aura = bpy.context.active_object
00289:     aura.name = "HeroAura"
00290:     aura.data.materials.append(mat)
00291: 
00292:     if parent is not None:
00293:         aura.parent = parent
00294: 
00295:     audio_controller = create_controller_empty(
00296:         "AuraAudioSampler",
00297:         location=aura_location,
00298:         parent=parent,
00299:         display_size=0.38,
00300:         hide_view=True,
00301:     )
00302:     init_audio_props(audio_controller)
00303: 
00304:     deform_field, field_modifier, field_texture = create_aura_deform_field(
00305:         audio_controller,
00306:         aura_location,
00307:         parent=parent,
00308:     )
00309:     deformers = add_hero_aura_deformers(aura, audio_controller, deform_field)
00310: 
00311:     return {
00312:         "object": aura,
00313:         "material": mat,
00314:         "strength_socket": aura_strength_socket,
00315:         "edge_ctrl": aura_edge_ctrl,
00316:         "audio_controller": audio_controller,
00317:         "deform_field": deform_field,
00318:         "field_modifier": field_modifier,
00319:         "field_texture": field_texture,
00320:         "deformers": deformers,
00321:         "audio_props": AURA_AUDIO_PROPS,
00322:     }
00323: 
00324: 
00325: def create_energy_rings(parent=None):
00326:     rings = []
00327: 
00328:     for i in range(ENERGY_RING_COUNT):
00329:         bpy.ops.mesh.primitive_torus_add(
00330:             major_radius=2.90 + i * 0.70,
00331:             minor_radius=0.014 + i * 0.006,
00332:             location=(0, 0, PRIMARY_BASE_Z + 1.10 + i * 0.16),
00333:             rotation=(
00334:                 math.radians(82 + i * 8),
00335:                 math.radians(10 + i * 10),
00336:                 math.radians(i * 20),
00337:             )
00338:         )
00339:         ring = bpy.context.active_object
00340:         ring.name = f"EnergyRing_{i:02d}"
00341: 
00342:         color = PALETTE_LIST[(i + 1) % len(PALETTE_LIST)]
00343:         mat, emit_socket = build_ring_material(f"EnergyRingMat_{i:02d}", color)
00344:         ring.data.materials.append(mat)
00345: 
00346:         if parent is not None:
```
