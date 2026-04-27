# Project Code Chunk 45/212

- File: `Scripting/v61b/io_utils.py`
- Part: `1`
- Lines: `1-81`

## Symbol Map
- Imports: `bpy`, `json`, `from pathlib import Path`
- Functions: `load_json(path)` line 6; `ensure_file_exists(path, label)` line 12; `ensure_inputs_exist(analysis_path, audio_path)` line 19; `clear_sequencer(scene)` line 25; `add_audio_strip(scene, audio_path, clear_existing, sync_audio)` line 49

## Content
```py
00001: import bpy
00002: import json
00003: from pathlib import Path
00004: 
00005: 
00006: def load_json(path):
00007:     path = Path(path)
00008:     with open(path, "r", encoding="utf-8") as f:
00009:         return json.load(f)
00010: 
00011: 
00012: def ensure_file_exists(path, label="File"):
00013:     path = Path(path)
00014:     if not path.exists():
00015:         raise FileNotFoundError(f"{label} non trovato: {path}")
00016:     return path
00017: 
00018: 
00019: def ensure_inputs_exist(analysis_path, audio_path):
00020:     analysis_file = ensure_file_exists(analysis_path, "Analysis JSON")
00021:     audio_file = ensure_file_exists(audio_path, "Audio")
00022:     return analysis_file, audio_file
00023: 
00024: 
00025: def clear_sequencer(scene):
00026:     seq = scene.sequence_editor
00027:     if not seq:
00028:         return
00029: 
00030:     strips = getattr(seq, "strips", None)
00031:     if strips is not None:
00032:         for strip in list(strips):
00033:             try:
00034:                 strips.remove(strip)
00035:             except Exception:
00036:                 pass
00037:         return
00038: 
00039:     sequences_all = getattr(seq, "sequences_all", None)
00040:     sequences = getattr(seq, "sequences", None)
00041:     if sequences_all is not None and sequences is not None:
00042:         for strip in list(sequences_all):
00043:             try:
00044:                 sequences.remove(strip)
00045:             except Exception:
00046:                 pass
00047: 
00048: 
00049: def add_audio_strip(scene, audio_path, clear_existing=True, sync_audio=True):
00050:     audio_path = Path(audio_path)
00051:     if not audio_path.exists():
00052:         raise FileNotFoundError(f"Audio non trovato: {audio_path}")
00053: 
00054:     seq = scene.sequence_editor
00055:     if seq is None:
00056:         seq = scene.sequence_editor_create()
00057: 
00058:     if clear_existing:
00059:         clear_sequencer(scene)
00060: 
00061:     strip_name = audio_path.stem
00062: 
00063:     if hasattr(seq, "strips") and hasattr(seq.strips, "new_sound"):
00064:         sound_strip = seq.strips.new_sound(
00065:             name=strip_name,
00066:             filepath=str(audio_path),
00067:             channel=1,
00068:             frame_start=1,
00069:         )
00070:     elif hasattr(seq, "sequences") and hasattr(seq.sequences, "new_sound"):
00071:         sound_strip = seq.sequences.new_sound(strip_name, str(audio_path), 1, 1)
00072:     else:
00073:         raise RuntimeError("API Sequencer non compatibile per creare una sound strip.")
00074: 
00075:     if sync_audio:
00076:         try:
00077:             scene.sync_mode = "AUDIO_SYNC"
00078:         except Exception:
00079:             pass
00080: 
00081:     return sound_strip
```
