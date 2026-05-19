# Context coverage status

This file tracks whether context documentation is complete, partial or only a navigation stub.

## Status legend

| Status | Meaning |
| --- | --- |
| `complete-enough` | Enough for AI/operator orientation; expand only if confusion recurs. |
| `partial` | Useful, but not exhaustive; inspect source before relying on it. |
| `stub` | Exists only to make the family discoverable. Must be expanded later. |
| `deferred` | Optional/manual process; not blocking normal documentation work. |

## Required reading chain

```text
CONTEXT_INDEX.md
-> Tools/CONTEXT_INDEX.md or docs/CONTEXT_INDEX.md or Scripting/CONTEXT_INDEX.md
-> area CONTEXT_INDEX.md
-> nearest TOOL_CONTEXT.md
-> dispatch.py/source files
```

## Tool context coverage

| Area/family | File | Status |
| --- | --- | --- |
| Root index | `CONTEXT_INDEX.md` | complete-enough |
| Tools global index | `Tools/CONTEXT_INDEX.md` | complete-enough |
| Tools overview | `Tools/TOOL_CONTEXT.md` | partial |
| Tools/ai overview | `Tools/ai/TOOL_CONTEXT.md` | partial |
| Tools/ai family index | `Tools/ai/CONTEXT_INDEX.md` | complete-enough |
| Tools/ai agent context | `Tools/ai/agent_context/TOOL_CONTEXT.md` | complete-enough |
| Tools/ai agent memory | `Tools/ai/agent_memory/TOOL_CONTEXT.md` | complete-enough |
| Tools/ai agent review | `Tools/ai/agent_review/TOOL_CONTEXT.md` | complete-enough |
| Tools/ai AI workload | `Tools/ai/ai_workload/TOOL_CONTEXT.md` | complete-enough |
| Tools/ai code product | `Tools/ai/code_product/TOOL_CONTEXT.md` | complete-enough |
| Tools/ai deterministic recommendations | `Tools/ai/deterministic_recommendations/TOOL_CONTEXT.md` | complete-enough |
| Tools/ai external heap | `Tools/ai/external_heap/TOOL_CONTEXT.md` | complete-enough |
| Tools/ai generated patch specs | `Tools/ai/generated_patch_specs/TOOL_CONTEXT.md` | complete-enough |
| Tools/ai heap context memory reload | `Tools/ai/heap_context_memory_reload/TOOL_CONTEXT.md` | complete-enough |
| Tools/ai heap exchange | `Tools/ai/heap_exchange/TOOL_CONTEXT.md` | complete-enough |
| Tools/ai heap final proposals | `Tools/ai/heap_final_proposals/TOOL_CONTEXT.md` | complete-enough |
| Tools/ai heap gate | `Tools/ai/heap_gate/TOOL_CONTEXT.md` | complete-enough |
| Tools/ai heap provider | `Tools/ai/heap_provider/TOOL_CONTEXT.md` | complete-enough |
| Tools/ai heap runtime | `Tools/ai/heap_runtime/TOOL_CONTEXT.md` | complete-enough |
| Tools/ai operator product core | `Tools/ai/operator_product_core/TOOL_CONTEXT.md` | complete-enough |
| Tools/ai patch product | `Tools/ai/patch_product/TOOL_CONTEXT.md` | complete-enough |
| Tools/ai pipeline | `Tools/ai/pipeline/TOOL_CONTEXT.md` | complete-enough |
| Tools/ai provider mesh | `Tools/ai/provider_mesh/TOOL_CONTEXT.md` | complete-enough |
| Tools/ai provider runtime blackboard | `Tools/ai/provider_runtime_blackboard/TOOL_CONTEXT.md` | complete-enough |
| Tools/ai repository product | `Tools/ai/repository_product/TOOL_CONTEXT.md` | stub |
| Tools/ai runtime tool | `Tools/ai/runtime_tool/TOOL_CONTEXT.md` | complete-enough |
| Tools/ai runtime universe | `Tools/ai/runtime_universe/TOOL_CONTEXT.md` | complete-enough |
| Tools/validation overview | `Tools/validation/TOOL_CONTEXT.md` | partial |
| Tools/validation family index | `Tools/validation/CONTEXT_INDEX.md` | complete-enough |
| Tools/validation agent context | `Tools/validation/agent_context/TOOL_CONTEXT.md` | complete-enough |
| Tools/validation agent memory | `Tools/validation/agent_memory/TOOL_CONTEXT.md` | complete-enough |
| Tools/validation agent review | `Tools/validation/agent_review/TOOL_CONTEXT.md` | complete-enough |
| Tools/validation code product | `Tools/validation/code_product/TOOL_CONTEXT.md` | complete-enough |
| Tools/validation deterministic recommendations | `Tools/validation/deterministic_recommendations/TOOL_CONTEXT.md` | complete-enough |
| Tools/validation docs hygiene | `Tools/validation/docs_hygiene/TOOL_CONTEXT.md` | complete-enough |
| Tools/validation generated artifacts | `Tools/validation/generated_artifacts/TOOL_CONTEXT.md` | complete-enough |
| Tools/validation generated patch specs | `Tools/validation/generated_patch_specs/TOOL_CONTEXT.md` | complete-enough |
| Tools/validation heap provider | `Tools/validation/heap_provider/TOOL_CONTEXT.md` | complete-enough |
| Tools/validation heap runtime | `Tools/validation/heap_runtime/TOOL_CONTEXT.md` | complete-enough |
| Tools/validation patch product | `Tools/validation/patch_product/TOOL_CONTEXT.md` | complete-enough |
| Tools/validation pipeline | `Tools/validation/pipeline/TOOL_CONTEXT.md` | complete-enough |
| Tools/validation provider mesh | `Tools/validation/provider_mesh/TOOL_CONTEXT.md` | complete-enough |
| Tools/validation real product | `Tools/validation/real_product/TOOL_CONTEXT.md` | complete-enough |
| Tools/validation runtime tool | `Tools/validation/runtime_tool/TOOL_CONTEXT.md` | complete-enough |
| Tools/validation runtime universe | `Tools/validation/runtime_universe/TOOL_CONTEXT.md` | complete-enough |
| Tools/workflow overview | `Tools/workflow/TOOL_CONTEXT.md` | partial |
| Tools/workflow family index | `Tools/workflow/CONTEXT_INDEX.md` | complete-enough |
| Tools/workflow workflow_run | `Tools/workflow/workflow_run/TOOL_CONTEXT.md` | complete-enough |
| Tools/npu overview | `Tools/npu/TOOL_CONTEXT.md` | partial |
| Tools/npu family index | `Tools/npu/CONTEXT_INDEX.md` | complete-enough |
| Tools/npu provider mesh | `Tools/npu/provider_mesh/TOOL_CONTEXT.md` | complete-enough |
| Tools/docs | `Tools/docs/TOOL_CONTEXT.md` | complete-enough |
| Tools/git | `Tools/git/TOOL_CONTEXT.md` | complete-enough |
| Tools/repo_patch_runner | `Tools/repo_patch_runner/TOOL_CONTEXT.md` | complete-enough |

