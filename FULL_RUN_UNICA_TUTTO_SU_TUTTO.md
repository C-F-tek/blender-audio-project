# IA-Carmine — FULL RUN UNICA / TUTTO SU TUTTO

Root-level manifesto for the canonical full local-AI run.

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

Historical/supporting reference only:

```text
docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure.md
```

That historical procedure must not override the unified launcher, the launcher contract or current telemetry/evidence policy.

## Current active full-run state

Current branch phase:

```text
Branch: codex/unified-local-ai-refactor-launcher
PR: #187 feat(workflow): add unified local AI refactor launcher
Task: docs/LOCAL_AI_TASKS/refactor-reuse-methods-classes-tools-planning.md
Run: 20260505-143844
Runtime bundle: ia_carmine_refactor_reuse_full_run_bundle_20260505-143844.zip
Mode: review-only until explicit human instruction
```

The runtime bundle is a GitHub draft release asset linked from PR #187 and is intentionally not committed to the repository. Do not infer bundle contents from file existence alone.

## Core policy

```text
FULL RUN UNICA = TUTTO SU TUTTO
```

A canonical full run activates every declared runtime/tool/provider/advisory/evidence/patch-spec/memory/telemetry/discovery/index/CSV-count lane unless an explicit maintenance/debug `-No*` flag disables one, the lane is diagnosed unavailable, the run is a dry-run planned state, or the operator documents a deliberate exclusion.

`Full0To10` is opt-out by lane, not opt-in per capability. Once the operator selects `-Full0To10`, the default assumption is that the full perimeter runs. If the operator does not want a lane, the operator says so explicitly.

`quick`, `balanced`, `deep` and `custom` are intensity profiles only. They change capacity, not scope:

```text
quick    = full scope with reduced budget
balanced = full scope with default budget
deep     = full scope with expanded budget
custom   = full scope with operator-defined budget
```

A smoke run is separate and must not be treated as evidence that a full run passed.

## Expandable perimeter

The meaning of `tutto` is intentionally expandable.

When a new production-ready capability is promoted, it must be added to the full-run perimeter or explicitly excluded with rationale. Examples:

```text
broker tools
runtime capability manifests
provider diagnostics
GPU/NPU sync diagnostics
repository consistency map/smoke
project tool registry
memory/context builders
semantic chunk manifests
selected chunk evidence
Markdown inventory
script/function/class/method inventory
Python line-count CSV/Markdown surfaces
CSV/count summaries
auto-discovery reports
index repair plans/reports
patch-plan validators
production AI-to-AI bundle components
telemetry summaries
```

Silent omission is a defect.

## Discovery, index repair and CSV/count rule

Discovery and count surfaces are evidence lanes for `TUTTO SU TUTTO`.

Expected surfaces when relevant:

```text
Markdown inventory JSON/MD
script inventory JSON/CSV/MD
function/class/method inventory CSV
Python line-count CSV/MD
semantic chunk manifest JSON/MD
selected chunk evidence JSON/MD when available
repository consistency map/smoke JSON/MD
auto-discovery report when scanner/index visibility drift is suspected
index repair plan/report when generated indexes are stale or missing
```

Policy:

```text
CSV/count outputs are evidence surfaces, not source authority.
Generated indexes and code chunks are not hand-maintained source.
Do not commit output/**.
Do not commit indexAI/code_chunks/**.
Index repair is plan/report-first unless explicitly requested.
```

## Telemetry as completeness accessory

Telemetry is an obligatory completeness accessory for evidence and patch plans.

It does not replace evidence and it does not replace patch plans. It travels with them so the next AI can understand whether the evidence is complete and whether the patch plan was produced from a real, degraded, blocked or partial run.

Every production handoff should therefore group:

```text
evidence artifacts
patch-plan artifacts
runtime telemetry artifacts
runtime capability manifest
full toolbox telemetry summary
shared AI-to-AI bundle/final summary
discovery/index/CSV-count summaries when selected or relevant
```

A patch plan without telemetry is incomplete because the next AI cannot reliably know:

```text
which tools executed
which tools failed
which tools were blocked
which provider lane degraded
which capability was available
whether patch application happened
whether source writes happened
whether GPU/NPU timings are real or fallback
whether discovery/index/count evidence was produced, skipped or degraded
```

File existence alone is not proof of successful execution.

## Explicit disablers

Do not use these flags in the canonical production full run unless the goal is intentionally scoped maintenance/debug:

```text
-NoStrictRealRunActivation
-NoOllamaProbe
-NoNpuProbe
-NoNpuDecodeSmoke
-NoMultistepProvider
-NoWorkloadQuality
-NoMemoryWrite
-NoEvidence
-NoPatchSpecs
```

