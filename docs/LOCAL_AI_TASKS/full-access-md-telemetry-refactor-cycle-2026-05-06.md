# Full access Markdown telemetry refactor cycle - 2026-05-06

## Purpose

Use this Markdown file as the task input for a local full-access IA-Carmine run.

The run should produce enriched telemetry and compact evidence proving what the cycle generated:

```text
advisory packets
repository proposals
review-only patch specs
patch/spec validations
adapter/unified manifests
telemetry JSON/Markdown
compact evidence bundle
post-run validation summaries
```

The goal is to make the run debuggable by the next AI/human reviewer and to prove the proposed patches through bundle evidence, not through raw `output/**` commits.

## Access posture

Full access here means broad local repository access to existing project tools:

```text
Tools/ai/**
Tools/validation/**
Tools/workflow/**
Tools/npu/**
docs/LOCAL_AI_TASKS/**
docs/*AI*.md
docs/*WORKFLOW*.md
```

Provider execution is allowed only when the operator launches the command with explicit provider flags or `-Full0To10`.

The run may write runtime reports under `output/**` and compact evidence under `docs/LOCAL_VALIDATION_EVIDENCE/**`.

The run must not automatically apply patches.

## Suggested launch command

Run from the repository root in PowerShell.

This command intentionally selects `-Full0To10`, so provider probes/advisory, memory input persistence, patch-spec drafts, telemetry and compact evidence are explicitly in scope. It still must not apply patches automatically.

```powershell
$Stamp = Get-Date -Format "yyyyMMdd-HHmmss"
$Task = ".\docs\LOCAL_AI_TASKS\full-access-md-telemetry-refactor-cycle-2026-05-06.md"

powershell.exe -NoProfile -ExecutionPolicy Bypass -File ".\Tools\workflow\run_unified_local_ai_refactor.ps1" `
  -TaskFile $Task `
  -TaskBranch "codex/full-access-md-telemetry-$Stamp" `
  -Stamp "full_access_md_telemetry_$Stamp" `
  -Full0To10 `
  -RunIntensity balanced `
  -BuildEvidence `
  -GeneratePatchSpecs `
  -FullContextGoldenPath `
  -OutputDir ".\output" `
  -EvidenceDir ".\docs\LOCAL_VALIDATION_EVIDENCE"
```

If you want a provider-free rehearsal, add these explicit disablers:

```powershell
  -NoOllamaProbe `
  -NoNpuProbe `
  -NoNpuDecodeSmoke `
  -NoMultistepProvider `
  -NoWorkloadQuality
```

## Required guardrails

```text
patch_application_performed=false
source_writes_performed=false unless a later human-reviewed patch step is selected
provider_execution_requested must be visible in manifest/telemetry
provider_execution_performed must be visible in manifest/telemetry
Blender runtime execution=false
FFmpeg runtime execution=false
no merge to master
no force-push
no rewrite history
no delete unless an explicit reset command with confirmation is provided
no secrets, permissions, billing, visibility or deploy changes
no commit of output/**
no commit of indexAI/code_chunks/**
no commit of *.db, *.sqlite, *.sqlite3
no commit of renders/**
```

## Reuse-first rule

Before proposing a new script/tool, inspect and reuse existing surfaces:

```text
Tools/ai/build_shared_toolbox_ai_to_ai_bundle.py
Tools/ai/build_github_evidence_bundle.py
Tools/ai/build_refactor_duplication_audit.py
Tools/ai/build_repository_consistency_map.py
Tools/ai/build_code_interpreter_report.py
Tools/validation/check_local_ai_adapter_manifest.py
Tools/validation/check_github_evidence_bundle.py
Tools/validation/run_refactor_duplication_audit_smoke.py
Tools/validation/run_repository_consistency_map_smoke.py
Tools/workflow/run_unified_local_ai_refactor.ps1
Tools/workflow/run_local_ai_task_via_pipeline.ps1
Tools/workflow/run_local_ai_task_via_pipeline/*.ps1
Tools/workflow/run_ai_cycle_startup_preflight.ps1
Tools/npu/pipeline/**
```

If a new file is unavoidable, the run must explain why no existing builder, validator, helper or workflow module covers the case.

## Primary analysis goals

Analyze the whole local AI workbench for robust engineering refactor opportunities:

```text
encapsulation
shared helper extraction
superclass/base-class candidates
module/package boundaries
report and manifest common contracts
telemetry completeness
evidence bundle completeness
patch/spec/proposal flow robustness
provider diagnostics visibility
workflow startup/preflight resilience
Markdown input to bundle/evidence/telemetry reliability
```

Keep Blender/audio runtime behavior out of ordinary tool refactors unless a later task explicitly scopes runtime validation.

## Required outputs

The run is successful only if it produces inspectable outputs for the current stamp:

```text
unified launcher manifest
local AI adapter manifest when official phase runs
local AI adapter telemetry JSON/Markdown when official phase runs
advisory packet JSON/Markdown
repository proposals JSON/Markdown
repository proposal validation report
review-only patch-spec manifest JSON/Markdown
patch-spec validation report
compact evidence bundle JSON/Markdown
evidence bundle validation report
AI-to-AI or shared toolbox final summary when available
runtime/tool/provider telemetry summaries when available
capability/hardware manifest when available
OpenVINO hardware governance report when provider lanes are in scope
startup/preflight report
```

The evidence bundle should include enough telemetry and report summaries to prove:

```text
which proposals were generated
which patch specs were generated
which validators passed
which guardrails remained false
which provider lanes were requested/performed/degraded
which outputs are expected for follow-up review
```

## Patch/spec/proposal rules

Patch/spec/proposal generation is allowed only as manual-review output.

Required classifications:

```text
SAFE_MECHANICAL
MANUAL_REVIEW
LOCAL_VALIDATION_REQUIRED
BLENDER_RUNTIME_REQUIRED
PROVIDER_VALIDATION_REQUIRED
DEFER
DO_NOT_PROMOTE
```

Patch targets must not include ordinary edits under:

```text
output/**
indexAI/code_chunks/**
docs/LOCAL_VALIDATION_EVIDENCE/**
renders/**
*.db
*.sqlite
*.sqlite3
```

Compact evidence under `docs/LOCAL_VALIDATION_EVIDENCE/**` may be committed only as selected proof of a run, not as normal source documentation.

## Stop conditions

Stop and report instead of continuing if:

```text
a needed tool already exists and the run is about to create a duplicate
a provider would run without explicit Full0To10/provider flags
a patch would be applied automatically
a change would require Blender or FFmpeg runtime validation
a generated DB, raw output, render, or code chunk would be staged
a file would exceed the 400-line policy without a split plan
```

## Post-run handling

After the run:

```text
read the unified launcher manifest first
inspect adapter telemetry and evidence validation
inspect proposals and patch specs before applying anything
select a small patch subset manually
commit source/docs patches separately from raw runtime outputs
commit compact evidence only when it proves the reviewed run
push to a review branch and open/update a draft PR
```
