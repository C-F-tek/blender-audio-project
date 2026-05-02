# Temporary PR109 refactor workspace

This folder is intentionally temporary and belongs to the `codex/refactor-workspace-109` branch.

Purpose:

- hold scratch notes/chunks for refactoring long files that are inconvenient to inspect through bounded API responses;
- keep temporary analysis out of the official PR #109 branch until a final source refactor is ready;
- mirror only the final useful source edits back to `codex/design-code-patch-plan-lane`.

Guardrails:

- no provider execution;
- no Blender runtime;
- no patch application;
- no raw `output/**` commits;
- no SQLite/full-analysis JSON;
- no merge to `master`.

Cleanup:

- this folder and the temporary PR must be removed/closed after useful refactors are mirrored into PR #109.
