# Codex App Handoff — Next Steps

## Repository

```text
C-F-tek/blender-audio-project
```

## Current working project title

```text
IA-Carmine Local AI Orchestration Workbench
```

The GitHub repository slug is historical. The active architecture is no longer Blender/audio-centric. Blender/audio remains the first application domain and legacy runtime target, but the current core is local AI orchestration, provider-lane routing, validation, guardrails and evidence bundles.

## Current baseline

This handoff originally started after PR #48. As of 2026-05-01, `master` is further ahead:

```text
ef6da71 feat(ai): add full-context golden proposal generator (#82)
```

The PR #48 provider-lane work is still the baseline for GPU/NPU advisory routing, but current next-step planning should also account for later selected-context, full-context and proposal-generator work.

Recent current capabilities on `master`:

```text
selected semantic chunk generation
selected-chunks contract/evidence validation
bounded context packs
SQLite-backed agent state packet usage in local runs
full-context AI/NPU golden path task entrypoint
full-context golden proposal coverage validator
deterministic full-context golden proposal generator
```

Provider-lane capabilities from PR #48 remain:

```text
quality-based advisory context filtering
Ollama/GPU primary advisory provider support
OpenVINO/NPU probe and decode-smoke diagnostics
parallel GPU/NPU multistep workflow
compact GitHub evidence bundles under docs/LOCAL_VALIDATION_EVIDENCE/
updated documentation identity for IA-Carmine local AI orchestration
```

## Provider mapping

Keep this mapping fixed:

```text
Ollama   -> GPU/CUDA -> primary advisory provider
OpenVINO -> NPU      -> probe / guardrail / decode diagnostic
```

Do not introduce OpenVINO GPU as a primary lane.

## Validated evidence already present

Important current evidence includes:

```text
docs/LOCAL_VALIDATION_EVIDENCE/parallel_gpu_npu_multistep_real_npu_v2_evidence.json
docs/LOCAL_VALIDATION_EVIDENCE/full_context_golden_selected_chunks_evidence.json
docs/LOCAL_VALIDATION_EVIDENCE/full_context_golden_core_ai_backend_context_pack_evidence.json
docs/LOCAL_VALIDATION_EVIDENCE/full_context_golden_local_ai_context_evidence.json
docs/LOCAL_VALIDATION_EVIDENCE/full_context_golden_local_ai_context_multistep_evidence.json
```

Validated decision summary:

```text
ollama_gpu_primary_advisory: true
npu_excluded_when_unusable: true
provider_execution_seen: true
npu_decode_smoke_passed: true
```

Meaning:

- Ollama/GPU is validated as the primary advisory lane when explicitly enabled.
- The old NPU workload report remains unusable and is excluded from advisory context.
- NPU/OpenVINO decode smoke passes through the dedicated NPU Python executable.
- NPU is validated for probe/diagnostic use, not yet as a general advisory lane.

## First action in Codex App

Start from clean `master`:

```powershell
git checkout master
git pull --ff-only
git status
```

Expected state:

```text
On branch master
Your branch is up to date with 'origin/master'.
nothing to commit, working tree clean
```

Then read these files in order:

```text
README.md
AGENTS.md
WORKFLOW.md
docs/README.md
docs/PROJECT_STATUS_POINT.md
docs/DATA_FLOW.md
docs/LOCAL_AI_WORKFLOW.md
docs/JSON_SCHEMAS.md
docs/LOCAL_AI_TASKS/README.md
Tools/npu/pipeline/README.md
Tools/validation/README.md
docs/LOCAL_VALIDATION_EVIDENCE/parallel_gpu_npu_multistep_real_npu_v2_evidence.md
docs/LOCAL_VALIDATION_EVIDENCE/full_context_golden_local_ai_context_evidence.md
```

## Current recommended next action

Use the full-context golden proposal families as the next controlled work queue:

```text
P1 adapter manifest validator
P2 reusable enrichment-plan helper
P3 full-context golden path docs contract
P4 optional wrapper preset flag
P5 selected-chunks evidence standard validation block
P6 NPU knowledge-broker / context-oracle prototype
```

Promote one family at a time into a reviewed patch spec or focused implementation PR. Keep provider execution explicit and do not apply patches automatically.

## Provider baseline validation to run when needed

Run a post-merge provider evidence workflow only when fresh GPU/NPU evidence is needed:

```powershell
powershell.exe -ExecutionPolicy Bypass -File .\Tools\workflow\run_parallel_ai_provider_multistep.ps1 `
  -Profile npu `
  -RunOllamaProbe `
  -RunNpuProbe `
  -RunNpuDecodeSmoke `
  -UsePrimaryAdvisoryProvider `
  -Basename master_post_merge_gpu_npu_multistep `
  -ProposalBasename master_post_merge_gpu_npu_multistep_proposals `
  -EvidenceBasename master_post_merge_gpu_npu_multistep_evidence
```

Then commit only compact evidence:

```powershell
git add docs/LOCAL_VALIDATION_EVIDENCE/
git commit -m "test: add master post-merge gpu npu evidence"
git push
```

Do not commit ignored `output/` files.

## Immediate review after evidence generation

Inspect:

