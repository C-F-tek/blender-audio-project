<!-- IA-CARMINE-MD-SPLIT: part -->
# FULL_RUN_UNICA_TUTTO_SU_TUTTO — parte 001 di 002

Sorgente indice: [`../FULL_RUN_UNICA_TUTTO_SU_TUTTO.md`](../FULL_RUN_UNICA_TUTTO_SU_TUTTO.md)

## Navigazione

- [Indice](README.md)
- [Parte successiva](part-002.md)

# IA-Carmine — RUN UNICA / TUTTO SU TUTTO / 0→10

Root-level manifesto and operating plan for the canonical local-AI run.

This document defines the **0→10 operational lifecycle**. It tells a future AI/operator how to start, what must be produced, how evidence travels, and when the run is complete enough for the next chat/master-AI review.

Executable command syntax belongs in:

```text
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
Tools/workflow/run_unified_local_ai_refactor.ps1
```

Do not copy long PowerShell launcher blocks here.

## Canonical procedure

The active procedure is the unified launcher runbook:

```text
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
Tools/workflow/run_unified_local_ai_refactor.ps1
```

Current compact operational bridge:

```text
docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md
```

Large Markdown policy:

```text
docs/LOCAL_AI_TASKS/large-markdown-operational-policy-2026-05-05.md
```

Historical/supporting reference only:

```text
docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure.md
```

That historical procedure must not override the unified launcher, the launcher contract, this 0→10 plan, or current telemetry/evidence policy.

## Current active run-unica state

Current branch phase:

```text
Branch: codex/unified-local-ai-refactor-launcher
PR: #187 feat(workflow): add unified local AI refactor launcher
Current baseline run: 20260505-143844
Runtime bundle baseline: ia_carmine_refactor_reuse_full_run_bundle_20260505-143844.zip
Mode: review-only until explicit human instruction
```

Current next intended complex run family:

```text
Task family: unused/useful code + tool/class/helper promotion + MD/code consistency
Expected mode: run unica Full0To10 custom parameters
Expected artifact: complete evidence/telemetry bundle ZIP plus compact evidence pushed by the maintainer for now
Patch application: false unless explicitly requested later
Source writes: false unless explicitly requested later
```

Runtime bundles are generated artifacts. They may be published as draft release assets or uploaded to the chat, but they are not normal source commits.

## Core policy

```text
RUN UNICA = one parameterized launcher path
Full0To10 = TUTTO SU TUTTO perimeter
quick/balanced/deep/custom = presets or operator parameters, not scope
-No* flags = explicit opt-out from selected lanes
```

A canonical run-unica `Full0To10` activates every declared runtime/tool/provider/advisory/evidence/patch-spec/memory/telemetry/discovery/index/CSV-count lane unless an explicit maintenance/debug `-No*` flag disables one, the lane is diagnosed unavailable, the run is a dry-run planned state, or the operator documents a deliberate exclusion.

`Full0To10` is opt-out by lane, not opt-in per capability. Once the operator selects `-Full0To10`, the default assumption is that the full perimeter runs. If the operator does not want a lane, the operator says so explicitly.

A smoke run is separate and must not be treated as evidence that a run-unica `Full0To10` passed.

## 0→10 operating plan

### 0 — Start from clean state

Before a run, the operator or local AI must verify:

```text
correct branch
remote sync state
working tree status
staged local files are intentional
ignored output/cache/state files are not staged
no forbidden generated paths are staged
```

If local files are staged, decide before running whether they are part of the current documentation/task setup.

Do not continue blindly with unrelated dirty changes.

### 1 — Read compact current state

Read compact entrypoints first:

```text
AGENTS.md
CHATGPT.md
CHATGPT/README.md
docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md
docs/LOCAL_AI_TASKS/large-markdown-operational-policy-2026-05-05.md
README.md
WORKFLOW.md
docs/README.md
docs/LOCAL_AI_RUN_BOOTSTRAP.md
docs/LOCAL_AI_TASKS/README.md
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
docs/UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md
```

Large Markdown files are not first-read operational surfaces. Treat them as catalog/supporting/evidence unless a compact bridge points to a specific section.

### 2 — Select or create the task file

Every serious run must have a task file under:

```text
docs/LOCAL_AI_TASKS/
```

The task file must define:

```text
scope
objective
priority areas
required evidence surfaces
classification labels
guardrails
expected review-only outputs
patch-plan requirements
```

For the current complex refactor intelligence family, the task must explicitly ask for:

```text
unused but useful code
true dead-code candidates
reusable functions/classes/methods
helper extraction candidates
base-class or mixin opportunities
project-tool promotion candidates
broker-tool promotion candidates
run-unica lane promotion candidates
MD/code drift caused by obsolete references
safe mechanical patch candidates
manual-review refactor candidates
```

### 3 — Launch run unica Full0To10

Use the unified launcher runbook as command owner.

Required semantic settings:

```text
-Full0To10
-NoExecutionTail for long runs
custom parameters when the operator needs more capacity
review-only patch-plan behavior
no patch application
no Blender runtime
no FFmpeg runtime
no media output
```

