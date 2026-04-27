# Project Code Chunk 84/212

- File: `Scripting/v61b_backgood/encode_image_sequence_v61b.py`
- Part: `1`
- Lines: `1-327`

## Symbol Map
- Imports: `re`, `sys`, `from pathlib import Path`, `bpy`, `config`
- Functions: `extract_frame_number(path)` line 67; `sorted_frame_files()` line 74; `contiguous_frame_files(frame_files)` line 100; `get_sequence_collection(editor)` line 127; `all_editor_strips(editor)` line 135; `remove_editor_strip(editor, strip)` line 147; `force_visible_sequencer(scene, editor)` line 160; `clear_sequence_editor(scene)` line 208; `add_image_sequence(editor, frame_files)` line 219; `add_synced_audio(editor, first_frame)` line 242; `configure_video_output(scene, frame_count)` line 268; `print_strip_report(scene, editor)` line 308; `main()` line 323
- Assignments: `SCRIPT_DIR`, `ROOT`, `RENDERS_DIR`, `AUDIO_PATH`, `OUTPUT_MP4`, `OUTPUT_IMAGE_SEQUENCE_DIR`, `OUTPUT_IMAGE_SEQUENCE_PREFIX`, `IMAGE_SEQUENCE_FORMAT`, `VIDEO_BITRATE`, `VIDEO_MAXRATE`, `VIDEO_MINRATE`, `VIDEO_BUFFERSIZE`, `AUDIO_BITRATE`, `ENCODE_SEQUENCE_AUTO_RENDER`, `ENCODE_SEQUENCE_SYNC_AUDIO_TO_FRAME_NUMBER`, `ENCODE_SEQUENCE_SKIP_PLACEHOLDERS`, `ENCODE_SEQUENCE_SWITCH_TO_SEQUENCER`

