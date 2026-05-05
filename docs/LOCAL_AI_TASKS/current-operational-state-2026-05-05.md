# Current operational state — IA-Carmine — 2026-05-05

## Status

Current doc-only operational state bridge for PR #187 on branch `codex/unified-local-ai-refactor-launcher`.

This file exists to keep future agents oriented without requiring a full rewrite of long indexes or opening large runtime bundles first.

## Active repository state

```text
Repository: C-F-tek/blender-audio-project
Branch: codex/unified-local-ai-refactor-launcher
PR: #187 feat(workflow): add unified local AI refactor launcher
Mode for ChatGPT/cloud work: GitHub-only/API unless local access is explicitly requested
```

## Active doctrine

```text
Full0To10 = TUTTO SU TUTTO
quick/balanced/deep/custom = intensity, not scope
telemetry accompanies evidence and patch plans
AI-to-AI bundle, runtime telemetry, capability manifest and full toolbox telemetry summary are operational handoff surfaces
```

## Current active work item

```text
Task: docs/LOCAL_AI_TASKS/refactor-reuse-methods-classes-tools-planning.md
Run: 20260505-143844
Runtime bundle: ia_carmine_refactor_reuse_full_run_bundle_20260505-143844.zip
Bundle location: GitHub draft release asset linked from PR #187
Patch mode: review-only until explicit human instruction
```

The runtime bundle is not committed to the repository and must not be reconstructed from guesses.

## Current handoff state

Expected current handoff file:

```text
CHATGPT/next-chat-handoff-refactor-reuse-full-run-20260505-143844.md
```

If this file is absent from GitHub, it is expected to be pending local add/commit/push. Use the PR comment and compact notes as interim context, not as a replacement for the handoff.

## Compact docs to read before long indexes

```text
CHATGPT.md
CHATGPT/README.md
docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md
docs/LOCAL_AI_TASKS/refactor-reuse-full-run-documentation-coherence-2026-05-05.md
docs/LOCAL_AI_TASKS/recent-telemetry-state-2026-05-05.md
docs/LOCAL_AI_TASKS/refactor-reuse-methods-classes-tools-planning.md
docs/LOCAL_AI_TASKS/project-tool-registry.md
docs/TECH_DEBT_TRACKER.md
```

## Recent validated baseline

Recent committed evidence shows:

```text
20260505-073332:
  passed=true
  recommendation_count=5
  patch_plan_count=5
  provider_execution_performed=true
  runtime broker bootstrap executed=3 failed=0 blocked=0

20260505-081141:
  passed=true
  recommendation_count=3
  patch_plan_count=3
  provider_execution_performed=true
  patch_application_performed=false
  source_writes_performed=false
  runtime broker bootstrap executed=3 failed=0 blocked=0
  local_provider_probe passed=false with ollama: probe failed
  ai_workload_report_quality passed=true
  usable_lanes=['npu']
```

Interpretation:

```text
The old broker telemetry loss is closed unless a new regression appears.
Provider degradation can be acceptable when visible, quality-gated and recovered.
Patch planning remains review-only.
File existence is not proof of execution; inspect telemetry fields.
```

## Current bundle inspection requirement

Before selecting any refactor/reuse patch from run `20260505-143844`, inspect:

```text
unified_local_ai_refactor_manifest.json
decision loop
recommendations
patch plan
runtime tool usage telemetry
runtime capability manifest
full toolbox telemetry summary
shared toolbox AI-to-AI bundle/final summary
provider diagnostics
ai_workload_report_quality
```

If the GitHub connector cannot download the draft release asset, state that limitation and continue only with committed evidence and PR comments.

## Candidate refactor family from committed code/docs inspection

The current safe-looking candidate family is:

```text
centralize report/telemetry helper functions in Tools/validation/report_utils.py
reuse them from Tools/ai/build_runtime_tool_usage_telemetry.py
reuse them from Tools/ai/build_full_toolbox_run_telemetry_summary.py
evaluate Tools/ai/build_shared_toolbox_ai_to_ai_bundle.py separately after bundle review
```

This remains provisional until the `20260505-143844` bundle is inspected.

## Current patch classification policy

Every recommendation/patch plan must be classified as one of:

```text
SAFE_MECHANICAL
MANUAL_REVIEW
LOCAL_VALIDATION_REQUIRED
BLENDER_RUNTIME_REQUIRED
PROVIDER_VALIDATION_REQUIRED
DEFER
DO_NOT_PROMOTE
```

## Known documentation drift to clean incrementally

Some long indexes may still describe broker telemetry follow-up as active work.

Current policy:

```text
Treat broker telemetry follow-up as historical/resolved unless investigating a new regression.
Treat refactor/reuse bundle inspection as the current active P1.
Treat external-controls pass-through as a follow-up, not as the current active task unless explicitly selected.
```

Preferred cleanup strategy:

```text
small focused doc patches
compact bridge notes
no full API rewrites of large Markdown indexes unless necessary
run docs-link/report-contract validation locally when available
```

## Hard guardrails

```text
No merge to master.
No delete, force-push or rewrite history.
No deploy.
No secret/permission/billing/visibility changes.
No commit of output/**.
No commit of indexAI/code_chunks/**.
No commit of *.db, *.sqlite or *.sqlite3.
No commit of renders/**.
No Blender runtime.
No FFmpeg runtime.
No provider execution without explicit request.
No automatic patch-spec apply.
No broad triple-quote/raw multiline rewrites for command-example cleanup.
```
