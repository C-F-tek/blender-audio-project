# Agentic Memory And Guardrail Pipeline

## Status

active

## Goal

Build a generic agentic layer that helps the project AI work beyond token-window limits through structured memory, task-specific context packets, non-blocking guardrail microtasks, and clear CPU/NPU/GPU lane policy.

The goal is operational self-awareness, not a claim of biological consciousness. In this repository that means: the agent can know the current task, constraints, recent and persistent memory, available files, planned microtasks, validation state, and remaining risks.

## Scope

- Generic memory records that can represent recent chat decisions, durable constraints, source files, generated artifacts, audio context, Blender context, or future file types.
- Task-specific state packets with selected memory under a character budget.
- Optional SQLite persistent memory using Python standard library only.
- Non-blocking microtask descriptors for CPU, NPU, GPU, validation and IO lanes.
- JSON and Markdown outputs that can be consumed by the app, another agent, or future specialized agents.
- First real validation target: Blender/audio workflows after the non-invasive packet layer is validated.

## Out of Scope

- No Blender runtime package migration.
- No long Blender render.
- No real GPU model execution.
- No mandatory NPU execution.
- No schema-v6 field meaning changes.
- No overwrite of full frame-level analysis JSON.
- No destructive refactor of `Scripting/v61b/` or generated packages.

## Files Likely Touched

```text
docs/EXECUTION_PLANS/active/2026-04-29_agentic_memory_guardrail_pipeline.md
Tools/ai/agent_state.py
Tools/ai/build_agent_state_packet.py
Tools/ai/agent_memory_policy.py
Tools/ai/review_agent_memory.py
Tools/ai/README.md
docs/AI_SMART_POLICY.md
docs/AI_MEMORY_POLICY.md
```

## Validation Commands

```powershell
python .\Tools\validation\check_python_syntax.py --repo-root .
python .\Tools\ai\build_agent_state_packet.py --repo-root . --objective "Validate generic agent memory and microtask packet" --include-file .\docs\AI_SMART_POLICY.md --include-file .\docs\LOCAL_AI_WORKFLOW.md --output-dir .\output\ai_pipeline\agent_state_smoke
python .\Tools\validation\check_docs_links.py --repo-root . --output .\output\validation\docs_links.json
python .\Tools\validation\check_agent_memory_policy.py --repo-root . --output .\output\validation\agent_memory_policy.json
python .\Tools\validation\check_blender_shared_compat_smoke.py --repo-root . --output .\output\validation\blender_shared_compat_smoke.json
python .\Tools\npu\build_project_ai_index.py
python .\Tools\npu\build_npu_code_context.py
```

## Risk Level

medium

The first implementation is low runtime risk because it is pure Python and non-invasive. The overall roadmap is medium risk because later Blender/audio app integration and hardware lanes must be tested carefully.

## Progress Log

- 2026-04-29: Read stable Markdown documentation, package/tool READMEs and generated Markdown indexes before implementation.
- 2026-04-29: First planned slice is a generic agent state packet builder, not runtime Blender integration.
- 2026-04-29: Added initial pure Python agent state packet helpers and CLI for memory plus microtask planning.
- 2026-04-29: Added optional SQLite memory database support without adding external dependencies.
- 2026-04-29: Added deterministic memory retention, quarantine and promotion-candidate policy.
- 2026-04-29: Added non-invasive Blender shared compatibility smoke validator; outside Blender it marks runtime checks as skipped.
- 2026-04-29: Ran Blender 5.1.1 background smoke; found and fixed VSE API change from `sequences` to `strips`.
- 2026-04-29: Blender 5.1.1 no-render smoke passed for frame range, noise node and VSE audio strip creation.

## Result

first slice in progress; runtime Blender/audio testing not started yet

## Follow-up

After packet generation is validated, create controlled Blender/audio smoke tasks:

```text
1. build an agent state packet for Blender compatibility testing;
2. run a manual Blender smoke test for Scripting/shared/blender_compat.py;
3. build an audio-analysis packet from representative JSON/audio context;
4. run guardrail review on those packets;
5. only then decide package adapter or app integration changes.
```
