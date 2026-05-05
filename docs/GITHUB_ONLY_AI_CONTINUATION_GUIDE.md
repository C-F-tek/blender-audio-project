# GitHub-Only AI Continuation Guide

## Purpose

This document is the handoff guide for AI agents that can read, write, branch, commit, push, review and open pull requests on GitHub, but cannot run the local workstation, Blender, NPU/GPU jobs, PowerShell validation runners, provider probes or index regeneration directly.

Use this guide to keep project work moving without pretending that GitHub-only access is equivalent to local validation.

This document is policy guidance, not a command catalog. Current executable examples live in:

```text
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
Tools/validation/README.md
Tools/npu/pipeline/README.md
```

## Current collaboration mode

When the maintainer explicitly says work is GitHub-only, do not ask for git sync, local commands, local provider runs or workstation validation until they explicitly ask for them or provide local results.

A GitHub-only agent should:

1. inspect repository files directly through GitHub/API;
2. make small, reviewable source or documentation PR updates;
3. use committed evidence and user-pasted telemetry as the only runtime facts;
4. state clearly when local validation is unavailable;
5. avoid claiming local pass/fail unless report content is visible in the repository or supplied in chat;
6. avoid asking for local commands while the maintainer is away unless the maintainer requests a validation block.

## Current doctrine

The active project model is:

```text
one canonical launcher flow
Full0To10 = TUTTO SU TUTTO
quick/balanced/deep/custom = intensity, not scope
smoke = separate non-full mode
perimeter of tutto can expand explicitly
telemetry accompanies evidence and patch plans for completeness
```

GitHub-only agents can update docs, contracts, PR bodies and small low-risk code when requested. They cannot prove runtime behavior without committed/pasted evidence.

## North star

Keep the app core, backend, AI pipeline, NPU pipeline, multistep orchestration, guardrails, memory policy, telemetry, capability manifests and validation contracts app-agnostic before touching artist-facing Blender runtime workflows.

The project can repeat these core loops multiple times:

```text
validation contracts
AI pipeline report/schema hardening
NPU/backend decomposition
memory and guardrail policy
runtime broker telemetry
runtime capability manifest
full toolbox telemetry summary
shared AI-to-AI bundle completeness
documentation and execution plans
local workstation proof when available
index regeneration only when explicitly scoped
```

Do not move to Ready To Jazz or broad `blender_compat.py` adoption until the core layers are stable and the maintainer explicitly asks for that phase.

## Current baseline

Current consolidation branch:

```text
codex/unified-local-ai-refactor-launcher
```

Current PR family:

```text
PR #187: unified local AI refactor launcher and documentation consolidation
```

Current validated states from committed or maintainer-provided evidence:

```text
broker telemetry validated by run 20260505-073332
provider diagnostics and deterministic degraded-provider recovery validated by run 20260505-081141
GPU sync timing source smoke validated with real rounds[*].elapsed_seconds samples
project-tool-registry.md seeded
shared bundle completeness patched for full-toolbox diagnostics
telemetry/capability/final summary documented as evidence completeness accessories
```

Current active local-AI entrypoint:

```text
Tools/workflow/run_unified_local_ai_refactor.ps1
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
docs/UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md
```

Do not restart from old PR chains, historical branch names or legacy helper-contract assumptions.

## What a GitHub-only agent may do

Safe work:

- inspect repository files directly through GitHub;
- inspect open PRs, comments, checks and diffs;
- create branches and pull requests when requested or clearly implied;
- update documentation and PR descriptions;
- make small validator or pipeline changes when behavior is clear and local validation can be deferred honestly;
- add or update execution plans under `docs/EXECUTION_PLANS/`;
- update tech debt and status documents when the evidence is in committed files or maintainer-provided reports;
- update telemetry/capability/evidence contracts;
- create patch plans or patch specs for later review without applying them.

Allowed but higher care:

- refactor `Tools/ai/`, `Tools/validation/` and `Tools/npu/` in small phases;
- split NPU/backend helpers only when CLI behavior is preserved;
- add schema/report contract validators that accept unknown future fields unless a field meaning is already documented;
- update GitHub PR descriptions with committed evidence paths and pending validation status.

Do not do these from GitHub-only mode:

- do not edit full frame-by-frame analysis JSON files;
- do not hand-edit generated indexes under `indexAI/` or generated NPU context/index files;
- do not claim Blender runtime compatibility without a local Blender smoke report;
- do not begin Ready To Jazz migration or broad `blender_compat.py` adoption;
- do not change NPU/Ollama provider execution behavior without an explicit narrow scope and local validation plan;
- do not split large Blender runtime scripts in a single PR;
- do not add external dependencies, CI workflows or heavy automation without explicit maintainer approval;
- do not mark local validation as passing unless the report is committed or the maintainer provides its contents;
- do not treat dry-run matrix, focused validator output or file existence as proof that `Full0To10` passed;
- do not queue or apply patch specs without explicit approval.

## Telemetry and evidence handling in GitHub-only mode

Telemetry is an accessory of completeness for evidence and patch plans.

A GitHub-only agent may rely on telemetry only when it is:

