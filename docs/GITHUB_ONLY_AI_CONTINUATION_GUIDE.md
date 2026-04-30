# GitHub-Only AI Continuation Guide

## Purpose

This document is the handoff thread for AI agents that can read, write, branch, commit, push, review and open pull requests on GitHub, but cannot run the local workstation, Blender, NPU/GPU jobs, PowerShell validation runners or index regeneration directly.

Use this guide to keep project work moving without pretending that GitHub-only access is equivalent to local validation.

## Current collaboration mode

As of 2026-04-30, the maintainer can still run local workstation validation and regenerate indexes from home.

That means a GitHub-only agent should:

1. make small, reviewable source or documentation PRs;
2. clearly state which local validation is required;
3. ask the maintainer to run the local commands when needed;
4. wait for the maintainer to paste report summaries or push regenerated indexes;
5. avoid claiming local pass/fail unless the report content is visible in the repository or supplied in chat.

When the maintainer says they can no longer run local validation or index regeneration, switch to the fallback mode in this file.

## North star

Keep the app core, backend, AI pipeline, NPU pipeline, multistep orchestration, guardrails, memory policy and validation contracts app-agnostic before touching artist-facing Blender runtime workflows.

The project can repeat these core loops multiple times:

```text
validation contracts
AI pipeline report/schema hardening
NPU/backend decomposition
memory and guardrail policy
documentation and execution plans
local workstation proof
index regeneration
```

Do not move to Ready To Jazz or broad `blender_compat.py` adoption until the core layers are stable and the maintainer explicitly asks for that phase.

## What a GitHub-only agent may do

Safe work:

- inspect repository files directly through GitHub;
- inspect open PRs, comments, checks and diffs;
- create branches and pull requests;
- make documentation updates;
- make small validator or pipeline changes when behavior is covered by existing tests or local validation can be requested;
- add or update execution plans under `docs/EXECUTION_PLANS/active/`;
- update tech debt and status documents when the evidence is in committed files or maintainer-provided reports;
- ask the maintainer to run local validation and push generated indexes.

Allowed but higher care:

- refactor `Tools/ai/`, `Tools/validation/` and `Tools/npu/` in small phases;
- split NPU/backend helpers only when CLI behavior is preserved;
- add schema/report contract validators that accept unknown future fields unless a field meaning is already documented;
- update GitHub PR descriptions with local report paths and pending validation status.

Do not do these from GitHub-only mode:

- do not edit full frame-by-frame analysis JSON files;
- do not hand-edit generated indexes under `indexAI/` or generated NPU context/index files;
- do not claim Blender runtime compatibility without a local Blender smoke report;
- do not begin Ready To Jazz migration or broad `blender_compat.py` adoption;
- do not split large Blender runtime scripts in a single PR;
- do not add external dependencies, CI workflows or heavy automation without explicit maintainer approval;
- do not mark local validation as passing unless the report is committed or the maintainer provides its contents.

## Current next sequence

1. Finish the active report-contract PR if it is still open.

   PR target: AI pipeline schema-v6 report contracts.

   Required proof:

   ```powershell
   powershell.exe -ExecutionPolicy Bypass -File .\Tools\workflow\run_local_validation_after_refactor.ps1 -SkipPull -ContinueOnError -MatrixWorkers 12 -RepeatCases 2
   ```

   Ask the maintainer for the latest `output/local_validation/*.json` and `*.md` paths, plus the validation report pass/fail summary.

2. After merge, continue with NPU pipeline decomposition phase 1.

   Keep entrypoints compatible. Start by extracting app-agnostic helpers from `Tools/npu/` into focused modules for:

   ```text
   config
   context building
   prompt construction
   provider/runtime boundaries
   artifact writing
   validation/reporting
   memory/guardrail coordination
   runner orchestration
   ```

   This is the next large core step because it reduces risk before any Blender runtime migration.

3. Continue formal contracts after the AI pipeline report layer is stable.

   Good follow-up targets:

   ```text
   music summary JSON
   scene spec JSON
   generated artifact manifests
   guardrail remediation reports
   memory packet shape
   ```

   Preserve unknown future fields unless a field is explicitly part of a documented contract.

4. Keep app-agnostic guardrails moving.

   Useful work:

   ```text
   memory retention checks
   quarantine and promotion rules
   generated artifact path safety
   dry-run-only semantics
   no-runtime-execution validators
   PR-local validation handoff templates
   ```

5. Only later, with explicit maintainer approval, begin Ready To Jazz / `blender_compat.py` adoption.

   When that phase starts:

   ```text
   one call site at a time
   one smoke test at a time
   no monolithic split
   no artistic behavior rewrite
   no broad runtime migration without local Blender proof
   ```

## How to request local validation from the maintainer

For source, validator, AI pipeline, NPU or core docs changes, ask for:

```powershell
cd C:\Users\carmi\blender\blender-audio-project
git checkout <branch>
git pull --rebase
powershell.exe -ExecutionPolicy Bypass -File .\Tools\workflow\run_local_validation_after_refactor.ps1 -SkipPull -ContinueOnError -MatrixWorkers 12 -RepeatCases 2
python .\Tools\npu\build_project_ai_index.py
python .\Tools\npu\build_npu_code_context.py
git status
git diff --stat
```

Then ask them to paste or commit:

```text
latest output/local_validation/*.json path
latest output/local_validation/*.md path
pass/fail
failed step names, if any
output/validation report pass/fail summary
git status
git diff --stat
generated index changes, if any
```

If only documentation changed and no validator/core behavior changed, a smaller request may be enough:

```powershell
python .\Tools\validation\check_docs_links.py --repo-root . --output .\output\validation\docs_links.json
python .\Tools\npu\build_project_ai_index.py
python .\Tools\npu\build_npu_code_context.py
git status
git diff --stat
```

## How to write PRs in GitHub-only mode

Every GitHub-only PR should say:

```text
what changed
why it advances the core/backend/AI/NPU goals
what was not touched
what local validation is required
whether indexes must be regenerated by the maintainer
what evidence is missing because the agent has no local workstation
```

Use honest validation language:

```text
GitHub-only review: completed
Local validation: pending maintainer
Index regeneration: pending maintainer
Blender runtime proof: not applicable / pending local Blender
```

Do not report line counts by default. The maintainer prefers changed files, purpose, validation status, risks and next step over code line counting.

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
docs/EXECUTION_PLANS/active/
docs/TECH_DEBT_TRACKER.md
docs/PROJECT_STATUS_POINT.md
docs/AI_PIPELINE_REFACTOR_STATUS.md
docs/JSON_SCHEMAS.md
docs/AI_ARTIFACT_SCHEMAS.md
docs/README.md
```

Only update status documents when there is evidence in committed code, validation reports, or maintainer-provided local output.

## Short prompt for future GitHub-only agents

```text
You are working GitHub-only on blender-audio-project. Read AGENTS.md, docs/README.md, docs/AI_ONBOARDING.md and docs/GITHUB_ONLY_AI_CONTINUATION_GUIDE.md first. Continue core/backend/AI/NPU/guardrail/memory work before Ready To Jazz or blender_compat adoption. Do not hand-edit generated indexes or full analysis JSON. Make small PRs, state local validation needed, and ask Carmine to run the local runner and regenerate indexes while he is available.
```
