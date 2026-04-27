# Project Code Chunk 27/212

- File: `Scripting/v61b/encode_image_sequence_v61b.py`
- Part: `1`
- Lines: `1-329`

## Symbol Map
- Imports: `re`, `sys`, `from pathlib import Path`, `bpy`, `config`
- Functions: `resolve_script_dir()` line 8; `extract_frame_number(path)` line 83; `sorted_frame_files()` line 90; `contiguous_frame_files(frame_files)` line 116; `get_sequence_collection(editor)` line 143; `all_editor_strips(editor)` line 151; `remove_editor_strip(editor, strip)` line 163; `force_visible_sequencer(scene, editor)` line 176; `clear_sequence_editor(scene)` line 224; `add_image_sequence(editor, frame_files)` line 235; `add_synced_audio(editor, first_frame)` line 258; `configure_video_output(scene, frame_count)` line 285; `print_strip_report(scene, editor)` line 327; `main()` line 342
- Assignments: `SCRIPT_DIR`, `ROOT`, `RENDERS_DIR`, `AUDIO_PATH`, `OUTPUT_MP4`, `OUTPUT_IMAGE_SEQUENCE_DIR`, `OUTPUT_IMAGE_SEQUENCE_PREFIX`, `IMAGE_SEQUENCE_FORMAT`, `VIDEO_BITRATE`, `VIDEO_MAXRATE`, `VIDEO_MINRATE`, `VIDEO_BUFFERSIZE`, `AUDIO_BITRATE`, `ENCODE_SEQUENCE_AUTO_RENDER`, `ENCODE_SEQUENCE_SYNC_AUDIO_TO_FRAME_NUMBER`, `ENCODE_SEQUENCE_AUDIO_ZERO_FRAME`, `ENCODE_SEQUENCE_SKIP_PLACEHOLDERS`, `ENCODE_SEQUENCE_SWITCH_TO_SEQUENCER`

