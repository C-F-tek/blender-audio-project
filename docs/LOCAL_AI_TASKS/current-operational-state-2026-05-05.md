# Current operational state — IA-Carmine — post-PR187 — 2026-05-06

## Status

Current doc-only operational bridge derived from the repository code and open PR state after merge of PR #187 into `master`.

The filename keeps the original 2026-05-05 date for compatibility with existing reading flows. This content reflects the code/state observed on 2026-05-06.

## Source-of-truth basis

This bridge is based on code and GitHub state, not only on previous handoff text:

```text
master contains Tools/workflow/run_unified_local_ai_refactor.ps1 from PR #187
master contains the unified launcher docs and Full0To10 doctrine
PR #192 adds report-only Full0To10 foundation tools on top of master
PR #191 contains a useful but diverged Full0To10 quick evidence branch
```

Code inspected for the current operational model:

```text
Tools/workflow/run_unified_local_ai_refactor.ps1
Tools/ai/build_runtime_tool_usage_telemetry.py
Tools/ai/build_shared_toolbox_ai_to_ai_bundle.py
Tools/ai/build_full_toolbox_run_telemetry_summary.py
Tools/validation/check_ai_workload_report_quality.py
```

Code inspected from the next candidate PR #192:

```text
Tools/ai/build_full_run_evidence_bundle_zip.py
Tools/ai/full_run_bundle_zip/*
Tools/ai/build_runtime_hardware_capability_manifest.py
Tools/ai/runtime_hardware_capability/*
Tools/validation/check_full_run_bundle_completeness.py
Tools/validation/full_run_bundle_completeness.py
Tools/validation/check_runtime_hardware_delegation_contract.py
Tools/validation/runtime_hardware_delegation_checks.py
```

## Active repository state

```text
Repository: C-F-tek/blender-audio-project
Default branch: master
Merged baseline: PR #187 feat(workflow): add unified local AI refactor launcher
Current GitHub-only documentation branch: codex/main-runtime-architecture-blackboard
Mode for ChatGPT/cloud work: GitHub-only/API unless local access is explicitly requested
```

## Active PR state

```text
PR #187: merged into master; unified launcher is now baseline.
PR #192: open and mergeable; report-only Full0To10 foundation checks.
PR #191: open but diverged/non-mergeable; useful evidence branch, not a clean merge candidate as-is.
```

Operational interpretation:

```text
Do not treat #187 as the current active branch anymore.
Treat #187 as the merged baseline for launcher, Full0To10 doctrine, telemetry and compact evidence policy.
Treat #192 as the next clean report-only foundation candidate after local/API review.
Treat #191 as evidence to mine or regenerate with the newer bundle-completeness path, not as the preferred direct merge path.
```

## Main runtime architecture target

The current target runtime architecture is documented in:

```text
docs/MAIN_RUNTIME_ARCHITECTURE.md
```

Target topology:

```text
shared runtime heap / blackboard
├─ GPU1 primary advisory / planner
├─ GPU0 coworker/helper OpenVINO
├─ NPU microtask responder
├─ broker unico executor
├─ semantic tools registry
├─ deterministic validators / CPU authority
└─ telemetry/event stream
```

Operational interpretation:

```text
providers publish observations, diagnostics, recommendations or microtask responses into shared state;
broker unico executor is the future centralized tool execution gateway;
semantic tools registry should become the capability source of truth;
deterministic validators remain CPU authority for pass/fail claims;
telemetry/event stream must expose executed, skipped, degraded and blocked phases.
```

Current state:

```text
This is a documentation-level architecture target on this branch.
It does not claim that every component is already implemented in code.
Existing code already has strong adjacent surfaces: unified launcher, runtime telemetry, capability manifest, broker telemetry/evidence and deterministic validators.
Future implementation should wire missing blackboard/registry/event-stream details incrementally and report-only first.
```

## Launcher code contract now on master

