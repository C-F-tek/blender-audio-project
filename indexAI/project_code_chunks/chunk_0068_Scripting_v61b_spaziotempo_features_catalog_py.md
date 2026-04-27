# Project Code Chunk 68/212

- File: `Scripting/v61b/spaziotempo/features/catalog.py`
- Part: `1`
- Lines: `1-19`

## Symbol Map
- Imports: `from spaziotempo.core.registry import FEATURE_CATALOG, LAYER_SPECS`
- Functions: `get_feature(name)` line 10; `feature_layer(name)` line 14

## Content
```py
00001: """Feature catalog facade.
00002: 
00003: Keep feature-level decisions here so adding a new block, for example water,
00004: does not require hunting through unrelated scene scripts.
00005: """
00006: 
00007: from spaziotempo.core.registry import FEATURE_CATALOG, LAYER_SPECS
00008: 
00009: 
00010: def get_feature(name):
00011:     return FEATURE_CATALOG.get(name)
00012: 
00013: 
00014: def feature_layer(name):
00015:     feature = get_feature(name)
00016:     if feature is None:
00017:         return None
00018:     layer_key = feature["layer"]
00019:     return LAYER_SPECS[layer_key]
```
