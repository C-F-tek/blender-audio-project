"""Configuration for NPU code-context generation."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT_DIR = ROOT / "Scripting" / "v61b"
OUT_DIR = ROOT / "Tools" / "npu" / "context_artifacts"
OUT_MD = OUT_DIR / "npu_code_context.md"
OUT_INDEX_MD = OUT_DIR / "npu_code_index.md"
OUT_JSON = OUT_DIR / "npu_code_manifest.json"
CHUNK_DIR = OUT_DIR / "npu_code_chunks"
MAX_CHUNK_CHARS = 10500

PRIORITY_FILES = [
    ROOT / "Tools" / "workflow" / "audio_analysis" / "analyzer.py",
    ROOT / "Tools" / "workflow" / "audio_analysis" / "summary.py",
    ROOT / "Tools" / "workflow" / "audio_analysis" / "analyze_cli.py",
    ROOT / "Tools" / "workflow" / "audio_analysis" / "summary_cli.py",
    ROOT / "Tools" / "workflow" / "scene_spec" / "normalizer.py",
    ROOT / "Tools" / "workflow" / "scene_spec" / "cli.py",
    ROOT / "Tools" / "npu" / "_shared" / "npu_runtime.py",
    ROOT / "Tools" / "npu" / "_shared" / "ollama_runtime.py",
    ROOT / "Tools" / "npu" / "build_blender_manual_context" / "cli.py",
    ROOT / "Tools" / "npu" / "dual_ai_pipeline" / "cli.py",
    SCRIPT_DIR / "config.py",
    SCRIPT_DIR / "main_v61b.py",
    SCRIPT_DIR / "animation.py",
    SCRIPT_DIR / "materials.py",
    SCRIPT_DIR / "physics_setup.py",
    SCRIPT_DIR / "fog_dynamics.py",
    SCRIPT_DIR / "fog_filaments.py",
    SCRIPT_DIR / "atmosphere_setup.py",
    SCRIPT_DIR / "world_setup.py",
    SCRIPT_DIR / "render_setup.py",
    SCRIPT_DIR / "scene_tuning_panel.py",
    SCRIPT_DIR / "hot_update_scene_v61b.py",
    SCRIPT_DIR / "encode_image_sequence_v61b.py",
    SCRIPT_DIR / "encode_ffmpeg_v61b.py",
    SCRIPT_DIR / "PROJECT_STRUCTURE.md",
    SCRIPT_DIR / "SCENE_TUNING_GUIDE.md",
]
DISCOVERY_GLOBS = [
    (SCRIPT_DIR, ["*.py", "*.md", "hotpatch/*.py", "spaziotempo/**/*.py"]),
    (ROOT / "Tools" / "npu", ["*.py", "*.ps1"]),
]
EXCLUDE_PARTS = {"__pycache__", ".npucache", "npu_code_chunks"}
TEXT_SUFFIXES = {".py", ".md", ".ps1", ".json", ".txt"}
