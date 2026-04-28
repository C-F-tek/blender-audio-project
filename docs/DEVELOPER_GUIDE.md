# Developer Guide

## Purpose

This guide defines a practical development workflow for this Blender audio-reactive project.

## Default branch

The repository default branch is currently `master`.

Use `master` as the pull request base unless the repository configuration changes.

## Recommended workflow

1. Pull the latest `master` branch.
2. Create a focused branch such as `feature/<topic>`, `fix/<topic>`, `docs/<topic>`, or `compat/<topic>`.
3. Read `README.md` and `AGENTS.md`.
4. Read `docs/README.md`, `docs/AI_REPOSITORY_MANIFEST.md`, `docs/MODULE_MAP.md`, and `docs/DATA_FLOW.md`.
5. Identify the target area.
6. Inspect the active script before editing.
7. Make a focused change.
8. Test inside Blender when possible.
9. Document assumptions and results.
10. Commit with a clear message.
11. Open a pull request using `.github/PULL_REQUEST_TEMPLATE.md`.

## Branch naming

Recommended branch prefixes:

- `feature/` for new functionality.
- `fix/` for bug fixes.
- `docs/` for documentation-only changes.
- `refactor/` for structure-only code changes.
- `compat/` for Blender/Python compatibility updates.
- `ci/` for GitHub Actions or automation changes.

## Working with Blender scripts

- Keep local paths configurable.
- Add comments around Blender API compatibility-sensitive code.
- Prefer functions with clear responsibility.
- Avoid global side effects where a parameter or config value is practical.
- For large scripts, prefer extracting helpers into modules only when it improves maintainability.
- Do not use Blender node types or APIs removed in newer versions without fallback logic.

## Working with AI-generated plans

- Treat generated implementation drafts as proposals, not source of truth.
- Validate target files before applying patches.
- Avoid applying broad changes without inspecting current code.
- Preserve original generated context files.
- Store derived plans in clearly named files.
- Use `docs/AI_PROMPTS.md` for repeatable prompt structure.
- Use `docs/REVIEW_CHECKLIST.md` before accepting AI-generated code.

## Working with generated data

- Do not commit heavy render outputs unless explicitly required.
- Do not overwrite full analysis JSON files without explicit instruction.
- Keep summaries separate from full data.
- Keep output paths configurable.

## Commit style

Use concise commit messages:

- `docs: add module map`
- `fix: update Blender node compatibility`
- `feat: add configurable audio path`
- `refactor: isolate material setup`
- `ci: add lightweight syntax checks`

## Pull request contents

Every pull request should include:

- summary;
- changed files;
- reason for the change;
- test results;
- Blender version tested, or `not specified`;
- risks;
- follow-up work.

## Test notes

When reporting a change, include:

- changed files;
- reason for the change;
- Blender version tested;
- command or action used;
- result;
- line count for scripts created or modified.

## Minimal local validation

Use the strongest practical validation for the change:

- Generic Python scripts: run Python compile checks.
- JSON files: run JSON parse validation.
- Blender-specific scripts: run Blender runtime or background-mode checks when available.
- If Blender testing was not run, write `not specified` in the PR.

## Not specified

- Formal formatter.
- Formal test framework.
- Release automation.
- Branch protection policy.
