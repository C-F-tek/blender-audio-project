# Context coverage status

<!-- IA-CARMINE-CURRENT-RUNTIME-CONTRACT:START -->
## Current Runtime/Tool Contract (2026-05-24)

Canonical wording: `docs/CURRENT_RUNTIME_MARKDOWN_CONTRACT.md`.

- GPU1/NVIDIA primary Ollama lane is the operational center and advances by heap pointer/recovery turns without waiting for GPU0/NPU sidecar completion.
- GPU0/NPU are `packet_review_only` sidecars: they start only after a reviewable GPU1 packet, do not close product, and remain deferred evidence until a later GPU1 turn consumes their pointer ids.
- Tool/lab/matrix/debug reporting must distinguish `lab_called`, `lab_report_written`, `lab_usable` and `lab_status`; attempted tool calls are evidence, not automatic usable lab output.
- `FINAL_PRODUCT` is single: text, code, or text+code. `PLAN_PRODUCT_FULL_PATCH.md` is its text/prose surface; `CODE_PRODUCT_FULL_PATCH.md` is its code/diff surface only when verified code exists. GPU1 emits causal `FINAL_PRODUCT_DELTA` records; blocked status is runtime/gate classification, not GPU1 output.
- Missing optional values stay empty/null; required missing devices or provider prerequisites raise or block with a typed reason rather than emitting placeholder text.
- Complete runs require explicit config flags, including `--files-per-round`, `--gpu0-ollama-num-ctx`, `--npu-micro-start-mode`, `--npu-final-wait-seconds` and `--max-degraded-lanes`.
<!-- IA-CARMINE-CURRENT-RUNTIME-CONTRACT:END -->


This file tracks whether context documentation is complete, partial or only a navigation stub.

## Status legend

| Status | Meaning |
| --- | --- |
| `complete-enough` | Enough for AI/operator orientation; expand only if confusion recurs. |
| `partial` | Useful, but not exhaustive; inspect source before relying on it. |
| `stub` | Exists only to make the family discoverable. Must be expanded later. |
| `stub-missing` | The family exists but a context file could not be created in the current remote-edit pass. |
| `deferred` | Optional/manual process; not blocking normal documentation work. |

## Required reading chain

```text
CONTEXT_INDEX.md
-> docs/AI_LIMITATIONS_AND_ANTI_AMBIGUITY_CONTRACT.md
-> docs/IA_UNIVERSE_MODEL_TO_CODE_MAP.md
-> docs/CORE_LANE_COMPLETENESS_CONTRACT.md
-> docs/HEAP_EXCHANGE_USEFUL_MODEL.md
-> docs/STANDALONE_HEAP_SURFACE_MODEL.md
-> docs/PROVIDER_LANES_UNIFIED_MIND_MODEL.md
-> docs/REAL_PRODUCT_RUN_MODEL.md
-> docs/COMPACT_EVIDENCE_MODEL.md
-> docs/PATCH_CODE_PRODUCT_BOUNDARY_MODEL.md
docs/CURRENT_RUNTIME_MARKDOWN_CONTRACT.md
-> docs/CONTEXT_COVERAGE_STATUS.md
-> docs/DISPATCHER_CONTEXT_COVERAGE.md
-> Tools/CONTEXT_INDEX.md or docs/CONTEXT_INDEX.md or Scripting/CONTEXT_INDEX.md
-> area CONTEXT_INDEX.md
-> nearest TOOL_CONTEXT.md
-> dispatch.py/source files
```

## Core model coverage