```text
committed under docs/LOCAL_VALIDATION_EVIDENCE/
pasted by the maintainer
included in a PR body/comment with concrete fields
```

Required companion surfaces for full-run evidence/patch-plan review:

```text
runtime_tool_usage_telemetry_<STAMP>.json/md
runtime_tool_capability_manifest_<STAMP>.json/md
full_toolbox_run_telemetry_summary_<STAMP>.json/md
shared_toolbox_ai_to_ai_bundle_<STAMP>.json/md
shared_toolbox_ai_to_ai_final_summary_<STAMP>.json
```

A GitHub-only agent must not infer success from:

```text
file exists
patch plan exists
dry-run report exists
provider report exists
NPU smoke exists
```

It must inspect fields such as:

```text
executed_count
failed_count
blocked_count
broker_reports
provider_advisory_state
provider_failure_reasons
degraded_provider_components
deterministic_recovery_used
gpu_metrics_source
round_duration_source
patch_application_performed
source_writes_performed
```

## Current next sequence

When working GitHub-only on the current branch, prioritize:

1. Keep canonical MD contracts aligned with code and evidence.
2. Keep PR #187 body aligned with current branch state.
3. Continue demoting obsolete/historical runbooks from active entrypoints.
4. Keep telemetry/capability/final-summary contracts attached to evidence and patch plans.
5. Document local validation as pending unless committed/pasted evidence proves it.
6. Avoid requesting local sync or runs until the maintainer asks for them.

Good follow-up targets:

```text
docs/QUALITY_GATE.md
docs/JSON_SCHEMAS.md
docs/TECH_DEBT_TRACKER.md
docs/GITHUB_LOCAL_VALIDATION_WORKFLOW.md
docs/GITHUB_ONLY_AI_CONTINUATION_GUIDE.md
Tools/validation/README.md
Tools/npu/pipeline/README.md
```

## How to request local validation

Only provide local validation commands when the maintainer asks for them, says they are back at the workstation, or explicitly requests a validation block.

When requested, prefer the unified launcher runbook as the command owner:

```text
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
```

For GitHub-only reports, use this language instead of asking for immediate local commands:

```text
GitHub-only review: completed.
Local workstation validation: not run in this session.
Runtime/provider/Blender evidence: not claimed unless committed or pasted.
Telemetry/capability handoff: reviewed only where committed/pasted.
```

## How to write PRs in GitHub-only mode

Every GitHub-only PR should say:

```text
what changed
why it advances the core/backend/AI/NPU/telemetry goals
what was not touched
what local validation is unavailable or still required
whether indexes must be regenerated later
what evidence is missing because the agent has no local workstation
which telemetry/capability/final-summary artifacts were reviewed, if any
```

Use honest validation language:

```text
GitHub-only review: completed
Local validation: not run in this session
Runtime/provider proof: not claimed
Index regeneration: deferred unless committed evidence exists
Blender runtime proof: not applicable / pending local Blender
```

When code/scripts are created or modified, include resulting line counts.

## Fallback mode when local validation is not available

When the maintainer says they are away from the workstation or cannot run tests/indexes, switch to lower-risk work:

- docs and execution plans;
- PR review and issue triage;
- code reading and decomposition plans;
- patch specs for later local application;
- small pure-Python changes only when they can be checked by GitHub-visible CI or direct reasoning;
- no Blender runtime migration;
- no NPU/GPU behavior assumptions;
- no merge recommendation for validation-sensitive PRs unless remote checks fully cover the change.

In fallback mode, label work clearly:

```text
local validation unavailable
index regeneration deferred
safe to review, not proven on workstation
```

## State updates to keep durable

When a macro step changes direction, update these files first:

```text
docs/EXECUTION_PLANS/
docs/TECH_DEBT_TRACKER.md
docs/PROJECT_STATUS_POINT.md
docs/AI_PIPELINE_REFACTOR_STATUS.md
docs/JSON_SCHEMAS.md
docs/AI_ARTIFACT_SCHEMAS.md
docs/README.md
docs/LOCAL_AI_TASKS/current-code-flow-guide-2026-05-05.md
```

Only update status documents when there is evidence in committed code, validation reports, telemetry artifacts, PR state or maintainer-provided local output.

## Short prompt for future GitHub-only agents

```text
You are working GitHub-only on C-F-tek/blender-audio-project / IA-Carmine. Read AGENTS.md, WORKFLOW.md, docs/README.md, docs/LOCAL_AI_RUN_BOOTSTRAP.md, docs/GITHUB_ONLY_AI_CONTINUATION_GUIDE.md and docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md first. Continue core/backend/AI/NPU/guardrail/memory/telemetry work before Ready To Jazz or blender_compat adoption. Current active branch family is codex/unified-local-ai-refactor-launcher / PR #187. Do not restart from old PR #41-#47 assumptions. Do not ask for local sync or runs while the maintainer is away unless requested. Do not hand-edit generated indexes or full analysis JSON. Make small PR updates, state local validation limits honestly, and treat telemetry/capability/final-summary artifacts as required companions for full-run evidence and patch plans.
```
