"""Constants for NPU knowledge broker packets."""

from __future__ import annotations

PACKET_KIND = "npu_knowledge_broker_packet"
APPLY_MODE = "context_only"
NPU_ROLE = "knowledge_broker_context_oracle"

FORBIDDEN_PREFIXES = (
    ".git/",
    ".venv/",
    "venv/",
    "indexAI/agent_memory/",
    "output/patch_specs/",
    "Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/",
)
FORBIDDEN_EXACT = {"Scripting/shared/blender_compat.py"}
FORBIDDEN_FRAGMENTS = ("full_analysis", "analysis_full")
