# IA-Carmine task — fix final runtime broker telemetry

Repository: `C-F-tek/blender-audio-project`

Branch: `codex/unified-local-ai-refactor-launcher`

Evidence run: `20260505-002508`

Evidence commit: `469722a test(ai): add post-broker full-run production evidence`

Code fix commit:

    a85bbf4 fix(ai): preserve broker report in final runtime telemetry

Current status:

    CODE_PATCH_PUSHED
    RUNTIME_VALIDATION_PENDING

Follow-up doc:

    docs/LOCAL_AI_TASKS/post-broker-runtime-telemetry-followup-2026-05-05.md

## Objective

Implement and validate a focused code patch so the final Git-trackable runtime usage telemetry includes broker-executed report-only tool calls.

Historical failed acceptance from pre-fix run `20260505-002508`:

    docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_usage_telemetry_20260505-002508.json
      inputs.broker_reports = []
      summary.tool_call_entry_count = 1
      summary.executed_count = 0
      summary.runtime_tool_request_count = 44
      summary.runtime_tool_execution_count = 0
      summary.declared_not_executed_count = 44

But the same run produced a broker report:

    output/validation/runtime_tool_broker_full_toolbox_20260505-002508.json

and the shared bundle listed it as present and passed.

Important:

    Do not use `20260505-002508` to validate commit `a85bbf4`.
    That run is older than the fix.
    Validation requires a new run after `a85bbf4`.

## Patch implemented

Commit:

    a85bbf4 fix(ai): preserve broker report in final runtime telemetry

Changed files:

    Tools/ai/build_runtime_tool_usage_telemetry.py
    Tools/workflow/run_agent_review_full_toolbox_decision_loop.ps1

Implemented behavior:

    - `build_runtime_tool_usage_telemetry.py` now discovers the conventional broker report path:
      `output/validation/runtime_tool_broker_full_toolbox_<STAMP>.json`
      when it exists and the caller omitted `--broker-report`.

    - `run_agent_review_full_toolbox_decision_loop.ps1` now passes:
      `--broker-report $RuntimeToolBrokerJson`
      in the runtime telemetry generation call.

Fallback guarantee:

    If a later/final telemetry generation path forgets `--broker-report`, the Python builder should still include the conventional broker report if present.

## Scope

Patched:

    Tools/workflow/run_agent_review_full_toolbox_decision_loop.ps1
    Tools/ai/build_runtime_tool_usage_telemetry.py

Inspected but not changed by patch script:

    Tools/workflow/run_unified_local_ai_refactor.ps1

Do not change provider execution semantics in this follow-up unless the new validation run proves the same path is still responsible.

Do not change patch-plan generation, deterministic recommendations, or repository consistency filtering in the broker telemetry validation patch.

## Pre-run sync

Before validating locally:

    git switch codex/unified-local-ai-refactor-launcher
    git fetch origin
    git pull --ff-only origin codex/unified-local-ai-refactor-launcher
    git log --oneline -5

Expected latest relevant commit:

    a85bbf4 fix(ai): preserve broker report in final runtime telemetry

## Static validation commands

Python syntax:

    python -m py_compile `
      .\Tools\ai\build_runtime_tool_usage_telemetry.py `
      .\Tools\ai\agent_runtime_tool_broker.py

PowerShell parser:

    powershell -NoProfile -ExecutionPolicy Bypass -Command '$p=(Resolve-Path ".\Tools\workflow\run_agent_review_full_toolbox_decision_loop.ps1").Path; $t=$null; $e=$null; [System.Management.Automation.Language.Parser]::ParseFile($p,[ref]$t,[ref]$e)|Out-Null; $e'

    powershell -NoProfile -ExecutionPolicy Bypass -Command '$p=(Resolve-Path ".\Tools\workflow\run_unified_local_ai_refactor.ps1").Path; $t=$null; $e=$null; [System.Management.Automation.Language.Parser]::ParseFile($p,[ref]$t,[ref]$e)|Out-Null; $e'

