# Project Code Chunk 157/212

- File: `Tools/npu/npu_code_manifest.json`
- Part: `10`
- Lines: `3011-3389`

## Content
```json
03011:             "line": 134,
03012:             "args": [
03013:               "name"
03014:             ],
03015:             "async": false
03016:           },
03017:           {
03018:             "name": "parent_objects_keep_transform",
03019:             "line": 141,
03020:             "args": [
03021:               "objects",
03022:               "parent"
03023:             ],
03024:             "async": false
03025:           },
03026:           {
03027:             "name": "center_and_scale_asset",
03028:             "line": 150,
03029:             "args": [
03030:               "root",
03031:               "objects",
03032:               "target_size",
03033:               "base_z"
03034:             ],
03035:             "async": false
03036:           },
03037:           {
03038:             "name": "collect_meshes",
03039:             "line": 171,
03040:             "args": [
03041:               "objects"
03042:             ],
03043:             "async": false
03044:           },
03045:           {
03046:             "name": "soften_materials_to_peace",
03047:             "line": 175,
03048:             "args": [
03049:               "meshes"
03050:             ],
03051:             "async": false
03052:           },
03053:           {
03054:             "name": "find_principled_node",
03055:             "line": 206,
03056:             "args": [
03057:               "material"
03058:             ],
03059:             "async": false
03060:           },
03061:           {
03062:             "name": "get_node_input",
03063:             "line": 216,
03064:             "args": [
03065:               "node"
03066:             ],
03067:             "async": false
03068:           },
03069:           {
03070:             "name": "link_node_sockets",
03071:             "line": 226,
03072:             "args": [
03073:               "links",
03074:               "output_socket",
03075:               "input_socket",
03076:               "replace_existing"
03077:             ],
03078:             "async": false
03079:           },
03080:           {
03081:             "name": "get_or_create_node",
03082:             "line": 243,
03083:             "args": [
03084:               "nodes",
03085:               "node_type",
03086:               "name",
03087:               "location"
03088:             ],
03089:             "async": false
03090:           },
03091:           {
03092:             "name": "find_material_output",
03093:             "line": 252,
03094:             "args": [
03095:               "material"
03096:             ],
03097:             "async": false
03098:           },
03099:           {
03100:             "name": "ensure_hero_surface_light_layer",
03101:             "line": 266,
03102:             "args": [
03103:               "mat",
03104:               "principled"
03105:             ],
03106:             "async": false
03107:           },
03108:           {
03109:             "name": "get_local_mesh_extent",
03110:             "line": 346,
03111:             "args": [
03112:               "obj"
03113:             ],
03114:             "async": false
03115:           },
03116:           {
03117:             "name": "add_hero_material_audio_nodes",
03118:             "line": 360,
03119:             "args": [
03120:               "meshes"
03121:             ],
03122:             "async": false
03123:           },
03124:           {
03125:             "name": "duplicate_hierarchy",
03126:             "line": 460,
03127:             "args": [
03128:               "root",
03129:               "name_prefix"
03130:             ],
03131:             "async": false
03132:           },
03133:           {
03134:             "name": "assign_material_to_hierarchy",
03135:             "line": 488,
03136:             "args": [
03137:               "root",
03138:               "material"
03139:             ],
03140:             "async": false
03141:           },
03142:           {
03143:             "name": "add_hero_mesh_deformers",
03144:             "line": 498,
03145:             "args": [
03146:               "asset_root",
03147:               "meshes"
03148:             ],
03149:             "async": false
03150:           },
03151:           {
03152:             "name": "_create_asset_from_dir",
03153:             "line": 653,
03154:             "args": [
03155:               "asset_dir",
03156:               "target_size",
03157:               "base_z",
03158:               "root_name",
03159:               "parent"
03160:             ],
03161:             "async": false
03162:           },
03163:           {
03164:             "name": "create_primary_asset",
03165:             "line": 688,
03166:             "args": [
03167:               "parent"
03168:             ],
03169:             "async": false
03170:           },
03171:           {
03172:             "name": "create_secondary_asset",
03173:             "line": 698,
03174:             "args": [
03175:               "parent"
03176:             ],
03177:             "async": false
03178:           }
03179:         ],
03180:         "classes": [],
03181:         "assignments": []
03182:       }
03183:     },
03184:     {
03185:       "file": "Scripting/v61b/camera_setup.py",
03186:       "exists": true,
03187:       "suffix": ".py",
03188:       "lines": 30,
03189:       "chars": 815,
03190:       "sha256": "8265f48a256d126408f250dfb84af546e4ff10fbdcd1c98dd114040e17e52181",
03191:       "symbols": {
03192:         "imports": [
03193:           "bpy",
03194:           "math",
03195:           "from config import CAMERA_BASE_LOCATION, CAMERA_BASE_LENS, CAMERA_DOF_FSTOP"
03196:         ],
03197:         "functions": [
03198:           {
03199:             "name": "create_camera_rig",
03200:             "line": 7,
03201:             "args": [],
03202:             "async": false
03203:           }
03204:         ],
03205:         "classes": [],
03206:         "assignments": []
03207:       }
03208:     },
03209:     {
03210:       "file": "Scripting/v61b/io_utils.py",
03211:       "exists": true,
03212:       "suffix": ".py",
03213:       "lines": 81,
03214:       "chars": 2234,
03215:       "sha256": "6f0db21475f14dff120a5cc57d748b2178b75fbc4f60fdb6d16b8e438513dd2d",
03216:       "symbols": {
03217:         "imports": [
03218:           "bpy",
03219:           "json",
03220:           "from pathlib import Path"
03221:         ],
03222:         "functions": [
03223:           {
03224:             "name": "load_json",
03225:             "line": 6,
03226:             "args": [
03227:               "path"
03228:             ],
03229:             "async": false
03230:           },
03231:           {
03232:             "name": "ensure_file_exists",
03233:             "line": 12,
03234:             "args": [
03235:               "path",
03236:               "label"
03237:             ],
03238:             "async": false
03239:           },
03240:           {
03241:             "name": "ensure_inputs_exist",
03242:             "line": 19,
03243:             "args": [
03244:               "analysis_path",
03245:               "audio_path"
03246:             ],
03247:             "async": false
03248:           },
03249:           {
03250:             "name": "clear_sequencer",
03251:             "line": 25,
03252:             "args": [
03253:               "scene"
03254:             ],
03255:             "async": false
03256:           },
03257:           {
03258:             "name": "add_audio_strip",
03259:             "line": 49,
03260:             "args": [
03261:               "scene",
03262:               "audio_path",
03263:               "clear_existing",
03264:               "sync_audio"
03265:             ],
03266:             "async": false
03267:           }
03268:         ],
03269:         "classes": [],
03270:         "assignments": []
03271:       }
03272:     },
03273:     {
03274:       "file": "Scripting/v61b/scene_utils.py",
03275:       "exists": true,
03276:       "suffix": ".py",
03277:       "lines": 98,
03278:       "chars": 2463,
03279:       "sha256": "98780b6455aae7c8857bf8698e8e4b57feceec9187a04a8850f87bad2bb4d295",
03280:       "symbols": {
03281:         "imports": [
03282:           "bpy"
03283:         ],
03284:         "functions": [
03285:           {
03286:             "name": "clear_scene",
03287:             "line": 4,
03288:             "args": [],
03289:             "async": false
03290:           },
03291:           {
03292:             "name": "deselect_all",
03293:             "line": 29,
03294:             "args": [],
03295:             "async": false
03296:           },
03297:           {
03298:             "name": "safe_active",
03299:             "line": 33,
03300:             "args": [
03301:               "obj"
03302:             ],
03303:             "async": false
03304:           },
03305:           {
03306:             "name": "create_controller_empty",
03307:             "line": 38,
03308:             "args": [
03309:               "name",
03310:               "location",
03311:               "parent",
03312:               "display_size",
03313:               "hide_view"
03314:             ],
03315:             "async": false
03316:           },
03317:           {
03318:             "name": "iter_action_fcurves",
03319:             "line": 53,
03320:             "args": [
03321:               "action"
03322:             ],
03323:             "async": false
03324:           },
03325:           {
03326:             "name": "set_linear_interpolation_idblock",
03327:             "line": 83,
03328:             "args": [
03329:               "idblock"
03330:             ],
03331:             "async": false
03332:           }
03333:         ],
03334:         "classes": [],
03335:         "assignments": []
03336:       }
03337:     },
03338:     {
03339:       "file": "Scripting/v61b/hotpatch/__init__.py",
03340:       "exists": true,
03341:       "suffix": ".py",
03342:       "lines": 4,
03343:       "chars": 51,
03344:       "sha256": "90be9d97c6b8230b5cabf560b23404b9a3b2699f8df93b89605425c5cf164147",
03345:       "symbols": {
03346:         "imports": [
03347:           "from runner import run_all"
03348:         ],
03349:         "functions": [],
03350:         "classes": [],
03351:         "assignments": [
03352:           "__all__"
03353:         ]
03354:       }
03355:     },
03356:     {
03357:       "file": "Scripting/v61b/hotpatch/accent_patch.py",
03358:       "exists": true,
03359:       "suffix": ".py",
03360:       "lines": 302,
03361:       "chars": 12916,
03362:       "sha256": "0e7166fd48278eaeab80e30d9b45d5b04c43c1c4a6f4b34a0d2ecf17b5745f94",
03363:       "symbols": {
03364:         "imports": [
03365:           "math",
03366:           "bpy",
03367:           "from materials import build_variant_material",
03368:           "from common import PALETTE_LIST, cfg_value, clear_animation, get_node, iter_objects_prefix, keyframe_if_possible, socket_by_name, store_base_vector"
03369:         ],
03370:         "functions": [
03371:           {
03372:             "name": "drive_for_band",
03373:             "line": 40,
03374:             "args": [
03375:               "band",
03376:               "response",
03377:               "sample",
03378:               "frame",
03379:               "phase"
03380:             ],
03381:             "async": false
03382:           },
03383:           {
03384:             "name": "ensure_accent_material",
03385:             "line": 63,
03386:             "args": [
03387:               "obj",
03388:               "index"
03389:             ],
```
