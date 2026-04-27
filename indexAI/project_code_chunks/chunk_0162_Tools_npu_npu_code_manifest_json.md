# Project Code Chunk 162/212

- File: `Tools/npu/npu_code_manifest.json`
- Part: `15`
- Lines: `4875-5244`

## Content
```json
04875:           "OUT_INDEX_MD",
04876:           "OUT_JSON",
04877:           "CHUNK_DIR",
04878:           "MAX_CHUNK_CHARS",
04879:           "PRIORITY_FILES",
04880:           "DISCOVERY_GLOBS",
04881:           "EXCLUDE_PARTS",
04882:           "TEXT_SUFFIXES"
04883:         ]
04884:       }
04885:     },
04886:     {
04887:       "file": "Tools/npu/build_project_ai_index.py",
04888:       "exists": true,
04889:       "suffix": ".py",
04890:       "lines": 420,
04891:       "chars": 14905,
04892:       "sha256": "5d0e447d5d77e945f831b80e31a0f0ccdd224276d30fe452a85293c99251e7c7",
04893:       "symbols": {
04894:         "imports": [
04895:           "from __future__ import annotations",
04896:           "from datetime import datetime",
04897:           "from pathlib import Path",
04898:           "argparse",
04899:           "ast",
04900:           "hashlib",
04901:           "json",
04902:           "re"
04903:         ],
04904:         "functions": [
04905:           {
04906:             "name": "sha256_text",
04907:             "line": 74,
04908:             "args": [
04909:               "text"
04910:             ],
04911:             "async": false
04912:           },
04913:           {
04914:             "name": "sha256_file",
04915:             "line": 78,
04916:             "args": [
04917:               "path"
04918:             ],
04919:             "async": false
04920:           },
04921:           {
04922:             "name": "rel_to_root",
04923:             "line": 86,
04924:             "args": [
04925:               "path"
04926:             ],
04927:             "async": false
04928:           },
04929:           {
04930:             "name": "slugify",
04931:             "line": 90,
04932:             "args": [
04933:               "value",
04934:               "max_len"
04935:             ],
04936:             "async": false
04937:           },
04938:           {
04939:             "name": "should_exclude",
04940:             "line": 95,
04941:             "args": [
04942:               "path"
04943:             ],
04944:             "async": false
04945:           },
04946:           {
04947:             "name": "collect_project_files",
04948:             "line": 116,
04949:             "args": [],
04950:             "async": false
04951:           },
04952:           {
04953:             "name": "target_name",
04954:             "line": 131,
04955:             "args": [
04956:               "target"
04957:             ],
04958:             "async": false
04959:           },
04960:           {
04961:             "name": "extract_symbols",
04962:             "line": 139,
04963:             "args": [
04964:               "source"
04965:             ],
04966:             "async": false
04967:           },
04968:           {
04969:             "name": "file_record",
04970:             "line": 182,
04971:             "args": [
04972:               "path"
04973:             ],
04974:             "async": false
04975:           },
04976:           {
04977:             "name": "format_symbol_summary",
04978:             "line": 196,
04979:             "args": [
04980:               "record"
04981:             ],
04982:             "async": false
04983:           },
04984:           {
04985:             "name": "numbered_lines",
04986:             "line": 223,
04987:             "args": [
04988:               "lines",
04989:               "start_line"
04990:             ],
04991:             "async": false
04992:           },
04993:           {
04994:             "name": "split_source",
04995:             "line": 227,
04996:             "args": [
04997:               "source",
04998:               "max_chars"
04999:             ],
05000:             "async": false
05001:           },
05002:           {
05003:             "name": "source_fingerprint",
05004:             "line": 249,
05005:             "args": [
05006:               "records"
05007:             ],
05008:             "async": false
05009:           },
05010:           {
05011:             "name": "existing_cache_valid",
05012:             "line": 258,
05013:             "args": [
05014:               "fingerprint"
05015:             ],
05016:             "async": false
05017:           },
05018:           {
05019:             "name": "write_readme",
05020:             "line": 272,
05021:             "args": [],
05022:             "async": false
05023:           },
05024:           {
05025:             "name": "write_chunks",
05026:             "line": 293,
05027:             "args": [
05028:               "records",
05029:               "max_chunk_chars"
05030:             ],
05031:             "async": false
05032:           },
05033:           {
05034:             "name": "write_index",
05035:             "line": 347,
05036:             "args": [
05037:               "records",
05038:               "chunks",
05039:               "created_at",
05040:               "fingerprint"
05041:             ],
05042:             "async": false
05043:           },
05044:           {
05045:             "name": "build_project_ai_index",
05046:             "line": 367,
05047:             "args": [
05048:               "force",
05049:               "max_chunk_chars"
05050:             ],
05051:             "async": false
05052:           },
05053:           {
05054:             "name": "main",
05055:             "line": 410,
05056:             "args": [],
05057:             "async": false
05058:           }
05059:         ],
05060:         "classes": [],
05061:         "assignments": [
05062:           "ROOT",
05063:           "INDEX_DIR",
05064:           "PROJECT_INDEX_MD",
05065:           "PROJECT_MANIFEST_JSON",
05066:           "PROJECT_CHUNK_DIR",
05067:           "PATCH_LIBRARY_DIR",
05068:           "README_MD",
05069:           "DEFAULT_MAX_CHUNK_CHARS",
05070:           "TEXT_SUFFIXES",
05071:           "EXCLUDE_DIRS",
05072:           "EXCLUDE_PARTS",
05073:           "EXCLUDE_FILE_PREFIXES",
05074:           "MEDIA_SUFFIXES"
05075:         ]
05076:       }
05077:     },
05078:     {
05079:       "file": "Tools/npu/run_dual_ai_pipeline - Copia.py",
05080:       "exists": true,
05081:       "suffix": ".py",
05082:       "lines": 706,
05083:       "chars": 29030,
05084:       "sha256": "868f5619cef911174e14aa2fa79b9ac61cd3c2b47c05144e468a6a663869ca95",
05085:       "symbols": {
05086:         "imports": [
05087:           "from __future__ import annotations",
05088:           "from pathlib import Path",
05089:           "argparse",
05090:           "json",
05091:           "subprocess",
05092:           "sys",
05093:           "from datetime import datetime",
05094:           "from build_music_context import build_music_context",
05095:           "from build_npu_code_context import main",
05096:           "from build_blender_manual_context import build_manual_context",
05097:           "from build_project_ai_index import PROJECT_INDEX_MD, PROJECT_MANIFEST_JSON, build_project_ai_index",
05098:           "from npu_runtime import DEFAULT_MODEL_DIR, DEFAULT_NPU_PYTHON, npu_preflight, write_npu_preflight_report",
05099:           "from ollama_runtime import OllamaModelManager, parse_json_response",
05100:           "from run_ollama_music_agent import build_prompt",
05101:           "from run_ollama_music_agent import markdown_from_insights"
05102:         ],
05103:         "functions": [
05104:           {
05105:             "name": "read_text",
05106:             "line": 38,
05107:             "args": [
05108:               "path"
05109:             ],
05110:             "async": false
05111:           },
05112:           {
05113:             "name": "read_json",
05114:             "line": 42,
05115:             "args": [
05116:               "path"
05117:             ],
05118:             "async": false
05119:           },
05120:           {
05121:             "name": "write_json",
05122:             "line": 47,
05123:             "args": [
05124:               "path",
05125:               "data"
05126:             ],
05127:             "async": false
05128:           },
05129:           {
05130:             "name": "validate_input_files",
05131:             "line": 52,
05132:             "args": [
05133:               "args"
05134:             ],
05135:             "async": false
05136:           },
05137:           {
05138:             "name": "looks_degraded_text",
05139:             "line": 72,
05140:             "args": [
05141:               "text"
05142:             ],
05143:             "async": false
05144:           },
05145:           {
05146:             "name": "deterministic_technical_notes",
05147:             "line": 85,
05148:             "args": [
05149:               "music_context",
05150:               "project_manifest",
05151:               "reason"
05152:             ],
05153:             "async": false
05154:           },
05155:           {
05156:             "name": "run_npu_technical_pass",
05157:             "line": 134,
05158:             "args": [
05159:               "args"
05160:             ],
05161:             "async": false
05162:           },
05163:           {
05164:             "name": "build_creative_scene_prompt",
05165:             "line": 178,
05166:             "args": [
05167:               "music_context",
05168:               "npu_notes",
05169:               "project_index"
05170:             ],
05171:             "async": false
05172:           },
05173:           {
05174:             "name": "build_merge_prompt",
05175:             "line": 254,
05176:             "args": [
05177:               "music_context",
05178:               "npu_notes",
05179:               "creative",
05180:               "technical"
05181:             ],
05182:             "async": false
05183:           },
05184:           {
05185:             "name": "build_implementation_prompt",
05186:             "line": 305,
05187:             "args": [
05188:               "plan",
05189:               "npu_notes",
05190:               "include_manual"
05191:             ],
05192:             "async": false
05193:           },
05194:           {
05195:             "name": "safe_parse_json",
05196:             "line": 373,
05197:             "args": [
05198:               "text",
05199:               "fallback_key"
05200:             ],
05201:             "async": false
05202:           },
05203:           {
05204:             "name": "write_brief",
05205:             "line": 380,
05206:             "args": [
05207:               "plan",
05208:               "creative",
05209:               "technical",
05210:               "npu_notes"
05211:             ],
05212:             "async": false
05213:           },
05214:           {
05215:             "name": "validate_implementation_draft",
05216:             "line": 403,
05217:             "args": [
05218:               "draft"
05219:             ],
05220:             "async": false
05221:           },
05222:           {
05223:             "name": "write_implementation_draft",
05224:             "line": 450,
05225:             "args": [
05226:               "draft"
05227:             ],
05228:             "async": false
05229:           },
05230:           {
05231:             "name": "main",
05232:             "line": 478,
05233:             "args": [],
05234:             "async": false
05235:           }
05236:         ],
05237:         "classes": [],
05238:         "assignments": [
05239:           "ROOT",
05240:           "TOOLS_DIR",
05241:           "OUTPUT_DIR",
05242:           "TRACK_STEM",
05243:           "MUSIC_AI_CONTEXT",
05244:           "DUAL_PLAN_JSON",
```
