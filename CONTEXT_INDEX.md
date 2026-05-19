# Repository context index

This is the compact navigation entrypoint for AI and operator context.

## Core model

| File | Role |
| --- | --- |
| `docs/HEAP_EXCHANGE_USEFUL_MODEL.md` | Current compact model for controlled input, shared heap/exchange, cooperating lanes, evidence and deterministic exit product. |

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
| `Tools/ai/CONTEXT_INDEX.md` | AI family context index. |
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
| `docs/LOCAL_AI_TASKS/exhaustive-script-surface-inventory-2026-05-19.md` | Script inventory procedure and baseline. |
| `docs/LOCAL_AI_TASKS/mapping-tool-evidence-publishing-2026-05-19.md` | Compact mapping evidence publication procedure. |

## Usage

Start here, then open the nearest area or family context before editing a package.

Canonical tool command pattern:

```powershell
python -m Tools.<area> <tool> [args...]
```

Mapping runs are optional and are not required before normal documentation updates.