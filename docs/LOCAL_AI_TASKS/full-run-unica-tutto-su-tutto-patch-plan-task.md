# IA-Carmine task — patch plan for FULL RUN UNICA / TUTTO SU TUTTO

## Repository

```text
C-F-tek/blender-audio-project
```

## Branch

```text
codex/unified-local-ai-refactor-launcher
```

## Objective

Generate a review-only patch plan for aligning the canonical IA-Carmine full run to the current policy:

```text
FULL RUN UNICA = TUTTO SU TUTTO
```

The output must be recommendations and patch-plan artifacts only. Do not apply source patches automatically.

## Current user decision

The previous conservative policy is no longer valid for canonical full runs.

Canonical full run policy:

```text
TUTTO SU TUTTO
all declared runtime/tool/provider/advisory/evidence/patch-spec/memory lanes active
```

Do not use a reduced/minimal command as the canonical full run. The canonical procedure must provide a long single PowerShell script with variables for input/output/runtime knobs.

## Required scope to analyze

Inspect at least:

```text
Tools/workflow/run_unified_local_ai_refactor.ps1
Tools/workflow/run_agent_review_full_toolbox_decision_loop_integrated.ps1
Tools/workflow/run_agent_review_full_toolbox_decision_loop.ps1
docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure.md
CHATGPT/README.md
CHATGPT/chatgpt-session-problems-and-robust-fixes-2026-05-04.md
CHATGPT/next-chat-handoff-2026-05-04-strict-real-run-tool-activation.md
```

## Required patch-plan themes

### 1. Launcher parameterization

Evaluate adding top-level parameters to `Tools/workflow/run_unified_local_ai_refactor.ps1`:

```powershell
[string]$OutputRoot = "output"
[string]$EvidenceDir = "docs/LOCAL_VALIDATION_EVIDENCE"
```

The patch plan should determine all needed wiring, especially:

```text
- deriving output/validation, output/ai_pipeline, output/analysis, output/patch_specs, output/local_ai_runs from OutputRoot where appropriate
- keeping AiPacketsRoot/AiPacketsDir compatible with OutputRoot
- passing OutputRoot and EvidenceDir into run_agent_review_full_toolbox_decision_loop_integrated.ps1
- preserving backward compatibility with default paths
```

### 2. Strict real-run all-lanes activation

The canonical full run must activate all lanes unless an explicit maintenance/debug `-No*` flag disables a lane.

Evaluate whether strict real-run activation should enable:

```text
RunOllamaProbe
RunNpuProbe
RunNpuDecodeSmoke
RunMultistepProviderWorkflow
BuildWorkloadQualityReport
BuildEvidence
GeneratePatchSpecs
UseOllamaAdvisory
UsePrimaryAdvisoryProvider
RunLegacyFullToolboxIntegrated
SaveInputsToMemoryDb / memory lane where supported
RequireProviderArtifacts through integrated/base workflow
```

### 3. Procedure documentation

Update the patch plan for `docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure.md` without deleting the long manual/expanded procedure.

Required documentation result:

```text
- keep the expanded/manual 0 -> 10 procedure as deep/debug reference
- add or update a canonical section: FULL SCRIPT UNICO — TUTTO SU TUTTO
- include variables at the top for input dirs, output dirs, evidence dir, AI packet dir, patch-bundle dir, task file and stamp
- include full runtime knobs as variables, not magic literals scattered in command lines
- make clear that canonical full run uses -Mode all + -Full0To10 and no -No* flags
- remove or supersede old read-only/conservative memory wording for canonical full runs
```

### 4. Guardrails that remain valid

Do not confuse runtime lane activation with destructive Git/ops actions.

Even under `TUTTO SU TUTTO`, these still require explicit separate command:

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

Patch application must remain explicit:

```text
recommendation -> patch plan -> patch bundle -> explicit apply -> validation -> PR
```

### 5. Validation requirements

Patch plan must include validation commands for any proposed patch:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -Command '$p=(Resolve-Path ".\Tools\workflow\run_unified_local_ai_refactor.ps1").Path; $t=$null; $e=$null; [System.Management.Automation.Language.Parser]::ParseFile($p,[ref]$t,[ref]$e)|Out-Null; $e'

powershell -NoProfile -ExecutionPolicy Bypass -Command '$p=(Resolve-Path ".\Tools\workflow\run_agent_review_full_toolbox_decision_loop_integrated.ps1").Path; $t=$null; $e=$null; [System.Management.Automation.Language.Parser]::ParseFile($p,[ref]$t,[ref]$e)|Out-Null; $e'

powershell -NoProfile -ExecutionPolicy Bypass -Command '$p=(Resolve-Path ".\Tools\workflow\run_agent_review_full_toolbox_decision_loop.ps1").Path; $t=$null; $e=$null; [System.Management.Automation.Language.Parser]::ParseFile($p,[ref]$t,[ref]$e)|Out-Null; $e'

git diff --check

python .\Tools\validation\check_python_syntax.py --repo-root . --output .\output\validation\python_syntax_after_full_run_policy_patch_plan.json
```

## Expected output from the local AI run

The run should produce:

```text
- diagnostics/evidence
- deterministic recommendations
- agent review decision loop report
- patch plan JSON/MD
- compact evidence bundle
- runtime telemetry/capability evidence where supported
```

Expected patch plan should be review-only and should target only source/docs files, likely:

```text
Tools/workflow/run_unified_local_ai_refactor.ps1
docs/LOCAL_AI_TASKS/full-toolbox-0-to-10-semi-automatic-procedure.md
```

Potentially also target integration/base workflow only if evidence shows more wiring is required:

```text
Tools/workflow/run_agent_review_full_toolbox_decision_loop_integrated.ps1
Tools/workflow/run_agent_review_full_toolbox_decision_loop.ps1
```

## Non-goals

Do not apply source changes automatically.
Do not create/delete branches automatically.
Do not merge.
Do not run Blender.
Do not run FFmpeg.
Do not commit output/**.
Do not commit patch bundles.
Do not rewrite history.

## Git policy

Commit only the task file and later, after explicit review, source/docs changes and compact evidence explicitly selected.

Never commit:

```text
output/**
output/validation/patch_bundles/**
renders/**
*.db
*.sqlite
*.sqlite3
```
