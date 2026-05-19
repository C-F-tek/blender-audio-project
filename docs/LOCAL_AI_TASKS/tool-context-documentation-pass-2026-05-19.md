# Tool context documentation pass — 2026-05-19

## Scope

Add descriptive context files for the refactored tool surface so AI agents and operator workflows can recover purpose, context, usage and boundaries from files rather than chat memory.

No PR is currently open, so this pass is applied directly to `master` by operator instruction.

## Root contract

`CHATGPT.md` has been restored at repository root as the canonical ChatGPT/GPT operating contract for IA-Carmine.

`CHATGPT/README.md` remains advisory historical handoff material.

## Files added in this pass

```text
CHATGPT.md
Tools/TOOL_CONTEXT.md
Tools/ai/TOOL_CONTEXT.md
Tools/validation/TOOL_CONTEXT.md
Tools/workflow/TOOL_CONTEXT.md
Tools/npu/TOOL_CONTEXT.md
Tools/docs/TOOL_CONTEXT.md
Tools/git/TOOL_CONTEXT.md
Tools/repo_patch_runner/TOOL_CONTEXT.md
Tools/ai/agent_context/TOOL_CONTEXT.md
Tools/ai/agent_memory/TOOL_CONTEXT.md
Tools/ai/heap_context_memory_reload/TOOL_CONTEXT.md
Tools/ai/heap_gate/TOOL_CONTEXT.md
Tools/ai/heap_runtime/TOOL_CONTEXT.md
Tools/ai/operator_product_core/TOOL_CONTEXT.md
Tools/ai/provider_mesh/TOOL_CONTEXT.md
Tools/ai/runtime_tool/TOOL_CONTEXT.md
Tools/ai/runtime_universe/TOOL_CONTEXT.md
Tools/ai/code_product/TOOL_CONTEXT.md
Tools/ai/patch_product/TOOL_CONTEXT.md
```

## Principles captured

- Use dispatcher invocation: `python -m Tools.<area> <tool>`.
- Prefer package-owned CLIs over scattered root scripts.
- Context builders do not produce patch targets by themselves.
- Provider output is evidence, not product.
- Matrix/lab/diff evidence is the source of code product applicability.
- Runtime artifacts and databases remain out of Git.
- Root `CHATGPT.md` is the current operating contract.

## First pass status

```text
[x] Root ChatGPT operating contract restored.
[x] Top-level Tools context index created.
[x] Top-level tool areas documented.
[x] Core Tools/ai families documented.
[x] Current task recorded in LOCAL_AI_TASKS.
```

## Next documentation targets

```text
Tools/ai/provider_runtime_blackboard/TOOL_CONTEXT.md
Tools/ai/external_heap/TOOL_CONTEXT.md
Tools/ai/repository_product/TOOL_CONTEXT.md
Tools/ai/agent_review/TOOL_CONTEXT.md
Tools/ai/generated_patch_specs/TOOL_CONTEXT.md
Tools/validation/heap_runtime/TOOL_CONTEXT.md
Tools/validation/runtime_tool/TOOL_CONTEXT.md
Tools/validation/runtime_universe/TOOL_CONTEXT.md
Tools/validation/provider_mesh/TOOL_CONTEXT.md
Tools/workflow/workflow_run/TOOL_CONTEXT.md
Tools/npu/provider_mesh/TOOL_CONTEXT.md
```

## Git hygiene

Keep runtime artifacts, SQLite databases, render outputs and generated chunk caches out of versioned documentation unless a compact evidence artifact is explicitly intended for Git.
