# Unified launcher parameter decision map — 2026-05-09

Status: active code-derived operator guide  
Scope: `Tools/workflow/run_unified_local_ai_refactor.ps1`.

This guide prevents agents from getting lost in the launcher parameter surface. Do not reason from the full parameter list. Choose the product lane first, then tune only the related parameter group.

## Source of truth

```text
AGENTS.md
docs/UNIFIED_LOCAL_AI_LAUNCHER_CONTRACT.md/
docs/LOCAL_AI_TASKS/code-derived-ai-toolchain-map-2026-05-07.md
docs/LOCAL_AI_TASKS/runtime-hardening-current-state-2026-05-08.md
Tools/workflow/run_unified_local_ai_refactor.ps1
Tools/workflow/python_env.ps1
Tools/workflow/unified_run_observer.ps1
```

Historical handoffs and old PR bodies are secondary. Current code and current contract docs win.

## First decision

| Intent | Use | Avoid |
|---|---|---|
| Fast syntax/config sanity | `-Mode smoke -DryRun` | `-Full0To10` |
| Debug one phase | `-Mode <phase> -NoStrictRealRunActivation` | implicit real-run activation |
| Full Markdown-to-review workflow | `-Full0To10` with task Markdown | hidden helper-only entrypoints |
| Evidence-only lightweight check | `-LightFull0To10` | provider success claims |
| Markdown/doc inventory | `-Mode md -NoStrictRealRunActivation` | provider switches |
| Python/script inventory | `-Mode python -NoStrictRealRunActivation` | patch apply |
| Provider advisory run | Full0To10 or explicit provider lane after Python preflight | system Python |
| Deterministic suggestion apply | review branch and review-PR controls | patch specs as auto-apply |
| Long-run observation | observer/watch scripts | silent waiting |

## Parameter control hierarchy

Use this order:

```text
repository and Python controls
run identity controls
mode/profile/intensity controls
strict activation controls
phase budget controls
provider controls
NPU micro controls
observer/evidence controls
product/review PR controls
reset controls
```

## Repository and Python controls

Normal real-run baseline:

```powershell
-RepoRoot .
-PythonExe .\.venv\Scripts\python.exe
$env:IA_CARMINE_PYTHON = (Resolve-Path .\.venv\Scripts\python.exe).Path
$env:PYTHONPATH = (Resolve-Path .).Path
```

Current policy: workflow/provider lanes must use a repository-owned Python executable. Bare `python`, WindowsApps Python and non-repository interpreters are invalid for provider/workflow lanes.

Provider preflight:

```powershell
& $env:IA_CARMINE_PYTHON -c "import sys; print(sys.executable); import numpy, openvino; from openvino import Core; c=Core(); print(c.available_devices)"
```

Expected workstation visibility:

```text
CPU, GPU.0, GPU.1, NPU
```

If `numpy`, `openvino` or `openvino-genai` is missing, classify the failure as `provider_python_environment_missing_dependency`, not GPU0/NPU failure.

## Run identity controls

```text
-Stamp
-TaskFile
-TaskBranch
-OutputDir
-EvidenceDir
-AiPacketsRoot
-AiPacketsDir
```

Rules:

```text
Use a unique Stamp for real runs.
TaskFile is the product input.
OutputDir stays local/ignored.
EvidenceDir is only for compact Git-trackable summaries.
AiPacketsRoot/AiPacketsDir route handoff packets, not source.
```

## Mode controls

Common modes:

