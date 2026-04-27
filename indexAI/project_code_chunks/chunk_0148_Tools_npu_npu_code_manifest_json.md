# Project Code Chunk 148/212

- File: `Tools/npu/npu_code_manifest.json`
- Part: `1`
- Lines: `1-383`

## Content
```json
00001: {
00002:   "created_at": "2026-04-27T14:41:26",
00003:   "root": "C:\\Users\\carmi\\blender\\blender-audio-project",
00004:   "script_dir": "C:\\Users\\carmi\\blender\\blender-audio-project\\Scripting\\v61b",
00005:   "long_context": {
00006:     "mode": "file_line_chunks",
00007:     "chunk_dir": "Tools/npu/npu_code_chunks",
00008:     "max_chunk_chars": 10500,
00009:     "chunk_count": 100,
00010:     "index": "Tools/npu/npu_code_index.md"
00011:   },
00012:   "files": [
00013:     {
00014:       "file": "analyze_wav.py",
00015:       "exists": true,
00016:       "suffix": ".py",
00017:       "lines": 258,
00018:       "chars": 10299,
00019:       "sha256": "f32673c8b1b1da5df82885235ad6be93a15ca36eb2adb924dac73a4e5a3c8ff8",
00020:       "symbols": {
00021:         "imports": [
00022:           "argparse",
00023:           "json",
00024:           "sys",
00025:           "from pathlib import Path",
00026:           "librosa",
00027:           "numpy",
00028:           "matplotlib.pyplot"
00029:         ],
00030:         "functions": [
00031:           {
00032:             "name": "moving_average",
00033:             "line": 11,
00034:             "args": [
00035:               "x",
00036:               "window"
00037:             ],
00038:             "async": false
00039:           },
00040:           {
00041:             "name": "robust_normalize",
00042:             "line": 18,
00043:             "args": [
00044:               "x",
00045:               "floor_percentile",
00046:               "ceil_percentile"
00047:             ],
00048:             "async": false
00049:           },
00050:           {
00051:             "name": "compress_curve",
00052:             "line": 27,
00053:             "args": [
00054:               "x",
00055:               "gamma"
00056:             ],
00057:             "async": false
00058:           },
00059:           {
00060:             "name": "band_envelope_from_stft",
00061:             "line": 32,
00062:             "args": [
00063:               "S_mag",
00064:               "freqs",
00065:               "fmin",
00066:               "fmax"
00067:             ],
00068:             "async": false
00069:           },
00070:           {
00071:             "name": "resample_to_fps",
00072:             "line": 48,
00073:             "args": [
00074:               "times",
00075:               "values",
00076:               "fps",
00077:               "duration"
00078:             ],
00079:             "async": false
00080:           },
00081:           {
00082:             "name": "build_music_context_if_available",
00083:             "line": 54,
00084:             "args": [
00085:               "json_path",
00086:               "output_dir",
00087:               "run_ollama",
00088:               "ollama_model"
00089:             ],
00090:             "async": false
00091:           },
00092:           {
00093:             "name": "build_ai_memory_context_if_available",
00094:             "line": 92,
00095:             "args": [
00096:               "track_stem",
00097:               "output_dir"
00098:             ],
00099:             "async": false
00100:           },
00101:           {
00102:             "name": "main",
00103:             "line": 106,
00104:             "args": [],
00105:             "async": false
00106:           }
00107:         ],
00108:         "classes": [],
00109:         "assignments": []
00110:       }
00111:     },
00112:     {
00113:       "file": "build_track_summary.py",
00114:       "exists": true,
00115:       "suffix": ".py",
00116:       "lines": 114,
00117:       "chars": 4062,
00118:       "sha256": "7dfbac89818d9b1903ae6828e502ec8b9965c84ce6097a5e049e551c95d3286a",
00119:       "symbols": {
00120:         "imports": [
00121:           "from pathlib import Path",
00122:           "argparse",
00123:           "json",
00124:           "sys",
00125:           "from statistics import mean"
00126:         ],
00127:         "functions": [
00128:           {
00129:             "name": "avg_top",
00130:             "line": 15,
00131:             "args": [
00132:               "values",
00133:               "ratio"
00134:             ],
00135:             "async": false
00136:           },
00137:           {
00138:             "name": "safe_mean",
00139:             "line": 22,
00140:             "args": [
00141:               "values"
00142:             ],
00143:             "async": false
00144:           },
00145:           {
00146:             "name": "build_summary",
00147:             "line": 26,
00148:             "args": [
00149:               "analysis_json",
00150:               "out_json",
00151:               "update_music_context"
00152:             ],
00153:             "async": false
00154:           },
00155:           {
00156:             "name": "main",
00157:             "line": 98,
00158:             "args": [],
00159:             "async": false
00160:           }
00161:         ],
00162:         "classes": [],
00163:         "assignments": [
00164:           "ROOT",
00165:           "PROJECT_DIR",
00166:           "OUTPUT_DIR",
00167:           "ANALYSIS_JSON",
00168:           "OUT_JSON"
00169:         ]
00170:       }
00171:     },
00172:     {
00173:       "file": "normalize_scene_spec.py",
00174:       "exists": true,
00175:       "suffix": ".py",
00176:       "lines": 488,
00177:       "chars": 14873,
00178:       "sha256": "e85a233bd5b31b27296f4bf5b761a0bc5b33bdce66aecc4f80dbf1d305f21b12",
00179:       "symbols": {
00180:         "imports": [
00181:           "from pathlib import Path",
00182:           "json",
00183:           "re",
00184:           "sys"
00185:         ],
00186:         "functions": [
00187:           {
00188:             "name": "load_json",
00189:             "line": 41,
00190:             "args": [
00191:               "path"
00192:             ],
00193:             "async": false
00194:           },
00195:           {
00196:             "name": "slugify",
00197:             "line": 48,
00198:             "args": [
00199:               "text"
00200:             ],
00201:             "async": false
00202:           },
00203:           {
00204:             "name": "safe_scene_name",
00205:             "line": 55,
00206:             "args": [
00207:               "name"
00208:             ],
00209:             "async": false
00210:           },
00211:           {
00212:             "name": "safe_visual_concept",
00213:             "line": 64,
00214:             "args": [
00215:               "text"
00216:             ],
00217:             "async": false
00218:           },
00219:           {
00220:             "name": "normalize_palette",
00221:             "line": 73,
00222:             "args": [
00223:               "values"
00224:             ],
00225:             "async": false
00226:           },
00227:           {
00228:             "name": "normalize_camera_style",
00229:             "line": 93,
00230:             "args": [
00231:               "camera_style"
00232:             ],
00233:             "async": false
00234:           },
00235:           {
00236:             "name": "build_object_specs",
00237:             "line": 123,
00238:             "args": [
00239:               "brief"
00240:             ],
00241:             "async": false
00242:           },
00243:           {
00244:             "name": "build_materials",
00245:             "line": 200,
00246:             "args": [
00247:               "brief"
00248:             ],
00249:             "async": false
00250:           },
00251:           {
00252:             "name": "build_node_animation",
00253:             "line": 275,
00254:             "args": [
00255:               "brief"
00256:             ],
00257:             "async": false
00258:           },
00259:           {
00260:             "name": "build_audio_mapping",
00261:             "line": 329,
00262:             "args": [
00263:               "brief"
00264:             ],
00265:             "async": false
00266:           },
00267:           {
00268:             "name": "build_optimization",
00269:             "line": 376,
00270:             "args": [],
00271:             "async": false
00272:           },
00273:           {
00274:             "name": "build_render_strategy",
00275:             "line": 393,
00276:             "args": [],
00277:             "async": false
00278:           },
00279:           {
00280:             "name": "normalize_brief",
00281:             "line": 401,
00282:             "args": [
00283:               "brief"
00284:             ],
00285:             "async": false
00286:           },
00287:           {
00288:             "name": "safe_scene_name",
00289:             "line": 436,
00290:             "args": [
00291:               "name"
00292:             ],
00293:             "async": false
00294:           },
00295:           {
00296:             "name": "safe_visual_concept",
00297:             "line": 445,
00298:             "args": [
00299:               "text"
00300:             ],
00301:             "async": false
00302:           },
00303:           {
00304:             "name": "main",
00305:             "line": 454,
00306:             "args": [],
00307:             "async": false
00308:           }
00309:         ],
00310:         "classes": [],
00311:         "assignments": [
00312:           "ROOT",
00313:           "PROJECT_DIR",
00314:           "IN_JSON",
00315:           "OUT_JSON",
00316:           "DEFAULT_SCENE_NAME",
00317:           "DEFAULT_VISUAL_CONCEPT",
00318:           "PALETTE_MAP",
00319:           "CAMERA_PRESETS"
00320:         ]
00321:       }
00322:     },
00323:     {
00324:       "file": "Tools/npu/npu_runtime.py",
00325:       "exists": true,
00326:       "suffix": ".py",
00327:       "lines": 96,
00328:       "chars": 3199,
00329:       "sha256": "8e0b1328626cb202c8f7a47bcf159df0725c7370a631440ce11989cca5be58bb",
00330:       "symbols": {
00331:         "imports": [
00332:           "from __future__ import annotations",
00333:           "from pathlib import Path",
00334:           "json",
00335:           "subprocess"
00336:         ],
00337:         "functions": [
00338:           {
00339:             "name": "_run_python",
00340:             "line": 13,
00341:             "args": [
00342:               "python_exe",
00343:               "code",
00344:               "timeout"
00345:             ],
00346:             "async": false
00347:           },
00348:           {
00349:             "name": "npu_preflight",
00350:             "line": 31,
00351:             "args": [
00352:               "python_exe",
00353:               "model_dir"
00354:             ],
00355:             "async": false
00356:           },
00357:           {
00358:             "name": "write_npu_preflight_report",
00359:             "line": 93,
00360:             "args": [
00361:               "report",
00362:               "out_path"
00363:             ],
00364:             "async": false
00365:           }
00366:         ],
00367:         "classes": [],
00368:         "assignments": [
00369:           "ROOT",
00370:           "DEFAULT_NPU_PYTHON",
00371:           "DEFAULT_MODEL_DIR"
00372:         ]
00373:       }
00374:     },
00375:     {
00376:       "file": "Tools/npu/ollama_runtime.py",
00377:       "exists": true,
00378:       "suffix": ".py",
00379:       "lines": 352,
00380:       "chars": 11053,
00381:       "sha256": "dbcdde9d1d43964bd77a64a8cfe8e900346aa4b5554e41daf19758269cbd4cbd",
00382:       "symbols": {
00383:         "imports": [
```