## Non-tool context coverage

| Area | File | Status |
| --- | --- | --- |
| docs index | `docs/CONTEXT_INDEX.md` | complete-enough |
| docs overview | `docs/TOOL_CONTEXT.md` | complete-enough |
| script surface map | `docs/SCRIPT_SURFACE_CONTEXT.md` | complete-enough |
| root surface map | `docs/ROOT_SURFACE_CONTEXT.md` | complete-enough |
| Scripting index | `Scripting/CONTEXT_INDEX.md` | complete-enough |
| Scripting overview | `Scripting/TOOL_CONTEXT.md` | complete-enough |
| Scripting/v61b | `Scripting/v61b/TOOL_CONTEXT.md` | complete-enough |
| Scripting/shared | `Scripting/shared/TOOL_CONTEXT.md` | complete-enough |
| Ready-to-Jazz package | `Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/TOOL_CONTEXT.md` | complete-enough |
| Template package | `Scripting/_template_audio_reactive_package/TOOL_CONTEXT.md` | complete-enough |
| config | `config/TOOL_CONTEXT.md` | complete-enough |
| assets | `assets/TOOL_CONTEXT.md` | complete-enough |
| indexAI | `indexAI/TOOL_CONTEXT.md` | complete-enough |

## Deferred mapping coverage

| Area | File | Status |
| --- | --- | --- |
| Mapping procedure | `docs/MAPPING_TOOL_EVIDENCE.md` | deferred |
| Exhaustive script inventory | `docs/LOCAL_AI_TASKS/exhaustive-script-surface-inventory-2026-05-19.md` | deferred |
| Mapping evidence publishing | `docs/LOCAL_AI_TASKS/mapping-tool-evidence-publishing-2026-05-19.md` | deferred |

## Known gaps

- `Tools/ai/repository_product/TOOL_CONTEXT.md` is a stub and should be expanded later from local editing if needed.
- Area overview files can remain partial because family indexes now provide direct navigation.
- Do not claim all 1479 scripts are individually documented. Current strategy documents macro-families and links to dispatch/source files.

## Rule

If a family is marked `stub` or `partial`, inspect the source files and dispatcher before making code changes.