## Content
```py
00001: import re
00002: import sys
00003: from pathlib import Path
00004: 
00005: import bpy
00006: 
00007: 
00008: def resolve_script_dir():
00009:     candidates = []
00010: 
00011:     try:
00012:         text = bpy.context.space_data.text
00013:         if text is not None and text.filepath:
00014:             candidates.append(Path(text.filepath).resolve().parent)
00015:     except Exception:
00016:         pass
00017: 
00018:     if "__file__" in globals():
00019:         try:
00020:             candidates.append(Path(__file__).resolve().parent)
00021:         except Exception:
00022:             pass
00023: 
00024:     candidates.append(Path.home() / "blender" / "blender-audio-project" / "Scripting" / "v61b")
00025: 
00026:     for candidate in candidates:
00027:         if (candidate / "config.py").exists() and (candidate / "encode_image_sequence_v61b.py").exists():
00028:             return candidate
00029: 
00030:     return candidates[-1]
00031: 
00032: 
00033: SCRIPT_DIR = resolve_script_dir()
00034: 
00035: if str(SCRIPT_DIR) not in sys.path:
00036:     sys.path.insert(0, str(SCRIPT_DIR))
00037: 
00038: sys.modules.pop("config", None)
00039: 
00040: import config as cfg  # noqa: E402
00041: 
00042: 
00043: ROOT = getattr(cfg, "ROOT", Path.home() / "blender")
00044: RENDERS_DIR = getattr(cfg, "RENDERS_DIR", ROOT / "renders")
00045: 
00046: AUDIO_PATH = cfg.AUDIO_PATH
00047: OUTPUT_MP4 = getattr(cfg, "OUTPUT_MP4", RENDERS_DIR / "spaziotempo_asset_visual_v61b.mp4")
00048: OUTPUT_IMAGE_SEQUENCE_DIR = getattr(
00049:     cfg,
00050:     "OUTPUT_IMAGE_SEQUENCE_DIR",
00051:     RENDERS_DIR / "spaziotempo_asset_visual_v61b_frames",
00052: )
00053: OUTPUT_IMAGE_SEQUENCE_PREFIX = getattr(
00054:     cfg,
00055:     "OUTPUT_IMAGE_SEQUENCE_PREFIX",
00056:     "spaziotempo_v61b_",
00057: )
00058: IMAGE_SEQUENCE_FORMAT = getattr(cfg, "IMAGE_SEQUENCE_FORMAT", "PNG")
00059: VIDEO_BITRATE = getattr(cfg, "VIDEO_BITRATE", 12000)
00060: VIDEO_MAXRATE = getattr(cfg, "VIDEO_MAXRATE", 16000)
00061: VIDEO_MINRATE = getattr(cfg, "VIDEO_MINRATE", 0)
00062: VIDEO_BUFFERSIZE = getattr(cfg, "VIDEO_BUFFERSIZE", 1792)
00063: AUDIO_BITRATE = getattr(cfg, "AUDIO_BITRATE", 320)
00064: ENCODE_SEQUENCE_AUTO_RENDER = getattr(cfg, "ENCODE_SEQUENCE_AUTO_RENDER", False)
00065: ENCODE_SEQUENCE_SYNC_AUDIO_TO_FRAME_NUMBER = getattr(
00066:     cfg,
00067:     "ENCODE_SEQUENCE_SYNC_AUDIO_TO_FRAME_NUMBER",
00068:     True,
00069: )
00070: ENCODE_SEQUENCE_AUDIO_ZERO_FRAME = int(getattr(cfg, "ENCODE_SEQUENCE_AUDIO_ZERO_FRAME", 1))
00071: ENCODE_SEQUENCE_SKIP_PLACEHOLDERS = getattr(
00072:     cfg,
00073:     "ENCODE_SEQUENCE_SKIP_PLACEHOLDERS",
00074:     True,
00075: )
00076: ENCODE_SEQUENCE_SWITCH_TO_SEQUENCER = getattr(
00077:     cfg,
00078:     "ENCODE_SEQUENCE_SWITCH_TO_SEQUENCER",
00079:     True,
00080: )
00081: 
00082: 
00083: def extract_frame_number(path):
00084:     stem = path.stem
00085:     tail = stem[len(OUTPUT_IMAGE_SEQUENCE_PREFIX):] if stem.startswith(OUTPUT_IMAGE_SEQUENCE_PREFIX) else stem
00086:     match = re.search(r"(\d+)$", tail)
00087:     return int(match.group(1)) if match else None
00088: 
00089: 
00090: def sorted_frame_files():
00091:     ext = ".png" if IMAGE_SEQUENCE_FORMAT.upper() == "PNG" else ""
00092:     pattern = f"{OUTPUT_IMAGE_SEQUENCE_PREFIX}*{ext}" if ext else f"{OUTPUT_IMAGE_SEQUENCE_PREFIX}*"
00093:     files = []
00094: 
00095:     for path in Path(OUTPUT_IMAGE_SEQUENCE_DIR).glob(pattern):
00096:         if not path.is_file():
00097:             continue
00098:         if ENCODE_SEQUENCE_SKIP_PLACEHOLDERS:
00099:             try:
00100:                 if path.stat().st_size <= 0:
00101:                     continue
00102:             except Exception:
00103:                 continue
00104:         files.append(path)
00105: 
00106:     return sorted(
00107:         files,
00108:         key=lambda path: (
00109:             extract_frame_number(path) is None,
00110:             extract_frame_number(path) or 0,
00111:             path.name,
00112:         ),
00113:     )
00114: 
00115: 
00116: def contiguous_frame_files(frame_files):
00117:     if not frame_files:
00118:         return [], None
00119: 
00120:     first_frame = extract_frame_number(frame_files[0])
00121:     if first_frame is None:
00122:         return frame_files, None
00123: 
00124:     kept = [frame_files[0]]
00125:     expected = first_frame + 1
00126: 
00127:     for path in frame_files[1:]:
00128:         frame_number = extract_frame_number(path)
00129:         if frame_number != expected:
00130:             print(
00131:                 "[WARN] Gap nella sequenza: "
00132:                 f"atteso frame {expected}, trovato {frame_number or path.name}. "
00133:                 "Uso solo il blocco continuo iniziale per mantenere sync audio."
00134:             )
00135:             break
00136: 
00137:         kept.append(path)
00138:         expected += 1
00139: 
00140:     return kept, first_frame
00141: 
00142: 
00143: def get_sequence_collection(editor):
00144:     for attr in ("sequences", "strips"):
00145:         collection = getattr(editor, attr, None)
00146:         if collection is not None:
00147:             return collection
00148:     raise AttributeError("SequenceEditor non espone ne 'sequences' ne 'strips'.")
00149: 
00150: 
00151: def all_editor_strips(editor):
00152:     for attr in ("sequences_all", "strips_all", "sequences", "strips"):
00153:         collection = getattr(editor, attr, None)
00154:         if collection is None:
00155:             continue
00156:         try:
00157:             return list(collection)
00158:         except Exception:
00159:             pass
00160:     return []
00161: 
00162: 
00163: def remove_editor_strip(editor, strip):
00164:     for attr in ("sequences", "strips"):
00165:         collection = getattr(editor, attr, None)
00166:         if collection is None or not hasattr(collection, "remove"):
00167:             continue
00168:         try:
00169:             collection.remove(strip)
00170:             return True
00171:         except Exception:
00172:             pass
00173:     return False
00174: 
00175: 
00176: def force_visible_sequencer(scene, editor):
00177:     try:
00178:         bpy.context.window.scene = scene
00179:     except Exception:
00180:         pass
00181: 
00182:     try:
00183:         bpy.context.workspace.sequencer_scene = scene
00184:     except Exception:
00185:         pass
00186: 
00187:     if not ENCODE_SEQUENCE_SWITCH_TO_SEQUENCER:
00188:         return
00189: 
00190:     try:
00191:         area = bpy.context.area
00192:         if area is not None:
00193:             area.type = 'SEQUENCE_EDITOR'
00194:             space = area.spaces.active
00195:             for attr, value in [
00196:                 ("view_type", 'SEQUENCER_PREVIEW'),
00197:                 ("display_mode", 'SEQUENCER_PREVIEW'),
00198:             ]:
00199:                 try:
00200:                     if hasattr(space, attr):
00201:                         setattr(space, attr, value)
00202:                 except Exception:
00203:                     pass
00204:     except Exception:
00205:         pass
00206: 
00207:     try:
00208:         screen = bpy.context.screen
00209:         for area in screen.areas:
00210:             if area.type != 'SEQUENCE_EDITOR':
00211:                 continue
00212:             region = next((r for r in area.regions if r.type == 'WINDOW'), None)
00213:             if region is None:
00214:                 continue
00215:             with bpy.context.temp_override(area=area, region=region, scene=scene):
00216:                 try:
00217:                     bpy.ops.sequencer.view_all()
00218:                 except Exception:
00219:                     pass
00220:     except Exception:
00221:         pass
00222: 
00223: 
00224: def clear_sequence_editor(scene):
00225:     editor = scene.sequence_editor
00226:     if editor is None:
00227:         editor = scene.sequence_editor_create()
00228:         return editor
00229: 
00230:     for strip in all_editor_strips(editor):
00231:         remove_editor_strip(editor, strip)
00232:     return editor
00233: 
00234: 
00235: def add_image_sequence(editor, frame_files):
00236:     collection = get_sequence_collection(editor)
00237:     strip = collection.new_image(
00238:         name="SpaziotempoRenderedFrames",
00239:         filepath=str(frame_files[0]),
00240:         channel=1,
00241:         frame_start=1,
00242:     )
00243: 
00244:     for frame_path in frame_files[1:]:
00245:         try:
00246:             strip.elements.append(frame_path.name)
00247:         except Exception:
00248:             break
00249: 
00250:     try:
00251:         strip.frame_final_duration = len(frame_files)
00252:     except Exception:
00253:         pass
00254: 
00255:     return strip
00256: 
00257: 
00258: def add_synced_audio(editor, first_frame):
00259:     audio_offset_frames = 0
00260:     audio_start_frame = 1
00261:     if ENCODE_SEQUENCE_SYNC_AUDIO_TO_FRAME_NUMBER and first_frame is not None:
00262:         audio_offset_frames = max(0, int(first_frame) - ENCODE_SEQUENCE_AUDIO_ZERO_FRAME)
00263:         audio_start_frame = 1 - audio_offset_frames
00264: 
00265:     collection = get_sequence_collection(editor)
00266:     sound = collection.new_sound(
00267:         name="Feel The Light Audio",
00268:         filepath=str(AUDIO_PATH),
00269:         channel=2,
00270:         frame_start=audio_start_frame,
00271:     )
00272: 
00273:     if audio_offset_frames > 0:
00274:         print(
00275:             "[INFO] Audio sincronizzato: "
00276:             f"frame originale {first_frame}, frame zero audio {ENCODE_SEQUENCE_AUDIO_ZERO_FRAME}, "
00277:             f"audio strip start {audio_start_frame}."
00278:         )
00279:     else:
00280:         print("[INFO] Audio sample avviato dal frame 1 della canzone.")
00281: 
00282:     return sound
00283: 
00284: 
00285: def configure_video_output(scene, frame_count):
00286:     scene.frame_start = 1
00287:     scene.frame_end = frame_count
00288:     scene.render.filepath = str(OUTPUT_MP4)
00289:     scene.render.use_file_extension = True
00290:     scene.render.use_overwrite = True
00291:     scene.render.use_sequencer = True
00292: 
00293:     try:
00294:         scene.render.image_settings.media_type = 'VIDEO'
00295:     except Exception:
00296:         pass
00297:     try:
00298:         scene.render.image_settings.file_format = 'FFMPEG'
00299:         scene.render.image_settings.color_mode = 'RGB'
00300:     except Exception:
00301:         pass
00302: 
00303:     scene.render.ffmpeg.format = 'MPEG4'
00304:     scene.render.ffmpeg.codec = 'H264'
00305:     scene.render.ffmpeg.audio_codec = 'AAC'
00306:     scene.render.ffmpeg.audio_bitrate = AUDIO_BITRATE
00307: 
00308:     for crf in ('PERC_LOSSLESS', 'HIGH'):
00309:         try:
00310:             scene.render.ffmpeg.constant_rate_factor = crf
00311:             break
00312:         except Exception:
00313:             pass
00314:     try:
00315:         scene.render.ffmpeg.ffmpeg_preset = 'GOOD'
00316:     except Exception:
00317:         pass
00318:     try:
00319:         scene.render.ffmpeg.video_bitrate = VIDEO_BITRATE
00320:         scene.render.ffmpeg.maxrate = VIDEO_MAXRATE
00321:         scene.render.ffmpeg.minrate = VIDEO_MINRATE
00322:         scene.render.ffmpeg.buffersize = VIDEO_BUFFERSIZE
00323:     except Exception:
00324:         pass
00325: 
00326: 
00327: def print_strip_report(scene, editor):
00328:     strips = all_editor_strips(editor)
00329:     print(f"[INFO] Scene corrente: {scene.name}")
```
