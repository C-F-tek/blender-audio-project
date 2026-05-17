import importlib
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

try:
    import bpy
except Exception:
    bpy = None


def resolve_script_dir():
    candidates = []

    if bpy is not None:
        try:
            text = bpy.context.space_data.text
            if text is not None and text.filepath:
                candidates.append(Path(text.filepath).resolve().parent)
        except Exception:
            pass

    if "__file__" in globals():
        try:
            candidates.append(Path(__file__).resolve().parent)
        except Exception:
            pass

    candidates.append(Path.home() / "blender" / "blender-audio-project" / "Scripting" / "v61b")

    for candidate in candidates:
        if (candidate / "config.py").exists():
            return candidate

    return candidates[-1]


SCRIPT_DIR = resolve_script_dir()

if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

cfg = importlib.import_module("config")
cfg = importlib.reload(cfg)


AUDIO_PATH = cfg.AUDIO_PATH
ANALYSIS_JSON_PATH = getattr(cfg, "ANALYSIS_JSON_PATH", None)
OUTPUT_IMAGE_SEQUENCE_DIR = cfg.OUTPUT_IMAGE_SEQUENCE_DIR
OUTPUT_IMAGE_SEQUENCE_PREFIX = getattr(cfg, "OUTPUT_IMAGE_SEQUENCE_PREFIX", "spaziotempo_v61b_")
IMAGE_SEQUENCE_FORMAT = getattr(cfg, "IMAGE_SEQUENCE_FORMAT", "PNG")
OUTPUT_MP4 = getattr(cfg, "FFMPEG_OUTPUT_MP4", cfg.OUTPUT_MP4)
FFMPEG_EXE_PATH = getattr(cfg, "FFMPEG_EXE_PATH", "")
FFMPEG_CRF = int(getattr(cfg, "FFMPEG_CRF", 17))
FFMPEG_PRESET = str(getattr(cfg, "FFMPEG_PRESET", "slow"))
FFMPEG_TUNE = str(getattr(cfg, "FFMPEG_TUNE", "film"))
FFMPEG_AUDIO_BITRATE = str(getattr(cfg, "FFMPEG_AUDIO_BITRATE", "320k"))
FFMPEG_PROFILE = str(getattr(cfg, "FFMPEG_PROFILE", "X264_HIGH_QUALITY")).upper()
FFMPEG_GPU_INDEX = int(getattr(cfg, "FFMPEG_GPU_INDEX", 0))
FFMPEG_NVENC_PRESET = str(getattr(cfg, "FFMPEG_NVENC_PRESET", "p7"))
FFMPEG_NVENC_TUNE = str(getattr(cfg, "FFMPEG_NVENC_TUNE", "hq"))
FFMPEG_NVENC_CQ = int(getattr(cfg, "FFMPEG_NVENC_CQ", 18))
FFMPEG_SVTAV1_PRESET = int(getattr(cfg, "FFMPEG_SVTAV1_PRESET", 4))
FFMPEG_SVTAV1_CRF = int(getattr(cfg, "FFMPEG_SVTAV1_CRF", 24))
FFMPEG_THREADS = int(getattr(cfg, "FFMPEG_THREADS", 12))
FFMPEG_VIDEO_FILTER = str(getattr(cfg, "FFMPEG_VIDEO_FILTER", "") or "")
FFMPEG_AUDIO_SAMPLE_RATE = int(getattr(cfg, "FFMPEG_AUDIO_SAMPLE_RATE", 48000))
SYNC_AUDIO = bool(getattr(cfg, "ENCODE_SEQUENCE_SYNC_AUDIO_TO_FRAME_NUMBER", True))
AUDIO_ZERO_FRAME = int(getattr(cfg, "ENCODE_SEQUENCE_AUDIO_ZERO_FRAME", 1))
SKIP_PLACEHOLDERS = bool(getattr(cfg, "ENCODE_SEQUENCE_SKIP_PLACEHOLDERS", True))
LAUNCH_VISIBLE_SHELL = bool(
    globals().get(
        "FFMPEG_LAUNCH_VISIBLE_SHELL",
        getattr(cfg, "FFMPEG_LAUNCH_VISIBLE_SHELL", False),
    )
)