Diff hygiene:

    git diff --check

## Runtime validation command family

Use a new stamp after `a85bbf4`:

    $Stamp = Get-Date -Format "yyyyMMdd-HHmmss"
    $TaskFile = ".\docs\LOCAL_AI_TASKS\fix-final-runtime-broker-telemetry-task-2026-05-05.md"

    $OutputDir = ".\output"
    $EvidenceDir = ".\docs\LOCAL_VALIDATION_EVIDENCE"
    $AiPacketsRoot = Join-Path $OutputDir "ai_packets"
    $AiPacketsDir = Join-Path $AiPacketsRoot $Stamp

Then run a short validation:

    powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Tools\workflow\run_unified_local_ai_refactor.ps1 `
      -Mode all `
      -Full0To10 `
      -SkipGitSync `
      -NoBranch `
      -Stamp $Stamp `
      -TaskFile $TaskFile `
      -OutputDir $OutputDir `
      -EvidenceDir $EvidenceDir `
      -AiPacketsRoot $AiPacketsRoot `
      -AiPacketsDir $AiPacketsDir `
      -Profile core `
      -RunIntensity custom `
      -BudgetMinutes 5 `
      -MaxRounds 30 `
      -FilesPerRound 8 `
      -MaxContextFiles 220 `
      -MaxCharsPerFile 8000 `
      -MaxNewTokens 3600 `
      -KeepAlive 35m `
      -NpuAuditorEveryRounds 3 `
      -NpuAuditorTimeoutSeconds 420 `
      -NpuMaxContextChars 8000 `
      -NpuMaxPromptChars 1200 `
      -NpuMaxNewTokens 384 `
      -NpuFinalWaitSeconds 180 `
      -MinRecommendations 1 `
      -MinPatchPlans 1 `
      -MaxRecommendations 40 `
      -MaxPatchPlans 40 `
      -RepositoryConsistencyMapWorkers 8 `
      -ContextPackMaxTotalChars 64000 `
      -ContextPackMaxFileChars 4000 `
      -AgentStateMaxMemoryChars 24000 `
      -MatrixWorkers 12 `
      -RepeatCases 2

## Acceptance criteria

After a new full run or focused full-toolbox decision loop run:

    docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_usage_telemetry_<STAMP>.json

must show:

    inputs.broker_reports.Count >= 1
    summary.tool_call_entry_count >= 3
    summary.executed_count >= 3
    summary.failed_count = 0
    summary.blocked_count = 0

Expected broker-executed tools:

    check_python_syntax
    build_python_line_count_csv
    check_validation_report_contract

The final telemetry may still include declared GPU planner counters. That is acceptable only if broker-executed entries are also present.

PowerShell check:

    $S = $Stamp
    $rtPath = ".\docs\LOCAL_VALIDATION_EVIDENCE\runtime_tool_usage_telemetry_${S}.json"
    Test-Path $rtPath
    $rt = Get-Content $rtPath -Raw | ConvertFrom-Json
    $rt.inputs.broker_reports
    $rt.summary
    $rt.tool_call_entries | Select-Object id, tool, caller, phase, executed, blocked, failed, returncode | Format-Table -AutoSize

Do not set:

    $S = "<STAMP>"

`<STAMP>` is a placeholder and is an invalid Windows path segment.

## Guardrails

No automatic patch application.
No provider execution during patch application.
No Blender runtime.
No FFmpeg.
No `output/**` commit.
No SQLite/DB commit.
No merge to master.
No force push.
No destructive operation.

## Proposal classification from `20260505-002508`

P0 — fix broker telemetry absorption:

    code patch pushed in a85bbf4; runtime validation pending.

P1 — investigate Ollama probe failure:

    separate diagnostic follow-up. Do not mix with broker telemetry unless proven same root cause.

P2 — filter patch-plan noise from archived evidence docs:

    future patch-plan quality improvement.

P2 — hardware/memory tuning:

    local operational tuning. NPU/GPU activation was visible, but RAM pressure was high.
