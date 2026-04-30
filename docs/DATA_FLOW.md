# Data Flow

## Purpose

This document describes expected data movement across the current Blender audio-reactive workflow and the reusable AI/NPU artifact workflow.

The current concrete production target is Blender, and the current concrete input family is audio/WAV analysis. The reusable pipeline boundary is broader:

```text
input-domain data
  -> context or technical analysis
  -> AI/helper planning payload
  -> generated artifact contract
  -> validation reports
  -> controlled runtime execution only after explicit validation
```

## High-level current Blender flow

```text
Audio file
  -> audio analysis process
  -> JSON analysis data
  -> music context / scene specification
  -> Blender Python script or package
  -> generated or tuned Blender scene
  -> render frames
  -> encoded video
```

## High-level reusable AI/NPU helper flow

```text
Project context and optional domain data
  -> bounded context bundle
  -> prompt payload or provider request descriptor
  -> model/provider result envelope or planned-only result
  -> implementation draft / generated artifact plan
  -> contract validation
  -> generated artifact path validation
  -> local validation report
  -> index regeneration after accepted structural changes
```

Current PR #41 keeps this flow helper-only. It does not execute NPU/Ollama providers and does not wire helpers into `Tools/npu/run_dual_ai_pipeline.py`.

## Main data categories

| Data | Producer | Consumer | Notes |
|---|---|---|---|
| WAV audio | User or audio production workflow | analysis tools and Blender/VSE | Exact location is local and configurable. |
| Analysis JSON | audio analysis script or AI pipeline | Blender scene script and music context builders | Full frame-level JSON must not be overwritten casually. |
| Music context JSON | AI-assisted music analysis workflow or fixture/helper builder | AI planning, prompt payloads and Blender script generation | Used as semantic context; schema remains partially specified. |
| Bounded context bundle | `Tools/npu/pipeline/context_builder.py` | prompt payload builders and future NPU/Ollama orchestration | Clips large text inputs deterministically before provider execution. |
| Prompt payload | `Tools/npu/pipeline/prompts.py` | future provider adapters or dry-run tests | Pure data structure; does not call providers. |
| Provider request descriptor | `Tools/npu/pipeline/providers.py` | future provider adapters and validator tests | Planned-only envelope in current helper package. |
| Provider result envelope | `Tools/npu/pipeline/providers.py` | future response parsing, validators and artifact writers | Current helper can produce non-executed planned results only. |
| Implementation draft JSON | AI/NPU pipeline or fixture helpers | validators and artifact planners | Unknown future fields should be preserved unless a contract says otherwise. |
| Generated artifact plan | `Tools/npu/pipeline/artifact_writer.py` or AI pipeline | generated artifact validators and human review | Writes must stay inside allowed generated destinations. |
| Legacy dual-AI runtime output policy | `Tools/npu/pipeline/artifact_paths.py` | `Tools/npu/run_dual_ai_pipeline.py` and helper validators | Exact known legacy outputs are allowed without broadening generated-file prefixes into source folders. |
| Provider preflight report | `Tools/npu/pipeline/providers.py` | dual-AI runtime and validation reports | Normalized report only; provider/model execution remains a later adapter phase. |
| NPU helper validation reports | `Tools/validation/check_npu_pipeline_*.py` | maintainer, PR review and future runtime-wiring gates | No Blender, NPU, GPU, Ollama, FFmpeg or provider execution. |
| Agent state packet | `Tools/ai/build_agent_state_packet.py` | app workers, AI agents and guardrail reviewers | Generic packet with selected memory, constraints, budgets and planned CPU/NPU/GPU/validation microtasks. |
| Persistent memory DB | app or agent workflow | agent state packet builder and memory policy reviewer | Optional SQLite store under generated data; do not commit local memory records. |
| Memory policy report | `Tools/ai/review_agent_memory.py` | human review, app policy and validators | Non-destructive retention, quarantine and promotion-candidate report. |
| Blender Python script | developer or AI-assisted generator | Blender | Must be inspected before execution. |
| Render frames | Blender render process | FFmpeg or video workflow | Output folder should be configurable. |
| Final video | FFmpeg workflow | publication or review | Codec and settings are workflow-specific. |
| AI/NPU indexes | `Tools/npu/build_project_ai_index.py`, `Tools/npu/build_npu_code_context.py` | AI agents and future development sessions | Generated context; do not hand-edit as source. |

## Current known workflow areas

- `Scripting/v61b/` contains the current Blender scripting workflow.
- `Scripting/shared/` contains package-agnostic shared scripting utilities.
- `Tools/ai/` contains AI artifact validation and generic agent state packet tooling.
- `Tools/ai/pipeline/` contains the modular AI artifact pipeline.
- `Tools/npu/` contains AI/NPU tooling for analysis, review, or implementation support.
- `Tools/npu/pipeline/` contains app-agnostic NPU helper contracts and validation fixtures; runtime wiring is pending.
- `Tools/validation/` contains non-invasive validators.
- `Tools/workflow/` contains local validation runners.
- `indexAI/` contains indexed context and patch/task artifacts.

## Rules for AI systems

- Do not overwrite large analysis JSON files unless explicitly requested.
- Treat JSON files as input data unless their generator is known.
- Treat `indexAI/` and generated `Tools/npu/*_index.md` / manifest files as generated context.
- Treat local agent memory stores as generated data unless a human promotes a distilled record into documentation.
- Preserve local path configurability.
- Keep input-domain validators separate from output-application adapters.
- Keep NPU/Ollama provider execution out of helper-contract validators.
- Document every new expected input and output.

## Missing formal schemas

`docs/JSON_SCHEMAS.md` exists as a schema-notes file, but the following production schemas are still not fully specified:

- audio analysis JSON schema;
- music context JSON schema;
- implementation draft JSON schema;
- generated artifact plan/manifest schema;
- patch library task packet schema;
- render output manifest schema;
- NPU helper validation report schemas beyond common validator root fields.

## Recommended next improvement

Strengthen `docs/JSON_SCHEMAS.md` after inspecting representative JSON files from `output/`, `Tools/npu/`, and `indexAI/patch_library/`, then add non-destructive validators for the confirmed fields.

For the active NPU helper batch, first run:

```powershell
powershell.exe -ExecutionPolicy Bypass -File .\Tools\workflow\run_npu_pipeline_helper_validation.ps1
```

Then run full local validation and regenerate indexes before any runtime wiring.
