"""Configuration for the generated project AI index."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
INDEX_DIR = ROOT / "indexAI"
PROJECT_INDEX_MD = INDEX_DIR / "project_code_index.md"
PROJECT_MANIFEST_JSON = INDEX_DIR / "project_code_manifest.json"
PROJECT_CHUNK_DIR = INDEX_DIR / "project_code_chunks"
PATCH_LIBRARY_DIR = INDEX_DIR / "patch_library"
README_MD = INDEX_DIR / "README.md"

DEFAULT_MAX_CHUNK_CHARS = 12000
TEXT_SUFFIXES = {".py", ".ps1", ".md", ".json", ".txt", ".cfg", ".ini", ".toml", ".yaml", ".yml"}
EXCLUDE_DIRS = {
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "__pycache__",
    "cache",
    "indexAI",
    "node_modules",
    "output",
    "renders",
    "venv",
    "venvs",
    "old script legacy",
}
EXCLUDE_PARTS = {
    ".npucache",
    "npu_blender_manual_chunks",
    "npu_code_chunks",
    "npu_music_chunks",
}
EXCLUDE_FILE_PREFIXES = {
    ".aider",
    "npu_code_context",
    "npu_code_index",
    "npu_context_for_aider",
    "npu_music_context",
    "npu_music_context_for_aider",
    "npu_dual_ai_chunk_notes",
    "npu_dual_ai_technical_notes",
    "ollama_music_insights",
    "dual_ai_blender_agent_brief",
    "generated_implementation_notes",
}
MEDIA_SUFFIXES = {
    ".wav",
    ".mp3",
    ".flac",
    ".mp4",
    ".mov",
    ".avi",
    ".mkv",
    ".png",
    ".jpg",
    ".jpeg",
    ".exr",
    ".blend",
    ".blend1",
}
