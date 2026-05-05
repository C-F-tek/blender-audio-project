# AI patch delivery policy

## Purpose

This note defines how AI-generated repository fixes should be delivered when a change is too long, fragile, or multi-file for direct chat copy/paste.

## Preferred delivery order

1. GitHub source file on the active branch when GitHub writes are explicitly requested and available.
2. ZIP patch bundle for multi-file or fragile source changes.
3. Single helper file such as `.ps1`, `.py`, `.md`, or `.txt` placed under a clear repository path.
4. Chat-only commands only for short surgical fixes.

## Manual helper-file rule

When chat copy/paste is risky, provide a file instead of a long inline script.

Recommended locations:

```text
Tools/workflow/                  workflow helpers and repair scripts
docs/LOCAL_AI_TASKS/             canonical procedures and policy notes
output/validation/patch_bundles/ local generated patch bundles, not source
output/validation/manual_patch_builder/ local temporary manual helpers, not source
```

## `$L += ...` fallback

Use the PowerShell `$L += ...` line-builder technique only when all of these are true:

```text
- the fix is surgical;
- the generated helper fits in one chat window;
- ZIP/GitHub file delivery is unnecessary or unavailable;
- the user needs to paste the script line-by-line into PowerShell.
```

Otherwise, prefer a real file or GitHub commit.

## Git policy

Do not stage blindly with `git add .`.

Do not commit generated local run directories or temporary patch-builder directories. Commit only source, documentation, tests, validation helpers, or compact evidence explicitly selected by the workflow.
