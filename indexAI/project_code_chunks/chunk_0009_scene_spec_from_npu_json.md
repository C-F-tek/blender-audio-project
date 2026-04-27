# Project Code Chunk 9/212

- File: `scene_spec_from_npu.json`
- Part: `1`
- Lines: `1-65`

## Content
```json
00001: {
00002:   "scene_name": ".",
00003:   "camera": {
00004:     "location": [
00005:       16,
00006:       16,
00007:       16
00008:     ],
00009:     "rotation": [
00010:       0,
00011:       540,
00012:       360
00013:     ],
00014:     "lens": 455
00015:   },
00016:   "palette": [
00017:     "#20354D",
00018:     "#38215A",
00019:     "#4D2A37"
00020:   ],
00021:   "objects": [
00022:     {
00023:       "type": "sphere",
00024:       "name": "central_sphere",
00025:       "location": [
00026:         8,
00027:         8,
00028:         8
00029:       ],
00030:       "scale": [
00031:         0.5,
00032:         0.5,
00033:         0.5
00034:       ]
00035:     },
00036:     {
00037:       "type": "light_columns_ring",
00038:       "name": ".",
00039:       "count": 12,
00040:       "radius": 5.0
00041:     }
00042:   ],
00043:   "audio_mapping": [
00044:     {
00045:       "target": "central_sphere",
00046:       "property": "material_select",
00047:       "band": "beat"
00048:     },
00049:     {
00050:       "target": "light_cobinates_ring",
00051:       "property": "strength",
00052:       "band": "beat"
00053:     },
00054:     {
00055:       "target": "central_sphere",
00056:       "property": "material_shader",
00057:       "band": "beat"
00058:     },
00059:     {
00060:       "target": "light_cobinates_ring",
00061:       "property": "strength",
00062:       "band": "beat"
00063:     }
00064:   ]
00065: }
```