| Area/family | File | Status |
| --- | --- | --- |
| AI limitations and anti-ambiguity contract | `docs/AI_LIMITATIONS_AND_ANTI_AMBIGUITY_CONTRACT.md` | complete-enough |
| IA universe model-to-code map | `docs/IA_UNIVERSE_MODEL_TO_CODE_MAP.md` | complete-enough |
| Core lane completeness contract | `docs/CORE_LANE_COMPLETENESS_CONTRACT.md` | complete-enough |
| Heap/exchange useful model | `docs/HEAP_EXCHANGE_USEFUL_MODEL.md` | complete-enough |
| Standalone heap surface model | `docs/STANDALONE_HEAP_SURFACE_MODEL.md` | complete-enough |
| Provider lanes unified mind model | `docs/PROVIDER_LANES_UNIFIED_MIND_MODEL.md` | complete-enough |
| Real product run model | `docs/REAL_PRODUCT_RUN_MODEL.md` | complete-enough |
| Compact evidence model | `docs/COMPACT_EVIDENCE_MODEL.md` | complete-enough |
| Patch/code product boundary model | `docs/PATCH_CODE_PRODUCT_BOUNDARY_MODEL.md` | complete-enough |

## Tool context coverage

| Area/family | File | Status |
| --- | --- | --- |
| Root index | `CONTEXT_INDEX.md` | complete-enough |
| Dispatcher coverage map | `docs/DISPATCHER_CONTEXT_COVERAGE.md` | complete-enough |
| Tools global index | `Tools/CONTEXT_INDEX.md` | complete-enough |
| Tools overview | `Tools/TOOL_CONTEXT.md` | partial |
| ia_carmine overview | `ia_carmine/TOOL_CONTEXT.md` | partial |
| ia_carmine family index | `ia_carmine/CONTEXT_INDEX.md` | complete-enough |
| ia_carmine shared helpers | `ia_carmine/_shared/TOOL_CONTEXT.md` | complete-enough |
| ia_carmine agent context | `ia_carmine/context/agent_context/TOOL_CONTEXT.md` | complete-enough |
| ia_carmine internal RAG context | `ia_carmine/context/agent_context/TOOL_CONTEXT.md` | complete-enough |
| ia_carmine agent memory | `ia_carmine/memory/agent_memory/TOOL_CONTEXT.md` | complete-enough |
| ia_carmine agent review | `ia_carmine/product/agent_review/TOOL_CONTEXT.md` | complete-enough |
| ia_carmine AI workload | `ia_carmine/product/ai_workload/TOOL_CONTEXT.md` | complete-enough |
| ia_carmine code product | `ia_carmine/product/code_product/TOOL_CONTEXT.md` | complete-enough |
| ia_carmine contractor universe | `ia_carmine/runtime/contractor_universe/TOOL_CONTEXT.md` | complete-enough |
| ia_carmine deterministic recommendations | `ia_carmine/product/deterministic_recommendations/TOOL_CONTEXT.md` | complete-enough |
| ia_carmine external heap | `ia_carmine/runtime/external_heap/TOOL_CONTEXT.md` | complete-enough |
| ia_carmine generated patch specs | `ia_carmine/product/generated_patch_specs/TOOL_CONTEXT.md` | complete-enough |
| ia_carmine heap context memory reload | `ia_carmine/context/heap_context_memory_reload/TOOL_CONTEXT.md` | complete-enough |
| ia_carmine heap exchange | `ia_carmine/runtime/heap_exchange/TOOL_CONTEXT.md` | complete-enough |
| ia_carmine heap final proposals | `ia_carmine/product/heap_final_proposals/TOOL_CONTEXT.md` | complete-enough |
| ia_carmine heap gate | `ia_carmine/runtime/heap_gate/TOOL_CONTEXT.md` | complete-enough |
| ia_carmine heap provider | `ia_carmine/runtime/heap_provider/TOOL_CONTEXT.md` | complete-enough |
| ia_carmine heap runtime | `ia_carmine/runtime/heap_runtime/TOOL_CONTEXT.md` | complete-enough |
| ia_carmine operator product core | `ia_carmine/product/operator_product_core/TOOL_CONTEXT.md` | complete-enough |
| ia_carmine patch product | `ia_carmine/product/patch_product/TOOL_CONTEXT.md` | complete-enough |
| ia_carmine patchkit | `ia_carmine/product/patchkit/TOOL_CONTEXT.md` | complete-enough |
| ia_carmine pipeline | `ia_carmine/product/pipeline/TOOL_CONTEXT.md` | complete-enough |
| ia_carmine provider mesh | `ia_carmine/providers/provider_mesh/TOOL_CONTEXT.md` | complete-enough |
| ia_carmine provider runtime blackboard | `ia_carmine/runtime/provider_runtime_blackboard/TOOL_CONTEXT.md` | complete-enough |
| ia_carmine repository product | `ia_carmine/product/repository_product/TOOL_CONTEXT.md` | stub |
| ia_carmine run command | `ia_carmine/runtime/run/TOOL_CONTEXT.md` | complete-enough |
| ia_carmine runtime tool | `ia_carmine/runtime/runtime_tool/TOOL_CONTEXT.md` | complete-enough |
| ia_carmine runtime universe | `ia_carmine/runtime/runtime_universe/TOOL_CONTEXT.md` | complete-enough |
| ia_carmine runtime universe unified | `ia_carmine/runtime/runtime_universe/unified/TOOL_CONTEXT.md` | complete-enough |
| Tools/validation overview | `Tools/validation/TOOL_CONTEXT.md` | partial |
| Tools/validation family index | `Tools/validation/CONTEXT_INDEX.md` | complete-enough |
| Tools/validation agent context | `Tools/validation/agent_context/TOOL_CONTEXT.md` | complete-enough |
| Tools/validation RAG context checks | `Tools/validation/agent_context/TOOL_CONTEXT.md` | complete-enough |
| Tools/validation agent memory | `Tools/validation/agent_memory/TOOL_CONTEXT.md` | complete-enough |
| Tools/validation agent review | `Tools/validation/agent_review/TOOL_CONTEXT.md` | complete-enough |
| Tools/validation AI workload | `Tools/validation/ai_workload/TOOL_CONTEXT.md` | complete-enough |
| Tools/validation code product | `Tools/validation/code_product/TOOL_CONTEXT.md` | complete-enough |
| Tools/validation deterministic recommendations | `Tools/validation/deterministic_recommendations/TOOL_CONTEXT.md` | complete-enough |
| Tools/validation docs hygiene | `Tools/validation/docs_hygiene/TOOL_CONTEXT.md` | complete-enough |
| Tools/validation external heap | `Tools/validation/external_heap/TOOL_CONTEXT.md` | complete-enough |
| Tools/validation generated artifacts | `Tools/validation/generated_artifacts/TOOL_CONTEXT.md` | complete-enough |
| Tools/validation generated patch specs | `Tools/validation/generated_patch_specs/TOOL_CONTEXT.md` | complete-enough |
| Tools/validation heap exchange | `Tools/validation/heap_exchange/TOOL_CONTEXT.md` | stub |
| Tools/validation heap final proposals | `Tools/validation/heap_final_proposals/TOOL_CONTEXT.md` | stub-missing |
| Tools/validation heap provider | `Tools/validation/heap_provider/TOOL_CONTEXT.md` | complete-enough |
| Tools/validation heap runtime | `Tools/validation/heap_runtime/TOOL_CONTEXT.md` | complete-enough |
| Tools/validation legacy Blender | `Tools/validation/legacy_blender/TOOL_CONTEXT.md` | complete-enough |
| Tools/validation patch product | `Tools/validation/patch_product/TOOL_CONTEXT.md` | complete-enough |
| Tools/validation pipeline | `Tools/validation/pipeline/TOOL_CONTEXT.md` | complete-enough |
| Tools/validation provider mesh | `Tools/validation/provider_mesh/TOOL_CONTEXT.md` | complete-enough |
| Tools/validation real product | `Tools/validation/real_product/TOOL_CONTEXT.md` | complete-enough |
| Tools/validation repository product | `Tools/validation/repository_product/TOOL_CONTEXT.md` | complete-enough |
| Tools/validation runtime tool | `Tools/validation/runtime_tool/TOOL_CONTEXT.md` | complete-enough |
| Tools/validation runtime universe | `Tools/validation/runtime_universe/TOOL_CONTEXT.md` | complete-enough |
| Tools/validation schema repair | `Tools/validation/schema_repair/TOOL_CONTEXT.md` | complete-enough |
| Tools/validation workflow run | `Tools/validation/workflow_run/TOOL_CONTEXT.md` | complete-enough |
| Tools/workflow overview | `Tools/workflow/TOOL_CONTEXT.md` | partial |
| Tools/workflow family index | `Tools/workflow/CONTEXT_INDEX.md` | complete-enough |
| Tools/workflow PowerShell wrappers | `Tools/workflow/_powershell/TOOL_CONTEXT.md` | complete-enough |
| Tools/workflow GUI | `Tools/workflow/gui/TOOL_CONTEXT.md` | complete-enough |
| Tools/workflow workflow_run | `Tools/workflow/workflow_run/TOOL_CONTEXT.md` | complete-enough |
| Tools/npu overview | `Tools/npu/TOOL_CONTEXT.md` | partial |
| Tools/npu family index | `Tools/npu/CONTEXT_INDEX.md` | complete-enough |
| Tools/npu PowerShell wrappers | `Tools/npu/_powershell/TOOL_CONTEXT.md` | complete-enough |
| Tools/npu dual AI pipeline | `Tools/npu/dual_ai_pipeline/TOOL_CONTEXT.md` | complete-enough |
| Tools/npu provider mesh | `Tools/npu/provider_mesh/TOOL_CONTEXT.md` | complete-enough |
| Tools/docs overview | `Tools/docs/TOOL_CONTEXT.md` | complete-enough |
| Tools/docs family index | `Tools/docs/CONTEXT_INDEX.md` | complete-enough |
| Tools/docs docs hygiene | `Tools/docs/docs_hygiene/TOOL_CONTEXT.md` | complete-enough |
| Tools/docs shared helpers | `Tools/docs/_shared/TOOL_CONTEXT.md` | stub-missing |
| Tools/git overview | `Tools/git/TOOL_CONTEXT.md` | complete-enough |
| Tools/git family index | `Tools/git/CONTEXT_INDEX.md` | complete-enough |
| Tools/git PowerShell wrappers | `Tools/git/_powershell/TOOL_CONTEXT.md` | complete-enough |
| Tools/repo_patch_runner overview | `Tools/repo_patch_runner/TOOL_CONTEXT.md` | complete-enough |
| Tools/repo_patch_runner family index | `Tools/repo_patch_runner/CONTEXT_INDEX.md` | complete-enough |
| Tools/repo_patch_runner apply repo mods | `Tools/repo_patch_runner/apply_repo_mods/TOOL_CONTEXT.md` | complete-enough |

