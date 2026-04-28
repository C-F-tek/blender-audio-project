# Data Flow

## Purpose

This document describes the expected data movement across the Blender audio-reactive workflow.

## High-level flow

```text
Audio file
  -> audio analysis process
  -> JSON analysis data
  -> Blender Python script
  -> generated or tuned Blender scene
  -> render frames
  -> encoded video
```

## Main data categories

| Data | Producer | Consumer | Notes |
|---|---|---|---|
| WAV audio | User or audio production workflow | analysis tools and Blender/VSE | Exact location is local and configurable. |
| Analysis JSON | audio analysis script or AI pipeline | Blender scene script | Schema is not fully specified yet. |
| Music context JSON | AI-assisted music analysis workflow | AI planning and Blender script generation | Used as semantic context. |
| Blender Python script | developer or AI-assisted generator | Blender | Must be inspected before execution. |
| Render frames | Blender render process | FFmpeg or video workflow | Output folder should be configurable. |
| Final video | FFmpeg workflow | publication or review | Codec and settings are workflow-specific. |

## Current known workflow areas

- `Scripting/v61b/` contains the current Blender scripting workflow.
- `Tools/npu/` contains AI/NPU tooling for analysis, review, or implementation support.
- `indexAI/` contains indexed context and patch/task artifacts.

## Rules for AI systems

- Do not overwrite large analysis JSON files unless explicitly requested.
- Treat JSON files as input data unless their generator is known.
- Treat `indexAI/` and `Tools/npu/` files as context or pipeline artifacts.
- Preserve local path configurability.
- Document every new expected input and output.

## Missing formal schemas

The following schemas are not specified yet:

- audio analysis JSON schema;
- music context JSON schema;
- implementation draft JSON schema;
- patch library task packet schema;
- render output manifest schema.

## Recommended next improvement

Create `docs/JSON_SCHEMAS.md` after inspecting representative JSON files from `output/`, `Tools/npu/`, and `indexAI/patch_library/`.
