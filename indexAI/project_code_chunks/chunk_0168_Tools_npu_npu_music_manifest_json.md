# Project Code Chunk 168/212

- File: `Tools/npu/npu_music_manifest.json`
- Part: `1`
- Lines: `1-305`

## Content
```json
00001: {
00002:   "created_at": "2026-04-27T14:37:27",
00003:   "root": "C:\\Users\\carmi\\blender\\blender-audio-project",
00004:   "analysis_json": "output/Ready To Jazz-Luca Vera_Master_analysis.json",
00005:   "blender_keyframes_json": "output/Ready To Jazz-Luca Vera_Master_analysis_blender_keyframes.json",
00006:   "analysis_ai_context_json": "output/Ready To Jazz-Luca Vera_Master_analysis_ai_context.json",
00007:   "track_summary_json": "output/Ready To Jazz-Luca Vera_Master_track_summary.json",
00008:   "compact_json": "output/Ready To Jazz-Luca Vera_Master_music_context.json",
00009:   "ai_memory_context": {
00010:     "format": "SPAZIOTEMPO_AI_MEMORY_CONTEXT_V1",
00011:     "track_stem": "Ready To Jazz-Luca Vera_Master",
00012:     "scene_brief_json": "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\Ready To Jazz-Luca Vera_Master_scene_brief.json",
00013:     "asset_inventory_json": "C:\\Users\\carmi\\blender\\blender-audio-project\\output\\spaziotempo_asset_inventory.json",
00014:     "has_scene_brief": false,
00015:     "scene_preferences": {},
00016:     "conversation_memory": {},
00017:     "recent_user_requests": [],
00018:     "durable_constraints": [],
00019:     "asset_memory": {
00020:       "asset_count": 5,
00021:       "primary_assets": [
00022:         {
00023:           "role": "primary_ball_asset",
00024:           "name": "ball",
00025:           "path": "C:\\Users\\carmi\\blender\\assets\\ball\\source\\ball.fbx",
00026:           "type": ".fbx"
00027:         },
00028:         {
00029:           "role": "animated_effect_asset",
00030:           "name": "Animated effect",
00031:           "path": "C:\\Users\\carmi\\blender\\assets\\animated-effect\\source\\Animated effect.blend",
00032:           "type": ".blend"
00033:         },
00034:         {
00035:           "role": "blend_scene_reference",
00036:           "name": "First good",
00037:           "path": "C:\\Users\\carmi\\blender\\First good.blend",
00038:           "type": ".blend"
00039:         },
00040:         {
00041:           "role": "blend_scene_reference",
00042:           "name": "second good",
00043:           "path": "C:\\Users\\carmi\\blender\\second good.blend",
00044:           "type": ".blend"
00045:         }
00046:       ],
00047:       "notes": [
00048:         "Use primary_ball_asset as known existing ball/hero asset when the scene director asks for ball or dual focus.",
00049:         "Do not assume imported .blend files are available inside the current Blender scene; import/link explicitly in generated scripts."
00050:       ]
00051:     },
00052:     "project_awareness": {},
00053:     "operating_rules": [
00054:       "Use this memory as interpretation context for AI outputs, never to alter numeric audio analysis.",
00055:       "Respect user corrections over generic defaults.",
00056:       "If the user mentions ball, prefer asset role primary_ball_asset.",
00057:       "Full analysis_blender_keyframes frames must remain complete and authoritative.",
00058:       "For two central ball objects, use counterphase animation and inverted audio mapping.",
00059:       "Do not suggest manual Blender/audio import steps already handled by the project pipeline."
00060:     ]
00061:   },
00062:   "context_md": "Tools/npu/npu_music_context.md",
00063:   "chunk_dir": "Tools/npu/npu_music_chunks",
00064:   "chunk_count": 28,
00065:   "segment_seconds": 16.0,
00066:   "segment_count": 22,
00067:   "scene_files": [
00068:     {
00069:       "file": "scene_spec_album_driven.json",
00070:       "chars": 1775,
00071:       "lines": 76,
00072:       "sha256": "4c65268928e2562850baa27cc07d6081babcd9f1dea0e32016467b5828155baf",
00073:       "summary": {
00074:         "file": "scene_spec_album_driven.json",
00075:         "type": "json",
00076:         "keys": [
00077:           "audio_mapping",
00078:           "camera_style",
00079:           "environment",
00080:           "hero_object",
00081:           "lighting_style",
00082:           "objects",
00083:           "palette",
00084:           "scene_name",
00085:           "style_mode",
00086:           "visual_concept"
00087:         ],
00088:         "scene_name": ". .",
00089:         "visual_concept": ".",
00090:         "style_mode": "stylized_cinematic_abstract",
00091:         "environment": "reflective_void_stage",
00092:         "lighting_style": "soft_volumetric_glow",
00093:         "palette": [
00094:           "deep_blue",
00095:           "muted_gold",
00096:           "soft_white",
00097:           "soft_white",
00098:           "midnight_black"
00099:         ],
00100:         "camera": {
00101:           "mood": "intimate",
00102:           "movement": "gentle_push",
00103:           "lens": 100,
00104:           "angle_bias": "slightly_top"
00105:         },
00106:         "objects_count": 3,
00107:         "materials_count": 0,
00108:         "audio_mapping_count": 6,
00109:         "node_animation_count": 0,
00110:         "object_names": [
00111:           "reflective_void_stage",
00112:           "luminous_arches",
00113:           "floating_centerpiece"
00114:         ],
00115:         "audio_targets": [
00116:           "reflective_void_stage:intensity:low",
00117:           "reflective_void_stage:intensity:mid",
00118:           "reflective_void_stage:intensity:high",
00119:           "floating_centerpiece:intensity:low",
00120:           "floating_centerpiece:intensity:mid",
00121:           "floating_centerpiece:intensity:high"
00122:         ]
00123:       }
00124:     },
00125:     {
00126:       "file": "scene_spec_album_driven_normalized.json",
00127:       "chars": 7341,
00128:       "lines": 325,
00129:       "sha256": "ad7b9afbf649af9a06f1c1dae92c685d2982e9be24a648944c4c818627d95dc7",
00130:       "summary": {
00131:         "file": "scene_spec_album_driven_normalized.json",
00132:         "type": "json",
00133:         "keys": [
00134:           "audio_mapping",
00135:           "camera_style",
00136:           "environment",
00137:           "hero_object",
00138:           "lighting_style",
00139:           "materials",
00140:           "node_animation",
00141:           "objects",
00142:           "optimization",
00143:           "palette",
00144:           "render_strategy",
00145:           "scene_name",
00146:           "style_mode",
00147:           "visual_concept"
00148:         ],
00149:         "scene_name": ". .",
00150:         "visual_concept": "Cinematic abstract soul architecture",
00151:         "style_mode": "stylized_cinematic_abstract",
00152:         "environment": "reflective_void_stage",
00153:         "lighting_style": "soft_volumetric_glow",
00154:         "palette": [
00155:           "#1F3A5F",
00156:           "#B08D57",
00157:           "#F2F0E8",
00158:           "#0B0D12"
00159:         ],
00160:         "camera": {
00161:           "mood": "intimate",
00162:           "movement": "gentle_push",
00163:           "lens": 65.0,
00164:           "angle_bias": "slightly_top",
00165:           "location": [
00166:             0.0,
00167:             -9.2,
00168:             3.4
00169:           ],
00170:           "rotation_degrees": [
00171:             72.0,
00172:             0.0,
00173:             0.0
00174:           ]
00175:         },
00176:         "objects_count": 5,
00177:         "materials_count": 5,
00178:         "audio_mapping_count": 6,
00179:         "node_animation_count": 7,
00180:         "object_names": [
00181:           "hero_core",
00182:           "light_architecture",
00183:           "reflective_floor",
00184:           "floating_lights",
00185:           "volumetric_shell"
00186:         ],
00187:         "audio_targets": [
00188:           "hero_core:scale:low",
00189:           "hero_core:rotation:mid",
00190:           "light_architecture:rotation:mid",
00191:           "light_architecture:emission:high",
00192:           "floating_lights:intensity:high",
00193:           "camera:pulse:beat"
00194:         ]
00195:       }
00196:     },
00197:     {
00198:       "file": "scene_spec_album_driven_raw.txt",
00199:       "chars": 1319,
00200:       "lines": 1,
00201:       "sha256": "661f73c43add339a50e542f7e65c23199a29b167163a1453edbc7114b2819f7e",
00202:       "summary": {
00203:         "file": "scene_spec_album_driven_raw.txt",
00204:         "type": "text",
00205:         "chars": 1319,
00206:         "lines": 1
00207:       }
00208:     },
00209:     {
00210:       "file": "scene_spec_from_npu.json",
00211:       "chars": 993,
00212:       "lines": 65,
00213:       "sha256": "c4f28325c5249aa6f434707884d3d97766f45d7768d0e067f649253ad26baf69",
00214:       "summary": {
00215:         "file": "scene_spec_from_npu.json",
00216:         "type": "json",
00217:         "keys": [
00218:           "audio_mapping",
00219:           "camera",
00220:           "objects",
00221:           "palette",
00222:           "scene_name"
00223:         ],
00224:         "scene_name": ".",
00225:         "visual_concept": null,
00226:         "style_mode": null,
00227:         "environment": null,
00228:         "lighting_style": null,
00229:         "palette": [
00230:           "#20354D",
00231:           "#38215A",
00232:           "#4D2A37"
00233:         ],
00234:         "camera": {
00235:           "location": [
00236:             16,
00237:             16,
00238:             16
00239:           ],
00240:           "rotation": [
00241:             0,
00242:             540,
00243:             360
00244:           ],
00245:           "lens": 455
00246:         },
00247:         "objects_count": 2,
00248:         "materials_count": 0,
00249:         "audio_mapping_count": 4,
00250:         "node_animation_count": 0,
00251:         "object_names": [
00252:           "central_sphere",
00253:           "."
00254:         ],
00255:         "audio_targets": [
00256:           "central_sphere:material_select:beat",
00257:           "light_cobinates_ring:strength:beat",
00258:           "central_sphere:material_shader:beat",
00259:           "light_cobinates_ring:strength:beat"
00260:         ]
00261:       }
00262:     },
00263:     {
00264:       "file": "scene_spec_from_npu_raw.txt",
00265:       "chars": 1014,
00266:       "lines": 53,
00267:       "sha256": "dfcc73cfd7b3c1a0e1cc79f68cc0c31e0c30a8f7243bb160bfe2dcba04addc5a",
00268:       "summary": {
00269:         "file": "scene_spec_from_npu_raw.txt",
00270:         "type": "text",
00271:         "chars": 1014,
00272:         "lines": 53
00273:       }
00274:     }
00275:   ],
00276:   "chunks": [
00277:     {
00278:       "index": 1,
00279:       "kind": "overview",
00280:       "path": "Tools/npu/npu_music_chunks/chunk_001_music_overview.md",
00281:       "chars": 14368,
00282:       "sha256": "2522f089dd0796c6a72d946ce09856e69ae520aef53dfff6d9b967cb56392d31"
00283:     },
00284:     {
00285:       "index": 2,
00286:       "kind": "audio_segment",
00287:       "segment_index": 1,
00288:       "start_sec": 0.0,
00289:       "end_sec": 16.0,
00290:       "path": "Tools/npu/npu_music_chunks/chunk_002_audio_segment_001.md",
00291:       "chars": 5722,
00292:       "sha256": "76779e234ef3a6442b0f1823061bd133e6c172c008f4433c357e2107abf5dc7e"
00293:     },
00294:     {
00295:       "index": 3,
00296:       "kind": "audio_segment",
00297:       "segment_index": 2,
00298:       "start_sec": 16.0,
00299:       "end_sec": 32.0,
00300:       "path": "Tools/npu/npu_music_chunks/chunk_003_audio_segment_002.md",
00301:       "chars": 5834,
00302:       "sha256": "2b2401be5412b9156a3324021b3da0164f5b3ccfe79a7feafef9aa1e5035391d"
00303:     },
00304:     {
00305:       "index": 4,
```
