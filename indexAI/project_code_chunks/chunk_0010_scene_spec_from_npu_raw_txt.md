# Project Code Chunk 10/212

- File: `scene_spec_from_npu_raw.txt`
- Part: `1`
- Lines: `1-53`

## Content
```txt
00001: ```json
00002: {
00003:   "scene_name": "dark futuristic stage",
00004:   "camera": {
00005:     "location": [0, 0, 0],
00006:     "rotation": [0, 0, 0],
00007:     "lens": 1
00008:   },
00009:   "palette": ["blue", "violet"],
00010:   "objects": [
00011:     {
00012:       "type": "sphere",
00013:       "name": "bass_sphere",
00014:       "location": [0, 5, 7.3],
00015:       "scale": [1, 1, 1]
00016:     }
00017:   ],
00018:   "objects_additional": [
00019:     {
00020:       "type": "light_columns_ring",
00021:       "name": "columns_ring",
00022:       "count": 12,
00023:       "radius": 0.5
00024:     }
00025:   ],
00026:   "audio_mapping": [
00027:     {
00028:       "target": "bass_sphere",
00029:       "property": "scale",
00030:       "band": "bass"
00031:     },
00032:     {
00033:       "target": "light_columns_ring",
00034:       "property": "radius",
00035:       "band": "bass"
00036:     },
00037:     {
00038:       "target": "light_columns_ring",
00039:       "property": "count",
00040:       "band": "bass"
00041:     },
00042:     {
00043:       "target": "light_columns_ring",
00044:       "property": "intensity",
00045:       "band": "mid"
00046:     },
00047:     {
00048:       "target": "light_columns_ring",
00049:       "property": "intensity",
00050:       "band": "high"
00051:     },
00052:     {
00053:       "target": "light_columns_
```
