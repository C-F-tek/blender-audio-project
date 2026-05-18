"""Configuration for NPU guardrail service."""

from __future__ import annotations

from pathlib import Path

from Tools.npu.provider_mesh._shared.npu_runtime import DEFAULT_MODEL_DIR, DEFAULT_NPU_PYTHON

ROOT = Path(__file__).resolve().parents[3]
DEFAULT_OUT = ROOT / "output" / "ai_pipeline" / "npu_guardrail_report.json"
EVENT_LOG = ROOT / "output" / "workflow_logs" / "npu_guardrail_events.jsonl"

BLOCKED_PATTERNS = {
    "ShaderNodeTexMusgrave": "Musgrave node unavailable in the Blender 5.x target environment.",
    "bpy.ops.wm.open_mainfile": "Generated scripts should not open project files implicitly.",
}
WARNING_PATTERNS = {
    "C:\\Users\\": "Potential hardcoded local Windows user path.",
    "bpy.ops.object.delete": "Scene deletion should be explicit, configurable, and documented.",
    "TODO": "Unresolved TODO marker in AI artifact.",
    "not specified": "Artifact contains unspecified assumptions; review whether they are acceptable.",
}
REQUIRED_IDEAS = ["Blender", "keyframe", "scene", "audio"]
SMART_CONTEXT_IDEAS = ["analysis_blender_keyframes", "scene_script", "selected_capsules"]
INTERMEDIATE_ENRICHMENT_FIELDS = {
    "track_summary": ["duration_sec", "estimated_bpm", "primary_series", "ai_readiness"],
    "music_segments": ["segments", "visual_directive", "estimated_intensity"],
    "audio_event_map": ["peak_events", "beats_sec", "series_used_for_peaks"],
    "scene_brief": [
        "creative_intent",
        "technical_intent",
        "recommended_visual_progression",
        "assumptions",
    ],
    "smart_context_packet": ["selected_capsules", "capsule_manifest", "task", "recommended_inputs"],
}