## Content
```py
00001: import re
00002: import sys
00003: from pathlib import Path
00004: 
00005: import bpy
00006: 
00007: 
00008: SCRIPT_DIR = None
00009: 
00010: try:
00011:     text = bpy.context.space_data.text
00012:     if text is not None and text.filepath:
00013:         SCRIPT_DIR = Path(text.filepath).resolve().parent
00014: except Exception:
00015:     SCRIPT_DIR = None
00016: 
00017: if SCRIPT_DIR is None:
00018:     SCRIPT_DIR = Path.home() / "blender" / "blender-audio-project" / "Scripting" / "v61b"
00019: 
00020: if str(SCRIPT_DIR) not in sys.path:
00021:     sys.path.insert(0, str(SCRIPT_DIR))
00022: 
00023: sys.modules.pop("config", None)
00024: 
00025: import config as cfg  # noqa: E402
00026: 
00027: 
00028: ROOT = getattr(cfg, "ROOT", Path.home() / "blender")
00029: RENDERS_DIR = getattr(cfg, "RENDERS_DIR", ROOT / "renders")
00030: 
00031: AUDIO_PATH = cfg.AUDIO_PATH
00032: OUTPUT_MP4 = getattr(cfg, "OUTPUT_MP4", RENDERS_DIR / "spaziotempo_asset_visual_v61b.mp4")
00033: OUTPUT_IMAGE_SEQUENCE_DIR = getattr(
00034:     cfg,
00035:     "OUTPUT_IMAGE_SEQUENCE_DIR",
00036:     RENDERS_DIR / "spaziotempo_asset_visual_v61b_frames",
00037: )
00038: OUTPUT_IMAGE_SEQUENCE_PREFIX = getattr(
00039:     cfg,
00040:     "OUTPUT_IMAGE_SEQUENCE_PREFIX",
00041:     "spaziotempo_v61b_",
00042: )
00043: IMAGE_SEQUENCE_FORMAT = getattr(cfg, "IMAGE_SEQUENCE_FORMAT", "PNG")
00044: VIDEO_BITRATE = getattr(cfg, "VIDEO_BITRATE", 12000)
00045: VIDEO_MAXRATE = getattr(cfg, "VIDEO_MAXRATE", 16000)
00046: VIDEO_MINRATE = getattr(cfg, "VIDEO_MINRATE", 0)
00047: VIDEO_BUFFERSIZE = getattr(cfg, "VIDEO_BUFFERSIZE", 1792)
00048: AUDIO_BITRATE = getattr(cfg, "AUDIO_BITRATE", 320)
00049: ENCODE_SEQUENCE_AUTO_RENDER = getattr(cfg, "ENCODE_SEQUENCE_AUTO_RENDER", False)
00050: ENCODE_SEQUENCE_SYNC_AUDIO_TO_FRAME_NUMBER = getattr(
00051:     cfg,
00052:     "ENCODE_SEQUENCE_SYNC_AUDIO_TO_FRAME_NUMBER",
00053:     True,
00054: )
00055: ENCODE_SEQUENCE_SKIP_PLACEHOLDERS = getattr(
00056:     cfg,
00057:     "ENCODE_SEQUENCE_SKIP_PLACEHOLDERS",
00058:     True,
00059: )
00060: ENCODE_SEQUENCE_SWITCH_TO_SEQUENCER = getattr(
00061:     cfg,
00062:     "ENCODE_SEQUENCE_SWITCH_TO_SEQUENCER",
00063:     True,
00064: )
00065: 
00066: 
00067: def extract_frame_number(path):
00068:     stem = path.stem
00069:     tail = stem[len(OUTPUT_IMAGE_SEQUENCE_PREFIX):] if stem.startswith(OUTPUT_IMAGE_SEQUENCE_PREFIX) else stem
00070:     match = re.search(r"(\d+)$", tail)
00071:     return int(match.group(1)) if match else None
00072: 
00073: 
00074: def sorted_frame_files():
00075:     ext = ".png" if IMAGE_SEQUENCE_FORMAT.upper() == "PNG" else ""
00076:     pattern = f"{OUTPUT_IMAGE_SEQUENCE_PREFIX}*{ext}" if ext else f"{OUTPUT_IMAGE_SEQUENCE_PREFIX}*"
00077:     files = []
00078: 
00079:     for path in Path(OUTPUT_IMAGE_SEQUENCE_DIR).glob(pattern):
00080:         if not path.is_file():
00081:             continue
00082:         if ENCODE_SEQUENCE_SKIP_PLACEHOLDERS:
00083:             try:
00084:                 if path.stat().st_size <= 0:
00085:                     continue
00086:             except Exception:
00087:                 continue
00088:         files.append(path)
00089: 
00090:     return sorted(
00091:         files,
00092:         key=lambda path: (
00093:             extract_frame_number(path) is None,
00094:             extract_frame_number(path) or 0,
00095:             path.name,
00096:         ),
00097:     )
00098: 
00099: 
00100: def contiguous_frame_files(frame_files):
00101:     if not frame_files:
00102:         return [], None
00103: 
00104:     first_frame = extract_frame_number(frame_files[0])
00105:     if first_frame is None:
00106:         return frame_files, None
00107: 
00108:     kept = [frame_files[0]]
00109:     expected = first_frame + 1
00110: 
00111:     for path in frame_files[1:]:
00112:         frame_number = extract_frame_number(path)
00113:         if frame_number != expected:
00114:             print(
00115:                 "[WARN] Gap nella sequenza: "
00116:                 f"atteso frame {expected}, trovato {frame_number or path.name}. "
00117:                 "Uso solo il blocco continuo iniziale per mantenere sync audio."
00118:             )
00119:             break
00120: 
00121:         kept.append(path)
00122:         expected += 1
00123: 
00124:     return kept, first_frame
00125: 
00126: 
00127: def get_sequence_collection(editor):
00128:     for attr in ("sequences", "strips"):
00129:         collection = getattr(editor, attr, None)
00130:         if collection is not None:
00131:             return collection
00132:     raise AttributeError("SequenceEditor non espone ne 'sequences' ne 'strips'.")
00133: 
00134: 
00135: def all_editor_strips(editor):
00136:     for attr in ("sequences_all", "strips_all", "sequences", "strips"):
00137:         collection = getattr(editor, attr, None)
00138:         if collection is None:
00139:             continue
00140:         try:
00141:             return list(collection)
00142:         except Exception:
00143:             pass
00144:     return []
00145: 
00146: 
00147: def remove_editor_strip(editor, strip):
00148:     for attr in ("sequences", "strips"):
00149:         collection = getattr(editor, attr, None)
00150:         if collection is None or not hasattr(collection, "remove"):
00151:             continue
00152:         try:
00153:             collection.remove(strip)
00154:             return True
00155:         except Exception:
00156:             pass
00157:     return False
00158: 
00159: 
00160: def force_visible_sequencer(scene, editor):
00161:     try:
00162:         bpy.context.window.scene = scene
00163:     except Exception:
00164:         pass
00165: 
00166:     try:
00167:         bpy.context.workspace.sequencer_scene = scene
00168:     except Exception:
00169:         pass
00170: 
00171:     if not ENCODE_SEQUENCE_SWITCH_TO_SEQUENCER:
00172:         return
00173: 
00174:     try:
00175:         area = bpy.context.area
00176:         if area is not None:
00177:             area.type = 'SEQUENCE_EDITOR'
00178:             space = area.spaces.active
00179:             for attr, value in [
00180:                 ("view_type", 'SEQUENCER_PREVIEW'),
00181:                 ("display_mode", 'SEQUENCER_PREVIEW'),
00182:             ]:
00183:                 try:
00184:                     if hasattr(space, attr):
00185:                         setattr(space, attr, value)
00186:                 except Exception:
00187:                     pass
00188:     except Exception:
00189:         pass
00190: 
00191:     try:
00192:         screen = bpy.context.screen
00193:         for area in screen.areas:
00194:             if area.type != 'SEQUENCE_EDITOR':
00195:                 continue
00196:             region = next((r for r in area.regions if r.type == 'WINDOW'), None)
00197:             if region is None:
00198:                 continue
00199:             with bpy.context.temp_override(area=area, region=region, scene=scene):
00200:                 try:
00201:                     bpy.ops.sequencer.view_all()
00202:                 except Exception:
00203:                     pass
00204:     except Exception:
00205:         pass
00206: 
00207: 
00208: def clear_sequence_editor(scene):
00209:     editor = scene.sequence_editor
00210:     if editor is None:
00211:         editor = scene.sequence_editor_create()
00212:         return editor
00213: 
00214:     for strip in all_editor_strips(editor):
00215:         remove_editor_strip(editor, strip)
00216:     return editor
00217: 
00218: 
00219: def add_image_sequence(editor, frame_files):
00220:     collection = get_sequence_collection(editor)
00221:     strip = collection.new_image(
00222:         name="SpaziotempoRenderedFrames",
00223:         filepath=str(frame_files[0]),
00224:         channel=1,
00225:         frame_start=1,
00226:     )
00227: 
00228:     for frame_path in frame_files[1:]:
00229:         try:
00230:             strip.elements.append(frame_path.name)
00231:         except Exception:
00232:             break
00233: 
00234:     try:
00235:         strip.frame_final_duration = len(frame_files)
00236:     except Exception:
00237:         pass
00238: 
00239:     return strip
00240: 
00241: 
00242: def add_synced_audio(editor, first_frame):
00243:     audio_offset_frames = 0
00244:     audio_start_frame = 1
00245:     if ENCODE_SEQUENCE_SYNC_AUDIO_TO_FRAME_NUMBER and first_frame is not None:
00246:         audio_offset_frames = max(0, int(first_frame) - 1)
00247:         audio_start_frame = 1 - audio_offset_frames
00248: 
00249:     collection = get_sequence_collection(editor)
00250:     sound = collection.new_sound(
00251:         name="Feel The Light Audio",
00252:         filepath=str(AUDIO_PATH),
00253:         channel=2,
00254:         frame_start=audio_start_frame,
00255:     )
00256: 
00257:     if audio_offset_frames > 0:
00258:         print(
00259:             "[INFO] Audio sincronizzato: "
00260:             f"frame originale {first_frame}, audio strip start {audio_start_frame}."
00261:         )
00262:     else:
00263:         print("[INFO] Audio sample avviato dal frame 1 della canzone.")
00264: 
00265:     return sound
00266: 
00267: 
00268: def configure_video_output(scene, frame_count):
00269:     scene.frame_start = 1
00270:     scene.frame_end = frame_count
00271:     scene.render.filepath = str(OUTPUT_MP4)
00272:     scene.render.use_file_extension = True
00273:     scene.render.use_overwrite = True
00274:     scene.render.use_sequencer = True
00275: 
00276:     try:
00277:         scene.render.image_settings.media_type = 'VIDEO'
00278:     except Exception:
00279:         pass
00280:     try:
00281:         scene.render.image_settings.file_format = 'FFMPEG'
00282:         scene.render.image_settings.color_mode = 'RGB'
00283:     except Exception:
00284:         pass
00285: 
00286:     scene.render.ffmpeg.format = 'MPEG4'
00287:     scene.render.ffmpeg.codec = 'H264'
00288:     scene.render.ffmpeg.audio_codec = 'AAC'
00289:     scene.render.ffmpeg.audio_bitrate = AUDIO_BITRATE
00290: 
00291:     try:
00292:         scene.render.ffmpeg.constant_rate_factor = 'HIGH'
00293:     except Exception:
00294:         pass
00295:     try:
00296:         scene.render.ffmpeg.ffmpeg_preset = 'GOOD'
00297:     except Exception:
00298:         pass
00299:     try:
00300:         scene.render.ffmpeg.video_bitrate = VIDEO_BITRATE
00301:         scene.render.ffmpeg.maxrate = VIDEO_MAXRATE
00302:         scene.render.ffmpeg.minrate = VIDEO_MINRATE
00303:         scene.render.ffmpeg.buffersize = VIDEO_BUFFERSIZE
00304:     except Exception:
00305:         pass
00306: 
00307: 
00308: def print_strip_report(scene, editor):
00309:     strips = all_editor_strips(editor)
00310:     print(f"[INFO] Scene corrente: {scene.name}")
00311:     print(f"[INFO] Strip nel Video Sequencer: {len(strips)}")
00312:     for strip in strips:
00313:         try:
00314:             print(
00315:                 "[INFO] Strip: "
00316:                 f"{strip.name} | type={strip.type} | channel={strip.channel} | "
00317:                 f"start={strip.frame_start} | duration={strip.frame_final_duration}"
00318:             )
00319:         except Exception:
00320:             print(f"[INFO] Strip: {getattr(strip, 'name', '<senza nome>')}")
00321: 
00322: 
00323: def main():
00324:     print("[INFO] Encode config:")
00325:     print(f"[INFO] Frames dir: {OUTPUT_IMAGE_SEQUENCE_DIR}")
00326:     print(f"[INFO] Prefix:     {OUTPUT_IMAGE_SEQUENCE_PREFIX}")
00327:     print(f"[INFO] Format:     {IMAGE_SEQUENCE_FORMAT}")
```