`Tools/workflow/run_unified_local_ai_refactor.ps1` is the canonical local AI operator entrypoint.

The launcher code exposes these mode families:

```text
smoke
reset
validation
md
json
python
chunks
context_pack
agent_state
official
provider
patch_specs
evidence
contract
full_validation
all
```

The launcher code is report/proposal-only by default. It declares no patch apply, no commit, no push, no merge, no Blender runtime and no FFmpeg runtime.

Reset mode remains plan-only unless both conditions are true:

```text
-ApplyReset
-ConfirmResetText "DELETE LOCAL AI ARTIFACTS"
```

## Full0To10 doctrine from code/docs

```text
Full0To10 = TUTTO SU TUTTO
quick/balanced/deep/custom = intensity, not scope
all full-run lanes are included by default
if the operator does not want a lane, the operator must disable it explicitly with -No* flags or documented exclusion
telemetry accompanies evidence and patch plans
AI-to-AI bundle, runtime telemetry, capability manifest and full toolbox telemetry summary are operational handoff surfaces
```

Provider/probe policy for full runs:

```text
In a Full0To10 run, provider probes, provider diagnostics, workload quality, runtime broker telemetry and capability manifests are expected by default.
They do not require a separate per-lane confirmation once Full0To10 is selected.
They may be skipped only through explicit -No* flags, unavailable-tool/provider diagnostics, dry-run planned state or a documented operator exclusion.
```

Relevant explicit disablers:

```text
-NoOllamaProbe
-NoNpuProbe
-NoNpuDecodeSmoke
-NoMultistepProvider
-NoWorkloadQuality
-NoMemoryWrite
-NoEvidence
-NoPatchSpecs
```

## 400-line policy for documentation and code

Hard limit for maintained files:

```text
Markdown: <= 400 lines per active .md file
Python/PowerShell/scripts/source code: <= 400 lines per maintained source file
```

For Markdown over 400 lines:

```text
Keep the original file as a compact index.
Create a sibling folder named exactly like the file, including .md: <file>.md/.
Move detailed content into <file>.md/part-001.md, part-002.md, ...
Keep each part under 400 lines.
The index must list all parts and state that the document was split for the 400-line policy.
```

Markdown example:

```text
docs/LOCAL_AI_TASKS/example.md
docs/LOCAL_AI_TASKS/example.md/part-001.md
docs/LOCAL_AI_TASKS/example.md/part-002.md
```

For code over 400 lines:

```text
Keep the public entrypoint/wrapper compact.
Move implementation into a same-purpose package or module folder.
Split by responsibility, not by arbitrary line number only.
Keep each module/file under 400 lines.
Preserve CLI/API compatibility unless the task explicitly allows breaking changes.
Report resulting line count for every created or modified code/script file.
```

Code examples:

```text
Tools/ai/example_tool.py                 # thin wrapper under 400 lines
Tools/ai/example_tool/cli.py             # under 400 lines
Tools/ai/example_tool/core.py            # under 400 lines
Tools/ai/example_tool/reports.py         # under 400 lines

Tools/workflow/example_runner.ps1        # thin wrapper under 400 lines
Tools/workflow/example_runner/phase.ps1  # under 400 lines
```

Existing files already over 400 lines are technical debt. Do not split them blindly in documentation-only work; refactor them progressively when touching that area for a code task.

## Canonical entrypoint

```text
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
Tools/workflow/run_unified_local_ai_refactor.ps1
```

Use the unified launcher runbook for current commands. Do not recreate old parallel 0-to-10 runbooks as active entrypoints.

## Current compact docs to read before long indexes

