# Project Code Chunk 79/212

- File: `Scripting/v61b_backgood/atmosphere_setup.py`
- Part: `1`
- Lines: `1-348`

## Symbol Map
- Imports: `bpy`, `math`, `random`, `from config import PRIMARY_BASE_Z, AURA_RADIUS, USE_HERO_AURA_MESH, AURA_DEFORM_SUBDIV_VIEW, AURA_DEFORM_SUBDIV_RENDER, AURA_DEFORM_FIELD_RADIUS, AURA_DEFORM_DISPLACE_MIN, AURA_DEFORM_DISPLACE_MAX, AURA_DEFORM_DETAIL_MAX, AURA_DEFORM_WAVE_HEIGHT_MAX, AURA_DEFORM_FIELD_STRENGTH_MAX, ENERGY_RING_COUNT, RIBBON_COUNT, CREATE_VARIANTS, VARIANT_COUNT, VARIANT_RING_RADIUS, VARIANT_SCALE_MIN, VARIANT_SCALE_MAX, USE_MIST_PARTICLES, MIST_PARTICLE_COUNT, MIST_SCALE_MIN, MIST_SCALE_MAX, ATMOSPHERE_CUBE_SIZE, FOG_RAMP_LOW_BASE, FOG_RAMP_HIGH_BASE, PALETTE_LIST, PEACE_PALETTE`, `from materials import build_aura_material, build_ring_material, build_ribbon_material, build_variant_material, build_atmosphere_volume_material, build_mist_particle_material`, `from asset_setup import duplicate_hierarchy, assign_material_to_hierarchy`, `from scene_utils import create_controller_empty`
- Functions: `init_audio_props(obj)` line 59; `add_prop_driver(idblock, data_path, expression, prop_targets)` line 68; `create_aura_deform_field(controller, aura_location, parent)` line 93; `add_hero_aura_deformers(aura, controller, deform_field)` line 141; `create_hero_aura(parent)` line 246; `create_energy_rings(parent)` line 322; `create_energy_ribbons(parent)` line 358; `create_variants(hero_root, parent)` line 396; `create_atmosphere_cube()` line 430; `create_mist_particles(parent)` line 491
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
00029:     FOG_RAMP_LOW_BASE,
00030:     FOG_RAMP_HIGH_BASE,
00031:     PALETTE_LIST,
00032:     PEACE_PALETTE,
00033: )
00034: from materials import (
00035:     build_aura_material,
00036:     build_ring_material,
00037:     build_ribbon_material,
00038:     build_variant_material,
00039:     build_atmosphere_volume_material,
00040:     build_mist_particle_material,
00041: )
00042: from asset_setup import duplicate_hierarchy, assign_material_to_hierarchy
00043: from scene_utils import create_controller_empty
00044: 
00045: 
00046: AURA_AUDIO_PROPS = [
00047:     "low",
00048:     "mid",
00049:     "high",
00050:     "onset",
00051:     "beat",
00052:     "pulse",
00053:     "aura_deform",
00054:     "detail",
00055:     "phase",
00056: ]
00057: 
00058: 
00059: def init_audio_props(obj):
00060:     for prop in AURA_AUDIO_PROPS:
00061:         obj[prop] = 0.0
00062:         try:
00063:             obj.id_properties_ui(prop).update(min=0.0, max=1.0)
00064:         except Exception:
00065:             pass
00066: 
00067: 
00068: def add_prop_driver(idblock, data_path, expression, prop_targets):
00069:     try:
00070:         fcurve = idblock.driver_add(data_path)
00071:     except Exception as exc:
00072:         print(f"[WARN] Driver non creato per {data_path}: {exc}")
00073:         return None
00074: 
00075:     driver = fcurve.driver
00076:     driver.type = 'SCRIPTED'
00077:     driver.expression = expression
00078: 
00079:     while driver.variables:
00080:         driver.variables.remove(driver.variables[0])
00081: 
00082:     for var_name, target_obj, prop_name in prop_targets:
00083:         var = driver.variables.new()
00084:         var.name = var_name
00085:         target = var.targets[0]
00086:         target.id_type = 'OBJECT'
00087:         target.id = target_obj
00088:         target.data_path = f'["{prop_name}"]'
00089: 
00090:     return fcurve
00091: 
00092: 
00093: def create_aura_deform_field(controller, aura_location, parent=None):
00094:     bpy.ops.mesh.primitive_uv_sphere_add(
00095:         segments=24,
00096:         ring_count=12,
00097:         radius=AURA_DEFORM_FIELD_RADIUS,
00098:         location=aura_location,
00099:     )
00100:     field = bpy.context.active_object
00101:     field.name = "AuraAudioDeformField"
00102:     field.display_type = 'WIRE'
00103:     field.hide_render = True
00104:     field.hide_viewport = True
00105:     field.hide_select = True
00106: 
00107:     if parent is not None:
00108:         field.parent = parent
00109: 
00110:     try:
00111:         field.data.name = "AuraAudioDeformFieldMesh"
00112:     except Exception:
00113:         pass
00114: 
00115:     tex = bpy.data.textures.new("AuraAudioDeformFieldTexture", type='CLOUDS')
00116:     for attr, value in [
00117:         ("noise_scale", 0.92),
00118:         ("noise_depth", 5),
00119:         ("contrast", 3.2),
00120:     ]:
00121:         try:
00122:             setattr(tex, attr, value)
00123:         except Exception:
00124:             pass
00125: 
00126:     mod = field.modifiers.new("AudioFieldInvisibleDisplace", 'DISPLACE')
00127:     mod.strength = 0.0
00128:     mod.mid_level = 0.50
00129:     mod.texture = tex
00130: 
00131:     add_prop_driver(
00132:         mod,
00133:         "strength",
00134:         f"aura * {AURA_DEFORM_FIELD_STRENGTH_MAX:.6f}",
00135:         [("aura", controller, "aura_deform")],
00136:     )
00137: 
00138:     return field, mod, tex
00139: 
00140: 
00141: def add_hero_aura_deformers(aura, controller, deform_field):
00142:     try:
00143:         bpy.ops.object.shade_smooth()
00144:     except Exception:
00145:         pass
00146: 
00147:     subdiv = aura.modifiers.new("AuraAudioSubdivision", 'SUBSURF')
00148:     subdiv.levels = AURA_DEFORM_SUBDIV_VIEW
00149:     subdiv.render_levels = AURA_DEFORM_SUBDIV_RENDER
00150: 
00151:     breath_tex = bpy.data.textures.new("AuraBreathDisplaceTexture", type='VORONOI')
00152:     for attr, value in [
00153:         ("noise_scale", 1.85),
00154:         ("intensity", 0.42),
00155:         ("contrast", 2.8),
00156:     ]:
00157:         try:
00158:             setattr(breath_tex, attr, value)
00159:         except Exception:
00160:             pass
00161: 
00162:     breath = aura.modifiers.new("AuraAudioBreathDisplace", 'DISPLACE')
00163:     breath.strength = AURA_DEFORM_DISPLACE_MIN
00164:     breath.mid_level = 0.48
00165:     breath.texture = breath_tex
00166:     try:
00167:         breath.direction = 'NORMAL'
00168:         breath.texture_coords = 'OBJECT'
00169:         breath.texture_coords_object = deform_field
00170:     except Exception:
00171:         pass
00172: 
00173:     add_prop_driver(
00174:         breath,
00175:         "strength",
00176:         f"{AURA_DEFORM_DISPLACE_MIN:.6f} + aura * {(AURA_DEFORM_DISPLACE_MAX - AURA_DEFORM_DISPLACE_MIN):.6f}",
00177:         [("aura", controller, "aura_deform")],
00178:     )
00179: 
00180:     detail_tex = bpy.data.textures.new("AuraTransientDetailTexture", type='CLOUDS')
00181:     for attr, value in [
00182:         ("noise_scale", 0.54),
00183:         ("noise_depth", 6),
00184:         ("contrast", 4.0),
00185:     ]:
00186:         try:
00187:             setattr(detail_tex, attr, value)
00188:         except Exception:
00189:             pass
00190: 
00191:     detail = aura.modifiers.new("AuraAudioTransientDetail", 'DISPLACE')
00192:     detail.strength = 0.0
00193:     detail.mid_level = 0.50
00194:     detail.texture = detail_tex
00195:     try:
00196:         detail.direction = 'NORMAL'
00197:         detail.texture_coords = 'OBJECT'
00198:         detail.texture_coords_object = deform_field
00199:     except Exception:
00200:         pass
00201: 
00202:     add_prop_driver(
00203:         detail,
00204:         "strength",
00205:         f"detail * {AURA_DEFORM_DETAIL_MAX:.6f}",
00206:         [("detail", controller, "detail")],
00207:     )
00208: 
00209:     wave = aura.modifiers.new("AuraAudioBeatWave", 'WAVE')
00210:     try:
00211:         wave.type = 'RINGS'
00212:         wave.use_x = True
00213:         wave.use_y = True
00214:         wave.use_normal = True
00215:         wave.width = 1.10
00216:         wave.narrowness = 1.85
00217:         wave.speed = 0.28
00218:         wave.height = 0.0
00219:         wave.start_position_object = deform_field
00220:     except Exception:
00221:         pass
00222: 
00223:     add_prop_driver(
00224:         wave,
00225:         "height",
00226:         f"pulse * {AURA_DEFORM_WAVE_HEIGHT_MAX:.6f}",
00227:         [("pulse", controller, "pulse")],
00228:     )
00229:     add_prop_driver(
00230:         wave,
00231:         "time_offset",
00232:         "-phase * 3.0",
00233:         [("phase", controller, "phase")],
00234:     )
00235: 
00236:     return {
00237:         "subdivision": subdiv,
00238:         "breath_modifier": breath,
00239:         "breath_texture": breath_tex,
00240:         "detail_modifier": detail,
00241:         "detail_texture": detail_tex,
00242:         "wave_modifier": wave,
00243:     }
00244: 
00245: 
00246: def create_hero_aura(parent=None):
00247:     aura_location = (0, 0, PRIMARY_BASE_Z + 0.95)
00248: 
00249:     if not USE_HERO_AURA_MESH:
00250:         proxy = create_controller_empty(
00251:             "HeroAuraProxy",
00252:             location=aura_location,
00253:             parent=parent,
00254:             display_size=0.30,
00255:             hide_view=True,
00256:         )
00257:         audio_controller = create_controller_empty(
00258:             "AuraAudioSampler",
00259:             location=aura_location,
00260:             parent=parent,
00261:             display_size=0.38,
00262:             hide_view=True,
00263:         )
00264:         init_audio_props(audio_controller)
00265: 
00266:         return {
00267:             "object": proxy,
00268:             "material": None,
00269:             "strength_socket": None,
00270:             "edge_ctrl": None,
00271:             "audio_controller": audio_controller,
00272:             "deform_field": None,
00273:             "field_modifier": None,
00274:             "field_texture": None,
00275:             "deformers": {},
00276:             "audio_props": AURA_AUDIO_PROPS,
00277:         }
00278: 
00279:     mat, aura_strength_socket, aura_edge_ctrl = build_aura_material()
00280: 
00281:     bpy.ops.mesh.primitive_uv_sphere_add(
00282:         radius=AURA_RADIUS,
00283:         location=aura_location
00284:     )
00285:     aura = bpy.context.active_object
00286:     aura.name = "HeroAura"
00287:     aura.data.materials.append(mat)
00288: 
00289:     if parent is not None:
00290:         aura.parent = parent
00291: 
00292:     audio_controller = create_controller_empty(
00293:         "AuraAudioSampler",
00294:         location=aura_location,
00295:         parent=parent,
00296:         display_size=0.38,
00297:         hide_view=True,
00298:     )
00299:     init_audio_props(audio_controller)
00300: 
00301:     deform_field, field_modifier, field_texture = create_aura_deform_field(
00302:         audio_controller,
00303:         aura_location,
00304:         parent=parent,
00305:     )
00306:     deformers = add_hero_aura_deformers(aura, audio_controller, deform_field)
00307: 
00308:     return {
00309:         "object": aura,
00310:         "material": mat,
00311:         "strength_socket": aura_strength_socket,
00312:         "edge_ctrl": aura_edge_ctrl,
00313:         "audio_controller": audio_controller,
00314:         "deform_field": deform_field,
00315:         "field_modifier": field_modifier,
00316:         "field_texture": field_texture,
00317:         "deformers": deformers,
00318:         "audio_props": AURA_AUDIO_PROPS,
00319:     }
00320: 
00321: 
00322: def create_energy_rings(parent=None):
00323:     rings = []
00324: 
00325:     for i in range(ENERGY_RING_COUNT):
00326:         bpy.ops.mesh.primitive_torus_add(
00327:             major_radius=2.90 + i * 0.70,
00328:             minor_radius=0.014 + i * 0.006,
00329:             location=(0, 0, PRIMARY_BASE_Z + 1.10 + i * 0.16),
00330:             rotation=(
00331:                 math.radians(82 + i * 8),
00332:                 math.radians(10 + i * 10),
00333:                 math.radians(i * 20),
00334:             )
00335:         )
00336:         ring = bpy.context.active_object
00337:         ring.name = f"EnergyRing_{i:02d}"
00338: 
00339:         color = PALETTE_LIST[(i + 1) % len(PALETTE_LIST)]
00340:         mat, emit_socket = build_ring_material(f"EnergyRingMat_{i:02d}", color)
00341:         ring.data.materials.append(mat)
00342: 
00343:         if parent is not None:
00344:             ring.parent = parent
00345: 
00346:         rings.append({
00347:             "object": ring,
00348:             "emit_socket": emit_socket,
```
