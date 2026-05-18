# Refactor/reuse full-run documentation coherence note — 2026-05-05

## Status

Current GitHub-only documentation coherence note for PR #187 and branch `codex/unified-local-ai-refactor-launcher`.

This note is doc-only. It does not replace the runtime bundle and does not claim local validation.

## Current active phase

The current active phase is the refactor/reuse full-run review pass:

```text
Task: docs/LOCAL_AI_TASKS/refactor-reuse-methods-classes-tools-planning.md
Run: 20260505-143844
Runtime bundle: ia_carmine_refactor_reuse_full_run_bundle_20260505-143844.zip
PR: #187 feat(workflow): add unified local AI refactor launcher
```

The bundle was published as a GitHub draft release asset and is intentionally not committed to the repository.

## Correct reading order for this phase

```text
AGENTS.md
CHATGPT.md
CHATGPT/README.md
CHATGPT/next-chat-handoff-refactor-reuse-full-run-20260505-143844.md
docs/LOCAL_AI_TASKS/refactor-reuse-methods-classes-tools-planning.md
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
docs/UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md
docs/LOCAL_AI_TASKS/current-code-flow-guide-2026-05-05.md
docs/LOCAL_AI_TASKS/project-tool-registry.md
docs/TECH_DEBT_TRACKER.md
```

If the timestamped CHATGPT handoff file is not present in GitHub, it is expected to exist only locally until it is explicitly added, committed and pushed.

## Current source of truth hierarchy

```text
1. current git state on codex/unified-local-ai-refactor-launcher
2. runtime bundle evidence for 20260505-143844 when accessible
3. manifest / decision loop / recommendations / patch plan / telemetry inside that bundle
4. canonical docs and task files in the repository
5. CHATGPT handoff notes as advisory operational memory
```

Do not infer runtime-bundle contents from file existence alone.

## Resolved broker telemetry context

The earlier broker telemetry issue from run `20260505-002508` is not the current active task.

It is historical/resolved context unless a new regression is found.

Known resolved state:

```text
Commit a85bbf4 preserved broker report inputs in final runtime telemetry.
Later evidence validated broker_reports propagation with executed_count=3, failed_count=0 and blocked_count=0.
```

Docs that still mention the broker telemetry task should treat it as historical or validated context, not as the current P0.

## Current review-only objective

The active objective is to inspect the refactor/reuse full-run bundle and classify the resulting recommendations and patch plans into:

```text
SAFE_MECHANICAL
MANUAL_REVIEW
LOCAL_VALIDATION_REQUIRED
BLENDER_RUNTIME_REQUIRED
PROVIDER_VALIDATION_REQUIRED
DEFER
DO_NOT_PROMOTE
```

No patch spec should be applied automatically.

## Candidate patch family currently selected for review

Before reading the runtime ZIP, code/docs inspection suggests one safe candidate family:

```text
centralize report/telemetry helper functions in Tools/validation/_shared/report_utils.py
reuse them from Tools/ai/runtime_tool/usage_telemetry/cli.py
reuse them from Tools/ai/full_toolbox_telemetry_summary/cli.py
then evaluate Tools/ai/shared_toolbox_bundle/cli.py separately
```

This is only a candidate. The bundle decision loop and patch plan remain the source of truth for final selection.

## Guardrails

```text
Do not merge to master.
Do not delete, force-push or rewrite history.
Do not deploy.
Do not touch secrets, permissions, billing or visibility.
Do not commit output/**.
Do not commit indexAI/code_chunks/**.
Do not commit *.db or *.sqlite.
Do not commit renders/**.
Do not run Blender runtime.
Do not run FFmpeg runtime.
Do not execute providers again unless explicitly requested.
Do not apply patch specs automatically.
Treat triple-quote/raw multiline edits as P1 risk for Python command-example cleanup.
```

## Documentation follow-up

The long task indexes may still contain historical references to broker telemetry as active work.

Preferred cleanup is incremental:

```text
CHATGPT.md and CHATGPT/README.md point to the refactor/reuse phase.
This note records the current coherence state without rewriting long indexes.
Later update docs/LOCAL_AI_TASKS/README.md and current-code-flow-guide-2026-05-05.md with focused edits or a local patch bundle.
```