```text
AGENTS.md
CHATGPT.md
CHATGPT/README.md
docs/LOCAL_AI_TASKS/current-operational-state-2026-05-05.md
docs/MAIN_RUNTIME_ARCHITECTURE.md
docs/LOCAL_AI_TASKS/recent-telemetry-state-2026-05-05.md
docs/LOCAL_AI_TASKS/refactor-reuse-full-run-documentation-coherence-2026-05-05.md
docs/LOCAL_AI_TASKS/refactor-reuse-methods-classes-tools-planning.md
docs/LOCAL_AI_TASKS/project-tool-registry.md
docs/TECH_DEBT_TRACKER.md
```

## Recent validated baselines

Committed/observed evidence before and after #187 shows:

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

20260506-004242 from PR #191:
  passed=true
  recommendation_count=20
  patch_plan_count=20
  provider_execution_performed=true
  patch_application_performed=false
  source_writes_performed=false
  deterministic_synthesizer_used=true
  runtime broker bootstrap executed=3 failed=0 blocked=0
  branch diverged from master after #187 merge
```

Interpretation:

```text
The old broker telemetry loss is closed unless a new regression appears.
Provider degradation can be acceptable when visible, quality-gated and recovered.
Patch planning remains review-only.
File existence is not proof of execution; inspect telemetry fields.
Large evidence PRs should be replaced or complemented by compact bundle-completeness surfaces.
```

## PR #192 code-derived status

PR #192 adds a report-only foundation layer that is consistent with the current code direction.

It introduces small modular code for:

```text
recursive Full0To10 evidence ZIP bundle creation
bundle completeness validation
runtime hardware capability manifest for CPU/GPU.0/NPU/NVIDIA visibility
hardware/delegation report-only contract validation
```

Expected resource visibility in the hardware manifest:

```text
CPU
GPU.0
NPU
NVIDIA_GPU
```

Expected side-effect contract:

```text
source_writes_allowed=false
patch_application_allowed=false
persistent_memory_write_allowed=false
media_runtime_allowed=false
network_or_secret_access_allowed=false
allowed_side_effects=[read_only, report_only]
```

Expected local validation before merge:

```text
py_compile new Python modules
hardware capability manifest generation
hardware/delegation contract validation
bundle completeness validation against a real or staged ZIP when available
git diff --check
git status --short
```

Guardrails for #192:

```text
no provider generation
no Blender runtime
no FFmpeg runtime
no patch-spec apply
no SQLite DB commit
no output/** commit
hardware lanes remain report-only visibility/capability entries
```

## Repository consistency state

The latest useful evidence still shows high repository-consistency noise. Do not apply automatic patch plans across all findings.

Preferred cleanup strategy:

```text
classify historical/generated/evidence docs separately from active runbooks
fix active stale references first
avoid editing compact evidence as if it were source documentation
use small focused doc patches
validate docs links/report contracts locally when available
```

## Current next-step recommendation

Priority order:

```text
P0: keep post-#187 operational docs aligned with code on master.
P0: review/validate PR #192 as the next clean report-only foundation layer.
P0: use docs/MAIN_RUNTIME_ARCHITECTURE.md as the architecture target for blackboard/broker/registry/validator/telemetry work.
P1: do not merge PR #191 as-is; rebase/regenerate/summarize its evidence after #192 or close/supersede.
P1: reduce repository-consistency noise incrementally, focused on active docs only.
P1: implement main runtime architecture incrementally with report-only validators and manifests first.
P2: decide whether provider-declared runtime tool requests remain advisory-only or become broker-executed feedback.
```

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

## Hard guardrails

```text
No merge to master without explicit human command.
No delete, force-push or rewrite history.
No deploy.
No secret/permission/billing/visibility changes.
No commit of output/**.
No commit of indexAI/code_chunks/**.
No commit of *.db, *.sqlite or *.sqlite3.
No commit of renders/**.
No Blender runtime.
No FFmpeg runtime.
No automatic patch-spec apply.
No broad triple-quote/raw multiline rewrites for command-example cleanup.
Full0To10 is opt-out by lane: provider/probe/telemetry/discovery lanes are included unless explicitly disabled or diagnosed unavailable.
```
