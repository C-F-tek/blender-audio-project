# ChatGPT session problems and robust fixes - 2026-05-04

## Scope

Repository: `C-F-tek/blender-audio-project`

Branch: `codex/unified-local-ai-refactor-launcher`

This note records problems encountered during a long ChatGPT-assisted IA-Carmine workflow session and the robust operational fixes adopted.

## Problem 1: long inline patch commands are fragile

Observed failure modes:

```text
- quoting mistakes in long PowerShell snippets;
- Markdown fences accidentally copied into files;
- incomplete here-strings;
- parser errors such as MissingExpressionAfterToken;
- duplicate or orphan command fragments after copy/paste interruption.
```

Robust fix:

```text
Prefer real files or patch bundles over long chat blocks.
For complex fixes, deliver a ZIP or repository file containing:
- README.txt or README.md;
- run_patch_bundle.py or run_patch_bundle.ps1;
- validation commands;
- exact target files;
- no automatic git add/commit/push.
```

Preferred repo-local temporary path:

```text
output/validation/patch_bundles/<bundle_name>/
```

Preferred committed helper path when stable:

```text
Tools/workflow/
docs/LOCAL_AI_TASKS/
CHATGPT/
```

## Problem 2: generated run artifacts pollute the working tree

Observed state:

```text
M  docs/LOCAL_VALIDATION_EVIDENCE/full_context_golden_*.json|md
M  indexAI/code_chunks/semantic_code_chunks*.json
?? docs/LOCAL_VALIDATION_EVIDENCE/*<Stamp>*
```

Robust fix before new real runs:

```powershell
git restore --staged -- `
  docs/LOCAL_VALIDATION_EVIDENCE `
  indexAI/code_chunks

git stash push -u -m "archive full toolbox run artifacts <Stamp> before next run" -- `
  docs/LOCAL_VALIDATION_EVIDENCE `
  indexAI/code_chunks

git status --short
```

Do not use `git add .` in this workflow.

## Problem 3: `output/**` is ignored and should not be committed

Observed message:

```text
The following paths are ignored by one of your .gitignore files:
output
```

Interpretation:

```text
This is expected. output/** is runtime/local artifact space.
Do not force-add it unless a user explicitly requests a one-off diagnostic artifact and policy allows it.
```

## Problem 4: `output/ai_packets/<Stamp>` was treated as a context file

Failure:

```text
PermissionError: [Errno 13] Permission denied: output/ai_packets/<Stamp>
```

Cause:

```text
A directory was passed where tools expected a concrete text file.
```

Fix adopted:

```text
- `output/ai_packets/<Stamp>` is a run packet directory.
- Only concrete files inside it may be passed as context.
- The workload-quality gate accepts either:
  - output/ai_packets
  - output/ai_packets/<Stamp>
- When root is passed, it scans immediate timestamp child directories.
```

Related commit:

```text
3061356 fix(ai): accept timestamped ai packet folders in workload quality gate
```

## Problem 5: `-Prod` disables debug tail evidence

Meaning:

```text
-Prod disables launcher transcript and execution-tail evidence.
This is correct for lighter production-like runs.
Use non-prod only when investigating launcher execution queues/debug tails.
```

## Problem 6: real runs must activate all declared tools/lanes

User policy clarified:

```text
Every real run must activate all declared probes, tools and provider lanes.
This applies to every real run, not only Full0To10.
```

Rule:

```text
A real run is any launcher execution that is not DryRun and not limited to smoke/reset planning.
Explicit `-No*` flags are the only acceptable way to disable a specific lane.
```

Patch bundle prepared:

```text
ia_carmine_real_run_strict_tool_activation_bundle.zip
```

Expected effect:

```text
- strict real-run activation in run_unified_local_ai_refactor.ps1;
- RequireProviderArtifacts passed into legacy full-toolbox decision wrapper;
- provider/GPU/evidence missing outputs become schema-valid failure artifacts;
- run stays red if provider really failed, but bundle diagnosis is complete.
```

## Problem 7: missing provider artifacts cascade into opaque decision-loop failures

Recurring fatal failures:

```text
output/ai_pipeline/full_toolbox_<Stamp>_parallel_gpu.json missing
output/ai_pipeline/agent_review_evidence_sufficiency.json missing
patch_plan_count below minimum: expected >= 1, got 0
```

Robust fix direction:

```text
Do not fake green status.
Create schema-valid fallback artifacts with passed=false and explicit classification:
required_provider_artifact_missing
```

This avoids missing-file cascades and keeps evidence bundles complete.

## Problem 8: chat Markdown fence nesting corrupts copy/paste readability

Observed failure mode:

```text
Long ChatGPT answers containing multiple nested triple-backtick code fences can render incorrectly in the chat UI.
When a response itself describes Markdown that contains fenced blocks, the outer and inner fences may interact visually.
The result is over-formatted output, broken sections, or commands that are hard to copy safely.
```

Robust fix:

```text
For chat responses, avoid nested triple-backtick fences.
Prefer one of these formats:
- plain text labels followed by short indented command blocks;
- separate downloadable/repository MD files for long procedures;
- patch bundles for complex scripts;
- single-backtick inline paths/flags for short references.
```

Operational rule:

```text
When the user asks to rewrite a previous answer because of formatting, do not repeat large nested fenced Markdown blocks.
Rewrite in compact sections with plain text and indented commands.
If a long Markdown procedure is needed, write it to a repository .md file and link/commit it instead of dumping the whole procedure into chat.
```

## Operational rule for future ChatGPT sessions

At session start, inspect:

```text
CHATGPT/README.md
CHATGPT/next-chat-handoff-*.md
CHATGPT/chatgpt-session-problems-and-robust-fixes-*.md
```

Then inspect the active branch, latest commits and `git status --short` before giving run commands.

## Problem 9: production bundle omitted from standard handoff language

Observed failure mode:

    Chat guidance focused on the decision-loop telemetry pair and treated the shared toolbox AI-to-AI bundle as optional or secondary.

Correct interpretation:

    For a completed IA-Carmine full run, shared_toolbox_ai_to_ai_bundle_<STAMP>.json/md is the standard production communication bundle.

Robust fix:

    When continuing work from a completed full run, request or inspect the production communication set first:

    - shared_toolbox_ai_to_ai_bundle_<STAMP>.json/md
    - full_toolbox_run_telemetry_summary_<STAMP>.json/md
    - runtime_tool_usage_telemetry_<STAMP>.json/md
    - runtime_tool_capability_manifest_<STAMP>.json/md
    - full_toolbox_<STAMP>_cloud_semantic_deterministic_chunk_manifest.json/md
    - full_toolbox_agent_review_decision_loop_<STAMP>.json/md

Operational rule:

    Do not describe the decision-loop evidence as the whole handoff. It is important but partial.
    The shared toolbox AI-to-AI bundle is the production bundle for cross-session communication.
