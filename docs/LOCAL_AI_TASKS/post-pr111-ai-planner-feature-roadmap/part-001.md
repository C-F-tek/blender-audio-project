<!-- IA-CARMINE-MD-SPLIT: part -->
# post-pr111-ai-planner-feature-roadmap — parte 001 di 002

Sorgente indice: [`../post-pr111-ai-planner-feature-roadmap.md`](../post-pr111-ai-planner-feature-roadmap.md)

## Navigazione

- [Indice](README.md)
- [Parte successiva](part-002.md)

# Post-PR111 AI Planner Feature Roadmap

## Purpose

Roadmap for the next AI/tooling improvements after PR #109 and PR #111.

The current refactoring level is now sufficient to reason about the pipeline as a reusable, evidence-driven local AI system instead of a set of isolated scripts.

This document captures candidate features beyond:

```text
feat(ai): harden GPU planner JSON output contract
```

## Current baseline

Recent merged work established:

```text
PR #109: manual-review code patch plan lane and modular GitHub evidence bundle helpers
PR #111: explicit report-only GPU repair-failure recommendation layer
project complete AI-to-AI procedure: canonical 0->10 runbook
project complete AI-to-AI request: canonical Markdown task request for local AI lanes
```

Observed reference run:

```text
provider execution: true
GPU planner execution: true
NPU checkpoint audits: true, 5 succeeded
GPU recommendations: 0
empty reason: repair_attempt_failed
fallback manual-review patch plan: 12 candidates
bundle and GitHub audit flow: working
```

## Feature 1 — Harden GPU planner JSON output contract

Primary next feature.

Goal:

```text
reduce repair_attempt_failed and schema-mismatch outputs
```

Candidate changes:

```text
reuse Tools.ai.model_json.parse_model_json_object in GPU parsing paths
add a JSON-only final prompt footer
forbid top-level files/content_preview/raw context echo in model output
separate schema_mismatch from JSON parse failure
record first parse error and raw response preview hash per failed round
```

Expected outcome:

```text
more valid GPU recommendation objects
fewer fallback-only runs
clearer failure classification when the model returns context echo instead of recommendations
```

## Feature 2 — Context echo detector

Goal:

```text
detect when the model returns the input context instead of the expected recommendation schema
```

Trigger examples:

```text
top-level files key
large content_preview fields in output
AGENTS.md / WORKFLOW.md echoed as JSON payload
response dominated by source preview rather than recommendations
```

Output classification:

```text
empty_recommendations_reason: context_echo_detected
schema_status: wrong_json_shape
recommended_next_layer: compact_prompt_retry or build_agent_review_patch_plan.py
```

Why it matters:

```text
The reference run showed a fenced JSON response containing files/content_preview instead of the expected recommendations object. This is not merely broken JSON; it is a task-shape failure.
```

## Feature 3 — Compact prompt retry lane

Goal:

```text
when a full-context GPU round fails with context echo or parse failure, retry once with a compact evidence-only prompt
```

Input should be reduced to:

```text
objective
required schema
summary of evidence readiness
top fallback/manual-review candidates
short file/module list
no raw content_preview blocks
```

Guardrails:

```text
one retry only by default
same provider/model settings
report-only
no patch application
retry result stored separately from original round
```

Expected outcome:

```text
recover usable recommendations without increasing token budget or changing provider settings first
```

## Feature 4 — Recommendation schema validator

Goal:

```text
validate model recommendation objects before they enter merge/filter logic
```

Checks:

```text
required keys present
status in allowed enum
risk in allowed enum
target_files list of strings
validation_commands list of strings
stop_conditions list of strings
no raw file previews embedded in recommendation
```

Output:

```text
valid_recommendation_count
invalid_recommendation_count
invalid_recommendation_reasons
schema_mismatch_count
```

Why it matters:

```text
A valid JSON object can still be unusable if it has the wrong shape. The planner should distinguish parse failure from semantic contract failure.
```

## Feature 5 — Provider agreement matrix

Goal:

```text
compare static/code-interpreter, GPU planner, NPU auditor and fallback patch-plan signals in one report
```

Rows:

```text
target file/module
static signal
GPU signal
NPU signal
fallback signal
risk
next action
```

Expected output:

```text
output/analysis/provider_agreement_matrix_<STAMP>.json
output/analysis/provider_agreement_matrix_<STAMP>.md
```

Why it matters:

```text
The current bundle proves all lanes can run, but the reviewer still has to manually correlate evidence across reports.
```

## Feature 6 — AI improvement impressions extractor

Goal:

```text
extract and normalize the AI improvement impressions requested by the canonical Markdown task
```

Output categories:

```text
evidence-backed
inferred from multiple signals
speculative but potentially useful
```

Each item should include:

```text
title
why it may improve the project
evidence signals
risk if ignored
minimal next action
issue/doc/PR classification
```

Why it matters:

```text
The request document now asks for impressions, but they should be structured so they can become issues, tasks or PR candidates.
```

## Feature 7 — Automatic issue/task candidate pack

Goal:

```text
turn validated recommendations and AI improvement impressions into issue/task candidate artifacts
```

Output only, no GitHub mutation by default:

```text
output/ai_pipeline/repository_issue_candidates_<STAMP>.json
output/ai_pipeline/repository_issue_candidates_<STAMP>.md
```

Each candidate:

```text
title
body
labels
risk
source evidence
suggested owner lane
manual approval required
```

Guardrail:

```text
creating GitHub issues remains explicit, not automatic
```

## Feature 8 — Reusable project-agnostic AI pipeline profile

Goal:

```text
make the local AI-to-AI pipeline easier to reuse outside this Blender project
```

Candidate abstraction:

```text
profile YAML/JSON for context roots
excluded paths
provider lanes
bundle policy
validation commands
artifact naming
```

Example profiles:

```text
project_complete_ai_to_ai
project_only_no_legacy
docs_contract_review
provider_json_contract_hardening
```

Why it matters:

```text
The refactor now separates evidence, provider execution, bundle generation and review enough to turn the workflow into a reusable local AI review framework.
```

## Feature 9 — Run manifest and reproducibility index

Goal:

```text
make each complete run reproducible from one manifest
```

Manifest fields:

```text
run_id
stamp
branch
commit_sha
request_md
procedure_md
context_roots
provider settings
input reports
output artifacts
bundle path
validation result
```

Expected output:

```text
output/ai_pipeline/run_manifest_<STAMP>.json
docs/LOCAL_VALIDATION_EVIDENCE/run_manifest_<STAMP>.md or included in bundle
```

Why it matters:

```text
The run procedure is now stable, but reproducing an exact run still requires reading command history and multiple reports.
```