A disabled lane must remain visible as disabled in manifest, warnings, phase status or telemetry. It must not disappear silently.

## Guardrails

The run remains report/proposal oriented until a separate explicit patch-apply command is issued.

Destructive or irreversible operations are not runtime lanes and still require an explicit separate command:

```text
delete
force-push
rewrite history
merge to master/protected branch
deploy production
change secrets
change permissions
change billing
change repository visibility
```

Never commit:

```text
output/**
output/validation/patch_bundles/**
renders/**
*.db
*.sqlite
*.sqlite3
indexAI/code_chunks/**
```

## Current command owner

Current executable examples live in:

```text
docs/LOCAL_AI_TASKS/unified-local-ai-refactor-launcher.md
```

Do not duplicate long PowerShell launcher blocks here. The runbook owns command syntax, flags, profiles and validation examples.

## Production AI-to-AI communication standard

The production communication artifact for a successful full run is the shared toolbox bundle:

```text
docs/LOCAL_VALIDATION_EVIDENCE/shared_toolbox_ai_to_ai_bundle_<STAMP>.json
docs/LOCAL_VALIDATION_EVIDENCE/shared_toolbox_ai_to_ai_bundle_<STAMP>.md
```

This bundle is the standard post-run handoff between local IA-Carmine and the next AI/chat/operator session.

It must carry the run in compact, AI-readable form:

```text
workflow and integrated decision-loop references
deterministic recommendations and patch-plan references
runtime tool usage telemetry
runtime tool capability manifest references
full toolbox telemetry summary references
semantic chunk manifest references
selected chunk evidence references
script/function/class/method inventory references
Python line-count CSV/MD references
auto-discovery/index repair plan references when relevant
provider/probe/advisory state
GPU/NPU sync diagnostics
repository consistency map/smoke when produced
guardrail state: patch application, source writes, SQLite writes, Blender/FFmpeg execution
evidence files selected for Git-trackable handoff
```

The standard communication set for a full run is:

```text
docs/LOCAL_VALIDATION_EVIDENCE/shared_toolbox_ai_to_ai_bundle_<STAMP>.json
docs/LOCAL_VALIDATION_EVIDENCE/shared_toolbox_ai_to_ai_bundle_<STAMP>.md
docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_run_telemetry_summary_<STAMP>.json
docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_run_telemetry_summary_<STAMP>.md
docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_usage_telemetry_<STAMP>.json
docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_usage_telemetry_<STAMP>.md
docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_capability_manifest_<STAMP>.json
docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_capability_manifest_<STAMP>.md
docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_<STAMP>_cloud_semantic_deterministic_chunk_manifest.json
docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_<STAMP>_cloud_semantic_deterministic_chunk_manifest.md
docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_<STAMP>.json
docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_agent_review_decision_loop_<STAMP>.md
```

Additional compact evidence may accompany it when relevant:

```text
script/function/class/method inventory summaries
Python line-count CSV/MD summaries
repository consistency map/smoke summaries
auto-discovery/index repair plan summaries
selected chunk evidence summaries
```

The decision-loop evidence remains important, but it is not the whole production handoff by itself. Telemetry and capability data must accompany it.

## Full-run provider, bundle and broker completion contract

A production full run is complete only when the handoff proves these independent facts:

```text
provider_diagnostics_present = true
patch_plan_summary_seen = true
runtime_tool_usage_telemetry.executed_count >= 3 when broker lane ran
runtime_tool_capability_manifest present
full_toolbox_run_telemetry_summary present
discovery/index/CSV-count surfaces present when selected or relevant
patch_application_performed = false unless explicitly requested
source_writes_performed = false unless explicitly requested
```

Provider diagnostics must distinguish:

```text
provider_execution_seen
gpu_primary_advisory_succeeded
provider_failure_detected
deterministic_recovery_used
provider_failure_reasons
degraded_provider_components
```

The shared production bundle must promote the full-run patch plan summary from:

```text
output/patch_specs/full_toolbox_<STAMP>_agent_review_patch_plan.json
```

The runtime toolbox must be exercised by a minimal report-only broker bootstrap before the production bundle is built. The default bootstrap tools are:

```text
check_python_syntax
build_python_line_count_csv
check_validation_report_contract
```

The bootstrap remains report-only and must not perform patch application, source writes, Git writes, Blender runtime or persistent memory writes. Provider/probe lanes belong to the full-run perimeter but must remain report-bound and quality-gated.
