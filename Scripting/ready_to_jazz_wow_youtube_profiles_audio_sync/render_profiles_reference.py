"""Render profile reference for main_ready_to_jazz_wow_youtube.py.

The executable scene script contains the same FINAL_YOUTUBE/YOUTUBE_RENDER_PROFILES
block inline so it can run standalone in Blender Text Editor.
"""

from pathlib import Path

FINAL_YOUTUBE = "2K_INTERMEDIATE"
OUTPUT_BASE_DIR = Path(r"C:\Users\carmi\blender\renders")
OUTPUT_PROJECT_SLUG = "ready_to_jazz_wow_elastic"
OUTPUT_FRAME_PREFIX = "ready_to_jazz_wow_"

AVAILABLE_PROFILES = [
    "HD_PREVIEW",
    "HD_INTERMEDIATE",
    "HD_FINAL",
    "2K_PREVIEW",
    "2K_INTERMEDIATE",
    "2K_FINAL",
]