def extract_frame_number(path):
    stem = path.stem
    tail = (
        stem[len(OUTPUT_IMAGE_SEQUENCE_PREFIX) :]
        if stem.startswith(OUTPUT_IMAGE_SEQUENCE_PREFIX)
        else stem
    )
    match = re.search(r"(\d+)$", tail)
    return int(match.group(1)) if match else None


def sorted_frame_files():
    ext = ".png" if IMAGE_SEQUENCE_FORMAT.upper() == "PNG" else f".{IMAGE_SEQUENCE_FORMAT.lower()}"
    pattern = f"{OUTPUT_IMAGE_SEQUENCE_PREFIX}*{ext}"
    files = []
    for path in Path(OUTPUT_IMAGE_SEQUENCE_DIR).glob(pattern):
        if not path.is_file():
            continue
        if SKIP_PLACEHOLDERS and path.stat().st_size <= 0:
            continue
        files.append(path)
    return sorted(
        files,
        key=lambda path: (
            extract_frame_number(path) is None,
            extract_frame_number(path) or 0,
            path.name,
        ),
    )


def contiguous_frame_files(frame_files):
    if not frame_files:
        return [], None

    first_frame = extract_frame_number(frame_files[0])
    if first_frame is None:
        return frame_files, None

    kept = [frame_files[0]]
    expected = first_frame + 1
    for path in frame_files[1:]:
        frame_number = extract_frame_number(path)
        if frame_number != expected:
            print(
                "[WARN] Gap nella sequenza: "
                f"atteso frame {expected}, trovato {frame_number or path.name}. "
                "Uso solo il blocco continuo iniziale."
            )
            break
        kept.append(path)
        expected += 1
    return kept, first_frame


def get_fps():
    override = getattr(cfg, "FPS_OVERRIDE", None)
    if override:
        return float(override)

    if bpy is not None:
        try:
            fps_base = float(getattr(bpy.context.scene.render, "fps_base", 1.0) or 1.0)
            return float(bpy.context.scene.render.fps) / fps_base
        except Exception:
            pass

    if ANALYSIS_JSON_PATH and Path(ANALYSIS_JSON_PATH).exists():
        try:
            data = json.loads(Path(ANALYSIS_JSON_PATH).read_text(encoding="utf-8"))
            return float(data.get("meta", {}).get("fps", 30.0))
        except Exception:
            pass

    return 30.0


def candidate_path_values():
    values = []
    if FFMPEG_EXE_PATH:
        values.append(Path(FFMPEG_EXE_PATH))

    found = shutil.which("ffmpeg")
    if found:
        values.append(Path(found))

    values.append(Path("C:/ProgramData/chocolatey/bin/ffmpeg.exe"))
    values.append(Path("C:/ffmpeg/bin/ffmpeg.exe"))

    for env_name in ("PATH", "Path"):
        for part in os.environ.get(env_name, "").split(os.pathsep):
            if part:
                values.append(Path(part) / "ffmpeg.exe")

    return values


def find_ffmpeg():
    for path in candidate_path_values():
        try:
            if path.exists() and path.name.lower() in {"ffmpeg.exe", "ffmpeg"}:
                return path
        except Exception:
            pass

    search_roots = [
        Path.home() / "Desktop",
        Path.home() / "Downloads",
        Path.home() / "AppData" / "Local" / "Microsoft" / "WinGet" / "Packages",
    ]
    for root in search_roots:
        if not root.exists():
            continue
        try:
            match = next(root.glob("**/ffmpeg.exe"), None)
        except Exception:
            match = None
        if match is not None:
            return match

    raise FileNotFoundError(
        "ffmpeg.exe non trovato. Imposta FFMPEG_EXE_PATH in config.py oppure riapri Blender dopo aver aggiornato il PATH."
    )


