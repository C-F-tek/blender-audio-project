# Project Code Chunk 25/212

- File: `Scripting/v61b/encode_ffmpeg_v61b.py`
- Part: `1`
- Lines: `1-322`

## Symbol Map
- Imports: `json`, `os`, `re`, `shutil`, `subprocess`, `sys`, `from pathlib import Path`, `config`
- Functions: `resolve_script_dir()` line 15; `extract_frame_number(path)` line 82; `sorted_frame_files()` line 89; `contiguous_frame_files(frame_files)` line 109; `get_fps()` line 133; `candidate_path_values()` line 155; `find_ffmpeg()` line 175; `build_image_pattern(first_file, first_frame)` line 203; `source_frame_to_audio_offset(first_frame, fps)` line 216; `build_command(ffmpeg, pattern, first_frame, frame_count, fps, audio_offset)` line 222; `write_visible_shell_launcher(command, output, first_frame, frame_count, fps, audio_offset)` line 328; `launch_visible_shell(command, output, first_frame, frame_count, fps, audio_offset)` line 355; `main()` line 362
- Assignments: `SCRIPT_DIR`, `AUDIO_PATH`, `ANALYSIS_JSON_PATH`, `OUTPUT_IMAGE_SEQUENCE_DIR`, `OUTPUT_IMAGE_SEQUENCE_PREFIX`, `IMAGE_SEQUENCE_FORMAT`, `OUTPUT_MP4`, `FFMPEG_EXE_PATH`, `FFMPEG_CRF`, `FFMPEG_PRESET`, `FFMPEG_TUNE`, `FFMPEG_AUDIO_BITRATE`, `FFMPEG_PROFILE`, `FFMPEG_GPU_INDEX`, `FFMPEG_NVENC_PRESET`, `FFMPEG_NVENC_TUNE`, `FFMPEG_NVENC_CQ`, `FFMPEG_SVTAV1_PRESET`, `FFMPEG_SVTAV1_CRF`, `FFMPEG_THREADS`, `FFMPEG_VIDEO_FILTER`, `FFMPEG_AUDIO_SAMPLE_RATE`, `SYNC_AUDIO`, `AUDIO_ZERO_FRAME`, `SKIP_PLACEHOLDERS`, `LAUNCH_VISIBLE_SHELL`