The run must preserve the full semantic perimeter. Custom budgets and limits increase or reduce capacity, not scope.

### 4 — Produce complete evidence, telemetry and discovery surfaces

A complete run-unica handoff should produce or explicitly diagnose absence of:

```text
launcher manifest
phase_status / phase_reports
workflow report
integrated decision-loop report
deterministic recommendations
agent-review patch plan
provider diagnostics
ai_workload_report_quality
runtime tool usage telemetry
runtime tool capability manifest
full toolbox telemetry summary
shared AI-to-AI bundle/final summary
semantic chunk manifest
selected chunk evidence when available
Markdown inventory JSON/MD
script inventory JSON/CSV/MD
function/class/method inventory CSV when available
Python line-count CSV/MD
repository consistency map/smoke
auto-discovery report when relevant
index repair plan/report when relevant
```

If a surface is missing, the run must show whether it was disabled, unavailable, planned-only, degraded or unexpectedly absent.

### 5 — Verify guardrail state

The run is not ready for review until guardrail state is visible:

```text
patch_application_performed=false unless explicitly requested
source_writes_performed=false unless explicitly requested
Blender runtime not executed unless explicitly scoped
FFmpeg runtime not executed unless explicitly scoped
SQLite persistent writes absent unless explicitly scoped
output/** not staged
indexAI/code_chunks/** not staged
renders/** not staged
*.db / *.sqlite / *.sqlite3 not staged
```

Provider/probe lanes may execute as report-bound run-unica lanes, but they must be quality-gated and visible in telemetry/bundle surfaces.

### 6 — Build bundle ZIP

After the run, produce a complete bundle ZIP for chat/master-AI review.

Recommended naming:

```text
ia_carmine_<task_family>_full_run_bundle_<STAMP>.zip
```

For unused/useful/tool-promotion runs:

```text
ia_carmine_unused_useful_tool_promotion_full_run_bundle_<STAMP>.zip
```

The ZIP must include all useful artifacts needed for a next AI to reconstruct the run without opening raw local output trees blindly.

Required ZIP content classes:

```text
manifest and phase reports
shared AI-to-AI bundle/final summary
runtime telemetry and capability manifest
full toolbox telemetry summary
provider diagnostics and workload quality
recommendations and patch plan
script/function/class/method inventories
Python line-count CSV/MD
repository consistency reports
semantic/selected chunk evidence
auto-discovery/index repair reports when produced
compact Markdown summaries
artifact manifest or file list
```

Do not include raw media, renders, SQLite databases, or unbounded generated output unless explicitly requested for a narrow diagnostic.

### 7 — Promote compact evidence for Git review

For now, the maintainer performs the evidence push manually.

Commit only compact, reviewed, Git-trackable evidence when it is useful for PR review:

```text
docs/LOCAL_VALIDATION_EVIDENCE/*.json
docs/LOCAL_VALIDATION_EVIDENCE/*.md
```

Do not bulk-add the evidence directory. Add selected files only.

Never commit:

```text
output/**
output/validation/patch_bundles/**
renders/**
*.db
*.sqlite
*.sqlite3
indexAI/code_chunks/**
indexAI/project_code_chunks/**
raw audio/video/media output
```

The ZIP bundle may be uploaded to chat or attached as a draft release asset, but it should not become normal source code.

### 8 — Push selected evidence/state updates

Manual maintainer push is currently the official path for evidence publication.

Before push:

```text
git status
git diff --stat
git diff --check
review staged files one by one
```

Push only:

```text
new/updated task file when needed
compact evidence selected for review
current-state or handoff docs when needed
small documentation corrections caused by evidence
```

Do not push patch application, generated DBs, raw output, generated code chunks or media artifacts.

### 9 — Send bundle and telemetry to next AI/chat

After the run, send the next AI/chat:

```text
bundle ZIP
shared_toolbox_ai_to_ai_final_summary_<STAMP>.json
shared_toolbox_ai_to_ai_bundle_<STAMP>.json/md
full_toolbox_run_telemetry_summary_<STAMP>.json/md
runtime_tool_usage_telemetry_<STAMP>.json/md
runtime_tool_capability_manifest_<STAMP>.json/md
decision loop JSON/MD
recommendations JSON/MD
patch plan JSON/MD
script/function/class/method inventory CSV/MD/JSON
Python line-count CSV/MD
repository consistency reports
provider diagnostics
ai_workload_report_quality
auto-discovery/index repair reports when present
```

Also paste a compact status block:

```text
STAMP:
run passed/failed:
bundle zip name:
patch_plan_count:
recommendation_count:
provider_advisory_state:
provider_failure_detected:
deterministic_recovery_used:
patch_application_performed:
source_writes_performed:
tool_call_entry_count:
executed_count:
failed_count:
blocked_count:
CSV/count surfaces present:
script inventory present:
function/class/method inventory present:
repository consistency present:
auto-discovery/index repair present:
notes/warnings:
```
