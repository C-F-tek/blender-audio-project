# Project Code Chunk 4/212

- File: `normalize_scene_spec.py`
- Part: `1`
- Lines: `1-315`

## Symbol Map
- Imports: `from pathlib import Path`, `json`, `re`, `sys`
- Functions: `load_json(path)` line 41; `slugify(text)` line 48; `safe_scene_name(name)` line 55; `safe_visual_concept(text)` line 64; `normalize_palette(values)` line 73; `normalize_camera_style(camera_style)` line 93; `build_object_specs(brief)` line 123; `build_materials(brief)` line 200; `build_node_animation(brief)` line 275; `build_audio_mapping(brief)` line 329; `build_optimization()` line 376; `build_render_strategy()` line 393; `normalize_brief(brief)` line 401; `safe_scene_name(name)` line 436; `safe_visual_concept(text)` line 445; `main()` line 454
- Assignments: `ROOT`, `PROJECT_DIR`, `IN_JSON`, `OUT_JSON`, `DEFAULT_SCENE_NAME`, `DEFAULT_VISUAL_CONCEPT`, `PALETTE_MAP`, `CAMERA_PRESETS`

## Content
```py
00001: from pathlib import Path
00002: import json
00003: import re
00004: import sys
00005: 
00006: ROOT = Path.home() / "blender"
00007: PROJECT_DIR = ROOT / "blender-audio-project"
00008: 
00009: IN_JSON = PROJECT_DIR / "scene_spec_album_driven.json"
00010: OUT_JSON = PROJECT_DIR / "scene_spec_album_driven_normalized.json"
00011: 
00012: DEFAULT_SCENE_NAME = "Living Life In Peace - Feel The Light"
00013: DEFAULT_VISUAL_CONCEPT = "Cinematic abstract soul architecture"
00014: 
00015: PALETTE_MAP = {
00016:     "deep_blue": "#1F3A5F",
00017:     "muted_gold": "#B08D57",
00018:     "deep_purple": "#5E3E8C",
00019:     "soft_white": "#F2F0E8",
00020:     "warm_amber": "#C27A3A",
00021:     "dark_teal": "#1E5A63",
00022:     "midnight_black": "#0B0D12"
00023: }
00024: 
00025: CAMERA_PRESETS = {
00026:     "frontal": {
00027:         "location": [0.0, -8.8, 2.4],
00028:         "rotation": [74.0, 0.0, 0.0]
00029:     },
00030:     "slightly_top": {
00031:         "location": [0.0, -9.2, 3.4],
00032:         "rotation": [72.0, 0.0, 0.0]
00033:     },
00034:     "angled_front": {
00035:         "location": [1.2, -8.9, 2.9],
00036:         "rotation": [73.0, 0.0, 7.0]
00037:     }
00038: }
00039: 
00040: 
00041: def load_json(path: Path) -> dict:
00042:     if not path.exists():
00043:         raise FileNotFoundError(f"Scene brief non trovato: {path}")
00044:     with open(path, "r", encoding="utf-8") as f:
00045:         return json.load(f)
00046: 
00047: 
00048: def slugify(text: str) -> str:
00049:     text = str(text).strip().lower()
00050:     text = re.sub(r"[^a-z0-9]+", "_", text)
00051:     text = re.sub(r"_+", "_", text).strip("_")
00052:     return text or "item"
00053: 
00054: 
00055: def safe_scene_name(name: str) -> str:
00056:     if not isinstance(name, str):
00057:         return DEFAULT_SCENE_NAME
00058:     name = name.strip()
00059:     if not name or name == ".":
00060:         return DEFAULT_SCENE_NAME
00061:     return name
00062: 
00063: 
00064: def safe_visual_concept(text: str) -> str:
00065:     if not isinstance(text, str):
00066:         return DEFAULT_VISUAL_CONCEPT
00067:     text = text.strip()
00068:     if not text or text == ".":
00069:         return DEFAULT_VISUAL_CONCEPT
00070:     return text
00071: 
00072: 
00073: def normalize_palette(values):
00074:     if not isinstance(values, list):
00075:         values = []
00076: 
00077:     colors = []
00078:     for v in values:
00079:         if isinstance(v, str) and v in PALETTE_MAP:
00080:             colors.append(PALETTE_MAP[v])
00081: 
00082:     if not colors:
00083:         colors = ["#1F3A5F", "#5E3E8C", "#B08D57", "#F2F0E8"]
00084: 
00085:     dedup = []
00086:     for c in colors:
00087:         if c not in dedup:
00088:             dedup.append(c)
00089: 
00090:     return dedup[:5]
00091: 
00092: 
00093: def normalize_camera_style(camera_style: dict):
00094:     if not isinstance(camera_style, dict):
00095:         camera_style = {}
00096: 
00097:     mood = str(camera_style.get("mood", "cinematic")).strip() or "cinematic"
00098:     movement = str(camera_style.get("movement", "floating_orbit")).strip() or "floating_orbit"
00099:     angle_bias = str(camera_style.get("angle_bias", "slightly_top")).strip() or "slightly_top"
00100: 
00101:     try:
00102:         lens = float(camera_style.get("lens", 50))
00103:     except Exception:
00104:         lens = 50.0
00105: 
00106:     if lens < 20:
00107:         lens = 50.0
00108:     elif lens > 85:
00109:         lens = 65.0
00110: 
00111:     preset = CAMERA_PRESETS.get(angle_bias, CAMERA_PRESETS["slightly_top"])
00112: 
00113:     return {
00114:         "mood": mood,
00115:         "movement": movement,
00116:         "lens": lens,
00117:         "angle_bias": angle_bias,
00118:         "location": preset["location"],
00119:         "rotation_degrees": preset["rotation"]
00120:     }
00121: 
00122: 
00123: def build_object_specs(brief: dict):
00124:     hero_object = brief.get("hero_object", "central_core")
00125:     objects = [
00126:         {
00127:             "type": "hero_core",
00128:             "name": "hero_core",
00129:             "role": "central emotional centerpiece",
00130:             "geometry": {
00131:                 "primitive": "uv_sphere",
00132:                 "location": [0.0, 0.0, 1.15],
00133:                 "rotation": [0.0, 0.0, 0.0],
00134:                 "scale": [1.15, 1.15, 1.15],
00135:                 "subdivisions": 2
00136:             },
00137:             "material": "hero_core_material"
00138:         },
00139:         {
00140:             "type": "light_architecture",
00141:             "name": "light_architecture",
00142:             "role": "surrounding luminous structure",
00143:             "geometry": {
00144:                 "primitive": "instanced_columns_ring",
00145:                 "count": 12,
00146:                 "radius": 4.4,
00147:                 "height": 2.6
00148:             },
00149:             "material": "light_arch_material"
00150:         },
00151:         {
00152:             "type": "reflective_floor",
00153:             "name": "reflective_floor",
00154:             "role": "depth and reflections",
00155:             "geometry": {
00156:                 "primitive": "plane",
00157:                 "location": [0.0, 0.0, 0.0],
00158:                 "rotation": [0.0, 0.0, 0.0],
00159:                 "scale": [14.0, 14.0, 1.0]
00160:             },
00161:             "material": "floor_material"
00162:         },
00163:         {
00164:             "type": "floating_lights",
00165:             "name": "floating_lights",
00166:             "role": "harmonic accents",
00167:             "geometry": {
00168:                 "primitive": "floating_orbs",
00169:                 "count": 4
00170:             },
00171:             "material": "floating_light_material"
00172:         },
00173:         {
00174:             "type": "volumetric_shell",
00175:             "name": "volumetric_shell",
00176:             "role": "atmosphere and cinematic depth",
00177:             "geometry": {
00178:                 "primitive": "cube_volume",
00179:                 "location": [0.0, 0.0, 3.0],
00180:                 "rotation": [0.0, 0.0, 0.0],
00181:                 "scale": [9.0, 9.0, 4.5]
00182:             },
00183:             "material": "volume_material"
00184:         }
00185:     ]
00186: 
00187:     if hero_object == "luminous_pillar":
00188:         objects[0]["geometry"]["primitive"] = "cylinder"
00189:         objects[0]["geometry"]["scale"] = [0.8, 0.8, 2.3]
00190:     elif hero_object == "abstract_signal_monolith":
00191:         objects[0]["geometry"]["primitive"] = "cube"
00192:         objects[0]["geometry"]["scale"] = [0.9, 0.9, 2.0]
00193:     elif hero_object == "music_totem":
00194:         objects[0]["geometry"]["primitive"] = "stacked_orb_column"
00195:         objects[0]["geometry"]["scale"] = [1.0, 1.0, 1.8]
00196: 
00197:     return objects
00198: 
00199: 
00200: def build_materials(brief: dict):
00201:     lighting_style = brief.get("lighting_style", "soft_volumetric_glow")
00202: 
00203:     materials = [
00204:         {
00205:             "name": "hero_core_material",
00206:             "target": "hero_core",
00207:             "shader_type": "emission_glass_mix",
00208:             "node_features": ["noise", "color_ramp", "fresnel", "mapping_rotation", "mix_shader"],
00209:             "purpose": "hero pulse and emotional focus",
00210:             "defaults": {
00211:                 "emission_strength": 2.2,
00212:                 "noise_scale": 3.0,
00213:                 "fresnel": 0.65,
00214:                 "mix_factor": 0.55
00215:             }
00216:         },
00217:         {
00218:             "name": "light_arch_material",
00219:             "target": "light_architecture",
00220:             "shader_type": "gradient_emission",
00221:             "node_features": ["gradient", "color_ramp", "mapping", "emission"],
00222:             "purpose": "rhythmic luminous architecture",
00223:             "defaults": {
00224:                 "emission_strength": 1.6,
00225:                 "gradient_shift": 0.0,
00226:                 "color_mix": 0.5
00227:             }
00228:         },
00229:         {
00230:             "name": "floor_material",
00231:             "target": "reflective_floor",
00232:             "shader_type": "reflective_principled",
00233:             "node_features": ["noise", "bump", "roughness_variation", "fresnel"],
00234:             "purpose": "depth, reflection and grounding",
00235:             "defaults": {
00236:                 "roughness": 0.24,
00237:                 "bump_strength": 0.08,
00238:                 "metallic": 0.18
00239:             }
00240:         },
00241:         {
00242:             "name": "floating_light_material",
00243:             "target": "floating_lights",
00244:             "shader_type": "soft_emission",
00245:             "node_features": ["emission", "noise", "color_variation"],
00246:             "purpose": "harmonic floating accents",
00247:             "defaults": {
00248:                 "emission_strength": 1.5,
00249:                 "noise_scale": 4.0
00250:             }
00251:         },
00252:         {
00253:             "name": "volume_material",
00254:             "target": "volumetric_shell",
00255:             "shader_type": "principled_volume",
00256:             "node_features": ["volume_density", "anisotropy"],
00257:             "purpose": "cinematic atmosphere",
00258:             "defaults": {
00259:                 "density": 0.015,
00260:                 "anisotropy": 0.20
00261:             }
00262:         }
00263:     ]
00264: 
00265:     if lighting_style == "reflective_low_key_lighting":
00266:         materials[2]["defaults"]["roughness"] = 0.18
00267:         materials[4]["defaults"]["density"] = 0.010
00268:     elif lighting_style == "soulful_color_bloom":
00269:         materials[0]["defaults"]["emission_strength"] = 2.8
00270:         materials[1]["defaults"]["emission_strength"] = 2.2
00271: 
00272:     return materials
00273: 
00274: 
00275: def build_node_animation(brief: dict):
00276:     return [
00277:         {
00278:             "target": "hero_core_material",
00279:             "parameter": "emission_strength",
00280:             "band": "beat",
00281:             "intent": "main musical pulse",
00282:             "strength": 1.0
00283:         },
00284:         {
00285:             "target": "hero_core_material",
00286:             "parameter": "noise_scale",
00287:             "band": "low",
00288:             "intent": "body deformation illusion",
00289:             "strength": 0.65
00290:         },
00291:         {
00292:             "target": "hero_core_material",
00293:             "parameter": "mix_factor",
00294:             "band": "mid",
00295:             "intent": "surface shimmer and motion",
00296:             "strength": 0.45
00297:         },
00298:         {
00299:             "target": "light_arch_material",
00300:             "parameter": "emission_strength",
00301:             "band": "high",
00302:             "intent": "harmonic brightness",
00303:             "strength": 0.80
00304:         },
00305:         {
00306:             "target": "light_arch_material",
00307:             "parameter": "gradient_shift",
00308:             "band": "mid",
00309:             "intent": "circulating light flow",
00310:             "strength": 0.50
00311:         },
00312:         {
00313:             "target": "floor_material",
00314:             "parameter": "roughness",
00315:             "band": "low",
```
