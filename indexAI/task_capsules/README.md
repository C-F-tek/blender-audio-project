# Task Capsules

Task capsules are compact AI-context files.

They are designed to give local or external AI systems precise operational memory without forcing them to read the entire repository on every run.

## Rules

- Capsules are generated or maintained context, not runtime source code.
- Capsules should be small, explicit, and task-specific.
- Capsules may contain guardrails, blocked patterns, preferred APIs, examples, and quality checks.
- Capsules must not include secrets or workstation-only credentials.
- Capsules should be regenerated or reviewed when the related workflow changes.

## Current capsules

| File | Purpose |
|---|---|
| `blender_51_compat.json` | Blender 5.x compatibility guardrails and blocked API patterns. |
| `scene_generation.json` | Package-generation rules for audio-reactive Blender scenes. |
| `audio_mapping.json` | Audio-to-visual mapping strategy for AI-generated scene specs. |

## Recommended usage

Use the capsules as additional context for:

- semantic code retrieval;
- NPU review prompts;
- GPU planner prompts;
- artifact validation;
- patch-plan generation;
- final AI quality review.
