<!-- IA-CARMINE-MD-SPLIT: part -->
# FULL_RUN_UNICA_TUTTO_SU_TUTTO — parte 002 di 002

Sorgente indice: [`../FULL_RUN_UNICA_TUTTO_SU_TUTTO.md`](../FULL_RUN_UNICA_TUTTO_SU_TUTTO.md)

## Navigazione

- [Indice](README.md)
- [Parte precedente](part-001.md)

### 10 — Master-AI review and next patch selection

The next AI/chat must review the bundle in this order:

```text
final summary
runtime telemetry
capability manifest
full toolbox telemetry summary
provider/workload quality
shared AI-to-AI bundle
decision loop
recommendations
patch plan
inventory CSV/count surfaces
repository consistency/discovery/index reports
```

The output of step 10 is not automatic apply. It is a selected next action:

```text
SAFE_MECHANICAL documentation patch
MANUAL_REVIEW refactor patch
project-tool promotion patch
broker-tool promotion patch
run-unica lane promotion patch
shared-helper extraction patch
base-class/mixin design patch
unused-but-useful inventory refinement
true dead-code deprecation plan
local validation request
provider validation request
Blender runtime validation request
DEFER / DO_NOT_PROMOTE decision
```

Patch application remains separate and explicit.

## Classification labels for complex refactor runs

Use these labels for recommendations and patch plans:

```text
PROMOTE_TO_PROJECT_TOOL
PROMOTE_TO_BROKER_TOOL
PROMOTE_TO_RUN_UNICA_LANE
EXTRACT_SHARED_HELPER
EXTRACT_BASE_CLASS_OR_MIXIN
KEEP_APP_DOMAIN
KEEP_HISTORICAL_SUPPORTING
DEPRECATE_DOC_ONLY
DEAD_CODE_CANDIDATE
UNUSED_BUT_USEFUL
GENERATED_DO_NOT_TOUCH
LOCAL_VALIDATION_REQUIRED
BLENDER_RUNTIME_REQUIRED
PROVIDER_VALIDATION_REQUIRED
DEFER
DO_NOT_PROMOTE
```

Every item must include:

```text
target file or component
evidence source
rationale
risk
validation minimum
source-write requirement later or none
provider-validation requirement or none
Blender-runtime requirement or none
forbidden path check
```

## Expandable perimeter

The meaning of `tutto` is intentionally expandable.

When a new production-ready capability is promoted, it must be added to the run-unica perimeter or explicitly excluded with rationale. Examples:

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

Every production handoff should group:

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

Do not use these flags in the canonical production run-unica Full0To10 run unless the goal is intentionally scoped maintenance/debug:

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
indexAI/project_code_chunks/**
raw audio/video/media output
```

## Production AI-to-AI communication standard

The production communication artifact for a successful run-unica Full0To10 run is the shared toolbox bundle:

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
bundle ZIP filename or release/upload location when available
```

The decision-loop evidence remains important, but it is not the whole production handoff by itself. Telemetry, capability, discovery/count surfaces and bundle metadata must accompany it.

## Run-unica provider, bundle and broker completion contract

A production run-unica Full0To10 run is complete only when the handoff proves these independent facts:

```text
provider_diagnostics_present = true
patch_plan_summary_seen = true
runtime_tool_usage_telemetry.executed_count >= 3 when broker lane ran
runtime_tool_capability_manifest present
full_toolbox_run_telemetry_summary present
discovery/index/CSV-count surfaces present when selected or relevant
bundle_zip_produced = true for chat/master-AI review
selected_compact_evidence_pushed_or_ready = true
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

The shared production bundle must promote the run-unica patch plan summary from:

```text
output/patch_specs/full_toolbox_<STAMP>_agent_review_patch_plan.json
```

The runtime toolbox must be exercised by a minimal report-only broker bootstrap before the production bundle is built. The default bootstrap tools are:

```text
check_python_syntax
build_python_line_count_csv
check_validation_report_contract
```

The bootstrap remains report-only and must not perform patch application, source writes, Git writes, Blender runtime or persistent memory writes. Provider/probe lanes belong to the run-unica perimeter but must remain report-bound and quality-gated.

## Current human/manual evidence push rule

For now, the maintainer pushes selected compact evidence manually.

A future automation may assist, but until explicitly implemented and approved:

```text
bundle ZIP can be produced locally and uploaded/attached by maintainer
selected docs/LOCAL_VALIDATION_EVIDENCE artifacts can be manually added, committed and pushed by maintainer
no automatic bulk evidence commit
no automatic output/** commit
no automatic patch apply
no automatic merge
```
