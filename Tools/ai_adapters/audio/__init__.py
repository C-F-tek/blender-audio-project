"""Audio-specific AI adapter.

This package converts WAV-derived analysis artifacts into compact, reusable
context objects for AI pipelines. It must not depend on Blender runtime.
"""
from .summaries import build_audio_ai_summary, normalize_audio_analysis, normalize_segments

__all__ = ["build_audio_ai_summary", "normalize_audio_analysis", "normalize_segments"]
