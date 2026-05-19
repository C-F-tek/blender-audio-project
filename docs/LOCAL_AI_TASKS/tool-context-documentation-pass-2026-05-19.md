# Tool context documentation pass — 2026-05-19

## Scope

Current task: add descriptive context files for the refactored tool surface so AI agents and operator workflows can recover purpose, context, safe usage and boundaries without relying on chat memory.

No PR is currently open, so this pass is being applied directly to `master` by explicit operator instruction.

## Root contract

`CHATGPT.md` has been restored at repository root as the canonical operating contract for ChatGPT/GPT clients in IA-Carmine.

`CHATGPT/README.md` remains advisory historical handoff material and does not override the root contract.

## Files added so far

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
```

## Current principles captured

- Use dispatcher invocation: `python -m Tools.<area> <tool>`.
- Prefer package-owned CLIs over scattered root scripts.
- Context builders do not produce patch targets by themselves.
- Provider output is evidence, not product.
- Matrix/lab/diff evidence is the source of code product applicability.
- Runtime artifacts and databases remain out of Git.
- Root `CHATGPT.md` is the current ChatGPT operating contract.

## Next documentation targets

Add section-level context files for the largest `Tools/ai` families:

```text
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

Then update higher-level Markdown indices/runbooks only after the current tool-context layer exists.

## Guardrails

Do not commit:

```text
output/**
*.db
*.sqlite
*.sqlite-wal
*.sqlite-shm
renders/**
indexAI/code_chunks/**
indexAI/project_code_chunks/**
```

This task is documentation-only. No runtime provider execution, source patch application, Blender runtime or destructive Git operation is part of this pass.