## Content
```py
00001: import json
00002: import os
00003: import re
00004: import shutil
00005: import subprocess
00006: import sys
00007: from pathlib import Path
00008: 
00009: try:
00010:     import bpy
00011: except Exception:
00012:     bpy = None
00013: 
00014: 
00015: def resolve_script_dir():
00016:     candidates = []
00017: 
00018:     if bpy is not None:
00019:         try:
00020:             text = bpy.context.space_data.text
00021:             if text is not None and text.filepath:
00022:                 candidates.append(Path(text.filepath).resolve().parent)
00023:         except Exception:
00024:             pass
00025: 
00026:     if "__file__" in globals():
00027:         try:
00028:             candidates.append(Path(__file__).resolve().parent)
00029:         except Exception:
00030:             pass
00031: 
00032:     candidates.append(Path.home() / "blender" / "blender-audio-project" / "Scripting" / "v61b")
00033: 
00034:     for candidate in candidates:
00035:         if (candidate / "config.py").exists():
00036:             return candidate
00037: 
00038:     return candidates[-1]
00039: 
00040: 
00041: SCRIPT_DIR = resolve_script_dir()
00042: 
00043: if str(SCRIPT_DIR) not in sys.path:
00044:     sys.path.insert(0, str(SCRIPT_DIR))
00045: 
00046: sys.modules.pop("config", None)
00047: import config as cfg  # noqa: E402
00048: 
00049: 
00050: AUDIO_PATH = cfg.AUDIO_PATH
00051: ANALYSIS_JSON_PATH = getattr(cfg, "ANALYSIS_JSON_PATH", None)
00052: OUTPUT_IMAGE_SEQUENCE_DIR = getattr(cfg, "OUTPUT_IMAGE_SEQUENCE_DIR")
00053: OUTPUT_IMAGE_SEQUENCE_PREFIX = getattr(cfg, "OUTPUT_IMAGE_SEQUENCE_PREFIX", "spaziotempo_v61b_")
00054: IMAGE_SEQUENCE_FORMAT = getattr(cfg, "IMAGE_SEQUENCE_FORMAT", "PNG")
00055: OUTPUT_MP4 = getattr(cfg, "FFMPEG_OUTPUT_MP4", getattr(cfg, "OUTPUT_MP4"))
00056: FFMPEG_EXE_PATH = getattr(cfg, "FFMPEG_EXE_PATH", "")
00057: FFMPEG_CRF = int(getattr(cfg, "FFMPEG_CRF", 17))
00058: FFMPEG_PRESET = str(getattr(cfg, "FFMPEG_PRESET", "slow"))
00059: FFMPEG_TUNE = str(getattr(cfg, "FFMPEG_TUNE", "film"))
00060: FFMPEG_AUDIO_BITRATE = str(getattr(cfg, "FFMPEG_AUDIO_BITRATE", "320k"))
00061: FFMPEG_PROFILE = str(getattr(cfg, "FFMPEG_PROFILE", "X264_HIGH_QUALITY")).upper()
00062: FFMPEG_GPU_INDEX = int(getattr(cfg, "FFMPEG_GPU_INDEX", 0))
00063: FFMPEG_NVENC_PRESET = str(getattr(cfg, "FFMPEG_NVENC_PRESET", "p7"))
00064: FFMPEG_NVENC_TUNE = str(getattr(cfg, "FFMPEG_NVENC_TUNE", "hq"))
00065: FFMPEG_NVENC_CQ = int(getattr(cfg, "FFMPEG_NVENC_CQ", 18))
00066: FFMPEG_SVTAV1_PRESET = int(getattr(cfg, "FFMPEG_SVTAV1_PRESET", 4))
00067: FFMPEG_SVTAV1_CRF = int(getattr(cfg, "FFMPEG_SVTAV1_CRF", 24))
00068: FFMPEG_THREADS = int(getattr(cfg, "FFMPEG_THREADS", 12))
00069: FFMPEG_VIDEO_FILTER = str(getattr(cfg, "FFMPEG_VIDEO_FILTER", "") or "")
00070: FFMPEG_AUDIO_SAMPLE_RATE = int(getattr(cfg, "FFMPEG_AUDIO_SAMPLE_RATE", 48000))
00071: SYNC_AUDIO = bool(getattr(cfg, "ENCODE_SEQUENCE_SYNC_AUDIO_TO_FRAME_NUMBER", True))
00072: AUDIO_ZERO_FRAME = int(getattr(cfg, "ENCODE_SEQUENCE_AUDIO_ZERO_FRAME", 1))
00073: SKIP_PLACEHOLDERS = bool(getattr(cfg, "ENCODE_SEQUENCE_SKIP_PLACEHOLDERS", True))
00074: LAUNCH_VISIBLE_SHELL = bool(
00075:     globals().get(
00076:         "FFMPEG_LAUNCH_VISIBLE_SHELL",
00077:         getattr(cfg, "FFMPEG_LAUNCH_VISIBLE_SHELL", False),
00078:     )
00079: )
00080: 
00081: 
00082: def extract_frame_number(path):
00083:     stem = path.stem
00084:     tail = stem[len(OUTPUT_IMAGE_SEQUENCE_PREFIX):] if stem.startswith(OUTPUT_IMAGE_SEQUENCE_PREFIX) else stem
00085:     match = re.search(r"(\d+)$", tail)
00086:     return int(match.group(1)) if match else None
00087: 
00088: 
00089: def sorted_frame_files():
00090:     ext = ".png" if IMAGE_SEQUENCE_FORMAT.upper() == "PNG" else f".{IMAGE_SEQUENCE_FORMAT.lower()}"
00091:     pattern = f"{OUTPUT_IMAGE_SEQUENCE_PREFIX}*{ext}"
00092:     files = []
00093:     for path in Path(OUTPUT_IMAGE_SEQUENCE_DIR).glob(pattern):
00094:         if not path.is_file():
00095:             continue
00096:         if SKIP_PLACEHOLDERS and path.stat().st_size <= 0:
00097:             continue
00098:         files.append(path)
00099:     return sorted(
00100:         files,
00101:         key=lambda path: (
00102:             extract_frame_number(path) is None,
00103:             extract_frame_number(path) or 0,
00104:             path.name,
00105:         ),
00106:     )
00107: 
00108: 
00109: def contiguous_frame_files(frame_files):
00110:     if not frame_files:
00111:         return [], None
00112: 
00113:     first_frame = extract_frame_number(frame_files[0])
00114:     if first_frame is None:
00115:         return frame_files, None
00116: 
00117:     kept = [frame_files[0]]
00118:     expected = first_frame + 1
00119:     for path in frame_files[1:]:
00120:         frame_number = extract_frame_number(path)
00121:         if frame_number != expected:
00122:             print(
00123:                 "[WARN] Gap nella sequenza: "
00124:                 f"atteso frame {expected}, trovato {frame_number or path.name}. "
00125:                 "Uso solo il blocco continuo iniziale."
00126:             )
00127:             break
00128:         kept.append(path)
00129:         expected += 1
00130:     return kept, first_frame
00131: 
00132: 
00133: def get_fps():
00134:     override = getattr(cfg, "FPS_OVERRIDE", None)
00135:     if override:
00136:         return float(override)
00137: 
00138:     if bpy is not None:
00139:         try:
00140:             fps_base = float(getattr(bpy.context.scene.render, "fps_base", 1.0) or 1.0)
00141:             return float(bpy.context.scene.render.fps) / fps_base
00142:         except Exception:
00143:             pass
00144: 
00145:     if ANALYSIS_JSON_PATH and Path(ANALYSIS_JSON_PATH).exists():
00146:         try:
00147:             data = json.loads(Path(ANALYSIS_JSON_PATH).read_text(encoding="utf-8"))
00148:             return float(data.get("meta", {}).get("fps", 30.0))
00149:         except Exception:
00150:             pass
00151: 
00152:     return 30.0
00153: 
00154: 
00155: def candidate_path_values():
00156:     values = []
00157:     if FFMPEG_EXE_PATH:
00158:         values.append(Path(FFMPEG_EXE_PATH))
00159: 
00160:     found = shutil.which("ffmpeg")
00161:     if found:
00162:         values.append(Path(found))
00163: 
00164:     values.append(Path("C:/ProgramData/chocolatey/bin/ffmpeg.exe"))
00165:     values.append(Path("C:/ffmpeg/bin/ffmpeg.exe"))
00166: 
00167:     for env_name in ("PATH", "Path"):
00168:         for part in os.environ.get(env_name, "").split(os.pathsep):
00169:             if part:
00170:                 values.append(Path(part) / "ffmpeg.exe")
00171: 
00172:     return values
00173: 
00174: 
00175: def find_ffmpeg():
00176:     for path in candidate_path_values():
00177:         try:
00178:             if path.exists() and path.name.lower() in {"ffmpeg.exe", "ffmpeg"}:
00179:                 return path
00180:         except Exception:
00181:             pass
00182: 
00183:     search_roots = [
00184:         Path.home() / "Desktop",
00185:         Path.home() / "Downloads",
00186:         Path.home() / "AppData" / "Local" / "Microsoft" / "WinGet" / "Packages",
00187:     ]
00188:     for root in search_roots:
00189:         if not root.exists():
00190:             continue
00191:         try:
00192:             match = next(root.glob("**/ffmpeg.exe"), None)
00193:         except Exception:
00194:             match = None
00195:         if match is not None:
00196:             return match
00197: 
00198:     raise FileNotFoundError(
00199:         "ffmpeg.exe non trovato. Imposta FFMPEG_EXE_PATH in config.py oppure riapri Blender dopo aver aggiornato il PATH."
00200:     )
00201: 
00202: 
00203: def build_image_pattern(first_file, first_frame):
00204:     if first_frame is None:
00205:         raise ValueError("I frame devono avere un numero finale nel nome per l'encoding ffmpeg.")
00206: 
00207:     match = re.search(r"(\d+)$", first_file.stem)
00208:     if match is None:
00209:         raise ValueError(f"Numero frame non trovato in: {first_file.name}")
00210: 
00211:     digits = match.group(1)
00212:     stem_prefix = first_file.stem[: -len(digits)]
00213:     return str(first_file.with_name(f"{stem_prefix}%0{len(digits)}d{first_file.suffix}"))
00214: 
00215: 
00216: def source_frame_to_audio_offset(first_frame, fps):
00217:     if not SYNC_AUDIO or first_frame is None:
00218:         return 0.0
00219:     return max(0.0, (float(first_frame) - float(AUDIO_ZERO_FRAME)) / float(fps))
00220: 
00221: 
00222: def build_command(ffmpeg, pattern, first_frame, frame_count, fps, audio_offset):
00223:     output = Path(OUTPUT_MP4)
00224:     output.parent.mkdir(parents=True, exist_ok=True)
00225: 
00226:     command = [
00227:         str(ffmpeg),
00228:         "-y",
00229:         "-hide_banner",
00230:         "-stats",
00231:         "-stats_period",
00232:         "0.5",
00233:         "-framerate",
00234:         f"{fps:.6f}",
00235:         "-start_number",
00236:         str(first_frame),
00237:         "-i",
00238:         pattern,
00239:     ]
00240: 
00241:     if audio_offset > 0:
00242:         command.extend(["-ss", f"{audio_offset:.6f}"])
00243:     command.extend(["-i", str(AUDIO_PATH)])
00244: 
00245:     if FFMPEG_VIDEO_FILTER:
00246:         command.extend(["-vf", FFMPEG_VIDEO_FILTER])
00247: 
00248:     command.extend([
00249:         "-frames:v",
00250:         str(frame_count),
00251:         "-map",
00252:         "0:v:0",
00253:         "-map",
00254:         "1:a:0",
00255:     ])
00256: 
00257:     if FFMPEG_PROFILE in {"GPU_AV1_YOUTUBE_SAFE", "GPU_AV1_NVENC", "AV1_NVENC"}:
00258:         command.extend([
00259:             "-c:v",
00260:             "av1_nvenc",
00261:             "-gpu",
00262:             str(FFMPEG_GPU_INDEX),
00263:             "-preset",
00264:             FFMPEG_NVENC_PRESET,
00265:             "-tune",
00266:             FFMPEG_NVENC_TUNE,
00267:             "-rc:v",
00268:             "vbr",
00269:             "-cq:v",
00270:             str(FFMPEG_NVENC_CQ),
00271:             "-b:v",
00272:             "0",
00273:         ])
00274:     elif FFMPEG_PROFILE in {"CPU_SVTAV1_YOUTUBE", "CPU_SVTAV1", "SVTAV1"}:
00275:         command.extend([
00276:             "-threads",
00277:             str(FFMPEG_THREADS),
00278:             "-c:v",
00279:             "libsvtav1",
00280:             "-preset",
00281:             str(FFMPEG_SVTAV1_PRESET),
00282:             "-crf",
00283:             str(FFMPEG_SVTAV1_CRF),
00284:             "-svtav1-params",
00285:             f"lp={FFMPEG_THREADS}",
00286:         ])
00287:     else:
00288:         command.extend([
00289:             "-threads",
00290:             str(FFMPEG_THREADS),
00291:             "-c:v",
00292:             "libx264",
00293:             "-preset",
00294:             FFMPEG_PRESET,
00295:             "-tune",
00296:             FFMPEG_TUNE,
00297:             "-crf",
00298:             str(FFMPEG_CRF),
00299:             "-profile:v",
00300:             "high",
00301:         ])
00302: 
00303:     command.extend([
00304:         "-pix_fmt",
00305:         "yuv420p",
00306:         "-colorspace",
00307:         "bt709",
00308:         "-color_primaries",
00309:         "bt709",
00310:         "-color_trc",
00311:         "bt709",
00312:         "-r",
00313:         f"{fps:.6f}",
00314:         "-c:a",
00315:         "aac",
00316:         "-ar",
00317:         str(FFMPEG_AUDIO_SAMPLE_RATE),
00318:         "-b:a",
00319:         FFMPEG_AUDIO_BITRATE,
00320:         "-shortest",
00321:         "-movflags",
00322:         "+faststart",
```
