# Task Capsules

Task capsules are compact AI context files.

They are not runtime source code. They provide stable guardrails for semantic retrieval, NPU review, GPU planning, validation, and patch generation.

Current capsules:

- `blender_51_compat.json`: Blender 5.x compatibility and blocked API patterns.
- `scene_generation.json`: package-generation rules.
- `audio_mapping.json`: audio-to-visual mapping strategy.
- `resource_budget.json`: local CPU/GPU/NPU resource policy.
