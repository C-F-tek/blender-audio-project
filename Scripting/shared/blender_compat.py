"""Small Blender compatibility helpers shared by generated scene packages.

This module is intentionally lightweight and additive. It should not import
``bpy`` at module import time, so normal Python validation can still compile it
outside Blender.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any


def require_bpy() -> Any:
    """Import and return bpy, or raise a clear RuntimeError outside Blender."""
    try:
        import bpy  # type: ignore
    except Exception as exc:  # pragma: no cover - executed outside Blender only on failure.
        raise RuntimeError("This helper requires Blender's bpy module and must run inside Blender.") from exc
    return bpy


def get_scene(context: Any | None = None) -> Any:
    """Return the active scene from a Blender context or bpy.context."""
    if context is not None and getattr(context, "scene", None) is not None:
        return context.scene
    bpy = require_bpy()
    return bpy.context.scene


def ensure_sequence_editor(scene: Any | None = None) -> Any:
    """Return a scene sequence editor, creating it when necessary."""
    active_scene = scene or get_scene()
    if getattr(active_scene, "sequence_editor", None) is None:
        active_scene.sequence_editor_create()
    return active_scene.sequence_editor


def clear_sequence_editor(scene: Any | None = None) -> int:
    """Remove all strips from the scene sequence editor and return removed count."""
    editor = ensure_sequence_editor(scene)
    sequences = list(getattr(editor, "sequences_all", None) or getattr(editor, "strips_all", []) or [])
    strip_collection = getattr(editor, "sequences", None) or getattr(editor, "strips", None)
    if strip_collection is None:
        return 0
    for strip in sequences:
        strip_collection.remove(strip)
    return len(sequences)


def create_sound_strip(
    audio_path: str | Path,
    *,
    scene: Any | None = None,
    name: str = "Audio",
    channel: int = 1,
    frame_start: int = 1,
) -> Any:
    """Create a sound strip in the VSE and return the created strip.

    The helper supports the current Blender API path first and falls back to the
    older operator-style API when necessary.
    """
    bpy = require_bpy()
    active_scene = scene or get_scene()
    editor = ensure_sequence_editor(active_scene)
    audio_file = str(Path(audio_path))

    sequences = getattr(editor, "sequences", None) or getattr(editor, "strips", None)
    if sequences is not None and hasattr(sequences, "new_sound"):
        return sequences.new_sound(name=name, filepath=audio_file, channel=channel, frame_start=frame_start)

    bpy.ops.sequencer.sound_strip_add(filepath=audio_file, frame_start=frame_start, channel=channel)
    strip = getattr(active_scene.sequence_editor, "active_strip", None)
    if strip is not None:
        strip.name = name
    return strip


def safe_set_scene_sync_audio(scene: Any | None = None, enabled: bool = True) -> bool:
    """Best-effort scene audio sync toggle.

    Returns True when a known property was set, otherwise False. Blender audio
    sync settings vary across versions and UI contexts, so this helper is
    defensive by design.
    """
    active_scene = scene or get_scene()
    for attr in ("sync_mode", "audio_sync_mode"):
        if hasattr(active_scene, attr):
            try:
                setattr(active_scene, attr, "AUDIO_SYNC" if enabled else "NONE")
                return True
            except Exception:
                continue
    render = getattr(active_scene, "render", None)
    if render is not None and hasattr(render, "use_audio_sync"):
        try:
            render.use_audio_sync = bool(enabled)
            return True
        except Exception:
            return False
    return False


def safe_create_node(node_tree: Any, node_type: str, *, fallback_type: str | None = None) -> Any:
    """Create a node with an optional fallback for Blender API changes."""
    try:
        return node_tree.nodes.new(node_type)
    except Exception:
        if not fallback_type:
            raise
        return node_tree.nodes.new(fallback_type)


def safe_create_noise_texture_node(node_tree: Any) -> Any:
    """Create a noise texture node as Blender 5.x-safe Musgrave replacement."""
    return safe_create_node(node_tree, "ShaderNodeTexNoise")


def set_frame_range_from_seconds(
    duration_seconds: float,
    *,
    scene: Any | None = None,
    fps: int | None = None,
    frame_start: int = 1,
) -> tuple[int, int]:
    """Set scene frame range from duration seconds and return `(start, end)`."""
    active_scene = scene or get_scene()
    effective_fps = int(fps or getattr(active_scene, "fps", None) or getattr(active_scene.render, "fps", 30) or 30)
    frame_end = frame_start + max(1, int(round(float(duration_seconds) * effective_fps))) - 1
    active_scene.frame_start = int(frame_start)
    active_scene.frame_end = int(frame_end)
    return active_scene.frame_start, active_scene.frame_end


def set_render_fps(scene: Any | None = None, fps: int = 30) -> int:
    """Set render FPS and return the normalized value."""
    active_scene = scene or get_scene()
    normalized = int(fps)
    active_scene.render.fps = normalized
    return normalized