```text
smoke
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

For diagnostics, always pair a single phase with:

```text
-NoStrictRealRunActivation
```

Without that flag, non-smoke/non-reset real runs can be promoted into TUTTO SU TUTTO.

## Full0To10 versus RunIntensity

`-Full0To10` means full semantic perimeter: all major phases unless an explicit `-No*` flag disables a lane or evidence classifies it unavailable/degraded.

`-RunIntensity` changes capacity, not scope:

```text
quick    = smaller budget/context/token envelope
balanced = default envelope
deep     = larger envelope
custom   = operator-supplied envelope
```

`quick` is not smoke. Use `-Mode smoke` for smoke.

## Budget controls

Tune these only after selecting the lane:

```text
-BudgetMinutes
-MaxRounds
-FilesPerRound
-MaxContextFiles
-MaxCharsPerFile
-MaxNewTokens
-KeepAlive
```

Guidance:

```text
Use small budgets for reproducing a fault.
Use balanced defaults for normal review.
Use deep/custom only when evidence says context was insufficient.
Do not increase budgets to hide missing inputs or provider failures.
```

## Context and memory controls

```text
-ContextPackMaxTotalChars
-ContextPackMaxFileChars
-AgentStateMaxMemoryChars
-MaxContextChars
-NoMemoryWrite
-SaveInputsToMemoryDb
-MemoryDb
```

Policy:

```text
SQLite memory is local/private runtime state.
Never commit DB files.
Context pack output is evidence/input, not source authority.
Memory write is appropriate only when continuity evidence is part of the task.
```

## Provider controls

Main provider switches:

```text
-UseOllamaAdvisory
-UsePrimaryAdvisoryProvider
-RunMultistepProviderWorkflow
-RunLegacyFullToolboxIntegrated
-RunLegacyNpuAuditorProvider
-RunOllamaProbe
-RunNpuProbe
-RunNpuDecodeSmoke
-NoOllamaProbe
-NoNpuProbe
-NoNpuDecodeSmoke
-NoMultistepProvider
-NoWorkloadQuality
-ProviderMaxContextChars
```

Current role model:

```text
GPU1/Ollama = primary advisory planner/worker.
GPU0/OpenVINO = peer companion/helper and tool-request producer.
NPU/OpenVINO = non-blocking microtask/tool-support lane.
CPU validators = pass/fail authority.
```

Use `RunLegacyNpuAuditorProvider` only for explicit legacy diagnostics. The preferred NPU role is micro support, not heavy audit authority.

## NPU micro controls

```text
-NpuMicroStartMode startup|deferred|live-seed-only|peer|post-gpu-provider|disabled
```

| Mode | Use |
|---|---|
| `deferred` | normal safe default |
| `startup` | early NPU visibility |
| `live-seed-only` | seed/diagnostic evidence only |
| `peer` | GPU peer-exchange support |
| `post-gpu-provider` | NPU support after GPU output exists |
| `disabled` | isolate GPU/Ollama/Python issues |

NPU degraded/skipped/blocked state must be visible in telemetry or reports.

## Observer controls

Current observer surfaces:

```text
Tools/workflow/unified_run_observer.ps1
Tools/workflow/watch_unified_run_telemetry.ps1
Tools/workflow/watch_unified_ai_conversation.ps1
Tools/workflow/watch_unified_raw_debug_good_info.ps1
```

Observer output improves visibility. It does not prove provider execution, patch application or product success.

Use `-Prod` or `-NoExecutionTail` only when less transcript/tail evidence is intentional.

## Patch and product controls

Patch-spec controls:

```text
-GeneratePatchSpecs
-BuildEvidence
-NoPatchSpecs
-NoEvidence
```

Review/product controls:

```text
-ReviewPrApplyDeterministicSuggestions
-BuildTaskPatchSuggestionReport
-PrepareReviewPr
-ReviewPrBranch
-ReviewPrBaseBranch
-ReviewPrRemote
-ReviewPrTitle
-ReviewPrCommitMessage
-ReviewPrIncludePath
-ReviewPrPush
-ReviewPrCreate
```

Policy:

```text
No patch apply by default.
No commit, push or PR by default.
Review PR staging must be allowlisted or derived from a safe apply report.
No merge to master from launcher.
Never stage output/**, DB, render, generated chunk or raw runtime artifacts.
```

Draft PR creation is canonical only if the active branch's `prepare_review_pr.py` exposes and validates an explicit draft flag.

## Reset controls

Reset is plan-first:

```text
-Mode reset
-ResetBeforeDate
-IncludeMemoryReset
-IncludeGeneratedIndexReset
```

Real deletion additionally requires:

```text
-ApplyReset
-ConfirmResetText "DELETE LOCAL AI ARTIFACTS"
```

Never use reset to clean source files.

## Safe command templates

Smoke dry-run:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass `
  -File .\Tools\workflow\run_unified_local_ai_refactor.ps1 `
  -RepoRoot . -Mode smoke -SkipGitSync -AllowDirty -DryRun -Prod `
  -NoOllamaProbe -NoNpuProbe -NoNpuDecodeSmoke -NoMultistepProvider -NoWorkloadQuality
```

Single-phase diagnostic:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass `
  -File .\Tools\workflow\run_unified_local_ai_refactor.ps1 `
  -RepoRoot . -Mode official -TaskFile .\docs\LOCAL_AI_TASKS\<task>.md `
  -Stamp diag_<stamp> -SkipGitSync -NoBranch -AllowDirty `
  -NoStrictRealRunActivation -Prod -NoExecutionTail
```

Full product shape:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass `
  -File .\Tools\workflow\run_unified_local_ai_refactor.ps1 `
  -RepoRoot . -TaskFile .\docs\LOCAL_AI_TASKS\<task>.md -Stamp <stamp> `
  -Full0To10 -RunIntensity balanced `
  -UseOllamaAdvisory -UsePrimaryAdvisoryProvider -RunMultistepProviderWorkflow `
  -BuildEvidence -GeneratePatchSpecs
```

## Anti-patterns

```text
Running -Mode md without -NoStrictRealRunActivation during diagnostics.
Treating LightFull0To10 as proof of provider execution.
Using system Python for provider lanes.
Increasing budgets before fixing missing inputs.
Promoting NPU to primary/heavy auditor by default.
Using patch specs as automatic apply input.
Staging output/** or generated chunks.
Assuming historical docs override current code.
```

## Minimal handoff for another AI

Provide:

```text
current branch and PR
exact launcher command
Stamp and TaskFile
selected Mode or Full0To10
whether NoStrictRealRunActivation was used
selected PythonExe / IA_CARMINE_PYTHON
manifest path
observer/current_state path for long runs
phase_status and phase_reports summary
first failing report path
git status --short
```

This is enough to prevent the next AI from getting lost in the parameter surface.
