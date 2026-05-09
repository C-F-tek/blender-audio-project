"""Constants for legacy LightFull0To10 compatibility evidence."""
from __future__ import annotations

PROMOTION_JSON = "full0to10_light_profile_promotion.json"
PROMOTION_MD = "full0to10_light_profile_promotion.md"
NEXT_LOOP_JSON = "full0to10_light_profile_next_loop.json"

REQUIRED_STEPS = (
    "startup_guard",
    "track_inputs",
    "repo_quality",
    "markdown_line_limit",
    "accelerator_control",
    "provider_governor",
    "provider_invocation_plan",
    "provider_execution_bridge",
    "provider_telemetry_semantic",
    "memory_visibility_assertion",
    "provider_tool_feedback_loop",
    "final_product_quality_package",
)

SAFETY_FALSE_FIELDS = (
    "provider_execution_performed",
    "patch_application_performed",
    "blender_runtime_execution_performed",
    "ffmpeg_execution_performed",
)

NEXT_LOOP_ACTIONS = (
    "keep LightFull0To10 only as a compatibility alias for unified run evidence",
    "keep NoExternalProbes default for compatibility evidence",
    "add provider telemetry semantic validator",
    "add GPU.0/NPU normalized device visibility check",
    "add provider tool feedback loop report-only",
    "route quality package evidence through the unified run product model",
)