def build_image_pattern(first_file, first_frame):
    if first_frame is None:
        raise ValueError("I frame devono avere un numero finale nel nome per l'encoding ffmpeg.")

    match = re.search(r"(\d+)$", first_file.stem)
    if match is None:
        raise ValueError(f"Numero frame non trovato in: {first_file.name}")

    digits = match.group(1)
    stem_prefix = first_file.stem[: -len(digits)]
    return str(first_file.with_name(f"{stem_prefix}%0{len(digits)}d{first_file.suffix}"))


def source_frame_to_audio_offset(first_frame, fps):
    if not SYNC_AUDIO or first_frame is None:
        return 0.0
    return max(0.0, (float(first_frame) - float(AUDIO_ZERO_FRAME)) / float(fps))


def build_command(ffmpeg, pattern, first_frame, frame_count, fps, audio_offset):
    output = Path(OUTPUT_MP4)
    output.parent.mkdir(parents=True, exist_ok=True)

    command = [
        str(ffmpeg),
        "-y",
        "-hide_banner",
        "-stats",
        "-stats_period",
        "0.5",
        "-framerate",
        f"{fps:.6f}",
        "-start_number",
        str(first_frame),
        "-i",
        pattern,
    ]

    if audio_offset > 0:
        command.extend(["-ss", f"{audio_offset:.6f}"])
    command.extend(["-i", str(AUDIO_PATH)])

    if FFMPEG_VIDEO_FILTER:
        command.extend(["-vf", FFMPEG_VIDEO_FILTER])

    command.extend(
        [
            "-frames:v",
            str(frame_count),
            "-map",
            "0:v:0",
            "-map",
            "1:a:0",
        ]
    )

    if FFMPEG_PROFILE in {"GPU_AV1_YOUTUBE_SAFE", "GPU_AV1_NVENC", "AV1_NVENC"}:
        command.extend(
            [
                "-c:v",
                "av1_nvenc",
                "-gpu",
                str(FFMPEG_GPU_INDEX),
                "-preset",
                FFMPEG_NVENC_PRESET,
                "-tune",
                FFMPEG_NVENC_TUNE,
                "-rc:v",
                "vbr",
                "-cq:v",
                str(FFMPEG_NVENC_CQ),
                "-b:v",
                "0",
            ]
        )
    elif FFMPEG_PROFILE in {"CPU_SVTAV1_YOUTUBE", "CPU_SVTAV1", "SVTAV1"}:
        command.extend(
            [
                "-threads",
                str(FFMPEG_THREADS),
                "-c:v",
                "libsvtav1",
                "-preset",
                str(FFMPEG_SVTAV1_PRESET),
                "-crf",
                str(FFMPEG_SVTAV1_CRF),
                "-svtav1-params",
                f"lp={FFMPEG_THREADS}",
            ]
        )
    else:
        command.extend(
            [
                "-threads",
                str(FFMPEG_THREADS),
                "-c:v",
                "libx264",
                "-preset",
                FFMPEG_PRESET,
                "-tune",
                FFMPEG_TUNE,
                "-crf",
                str(FFMPEG_CRF),
                "-profile:v",
                "high",
            ]
        )

    command.extend(
        [
            "-pix_fmt",
            "yuv420p",
            "-colorspace",
            "bt709",
            "-color_primaries",
            "bt709",
            "-color_trc",
            "bt709",
            "-r",
            f"{fps:.6f}",
            "-c:a",
            "aac",
            "-ar",
            str(FFMPEG_AUDIO_SAMPLE_RATE),
            "-b:a",
            FFMPEG_AUDIO_BITRATE,
            "-shortest",
            "-movflags",
            "+faststart",
            str(output),
        ]
    )
    return command
