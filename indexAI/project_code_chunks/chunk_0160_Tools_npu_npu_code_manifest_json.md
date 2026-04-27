# Project Code Chunk 160/212

- File: `Tools/npu/npu_code_manifest.json`
- Part: `13`
- Lines: `4112-4488`

## Content
```json
04112:             ],
04113:             "async": false
04114:           },
04115:           {
04116:             "name": "classify_object",
04117:             "line": 64,
04118:             "args": [
04119:               "obj"
04120:             ],
04121:             "async": false
04122:           },
04123:           {
04124:             "name": "link_object_to_layer",
04125:             "line": 86,
04126:             "args": [
04127:               "obj",
04128:               "collection"
04129:             ],
04130:             "async": false
04131:           },
04132:           {
04133:             "name": "apply_object_metadata",
04134:             "line": 91,
04135:             "args": [
04136:               "obj",
04137:               "spec"
04138:             ],
04139:             "async": false
04140:           },
04141:           {
04142:             "name": "classify_scene_objects",
04143:             "line": 99,
04144:             "args": [
04145:               "scene",
04146:               "include_reserved"
04147:             ],
04148:             "async": false
04149:           },
04150:           {
04151:             "name": "compact_structure_summary",
04152:             "line": 126,
04153:             "args": [
04154:               "report"
04155:             ],
04156:             "async": false
04157:           }
04158:         ],
04159:         "classes": [],
04160:         "assignments": []
04161:       }
04162:     },
04163:     {
04164:       "file": "Scripting/v61b/spaziotempo/core/registry.py",
04165:       "exists": true,
04166:       "suffix": ".py",
04167:       "lines": 222,
04168:       "chars": 6567,
04169:       "sha256": "020c0bb68dc89e3fc2221d37ff68f61a7988df30d9d291ef38470ff54f6db14a",
04170:       "symbols": {
04171:         "imports": [
04172:           "from dataclasses import dataclass"
04173:         ],
04174:         "functions": [],
04175:         "classes": [
04176:           {
04177:             "name": "LayerSpec",
04178:             "line": 16,
04179:             "methods": []
04180:           }
04181:         ],
04182:         "assignments": [
04183:           "PROJECT_ROOT_COLLECTION",
04184:           "STRUCTURE_VERSION",
04185:           "LAYER_SPECS",
04186:           "LAYER_ORDER",
04187:           "EXACT_OBJECT_LAYERS",
04188:           "PREFIX_OBJECT_LAYERS",
04189:           "PARENT_LAYER_HINTS",
04190:           "TYPE_FALLBACK_LAYERS",
04191:           "FEATURE_CATALOG"
04192:         ]
04193:       }
04194:     },
04195:     {
04196:       "file": "Scripting/v61b/spaziotempo/features/__init__.py",
04197:       "exists": true,
04198:       "suffix": ".py",
04199:       "lines": 2,
04200:       "chars": 49,
04201:       "sha256": "341fbf840d490246ee054c4503c7aaaa697331ff4afe12a5356d124aacc16a3f",
04202:       "symbols": {
04203:         "imports": [],
04204:         "functions": [],
04205:         "classes": [],
04206:         "assignments": []
04207:       }
04208:     },
04209:     {
04210:       "file": "Scripting/v61b/spaziotempo/features/catalog.py",
04211:       "exists": true,
04212:       "suffix": ".py",
04213:       "lines": 20,
04214:       "chars": 466,
04215:       "sha256": "39e20ca9b04ec97730a95013071e03e253c00dfacc0345af72ddeec2b79cd3b3",
04216:       "symbols": {
04217:         "imports": [
04218:           "from spaziotempo.core.registry import FEATURE_CATALOG, LAYER_SPECS"
04219:         ],
04220:         "functions": [
04221:           {
04222:             "name": "get_feature",
04223:             "line": 10,
04224:             "args": [
04225:               "name"
04226:             ],
04227:             "async": false
04228:           },
04229:           {
04230:             "name": "feature_layer",
04231:             "line": 14,
04232:             "args": [
04233:               "name"
04234:             ],
04235:             "async": false
04236:           }
04237:         ],
04238:         "classes": [],
04239:         "assignments": []
04240:       }
04241:     },
04242:     {
04243:       "file": "Tools/npu/ai_memory_context.py",
04244:       "exists": true,
04245:       "suffix": ".py",
04246:       "lines": 112,
04247:       "chars": 4815,
04248:       "sha256": "4febdeb28cc24886e60e547d4cb1097a0928f17283ecd58ba22db9fd3c12f9a7",
04249:       "symbols": {
04250:         "imports": [
04251:           "from __future__ import annotations",
04252:           "from pathlib import Path",
04253:           "from typing import Any",
04254:           "json"
04255:         ],
04256:         "functions": [
04257:           {
04258:             "name": "read_json",
04259:             "line": 13,
04260:             "args": [
04261:               "path"
04262:             ],
04263:             "async": false
04264:           },
04265:           {
04266:             "name": "compact_asset_inventory",
04267:             "line": 23,
04268:             "args": [
04269:               "asset_inventory"
04270:             ],
04271:             "async": false
04272:           },
04273:           {
04274:             "name": "slugify",
04275:             "line": 43,
04276:             "args": [
04277:               "value"
04278:             ],
04279:             "async": false
04280:           },
04281:           {
04282:             "name": "compact_project_awareness",
04283:             "line": 48,
04284:             "args": [
04285:               "track_stem"
04286:             ],
04287:             "async": false
04288:           },
04289:           {
04290:             "name": "build_ai_memory_context",
04291:             "line": 76,
04292:             "args": [],
04293:             "async": false
04294:           }
04295:         ],
04296:         "classes": [],
04297:         "assignments": [
04298:           "ROOT",
04299:           "OUTPUT_DIR",
04300:           "INDEX_AI_DIR"
04301:         ]
04302:       }
04303:     },
04304:     {
04305:       "file": "Tools/npu/build_ai_service_packet.py",
04306:       "exists": true,
04307:       "suffix": ".py",
04308:       "lines": 356,
04309:       "chars": 15673,
04310:       "sha256": "0906bc0f6df6c0da50221ca38e0cce89d78afea243278b5f396225c6eb38af1d",
04311:       "symbols": {
04312:         "imports": [
04313:           "from __future__ import annotations",
04314:           "from datetime import datetime",
04315:           "from pathlib import Path",
04316:           "argparse",
04317:           "hashlib",
04318:           "json",
04319:           "re",
04320:           "from typing import Any"
04321:         ],
04322:         "functions": [
04323:           {
04324:             "name": "slugify",
04325:             "line": 20,
04326:             "args": [
04327:               "value",
04328:               "max_len"
04329:             ],
04330:             "async": false
04331:           },
04332:           {
04333:             "name": "read_json",
04334:             "line": 25,
04335:             "args": [
04336:               "path"
04337:             ],
04338:             "async": false
04339:           },
04340:           {
04341:             "name": "sha256_file",
04342:             "line": 33,
04343:             "args": [
04344:               "path"
04345:             ],
04346:             "async": false
04347:           },
04348:           {
04349:             "name": "safe_float",
04350:             "line": 43,
04351:             "args": [
04352:               "value",
04353:               "default"
04354:             ],
04355:             "async": false
04356:           },
04357:           {
04358:             "name": "top_project_files",
04359:             "line": 50,
04360:             "args": [
04361:               "manifest"
04362:             ],
04363:             "async": false
04364:           },
04365:           {
04366:             "name": "role_for_file",
04367:             "line": 83,
04368:             "args": [
04369:               "file_name"
04370:             ],
04371:             "async": false
04372:           },
04373:           {
04374:             "name": "compact_segments",
04375:             "line": 102,
04376:             "args": [
04377:               "music_context",
04378:               "limit"
04379:             ],
04380:             "async": false
04381:           },
04382:           {
04383:             "name": "build_ai_service_packet",
04384:             "line": 138,
04385:             "args": [
04386:               "track_stem",
04387:               "analysis_path",
04388:               "track_summary_path",
04389:               "music_context_path",
04390:               "analysis_ai_context_path",
04391:               "blender_keyframes_path",
04392:               "dual_plan_path",
04393:               "npu_notes",
04394:               "npu_status",
04395:               "scene_brief",
04396:               "asset_inventory"
04397:             ],
04398:             "async": false
04399:           },
04400:           {
04401:             "name": "format_capsule_md",
04402:             "line": 305,
04403:             "args": [
04404:               "capsule"
04405:             ],
04406:             "async": false
04407:           },
04408:           {
04409:             "name": "main",
04410:             "line": 325,
04411:             "args": [],
04412:             "async": false
04413:           }
04414:         ],
04415:         "classes": [],
04416:         "assignments": [
04417:           "ROOT",
04418:           "OUTPUT_DIR",
04419:           "INDEX_AI_DIR",
04420:           "PATCH_LIBRARY_DIR",
04421:           "SCENE_SCRIPTS_DIR",
04422:           "PROJECT_MANIFEST_JSON"
04423:         ]
04424:       }
04425:     },
04426:     {
04427:       "file": "Tools/npu/build_music_context.py",
04428:       "exists": true,
04429:       "suffix": ".py",
04430:       "lines": 712,
04431:       "chars": 27167,
04432:       "sha256": "dedb206a9a9e8d6f554be7d0a70ab29fe3d27ec81ffb133130e12b61b2a5d97b",
04433:       "symbols": {
04434:         "imports": [
04435:           "from __future__ import annotations",
04436:           "from pathlib import Path",
04437:           "argparse",
04438:           "hashlib",
04439:           "json",
04440:           "math",
04441:           "statistics",
04442:           "from datetime import datetime",
04443:           "from ai_memory_context import build_ai_memory_context"
04444:         ],
04445:         "functions": [
04446:           {
04447:             "name": "sha256_text",
04448:             "line": 41,
04449:             "args": [
04450:               "text"
04451:             ],
04452:             "async": false
04453:           },
04454:           {
04455:             "name": "rel_to_root",
04456:             "line": 45,
04457:             "args": [
04458:               "path"
04459:             ],
04460:             "async": false
04461:           },
04462:           {
04463:             "name": "read_text",
04464:             "line": 52,
04465:             "args": [
04466:               "path"
04467:             ],
04468:             "async": false
04469:           },
04470:           {
04471:             "name": "load_json",
04472:             "line": 56,
04473:             "args": [
04474:               "path"
04475:             ],
04476:             "async": false
04477:           },
04478:           {
04479:             "name": "round_float",
04480:             "line": 61,
04481:             "args": [
04482:               "value",
04483:               "digits"
04484:             ],
04485:             "async": false
04486:           },
04487:           {
04488:             "name": "quantile",
```
