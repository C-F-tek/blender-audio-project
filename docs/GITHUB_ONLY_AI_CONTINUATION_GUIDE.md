# GitHub-Only AI Continuation Guide

## Purpose

Guide for AI agents that can read/write GitHub repository content, branches, commits, PRs and comments, but cannot run the local workstation, PowerShell launchers, Blender, NPU/GPU jobs, provider probes or index regeneration directly.

This is policy guidance, not a command catalog.

Current code-driven maps:

```text
docs/LOCAL_AI_TASKS/read-first-reuse-first-small-files-rule-2026-05-07.md
docs/LOCAL_AI_TASKS/code-derived-ai-toolchain-map-2026-05-07.md
docs/LOCAL_AI_TASKS/script-census-and-validation-flow-2026-05-07.md
docs/LOCAL_AI_TASKS/single-owner-scripts-and-flow-boundaries-2026-05-07.md
docs/LOCAL_AI_TASKS/code-driven-data-flow-map-2026-05-07.md
docs/LOCAL_AI_TASKS/validator-smoke-cycle-map-2026-05-07.md
```

## GitHub-only rule

When working GitHub-only, do not pretend GitHub access equals local validation.

A GitHub-only agent should:

```text
inspect repository files directly through GitHub/API
make small reviewable source or documentation updates
use committed evidence and user-pasted telemetry as the only runtime facts
state clearly when local validation is unavailable
avoid claiming local pass/fail unless report content is visible
avoid asking for local commands while the maintainer is away unless requested
```

## Current doctrine

```text
run_unified_local_ai_refactor.ps1 = run unica
Full0To10 = TUTTO SU TUTTO perimeter
quick/balanced/deep/custom = intensity or budget, not scope
-No* flags = explicit opt-out from selected lanes
-NoStrictRealRunActivation = single-phase diagnostics only
telemetry accompanies evidence and patch plans for completeness
monolithic/historical runbooks stay out of primary flow
```

## Reading order

```text
AGENTS.md
CHATGPT.md
CHATGPT/README.md
docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md
docs/LOCAL_AI_TASKS/read-first-reuse-first-small-files-rule-2026-05-07.md
docs/LOCAL_AI_TASKS/code-derived-ai-toolchain-map-2026-05-07.md
docs/LOCAL_AI_TASKS/script-census-and-validation-flow-2026-05-07.md
docs/LOCAL_AI_TASKS/single-owner-scripts-and-flow-boundaries-2026-05-07.md
docs/LOCAL_AI_TASKS/code-driven-data-flow-map-2026-05-07.md
docs/LOCAL_AI_TASKS/validator-smoke-cycle-map-2026-05-07.md
docs/LOCAL_AI_TASKS/obsolete-monolithic-docs-review-2026-05-07.md
docs/MAIN_RUNTIME_ARCHITECTURE.md
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
docs/UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md
```

Historical PR numbers, branch names and handoff docs are context only unless current GitHub state confirms them.

## What GitHub-only mode may do

Safe work:

```text
inspect repository files
inspect open PRs/comments/checks/diffs
create or update documentation branches and PRs when requested or implied
update documentation, PR descriptions and compact status docs
make small low-risk code changes when behavior is clear and validation limits are stated
add report-only validators or schema/docs changes
create patch plans or patch specs for later review without applying them
mark historical/monolithic docs as reference/superseded
```

Do not do from GitHub-only mode:

```text
claim local validation passed without visible report content
claim provider/GPU/NPU/Blender runtime behavior without committed or pasted evidence
hand-edit generated indexes under indexAI/
commit output/** or indexAI/code_chunks/**
edit full frame-by-frame analysis JSON files
queue/apply patch specs without explicit approval
change provider/model execution semantics without local validation plan
merge to protected branch unless explicitly instructed
```

## Telemetry and evidence handling

A GitHub-only agent may rely on runtime telemetry only when it is:

```text
committed under docs/LOCAL_VALIDATION_EVIDENCE/
pasted by the maintainer
included in a PR body/comment with concrete fields
```

Required companion surfaces for run-unica evidence or patch-plan review:

```text
launcher manifest
phase_status / phase_reports
runtime_tool_usage_telemetry_<STAMP>.json/md
runtime_tool_capability_manifest_<STAMP>.json/md
full_toolbox_run_telemetry_summary_<STAMP>.json/md
shared_toolbox_ai_to_ai_bundle_<STAMP>.json/md
shared_toolbox_ai_to_ai_final_summary_<STAMP>.json
CSV/count summaries when inventory lanes ran
discovery/index repair reports when relevant
file-line-limit reports when maintainability is in scope
```

Do not infer success from:

```text
file exists
patch plan exists
dry-run report exists
provider report exists
NPU smoke exists
large Markdown mentions it
```

## Local validation request policy

Only provide local validation commands when the maintainer asks, says they are at the workstation, or explicitly requests a validation block.

When requested, use the command owner:

```text
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
docs/LOCAL_AI_TASKS/validator-smoke-cycle-map-2026-05-07.md
```

For GitHub-only reports, use honest status language:

```text
GitHub-only review: completed.
Local workstation validation: not run in this session.
Runtime/provider/Blender evidence: not claimed unless committed or pasted.
Telemetry/capability handoff: reviewed only where committed/pasted.
```

## PR report contract

Every GitHub-only PR should state:

```text
what changed
why it advances the project
what was not touched
what local validation is unavailable or still required
whether indexes must be regenerated later
what runtime/provider/media proof is not claimed
which committed/pasted telemetry or evidence was reviewed, if any
```

For docs/workflow-state cleanup PRs, explicitly state:

```text
No runtime files, provider behavior, generated indexes, full analysis JSON, Blender scripts or audio/media outputs touched.
```

When code/scripts are created or modified, include resulting line counts.

## Fallback mode

When local validation is unavailable, prefer lower-risk work:

```text
docs and execution plans
PR review and issue triage
code reading and decomposition plans
patch specs for later local application
small pure-Python changes with honest validation limits
no Blender runtime migration
no NPU/GPU behavior assumptions
```

## Durable state updates

When macro direction changes, update compact/current maps first, not historical monoliths:

```text
docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md
docs/LOCAL_AI_TASKS/code-derived-ai-toolchain-map-2026-05-07.md
docs/LOCAL_AI_TASKS/script-census-and-validation-flow-2026-05-07.md
docs/LOCAL_AI_TASKS/single-owner-scripts-and-flow-boundaries-2026-05-07.md
docs/LOCAL_AI_TASKS/code-driven-data-flow-map-2026-05-07.md
docs/LOCAL_AI_TASKS/validator-smoke-cycle-map-2026-05-07.md
docs/TECH_DEBT_TRACKER.md
```

## Short prompt for future GitHub-only agents

```text
You are working GitHub-only on C-F-tek/blender-audio-project / IA-Carmine. Read AGENTS.md, CHATGPT.md, CHATGPT/README.md, current operational state, read-first/reuse-first rule, code-derived toolchain map, script census, single-owner map, data-flow map, validator-smoke map, obsolete-monolithic review, MAIN_RUNTIME_ARCHITECTURE, unified launcher runbook and launcher contract. Make small reviewable changes. Do not claim local/provider/GPU/NPU/Blender validation unless committed or pasted evidence proves it. Do not hand-edit generated indexes or output/**. Keep monolithic/historical runbooks out of primary flow.
```
