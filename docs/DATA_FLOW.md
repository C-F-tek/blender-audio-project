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
| Agent state packet | `Tools/ai/build_agent_state_packet.py` | app workers, AI agents and guardrail reviewers | Generic packet with selected memory, constraints, budgets and planned CPU/NPU/GPU/validation microtasks. |
| Persistent memory DB | app or agent workflow | agent state packet builder and memory policy reviewer | Optional SQLite store under generated data; do not commit local memory records. |
| Memory policy report | `Tools/ai/review_agent_memory.py` | human review, app policy and validators | Non-destructive retention, quarantine and promotion-candidate report. |
| Blender Python script | developer or AI-assisted generator | Blender | Must be inspected before execution. |
| Render frames | Blender render process | FFmpeg or video workflow | Output folder should be configurable. |
| Final video | FFmpeg workflow | publication or review | Codec and settings are workflow-specific. |

## Current known workflow areas

- `Scripting/v61b/` contains the current Blender scripting workflow.
- `Tools/npu/` contains AI/NPU tooling for analysis, review, or implementation support.
- `Tools/ai/` contains AI artifact validation and generic agent state packet tooling.
- `indexAI/` contains indexed context and patch/task artifacts.

## Rules for AI systems

- Do not overwrite large analysis JSON files unless explicitly requested.
- Treat JSON files as input data unless their generator is known.
- Treat `indexAI/` and `Tools/npu/` files as context or pipeline artifacts.
- Treat local agent memory stores as generated data unless a human promotes a distilled record into documentation.
- Preserve local path configurability.
- Document every new expected input and output.

## Missing formal schemas

`docs/JSON_SCHEMAS.md` exists as a schema-notes file, but the following production schemas are still not fully specified:

- audio analysis JSON schema;
- music context JSON schema;
- implementation draft JSON schema;
- patch library task packet schema;
- render output manifest schema.

## Recommended next improvement

Strengthen `docs/JSON_SCHEMAS.md` after inspecting representative JSON files from `output/`, `Tools/npu/`, and `indexAI/patch_library/`, then add non-destructive validators for the confirmed fields.
