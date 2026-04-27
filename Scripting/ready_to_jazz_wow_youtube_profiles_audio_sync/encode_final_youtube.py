#!/usr/bin/env python3
"""Encode rendered PNG sequence + WAV to YouTube/social-safe MP4.

Run from PowerShell after Blender has rendered the frame sequence:

    python .\encode_final_youtube.py

This script uses explicit Rec.709/bt709 tags and yuv420p.
It also keeps audio in sync when the first rendered frame is not frame 1.
"""
import re
import shutil
import subprocess
from pathlib import Path

FINAL_YOUTUBE = "2K_INTERMEDIATE"  # HD_PREVIEW, HD_INTERMEDIATE, HD_FINAL, 2K_PREVIEW, 2K_INTERMEDIATE, 2K_FINAL
OUTPUT_BASE_DIR = Path(r"C:\Users\carmi\blender\renders")
OUTPUT_PROJECT_SLUG = "ready_to_jazz_wow_elastic"
OUTPUT_FRAME_PREFIX = "ready_to_jazz_wow_"
AUDIO_FILE_NAME = "Ready To Jazz-Luca Vera_Master.wav"
TRACK_STEM = "Ready To Jazz-Luca Vera_Master"
FPS = 30

# Preferisci H264 per massima compatibilita social; SVT_AV1 per master YouTube piu moderno.
ENCODER_PROFILE = "H264_YOUTUBE_SOCIAL"  # H264_YOUTUBE_SOCIAL | CPU_SVTAV1_YOUTUBE | NVENC_AV1_YOUTUBE
CPU_THREADS = 12

PROFILES = {
    "HD_PREVIEW": (1920, 1080, 12000, 16000, 18),
    "HD_INTERMEDIATE": (1920, 1080, 18000, 22000, 17),
    "HD_FINAL": (1920, 1080, 20000, 24000, 16),
    "2K_PREVIEW": (2560, 1440, 16000, 20000, 18),
    "2K_INTERMEDIATE": (2560, 1440, 24000, 30000, 17),
    "2K_FINAL": (2560, 1440, 28000, 34000, 16),
}


def normalize_profile(name: str) -> str:
    name = str(name or "2K_INTERMEDIATE").upper().replace("-", "_").replace(" ", "_")
    aliases = {
        "HD": "HD_FINAL",
        "1080P": "HD_FINAL",
        "2K": "2K_FINAL",
        "1440P": "2K_FINAL",
        "PREVIEW": "HD_PREVIEW",
        "INTERMEDIATE": "2K_INTERMEDIATE",
        "FINAL": "2K_FINAL",
    }
    name = aliases.get(name, name)
    if name not in PROFILES:
        raise SystemExit(f"Profilo sconosciuto: {name}. Profili: {', '.join(PROFILES)}")
    return name


def project_paths(profile: str):
    profile = normalize_profile(profile)
    base = OUTPUT_BASE_DIR / f"{OUTPUT_PROJECT_SLUG}_{profile.lower()}"
    frames = base / "frames"
    mp4 = base / f"{OUTPUT_PROJECT_SLUG}_{profile.lower()}_bt709.mp4"
    return base, frames, mp4


def candidate_audio_paths():
    home = Path.home()
    return [
        Path.cwd() / AUDIO_FILE_NAME,
        Path.cwd().parent / AUDIO_FILE_NAME,
        home / "blender" / "audio" / AUDIO_FILE_NAME,
        home / "blender" / "blender-audio-project" / "audio" / AUDIO_FILE_NAME,
        home / "blender" / "blender-audio-project" / "output" / AUDIO_FILE_NAME,
        home / "Desktop" / AUDIO_FILE_NAME,
        home / "Desktop" / "Living Life In Peace-Luca Vera" / AUDIO_FILE_NAME,
    ]


def find_audio():
    for path in candidate_audio_paths():
        if path.exists():
            return path
    for base in [Path.home() / "blender" / "audio", Path.home() / "Desktop"]:
        if base.exists():
            for ext in ("wav", "flac", "mp3"):
                hits = sorted(base.rglob(f"{TRACK_STEM}*.{ext}"))
                if hits:
                    return hits[0]
    raise FileNotFoundError(f"Audio non trovato: {AUDIO_FILE_NAME}")


def frame_number(path: Path):
    m = re.search(r"(\d+)$", path.stem)
    return int(m.group(1)) if m else None