## Non-tool context coverage

| Area | File | Status |
| --- | --- | --- |
| docs index | `docs/CONTEXT_INDEX.md` | complete-enough |
| docs overview | `docs/TOOL_CONTEXT.md` | complete-enough |
| AI workload report quality gate | `docs/AI_WORKLOAD_REPORT_QUALITY_GATE.md` | complete-enough |
| local AI core tool activation | `docs/LOCAL_AI_CORE_TOOL_ACTIVATION.md` | complete-enough |
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

- `ia_carmine/product/repository_product/TOOL_CONTEXT.md` is a stub and should be expanded later from local editing if needed.
- `Tools/docs/_shared/TOOL_CONTEXT.md` could not be created through the remote editor and remains a known stub-missing item.
- `Tools/validation/heap_final_proposals/TOOL_CONTEXT.md` could not be created through the remote editor and remains a known stub-missing item.
- Area overview files can remain partial because family indexes now provide direct navigation.
- Do not claim all 1479 scripts are individually documented. Current strategy documents macro-families and links to dispatch/source files.
- Some `ia_carmine` modules still import generic report helpers from
  `Tools.validation._shared.report_utils`; decouple progressively through
  `ia_carmine._shared.report_io` instead of treating validation as runtime core.

## Rule

If a family is marked `stub`, `stub-missing`, or `partial`, inspect the source files and dispatcher before making code changes.
