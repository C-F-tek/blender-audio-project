# Repository context index

This is the compact navigation entrypoint for AI and operator context.

## Core contracts and models

| File | Role |
| --- | --- |
| `docs/AI_LIMITATIONS_AND_ANTI_AMBIGUITY_CONTRACT.md` | Mandatory anti-ambiguity contract for AI limitations, context loss, smoke overfitting, optionalized lanes and evidence-free completion claims. |
| `docs/IA_UNIVERSE_MODEL_TO_CODE_MAP.md` | Core bridge from each Universo IA model to real code families, dispatcher commands, artifacts and validators. |
| `docs/CORE_LANE_COMPLETENESS_CONTRACT.md` | Complete/full run contract: required lanes need viable evidence; degraded/unavailable equals unviable. |
| `docs/HEAP_EXCHANGE_USEFUL_MODEL.md` | Current compact model for controlled input, shared heap/exchange, cooperating lanes, evidence and deterministic exit product. |
| `docs/STANDALONE_HEAP_SURFACE_MODEL.md` | Current compact model for deterministic heap surfaces: preload, memory, chunks, namespaces, tool catalog, broker, lanes and composer. |
| `docs/PROVIDER_LANES_UNIFIED_MIND_MODEL.md` | Current compact model for Ollama/main provider, GPU0 coworker lane and NPU micro-lane as one operational mind with departments. |
| `docs/REAL_PRODUCT_RUN_MODEL.md` | Current compact model for evidence-only, blocked and real product run states. |
| `docs/COMPACT_EVIDENCE_MODEL.md` | Current compact model for raw runtime output, selected compact evidence, AI-to-AI bundles and Git-trackable evidence. |
| `docs/PATCH_CODE_PRODUCT_BOUNDARY_MODEL.md` | Current compact model for provider proposal, patch plan, code product, PatchKit, repo-patch-runner and reviewed apply boundaries. |

## Coverage status

| File | Role |
| --- | --- |
| `docs/CONTEXT_COVERAGE_STATUS.md` | Tracks which context files are complete-enough, partial, stub or deferred. |
| `docs/DISPATCHER_CONTEXT_COVERAGE.md` | Tracks dispatcher-driven tool-family coverage and known gaps. |

## Root contracts

| File | Role |
| --- | --- |
| `AGENTS.md` | Primary agent contract. |
| `CHATGPT.md` | ChatGPT/GPT operating contract. |
| `README.md` | Project identity and high-level orientation. |
| `docs/ROOT_SURFACE_CONTEXT.md` | Root-level surface map. |

## Tooling context

| File | Role |
| --- | --- |
| `Tools/CONTEXT_INDEX.md` | Global tool context index. |
| `Tools/TOOL_CONTEXT.md` | Main tool area overview. |
| `ia_carmine/CONTEXT_INDEX.md` | AI family context index. |
| `Tools/validation/CONTEXT_INDEX.md` | Validation family context index. |
| `Tools/workflow/CONTEXT_INDEX.md` | Workflow family context index. |
| `Tools/npu/CONTEXT_INDEX.md` | NPU family context index. |

## Non-tool surfaces

| File | Role |
| --- | --- |
| `docs/CONTEXT_INDEX.md` | Documentation surface index. |
| `docs/SCRIPT_SURFACE_CONTEXT.md` | Non-Tools script/document surface map. |
| `Scripting/CONTEXT_INDEX.md` | Scripting package context index. |
| `Scripting/TOOL_CONTEXT.md` | Scripting area overview. |
| `config/TOOL_CONTEXT.md` | Repository configuration context. |
| `assets/TOOL_CONTEXT.md` | Asset context. |
| `indexAI/TOOL_CONTEXT.md` | AI index/memory/chunk context. |

## Mapping evidence

| File | Role |
| --- | --- |
| `docs/MAPPING_TOOL_EVIDENCE.md` | Optional operator-scheduled mapping procedure. |
| `docs/RUNTIME_PROVIDER_FAILURE_NOTES_20260520.md` | Compact public note for the 2026-05-20 provider-lane runtime failures and repairs. |
| `docs/LOCAL_AI_TASKS/exhaustive-script-surface-inventory-2026-05-19.md` | Script inventory procedure and baseline. |
| `docs/LOCAL_AI_TASKS/mapping-tool-evidence-publishing-2026-05-19.md` | Compact mapping evidence publication procedure. |

## Usage

Start here, then open the nearest area or family context before editing a package.

Canonical tool command pattern:

```powershell
python -m Tools.<area> <tool> [args...]
```

Mapping runs are optional and are not required before normal documentation updates.