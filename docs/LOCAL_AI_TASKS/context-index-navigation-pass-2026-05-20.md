# Context index navigation pass — 2026-05-20

## Scope

Add compact navigation entrypoints so AI agents and operators can discover context files without relying on chat memory or manually opening every package folder.

## Files added or linked

```text
CONTEXT_INDEX.md
Tools/CONTEXT_INDEX.md
Tools/ai/CONTEXT_INDEX.md
Tools/validation/CONTEXT_INDEX.md
Tools/workflow/CONTEXT_INDEX.md
Tools/npu/CONTEXT_INDEX.md
docs/CONTEXT_INDEX.md
docs/CONTEXT_COVERAGE_STATUS.md
Scripting/CONTEXT_INDEX.md
```

## Purpose

These files are lightweight navigation indexes. They do not replace the detailed `TOOL_CONTEXT.md` files.

Expected reading flow:

```text
CONTEXT_INDEX.md
-> docs/CONTEXT_COVERAGE_STATUS.md
-> nearest area CONTEXT_INDEX.md
-> nearest TOOL_CONTEXT.md
-> dispatcher/source file
```

## Current root entrypoints

```text
AGENTS.md
CHATGPT.md
CONTEXT_INDEX.md
README.md
docs/CONTEXT_COVERAGE_STATUS.md
Tools/CONTEXT_INDEX.md
docs/CONTEXT_INDEX.md
Scripting/CONTEXT_INDEX.md
```

## Status model

`docs/CONTEXT_COVERAGE_STATUS.md` marks context files as:

```text
complete-enough
partial
stub
deferred
```

This prevents false claims that every one of the 1479 scripts is individually documented.

## Notes

`Tools/TOOL_CONTEXT.md` and some larger operational docs could not always be updated directly through the remote editor because of platform filtering. Separate `CONTEXT_INDEX.md` files were added to avoid blocking the documentation pass.

## Next steps

```text
sync local master
verify context index and coverage files exist locally
continue package-level TOOL_CONTEXT.md only for families that cause recurring ambiguity
expand Tools/ai/repository_product/TOOL_CONTEXT.md later from local editor if needed
```

## Guardrails

This pass is documentation-only. No runtime execution, provider execution, Blender execution, patch apply, merge, deploy or cleanup is part of this pass.