def find_first_frame(frames_dir: Path):
    files = sorted(frames_dir.glob(f"{OUTPUT_FRAME_PREFIX}*.png"))
    numbered = [(frame_number(p), p) for p in files]
    numbered = [(n, p) for n, p in numbered if n is not None]
    if not numbered:
        raise FileNotFoundError(f"Nessun frame PNG trovato in {frames_dir}")
    numbered.sort(key=lambda x: x[0])
    return numbered[0]


def ffmpeg_exe():
    exe = shutil.which("ffmpeg")
    if exe:
        return exe
    candidates = [
        Path(r"C:\ffmpeg\bin\ffmpeg.exe"),
        Path.home() / "Downloads" / "ffmpeg" / "bin" / "ffmpeg.exe",
        Path.home() / "Desktop" / "ffmpeg" / "bin" / "ffmpeg.exe",
    ]
    for path in candidates:
        if path.exists():
            return str(path)
    raise FileNotFoundError("ffmpeg non trovato nel PATH o nei percorsi standard.")


def audio_offset_seconds(first_number: int, fps: int = FPS) -> float:
    """Return the audio seek offset for a frame sequence that starts after frame 1.

    Frame 1 means audio starts at 0.000s.
    Frame 301 at 30 fps means audio starts at 10.000s.
    """
    try:
        first_number = int(first_number)
        fps = int(fps)
    except Exception:
        return 0.0

    if fps <= 0 or first_number <= 1:
        return 0.0

    return (first_number - 1) / float(fps)



def build_command(ffmpeg, frames_dir, first_number, audio, output, profile):
    width, height, bitrate, maxrate, crf = PROFILES[profile]
    pattern = str(frames_dir / f"{OUTPUT_FRAME_PREFIX}%04d.png")
    audio_offset = audio_offset_seconds(first_number, FPS)
    audio_input_args = []
    if audio_offset > 0:
        audio_input_args.extend(["-ss", f"{audio_offset:.6f}"])

    common = [
        ffmpeg, "-y",
        "-framerate", str(FPS),
        "-start_number", str(first_number),
        "-i", pattern,
        *audio_input_args,
        "-i", str(audio),
        "-map", "0:v:0", "-map", "1:a:0",
        "-vf", "eq=brightness=0.012:contrast=1.012:saturation=1.035,format=yuv420p",
        "-colorspace", "bt709",
        "-color_primaries", "bt709",
        "-color_trc", "bt709",
        "-r", str(FPS),
        "-c:a", "aac", "-b:a", "320k", "-ar", "48000",
        "-movflags", "+faststart",
        "-shortest",
    ]
    if ENCODER_PROFILE == "CPU_SVTAV1_YOUTUBE":
        return common + ["-c:v", "libsvtav1", "-preset", "4", "-crf", "24", "-threads", str(CPU_THREADS), str(output)]
    if ENCODER_PROFILE == "NVENC_AV1_YOUTUBE":
        return common + ["-c:v", "av1_nvenc", "-gpu", "0", "-preset", "p7", "-tune", "hq", "-rc:v", "vbr", "-cq:v", "18", "-b:v", "0", str(output)]
    return common + [
        "-c:v", "libx264",
        "-preset", "slow",
        "-crf", str(crf),
        "-b:v", f"{bitrate}k",
        "-maxrate", f"{maxrate}k",
        "-bufsize", f"{maxrate * 2}k",
        "-profile:v", "high",
        "-level", "5.1",
        "-threads", str(CPU_THREADS),
        str(output),
    ]


def main():
    profile = normalize_profile(FINAL_YOUTUBE)
    base, frames_dir, output = project_paths(profile)
    first_number, first_frame = find_first_frame(frames_dir)
    audio = find_audio()
    output.parent.mkdir(parents=True, exist_ok=True)
    offset = audio_offset_seconds(first_number, FPS)
    cmd = build_command(ffmpeg_exe(), frames_dir, first_number, audio, output, profile)
    print("=" * 72)
    print(f"Profile: {profile}")
    print(f"Frames:  {frames_dir}")
    print(f"First:   {first_frame.name} -> start_number={first_number}")
    print(f"Audio:   {audio}")
    print(f"Offset:  {offset:.6f}s (auto sync from first frame)")
    print(f"Output:  {output}")
    print(f"Encoder: {ENCODER_PROFILE}")
    print("=" * 72)
    subprocess.run(cmd, check=True)
    print(f"[OK] MP4 scritto: {output}")


if __name__ == "__main__":
    main()
