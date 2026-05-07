# Current operational state — IA-Carmine — post-PR187 / PR194 integration — 2026-05-07

## Status

Current operational bridge derived from repository code, GitHub PR state and the local merge of `origin/master` into `codex/md-bundle-telemetry-refactor`.

The filename keeps the original 2026-05-05 date for compatibility with existing reading flows. This content reflects the code/state observed during the 2026-05-07 PR #194 merge alignment.

## Source-of-truth basis

This bridge is based on code, GitHub state and current branch evidence, not only on previous handoff text:

```text
master contains Tools/workflow/run_unified_local_ai_refactor.ps1 from PR #187
master contains the unified launcher docs and Full0To10 doctrine
master contains docs/MAIN_RUNTIME_ARCHITECTURE.md
PR #194 contains the current Codex/provider-mesh/Markdown telemetry hardening branch
PR #192 adds report-only Full0To10 foundation tools on top of master
PR #191 contains a useful but diverged Full0To10 quick evidence branch
```

Code inspected for the current operational model:

```text
Tools/workflow/run_unified_local_ai_refactor.ps1
Tools/workflow/run_agent_review_full_toolbox_decision_loop.ps1
Tools/workflow/run_agent_review_full_toolbox_decision_loop.py
Tools/workflow/run_agent_review_full_toolbox_decision_loop/*.py
Tools/ai/run_agent_gpu_npu_parallel_orchestrator.py
Tools/ai/run_agent_gpu_deep_planning_supervised.py
Tools/ai/provider_runtime_heap*.py
Tools/ai/build_runtime_tool_usage_telemetry.py
Tools/ai/build_shared_toolbox_ai_to_ai_bundle.py
Tools/ai/build_full_toolbox_run_telemetry_summary.py
Tools/validation/check_ai_workload_report_quality.py
Tools/validation/check_provider_evidence_contract.py
```

## Active repository state

```text
Repository: C-F-tek/blender-audio-project
Default branch: master
Merged baseline: PR #187 feat(workflow): add unified local AI refactor launcher
Current integration branch: codex/md-bundle-telemetry-refactor
Current integration PR: #194 feat(ai): harden markdown pipeline telemetry bundle
Mode for ChatGPT/cloud work: GitHub-only/API unless local access is explicitly requested
```

## Active PR state

```text
PR #187: merged into master; unified launcher is now baseline.
PR #194: open integration candidate; hardens Markdown telemetry/evidence, provider mesh, Python workflow engine and live runtime heap.
PR #192: open report-only Full0To10 foundation checks; review after #194 alignment.
PR #191: open but diverged/non-mergeable; useful evidence branch, not a clean merge candidate as-is.
```

Operational interpretation:

```text
Do not treat #187 as the current active branch anymore.
Treat #187 as the merged baseline for launcher, Full0To10 doctrine, telemetry and compact evidence policy.
Treat #194 as the current Codex integration path for tool/provider/documentation promotion into master.
Treat #192 as the next clean report-only foundation candidate after local/API review.
Treat #191 as evidence to mine or regenerate with the newer bundle-completeness path, not as the preferred direct merge path.
```

## Current PR #194 state

PR #194 adds the current Codex local-AI operational layer.

Code/docs changed by that branch include:

```text
Tools/workflow/run_local_ai_task_via_pipeline.ps1 is now a thin adapter.
Tools/workflow/run_local_ai_task_via_pipeline/*.ps1 holds paths, context, enrichment, validation, manifest, evidence and telemetry responsibilities.
Tools/workflow/run_agent_review_full_toolbox_decision_loop.ps1 is a thin launcher.
Tools/workflow/run_agent_review_full_toolbox_decision_loop.py is the default Python control entrypoint.
Tools/workflow/run_agent_review_full_toolbox_decision_loop/*.py holds engine, mesh, product and support phases.
Tools/ai/build_code_interpreter_report.py delegates to Tools/ai/code_interpreter_report/*.
Tools/ai/build_repository_consistency_map.py delegates to Tools/ai/repository_consistency_map/*.
Tools/ai/provider_runtime_heap*.py provides runtime heap / live signal surfaces.
Tools/ai/run_agent_gpu_npu_parallel_orchestrator.py wires GPU1 primary advisory, GPU0 peer support, NPU micro support and broker bootstrap.
Tools/validation/check_local_ai_adapter_manifest.py recognizes telemetry outputs and emits explicit guardrail flags.
Tools/validation/check_generated_artifact_path_policy.py enforces compact path/name constraints for generated artifacts.
```

Operational interpretation:

```text
Markdown task runs should be able to prove proposals, patch specs, telemetry and compact evidence from a single review cycle.
Raw output remains runtime-only; compact evidence is the review/push surface.
The PowerShell wrapper should stay a human launcher, while Python owns production workflow orchestration.
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
providers publish observations, diagnostics, recommendations or microtask responses into shared state
broker unico executor is the future centralized tool execution gateway
semantic tools registry should become the capability source of truth
deterministic validators remain CPU authority for pass/fail claims
telemetry/event stream must expose executed, skipped, degraded and blocked phases
```

Current state:

```text
This is now both a documentation-level architecture target and a partially implemented runtime direction.
Implemented adjacent surfaces include unified launcher, Python decision-loop engine, runtime telemetry, capability manifest, broker telemetry/evidence, provider runtime heap and deterministic validators.
Missing blackboard/registry/event-stream details should be wired incrementally and report-only first.
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
Markdown: <= 500 lines per active .md file
Preferred active runbook: <= 400 lines
Python/PowerShell/scripts/source code: <= 400 lines per maintained source file
```

For Markdown over 500 lines:

```text
Keep the original file as a compact index.
Create a sibling folder named exactly like the file, including .md: <file>.md/.
Move detailed content into <file>.md/part-001.md, part-002.md, ...
Keep each part under 500 lines.
The index must list all parts and state that the document was split for the line policy.
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

Existing files already over line limits are technical debt. Do not split them blindly in documentation-only work; refactor them progressively when touching that area for a code task.

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
docs/LOCAL_AI_TASKS/gpu-peer-exchange-operational-principle.md
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

20260507 PR #194 provider mesh evidence:
  GPU1/Ollama primary advisory executed
  GPU0 peer support produced overlap/success evidence
  NPU micro support produced brokered tool-support evidence
  runtime heap telemetry and pending broker request closure are visible
  path policy validates compact generated artifact names
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
P0: complete PR #194 merge alignment so Codex tool/provider/docs changes can land in master.
P0: keep post-#187 operational docs aligned with code on master.
P0: use docs/MAIN_RUNTIME_ARCHITECTURE.md as the architecture target for blackboard/broker/registry/validator/telemetry work.
P1: review/validate PR #192 after #194 alignment.
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
