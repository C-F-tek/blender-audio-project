# Project Code Chunk 7/212

- File: `scene_spec_album_driven_normalized.json`
- Part: `1`
- Lines: `1-325`

## Content
```json
00001: {
00002:   "scene_name": ". .",
00003:   "style_mode": "stylized_cinematic_abstract",
00004:   "visual_concept": "Cinematic abstract soul architecture",
00005:   "hero_object": "abstract_signal_monolith",
00006:   "environment": "reflective_void_stage",
00007:   "lighting_style": "soft_volumetric_glow",
00008:   "palette": [
00009:     "#1F3A5F",
00010:     "#B08D57",
00011:     "#F2F0E8",
00012:     "#0B0D12"
00013:   ],
00014:   "camera_style": {
00015:     "mood": "intimate",
00016:     "movement": "gentle_push",
00017:     "lens": 65.0,
00018:     "angle_bias": "slightly_top",
00019:     "location": [
00020:       0.0,
00021:       -9.2,
00022:       3.4
00023:     ],
00024:     "rotation_degrees": [
00025:       72.0,
00026:       0.0,
00027:       0.0
00028:     ]
00029:   },
00030:   "objects": [
00031:     {
00032:       "type": "hero_core",
00033:       "name": "hero_core",
00034:       "role": "central emotional centerpiece",
00035:       "geometry": {
00036:         "primitive": "cube",
00037:         "location": [
00038:           0.0,
00039:           0.0,
00040:           1.15
00041:         ],
00042:         "rotation": [
00043:           0.0,
00044:           0.0,
00045:           0.0
00046:         ],
00047:         "scale": [
00048:           0.9,
00049:           0.9,
00050:           2.0
00051:         ],
00052:         "subdivisions": 2
00053:       },
00054:       "material": "hero_core_material"
00055:     },
00056:     {
00057:       "type": "light_architecture",
00058:       "name": "light_architecture",
00059:       "role": "surrounding luminous structure",
00060:       "geometry": {
00061:         "primitive": "instanced_columns_ring",
00062:         "count": 12,
00063:         "radius": 4.4,
00064:         "height": 2.6
00065:       },
00066:       "material": "light_arch_material"
00067:     },
00068:     {
00069:       "type": "reflective_floor",
00070:       "name": "reflective_floor",
00071:       "role": "depth and reflections",
00072:       "geometry": {
00073:         "primitive": "plane",
00074:         "location": [
00075:           0.0,
00076:           0.0,
00077:           0.0
00078:         ],
00079:         "rotation": [
00080:           0.0,
00081:           0.0,
00082:           0.0
00083:         ],
00084:         "scale": [
00085:           14.0,
00086:           14.0,
00087:           1.0
00088:         ]
00089:       },
00090:       "material": "floor_material"
00091:     },
00092:     {
00093:       "type": "floating_lights",
00094:       "name": "floating_lights",
00095:       "role": "harmonic accents",
00096:       "geometry": {
00097:         "primitive": "floating_orbs",
00098:         "count": 4
00099:       },
00100:       "material": "floating_light_material"
00101:     },
00102:     {
00103:       "type": "volumetric_shell",
00104:       "name": "volumetric_shell",
00105:       "role": "atmosphere and cinematic depth",
00106:       "geometry": {
00107:         "primitive": "cube_volume",
00108:         "location": [
00109:           0.0,
00110:           0.0,
00111:           3.0
00112:         ],
00113:         "rotation": [
00114:           0.0,
00115:           0.0,
00116:           0.0
00117:         ],
00118:         "scale": [
00119:           9.0,
00120:           9.0,
00121:           4.5
00122:         ]
00123:       },
00124:       "material": "volume_material"
00125:     }
00126:   ],
00127:   "materials": [
00128:     {
00129:       "name": "hero_core_material",
00130:       "target": "hero_core",
00131:       "shader_type": "emission_glass_mix",
00132:       "node_features": [
00133:         "noise",
00134:         "color_ramp",
00135:         "fresnel",
00136:         "mapping_rotation",
00137:         "mix_shader"
00138:       ],
00139:       "purpose": "hero pulse and emotional focus",
00140:       "defaults": {
00141:         "emission_strength": 2.2,
00142:         "noise_scale": 3.0,
00143:         "fresnel": 0.65,
00144:         "mix_factor": 0.55
00145:       }
00146:     },
00147:     {
00148:       "name": "light_arch_material",
00149:       "target": "light_architecture",
00150:       "shader_type": "gradient_emission",
00151:       "node_features": [
00152:         "gradient",
00153:         "color_ramp",
00154:         "mapping",
00155:         "emission"
00156:       ],
00157:       "purpose": "rhythmic luminous architecture",
00158:       "defaults": {
00159:         "emission_strength": 1.6,
00160:         "gradient_shift": 0.0,
00161:         "color_mix": 0.5
00162:       }
00163:     },
00164:     {
00165:       "name": "floor_material",
00166:       "target": "reflective_floor",
00167:       "shader_type": "reflective_principled",
00168:       "node_features": [
00169:         "noise",
00170:         "bump",
00171:         "roughness_variation",
00172:         "fresnel"
00173:       ],
00174:       "purpose": "depth, reflection and grounding",
00175:       "defaults": {
00176:         "roughness": 0.24,
00177:         "bump_strength": 0.08,
00178:         "metallic": 0.18
00179:       }
00180:     },
00181:     {
00182:       "name": "floating_light_material",
00183:       "target": "floating_lights",
00184:       "shader_type": "soft_emission",
00185:       "node_features": [
00186:         "emission",
00187:         "noise",
00188:         "color_variation"
00189:       ],
00190:       "purpose": "harmonic floating accents",
00191:       "defaults": {
00192:         "emission_strength": 1.5,
00193:         "noise_scale": 4.0
00194:       }
00195:     },
00196:     {
00197:       "name": "volume_material",
00198:       "target": "volumetric_shell",
00199:       "shader_type": "principled_volume",
00200:       "node_features": [
00201:         "volume_density",
00202:         "anisotropy"
00203:       ],
00204:       "purpose": "cinematic atmosphere",
00205:       "defaults": {
00206:         "density": 0.015,
00207:         "anisotropy": 0.2
00208:       }
00209:     }
00210:   ],
00211:   "node_animation": [
00212:     {
00213:       "target": "hero_core_material",
00214:       "parameter": "emission_strength",
00215:       "band": "beat",
00216:       "intent": "main musical pulse",
00217:       "strength": 1.0
00218:     },
00219:     {
00220:       "target": "hero_core_material",
00221:       "parameter": "noise_scale",
00222:       "band": "low",
00223:       "intent": "body deformation illusion",
00224:       "strength": 0.65
00225:     },
00226:     {
00227:       "target": "hero_core_material",
00228:       "parameter": "mix_factor",
00229:       "band": "mid",
00230:       "intent": "surface shimmer and motion",
00231:       "strength": 0.45
00232:     },
00233:     {
00234:       "target": "light_arch_material",
00235:       "parameter": "emission_strength",
00236:       "band": "high",
00237:       "intent": "harmonic brightness",
00238:       "strength": 0.8
00239:     },
00240:     {
00241:       "target": "light_arch_material",
00242:       "parameter": "gradient_shift",
00243:       "band": "mid",
00244:       "intent": "circulating light flow",
00245:       "strength": 0.5
00246:     },
00247:     {
00248:       "target": "floor_material",
00249:       "parameter": "roughness",
00250:       "band": "low",
00251:       "intent": "subtle reflective breathing",
00252:       "strength": 0.3
00253:     },
00254:     {
00255:       "target": "volume_material",
00256:       "parameter": "density",
00257:       "band": "beat",
00258:       "intent": "volumetric pulse",
00259:       "strength": 0.18
00260:     }
00261:   ],
00262:   "audio_mapping": [
00263:     {
00264:       "target": "hero_core",
00265:       "property": "scale",
00266:       "band": "low",
00267:       "intent": "central body pulse",
00268:       "strength": 0.55
00269:     },
00270:     {
00271:       "target": "hero_core",
00272:       "property": "rotation",
00273:       "band": "mid",
00274:       "intent": "gentle musical sway",
00275:       "strength": 0.25
00276:     },
00277:     {
00278:       "target": "light_architecture",
00279:       "property": "rotation",
00280:       "band": "mid",
00281:       "intent": "architectural motion",
00282:       "strength": 0.4
00283:     },
00284:     {
00285:       "target": "light_architecture",
00286:       "property": "emission",
00287:       "band": "high",
00288:       "intent": "harmonic brightness accents",
00289:       "strength": 0.72
00290:     },
00291:     {
00292:       "target": "floating_lights",
00293:       "property": "intensity",
00294:       "band": "high",
00295:       "intent": "sparkle accents",
00296:       "strength": 0.7
00297:     },
00298:     {
00299:       "target": "camera",
00300:       "property": "pulse",
00301:       "band": "beat",
00302:       "intent": "subtle rhythmic camera bump",
00303:       "strength": 0.28
00304:     }
00305:   ],
00306:   "optimization": {
00307:     "use_instancing": true,
00308:     "use_procedural_materials": true,
00309:     "avoid_heavy_geometry": true,
00310:     "animate_nodes_more_than_meshes": true,
00311:     "geometry_budget": "low_geometry_high_shading",
00312:     "notes": [
00313:       "keep hero object simple",
00314:       "use instanced ring architecture",
00315:       "prefer procedural shading",
00316:       "use one volumetric shell only",
00317:       "avoid subdivision-heavy meshes"
00318:     ]
00319:   },
00320:   "render_strategy": {
00321:     "engine": "BLENDER_EEVEE",
00322:     "priority": "fast iteration with rich shading",
00323:     "notes": "use emission, procedural shaders and moderate volumetrics"
00324:   }
00325: }
```
