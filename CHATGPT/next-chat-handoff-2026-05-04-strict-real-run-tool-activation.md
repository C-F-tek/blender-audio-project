# Next chat handoff - strict real-run tool activation - 2026-05-04

## Repository state

Repository: `C-F-tek/blender-audio-project`

Branch: `codex/unified-local-ai-refactor-launcher`

Latest confirmed commits during this session:

```text
346ed6a docs(ai): repair datastamp procedure and patch delivery policy
3061356 fix(ai): accept timestamped ai packet folders in workload quality gate
5d0e56e docs(chatgpt): add AI session memory index
bc67cc7 docs(chatgpt): document robust chat recovery patterns
```

This file is expected to be followed by a commit adding this handoff file.

## User policy now clarified

User requirement:

```text
Every real run must activate all declared probes, tools, functions and lanes.
This applies to every real run, not only Full0To10.
```

Interpretation:

```text
A real run is any non-DryRun launcher execution that is not limited to smoke/reset planning.
Explicit -No* flags are the only acceptable way to disable a lane.
```

## What was fixed and validated

### AI packet directory contract

Old failure:

```text
PermissionError reading output/ai_packets/<Stamp> as file
```

Fixed:

```text
- output/ai_packets/<Stamp> is a directory, not a context file;
- concrete files inside it may be context/report inputs;
- workload quality accepts output/ai_packets root and scans timestamp child folders.
```

Validated by smoke:

```text
passed=True
quality_passed=True
selected_count=5
unselected_known_count=6
errors=0
warnings=0
```

Validated by full run context:

```text
output/ai_packets/20260504-224354/npu_real_workload_report.md
```

No more directory-as-file PermissionError.

### Telemetry in bundle

Telemetry files are included in evidence/chunks:

```text
full_toolbox_run_telemetry_summary_<Stamp>.json|md
runtime_tool_usage_telemetry_<Stamp>.json|md
runtime_tool_capability_manifest_<Stamp>.json|md
full_toolbox_<Stamp>_cloud_semantic_deterministic_chunks/*telemetry*
```

## Remaining blocker

Full run still completes the launcher but decision loop remains red:

```text
Passed: False
Recommendation count: 20
Patch plan count: 0
Fatal report failure count: 5
```

Observed recurring missing artifacts:

```text
output/ai_pipeline/full_toolbox_<Stamp>_parallel_gpu.json
output/ai_pipeline/agent_review_evidence_sufficiency.json
```

The issue is no longer `ai_packets` or telemetry. It is provider/evidence artifact production and strict lane activation.

## Patch bundle prepared but not yet applied at time of this handoff

Bundle name:

```text
ia_carmine_real_run_strict_tool_activation_bundle.zip
```

Purpose:

```text
- enforce strict activation for every real run;
- add -NoStrictRealRunActivation only for local maintenance/debug;
- pass RequireProviderArtifacts into the full-toolbox legacy wrapper;
- create schema-valid passed=false fallback artifacts when required provider artifacts are missing;
- avoid opaque missing-file cascades;
- keep runs red when providers fail, but produce complete diagnostic bundle.
```

Expected patched files:

```text
Tools/workflow/run_unified_local_ai_refactor.ps1
Tools/workflow/run_agent_review_full_toolbox_decision_loop.ps1
docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure.md
```

## Historical prepared bundle note

The previously referenced strict-activation ZIP was a local transient bundle, not a tracked repository command. Do not document an `output/validation/patch_bundles/**/run_patch_bundle.py` path as an executable project command.

Current rule:

```text
Recreate patch bundles from current tracked tooling when needed.
Keep transient bundle runners under output/** uncommitted.
Validate the tracked workflow files directly after any replacement.
```

Validation for tracked workflow files remains:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -Command "$p=(Resolve-Path '.\Tools\workflow\run_unified_local_ai_refactor.ps1').Path; $t=$null; $e=$null; [System.Management.Automation.Language.Parser]::ParseFile($p,[ref]$t,[ref]$e)|Out-Null; $e"

powershell -NoProfile -ExecutionPolicy Bypass -Command "$p=(Resolve-Path '.\Tools\workflow\run_agent_review_full_toolbox_decision_loop.ps1').Path; $t=$null; $e=$null; [System.Management.Automation.Language.Parser]::ParseFile($p,[ref]$t,[ref]$e)|Out-Null; $e"
```

## Before running again

Ensure working tree is clean:

```powershell
git status --short
```

If artifacts remain:

```powershell
git restore --staged -- `
  docs/LOCAL_VALIDATION_EVIDENCE `
  indexAI/code_chunks

git stash push -u -m "archive run artifacts before next strict real run" -- `
  docs/LOCAL_VALIDATION_EVIDENCE `
  indexAI/code_chunks
```

## Next full run intent

After applying strict activation patch and pushing it, run a real full run. Expected behavior:

```text
- all declared probes/tools/lanes are activated unless explicitly disabled;
- if provider/GPU/evidence artifacts are missing, schema-valid passed=false fallback files are produced;
- evidence bundle contains complete diagnostics instead of missing-file cascades;
- run may remain red if provider truly failed, but failure reason must be explicit and discoverable.
```

## Important local run command pattern

Use fresh stamp:

```powershell
$Stamp = Get-Date -Format "yyyyMMdd-HHmmss"
$DataStamp = $Stamp
$TaskFile = ".\docs\LOCAL_AI_TASKS\shared-runtime-toolbox-ai-to-ai-next-task-2026-05-03.md"
$ScriptPath = (Resolve-Path ".\Tools\workflow\run_unified_local_ai_refactor.ps1").Path
$AiPacketsRoot = ".\output\ai_packets"
$AiPacketsDir = Join-Path $AiPacketsRoot $DataStamp
New-Item -ItemType Directory -Force -Path $AiPacketsDir | Out-Null
```

Then full command with explicit `-AiPacketsRoot` and `-AiPacketsDir`.

## ChatGPT operational preference

For future large fixes:

```text
- prefer GitHub files or ZIP patch bundles;
- avoid huge inline chat scripts;
- use CHATGPT/*.md for small durable session notes;
- make notes discoverable to local AI and cloud AI by keeping them small and plainly named.
```