```powershell
Get-Content .\docs\LOCAL_VALIDATION_EVIDENCE\master_post_merge_gpu_npu_multistep_evidence.json -Raw
Get-Content .\docs\LOCAL_VALIDATION_EVIDENCE\master_post_merge_gpu_npu_multistep_evidence.md -Raw
git status
git diff --stat HEAD~1..HEAD
```

Expected decision fields:

```text
ollama_gpu_primary_advisory: true
npu_excluded_when_unusable: true
provider_execution_seen: true
npu_decode_smoke_passed: true
```

If `npu_decode_smoke_passed` is false, inspect the report summary for:

```text
python_exe
device
raw_exit_code
provider_envelope.error
```

The NPU smoke must use the dedicated Python executable from `Tools.npu.npu_runtime.DEFAULT_NPU_PYTHON`.

## Next milestones

### 1. Formal schema documentation for new reports

Priority: high.

Add/extend schema notes in:

```text
docs/JSON_SCHEMAS.md
docs/AI_ARTIFACT_SCHEMAS.md
Tools/validation/README.md
```

Report kinds to document:

```text
ai_workload_quality_lane_routing
npu_decode_quality_remediation
npu_decode_smoke_diagnostic
github_validation_evidence_bundle
```

Expected output:

- field tables;
- required/optional fields;
- producer tool;
- consumer tool;
- validation command;
- promotion/stop conditions.

Do not make validators stricter until representative local evidence exists on `master`.

### 2. Add contract validator for evidence bundles

Priority: high.

Candidate new validator:

```text
Tools/validation/check_github_evidence_bundle.py
```

Scope:

- validate files under `docs/LOCAL_VALIDATION_EVIDENCE/*.json`;
- check `kind == github_validation_evidence_bundle`;
- check `schema_version == 1`;
- check `decision` fields exist;
- check every summarized report has `path`, `exists`, `json_ok`, `kind`, `passed`, `summary`;
- report warnings, not hard failures, for missing optional provider fields.

Keep it non-invasive and stdlib-only.

### 3. NPU advisory promotion planning

Priority: medium.

Do not promote NPU to general advisory based only on smoke success.

Create a future milestone only if needed:

```text
P-NPU-ADVISORY-PROMOTION-GATE
```

Minimum acceptance criteria:

```text
real NPU workload report is classified usable_text
alpha_ratio and word_count pass quality thresholds
output is not numeric/hex-like
report has useful natural language content
quality gate lists npu in usable_lanes
advisory routing can trust npu without contaminating packet context
```

Until then:

```text
NPU/OpenVINO = probe / guardrail / decode diagnostic
Ollama/GPU   = primary advisory provider
```

### 4. Project rename decision

Priority: medium.

Documentation now uses:

```text
IA-Carmine Local AI Orchestration Workbench
```

Repository slug remains:

```text
C-F-tek/blender-audio-project
```

Do not rename the GitHub repository without explicit maintainer confirmation, because it changes remotes/URLs and may affect workflows.

If maintainer confirms rename, prepare a separate issue/PR checklist first:

```text
new repo slug
remote update commands
docs URL updates
GitHub Actions impact
local clone impact
external links impact
fallback plan
```

### 5. Execution plan reconciliation

Priority: medium.

Review active plans:

```text
docs/EXECUTION_PLANS/active/
```

Move completed/stale plans only when there is evidence they are done or superseded.

Run:

```powershell
python .\Tools\validation\check_execution_plan_status.py --repo-root . --output .\output\validation\execution_plan_status.json
```

### 6. Tech-debt tracker update

Priority: medium.

Update:

```text
docs/TECH_DEBT_TRACKER.md
```

Add or update entries for:

```text
repository slug still historical
formal schemas missing for new AI orchestration reports
NPU smoke passes but NPU general advisory promotion still pending
active execution plans need reconciliation
ignored output reports require compact evidence bundle workflow
```

## Guardrails

Do not do these in Codex unless explicitly instructed:

```text
no Blender runtime edits
no Ready To Jazz work
no broad blender_compat adoption
no full analysis JSON edits
no legacy output edits
no generated index manual edits
no implicit provider execution
no model/temperature/prompt prose/provider orchestration legacy changes
no OpenVINO GPU primary lane
no repository rename without confirmation
```

## Safe files to edit next

Recommended safe targets:

```text
docs/JSON_SCHEMAS.md
docs/AI_ARTIFACT_SCHEMAS.md
Tools/validation/README.md
Tools/validation/check_github_evidence_bundle.py
docs/TECH_DEBT_TRACKER.md
docs/EXECUTION_PLANS/active/*.md
```

Avoid runtime/application targets:

```text
Scripting/
Scripting/v61b/
Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/
full analysis JSON files
indexAI/ generated indexes unless regenerated by tools
```

## Expected Codex output format

For the next PR, include:

```text
scope
files changed
provider execution mode
validation commands run
local evidence path if generated
line counts for created/modified scripts
risks
follow-up recommendations
```

## Recommended next PR title

```text
Add schema and validation contracts for AI orchestration evidence
```

## Recommended next branch name

```text
ai/evidence-schema-contracts
```

## Success condition for next PR

A good next PR should:

```text
not touch Blender runtime
not change provider behavior
document report schemas
add a non-invasive evidence bundle validator
run successfully on existing evidence bundles
produce or reference a compact evidence bundle
```
