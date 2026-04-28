"""Configuration template for an audio-reactive Blender package.

Copy this folder before using it for a real project.
Do not hardcode private workstation paths unless the package is explicitly local-only.
"""

from pathlib import Path

PACKAGE_DIR = Path(__file__).resolve().parent
INPUT_DIR = PACKAGE_DIR / "inputs"
OUTPUT_DIR = PACKAGE_DIR / "outputs"

# Project identity
PACKAGE_NAME = "_template_audio_reactive_package"
TRACK_TITLE = "not specified"
ARTIST_NAME = "not specified"

# Input paths
AUDIO_PATH = INPUT_DIR / "audio.wav"
TRACK_SUMMARY_JSON = INPUT_DIR / "track_summary.json"
MUSIC_CONTEXT_JSON = INPUT_DIR / "music_context.json"
FULL_ANALYSIS_JSON = None

# Blender timing
FPS = 30
FRAME_START = 1
FRAME_END = None

# Render output
OUTPUT_IMAGE_SEQUENCE_DIR = OUTPUT_DIR / "frames"
OUTPUT_IMAGE_SEQUENCE_PREFIX = "frame_"
IMAGE_SEQUENCE_FORMAT = "PNG"
OUTPUT_VIDEO_PATH = OUTPUT_DIR / "final_video.mp4"

# Render profile
RENDER_PROFILE = "PREVIEW"
RESOLUTION_X = 1920
RESOLUTION_Y = 1080
RENDER_PERCENTAGE = 100

# FFmpeg
FFMPEG_EXE_PATH = ""
FFMPEG_PROFILE = "CPU_SVTAV1"
FFMPEG_THREADS = 12
FFMPEG_AUDIO_BITRATE = "320k"
FFMPEG_AUDIO_SAMPLE_RATE = 48000

# Safety
ALLOW_DESTRUCTIVE_SCENE_CLEAR = True
