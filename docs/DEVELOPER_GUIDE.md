# Developer Guide

## Purpose

This guide defines a practical development workflow for this Blender audio-reactive project.

## Recommended workflow

1. Pull the latest `master` branch.
2. Read `README.md` and `AGENTS.md`.
3. Read `docs/MODULE_MAP.md` and `docs/DATA_FLOW.md`.
4. Identify the target area.
5. Inspect the active script before editing.
6. Make a focused change.
7. Test inside Blender when possible.
8. Document assumptions and results.
9. Commit with a clear message.

## Working with Blender scripts

- Keep local paths configurable.
- Add comments around Blender API compatibility-sensitive code.
- Prefer functions with clear responsibility.
- Avoid global side effects where a parameter or config value is practical.
- For large scripts, prefer extracting helpers into modules only when it improves maintainability.

## Working with AI-generated plans

- Treat generated implementation drafts as proposals, not source of truth.
- Validate target files before applying patches.
- Avoid applying broad changes without inspecting current code.
- Preserve original generated context files.
- Store derived plans in clearly named files.

## Working with generated data

- Do not commit heavy render outputs unless explicitly required.
- Do not overwrite full analysis JSON files without explicit instruction.
- Keep summaries separate from full data.
- Keep output paths configurable.

## Commit style

Use concise commit messages:

```text
docs: add module map
fix: update Blender node compatibility
feat: add configurable audio path
refactor: isolate material setup
```

## Test notes

When reporting a change, include:

- changed files;
- reason for the change;
- Blender version tested;
- command or action used;
- result;
- line count for scripts created or modified.

## Not specified

- Formal formatter.
- Formal test framework.
- Release automation.
- Branch protection policy.
