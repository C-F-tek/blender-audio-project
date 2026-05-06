# Agentic Memory And Guardrail Pipeline

## Status

active

## Current review note — 2026-05-07

This is one of the oldest remaining execution plans under `active/`. It predates the current post-PR187 Full0To10 baseline and the main runtime architecture contract.

Treat it as **legacy active / architecture-seeded follow-up**. It contains useful memory/guardrail design history, but current work must use:

```text
docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md
docs/MAIN_RUNTIME_ARCHITECTURE.md
docs/UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md
```

Current runtime target:

```text
shared runtime heap / blackboard
├─ GPU1 primary advisory / planner
├─ GPU0 coworker/helper OpenVINO
├─ NPU microtask responder
├─ broker unico executor
├─ semantic tools registry
├─ deterministic validators / CPU authority
└─ telemetry/event stream
```

Mapping from this older plan to the current architecture:

```text
agent state packet -> shared runtime heap / blackboard candidate
memory policy -> blackboard retention and promotion policy
microtask descriptors -> NPU microtask responder / CPU validator task records
validation state -> deterministic validators / CPU authority
risk/remaining tasks -> telemetry/event stream and evidence summaries
```

Do not implement this plan as a separate parallel architecture. Reuse its ideas only through the current blackboard/broker/registry/validator/telemetry model.

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

Current additional risk:

```text
Do not create a second memory/agentic architecture outside the main blackboard/broker/runtime model.
```

## Progress Log

- 2026-04-29: Read stable Markdown documentation, package/tool READMEs and generated Markdown indexes before implementation.
- 2026-04-29: First planned slice is a generic agent state packet builder, not runtime Blender integration.
- 2026-04-29: Added initial pure Python agent state packet helpers and CLI for memory plus microtask planning.
- 2026-04-29: Added optional SQLite memory database support without adding external dependencies.
- 2026-04-29: Added deterministic memory retention, quarantine and promotion-candidate policy.
- 2026-04-29: Added non-invasive Blender shared compatibility smoke validator; outside Blender it marks runtime checks as skipped.
- 2026-04-29: Ran Blender 5.1.1 background smoke; found and fixed VSE API change from `sequences` to `strips`.
- 2026-04-29: Blender 5.1.1 no-render smoke passed for frame range, noise node and VSE audio strip creation.
- 2026-05-07: Reviewed against the main runtime architecture. Future implementation should flow through shared runtime heap / blackboard, broker, registry, CPU validators and telemetry/event stream.

## Result

first slice in progress historically; runtime Blender/audio testing was not the current active architecture path.

## Follow-up

Next safe follow-up under current architecture:

```text
1. define blackboard record shapes for agent state packet summaries;
2. keep SQLite memory local and untracked;
3. route memory review through deterministic validators;
4. expose memory/blackboard state in telemetry/evidence summaries;
5. avoid direct prompt injection or provider-side mutation until validators pass.
```

Manual execution-plan cleanup may later move this plan to `completed/` or superseded after explicit approval for file moves.
