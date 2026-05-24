# Tool context documentation pass — 2026-05-19

## Scope

Add descriptive context files for the refactored tool surface so AI agents and operator workflows can recover purpose, context, usage and boundaries from files rather than chat memory.

No PR is currently open, so this pass is applied directly to `master` by operator instruction.

## Root contract

`CHATGPT.md` is the canonical ChatGPT/GPT operating contract for IA-Carmine.

`CHATGPT/README.md` remains advisory historical handoff material.

## Files added in this pass

```text
CHATGPT.md
Tools/TOOL_CONTEXT.md
ia_carmine/TOOL_CONTEXT.md
Tools/validation/TOOL_CONTEXT.md
Tools/workflow/TOOL_CONTEXT.md
Tools/npu/TOOL_CONTEXT.md
Tools/docs/TOOL_CONTEXT.md
Tools/git/TOOL_CONTEXT.md
Tools/repo_patch_runner/TOOL_CONTEXT.md
ia_carmine/context/agent_context/TOOL_CONTEXT.md
ia_carmine/memory/agent_memory/TOOL_CONTEXT.md
ia_carmine/context/heap_context_memory_reload/TOOL_CONTEXT.md
ia_carmine/runtime/heap_gate/TOOL_CONTEXT.md
ia_carmine/runtime/heap_runtime/TOOL_CONTEXT.md
ia_carmine/product/operator_product_core/TOOL_CONTEXT.md
ia_carmine/providers/provider_mesh/TOOL_CONTEXT.md
ia_carmine/runtime/runtime_tool/TOOL_CONTEXT.md
ia_carmine/runtime/runtime_universe/TOOL_CONTEXT.md
ia_carmine/product/code_product/TOOL_CONTEXT.md
ia_carmine/product/patch_product/TOOL_CONTEXT.md
ia_carmine/runtime/provider_runtime_blackboard/TOOL_CONTEXT.md
ia_carmine/runtime/external_heap/TOOL_CONTEXT.md
ia_carmine/product/repository_product/TOOL_CONTEXT.md
ia_carmine/product/agent_review/TOOL_CONTEXT.md
ia_carmine/product/generated_patch_specs/TOOL_CONTEXT.md
Tools/validation/heap_runtime/TOOL_CONTEXT.md
Tools/validation/runtime_tool/TOOL_CONTEXT.md
Tools/validation/runtime_universe/TOOL_CONTEXT.md
Tools/validation/provider_mesh/TOOL_CONTEXT.md
Tools/workflow/workflow_run/TOOL_CONTEXT.md
Tools/npu/provider_mesh/TOOL_CONTEXT.md
```

## Status

```text
[x] Root contract restored.
[x] Top-level Tools areas documented.
[x] Core ia_carmine families documented.
[x] Second-level ia_carmine families documented.
[x] Second-level Tools/validation families documented.
[x] Workflow and NPU package contexts documented.
```

## Remaining candidates

```text
more granular package-level contexts under ia_carmine where useful
more granular validation contexts where useful
docs/PACKAGE_CREATION_WORKFLOW.md alignment check
docs/PROJECT_AUDIT.md alignment check
root-level standalone file audit if new root scripts appear
```

## Git hygiene

Keep runtime artifacts, SQLite databases, render outputs and generated chunk caches out of versioned documentation unless a compact evidence artifact is explicitly intended for Git.
