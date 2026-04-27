# Project Code Chunk 154/212

- File: `Tools/npu/npu_code_manifest.json`
- Part: `7`
- Lines: `1965-2282`

## Content
```json
01965:           "from config import PRIMARY_BASE_Z, AURA_RADIUS, USE_HERO_AURA_MESH, AURA_DEFORM_SUBDIV_VIEW, AURA_DEFORM_SUBDIV_RENDER, AURA_DEFORM_FIELD_RADIUS, AURA_DEFORM_DISPLACE_MIN, AURA_DEFORM_DISPLACE_MAX, AURA_DEFORM_DETAIL_MAX, AURA_DEFORM_WAVE_HEIGHT_MAX, AURA_DEFORM_FIELD_STRENGTH_MAX, ENERGY_RING_COUNT, RIBBON_COUNT, CREATE_VARIANTS, VARIANT_COUNT, VARIANT_RING_RADIUS, VARIANT_SCALE_MIN, VARIANT_SCALE_MAX, USE_MIST_PARTICLES, MIST_PARTICLE_COUNT, MIST_SCALE_MIN, MIST_SCALE_MAX, ATMOSPHERE_CUBE_SIZE, FOG_VOLUME_ENABLED, FOG_VOLUME_VIEWPORT_VISIBLE, FOG_RAMP_LOW_BASE, FOG_RAMP_HIGH_BASE, PALETTE_LIST, PEACE_PALETTE",
01966:           "from materials import build_aura_material, build_ring_material, build_ribbon_material, build_variant_material, build_atmosphere_volume_material, build_mist_particle_material",
01967:           "from asset_setup import duplicate_hierarchy, assign_material_to_hierarchy",
01968:           "from scene_utils import create_controller_empty",
01969:           "from fog_filaments import ensure_fog_filaments"
01970:         ],
01971:         "functions": [
01972:           {
01973:             "name": "init_audio_props",
01974:             "line": 62,
01975:             "args": [
01976:               "obj"
01977:             ],
01978:             "async": false
01979:           },
01980:           {
01981:             "name": "add_prop_driver",
01982:             "line": 71,
01983:             "args": [
01984:               "idblock",
01985:               "data_path",
01986:               "expression",
01987:               "prop_targets"
01988:             ],
01989:             "async": false
01990:           },
01991:           {
01992:             "name": "create_aura_deform_field",
01993:             "line": 96,
01994:             "args": [
01995:               "controller",
01996:               "aura_location",
01997:               "parent"
01998:             ],
01999:             "async": false
02000:           },
02001:           {
02002:             "name": "add_hero_aura_deformers",
02003:             "line": 144,
02004:             "args": [
02005:               "aura",
02006:               "controller",
02007:               "deform_field"
02008:             ],
02009:             "async": false
02010:           },
02011:           {
02012:             "name": "create_hero_aura",
02013:             "line": 249,
02014:             "args": [
02015:               "parent"
02016:             ],
02017:             "async": false
02018:           },
02019:           {
02020:             "name": "create_energy_rings",
02021:             "line": 325,
02022:             "args": [
02023:               "parent"
02024:             ],
02025:             "async": false
02026:           },
02027:           {
02028:             "name": "create_energy_ribbons",
02029:             "line": 361,
02030:             "args": [
02031:               "parent"
02032:             ],
02033:             "async": false
02034:           },
02035:           {
02036:             "name": "create_variants",
02037:             "line": 399,
02038:             "args": [
02039:               "hero_root",
02040:               "parent"
02041:             ],
02042:             "async": false
02043:           },
02044:           {
02045:             "name": "create_atmosphere_cube",
02046:             "line": 433,
02047:             "args": [
02048:               "parent"
02049:             ],
02050:             "async": false
02051:           },
02052:           {
02053:             "name": "create_mist_particles",
02054:             "line": 502,
02055:             "args": [
02056:               "parent"
02057:             ],
02058:             "async": false
02059:           }
02060:         ],
02061:         "classes": [],
02062:         "assignments": [
02063:           "AURA_AUDIO_PROPS"
02064:         ]
02065:       }
02066:     },
02067:     {
02068:       "file": "Scripting/v61b/world_setup.py",
02069:       "exists": true,
02070:       "suffix": ".py",
02071:       "lines": 199,
02072:       "chars": 6567,
02073:       "sha256": "4d57f4b5253bb156e40125592238f3a9e872420ebe9b5d5b273d392f3759ef04",
02074:       "symbols": {
02075:         "imports": [
02076:           "bpy",
02077:           "from pathlib import Path",
02078:           "from config import PEACE_PALETTE, WORLD_STRENGTH, WORLD_CAMERA_STRENGTH, WORLD_LIGHT_COLOR, WORLD_CAMERA_COLOR, USE_HDRI_WORLD, HDRI_PATH, HDRI_STRENGTH, HDRI_ROT_Z, LIGHT_ENERGY_MIN, FLOOR_SIZE, FLOOR_RENDER_VISIBLE, FLOOR_VIEWPORT_VISIBLE, USE_SOFT_BACKDROP, BACKDROP_SIZE, BACKDROP_LOCATION, BACKDROP_ROT_X, USE_INVISIBLE_COLLISION_PLANE, INVISIBLE_COLLISION_PLANE_SIZE, INVISIBLE_COLLISION_PLANE_Z",
02079:           "from materials import build_reflective_floor_material, build_invisible_surface_material, build_soft_backdrop_material",
02080:           "from scene_utils import create_controller_empty"
02081:         ],
02082:         "functions": [
02083:           {
02084:             "name": "configure_world",
02085:             "line": 34,
02086:             "args": [
02087:               "scene"
02088:             ],
02089:             "async": false
02090:           },
02091:           {
02092:             "name": "create_floor_and_backdrop",
02093:             "line": 110,
02094:             "args": [],
02095:             "async": false
02096:           },
02097:           {
02098:             "name": "create_area_lights",
02099:             "line": 175,
02100:             "args": [],
02101:             "async": false
02102:           }
02103:         ],
02104:         "classes": [],
02105:         "assignments": []
02106:       }
02107:     },
02108:     {
02109:       "file": "Scripting/v61b/render_setup.py",
02110:       "exists": true,
02111:       "suffix": ".py",
02112:       "lines": 271,
02113:       "chars": 8038,
02114:       "sha256": "d798f6054b2e94e063ff5b21a9648641ce99231902dd16e288784ecf962a24ca",
02115:       "symbols": {
02116:         "imports": [
02117:           "bpy",
02118:           "from pathlib import Path",
02119:           "from config import RENDER_RESOLUTION_X, RENDER_RESOLUTION_Y, USE_4K, RENDER_PERCENT, USE_MOTION_BLUR, EEVEE_TAA_RENDER_SAMPLES, USE_BLOOM, BLOOM_THRESHOLD, BLOOM_INTENSITY, VIEW_EXPOSURE, VIEW_GAMMA, VIDEO_BITRATE, VIDEO_MAXRATE, VIDEO_MINRATE, VIDEO_BUFFERSIZE, AUDIO_BITRATE, RENDER_OUTPUT_MODE, OUTPUT_IMAGE_SEQUENCE_DIR, OUTPUT_IMAGE_SEQUENCE_PREFIX, IMAGE_SEQUENCE_FORMAT, IMAGE_SEQUENCE_COLOR_DEPTH, IMAGE_SEQUENCE_COMPRESSION, VOLUMETRIC_SAMPLES, VOLUMETRIC_TILE_SIZE, FOG_VOLUME_ENABLED, USE_COMPOSITING, COMPOSITOR_GLARE_THRESHOLD_MAX, COMPOSITOR_GLARE_MIX, COMPOSITOR_GLARE_SIZE, COMPOSITOR_LENS_DISTORT_MIN, COMPOSITOR_LENS_DISPERSION_MIN"
02120:         ],
02121:         "functions": [
02122:           {
02123:             "name": "configure_scene_physics",
02124:             "line": 39,
02125:             "args": [
02126:               "scene"
02127:             ],
02128:             "async": false
02129:           },
02130:           {
02131:             "name": "get_scene_compositor_tree",
02132:             "line": 67,
02133:             "args": [
02134:               "scene"
02135:             ],
02136:             "async": false
02137:           },
02138:           {
02139:             "name": "configure_compositor",
02140:             "line": 75,
02141:             "args": [
02142:               "scene"
02143:             ],
02144:             "async": false
02145:           },
02146:           {
02147:             "name": "configure_render",
02148:             "line": 157,
02149:             "args": [
02150:               "scene",
02151:               "output_mp4",
02152:               "fps"
02153:             ],
02154:             "async": false
02155:           }
02156:         ],
02157:         "classes": [],
02158:         "assignments": []
02159:       }
02160:     },
02161:     {
02162:       "file": "Scripting/v61b/scene_tuning_panel.py",
02163:       "exists": true,
02164:       "suffix": ".py",
02165:       "lines": 1263,
02166:       "chars": 47791,
02167:       "sha256": "55c3c28fad20ca2dd87058f9f9959ad655e51b0a85286e1af9876627eac81057",
02168:       "symbols": {
02169:         "imports": [
02170:           "json",
02171:           "sys",
02172:           "traceback",
02173:           "from pathlib import Path",
02174:           "bpy",
02175:           "from bpy.props import BoolProperty, FloatProperty, PointerProperty, StringProperty"
02176:         ],
02177:         "functions": [
02178:           {
02179:             "name": "resolve_script_dir",
02180:             "line": 20,
02181:             "args": [],
02182:             "async": false
02183:           },
02184:           {
02185:             "name": "iter_action_fcurves",
02186:             "line": 56,
02187:             "args": [
02188:               "action"
02189:             ],
02190:             "async": false
02191:           },
02192:           {
02193:             "name": "find_obj",
02194:             "line": 88,
02195:             "args": [
02196:               "name"
02197:             ],
02198:             "async": false
02199:           },
02200:           {
02201:             "name": "objects_with_prefix",
02202:             "line": 92,
02203:             "args": [
02204:               "prefix"
02205:             ],
02206:             "async": false
02207:           },
02208:           {
02209:             "name": "particle_emitters",
02210:             "line": 96,
02211:             "args": [],
02212:             "async": false
02213:           },
02214:           {
02215:             "name": "particle_source_objects",
02216:             "line": 106,
02217:             "args": [],
02218:             "async": false
02219:           },
02220:           {
02221:             "name": "store_base_vector",
02222:             "line": 117,
02223:             "args": [
02224:               "obj",
02225:               "key",
02226:               "value"
02227:             ],
02228:             "async": false
02229:           },
02230:           {
02231:             "name": "store_base_float",
02232:             "line": 123,
02233:             "args": [
02234:               "idblock",
02235:               "key",
02236:               "value"
02237:             ],
02238:             "async": false
02239:           },
02240:           {
02241:             "name": "set_scale_from_base",
02242:             "line": 132,
02243:             "args": [
02244:               "obj",
02245:               "factor",
02246:               "key"
02247:             ],
02248:             "async": false
02249:           },
02250:           {
02251:             "name": "keyframe_if_possible",
02252:             "line": 140,
02253:             "args": [
02254:               "idblock",
02255:               "data_path",
02256:               "frame"
02257:             ],
02258:             "async": false
02259:           },
02260:           {
02261:             "name": "find_material",
02262:             "line": 147,
02263:             "args": [
02264:               "name"
02265:             ],
02266:             "async": false
02267:           },
02268:           {
02269:             "name": "find_node",
02270:             "line": 151,
02271:             "args": [
02272:               "material_name",
02273:               "node_name"
02274:             ],
02275:             "async": false
02276:           },
02277:           {
02278:             "name": "set_value_node",
02279:             "line": 158,
02280:             "args": [
02281:               "material_name",
02282:               "node_name",
```
